# Second-Pass Robustness Audit

## Scope

This audit covers the maintained implementation under `src/gifted_masking`.
The legacy directories `simulations1`, `simulations2`, and `simulations3` are
preserved reference artifacts and were not treated as the maintained code path.

The revised evidentiary standard is:

- M3 may be described as evidence for search burden, not generic context
  multiplicity harm.
- M4 may be described as path dependence under the tested schedule, not true
  hysteresis.
- M2 structural-lock-in claims require comparison to an optimal MDP policy.

## Canonical Verification Record

| Field | Value |
| ----- | ----- |
| Command | `./scripts/verify.sh` |
| Working directory | `/Users/omer/workspace/test-code/gifted-masking` |
| Environment | repo-local `.venv` through `scripts/verify.sh` |
| Exit code | `0` on escalated rerun |
| Test count | `34` |
| Runtime | `6.691s` wall time from `time ./scripts/verify.sh` |
| Generated artifacts | `results/raw/robustness_full.csv`, `results/summaries/robustness_full_summary.csv`, `results/reports/robustness_full_report.md`, `results/manifests/robustness_full.json` |
| Warnings | none reported by the successful run |
| Skipped tests | none |
| Failures | none in successful run |

The first non-escalated run passed all tests but failed while writing
`results/raw/robustness_full.csv` due to sandbox permission denial. That was an
execution-environment write restriction, not a code or test failure. The same
canonical command passed once write access to the results directory was allowed.

## Maintained Package Inventory

| Module | Purpose | Public functions/classes | Tests covering it | RNG use | Outputs | Remaining risk |
| ------ | ------- | ------------------------ | ----------------- | ------- | ------- | -------------- |
| `src/gifted_masking/core.py` | Shared numerics, final-window sizing, softmax, loss-aversion transform, uncertainty helpers | `make_rng`, `final_window_size`, `subjective_value`, `softmax_probabilities`, `softmax_sample`, `standard_error`, `bootstrap_ci`, `EstimateSummary`, `summarize_mean` | `tests/test_core.py`, `tests/test_determinism.py`, robustness tests indirectly | Accepts explicit `np.random.Generator`; bootstrap uses seeded generator | No files; returns arrays and summaries | Bootstrap unit is only as good as the array supplied by callers; no independent seed hierarchy object exists |
| `src/gifted_masking/params.py` | Lightweight parameter dataclasses and validation | `AgentParams`, `RunParams`, `DEFAULT_PAYOFFS` | Not directly tested | None | No files | Dataclasses are not yet used consistently by model kernels or manifests |
| `src/gifted_masking/models/m0.py` | M0 two-arm masking/authenticity bandit and analytic rewards | `expected_rewards`, `expected_gap`, `objective_indifference_r`, `subjective_indifference_r`, `simulate` | `tests/test_m0.py`, `tests/test_determinism.py`, robustness smoke suite | Local `default_rng(seed)` per simulation | Per-child final-window mask-rate array | Subjective indifference formula is exposed without guarding the region where rejected reward is negative |
| `src/gifted_masking/models/m1.py` | Graded-disclosure action space with independent Q-values per disclosure level | `disclosure_levels`, `acceptance_probability`, `expected_reward`, `simulate` | `tests/test_m1.py`, `tests/test_determinism.py`, robustness smoke suite | Local `default_rng(seed)` per simulation | Per-child final-window mean disclosure array | No smooth generalization model exists; intermediate disclosure should not be described as statically optimal under the linear payoff |
| `src/gifted_masking/models/m2.py` | Three-state stigma MDP with Q-learning | `transition_step`, `simulate`, state constants | `tests/test_m2.py`, `tests/test_determinism.py`, robustness smoke suite | Local `default_rng(seed)` per simulation; separate random draws for outcome, turnover, escape | Per-child final-window mask-rate array | No value-iteration or regret benchmark; cannot support optimal-learner trap or suboptimal structural-lock-in claims |
| `src/gifted_masking/models/m3.py` | Peer-group search model and ablation variants | `group_probabilities`, `decode_action`, `expected_reward_for_action`, `simulate`, `simulate_hierarchical`, `simulate_global_mask`, `simulate_fixed_good_pond` | `tests/test_m3.py`, `tests/test_determinism.py`, M3 ablation suite | Local `default_rng(seed)` per simulation | Per-child settling indicator, mask rate, modal action | No random good-pond identity per child and no multiple-good-pond variant yet |
| `src/gifted_masking/models/m4.py` | Endogenous receptivity bandit and ramp-up/ramp-down path experiment | `update_receptivity`, `simulate`, `simulate_from_state`, `hysteresis_experiment` | `tests/test_m4.py`, `tests/test_determinism.py`, M4 path suite | Local `default_rng(seed)` per segment; Q and `p_t` carried across ramp segments | Per-child mask rate, final `p_t`, optional trajectories, ramp summaries | Current diagnostics support path dependence only; no loop area, threshold separation, ramp-speed sensitivity, or seed replication |
| `src/gifted_masking/experiments/robustness.py` | Robustness suites, summary rows, CSV/report/manifest writing | `CheckResult`, `run_smoke_suite`, `run_m3_ablation_suite`, `run_m4_hysteresis_suite`, `write_suite` | `tests/test_robustness.py` | Uses fixed seeds per comparison and bootstrap seeds for CIs | CSV raw/summary, markdown report, manifest JSON | File named `raw` contains summary-level rows rather than per-child/per-cell observations; manifest omits full parameter grid and seed hierarchy |
| `src/gifted_masking/plotting/legacy_figures.py` | Maintained figure generation with lazy plotting imports | `generate_all`, `fig_m0`, `fig_m1`, `fig_m2`, `fig_m3`, `fig_m0_bistability`, `fig_m3_bflpe`, `fig_m4`, `fig_m0_by_risk`, `fig_downstream_by_risk` | Not directly covered except importability through package tests | Calls model simulations with fixed seeds | PNG figures under requested output directory | Plotting remains coupled to data generation at figure-call time; no saved intermediate data tables for figures |
| `src/gifted_masking/repro.py` | Environment snapshot, manifest, JSON and CSV writing | `git_commit_hash`, `environment_snapshot`, `ensure_results_dirs`, `write_json`, `write_csv`, `build_manifest` | `tests/test_robustness.py` indirectly | None | Manifest JSON and CSV files | Manifest is too shallow for publication-grade reproducibility |
| `src/gifted_masking/cli.py` | CLI for robustness and legacy figures | `build_parser`, `main` | Robustness path covered indirectly | Delegates to suites and plotting functions | Results or figures depending on command | No direct CLI parser tests |

