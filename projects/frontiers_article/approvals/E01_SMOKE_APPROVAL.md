# E01 Scientific Approval Record

**Decision:** `APPROVED_FOR_SMOKE`  
**Date:** 2026-08-12  
**Scientific owner:** `gpt-5.6-sol`, `xhigh`  
**Scope:** bounded implementation and smoke execution only

No scientific blocker remains after the corrected Stage 2 baseline gate. This
record freezes the E01 implementation contract. It does not authorize a
standard or publication-tier run and does not authorize claim adjudication.

## Baseline audit

- M0 implements mask reward `b-c=0.75`, authentic rewards `b+a=1.6` and
  `a-r=-1.4`, with authenticity objectively optimal at `p=.75` and `.85`.
- `lambda` changes the learning signal only; maintained softmax is stable.
- Maintained RNG order is policy draw, acceptance draw for every learner,
  reward, then Q update. E01 must preserve that order.
- Do not modify `m0.py`, maintained defaults, or the existing robustness suite.
- Commit at approval: `e0e9a738986dd440180a228b024b0807336cd957` in a dirty
  Stage 1 worktree. The corrected workspace-venv gate passed 47 discovered
  tests, artifact generation/validation, and 4 post-generation tests.

## Frozen smoke configuration

- Config: `configs/frontiers_article/e01_hot_stove_smoke.json`
- Run ID: `frontiers_hot_stove_v1_smoke`
- Model/payoffs: M0; `b=1`, `a=.6`, `c=.25`, `r=2`
- Learner: `alpha=.1`, `tau=.25`, `q0=0`
- `n=96` per cell; `T=300`; final fraction `.20`; window steps 240-299
- Smoke master seed: `2026081199`
- Bootstrap seed: `2026081201`, recorded but unused for smoke inference
- Standard seeds reserved and not executable in this pass:
  `2026081101` through `2026081105`
- Workers: exactly 1
- Sort: canonical lexicographic cell order, master seed, child ID

Execute exactly ten cells:

1. At `p=.75`, `lambda=1`: `controlled_baseline`,
   `forced_authentic_0.05`, `counterfactual_authentic_feedback`.
2. At `p=.85`, `lambda=1`: the same three conditions.
3. At `p=.75`, controlled baseline: `lambda=.5` and `2.5` semantic
   sentinels.
4. At `p=.65`, `maintained_baseline` with no forced initial action:
   `lambda=.5` and `2.5` C3 replication-path sentinels.

Smoke output is diagnostic only and must not adjudicate C1-C3.

## Frozen experiment semantics

At every step, including step 0:

1. sample maintained softmax policy action;
2. draw latent acceptance for every learner from the main cell RNG;
3. apply any experiment-only action override;
4. calculate actual objective reward;
5. apply `subjective_value` only to the learning update;
6. update Q-values;
7. accumulate diagnostics.

For controlled cells, discard the sampled step-0 action and force
authenticity. The unused policy draw and acceptance draw are retained to
preserve maintained RNG consumption. Initial outcome is the step-0 acceptance.

From step 1:

- `controlled_baseline`: sampled action unchanged.
- `forced_authentic_0.05`: use a separate intervention RNG and independent
  learner-step exposure flags. Override only sampled masking to authenticity;
  record exposure flags and actual overrides.
- `counterfactual_authentic_feedback`: do not change actual action or payoff.
  On masked trials update `Q_mask` from actual mask reward and update `Q_auth`
  once from the unreceived authentic reward implied by the already-drawn
  acceptance. Apply `lambda` to the counterfactual learning signal and never
  add it to environment return.
- No v1 condition combines forced exploration and counterfactual feedback.
- `maintained_baseline` has no step-0 override or intervention and must exactly
  match `m0.simulate` for the same seed, parameters, horizon, and window.

Primary regret is objective pseudo-regret: the sum over time of the analytic
optimal expected reward minus the expected reward of the chosen action.
Normalized regret divides by `T * abs(E_auth-E_mask)` and is therefore the
fraction of objectively suboptimal actions in these non-tie cells. Store
realized objective payoff separately.

## Seed hierarchy

Use canonical semantic cell IDs, never input positions:

1. SHA-256 the canonical cell ID.
2. Read the first 16 digest bytes as four little-endian uint32 words.
3. Construct `SeedSequence([master_seed, 1, word0, word1, word2, word3])`.
4. Spawn exactly two sequences: component 0 policy/environment, component 1
   forced-exploration intervention.
5. Convert each to one uint64 with `generate_state`; record both.
6. Initialize the maintained-style generator with the recorded
   policy/environment integer.

Children remain vectorized draws from the maintained cell stream. Record child
ID, leave `child_seed` blank, and set `rng_unit=vectorized_cell_stream`.

## Ordered primary-row schema

