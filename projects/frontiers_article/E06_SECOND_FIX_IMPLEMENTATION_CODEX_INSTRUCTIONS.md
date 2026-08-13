# E06 second `FIX_IMPLEMENTATION` — Codex instruction set

**Authority:** `checkpoints/E06_SOL_SMOKE_REVIEW.md`
**Authorized work:** packed-raw validation, adversarial tests, canonical report,
and verification/provenance sealing only
**Implementation model:** `gpt-5.6-terra`
**Reasoning effort:** `high`
**Mode:** standard Codex task
**Required terminal status:** `READY_FOR_USER_FULL_VERIFICATION` or
`BLOCKED_BEFORE_FULL_VERIFICATION`
**Standard:** refused
**Qualification:** refused

## 1. Copy-ready task

Implement the bounded second E06 `FIX_IMPLEMENTATION` decision recorded in
`projects/frontiers_article/checkpoints/E06_SOL_SMOKE_REVIEW.md`.

The current canonical smoke is scientifically correct and reproducible, and
the previous user-owned repository verification passed. The release gate still
fails because `validate_e06_raw(...)` accepts mutations to frozen identity,
seed, parameter, traversal, reset, and Q-continuity fields, and because the
canonical report/manifest do not form the complete frozen release package.

Correct those two release defects without changing model semantics, configs,
random behavior, or scientific artifact bytes. Run the focused checks and
fresh-directory smoke regenerations specified here. Do **not** run
`./scripts/verify.sh`; the user owns the next full repository verification.
Do not run standard or qualification. Do not create `E06_STANDARD_GO.md`.

Stop with exactly one of:

- `READY_FOR_USER_FULL_VERIFICATION`, only when every pre-verification
  acceptance criterion below passes; or
- `BLOCKED_BEFORE_FULL_VERIFICATION`, with exact failed criteria, commands,
  logs, and artifact paths.

## 2. Mandatory consumption order

Read every listed file completely before editing. Continue any truncated read
to EOF. Do not rely on summaries from another task.

### Governance and scientific authority

1. `AGENTS.md`
2. `projects/frontiers_article/E06_SECOND_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`
3. `projects/frontiers_article/checkpoints/E06_SOL_SMOKE_REVIEW.md`
4. `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`
5. `projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md`
6. `projects/frontiers_article/E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`
7. `projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`
8. `projects/frontiers_article/RDS.md`
9. `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`
10. C8 and C9 in `projects/frontiers_article/CLAIM_LEDGER.md`
11. `projects/frontiers_article/CURRENT_STATE.md`
12. `projects/frontiers_article/BACKLOG.md`
13. `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`
14. `ARCHITECTURE.md`

Authority order is repository safety, the RDS, the E06 smoke approval, the Sol
review decision, and then this implementation instruction. Stop on a real
scientific conflict. Do not resolve one by tuning.

### Code, tests, configs, and current evidence

15. `src/gifted_masking/experiments/e06.py`
16. `src/gifted_masking/models/m4.py`
17. `src/gifted_masking/core.py`
18. `src/gifted_masking/repro.py`
19. `src/gifted_masking/cli.py`
20. `scripts/verify.sh`
21. `pyproject.toml`
22. `tests/test_article_e06.py`
23. `tests/test_m4.py`
24. `tests/test_core.py`
25. `tests/test_determinism.py`
26. `tests/test_reproducibility.py`
27. `tests/test_manifest_completeness.py`
28. `tests/test_primary_raw_schema.py`
29. `tests/test_summary_matches_raw.py`
30. all three `configs/frontiers_article/e06_*.json` files
31. `results/manifests/frontiers_m4_path_diagnostics_v1_smoke.json`
32. `results/manifests/frontiers_m4_path_diagnostics_v1_smoke_preverification.json`
33. `results/raw/frontiers_m4_path_diagnostics_v1_smoke_units.csv`
34. all five `results/summaries/frontiers_m4_path_diagnostics_v1_smoke_*.csv`
35. `results/figures/frontiers_m4_path_diagnostics_v1_smoke_m4_path_diagnostics.png`
36. `results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md`
37. `results/reports/frontiers_m4_path_diagnostics_v1_smoke_warnings.log`
38. every file in `results/reports/e06_preverification_logs/`

Before editing, run and record:

```bash
cd /Users/omer/workspace/personal/repos/gifted-masking
git status --short
git branch --show-current
git rev-parse HEAD
```

