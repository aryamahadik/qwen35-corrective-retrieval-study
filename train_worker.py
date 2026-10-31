"""One-GPU BF16 LoRA worker. Importing this module does not load GPU libraries.

Only reviewed, pretokenized SFT data from prepare_sft may enter this worker.
Task specifications and evaluator records are not SFT data. Cloud launch and the
campaign's aggregate dollar ledger are the caller's responsibility.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import time
from typing import Callable

MODEL_ID = "Qwen/Qwen3.5-9B"
MODEL_REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
TARGET_SUFFIXES = (
    "q_proj", "k_proj", "v_proj", "o_proj", "in_proj_qkv", "in_proj_z",
    "in_proj_a", "in_proj_b", "out_proj", "gate_proj", "up_proj", "down_proj",
)


class TrainingGateError(ValueError):
    """Input/configuration is not eligible for this training worker."""


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def _positive_int(value, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise TrainingGateError(f"{name} must be a positive integer")
    return value


def load_config(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path else Path(__file__).parent / "config/training.json"
    config = json.loads(path.read_text())
    if config.get("model_id") != MODEL_ID or config.get("model_revision") != MODEL_REVISION:
        raise TrainingGateError("This worker is pinned to the reviewed Qwen3.5-9B revision")
    if config.get("packing") is not False or config.get("save_only_model") is not False:
        raise TrainingGateError("Packing must be disabled; optimizer/RNG checkpoint state must be saved")
    if config.get("lora_target_modules") != list(TARGET_SUFFIXES):
        raise TrainingGateError("All twelve reviewed language projection targets are required")
    for name in ("max_seq_length", "vocab_size", "expected_training_tasks", "lora_rank",
                 "lora_alpha", "gradient_accumulation_steps", "save_steps", "save_total_limit",
                 "max_wall_seconds", "checkpoint_reserve_seconds"):
        _positive_int(config.get(name), name)
    if config["max_seq_length"] not in (8192, 16384, 32768):
        raise TrainingGateError("Sequence length must be a reviewed 8K/16K/32K configuration")
    if config.get("per_device_train_batch_size") != 1 or config.get("num_train_epochs") != 1:
        raise TrainingGateError("This budgeted run requires microbatch 1 and one epoch")
    if config.get("vocab_size") != 248320 or config.get("expected_target_matrices") != 248:
        raise TrainingGateError("Unexpected architecture dimensions")
    if config.get("expected_adapter_parameters") != config["lora_rank"] * 2704896:
        raise TrainingGateError("Adapter parameter expectation does not match rank")
    if config["checkpoint_reserve_seconds"] >= config["max_wall_seconds"]:
        raise TrainingGateError("Checkpoint reserve must be smaller than wall time")
    if config.get("optim") != "adamw_torch" or config.get("lora_dropout") != 0.0:
        raise TrainingGateError("The reviewed optimizer/dropout settings were changed")
    for key in ("learning_rate", "weight_decay", "warmup_ratio", "max_grad_norm"):
        value = config.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            raise TrainingGateError(f"{key} must be finite")
    if not 0 < config["learning_rate"] <= 0.001 or not 0 <= config["warmup_ratio"] < 1:
        raise TrainingGateError("Invalid learning-rate or warmup setting")
    if config["weight_decay"] < 0 or config["max_grad_norm"] <= 0:
        raise TrainingGateError("Invalid optimizer settings")
    return config


def validate_prepared_data(train_jsonl: str | Path, prepared_manifest_path: str | Path,
                           config: dict, *, frozen_split_manifest_path: str | Path | None = None
                           ) -> tuple[list[dict], dict, str]:
    """Standard-library gate: verify structure/provenance before GPU imports.

    Review receipts are externally asserted provenance, not a claim that this
    worker independently replayed or solved the benchmark tasks.
    """
    path, manifest_path = Path(train_jsonl).resolve(), Path(prepared_manifest_path).resolve()
    manifest = json.loads(manifest_path.read_text())
    if (manifest.get("schema_version") != 1 or manifest.get("status") != "READY_FOR_TRAINING"
            or manifest.get("ready") is not True):
        raise TrainingGateError("Verified SFT data are not ready; raw task files cannot be trained")
    if manifest.get("model_id") != MODEL_ID or manifest.get("model_revision") != MODEL_REVISION:
        raise TrainingGateError("Prepared data model identity/revision mismatch")
    if manifest.get("tokenizer_revision") != MODEL_REVISION:
        raise TrainingGateError("Prepared data tokenizer revision mismatch")
    if manifest.get("max_seq_length") != config["max_seq_length"]:
        raise TrainingGateError("Prepared data context length differs from training configuration")
    if manifest.get("train_file") != path.name or manifest_path.parent / path.name != path:
        raise TrainingGateError("Prepared training file must be beside its manifest")
    if manifest.get("train_file_sha256") != file_sha256(path):
        raise TrainingGateError("Prepared training-file hash mismatch")
    for key in ("split_manifest_sha256", "source_traces_sha256", "chat_template_sha256"):
        if not isinstance(manifest.get(key), str) or not re.fullmatch(r"[0-9a-f]{64}", manifest[key]):
            raise TrainingGateError(f"Missing or invalid provenance hash: {key}")
    split_location = frozen_split_manifest_path or os.environ.get("ENTERPRISEOPS_SPLIT_MANIFEST")
    split_path = (Path(split_location) if split_location else
                  Path(__file__).parent / "data/metadata/split_manifest.json")
    split_hash = file_sha256(split_path)
    if split_hash != config.get("split_manifest_sha256") or split_hash != manifest["split_manifest_sha256"]:
        raise TrainingGateError("Prepared data do not match the pinned frozen split manifest")
    frozen_split = json.loads(split_path.read_text())
    expected_ids = frozen_split["task_ids"]["train"]
    if (len(expected_ids) != config["expected_training_tasks"] or len(set(expected_ids)) != len(expected_ids)
            or manifest.get("training_task_ids") != sorted(expected_ids)):
        raise TrainingGateError("Prepared task IDs must match the frozen training membership, excluding dev/test/holds")
    template_name = manifest.get("chat_template_file")
    if not isinstance(template_name, str) or Path(template_name).name != template_name:
        raise TrainingGateError("Chat-template path must be one local filename")
    template_path = manifest_path.parent / template_name
    if file_sha256(template_path) != manifest["chat_template_sha256"]:
        raise TrainingGateError("Training chat-template hash mismatch")
    template = template_path.read_text()
    if "generation" not in template or "endgeneration" not in template:
        raise TrainingGateError("Prepared data require the reviewed assistant-mask training template")
    for package in ("transformers", "tokenizers", "jinja2"):
        if manifest.get("versions", {}).get(package) != config["required_versions"][package]:
            raise TrainingGateError(f"Prepare data using the pinned {package} version")
    rows, ids, total, supervised = [], [], 0, 0
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if set(row) not in ({"input_ids", "labels", "source_task_id"},
                                {"input_ids", "labels", "source_task_id", "attention_mask"}):
                raise TrainingGateError(f"Row {line_number}: only prepared token/label fields are allowed")
            tokens, labels = row["input_ids"], row["labels"]
            if not isinstance(tokens, list) or not isinstance(labels, list) or len(tokens) != len(labels):
                raise TrainingGateError(f"Row {line_number}: token/label length mismatch")
            if not 2 <= len(tokens) <= config["max_seq_length"]:
                raise TrainingGateError(f"Row {line_number}: empty/overlength sequence; no truncation is allowed")
            if any(type(token) is not int or not 0 <= token < config["vocab_size"] for token in tokens):
                raise TrainingGateError(f"Row {line_number}: invalid token ID")
            if any(type(label) is not int or label not in (-100, token) for token, label in zip(tokens, labels)):
                raise TrainingGateError(f"Row {line_number}: labels must copy tokens or use -100")
            count = sum(label != -100 for label in labels[1:])
            if labels[0] != -100 or not count:
                raise TrainingGateError(f"Row {line_number}: first token must be masked and assistant targets nonempty")
            if "attention_mask" in row and row["attention_mask"] != [1] * len(tokens):
                raise TrainingGateError(f"Row {line_number}: prepared rows must be unpadded")
            task_id = row["source_task_id"]
            if not isinstance(task_id, str) or not task_id:
                raise TrainingGateError(f"Row {line_number}: missing source task ID")
            ids.append(task_id)
            rows.append({"input_ids": tokens, "labels": labels})
            total += len(tokens)
            supervised += count
    if len(ids) != len(set(ids)):
        raise TrainingGateError("This preparation contract requires exactly one full trajectory per task")
    if len(ids) != config["expected_training_tasks"]:
        raise TrainingGateError("All expected training-task demonstrations are required")
    if sorted(ids) != manifest.get("training_task_ids"):
        raise TrainingGateError("Prepared task IDs differ from manifest")
    for key, observed in (("row_count", len(rows)), ("task_count", len(ids)),
                          ("total_tokens", total), ("supervised_tokens", supervised)):
        if manifest.get(key) != observed:
            raise TrainingGateError(f"Prepared manifest {key} mismatch")
    receipts = manifest.get("review_receipts")
    if not isinstance(receipts, dict) or set(receipts) != set(ids) or any(not r for r in receipts.values()):
        raise TrainingGateError("Every training task requires an external review receipt")
    return rows, manifest, template


def validate_prepared_dataset(train_jsonl: str | Path, prepared_manifest_path: str | Path,
                              config: dict, *, frozen_split_manifest_path: str | Path | None = None) -> dict:
    """Lightweight public launch gate; returns counts/hashes, never transcript text."""
    rows, manifest, _ = validate_prepared_data(
        train_jsonl, prepared_manifest_path, config, frozen_split_manifest_path=frozen_split_manifest_path)
    return {
        "ready": True, "row_count": len(rows), "task_count": manifest["task_count"],
        "total_tokens": manifest["total_tokens"],
        "supervised_tokens": manifest["supervised_tokens"],
        "model_id": MODEL_ID, "model_revision": MODEL_REVISION,
        "train_file_sha256": manifest["train_file_sha256"],
        "prepared_manifest_sha256": file_sha256(prepared_manifest_path),
        "review_note": "External review receipts are asserted provenance; this gate does not replay tasks.",
    }


def padded_batch(rows: list[dict], pad_token_id: int) -> dict:
    """Pure-Python padding, also useful for checking the GPU collator locally."""
    if not rows:
        raise TrainingGateError("Cannot collate an empty batch")
    width = max(len(row["input_ids"]) for row in rows)
    result = {"input_ids": [], "labels": [], "attention_mask": []}
    for row in rows:
        n = len(row["input_ids"])
        result["input_ids"].append(row["input_ids"] + [pad_token_id] * (width - n))
        result["labels"].append(row["labels"] + [-100] * (width - n))
        result["attention_mask"].append([1] * n + [0] * (width - n))
    return result


def runtime_versions(config: dict) -> dict:
    found = {}
    for package, expected in config["required_versions"].items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError as error:
            raise TrainingGateError(f"Missing pinned training package: {package}") from error
        found[package] = actual
        if actual != expected:
            raise TrainingGateError(f"{package}: expected {expected}, found {actual}; rebuild the pinned image")
    return found


def validate_checkpoint(path: str | Path) -> None:
    path = Path(path)
    required = ("trainer_state.json", "optimizer.pt", "scheduler.pt", "rng_state.pth", "adapter_config.json")
    if not path.is_dir() or any(not (path / name).is_file() for name in required):
        raise TrainingGateError("Resume requires a complete optimizer/scheduler/RNG/adapter checkpoint")
    if not (path / "adapter_model.safetensors").is_file():
        raise TrainingGateError("Checkpoint adapter weights are missing")


def portable_checkpoint_identity(checkpoint_path: str | Path) -> dict:
    """Read run identity only after the portable checkpoint's inventory verifies."""
    helper_path = Path(__file__).parent / "checkpoint_utils.py"
    spec = importlib.util.spec_from_file_location("_qwen_checkpoint_integrity", helper_path)
    if spec is None or spec.loader is None:
        raise TrainingGateError("Checkpoint integrity helper is unavailable")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    manifest = helper.verify_checkpoint(checkpoint_path)
    if "run_identity.json" not in manifest["files"]:
        raise TrainingGateError("Portable checkpoint lacks a hashed run_identity.json")
    return json.loads((Path(checkpoint_path) / "run_identity.json").read_text())


