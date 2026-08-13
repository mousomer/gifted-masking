# Article Claim Ledger

This ledger is the working contract between manuscript language and evidence.
It freezes the Stage 1 claim hierarchy, identifies exact current evidence, and
defines the evidence gate for stronger wording. Status values are `supported`,
`partial`, `planned`, or `excluded`.

## Claim hierarchy

| Rank | ID | Intended article role | Stage 1 status |
| --- | --- | --- | --- |
| Primary 1 | C1 | Central outcome: learned masking despite optimal authenticity | Partial |
| Primary 2 | C2 | Central mechanism: hot-stove information restriction | Planned |
| Primary 3 | C4 | Graded disclosure as a lower-exposure exploratory route | Partial |
| Primary 4 | C5 | M2 learned suboptimal-masking regime | Partial |
| Primary 5 | C6 | M3 context-search burden | Partial |
| Primary 6 | C8 | M4 endogenous feedback and path dependence | Partial |
| Secondary 1 | C3 | Negative-outcome weighting increases avoidance | Partial |
| Secondary 2 | C7 | Learned comparison-cost retreat before objective indifference | Partial |
| Excluded | C9 | M4 establishes hysteresis | Excluded |
| Excluded | C10 | Simulations estimate human prevalence or intervention effects | Excluded |

`Partial` does not mean the current result is absent. It means the result does
not yet meet the RDS publication minimum of direct mechanism-appropriate
analysis, uncertainty, and at least three independent master seeds.

## Evidence records

### C1 — Learned masking despite optimal authenticity

- **Intended outcome:** risky authenticity can produce persistent learned
  masking in cells where authenticity is the objective optimal policy.
- **Current evidence class:** analytically benchmarked and computationally
  demonstrated across five independent master seeds in the frozen default M2
  domain, with learner-parameter qualification.
- **E01 disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for the information-
  restriction component only. E01 did not show that one initial rejection
  increased final-window masking, so it does not strengthen the C1 persistence
  result itself.
- **E03 disposition:** `SUPPORTED_IN_NARROW_DOMAIN`. The default-learner M2
  regime passed its exact-grid, seed-interval, stability, and `n`/`T`/window
  gates, but the frozen learner-qualification rule was triggered by the
  `gamma=.5` case.
- **Exact evidence:**
  - `results/summaries/m2_lock_in_region_map.csv`, selector
    `region=learned_suboptimal_lock_in` (226 rows of 357);
  - `doc-reviews/frontiers_submission/data/m2_suboptimal_masking_regime_summary.csv`,
    rows `learned_suboptimal_masking_cells`,
    `learned_suboptimal_masking_fraction`, and
    `mean_neutral_mask_probability_in_classified_cells`;
  - `results/summaries/m2_optimal_policy_benchmark.csv`, cases
    `robustness_higher_escape_eta_0.00` and
    `robustness_higher_escape_eta_0.20`;
  - generators `scripts/map_m2_lock_in_regions.py`,
    `scripts/analyze_m2_regimes.py`, and
    `scripts/benchmark_m2_optimal_policy.py`;
  - current display
    `doc-reviews/frontiers_submission/figures/Figure_2_m2_suboptimal_masking_regime.tif`.
  - E01 effects `results/summaries/frontiers_hot_stove_v1_effects.csv`,
    selectors `level=across_master_seeds` and
    `effect_name=rejected_minus_accepted_final_mask_rate`: pooled estimate
    `-0.000343`, 95% Student-t interval `[-0.011605, 0.010918]`; the effect was
    positive in four of five seeds at `p=.75` but only two of five at `p=.85`.
  - E03 primary units
    `results/raw/frontiers_m2_regime_replication_v1_units.csv`, selector
    `tier=standard`, `component=exact_grid`, `sensitivity_name=baseline`, and
    `master_seed in {2026081301,...,2026081305}`;
  - E03 cells and effects
    `results/summaries/frontiers_m2_regime_replication_v1_cells.csv` and
    `results/summaries/frontiers_m2_regime_replication_v1_effects.csv`, same
    exact-grid selector and effect
    `learned_suboptimal_masking_fraction`: every seed had `243/357` and the
    across-seed estimate was `0.680672268907563`, 95% Student-t interval
    `[0.680672268907563,0.680672268907563]`;
  - E03 stability
    `results/summaries/frontiers_m2_regime_replication_v1_stable_cells.csv`,
    selector `stable=True` and
    `classification=learned_suboptimal_masking` (243 rows); and
  - E03 provenance and execution metadata
    `results/manifests/frontiers_m2_regime_replication_v1.json` and
    `results/reports/frontiers_m2_regime_replication_v1_report.md`.