Separation status: model kernels, plotting, experiment orchestration, and
reproducibility helpers are separated at module level. The remaining coupling is
that plotting functions still run simulations directly instead of loading frozen
data artifacts.

## Artifact Completeness Audit

Files inspected:

- `results/manifests/robustness_full.json`
- `results/raw/robustness_full.csv`
- `results/summaries/robustness_full_summary.csv`
- `results/reports/robustness_full_report.md`
- `CURRENT_STATE.md`

| Manifest field | Present? | Value / location | Severity if missing |
| -------------- | -------- | ---------------- | ------------------- |
| Git commit hash or explicit unavailable marker | Partial | `environment.git_commit: null`; `CURRENT_STATE.md` states repo is not a git repo | Major, partly mitigated by explicit current-state note |
| Python version | Yes | `environment.python_version` | n/a |
| Package versions | Partial | `numpy_version`, `matplotlib_version`; no package lockfile or installed-package snapshot | Major |
| Command used | Yes | `command: python -m gifted_masking.cli robustness` | n/a |
| Working directory | Yes | `cwd` | n/a |
| Master seed | No | Not recorded | Blocker |
| Seed hierarchy | No | Fixed seeds exist in `robustness.py`, but are not serialized | Blocker |
| Independent RNG streams by parameter cell or child | No | Code uses local generators, but manifest does not describe stream hierarchy | Blocker |
| Parameter grids | No | Only suite and check count recorded | Blocker |
| n per cell | No | Present in code calls, absent from manifest | Major |
| T / horizon | No | Present in code calls, absent from manifest | Major |
| Final-window fraction | No | Defaults in model signatures, absent from manifest | Major |
| Start timestamp | Yes | `timestamps.started_at` | n/a |
| End timestamp | Yes | `timestamps.finished_at` | n/a |
| Artifact paths | Yes | `output_paths` | n/a |
| Code hash or config hash | No | Not present | Major |
| Verification status | No | Not present in manifest; available only from command output | Moderate |
| Environment information | Partial | Python/platform/NumPy/matplotlib present; no full dependency set | Major |

