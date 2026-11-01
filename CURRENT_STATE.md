> Hosted verification is configured for macOS/Python 3.14.8 using the same full
> software verifier and exact dependency pins. It keeps generated results and
> raw verifier logs on the disposable runner, with no upload/cache/secret input.
> A hosted run remains unobserved until the workflow is published and executed.

> Software-only governance adoption: distribution 1.4.0/runtime 0.7.0 uses the
> published source baseline and retains every original verifier obligation.
> Unit output/source fixtures are isolated. Later local research history,
> scientific records and derived artifacts are outside this update; existing
> scientific execution, sealing and review gates remain unchanged.

# Current State

## Repository Status

- Legacy simulation scripts are preserved as reference artifacts.
- The maintained implementation lives in `src/gifted_masking`.
- The maintained package separates:
  - core numerics and validation,
  - per-model kernels for M0 through M4,
  - robustness experiments,
  - plotting utilities with lazy `matplotlib` imports,
  - reproducibility and manifest writing.
- The maintained implementation includes modular M3 ablation paths and an
  explicit M4 hysteresis-style path experiment.
- The maintained implementation includes an M2 optimal-policy benchmark module
  using value iteration against the current three-state MDP semantics.
- The maintained implementation includes a deterministic coarse M2 lock-in map
  over `(p, eta)` using the current learner defaults.
- The maintained implementation includes M2 regime sensitivity artifacts and
  figures for default thresholds, learner settings, and environment variants.
- The current workspace is a git repository. Older result manifests were generated
  in a copied non-git worktree and correctly record the commit as unavailable for
  those historical runs.
- A claim-audited Original Research manuscript for Frontiers in Psychology is in
  `doc-reviews/frontiers_submission/`, together with four submission figures, a
  manuscript-specific estimates table, and a completion checklist.
- The current assertive revision is
  `gifted_masking_frontiers_original_research_assertive_revision.docx`; it leads
  with the central outcomes and reserves qualifications for the later limitations
  section.
- A byte-matched, visually verified PDF export is available at
  `output/pdf/gifted_masking_frontiers_original_research_assertive_revision.pdf`.
- A dedicated article-development sub-project now lives in
  `projects/frontiers_article/`. Its RDS is the source of truth for manuscript
  scope, evidence gates, figures, and the nine-stage route to submission; model
  semantics remain governed at repository level.

## Current Focus

1. Correct the E06 packed-raw validator and canonical report/provenance seal.
   User-owned full verification passed, but the fresh independent smoke review
   returned `FIX_IMPLEMENTATION` after representative frozen row, seed-map,
   traversal, reset, and Q-continuity corruptions passed validation. E06
   standard and qualification execution remain refused.
2. Preserve the isolated E01 implementation and all baseline semantics while
   awaiting the smoke decision.
3. Extend M2 optimal-policy benchmarking across learner-parameter and `p`/`eta`
   perturbation grids.
4. Add further M3 ablations for randomized and multiple good ponds.
5. Tighten the M4 path experiment into a stronger hysteresis claim test.

## Environment Policy

- Normal Python execution must use `/Users/omer/workspace/venvs/venv314`.
- System Python is bootstrap-only if that workspace venv must be repaired.

## Next Verification Target

- `./scripts/verify.sh`

That command should:

- run unit and integration tests,
- execute the full robustness suite,
- write machine-readable artifacts into `results/`.

## Latest Verified Outcome

- `./scripts/verify.sh` passed using the shared workspace venv at
  `/Users/omer/workspace/venvs/venv314`.
- Test count: `47` tests in discovery plus `4` explicit infrastructure tests
  run after artifact generation.
- Result artifacts produced:
  - `results/manifests/robustness_full.json`
  - `results/raw/robustness_full.csv`
  - `results/raw/robustness_full_units.csv`
  - `results/summaries/robustness_full_summary.csv`
  - `results/summaries/robustness_full_recomputed_effects.csv`
  - `results/summaries/robustness_full_headline_uncertainty.csv`
  - `results/summaries/m2_optimal_policy_benchmark.csv`
  - `results/summaries/m2_lock_in_region_map.csv`
  - `results/summaries/m2_lock_in_region_thresholds.csv`
  - `results/summaries/m2_regime_refined_thresholds.csv`
  - `results/summaries/m2_learner_parameter_sensitivity.csv`
  - `results/summaries/m2_optimal_regime_sensitivity.csv`
  - `results/figures/m2_lock_in_region_map.png`
  - `results/figures/m2_regime_thresholds.png`
  - `results/figures/m2_learner_sensitivity.png`
  - `results/reports/robustness_full_report.md`
