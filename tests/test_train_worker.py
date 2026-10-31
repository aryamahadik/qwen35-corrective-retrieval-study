"""Offline tests: preparation gates and padding; no torch/model/network imports."""
import copy
import ast
import contextlib
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import types
import unittest


WORKER_PATH = Path(__file__).resolve().parents[1] / "train_worker.py"
SPEC = importlib.util.spec_from_file_location("isolated_train_worker", WORKER_PATH)
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)


class PreparedGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.config = worker.load_config()
        # Keep the fixture small while exercising the same expected-ID contract.
        self.config["expected_training_tasks"] = 2
        self.rows = [
            {"source_task_id": "fixture-a", "input_ids": [1, 2, 3, 4], "labels": [-100, -100, 3, 4]},
            {"source_task_id": "fixture-b", "input_ids": [1, 5, 6], "labels": [-100, -100, 6]},
        ]
        self.data_path = self.directory / "train.tokens.jsonl"
        self.manifest_path = self.directory / "prepared_manifest.json"
        self.template_path = self.directory / "training_chat_template.jinja"
        self.template_path.write_text("{% generation %}fixture{% endgeneration %}")
        self.split_path = self.directory / "split_manifest.json"
        self.split_path.write_text(json.dumps({"task_ids": {"train": ["fixture-a", "fixture-b"]}}))
        self.config["split_manifest_sha256"] = worker.file_sha256(self.split_path)
        self.manifest = {
            "schema_version": 1, "status": "READY_FOR_TRAINING", "ready": True,
            "model_id": worker.MODEL_ID, "model_revision": worker.MODEL_REVISION,
            "tokenizer_revision": worker.MODEL_REVISION, "max_seq_length": self.config["max_seq_length"],
            "train_file": self.data_path.name, "split_manifest_sha256": self.config["split_manifest_sha256"],
            "source_traces_sha256": "b" * 64,
            "chat_template_file": self.template_path.name,
            "chat_template_sha256": worker.file_sha256(self.template_path),
            "training_task_ids": ["fixture-a", "fixture-b"], "task_count": 2,
            "row_count": 2, "total_tokens": 7, "supervised_tokens": 3,
            "versions": {key: self.config["required_versions"][key]
                         for key in ["transformers", "tokenizers", "jinja2"]},
            "review_receipts": {"fixture-a": {"fixture": True}, "fixture-b": {"fixture": True}},
        }
        self.write_fixture()

    def write_fixture(self):
        self.data_path.write_text("".join(json.dumps(row) + "\n" for row in self.rows))
        self.manifest["train_file_sha256"] = worker.file_sha256(self.data_path)
        self.manifest_path.write_text(json.dumps(self.manifest))

    def validate(self):
        return worker.validate_prepared_data(
            self.data_path, self.manifest_path, self.config, frozen_split_manifest_path=self.split_path)

    def test_valid_fixture_strips_task_metadata_and_reports_counts(self):
        rows, _, _ = self.validate()
        self.assertEqual(set(rows[0]), {"input_ids", "labels"})
        summary = worker.validate_prepared_dataset(
            self.data_path, self.manifest_path, self.config, frozen_split_manifest_path=self.split_path)
        self.assertEqual(summary["supervised_tokens"], 3)
        self.assertNotIn("input_ids", summary)

    def test_raw_task_specs_rejected_before_gpu_import(self):
        self.rows[0] = {"task_id": "fixture-a", "user_prompt": "not a demonstration", "verifiers": []}
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "only prepared token"):
            self.validate()

    def test_source_release_not_ready_rejected(self):
        self.manifest["ready"] = False
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "not ready"):
            self.validate()

    def test_tampered_tokens_rejected_by_hash(self):
        self.data_path.write_text(self.data_path.read_text() + "\n")
        with self.assertRaisesRegex(worker.TrainingGateError, "hash mismatch"):
            self.validate()

    def test_zero_targets_rejected(self):
        self.rows[0]["labels"] = [-100] * 4
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "targets nonempty"):
            self.validate()

    def test_shifted_first_label_cannot_corrupt_denominator(self):
        self.rows[0]["labels"][0] = 1
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "first token"):
            self.validate()

    def test_duplicate_source_task_rejected(self):
        self.rows[1]["source_task_id"] = "fixture-a"
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "one full trajectory"):
            self.validate()

    def test_unmatched_prediction_label_rejected(self):
        self.rows[0]["labels"][2] = 999
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "copy tokens"):
            self.validate()

    def test_wrong_tokenizer_environment_rejected(self):
        self.manifest["versions"]["transformers"] = "4.57.6"
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "pinned transformers"):
            self.validate()

    def test_missing_review_receipt_rejected(self):
        del self.manifest["review_receipts"]["fixture-b"]
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "review receipt"):
            self.validate()

    def test_self_consistent_foreign_task_ids_still_rejected(self):
        self.rows[1]["source_task_id"] = "heldout-task"
        self.manifest["training_task_ids"] = ["fixture-a", "heldout-task"]
        self.manifest["review_receipts"] = {"fixture-a": {"fixture": True}, "heldout-task": {"fixture": True}}
        self.write_fixture()
        with self.assertRaisesRegex(worker.TrainingGateError, "frozen training membership"):
            self.validate()

    def test_padding_never_supervises_padding_or_discards_labels(self):
        original = copy.deepcopy(self.rows)
        batch = worker.padded_batch(self.rows, 0)
        self.assertEqual(batch["labels"], [[-100, -100, 3, 4], [-100, -100, 6, -100]])
        self.assertEqual(batch["attention_mask"], [[1, 1, 1, 1], [1, 1, 1, 0]])
        self.assertEqual(batch["input_ids"][1], [1, 5, 6, 0])
        self.assertEqual(self.rows, original)

    def test_partial_checkpoint_rejected(self):
        checkpoint = self.directory / "checkpoint-1"
        checkpoint.mkdir()
        (checkpoint / "adapter_model.safetensors").write_bytes(b"fixture")
        with self.assertRaisesRegex(worker.TrainingGateError, "complete optimizer"):
            worker.validate_checkpoint(checkpoint)

    def test_published_checkpoint_is_not_rewritten_and_identity_is_portable(self):
        checkpoint = self.directory / "checkpoint-1"
        checkpoint.mkdir()
        for name in ("optimizer.pt", "scheduler.pt", "rng_state.pth", "adapter_model.safetensors"):
            (checkpoint / name).write_bytes(b"fixture-not-real-model-state")
        (checkpoint / "adapter_config.json").write_text("{}")
        (checkpoint / "trainer_state.json").write_text(json.dumps({"global_step": 1}))
        calls = []
        def save_tokenizer(path):
            calls.append(path)
            (Path(path) / "tokenizer_config.json").write_text('{"fixture": true}')
        identity = {"model_id": worker.MODEL_ID, "fixture": True}
        self.assertTrue(worker.finalize_checkpoint_payload(checkpoint, identity, save_tokenizer))
        spec = importlib.util.spec_from_file_location("fixture_checkpoint_utils", WORKER_PATH.parent / "checkpoint_utils.py")
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        metadata = {
            "model_id": worker.MODEL_ID, "model_revision": worker.MODEL_REVISION,
            "split_manifest_sha256": "a" * 64, "training_dataset_sha256": "b" * 64,
            "chat_template_sha256": "c" * 64,
        }
        helper.publish_checkpoint(checkpoint, metadata)
        before = {p.name: worker.file_sha256(p) for p in checkpoint.iterdir()}
        self.assertFalse(worker.finalize_checkpoint_payload(checkpoint, identity, save_tokenizer))
        self.assertEqual(before, {p.name: worker.file_sha256(p) for p in checkpoint.iterdir()})
        self.assertEqual(len(calls), 1)
        self.assertEqual(worker.portable_checkpoint_identity(checkpoint), identity)


