# Static audit of the329task release

Status: **STATIC_CHECKS_PASS_WITH_QUALITY_CAVEATS**. Audited329 task specifications; no API/GPU/Docker/model runs or SQL execution. Sources and membership were not changed.

- Roles: {'train': 128, 'development': 41, 'final_test': 160}.
- Verifier entries: 1749; distinct selected tool names: 306.
- SQL parser: sqlglot 30.6.0, SQLite dialect; results: {'parsed': 1749}.
- Structural/error findings: 0; warning occurrences: 1.

## Actionable findings

| Finding | Count | Required action |
|---|---:|---|
| Tasks with repeated verifier names |0|Evaluate by task ID + stable zero-based verifier index, never a name-keyed dictionary.|
| Entries overwritten by name-keying |0|Retain every original verifier entry; this loses 0 distinct normalized checks.|
| Tasks losing nonidentical named checks |0|Treat this as a scoring correctness issue, not cosmetic duplication.|
| Redundant normalized-check entries |226|Keep immutable checks; disclose duplicate weighting in diagnostic verifier rates.|
| Tasks with incompatible same-query constraints |0|Curator review is required before a claim that these tasks can pass. No replacement targets inferred.|
| SQL parser failures |0|Check actual SQLite compilation and intended schema; parser rejection alone is not proof of a server bug.|

## Concrete errors and review warnings

Frozen-source normalization candidates: 44 exact field edits, enumerated with original/replacement values in the curator-only JSON report. They are not applied by this script.
- `semantic_verifier_alignment_unresolved` — `task_20260115_154856_907_1628b966_275e920f`: Source task requests an open-case overview, a specific case closure/reassignment, and spreadsheet content/name/description. Current checks cover active account count, remaining open-case count greater than1, and spreadsheet name/MIME only. They do not verify the requested case mutation or spreadsheet fields/content/description. The remaining-case threshold is not established by the user request and disagrees with the verifier description at least one.
No malformed required fields, empty queries, broken gym references, invalid role quotas, or detected cross-role audited-family leakage were found.

## What remains unverified

The329 tasks are structurally present. This audit cannot certify that all are semantically clean or executable. Live tool catalogs, per-task reset/isolation, SQL schema/result shape, task/verifier agreement, and final-state completeness still require controlled environment validation. No successful SFT demonstrations have been created.

The curator-only verifier inventory assigns stable IDs and records hashes, parser results, table names, and duplicate relationships. It deliberately omits source SQL text and expected values. Do not pass inventory or evaluator-only files to the agent.

## Reproduce

```bash
python3 MODAL/scripts/audit_dataset.py
```

For normalized working files, add `--payload-root MODAL/data`. The script validates every recorded mechanical transformation and unchanged full records against the immutable source.

Optional SQL parsing dependency: `sqlglot==30.6.0`. Without it, the script explicitly reports SQL parsing unverified. All other checks use the standard library.

Detailed findings and task/verifier identifiers are in `dataset_audit.json`; no record corrections were applied.