Main finding: artifact paths and basic environment metadata exist, but the
manifest is not yet sufficient to reproduce a robustness run without reading
source code.

## Headline Outcome Recompute

Tolerance: report and `CURRENT_STATE.md` values are rounded to four decimals, so
comparisons to those documents use absolute tolerance `0.00005` after rounding.
Comparisons between raw and summary CSV rows use exact numeric equality as
serialized estimates.

Important limitation: `results/raw/robustness_full.csv` is not raw per-child,
per-seed, or per-cell data. It is a summary-level table with one row per check.
Therefore the headline estimates can be re-read from the raw-labeled file and
cross-checked against summary/report/current-state documents, but independent
recomputation from primary simulation units is not possible from current
artifacts. This is a Major limitation for normal claims and a Blocker for
publication-grade headline claims.

| Claim | Reported value | Recomputed value | Absolute difference | Match? | Notes |
| ----- | -------------: | ---------------: | ------------------: | ------ | ----- |
| M0 higher-receptivity masking reduction | 0.7332 | 0.7331555556 | 0.0000444444 | yes | Matches rounded report/current-state value |
| M0 higher-loss-aversion masking increase | 0.4031 | 0.4031111111 | 0.0000111111 | yes | Matches rounded report/current-state value |
| M1 higher-receptivity disclosure increase | 0.5689 | 0.5689111111 | 0.0000111111 | yes | Matches rounded report/current-state value |
| M2 higher-stigma-escape masking reduction | 0.2007 | 0.2007291667 | 0.0000291667 | yes | Matches rounded report/current-state value |
| M3 flat 2K K=1 vs K=8 settling gap | 0.1682 | 0.1681818182 | 0.0000181818 | yes | Matches rounded report/current-state value |
| M3 hierarchical K=1 vs K=8 settling gap | 0.3773 | 0.3772727273 | 0.0000272727 | yes | Matches rounded report/current-state value |
| M3 global-mask K=1 vs K=8 settling gap | 0.0045 | 0.0045454545 | 0.0000454545 | yes | Matches rounded report value |
| M3 fixed-good-pond K=1 vs K=8 settling gap | -0.0045 | -0.0045454545 | 0.0000454545 | yes | Matches rounded report value |
| M4 mean mask-path gap | 0.0651 | 0.0651428571 | 0.0000428571 | yes | Matches rounded report/current-state value |
| M4 mean receptivity-path gap | -0.1061 | -0.1060646416 | 0.0000353584 | yes | Matches rounded report/current-state value |

## Uncertainty Intervals

The CSV files include `standard_error`, `ci_low`, and `ci_high`. The CI source is
`summarize_mean`, which bootstraps the arrays supplied by the robustness suite.
Because only summary rows are persisted, these intervals cannot be independently
recomputed from saved raw units.

| Effect | Estimate | 95% CI | Resampling unit | Number of units | Robust? |
| ------ | -------: | -----: | --------------- | --------------: | ------- |
| M0 receptivity effect | 0.7332 | [0.7196, 0.7444] | per-child paired-position difference array created in memory | 250 | yes |
| M0 loss-aversion effect | 0.4031 | [0.3861, 0.4199] | per-child paired-position difference array created in memory | 250 | yes |
| M1 disclosure effect | 0.5689 | [0.5567, 0.5824] | per-child paired-position difference array created in memory | 250 | yes |
| M2 escape-rate effect | 0.2007 | [0.1214, 0.2741] | per-child paired-position difference array created in memory | 200 | yes, with wider interval |
| M3 flat 2K K gap | 0.1682 | [0.1136, 0.2273] | per-child paired-position difference array created in memory | 220 | yes |
| M3 hierarchical K gap | 0.3773 | [0.3136, 0.4500] | per-child paired-position difference array created in memory | 220 | yes |
| M3 global-mask K gap | 0.0045 | [-0.0227, 0.0364] | per-child paired-position difference array created in memory | 220 | no directional K effect |
| M3 fixed-good-pond K gap | -0.0045 | [-0.0318, 0.0227] | per-child paired-position difference array created in memory | 220 | no directional K effect |
| M4 mask-path gap | 0.0651 | [0.0338, 0.0939] | matched ramp-grid values | 7 | partially supported; few units |
| M4 receptivity-path gap | -0.1061 | [-0.1334, -0.0736] | matched ramp-grid values | 7 | partially supported; few units |