def finalize_checkpoint_payload(checkpoint_path: str | Path, identity: dict,
                                save_tokenizer: Callable[[str], object]) -> bool:
    """Finish payload before first publication; never rewrite a published copy.

    Returns True if files were added, False if an already published checkpoint
    was verified unchanged. The caller publishes only after this function.
    """
    path = Path(checkpoint_path)
    validate_checkpoint(path)
    if (path / "checkpoint_manifest.json").exists():
        if portable_checkpoint_identity(path) != identity:
            raise TrainingGateError("Published checkpoint run identity mismatch")
        return False
    save_tokenizer(str(path))
    _write_json(path / "run_identity.json", identity)
    return True


def run_training(train_jsonl: str, output_dir: str, *, prepared_manifest_path: str,
                 config_path: str | None = None, resume_from_checkpoint: str | None = None,
                 on_checkpoint: Callable[[str], None] | None = None,
                 max_wall_seconds: int | None = None) -> dict:
    """Train reviewed pretokenized SFT, returning measurements and checkpoint paths.

    Call only behind the app's CPU readiness/budget gate. ``on_checkpoint`` runs
    after complete checkpoint writes and can commit a Modal Volume. The caller
    must count earlier attempts and image/runtime costs against the $40 ledger.
    The wall callback stops at an optimizer boundary; an external Modal timeout
    remains necessary for stalls or an overlong single update.
    """
    started = time.monotonic()
    config = load_config(config_path)
    rows, prepared, training_template = validate_prepared_data(train_jsonl, prepared_manifest_path, config)
    duration = config["max_wall_seconds"] if max_wall_seconds is None else min(
        config["max_wall_seconds"], _positive_int(max_wall_seconds, "max_wall_seconds"))
    if duration <= config["checkpoint_reserve_seconds"]:
        raise TrainingGateError("Insufficient wall-time allocation after checkpoint reserve")
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    identity = {
        "model_id": MODEL_ID, "model_revision": MODEL_REVISION,
        "prepared_manifest_sha256": file_sha256(prepared_manifest_path),
        "config": config,
    }
    identity_path = output / "run_identity.json"
    if resume_from_checkpoint:
        checkpoint = Path(resume_from_checkpoint).resolve()
        if checkpoint.parent != output:
            raise TrainingGateError("Resume checkpoint must belong to this run output directory")
        validate_checkpoint(checkpoint)
        checkpoint_identity = portable_checkpoint_identity(checkpoint)
        if checkpoint_identity != identity:
            raise TrainingGateError("Portable checkpoint model, data or training configuration differs")
        if not identity_path.exists():
            _write_json(identity_path, checkpoint_identity)
        if json.loads(identity_path.read_text()) != identity:
            raise TrainingGateError("Resume model, data or training configuration differs from original run")
    elif any(output.glob("checkpoint-*")) or (output / "training_result.json").exists():
        raise TrainingGateError("Existing training detected; resume explicitly or choose a fresh run directory")
    elif identity_path.exists() and json.loads(identity_path.read_text()) != identity:
        raise TrainingGateError("Existing run identity differs from requested model/data/config")
    versions = runtime_versions(config)
    for bad in ("UNSLOTH_ENABLE_FULL_FINETUNING", "UNSLOTH_RETURN_LOGITS"):
        if os.environ.get(bad, "0") not in ("", "0"):
            raise TrainingGateError(f"{bad} must be disabled for the reviewed LoRA/loss path")
    os.environ["UNSLOTH_RETURN_LOGITS"] = "0"
    # Import order is part of Unsloth's documented API contract.
    import unsloth  # noqa: F401
    import torch
    from unsloth import FastLanguageModel, FastModel
    from transformers import Trainer, TrainerCallback, TrainingArguments, set_seed

    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise TrainingGateError("This worker requires exactly one visible CUDA GPU")
    properties = torch.cuda.get_device_properties(0)
    if "A100" not in properties.name or properties.total_memory < 75 * 10**9:
        raise TrainingGateError("This release expects an A100 with approximately 80GB VRAM")
    if not torch.cuda.is_bf16_supported():
        raise TrainingGateError("GPU does not support BF16")
    if torch.version.cuda != "12.8":
        raise TrainingGateError("Expected the pinned CUDA 12.8 PyTorch runtime")
    if int(os.environ.get("WORLD_SIZE", "1")) != 1:
        raise TrainingGateError("Distributed training is outside this single-GPU contract")
    _write_json(identity_path, identity)
    set_seed(config["seed"])
    torch.cuda.reset_peak_memory_stats()
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_ID, revision=MODEL_REVISION, use_exact_model_name=True,
        max_seq_length=config["max_seq_length"], dtype=torch.bfloat16,
        load_in_4bit=False, load_in_8bit=False, load_in_16bit=True,
        full_finetuning=False, text_only=True, trust_remote_code=False,
        fast_inference=False, device_map={"": "cuda:0"},
        use_gradient_checkpointing="unsloth", random_state=config["seed"],
    )
    # Resolve exact language-only module names rather than broad suffix matches
    # on a VLM. This also rejects renamed/fused architectures requiring review.
    targets = []
    dimension_count = 0
    for name, module in model.named_modules():
        if (re.search(r"(?:^|\.)layers\.\d+\.", name)
                and name.rsplit(".", 1)[-1] in TARGET_SUFFIXES
                and not any(x in name.split(".") for x in ("visual", "vision", "mtp"))
                and isinstance(module, torch.nn.Linear)):
            targets.append(name)
            dimension_count += config["lora_rank"] * (module.in_features + module.out_features)
    if len(targets) != config["expected_target_matrices"] or dimension_count != config["expected_adapter_parameters"]:
        raise TrainingGateError(f"Loaded target architecture differs: {len(targets)} matrices, {dimension_count} adapter parameters")
    # An exact-name regex avoids Unsloth reinterpreting a list of full module
    # names through its suffix-based vision/language target selector.
    target_regex = "^(?:" + "|".join(re.escape(name) for name in targets) + ")$"
    model = FastModel.get_peft_model(
        model, r=config["lora_rank"], lora_alpha=config["lora_alpha"],
        lora_dropout=0.0, bias="none", target_modules=target_regex,
        finetune_vision_layers=False, finetune_language_layers=True,
        finetune_attention_modules=True, finetune_mlp_modules=True,
        modules_to_save=None, use_gradient_checkpointing="unsloth",
        random_state=config["seed"],
    )
    trainable = {name: parameter for name, parameter in model.named_parameters() if parameter.requires_grad}
    if any("lora_A" not in name and "lora_B" not in name for name in trainable):
        raise TrainingGateError("Unexpected base/vision/embedding/head parameters became trainable")
    adapter_count = sum(parameter.numel() for parameter in trainable.values())
    if adapter_count != dimension_count:
        raise TrainingGateError("Actual trainable adapter parameter count differs from the validated targets")
    tokenizer.chat_template = training_template
    tokenizer.padding_side = "right"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    if tokenizer.pad_token_id is None:
        raise TrainingGateError("Tokenizer has no usable padding token")
    model.config.use_cache = False
    FastModel.for_training(model, use_gradient_checkpointing=True)
    model_metadata = {
        "runtime_versions": versions, "gpu_name": properties.name,
        "all_installed_versions": {
            distribution.metadata["Name"]: distribution.version
            for distribution in importlib.metadata.distributions()
            if distribution.metadata.get("Name")
        },
        "gpu_memory_bytes": properties.total_memory,
        "loaded_parameter_count": sum(p.numel() for p in model.parameters()),
        "loaded_tensor_bytes": sum(p.numel() * p.element_size() for p in model.parameters()),
        "trainable_adapter_parameters": adapter_count,
        "target_matrices": targets, "prepared_total_tokens": prepared["total_tokens"],
        "prepared_supervised_tokens": prepared["supervised_tokens"],
        "runtime_verified": False, "accuracy_claim": None,
    }
    _write_json(output / "runtime_metadata.json", model_metadata)

    class TokenCollator:
        def __call__(self, features):
            batch = padded_batch(features, tokenizer.pad_token_id)
            return {key: torch.tensor(value, dtype=torch.long) for key, value in batch.items()}

    class TokenWeightedTrainer(Trainer):
        """Sum token loss over an accumulation group, divided by target tokens.

        The patched model supplies its ordinary mean shifted-label NLL without
        ``num_items_in_batch``. Rescale that mean here by each microbatch's target
        count / the accumulation group's target count. Setting the consumption
        flag prevents Trainer from dividing a second time by accumulation steps.
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.model_accepts_loss_kwargs = True
            self.processed_tokens_this_invocation = 0
            self.supervised_tokens_this_invocation = 0
            self.loss_calls = 0

        def get_batch_samples(self, epoch_iterator, num_batches, device):
            samples = []
            for _ in range(num_batches):
                try:
                    samples.append(next(epoch_iterator))
                except StopIteration:
                    break
            count = sum(int(batch["labels"][:, 1:].ne(-100).sum().item()) for batch in samples)
            if samples and count == 0:
                raise TrainingGateError("Accumulation group has no supervised tokens")
            return samples, count if samples else None

        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            n = inputs["labels"][:, 1:].ne(-100).sum()
            if n.item() == 0:
                raise TrainingGateError("Microbatch has no supervised target tokens")
            outputs = model(**inputs)  # do not pass the group denominator twice
            loss = outputs.loss
            if loss is None or loss.numel() != 1 or not torch.isfinite(loss.detach()).item():
                raise TrainingGateError("Model did not produce a finite scalar supervised loss")
            logits = getattr(outputs, "logits", None)
            if isinstance(logits, torch.Tensor) and logits.numel() > 0:
                raise TrainingGateError("Full logits were materialized; the required Unsloth fused-loss path is inactive")
            if model.training:
                self.processed_tokens_this_invocation += int(inputs["attention_mask"].sum().item())
                self.supervised_tokens_this_invocation += int(n.item())
                self.loss_calls += 1
                if num_items_in_batch is None or int(num_items_in_batch) <= 0:
                    raise TrainingGateError("Missing token denominator for gradient accumulation")
                loss = loss * n.to(loss.device) / num_items_in_batch
            return (loss, outputs) if return_outputs else loss

        def training_step(self, model, inputs, num_items_in_batch=None):
            # Accelerator 1.12 always divides backward loss by its configured
            # accumulation count. We already used the group's *token* count,
            # including a partial final group, so explicitly cancel that extra
            # division instead of inheriting a version-dependent double scale.
            if self.accelerator.num_processes != 1 or self.accelerator.scaler is not None:
                raise TrainingGateError("Token-weighted worker supports single-GPU BF16 without GradScaler only")
            model.train()
            inputs = self._prepare_inputs(inputs)
            with self.compute_loss_context_manager():
                loss = self.compute_loss(model, inputs, num_items_in_batch=num_items_in_batch)
            self.accelerator.backward(loss * self.accelerator.gradient_accumulation_steps)
            return loss.detach()

    class BudgetCheckpointCallback(TrainerCallback):
        def __init__(self):
            self.stopped_for_wall_budget = False
            self.last_complete_checkpoint = None

        def on_train_begin(self, args, state, control, **kwargs):
            if time.monotonic() - started >= duration - config["checkpoint_reserve_seconds"]:
                raise TrainingGateError("Model loading used the allocated training time; no optimizer step started")
            return control

        def on_step_end(self, args, state, control, **kwargs):
            if time.monotonic() - started >= duration - config["checkpoint_reserve_seconds"]:
                self.stopped_for_wall_budget = True
                control.should_save = True
                control.should_training_stop = True
            return control

        def on_save(self, args, state, control, **kwargs):
            checkpoint_path = output / f"checkpoint-{state.global_step}"
            finalize_checkpoint_payload(checkpoint_path, identity, tokenizer.save_pretrained)
            self.last_complete_checkpoint = str(checkpoint_path)
            if on_checkpoint:
                on_checkpoint(str(checkpoint_path))
            return control

    callback = BudgetCheckpointCallback()
    arguments = TrainingArguments(
        output_dir=str(output), per_device_train_batch_size=1,
        gradient_accumulation_steps=config["gradient_accumulation_steps"],
        num_train_epochs=1, learning_rate=config["learning_rate"],
        lr_scheduler_type=config["lr_scheduler_type"], warmup_ratio=config["warmup_ratio"],
        weight_decay=config["weight_decay"], max_grad_norm=config["max_grad_norm"],
        bf16=True, fp16=False, tf32=True, optim=config["optim"],
        gradient_checkpointing=True, logging_steps=1, report_to=[],
        save_strategy="steps", save_steps=config["save_steps"],
        save_total_limit=config["save_total_limit"], save_only_model=False,
        eval_strategy="no", dataloader_num_workers=0, dataloader_pin_memory=True,
        remove_unused_columns=False, seed=config["seed"], data_seed=config["seed"],
        include_num_input_tokens_seen="non_padding", average_tokens_across_devices=False,
        label_names=["labels"],
    )
    trainer = TokenWeightedTrainer(
        model=model, args=arguments, train_dataset=rows,
        data_collator=TokenCollator(), processing_class=tokenizer, callbacks=[callback],
    )
    try:
        result = trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        # The pinned Trainer API writes model, optimizer, scheduler, RNG and state.
        # A final non-save-step checkpoint is required even after a short epoch.
        checkpoint_path = output / f"checkpoint-{trainer.state.global_step}"
        if (callback.last_complete_checkpoint != str(checkpoint_path)
                and not (checkpoint_path / "checkpoint_manifest.json").exists()):
            trainer._save_checkpoint(model, trial=None)
        finalize_checkpoint_payload(checkpoint_path, identity, tokenizer.save_pretrained)
        if on_checkpoint:
            on_checkpoint(str(checkpoint_path))
        adapter_path = output / "final_adapter"
        model.save_pretrained(str(adapter_path))
        tokenizer.save_pretrained(str(adapter_path))
        elapsed = time.monotonic() - started
        summary = {
            "status": "WALL_BUDGET_STOPPED" if callback.stopped_for_wall_budget else "EPOCH_COMPLETE",
            "optimizer_steps_total": trainer.state.global_step,
            "epoch": trainer.state.epoch, "elapsed_seconds_this_invocation": elapsed,
            "processed_tokens_this_invocation": trainer.processed_tokens_this_invocation,
            "supervised_tokens_this_invocation": trainer.supervised_tokens_this_invocation,
            "processed_tokens_per_second_including_setup": trainer.processed_tokens_this_invocation / elapsed,
            "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
            "peak_reserved_bytes": torch.cuda.max_memory_reserved(),
            "checkpoint_path": str(checkpoint_path), "adapter_path": str(adapter_path),
            "train_metrics": result.metrics, "accuracy_claim": None,
            "cost_note": "Elapsed worker time is not a total campaign bill; caller owns the cumulative dollar ledger.",
        }
        model_metadata["runtime_verified"] = trainer.loss_calls > 0
        _write_json(output / "runtime_metadata.json", model_metadata)
        _write_json(output / "training_result.json", summary)
        if on_checkpoint:
            on_checkpoint(str(checkpoint_path))
        return summary
    except BaseException as error:
        _write_json(output / "training_failure.json", {
            "error_type": type(error).__name__, "message": str(error),
            "last_complete_checkpoint": callback.last_complete_checkpoint,
            "elapsed_seconds_this_invocation": time.monotonic() - started,
            "partial_optimizer_update_saved": False,
        })
        if on_checkpoint and callback.last_complete_checkpoint:
            on_checkpoint(callback.last_complete_checkpoint)
        raise
