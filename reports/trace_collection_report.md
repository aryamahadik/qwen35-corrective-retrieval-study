# Training trace collection report

Status: **COLLECTION CLOSED — PARTIAL CORPUS, NOT READY FOR TRAINING**

The frozen 128-task training split is fully dispositioned: **57 real, independently
reviewed demonstrations were accepted** and **71 tasks are on evidence-backed quality
hold**. There are no unaccounted training tasks and no accepted/hold overlap. The
requested 128 accepted demonstrations were therefore **not** achieved, and this
report does not represent the partial corpus as complete or training-ready.

Development and final-test payloads were not used for solver generation. Modal,
GPU jobs, production accounts, and external teacher APIs were not used or changed.

## Final disposition

| Domain | Frozen tasks | Accepted | Quality holds |
|---|---:|---:|---:|
| Calendar | 8 | 2 | 6 |
| CSM | 24 | 12 | 12 |
| Drive | 8 | 2 | 6 |
| Email | 8 | 5 | 3 |
| HR | 24 | 9 | 15 |
| Hybrid | 24 | 6 | 18 |
| ITSM | 24 | 18 | 6 |
| Teams | 8 | 3 | 5 |
| **Total** | **128** | **57** | **71** |

Every accepted task has exactly one published trace and one bound schema-v2
verifier receipt. The 71 holds are recorded individually in
`data/collection/quality_holds.jsonl`, including attempt IDs, the observed reason,
and required remediation. Major hold classes are:

- missing or contradictory required user inputs, identities, roles, and tool coverage;
- visible policy conflicts that a faithful solver may not bypass;
- pinned backend schema, persistence, authorization, and serialization failures;
- brittle hidden IDs, insertion order, text literals, or verifier cardinalities;
- task/verifier semantic conflicts and false-positive verifier results rejected by
  independent review.

One originally accepted Calendar attempt remains sealed as raw evidence but was
revoked and removed from publication. Its revocation is preserved under
`data/collection/revocations/`. This explains why raw terminal state contains 54
`ACCEPTED` attempts while the effective corpus contains 57.

A final recovery audit corrected two cross-task reviewer errors and accepted fresh
CSM executions for those tasks. A trusted executor adapter also normalized three
misnamed authentication headers without changing their frozen token values; this
recovered one Calendar task and exposed two deeper, now-documented contract/policy
defects. The normalization names are recorded in privileged hash-chained attempt
evidence and are never model-visible. Separate live `/api/user-info` attestations
also disproved suspected HR and ITSM identity mismatches. The ITSM task was recovered;
the HR attempts exposed an independent visible-policy/verifier text conflict instead.

## Attempts and runtime evidence

- Raw attempt states: **182** total — 58 `ACCEPTED`, 110 `ATTEMPT_FAILED`,
  10 `REVIEW_REJECTED`, and 4 `BLOCKED_BACKEND`.
- **171** attempts have complete setup-to-finish timestamps totaling 32,535.3 seconds
  (mean 190.3 seconds). Infrastructure-only setup failures and incomplete timing
  records are excluded from that duration calculation.
- All seven pinned Linux/AMD64 images were pulled and exercised locally by digest.
  Services were loopback-only, ephemeral, log-disabled, capability-dropped,
  `no-new-privileges`, memory/CPU limited, and normally restricted to one domain or
  the required Hybrid pair. All collection containers were stopped at closeout.
- All 39 training seed files matched their recorded size and SHA-256. Fresh database
  IDs were used per attempt and cleanup status was recorded.
- Live catalogs were captured from the pinned servers. Every selected tool across
  the 128 training tasks existed, and selected Hybrid tool names had no routing
  collisions.
- Solver agents received only a per-attempt solver bundle and the step gateway.
  Verifier contracts, seed SQL, prior attempts, and hidden expected values were not
  supplied to retry solvers. This is a procedural isolation boundary; no OS-level
  filesystem sandbox is claimed.
- `scripts/local_collection_harness.py` records exact assistant messages, real MCP
  calls/results, JSON-RPC/session evidence, database lifecycle, indexed verifier
  outcomes, cleanup, reviews, and publication in hash-chained immutable attempt logs.
  Executor database IDs and authentication tokens are redacted from model-visible
  results while raw wire responses remain in privileged attempt evidence.

Provider usage and price are **unknown, not zero**: all 182 attempt states record
`unknown_provider_cost_not_reported`, with null usage and cost fields. No configured
external API key, paid teacher request, Modal call, GPU job, or training job was
initiated by the collector. The Codex collaboration runtime did not expose a billable
token/cost ledger, so absence of a local spend record is not proof of zero account
spend.