```text
run_id,experiment_id,tier,model,condition,intervention,
master_seed,parameter_cell_id,cell_seed,
policy_environment_seed,intervention_seed,
child_id,child_seed,rng_unit,
p,b,a,c,r,alpha,tau,lambda,q0,n,T,
final_window_fraction,final_window_start,final_window_end,
expected_mask_reward,expected_auth_reward,objective_reward_gap,
analytic_optimal_action,
initial_action_forced,initial_policy_action,
initial_accepted,initial_outcome,
initial_objective_reward,initial_subjective_value,
early_post_initial_steps_observed,
time_to_next_authentic_action,time_to_next_authentic_censored,
authentic_count_steps_1_100,
authentic_count_post_initial,authentic_rate_post_initial,
authentic_accept_count_post_initial,authentic_reject_count_post_initial,
final_window_mask_count,final_window_mask_rate,
cumulative_realized_objective_payoff,
cumulative_objective_pseudo_regret,normalized_objective_pseudo_regret,
q_mask_final,q_auth_final,
forced_exposure_count,forced_override_count,
counterfactual_feedback_count,
counterfactual_auth_accept_count,counterfactual_auth_reject_count,
counterfactual_auth_reward_sum,counterfactual_auth_subjective_value_sum
```

`time_to_next_authentic_action` is the first `t>=1`, blank if censored.
Steps 1-100 are inclusive and use `min(100,T-1)` as the recorded denominator.
Controlled initial strata are `accepted` or `rejected`; ordinary maintained
baseline rows use `not_applicable` when step 0 masks. Counterfactual aggregates
cover masked trials only.

## Summary and inference contract

Cells output one row per master seed, cell, and stratum: `all`, `accepted`, and
`rejected` for controlled cells; `all` only for maintained-baseline C3 cells.
Include denominators and means for post-initial authentic rate, final masking,
realized payoff, normalized regret, Q-values, intervention exposures, and
counterfactual aggregates.

Effects output seed-level and across-seed rows for:

- rejected minus accepted final mask rate;
- rejected minus accepted post-initial authentic rate;
- rejected minus accepted normalized regret;
- baseline minus intervention final masking after rejection;
- baseline minus intervention normalized regret after rejection;
- intervention minus baseline authentic sampling after rejection;
- maintained `p=.65` `lambda=2.5` minus `.5` final mask rate;
- controlled early-rejection gap-in-gap for high versus low lambda.

Pool `p=.75` and `.85` by equal weighting of p-specific effects, never by
pooling children. Do not pair administrative child IDs between cells. Standard
five-seed intervals will use `t(.975,4)=2.7764451051977987`. With one smoke
seed, leave interval fields blank and set
`ci_status=not_estimable_lt_2_master_seeds`.

Decision rules are those in `STAGE2_EXPERIMENT_SPECIFICATIONS.md` plus the
scientific review: both p cells and 4/5 seed directionality for direct support;
one same intervention reducing both masking and normalized regret for
information restoration; at least 10% relative materiality; positive
high-minus-low lambda gap-in-gap for H3; and positive maintained-M0 C3
replication. These rules are frozen for later standard adjudication and must
not be applied to smoke.

## Tests required before smoke

1. No-intervention maintained trace exactly equals `m0.simulate`.
2. Existing M0 and robustness outputs do not change.
3. Forced step 0 is authentic with exact M0 rewards.
4. Forced exploration only changes masking to authenticity.
5. Counterfactual feedback changes information, never actual return.
6. Actual/counterfactual reward sums reconcile from event counts.
7. Normalized deterministic reruns byte-match machine-readable artifacts.
8. Cell reordering preserves seeds, rows, and values.
9. Global NumPy RNG state is unused.
10. Raw-to-cell/effect recomputation matches within `1e-12`.
11. Exact and non-integer final windows use `ceil(T*fraction)`.
12. Pseudo-regret matches analytic cases at `p=.65,.75,.85`.
13. Config validation rejects missing/unknown modes, invalid probabilities,
    invalid learner values, nonpositive `n/T`, and non-auth-optimal primary
    cells.
14. Both controlled initial strata exist.
15. Manifest validation covers config/hash, seed derivations, dirty diff hash,
    timestamps, verification, warnings, output hashes, and paths.
16. E01 v1 rejects worker counts other than 1.
17. Full `./scripts/verify.sh` passes.

## Manual smoke sentinels

Inspect the lowest child ID in each controlled baseline accepted/rejected
stratum at both p values; a forced-exploration row with an override; a
counterfactual row with masked trials; and both maintained p=.65 lambda rows.
Confirm exact initial rewards, mask reward `.75`, counterfactual count versus
masked trials, exclusion of counterfactual reward from return, plausible
exposure/acceptance frequencies, both strata, and stable sorted rows/seeds.

## Required smoke artifacts and cost guardrail

```text
results/manifests/frontiers_hot_stove_v1_smoke.json
results/raw/frontiers_hot_stove_v1_smoke_units.csv
results/summaries/frontiers_hot_stove_v1_smoke_cells.csv
results/summaries/frontiers_hot_stove_v1_smoke_effects.csv
results/figures/frontiers_hot_stove_v1_smoke_stratum_diagnostics.png
results/reports/frontiers_hot_stove_v1_smoke_report.md
```

The report must contain all 13 smoke-checkpoint items and state that no claim
was adjudicated. The manifest records normalized config/hash, commit and dirty
diff hash, command, environment, seed map/RNG order, timing, warnings,
verification status, sort keys, and artifact hashes/sizes; it excludes itself
from its output-hash list.

Expected experiment runtime is under 2 seconds, about 960 raw rows, and under
1 MB. More than 10 seconds excluding repository verification, raw output above
5 MB, or unexpected memory growth requires cost review. Stop after the smoke
checkpoint.
