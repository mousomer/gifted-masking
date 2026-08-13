# Stage 2 Claim-Closing Experiment Specifications

## Scope and execution rule

This document converts every Stage 1 evidence gap into an executable,
decision-bearing Stage 2 experiment. It specifies analyses; it does not
authorize silent changes to M0-M4 semantics or defaults. Any intervention or
alternative action architecture must live behind an explicit experiment
configuration and must leave the maintained baseline path unchanged.

Stage 2 runs begin only after the smoke configuration for that experiment
passes review. Large or publication-tier sweeps are not part of routine
verification and require an explicit run decision after runtime measurement.

## Shared protocol

### Implementation contract

Create one configuration file per experiment under the planned path
`configs/frontiers_article/` and one orchestration module or script that calls
the maintained model kernels. The preferred planned command is:

```text
/Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli \
  article-experiment --config configs/frontiers_article/<experiment>.json
```

This command and config path do not exist at Stage 1; adding them is Stage 2
implementation work. Every new mode must be isolated behind the config and
named in the manifest. No existing default may change.

### Required outputs

Each run ID `<run_id>` must write:

```text
results/
  manifests/<run_id>.json
  raw/<run_id>_units.csv
  summaries/<run_id>_cells.csv
  summaries/<run_id>_effects.csv
  figures/<run_id>_<figure_name>.png
  reports/<run_id>_report.md
```

The manifest must record the exact command/config, git commit and dirty diff
hash, Python/OS/package versions, start/end time, parameter grid, `n`, `T`,
final-window fraction, master seeds, RNG stream derivation, bootstrap seed,
warnings, output hashes, and output paths. Raw rows must contain `run_id`,
experiment, architecture/intervention, master seed, cell seed, child ID or
seed, parameters, primary outcomes, and any experiment-specific trajectory
variables. Output ordering must be deterministic.

### Seed hierarchy and uncertainty

- Claim-closing standard runs use five independent master seeds. The first
  three are the RDS minimum; seeds four and five expose fragility before the
  manuscript is rewritten.
- Use `numpy.random.SeedSequence(master_seed).spawn(...)` or an equivalently
  recorded hierarchy to create independent streams by parameter cell, child,
  and stochastic component where component separation is required.
- A rerun with the same config and code must byte-match machine-readable
  artifacts after timestamps and runtime fields are normalized.
- Report seed-level estimates and a 95% interval across independent master-seed
  estimates. Child-level bootstrap intervals may also be reported, but cannot
  replace seed replication.
- Use independent-condition resampling unless an experimental design creates a
  genuine within-unit pairing through shared potential outcomes. Administrative
  child indices are not pairs.
- Report absolute effects first, relative effects second, and the denominator
  for every fraction.

### Compute tiers

| Tier | Purpose | Typical n/cell | Typical T | Master seeds | Run rule |
| --- | --- | ---: | ---: | ---: | --- |
| smoke | validate semantics, schema, RNG, and summaries | 64-128 | 200-500 | 1 | required before review |
| claim-closing standard | decide C1-C8 wording | 320-500 | 1,000-2,000 | 5 | Stage 2 default |
| publication sensitivity | boundary precision and long-horizon robustness | 1,000 | 5,000 | 10 | explicit approval after profiling |

Publication sensitivity is targeted or adaptive; it is not a Cartesian sweep
over every parameter listed below.

### Shared tests before any standard run

1. Baseline configuration reproduces the maintained result for the same seed.
2. Worker count, if parallelism is later added, does not change rows or values.
3. Cell reordering does not change cell outputs.
4. Raw-to-summary recomputation matches to `1e-12` for deterministic summaries.
5. Final-window indices are tested at exact integer and non-integer fractions.
6. Manifest validation fails on missing seed, grid, horizon, window, or output.
7. New intervention/architecture modes do not alter the baseline model path.

## E01 — Early outcome and information restoration

**Closes:** C1 mechanism support, C2, and C3 replication.  
**Planned run ID:** `frontiers_hot_stove_v1`.

### Question and hypotheses

Does an early rejected authentic outcome reduce later authentic sampling, final
objective reward, and policy quality; and does restoring information reduce
that persistence without changing the baseline payoff function?

- H1: after a controlled initial authentic attempt, rejected learners show
  higher final-window masking and fewer later authentic samples than accepted
  learners at the same objective parameters.
