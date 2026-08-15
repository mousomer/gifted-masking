# Stage 2 Execution Log

## 2026-08-13 — E06 standard-readiness implementation design

Started the bounded post-Round-2 `FIX_IMPLEMENTATION` pass. The design in
`E06_STANDARD_READINESS_IMPLEMENTATION.md` preserves the sealed diagnostic
smoke and implements only future standard readiness: canonical GO binding,
five-master/scenario/path deterministic ordering, 400-row family streaming,
independent second-pass reconstruction, complete master-level inference, and
collision-free seed-map provenance. The readiness fixture must include both
simulation/replay passes and meet the stricter 600-second/150-MiB raw/200-MiB
total/512-MiB RSS review thresholds while retaining the approval's formal
execution stops. No standard, qualification, C8/C9, ledger, manuscript, or
Figure 4 action is authorized in this pass.

## 2026-08-13 — E06 Round 2 external seal and independent smoke gate

**Decision:** `FIX_IMPLEMENTATION`.

The immutable pre-seal audit matched Git HEAD
`9b2550248540152ad0d76758ee786bf228592880`, branch
`codex/frontiers-stage2-e06`, dirty state `true`, and porcelain SHA-256
`5fe733cc7c6f7d9155cd965032ea3716ff83a9c95653c21271cae239429f7316`
against both the pending manifest and v2 preverification index. Config,
approval, ordered source fingerprints, focused logs, two fresh deterministic
roots, and all eight E06 scientific artifacts matched. The Round 2 user log
parsed as 116 discovery tests in 128.321s and 1/1/2 post-artifact tests in
1.694/1.679/3.240s: 120 tests in 134.934s total, with exact log SHA-256
`73a5922e...` and exit SHA-256 `e0eb8bd6...`.

The evidence was archived with metadata under
`results/reports/e06_round2_user_verification/` without changing the porcelain
bytes/hash. A temporary production-seal probe passed and left canonical bytes
unchanged. The production sealer was then called once on the canonical map.
The manifest is now `passed` / `external_evidence_verified`, SHA-256
`3cf23f2082f4d8b770d0fc44b8d1c5f5082fa66cc3d9f4e0f64f8abff7cf7b5d`;
the report SHA-256 is
`45a2809bc4cc25b792badfcb2fbc7ad42384ca0b894015c2e3fbb573785bf36e`.
Raw, five summaries, PNG, and warnings retained their exact bytes. Independent
validation reconstructed 320 ordered 55-field rows, every derived table,
43,887 mask / 25,233 authentic / 22,608 accepted / 2,625 rejected actions,
zero bounds violations, 30 materialized and 30 parsed-CSV adversarial
rejections, seven derived-boundary rejections, and all 33 protected E01--E05
artifact hashes.

The smoke itself is valid and noninferential, but the standard release gate is
blocked. `run_e06_experiment` unconditionally rejects every non-smoke tier;
its execution loop uses only the one smoke `master_seed`; its derived builder
emits smoke-ineligible, zero-bootstrap diagnostic rows; and its manifest seed
map cannot preserve all masters. A GO would therefore bind a command that
cannot produce the frozen five-master standard package. The standard resource
projection also multiplies smoke RSS by only 1.5 and scales a phase containing
a complete deterministic replay only by row count despite materializing
candidate, cached reconstruction, and expected-copy rows. That projection is
not a conservative executable-standard high-water bound.

No `E06_STANDARD_GO.md` was created. No standard, qualification, C8/C9
adjudication, claim-ledger, manuscript, or Figure 4 action occurred. The exact
required correction and evidence are in
`checkpoints/E06_ROUND2_SOL_SMOKE_REVIEW.md`; another user-owned verification,
external seal, and fresh review are required after the bounded implementation
repair.

## 2026-08-13 — E06 second `FIX_IMPLEMENTATION` operational handoff

Wrote `E06_SECOND_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md` for a bounded
`gpt-5.6-terra`/high implementation pass. The task is limited to complete
55-field packed-raw reconstruction, materialized/parsed-CSV and derived-boundary
adversarial coverage, the canonical 13-item report and complete manifest, and a
fail-closed external verification sealer. It freezes the current scientific
smoke bytes, preserves the prior successful verification as historical evidence,
requires new Round 2 user-owned full verification after the correction, and
stops before standard, qualification, C8/C9, ledger, manuscript, or Figure 4
work. A fresh `gpt-5.6-sol`/xhigh review remains the only authority that may
issue a later `GO_STANDARD` decision.

## 2026-08-13 — E06 independent smoke review after user verification

**Decision:** `FIX_IMPLEMENTATION`.

The user-owned repository gate is valid. The preserved log uses
`/Users/omer/workspace/venvs/venv314/bin/python`, records 113 discovery tests
passing in 128.937 seconds and the 1/1/2 post-artifact suites passing in 1.937,
1.956, and 3.861 seconds, and has exit code zero. Its SHA-256 is
`ce9ebaaf2278e2bc1f058355129de29b1af0705a9ccc1171f99e848ee9745749`;
the exit-record SHA-256 is
`e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063`.
Current approval, normalized config, source fingerprint, and dirty-state hash
match the canonical preverification state, and no fingerprinted source was
modified after that verification.

Independent reconstruction confirmed that the 320 canonical raw rows contain
real mask/authentic/accepted/rejected and objective-reward diagnostics, exact
maintained-M4 order and replay, correct segment seeds and pairing, p/Q
continuity/reset state, zero bounds violations, exact derived tables, smoke
noneligibility, and byte-deterministic fresh regeneration. Two cold-cache CLI
processes matched all scientific outputs and produced conservative core
projections of 198.137 and 196.820 seconds; the maximum projection is 126.661
MiB raw, 140.829 MiB total, and 129.281 MiB peak RSS, within every core limit.
Standard and qualification dispatch both refused, and 33 recorded E01--E05
artifacts retained their manifest hashes.

The release gate fails because `validate_e06_raw` accepts representative
corruptions to frozen row identity/provenance, including matched-family and
segment seed-map fields, declared n/window/parameters, traversal semantics,
disabled-reversal reset state, and inherited authentic-Q continuity. Fourteen
of 17 initial adversarial cases were accepted; same-length direction and km
mutations also passed. Consequently `validate_e06_derived(...)` is exact only
conditional on a fail-open raw boundary. The canonical report also has seven
rather than 13 items, and its manifest does not yet carry the complete commit,
seed map, focused/deterministic evidence, or user-verification seal required by
the corrective contract.

The detailed record is `checkpoints/E06_SOL_SMOKE_REVIEW.md`. No canonical
manifest or preverification-index status was changed to passed, no
`E06_STANDARD_GO.md` was created, and no standard, qualification, C8/C9,
ledger, article, or Figure 4 action occurred.

## 2026-08-13 — E06 derived-validation pre-verification correction

**Scope and boundary.** Implemented only the remaining fail-closed derived
validation gate under `E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`. No
maintained M4 semantics/defaults, smoke design, standard/qualification run,
C8/C9 adjudication, claim evidence/ledger, article prose, or Figure 4 changed.

**Correction.** Added the shared
`validate_e06_derived(raw_rows,cells,paths,loops,transitions,effects,config)`
interface. It requires the exact frozen config and validated packed raw rows,
independently reconstructs all five tables, enforces exact ordered schemas,
identities/order/cardinality, checks finite estimates at `1e-12`, verifies
numeric-km path alignment and gaps, signed/absolute loop areas, separation,
control excess, cold-start endpoints, disabled-feedback placebo effects,
transitions/censoring/bootstrap fields, and smoke noneligibility. It runs
against materialized rows and parsed emitted CSVs before the manifest is
written. E06 has no streaming writer; its manifest records
`not_applicable_materialized_packed_rows` with the frozen raw/RSS capacity
rationale rather than inventing a duplicate architecture.

**Adversarial and focused evidence.** Seven E06 tests passed, including
rejection of 18 derived mutations: cell/effect values and identities, path gap
and km alignment, signed/absolute/control-excess loop values, transition
estimate/status/eligibility, reordering, duplicates, missing/foreign rows,
NaN, and infinity. M4 (4) and core/determinism (7) focused tests passed. The
post-artifact E06 contract also passed. Logs contain commands, stdout/stderr,
exit codes, and elapsed times under `results/reports/e06_preverification_logs/`.

**Approved smoke and readiness.** Regenerated only the 320-row, 345,600-step
smoke. A fresh process in `/private/tmp/e06_regen_derived_final` byte-matched
raw, cells, paths, loops, transitions, effects, PNG, and warnings; normalized
manifest/report comparison passed. The conservative phase-separated core
projection is 181.547 s, 126.661 MiB raw, 140.829 MiB total, and 119.625 MiB
RSS, within frozen limits. Qualification is separately projected and refused.

**Handoff.** The canonical manifest remains
`verification.status=pending_user_full_verification`. Full repository
verification was not run; it is user-owned through
`results/reports/E06_USER_FULL_VERIFICATION_INSTRUCTIONS.md`. The complete
assessment index is
`results/manifests/frontiers_m4_path_diagnostics_v1_smoke_preverification.json`.
Status: `READY_FOR_USER_FULL_VERIFICATION`.

## 2026-08-13 — E06 Pass B2 pre-full-verification handoff

Corrected E06's local M4 diagnostic recorder to preserve the maintained draw,
reward, Q-update, and receptivity order while recording final-window mask,
authentic, accepted-authentic, rejected-authentic, and objective-reward
diagnostics. The frozen config and raw/derived validators were hardened, and
synthetic five-master inference/bootstrap helpers plus parity tests were added.
The approved 320-row/345,600-step smoke was regenerated; a fresh-directory
regeneration byte-matched raw, summaries, PNG, and warnings. Focused E06, M4,
core/determinism, and post-artifact tests passed. A phase-separated n=400
segment readiness measurement projects the exact core at 188.121s, 126.661 MiB
raw, 140.767 MiB total, and 126.094 MiB RSS, within frozen limits; qualification
is separately projected and refused. Full repository verification was not run:
the manifest is `pending_user_full_verification` and the user owns that step.
No standard/qualification, C8/C9, ledger, manuscript, or Figure 4 action occurred.

## 2026-08-13 — E06 `FIX_IMPLEMENTATION` corrective instructions

The initial Pass B smoke is not eligible for standard GO. Review found
placeholder accepted/rejected/reward diagnostics, incomplete fail-closed raw
and derived validation, absent standard-only five-seed/bootstrap helpers, an
unsealed `pending_external_tests` manifest, a seven-item rather than 13-item
report, incomplete source provenance, and a naive core runtime projection of
approximately 1,856 seconds against the frozen 600-second limit.

The corrective implementation is specified in
`E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md` and assigned to
`gpt-5.6-terra/high`. It may repair code, strengthen focused tests, regenerate
only the smoke, and produce a complete human/machine assessment bundle. It
must not run full repository verification; that step is explicitly user-owned.
The corrective task may return `READY_FOR_USER_FULL_VERIFICATION` only if all
focused, deterministic, provenance, reporting, and phase-separated capacity
gates pass. Standard, qualification, C8/C9 adjudication, ledger, manuscript,
and Figure 4 actions remain refused.