## Validation and leakage checks

- All **57/57** published traces pass `prepare_sft.validate_trace` individually
  against the exact frozen training input and normalized verifier contract.
- All 57 receipt files are present, schema-v2, all-checks-passed, and SHA-bound to
  their corresponding canonical task, verifier list, and model-visible payload.
- Task IDs are unique across traces and holds; accepted intersection holds is empty,
  and accepted union holds equals all 128 frozen training IDs.
- Published source IDs are training-only. Canonical system/user prefixes exactly
  match `data/task_inputs/train.jsonl`; no development or final-test task membership
  appears in the corpus.
- Exact per-attempt executor database IDs and authentication-token values do not
  occur in any published trace. Redaction markers remain where redaction was
  exercised; they do not contain the secret value.
- Full CPU test result: **85 passed**, plus **18 subtests passed**. The only warning
  is the environment's unrecognized `asyncio_mode` pytest option.
- `foundation_check.py --json` reports integrity passed but correctly returns
  `NOT_READY_MISSING_ARTIFACTS`, because 71 accepted workflows and prepared training
  artifacts are absent.
- `prepare_sft.py --validate-only` correctly refuses publication with:
  `Missing reviewed training workflows: 71 of 128`.

The frozen planning queue/collection manifest still says `NOT_COLLECTED` for all
tasks. It is retained as an immutable planning/source artifact and must not be read
as live campaign status; this report, reviewed traces, receipts, holds, revocation,
and raw attempts are the live collection evidence.

## Token audit

The pinned Qwen3.5 tokenizer and reviewed template render all 57 complete traces with
valid prefix equivalence and assistant masks:

- total processed tokens: **607,327**;
- supervised assistant tokens: **46,057**;
- five traces exceed 16,384 tokens: **16,612**, **18,544**, **22,999**,
  **27,740**, and **35,906** tokens;
- one accepted trace exceeds the repository's supported 32,768-token maximum:
  `task_20260106_151754_319_d4a463c3_41f0af13` at **35,906** tokens.

No trace was truncated. The over-32K row remains accepted as execution evidence but
is explicitly recorded in `data/collection/preparation_holds.jsonl` and is not
training-ready under the current worker/preparer contract. The other four long rows
are also recorded there as requiring a reviewed 32K preparation policy rather than
the current 16K default. A fresh visible-only replacement attempt for the >32K task
was also collected: it chose a different, plausibly relevant installed product,
failed all frozen checks, and still rendered to 33,969 tokens, so it was not used to
supersede the accepted trace.

## Integrity hashes

Hashes below bind the final campaign artifacts at closeout (SHA-256):

| Artifact | SHA-256 |
|---|---|
| Frozen split manifest | `1742388aa1c1fe079de568183e6f6cd11cf0ac95265a753695b6a08f3a55094c` |
| Canonical training inputs | `bf8927ea678049ea7e68aecd7dd8047a68b8fd194634d4d9fd311599a548f6b4` |
| Normalized training verifier contracts | `4e6fbcb99f2a06e456a27b26b819bfa85cf876e8006a30fa5ef2cfcb0e3662c8` |
| Reviewed traces | `b5510526e25352c33d3c006e5e504ce3102c188159946dcd56cab07dc49a0155` |
| Quality holds | `4db4b67b42d83d2bb969e76c02c119156f2e057ea94713fea0d7b4a02e0afb57` |
| Preparation holds | `24b84e932d34d6ffc54afba10a6a2a8144211e02024672a9a0d345ecd328869e` |
| Sorted receipt filename/hash manifest | `fd5922f1435af437019c72565fdb21c978f05f45e4e4fc3d4890944a2ea5f061` |
| Collection harness | `7dee047dead2454e8243d345ad65bd820e4f04ebeaa4cf34978531b66c926121` |
| Harness tests | `f09ce67002cde45d907cc3c36b34f61032137d95dc71b2f314e6af54d9e4a8e3` |

## Required next work

This partial corpus must not be submitted to training as the requested 128-row
foundation. Completing it requires resolving the 71 recorded task/backend/policy/
verifier holds, recollecting those tasks with fresh isolated solvers, and rerunning
the same independent review and validation. Separately, the 35,906-token trace needs
a reviewed over-32K strategy or a new faithful shorter execution; silent truncation
is prohibited.

The retained final-test semantic scorer hold remains separate and untouched.
