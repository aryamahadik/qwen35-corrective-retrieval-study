# Current phase: dataset foundation

Work only in this copied folder:

`/Users/aryamahadik/Documents/ECHO Architecture/Modal/MODAL`

Modal authentication, deployment, GPU execution, training-worker changes and cloud configuration are deferred. The existing Modal code is historical preparation; it has not been deployed or validated on an A100. The user intends to write/review that code manually together later.

Current work is the local foundation: preserve the frozen split and source files; validate the cleaned task data; prepare training-only environment assets and collection queues; require real, complete, independently reviewed tool trajectories; bind reviews to exact policies, tools and all required checks; and tokenize without corrupting labels or truncating required facts.

The selected task pool remains 329 specifications: 128 train, 41 development, 160 test. Task specifications are not demonstrations. Neither setup, source checks, synthetic unit tests nor an accepted-status field establishes that an enterprise workflow succeeded.

Use `python3 scripts/foundation_check.py` as the entry point. A `NOT_READY` result with missing real traces is correct until those traces and their verifier receipts exist. It must not be bypassed or relabeled as ready.

The campaign spending limit remains $40. No new paid calls or cloud jobs are needed for this local foundation work. Preserved Modal files are tracked in `work/deferred_modal_files_sha256.json` to confirm they are unchanged.