## 2026-08-13 — E06 Pass B diagnostic smoke checkpoint

**Status:** `PENDING_SOL_SMOKE_REVIEW`

Pass B implemented the isolated E06 M4 continuation-path runner, exact frozen
smoke/standard/qualification configurations, CLI routing, packed raw rows,
fail-closed raw and raw-to-derived validation, nondecreasing-PAVA transition
diagnostics, trapezoidal loop estimators, and focused synthetic tests. The
runner delegates every segment to maintained `m4.simulate_from_state`; no M4
semantic/default/RNG or legacy-artifact change was made. The approved smoke
alone completed as `frontiers_m4_path_diagnostics_v1_smoke` with 320 packed
rows and 345,600 learner-steps. Its independent fresh-directory regeneration
matched all scientific CSV/PNG outputs and normalized machine artifacts.

The staged core standard and qualification configs are present only as
non-executable contracts. Neither was executed; no C8/C9 adjudication, ledger
change, manuscript edit, Figure 4 replacement, standard-only inference, or
smoke hysteresis claim occurred. Focused E06/M4 checks and repository
verification are recorded in the sealed manifest/report. The next action is a
fresh Sol/xhigh smoke audit, whose decision remains the only authority that
could create a separate core-standard GO.

## 2026-08-13 — E06 scientific approval

**Decision:** `APPROVED_FOR_SMOKE`

The E06 design is frozen in `approvals/E06_SMOKE_APPROVAL.md`, with a copy-
ready implementation/review handoff in `runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`.
The contract preserves maintained reward--Q--receptivity order; defines
inherited, reversal-only reset, cold-start, and disabled-feedback controls;
uses SHA-256-derived segment streams paired only between inherited and reset
counterfactuals; freezes signed trapezoidal loop area and nondecreasing-PAVA
transition estimators; and supplies fail-closed C8 and C9 rules.

The exact smoke is baseline-only (`n=64`, five-point nominal ramp, segment
horizon 120, one master seed), with 320 packed primary rows and 345,600 learner-
steps. The staged core standard has 52,000 packed rows and 913,000,000 learner-
steps across five master seeds. Long-horizon and learner-sensitivity work is a
separate qualification tier that remains refused unless the core C9
eligibility gate passes and a separate GO is issued. No implementation,
simulation, result, claim, ledger, article, or figure action occurred.

The Codex handoff is frozen in `E06_CODEX_INSTRUCTION_SET.md`. Active Pass B is
assigned to `gpt-5.6-terra/high`; independent smoke and core claim reviews use
fresh `gpt-5.6-sol/xhigh` tasks; only qualification authorization and final C9
adjudication use `gpt-5.6-sol/max`. Each pass has an ordered mandatory
consumption manifest and a distinct authorization and stop boundary.

## 2026-08-13 — E05 result-preservation documentation pass

The completed E05 finding is now preserved as a paired analytic--simulation
result in `E05_MAIN_RESULTS.md`, the RDS, C7 claim ledger, manuscript
integration map, and the reader-facing Results, Discussion, and Model Cascade
chapters. The article-facing text now leads with the flat learned `.5` crossing
at `bf=0.312852` (95% master-seed bootstrap interval
`[0.307836,0.316918]`) occurring before the exact objective crossover
`8/17=0.470588`, with approximately `.134` objective advantage remaining at
the learned crossing. It retains the hierarchical no-estimable-crossing
boundary and explicitly treats hot-stove causation and human calibration as
unresolved. No code, config, simulation, machine artifact, claim disposition,
or manuscript DOCX was changed.

## 2026-08-13 — E05 Pass E standard adjudication

**Disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for the frozen K=4,
fixed-good-context, default-learner flat-2K representation.

The final GO-authorized package was independently reconstructed from all
90,000 raw rows into 18 analytic, 180 cell, 1,548 effect, and 12 transition
rows; validators passed and every recorded output hash matched. Flat 2K met
the complete frozen rule: five of five seed crossings were valid, pooled
transition `bf=0.3128521127`, 95% master-seed bootstrap interval
`[0.3078358209,0.3169178027]`, 10,000/10,000 valid bootstrap crossings, and
zero material upward adjacent violations. The separate objective crossover is
exactly `8/17 = 0.4705882353`. Hierarchical had zero of five seed crossings
and no pooled crossing because response was already below `.5` at the dense
lower boundary; it cannot support an architecture-general threshold.

Final provenance matched current source fingerprint `f229a17d...`, all output
hashes, and three canonical 30,000-row shard hashes against the byte-identical
assembled raw file. Recorded reproduction was 96s aggregate with a 50s maximum
block, 88.502 MiB raw, 89.115 MiB total, and 606.172 MiB observed peak RSS;
all frozen limits passed. Focused, full-repository, and post-artifact
verification were recorded as passed. This adjudication changed only C7 and
project checkpoint documents. No simulation, code, result, manuscript,
`T=5000`, sensitivity, or publication-tier work occurred.

## 2026-08-12 — E05 repeat `FIX_IMPLEMENTATION` batch

Implemented only the smoke-gate corrections: PAVA/inversion reject nonfinite
or unsorted inputs; standard-only helpers now require exactly five master-seed
curves, generate architecture-isolated 10,000-replicate top-level bootstrap
transition summaries, and emit five-seed Student-t aggregate effects; and a
deterministic raw streaming writer validates the frozen order. The E05 runner
records an executable `PYTHONPATH=src` provenance command and retains the
smoke-only dispatcher refusal. Fresh independent regeneration preserved the
previous scientific CSV and PNG SHA-256 values exactly (raw
`9a60738fdc788bc6342c5141a9a11606e8e651a1485d3901127ea3bb0f45310e`; PNG
`7ce1a94a4915c08836367e64cb16142ba0df6172b7c8b7fa5428c5104249b995`).
Targeted E01--E05 tests passed (58); `./scripts/verify.sh` was run in the
required workspace venv. The smoke is resealed as deterministic and remains
`PENDING_SOL_SMOKE_REVIEW`; no standard, T=5000, sensitivity, C7 claim,
ledger, or manuscript action was performed.

### Reviewer-directed semantic hardening

The materialized validator and deterministic streaming writer now both invoke
one full frozen-row semantic boundary. Direct adversarial probes mutate tier,
model, component, K, good-context ID, p-good, bf label/anchor, n/T/window,
seed, final rates, modal fields, expected reward, and regret; every probe is
rejected in both paths. Derived validation now requires upstream raw rows and
exactly reconstructs analytic, cell, effect, and transition tables. Fresh
cross-directory smoke regeneration retained the six scientific artifact hashes
recorded above exactly; manifest/report were resealed only after source edits.

### Final narrow correction

The shared row validator now reconstructs realized objective reward and
pseudo-regret from action/accepted/rejected counts, checks good/bad authentic
totals against the action vector, and rejects every nonfinite Q entry. Standard
helpers reject any missing, duplicate, or foreign architecture/bf/master-seed
cell before five-seed aggregation. Capacity projection now separates raw-row
and learner-step scaling, rejects nonfinite/negative input, and exposes raw,
total-artifact, runtime, and RSS limits. These are implementation guards only;
the standard dispatcher remains refused.

### Final provenance-only correction

No E05 simulation was run. The resealed manifest now carries the enforced
standard-capacity projection (separate raw-row and learner-step factors, raw,
total, runtime, RSS, limits, and pass/fail), the executable command and final
source/dirty provenance. The report is a completed 13-item checkpoint: 17
focused and 106 full checks, baseline/manual sentinels, cross-directory
normalized regeneration, artifact list, resources, and the pending gate are
all stated as completed evidence rather than forward references.

## 2026-08-13 — E05 standard recovery checkpoint

The exact GO-authorized standard core artifacts were generated (90,000 raw
rows, 180 cells, 1,548 effects, 12 transitions, and the diagnostic figure),
but the original finalizer stopped after the figure with `KeyError: row_ratio`
in smoke-only report formatting. Recovery performed no simulation: it validated
all raw rows against the exact standard config/GO record, recomputed every
summary and a temporary figure byte-for-byte, then serialized a manifest/report
that records this interruption and recovery provenance. Raw is 88.50 MiB and
total core artifacts 89.09 MiB; recovery RSS was 611.98 MiB. Stop at
`PENDING_SOL_STANDARD_REVIEW`; no T5000, sensitivity, claims, ledger, or
manuscript action occurred.

## 2026-08-12 — E05 `FIX_IMPLEMENTATION` corrective handoff

### Outcome

The corrective implementation is complete and stops at
`PENDING_SOL_SMOKE_REVIEW`. E05 standard and `T=5000` remain refused.

The readiness estimator now profiles simulation, derived-table computation,
serialization, and figure generation separately. It scales learner simulation
by the frozen learner-step ratio, serialization by the frozen primary-row
ratio, derived work by the maximum frozen summary-cardinality ratio, and the
single diagnostic figure by `1x`. First-process matplotlib/font-cache work is
therefore measured as full-process fixed overhead rather than incorrectly
multiplied by `173.611111x`.

### Reproducibility and resource evidence

- Two independent fresh CLI processes used separate temporary output roots and
  deliberately incurred cold matplotlib font-cache construction. Both
  completed rather than tripping the stop rule.
- Their phase-scaled standard projections were `150.6645` and `151.2498`
  seconds, both below the frozen `600`-second cap. The canonical smoke projected
  `145.6302` seconds.
- Raw, analytic, cell, effect, transition, and PNG artifacts were byte-identical
  between both fresh processes and the pre-correction canonical smoke. Their
  SHA-256 values remain respectively:
  `9a60738fdc788bc6342c5141a9a11606e8e651a1485d3901127ea3bb0f45310e`,
  `bfb00ddd46900c09046de7489ace950c2f02065b0b98fb6235ed5e99a83e476c`,
  `44dd93547a2c85e9edd73a5f48fd4337c3efa06cfd917a42ab413b57c5b575eb`,
  `9f9c20f489ebdc1d0278833ae289ea0e22660b85e321f47f460845367aed8d65`,
  `196cfc851d87193e8f241096bb6a44a626cbea901e2c2595b9d960e5a7189134`,
  and `7ce1a94a4915c08836367e64cb16142ba0df6172b7c8b7fa5428c5104249b995`.
- Eight focused E05 tests pass, including phase-scaling and fail-closed sealing
  tests. Final `./scripts/verify.sh` passed 104 discovered tests plus four
  explicit post-generation artifact tests.
- The canonical smoke manifest is resealed with
  `verification.status=passed`, the exact verification command, deterministic
  scientific-artifact confirmation, refreshed output hashes, and the complete
  phase/readiness breakdown.

### Boundary

No M3 or E05 simulation semantics, defaults, parameters, RNG streams,
scientific rows, summaries, transitions, or figure bytes changed. No standard,
`T=5000`, claim-ledger, manuscript, or publication-tier action was performed.
The package now returns for the independent E05 smoke-gate review.

## 2026-08-12 — E05 repeat Pass C smoke-gate review

### Decision

`FIX_IMPLEMENTATION`

