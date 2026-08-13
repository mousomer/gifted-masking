# Frontiers Article Sub-project — Current State

## Status

- Stage 1 — Establish the source of truth is complete.
- RDS version `0.4` is active.
- Current stage: **Stage 2 — Close essential evidence gaps**.
- Stage 1 authored only article-governance Markdown under
  `projects/frontiers_article/`; it did not change model code, model semantics,
  defaults, or RNG behavior.
- E01 smoke, authorized standard execution, provenance repair, and separate
  Pass E adjudication are complete. The disposition is
  `SUPPORTED_IN_NARROW_DOMAIN`; no E01 sensitivity, publication-tier, or
  unapproved follow-on run was executed.
- E02 smoke implementation and its approved diagnostic run are complete:
  six forced-initial matched cells produced 576 raw units, 15 analytic-arm
  rows, 18 cell/stratum summaries, 192 seed/aggregate diagnostic effects, a
  figure, manifest, and 13-item checkpoint. Its separately authorized Pass D
  standard execution then produced 15,000 primary rows, 15 arm benchmarks, 90
  cell/stratum summaries, 576 paired seed/Student-t effect rows, a figure,
  manifest, and standard-tier report. Separate Pass E adjudication is complete
  as `SUPPORTED_IN_NARROW_DOMAIN`: graded independent arms preserved nonzero-
  disclosure exploration after rejection but diluted full-authentic endpoint
  discovery and did not improve pooled regret. The claim ledger was updated;
  no manuscript, sensitivity, or publication-tier work occurred.
  Targeted E02/E01 tests and `./scripts/verify.sh` passed; standard raw, arm,
  cell, effect, and figure files byte-match an independent deterministic
  regeneration.
- The repeat smoke-gate corrective batch strengthened recursive JSON type/value
  validation and binary-safe provenance, expanded the report and regressions,
  and replaced the stable-policy diagnostic's quadratic suffix search with an
  equivalent linear scan. The pre- and post-fix smoke scientific artifacts,
  including the PNG, byte-match exactly.
- E03 smoke implementation and its approved diagnostic execution are complete:
  the historic 357-cell map replayed with 226 learned-suboptimal cells, frozen
  fraction and map hash; six new-stream sentinels produced 384 child rows,
  machine artifacts and the diagnostic PNG byte-matched an independent rerun,
  and repository verification passed. At the smoke gate it was pending separate
  Sol review; no unapproved E03 standard, sensitivity, claim, ledger, or
  manuscript work ran.
  The smoke-gate correction now records exact `math.fsum` legacy provenance,
  state-level count reconciliation, a genuine default-T/window-only RNG family,
  standard-ready streaming/aggregation helpers, and an E03-specific future-GO
  dispatcher. The refreshed smoke source fingerprint and independent rerun
  match; the frozen standard config was non-executable until the later
  canonical E03-specific GO record described below.
  Final readiness correction makes five-seed exact-grid summaries fail closed
  on seed/cell cardinality and component isolation, uses collision-resistant
  component/sensitivity-aware parameter IDs, and records the measured 372.8
  MiB standard raw estimate with a ~400 MiB bound and ~35.6 MiB stream peak.
- E03 Pass D standard execution is complete under the canonical E03 GO record:
  five reserved seeds produced 364,800 streamed primary rows, 2,250 cell
  records, exact-grid seed fractions/Student-t intervals/4-of-5 stability,
  objective and bounded learned-threshold outputs, harsh `b2=0` diagnostics,
  the legacy replay, figure, manifest, and 13-item report. It took 167.454
  seconds and wrote 391,221,606 bytes (~373 MiB), within its four-minute and
  ~400 MiB gates. An independent streamed regeneration byte-matched all
  machine artifacts and PNG; raw-to-cell reconciliation and post-output E03,
  E01/E02, and full repository verification passed. Separate Pass E
  adjudication is complete as `SUPPORTED_IN_NARROW_DOMAIN`: 243 of 357 cells
  were stably learned-suboptimal, every seed fraction was `243/357`, and all
  five dynamic-authenticity sentinels survived the frozen `n`/`T`/window
  checks. The claim is qualified because `gamma=.5` changed three sentinel
  classifications by changing the objective M2 policy to masking. The claim
  ledger was updated; no manuscript, publication-tier, or further sensitivity
  work occurred.
