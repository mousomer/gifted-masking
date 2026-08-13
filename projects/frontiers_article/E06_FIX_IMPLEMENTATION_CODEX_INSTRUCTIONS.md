# E06 FIX_IMPLEMENTATION — Codex Instructions Through Pre-Verification Handoff

**Decision being implemented:** `FIX_IMPLEMENTATION`  
**Authorized pass:** E06 Pass B2 corrective implementation and smoke regeneration  
**Terminal status:** `READY_FOR_USER_FULL_VERIFICATION`  
**Full repository verification owner:** user  
**Standard/qualification status:** refused

## 1. Model assignment

```text
model: gpt-5.6-terra
reasoning effort: high
mode: standard
```

Use Terra/high for the corrective implementation. The scientific design is
already frozen; this task is exact code repair, validation hardening,
deterministic smoke regeneration, focused testing, and evidence packaging.

Do not use the implementation task to make the subsequent smoke-gate decision.
After the user runs full verification and the package is sealed, a fresh
`gpt-5.6-sol/xhigh` task must perform the independent review.

## 2. Objective

Correct the E06 smoke implementation so that it records and validates the
actual M4 action/outcome/reward mechanism, implements the prespecified
standard-only inference helpers synthetically, produces a reproducible phase-
separated capacity estimate, and emits a complete pre-verification assessment
package.

Run all focused E06 and M4 validation required to establish readiness, but
**do not run `./scripts/verify.sh` or any equivalent full repository test
command**. The user will run full verification separately.

Stop only when either:

- every pre-verification acceptance criterion passes and the status is
  `READY_FOR_USER_FULL_VERIFICATION`; or
- a concrete blocker prevents that status, in which case write
  `BLOCKED_BEFORE_FULL_VERIFICATION` with exact evidence.

## 3. Mandatory consumption order

“Consume” means read the complete file directly. Continue truncated reads to
EOF. Do not work from an assistant summary.

### Governance and scientific authority

1. `AGENTS.md`
2. `projects/frontiers_article/E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`
3. `projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md`
4. `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`
5. `projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`
6. `projects/frontiers_article/RDS.md`
7. `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`
8. C8 and C9 in `projects/frontiers_article/CLAIM_LEDGER.md`
9. `projects/frontiers_article/CURRENT_STATE.md`
10. `projects/frontiers_article/BACKLOG.md`
11. `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`
12. `ARCHITECTURE.md`
13. repository-root `CURRENT_STATE.md`
14. repository-root `BACKLOG.md`

Authority order is repository safety, RDS, E06 scientific approval, this
corrective instruction set, then operational documentation. If a true
scientific conflict remains, stop and record it; do not resolve it by tuning.

### Maintained code and experiment infrastructure

15. `src/gifted_masking/core.py`
16. `src/gifted_masking/models/m4.py`
17. `src/gifted_masking/repro.py`
18. `src/gifted_masking/cli.py`
19. `src/gifted_masking/experiments/e06.py`
20. `src/gifted_masking/experiments/e05.py`
21. `src/gifted_masking/experiments/article.py`
22. `src/gifted_masking/experiments/robustness.py`
23. `scripts/verify.sh`
24. `pyproject.toml`

### Tests

25. `tests/test_article_e06.py`
26. `tests/test_m4.py`
27. `tests/test_core.py`
28. `tests/test_determinism.py`
29. `tests/test_reproducibility.py`
30. `tests/test_article_e05.py`
31. `tests/test_manifest_completeness.py`
32. `tests/test_primary_raw_schema.py`
33. `tests/test_summary_matches_raw.py`

### Current E06 configs and smoke evidence

34. all three `configs/frontiers_article/e06_*.json` files
35. `results/manifests/frontiers_m4_path_diagnostics_v1_smoke.json`
36. `results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md`
37. `results/reports/frontiers_m4_path_diagnostics_v1_smoke_warnings.log`
38. `results/raw/frontiers_m4_path_diagnostics_v1_smoke_units.csv`
39. every `results/summaries/frontiers_m4_path_diagnostics_v1_smoke_*.csv`
40. `results/figures/frontiers_m4_path_diagnostics_v1_smoke_m4_path_diagnostics.png`

Before editing, inspect `git status --short`, record the dirty worktree, and
preserve unrelated user changes.

## 4. Frozen boundaries

### Allowed

- edit the isolated E06 experiment and focused E06 tests;
- edit the minimal CLI or shared experiment support required by E06;
- update E06 documentation and checkpoint files;
- regenerate only the exact approved E06 diagnostic smoke;
- run small unit tests and the focused commands in Section 12;
- perform fresh-directory smoke regeneration and artifact comparison;
- measure individual runtime phases and RSS;
- write the required assessment bundle.