- **Source locations:** `RESULTS_BY_FINDING_CHAPTER.md` lines 3 and 21-31;
  `DISCUSSION_CHAPTER.md` lines 3 and 17-25.
- **Current DOCX locations:** P9, P47-P48, P57-P58, P71, P77; Figure 2
  legend P107; Table 1 row M2.
- **Evidence still required:** no further E03 run is required for this narrow
  disposition. Generalization beyond the exact default learner, the tested
  `p`/`eta` grid, or the frozen `n`/`T`/window perturbations requires a
  separately approved design.
- **Maximum current wording:** “Under the frozen default M2 learner
  (`alpha=.1`, `tau=.25`, `lambda=1`, `q0=0`, `gamma=.9`), learned neutral-state
  masking persisted although value iteration selected authenticity in 243 of
  357 tested `p`-by-`eta` cells (68.1%; five-seed Student-t interval 68.1% to
  68.1%). The same classification held in all five seeds at all five dynamic-
  authenticity sentinels under the prespecified population-size, horizon, and
  final-window perturbations.” Always identify this as a share of the tested
  grid, not a learner or human-population prevalence.
- **Boundary:** “Robust default-learner regime in the tested M2 domain” is
  permitted; an unqualified learner-robust claim is not. At `gamma=.5`, value
  iteration switched from authenticity to masking at three of the five default
  dynamic-authenticity sentinels, triggering the prespecified learner
  qualification. Do not cite E01 as evidence that one early rejected authentic
  outcome increases persistent final-window masking.

### C2 — Hot-stove information restriction

- **Intended outcome:** early adverse authentic outcomes restrict later
  authentic sampling and corrective information, producing persistence.
- **Current evidence class:** demonstrated computationally in the narrow E01
  domain for later sampling, regret, and information-restoring interventions;
  not supported for an early-rejection effect on final-window masking.
- **E01 disposition:** `SUPPORTED_IN_NARROW_DOMAIN`.
- **Exact evidence:**
  - model update and softmax pathway in `src/gifted_masking/models/m0.py`,
    `src/gifted_masking/models/m2.py`, and `src/gifted_masking/core.py`;
  - `results/summaries/m2_learner_parameter_sensitivity.csv`, selectors
    `p=0.75`, `eta=0`, and `learner_case in
    {low_tau,default,high_tau}`;
  - primary units `results/raw/frontiers_hot_stove_v1_units.csv`, selectors
    `tier=standard`, `p in {0.75,0.85}`, `lambda=1`, five master seeds, and
    `condition in {controlled_baseline,forced_authentic_0.05,
    counterfactual_authentic_feedback}`;
  - `results/summaries/frontiers_hot_stove_v1_effects.csv`, selector
    `level=across_master_seeds`:
    - pooled `rejected_minus_accepted_post_initial_authentic_rate` =
      `-0.025837`, 95% Student-t interval `[-0.035753,-0.015922]`;
    - pooled `rejected_minus_accepted_normalized_regret` = `0.025824`, interval
      `[0.015914,0.035735]`;
    - pooled `rejected_minus_accepted_final_mask_rate` = `-0.000343`, interval
      `[-0.011605,0.010918]`;
    - pooled forced-exploration reductions after rejection: final masking
      `0.046590` `[0.033230,0.059951]`, normalized regret `0.057954`
      `[0.045614,0.070293]`;
    - pooled counterfactual-feedback reductions after rejection: final masking
      `0.118135` `[0.109683,0.126587]`, normalized regret `0.141318`
      `[0.132369,0.150267]`;
  - reproducibility metadata `results/manifests/frontiers_hot_stove_v1.json`
    and execution report `results/reports/frontiers_hot_stove_v1_report.md`.
- **Source locations:** `LITERATURE_REVIEW_CHAPTER.md` lines 49-57;
  `RESULTS_BY_FINDING_CHAPTER.md` lines 23-29;
  `DISCUSSION_CHAPTER.md` lines 17-25.
- **Current DOCX locations:** P9, P12, P14, P48, P58, P63, P74, P77.
- **Decision-rule result:** early rejection reduced later authentic sampling in
  five of five seeds at both primary p values, but the required final-masking
  effect failed at `p=.85` and its pooled interval included zero. Both
  information-restoring interventions reduced masking and regret with intervals
  excluding zero. Forced exploration reduced pooled rejection-stratum masking
  by `10.8%` and normalized regret by `13.0%`; counterfactual feedback reduced
  them by `27.4%` and `31.8%`, respectively, satisfying materiality.
