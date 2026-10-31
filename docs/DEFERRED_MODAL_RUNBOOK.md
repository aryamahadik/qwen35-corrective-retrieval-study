# Working in MODAL

Run commands from this `MODAL` directory. No command below should be treated as evidence that training data already exist. GPU work is not started by setup or the offline plan.

**1. Inspect the dataset and audit**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-client.txt -r requirements-audit.txt
.venv/bin/python scripts/audit_dataset.py --payload-root data
.venv/bin/python scripts/launch.py --plan
```

Read `reports/dataset_audit.md` and `data/metadata/quality_holds.json`. The audit supports structural cleanliness; a live benchmark backend and task/scorer review are still necessary. `scripts/clean_dataset.py` deterministically rebuilds the working payloads from `data/source_release`, but do not rerun it over intentional later edits without versioning them. Never edit the frozen source copy.

**2. Collect reviewed demonstrations**

Use only `data/task_inputs/train.jsonl` for teaching examples. Run complete workflows against their configured environments, record the actual selected tool schemas and observed tool responses, and grade every indexed verifier. `scripts/strict_verifier_results.py` refuses missing/duplicate outcomes and explicit quality holds; it does not execute the backend itself.

Store externally reviewed trajectories at `data/sft/reviewed_traces.jsonl`, with receipt files beside them. Follow `config/trace_schema.json` and `config/verifier_receipt.schema.json`. The schema specifies provenance, exact model-visible hashes and real verification results. It is not a template for inventing successful examples. The public task specifications do not include these demonstrations, and this project does not yet implement a teacher-generation service or deploy all eight enterprise environments on Modal.

Check the 128 workflows without downloading the tokenizer:

```bash
.venv/bin/python scripts/prepare_sft.py --traces data/sft/reviewed_traces.jsonl --validate-only
```

**3. Prepare tokens locally**

Use a separate tokenizer-only environment on the Mac. Do not install the CUDA training requirements locally.

```bash
python3 -m venv .venv-prepare
.venv-prepare/bin/python -m pip install -r requirements-prepare.txt
.venv-prepare/bin/python scripts/prepare_sft.py --traces data/sft/reviewed_traces.jsonl --output-dir data/sft/prepared
```

The output is `train.tokens.jsonl`, `prepared_manifest.json` and the exact training template. All 128 training identities must be present exactly once. Incorrect masks, mismatched receipts, missing tool results or sequences longer than 16K cause refusal. No automatic truncation occurs. The model and tokenizer revisions are pinned in `config/training.json`; the real-tokenizer smoke check is documented in `reports/data_checkpoint_validation.json`.

**4. Configure Modal and billing**

Authenticate through Modal's browser flow; never paste tokens into files in this project:

```bash
.venv/bin/modal token new --profile enterpriseops
.venv/bin/modal profile activate enterpriseops
```

In Modal Usage & Billing, set a workspace gross usage allowance consistent with this campaign's remaining $30 Modal share. Include existing usage and other workloads; do not increase any stricter limit. Independently cap all external teacher/API attempts at $10. Record that provider setup in `config/modal.json` by setting `budget_enforcement.platform_usage_cap_configured` to true only after it has actually been configured. The flag is a local operator record, not a verified API reading.

The current pricing calculation is $2.814912/hour for the requested Function resources. Image builds, memory/CPU use, storage and interrupted attempts must be counted. If the prices or resource settings change, update the calculation before launch. Free credits do not increase the authorized $40 gross resource budget.

**5. Start or resume one training chunk**

```bash
.venv/bin/python scripts/launch.py --plan
.venv/bin/python scripts/launch.py --train --run-name qwen35-9b-lora-v1
```

Use `--environment NAME` if needed. Prepared-data and budget checks happen locally before an image build/upload/GPU call. No final-test or evaluator-only payloads are uploaded. The first image build and GPU preflight still need validation; dependency pins are source-reviewed, not cloud-tested.

Training runs in bounded chunks. The callback saves full state at optimizer boundaries and the app commits completed checkpoints to the `enterpriseops-qwen35-checkpoints` Volume. The same pinned run can continue using:

```bash
.venv/bin/python scripts/launch.py --train --run-name qwen35-9b-lora-v1 --resume
```

Use the same prepared dataset and model/config revisions. A completed epoch returns its existing result rather than silently starting another. If the budget ledger has an unresolved call, check that call before attempting another one. Do not clear the ledger to bypass a limit. The worker defaults to one epoch and does not automatically select a checkpoint from final-test outcomes.

**6. Download and verify progress before credits expire**

```bash
.venv/bin/modal volume get enterpriseops-qwen35-checkpoints /runs/qwen35-9b-lora-v1 checkpoints/qwen35-9b-lora-v1 --profile enterpriseops
.venv/bin/python scripts/checkpoint_transfer.py latest checkpoints/qwen35-9b-lora-v1
```

Then use the actual printed `checkpoint-N` path:

```text
python scripts/checkpoint_transfer.py verify checkpoints/qwen35-9b-lora-v1/checkpoint-N
python scripts/checkpoint_transfer.py export checkpoints/qwen35-9b-lora-v1/checkpoint-N checkpoints/resume.zip
```

Here `N` is a placeholder for the saved step, not a literal directory to create. Only fully published, hash-verified checkpoints are accepted. A checkpoint includes the LoRA adapter, optimizer, scheduler, RNG, trainer state, tokenizer and run identity. It excludes the frozen base weights, which can be downloaded again at their pinned revision.

**7. Continue in another account/workspace**

Copy this folder's prepared training data, configs and `runs/budget_ledger.json`, plus the verified checkpoint archive. Create/authenticate the destination profile and create its checkpoint Volume. Volumes and credits are workspace-scoped; they do not move automatically.

Import the archive into a new local destination run directory, then upload that run directory:

```text
python scripts/checkpoint_transfer.py import checkpoints/resume.zip checkpoints/migrated-run
modal volume create enterpriseops-qwen35-checkpoints --profile destination
modal volume put enterpriseops-qwen35-checkpoints checkpoints/migrated-run /runs/qwen35-9b-lora-v1 --profile destination
```

Switch to the destination profile, verify its billing controls, and invoke the same `launch.py --train --run-name qwen35-9b-lora-v1 --resume` command. The launcher stages the identical prepared training data in the destination data Volume. Do not discard previous spending when moving accounts. No additional spending above the campaign's current $40 limit is authorized merely by changing account.

**8. Evaluate separately**

The training worker intentionally mounts no test tasks. Evaluate the base and selected adapter using the same frozen tasks, normalized checks, tool interface and generation limits in a separate runner. This folder provides the task data and indexed-result guard, not a completed cloud deployment of the EnterpriseOps environments. Resolve the existing semantic scorer hold first. Report incomplete attempts honestly, and never use a partial run or trained-on tasks as a full official leaderboard score.

**Local verification**

```bash
python3 -m unittest discover -s tests -v
```

Unit tests use temporary synthetic fixtures, not purported enterprise demonstrations. They do not replace a real GPU smoke test, environment replay or held-out model evaluation.