The phase-scaled smoke correction is reproducible but does not make the E05
standard package safe to authorize. Independent review confirmed that the
3,456 raw / 18 analytic / 36 cell / 258 effect / 4 diagnostic-transition smoke
artifacts are byte-deterministic, all analytic anchor and reward-placement
checks pass, and fresh cold smoke stayed within smoke resource limits. However:

- raw validation accepts numerous frozen identity, tier, parameter, rate,
  modal, reward, regret, and status corruptions;
- derived validation is largely schema/cardinality-only and accepts corrupted
  analytic, cell, effect, and transition quantities;
- PAVA and inversion accept nonfinite values and unsorted `bf` coordinates;
- the required standard five-seed Student-t effects, bootstrap transition
  intervals, crossing fraction, and decision eligibility are not implemented;
- standard streaming and conservative storage/RSS capacity checks are absent;
- the manifest command omits the project import path; and
- the smoke report is not a completed 13-item audit record.

The reviewer ran 15 focused checks and full workspace-venv verification (104
tests); both passed. Standard and `T=5000` dispatch remain refused. Pass B must
implement the fail-closed raw-to-derived boundary, complete standard-only
inference and streaming readiness, fix command/report provenance, preserve
scientific smoke bytes, reseal, and return for a fresh independent review.

## 2026-08-12 — E05 Pass C smoke-gate review

### Decision

`FIX_IMPLEMENTATION`

The diagnostic smoke's semantic and artifact checks are promising but it is not
eligible for standard authorization. The independent reviewer confirmed that
the focused E05 suite passes (6 tests) and that the workspace-venv repository
verification passes, but the sealed smoke manifest still records
`verification.status=pending_external_tests`. That is not a final, auditable
smoke checkpoint.

More importantly, an independent fresh-process regeneration invoked exactly
the frozen smoke config and correctly stopped before artifact creation because
its linear standard projection exceeded the frozen ten-minute limit. The
stored smoke projected 228.607 seconds from 1.317 seconds wall time, while the
fresh run included first-process plotting initialization and exceeded the
limit. The current readiness estimate is therefore not reproducible enough to
support a `GO_STANDARD` decision.

The review also confirmed that standard and `T=5000` dispatch remain refused;
no E05 standard, sensitivity, claim-ledger, or manuscript action occurred.
Pass B must profile the full process, remove or separately account for
non-simulation startup work without changing M3 semantics or RNG, prove
scientific artifact identity before/after any optimization, run final targeted
and full verification, reseal provenance, and return for another smoke review.

## 2026-08-12 — E04 Pass E claim adjudication

### Disposition

`SUPPORTED_IN_NARROW_DOMAIN`

The finalized E04 implementation is valid. The exact standard config and
canonical `E04_STANDARD_GO.md` hash match the manifest; the content-inclusive
source fingerprint and every recorded output hash match. The package contains
exactly 137,500 ordered baseline primary rows, 275 curves, 1,182 effects, 55
canonical cells, 120 equivalence rows with 55 canonical representatives, and
five complete reserved-seed copies of every canonical cell. No smoke,
sensitivity, publication, or cross-experiment row contaminated inference.

The bounded recovery is acceptable: it added no simulated rows, revalidated
the complete raw/canonical/equivalence/curve/effect package, and serialized
provenance after the original process was interrupted following figure
completion. The report correctly distinguishes the 51.625 MiB recovery RSS
from an unavailable original-process high-water. Pass D's independent replay
byte-matched raw, canonical, equivalence, curves, effects, and figure.

### Frozen decision-rule results

- **Fixed-one search effects passed.** Flat 2K settling slope per log2(K) was
  `-0.058240` (95% Student-t interval `[-0.063915,-0.052565]`) and its
  K=16-minus-K=1 change was `-0.234000`
  `[-0.246417,-0.221583]`. Hierarchical slope was `-0.114760`
  `[-0.124541,-0.104979]`, with endpoint change `-0.470400`
  `[-0.511031,-0.429769]`. Both slopes were negative in five of five seeds.
- **Architecture contrasts and controls passed.** Flat-minus-global slope was
  `-0.059960` `[-0.065503,-0.054417]`; hierarchical-minus-global was
  `-0.116480` `[-0.126124,-0.106836]`. Global mask changed only `0.008800`
  `[0.002090,0.015510]` from K=1 to K=16, and the K-invariant fixed-known-good
  effect was `0` `[0,0]`. Both controls meet absolute change below `.05` and
  interval containment in `[-.10,.10]`.
- **Randomized identity passed.** Using the explicit equivalent K=1 alias,
  randomized one-good K=16-minus-K=1 changes were `-0.2400`
  `[-0.2571,-0.2229]` for flat 2K and `-0.4596`
  `[-0.4683,-0.4509]` for hierarchical. Direct K=2--16 slopes were negative
  in all five seeds: `-0.07436` `[-0.07981,-0.06892]` and `-0.09636`
  `[-0.09961,-0.09311]`.
- **Multiple-good variants establish the boundary.** With two good contexts,
  flat K=2--16 slope attenuated from `-0.07144` to `-0.02080` and hierarchical
  from `-0.09776` to `-0.07252`; paired attenuation effects were `0.05064`
  `[0.04520,0.05608]` and `0.02524` `[0.01299,0.03749]`. Under the
  proportional-25 regime, direct slopes were near zero: `0.00220`
  `[-0.00099,0.00539]` and `-0.00252` `[-0.00792,0.00288]`.

### Correctness, reproducibility, and boundary

Independent adjudication streamed and semantically validated all 137,500 raw
rows, including exact architecture actions, child good sets, comparator/reward
and regret identities, discovery, modal/tie, entropy/allocation, Q shapes,
seeds, and deterministic ordering. It reconstructed all 275 curves from raw,
all 1,182 effects from curves, and all 197 across-seed Student-t estimates and
intervals; maximum independent interval error was `3.6e-15`. Each of the 80
architecture/K/master policy families used one shared policy/environment seed
across identity/good-count variants, while all 275 seed/canonical-cell identity
streams remained separately derived. The package used 128.724 seconds through
the completed figure and 174,838,110 raw bytes, within its authorized limits.

Maximum wording is: “In the frozen M3 baseline, increasing K reduced final-
window settling on a receptive-context authenticity action in both the flat 2K
and hierarchical search representations, while global-mask and known-good
controls remained practically equivalent across K. The decline survived
randomized receptive-context identity but weakened with two good contexts and
was near zero when 25% of contexts were receptive. Thus the tested effect
reflects representation-dependent search burden under scarce receptivity, not
context count alone.”

This does not generalize beyond `p_good=.85`, `p_bad=.20`, `bf=0`, default
learner settings, K through 16, or the tested identity/good-count regimes. The
staged p/tau sensitivity was not authorized or run. No simulation, code,
result artifact, sensitivity, publication-tier work, figure replacement, or
manuscript prose changed during adjudication.

## 2026-08-12 — E03 Pass E claim adjudication

### Disposition

`SUPPORTED_IN_NARROW_DOMAIN`

The E03 implementation is valid. The frozen standard config, canonical GO
record, source fingerprint, and all manifest output hashes match. Independent
streaming review reconciled all 364,800 primary rows to 2,250 cell/seed records
with maximum cell-mean differences below `4.5e-15`; all canonical IDs, exact
parameters, derived cell seeds, final windows, state-action/visit counts, reward
sums, and component memberships passed. Exact-grid effects and stability use
only 1,785 `exact_grid`/`baseline` cell/seed records; sentinel, harsh, smoke,
and threshold-refinement components do not enter the 357 denominator.

### Frozen decision-rule results

- **Grid support passed.** Every master seed `2026081301` through `2026081305`
  classified `243/357` cells as `learned_suboptimal_masking`, fraction
  `0.680672268907563`. The five-seed Student-t 95% interval is therefore
  `[0.680672268907563,0.680672268907563]`. The stable table contains 243
  learned-suboptimal cells, exceeding the required 179; its lower seed-level
  interval bound exceeds `.40`.
- **Stability and adequacy passed in the default domain.** Of 357 cells, 350
  have a stable 4-of-5 classification: 243 learned-suboptimal and 107
  learner/objective matches. The seven unstable cells are the low-`p`,
  `eta=0` cells from `p=0` through `.30`; their failures are inadequate neutral
  visits, not forced ties. All 1,785 value-iteration comparisons converged; no
  objective Q tie or learned neutral-action tie was classified. Across the
  1,215 learned-suboptimal seed/cell records, the strict neutral authenticity-
  minus-mask Q gap ranges from `0.0021754608` to `0.85`; only 907 have adequate
  counts for a full-policy regret, so the primary classification correctly
  uses the neutral decision axis.
- **The five dynamic-authenticity sentinels passed `n`/`T`/window.** For
  `(p,eta)` in `{(.40,0),(.55,0),(.55,.2),(.75,0),(.90,.2)}`, every one of the
  150 records spanning five seeds and baseline, `n=320`, `T=2000`, `T=5000`,
  window `.1`, and window `.4` remained learned-suboptimal masking with
  adequate neutral visits.
- **Learner qualification triggered.** At `gamma=.5`, the first three of the
  five dynamic-authenticity sentinels change to `learner_matches_objective` in
  all five seeds because value iteration switches to masking while the learned
  action remains masking. This exceeds the frozen two-sentinel qualification
  rule. At `alpha=.03`, the `.75,0` sentinel becomes 3/5 learned-suboptimal and
  the `.90,.2` sentinel becomes 5/5 matched; at `tau=.6`, `.75,0` is 4/5 and
  `.90,.2` is unstable at 2/5 learned-suboptimal. The other frozen alternate
  cases retain the default classification at all five sentinels. The claim is
  therefore default-learner/domain robust, not learner-parameter general.
- **Objective and learner axes remain separate.** The 243 stable default
  learner failures comprise 141 cells where dynamic M2 authenticity overrides
  static M0 masking and 102 where both objective axes select authenticity.
  There are no default-grid `optimal_policy_masking` cells. In the separate
  harsh `b2=0`, `r2=8`, `delta=.3`, `eta=0` sentinel, only `p=.75` satisfies
  static M0 authenticity plus objective M2 masking, in all five seeds (VI Q gap
  `-0.4062934363`). At `p=.70`, both objective axes mask; at `p=.80`, objective
  M2 authenticity plus learned masking is learner failure.
- **Threshold handling passed without overreach.** Default objective M2
  authenticity is bracketed at `[.3839111328,.3839721680]` for `eta=0`,
  `[.3387451172,.3388061523]` for `eta=.2`, and
  `[.2689819336,.2690429688]` for `eta=.8`; every width is
  `6.103515625e-05`, below `1e-4`. Learned refinement added no points and
  reported `censored_inconclusive` at `eta=0` and `censored_no_crossing` at
  `eta=.2/.8`. No learned threshold may be stated.

### Reproducibility, limitation, and boundary

- The package contains exactly 1,785 exact-grid, 450 sentinel/OAT, and 15 harsh
  cell/seed rows. Its manifest has 2,250 seed records, with 2,160 distinct cell
  seeds: the only sharing is the intended 30 master-seed/sentinel T-window
  trajectory families, four variants each. The original legacy replay remains
  byte-identical at 357 rows, 226 learned-suboptimal cells, fraction
  `0.6330532212885154`, `math.fsum` mean `0.9501766068109203`, and SHA-256
  `bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`.