Expected starting branch is `codex/frontiers-stage2-e06`. The reviewed E06
checkpoint is commit `10018bd47bc789594e98ccd79fe51da3c3189b66`; later
document-only commits are allowed ancestors of the working HEAD. Do not reset,
rewrite, or discard them.

## 3. Frozen boundaries

### Allowed

- edit `src/gifted_masking/experiments/e06.py`;
- edit `tests/test_article_e06.py`;
- add a narrowly scoped E06 sealing helper or CLI only if necessary;
- update E06-specific architecture, checkpoint, state, backlog, execution-log,
  and user-handoff documentation;
- regenerate only the approved E06 smoke in fresh temporary/output roots;
- run only the focused tests and smoke checks authorized below;
- create a new pre-verification assessment index and focused logs.

### Prohibited

- no change to maintained M4 semantics, defaults, action selection, reward,
  update order, or RNG consumption;
- no change to any E06 config payload, hash, scenario, path, grid, seed,
  population, horizon, window, payoff, learner parameter, or resource limit;
- no change made merely to strengthen a result;
- no E06 standard or qualification execution;
- no `./scripts/verify.sh`, full test discovery, CI-equivalent command, or
  another full-repository verifier;
- no C8/C9 adjudication, claim-ledger update, manuscript edit, or Figure 4
  replacement;
- no claim of hysteresis from smoke output;
- no `E06_STANDARD_GO.md`;
- no manual edit that marks the canonical manifest or assessment index
  `verification.status=passed` before new user-owned full verification;
- no deletion or overwrite of the previous successful verification evidence.

## 4. Preserve the scientific bytes

Before code changes, record path, byte count, and SHA-256 for these eight
scientific artifacts:

1. packed raw CSV;
2. cells CSV;
3. paths CSV;
4. loops CSV;
5. transitions CSV;
6. effects CSV;
7. PNG figure;
8. warnings log.

The correction may change the canonical report and manifest. It must not change
any of the eight scientific artifacts above. Every fresh regeneration must
byte-match the pre-fix versions. If scientific bytes change, stop and return
`BLOCKED_BEFORE_FULL_VERIFICATION`; do not bless the drift as formatting.

Preserve the prior user verification files and hashes:

```text
results/reports/e06_preverification_logs/user_full_repository_verification.log
ce9ebaaf2278e2bc1f058355129de29b1af0705a9ccc1171f99e848ee9745749

results/reports/e06_preverification_logs/user_full_repository_verification_exit.txt
e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063
```

These prove the prior gate but cannot seal the corrected source. A new
user-owned verification is mandatory after this pass.

## 5. Correction A — reconstruct the complete packed raw contract

Replace partial `validate_e06_raw(...)` checks with a fail-closed comparison
against rows reconstructed from the exact frozen config and semantic seed
derivation.

The expected-row builder must not trust identity, parameters, traversal,
seeds, reset state, or continuity values taken from the candidate row. Build
those from the config, scenario definition, path definition, child index, and
semantic segment-seed functions. It must not validate a row by copying the
same row or by calling a helper that merely returns the candidate values.

For stochastic scientific values, deterministic replay from the frozen segment
seeds is permitted. Maintained-M4 parity remains a separate required test. The
validator must compare the complete ordered 55-field row, not a selected subset.

### Required validation groups

Validate all of the following in materialized Python rows and parsed emitted
CSV rows:

1. **Schema and cardinality**
   - exactly `RAW_FIELDS`, in exact order;
   - exactly `expected_rows(config)` rows;
   - exact deterministic row order;
   - no missing, duplicate, foreign, or reordered row;
   - no extra/missing field and no `None` overflow field.

2. **Run and scenario identity**
   - run, experiment, tier, model, component;
   - scenario ID and role;
   - path type and master seed;
   - matched-family ID;
   - child ID, declared child-seed representation, and RNG-unit declaration.

3. **Dimensions and final window**
   - declared `n`, segment horizon, total segments;
   - final-window fraction, start, and inclusive end;
   - ceiling-window convention and array lengths.

4. **Environment and learner parameters**
   - `p0`, `p_min`, `p_max`, `ka`, `kr`, and `km_mode`;
   - `b`, `a`, `c`, `r`, `alpha`, `tau`, `lambda`, and `q0`;
   - exact strict JSON types, rejecting booleans as integers and nonfinite
     values everywhere.