### Prohibited

- do not change `src/gifted_masking/models/m4.py` semantics or defaults;
- do not change payoff, learner, ramp, scenario, seed, horizon, or sample-size
  contracts;
- do not run the core standard or qualification config;
- do not add exploratory parameter cells;
- do not adjudicate C8 or C9;
- do not edit article prose or replace Figure 4;
- do not call smoke output hysteresis;
- do not issue `E06_STANDARD_GO.md`;
- do not mark full verification passed;
- do not run `./scripts/verify.sh`, `unittest discover` over the complete test
  directory, or another command that is equivalent to full repository
  verification.

## 5. Required correction A — real segment diagnostics

The present E06 runner derives only mask rate and final state from maintained
`m4.simulate_from_state`. It then writes zero accepted/rejected counts and an
empty objective-reward array. This must be replaced.

Implement an E06-local diagnostic segment kernel that replays the maintained
M4 algorithm exactly while recording final-window scientific diagnostics.
Do not modify maintained M4 to make the test easier.

For every learner and step, preserve this exact order:

1. stable softmax action selection from the two Q-values;
2. consume one acceptance uniform for every learner, including masking;
3. calculate objective reward from the pre-update receptivity;
4. update only the selected Q-value using subjective reward;
5. update receptivity after reward/Q update;
6. clip receptivity to `[p_min,p_max]`.

For every final-window segment record per child:

- mask count;
- authentic count;
- accepted-authentic count;
- rejected-authentic count;
- mean realized objective reward;
- mask rate;
- segment start/end p;
- segment start/end Q values;
- bounds-violation count before clipping and after update as defined below.

Define `bounds_violation_count` as the number of stored post-update p values
outside `[p_min,p_max]`; it must be zero. If a separate pre-clip diagnostic is
useful, add a differently named field only after updating the frozen schema
through a documented correction; never overload the frozen field.

The final-window mean objective reward must reconstruct exactly, within
`1e-12`, from:

```text
[mask_count*(b-c)
 + auth_accept_count*(b+a)
 + auth_reject_count*(a-r)] / final_window_size
```

### Required parity proof

For identical initial p/Q arrays, parameters, seed, and horizon, the E06-local
kernel must match maintained `m4.simulate_from_state` for:

- every child's final-window mask rate;
- every child's final p;
- every element of final Q;
- optional p trajectory when requested by the test helper.

Test at least:

- masking and authenticity both selected;
- accepted and rejected authenticity both occur;
- `km=0` and `km>0`;
- reset and inherited starts;
- multiple nontrivial seeds;
- a non-integer final-window fraction case to verify the maintained ceiling
  convention.

Use exact equality where deterministic floating replay permits it; otherwise
use no weaker than `rtol=0`, `atol=1e-12` and explain why.

## 6. Required correction B — fail-closed configuration and raw validation

### Config validation

Validate the complete canonical structure for each tier, not merely top-level
keys and master seeds. Reject any mutation to:

- run ID, tier, model, n, default segment horizon, final-window fraction;
- master seed(s), bootstrap seed/replicates, workers;
- payoffs, learner parameters, bounds;
- exact numeric `km` grid and JSON numeric types;
- scenario ID, role, order, p0, ka, kr, optional tau/lambda/horizon;
- `actual_km_mode` and exact path-type list/order;
- smoke, core, or qualification row/segment/learner-step cardinality;
- approval flags;
- unknown/missing/duplicate keys at every nested level.

Prefer immutable canonical expected payloads or an equally strict recursive
comparison. Booleans must not pass for integers.

### Raw validation

Reconstruct expected row identity from the config and reject missing,
duplicated, foreign, or reordered rows. Validate every frozen scalar and every
packed field, including:

- run/tier/model/component/scenario/path/master/child identity;
- matched-family ID;
- exact semantic segment IDs and derived uint64 seed map;
- canonical direction, position, traversal, numeric km, and actual km;
- declared n, horizons, windows, parameters, and array lengths;
- finite p and Q starts/ends and final scalar states;
- reset of both Q and p for reversal and cold paths;
- exact p, mask-Q, and authentic-Q continuity for inherited and disabled-
  inherited paths, including the turning point;
- mask plus authentic counts equal the final-window size;
- accepted plus rejected authentic counts equal authentic count;
- mask rate and mean objective reward reconstruct from counts;
- all rates and counts have valid ranges/types;
- bounds violations are zero;
- final scalar p/Q equals the final packed segment state;
- no NaN or infinity anywhere, including inside JSON.

