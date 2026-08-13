# E05 Scientific Approval Record

**Decision:** `APPROVED_FOR_SMOKE`  
**Date:** 2026-08-12  
**Scope:** bounded E05 implementation and diagnostic smoke only  
**Question preserved:** where learned good-context authenticity changes as
`bf` crosses the analytic objective threshold, with the analytic and learned
quantities reported separately.

This record resolves the E05 implementation ambiguities in
`STAGE2_EXPERIMENT_SPECIFICATIONS.md`. It does not authorize an E05 standard
run, a `T=5000` run, claim adjudication, a claim-ledger update, a manuscript
edit, or any change to maintained M3 semantics, defaults, or RNG behavior.

## 1. Authority and provenance audit

The design was checked against repository `AGENTS.md`, the article RDS, the
Stage 2 experiment specification and runbook, C7 in `CLAIM_LEDGER.md`, current
state/backlog/architecture records, maintained M3 code and tests, the coarse
C7 artifacts, and the completed E04 smoke infrastructure and artifacts.

The audit found:

1. `src/gifted_masking/models/m3.py` implements the intended flat action
   decoding and subtracts `bf` only from an accepted authentic reward in the
   fixed good context. Masking, rejected authenticity, and bad-context
   authenticity do not receive the cost.
2. At the frozen defaults, maintained analytic replay gives
   `E(mask)=0.75`, `E(good auth)=1.15-0.85*bf`, `E(bad auth)=-0.80`, and
   `bf*=8/17=0.47058823529411764`. The good-authentic objective advantage is
   `0.40-0.85*bf`: `0.40` at `bf=0`, `0.0175` at `.45`, zero at the exact
   anchor, `-0.00375` at `.475`, and `-0.28` at `.80` (up to binary floating
   representation).
3. The maintained coarse C7 artifact reproduces `220` units per endpoint and
   a low-minus-high modal-good-authentic difference of
   `0.9181818181818182` (`0.9181818` at `bf=0`, `0` at `bf=.8`). Its two
   conditions use different seeds and it has neither a dense response nor
   independent-master-seed transition uncertainty. It remains descriptive
   provenance, not E05 evidence and not a paired estimate.
4. The E04 smoke manifest's seven recorded output hashes and its approval hash
   match the current files. E04 established an isolated, fixed-identity replay
   for flat and hierarchical architectures and a cell-order-independent matched
   stream pattern at `bf=0`. It did not vary `bf` and cannot identify a C7
   transition.
5. `E04_STANDARD_GO.md` exists, but no E04 standard artifacts are present and
   the current E04 dispatcher still refuses standard execution. E05 therefore
   must not cite an E04 standard result. E05 is scientifically separable and
   may proceed to its own smoke gate without adjudicating C6.

No provenance conflict changes the E05 question. The missing dense behavioral
evidence is exactly what E05 is designed to produce.

## 2. Frozen scientific semantics

- Primary architecture: maintained flat `2K` M3 with `K=4`, eight joint arms,
  fixed good-context identity `good_context_id=0`, and good-authentic action
  index `1`.
- Secondary architecture: maintained hierarchical context-then-behavior M3 at
  the same `K=4` and fixed identity. It has four group values and a `4 x 2`
  behavior table; the reported joint modal index remains `2*group+behavior`.
- Architectures are analyzed separately. No outcome, transition, interval, or
  bootstrap sample may pool them.
- Frozen receptivity: `p_good=.85`, `p_bad=.20`.
- Frozen payoffs: `b=1.0`, `a=.6`, `c=.25`, `r=2.0`.
- Frozen learner: `alpha=.1`, `tau=.25`, `lambda=1.0`, `q0=0.0`.
- Reward/update order must replay maintained M3 exactly. Flat draws one policy
  uniform then one acceptance uniform per learner/step. Hierarchical draws a
  group policy uniform, a behavior policy uniform, then an acceptance uniform.
  The acceptance draw is consumed even on masking trials. Objective reward is
  calculated, subjective value is formed, and only the selected flat action or
  selected hierarchical group and behavior entries are updated.