- E04 Pass D and separate Pass E adjudication are complete. The frozen
  GO-authorized baseline produced 137,500 primary rows, 275 curves, 1,182
  effects, 55 canonical cells, and 120 aliases. The disposition is
  `SUPPORTED_IN_NARROW_DOMAIN`: flat and hierarchical K responses were
  negative in all five seeds and differed from the practically equivalent
  controls; randomized identity preserved the direction, while two-good and
  proportional-25 variants attenuated it. All hashes, authorization/config
  fingerprints, streamed raw semantics, raw-to-curve-to-effect reconstruction,
  and 197 five-seed Student-t intervals passed independent adjudication. No E04
  sensitivity, publication-tier, manuscript, or simulation rerun occurred.
- E05 standard execution and separate Pass E adjudication are complete as
  `SUPPORTED_IN_NARROW_DOMAIN`. In flat 2K, all five seed curves crossed `.5`;
  the learned transition was `bf=0.312852` with master-seed bootstrap interval
  `[0.307836,0.316918]`, before the exact objective crossover
  `8/17=0.470588`. The hierarchical response was already below `.5` at the
  lower dense boundary, so its crossing was not estimable. Deterministic
  three-shard reproduction, output hashes, focused/full/post-artifact checks,
  and provenance passed. No `T=5000` or publication-tier work occurred.
- E06 user-owned full repository verification passed: 113 discovery tests and
  the 1/1/2 post-artifact suites completed with exit code zero under the
  required workspace Python. The fresh independent smoke review nevertheless
  returned `FIX_IMPLEMENTATION`. The canonical smoke itself has real action,
  outcome, reward, and state diagnostics; maintained-M4 parity, exact current
  raw reconciliation, deterministic fresh-directory regeneration, derived
  corruption rejection, and the phase-separated core capacity gate passed.
  However, the packed-raw validator accepted representative frozen identity,
  seed-map, parameter, traversal, disabled-reset, and authentic-Q continuity
  corruptions, so the raw-grounded derived boundary is not fail-closed. The
  canonical report also remains seven rather than 13 items and its manifest has
  stale/incomplete verification and provenance. Standard, qualification, C8/C9
  adjudication, ledger, manuscript, and Figure 4 actions remain refused.
- Model routing is established: Sol owns scientific judgment and release gates;
  Terra owns bounded implementation and production after requirements are fixed.
- `runbooks/STAGE2_EVIDENCE.md` now provides the complete smoke-first operating
  procedure, handoff decisions, stop conditions, reports, and launch prompts.
- Stage 2 Step 0 passed on 11 August 2026 after `scripts/verify.sh` was corrected
  to use `/Users/omer/workspace/venvs/venv314/bin/python`; 47 discovered tests,
  maintained artifact regeneration/validation, and 4 post-generation tests
  passed. See `STAGE2_EXECUTION_LOG.md`.

## Stage 1 Deliverables

1. `CLAIM_LEDGER.md`
   - freezes six primary, two secondary, and two excluded claims;
   - links every claim to exact artifacts, result selectors, generators or
     missing generators, source-chapter lines, current DOCX paragraphs, and
     figure/table anchors;
   - sets maximum current wording and stronger-wording evidence gates;
   - freezes article terminology.
2. `MANUSCRIPT_INTEGRATION_MAP.md`
   - assigns all 156 prose paragraphs across the four source chapters;
   - assigns the 17 literature references to a citation pool;
   - maps sources to the final Introduction, Methods, Results, and Discussion
     functions and current DOCX anchors.
3. `STAGE2_EXPERIMENT_SPECIFICATIONS.md`
   - defines E01 hot-stove information restoration;
   - E02 binary-versus-graded disclosure;
   - E03 M2 regime replication;
   - E04 M3 search architectures/context identity;
   - E05 dense BFLPE crossover;
   - E06 M4 path diagnostics;
   - fixes shared seed, uncertainty, artifact, decision, and stop/go rules.

