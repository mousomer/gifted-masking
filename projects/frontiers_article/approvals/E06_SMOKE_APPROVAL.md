# E06 Scientific Approval Record

**Decision:** `APPROVED_FOR_SMOKE`  
**Date:** 2026-08-13  
**Scope:** bounded E06 implementation and diagnostic smoke only  
**Claims:** C8 endogenous feedback/path dependence; C9 hysteresis remains excluded

## 1. Scientific question

E06 asks whether the ascending/descending M4 path separation already observed
under one continuation schedule is reproducible across independent master
seeds, ramp speeds, initial conditions, and feedback structures; whether it
exceeds separation produced by stochastic schedule order without inherited
state; and whether transition separation survives a longer-horizon test well
enough to justify reconsidering hysteresis.

The default interpretation remains **schedule-specific path dependence**.
E06 does not begin from an assumption that hysteresis exists. Null, shrinking,
censored, direction-reversing, or control-equivalent loops are valid results.

This record authorizes implementation and the exact diagnostic smoke only. It
does not authorize the staged core standard, the separately staged hysteresis-
qualification extension, C8/C9 adjudication, claim-ledger changes, article
edits, figure replacement, or publication-tier work.

## 2. Maintained M4 semantics that must not change

E06 must replay `src/gifted_masking/models/m4.py` exactly:

1. The learner has two Q-values, masking and authenticity. Q-values do not
   condition on current receptivity, so M4 is an endogenous/nonstationary
   bandit, not ordinary stateful Q-learning.
2. At each step, action selection uses the maintained numerically stable
   softmax with temperature `tau`.
3. One acceptance uniform is consumed for every learner and step, including
   masking trials, preserving maintained RNG order.
4. Reward is calculated from the pre-update `p_t`:

   ```text
   mask                  = b-c
   accepted authenticity = b+a
   rejected authenticity = a-r
   ```

5. The selected Q-value is updated from the subjective reward, with loss
   aversion applied only to negative realized rewards.
6. Receptivity is updated **after reward and Q update**:

   ```text
   accepted authenticity: p += ka*(p_max-p)
   rejected authenticity: p -= kr*(p-p_min)
   masking:                p -= km*(p-p_min)
   ```

7. Receptivity is clipped to `[p_min,p_max]` after every update.
8. Inherited ramps continue both the complete per-child Q-vector and `p_t`
   between segments. Reset controls reset both quantities.

Maintained M4 code, defaults, and legacy robustness artifacts must not be
modified. Implement E06 in an isolated config-driven experiment kernel with
exact replay tests against `simulate_from_state`.

## 3. Frozen baseline parameters

```text
b=1.0, a=0.6, c=0.25, r=2.0
alpha=0.1, tau=0.25, lambda=1.0, q0=0.0
p_min=0.05, p_max=0.95
p0=0.45
ka=0.12, kr=0.04
final_window_fraction=0.20
workers=1
```

The nominal ramp contains exactly 11 increasing binary64 values:

```text
[0.0, 0.0004, 0.0008, 0.0012, 0.0016, 0.0020,
 0.0024, 0.0028, 0.0032, 0.0036, 0.0040]
```

Canonical `km_label` values are four-decimal strings (`0.0000`, `0.0004`,
..., `0.0040`). Smoke labels use the same rule (`0.0000`, `0.0010`, ...,
`0.0040`). Numeric sorting controls traversal; labels are never sorted
lexically to define a path.

The inherited ascending path evaluates all 11 values in that order. The
descending path immediately continues from the final ascending state and
evaluates the same 11 values in reverse order, including the repeated `.004`
turning point. Do not drop either endpoint. Analysis aligns descending values
back into increasing numeric `km` order.

## 4. Experimental path types

### 4.1 Inherited loop — primary evidence

- Initialize every child once at `Q=[q0,q0]` and `p=p0`.
- Run the complete ascending ramp, continuing both Q and p.
- Continue directly through the complete descending ramp.
- Record start state, counts, final-window outcomes, and end state for every
  segment.
- This is the only path type that can supply positive path-dependence or
  hysteresis evidence.

### 4.2 Reversal-only reset control — stochastic schedule control

- Use the same ascending and descending schedule positions and the exact same
  segment-specific policy/environment seeds as the inherited loop.
- Reset every child to `Q=[q0,q0]` and `p=p0` before every segment.
- Consequently it inherits RNG schedule/order but no behavioral or
  environmental state.
- Its aligned descending-minus-ascending separation estimates ordinary
  directional-stream/schedule noise. It cannot support path dependence.

### 4.3 Cold-start curve — state-free comparator