- Realized reward is exactly:

  ```text
  mask in any context                 = b - c = 0.75
  accepted auth in good context       = b + a - bf = 1.60 - bf
  rejected auth in good context       = a - r = -1.40
  accepted auth in a bad context      = b + a = 1.60
  rejected auth in a bad context      = a - r = -1.40
  ```

  Thus `bf` is subtracted if and only if
  `authentic and context==0 and accepted`. It never changes an acceptance
  probability and is never applied to masking, rejection, or bad contexts.
- Maintained M3 and robustness code are not to be modified. Implement E05 as
  an isolated config-driven experiment kernel. A shared private diagnostic
  helper may be extracted only if pre/post E04 smoke machine artifacts and PNG
  remain byte-identical and maintained M3 replay tests still pass.

## 3. Analytic benchmark and dense grid

For every `bf`, emit the objective quantities independently of learner output:

```text
E_mask = b - c = 0.75
E_good_auth(bf) = p_good*(b+a-bf) + (1-p_good)*(a-r)
                = 1.15 - 0.85*bf
Delta_objective(bf) = E_good_auth(bf) - E_mask
                    = 0.40 - 0.85*bf
bf* = 0.40/0.85 = 8/17 = 0.47058823529411764
E_bad_auth = p_bad*(b+a) + (1-p_bad)*(a-r) = -0.80
```

The exact threshold anchor is the nearest binary64 representation of `8/17`,
written in JSON as `0.47058823529411764`. The analytic table must also store
the exact string `8/17`. At that anchor the comparator is a tie within absolute
tolerance `1e-12`; the stored analytic advantage is canonicalized to `0.0`.

Both tiers use the same 18 unique, sorted `bf` values:

```text
[0.0,
 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45,
 0.47058823529411764,
 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65,
 0.8]
```

The decision-bearing dense range is `[.30,.65]`, including the exact threshold
anchor. `0` and `.80` are endpoint anchors only; they cannot create an
otherwise absent in-range learned crossing.

Canonical `bf_label` values are three-decimal strings for all nonthreshold
points (`0.000`, `0.300`, ..., `0.800`) and the literal `8over17` for the exact
threshold. The parameter cell ID is exactly
`E05|architecture=<architecture>|K=4|identity=fixed0|bf=<bf_label>`.
Parameter IDs do not depend on tier, `n`, or horizon; those fields remain
explicit elsewhere. Sorting uses numeric `bf`, never lexical label order.

For flat and hierarchical architectures, the objective-best joint-action sets
are `[1]` below the threshold, `[0,1,2,4,6]` at the threshold, and
`[0,2,4,6]` above it. The analytic threshold is proved from the equation and
must never be labeled a learned threshold.

## 4. Exact smoke and staged-standard configurations

Pass B must add exactly these config paths:

- `configs/frontiers_article/e05_m3_bflpe_crossover_smoke.json`
- `configs/frontiers_article/e05_m3_bflpe_crossover_standard.json`

The smoke configuration is:

```json
{"experiment_id":"E05","run_id":"frontiers_m3_bflpe_crossover_v1_smoke","tier":"smoke","model":"M3","n":96,"T":300,"final_window_fraction":0.2,"master_seed":2026081599,"bootstrap_seed":2026081597,"bootstrap_replicates":0,"workers":1,"payoffs":{"b":1.0,"a":0.6,"c":0.25,"r":2.0},"learner":{"alpha":0.1,"tau":0.25,"lambda":1.0,"q0":0.0},"design":{"architectures":["flat_2k","hierarchical"],"K":4,"good_context_id":0,"p_good":0.85,"p_bad":0.2,"bf_values":[0.0,0.3,0.325,0.35,0.375,0.4,0.425,0.45,0.47058823529411764,0.475,0.5,0.525,0.55,0.575,0.6,0.625,0.65,0.8],"analytic_threshold_exact":"8/17","analytic_threshold_bf":0.47058823529411764,"dense_bf_min":0.3,"dense_bf_max":0.65,"transition_response":0.5}}
```

It has exactly `36` architecture-by-`bf` cells, `3,456` primary rows, and
`1,036,800` learner-steps. Its final window is steps `240-299` inclusive. It
is diagnostic: no Student-t interval, bootstrap interval, learned-threshold
claim, or C7 adjudication is permitted.

The standard configuration must be staged but remain non-executable:

```json
{"experiment_id":"E05","run_id":"frontiers_m3_bflpe_crossover_v1","tier":"standard","model":"M3","n":500,"T":2000,"final_window_fraction":0.2,"master_seed":2026081501,"master_seeds":[2026081501,2026081502,2026081503,2026081504,2026081505],"bootstrap_seed":2026081597,"bootstrap_replicates":10000,"workers":1,"approved_standard":false,"payoffs":{"b":1.0,"a":0.6,"c":0.25,"r":2.0},"learner":{"alpha":0.1,"tau":0.25,"lambda":1.0,"q0":0.0},"design":{"architectures":["flat_2k","hierarchical"],"K":4,"good_context_id":0,"p_good":0.85,"p_bad":0.2,"bf_values":[0.0,0.3,0.325,0.35,0.375,0.4,0.425,0.45,0.47058823529411764,0.475,0.5,0.525,0.55,0.575,0.6,0.625,0.65,0.8],"analytic_threshold_exact":"8/17","analytic_threshold_bf":0.47058823529411764,"dense_bf_min":0.3,"dense_bf_max":0.65,"transition_response":0.5}}
```

It has exactly `90,000` primary rows and `180,000,000` learner-steps; the
final window is steps `1600-1999`. Smoke authorization must not flip
`approved_standard`, add a standard dispatcher, or accept any approval record
other than a future canonical E05-specific `GO_STANDARD` record.

Config loading must reject duplicate JSON keys, booleans in numeric fields,
integer/float substitutions where exact JSON type is frozen, numeric strings,
unknown or missing keys, reordered/duplicated/missing `bf` values, a missing or
altered exact anchor, any extra architecture, nonfixed identity, changed
payoff/learner values, workers other than one, and any standard mutation.

## 5. RNG and pairing contract

- Use a fresh vectorized policy/environment RNG for every
  architecture/master-seed matched family and reinitialize that same family
  seed at every `bf`. This creates genuine common-random-number child pairing
  across all `bf` conditions within one architecture and master seed.
- The matched family ID is exactly
  `E05|master=<seed>|architecture=<architecture>|K=4|identity=fixed0|policy_environment`.
- Derive the family seed with SHA-256 words from that ID and
  `SeedSequence([master_seed,5,*words]).spawn(1)`. Record the full derivation
  and resulting seed in the manifest and every primary row.
- `cell_seed` equals `policy_environment_seed`; `child_seed` is the literal
  `vectorized_matched_policy_environment_stream`. `child_id` is a real paired
  identifier only for different `bf` values sharing the same recorded matched
  family. It is not a pair across architectures or master seeds.
- Flat and hierarchical architectures use different family IDs and seeds.
  Never perform a paired flat-versus-hierarchical test. Master seeds are
  independent top-level replicates.
- There is no identity RNG because good-context identity is fixed at index `0`.
- The one maintained policy/acceptance RNG stream is not split into new
  components. Reusing it preserves architecture-specific M3 draw order.
- Cell execution order must not affect any row: each cell starts by rebuilding
  its family RNG from the recorded seed. Primary row order is exactly
  architecture declaration order (`flat_2k`, then `hierarchical`), numeric
  `bf`, numeric master seed, numeric child ID.
- Bootstrap RNG is analysis-only. Derive separate flat and hierarchical
  streams from `SeedSequence([2026081597,50,architecture_code])`, with codes
  `0` and `1`. Bootstrap draws cannot affect simulation rows.

## 6. Exact ordered primary schema

Write one row per child, architecture, `bf`, and master seed. CSV columns must
appear in exactly this order:

```text
run_id,experiment_id,tier,model,component,sensitivity_name,architecture,architecture_role,master_seed,matched_family_id,parameter_cell_id,cell_seed,policy_environment_seed,child_id,child_seed,rng_unit,K,good_context_id,p_good,p_bad,bf,bf_label,is_analytic_threshold_anchor,b,a,c,r,alpha,tau,lambda,q0,n,T,final_window_fraction,final_window_start,final_window_end,joint_action_count,group_action_count,behavior_action_count,expected_mask_reward,expected_good_auth_reward,expected_bad_auth_reward,analytic_objective_advantage_good_auth_minus_mask,analytic_threshold_bf,objective_best_expected_reward,objective_comparator,objective_best_joint_actions_json,mask_count_total,good_auth_count_total,good_auth_accept_count_total,good_auth_reject_count_total,bad_auth_count_total,bad_auth_accept_count_total,bad_auth_reject_count_total,authentic_count_total,good_context_action_count_total,total_action_counts_json,final_window_mask_count,final_window_mask_rate,final_window_authentic_count,final_window_authentic_rate,final_window_good_context_action_count,final_window_good_auth_count,final_window_good_auth_rate,final_window_auth_given_good_context_rate,final_window_auth_given_good_context_status,final_window_action_counts_json,final_window_modal_action_index,final_window_modal_context,final_window_modal_behavior,final_window_modal_tie_count,final_window_unique_modal,modal_good_auth_argmax,modal_good_auth_unique,modal_is_objective_optimal,cumulative_realized_objective_reward,mean_realized_objective_reward,cumulative_expected_static_regret,mean_expected_static_regret,cumulative_realized_pseudo_regret,mean_realized_pseudo_regret,q_final_json,q_group_final_json,q_behavior_final_json
```

`architecture_role` is `primary` for flat and `secondary` for hierarchical.
`component=primary`, `sensitivity_name=baseline`, and `rng_unit` is
`vectorized_architecture_matched_bf_stream`. Conditional authentic-in-good
rate is blank with status `undefined_no_good_context_actions` only when its
denominator is zero. JSON vectors are compact and have architecture-correct
lengths. Ties retain NumPy's maintained first-argmax result in
`modal_good_auth_argmax`; `modal_good_auth_unique` additionally requires a
unique modal action. The primary learned response is the mean of
`modal_good_auth_argmax`; tie and unique-modal rates are mandatory diagnostics.

The objective comparator is `good_auth`, `tie`, or `mask`. Expected static
regret uses the architecture-available best static joint action set at that
`bf` and is nonnegative up to `1e-12`. Objective realized reward remains
separate from subjective learning value.

## 7. Ordered derived schemas and artifacts

Each run must produce:

```text
results/manifests/<run_id>.json
results/raw/<run_id>_units.csv
results/summaries/<run_id>_analytic.csv
results/summaries/<run_id>_cells.csv
results/summaries/<run_id>_effects.csv
results/summaries/<run_id>_transitions.csv
results/figures/<run_id>_bflpe_crossover_diagnostics.png
results/reports/<run_id>_report.md
```

The analytic CSV has exactly this schema and 18 rows:

```text
run_id,experiment_id,tier,bf,bf_label,is_analytic_threshold_anchor,p_good,p_bad,b,a,c,r,expected_mask_reward,expected_good_auth_reward,expected_bad_auth_reward,analytic_objective_advantage_good_auth_minus_mask,analytic_threshold_exact,analytic_threshold_bf,objective_comparator
```

The cell CSV has one row per architecture/master seed/`bf`, sorted in the same
leading order as raw, and this exact schema:

```text
run_id,experiment_id,tier,architecture,architecture_role,master_seed,matched_family_id,parameter_cell_id,bf,bf_label,is_analytic_threshold_anchor,n,T,final_window_fraction,final_window_start,final_window_end,modal_good_auth_argmax_n,modal_good_auth_argmax_fraction,modal_good_auth_unique_n,modal_good_auth_unique_fraction,unique_modal_n,modal_tie_n,mean_final_window_good_auth_rate,mean_final_window_auth_given_good_context_rate,conditional_good_context_defined_n,mean_final_window_authentic_rate,mean_final_window_mask_rate,mean_realized_objective_reward,mean_expected_static_regret,mean_realized_pseudo_regret,analytic_objective_advantage_good_auth_minus_mask,objective_comparator
```

Its cardinality is exactly `36` rows for smoke and `180` for standard.

The effect CSV schema is:

```text
run_id,experiment_id,tier,architecture,architecture_role,effect_family,effect_name,metric,level,master_seed,bf_low,bf_high,estimate,seed_n,ci_method,ci_low,ci_high,decision_input,notes
```

It must contain, separately by architecture, response-at-`bf` and endpoint rows
for exactly these six metrics:

```text
modal_good_auth_argmax_fraction
modal_good_auth_unique_fraction
mean_final_window_good_auth_rate
mean_final_window_auth_given_good_context_rate
mean_realized_objective_reward
mean_expected_static_regret
```

It also contains every adjacent dense-grid higher-minus-lower change for
`modal_good_auth_argmax_fraction`. There are 16 decision-range points and 15
adjacent changes per architecture; anchors are excluded from this shape test.
Endpoint rows are `bf=.80 minus bf=0`. Standard across-seed rows use the five
paired master-seed estimates and the fixed two-sided Student-t critical value
`2.7764451051977987`; smoke has only one seed row with blank intervals and
`ci_method=not_estimable_smoke`. Consequently the exact effect cardinality is
`258` rows for smoke and `1,548` rows for standard.

Effect names are canonical strings:

```text
response|metric=<metric>|bf=<bf_label>
adjacent|metric=modal_good_auth_argmax_fraction|bf=<low_label>_to_<high_label>
endpoint|metric=<metric>|bf=0.000_to_0.800
```

The transition CSV schema is:

```text
run_id,experiment_id,tier,architecture,architecture_role,level,master_seed,response_metric,fit_method,target_response,dense_bf_min,dense_bf_max,transition_bf,transition_status,raw_dense_start_response,raw_dense_end_response,isotonic_dense_start_response,isotonic_dense_end_response,valid_dense_crossing,valid_seed_crossing_count,monotonicity_violation_count,bootstrap_replicates,bootstrap_valid_crossings,bootstrap_crossing_fraction,ci_method,ci_low,ci_high,analytic_threshold_bf,learned_minus_analytic_threshold,decision_eligible,notes
```

The standard table has five seed rows and one pooled row per architecture.
Smoke has one diagnostic seed row and one pooled-diagnostic row per
architecture; both are explicitly noninferential and `decision_eligible=False`.
Transition cardinality is therefore exactly `4` smoke rows and `12` standard
rows.

The figure must separate the analytic objective-advantage panel from learned
response panels. Learned flat and hierarchical curves are not pooled. Draw an
analytic vertical marker at `8/17`. Draw an architecture-specific learned
marker only when that architecture's frozen transition criteria pass; otherwise
label the transition unavailable. The smoke figure must be labeled diagnostic
and omit inferential intervals and learned-threshold claims.

The manifest must include the exact config/command, canonical approval hash,
commit and binary dirty/source fingerprints, Python/platform/NumPy/matplotlib
versions, seed derivation and matched-family map, ordered schema and sort keys,
analytic formula and exact threshold, estimator/bootstrap version, timestamps,
resource measurements/projections, warnings, output paths, row counts, hashes,
and verification state. Source fingerprinting must include E05 runner, CLI,
core, M3, repro, both E05 configs, E05 tests, this approval, `pyproject.toml`,
and `scripts/verify.sh` (plus any imported shared experiment helper).

The 13-item runbook report must reproduce all decision inputs, explicitly
separate analytic and learned results, state that smoke is noninferential,
record baseline replays/determinism/reconciliation/manual sentinels, list all
artifacts, and stop with a recommendation for separate smoke review rather
than a C7 conclusion.

## 8. Dependency-free learned-transition estimator

No new package is permitted. Implement a pure Python/NumPy nonincreasing PAVA:

1. Input the raw seed-level primary response in numeric `bf` order.
2. Start one equal-`n` weighted block per point.
3. While a left block mean is less than the following block mean, merge the
   adjacent blocks using their total weights; continue backward until all
   block means are nonincreasing.
4. Expand block means to fitted points. Do not round fitted values.
5. Restrict transition inversion to the dense points in `[.30,.65]`; anchors
   `0` and `.80` are excluded.
6. If a contiguous fitted plateau equals `.5` within absolute tolerance
   `1e-15`, use the midpoint of the plateau's minimum and maximum `bf`.
   Otherwise linearly interpolate the unique adjacent fitted points with
   values strictly above and below `.5`.
7. A seed transition is valid only if the fitted response brackets `.5` and
   the resulting location is strictly inside `(.30,.65)`. Otherwise report
   `no_crossing_above`, `no_crossing_below`, or `boundary_or_undefined`; never
   extrapolate.