## Reconciled Evidence Boundaries

1. Manuscript intervals come from
   `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`,
   which resamples independently seeded conditions separately. The maintained
   matched-child uncertainty rows must not replace them.
2. The M1 estimate `0.569` is a receptivity contrast within M1; it does not
   establish a binary-versus-graded benefit.
3. E01 directly supports information restriction for later sampling and regret
   in the tested M0 domain: restoration reduced both masking and regret after
   rejection. A single initial rejection did not increase final-window
   masking, so the broader persistent hot-stove wording remains prohibited.
4. The historic M2 `226/357` value remains provenance. E03's publication-facing
   default-learner result is 243 stable learned-suboptimal cells out of the same
   357-cell tested grid, not a learner or human prevalence estimate; it is
   explicitly qualified by learner discount sensitivity.
5. The M3 flat effects `0.200` and `0.168` come from different maintained runs
   and must remain labeled rather than combined.
6. The M4 continuation result is schedule-specific path dependence, not
   established hysteresis.
7. The current article TIFFs and manuscript-specific CSVs do not have a
   checked-in article-specific deterministic regeneration script; Stage 5 must
   close that provenance gap.

## Immediate Next Actions

1. Apply the bounded E06 validation/sealing correction in
   `checkpoints/E06_SOL_SMOKE_REVIEW.md`: reconstruct every frozen raw field,
   add complete adversarial coverage, and complete the canonical 13-item report
   and provenance/verification record without changing scientific bytes. Then
   repeat user-owned full verification and fresh independent smoke review.
   Standard, qualification, C8/C9 adjudication, ledger changes, and manuscript
   changes remain refused.
2. Preserve the paired E05 result in `E05_MAIN_RESULTS.md`: the flat learned
   crossing `bf=0.312852` occurred before the exact objective crossover
   `8/17=0.470588`; no hierarchical crossing was estimable in the approved
   range. Do not run `T=5000` without a separate GO record.
3. Preserve the adjudicated E03 config, five-seed hierarchy, primary rows,
   hashes, exact selectors, censoring results, and maximum wording. Do not run
   additional E03 sensitivity/publication work or rebuild manuscript Figure 3
   without the next separately authorized stage action.
4. Preserve the adjudicated E04 baseline config, five-seed hierarchy, hashes,
   exact selectors, and bounded wording. Any p/tau sensitivity or broader M3
   generalization requires a separate approval and may not replace this result.
5. Preserve the adjudicated E01 config, seed hierarchy, primary rows, hashes,
   and maximum wording; treat any change as a new scientific review item.
6. Preserve the adjudicated E02 config, matched RNG hierarchy, primary rows,
   hashes, and maximum wording. Do not run E01/E02 sensitivity or publication-
   tier work without a separately approved cost and evidence-gap decision.

## E03 Standard Adjudication

- **Disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for the frozen default M2
  learner and exact tested grid.
- Every reserved master seed classified `243/357` exact-grid cells as learned
  suboptimal masking (`0.680672268907563`); the across-seed Student-t interval
  is `[0.680672268907563,0.680672268907563]`. The stable-cell table contains 243
  learned-suboptimal cells, 107 learner/objective matches, and seven unstable
  low-`p`, `eta=0` cells. This passes the `>=179` and lower-bound `>0.40` rules.
- The 243 learned-suboptimal cells split into 141 where dynamic M2 authenticity
  overrides static M0 masking and 102 where both static M0 and dynamic M2 favor
  authenticity. Their strict neutral objective Q gaps range from `0.00217546`
  to `0.85`; classification uses that neutral decision gap, not aggregate mask
  rate or an unavailable full-policy regret.
- All 150 records spanning five dynamic-authenticity sentinels, five seeds, and
  baseline/`n=320`/`T=2000,5000`/window `.1,.4` cases remained learned
  suboptimal masking. Neutral visits were adequate in every decision-bearing
  sentinel case. The learner qualification nevertheless triggers: at
  `gamma=.5`, three sentinels become learner/objective matches because value
  iteration selects masking; low `alpha=.03` and high `tau=.6` also reduce
  upper-`p` sentinel stability.
