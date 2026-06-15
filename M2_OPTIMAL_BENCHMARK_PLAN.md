# M2 Optimal-Policy Benchmark Plan

## Current Status

The maintained M2 implementation has transition-level tests and learned
final-window mask-rate checks, but no optimal MDP benchmark. There is no value
iteration, policy iteration, exact finite-state dynamic programming, or dynamic
regret estimate.

## Required Selected Cells

| Case | p | eta |
| ---- | -: | --: |
| low receptivity, low escape | 0.20 | 0.00 |
| intermediate receptivity, low escape | 0.55 | 0.00 |
| intermediate receptivity, high escape | 0.55 | 0.20 |
| high receptivity, low escape | 0.85 | 0.00 |
| high receptivity, high escape | 0.85 | 0.20 |

## Benchmark Design

Implement a separate module or script, not a change to `models/m2.py` semantics.
Recommended path:

```text
src/gifted_masking/benchmarks/m2_value_iteration.py
```

The benchmark should:

- enumerate states `neutral`, `accepted`, `stigmatized`;
- enumerate actions `mask`, `authentic`;
- encode the same reward and transition order as `transition_step`;
- compute an optimal discounted policy by value iteration for selected cells;
- report optimal neutral-state action;
- run the existing learner for the same cell;
- estimate final-window learned mask rate;
- estimate regret by comparing learned action values to optimal values under
  the same transition dynamics.

## Required Report Table

| p | eta | Optimal neutral-state action | Learned final mask rate | Estimated regret | Interpretation |
| -: | --: | ---------------------------- | ----------------------: | ---------------: | -------------- |
| 0.20 | 0.00 | TBD | TBD | TBD | TBD |
| 0.55 | 0.00 | TBD | TBD | TBD | TBD |
| 0.55 | 0.20 | TBD | TBD | TBD | TBD |
| 0.85 | 0.00 | TBD | TBD | TBD | TBD |
| 0.85 | 0.20 | TBD | TBD | TBD | TBD |

## Acceptance Criteria

- Benchmark has tests for transition probabilities summing to one.
- Benchmark uses the same reward defaults as `models/m2.py`.
- Benchmark output is written under `results/`.
- Claims about M2 suboptimality or optimal-learner traps are prohibited until
  this benchmark exists and shows positive regret under relevant cells.