Adversarial tests must mutate at least one field from every group above and
show rejection in both materialized and streaming validation paths if both
paths exist.

## 7. Required correction C — derived reconstruction

All cells, paths, loops, transitions, and effects must be deterministic pure
reconstructions from validated raw rows. Validation must take raw rows as an
explicit input and reject any altered derived quantity, identity, interval,
censoring status, decision eligibility, or cardinality.

Required checks include:

- exact cell/path/loop/transition/effect row identities and ordering;
- child means, standard errors, quantiles, counts, and Q summaries;
- aligned descending paths in increasing numeric km order;
- down-minus-up gaps;
- signed and absolute trapezoidal areas;
- mean vertical and maximum absolute separation;
- inherited-minus-reversal control-excess areas;
- cold-start endpoint effects;
- disabled-feedback placebo contrasts;
- transition fit, censoring status, and width;
- `decision_eligible=false` and unavailable inference for smoke.

Do not silently fill unavailable values with zeros. Use an explicit blank plus
status field, or a contract-approved `not_estimable` representation.

## 8. Required correction D — standard-only inference helpers

Implement but do not run the standard simulation. Exercise these helpers only
with synthetic five-seed curves and small derived fixtures.

Required helpers/tests:

1. paired five-master-seed Student-t effects using the fixed df=4 critical
   value used by the article infrastructure;
2. nondecreasing equal-weight PAVA with finite/ordered input enforcement;
3. `.5` and `.75` transition inversion with exact plateau midpoint,
   interpolation, boundary rejection, and no extrapolation;
4. paired transition width
   `ascending_transition - descending_transition`;
5. 10,000-resample top-level bootstrap over exactly five complete seed-pair
   curves;
6. scenario/response/target-isolated bootstrap seed derivation under namespace
   60;
7. valid paired-width fraction;
8. interval availability only when the pooled pair is valid and at least 95%
   of bootstrap pairs are valid;
9. version-independent linear `.025`/`.975` percentile arithmetic;
10. complete censoring and invalid-cardinality behavior;
11. control-excess loop effects and speed/horizon contrasts.

Child resampling is prohibited. Administrative pairing across scenarios is
prohibited unless explicitly frozen. Smoke must never emit standard
confidence intervals or eligible transitions.

## 9. Required correction E — reproducible phase-separated readiness

Replace total-wall-time multiplication with separately measured phases:

- M4 learner simulation;
- raw serialization;
- raw validation and derived reconstruction;
- standard-only five-seed effects and 10,000 bootstrap projection;
- figure creation;
- fixed import/Matplotlib/font-cache startup;
- peak RSS;
- raw and total artifact size.

Scale simulation by learner steps, serialization by packed rows and array
lengths, derived work by frozen output cardinality, and bootstrap by measured
synthetic replicate cost. Treat figure/startup work as fixed rather than
multiplying it by learner steps.

Run the diagnostic smoke/readiness measurement in at least two fresh CLI
processes with separate writable `MPLCONFIGDIR` directories so cold cache
behavior is visible. Record both projections and the conservative maximum.

The pre-verification package is ready only if the reproducible core projection
satisfies all frozen limits:

```text
runtime <= 600 seconds
raw <= 400 MiB
total artifacts <= 500 MiB
peak RSS <= 2 GiB
```

If the corrected conservative projection still fails any limit, do not alter
the scientific design. Set status `BLOCKED_BEFORE_FULL_VERIFICATION` with
recommended `REVISE_SPECIFICATION`, and stop without asking the user to spend
time on full verification.

Qualification must have a separate projection and remain refused regardless
of its estimate.

## 10. Required correction F — deterministic regeneration and provenance

Regenerate only the approved smoke after code and focused tests are stable.
Because current raw diagnostics are scientifically incomplete, corrected raw
and derived hashes are expected to change. Do not claim that corrected
scientific artifacts must match the invalid prior smoke.

Then regenerate into at least one fresh temporary output root and compare:

- raw, cells, paths, loops, transitions, effects, and PNG byte-for-byte;
- normalized manifest and report content after removing only documented
  timestamps, elapsed timings, absolute output roots, and environment-specific
  cache paths;
- warnings byte-for-byte.

The normalization function must not hide scientific values, hashes, seeds,
source fingerprints, row counts, verification states, or decision statuses.

The pending manifest must include:

- config path, normalized config, and SHA-256;
- approval path and SHA-256;
- executable command;
- Git commit and dirty state;
- content-inclusive source fingerprint covering E06 source, CLI, core, M4,
  repro, configs, tests, approval/instruction documents, pyproject, and verify
  script;