- In the harsh `b2=0`, `r2=8`, `delta=.3`, `eta=0` cases, only `p=.75` meets
  the structural selector: static M0 authenticity, objective M2 masking, and
  `optimal_policy_masking` in all five seeds. At `p=.70` both objective axes
  select masking; at `p=.80` value iteration selects authenticity and learned
  masking is learner failure.
- Objective bisection reproduced brackets of width `6.1035e-05` at all three
  eta values. Learned refinement is censored, not estimated: inconclusive low-
  `p` cells at `eta=0`, and no crossing at `eta=.2` or `.8`. No extrapolated
  learned threshold is permitted.
- All manifest hashes, the content-inclusive source fingerprint, config and GO
  record, 2,250 cell/seed records, 364,800 primary rows, seed derivations, and
  raw count/reward summaries independently reconciled. Exact-grid effects and
  stability tables contain no sentinel, harsh, smoke, or refinement rows. The
  raw file is deterministically ordered by parameter ID, master seed, and child
  ID; the manifest's shorter declared `sort_keys` list names a different order
  and omits child ID. This is a non-decision metadata limitation, not scientific
  contamination, and should be repaired without rerunning the evidence.
- Exact selectors and maximum wording are frozen in `CLAIM_LEDGER.md`. No
  manuscript prose or figure was changed during adjudication. The required
  post-adjudication `./scripts/verify.sh` passed 87 discovered tests and four
  explicit post-generation tests; no E03 evidence run was repeated.

## E01 Smoke Checkpoint

- Run ID: `frontiers_hot_stove_v1_smoke`; config:
  `configs/frontiers_article/e01_hot_stove_smoke.json`.
- Artifacts: manifest, 960 primary rows, 26 cell/stratum summaries, 62
  diagnostic effect rows, a stratum diagnostic figure, and the 13-item report
  under `results/` with the run ID prefix.
- Baseline M0 reproduction, canonical cell-order independence, normalized
  deterministic reruns, raw-to-summary reconciliation, required schema, and
  manual semantic sentinels passed. The smoke produced no warning and took
  about 0.55 seconds after the local plotting cache was initialized.
- The checkpoint is diagnostic only. No C1-C3 claim was adjudicated, and no
  standard or sensitivity result may be inferred from it.
- Corrective smoke review fixes are complete: the diagnostic figure is
  nonblank, equal-weight p=.75/.85 seed-level pooled effects are emitted, the
  report is self-contained, source fingerprints include untracked contents,
  and an explicitly non-executable five-seed standard config is staged.
- E01 standard Pass D is complete under its GO record: five reserved seeds,
  25,000 primary rows, seed-level summaries, and Student-t seed intervals.

## E01 Standard Adjudication

- **Disposition:** `SUPPORTED_IN_NARROW_DOMAIN`.
- Early rejection reduced post-initial authentic sampling by `0.025837`
  (95% Student-t interval `[0.015922,0.035753]` in absolute magnitude) and
  increased normalized regret by `0.025824` `[0.015914,0.035735]`, but its
  pooled final-mask effect was `-0.000343` `[-0.011605,0.010918]`.
- Forced exploration reduced rejection-stratum final masking by `0.046590`
  `[0.033230,0.059951]` and normalized regret by `0.057954`
  `[0.045614,0.070293]`. Counterfactual feedback reduced them by `0.118135`
  `[0.109683,0.126587]` and `0.141318` `[0.132369,0.150267]`.
- Increasing `lambda` from `.5` to `2.5` in the maintained `p=.65` contrast
  increased masking by `0.402990` `[0.395366,0.410614]`; the controlled
  early-rejection gap-in-gap was not supported (`-0.001067`,
  `[-0.015031,0.012898]`).
- Exact selectors are in `CLAIM_LEDGER.md`; the manifest is
  `results/manifests/frontiers_hot_stove_v1.json`, primary rows are
  `results/raw/frontiers_hot_stove_v1_units.csv`, and effects are
  `results/summaries/frontiers_hot_stove_v1_effects.csv`.