- Headline values now recompute exactly from primary unit rows with tolerance
  `1e-12`.
- Headline confidence intervals are generated from primary unit rows.
- Manifest validation now checks seed strategy, parameter grids, `n`, `T`,
  final-window fractions, and artifact paths.

## Current Outcome Summary

- The Frontiers manuscript now leads with its main finding: persistent learned
  masking occupies a large region in which authenticity is value-iteration optimal.
  Qualifications about translation to human populations follow in the later
  limitations section.
- Manuscript confidence intervals were recomputed with independent within-condition
  bootstraps; the original workflow's child-index matching was not treated as an
  experimental pairing.

- M0 smoke checks passed:
  - higher receptivity reduced masking by about `0.7332`
  - higher loss aversion increased masking by about `0.4031`
- M1 smoke check passed:
  - higher receptivity increased disclosure by about `0.5689`
- M2 smoke check passed:
  - higher stigma escape reduced masking by about `0.2007`
- M2 optimal-policy benchmark:
  - value iteration converges for selected target and robustness cells
  - learned final-window policies are compared against the M2 optimum for the
    current `p=0.55`, `eta=0.0/0.2` robustness cells
  - target cells absent from the primary raw artifact are reported as missing
    empirical-policy regret rather than imputed
- M2 coarse lock-in map:
  - current coarse grid shows no `optimal_learner_lock_in` cells
  - `226/357` coarse-grid cells (`63.3%`) show `learned_suboptimal_lock_in`
  - mean learned neutral-state masking probability across those cells is about
    `0.950`
  - on the current grid, learned neutral behavior remains masking even where
    the M2 optimum has already switched to authenticity
- M2 regime sensitivity:
  - default refined thresholds show dynamic M2 authenticity becomes optimal
    well before static M0 authenticity
  - learner-parameter sensitivity confirms learned masking is the dominant
    default failure mode
  - environment sensitivity finds true `optimal_learner_lock_in` under harsher
    stigmatized-failure and turnover settings
- M3 smoke and ablation summary:
  - flat `2K` formulation showed a `K=1` vs `K=8` settling gap of about `0.1682`
  - hierarchical formulation showed a larger settling gap of about `0.3773`
  - global-mask and fixed-known-good-pond formulations showed near-zero gap
  - current interpretation: search burden appears materially stronger in the
    flat and hierarchical formulations than in controls that remove or compress
    the search burden
- M4 path experiment summary:
  - descending-`km` and ascending-`km` paths differ
  - mean mask-path gap is about `0.0651`
  - mean receptivity-path gap is about `-0.1061`
  - current interpretation: the code shows path dependence under this ramp
    experiment, but this should still be treated as a hysteresis-style signal,
    not a final strong hysteresis claim

## Current Blocker Status

- Raw artifact blocker: improved. Primary units are now stored in
  `results/raw/robustness_full_units.csv`; the old `robustness_full.csv` remains
  as a compatibility summary artifact.
- Manifest blocker: improved. The manifest now records seed strategy, RNG
  strategy, parameter grids, `n`, `T`, final-window fractions, and artifact
  paths.
- M2 optimal benchmark: present for selected cells; broader learner-parameter
  and dense perturbation sweeps remain absent.
- M2 lock-in map: present for a coarse default-learner grid; threshold-local
  refinement and learner-parameter perturbation are still absent.
- M4 hysteresis: still path dependence only; ramp-speed, loop-area, threshold,
  and seed-replication diagnostics remain absent.
- M3 variants: random-good-pond and multiple-good-pond variants remain absent.

## E02 Smoke Checkpoint

- The approved E02 binary-versus-independent-graded disclosure smoke is
  implemented as isolated article-experiment infrastructure. It preserves M0
  and M1 baseline behavior when the experiment-only first-step override is
  disabled, and standard execution is explicitly refused without a future
  E02-specific approval.