- Pass D's independent streamed regeneration and normalized manifest match are
  retained in the evidence record. Post-adjudication `./scripts/verify.sh`
  passed 87 discovered tests plus the four explicit post-generation tests
  using the required workspace Python. No E03 standard or extra sensitivity
  run was performed during adjudication.
- Minor non-decision metadata limitation: the raw CSV is deterministically
  ordered by `parameter_cell_id`, `master_seed`, and `child_id`, but the
  manifest's `sort_keys` field names `component`, `sensitivity_name`, `eta`,
  `p`, and `master_seed` and omits child ID. Actual ordering, row content,
  hashes, regeneration, and inference are unaffected; repair the declaration
  only in a separately authorized metadata batch without rerunning evidence.
- Maximum wording and exact selectors are now frozen in `CLAIM_LEDGER.md`.
  No manuscript prose or figure, model semantics/defaults/RNG behavior,
  publication-tier work, or unplanned sensitivity was changed or executed.

## 2026-08-12 — E03 Pass D frozen standard execution

- Executed only `configs/frontiers_article/e03_m2_regime_standard.json` under
  the canonical `approvals/E03_STANDARD_GO.md` record. The dispatcher accepts
  no copied, wrong-path, missing, malformed, smoke, or cross-experiment record.
- The five reserved seeds produced 364,800 streamed primary rows across the
  canonical 357-cell exact grid, frozen six-sentinel OAT cases, and three
  `b2=0` harsh cells. Learned refinement was attempted under its frozen bounds
  and recorded its censoring status; no factor crossing or extra sensitivity
  was run. The raw file is 391,221,606 bytes (~373 MiB), under the ~400 MiB
  bound; generation took 167.454 seconds, under the four-minute limit.
- Historic provenance remains exact: 357 legacy rows, 226 learned-suboptimal,
  fraction `0.6330532212885154`, `math.fsum` mean
  `0.9501766068109203`, and SHA-256
  `bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`.
  The standard package contains raw, cell, effect, stable-cell, threshold,
  legacy, figure, manifest, and 13-item report artifacts under `results/`.
- An independently streamed temporary regeneration byte-matched raw, cells,
  effects, stable cells, thresholds, legacy CSV, and PNG; normalized machine
  manifests matched. Independent streaming reconciliation verified every
  state mask+authentic=visit identity and raw-to-cell final-window means.
  Targeted E01/E02/E03 tests (40 plus 7 subtests) and post-output
  `./scripts/verify.sh` (87 tests) passed.
- Stop at `PENDING_SOL_STANDARD_REVIEW`. No E03 claim adjudication, ledger
  update, manuscript edit, publication-tier run, or additional sensitivity was
  executed.

## 2026-08-12 — E03 canonical-grid and capacity correction

- The standard summarizer is now bound to the canonical 21 p by 17 eta grid
  generated from the frozen standard config and component-aware exact-grid IDs,
  not any same-cardinality set supplied by a caller. It requires every row to
  be an approved `exact_grid`/`baseline` row and validates p, eta, all frozen
  environment/learner fields, n, T, and window against the ID/grid. Arbitrary
  IDs, altered fields, and even one non-grid row reject before aggregation.
- Capacity is corrected to measured `390,912,614` bytes (`372.8 MiB`), a
  conservative `~400 MiB` raw bound, and a `~35.6 MiB` streaming peak under the
  existing <2 GiB cap. The accepted standard runtime remains 2.8–4 minutes.
  This correction does not authorize or execute standard work.
- E03's 13 focused tests, E01/E02 targeted suites, and `./scripts/verify.sh`
  passed. The only regenerated E03 smoke had 384 rows in 20.756 seconds with
  a refreshed source fingerprint; its 357/226/fraction/exact-mean/hash legacy
  replay and all state-count/raw-summary checks passed. A deterministic rerun
  byte-matched raw, cells, effects, stable, thresholds, legacy, and PNG
  artifacts. Stop at `PENDING_SOL_SMOKE_REVIEW`.

## 2026-08-12 — E03 final readiness correction

### Readiness controls and regenerated smoke

- `summarize_e03_standard_classifications` is now fail-closed: it accepts only
  the five reserved seeds `2026081301`–`2026081305`, exactly 357 unique
  `exact_grid` parameter cells for every seed, no duplicate seed/cell key, and
  identical cell sets across seeds. It rejects missing, extra, unexpected, and
  duplicate records before denominators or intervals are calculated.
- Stable-cell grouping filters to `component=exact_grid` before grouping and
  independently verifies every cell has exactly one record from each expected
  seed. Sentinel or sensitivity identifier collisions therefore cannot affect
  exact-grid fractions, intervals, or stable labels.
- Canonical parameter IDs now encode run ID, tier, model, component,
  sensitivity name, p/eta, every environment and learner parameter, n, T, and
  final window. Master seed is intentionally separate for repeated-measure
  grouping. Tests cover exact/default-sentinel/OAT/harsh/refinement
  non-collision. Only approved T/window family pairing remains exempt from
  independent seed-family generation.
- The future standard streaming plan is revised to measured 372.8 MiB raw,
  conservative ~400 MiB bound, approximately 35.6 MiB streaming peak
  (<2 GiB cap), and accepted 2.8–4 minute runtime. No standard execution
  occurred.
- The sole regenerated smoke passed: 384 rows, 20.855 seconds, 386,835-byte
  raw output. Legacy replay remains 357/226, fraction `0.6330532212885154`,
  exact `math.fsum` mean `0.9501766068109203`, and SHA-256
  `bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`.
  Source fingerprint, state visits, raw summaries, and manual classification
  sentinels were independently checked. Raw/cell/effect/stable/threshold/
  legacy/PNG artifacts byte-match a deterministic regeneration.
- E03 (13 tests), E01/E02 targeted suites, and `./scripts/verify.sh` passed.
  Stop at `PENDING_SOL_SMOKE_REVIEW`; no standard, sensitivity, claim, ledger,
  or manuscript work was performed.

## 2026-08-12 — E03 smoke-gate correction plan

### Plan and acceptance criteria

1. Correct E03 provenance aggregation to use the frozen `math.fsum` result
   (with at most one ULP tolerated for platform reconciliation), add a real
   `rng_family_id` contract for future default T/window variants, and preserve
   all maintained M2 paths and the historic RNG mapping.
2. Add unexecuted-standard helpers and tests for five-seed stability/fractions,
   intervals, objective and learned threshold handling, harsh `b2=0` cases,
   stream-to-CSV aggregation, and an E03-specific future authorization gate.
3. Regenerate only the frozen E03 smoke after every code/test edit; recompute
   its source fingerprint and scientific artifacts independently. Do not
   execute standard, sensitivity, claim, ledger, or manuscript work.

Acceptance requires the 357/226/hash replay and 384-row sentinel smoke to
remain scientifically identical for unchanged default cells, exact per-state
action/visit reconciliation, a self-consistent manifest fingerprint, a strict
future standard refusal, and passing E03/E01/E02 plus full repository checks.

### Corrected smoke result

- Legacy aggregation now uses `math.fsum` over the exported cell values, which
  exactly reproduces the frozen mean `0.9501766068109203`. The provenance gate
  permits only exact equality or one adjacent IEEE-754 value for external
  platform reconciliation; the old broad `1e-15` tolerance and auxiliary
  NumPy mean were removed.
- Every raw E03 row now records `rng_family_id`. Parameter-cell IDs retain T
  and final-window fraction. Only approved, default-environment/default-learner
  E03-standard T/window OAT cells may share the family; all other cases receive
  distinct semantic family IDs. Smoke default trajectories retain their prior
  scientific outputs.
- The staged, non-executable standard path now has tested pure helpers for
  five-seed fractions and Student-t intervals, 4/5 stability, objective
  bisection, censored/nonmonotone learned refinement, and the `b2=0` harsh
  cells. Its planned writer streams cell chunks directly to CSV and aggregates
  online: 408m new plus 57.12m legacy steps, approximately 384k rows/214 MiB
  raw, with a <2 GiB peak-memory target. No standard simulation was executed.
- Regenerated smoke: 20.801 seconds, 284,107-byte raw file, 384 rows. The
  357-row legacy replay again matched 226 cells, the frozen fraction/mean, and
  SHA-256 `bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`.
  Source fingerprint was independently recomputed from current files. Every
  per-state mask+auth count equals its visit count; raw-to-summary identities
  passed at `1e-12`.
- Targeted E03/E01/E02 tests and `./scripts/verify.sh` passed. Independent
  regeneration byte-matched raw, cells, effects, stable, thresholds, legacy,
  and PNG; normalized machine artifacts matched. Stop again at
  `PENDING_SOL_SMOKE_REVIEW`; no standard, sensitivity, claim, ledger, or
  manuscript work was performed.

## 2026-08-12 — E03 bounded implementation and smoke plan

### Plan

1. Implement an isolated E03 M2 experiment runner, strict frozen smoke and
   staged-standard configuration validation, canonical new-stream seeding, and
   a replay path that calls the maintained M2 diagnostic kernel unchanged.
2. Reproduce the frozen 357-cell legacy map before writing or interpreting
   smoke sentinel results; preserve its original cell-seed formula separately
   from the E03 semantic-ID stream.
3. Emit only the approved smoke artifacts: primary child units for six new-seed
   sentinels, cell/effect/stable/threshold/legacy-replay tables, a diagnostic
   figure, manifest, and a 13-item checkpoint report.  Do not execute standard,
   sensitivity, threshold refinement, claim adjudication, ledger, or manuscript
   work.
4. Run focused E03 and E01/E02 non-regression tests plus `./scripts/verify.sh`,
   then run the smoke configuration once and stop if provenance/replay,
   runtime, or raw-size gates fail.

### Acceptance criteria

- The maintained legacy replay has exactly 357 cell diagnostics, 226
  learned-suboptimal cells, fraction `0.6330532212885154`, classified-cell
  neutral-mask mean `0.9501766068109203`, and the frozen map SHA-256.
- Six smoke sentinels produce exactly 384 canonically ordered child rows using
  the approved semantic-ID `SeedSequence([master_seed, 3, ...])` hierarchy;
  no global RNG state or M2 model semantics/defaults are changed.
- Value iteration converges with the declared tolerance; neutral ties and
  inadequate visits are inconclusive, while missing stigma visits at `p=1`
  cannot erase an adequate neutral mismatch.
- Per-child action/visit/window/reward totals reconcile exactly, raw summaries
  reproduce at `1e-12`, and independent normalized regeneration is identical.
- Actual smoke cost remains below 60 seconds and 20 MiB raw output.  The report
  records the smoke-only gate and staged-standard projection without executing
  it.

### Smoke execution and passed implementation gate

- `configs/frontiers_article/e03_m2_regime_smoke.json` completed using
  `/Users/omer/workspace/venvs/venv314/bin/python` in 20.693 seconds. The
  224,829-byte primary file contains exactly 384 children (six cells times
  n=64); every final-window action count, state visit count, mask count, and
  reward sum reconciled.