- **Maximum current wording:** “In the tested M0 domain (`p=.75` and `.85`), an
  initial rejection reduced later authentic sampling and increased normalized
  regret but did not measurably increase final-window masking. Restoring
  information through forced authentic exploration or counterfactual feedback
  reduced both final masking and regret after rejection. This supports an
  information-restriction mechanism for sampling and regret in this domain,
  not the stronger claim that one early rejection caused persistent masking.”
- **Boundary:** do not call the full direct hot-stove persistence hypothesis
  supported and do not omit the null final-window masking result.

### C3 — Negative-outcome weighting

- **Intended outcome:** greater weighting of realized negative outcomes
  increases learned avoidance without changing objective environmental payoff.
- **Current evidence class:** computationally demonstrated and replicated
  across five independent master seeds in the maintained M0 contrast.
- **E01 disposition:** `SUPPORTED_IN_NARROW_DOMAIN`; the maintained avoidance
  contrast replicated, but greater negative-outcome weighting did not amplify
  the controlled early-rejection gap.
- **Exact evidence:**
  - `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`, row
    `effect=higher_loss_aversion_increases_masking`;
  - primary units `results/raw/robustness_full_units.csv`, selector
    `headline_effect_name=higher_loss_aversion_increases_masking`;
  - generator `src/gifted_masking/experiments/robustness.py`, conditions
    `lam_0.50` and `lam_2.50` at `p=0.65`;
  - invariant coverage in `tests/test_core.py` and `tests/test_m0.py`;
  - current display
    `doc-reviews/frontiers_submission/figures/Figure_1_directional_contrasts.tif`.
  - E01 standard primary units `results/raw/frontiers_hot_stove_v1_units.csv`,
    selector `condition=maintained_baseline`, `p=.65`,
    `lambda in {.5,2.5}`, and five master seeds;
  - E01 effects `results/summaries/frontiers_hot_stove_v1_effects.csv`,
    selector `level=across_master_seeds` and
    `effect_name=maintained_p_0.65_lambda_2.5_minus_0.5_final_mask_rate`:
    `0.402990`, 95% Student-t interval `[0.395366,0.410614]`;
  - same file, selector
    `effect_name=controlled_early_rejection_gap_in_gap_high_minus_low_lambda`:
    `-0.001067`, interval `[-0.015031,0.012898]`.
- **Source locations:** `RESULTS_BY_FINDING_CHAPTER.md` line 19;
  `DISCUSSION_CHAPTER.md` lines 27-35.
- **Current DOCX locations:** P19, P43, P58, P70; Figure 1 legend P106;
  Table 3 row M0 negative weighting.
- **Evidence still required:** no further E01 run. Broader generalization beyond
  the tested `p=.65`, learner settings, and five master seeds requires a
  separately approved sensitivity design.
- **Maximum current wording:** “Across five independent master seeds at
  `p=.65`, increasing negative-outcome weighting from 0.50 to 2.50 increased
  final-window masking by 0.403 (95% Student-t interval 0.395 to 0.411) without
  changing objective payoffs. It did not measurably amplify the masking gap
  caused by the controlled initial outcome.”
- **Boundary:** do not map `lambda` to a stable human trait or call it objective
  rejection severity.

### C4 — Graded disclosure

- **Intended outcome:** graded disclosure supplies lower-exposure sampling and
  can preserve exploration relative to a binary action space.
- **Current evidence class:** analytically benchmarked and computationally
  demonstrated across five independent master seeds for preservation of
  nonzero-disclosure exploration in the narrow frozen E02 domain. The same
  experiment shows action-space dilution rather than improved full-authentic
  endpoint discovery or pooled regret.
- **E02 disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for changing the exposure
  distribution of exploration only.
- **Exact evidence:**
  - `src/gifted_masking/models/m1.py` functions `disclosure_levels`,
    `acceptance_probability`, `expected_reward`, and `simulate`;
  - endpoint and monotonicity coverage in `tests/test_m1.py`;
  - `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`, row
    `effect=higher_receptivity_increases_disclosure`;
  - primary units `results/raw/robustness_full_units.csv`, selector
    `headline_effect_name=higher_receptivity_increases_disclosure`;
  - current display
    `doc-reviews/frontiers_submission/figures/Figure_1_directional_contrasts.tif`;
  - E02 primary units
    `results/raw/frontiers_m1_binary_graded_v1_units.csv`, selectors
    `tier=standard`, `initial_outcome=rejected`, `p in {.75,.85}`, the five
    reserved master seeds, and
    `architecture in {binary_endpoints,graded_independent_5}`;
  - E02 effects
    `results/summaries/frontiers_m1_binary_graded_v1_effects.csv`, selectors
    `level=across_master_seeds`, `stratum=rejected`, and
    `p=pooled_equal_weight_p_0.75_0.85`:
    - `graded_any_minus_binary_full_post_initial_rate` = `0.255040`, 95%
      Student-t interval `[0.253004,0.257077]`;
    - `graded_minus_binary_full_final_window_rate` = `-0.328692`, interval
      `[-0.342037,-0.315348]`;
    - `graded_minus_binary_optimal_endpoint_modal_probability` = `-0.221740`,
      interval `[-0.288755,-0.154724]`;
    - `binary_minus_graded_normalized_regret` = `-0.029761`, interval
      `[-0.033874,-0.025648]`;
  - reproducibility metadata
    `results/manifests/frontiers_m1_binary_graded_v1.json` and execution report
    `results/reports/frontiers_m1_binary_graded_v1_report.md`.