For monotonicity within Monte Carlo uncertainty, compute each adjacent
dense-grid change as `response(higher bf)-response(lower bf)` within each
master seed, then its five-seed paired Student-t interval. A material upward
violation is an interval whose lower bound is greater than zero. Count and
report violations separately by architecture. There is no multiple-comparison
adjustment because this is a fail-closed shape diagnostic, not a collection of
positive claims.

For the standard learned-transition interval:

1. Use the five complete master-seed response curves as the top-level units.
   Do not resample children and do not use administrative pairing across
   architectures.
2. For each of exactly `10,000` replicates, sample five master-seed curves with
   replacement, average them with equal seed weight at each `bf`, run the same
   PAVA and dense-range inversion, and record a transition only when valid.
3. Report `bootstrap_crossing_fraction = valid/10000`. An interval is
   estimable only if the pooled curve has a valid transition and at least 95%
   of bootstrap replicates are valid.
4. Use a version-independent linear percentile: after sorting valid locations,
   for quantile `q`, set `h=(N-1)q` and linearly interpolate values at
   `floor(h)` and `ceil(h)`. Report the `.025` and `.975` quantiles.
5. If fewer than 95% are valid, leave interval and learned-minus-analytic
   interval claims unavailable; report the curve and censoring fraction.

## 9. Frozen decision rule

The analytic threshold is reported from the reward equation whenever analytic
validation passes, regardless of learned behavior.

A learned crossover is supported for the **primary flat architecture** only if
all of these hold in the complete standard package:

1. at least four of five seed-level PAVA curves have a valid transition
   strictly inside `(.30,.65)`;
2. no adjacent dense-grid response change has a material upward monotonicity
   violation under the five-seed paired Student-t rule;
3. the equal-seed pooled PAVA curve has a valid dense-range transition;
4. at least 95% of the 10,000 top-level bootstrap replicates have a valid
   transition and therefore yield a finite percentile interval; and
5. all semantic, RNG, schema, reconciliation, determinism, provenance, and
   verification gates pass.

Apply the same rule separately to hierarchical results as a secondary finding.
Hierarchical success cannot rescue a failed primary-flat decision, and flat
success cannot be generalized to the hierarchical architecture if its rule
fails. Even when both pass, report architecture-specific learned transitions,
not one pooled or universal threshold.

If the flat rule fails, report its response curve, seed variation, endpoint
change, and failure reason; do not report a flat learned threshold. Smoke can
never satisfy the rule. No `bf` value may be translated into a human placement,
self-concept, or intervention threshold.

## 10. `T=5000` authorization boundary

No `T=5000` execution is authorized by this record or by a future baseline
`GO_STANDARD` record. The first standard execution, if separately approved,
is the full frozen dense `T=2000` package only.

After that package is reviewed, a distinct `E05_T5000_GO.md` may authorize a
targeted horizon sensitivity only for architectures whose pooled `T=2000`
transition is valid. For each eligible architecture, the deterministic selector
is every frozen dense/threshold `bf` point satisfying
`abs(bf-transition_bf) <= .05`; no new `bf` may be invented. This selects at
most six points per architecture. The future config must use `n=500`,
`T=5000`, final window `.2`, the same five master seeds, the same family seeds
and child pairing (so the first 2,000 steps are an exact prefix), one worker,
and an exact point list recorded in the new GO file. Its projected runtime and
storage must be reviewed before execution.

If no valid standard transition exists, no `T=5000` threshold-local run is
performed. A `T=5000` result is horizon sensitivity, not permission to tune the
transition or expand the dense range.

## 11. Strict validation, tests, and manual sentinels

Pass B must add focused E05 tests before smoke and run E05, M3, E04 regression,
and full repository verification. Required automated checks are:

1. exact config types/keys/values; exact 18-point order, unique threshold
   anchor, 36 cells, tier cardinalities, and standard refusal;
2. `bf*=8/17`, all analytic anchor values, comparator ties/actions, and
   absolute analytic agreement with maintained `expected_reward_for_action`
   to `1e-12`;
3. event-level proof that `bf` changes only accepted good-authentic reward;
4. exact flat and hierarchical maintained-kernel replay at `bf=0` and `.80`
   for small fixed cases, including draw and update order;