- The standard package passed baseline replay, raw-to-summary and Student-t
  recomputation, independent deterministic regeneration, artifact hashing, and
  post-run `./scripts/verify.sh`. No model semantic, default, objective payoff,
  or RNG change was made.

## E02 Standard Adjudication

- **Disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for exploration exposure only.
- In the rejected-initial-outcome stratum, effect 1 (graded any-disclosure minus
  binary full-authentic post-initial rate) was positive in five of five seeds
  at both authenticity-optimal p values: `0.349635`
  `[0.346303,0.352967]` at `p=.75` and `0.160446`
  `[0.158193,0.162698]` at `p=.85`. The equal-p-weight pooled effect was
  `0.255040` `[0.253004,0.257077]`.
- Endpoint discovery failed. Effect 3 (final-window full-authentic rate) was
  negative in five of five seeds at both p values and pooled to `-0.328692`
  `[-0.342037,-0.315348]`. Effect 4 (optimal-endpoint modal probability) was
  also negative in all five seeds at both p values and pooled to `-0.221740`
  `[-0.288755,-0.154724]`.
- Regret benefit failed. Effect 5 (binary minus graded normalized regret) was
  positive at `p=.75` (`0.051046` `[0.048990,0.053101]`) but negative at
  `p=.85` (`-0.110568` `[-0.116966,-0.104169]`); the prespecified pooled
  effect was negative in all five seeds, `-0.029761`
  `[-0.033874,-0.025648]`. The `p=.65` mask-optimal cell was control only, and
  mean disclosure was not a decision input.
- The standard implementation is valid: all hashes and the content-inclusive
  source fingerprint match; all 15 p-by-seed trace pairs shared the full latent
  uniform stream; all 30 unforced standard cells replayed maintained M0/M1;
  primary-row definitions and 90 cell/576 effect rows reconstructed; all
  Student-t intervals reproduced; and no child was paired across p values or
  master seeds. Raw, arms, cells, effects, and figure byte-matched an
  independent regeneration, normalized manifests matched, and the post-
  adjudication 73-test `./scripts/verify.sh` run passed.
- The maximum wording is limited to changing or preserving nonzero-disclosure
  exploration exposure in the frozen independent-five-arm, forced-initial,
  `p=.75/.85`, default-learner domain. Do not claim improved endpoint discovery,
  regret, smooth generalization, or protective ladder climbing. Exact selectors
  are recorded in `CLAIM_LEDGER.md`.
- Minor metadata limitation: standard master-seed effect rows correctly leave
  per-seed intervals blank but retain the smoke-specific
  `ci_status=not_estimable_smoke` label and diagnostic note. The across-seed
  rows, estimates, and intervals are correct; this label does not affect the
  adjudication and should be repaired without rerunning the science.

## Stage 1 Verification

- `./scripts/verify.sh` now passes using the required workspace virtual
  environment; Stage 2 preflight corrected and independently reran the command
  after detecting the earlier repository-local environment mismatch.
- 47 discovered tests and 4 explicit artifact/reproducibility tests passed.
- The paragraph-map audit found no missing source prose paragraph, literature
  reference, or current main-text DOCX anchor from P11 through P77.
- No unintended architectural drift was introduced; article governance remains
  subordinate to repository model-semantics authority.

## Stage 2 Gate

Stage 2 is complete only when every primary claim is either supported at the
RDS publication minimum or explicitly narrowed/excluded; E01-E06 artifacts are
machine-readable and deterministic; all headline stochastic results include
independent-master-seed uncertainty; and repository verification passes.

## E04 Final Release Correction

- E04 raw/curve/effect validators now recompute frozen semantic identifiers,
  seeds, good sets, comparator/reward/count/entropy/modal/regret diagnostics,
  and exact effect keys. Normalized artifacts are location/timing independent;
  strict streaming sequence checks passed.
- The smoke was regenerated and E01-E04 targeted plus full verification passed.
  The later canonical `approvals/E04_STANDARD_GO.md` authorized the exact
  baseline standard, which has since completed and been independently
  adjudicated as `SUPPORTED_IN_NARROW_DOMAIN` under the selectors below.

