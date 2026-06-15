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
- The repo is not currently a git repository, so reproducibility metadata must
  tolerate missing commit hashes.

## Current Focus

1. Extend M2 optimal-policy benchmarking across learner-parameter and `p`/`eta`
   perturbation grids.
2. Add further M3 ablations for randomized and multiple good ponds.
3. Tighten the M4 path experiment into a stronger hysteresis claim test.
4. Improve reporting depth and comparison artifacts.

## Environment Policy

- Normal Python execution must use the repo-local `.venv`.
- System Python is only for bootstrapping `.venv` when it is absent.

## Next Verification Target

- `./scripts/verify.sh`

That command should:

- run unit and integration tests,
- execute the full robustness suite,
- write machine-readable artifacts into `results/`.

## Latest Verified Outcome

- `./scripts/verify.sh` passed in the repo-local `.venv`.
- Test count: `38` tests in discovery plus `4` explicit infrastructure tests
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
  - many coarse-grid cells show `learned_suboptimal_lock_in`
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