5. matched-family equality across `bf`, inequality across architectures and
   master seeds, child pairing scope, cell-order independence, deterministic
   order, and no global RNG mutation;
6. exact ordered raw schema and cross-field reconciliation of action vectors,
   mask/authentic/good/bad accept/reject counts, final-window indices, modal
   ties, Q shapes, realized reward, expected regret, and pseudo-regret;
7. raw-to-analytic/cell/effect/transition reconstruction to `1e-12`, with
   missing/duplicate/foreign seed-cell-child rows rejected;
8. PAVA synthetic cases for unchanged decreasing curves, pooled violations,
   interpolation, exact `.5` plateaus, boundary cases, no-crossing statuses,
   and anchor exclusion;
9. fixed synthetic five-seed Student-t and 10,000-replicate bootstrap tests,
   including master-seed resampling, deterministic architecture streams,
   percentile arithmetic, valid-crossing fraction, and censored intervals;
10. smoke intervals/claims remain unavailable; standard effects require all
    five frozen seeds before pooling;
11. normalized same- and cross-directory deterministic regeneration, byte-match
    of CSVs and PNG, manifest completeness, approval/source/output hash checks,
    and binary dirty-state provenance; and
12. E04 smoke scientific artifacts remain byte-identical and maintained M3
    code/defaults/RNG have not changed.

Manual smoke inspection must include:

- flat actions `0/1` for good mask/auth and `6/7` for context 3;
- hierarchical joint decoding plus both selected Q updates;
- one accepted/rejected good-auth, accepted/rejected bad-auth, and mask row at
  more than one `bf`, with the realized-reward identity recomputed by hand;
- analytic advantages at `0`, `.45`, `8/17`, `.475`, and `.80`;
- threshold tie actions `[0,1,2,4,6]` and no cost on mask/rejection/bad-auth;
- exact final-window steps `240-299`, all 96 child IDs in every smoke cell,
  same family seed/child ID across `bf`, and distinct architecture families;
- at least one modal good-auth and one non-good-auth row per architecture when
  present; if a sentinel is absent stochastically, use a deterministic
  synthetic row rather than changing the seed; and
- diagnostic PAVA crossing/no-crossing output without interpreting it as an
  E05 result.

Any analytic disagreement, reward-semantic drift, baseline replay failure,
nondeterminism, pairing leak, invalid raw reconstruction, missing exact anchor,
or manifest/hash failure returns `FIX_IMPLEMENTATION` or
`REVISE_SPECIFICATION`; it is not waived by a plausible curve.

## 12. Runtime, storage, and stop limits

The E04 measured vectorized rate implies approximately `1.8` seconds for the
E05 smoke learner kernel and approximately `5.2` minutes for the baseline
standard learner work before environment-specific overhead. These are planning
estimates, not executed E05 timings.

Smoke must stop and report rather than self-authorize standard if any of these
holds:

- wall time exceeds `60` seconds;
- raw CSV exceeds `10 MiB`;
- peak RSS exceeds `512 MiB`;
- exact raw/cell cardinality differs from `3,456/36`;
- the linear standard projection exceeds `10` minutes, `200 MiB` raw, `250 MiB`
  total artifacts, or `2 GiB` peak RSS; or
- any required semantic, deterministic, provenance, or verification check
  fails.

Any future baseline standard run must stop above `600` seconds wall time,
`200 MiB` raw, `250 MiB` total artifacts, or `2 GiB` peak RSS and return to
review. Streaming primary-row writing is required for standard; deterministic
cell summaries may be accumulated in memory. No parallel execution is approved.

## 13. Pass B acceptance and handoff

Pass B may implement only the isolated E05 runner, CLI route, exact smoke and
staged-standard configs, tests, artifacts, and documentation required above.
It may execute only the smoke config using
`/Users/omer/workspace/venvs/venv314/bin/python`, then run targeted tests and
`./scripts/verify.sh`, reconcile and regenerate the smoke, finalize the
13-item checkpoint, and stop for a separate Sol smoke-gate review.

No model semantic, default, maintained RNG, C7 wording, claim ledger,
manuscript, E04 result, sensitivity, standard, or publication-tier change is
authorized.