- **Source locations:** `LITERATURE_REVIEW_CHAPTER.md` lines 61-65;
  `MODEL_CASCADE_CHAPTER.md` lines 61-77;
  `RESULTS_BY_FINDING_CHAPTER.md` lines 33-39;
  `DISCUSSION_CHAPTER.md` lines 37-45.
- **Current DOCX locations:** P13-P14, P24, P45, P59, P64, P70, P74;
  Figure 1 legend P106; Table 1 row M1; Table 3 row M1.
- **Decision-rule result:** exploration effect 1 was positive in five of five
  seeds separately at both `p=.75` and `.85`, and its equal-p-weight interval
  excluded zero. Endpoint effects 3 and 4 were negative in all five seeds at
  both p values, and their pooled intervals were below zero. Regret effect 5
  was positive at `p=.75` but negative at `p=.85`; its prespecified pooled
  effect was negative in all five seeds with an interval below zero. The
  `p=.65` mask-optimal control was not a decision input and showed the same
  exploration/action-space-dilution pattern. Mean disclosure was not used for
  adjudication.
- **Evidence still required:** no further E02 run is required for the narrow
  disposition. Generalization beyond independent five-arm Q-values, the
  forced initial rejection, `p in {.75,.85}`, default learner settings, and
  `T=2000` requires separately approved levels, temperature, or horizon
  sensitivity; such sensitivity was not run here.
- **Maximum current wording:** “In the tested forced-initial M0/M1 comparison
  at `p=.75` and `.85`, independent graded actions increased post-rejection
  nonzero disclosure relative to binary full-authentic resampling by 0.255
  (95% Student-t interval 0.253 to 0.257). They did not improve discovery of
  the objectively optimal full-authentic endpoint or pooled normalized regret;
  instead, the additional arms diluted endpoint sampling.”
- **Boundary:** describe E02 as changing or preserving the exposure
  distribution of exploration, not as improving endpoint discovery, regret,
  protective ladder climbing, or smooth generalization. Intermediate
  disclosure is not generally the static optimum, the independent Q-values do
  not share experience, and the `p=.65` control cannot support an
  authenticity-optimal claim.

### C5 — M2 learned suboptimal-masking regime

- **Intended outcome:** learned behavior can remain masking even when value
  iteration selects authenticity in the same MDP.
- **Current evidence class:** analytically benchmarked and computationally
  demonstrated across five independent master seeds for the frozen default M2
  learner and tested grid; parameter-general robustness is not established.
- **E03 disposition:** `SUPPORTED_IN_NARROW_DOMAIN`.
- **Exact evidence:** C1 artifacts plus
  `results/summaries/m2_regime_refined_thresholds.csv`, all rows;
  `results/summaries/m2_learner_parameter_sensitivity.csv`, especially
  `region=learned_suboptimal_lock_in`; and
  `results/summaries/m2_optimal_regime_sensitivity.csv`, selector
  `optimal_lock_in_width>0`; and the E03 selectors below:
  - `results/summaries/frontiers_m2_regime_replication_v1_stable_cells.csv`,
    `stable=True` and `classification=learned_suboptimal_masking` (243/357);
  - `results/summaries/frontiers_m2_regime_replication_v1_cells.csv`,
    `component=sentinels`, the five dynamic-authenticity sentinels, and
    `sensitivity_name in {baseline,n,T,final_window_fraction}`: all 150
    seed-by-sentinel-by-case records are `learned_suboptimal_masking`;
  - the same cells file with `component=sentinels`,
    `sensitivity_name=gamma`, and `gamma=.5`: three sentinels are instead
    `learner_matches_objective` in all five seeds because objective value
    iteration selects masking while the learned action remains masking;
  - the same cells file with `component=harsh`,
    `sensitivity_name=b2_r2_delta`, `b2=0`, `r2=8`, `delta=.3`, `eta=0`, and
    `p=.75`: all five seeds satisfy static M0 authenticity, objective M2
    masking, and `classification=optimal_policy_masking`; and
  - `results/summaries/frontiers_m2_regime_replication_v1_thresholds.csv`,
    all six rows.