- H2: forced exploration or counterfactual feedback reduces the rejection-
  conditioned gap and reduces objective regret in an authenticity-optimal
  domain.
- H3: greater negative-outcome weighting increases the baseline gap but does
  not change objective expected rewards.

### Design

| Component | Standard specification |
| --- | --- |
| Model | M0 baseline plus explicitly labeled experiment-only information interventions |
| `p` | 0.75 and 0.85; both exceed the default objective threshold 0.7167 |
| `lambda` | 1.0 primary; 0.5 and 2.5 supporting C3 replication |
| Initial exposure | authentic action forced at step 0; record accepted/rejected outcome |
| Conditions | baseline; 5% forced-authentic sampling after step 0; counterfactual authentic feedback on masked trials |
| `n`, `T`, final window | 500 per cell, 2,000 steps, final 20% |
| Master seeds | 5 independent seeds |
| Sensitivity | forced-exploration rate 2%, 5%, 10%; `T` 1,000 and 5,000 on sentinel cells |

The forced step and feedback modes are experimental manipulations, not changes
to M0. Counterfactual feedback must update only the learner's information and
must store both the actual objective payoff and the unreceived counterfactual;
it must not award the counterfactual payoff to the environment return.

### Required raw fields and summaries

- initial authentic outcome and realized reward;
- time to next authentic action;
- authentic action count in steps 1-100 and across the full run;
- final-window mask rate;
- cumulative objective payoff and regret versus the analytic optimal arm;
- final Q-values;
- intervention exposure count;
- accepted-versus-rejected effect within each condition and seed;
- intervention-versus-baseline effect within each initial-outcome stratum.

### Decision rules

- **Direct hot-stove support:** in both primary `p` cells, early rejection has a
  positive effect on final masking and a negative effect on later authentic
  sampling in at least four of five seeds; the seed-level 95% interval for the
  pooled effect excludes zero.
- **Information-restriction support:** at least one prespecified information-
  restoring condition reduces both final masking and objective regret after
  early rejection, with a seed-level interval excluding zero and no change to
  the objective payoff equations.
- **Materiality:** the primary intervention reduces rejection-stratum mean
  final masking or normalized regret by at least 10% relative to baseline.
- If the early-outcome result holds but restoration does not, C2 remains
  “consistent with hot-stove persistence,” and alternative update/state
  explanations must be emphasized.
- If neither holds, remove the causal hot-stove claim and report only the
  maintained policy-learning result.

## E02 — Binary versus graded disclosure

**Closes:** C4.  
**Planned run ID:** `frontiers_m1_binary_graded_v1`.

### Question and hypotheses

Does access to independent intermediate disclosure arms preserve information
gathering or improve discovery of full authenticity relative to an otherwise
matched binary learner?

- H1: after a controlled rejected full-authentic attempt, the graded learner
  continues nonzero disclosure more often than the binary learner samples full
  authenticity.
- H2: graded actions improve later discovery of the objectively optimal full-
  authentic endpoint or reduce regret; mean disclosure alone is insufficient.

### Design

| Component | Standard specification |
| --- | --- |
| Architectures | M0 binary endpoints; M1 with five independent levels `0, .25, .5, .75, 1` |
| `p` | 0.65 (mask-optimal), 0.75 (near-threshold auth-optimal), 0.85 (auth-optimal) |
| Initial exposure | force `d=1`/authentic at step 0 and stratify by outcome |
| Learner settings | identical `alpha=0.1`, `tau=0.25`, `lambda=1`, `q0=0` |
| `n`, `T`, final window | 500 per cell, 2,000 steps, final 20% |
| Master seeds | 5 |
| Sensitivity | levels 3, 5, 9; `tau` 0.1, 0.25, 0.6; `T` 1,000 and 5,000 on sentinel cells |

The primary comparison is the implemented independent-arm M1, not a smooth-
generalization model. A generalization variant, if later studied, is a separate
secondary experiment and cannot be pooled with E02.

### Outcomes

- full-authentic (`d=1`) sampling rate and time to stable sampling;
- any-disclosure (`d>0`) sampling after early rejection;
- cumulative objective payoff and regret against the best static endpoint;
- probability the modal final-window arm is the objectively optimal endpoint;
- final-window mean disclosure and action distribution;
- rejection exposure and reward variance during exploration.

