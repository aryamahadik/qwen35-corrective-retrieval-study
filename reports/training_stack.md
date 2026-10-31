# Qwen3.5-9B Modal training stack

Status: **implemented and locally checked; no cloud image build, GPU model load, or training run has been performed.** The frozen 128 training tasks are task specifications, not reviewed demonstrations. The worker rejects them. It needs the separately prepared `READY_FOR_TRAINING` manifest and 128 complete reviewed/tokenized trajectories.

## Worker interface

```python
config = load_config(config_path)
summary = validate_prepared_dataset(train_jsonl, prepared_manifest_path, config)
# Both calls above use the standard library only: no GPU libraries or cloud calls.

result = run_training(
    train_jsonl,
    output_dir,
    prepared_manifest_path=prepared_manifest_path,
    config_path=config_path,
    resume_from_checkpoint=None,
    on_checkpoint=publish_and_commit,
    max_wall_seconds=approved_remaining_seconds,
)
```

`on_checkpoint(path)` runs only after a complete optimizer-boundary checkpoint and its tokenizer/run identity have been written. The root app publishes its integrity manifest and commits its Modal Volume. Published checkpoints are not rewritten at the end of training. Portable resume verifies a checkpoint inventory before restoring its embedded run identity to a new parent directory.

The worker verifies the prepared file/template hashes, package versions, target-token masks, task counts and membership against the frozen split's pinned SHA256. The remote image can point `ENTERPRISEOPS_SPLIT_MANIFEST` to the copied metadata manifest; this does not copy test prompts or evaluator records. Review receipts establish externally asserted provenance: the worker does not claim to independently replay or certify the demonstrations.

## Chosen model/configuration