- **Source locations:** `MODEL_CASCADE_CHAPTER.md` lines 81-91;
  `RESULTS_BY_FINDING_CHAPTER.md` lines 21-31;
  `DISCUSSION_CHAPTER.md` lines 19-35.
- **Current DOCX locations:** P26-P27, P47-P48, P57-P58, P71, P77;
  Figure 2 legend P107.
- **Decision-rule result:** passed `243>=179`, the lower seed-level interval
  bound was `0.680672>0.40`, and all five dynamic-authenticity sentinels were
  stable across `n=320`, `T in {2000,5000}`, and final-window fractions
  `{.1,.4}`. Seven low-`p`, `eta=0` cells were not stable because of inadequate
  neutral visits; no objective or learned-action tie was forced into a class.
  The `gamma=.5` alternate changed three sentinel classifications and therefore
  requires learner qualification. Objective thresholds were bracketed at
  `[.383911,.383972]` for `eta=0`, `[.338745,.338806]` for `eta=.2`, and
  `[.268982,.269043]` for `eta=.8`. Learned transition locations were not
  estimated: `eta=0` was censored by inconclusive low-`p` cells and `eta=.2/.8`
  had no observed crossing.
- **Evidence still required:** no further E03 run for the narrow disposition.
  Any broad learner-parameter claim or learned-threshold estimate requires a
  new approved experiment; the censored threshold rows cannot be extrapolated.
- **Maximum current wording:** “For the frozen default M2 learner and tested
  grid, learned suboptimal masking formed a seed-stable regime in 243 of 357
  cells and survived the prespecified population-size, horizon, and final-
  window checks. The classification was learner-parameter dependent. Under the
  separately labeled harsh `b2=0`, `r2=8`, `delta=.3` boundary, objective M2
  masking despite static M0 authenticity occurred at the tested `p=.75` cell.”
- **Boundary:** reserve “structural lock-in” for cells where the optimal M2
  policy masks while static M0 favors authenticity; do not apply it to the
  243-cell default-learner failure regime. Do not report a learned transition
  threshold from the censored refinement rows, and do not generalize the harsh
  three-point sentinel into a broad parameter-space width.

### C6 — Context-search burden

- **Intended outcome:** increasing contexts burdens discovery when the action
  representation preserves context-specific search; context count alone is not
  sufficient.
- **Current evidence class:** computationally demonstrated across five
  independent master seeds for the frozen E04 baseline, with full K curves,
  action-space controls, randomized receptive-context identity, and
  multiple-good-context variants (137,500 primary learner rows).
- **E04 disposition:** `SUPPORTED_IN_NARROW_DOMAIN`.
- **Exact evidence:**
  - `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`,
    rows `flat_2k_k1_vs_k8_settling_gap`,
    `hierarchical_k1_vs_k8_settling_gap`,
    `global_mask_k1_vs_k8_settling_gap`, and
    `fixed_good_pond_k1_vs_k8_settling_gap`;
  - primary units `results/raw/robustness_full_units.csv`, same effect selectors;
  - generator `src/gifted_masking/experiments/robustness.py`, M3 ablation block;
  - current display
    `doc-reviews/frontiers_submission/figures/Figure_3_m3_action_space_ablations.tif`;
  - E04 primary units
    `results/raw/frontiers_m3_search_architectures_v1_units.csv`, selectors
    `tier=standard`, `component=primary`, `sensitivity_name=baseline`, the five
    master seeds `2026081401` through `2026081405`, and the requested
    architecture/identity/good-count cell;
  - E04 curves
    `results/summaries/frontiers_m3_search_architectures_v1_curves.csv`, all
    275 seed-by-canonical-cell rows;
  - E04 effects
    `results/summaries/frontiers_m3_search_architectures_v1_effects.csv`,
    selector `level=across_master_seeds`, especially:
    - `flat_2k_mean_settled_any_good_auth_argmax_slope_log2K_fixed_one` =
      `-0.058240`, 95% Student-t interval `[-0.063915,-0.052565]`, and
      `flat_2k_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one` =
      `-0.234000` `[-0.246417,-0.221583]`;
    - `hierarchical_mean_settled_any_good_auth_argmax_slope_log2K_fixed_one` =
      `-0.114760` `[-0.124541,-0.104979]`, and
      `hierarchical_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one` =
      `-0.470400` `[-0.511031,-0.429769]`;
    - `flat_2k_minus_global_mask_mean_settled_any_good_auth_argmax_slope_contrast`
      = `-0.059960` `[-0.065503,-0.054417]` and the corresponding
      hierarchical contrast = `-0.116480` `[-0.126124,-0.106836]`;
    - `global_mask_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one` =
      `0.008800` `[0.002090,0.015510]` and
      `fixed_known_good_mean_settled_any_good_auth_argmax_structural_K_effect`
      = `0` `[0,0]`, both inside the prespecified practical-equivalence band;
    - randomized-minus-fixed, two-minus-one, and proportional-25-minus-one
      slope effects for flat and hierarchical architectures;
  - canonicalization and aliases in
    `results/summaries/frontiers_m3_search_architectures_v1_canonical_cells.csv`
    (55 rows) and
    `results/summaries/frontiers_m3_search_architectures_v1_equivalences.csv`
    (120 rows); and
  - provenance and execution metadata in
    `results/manifests/frontiers_m3_search_architectures_v1.json` and
    `results/reports/frontiers_m3_search_architectures_v1_report.md`.
