# E06 compression-ready independent Sol review — Codex instructions

## Task configuration

- **Model:** `gpt-5.6-sol`
- **Reasoning effort:** `xhigh`
- **Mode:** standard/default task mode
- **Fresh task:** required; do not continue the implementation conversation
- **Working directory:** `/Users/omer/workspace/personal/repos/gifted-masking`

This is an independent release-gate review, not an implementation pass. Sol
owns scientific/release judgment. Do not delegate the decision to a subagent.

## Objective

Audit the sealed E06 compression-ready diagnostic-smoke package and decide
whether the exact frozen five-master core standard is safe, reproducible,
scientifically complete, and operationally authorized for a later Terra
execution pass.

Return exactly one release decision:

- `GO_STANDARD`
- `FIX_IMPLEMENTATION`
- `REVISE_SPECIFICATION`
- `NARROW_OR_STOP_CLAIM`

Only `GO_STANDARD` may create
`projects/frontiers_article/approvals/E06_STANDARD_GO.md`. Every other decision
must leave that file absent.

## Absolute prohibitions

Do not:

1. run E06 standard;
2. run E06 qualification;
3. rerun `./scripts/verify.sh`;
4. change model, experiment, validator, fixture, test, config, or CLI code;
5. repair a defect found during review;
6. change seeds, scenarios, grid, horizons, n, bootstrap count, output schemas,
   gzip settings, or resource limits;
7. adjudicate C8 or C9;
8. update the claim ledger, manuscript, figures, or submission files;
9. treat the compression amendment as execution authority;
10. infer a GO from green tests alone.

Read-only checks, small temporary adversarial probes, and fresh non-scientific
fixture/smoke regeneration are allowed. Write temporary outputs only under a
fresh `/private/tmp` directory. Do not overwrite canonical scientific files.

The only permitted repository writes are:

- the independent review checkpoint
  `projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`;
- and, only for a final `GO_STANDARD`, the canonical approval record
  `projects/frontiers_article/approvals/E06_STANDARD_GO.md`.

## Consume completely before deciding

Read these files completely, not selectively:

1. `AGENTS.md`
2. `ARCHITECTURE.md`
3. `projects/frontiers_article/RDS.md`
4. `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`
5. `projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md`
6. `projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`
7. `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`
8. `projects/frontiers_article/approvals/E06_STANDARD_COMPRESSION_AMENDMENT.md`
9. `projects/frontiers_article/E06_STANDARD_READINESS_IMPLEMENTATION.md`
10. `projects/frontiers_article/checkpoints/E06_ROUND2_SOL_SMOKE_REVIEW.md`
11. `projects/frontiers_article/checkpoints/E06_STANDARD_READINESS_IMPLEMENTATION_CHECKPOINT.md`
12. `projects/frontiers_article/checkpoints/E06_STANDARD_COMPRESSION_FIXTURE.json`
13. `projects/frontiers_article/CURRENT_STATE.md`
14. `projects/frontiers_article/BACKLOG.md`
15. the E06 entries in `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`
16. `configs/frontiers_article/e06_m4_paths_smoke.json`
17. `configs/frontiers_article/e06_m4_paths_standard.json`
18. `configs/frontiers_article/e06_m4_hysteresis_qualification.json`
19. `src/gifted_masking/experiments/e06.py`
20. `src/gifted_masking/models/m4.py`
21. `src/gifted_masking/core.py`
22. `src/gifted_masking/cli.py`
23. `tests/test_article_e06.py`

Inspect, rather than trust summaries of:

- `results/manifests/frontiers_m4_path_diagnostics_v1_smoke.json`
- `results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md`
- all eight paths under the manifest's `scientific_artifacts` map;
- `results/reports/e06_compression_preverification/`;
- `results/reports/e06_compression_user_verification/`.

## Required independent audit

### 1. Seal, provenance, and immutability

Independently recompute and verify:

- smoke config normalization and SHA-256;
- compression-amendment SHA-256;
- the complete ordered source-fingerprint map and aggregate fingerprint;
- the sealed package's recorded pre-seal Git HEAD, branch, dirty flag, and
  porcelain hash against the archived pre-seal evidence;
- current post-seal Git drift separately, proving it is limited to seal/status/
  review-instruction records and does not alter source-fingerprinted inputs or
  any scientific artifact;
- all eight scientific artifact byte counts and SHA-256 values;
- `verification.status=passed` and
  `verification.seal_state=external_evidence_verified`;
- full-log SHA-256 `0b516c8eac187da4459e2d81a28a52c817bad802b9a7f9ea94511b72dc7a6e7e`;
- exact exit-record SHA-256
  `e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063`;