### Decision rules

- Support “graded actions preserve exploration relative to binary” only if the
  graded architecture improves a prespecified information outcome after early
  rejection in at least four of five seeds and the seed-level interval excludes
  zero.
- Support “improves discovery” only if full-authentic endpoint selection or
  objective regret also improves in the auth-optimal cells.
- If graded learners merely choose intermediate arms without improving endpoint
  discovery or regret, wording is limited to “changes the exposure distribution
  of exploration.”
- If additional arms worsen discovery through action-space dilution, report
  that result and remove protective wording.

## E03 — M2 regime replication and optimal-policy sensitivity

**Closes:** C1 and C5.  
**Planned run ID:** `frontiers_m2_regime_replication_v1`.

### Question and hypotheses

Is the maintained learned-suboptimal-masking classification stable across
independent master seeds, horizon, population size, final window, and targeted
learner settings when benchmarked against the same objective MDP?

### Design

The standard run has three linked parts:

1. **Exact-grid replication:** reproduce the current `p=0.00:0.05:1.00` by
   `eta=0.00:0.05:0.80` grid with `n=160`, `T=1,000`, final 20%, and five
   independent master seeds. This preserves comparability with 226/357.
2. **Sentinel sensitivity:** cells `(p,eta)` in
   `{(0.35,0),(0.40,0),(0.55,0),(0.55,.2),(.75,0),(.90,.2)}` with
   `n in {160,320}`, `T in {1,000,2,000,5,000}`, final-window fractions
   `{.1,.2,.4}`, and learner cases for `alpha {0.03,.1,.3}`,
   `tau {.1,.25,.6}`, `lambda {.5,1,2.5}`, `q0 {0,.75}`, and
   `gamma {.5,.9,.99}` one factor at a time.
3. **Threshold-local refinement:** adaptive `p` evaluation around the dynamic
   optimal threshold and the learned transition for `eta in {0,.2,.8}` until
   analytic threshold tolerance is `1e-4` and Monte Carlo transition-location
   uncertainty is reported.

Environment variants for `r2`, `b2`, and `delta` remain targeted sensitivity,
not part of the default-grid denominator. At minimum retain the current harsh
sentinel `r2=8`, `delta=.30`, `eta=0`, `gamma=.9` that produced a narrow
optimal-policy-masking width.

### Classification contract

For each seed and cell, report:

- static M0 optimal action;
- objective M2 optimal actions and value gap from value iteration;
- learned neutral action from final-window neutral-state counts;
- neutral-state mask probability;
- empirical policy value and dynamic regret;
- neutral-state visit count and a missing/inconclusive flag;
- region under the maintained definitions.

A cell is not classified by an aggregate mask rate alone. Ties within the
value-iteration tolerance and cells with inadequate neutral-state visits are
inconclusive, not forced into a regime.

### Uncertainty and decision rules

- Report the learned-suboptimal cell fraction separately by seed, its mean and
  seed-level 95% interval, and per-cell classification frequency across five
  seeds.
- Define a stable headline cell as the same non-inconclusive classification in
  at least four of five seeds.
- The 226/357 value may remain in final prose only if the exact replication
  reproduces 226 for the original seed; the publication headline must use the
  replicated distribution or a stability-qualified count.
- Support a broad default learner-failure regime if at least 50% of exact-grid
  cells are stably learned-suboptimal, the lower seed-level interval for the
  fraction exceeds 0.40, and sentinel directions survive `n`, `T`, and window
  sensitivity.
- Call masking “structurally optimal” only in cells whose objective M2 value
  iteration selects mask while static M0 selects authenticity. Report those
  cells and widths separately from learner failure.
- If classification changes materially with horizon or learner parameters,
  narrow the claim to the stable domain and show the dependence.

## E04 — M3 context-search architectures and context identity

**Closes:** C6.  
**Planned run ID:** `frontiers_m3_search_architectures_v1`.

### Question and hypotheses

Does increasing K reduce discovery because of action-space/search structure,
and does the result survive randomized receptive-context identity and multiple
receptive contexts?

### Design