- **Source locations:** `LITERATURE_REVIEW_CHAPTER.md` lines 69-71;
  `MODEL_CASCADE_CHAPTER.md` lines 95-103;
  `RESULTS_BY_FINDING_CHAPTER.md` lines 41-47;
  `DISCUSSION_CHAPTER.md` lines 47-55.
- **Current DOCX locations:** P13-P14, P29-P30, P50, P60, P65, P72, P74,
  P77; Figure 3 legend P108; Table 1 row M3.
- **Decision-rule result:** flat and hierarchical fixed-one slopes were
  negative in five of five seeds, and both architecture-by-K slope-contrast
  intervals excluded zero. The global-mask K=16-minus-K=1 change was `0.0088`
  with its interval wholly inside `[-.10,.10]`; the K-invariant known-good
  control was structurally zero. Using the equivalent canonical K=1 cell,
  randomized identity retained K=16-minus-K=1 declines of `-0.2400`
  `[-0.2571,-0.2229]` for flat 2K and `-0.4596`
  `[-0.4683,-0.4509]` for hierarchical. Two good contexts attenuated the
  K=2--16 slopes from `-0.07144` to `-0.02080` for flat and from `-0.09776`
  to `-0.07252` for hierarchical. Under proportional-25 receptive contexts,
  slopes were near zero: `0.00220` `[-0.00099,0.00539]` and `-0.00252`
  `[-0.00792,0.00288]`, respectively.
- **Evidence still required:** no further E04 run is required for this narrow
  baseline disposition. Generalization beyond `p_good=.85`, `p_bad=.20`,
  `bf=0`, the default learner, `n=500`, `T=2000`, K through 16, and the tested
  good-context regimes requires separately authorized sensitivity evidence;
  the staged p/tau sensitivity was not executed.
- **Maximum current wording:** “In the frozen M3 baseline, increasing K reduced
  final-window settling on a receptive-context authenticity action in both the
  flat 2K and hierarchical search representations, while global-mask and
  known-good controls remained practically equivalent across K. The decline
  survived randomized receptive-context identity but weakened with two good
  contexts and was near zero when 25% of contexts were receptive. Thus the
  tested effect reflects representation-dependent search burden under scarce
  receptivity, not context count alone.”
- **Boundary:** do not generalize to arbitrary social variety, receptivity
  distributions, learner parameters, K beyond 16, or human settings. Do not
  claim that more contexts are inherently harmful; the proportional-good and
  action-space controls show that receptive-context scarcity and representation
  determine the effect.

### C7 — Comparison cost and learned premature retreat

- **Intended outcome:** comparison cost can remove the objective advantage of
  authenticity in a receptive context, while a reinforcement learner may
  retreat from that action before objective indifference.
- **E05 disposition:** `SUPPORTED_IN_NARROW_DOMAIN` for the frozen K=4,
  fixed-good-context, default-learner flat-2K representation. The hierarchical
  representation did not yield an estimable learned crossing and therefore
  does not broaden this disposition.
- **Current evidence class:** exact analytic crossover plus a five-seed dense
  learned-response sweep with prespecified PAVA, paired Student-t shape checks,
  and architecture-isolated master-seed bootstrap uncertainty.
- **Exact evidence:**
  - analytic implementation and tests in `src/gifted_masking/models/m3.py` and
    `tests/test_m3.py`;
  - 90,000 primary child rows in
    `results/raw/frontiers_m3_bflpe_crossover_v1_units.csv`;
  - 18 analytic, 180 cell, 1,548 effect, and 12 transition rows in the
    corresponding `frontiers_m3_bflpe_crossover_v1` summary tables;
  - exact configuration, authorization, hashes, three-block deterministic
    reproduction, and verification evidence in
    `results/manifests/frontiers_m3_bflpe_crossover_v1.json`; and
  - the 13-item checkpoint in
    `results/reports/frontiers_m3_bflpe_crossover_v1_report.md`.
