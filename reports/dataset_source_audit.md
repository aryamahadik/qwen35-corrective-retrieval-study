# Static audit of the329task release

Status: **STRUCTURAL_ERRORS_REVIEW_REQUIRED**. Audited329 task specifications; no API/GPU/Docker/model runs or SQL execution. Sources and membership were not changed.

- Roles: {'train': 128, 'development': 41, 'final_test': 160}.
- Verifier entries: 1749; distinct selected tool names: 306.
- SQL parser: sqlglot 30.6.0, SQLite dialect; results: {'parsed': 1749}.
- Structural/error findings: 44; warning occurrences: 173.

## Actionable findings

| Finding | Count | Required action |
|---|---:|---|
| Tasks with repeated verifier names |48|Evaluate by task ID + stable zero-based verifier index, never a name-keyed dictionary.|
| Entries overwritten by name-keying |264|Retain every original verifier entry; this loses 40 distinct normalized checks.|
| Tasks losing nonidentical named checks |14|Treat this as a scoring correctness issue, not cosmetic duplication.|
| Redundant normalized-check entries |226|Keep immutable checks; disclose duplicate weighting in diagnostic verifier rates.|
| Tasks with incompatible same-query constraints |0|Curator review is required before a claim that these tasks can pass. No replacement targets inferred.|
| SQL parser failures |0|Check actual SQLite compilation and intended schema; parser rejection alone is not proof of a server bug.|

## Concrete errors and review warnings

Frozen-source normalization candidates: 44 exact field edits, enumerated with original/replacement values in the curator-only JSON report. They are not applied by this script.
- `duplicate_tool_names` — `task_20251203_091910_549_bca89e7d_de59e44a`: Tool names repeat within a task list.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0003`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0004`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0005`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0006`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260107_162554_472_accab84d_41d2e871::v0007`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260108_041838_219_df0ecdeb_3f8c0642::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260108_041838_219_df0ecdeb_3f8c0642::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260108_041838_219_df0ecdeb_3f8c0642::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260116_080150_885_1628b966_5a58d8e3::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260116_080150_885_1628b966_5a58d8e3::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_150447_596_1afb323a_0a1e4085::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_150447_596_1afb323a_0a1e4085::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_150447_596_1afb323a_0a1e4085::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_150447_596_1afb323a_0a1e4085::v0003`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `duplicate_tool_names` — `task_20251203_142634_160_bca89e7d_193f597f`: Tool names repeat within a task list.
- `duplicate_tool_names` — `task_20251223_064316_340_01395ded_9c6f3e01`: Tool names repeat within a task list.
- `count_expected_string` — `task_20260106_071510_179_911d75d7_0ae789ae::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260106_071510_179_911d75d7_0ae789ae::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `duplicate_tool_names` — `task_20260107_202437_273_911d75d7_89789b9a`: Tool names repeat within a task list.
- `duplicate_tool_names` — `task_20260107_212831_019_911d75d7_d1212b63`: Tool names repeat within a task list.
- `duplicate_tool_names` — `task_20260109_043327_590_806f1a83_d690097e`: Tool names repeat within a task list.
- `count_expected_string` — `task_20260113_152354_165_9a1e131b_fc5e2cac::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260113_152354_165_9a1e131b_fc5e2cac::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260113_152354_165_9a1e131b_fc5e2cac::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260114_124106_138_1628b966_ddc2587a::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260114_124106_138_1628b966_ddc2587a::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `duplicate_tool_names` — `task_20260115_034527_380_66392a82_a172d90d`: Tool names repeat within a task list.
- `count_expected_string` — `task_20260115_154856_907_1628b966_275e920f::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260115_154856_907_1628b966_275e920f::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260115_154856_907_1628b966_275e920f::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260117_084409_361_4d9df647_9892db8c::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260117_084409_361_4d9df647_9892db8c::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260117_084409_361_4d9df647_9892db8c::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260117_084409_361_4d9df647_9892db8c::v0003`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260117_084409_361_4d9df647_9892db8c::v0004`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_161936_323_cbcf38f8_50ccd164::v0000`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_161936_323_cbcf38f8_50ccd164::v0001`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_161936_323_cbcf38f8_50ccd164::v0002`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_161936_323_cbcf38f8_50ccd164::v0003`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `count_expected_string` — `task_20260121_161936_323_cbcf38f8_50ccd164::v0004`: Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.
- `semantic_verifier_alignment_unresolved` — `task_20260115_154856_907_1628b966_275e920f`: Source task requests an open-case overview, a specific case closure/reassignment, and spreadsheet content/name/description. Current checks cover active account count, remaining open-case count greater than1, and spreadsheet name/MIME only. They do not verify the requested case mutation or spreadsheet fields/content/description. The remaining-case threshold is not established by the user request and disagrees with the verifier description at least one.

## What remains unverified

The329 tasks are structurally present. This audit cannot certify that all are semantically clean or executable. Live tool catalogs, per-task reset/isolation, SQL schema/result shape, task/verifier agreement, and final-state completeness still require controlled environment validation. No successful SFT demonstrations have been created.

The curator-only verifier inventory assigns stable IDs and records hashes, parser results, table names, and duplicate relationships. It deliberately omits source SQL text and expected values. Do not pass inventory or evaluator-only files to the agent.

## Reproduce

```bash
python3 MODAL/scripts/audit_dataset.py
```

Optional SQL parsing dependency: `sqlglot==30.6.0`. Without it, the script explicitly reports SQL parsing unverified. All other checks use the standard library.

Detailed findings and task/verifier identifiers are in `dataset_audit.json`; no record corrections were applied.