- The replay ran before sentinels and wrote 357 legacy diagnostics. It matched
  226 learned-suboptimal cells, fraction `0.6330532212885154`, and legacy map
  SHA-256 `bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`.
  The frozen reported classified-cell mean is `0.9501766068109203`; the local
  NumPy pairwise reduction was one ULP higher (`0.9501766068109204`), while
  every exported legacy row byte-matched the frozen hash. The gate records the
  frozen decimal and numerical reconciliation rather than treating a reduction
  order artifact as changed provenance.
- Five sentinels classified as `learned_suboptimal_masking`; `(p=.35, eta=0)`
  was inconclusive under the frozen visit rule. These are diagnostic smoke
  outcomes only and are not a replicated-grid result or claim decision.
- Targeted E03/E01/E02 tests and `./scripts/verify.sh` passed. An independent
  regeneration byte-matched the raw, cell, legacy, and PNG outputs; normalized
  machine artifacts matched exactly. The staged E03 standard config remains
  explicitly non-executable.
- Artifacts are `results/manifests/frontiers_m2_regime_replication_v1_smoke.json`,
  `results/raw/frontiers_m2_regime_replication_v1_smoke_units.csv`, the seven
  matching E03 summary/figure/report files, and the self-contained checkpoint.
  Stop at `PENDING_SOL_SMOKE_REVIEW`: no standard, sensitivity, claim ledger,
  or manuscript work was executed.

## 2026-08-11 — Step 0 preflight

### Plan and acceptance criteria

1. Freeze the worktree, commit, Python environment, maintained M0-M4 entry
   points, and current claim-ledger artifact selectors.
2. Run the repository verification command without changing model code.
3. Proceed to the separate E01 scientific-approval pass only if verification
   uses the required workspace Python and every baseline check passes.

Acceptance required preservation of all pre-existing worktree changes, use of
`/Users/omer/workspace/venvs/venv314/bin/python`, successful baseline tests and
artifact checks, identifiable maintained entry points and artifacts, and no
change to model semantics, defaults, RNG behavior, article prose, or claims.

### Frozen baseline

- Commit: `e0e9a738986dd440180a228b024b0807336cd957` on `master`.
- Required Python: `/Users/omer/workspace/venvs/venv314/bin/python`, version
  `3.14.6`.
- Tracked-diff SHA-256 at preflight:
  `7c79a96763f4a7d69c312509b29e22270a6e95842d978db2052c1248d1398fd5`.
- Porcelain-status SHA-256 at preflight:
  `f2a3ab688dfa2c99b6bb4cfadc105a7aedb078b94ba49a79faad5841b0855055`.
- The worktree already contained Stage 1 governance/document changes,
  untracked article/output trees, and deleted legacy document artifacts. These
  were treated as pre-existing user work and were not reverted or overwritten.
- Maintained baseline entry points were found in
  `src/gifted_masking/models/m0.py` through `m4.py`, with orchestration in
  `src/gifted_masking/experiments/robustness.py` and
  `src/gifted_masking/cli.py`.
- Claim-ledger selectors and maintained artifacts were present under
  `results/raw/`, `results/summaries/`, `results/manifests/`, and
  `results/reports/`.

### Verification evidence and failed gate

`./scripts/verify.sh` completed with 47 discovered tests and 4 explicit
post-generation artifact tests passing. It regenerated the maintained
robustness and M2 artifacts without reporting a test failure.

The verification gate is nevertheless invalid for Stage 2 because
`scripts/verify.sh` hardcodes `ROOT_DIR/.venv/bin/python`. The resolved
executable was
`/Users/omer/workspace/personal/repos/gifted-masking/.venv/bin/python`, a
repository-local environment. Repository `AGENTS.md` and the Stage 2 runbook
require `/Users/omer/workspace/venvs/venv314/bin/python` and explicitly prohibit
using a repository-local virtual environment.

This is an authority/environment conflict under runbook Sections 2, 4, and 8.
The E01 scientific-approval pass was halted, no E01 implementation or smoke run
was started, and no model, default, RNG, claim, or manuscript change was made.

### Required corrective action

Repair `scripts/verify.sh` so the repository verification command resolves the
required workspace Python, then rerun Stage 2 Step 0 from a freshly recorded
dirty-state hash. Only a valid passing preflight may launch the E01
scientific-approval pass.

## 2026-08-11 — Step 0 correction and passed gate

`scripts/verify.sh` is now pinned to
`/Users/omer/workspace/venvs/venv314/bin/python` and prints the selected
interpreter before running checks. Its post-generation test invocations now use
per-file `unittest discover` calls, avoiding resolution to an unrelated
installed `tests` package in the shared environment.

The first corrected-environment run passed the 47-test discovery suite and all
artifact-generation commands but exposed that test-module resolution defect in
the final checks. After the shell-only correction, the three targeted
post-generation files passed (4 tests), followed by a complete successful
`./scripts/verify.sh` run:

- interpreter: `/Users/omer/workspace/venvs/venv314/bin/python`;
- discovered tests: 47 passed;
- maintained robustness and M2 artifacts: regenerated and validated;
- post-generation artifact/reproducibility tests: 4 passed;
- final exit status: 0.

The passing-gate tracked-diff SHA-256 was
`dd590bcc65a8eb9391cc9da2caf446d80de2da7b35d0921acdca31ada27c5196`;
the porcelain-status SHA-256 remained
`60fb122ed232f332a56d53ad3c794f8aae1d01fd8352eae7c2a1783e973bd2b8`.
No model source, model default, reward equation, transition, action indexing,
or RNG behavior changed. Step 0 is passed and E01 scientific approval may
proceed.

## 2026-08-12 — E01 bounded implementation and smoke plan

### Plan

1. Add the minimum config validation, canonical E01 cell/seed derivation,
   article-experiment CLI, raw/summaries/manifest/report/diagnostic outputs,
   and tests required by `approvals/E01_SMOKE_APPROVAL.md`.
2. Keep all experiment-only intervention logic in a new article experiment
   module; do not modify `src/gifted_masking/models/m0.py`, model defaults, or
   the maintained robustness suite.
3. Run targeted E01 tests, the repository verification command, and exactly
   `configs/frontiers_article/e01_hot_stove_smoke.json`; then perform the
   required reconciliation, normalized-rerun, cell-order, baseline, schema,
   manifest, and manual-sentinel checks.
4. Write the smoke checkpoint and update only affected architecture/state/
   backlog documentation. Stop at the smoke gate without claim adjudication or
   a standard/sensitivity run.

### Acceptance criteria

- The frozen ten cells produce exactly 960 canonically sorted primary rows and
  the six approved artifact paths.
- The maintained-baseline sentinel byte-matches `m0.simulate` for the same
  parameters and seed; E01 does not alter M0 or existing robustness outputs.
- RNG derives from canonical semantic cell IDs, is order-independent, and
  machine-readable outputs byte-match after timestamp/runtime normalization.
- Actual objective payoff remains distinct from counterfactual learning values;
  forced exploration changes actions only and no counterfactual reward enters
  the environment return.
- Raw-to-summary recomputation agrees within `1e-12`, required schema and
  manifest fields validate, all requested tests and `./scripts/verify.sh`
  pass, and no stop condition is triggered.

## 2026-08-12 — E01 smoke checkpoint

1. **Experiment and run ID:** E01, `frontiers_hot_stove_v1_smoke`.
2. **Model, effort, commit, dirty state:** M0; bounded Terra/high-equivalent
   implementation; commit `e0e9a738986dd440180a228b024b0807336cd957`; dirty
   state and combined diff/status hash
   `8b4deeee572d4b7a83db377e5901d08fbb7d26a8638b4affd9f89170cb9f80fa`
   are recorded in the manifest. Pre-existing worktree changes were preserved.
3. **Implemented files and isolated modes:** `experiments/article.py`, the
   E01 JSON config, CLI route, and E01 tests. The modes are
   `controlled_baseline`, `forced_authentic_0.05`, and
   `counterfactual_authentic_feedback`; no M0 source/default/RNG path changed.
4. **Smoke config:** ten frozen cells; n=96/cell; T=300; final window .20
   (steps 240-299); one master seed `2026081199`; workers=1.
5. **Targeted and full verification:** 8 E01 tests passed. The final
   `./scripts/verify.sh` passed using the required workspace Python (55
   discovered tests, maintained artifact generation/validation, and the 4
   explicit post-generation tests).
6. **Baseline reproduction:** the maintained p=.65 lambda=.5 baseline exactly
   matched `m0.simulate` for its recorded semantic cell seed.
7. **Determinism and cell order:** normalized deterministic reruns matched;
   reversed input-cell order preserved the byte-identical raw, cell-summary,
   and effect rows.
8. **Raw-to-summary reconciliation:** 960 raw rows recomputed to 26 cell/
   stratum summaries and 62 diagnostic effects exactly (all deterministic
   comparisons satisfy the required `1e-12` criterion).
9. **Manual semantic inspection:** both controlled accepted/rejected strata
   occur at p=.75 and .85; their lowest-ID sentinels have correct forced-auth
   initial rewards (1.6/-1.4). A forced row had 12 exposures/9 overrides. A
   counterfactual row had 78 masked-feedback events (66 accepted, 12 rejected),
   reward sum 88.8, and realized return 263.7, confirming feedback was not
   credited to the environment. Maintained rows have no forced initial action.
10. **Produced artifacts:**
    - `results/manifests/frontiers_hot_stove_v1_smoke.json`
    - `results/raw/frontiers_hot_stove_v1_smoke_units.csv`
    - `results/summaries/frontiers_hot_stove_v1_smoke_cells.csv`
    - `results/summaries/frontiers_hot_stove_v1_smoke_effects.csv`
    - `results/figures/frontiers_hot_stove_v1_smoke_stratum_diagnostics.png`
    - `results/reports/frontiers_hot_stove_v1_smoke_report.md`
11. **Cost:** experiment-only wall time 0.589 seconds, 596,967-byte primary
    CSV, and 635,760 bytes across all five non-manifest outputs; below the
    approval guardrails. Standard-tier cost remains a separate review item.
12. **Warnings, failed checks, interpretation risks:** none. The one-seed
    smoke has no estimable seed interval and cannot adjudicate C1-C3.
13. **Recommended gate decision:** `PENDING_SOL_REVIEW`. Stop here; only a
    separate Sol/xhigh decision may authorize E01 standard execution.

No claim, claim ledger, manuscript prose, standard run, or sensitivity run was
updated from this diagnostic smoke.

## 2026-08-12 — E01 smoke-gate corrective batch plan

### Plan

1. Correct only the reviewer-identified E01 presentation, pooling, report,
   validation, provenance, and gated-standard-readiness defects.
2. Preserve the frozen M0 semantics, baseline path, default parameters, and
   approved smoke cell execution; add the standard configuration without
   authorizing or executing it.
3. Regenerate E01 smoke only, run targeted tests and full repository
   verification, reconcile the artifacts independently, inspect manual
   sentinels, and update the checkpoint documents for repeat Sol review.

### Acceptance criteria

- The diagnostic figure contains real plotted bars; pooled p=.75/.85 rows are
  equal-weight means of p-specific seed-level effects, never child pooling.