- At every numeric `km`, initialize independently from the same declared
  `Q=[q0,q0],p=p0` state.
- Use a direction-free, `km`-specific RNG family distinct from inherited and
  reversal families.
- This produces one cold-start response curve, not an artificial up/down loop.
- It is the primary comparator for the direct `.004-minus-0` feedback effect.

### 4.4 Disabled-masking-feedback schedule placebo

- Traverse the nominal up/down schedule and record nominal `km`, but pass
  `actual_km=0` at every segment.
- Run inherited and reversal-only versions with default `ka` and `kr`.
- This tests path separation caused by continuation/time order when the ramped
  control parameter has no effect on receptivity.
- It may never be combined with the active-`km` curve as if it were another
  numeric ramp.

These controls are analytically distinct. Do not label cold-start and reversal-
only rows interchangeably.

## 5. RNG and pairing contract

Master seeds are the independent inferential units. Children are paired only
within a declared master-seed/scenario/path family and never across master
seeds or sensitivity scenarios.

Use the exact article seed derivation. The semantic segment ID is:

```text
E06|master=<seed>|scenario=<scenario_id>|direction=<up|down|cold>
|position=<0-based position>|km=<canonical label>|policy_environment
```

Take the first 16 bytes of `SHA-256(segment_id)` as four little-endian uint32
words and derive:

```text
SeedSequence([master_seed,6,*words]).spawn(1)[0]
  .generate_state(1,dtype=uint64)[0]
```

The resulting uint64 is the vectorized policy/environment seed for that
semantic segment. Rebuild a fresh RNG from that seed at segment entry. The
inherited and reversal-only
versions of the same semantic up/down segment must reuse that exact seed. They
therefore share policy and acceptance uniforms while differing only in their
starting state. Cold-start seeds use `direction=cold` and are separate.

Do not seed segments with arithmetic such as `seed+offset`. Do not use global
NumPy random state. Record all derivations and seeds. Execution order must not
change rows or summaries. Bootstrap RNG is analysis-only, architecture-
isolated by scenario/outcome, and must not affect simulation artifacts. For a
bootstrap ID
`E06|bootstrap|scenario=<id>|response=<mask|p>|target=<none|0.5|0.75>`, use
the same four-word hash rule with
`SeedSequence([bootstrap_seed,60,*words])`; never reuse a policy/environment
stream.

## 6. Exact diagnostic smoke

Pass B must add:

- `configs/frontiers_article/e06_m4_paths_smoke.json`;
- `configs/frontiers_article/e06_m4_paths_standard.json`;
- `configs/frontiers_article/e06_m4_hysteresis_qualification.json`.

Only the smoke config is executable under this record.

The smoke is frozen as:

```text
run_id=frontiers_m4_path_diagnostics_v1_smoke
tier=smoke
n=64
segment_horizon=120
final_window_fraction=.20
master_seed=2026081699
bootstrap_seed=2026081697
bootstrap_replicates=0
km=[0,.001,.002,.003,.004]
scenario=baseline only: p0=.45, ka=.12, kr=.04, tau=.25, lambda=1
path types=inherited_loop,reversal_only,cold_start,km_disabled_loop
workers=1
```

The final window is steps 96--119 inclusive. The active inherited and reversal
paths contain ten segments each; cold start contains five; disabled-feedback
inherited and reversal paths contain ten each. With packed path-family primary
rows, the smoke contains exactly `5 path families x 64 = 320` primary rows and
`345,600` learner-steps:

```text
active inherited       10*64*120 =   76,800
active reversal        10*64*120 =   76,800
active cold             5*64*120 =   38,400
disabled inherited     10*64*120 =   76,800
disabled reversal      10*64*120 =   76,800
total                                    345,600
```

Smoke transitions, intervals, and C8/C9 decisions are unavailable. Smoke may
exercise PAVA and loop estimators diagnostically but must mark every such row
`decision_eligible=false`.

## 7. Staged core standard — not authorized

The staged core standard is:

```text
run_id=frontiers_m4_path_diagnostics_v1
n=400
master_seeds=2026081601,2026081602,2026081603,2026081604,2026081605
bootstrap_seed=2026081697
bootstrap_replicates=10000
km=11-point frozen ramp
workers=1
approved_standard=false
```

It contains the following exact scenarios:

| ID | Role | p0 | ka | kr | tau | lambda | Horizon | Path types |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| S00 | primary fast | .45 | .12 | .04 | .25 | 1.0 | 500 | inherited, reversal, cold |
| S01 | primary slow | .45 | .12 | .04 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S02 | low p0 | .10 | .12 | .04 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S03 | high p0 | .90 | .12 | .04 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S04 | ka less than kr | .45 | .04 | .12 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S05 | ka equals kr | .45 | .08 | .08 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S06 | no acceptance gain | .45 | 0 | .04 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S07 | no rejection loss | .45 | .12 | 0 | .25 | 1.0 | 1000 | inherited, reversal, cold |
| S08 | km disabled placebo | .45 | .12 | .04 | .25 | 1.0 | 1000 | inherited, reversal |

`S01` supplies the maintained `ka>kr` feedback-balance case. In `S08`, nominal
`km` follows the ramp but `actual_km=0` for every segment. All other scenarios
use `actual_km=nominal_km`.

There are 26 scenario/path families per master seed and exactly 52,000 packed
primary rows. The exact learner-step count is `913,000,000`. These numbers must
be recomputed independently from the config. A future smoke review may
authorize only this unchanged package through `E06_STANDARD_GO.md`.

## 8. Staged hysteresis qualification — separately gated

The qualification config is not part of the core standard and remains
non-executable even if the core standard receives GO. It may receive a separate
`E06_HYSTERESIS_QUALIFICATION_GO.md` only if core adjudication finds C9 eligible
for reconsideration under Section 13.

| ID | Role | p0 | ka | kr | tau | lambda | Horizon | Path types |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Q00 | long-horizon sentinel | .45 | .12 | .04 | .25 | 1.0 | 2000 | inherited, reversal, cold |
| Q01 | low loss weighting | .45 | .12 | .04 | .25 | .5 | 1000 | inherited, reversal, cold |
| Q02 | high loss weighting | .45 | .12 | .04 | .25 | 2.5 | 1000 | inherited, reversal, cold |
| Q03 | low temperature | .45 | .12 | .04 | .10 | 1.0 | 1000 | inherited, reversal, cold |
| Q04 | high temperature | .45 | .12 | .04 | .60 | 1.0 | 1000 | inherited, reversal, cold |

It uses the same `n=400`, five master seeds, ramp, seed rules, and bootstrap
rules. It contains 15 path families per master seed, 30,000 packed primary
rows, and exactly `660,000,000` learner-steps. Q01--Q04 map robustness but do
not rescue a failed primary C9 gate. Q00 supplies the required long-horizon
test. No other long-horizon or parameter cells may be added without a revised
scientific record.

## 9. Ordered packed primary schema

Write one row per child, master seed, scenario, and path family. Array fields
are compact JSON in aligned increasing numeric `km` order unless explicitly
named as traversal order. The exact ordered schema is:

```text
run_id,experiment_id,tier,model,component,scenario_id,scenario_role,
path_type,master_seed,matched_family_id,policy_environment_seed_map_json,
child_id,child_seed,rng_unit,n,segment_horizon,total_segments,
final_window_fraction,final_window_start,final_window_end,
p0,p_min,p_max,ka,kr,km_mode,nominal_km_values_json,actual_km_values_json,
b,a,c,r,alpha,tau,lambda,q0,
traversal_direction_json,traversal_nominal_km_json,traversal_actual_km_json,
mask_rate_json,mask_count_json,auth_count_json,auth_accept_count_json,
auth_reject_count_json,mean_objective_reward_json,
p_start_json,p_end_json,q_mask_start_json,q_auth_start_json,
q_mask_end_json,q_auth_end_json,bounds_violation_count_json,
final_p,final_q_mask,final_q_auth
```

For inherited/reversal/disabled loops, traversal arrays have 22 entries under
the standard grid. For cold start they have 11. Smoke lengths are 10 and five.
Reversal and cold rows must show `p_start=p0` and both Q starts equal `q0` for
every segment. Inherited state continuity must hold exactly from one segment's
end state to the next segment's start state per child. Every count must sum to
the segment horizon and every rate must reconstruct from counts.

`child_seed` is the literal `vectorized_segment_streams`; child IDs are paired
only because every child index receives the same segment RNG vector inside its
recorded matched family. Do not invent independent per-child RNG seeds.

## 10. Derived artifacts

Every tier produces:

```text
results/raw/<run_id>_units.csv
results/summaries/<run_id>_cells.csv
results/summaries/<run_id>_paths.csv
results/summaries/<run_id>_loops.csv
results/summaries/<run_id>_transitions.csv
results/summaries/<run_id>_effects.csv
results/figures/<run_id>_m4_path_diagnostics.png
results/manifests/<run_id>.json
results/reports/<run_id>_report.md
results/reports/<run_id>_warnings.log
```