- Python/platform/NumPy/Matplotlib versions;
- exact seed derivation and complete segment seed map;
- ordered raw/derived schemas and sort keys;
- estimator and bootstrap definitions;
- exact artifact paths, row counts, byte sizes, and hashes;
- phase timings, resource projections, and limits;
- focused test commands, counts, runtimes, and results;
- deterministic regeneration result;
- warnings;
- full verification command but no fabricated result;
- `verification.status=pending_user_full_verification`.

Do not include the manifest's own hash inside itself.

## 11. Required 13-item checkpoint report

Write a complete 13-item report containing:

1. exact tier, run ID, config, and approval;
2. full frozen smoke design and exact cardinalities;
3. maintained semantic replay evidence;
4. path/control definitions;
5. seed hierarchy and pairing boundaries;
6. real action/outcome/reward and state-continuity reconciliation;
7. raw-to-derived reconstruction and adversarial validation;
8. diagnostic loop/transition results labeled noninferential;
9. deterministic fresh-directory regeneration and hashes;
10. focused tests with exact commands/counts/results;
11. phase-separated core and qualification resource projections;
12. complete provenance, artifacts, warnings, and unresolved risks;
13. status `READY_FOR_USER_FULL_VERIFICATION`, with standard,
    qualification, adjudication, ledger, manuscript, and Figure 4 actions
    explicitly refused.

Do not write `PENDING_SOL_SMOKE_REVIEW` yet. Sol review occurs only after the
user's full verification is incorporated and the package is finally sealed.

## 12. Focused commands Codex must run

Use the workspace Python and a writable Matplotlib cache. Codex must run all
of these, adjusting only test selectors if the test file is deliberately split:

```bash
MPLCONFIGDIR=/private/tmp/e06_fix_mpl \
PYTHONPATH=src \
/Users/omer/workspace/venvs/venv314/bin/python -m unittest \
  tests/test_article_e06.py -v
```

```bash
MPLCONFIGDIR=/private/tmp/e06_fix_mpl \
PYTHONPATH=src \
/Users/omer/workspace/venvs/venv314/bin/python -m unittest \
  tests/test_m4.py -v
```

```bash
MPLCONFIGDIR=/private/tmp/e06_fix_mpl \
PYTHONPATH=src \
/Users/omer/workspace/venvs/venv314/bin/python -m unittest \
  tests/test_core.py tests/test_determinism.py -v
```

Also run exact post-artifact focused tests for:

- pending-manifest completeness;
- E06 primary raw schema and semantic validation;
- raw-to-derived E06 reconstruction;
- deterministic cross-directory regeneration;
- standard and qualification dispatch refusal.

Do **not** run `./scripts/verify.sh`.

Capture each focused command's stdout/stderr, exit code, elapsed seconds, and
test count under:

```text
results/reports/e06_preverification_logs/
```

These logs are assessment artifacts and must be listed and hashed in the
assessment index. Avoid absolute temporary paths inside canonical scientific
artifacts where practical.

## 13. Mandatory assessment bundle

The task must leave all evidence required for later assessment in the
workspace. Create:

```text
projects/frontiers_article/checkpoints/E06_FIX_IMPLEMENTATION_PREVERIFY.md
results/manifests/frontiers_m4_path_diagnostics_v1_smoke_preverification.json
results/reports/e06_preverification_logs/
results/reports/E06_USER_FULL_VERIFICATION_INSTRUCTIONS.md
```

### Human checkpoint

`E06_FIX_IMPLEMENTATION_PREVERIFY.md` must report:

- status;
- precise fixes implemented;
- files changed;
- scientific behavior changes versus the invalid smoke;
- focused commands/results;
- smoke and regeneration commands;
- artifact inventory, counts, bytes, and hashes;
- deterministic comparison result;
- phase and capacity measurements;
- unresolved warnings;
- exact full verification command withheld for the user;
- exact files an assessor should inspect next;
- explicit confirmation that standard and qualification were not run.

### Machine assessment index

The preverification JSON must contain at least:

```json
{
  "status": "ready_for_user_full_verification",
  "run_id": "frontiers_m4_path_diagnostics_v1_smoke",
  "source_fingerprint_sha256": "...",
  "config_sha256": "...",
  "approval_sha256": "...",
  "focused_verification": [],
  "deterministic_regeneration": {},
  "artifacts": {},
  "core_projection": {},
  "qualification_projection": {},
  "full_verification": {
    "status": "not_run_user_owned",
    "command": "MPLCONFIGDIR=/private/tmp/e06_user_verify ./scripts/verify.sh",
    "result_log": "/private/tmp/e06_user_full_verification.log"
  },
  "standard_executed": false,
  "qualification_executed": false,
  "warnings": []
}
```

