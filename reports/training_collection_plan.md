# Training demonstration collection plan

The training-only queue is prepared: **128 tasks, 105 audited workflow groups, 754 required verifier entries**. Every task is **NOT_COLLECTED**. No teacher call, environment execution, receipt, successful demonstration or token count was produced by this work. Platform preparation and GPU work are deferred.

## Files and boundaries

| File | Purpose |
|---|---|
| `data/task_inputs/train.jsonl` | Canonical cleaned training policies, requests and declared tool names. This remains the sole task-input source. |
| `data/collection/task_index.jsonl` | Operator queue: task ID, domain, workflow group, stable queue order, required tool names, source line/hash and collection status. It contains no task solutions. |
| `data/collection/evaluator_receipt_requirements.jsonl` | Executor/reviewer-only contract hashes, exact verifier counts and required indices. These are requirements, **not completed receipts**. |
| `data/collection/domain_collection_plan.json` | Domain coverage, declared tool inventory and collection considerations. |
| `data/collection/collection_manifest.json` | Source and artifact SHA256 hashes, collection scope and readiness status. |
| `scripts/build_collection_queue.py` | Deterministically rebuilds or checks this plan, without a model, backend, SQL or cloud call. |

The administrative queue, contract metadata, evaluator records and domain plan are not model input. Fetch a canonical **training** input by task ID, verify its recorded `input_sha256`, and pass only its allowed system/user context plus the actual selected tool schemas to the teacher. Do not serialize an entire queue or evaluator record into a prompt. Folder separation alone is not an operating-system access boundary.

`input_sha256` hashes the six-field source input object. The verifier contract hash hashes the complete normalized `verifiers` **list**, preserving order and every check. Both use sorted JSON keys, compact separators, UTF8 with `ensure_ascii=False`, and no NaN. A later `model_visible_sha256` hashes `{messages, tools}` from the actual recorded conversation; it is a different hash and cannot be filled in before a trace exists.

## Coverage and queue order

| Domain | Training tasks | Audited groups | Required verifier entries | Declared distinct tool names |
|---|---:|---:|---:|---:|
| Calendar | 8 | 7 | 42 | 16 |
| CSM | 24 | 22 | 155 | 54 |
| Drive | 8 | 8 | 51 | 26 |
| Email | 8 | 8 | 32 | 30 |
| HR | 24 | 21 | 198 | 54 |
| Hybrid | 24 | 22 | 110 | 84 |
| ITSM | 24 | 10 | 113 | 40 |
| Teams | 8 | 7 | 53 | 25 |
| **Total** | **128** | **105** | **754** | **Not additive across domains** |

The first105 queue positions cover one representative per audited workflow group. The remaining23 positions cover the other members. Within each phase, domains are interleaved in alphabetical round-robin order; selection within groups is deterministic. This avoids starting with many related ITSM variants while other workflows remain untested. It is a coverage order, not an estimate of task difficulty or a prediction of model performance.

All128 frozen training IDs are retained. No development/test/reserve task is added. Workflow groups are a bounded source audit, not proof of exhaustive semantic independence. Shared synthetic environments and other correlations remain.

## Teacher instructions for each real attempt

1. Receive the exact authorized task system prompt and user request. Keep original dates, identity, policies and conditionals. Do not replace a request with a manufactured “solved” version.
2. Receive the actual tool schemas from the pinned environment registry, filtered to the task's selected/restricted tool policy. The queue stores names only; names are not sufficient to invent parameters or claim a live tool exists.
3. Resolve records through real tool calls. Use only returned IDs, contents and observations. Follow the permitted system policy if a user request conflicts with it.
4. Perform the complete workflow, recording every assistant call and actual tool response in order. If a tool fails, preserve its failure. Do not substitute an imagined successful result or an answer copied from another task.
5. Stop with an honest final response based on observed outcomes. An initiated call does not mean people spoke; a submitted update does not mean it succeeded; a created draft is not a sent email.
6. Never receive or consult verifier SQL, expected state/value, seed database dumps, hidden administrative endpoints or another task's answer. Do not expose hidden checks through retry hints. Do not request inaccessible private reasoning from a teacher; retain only permitted, actually supplied output and useful visible rationale.

These collection instructions guide the harness/operator. They must not silently override or replace the benchmark's supplied system policy. The model-visible transcript must accurately reflect the messages and tool schemas the teacher actually received.

