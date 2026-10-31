# Local Foundation Workflow

Work only in `/Users/aryamahadik/Documents/ECHO Architecture/Modal/MODAL`. Platform preparation is deferred; previous instructions are preserved in `docs/DEFERRED_MODAL_RUNBOOK.md`.

**Check the foundation**

```bash
python3 scripts/foundation_check.py
python3 scripts/environment_doctor.py
python3 scripts/build_collection_queue.py --check
```

The first command returns exit code 2 / `NOT_READY` while actual execution evidence or demonstrations are missing. It does not allocate a GPU, start Docker, run SQL or call a teacher. A listening port is not a verified tool server.

The seed assets and image identities are inside this folder, with hashes in `data/environment/source_manifest.json` and `image_manifest.json`. Server bindings are in `config/local_environment.json`. Start only the services needed by the current task when beginning real local collection; Hybrid tasks can need several. Runtime schemas, actual tools and reset behavior have not yet been validated.

**Collect actual training traces**

Read `reports/training_collection_plan.md`. `data/collection/task_index.jsonl` orders all 128 training tasks, covering each of the 105 audited groups before repeating relatives. Every row is `NOT_COLLECTED`.

The teacher receives only the canonical training policy/request and actual permitted tool schemas. The executor/reviewer keeps seeds, administration and SQL checks separate. Record observed tool calls/results, model output, revisions, token usage and costs. Preserve failures; do not splice outputs from different resets into one supposed successful run.

Use `config/trace_schema.json` and `config/verifier_receipt.schema.json`. Receipt version 2 requires exact canonical task-input binding and every indexed verifier outcome. Old summary receipts cannot be upgraded by inventing the missing outcomes; recover actual results or rerun verification.

Store real reviewed conversations at `data/sft/reviewed_traces.jsonl` with actual receipt files beside them. Queue records are requirements, not receipts. Validate them locally:

```bash
python3 scripts/prepare_sft.py --traces data/sft/reviewed_traces.jsonl --validate-only
```

**Prepare tokens only after the corpus is accepted**

The `.venv-prepare` environment contains pinned tokenizer libraries, without model training packages. `data/tokenizer/model` contains pinned assets checked by the adjacent manifest.

```bash
.venv-prepare/bin/python scripts/prepare_sft.py --traces data/sft/reviewed_traces.jsonl --output-dir data/sft/prepared
```

The preparer uses local files only. Incorrect policies, missing/extra tools, incomplete results, inconsistent receipts, malformed masks or overlength traces cause refusal. The initial recipe accepts one complete trajectory per training task. Do not remove necessary information to force it into 16K; review any windowed recipe separately.

Count real processed and supervised tokens after preparation. They are not the same as the number of source tasks. The $40 cap includes any future teacher attempts, retries, training, evaluation and storage. No Modal login or deployment is needed for this foundation phase.

The known Hybrid final-test scorer mismatch is separate from the 128 training tasks. It must be resolved before a complete final evaluation; do not silently delete it or use final-test feedback to curate training.

**Run local tests**

```bash
mkdir -p work/test-tmp
TMPDIR="$PWD/work/test-tmp" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Synthetic fixtures are never training data. Passing local tests does not establish live task execution, backend correctness or GPU compatibility.