- 122 + 1 + 1 + 2 = 126 passing tests and 145.167 seconds reconstructed
  from the archived log, not caller-supplied totals.

The external seal changes only manifest/report seal fields. Confirm it did not
change raw, cells, paths, loops, transitions, effects, PNG, or warnings.

### 2. Model and raw semantics

Audit the standard implementation against the maintained M4 kernel and frozen
specification:

- stable softmax and exact draw order;
- one acceptance draw for every learner, including masking;
- objective reward versus subjective learning reward;
- selected-Q update;
- reward first, then clipped receptivity update;
- p and both Q values inherited or reset exactly by path type;
- km-disabled paths use actual `km=0` while retaining nominal traversal;
- final-window ceiling convention and exact action/outcome/reward
  reconstruction;
- bounded p after every update;
- semantic segment seeds and matched reuse/isolation;
- no change to M4 semantics caused by compression.

### 3. Exact standard dispatch contract

Recompute from the standard config:

- five masters `2026081601` through `2026081605`;
- nine scenarios;
- 26 families per master and 130 total families;
- n=400;
- exactly 52,000 packed rows;
- exactly 913,000,000 learner steps;
- master declaration → scenario declaration → path declaration → child order;
- unique master/scenario/path seed-map keys;
- bootstrap seed `2026081697` and exactly 10,000 complete-master resamples;
- standard raw path ends in `_units.csv.gz`;
- qualification remains unreachable through every standard dispatch path.

Confirm standard authorization fails before directory/file creation for:

- missing GO;
- copied GO at a noncanonical path;
- malformed or duplicate-key binding;
- wrong config path/hash;
- stale source fingerprint;
- changed smoke manifest/hash;
- unsealed smoke;
- wrong command;
- any qualification authorization.

Do not make a valid GO available while testing refusal unless the review has
already completed every other acceptance gate. Prefer synthetic temporary-root
probes.

### 4. Deterministic gzip contract

Independently inspect and test:

- gzip level 9;
- `mtime=0`;
- empty original filename;
- canonical ten-byte header;
- exactly one member;
- no trailing bytes;
- UTF-8 logical CSV with Python `csv` newline behavior;
- deterministic compressed bytes across independent generations;
- separately computed compressed and logical SHA-256/byte counts;
- streamed decompression without full raw materialization.

Adversarial temporary probes must demonstrate rejection of at least:

- non-gzip input;
- altered header/mtime/flags;
- truncation or checksum corruption;
- concatenated members;
- trailing bytes;
- changed logical CSV row;
- reordered, duplicate, missing, or foreign row;
- raw schema change;
- emitted cell or quantile corruption.

Confirm smoke remains the original uncompressed CSV and all smoke scientific
bytes are unchanged.

### 5. Streaming, atomicity, and resource stops

Verify from code and bounded probes that:

- no 52,000-row candidate or expected raw list is materialized;
- at most one 400-row family plus bounded aggregates is retained;
- the second pass independently reconstructs every expected family and checks
  raw plus cell rows;
- existing target packages are refused;
- all outputs are staged;
- manifest is promoted last;
- a publication failure removes newly promoted partial files;
- runtime, compressed raw, logical raw, stored total, and RSS stops are checked
  during and before publication.

Independently reconstruct the exact-cardinality compression fixture. It must be
clearly non-scientific and contain 36,000 22-segment plus 16,000 11-segment
rows. Verify its deterministic high-entropy generation, compressed/logical
hashes, arithmetic, limits, and source/config binding. Do not accept a
repetition-only fixture.

Recompute the conservative release bounds:

- measured fixture logical: approximately 296.980 MiB;
- measured fixture gzip: approximately 90.615 MiB;
- worst-width logical: approximately 344.136 MiB;
- worst-width-adjusted stored gzip: approximately 105.003 MiB;
- stored-total bound: approximately 137.003 MiB;
- projected runtime: approximately 434.753 seconds;
- projected RSS: approximately 226.438 MiB.

Require all strict gates: 600 seconds, 150 MiB stored raw, 200 MiB stored total,
512 MiB RSS, and 400 MiB logical raw. Reject a projection that silently uses
compressed size for the logical-raw stop or that uses the 90.615-MiB fixture
directly instead of the worst-width adjustment.

### 6. Standard derived and inferential completeness

Independently verify that standard output—not smoke output—would provide:

- per-master cells and p-end quantiles;
- aligned seed-level paths;
- seed-level and across-master loops;
- signed/absolute area, mean and maximum separation, and control excess;
- seed-level transitions at `.5` and `.75`;
- pooled equal-master PAVA transitions;
- 10,000 complete-master paired bootstrap widths;
- estimability only when pooled crossings are valid and at least 95% of draws
  have valid paired widths;