- The smoke report contains all concrete checkpoint outcomes and a cost-based
  standard projection without pending/external placeholders.
- Validation rejects any altered frozen smoke contract; provenance fingerprints
  include binary-safe tracked and untracked source contents and record
  matplotlib's version.
- A five-seed standard config exists but is refused unless an explicit approved
  authorization is supplied; no standard-scale execution occurs.
- Corrected targeted tests, `./scripts/verify.sh`, smoke-only regeneration,
  deterministic/reconciliation checks, and manual sentinels pass with no new
  stop condition.

### Corrective outcome

- Ten targeted E01 tests and the full repository verification passed. The
  corrected smoke was regenerated only; it retains 960 raw rows and no warnings.
- The figure now contains plotted bars. The equal-weight pooled primary
  rejected-minus-accepted final-mask effect is `0.12452302631578949`, computed
  from the two p-specific seed-level effects (`0.2150877193`, `0.0339583333`).
- The manifest records matplotlib `3.10.8`, content-inclusive source fingerprint
  `53b09466386e6eb5c950ca2ba2a9b317f1dbd51a9c782792fd4ceba6bef77111`, and
  passed repository verification. The five-seed standard config exists but the
  runner rejects it; it was not executed.
- Stop for repeat Sol smoke-gate review. No claims or manuscript content changed.

## 2026-08-12 — Second corrective batch plan

### Plan and acceptance criteria

Freeze the M0 payoff, primary-cell optimality, and entire staged-standard
contract; correct the standard projection; and add direct figure/fingerprint
regressions. Acceptance requires mutation rejection for every reviewer case,
independent manifest-hash recomputation, correct 25,000-row/173.611111-step
projection, smoke-only regeneration, passing targeted/full verification, and
no standard execution or claim/manuscript changes.

## 2026-08-12 — E01 Pass D standard execution

- Authorized only by `approvals/E01_STANDARD_GO.md`; executed the frozen standard
  config once per reserved master seed with n=500 and T=2000. No sensitivity
  or publication-tier work ran.
- Produced 25,000 primary rows, 130 cell/stratum summaries, and 186 effects:
  155 seed-level rows and 31 across-seed Student-t 95% interval rows using
  `t=2.7764451051977987`.
- Targeted E01 tests and the full repository verification passed before the
  authorized execution. Row ordering, M0 baseline replay, raw-to-summary
  reconstruction, and manifest/source-row inspection passed. Stop before
  claim adjudication.

### Second corrective outcome

- The ten targeted E01 tests and full verification passed; only the approved
  960-row smoke was regenerated. Manual sentinels and raw-to-summary replay
  remain valid, and the report now carries the corrected 25,000-row,
  173.611111x standard projection.
- Smoke and staged-standard mutation tests reject altered payoff, primary p,
  seed list, n, horizon, window, worker count, keys, and cell set. Standard
  execution remains refused and was not attempted.
- The figure regression verifies both intended bar colors; manifest tests
  independently recompute output and source fingerprints. Stop for repeat Sol
review; no claims, ledger, manuscript, or standard result changed.

## 2026-08-12 — E01 standard provenance repair plan

The preceding "Second corrective outcome" occurred before Pass D despite its
position after the Pass D note; this repair corrects that chronology. Repair
only standard provenance/verification. Acceptance requires an exact standard
tier/command/window/seed report and manifest, post-run verification, and a
normalized deterministic regeneration. Raw data, config, model semantics,
seeds, decision rules, claims, and manuscript remain frozen.

### Provenance repair outcome

- Final manifest tier and raw/config tier are all `standard`; its recorded
  command includes the exact GO approval record. The standard report identifies
  n=500, T=2000, five reserved seeds, and final steps 1600-1999.
- A second authorized regeneration in `/private/tmp/e01-standard-regeneration`
  byte-matched raw, cells, effects, and diagnostic figure. Post-run
  `./scripts/verify.sh` passed, after which the manifest/report were finalized
  with passed verification and refreshed artifact hashes.
- Stop for fresh claim adjudication. No claim ledger, manuscript, sensitivity,
or publication-tier work changed.

## 2026-08-12 — Final standard report wording repair

- Made report wording tier-aware: standard item 2 identifies Pass D, item 12
  identifies standard interpretation risk, and the close records the authorized
  standard execution while excluding sensitivity, publication-tier, and
  adjudication work. Smoke wording remains smoke-specific.
- Added tier-wording regression assertions. Eleven targeted E01 tests and the
  full workspace-venv verification passed. Report and manifest hashes were
  refreshed without changing standard raw rows, summaries, effects, figure,
  config, or seeds. Stop for fresh adjudication.

## 2026-08-12 — E01 Pass E claim adjudication

### Disposition

`SUPPORTED_IN_NARROW_DOMAIN`

The final implementation is valid. The standard and smoke reports are
tier-correct, all manifest output hashes match, and the frozen standard config,
five seeds, 25,000 raw rows, 130 cell/stratum rows, 186 effect rows, and figure
remain unchanged. Ten maintained-baseline seed/cell replays exactly matched
`m0.simulate`; independent raw-to-cell recomputation differed by at most
`9.1e-13`; all 31 five-seed Student-t estimates and intervals reproduced
exactly; and no administrative child-index pairing was used.

### Frozen decision-rule results

- **Direct hot-stove support failed.** At `p=.75`, the rejected-minus-accepted
  final-mask effect was positive in four of five seeds but its mean `0.002479`
  had interval `[-0.017317,0.022274]`. At `p=.85`, only two of five seed
  effects were positive and the mean was `-0.003165`
  `[-0.013669,0.007338]`. The equal-p-weight pooled estimate was `-0.000343`
  `[-0.011605,0.010918]`.
- **The early sampling/regret component passed.** Post-initial authentic
  sampling was lower after rejection in five of five seeds at both p values;
  the pooled effect was `-0.025837` `[-0.035753,-0.015922]`. Pooled normalized
  regret increased by `0.025824` `[0.015914,0.035735]`.
- **Information restoration and materiality passed.** Forced exploration
  reduced rejection-stratum masking by `0.046590`
  `[0.033230,0.059951]` and regret by `0.057954`
  `[0.045614,0.070293]`, relative reductions of `10.8%` and `13.0%`.
  Counterfactual feedback reduced masking by `0.118135`
  `[0.109683,0.126587]` and regret by `0.141318`
  `[0.132369,0.150267]`, relative reductions of `27.4%` and `31.8%`.
- **The maintained C3 contrast passed, but its early-outcome moderation did
  not.** `lambda=2.5` minus `.5` increased final masking by `0.402990`
  `[0.395366,0.410614]`; the high-minus-low-lambda controlled rejection
  gap-in-gap was `-0.001067` `[-0.015031,0.012898]`.

### Maximum wording and selectors

Maximum wording is limited to information restriction for later sampling and
regret in the tested `p=.75/.85` M0 domain, plus the replicated maintained
`p=.65` negative-outcome-weighting contrast. It must state that the controlled
initial rejection did not increase final-window masking and must not claim that
greater `lambda` amplified the early-outcome gap.

Primary selectors are `results/raw/frontiers_hot_stove_v1_units.csv` with
`tier=standard` and the five reserved master seeds, and
`results/summaries/frontiers_hot_stove_v1_effects.csv` with
`level=across_master_seeds` and the named effect rows above. Provenance is in
`results/manifests/frontiers_hot_stove_v1.json`; the execution report is
`results/reports/frontiers_hot_stove_v1_report.md`.

No manuscript prose, sensitivity, or publication-tier run was changed or
executed during adjudication.

## 2026-08-13 — E06 compression release-gate repair

- Implemented only the five Sol `FIX_IMPLEMENTATION` release controls:
  fixture authentication, continuous resource stops, strict one-family replay,
  a reconciled conservative projection, and content-aware post-seal Git drift.
- No E06 standard/qualification execution, repository-wide verification,
  C8/C9 adjudication, claim, manuscript, or Figure 4 action occurred.
- The subsequent smoke refresh remains a pending/unsealed package and requires
  fresh user-owned full verification before any external seal or review.

## 2026-08-13 — E06 standard-readiness implementation

- Implemented exact canonical GO binding, five-master family streaming,
  independent 55-field raw and standard-cell replay, master-level inference,
  frozen contrasts, a five-panel diagnostic, and manifest-last publication.
- E06 focused tests passed 14/14 in 56.216 seconds. Maintained M4/core/
  determinism passed 11/11 in 0.335 seconds; `py_compile` and
  `git diff --check` passed.
- Fresh smoke scientific artifacts remained byte-identical to the sealed
  baseline. Standard, qualification, C8/C9 adjudication, ledger, manuscript,
  and Figure 4 work were not run.
- Correct standard array-length accounting replaced the invalid row-count-only
  raw projection. The reproducible field-shaped bound is 344.136 MiB raw,
  376.136 MiB total, 434.753 seconds, and 226.438 MiB RSS.
- Status is `BLOCKED_BEFORE_FULL_VERIFICATION`: formal 400/500-MiB artifact
  stops pass, but the Round 2 150/200-MiB review limits fail. Resolve that
  contract/limit conflict independently before full verification or GO.

### Deterministic-compression amendment

The user explicitly authorized a standard-only `.csv.gz` implementation. The
logical 55-column CSV, model/RNG semantics, smoke bytes, and qualification
refusal remain unchanged. Canonical gzip uses level 9, `mtime=0`, an empty
filename, and one member; compressed/logical fingerprints are separate and an
independent decompression pass validates raw and cell rows.

The exact 52,000-row high-entropy non-scientific fixture produced 296.980 MiB
logical / 90.615 MiB stored in 36.985 seconds at 157.375 MiB RSS. Its compressed
bytes reproduced three times. Applying its ratio to the 344.136-MiB worst-width
logical bound yields 105.003 MiB raw and 137.003 MiB total; all strict/formal
gates pass. E06 now has 16 focused tests covering gzip headers/members/trailing
bytes, fixture binding, decompressed replay, GO, and inference. Standard and
qualification were not run.

### User verification and compression-ready external seal

The user-owned command completed under the required workspace Python. The log
reconstructed 122 discovery tests in 138.444 seconds plus post-artifact suites
of 1/1/2 tests in 1.705/1.690/3.328 seconds: 126 passing tests in 145.167
seconds. Log SHA-256 is `0b516c8e...a6e7e`; the exact zero exit record SHA-256
is `e0eb8bd6...0063`.

Evidence was archived under
`results/reports/e06_compression_user_verification/`. The one-time production
sealer passed all config/source/Git/artifact/focused/deterministic/full-log
bindings and set the canonical smoke to `passed` /
`external_evidence_verified` without changing any of the eight scientific
hashes. Next status is `READY_FOR_INDEPENDENT_SOL_REVIEW`; standard and
qualification remain refused.

## E06 second FIX_IMPLEMENTATION preverification

Implemented the review-directed bounded correction: complete expected packed
raw-row reconstruction, strict JSON/type comparison, comprehensive named
materialized and parsed-CSV adversarial tests, a 13-item pending report,
expanded provenance, and an evidence-driven external seal interface.  Two
fresh smoke output roots with distinct Matplotlib caches byte-matched the
preserved raw, five summaries, figure, and warnings artifacts.  Full
repository verification, E06 standard, and E06 qualification were not run.
The next gate is the user-owned round-2 verification command.