- **Source locations:** `LITERATURE_REVIEW_CHAPTER.md` lines 73-77;
  `MODEL_CASCADE_CHAPTER.md` line 99;
  `RESULTS_BY_FINDING_CHAPTER.md` lines 49-53;
  `DISCUSSION_CHAPTER.md` lines 57-65.
- **Current DOCX locations:** P29, P41, P52, P61, P66; Figure 1 legend P106;
  Table 3 row M3 comparison cost.
- **Decision-rule result:** the objective advantage is `0.40 - 0.85*bf`, with
  exact analytic crossover `8/17 = 0.4705882353`. In flat 2K, all five seed
  PAVA transitions were valid inside `(.30,.65)`; the pooled learned crossing
  was `0.312852` with 10,000/10,000 valid bootstrap crossings and 95% interval
  `[0.307836,0.316918]`. There were zero material upward adjacent violations.
  The flat endpoint change from `bf=0` to `.80` was `-0.9400`
  `[-0.957993,-0.922007]`. Hierarchical response was already below `.5` at the
  lower dense boundary, with 0/5 valid seed crossings and 0/10,000 valid
  bootstrap crossings; its endpoint change was `-0.6932`
  `[-0.732488,-0.653912]`.
- **Paired analytic--simulation meaning:** the flat learned crossing preceded
  the objective crossover by `0.157736`. At `bf=0.312852`, the analytic
  objective advantage of receptive-context authenticity was still
  approximately `0.134`, about one-third of its `bf=0` value. The main E05
  finding is therefore not merely that sufficiently large cost can reverse
  objective value; it is that the tested learner retreated while authenticity
  remained objectively preferable.
- **Evidence still required:** no further run is required for this narrow flat
  2K disposition. Generalization across K, good-context identity/count,
  receptivity, learner parameters, horizons, or other action representations
  requires separate authorization and evidence. `T=5000` was not run.
- **Maximum current wording:** “In the frozen K=4 flat-2K M3 representation,
  increasing comparison cost reduced final-window selection of receptive-
  context authenticity. The learned `.5` response crossing occurred at
  `bf=0.313` (95% master-seed bootstrap interval `0.308–0.317`), substantially
  before the exact objective payoff crossover at `8/17 = 0.471`; at the
  learned crossing, authenticity still retained an objective advantage of
  approximately `0.134`. The tested hierarchical response was already below
  `.5` at the dense-range lower boundary, so no hierarchical learned crossing
  was estimable.”
- **Boundary:** do not equate the analytic crossover with the learned behavioral
  transition, generalize the flat-2K crossing to hierarchical or other action
  representations, or calibrate `bf` to human academic self-concept. This is a
  model-specific action-selection result, not a human threshold or prevalence
  estimate.
- **Canonical preservation record:** `E05_MAIN_RESULTS.md`. Later manuscript
  revisions may shorten this finding but must preserve the separation and
  ordering of the analytic and learned crossovers.

### C8 — Endogenous receptivity and path dependence

- **Intended outcome:** behavior-dependent receptivity makes masking
  self-reinforcing and can retain path history.
- **Current evidence class:** feedback is established by model construction;
  schedule-specific path dependence is computationally observed once.
- **Exact evidence:**
  - `src/gifted_masking/models/m4.py` functions `simulate` and
    `hysteresis_experiment`, with bounds/order coverage in `tests/test_m4.py`;
  - `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`, row
    `effect=higher_entrenchment_increases_masking`;
  - `results/summaries/robustness_full_recomputed_effects.csv`, rows
    `mask_path_gap` and `receptivity_path_gap`;
  - primary units `results/raw/robustness_full_units.csv`, selectors
    `headline_effect_name in {higher_entrenchment_increases_masking,
    mask_path_gap,receptivity_path_gap}`;
  - current display
    `doc-reviews/frontiers_submission/figures/Figure_4_m4_ramp_paths.tif`.
- **Source locations:** `LITERATURE_REVIEW_CHAPTER.md` lines 81-85;
  `MODEL_CASCADE_CHAPTER.md` lines 107-133;
  `RESULTS_BY_FINDING_CHAPTER.md` lines 55-61;
  `DISCUSSION_CHAPTER.md` lines 67-75.
- **Current DOCX locations:** P13-P14, P31-P33, P54, P61, P72, P74, P77;
  Figure 4 legend P109; Table 1 row M4.
- **Evidence still required:** E06 independent ramps, speed/horizon
  sensitivity, loop area, transition thresholds, and cold-start controls.