5. **Nominal grid, actual grid, and traversal**
   - declared nominal and actual km arrays;
   - complete direction array;
   - complete traversal nominal-km and actual-km arrays;
   - exact length, order, up/down/cold direction semantics;
   - active versus disabled-feedback actual-km semantics;
   - same-length substitutions must fail.

6. **Seed hierarchy**
   - the complete ordered policy/environment segment-seed map;
   - direction, position, canonical km label, and derived seed in every entry;
   - matched reuse/isolation rules across inherited, reversal, cold-start, and
     disabled-feedback paths;
   - duplicate JSON keys, truncated maps, reordered maps, or foreign entries
     must fail.

7. **Action, outcome, and reward arrays**
   - mask rate/count and authentic count;
   - authentic accept/reject counts;
   - mean objective reward;
   - exact segment-array lengths, integer count types, bounds, and identities;
   - `mask_count + auth_count == final_window_size`;
   - `auth_accept_count + auth_reject_count == auth_count`;
   - mask rate and reward reconstruct within the frozen tolerance.

8. **Receptivity state and reset semantics**
   - p start/end arrays, bounds-violation arrays, and final p;
   - inherited continuation between adjacent segments;
   - reversal-only reset at every segment, including disabled reversal;
   - cold-start reset at every segment;
   - final scalar equals the last packed end value;
   - bounds and zero stored post-update violations.

9. **Both Q components and continuity**
   - mask-Q and authentic-Q start/end arrays;
   - inherited continuity for both components;
   - reset-to-q0 semantics for both components on reversal-only, disabled
     reversal-only, and cold-start paths;
   - final mask-Q and authentic-Q scalars;
   - candidate corruption of either component must fail.

10. **JSON and numeric safety**
    - strict duplicate-key rejection;
    - exact list/object types and ordered contents;
    - reject NaN, positive/negative infinity, numeric strings where numbers are
      required, booleans where numeric values are required, and lossy coercion;
    - define field-specific exact/tolerant comparison instead of a blanket
      `float(...)` conversion.

`validate_e06_derived(...)` must continue to call this corrected raw boundary.
It must reject a foreign family ID, empty/altered seed map, or any other raw
corruption before deriving tables.

## 6. Correction B — comprehensive adversarial coverage

Add table-driven tests with named mutations. At minimum, include one mutation
from every validation group above, but target comprehensive coverage rather
than ten token cases.

Every required corruption must be exercised through both paths:

1. materialized rows passed directly to `validate_e06_raw(...)`; and
2. rows serialized to CSV, parsed through the production E06 reader, and then
   passed to the same validator.

Also prove that `validate_e06_derived(...)` rejects representative identity,
seed-map, parameter, traversal, reset, and both-Q corruptions at its raw
grounding boundary.

Required named cases include the exact review failures:

- `scenario_role`;
- `matched_family_id`;
- full policy/environment seed map, plus one nested seed-map member;
- `child_seed` and `rng_unit`;
- declared `n`;
- final-window start and end;
- `ka`, `km_mode`, declared nominal grid, and `alpha`;
- same-length traversal direction, nominal-km, and actual-km substitutions;
- inherited authentic-Q continuity;
- inherited mask-Q continuity;
- disabled-reversal p reset;
- disabled-reversal mask-Q and authentic-Q reset;
- missing, duplicate, reordered, and foreign rows;
- NaN, infinity, wrong JSON type, duplicate JSON key, and wrong array length.

The focused E06 test log must report the number of named adversarial mutations,
separated into materialized, parsed-CSV, and derived-boundary counts.

## 7. Correction C — complete canonical 13-item report

Make the runner emit one canonical report with exactly these 13 numbered
subjects, in this order:

1. run identity, tier, config, and authorization boundary;
2. frozen scenario, paths, grid, population, horizon, final window, rows, and
   learner-step count;
3. maintained M4 action/reward/Q/receptivity update order and parity evidence;
4. real packed action/outcome/reward diagnostics and raw reconciliation;
5. semantic seed derivation, pairing/isolation, traversal, resets, and p/Q
   continuity;
6. five derived tables, reconstruction, smoke ineligibility, and unavailable
   smoke intervals;
7. materialized and parsed-CSV fail-closed validation and adversarial coverage;
8. fresh-process deterministic regeneration and exact scientific-byte result;
9. phase-separated runtime/storage/RSS measurements and frozen core limits;
10. qualification projection and unconditional qualification refusal;
11. source/config/approval/Git/dirty-state provenance;
12. focused verification plus current user-full-verification status and evidence;
13. warnings, prohibited claims/actions, and exact next gate.