## Executor and reviewer instructions

1. Select the next eligible training-only queue ID. Read its canonical input and matching evaluator contract separately. Verify the input hash and complete verifier-list hash before executing anything.
2. Use the actual benchmark backend with the task's configured identity and a fresh isolated reset. The trusted executor may load hidden environment configuration to start the sandbox; the teacher may not inspect it. Hybrid tasks require the necessary domains to be reset consistently.
3. Resolve the live tool registry and record its revision and exact visible schemas. If the backend, tool, schema, permission context or reset mechanism is unavailable, record **BLOCKED_BACKEND** as an actual attempt outcome. This queue does not establish backend readiness.
4. Record a raw append-only attempt trace with a unique attempt ID, teacher/model settings, generator/environment revisions, tool calls/results, final assistant response and provider-reported usage. Capture unknown usage as unknown, not zero. Record failed attempts and costs as well as accepted ones.
5. After the attempt, run every declared verifier in the isolated final state, keyed by stable zero-based verifier index. Missing, duplicate, errored or unexecuted checks cannot produce success. Never collapse checks by name or discard redundant entries. `scripts/strict_verifier_results.py` aggregates supplied outcomes; it does not execute the SQL or prove the environment exists.
6. Review the whole task against its policy and observed trace as well as the checks. A passing but incomplete scorer is not enough to certify a faithful demonstration. If a training task reveals an alignment or feasibility issue, record a quality hold and stop collection for that task; do not silently rewrite its query, threshold, membership or answer.
7. Only an actual accepted run may receive a receipt reporting `status="passed"` and matching `checks_total`, `checks_passed`, full verifier contract hash, canonical task-input hash, verifier revision, complete indexed check outcomes and exact model-visible trace hash. A reviewer then binds that receipt file/hash to the trace and records the reviewer, timestamp and isolation attestation. Hashes detect changed content; they do not authenticate a dishonest producer.
8. Preserve failed attempts separately. For the initial SFT corpus select one complete accepted trajectory for every one of the128 training tasks. Do not splice successful fragments from different resets into a supposed single observed run.

Follow the existing `config/trace_schema.json` and `config/verifier_receipt.schema.json` for accepted artifacts. `data/collection/evaluator_receipt_requirements.jsonl` deliberately has no successful status, observed passed count, trace hash or verifier revision; copying it into an “accepted” receipt would fabricate evidence.

## Progress and token accounting

The deterministic plan is not a live result database. Store attempt events and their immutable raw files separately, for example under `data/collection/attempts/`, and reference them from a collection-progress record. Suggested observed outcomes are **BLOCKED_BACKEND**, **ATTEMPT_FAILED**, **RECORDED_PENDING_REVIEW**, **REVIEW_REJECTED**, **QUALITY_HOLD** and **ACCEPTED**. Only actual executor/reviewer events should change these states. The queue builder refuses to reset task-index rows whose status or artifact paths have been changed from the initial uncollected state.

Measure complete rendered conversation tokens after collection: system policy + tool schemas + user request + tool history + actual assistant reasoning/calls/final answer. No such lengths are currently known. The existing first preparation contract accepts one complete trajectory per task and rejects sequences exceeding16,384 tokens; it does not truncate essential observations or create independent examples by splitting a task. A later windowing/compaction recipe requires a separate, reviewed contract before use.

Count unique tasks, groups, attempts, accepted episodes, processed tokens, supervised assistant tokens and billed tokens separately. Extra attempts consume budget without increasing the unique-task count. The existing campaign authorization remains$40 overall, with a$10 external-teacher/API envelope; no paid work is initiated by this plan. Whether128 complete accepted trajectories fit that envelope is unknown until actual usage and failure rates are observed.

## Reproduce and check locally

```bash
python3 scripts/build_collection_queue.py
python3 scripts/build_collection_queue.py --check
```

The builder checks exact training membership, exclusions, six input fields, input/evaluator agreement, normalized source-file hashes, nonempty uniquely identified verifier lists, training workflow-group coverage and training quality holds. It opens no development or final-test payload file. The resulting plan has128 unique queue IDs and128 separate receipt-requirement records, all initially uncollected. No source record, frozen membership, verifier semantics or trainer/platform code is changed.
