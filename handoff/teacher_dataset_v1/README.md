# Teacher Dataset Handoff

This package contains the **128 frozen training tasks only**. It excludes all development tasks, final-test tasks, seed databases, environment administration, SQL verifiers, expected answers, and gold solutions.

Use `teacher_tasks.jsonl` as the primary dataset. Tasks are sorted by `queue_order`; the first 105 cover one representative from each audited workflow family before related tasks repeat. The same tasks are also separated by domain under `by_domain/`.

Each row contains:

- `queue_order`, `coverage_phase`, and `workflow_group_id` for collection order;
- the canonical `task_id`, `domain`, `system_prompt`, and `user_prompt`;
- names of permitted and restricted tools;
- a stable input hash and an initial `NOT_COLLECTED` status.

The tool names are not complete callable schemas. The collecting agent must obtain the real schemas and execute the tools in the benchmark environment. It must record actual calls and actual tool responses. It must never invent a successful result.

Write accepted conversations using `trace_schema.json`. Verification receipts are created separately by the trusted executor/reviewer using `verifier_receipt.schema.json`; hidden verifier data must not be shown to the teacher model.

Start with five tasks. If the agent cannot access the local benchmark environment or Docker, it should stop and report that limitation rather than fabricate traces.

The package is a collection input, not a finished SFT dataset. At creation time it contains zero verified demonstrations.
