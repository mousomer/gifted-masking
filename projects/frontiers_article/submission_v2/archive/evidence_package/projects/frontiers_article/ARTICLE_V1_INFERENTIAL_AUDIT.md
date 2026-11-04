# Article V1 Inferential-Replication Audit

**Audit date:** 2026-08-13  
**Scope:** frozen standard E01–E05 artifacts only  
**Scientific simulations run for this audit:** none

## Summary

| Experiment | Inferential unit | n independent units | Interval method | Population/stratum | Status |
| --- | --- | ---: | --- | --- | --- |
| E01 | one master-seed effect estimate | 5 | two-sided Student-t 95%, df=4 | equal-weight `p=.75/.85`; accepted/rejected initial-outcome strata or rejected-only intervention contrasts | PASS_WITH_BOUNDARY |
| E02 | one paired architecture effect per master seed | 5 | two-sided Student-t 95%, df=4 | rejected-initial-outcome stratum, equal-weight `p=.75/.85` | PASS_WITH_BOUNDARY |
| E03 | one exact-grid fraction per master seed | 5 | two-sided Student-t 95%, df=4 | all 357 frozen default-learner `p`-by-`eta` cells | PASS_WITH_BOUNDARY |
| E04 | one paired K-slope/contrast estimate per master seed | 5 | two-sided Student-t 95%, df=4 | 500 learners per canonical architecture/identity/good-count/K cell | PASS_WITH_BOUNDARY |
| E05 | one architecture-specific curve/effect per master seed | 5 | paired Student-t 95% for effects; 10,000-resample top-level master bootstrap for crossing | K=4, fixed good context 0; flat and hierarchical kept separate | PASS_WITH_BOUNDARY |

`PASS_WITH_BOUNDARY` means the published interval is genuinely built across
five master-level estimates, but five is still a small top-level sample and
does not quantify model-specification or human-population uncertainty. The
master IDs are frozen explicit constants, not a probability sample from a
documented master-seed generator.

## E01 — hot-stove and information restoration

- **Top-level unit:** a master-seed-specific effect computed from cell/stratum
  means. Code: `recompute_e01_summaries` and `_e01_effects` in
  `src/gifted_masking/experiments/article.py`.
- **Independent n and IDs:** 5;
  `2026081101, 2026081102, 2026081103, 2026081104, 2026081105`.
- **Seed derivation:** SHA-256 of a semantic cell ID, first four little-endian
  uint32 words, then
  `SeedSequence([master_seed,1,*words]).spawn(2)` for the policy/environment
  and intervention streams. Children are vectorized draws, not independent
  top-level replicates.
- **Pairing:** accepted and rejected rows are disjoint outcome strata within a
  master/cell, not paired children. Intervention conditions have different
  semantic cell IDs and streams; child IDs must not be paired across those
  cells. The two `p` effects are averaged with equal weight within master.
- **Interval:** mean of the five master-seed effects plus/minus
  `2.7764451051977987 * sd/sqrt(5)`.
- **Child-level variation:** it enters each master estimate through the
  cell/stratum mean and random stratum denominators; children are not supplied
  directly to the Student-t interval.
- **Article-facing population:** for direct rejection effects, the accepted
  versus rejected strata after the forced first authentic action at
  `p=.75/.85`. For restoration effects, rejected learners only. The maintained
  lambda contrast is an all-learner `p=.65` M0 contrast.
- **Mismatch:** artifact intervals are correct; older manuscript/source
  intervals are independent child bootstraps from different maintained runs.
  E01 did not show increased final-window masking after one rejection.

## E02 — binary versus graded disclosure

- **Top-level unit:** a within-master, within-`p`, within-stratum paired
  architecture effect, followed by equal weighting of `p=.75/.85`. Code:
  `_e02_effects` in `src/gifted_masking/experiments/e02.py`.
- **Independent n and IDs:** 5;
  `2026081201, 2026081202, 2026081203, 2026081204, 2026081205`.
- **Seed derivation:** SHA-256 of the semantic M0/M1 matched-pair ID, then
  `SeedSequence([master_seed,2,*words]).spawn(1)`.
- **Pairing:** valid within the same master seed and `p`. Binary and graded
  learners reinitialize the same policy/environment seed and share full latent
  uniforms and initial outcome by child ID. Pairing does not cross `p` or
  master seed.
- **Interval:** Student-t 95% across the five pooled master-seed effects.
- **Child-level variation:** it enters the paired stratum means. It is not the
  interval resampling unit.
- **Article-facing population:** rejected-initial-outcome learners at
  `p=.75/.85`, equal p weight. The `p=.65` control is not a decision input.

### Why the principal E02 interval is narrow

The narrow `0.253004–0.257077` interval is not a child-level confidence
interval. The five master estimates for
`graded_any_minus_binary_full_post_initial_rate` are:

```text
2026081201  0.2569712239
2026081202  0.2538080635
2026081203  0.2556477972
2026081204  0.2558530639
2026081205  0.2529218542
```

Their sample SD is `0.0016404515` and their SE is `0.0007336322`; applying the
df=4 critical value yields the stored interval. The stability is aided by the
frozen common-random-number architecture pairing and the large within-cell
population. This is a valid five-master Monte Carlo interval for this paired
design, not evidence of population-level precision. With only five top-level
units, tail behavior and model uncertainty remain weakly characterized.

## E03 — M2 regime replication

- **Top-level unit:** one master seed's fraction of the exact 357-cell grid
  classified `learned_suboptimal_masking`.
- **Independent n and IDs:** 5;
  `2026081301, 2026081302, 2026081303, 2026081304, 2026081305`.
- **Seed derivation:** SHA-256 of a semantic RNG family ID, then
  `SeedSequence([master_seed,3,*words]).spawn(1)`. Only approved T/window
  sentinel variants share trajectory-prefix families. The legacy
  `9100 + 100*eta_index + p_index` map is separate provenance and has no master
  seed.
- **Pairing:** exact-grid cells have semantic streams within each master. The
  inferential fraction is paired by the common grid definition across masters;
  cells are not independent inferential replicates. Approved T/window sentinel
  variants share a trajectory prefix by design.
- **Interval:** Student-t 95% across five exact-grid fractions. Each fraction is
  exactly `243/357`, so the stored interval collapses to the point estimate
  `0.6806722689`. This is stability across the selected streams, not zero
  scientific uncertainty.
- **Child-level variation:** used to determine state visit adequacy, learned
  neutral action, and cell classification; it does not directly enter the
  across-master interval after classification.
- **Population:** the specified 21-by-17 parameter grid under the frozen
  default learner. It is not a learner or human prevalence denominator.
- **Mismatch:** older sources and the current DOCX still report the legacy
  one-map `226/357`; Article V1 must use the adjudicated result only if it is
  needed as tested-grid provenance and not as a headline.

## E04 — context-search architectures

- **Top-level unit:** one master-specific K slope or endpoint/architecture
  contrast computed from 500-learner canonical cell means.
- **Independent n and IDs:** 5;
  `2026081401, 2026081402, 2026081403, 2026081404, 2026081405`.
- **Seed derivation:** policy/environment family ID to
  `SeedSequence([master,4,*words]).spawn(1)`; identity separately to
  `SeedSequence([master,40,*words]).spawn(1)`.
- **Pairing:** policy/environment streams are matched across identity and
  good-context-count cells within architecture/K/master; identity streams are
  separate. K/architecture contrasts are reduced inside master and the
  Student-t interval is across masters.
- **Interval:** two-sided Student-t 95%, df=4.
- **Child-level variation:** enters canonical cell proportions and within-master
  slopes; children are not the interval unit.
- **Population:** frozen baseline `p_good=.85`, `p_bad=.20`, `bf=0`, K through
  16, requested identity/good-count regimes. Staged p/tau sensitivity was not
  run.
- **Mismatch:** manuscript/source text uses older K=1/K=8, one-run bootstrap
  effects. These do not replace E04's K=1/K=16 five-master results.

## E05 — dense comparison-cost crossover

- **Top-level unit:** one master-specific 16-point dense response curve within
  one architecture. Endpoint effects are paired within master; the transition
  bootstrap resamples entire master curves.
- **Independent n and IDs:** 5;
  `2026081501, 2026081502, 2026081503, 2026081504, 2026081505`.
- **Seed derivation:** for each architecture/master family, SHA-256 the exact
  family ID and use `SeedSequence([master_seed,5,*words]).spawn(1)`. The same
  family seed is reinitialized at every `bf`, producing valid child/common-
  random-number pairing across `bf` within architecture. Architectures are not
  paired. The analysis bootstrap uses
  `SeedSequence([2026081597,50,architecture_code])`.
- **Interval:** paired Student-t 95% across five master effects for endpoint
  changes; architecture-isolated 10,000-resample master-curve bootstrap for the
  PAVA crossing.
- **Child-level variation:** enters each 500-learner response fraction. The
  bootstrap resamples masters, not children or `bf` rows.
- **Population:** K=4, fixed receptive context 0, flat 2K primary and
  hierarchical secondary, default learner, 18 `bf` values, T=2000.
- **Mismatch:** older two-endpoint prose is obsolete as the primary finding.
  The hierarchical response is left-censored at the dense range and has no
  estimable crossing.

## Cross-experiment boundary

All five experiments use independent, experiment-specific master lists and
different semantic seed namespaces. “Five master seeds” does not make their
effects exchangeable across experiments. Article V1 may compare qualitative
mechanisms only after outcome, population, aggregation, and sign have been
made explicit; it must not treat child counts or grid cells as additional
independent inferential replicates.
