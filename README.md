# EnterpriseOps Dataset Foundation

This copied ECHO `Modal/MODAL` folder is the working location. **Modal preparation and cloud execution are deferred**; the existing platform code is preserved for later manual review. Read `PHASE.md` for the current scope.

Start with:

```bash
python3 scripts/foundation_check.py
```

The checker distinguishes verified foundation files from actual training readiness. `NOT_READY` is the correct result while real demonstrations are missing.

| Foundation item | Current state |
|---|---|
| Selected tasks | 329 specifications: 128 train, 41 development, 160 test |
| Source, membership and working normalization | Preserved; checked by hashes and normalization replay |
| Training collection queue | 128 tasks, 105 audited workflow groups, 754 required checks |
| Training seed SQL | 39 pinned files present inside this folder |
| Backend images | Seven published image digests recorded; no containers started |
| Tokenizer | Local pinned assets and tokenizer-only environment; no model weights |
| Verified demonstrations | 0 collected |
| Actual training token count | Unknown until complete accepted traces exist |
| Known final-test issue | One semantic scorer hold, retained in membership |
| Platform work | Deferred; no paid cloud or teacher-generation job launched |

**Where things are**

- `data/source_release/`: unchanged original task release.
- `data/task_inputs/`: cleaned policies, requests and selected tool names.
- `data/evaluator_only/`: privileged runner and SQL verifier contracts.
- `data/metadata/`: frozen IDs, source hashes, family groups and quality holds.
- `data/collection/`: deterministic training-only queue and separate verification requirements.
- `data/environment/`: pinned source archive, 39 training seed files and server-image identities.
- `data/tokenizer/`: local pinned tokenizer files and provenance manifest.
- `data/sft/`: future real reviewed traces and prepared tokens; currently no training corpus.
- `reports/foundation_audit.md`: current integrity and readiness report.
- `reports/training_collection_plan.md`: complete collection procedure.
- `RUNBOOK.md`: active local workflow.
- `docs/DEFERRED_MODAL_RUNBOOK.md`: previous platform notes, preserved for later.

**What a valid demonstration must satisfy**

Use one of the exact 128 training IDs, the canonical task policy and user request, and its selected tool-name set. Actual parameters/schemas still need a live verified tool catalog. Accepted reviews and receipts must bind the exact task input, model-visible conversation and normalized verifier contract. Every required verifier index/name must appear once with a real passing result and no error. A claimed pass count alone is insufficient.

The preparer checks complete tool call/result ordering, original Qwen prompt rendering, assistant-only loss masks and length. It uses this folder's verified tokenizer assets with no network/home-cache fallback. Overlength traces are rejected rather than truncated. A windowed recipe needs its own reviewed contract.

Checks can catch mistakes and changed evidence; they do not authenticate a dishonest review or independently execute the environment. Never create accepted statuses, receipts or successful tool results merely to make validation pass.

**Still required before training**

1. Start and validate the actual local backend, tool catalog and reset behavior. Docker and all seven server ports were unavailable during the read-only check.
2. Collect complete real trajectories for the 128 training tasks, recording failures and usage.
3. Execute all required indexed checks and independently review policy/goal completion.
4. Prepare tokens and calculate cost from the real corpus.
5. Later, write/review the Modal code together and run a measured GPU smoke test.

The existing campaign limit is $40. No paid execution was started in this phase. The preserved platform files are tracked in `work/deferred_modal_files_sha256.json` and remain unchanged. Structural integrity is checked; a perfect dataset, complete semantic correctness or frontier accuracy is not claimed.