The model is `Qwen/Qwen3.5-9B` at revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`. The loader requests `text_only=True`, BF16 base weights, no quantization, no full finetuning, no fast vLLM inference, one explicit CUDA device and Unsloth gradient checkpointing. These arguments exist in the inspected Unsloth2026.9.4 wheel. [Unsloth loader source](https://github.com/unslothai/unsloth/blob/main/unsloth/models/loader.py).

The initial configuration is 16,384 tokens, rank32/alpha32/dropout0, batch1, eight accumulation microbatches, AdamW at1e-4, one epoch, and checkpointing every two optimizer updates. There is no automatic extra epoch. The rank32 adapters cover248 language linear matrices and must total86,556,672 trainable parameters. The worker discovers actual full module names and applies an exact-name regex; it rejects a renamed/fused layout needing a fresh count. It also rejects any trainable parameter outside LoRA A/B matrices. The suffixes are:

```
q_proj k_proj v_proj o_proj
in_proj_qkv in_proj_z in_proj_a in_proj_b out_proj
gate_proj up_proj down_proj
```

Embedding, LM head, vision and MTP weights remain frozen/excluded. The runtime records actual loaded parameters/bytes, target names, package inventory, GPU capacity, and measured peak memory. Memory fit and throughput remain unmeasured until an actual run.

## Dependency pins and compatibility evidence

| Component | Pin | Evidence |
|---|---|---|
| PyTorch |2.10.0+cu128|Official PyTorch CUDA12.8 wheel matrix|
| torchvision / torchaudio |0.25.0+cu128 /2.10.0+cu128|Same official matrix|
| xformers |0.0.34|Unsloth's `cu128-torch2100` extra pins this version|
| Unsloth / zoo |2026.9.4 /2026.9.3|Publisher PyPI dependency metadata|
| Transformers |5.5.0|Within both Unsloth packages' allowed maximum|
| TRL |0.24.0|Within both Unsloth packages' allowed maximum|
| PEFT |0.18.0|Meets Unsloth's minimum|
| torchao |0.16.0|Official compatibility statement for Torch2.10 C++ extensions|
| datasets / accelerate |4.3.0 /1.12.0|Meet reviewed dependency constraints|
| tokenizers / Jinja2 |0.22.2 /3.1.6|Pinned for matching preparation/rendering|

Sources: [PyTorch wheel matrix](https://pytorch.org/get-started/previous-versions/), [torchao releases](https://github.com/pytorch/ao/releases), [Unsloth2026.9.4 package metadata](https://pypi.org/pypi/unsloth/2026.9.4/json), [Unsloth zoo2026.9.3 metadata](https://pypi.org/pypi/unsloth_zoo/2026.9.3/json), [TRL0.24 metadata](https://pypi.org/pypi/trl/0.24.0/json).

These are **source/metadata-reviewed pins, not a claim of an already validated cloud environment**. A dependency resolver/build and CUDA smoke test still need to succeed. The requirements file pins the main numerical/model/tokenization stack; remaining transitive packages are captured in `runtime_metadata.json` after loading. Reproduction should retain the built image and full installed-version inventory.

The official [Modal Unsloth example](https://modal.com/docs/examples/unsloth_finetune) is useful for Volumes/checkpoint orchestration, but its listed Qwen3/Transformers4.54/Unsloth2025.7 versions predate Qwen3.5. They must not be copied as a Qwen3.5 compatibility recipe. Modal already supplies GPU drivers; [CUDA toolkit guidance](https://modal.com/docs/examples/install_cuda) explains when a CUDA-devel image is needed. A100 is Ampere and supports the selected BF16 path.

## SFT objective and long-context loss

Prepared rows contain `input_ids`, `labels` and `source_task_id`; the latter is removed before collation. Padding uses the tokenizer's pad ID, attention mask0 and label−100. No row is truncated, packed, or silently assigned a new label mask. The first token must have label−100 and every row must retain supervised tokens after the causal shift.

This worker uses Hugging Face `Trainer` for the SFT objective because preparation already produces exact labels. It does not depend on a recent `SFTTrainer` auto-patcher: Unsloth's current package metadata restricts TRL to≤0.24, whereas current TRL documentation describes newer template APIs. The preparer supplies the inspected Qwen3.5 generation-marked template and validates rendering/masks. [TRL0.24 SFT API](https://huggingface.co/docs/trl/v0.24.0/en/sft_trainer).

For accumulation, a microbatch with mean supervised loss `L_i` and `n_i` target tokens contributes `L_i*n_i/sum(n_i)`. The custom Trainer counts actual shifted targets across the accumulation group, including a partial final group. Its backward method cancels Accelerator1.12's automatic division by the accumulation-step count so this token normalization is applied exactly once. This single-GPU BF16 path rejects multiple processes and GradScaler. A numerical mock runs the worker's actual Trainer methods and distinguishes token weighting from incorrect equal-microbatch averaging and double division. [Pinned Trainer source](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/trainer.py), [Accelerator1.12 source](https://github.com/huggingface/accelerate/blob/v1.12.0/src/accelerate/accelerator.py).

Unsloth is imported before torch/Transformers. The inspected zoo compiler supplies fused/chunked LM-head cross entropy, and its custom backward supports upstream loss scaling. The worker requires `UNSLOTH_RETURN_LOGITS=0` and fails if a training forward returns a nonempty full-logits tensor. The path still requires GPU verification. It does not request TRL `chunked_nll`, whose current documentation lists PEFT/VLM incompatibility. [Unsloth compiler](https://github.com/unslothai/unsloth-zoo/blob/main/unsloth_zoo/compiler.py), [fused loss](https://github.com/unslothai/unsloth-zoo/blob/main/unsloth_zoo/fused_losses/cross_entropy_loss.py), [TRL memory restrictions](https://huggingface.co/docs/trl/reducing_memory_usage#chunked-cross-entropy-for-reducing-peak-memory-usage).

## Checkpoints, budget and verification

Checkpoints include adapter weights/config, optimizer, scheduler, RNG, Trainer state, tokenizer/template and run identity. `save_only_model=False`; the separate `final_adapter` is an inference export, not the resumable checkpoint. Resume preserves the total one-epoch target and requires matching model/data/config identity.

The worker's wall allowance includes loading/compilation. It requests stop plus save at an optimizer boundary once the checkpoint reserve begins. A single long update or stall can exceed that soft limit, so the root Modal timeout and cumulative dollar ledger must also apply. Retrying or resuming does not create a new$40 budget. No accuracy or performance claim is inferred from a completed training loss.

Local validation: 15 standard-library/mock tests cover raw-data rejection, readiness, hash/ID/token/receipt checks, padding, partial checkpoint rejection, immutable publication, portable run identity, and accumulation math. All TrainingArguments keyword names were also checked against the pinned5.5.0 wheel source. These checks do not validate CUDA kernels, numerical GPU equivalence, model loading or actual memory fit.