class AccumulationMathTests(unittest.TestCase):
    def test_real_trainer_methods_weight_tokens_and_cancel_accelerator_extra_division(self):
        # Execute the worker's actual nested class against a tiny numerical fake.
        # This checks integration math without importing torch or allocating a GPU.
        class Scalar:
            def __init__(self, value): self.value = value
            def item(self): return self.value
            def numel(self): return 1
            def detach(self): return self
            def to(self, _): return self
            device = "fixture"
            def __mul__(self, other): return Scalar(self.value * (other.value if isinstance(other, Scalar) else other))
            def __truediv__(self, other): return Scalar(self.value / (other.value if isinstance(other, Scalar) else other))

        class Labels:
            def __init__(self, values): self.values = values
            def __getitem__(self, index): return Labels([row[index[1]] for row in self.values])
            def ne(self, value): return Labels([[x != value for x in row] for row in self.values])
            def sum(self): return Scalar(sum(sum(row) for row in self.values))

        class Accelerator:
            num_processes, scaler, gradient_accumulation_steps = 1, None, 8
            def __init__(self): self.backward_total = 0.0
            def backward(self, loss):
                # Exact pinned Accelerator1.12 non-DeepSpeed normalization.
                self.backward_total += loss.value / self.gradient_accumulation_steps

        class FakeTrainer:
            def __init__(self): self.accelerator = Accelerator()
            def _prepare_inputs(self, inputs): return inputs
            def compute_loss_context_manager(self): return contextlib.nullcontext()

        class Model:
            training = True
            def train(self): self.training = True
            def __call__(self, **inputs):
                return types.SimpleNamespace(loss=Scalar(inputs["fixture_mean_loss"]), logits=None)

        source = ast.parse(WORKER_PATH.read_text())
        trainer_class = next(n for n in ast.walk(source)
                             if isinstance(n, ast.ClassDef) and n.name == "TokenWeightedTrainer")
        namespace = {
            "Trainer": FakeTrainer, "TrainingGateError": worker.TrainingGateError,
            "torch": types.SimpleNamespace(Tensor=Scalar, isfinite=lambda x: Scalar(math.isfinite(x.value))),
        }
        exec(compile(ast.fix_missing_locations(ast.Module(body=[trainer_class], type_ignores=[])),
                     "actual_nested_worker_trainer", "exec"), namespace)
        trainer = namespace["TokenWeightedTrainer"]()
        batches = [
            {"labels": Labels([[-100, 3, 4]]), "attention_mask": Labels([[1, 1, 1]]), "fixture_mean_loss": 2},
            {"labels": Labels([[-100, 6]]), "attention_mask": Labels([[1, 1]]), "fixture_mean_loss": 8},
        ]
        samples, target_count = trainer.get_batch_samples(iter(batches), 8, "fixture")
        self.assertEqual(target_count, 3)  # partial final accumulation group: 2/8 microbatches
        logged = sum(trainer.training_step(Model(), b, target_count).value for b in samples)
        self.assertAlmostEqual(logged, 4.0)  # (2 targets*2 NLL +1 target*8 NLL)/3
        self.assertAlmostEqual(trainer.accelerator.backward_total, 4.0)
        self.assertEqual(trainer.processed_tokens_this_invocation, 5)
        self.assertEqual(trainer.supervised_tokens_this_invocation, 3)


if __name__ == "__main__":
    unittest.main()