## M0 Audit

M0 implements:

- `E[mask] = b - c`
- `E[auth] = p * (b + a) + (1 - p) * (a - r)`

The default sanity checks are covered by `tests/test_m0.py`: `E[mask] = 0.75`,
`E[auth]` at `p=0.5` equals `0.1`, and the objective threshold
`p* = 2.15 / 3` gives zero expected gap.

Other findings:

- `p=0` and `p=1` are implied by `expected_rewards` but should be explicitly
  tested.
- `lambda=1` baseline behavior is checked analytically for the subjective
  indifference curve, and learned directionality is smoke-tested.
- Loss aversion applies only through `subjective_value(reward, lam)` in the
  learning update; objective payoff variables are not rewritten.
- `softmax_probabilities` is numerically stable by subtracting row maxima and
  rejects nonpositive temperature.
- RNG determinism is tested for M0; independence is implemented through local
  generators but not documented in manifest form.

## M1 Audit

M1 implements:

- `acceptance_probability(d) = 1 - (1 - p) * d`
- `reward = a*d - c*(1-d) + b` when accepted
- `reward = a*d - c*(1-d) - r` when rejected
- `E(d) = b - c + d * [a + c - (1-p)*(b+r)]`

Endpoint tests confirm `d=0` equals masking and `d=1` equals full authenticity.
The disclosure grid includes exactly `0` and `1`, and acceptance probabilities
are range-checked.

Interpretation risk: the current implementation uses independent Q-values per
disclosure level. It supports lower-risk exploration across discrete disclosure
levels, not smooth generalization from small disclosures to larger disclosures.
The linear expected reward model also does not make intermediate disclosure
statically optimal except at indifference.

## M2 Audit

M2 transition order in `transition_step`:

- Reward is computed from the current state and action.
- Neutral authentic acceptance transitions to accepted; rejection transitions to
  stigmatized.
- Accepted state authentic action reliably pays `b + a`; masking pays `b - c`.
- Delta turnover is applied after current accepted-state reward and affects the
  next state.
- Stigmatized masking pays `b2 - c` and does not change state unless escape is
  drawn.
- Stigmatized authenticity redemption succeeds with probability `p / 2`; failure
  pays `a - r2`.
- Eta escape is applied after current stigmatized-state reward and affects the
  next state.

The implementation matches the stated transition mechanics. However, no value
iteration, policy iteration, or learned-policy regret benchmark exists. As a
result, M2 currently supports only cautious claims such as "higher stigma escape
reduces learned masking" and "sticky stigma constrains the environment." It does
not support "suboptimal structural lock-in" or "traps even optimal learners."

See `M2_OPTIMAL_BENCHMARK_PLAN.md`.

## M3 Search-Burden Audit

| Formulation | Action space | What search burden remains? | What is controlled away? | K gap |
| ----------- | ------------ | --------------------------- | ------------------------ | ----: |
| flat 2K | one arm per behavior-context pair | must discover both receptive group and authentic action in a larger flat arm set | nothing; this is the most burdensome maintained formulation | 0.1682 |
| hierarchical | choose group, then choose behavior within group | group search remains explicit, behavior learning is separated by group | some flat action-space competition is removed | 0.3773 |
| global-mask | one shared mask action plus K authentic-in-group actions | authentic group search remains, but masking is not duplicated across groups | duplicated masking arms are removed | 0.0045 |
| fixed-known-good-pond | two actions in known good group | search burden is removed | context discovery is removed | -0.0045 |