## 2026-08-13 — E06 second FIX_IMPLEMENTATION external-sealer correction

The remaining sealing defect was corrected without changing M4, any frozen
config, RNG consumption, or the eight scientific artifacts. The external
sealer now reconstructs all full-verification suite totals and runtimes from a
strict log, accepts only the exact newline-terminated zero exit record, and
recomputes config, approval, ordered source fingerprints, Git/dirty state,
scientific artifact hashes, focused logs, and deterministic-regeneration
evidence before an atomic manifest/report update. Synthetic temporary-package
coverage accepts one complete bundle and rejects log/exit/count/runtime,
source/config/approval/Git/dirty, artifact, focused, deterministic,
normalization, already-sealed, and inconsistent-pending corruptions.

The canonical package is refreshed only as
`pending_user_full_verification`/`unsealed`; a user-owned round-2 repository
verification is still required. No full verifier, standard, qualification,
C8/C9 adjudication, ledger, manuscript, or Figure 4 action occurred.

## 2026-08-12 — E04 authorized baseline standard execution

The canonical `E04_STANDARD_GO.md` authorized only the frozen baseline
standard. The dispatch requires that record, the exact config, the five
reserved seeds, one worker, and baseline-only design.

The completed package contains 137,500 raw child rows (55 canonical cells x
five seeds x n=500), 275 curves, 1,182 effects, 55 canonical cells, a 120-row
equivalence table, figure, report, and manifest. Raw storage is 174,838,110
bytes (~166.7 MiB). Raw creation through completed figure took 128.724s, under
the 600s runtime and 400 MiB raw limits; the streamed runner applied the 2 GiB
RSS stop check per cell. An external supervisor interrupted the original
process after figure completion and before serialization, so bounded recovery
revalidated and finalized the completed artifacts. Its 51.4 MiB RSS is a
recovery observation, not reconstructed execution high-water.

Independent canonical-cell replay byte-matched raw, canonical, equivalence,
curves, effects, and figure after deterministic seed-order pooling. Manual
checks confirmed all five seeds, unique seed/cell/child keys, 2,000 total and
400 final-window actions per child, action-vector cardinalities, comparator
payloads, and exact accepted-good discovery equivalence.

Disposition: `PENDING_SOL_STANDARD_REVIEW`. No E04 result is adjudicated here;
no sensitivity, publication, claim/ledger, or manuscript work was performed.

## 2026-08-12 — E05 Pass B bounded smoke implementation

### Plan and acceptance criteria

Implement only the `E05_SMOKE_APPROVAL.md` contract: a separate config-driven
M3 BFLPE crossover kernel, strict frozen-config and raw-artifact validators,
smoke-only CLI dispatch, tests, and the exact diagnostic smoke. The design was
compared before implementation with `ARCHITECTURE.md` (article experiments are
isolated from maintained model kernels), the article RDS (analytic and learned
quantities must stay distinct), `STAGE2_EXPERIMENT_SPECIFICATIONS.md`, and the
E05 approval record. Maintained `models/m3.py`, defaults, and its RNG behavior
must remain unchanged.

Acceptance requires: exact frozen smoke and non-executable standard configs;
accepted-good-auth-only comparison cost; separate architecture family streams
reinitialized across `bf`; the `8/17` analytic anchor; exact 3,456/36 smoke
raw/cell cardinalities; strict raw/summary/effect/transition/provenance
validation; deterministic independent regeneration; E01--E05 targeted tests
and `./scripts/verify.sh`; updated project state/docs; and a stop at
`PENDING_SOL_SMOKE_REVIEW`. No standard, `T=5000`, claim/ledger, or manuscript
action is authorized.

### Smoke checkpoint

- Executed exactly `configs/frontiers_article/e05_m3_bflpe_crossover_smoke.json`
  using `/Users/omer/workspace/venvs/venv314/bin/python`: `n=96`, `T=300`, one
  master seed, final steps `240-299`, 36 architecture-by-bf cells, and 3,456
  primary rows. The staged standard config was loaded only to confirm strict
  validation and dispatcher refusal; it was not executed.
- Produced 18 analytic rows, 36 cell rows, 258 smoke-only effect rows, four
  noninferential transition rows, a diagnostic PNG, manifest, and report.
  Runtime was under two seconds with a 3,513,121-byte raw CSV; peak RSS and
  the implementation's linear readiness calculation were below smoke stops.
- Manual sentinels reproduced analytic advantage `0.40`, `.0175`, `0`,
  `-.00375`, and `-.28` at `bf=0`, `.45`, `8/17`, `.475`, and `.80`;
  `8/17` stored exact zero/tie actions `[0,1,2,4,6]`; final window is exactly
  `240-299`; the same family seed is retained across bf within architecture,
  while flat and hierarchical family seeds differ.
- Raw schema/count/Q-shape/action-count/accept-reject/conditional-rate
  validators and derived artifact cardinalities passed. An independent output
  directory regeneration byte-matched raw, analytic, cells, effects,
  transitions, and PNG; normalized manifests matched.
- Pending final targeted E01--E05 and repository verification. No standard,
  `T=5000`, C7 conclusion, claim-ledger update, or manuscript edit has been
  made. Stop condition remains `PENDING_SOL_SMOKE_REVIEW`.

## 2026-08-12 — E05 scientific approval

### Decision and bounded contract

`APPROVED_FOR_SMOKE`

The scientific-design pass audited E05 against the maintained M3 equations and
tests, the coarse C7 endpoint artifact, and the verified E04 smoke provenance.
It froze flat `2K`, `K=4`, fixed good-context identity `0` as primary and the
hierarchical architecture as a separately analyzed secondary check. It also
froze the exact `8/17` analytic anchor, the 18-point dense/anchor `bf` grid,
architecture-specific common-random-number families across `bf`, ordered raw
and summary schemas, dependency-free PAVA and master-seed bootstrap rules,
decision gates, manual sentinels, and resource limits in
`approvals/E05_SMOKE_APPROVAL.md`.

The approved smoke is `n=96`, `T=300`, final window `.2`, master seed
`2026081599`, 36 architecture-by-`bf` cells, 3,456 primary rows, and 1,036,800
learner-steps. The five-seed `n=500`, `T=2000` config is staged only and must
remain non-executable. `T=5000` points require a later, separate
`E05_T5000_GO.md` after a valid `T=2000` transition and an exact targeted point
list exist.

### Provenance boundary

The maintained analytic replay reproduced `bf*=0.47058823529411764`; the
current coarse C7 result reproduced a `0.9181818181818182` low-minus-high
endpoint difference but remains descriptive because it lacks a dense,
five-seed transition analysis. All seven E04 smoke output hashes and its
approval hash matched. No E05 simulation, implementation, standard run,
claim/ledger change, or manuscript edit occurred in this approval pass.

## 2026-08-12 — E04 smoke-only final validator/review preparation

### Plan and acceptance criteria

- Keep E04 limited to the approved frozen smoke; standard execution, sensitivity
  cells, claims, ledger, and manuscript work remain out of scope.
- Use one shared per-row semantic recomputation for materialized raw validation
  and incremental streaming validation; fail closed on frozen fields, identity,
  action/count/reward/regret, discovery, entropy/allocation, and modal/Q state.
- Regenerate the smoke only after documentation is current, reconcile its
  machine artifacts, compare normalized same/cross-directory regeneration, and
  run targeted E01--E04 plus repository verification.

### Implemented reviewer corrections

- The shared row validator rejects corrupt `bf`, effective-good fraction,
  child seed, RNG-unit declaration, group action count, good-set JSON, modal
  action, mask count, cumulative regret, and inconsistent accepted-good
  discovery/censoring. Adversarial raw and streaming tests cover those fields
  and representative schema groups.
- The 13-item smoke report now records actual effort, commit and dirty-diff
  provenance, implemented files, artifact paths, resource projection, and the
  exact non-authorizing recommendation `RECOMMEND_GO_STANDARD_REVIEW`.

This entry is preparation for smoke review only. It does not approve or run an
E04 standard experiment.

### Final smoke-only performance correction

- Profiling the workspace-venv smoke found repeated validation-time identity
  assignment regeneration as the dominant avoidable cost; the learner remains
  the unchanged vectorized O(nT) kernel. Immutable, independently seeded good
  sets are cached by their full identity-stream inputs, so no policy RNG draw,
  learner update, or scientific output changes.
- The pre/post raw, canonical, equivalence, curve, effect, and figure SHA-256
  values matched exactly. The measured smoke fell from about 4.66s to 2.57s;
  the explicit linear standard-readiness gate now reports 7.45 minutes,
  186.5 MiB raw, and a 442.5 MiB conservative peak budget. This is a capacity
  estimate only; no standard E04 run was performed.
- `ever_accepted_good_auth` is now exactly equivalent to positive accepted-good
  count in both raw and streaming validation, with adversarial tests in both
  directions.

## 2026-08-12 — E04 approved smoke implementation and checkpoint

Implemented only the E04 `APPROVED_FOR_SMOKE` contract: an isolated
config-driven M3 diagnostic kernel, frozen smoke and non-executable standard
configs, canonicalization of 120 requested cells to 55 executable cells, and
diagnostic/raw/summary/figure/report/manifest artifacts. Maintained M3 and
robustness code were not changed.

- Run ID: `frontiers_m3_search_architectures_v1_smoke`; exact smoke: 5,280
  primary rows and 1,584,000 learner-steps (n=96, T=300, final window=.20,
  master seed=2026081499, bootstrap seed=2026081497, workers=1).
- The canonical table has 55 cells (18 each flat, hierarchical, global-mask,
  and one K-invariant fixed-known-good control); the equivalence table has all
  120 requested cells. Aliases never added observations.
- Fixed-identity replays against all maintained M3 architecture kernels,
  raw-schema/cardinality and raw-to-summary reconciliation, global-RNG
  isolation, seed separation, action/reward/regret/entropy/tie sentinels, and
  standard refusal passed. Independent regenerations byte-matched all machine
  CSV artifacts.
- Unexecuted standard projection: 137,500 rows, 275,000,000 learner-steps;
  smoke-derived runtime is under 10 minutes, raw is under ~400 MiB, and
  vector-array lower-bound memory is under 2 GiB. These are planning-only.

`PENDING_SOL_SMOKE_REVIEW`: no E04 standard, sensitivity, claim adjudication,
claim-ledger change, or manuscript edit was executed.

### E04 smoke-gate corrective implementation

The smoke artifact was regenerated after review corrections. The objective
comparator now records each child's architecture-available optimal action set
(all good-authentic actions when authenticity is best; every masking action in
flat/hierarchical when masking is best). The 120-row equivalence table now
names one compatible requested source row for each of exactly 55 canonical
cells. The runner fails closed on duplicate JSON keys, exact types, frozen
seed/cell/cardinality/cross-field drift, and incomplete standard inputs before
any Student-t pooling.