Before the new user verification, item 12 and the canonical manifest must say
`pending_user_full_verification`. They may mention the prior successful gate as
historical evidence but must state that it does not seal corrected source.

The report must not claim C8/C9 support, bistability, hysteresis, or permission
for standard/qualification.

## 8. Correction D — complete canonical manifest and provenance

Expand the manifest so one canonical package binds:

- exact normalized config and SHA-256;
- approval path and SHA-256;
- Git HEAD commit, branch when available, dirty boolean, and deterministic
  porcelain hash;
- explicit source-fingerprint path list and aggregate SHA-256;
- complete ordered segment-seed maps for every scenario/path/direction used;
- exact schemas, sort keys, counts, bytes, and SHA-256 for every artifact;
- phase timings, raw/total storage, RSS, core projection, qualification
  projection, and pass/refusal decisions;
- materialized, parsed-CSV, and derived validation status;
- adversarial test counts by boundary;
- focused command, exit code, test count, runtime, and log path/hash records;
- deterministic-regeneration commands, roots, normalized comparison, and
  byte-comparison records;
- standard/qualification dispatch refusals;
- user verification status, required command, evidence fields, and seal state;
- warnings and timestamps;
- strict JSON with no duplicate keys, NaN, or infinity.

Expand `SOURCE_FINGERPRINT_PATHS` to include all stable governing E06 sources,
including this instruction set, the original instruction sets, approval,
runbook, Sol review, configs, E06 code/tests, maintained M4/core/repro, CLI,
verification script, architecture, and `pyproject.toml`. Do not include a file
that the same run necessarily rewrites after fingerprinting.

Tests must independently recompute and reject a missing, altered, duplicated,
stale, or foreign provenance entry.

## 9. Correction E — replace the permissive external seal

The current `seal_e06_verification(out, focused_count, full_count)` interface is
not sufficient. Replace it with a fail-closed external sealing operation that
accepts explicit evidence and verifies it before changing the canonical report
or manifest.

The seal must verify at least:

- exact expected full-verification command;
- exit-record file exists, has recorded SHA-256, parses strictly, and contains
  exit code zero;
- complete verification log exists, has recorded SHA-256, names the required
  workspace Python, contains the expected suite completions/counts, and has no
  failure/error termination;
- recorded test counts and runtimes agree with the log rather than caller-only
  numbers;
- current config, approval, source fingerprint, Git HEAD/dirty-state binding,
  and scientific artifact hashes agree with the pre-verification package;
- no fingerprinted source is newer than the verification evidence;
- focused logs and deterministic-regeneration evidence exist and match their
  recorded hashes;
- standard and qualification remain unexecuted/refused;
- the canonical manifest is in the expected pending state before sealing.

The seal must update verification/provenance/report fields only. It must not
regenerate or rewrite raw, derived, figure, or warnings artifacts. Use atomic
writes for the report and manifest where practical.

Add temporary/synthetic tests proving acceptance of a complete valid evidence
bundle and rejection of nonzero exit, altered log, altered exit record, wrong
command, stale source, source-fingerprint drift, Git/dirty-state drift, changed
scientific artifact, missing focused evidence, and already/inconsistently
sealed state.

Do not apply the seal to the canonical package during this task. The corrected
source has not yet received its new user-owned full verification.

## 10. Focused execution allowed in this task

Use only `/Users/omer/workspace/venvs/venv314/bin/python` for Python commands.
Store complete commands, stdout/stderr, exit codes, test counts, and runtimes in
a new directory:

```text
results/reports/e06_second_fix_preverification_logs/
```

Required focused checks:

1. focused E06 tests;
2. maintained M4 tests;
3. core, determinism, and reproducibility tests;
4. focused post-artifact manifest/schema/reconciliation tests relevant to E06;
5. standard and qualification dispatch-refusal tests;
6. canonical materialized and parsed-CSV raw validation;
7. canonical derived validation;
8. all adversarial mutation tests;
9. external-seal acceptance/rejection tests using only temporary copies and
   synthetic evidence;
10. two fresh smoke CLI regenerations in different temporary output roots and
    different `MPLCONFIGDIR` directories;
11. comparison of both fresh runs with each other and with the pre-fix
    scientific artifacts;