All referenced repository paths must exist. Every artifact entry must include
path, row count where applicable, byte count, and SHA-256. The index must be
strict JSON with no NaN or infinity.

### User verification instructions

Write a concise, copy-ready document containing:

```bash
cd /Users/omer/workspace/personal/repos/gifted-masking
MPLCONFIGDIR=/private/tmp/e06_user_verify \
./scripts/verify.sh 2>&1 | tee /private/tmp/e06_user_full_verification.log
```

Also provide the command that records the exit code without losing it through
the pipe, using `set -o pipefail`, and instructions not to run standard or
qualification afterward. Do not execute this command in Pass B2.

## 14. Documentation updates

Before handoff:

- update `ARCHITECTURE.md` for any E06-local diagnostic or validation
  architecture change;
- update project `CURRENT_STATE.md` to the true pre-verification state;
- mark the original Pass B smoke as completed but corrective work required in
  the backlog, then mark this corrective implementation complete only when the
  bundle is ready;
- append the execution log with plan, corrections, focused results, artifact
  regeneration, projections, and the fact that full verification is user-owned
  and not run;
- do not update C8/C9 evidence or manuscript chapters.

## 15. Pre-verification acceptance checklist

Every item must pass before returning `READY_FOR_USER_FULL_VERIFICATION`:

- [ ] real accepted/rejected/action/reward diagnostics exist;
- [ ] maintained M4 parity tests pass;
- [ ] complete frozen config validation passes adversarial tests;
- [ ] raw validator rejects all frozen semantic corruptions;
- [ ] raw rows reconstruct all derived tables exactly;
- [ ] standard-only five-seed/bootstrap helpers pass synthetic tests;
- [ ] smoke remains noninferential and decision-ineligible;
- [ ] standard and qualification remain non-executable;
- [ ] smoke row count is 320 and learner-step count is 345,600;
- [ ] corrected smoke regenerates deterministically;
- [ ] pending manifest is complete and source-fingerprinted;
- [ ] 13-item report is complete;
- [ ] focused E06/M4/core/determinism tests pass;
- [ ] post-artifact focused checks pass;
- [ ] core capacity projection passes every frozen limit;
- [ ] qualification remains separately projected and refused;
- [ ] assessment bundle exists and all indexed paths/hashes validate;
- [ ] full repository verification has not been run by Codex;
- [ ] no standard, qualification, C8/C9, ledger, article, or Figure 4 action
      occurred.

If any item fails, status must be `BLOCKED_BEFORE_FULL_VERIFICATION`, not a
partial success disguised as readiness.

## 16. Required Codex final response

Lead with exactly one status:

- `READY_FOR_USER_FULL_VERIFICATION`, or
- `BLOCKED_BEFORE_FULL_VERIFICATION`.

Then give:

1. concise outcome;
2. files changed;
3. focused tests and results;
4. corrected smoke artifacts and deterministic regeneration result;
5. capacity decision;
6. path to the human checkpoint;
7. path to the machine assessment index;
8. path to user verification instructions;
9. explicit statement that full verification was not run;
10. explicit statement that standard and qualification remain refused;
11. diffstat only, not a unified diff.

## 17. Copy-ready Codex task

```markdown
Implement the E06 FIX_IMPLEMENTATION corrective pass through the pre-full-
verification handoff only.

Use gpt-5.6-terra with high reasoning in standard mode.
Repository: /Users/omer/workspace/personal/repos/gifted-masking
Python: /Users/omer/workspace/venvs/venv314/bin/python

Read `projects/frontiers_article/E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`
completely, then consume every governing document, code file, test, config, and
artifact it lists in exact order. Implement all required corrections and
produce the complete assessment bundle.

You may run focused E06, M4, core, determinism, post-artifact, and fresh-
regeneration checks. You may regenerate only the approved E06 diagnostic
smoke. Do not run `./scripts/verify.sh` or any equivalent full repository
verification; the user owns that step. Do not run standard or qualification,
adjudicate C8/C9, update claim evidence, edit the article, or replace Figure 4.

Return `READY_FOR_USER_FULL_VERIFICATION` only if every checklist item passes,
including the phase-separated core capacity gate. Otherwise return
`BLOCKED_BEFORE_FULL_VERIFICATION` with exact evidence. Leave the canonical
manifest at `verification.status=pending_user_full_verification` and make all
outputs available through the human checkpoint, machine assessment index,
focused logs, and user verification instructions specified in the document.
```