| Component | Standard specification |
| --- | --- |
| Architectures | flat 2K; hierarchical context-then-behavior; global mask; fixed-known-good context |
| K curve | 1, 2, 4, 8, 16 |
| Receptivity | `p_good=.85`, `p_bad=.20`, `bf=0` primary |
| Good-context identity | fixed index 0; randomized per child and recorded |
| Multiple-good variants | one good; two good where K permits; 25% of contexts good |
| `n`, `T`, final window | 500 per cell, 2,000 steps, final 20% |
| Master seeds | 5 |
| Sensitivity | `p_good {.70,.85,.95}`, `p_bad {.05,.20,.40}`, `tau {.1,.25,.6}` on K `{2,8,16}` |

For K=1, multiple-good and identity variants collapse to the same environment
and should be emitted once with explicit equivalence metadata.

### Outcomes

- probability modal final-window action is authenticity in any good context;
- time to first accepted authenticity in a good context;
- number of distinct contexts sampled authentically;
- cumulative objective reward/regret against the known best architecture-
  appropriate action;
- context-choice entropy and authentic-sampling allocation;
- K-response slope or contrast with seed-level uncertainty;
- recorded good-context identities and counts for every child.

### Decision rules

- Support “search burden” if flat and/or hierarchical architectures show a
  negative K response in at least four of five seeds while global-mask and
  fixed-known-good controls remain practically near zero, with architecture-by-
  K contrast intervals excluding zero.
- Prespecify practical equivalence for control K effects as absolute change
  below 0.05 in settling probability and an interval contained within
  `[-0.10,0.10]`.
- Generalize beyond fixed identity only if direction survives randomized
  identity. Generalize beyond one rare receptive context only after reporting
  how effect size changes with two and 25% receptive contexts.
- If K effects disappear when good identity is randomized, label the current
  result an index/initialization artifact and do not use the broad claim.

## E05 — Dense BFLPE behavioral crossover

**Closes:** C7.  
**Planned run ID:** `frontiers_m3_bflpe_crossover_v1`.

### Question and hypotheses

Where does learned good-context authenticity change as `bf` crosses the
analytic objective threshold `0.470588`, and how uncertain is that learned
transition?

### Design

- Flat M3 at K=4 with fixed good-context identity for primary comparability.
- `bf` grid `0.30:0.025:0.65`, including the analytic threshold between grid
  points; add `0`, `0.4705882353`, and `0.80` as anchors.
- `n=500`, `T=2,000`, final 20%, five master seeds.
- Repeat targeted points within `±0.05` of the estimated transition at
  `T=5,000` for horizon sensitivity.
- Secondary check in the hierarchical architecture; do not pool architectures.

### Outcomes and estimation

- modal good-context-authentic fraction, its seed-level interval, mean authentic
  rate in the good context, objective reward, and regret;
- analytic objective advantage at every `bf`;
- learned 50% transition location estimated by monotone interpolation or a
  prespecified dependency-free isotonic procedure;
- bootstrap transition-location interval using master seed as the top-level
  unit;
- separate vertical markers for analytic and learned thresholds.

### Decision rules

- The analytic threshold is reported as proved from the reward equation,
  independent of the behavioral fit.
- Support a learned crossover only if the response is monotonically decreasing
  within Monte Carlo uncertainty and crosses 0.5 inside the tested dense range
  in at least four of five seeds.
- If no 0.5 crossing occurs, report the response curve and endpoint change, not
  a learned threshold.
- Never translate `bf` units or the crossover into a human placement threshold.

## E06 — M4 feedback, path dependence, and hysteresis diagnostics

**Closes:** C8 and determines whether C9 remains excluded.  
**Planned run ID:** `frontiers_m4_path_diagnostics_v1`.

**Operational authority:** the ambiguity-resolving frozen design, exact smoke,
core-standard scenarios, separately gated qualification tier, RNG/control
semantics, estimators, schemas, decision rules, and resource gates are in
`approvals/E06_SMOKE_APPROVAL.md`. Where this section is less specific, that
approval record controls. Core standard GO never authorizes the qualification
tier.

### Question and hypotheses

Is path separation reproducible across independent seeds, ramp speeds, and
horizons, and does it exceed continuation/stochastic controls strongly enough
to justify hysteresis rather than schedule-specific path dependence?

### Design

