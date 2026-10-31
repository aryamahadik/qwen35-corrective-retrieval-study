# MODAL EnterpriseOps Workspace

This is the organized working folder for the Qwen3.5-9B LoRA experiment.

**Current status:** 329 task specifications are organized and the working files pass the static structural audit. The split remains 128 training, 41 development and 160 final-test tasks. One final-test task has an unresolved semantic scorer issue. No verified 128-workflow SFT corpus exists yet, no Modal account was authenticated, and no paid GPU training has run.

Start with `python3 scripts/launch.py --plan`. It runs locally, reports readiness and budget, and allocates no cloud resources. See [RUNBOOK.md](RUNBOOK.md) for the full workflow.

**Folder layout**

```text
MODAL/
  data/
    source_release/       untouched copy of the original 329-task release
    task_inputs/          cleaned train / development / final_test inputs
    evaluator_only/       matching SQL checks and environment configuration
    metadata/             frozen IDs, hashes, groups, cleaning ledger, quality holds
    sft/                  reviewed training conversations and prepared tokens go here
  config/                 model, Modal resources, templates and receipt schemas
  scripts/                audit, cleaning, data preparation, launch, checkpoint transfer
  reports/                source audit, cleaned audit, validation and stack notes
  train_worker.py         gated BF16 LoRA training worker
  modal_app.py            A100 Function and persistent Volumes
  checkpoint_utils.py    complete-checkpoint publication and portable import/export
  budget_control.py      conservative cumulative call reservations
  tests/                  local correctness tests
  checkpoints/            local copies downloaded from Modal
  runs/                   budget ledger and local run records
```

**Dataset split**

| Domain | Train | Development | Final test | Total |
|---|---:|---:|---:|---:|
| Calendar | 8 | 3 | 20 | 31 |
| CSM | 24 | 3 | 20 | 47 |
| Drive | 8 | 3 | 20 | 31 |
| Email | 8 | 3 | 20 | 31 |
| HR | 24 | 3 | 20 | 47 |
| Hybrid | 24 | 3 | 20 | 47 |
| ITSM | 24 | 20 | 20 | 64 |
| Teams | 8 | 3 | 20 | 31 |
| **Total** | **128** | **41** | **160** | **329** |

The former 311 reserve tasks and nine prior ITSM quality holds are absent from task payloads. The source copy and working copy contain the same 329 identities; copies are not additional examples. Existing ITSM membership is preserved.

**What was cleaned and checked**

- Unique task IDs, split disjointness, exclusions, domain counts, input/evaluator alignment, source hashes and audited workflow-family separation were checked.
- Seven repeated tool-name lists were deduplicated without changing their order of first appearance.
- All 1,749 verifier identifiers were made unique by index. This prevents a name-keyed scorer from overwriting distinct checks. No verifier was deleted.
- Thirty-seven direct SQL `COUNT` expectations stored as numeric strings were converted to integers. Query text, operators and numeric magnitudes were preserved.
- All 1,749 SQL statements parse as read queries. Parsing does not establish that the live schema exists or that every task can be completed.
- The 226 redundant normalized verifier entries were retained to preserve the declared check inventory; they are diagnostics, not independent evidence of accuracy.

Every edit is in `data/metadata/normalization_changes.jsonl`. The original source files remain unchanged in `data/source_release/`. This working normalization is a documented custom evaluation version; its scores must be compared against baselines using the same version.

One Hybrid final-test task remains in `data/metadata/quality_holds.json`: its checks do not fully match the requested workflow and include a questionable remaining-open-case threshold. The numeric type was normalized, but no threshold or new SQL was invented. Keep the task in the frozen membership and resolve the scorer before a complete final claim. Do not silently drop it from the denominator or treat the other 328 tasks as semantically certified.

The detailed result is `reports/dataset_audit.md`: **static checks pass with quality caveats**. Backend tool behavior, live SQL execution and full semantic feasibility remain unverified. This is a workflow-family split within familiar synthetic environments, not proof of unseen-organization generalization or foundation-model decontamination.

**Fine-tuning data are a separate stage**

`data/task_inputs/train.jsonl` contains questions, policies and tool names. It has no successful assistant targets. Generate real, complete training-only trajectories in the actual benchmark environment, retain tool schemas/results, verify outcomes, and record external review receipts. Never fabricate receipts just to satisfy a schema. The preparation code checks provenance binding but does not independently execute the environment or authenticate the reviewer.

`scripts/prepare_sft.py` accepts only the 128 frozen training IDs, accepted reviews and matching verifier receipts. It validates native tool conversations, the actual pinned Qwen tokenizer, assistant-only labels, original prompt equivalence and length limits. It rejects overlong or incomplete traces instead of truncating required evidence. The first recipe uses one complete trajectory per task; a different windowed recipe needs a separately validated preparation contract.

The Modal launcher uploads only the prepared training tokens, their manifest and training template. It does not mount final-test questions, evaluator SQL or source database dumps in the training worker. Folder names alone do not enforce OS-level isolation on this local machine.

**Modal and the $40 limit**

The Function requests one `A100-80GB`, four **physical** CPU cores and 16 GiB host RAM. Modal counts one physical core as two vCPUs. At the checked Function rates:

`(.000694 + 4 × .0000131 + 16 × .00000222) × 3600 = $2.814912/hour`

This replaces the earlier assumed $2.77/hour for actual Modal planning. The $27.70 compute envelope buys at most about 9.84 hours at the requested rate, before other compute charges or overruns. CPU and RAM can be billed above requests; explicit limits are set, and the provider usage limit remains the outer guardrail.

The whole campaign remains capped at $40: $10 external teacher/API costs, $27.70 GPU compute reservations and $2.30 other Modal charges. Configure a workspace **gross usage** allowance consistent with the remaining $30 Modal share before paid work; a net spend limit after credits is a different control. Other jobs and prior monthly usage must be accounted for. No cap has been configured remotely by this workspace.

Local call reservations are conservative: one chunk reserves $3.34 for its maximum execution/startup/tail allowance. Completed or interrupted calls do not automatically refund that reservation. Reconcile against actual bills before reclaiming it. Save and transfer the ledger when switching accounts. A timer or `retries=0` alone is insufficient: Modal can restart preempted containers, and startup time is separately bounded.

The runtime uses one container, persistent Volumes, an absolute per-invocation deadline, checkpoint saves at optimizer boundaries, and a local ledger. These reduce accidental overspend and lost progress, but do not replace provider billing controls or establish that the full experiment will finish under $40.

**What has been tested**

Local tests cover raw-task rejection before GPU imports, split and receipt checks, masking/padding, token-weighted accumulation, checkpoint completeness/tampering, atomic publication, interrupted-save quarantine, portable import/export, indexed scoring, and budget refusal. A real pinned tokenizer smoke check passed on a clearly synthetic tool conversation. That fixture is not part of the training data.

The Modal app declaration imports with SDK 1.5.5 without a cloud call. Linux training dependency metadata and APIs were reviewed and pinned. The CUDA image build, A100 load, fused-kernel execution, full training, Modal persistence and cross-account resume have not yet been exercised on cloud hardware. Runtime assertions deliberately fail if architecture, package versions, trainable parameters or the fused-loss path differ.

See `reports/validation_summary.json` for the final local check record and `reports/training_stack.md` for compatibility details.

Sources: [dataset](https://huggingface.co/datasets/ServiceNow-AI/EnterpriseOps-Gym), [Modal pricing](https://modal.com/pricing), [resource semantics](https://modal.com/docs/guide/resources), [budget semantics](https://modal.com/docs/guide/budgets), [persistent Volumes](https://modal.com/docs/guide/volumes).