`cells` has one row per master seed/scenario/path/direction/km and reports mean
mask rate, mean end receptivity, their standard errors across children, state
quantiles, mean Q-values, action/outcome counts, and bounds violations.

`paths` aligns ascending and descending curves by increasing numeric `km` and
records down-minus-up gaps for masking and receptivity. Cold-start rows have no
directional gap. Never average path types before effect calculation.

`loops` contains seed-level and across-seed signed/absolute area, maximum and
mean absolute matched-`km` separation, control-excess area, and direction.

`transitions` contains seed-level and pooled transition estimates, censoring
status, bootstrap validity, interval, and eligibility for mask targets `.5`
and `.75`.

`effects` contains seed-level and five-seed Student-t summaries for feedback
endpoint effects, inherited-versus-control loop effects, speed/horizon changes,
and scenario contrasts. Children may describe cell means but may not replace
master seeds as inferential units.

The figure must display, separately:

1. inherited mask paths by ramp speed;
2. inherited receptivity paths by ramp speed;
3. inherited versus reversal-only aligned gaps;
4. seed-level signed loop areas and transition widths;
5. sensitivity/ablation results only when that tier includes them.

Do not label the figure “hysteresis” unless Pass E supports C9. Before then use
“M4 continuation-path diagnostics.”

## 11. Loop and transition estimators

### Loop area

Let increasing `x` be the numeric `km` grid, `u(x)` the ascending response,
and `d(x)` the descending response reversed back into increasing-x alignment.
For each seed and response, define:

```text
signed_area = sum_i .5 * ((d_i-u_i) + (d_{i+1}-u_{i+1}))
                    * (x_{i+1}-x_i)
absolute_area = sum_i .5 * (abs(d_i-u_i) + abs(d_{i+1}-u_{i+1}))
                      * (x_{i+1}-x_i)
```

Positive mask signed area means the descending path masks more than the
ascending path at matched `km`. Negative receptivity signed area means the
descending path has lower receptivity. Do not normalize area by ramp width in
the primary field; a separately named `mean_vertical_separation` may equal
`signed_area/.004`.

Compute the same quantities for reversal-only controls. The paired seed-level
control-excess mask area is inherited mask area minus reversal mask area. For
receptivity, use inherited receptivity area minus reversal receptivity area;
the expected direction is negative.

### Transition locations

For each path and seed, fit the mask response over increasing `km` with an
equal-weight nondecreasing PAVA. Reject nonfinite or unsorted inputs. Invert
targets `.5` and `.75` only when fitted values bracket the target and the
linear-interpolated or exact-plateau midpoint lies strictly inside `(0,.004)`.
Never extrapolate. Status is one of `valid`, `no_crossing_below`,
`no_crossing_above`, or `boundary_or_undefined`.

For a valid target, define hysteresis width as:

```text
width = ascending_transition_km - descending_transition_km
```

A positive width is the expected direction when descending masking remains
higher at matched `km`. Target `.5` is primary; `.75` is a prespecified
secondary diagnostic and may be censored without alone failing C9.

Bootstrap transition widths by resampling exactly five complete master-seed
path pairs with replacement 10,000 times, averaging curves with equal seed
weight, refitting PAVA, and retaining a width only when both transitions are
valid. An interval is estimable only when the pooled pair is valid and at least
95% of bootstrap samples yield valid paired transitions. Use the same version-
independent linear percentile rule as E05.

## 12. Frozen C8 decision rules

### Self-reinforcing masking feedback

C8's feedback component passes in S01 only if all hold:

1. cold-start mask rate at actual `km=.004` minus `km=0` is positive in at
   least four of five seeds and its paired five-seed Student-t interval has
   lower bound greater than zero;
2. cold-start final receptivity at `.004` minus `0` is negative in at least
   four of five seeds and its interval has upper bound below zero;
3. bounds violations are zero and raw/count/state reconciliation passes.

### Replicated path dependence

C8's path-dependence component passes for a primary speed only if all hold:

1. inherited mask signed area is positive and inherited receptivity signed
   area is negative in at least four of five seeds;
2. their five-seed intervals exclude zero in the expected directions;
3. inherited-minus-reversal control-excess mask area is positive and
   receptivity area is negative, with intervals excluding zero;
4. mean or maximum matched-`km` separation is nonzero in at least four seeds;
5. S08 disabled-feedback placebo does not equal or exceed the active S01
   control-excess area in the same direction;
6. semantics, determinism, completeness, and provenance gates pass.

If only one primary speed passes, maximum wording remains “schedule-specific
path dependence at the tested speed.” If both pass but the effect changes
materially with speed, report speed-dependent path dependence. C8 does not
require C9.