- **Maximum current wording:** “M4 produced self-reinforcing feedback and
  schedule-specific path dependence under the maintained continuation ramp.”
- **Boundary:** do not use “irreversible,” “entrenched state,” or “hysteresis”
  as an established result.

### C9 — Hysteresis

- **Status:** excluded.
- **Current evidence:** no replicated threshold separation, speed robustness,
  or stochastic-control result. The two path-gap rows and Figure 4 demonstrate
  one continuation schedule only.
- **Current DOCX locations:** P33, P54, P72, and Figure 4 legend P109 correctly
  limit the result to path dependence; any stronger wording elsewhere must be
  revised at Stage 6-8 audit.
- **Restoration gate:** E06 must pass every hysteresis decision rule before C9
  can be reconsidered.
- **Permitted wording:** “schedule-specific path dependence.”

### C10 — Human prevalence or intervention effects

- **Status:** excluded.
- **Current evidence:** no human calibration, participant data, causal
  intervention, psychometric mapping, or prevalence design exists.
- **Source locations:** `LITERATURE_REVIEW_CHAPTER.md` lines 5, 25, 37, 77,
  85, and 89-95; `DISCUSSION_CHAPTER.md` lines 85-111.
- **Current DOCX locations:** P17, P38, P63-P75, P77, P79-P89.
- **Permitted wording:** educational implications are testable hypotheses.
- **Restoration gate:** none within this article; supporting C10 would require a
  separate empirical research program and a new RDS.

## Stage 1 reconciliation decisions

1. **Uncertainty source.** The manuscript uses
   `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`,
   which resamples the two independently seeded conditions separately with
   bootstrap seed 90517. Do not substitute the intervals in
   `results/summaries/robustness_full_headline_uncertainty.csv`; those rows use
   administrative child-index matching across different RNG streams. Point
   estimates agree, but the inferential unit and intervals differ.
2. **Two M3 flat estimates.** The original flat comparison is 0.200
   (`more_contexts_reduce_settling_in_good_pond`, seeds 19/20). The dedicated
   four-architecture ablation reports 0.168 for flat 2K (seeds 301/308). Both
   are valid maintained runs and must be labeled by run rather than merged.
3. **M2 denominator.** `226/357` is a cell count in the specified 21 by 17
   grid. It is never a learner fraction or human prevalence estimate.
4. **M1 boundary.** The 0.569 result is a receptivity contrast within M1, not a
   binary-versus-graded treatment effect. Current DOCX P45, P59, and P77 must be
   narrowed or supported by E02 before finalization.
5. **Hot-stove boundary.** Exploration sensitivity supports the proposed
   information-restriction mechanism but does not replace early-outcome and
   information-restoration tests. Current DOCX P9, P58, and P77 require E01 or
   narrower wording.
6. **M4 boundary.** The maintained ramp uses one seed sequence and serially
   dependent continuation points. It supports path dependence, not hysteresis.
7. **Figure provenance.** No checked-in deterministic article-specific script
   was found for the four current TIFFs or the two manuscript-specific CSVs.
   They remain evidence displays, not final reproducible publication figures.
   Stage 5 must add source-data exports and regeneration commands.

## Frozen terminology

| Use | Definition | Avoid |
| --- | --- | --- |
| masking | the modeled safer, lower-visibility action | diagnosis, trait, or all privacy behavior |
| authenticity | the modeled higher-visibility action | moral ideal or universal desired endpoint |
| disclosure level | M1 action `d` in `[0,1]` | ladder climbing unless transfer is modeled |
| receptivity | acceptance probability `p`, or endogenous `p_t` in M4 | observed classroom climate without measurement |
| negative-outcome weighting | `lambda` applied only to realized negative learning signals | objective rejection penalty or calibrated trait |
| persistent | dominant over the stated final window and horizon | absorbing, permanent, or irreversible |
| learned suboptimal masking | learned neutral action masks while value iteration favors authenticity | structural lock-in |
| optimal-policy masking | value iteration favors masking under the specified MDP | learner failure |
| context | one M3 choice setting; “good context” means the modeled receptive setting | “pond” in final prose except when naming BFLPE |
| path dependence | matched current parameter yields different outcomes after different continuation histories | hysteresis without E06 |
| Monte Carlo interval | uncertainty for a declared synthetic resampling unit | human-population confidence interval |

## Stage 1 completion check

- [x] Every intended claim names exact result rows, scripts or missing scripts,
  displays, source locations, and current manuscript paragraphs.
- [x] Primary, secondary, and excluded claims are frozen.
- [x] Maximum current wording and stronger-wording gates are explicit.
- [x] Every evidence gap maps to a Stage 2 experiment specification.
- [x] Numerical and terminology discrepancies are reconciled above.