## E04 Smoke Checkpoint

- E04 `APPROVED_FOR_SMOKE` infrastructure is implemented and the frozen smoke
  completed as `frontiers_m3_search_architectures_v1_smoke`.
- The isolated kernel preserves maintained M3/robustness code, canonicalizes
  120 requested cells to 55 executable cells, records identity, discovery,
  allocation/entropy, modal, reward, and regret diagnostics, and stages an
  exact but non-executable five-seed standard config.
- The diagnostic smoke has 5,280 raw rows and 1,584,000 learner-steps. Replay,
  reconciliation, deterministic regeneration, and targeted tests passed.
- This checkpoint was originally pending smoke review. The later canonical
  E04 GO record authorizes only the frozen baseline standard; that run has not
  occurred, and no claim, ledger, sensitivity, or manuscript action follows
  from the smoke.

### Corrective smoke readiness

- E04 comparator actions, equivalence metadata, strict JSON/config/raw/curve/
  effect validation, provenance, matched-family IDs, entropy denominators, and
  baseline-standard readiness estimates were corrected and smoke regenerated.
- Smoke RSS was approximately 133 MiB; projected baseline-standard raw is
  approximately 186.5 MiB with a 442.5 MiB conservative process budget.
  This remains non-authorizing readiness information only.

### Final reviewer hardening

- Frozen payoff/learner, settled/discovery, undefined-field, upstream
  provenance, and streaming seed/mask corruption now fail closed. The smoke
  artifact will be regenerated after this documentation update; standard stays
  refused.

### E04 final smoke-review preparation

- Materialized and streaming raw outputs now share a single frozen per-row
  semantic recomputation. It covers configuration/seed/identity/action,
  counts, discovery, entropy/allocation, modal/settling, Q-shape, reward, and
  regret cross-fields; adversarial tests include all newly requested corruptions.
- The 13-item report records actual effort and dirty-state hash, implemented
  files, artifact paths, and the recommendation
  `RECOMMEND_GO_STANDARD_REVIEW`. That recommendation was subsequently reviewed
  and the canonical E04 GO record was written; no standard, sensitivity,
  claim, ledger, or manuscript work has yet been executed.

### E04 smoke performance/readiness correction

- The validator now caches immutable good-set assignments by independent
  identity-stream inputs. Pre/post scientific raw/summaries/figure hashes are
  byte-identical, while the measured smoke is about 2.57s and projects a
  baseline standard at about 7.45 minutes, 186.5 MiB raw, and 442.5 MiB peak.
  The runner rejects a smoke whose linear projection exceeds 10 minutes.
- Accepted-good discovery is exact in both directions:
  `ever_accepted_good_auth == (good_auth_accept_count_total > 0)`; raw and
  streaming adversarial tests cover both invalid directions. Standard remains
  absent; execution must use the canonical E04 GO record and a corrected
  standard dispatcher rather than treating smoke as evidence.

## E04 Standard Checkpoint

- The GO-authorized frozen baseline completed 137,500 raw rows, 275 curves,
  1,182 effects, 55 canonical cells, and 120 equivalence rows. Raw storage is
  174,838,110 bytes (~166.7 MiB), with 128.724s from raw creation to figure.
- The original process was externally interrupted after its completed figure
  and before serialization. Bounded recovery revalidated and finalized it;
  recorded 51.4 MiB is recovery RSS, not reconstructed execution high-water.
  The streamed runner enforced <600s/<400MiB/<2GiB limits per cell.
- Independent replay byte-matched raw, canonical, equivalence, curves, effects,
  and figure after deterministic seed-order pooling. This checkpoint stopped at
  `PENDING_SOL_STANDARD_REVIEW`; the subsequent separate adjudication is
  recorded below. No sensitivity or manuscript work followed from Pass D.

## E04 Standard Adjudication

- **Disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for representation-dependent
  search burden in the frozen baseline M3 domain.
