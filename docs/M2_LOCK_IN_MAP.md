# M2 Lock-In Map

## Purpose

This document defines the maintained meanings of the current M2 map outputs.
The goal is to separate:

- static one-step M0 masking;
- dynamic M2 optimal-policy masking;
- learned masking that is suboptimal relative to the M2 optimum.

## Region Definitions

`optimal_learner_lock_in`

- static M0 neutral optimum is `authentic`;
- optimal M2 neutral action is `mask`.

This is the strong form of dynamic lock-in for an optimal decision-maker.

`learned_suboptimal_lock_in`

- optimal M2 neutral action is `authentic`;
- learned final-window neutral action is `mask`;
- neutral-state regret is positive.

This is a learner failure region, not an optimal-policy masking region.

`dynamic_authenticity_overrides_static_masking`

- static M0 neutral optimum is `mask`;
- optimal M2 neutral action is `authentic`.

This is the opposite of optimal lock-in: dynamic state value makes authenticity
worth taking even when the static bandit comparison still favors masking.

`masking_optimal_and_learned_not_proven_suboptimal`

- optimal M2 neutral action is `mask`;
- the current simulation does not establish a positive-regret mismatch against
  that masking optimum.

`authenticity_optimal_or_learned_matches`

- the current cell does not meet the stronger lock-in criteria above.

## Current Maintained Sweep

Artifact paths:

```text
results/summaries/m2_lock_in_region_map.csv
results/summaries/m2_lock_in_region_thresholds.csv
results/summaries/m2_regime_refined_thresholds.csv
results/summaries/m2_learner_parameter_sensitivity.csv
results/summaries/m2_optimal_regime_sensitivity.csv
results/figures/m2_lock_in_region_map.png
results/figures/m2_regime_thresholds.png
results/figures/m2_learner_sensitivity.png
```

Current deterministic grid:

- `p = 0.00` to `1.00` by `0.05`;
- `eta = 0.00` to `0.80` by `0.05`;
- `n=160`;
- `horizon=1000`;
- `alpha=0.1`;
- `tau=0.25`;
- `lambda=1.0`;
- `q0=0.0`;
- `gamma=0.9`.

## Current Outcome

On the maintained coarse grid:

- no cells are currently classified as `optimal_learner_lock_in`;
- many cells are classified as `learned_suboptimal_lock_in`;
- the learned neutral policy stays masking across the maintained coarse grid;
- the dynamic M2 neutrality threshold for authenticity appears well below the
  static M0 threshold.

For example:

- at `eta=0.00`, static M0 authenticity begins at `p=0.75`;
- at `eta=0.00`, optimal M2 neutrality authenticity begins at `p=0.40`;
- at `eta=0.20`, optimal M2 neutrality authenticity begins at `p=0.35`.

The refined threshold analysis estimates the default dynamic authenticity
threshold more precisely:

- `eta=0.00`: dynamic threshold `p ~= 0.3839`;
- `eta=0.20`: dynamic threshold `p ~= 0.3388`;
- `eta=0.80`: dynamic threshold `p ~= 0.2690`;
- static M0 authenticity threshold remains `p ~= 0.7167`.

## Sensitivity Outcome

The learner-parameter sensitivity grid confirms that default-like learners can
remain in learned suboptimal masking across cells where the M2 optimum is
authentic. Higher exploration and slower learning reduce masking in some
high-receptivity cells, but do not remove the failure mode across the selected
grid.

The optimal-regime sensitivity grid found a missing regime: true
`optimal_learner_lock_in` becomes possible under harsher environment/dynamic
settings, especially high stigmatized-authentic failure penalty `r2`, high
turnover `delta`, and low escape `eta`. The largest tested optimal-lock-in
width was about `0.056` in `p` units for `gamma=0.9`, `r2=8`, `delta=0.3`,
and `eta=0.0`.

## Claim Boundary

This map supports statements about the maintained default parameterization and
the explicit sweep grids only. It does not by itself establish publication-grade
threshold estimates, but it does show that learned suboptimal lock-in and true
optimal-policy masking are distinct regimes produced by different parts of the
parameter space.