| Component | Standard specification |
| --- | --- |
| Primary `km` ramp | 11 evenly spaced points from 0 to .004, ascending then descending |
| Per-point horizon | 500 and 1,000 steps as two ramp speeds |
| Learners | 400 per path cell |
| Master seeds | 5 |
| Initial receptivity | `p0=.45` primary; `.10` and `.90` sensitivity |
| Feedback balance | `ka=.12, kr=.04` primary; cases `ka<kr`, `ka=kr`, `ka>kr` |
| Mechanism ablations | `km=0`; `ka=0`; `kr=0`; paired cold starts at every `km` |
| Learner sensitivity | `lambda {.5,2.5}` and `tau {.1,.6}` on primary speed |
| Long horizon | 2,000 steps per point on sentinel configurations |

The ascending and descending paths must continue Q-values and `p_t`. Cold-start
controls initialize every `km` independently from the same declared `q0,p0`
distribution. A reversal-only control repeats the RNG design without inheriting
state to estimate ordinary schedule noise.

### Outcomes

- mask-rate and final-receptivity paths by seed;
- signed and absolute loop area using a declared trapezoidal convention;
- ascending and descending transition locations for prespecified mask-rate
  levels 0.5 and 0.75, when crossed;
- threshold separation and its seed-level interval;
- maximum and mean matched-`km` path separation;
- same summaries for cold-start and reversal-only controls;
- bounds violations (must be zero), final Q-values, and final `p_t`
  distributions.

### Decision rules

- **Self-reinforcing feedback:** retain C8 if `km>0` increases masking and
  lowers receptivity relative to `km=0` in at least four of five seeds, with
  seed-level intervals excluding zero.
- **Path dependence:** retain if inherited ascending/descending paths have a
  nonzero loop area and matched-parameter separation in at least four of five
  seeds and exceed cold-start control separation.
- **Hysteresis:** reconsider C9 only if both ascending and descending transition
  locations are estimable, their separation has a seed-level interval excluding
  zero, loop direction is consistent, and these results survive both ramp
  speeds, the long-horizon sentinel, and the stochastic controls.
- If separation shrinks materially toward zero as per-point horizon increases,
  describe transient path dependence rather than hysteresis.
- If only the primary schedule separates, retain exactly “schedule-specific
  path dependence.”

## Stage 2 execution order and stop/go gates

| Order | Work item | Why first | Stop/go decision |
| ---: | --- | --- | --- |
| 1 | Implement shared config/seed/manifest schema and run E01 smoke | Central mechanism and infrastructure proof | Review raw trajectory semantics before standard run |
| 2 | Run E02 smoke and standard | Resolves an overstatement in current P45/P59/P77 | Narrow C4 immediately if architecture benefit is absent |
| 3 | Run E03 exact-grid replication | Central quantitative headline | Do not rebuild Figure 3/article Results until stable-cell summary exists |
| 4 | Run E04 standard K curves/variants | Tests whether M3 claim is representationally robust | Drop broad context-search claim if identity control fails |
| 5 | Run E05 dense crossover | Targeted and separable from E04 | Report response only if learned threshold is not identified |
| 6 | Run E06 standard diagnostics | Most stateful and interpretation-sensitive | Keep C9 excluded unless every gate passes |
| 7 | Publication-tier sentinels only | Refine supported boundaries | Explicit approval after runtime/cost report |

No experiment proceeds from smoke to standard if repository verification fails,
raw-to-summary reconciliation fails, or baseline reproduction changes. Failed
claim gates narrow the manuscript; they are not reasons to tune defaults or
rewrite model semantics.

## Stage 2 completion gate

- [ ] E01-E06 smoke configurations pass semantic, RNG, schema, and summary tests.
- [ ] Every standard experiment has at least five independent master seeds.
- [ ] Every headline effect has seed-level uncertainty and source rows.
- [ ] E03 distinguishes learned suboptimal masking from optimal-policy masking.
- [ ] E04 includes full K curves, randomized identity, and multiple-good variants.
- [x] E05 separates analytic and learned crossovers; preserve the canonical
  paired result and boundaries in `E05_MAIN_RESULTS.md`.
- [ ] E06 reports loop area, transition separation, speeds, horizons, and controls.
- [ ] The claim ledger is updated to supported, narrowed, or excluded from the
  new evidence without changing model semantics to favor a conclusion.
- [ ] Final Stage 2 artifacts regenerate deterministically and pass
  `./scripts/verify.sh`.