- five-master Student-t summaries;
- cold-start feedback endpoints;
- inherited-versus-reversal effects;
- S00/S01 speed contrasts;
- S02--S07 versus S01 contrasts;
- active S01 versus disabled-feedback S08 placebo contrasts;
- no child-level pseudo-replication;
- no C8/C9 decision embedded in the execution package.

Use synthetic temporary cells/curves to test valid, censored, boundary,
plateau, nonfinite, reordered, and mutated-derived cases. Do not use smoke as
inferential evidence.

### 7. Figure and reporting contract

Confirm the future standard figure has five separate diagnostic panels for:

1. inherited mask paths by speed;
2. inherited receptivity paths by speed;
3. inherited versus reversal-only aligned gaps;
4. seed-level loop areas and transition widths;
5. included sensitivity/ablation results.

It must be called “M4 continuation-path diagnostics,” not hysteresis. Confirm
the report and manifest clearly state that standard execution is not C8/C9
adjudication and qualification is refused.

## Decision rules

### `GO_STANDARD`

Issue only if every gate above passes and no Blocker or Major defect remains.
Create both:

1. `projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`
2. `projects/frontiers_article/approvals/E06_STANDARD_GO.md`

The review must explicitly state:

- the audit evidence and independently recomputed values;
- absence of standard/qualification execution;
- absence of code/scientific/manuscript changes;
- why compression preserves logical scientific evidence;
- exact authorization scope and stop rules;
- `GO_STANDARD` as the sole final decision.

The GO file must contain exactly one fenced machine block. Construct values
from current files at review completion—never copy hashes from this prompt:

````markdown
```e06-go-binding
{"decision":"GO_STANDARD","experiment_id":"E06","config_path":"configs/frontiers_article/e06_m4_paths_standard.json","config_sha256":"<current normalized-config sha256>","source_fingerprint_sha256":"<current ordered source fingerprint>","smoke_manifest_path":"results/manifests/frontiers_m4_path_diagnostics_v1_smoke.json","smoke_manifest_sha256":"<current sealed-manifest sha256>","review_checkpoint_path":"projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md","review_checkpoint_sha256":"<current independent review sha256>","command":"PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli article-experiment --config configs/frontiers_article/e06_m4_paths_standard.json --approval-record projects/frontiers_article/approvals/E06_STANDARD_GO.md --output-dir results","qualification":"REFUSED"}
```
````

The key order, string types, relative paths, command, and qualification value
are exact parser requirements. After writing the GO, call the production
authorization validator read-only and prove it accepts the canonical record.
Do not dispatch the experiment.

### `FIX_IMPLEMENTATION`

Use for a bounded implementation/test/provenance defect with the frozen design
still defensible. Do not create GO. For each finding give severity, exact
location, evidence, consequence, required fix/test, and ignored risk.

### `REVISE_SPECIFICATION`

Use when a correct repair requires changing the frozen experiment, artifact,
inference, resource, or authorization contract. Do not create GO or implement
the revision.

### `NARROW_OR_STOP_CLAIM`

Use when the standard cannot defensibly answer its intended C8/C9 gate even if
implemented correctly. Do not run it or create GO.

## Required final response

Lead with the exact decision token. Then report:

- files created;
- seal/provenance result;
- model/raw/streaming/gzip audit result;
- exact standard cardinality and learner steps;
- inferential-output completeness;
- fixture and conservative resource bounds;
- focused/full-verification evidence;
- whether the canonical authorization validator accepts the GO, if created;
- explicit confirmation that standard and qualification were not run;
- `git diff --check` result and task-only diffstat.

Do not report readiness as scientific support for C8 or C9.

## Copy-ready prompt

```markdown
Perform the fresh independent E06 compression-ready Sol release-gate review.

Use gpt-5.6-sol with xhigh reasoning. Work in
`/Users/omer/workspace/personal/repos/gifted-masking`.

Read `projects/frontiers_article/E06_COMPRESSION_SOL_REVIEW_CODEX_INSTRUCTIONS.md`
completely and follow it exactly. Independently audit the sealed smoke,
deterministic standard gzip amendment, 52,000-row high-entropy fixture,
five-master standard dispatch/inference path, streaming/atomic behavior,
provenance, user verification, and all strict/formal resource gates.

Do not run E06 standard, qualification, or `./scripts/verify.sh`. Do not change
code, configs, scientific artifacts, claim ledger, manuscript, or figures.
Return exactly one of `GO_STANDARD`, `FIX_IMPLEMENTATION`,
`REVISE_SPECIFICATION`, or `NARROW_OR_STOP_CLAIM`. Create the canonical GO only
if every acceptance gate passes, then validate it read-only without dispatch.
```
