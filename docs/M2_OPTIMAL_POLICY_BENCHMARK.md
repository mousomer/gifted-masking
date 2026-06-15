# M2 Optimal-Policy Benchmark

## Current Implementation Audit

| Area | Maintained behavior | Benchmark handling |
| ---- | ------------------- | ------------------ |
| States | `neutral=0`, `accepted=1`, `stigmatized=2` | Value iteration uses the same three states in that order. |
| Actions | `mask=0`, `authentic=1` | Optimal and empirical policies are reported with these two actions. |
| Neutral masking | Reward `b-c`; next state remains neutral | Transition table has deterministic neutral self-loop. |
| Neutral authenticity | Accepts with probability `p`, reward `b+a`, next accepted; rejects with probability `1-p`, reward `a-r`, next stigmatized | Transition table mirrors both branches. |
| Accepted state | Mask reward `b-c`; authentic reward `b+a`; turnover `delta` can reset to neutral after reward | Transition table applies `delta` to both accepted-state actions after current reward. |
| Stigmatized masking | Reward `b2-c`; escape `eta` can reset to neutral after reward | Transition table applies `eta` after the stigmatized masking reward. |
| Stigmatized authenticity | Redemption succeeds with probability `p/2`, reward `b+a`, next accepted; failure reward `a-r2`; failed stigmatized rows can escape with `eta` | Transition table does not escape successful redemption to accepted, matching current code. |
| Learning target | Q-learning uses subjective reward plus `gamma * max Q(next_state)` | Benchmark solves the environment optimum directly; subjective mode is available for reward-transformed comparisons. |

## Transition Ordering

The maintained ordering is reward first, then turnover or escape changes the
next state. `delta` applies to accepted-state rows after reward. `eta` applies
to stigmatized rows after reward, but only to outcomes whose next state is still
stigmatized.

## Value Iteration

`gifted_masking.analysis.m2_optimal.solve_m2_value_iteration` solves the exact
discounted MDP for selected parameter cells. The default reward mode is
objective payoff. Subjective mode applies the loss-aversion transform to
realized rewards before expectation and is available for diagnostics, but the
current benchmark artifact uses objective reward.

Tie handling records all optimal actions within tolerance and also records a
deterministic chosen action for downstream CSV stability.

## Empirical Policy Evaluation

The benchmark reads state-conditional final-window action counts from
`results/raw/robustness_full_units.csv` where available. The current robustness
suite provides empirical M2 policies for the `higher_escape_rate_reduces_masking`
cells at `p=0.55`, `eta=0.0` and `eta=0.2`.

For selected target cells that are not present in the primary raw artifact, the
benchmark still reports static M0 and optimal M2 values but marks empirical
policy regret unavailable.

## Output

The machine-readable output is:

```text
results/summaries/m2_optimal_policy_benchmark.csv
results/summaries/m2_lock_in_region_map.csv
results/summaries/m2_lock_in_region_thresholds.csv
results/summaries/m2_regime_refined_thresholds.csv
results/summaries/m2_learner_parameter_sensitivity.csv
results/summaries/m2_optimal_regime_sensitivity.csv
```

Required interpretation values are limited to:

```text
learned_matches_m2_optimal
learned_suboptimal_vs_m2
stigma_changes_static_optimum
inconclusive_due_to_tie
inconclusive_due_to_missing_empirical_policy
```

## Claim Boundary

This benchmark permits M2 learned-policy comparisons against an optimal MDP
policy for cells with empirical state-conditional counts. It does not by itself
establish publication-grade robustness across learner parameters, seed
replication, or dense `p`/`eta` perturbation grids.

## Current Map Outcome

The maintained coarse sweep currently uses:

- `p = 0.00` to `1.00` in steps of `0.05`;
- `eta = 0.00` to `0.80` in steps of `0.05`;
- learner simulation `n=160`, `horizon=1000`, `alpha=0.1`, `tau=0.25`,
  `lambda=1.0`, `q0=0.0`, `gamma=0.9`.

Current result under those settings:

- no coarse-grid cells show `optimal_learner_lock_in`;
- many cells show `learned_suboptimal_lock_in`;
- dynamic M2 authenticity becomes optimal well before the static M0
  authenticity threshold.

Additional sensitivity analysis found that `optimal_learner_lock_in` can appear
outside the default environment grid, especially when stigmatized authenticity
failure is harsher, accepted-state turnover is higher, and stigma escape is
low. This means the default model mainly shows learned suboptimal masking,
while harsher M2 variants can create true dynamic optimal-policy masking.

This is evidence about the maintained defaults and current grid only. It is not
yet a claim about all nearby perturbations.