- Fixed-one-good settling slopes were `-0.058240`
  `[-0.063915,-0.052565]` for flat 2K and `-0.114760`
  `[-0.124541,-0.104979]` for hierarchical; their K=16-minus-K=1 changes were
  `-0.234000` and `-0.470400`. Every seed had the negative direction.
- Slope contrasts against global mask were `-0.059960`
  `[-0.065503,-0.054417]` and `-0.116480`
  `[-0.126124,-0.106836]`. Global mask changed by only `0.008800`
  `[0.002090,0.015510]` from K=1 to K=16, and fixed-known-good was
  structurally zero; both passed the prespecified practical-equivalence rule.
- Randomized identity preserved K=16-minus-equivalent-K=1 declines of `-0.2400`
  `[-0.2571,-0.2229]` and `-0.4596` `[-0.4683,-0.4509]`. Two-good slopes
  remained negative but were attenuated; proportional-25 slopes were near zero.
  The result therefore supports scarce-receptive-context search burden, not an
  inherent harm of context count.
- The adjudication revalidated all 137,500 streamed rows, reconstructed all 275
  curves and 1,182 effects, independently reproduced all 197 Student-t
  intervals, and matched the exact config, GO record, source fingerprint, and
  output hashes. Bounded recovery after an interruption was valid and did not
  simulate or alter rows. Exact selectors and maximum wording are frozen in
  `CLAIM_LEDGER.md`; no sensitivity, publication-tier, manuscript, result, or
  code change was made.

## E05 Smoke Checkpoint (historical; superseded by standard adjudication)

- E05 `APPROVED_FOR_SMOKE` infrastructure is implemented and the exact
  diagnostic smoke completed as `frontiers_m3_bflpe_crossover_v1_smoke`.
- The isolated kernel preserves maintained M3/default/RNG behavior, applies
  `bf` only to accepted authentic reward in fixed good context 0, records the
  exact `8/17` analytic anchor separately from learned responses, and keeps
  flat and hierarchical matched-family streams separate.
- Artifacts contain 3,456 raw rows, 18 analytic rows, 36 architecture-by-bf
  cells, 258 smoke-only effects, four noninferential transitions, a diagnostic
  figure, manifest, and checkpoint report. Raw/schema checks, reconciliation,
  manual anchor sentinels, and byte-matched independent regeneration passed.
- At this historical checkpoint the staged standard remained refused. It was
  later separately authorized, executed, and adjudicated below. This paragraph
  is retained only to preserve the gate history and is not the current status.

## E05 Standard Adjudication

- **Disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for the frozen K=4,
  fixed-good-context, default-learner flat-2K representation.
- The exact GO-authorized package contains 90,000 raw rows, 18 analytic rows,
  180 cells, 1,548 effects, and 12 transition rows. Independent reconstruction
  passed raw and derived validation and matched all output hashes.
- Flat 2K passed every frozen primary rule: 5/5 valid seed crossings, pooled
  transition `0.312852`, 95% master-seed bootstrap interval
  `[0.307836,0.316918]`, 10,000/10,000 valid bootstrap crossings, and zero
  material upward adjacent violations. The distinct analytic objective
  crossover is `8/17 = 0.470588`.
- Hierarchical had 0/5 valid seed crossings and no pooled crossing because its
  learned response was already below `.5` at the dense lower boundary. It is a
  boundary result, not support for an architecture-general learned threshold.
- Provenance closure matched source fingerprint `f229a17d...`, every output
  hash, and all three 30,000-row shard hashes against the assembled raw file.
  Recorded reproduction was 96s aggregate (50s maximum block), 88.502 MiB raw,
  89.115 MiB total, and 606.172 MiB observed peak RSS, within all frozen gates.
- Exact selectors and maximum wording are frozen in `CLAIM_LEDGER.md`. No
  `T=5000`, sensitivity, manuscript, result, code, or publication-tier action
  was performed during adjudication.
- The paired analytic--simulation meaning and mandatory manuscript preservation
  rules are recorded in `E05_MAIN_RESULTS.md`. Article chapters now state the
  dense E05 result rather than the obsolete two-endpoint result.