## 13. Frozen C9 hysteresis reconsideration rule

C9 remains excluded unless the core standard first makes it **eligible for
qualification**. Eligibility requires all of the following in both S00 and
S01:

1. the pooled inherited ascending and descending `.5` transitions are valid;
2. at least four of five seed pairs have valid `.5` widths;
3. at least 95% of bootstrap replicates have valid paired widths;
4. the 95% width interval is strictly positive;
5. mask and receptivity loop directions are consistent across speeds;
6. inherited loop/control-excess rules in Section 12 pass;
7. the reversal-only and S08 placebo results cannot account for the inherited
   transition width or loop area.

If any item fails, do not run the qualification tier merely to search for a
favorable result. C9 stays excluded and E06 may still complete C8.

After a separately authorized Q00 run, C9 can be reconsidered only if the
same `.5` transition and control rules pass at horizon 2000. Define material
decay as both:

- absolute Q00 mean width or control-excess mask area is less than 50% of its
  S00 value; and
- the Q00 interval includes zero.

Material decay requires the wording “transient path dependence,” not
hysteresis. Q01--Q04 report learner sensitivity and cannot rescue a failed
S00/S01/Q00 gate. Even if every gate passes, the maximum claim is
“hysteresis in the frozen M4 continuation experiment,” not irreversibility,
entrenchment in human students, or a universal behavioral phase transition.

## 14. Validation and tests required before smoke

Pass B must add focused tests for:

1. exact reward-then-Q-then-receptivity order;
2. maintained replay against `simulate_from_state` for forced and stochastic
   small cases;
3. p bounds and zero bounds-violation accounting;
4. inherited Q/p continuity across every segment including the turning point;
5. reversal/cold reset of both Q and p;
6. exact segment RNG pairing between inherited and reversal paths;
7. global-RNG isolation and execution-order independence;
8. strict config validation, including duplicate keys and exact numeric types;
9. packed-array lengths, counts, rates, states, Q-values, and JSON finiteness;
10. raw-to-cell/path/loop/effect/transition reconstruction;
11. trapezoidal signed/absolute area on synthetic curves;
12. PAVA transition interpolation, plateau, censoring, nonfinite, and unsorted
    cases;
13. bootstrap master-seed pairing, valid-width fraction, and percentile math;
14. smoke inference/claims unavailable and standard dispatch refused;
15. deterministic same- and cross-directory regeneration;
16. byte-identical maintained M4/legacy artifacts before and after any shared
    helper extraction;
17. exact row, segment, learner-step, runtime, raw-size, total-size, and RSS
    capacity calculations.

Every validator must fail closed. Schema/cardinality-only validation is not
sufficient.

## 15. Resource and stop gates

The smoke manifest/report must separately measure or conservatively project:

- simulation by learner-step ratio;
- raw serialization by packed primary-row size and array lengths;
- derived analysis by scenario/path/cell cardinality;
- bootstrap cost;
- figure/startup as fixed overhead;
- peak RSS.

Before a future core-standard GO, the fresh-process projection must be
reproducible and satisfy:

```text
wall time <= 600 seconds
raw artifact <= 400 MiB
all artifacts <= 500 MiB
peak RSS <= 2 GiB
```

If a gate fails, return `REVISE_SPECIFICATION`; do not optimize model semantics,
drop adverse scenarios silently, or execute only convenient shards. Streaming
or resumable execution may be implemented, but canonical output must be
deterministic and invariant to shard boundaries.

The qualification tier requires its own measured projection and GO. Core GO
never authorizes qualification.

## 16. Smoke artifacts and checkpoint

The smoke checkpoint report must state:

1. exact config and approval hash;
2. maintained semantic replay results;
3. path/control definitions;
4. seed hierarchy and pairing boundaries;
5. exact rows, segments, and learner-steps;
6. state-continuity and reset checks;
7. bounds and count reconciliation;
8. diagnostic path/loop/transition output, explicitly noninferential;
9. deterministic regeneration and hashes;
10. focused and full-repository verification;
11. standard and qualification resource projections;
12. warnings and unresolved risks;
13. stop status `PENDING_SOL_SMOKE_REVIEW`.

The smoke gate reviewer must return exactly one of `GO_STANDARD`,
`FIX_IMPLEMENTATION`, `REVISE_SPECIFICATION`, or `NARROW_OR_STOP_CLAIM`.
Only a later canonical `E06_STANDARD_GO.md` may flip the exact core standard's
approval state. No E06 result may enter the claim ledger or manuscript before
independent standard adjudication.