12. normalized manifest/report equivalence after removing only explicitly
    nondeterministic timing/path/timestamp/Git fields;
13. resource projection recomputation and frozen-limit checks;
14. hashes of all focused logs and assessment artifacts.

Do not use full `unittest discover`. Do not invoke `scripts/verify.sh` directly
or indirectly.

## 11. Documentation and output package

Before handoff, update E06-specific sections of:

- `ARCHITECTURE.md` if the validator/sealer interface changes;
- `projects/frontiers_article/CURRENT_STATE.md`;
- `projects/frontiers_article/BACKLOG.md`;
- `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`.

Create:

```text
projects/frontiers_article/checkpoints/E06_SECOND_FIX_PREVERIFY.md
results/manifests/frontiers_m4_path_diagnostics_v1_smoke_preverification_v2.json
results/reports/E06_USER_FULL_VERIFICATION_ROUND2_INSTRUCTIONS.md
results/reports/e06_second_fix_preverification_logs/
```

The machine-readable preverification index must include:

- status;
- starting and current Git identifiers;
- config/approval/source/dirty-state hashes;
- scientific pre/post hashes and byte-preservation decision;
- every focused command/log/hash/count/runtime;
- adversarial counts by boundary;
- deterministic-regeneration roots and comparisons;
- canonical artifact paths/counts/bytes/hashes;
- core and qualification projections;
- canonical manifest/report status;
- `full_verification.status=not_run_user_owned`;
- `standard_executed=false`;
- `qualification_executed=false`;
- warnings.

The Round 2 user instructions must preserve the full log and exit code without
losing it through a pipe. Use new filenames so prior evidence is not
overwritten:

```bash
cd /Users/omer/workspace/personal/repos/gifted-masking

MPLCONFIGDIR=/private/tmp/e06_user_verify_round2 \
  ./scripts/verify.sh \
  > /private/tmp/e06_user_full_verification_round2.log 2>&1

verify_status=$?

tail -80 /private/tmp/e06_user_full_verification_round2.log

printf 'verification_exit_code=%s\n' "$verify_status" \
  | tee /private/tmp/e06_user_full_verification_round2_exit.txt
```

The instructions must say not to run E06 standard or qualification afterward.

## 12. Pre-verification acceptance criteria

Return `READY_FOR_USER_FULL_VERIFICATION` only if all are true:

1. The exact frozen configs and model/RNG semantics are unchanged.
2. The validator reconstructs and compares every ordered raw field.
3. Every required materialized and parsed-CSV adversarial mutation is rejected.
4. Derived validation rejects representative corrupt raw identity, seeds,
   parameters, traversal, resets, and both Q components.
5. Maintained-M4 parity remains exact within the frozen tolerance.
6. The canonical unmodified rows and all five derived tables pass.
7. The eight scientific artifacts byte-match the pre-fix checkpoint.
8. Two fresh runs byte-match each other and the checkpoint scientifically.
9. The canonical report has all 13 required items and remains scientifically
   noninferential.
10. The manifest contains the complete provenance schema and remains
    `pending_user_full_verification`.
11. The external sealer accepts complete temporary evidence and rejects every
    required corruption without sealing the canonical package.
12. Focused tests pass with complete logs, counts, runtimes, and hashes.
13. Core projections remain within all frozen limits.
14. Standard and qualification dispatch remain refused and unexecuted.
15. No C8/C9, ledger, manuscript, or figure action occurred.
16. The user verification instructions and machine assessment index are
    complete and self-consistent.
17. `git diff --check` passes for edited source/tests/docs. Generated CRLF CSV
    artifacts may be checked separately without normalizing their frozen bytes.

## 13. Final response contract

The response must begin with exactly one terminal status:

```text
READY_FOR_USER_FULL_VERIFICATION
```

or

```text
BLOCKED_BEFORE_FULL_VERIFICATION
```

Then provide:

- concise outcome;
- files changed/created;
- focused test counts and adversarial counts by boundary;
- scientific byte-preservation result;
- deterministic-regeneration result;
- resource projections;
- canonical report/manifest status;
- confirmation that full verification was not run;
- confirmation that standard and qualification were not run;
- exact next user command or exact blockers;
- task-only diffstat, noting any pre-existing worktree state.

Do not claim completion merely because tests pass. The package is ready only
when the entire fail-closed boundary and preverification evidence contract are
satisfied.