The maintained code includes:

- flat 2K formulation: yes
- hierarchical formulation: yes
- global-mask formulation: yes
- fixed-known-good-pond control: yes
- BFLPE sweep/check: partial; smoke comparison at `bf=0.0` vs `bf=0.8` exists
- random good-pond identity per child: no
- multiple-good-pond variant: no

Interpretation: flat 2K and hierarchical formulations show positive K gaps,
while global-mask and fixed-known-good-pond controls are near zero with CIs that
cross zero. The supported mechanism is search burden, not generic harm from
more contexts.

## BFLPE Audit

The analytic crossover is:

`bf* = [p_good*(b+a) + (1-p_good)*(a-r) - (b-c)] / p_good`

With defaults `p_good=0.85`, `b=1.0`, `a=0.6`, `r=2.0`, `c=0.25`, this gives
approximately `0.470588`.

Implementation status:

- In M3 reward simulation, `bf` is subtracted only from accepted authentic payoff
  in the good pond via `b + a - bf * (group == good_group)`.
- It is not applied to masking.
- It is not applied to bad ponds.
- The robustness suite compares behavior at `bf=0.0` and `bf=0.8`, but does not
  yet sweep around the analytic crossover with uncertainty.

The current evidence supports that a high BFLPE cost reduces modal good-pond
authenticity in the maintained smoke comparison. It does not yet establish the
behavioral crossover location or anticipatory-retreat threshold with precision.

## M4 Path Dependence Versus Hysteresis

| Evidence | Present? | Notes |
| -------- | -------- | ----- |
| Split trajectories from same start | partial | earlier `simulate(..., ntraj=...)` supports trajectory plotting, but full robustness artifact does not persist trajectories |
| Ramp-up/ramp-down path gap | yes | `hysteresis_experiment` ramps `km` up then down |
| Nonzero loop area | no | no loop-area calculation exists |
| Transition threshold separation | no | no threshold detection exists |
| Robust across ramp speeds | no | single segment horizon and ramp schedule |
| Robust across seeds | no | one seed sequence is used |
| Robust across parameter grids | no | one `p0`, one `ka/kr`, one grid |
| Confidence interval excludes zero | yes | current mask and receptivity path-gap CIs exclude zero, but unit count is seven ramp points |

Experiment details:

- Control parameter: `km`.
- Ramp schedule: `np.linspace(0.0, 0.003, 7)` upward, then the same values
  downward.
- Ramp speed: `horizon=500` per segment in the robustness suite.
- Learner Q-values are carried forward across ramp segments.
- Environment state `p_t` is carried forward across ramp segments.
- Seeds are advanced by segment offset, not reused.
- Multiple ramp speeds are not tested.
- Loop area and transition thresholds are not computed.

Acceptable wording: the ramp-up/ramp-down experiment shows path dependence under
the tested schedule. The evidence is consistent with hysteresis-like dynamics,
but current diagnostics do not establish true hysteresis.

## Overall Findings

| Severity | Finding |
| -------- | ------- |
| Blocker | Manifest lacks explicit seed hierarchy, parameter grid, and RNG stream strategy. |
| Blocker | Current `raw` artifact is summary-level, not per-child/per-seed raw data, so headline CIs cannot be independently recomputed from saved primary units. |
| Major | M2 lacks optimal-policy and regret benchmarking. |
| Major | M4 lacks loop-area, transition-threshold, ramp-speed, seed-replication, and parameter-grid diagnostics. |
| Major | M3 still lacks random-good-pond and multiple-good-pond variants. |
| Major | Package/version metadata is incomplete for publication-grade reproducibility. |
| Moderate | Plotting functions still generate data internally rather than consuming frozen result artifacts. |

## Audit Conclusion

The maintained package is modular and passes canonical verification. The current
artifacts support the revised M3 search-burden interpretation and a cautious M4
path-dependence interpretation. They do not support stronger claims about
generic context multiplicity harm, true hysteresis, or M2 optimal-learner traps.