- The smoke checkpoint is diagnostic only. It produces 576 raw rows, 15 arm
  benchmarks, 18 cell/stratum summaries, 192 effects, a figure, report, and
  manifest. It has not changed the E01 disposition, article claim ledger, or
  manuscript.
- The corrective smoke-gate batch now enforces exact nested JSON types/values,
  records content-inclusive provenance, and uses a linear stable-policy suffix
  diagnostic. Its regenerated raw, summaries, and figure byte-match the
  original smoke scientific outputs. The separately approved E02 standard
  execution produced its five-seed 15,000-row package and passed deterministic
  regeneration, reconciliation, and repository verification; claim
  adjudication remains a separate next gate.

## E04 Smoke Checkpoint

- An isolated E04 M3 architecture/identity/multiple-good diagnostic kernel now
  exists without modifying maintained M3 or robustness code. The frozen smoke
  emitted 5,280 primary rows, 55 canonical cells, and a 120-row equivalence
  table; standard execution remains explicitly refused.
- Fixed-identity replay against each maintained architecture, raw
  reconciliation, deterministic regeneration, and targeted regression tests
  passed. No E04 claim has been adjudicated; await separate smoke review.

### E04 Smoke Gate Corrective Batch

- Comparator action sets now follow each child's good-context set and the
  architecture action space; equivalence metadata has exactly 55 compatible
  canonical requested rows among 120 aliases; input/artifact validation fails
  closed on schema, type, seed, and cardinality drift.
- Regenerated smoke remains diagnostic only. It measured approximately 133 MiB
  peak RSS and projects a baseline-only standard below the configured resource
  caps; this is not authority to execute it.

### E04 Final Release Correction

- Raw, curve, and effect artifacts now fail closed against recomputed frozen
  semantic fields. Same-/cross-directory normalized regeneration and strict
  streaming order checks passed with E01-E04 targeted and full verification.
- Standard execution remains refused pending separate smoke review.

### Final Reviewer Hardening

- E04 now rejects frozen-payoff/learner, settled/discovery, undefined payload,
  upstream-provenance, and streaming seed/mask corruption. The final smoke
  regeneration refreshes provenance after this documentation update; standard
  remains refused.

### E04 final smoke-review preparation

- The materialized and incremental-streaming paths now invoke the same frozen
  per-row semantic validator. It rejects corrupt `bf`, good fraction, child/RNG
  declarations, action/count/modal fields, good-set JSON, regret, and coupled
  discovery/censoring, alongside the previously hardened semantic surface.
- The smoke report now lists actual effort, dirty-state provenance, implemented
  files and artifact paths, and recommends only
  `RECOMMEND_GO_STANDARD_REVIEW`. No standard/sensitivity execution or E04
  claim, ledger, or manuscript work is authorized.

### E04 smoke performance/readiness correction

- Workspace-venv profiling located repeated validator identity regeneration,
  not a learner semantic/RNG operation, as the avoidable hot path. Cached
  immutable identity assignments make the smoke about 2.57s; pre/post raw,
  canonical, equivalence, curve, effect, and figure hashes match exactly.
- The runner now fails its readiness gate above a 10-minute linear standard
  projection. This smoke projects about 7.45 minutes, 186.5 MiB raw, and a
  442.5 MiB conservative peak; it remains an execution-free estimate.
- `ever_accepted_good_auth` is exactly tied to positive accepted-good count in
  raw and streaming validation, with adversarial tests for both directions.

### E04 authorized baseline standard checkpoint

- The GO-authorized frozen baseline completed 137,500 raw units, 275 curves,
  1,182 effects, 55 canonical cells, and 120 aliases; raw storage is
  174,838,110 bytes (~166.7 MiB), with 128.724s through the completed figure.
- External supervision interrupted the original process after figure creation
  and before manifest serialization. Bounded recovery revalidated/finalized it;
  51.4 MiB is recovery-process RSS, not reconstructed execution peak. Per-cell
  <600s/<400MiB/<2GiB stop checks were enforced.
- Independent replay byte-matched raw, canonical, equivalence, curves, effects,
  and figure after deterministic seed-order pooling. Stop at
  `PENDING_SOL_STANDARD_REVIEW`; do not adjudicate claims or run sensitivity,
  publication, ledger, or manuscript work.