The manifest now captures command, binary dirty/source fingerprints, approval
fingerprint, Python/NumPy/matplotlib versions, seed family IDs including master
seed/sensitivity, output hashes/sizes/timestamps, and readiness data. Measured
smoke peak RSS was approximately 133 MiB; conservative baseline-standard
readiness projects 137,500 rows, 275m learner steps, 5.33 minutes, 186.5 MiB
raw, and 442.5 MiB peak budget. It is a readiness estimate only; no standard
or sensitivity run was executed.

### Final E04 release correction

The release validator now recomputes every raw row's semantic identity and
diagnostic contract: exact policy/identity/cell seeds and matched family,
canonical child IDs/order, good set, comparator, reward equations,
count/rates, discovery censoring, entropy/allocation, modal outcome, Q shapes,
and regret identities. Curves are bound to recomputed raw summaries; effects
are bound to exact frozen keys and recomputed estimates. Normalized manifests
remove output-directory and volatile timing/readiness fields. Same- and
cross-directory regenerations matched after normalization, strict streaming
sequence rejection passed, and E01-E04 targeted plus full verification passed.
No standard, sensitivity, claim, or manuscript action was executed.

### Final reviewer hardening

The final smoke-only correction closes the remaining fail-open paths: raw
validation rejects frozen payoff/learner mutations, settled/discovery-count
mutations, and nonblank values for undefined entropy/allocation fields. Curve
validation now requires raw provenance; effect validation requires curves and
recomputed effect keys. The streaming writer independently rejects seed and
final-window mask/count corruption. Adversarial tests cover each case. After
the final documentation update, smoke artifacts will be regenerated to refresh
manifest source and dirty-diff fingerprints; standard remains refused.

## 2026-08-12 — E02 smoke implementation plan

Implement only the frozen binary-versus-independent-graded E02 smoke dispatcher,
matched seed hierarchy, primary schema, analytic arms, summaries/effects,
artifacts, and regressions. Acceptance requires six forced-initial matched cells
(576 rows), deterministic/reconciled artifacts, preserved E01 regression and
model kernels, and no E02 standard/adjudication run.

## 2026-08-12 — E02 approved smoke execution

### Scope and outcome

- Implemented the isolated `experiments/e02.py` dispatcher and routed E02
  configs through the existing article CLI without changing M0/M1 kernels,
  defaults, or maintained RNG behavior.
- The approved smoke used the frozen six p/architecture cells, `n=96`,
  `T=300`, a final 20% window, master seed `2026081299`, and forced d=1 after
  the policy draw and latent acceptance uniform at t=0.
- The matched SHA-256/SeedSequence pair hierarchy yielded 576 sorted primary
  rows, 15 arm benchmarks, 18 cell/stratum summaries, 192 diagnostic effects,
  a disclosure diagnostic PNG, a manifest, and a 13-item report under the
  `frontiers_m1_binary_graded_v1_smoke` prefix.

### Checks and boundary

- Targeted E02 tests cover analytic endpoints, maintained unforced M0/M1
  replays, forced draw order, matched initial potential outcomes,
  selected-arm-only updates, global RNG isolation, final windows, raw-to-output
  recomputation, cell-order determinism, config mutation rejection, and E01
  standard-approval rejection. Targeted E01 regressions also passed.
- A deterministic regeneration in `/private/tmp` byte-matched raw, arm, cell,
  and effect files after normalization. Manual sentinels covered each p's
  accepted/rejected pair, intermediate and endpoint actions, selected-arm Q
  updates, count/payoff/regret reconciliation, strata, canonical IDs, and
  warning limits.
- The targeted E02/E01 suites and the full workspace-venv `./scripts/verify.sh`
  passed. The E02 manifest and report record that verification, and every
  manifest output hash was independently rechecked.
- Stop at `PENDING_SOL_SMOKE_REVIEW`. No E02 standard, sensitivity, claim
  adjudication, claim ledger update, or manuscript edit was run.

## 2026-08-12 — E02 smoke-gate corrective batch

### Scope and implementation

- Hardened E02 config validation to require exact JSON types and recursively
  frozen top-level, payoff, learner, cell, and standard-only fields. Numeric
  strings, float/integer substitutions, booleans in numeric fields, missing
  nested keys, and unknown nested keys are rejected before any simulation.
- Ported E01-grade provenance: binary-safe dirty-diff/porcelain hashing,
  matplotlib version, content-inclusive source fingerprints spanning the E02
  runner, shared M0/M1/core/repro dependencies, dispatcher, configs, and tests.
- Replaced the O(nT²) stable full-auth policy suffix test with an equivalent
  O(nT) backward scan. A quadratic reference regression covers equality/tie
  behavior and synthetic stable-boundary cases.

### Corrective outcome

- Added full-stream common-potential-outcome checks, shared common-endpoint
  action checks, explicit intermediate-modal/tie/censoring tests, synthetic
  five-seed Student-t interval checks, hardened approval isolation, and
  independent provenance/hash tests.
- The new smoke raw, arm, cell, effect, and figure bytes exactly match the
  pre-fix smoke scientific artifacts. A second regeneration matched again;
  manual paired-event/count/payoff/regret sentinels and E01 smoke/standard
  artifact hashes passed.
- Targeted E02 (14 tests), targeted E01 (11 tests), and full
  `./scripts/verify.sh` passed. The renewed report contains all thirteen
  runbook items, including a non-executed five-seed standard projection.
- Stop at `PENDING_SOL_SMOKE_REVIEW`; no E02 standard, sensitivity, claim,
  ledger, or manuscript action was executed.

## 2026-08-12 — E02 Pass D standard execution

### Authorization and artifacts

- Executed only `configs/frontiers_article/e02_binary_graded_standard.json`
  under `approvals/E02_STANDARD_GO.md`. The dispatcher rejects missing,
  E01, smoke, copied/wrong-path, and malformed authorization records.
- The frozen five reserved seeds, six binary/graded p cells, `n=500`, `T=2000`,
  final steps 1600-1999, one worker, frozen payoffs/learner settings, and
  forced step-zero full authenticity produced 15,000 primary rows, 15 arm
  benchmark rows, 90 cell/stratum rows, 480 paired seed-level effects, and 96
  across-seed Student-t rows (576 effects total).

### Validation and boundary

- An independent temporary standard regeneration byte-matched raw, arms,
  cells, effects, and the diagnostic PNG; normalized machine manifests also
  matched. Raw-to-summary/effect reconstruction, paired initial outcomes,
  final-window/modal/censoring, count/payoff/regret, and representative
  maintained M0/M1 unforced replays passed.
- Targeted E02 (15 tests), targeted E01 (11 tests), and full
  `./scripts/verify.sh` passed after final standard execution. The finalized
  manifest/report record `tier=standard`, the exact E02 GO command/record,
  verification, artifact hashes, and runtime/storage.
- Stop at `PENDING_E02_CLAIM_ADJUDICATION`. No sensitivity, publication-tier,
  claim/ledger update, or manuscript edit was executed.

## 2026-08-12 — E02 Pass E claim adjudication

### Disposition

`SUPPORTED_IN_NARROW_DOMAIN`

The final implementation is valid. The frozen standard config and E02 GO
record match the manifest; all recorded output hashes and the content-inclusive
source fingerprint match; and the standard prefix contains 15,000 primary
rows, 15 arms, 90 cells, 576 effects, the diagnostic figure, manifest, and
standard report, distinct from smoke artifacts. An independent standard
regeneration byte-matched raw, arms, cells, effects, and figure, and normalized
machine manifests matched after finalizing verification metadata.

Independent audit reconstructed event rewards, action/count vectors, objective
payoff and pseudo-regret, post-initial exploration mean/population variance,
final-window steps 1600-1999, unique modal/tie fields, and stable-policy
censoring for all 15,000 rows. It reconstructed all cell summaries and all
seed/across-seed effects and Student-t intervals. All 15 master-seed/p forced
trace pairs shared the full latent-uniform stream and updated only selected
arms; all 30 unforced standard architecture cells exactly replayed maintained
M0/M1 outputs. Pairing was confined to the same master seed and p; p cells and
master seeds had distinct policy/environment seeds. Targeted E02 tests and the
post-adjudication 73-test `./scripts/verify.sh` run passed.

### Frozen decision-rule results

- **Exploration effect 1 passed.** In the rejected-initial-outcome stratum,
  graded any-disclosure minus binary full-authentic post-initial rate was
  positive in five of five seeds at `p=.75` and five of five at `p=.85`.
  Estimates were `0.349635` `[0.346303,0.352967]` at `.75`, `0.160446`
  `[0.158193,0.162698]` at `.85`, and `0.255040`
  `[0.253004,0.257077]` for the prespecified equal-p-weight pool.
- **Endpoint discovery effects 3 and 4 failed.** Final-window full-authentic
  rate differences were negative in five of five seeds at both p values and
  pooled to `-0.328692` `[-0.342037,-0.315348]`. Optimal-endpoint modal-
  probability differences were also negative in all five seeds at both p
  values and pooled to `-0.221740` `[-0.288755,-0.154724]`.
- **Regret effect 5 failed.** Binary minus graded normalized regret was positive
  at `p=.75` (`0.051046` `[0.048990,0.053101]`) but negative at `p=.85`
  (`-0.110568` `[-0.116966,-0.104169]`). The prespecified pooled effect was
  negative in all five seeds: `-0.029761` `[-0.033874,-0.025648]`.
- The `p=.65` cell was control only. It also showed positive nonzero-disclosure
  exposure (`0.422146` `[0.416591,0.427700]`) together with lower endpoint
  selection and worse regret. Effect 8/mean disclosure was not used in any
  decision.

### Maximum wording and selectors

Maximum wording is: “In the tested forced-initial M0/M1 comparison at `p=.75`
and `.85`, independent graded actions increased post-rejection nonzero
disclosure relative to binary full-authentic resampling by 0.255 (95% Student-t
interval 0.253 to 0.257). They did not improve discovery of the objectively
optimal full-authentic endpoint or pooled normalized regret; instead, the
additional arms diluted endpoint sampling.” Do not claim protective ladder
climbing, smooth generalization, improved endpoint discovery, or regret benefit.

Primary selectors are
`results/raw/frontiers_m1_binary_graded_v1_units.csv` with `tier=standard`,
`initial_outcome=rejected`, `p in {.75,.85}`, the five reserved master seeds,
and both architectures; and
`results/summaries/frontiers_m1_binary_graded_v1_effects.csv` with
`level=across_master_seeds`, `stratum=rejected`,
`p=pooled_equal_weight_p_0.75_0.85`, and effects 1, 3, 4, and 5 named above.
Provenance is in `results/manifests/frontiers_m1_binary_graded_v1.json`; the
execution report is `results/reports/frontiers_m1_binary_graded_v1_report.md`.

One non-decision metadata limitation remains: standard master-seed effect rows
correctly have blank per-seed intervals but retain the smoke-specific
`ci_status=not_estimable_smoke` label and diagnostic note. Across-seed rows and
all decision estimates/intervals are correct, so this does not invalidate the
experiment. Repair it in a later separately authorized infrastructure batch
without changing or rerunning the adjudicated scientific artifacts.

No manuscript prose, sensitivity, or publication-tier run was changed or
executed during adjudication.
