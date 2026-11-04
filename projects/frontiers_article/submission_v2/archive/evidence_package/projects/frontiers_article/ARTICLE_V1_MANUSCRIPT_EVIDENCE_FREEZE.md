# Article V1 Manuscript Evidence Freeze

**Freeze date:** 15 August 2026
**Repository:** `gifted-masking`, branch `codex/frontiers-stage2-e06`, HEAD `ea46c9d9bbd39c1bfcd84a9b818d7bd16e30bf32`
**Scope:** **PRIMARY ARTICLE V1 = E01–E05 ONLY**; M0–M3 semantics; Article-V1 manuscript-facing wording
**Deferred:** **E06/M4 is deferred from the primary Article V1 manuscript and retained as future work.**
**Document class:** documentation only. This freeze changes no code, config, artifact, figure, or scientific claim. It fixes the exact evidence, estimand definitions, and maximum defensible wording from which Article-V1 prose may be written.
**Completion state:** `READY_FOR_SHORT_ARTICLE`

---

## A. Purpose and authority precedence

This freeze is the single manuscript-facing evidence source for Article V1. Prose must be written from this document and the two authorities beneath it. It exists because the consistency audit returned `PUBLICATION_BLOCKING_GAP_FOUND` against the current manuscript chapters, and because the numeric evidence is intact while the interpretation attached to it is not.

Authority order, highest first:

1. `projects/frontiers_article/ARTICLE_V1_EVIDENCE_MATRIX.csv` — 29 adjudicated candidate claims with content-addressed artifacts, estimands, inferential units, and maximum defensible wording. This is the primary claim authority.
2. `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` — statement-level verdicts, gap register G-01…G-15, model verification, scientific-boundary summary. This is the primary interpretation-constraint authority.
3. `projects/frontiers_article/ARTICLE_V1_E01_E02_INTERPRETATION.md`, `..._E03_...`, `..._E04_...`, `..._E05_...` — per-experiment interpretation authorities, supplied 15 August 2026 (Section H). They govern theoretical framing, mechanism language, and the supported/qualified/unsupported boundaries **subordinate to Sections C, E, and I of this freeze**, which override them wherever they differ.
4. `projects/frontiers_article/ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md` and `_INDEX.csv` — historical generator-source identity.
5. Frozen artifacts under `results/summaries/`, manifests under `results/manifests/`, configs under `configs/frontiers_article/`, approvals under `projects/frontiers_article/approvals/`.

**Not authorities.** `doc-reviews/frontiers_submission/RESULTS_BY_FINDING_CHAPTER.md`, `doc-reviews/frontiers_submission/DISCUSSION_CHAPTER.md`, and `PAPER_REVISION_NOTES.md` are stale drafting sources. They are retained only as the inventory of claims to be removed or replaced (Section G). No sentence may be carried from them into V1 without re-derivation against this freeze.

### A.1 Editorial scope and next artifact

**PRIMARY ARTICLE V1: E01–E05 ONLY.** E06/M4 is deferred from the primary
manuscript and retained as future work. This is an editorial scope decision,
not a finding that E06 is invalid, failed, disproven, unusable, or abandoned.
E01–E05 already form a complete progression; E06 adds endogenous
environment–behaviour feedback and would materially expand a concise first
article into a broader programme report.

The next artifact is a normal short research article of approximately
6,000–8,000 main-text words, with approximately 1,200–1,600 words of main
Methods, approximately four to five main figures, and a conclusion of no more
than two paragraphs. The long Formal Model and Methods authority is preserved
for later separation into main Methods, Supplementary Methods, and repository
reproducibility/technical documentation. It is not the intended main-text
Methods section, and no compression is authorized in this freeze stage.

No new E01–E05 research, numerical inference, result regeneration, or model
change is required before manuscript construction. The next stage is an
article skeleton followed by a claim/evidence/figure map; prose drafting does
not begin in this stage.

### A.2 Scientific spine

Article V1 constructs a progression of ability-concealment learning
environments in which behavioural findings are evaluated against explicit
analytic or dynamic-programming objective benchmarks. This makes several
distinct forms of learned–objective divergence measurable rather than inferred.

| Experiment | Article function |
|---|---|
| E01 | adverse-history sampling-trajectory effect |
| E02 | endpoint-discovery divergence |
| E03 | dynamic policy-disagreement region |
| E04 | receptive-context discovery gap |
| E05 | behavioural/objective threshold displacement |

The conceptual progression is `history -> endpoint discovery -> dynamic
disagreement -> social discoverability -> boundary displacement`. The bounded
synthesis is `immediate value != dynamic value != discoverability != learned
behavioural boundary`.

---

## B. Verification state at freeze time

### B.1 Artifact identity

All ten summary artifacts named by the evidence matrix were rehashed at freeze time and byte-match the matrix `artifact_sha256` values:

| Experiment | Artifact | SHA-256 | Match |
|---|---|---|---|
| E01 | `results/summaries/frontiers_hot_stove_v1_effects.csv` | `4ce67da8b48e8d770388db9e2c6ebe240b868c0696ba90678cc9940de02684d8` | PASS |
| E02 | `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` | `11d29c72508649a174b285957dfec3752edff76a099aa76de9f6fe3a4e515a8a` | PASS |
| E03 | `..._m2_regime_replication_v1_effects.csv` | `5a1ee392560e94695dfe0d04ff89caeafdb0b58fa2b70e6def365726d66ab3af` | PASS |
| E03 | `..._m2_regime_replication_v1_stable_cells.csv` | `91814ab4430f63bc5e46596c61718e1fec6705d355b6cab3d8c18d29c1dfaea7` | PASS |
| E03 | `..._m2_regime_replication_v1_thresholds.csv` | `0987aea9f6085f81bad791454eaca03127c6144f172a7cc9f41cdad6c316f9bf` | PASS |
| E03 | `..._m2_regime_replication_v1_cells.csv` | `198cb7be9b2a93aa89569d9dd656326f521b7a2ec99543733fd6e779e0508851` | PASS |
| E04 | `..._m3_search_architectures_v1_effects.csv` | `dd426992f0a1a0ae05542756dc6dca918fbf56a589347676a93a309d08a41d44` | PASS |
| E05 | `..._m3_bflpe_crossover_v1_analytic.csv` | `e1045d0593709561761ec8c9ba0684ef1a80e26d6b0b15f12f57434b74f22a42` | PASS |
| E05 | `..._m3_bflpe_crossover_v1_transitions.csv` | `96b8d8dc1cf27e3a226282e4d8755effde74e855d81b8f8bbc6db6515c607097` | PASS |
| E05 | `..._m3_bflpe_crossover_v1_effects.csv` | `33eb752c89d87ce79ef13bfe196623fb4d4f53c4fff63e03b84af413a68200d5` | PASS |

Model and core blobs match the mathematical hand-off reference exactly (audit §B.2). No frozen result is affected by a maintained-model semantic change.

### B.2 Approval state

`E01_STANDARD_GO.md` … `E05_STANDARD_GO.md` are all present and record a standard GO. E06 holds only a smoke approval, a compression amendment, and a standing readiness blocker — **there is no E06 standard GO**, which is independently consistent with excluding E06 from Article V1.

Note for reviewers: the `approved_standard: false` flag inside the frozen standard configs is a run-time gate recorded at generation, not a retraction of the separate written approval records.

### B.3 Divergences from the consistency audit's snapshot

The audit was written at HEAD `441cfe44`. Two later commits change two of its findings. Neither touched E01–E05 configs, artifacts, or model code.

| Audit finding | Audit state at `441cfe44` | State at `ea46c9d9` | Effect on this freeze |
|---|---|---|---|
| #5 / G-05 — missing authorities | `HANDOFF.md`, six named `ARTICLE_V1_*` files, and four interpretation notes "not supplied or found" | All seven named authorities present under `projects/frontiers_article/` (added by `907abfb`); all four interpretation notes supplied 15 August 2026 and added at freeze time | **Resolved.** G-05 closes. The statement audit can now be completed against the interpretation notes rather than the matrix alone (Section H). |
| #4 / G-04 — generator-source provenance | Exact generator source not recoverable for E01–E05 | `ea46c9d` recovered fingerprint-exact historical source bundles for **E04 and E05**; E01–E03 remain unrecoverable | **Narrowed.** The limitation statement in Section F is scoped to E01–E03. |

All other audit findings stand unchanged, including both BLOCKERs.

---

## C. Cross-cutting definitions binding on all V1 prose

These definitions are mandatory wherever the corresponding number appears. They are the substance of gaps G-06, G-08, G-09, G-11, and G-12.

**C.1 Inferential unit.** Every simulation interval in E01, E02, E04, and E05 is a Student-t interval across **five master seeds** (df = 4), not across children. `n=500` (E01/E02/E04/E05) or `n=160` (E03) is the number of simulated learners per cell, not the inferential replicate count. Never report a per-child bootstrap as the uncertainty of a headline effect.

**C.2 E03 grid cells are not independent units.** The five master-seed grid fractions are identical, so the stored 95% interval collapses to a point. Report this as "identical across the five selected master streams"; do not present it as zero Monte Carlo or model uncertainty (G-12).

**C.3 "Learned masking" in E03** means: aggregate final-window Neutral-state action counts favour masking, subject to the prespecified visit-adequacy rule and explicit tie handling, while full-information value iteration selects authenticity in the same cell. It is **not** a Q-ordering classifier, **not** an individual-policy prevalence, and **not** an information-matched comparison (G-06).

**C.4 "Settled" in E04/E05** means final-window `argmax` classification. The prespecified primary metric permits non-unique modal arms. Strict unique-modal recomputations exist and agree in direction, but are post hoc frozen diagnostics and may not silently replace the prespecified estimand (G-11).

**C.5 E01 regret is not independent of E01 sampling.** In the authenticity-optimal binary cells, normalized pseudo-regret equals the fraction of suboptimal mask actions. With the forced authentic first action and T = 2000,

> normalized-regret contrast = −(T−1)/T × post-initial authentic-rate contrast,

verified at freeze time: −(1999/2000) × (−0.02583704230615776) = 0.025824123785. Present one primary estimand and translate it into the other unit explicitly; never present both as independent confirmations (G-08).

**C.6 E02 regret is a disclosure-distance identity.** M1 expected reward is affine in disclosure d, so in the authenticity-optimal strata per-step normalized regret is exactly `1 − d`. The regret contrast is a horizon-average disclosure-distance contrast — objectively meaningful, but not independent welfare evidence (G-09).

**C.7 Cross-experiment commensurability.** The matrix marks E01 and E02 regret estimands `NOT_COMPARABLE`. E01's rejected-minus-accepted contrast and E02's architecture contrast are different estimands and must not be arranged as a dissociation.

**C.8 Comparators are full-information.** E03's DP comparator and E04/E05's objective benchmarks know the complete payoff structure. They do not share the learner's information limits. No statement may claim the learner underperformed the best policy attainable under its own information constraints.

---

## D. Frozen evidence by experiment

Each row states the exact estimand, the frozen value, the interval, and the wording ceiling. Values are reproduced from the artifacts and the matrix; where the matrix reports a p-pooled figure, the pooling is equal weight over p ∈ {0.75, 0.85} and was re-derived at freeze time from the per-p `across_master_seeds` rows.

### D.1 E01 — M0 hot stove

Config `configs/frontiers_article/e01_hot_stove_standard.json` (`1d8ac315…`); run `frontiers_hot_stove_v1`; n = 500, T = 2000, final window 0.2 (steps 1600–1999); master seeds 2026081101–05; primary λ = 1.

| Claim ID | Exact estimand | Value | 95% Student-t | Ceiling wording |
|---|---|---|---|---|
| E01-C2-SAMPLING | rejected − accepted post-initial authentic action rate, steps 1–1999 | **−0.025837** | [−0.035753, −0.015922] | An initial rejection reduced later authentic sampling by 0.0258 in the tested p = .75/.85 M0 domain. |
| E01-C2-REGRET | rejected − accepted normalized objective pseudo-regret | **+0.025824** | [+0.015914, +0.035735] | The same behaviour expressed as normalized objective loss. Governed by C.5 — not a second finding. |
| E01-C2-FINAL-MASK | rejected − accepted final-window mask rate | **−0.000343** | [−0.011605, +0.010918] | The experiment did not detect an increase in final-window masking after one initial rejection. No equivalence margin was tested. |
| E01-C2-FORCED-MASK | baseline − forced-authentic-0.05 final mask rate, rejected stratum | **+0.046590** | [+0.033230, +0.059951] | Five-percent forced authentic exploration reduced rejection-stratum final masking by 0.0466 in the model. |
| E01-C2-FORCED-REGRET | same, normalized regret | **+0.057954** | [+0.045614, +0.070293] | Reduced rejection-stratum normalized pseudo-regret by 0.0580. Model information manipulation only. |
| E01-C2-CF-MASK | baseline − counterfactual-authentic-feedback final mask rate | **+0.118135** | [+0.109683, +0.126587] | Counterfactual authentic feedback reduced rejection-stratum final masking by 0.118. |
| E01-C2-CF-REGRET | same, normalized regret | **+0.141318** | [+0.132369, +0.150267] | Reduced rejection-stratum normalized pseudo-regret by 0.141. |
| E01-C3-LAMBDA | maintained p = .65, λ 2.5 − λ 0.5 final mask rate | **+0.402990** | [+0.395366, +0.410614] | At p = .65, raising λ from .5 to 2.5 increased final masking by 0.403 **without changing objective payoffs**. |
| E01-C3-GAP | high-λ minus low-λ controlled early-rejection gap (gap-in-gap) | **−0.001067** | [−0.015031, +0.012898] | Greater loss weighting did not measurably amplify the controlled initial-outcome masking gap. |

**E01 boundaries.** The final-mask null is a failure to detect, not proof of equivalence, and not support for a persistent-mask subregion (G-07). Only p = .75 and .85 were tested for controlled initial outcome. The forced-exploration and counterfactual-feedback results are manipulations of the model's information channel; they are not human intervention estimates.

### D.2 E02 — M0/M1 binary versus graded

Config `e02_binary_graded_standard.json` (`08aa809c…`); run `frontiers_m1_binary_graded_v1`; matched common-random-number pairs within master and p; rejected initial-outcome stratum; n = 500, T = 2000, window 0.2; master seeds 2026081201–05.

| Claim ID | Exact estimand | Value | 95% Student-t | Ceiling wording |
|---|---|---|---|---|
| E02-C4-EXPLORATION | graded d > 0 post-initial rate − binary d = 1 post-initial rate | **+0.255040** | [+0.253004, +0.257077] | Independent graded arms increased post-rejection nonzero disclosure by 0.255 relative to binary full-authentic resampling. Exposure distribution, not endpoint discovery. |
| E02-C4-FULL-ENDPOINT | graded − binary full-authentic final-window rate | **−0.328692** | [−0.342037, −0.315348] | The additional graded arms reduced full-authentic final-window selection. |
| E02-C4-MODAL | graded − binary probability the unique final-window modal arm is the objective endpoint d = 1 | **−0.221740** | [−0.288755, −0.154724] | Graded arms did not improve optimal-endpoint discovery; modal selection was lower. |
| E02-C4-REGRET | binary − graded normalized regret | **−0.029761** | [−0.033874, −0.025648] | Graded did not improve pooled normalized regret and was worse under the prespecified contrast. Governed by C.6. |

**E02 boundaries.** The exploration result may not be reported without the three adverse results beside it. Prohibited framings: ladder climbing, endpoint discovery, smooth generalization, protective effect, independent welfare improvement. M1 assigns independent Q values per arm — there is no interpolation or generalized update between neighbouring disclosure levels.

### D.3 E03 — M2 regime replication

Config `e03_m2_regime_standard.json` (`52197a07…`); run `frontiers_m2_regime_replication_v1`; frozen 21 × 17 p-by-η exact grid = 357 cells; n = 160, T = 1000, window 0.2; master seeds 2026081301–05; γ = 0.9, α = 0.1, τ = 0.25, λ = 1.

| Claim ID | Exact estimand | Value | Uncertainty | Ceiling wording |
|---|---|---|---|---|
| E03-C5-GRID | share of tested cells classified `learned_suboptimal_masking` | **0.680672268907563 = 243/357** | identical in all five masters; stored interval collapses to a point | Under the frozen default learner, aggregate final-window Neutral action counts favoured masking while full-information value iteration selected authenticity in 243 of 357 tested cells. |
| E03-C5-STABILITY | stable-cell count under the 4-of-5 rule | **350/357 stable; 243 stable learned-suboptimal; 7 inconclusive** | no interval | Classification was stable in 350 of 357 tested cells; seven low-p, η = 0 cells were inconclusive because Neutral visits failed the prespecified adequacy rule. |
| E03-C5-THRESHOLDS | objective dynamic neutral-authenticity threshold brackets, bisection width 6.1e−05 | **η = 0: [0.3839111, 0.3839722]; η = .2: [0.3387451, 0.3388062]; η = .8: [0.2689819, 0.2690430]** | deterministic | Under the frozen M2 transition model the objective thresholds bracket near .384, .339, and .269 for η = 0, .2, .8, below the static M0 threshold 43/60. No learned transition threshold was estimable. |
| E03-C5-GAMMA | sentinel reclassification at γ = .5 | first three of five dynamic-authenticity sentinels became `learner_matches_objective` in all five masters | classification frequency | The classification is conditional on γ; at γ = .5 the **objective** policy changed at three prespecified sentinels. This is not improved learning. |
| E03-C5-ALPHA-TAU | sentinel reclassification at α = .03 and τ = .6 | α = .03 changed p = .75/η = 0 and p = .90/η = .2; τ = .6 made .90/.2 unstable and .75/0 only 4-of-5 | classification frequency | Classification is conditional on the frozen learner settings; named perturbations changed specific sentinels. No monotone learner generalization follows. |
| E03-C5-HARSH | harsh sentinel b2 = 0, r2 = 8, δ = .3, η = 0, p = .75 | objective neutral Q(auth − mask) = **−0.4062934363**; `optimal_policy_masking` in all five masters | five-master consistency | Under the separately labelled harsh boundary, objective M2 masking despite static M0 authenticity occurred at p = .75 in all five masters. |

**E03 boundaries.** `243/357` is **tested-grid coverage under a frozen learner**, not prevalence of any kind, not phase-space volume, and not a headline number. It belongs in supplement or tested-grid provenance. The learned neutral-dyadic threshold rows in the frozen thresholds table are `censored_inconclusive` (η = 0) or `censored_no_crossing` (η = .2, .8) — no learned threshold may be quoted. The harsh sentinel is a single labelled cell; no structural lock-in region may be extrapolated from it.

### D.4 E04 — M3 search architectures

Config `e04_m3_search_architectures_standard.json` (`e8b73dc7…`); run `frontiers_m3_search_architectures_v1`; n = 500, T = 2000, window 0.2; master seeds 2026081401–05; p_good = .85, p_bad = .2, bf = 0.

**Primary estimand.** `mean_settled_any_good_auth_argmax` = the per-cell mean over children of an indicator that the child's final-window modal action, taken by `argmax` over final-window action counts, is an authentic behaviour in a good (receptive) context. Defined in `src/gifted_masking/experiments/e04.py`; ties permitted (C.4).

**Architectures** (`e04.py:40`): `flat_2k` — one softmax over 2K joint context-behaviour arms. `hierarchical` — a K-way context softmax followed within the same trial by a two-way behaviour softmax, both Q tables receiving the same realized reward. `global_mask` — one shared mask arm plus K context-authentic arms. `fixed_known_good` — a two-arm problem with no context choice, structurally K-invariant.

**K-invariant objective benchmark.** With one fixed good context, increasing K changes multiplicities only. The distinct objective reward set {R_M, R_G, R_B} and `max(R_M, R_G, R_B)` are K-invariant, carried per row as `objective_best_expected_reward`. Any decline in settling is therefore a learner/representation effect, not a change in what is objectively achievable.

| Claim ID | Exact estimand | Value | 95% Student-t | Ceiling wording |
|---|---|---|---|---|
| E04-C6-FLAT | flat_2k K = 16 − K = 1, fixed one good context | **−0.2340** | [−0.246417, −0.221583] | In the frozen scarce-receptivity flat-2K representation, K = 16 reduced receptive-context authentic settling by 0.234 relative to K = 1. |
| E04-C6-HIER | hierarchical, same contrast | **−0.4704** | [−0.511031, −0.429769] | In the frozen hierarchical representation the corresponding reduction was 0.470. Do not imply architecture-general magnitude. |
| E04-C6-CONTROLS | global_mask same contrast; fixed_known_good structural K effect | **+0.0088**; **0** | [+0.002090, +0.015510]; [0, 0] | Global-mask and known-good controls remained practically equivalent across K under the prespecified band. Global-mask differs statistically from zero but is practically near zero. |
| E04-C6-IDENTITY | randomized − fixed identity K-slope, one good context | flat **−0.00292**; hier **+0.00140** | flat [−0.012269, +0.006429]; hier [−0.012620, +0.015420] | Randomizing receptive-context identity did not materially change the flat or hierarchical K decline. Rules against a fixed-label artifact in this design. |
| E04-C6-MULTIPLE | two-good − one-good slope; proportional-25 − one-good slope | two: flat **+0.05064**, hier **+0.02524**; prop-25: flat **+0.06044**, hier **+0.11224** | flat two [+0.045204, +0.056076]; hier two [+0.012988, +0.037492]; flat prop [+0.055044, +0.065836]; hier prop [+0.104787, +0.119693] | The K decline weakened with two receptive contexts and was near zero in the tested proportional-25 regime. |

**E04 boundaries.** The defensible claim is a **conjunction**: representation-dependent search burden under scarce receptivity. The one-good K manipulation alone confounds K with good-fraction 1/K and does not identify scarcity (G-13). `global_mask` changes action cardinality, initial probability mass, competition, and update allocation — it does not isolate duplicate-mask normalization (G-10). The model is repeated joint/context choice with learned values; it does not model human movement between peer groups, availability, or literal sequential search (G-14).

**Post hoc diagnostic, not a headline.** Recomputing the same contrasts from `mean_settled_any_good_auth_unique` gives flat −0.2412 ([−0.2520, −0.2304]) and hierarchical −0.4812 ([−0.5191, −0.4433]). Direction is not created by ties. This was not the prespecified estimand.

### D.5 E05 — M3 comparison-cost crossover

Config `e05_m3_bflpe_crossover_standard.json` (`571d3c93…`); run `frontiers_m3_bflpe_crossover_v1`; K = 4, fixed good context, p_good = .85, p_bad = .2; n = 500, T = 2000, window 0.2; master seeds 2026081501–05; **primary λ = 1** (config `learner.lambda = 1.0`), α = .1, τ = .25, q0 = 0.

**Reported population response.** `modal_good_auth_argmax_fraction` = the across-child fraction whose final-window modal arm, by `argmax`, is the single good-context authentic arm, in a flat eight-action (2K, K = 4) policy. Fitted by equal-n nonincreasing PAVA over the dense bf grid [0.30, 0.65]; the reported crossing is where the pooled fitted response crosses 0.5. **This is not a binary softmax probability** — see Section E.

| Claim ID | Exact estimand | Value | Uncertainty | Ceiling wording |
|---|---|---|---|---|
| E05-C7-ANALYTIC | objective bf at which good-context authenticity equals masking | **8/17 = 0.47058823529411764** | exact; deterministic | Under the frozen payoffs R_M = .75 and R_G = 1.15 − .85·bf, the exact objective crossover is bf = 8/17 = .470588. Not a learned threshold. |
| E05-C7-CROSSING | flat_2k bf where the pooled PAVA response crosses .5 | **0.31285211267605634** | bootstrap [0.3078358208955224, 0.3169178027050235]; 10,000 resamples of five complete master curves, 10,000/10,000 valid | In the frozen K = 4 flat 2K representation the learned .5 crossing was bf = .313 (.308–.317), before the objective crossover .471. |
| E05-C7-GAP | objective advantage `.40 − .85·bf` evaluated at the learned crossing | **≈ 0.134076** | inherits crossing uncertainty; transformed bounds ≈ [0.130620, 0.138340] | At the learned crossing, good-context authenticity still retained about .134 objective advantage. Conditional on the point crossing; not separately tabulated uncertainty. |
| E05-C7-ENDPOINT | flat_2k modal good-auth fraction, bf = .80 minus bf = 0 | **−0.9400** | Student-t [−0.957993, −0.922007] | The flat good-auth modal fraction fell by .940 from bf = 0 to .80. Supporting context only; must not replace the dense crossing. |
| E05-C7-HIER-CENSOR | hierarchical in-range crossing status | **`no_crossing_below`**; isotonic response **0.1176** at bf = .30; 0 of 10,000 bootstrap crossings valid | not estimable | The hierarchical response was already below .5 at the lower dense boundary bf = .30, so no in-range crossing was estimable. **Left-censored, not absent globally.** |

**E05 boundaries.** Bad-context authenticity is not the competing optimum in this range: good-versus-bad crosses at 39/17, far outside the dense grid. No hierarchical crossing may be estimated or extrapolated outside the approved dense range. The crossing's inferential unit remains five master curves.

**Post hoc diagnostic, not a headline.** Using `modal_good_auth_unique_fraction` with the same grid, PAVA, and master bootstrap gives point .31033, interval ≈ [.30503, .31412]. This does not repair the Section E blocker.

---

## E. Standing BLOCKER — the E05 binary-softmax misapplication

**This is unresolved. Article V1 may not be submitted with any wording that depends on it.**

Proposition G2 states that for a **two-action** softmax, P(A) = .5 exactly when Q_A = Q_M. The E05 reported crossing is not that quantity. It is the across-child fraction whose final-window modal arm is one specific arm in an **eight-action** flat policy. For K actions the corresponding condition is π_i = .5 iff Q_i = τ·log(Σ_{j≠i} exp(Q_j/τ)), which depends on every alternative. E05 measures neither.

Consequences that bind the manuscript:

- The **empirical crossing remains valid** and fully reportable at the wording ceiling in D.5.
- The **causal exclusion does not hold.** Fixed temperature and multi-action normalization are **not** ruled out as contributors to the measured displacement.
- Prohibited: applying G2 to the E05 crossing; stating or implying that fixed temperature alone has been excluded; presenting the learned/objective separation as evidence of a specific mechanism.
- Required: report the learned/objective separation **descriptively**, and list fixed temperature, action-set normalization, and hot-stove sampling among unresolved contributors that the current design does not decompose.

### E.1 Sources carrying the misapplication

Three supplied sources apply the binary theorem to the E05 gap. All are superseded by this section.

| Source | Passage | Disposition |
|---|---|---|
| Hand-off analytic DOCX | §2.3, Table 8 | Superseded. |
| Literature DOCX | §3.2 | Superseded. |
| `ARTICLE_V1_E05_INTERPRETATION.md` | §6 "Why fixed common softmax temperature cannot explain the shift by itself", closing "Temperature alone is ruled out."; the §7 concession; the executive summary; and the **Supported** bullet "Fixed common binary softmax temperature alone cannot explain a shifted 50% Q-equality location." | Superseded **for E05**. See E.2. |

### E.2 Why the E05 note's own caveat is not sufficient

The E05 interpretation note is more careful than the DOCX sources: its §7 states the multi-action condition explicitly, concedes that "a multi-action 50% probability point is not generally equivalent to pairwise equality with one competitor", and its §8 lists finite-sample estimation, endogenous under-sampling, search, multi-action normalization, step-size, and representation as unidentified plausible contributors. That framing is correct and is retained.

The residual defect is narrower and survives the caveat. Both §6 and §7 reason about the location at which a **softmax action probability** equals 0.5. E05 does not measure a softmax action probability. It measures the across-child fraction whose final-window **modal arm** is the good-context authentic arm. The bullet "fixed common binary softmax temperature alone cannot explain a shifted 50% Q-equality location" is a true statement about Q-equality, and a non-sequitur about E05's estimand — no softmax indifference identity, binary or multi-action, governs where a modal-classification fraction crosses 0.5.

Therefore, for V1 prose: keep §8's list of unresolved contributors, and **move fixed temperature into it** rather than out of it. Delete "Temperature alone is ruled out" and the corresponding **Supported** bullet. This does not weaken the empirical result in D.5, which stands unchanged.

---

## F. Provenance limitation — required manuscript statement

Artifact identity, model-semantics identity, and generator-source identity are three separate questions, and they resolve differently:

- **Artifact identity — intact.** All 33 protected output hashes across the five standard runs match their manifests. Fail-closed validators pass.
- **Model-semantics identity — intact.** Current `core.py` and `m0.py`–`m4.py` blobs equal the audited mathematical reference.
- **Generator-source identity — partial.** The manifests record runs from commit `e0e9a738…` against a dirty worktree, retaining `dirty_diff_sha256`, `porcelain_sha256`, and `source_fingerprint_sha256` but not the dirty bytes themselves. Bounded forensic recovery found fingerprint-exact historical bundles for **E04 and E05**; **E01, E02, and E03 remain `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`.**

**Required disclosure wording (reproducibility statement):** the frozen E01–E05 outputs are content-addressed and verified against their manifests, and the maintained model implementation matches the audited specification; however, for E01–E03 the exact generator-source worktree state at run time is identified by recorded fingerprints only and cannot be reconstructed from the repository history. Independent byte-exact regeneration of E01–E03 is therefore not currently possible. This is a historical reproducibility limitation and is not evidence that the frozen artifacts are altered.

Do not describe E01–E05 as byte-exactly reproducible from source. Do not silently omit the limitation.

---

## G. Removal register — stale manuscript sources

Every item below must be deleted or rewritten before its content can appear in V1.

| Location | Stale content | Required action |
|---|---|---|
| `RESULTS_BY_FINDING_CHAPTER.md:3`, `:27`; `DISCUSSION_CHAPTER.md:3`; `PAPER_REVISION_NOTES.md:8` | `226/357`, `63.3%`, mean learned neutral masking `0.950`, presented as the central finding | **Delete.** The superseding frozen value is 243/357, and by C.3/D.3 it is bounded supplementary coverage, not a headline or a prevalence. The `0.950` figure has no standing in the frozen evidence. |
| `RESULTS_BY_FINDING_CHAPTER.md:15–45`; Discussion limitations | one-run child-bootstrap intervals, superseded n/T/seed descriptions, obsolete E04 K = 8 endpoint comparisons, old direct-ablation claims | **Rewrite** from Section D and the frozen configs, experiment by experiment, with the C.1 inferential unit. |
| `RESULTS_BY_FINDING_CHAPTER.md:37` | intermediate disclosure "allowed" continued informative sampling, as an exploratory bridge | **Rewrite.** E02 shows more d > 0 actions **and** worse full-endpoint selection, modal endpoint discovery, and pooled regret. The bridge reading is plausible but not isolated; it belongs in "plausible but untested". |
| `RESULTS_BY_FINDING_CHAPTER.md:65`; `DISCUSSION_CHAPTER.md:71` | numerical M4 path results (k_m 0 → 0.003 raising final masking 0.304 → 0.712, Δ 0.409, interval 0.338–0.478, 220 learners) used as V1 evidence | **Delete from Results and confirmatory Discussion.** M4 equations may be retained only as future/Track-B architecture. No E06 standard GO exists. |
| `DISCUSSION_CHAPTER.md:99` | M4-derived empirical prediction presented as a V1 prediction | **Delete.** |
| `DISCUSSION_CHAPTER.md:93–99` | E02/E04 statements presented as human predictions | **Relabel** as model-derived hypotheses, not predictions about students. |
| Hand-off analytic DOCX §2.3 / Table 8; literature DOCX §3.2 | binary 50% theorem used to constrain the E05 learned/objective gap | **Remove the exclusion** per Section E. |
| `ARTICLE_V1_E05_INTERPRETATION.md` §6, summary, **Supported** list | "Temperature alone is ruled out"; temperature exclusion listed as supported | **Do not carry into V1** per E.2. Retain §7's multi-action statement and §8's contributor list; relocate fixed temperature into §8. The rest of the note is usable. |

---

## H. Interpretation authorities — recovered

The four per-experiment interpretation notes were supplied on 15 August 2026 and added to the repository at freeze time. **Audit gap G-05 is closed.** They are no longer retired; they are active interpretation authorities at precedence level 3.

| File | SHA-256 (16) | Bytes |
|---|---|---|
| `projects/frontiers_article/ARTICLE_V1_E01_E02_INTERPRETATION.md` | `4ac5d20f9560508d` | 17,786 |
| `projects/frontiers_article/ARTICLE_V1_E03_INTERPRETATION.md` | `ca10fea29ff37a88` | 20,467 |
| `projects/frontiers_article/ARTICLE_V1_E04_INTERPRETATION.md` | `56bd98c1bf55d8ac` | 19,385 |
| `projects/frontiers_article/ARTICLE_V1_E05_INTERPRETATION.md` | `79f735b1ac4a727f` | 16,080 |

### H.1 Variant selection

Two revisions of the E04 and E05 notes were supplied. The later revision was taken for both.

- **E04** — the two revisions differ only editorially (line wrapping, three reworded phrases). The extracted numeric multiset is **identical**; no figure, interval, or threshold differs.
- **E05** — the later revision is editorially tightened and improves one figure's precision, replacing a rounded `0.1577` with the full-precision learned-minus-analytic displacement `0.157736`. It also renumbers sections 12.x → 11.x. No result changed. The earlier revision additionally contained a since-removed sentence attributing the crossing shift to a temperature of 0.25; its removal is consistent with Section E.
- E01/E02 and E03 were supplied in a single revision each (duplicate downloads were byte-identical).

### H.2 Concordance with this freeze

The notes were checked against the audit's gap register. They are broadly concordant and add genuine theoretical framing that the evidence matrix does not carry:

- **E03 note** independently states that `243/357` is a tested-grid count and "not a prevalence estimate", excludes information-matched failure and irreversibility, and rules M4/endogenous-receptivity evidence out of E03 — matching C.3, C.8, and I.2/I.3.
- **E01/E02 note** states the final-window contrast `−0.000343` spans zero and that no persistent-mask subregion was established — matching D.1 and I.4.
- **E04 note** lands on scarcity/discovery/representation as a conjunction and rejects "context count itself causes masking" and literal human sequential search — matching D.4 and I.6.

Two carve-outs apply, in which this freeze overrides the notes:

1. **E05 §6 / summary / Supported list** — the temperature exclusion. Superseded per E.2. This is the only substantive conflict found.
2. **E01/E02 note, mechanism-plus-welfare phrasing** — the note presents reduced sampling and increased regret as two coordinate outcomes. Section C.5 governs: they are the same action-frequency information under an exact identity. Report one estimand and translate. The equivalent constraint C.6 applies to the note's E02 regret discussion.

Beyond these, the notes may be used freely for framing, theoretical motivation, and the supported/qualified/unsupported boundaries.

### H.3 Other named authorities

The seven previously-missing named authorities (`HANDOFF.md`, `ARTICLE_V1_CURRENT_STATE.md`, `ARTICLE_V1_ANALYTIC_RESULTS.md`, `ARTICLE_V1_LITERATURE_AUDIT.md`, `ARTICLE_V1_CLAIM_LEDGER.md`, `ARTICLE_V1_NEXT_STAGE.md`, `ARTICLE_V1_SOURCE_LEDGER.csv`) are present under `projects/frontiers_article/` and are available for drafting, subordinate to the precedence order in Section A.

**No named Article-V1 authority is now missing.**

---

## I. Prohibited claims — hard list

No Article-V1 sentence may assert any of the following.

1. Applying binary-softmax Proposition G2 to the E05 eight-action across-child modal crossing, or stating that fixed temperature has been ruled out as a contributor.
2. Treating `243/357` — or legacy `226/357` — as human prevalence, learner prevalence, or intrinsic phase-space volume.
3. Describing the E03 comparator as information-matched, or claiming the learner failed relative to the best policy attainable under its own information constraints.
4. Claiming one early rejection caused persistent final masking in E01, or that an exact null was established.
5. Claiming graded disclosure improved endpoint discovery, welfare, or smooth generalization in E02.
6. Claiming K alone proves scarcity causes masking; that global-mask isolates duplicate-mask normalization; or that M3 implements literal human peer-group search.
7. Estimating or implying a hierarchical E05 crossing outside the approved dense range.
8. Using any M4 or E06 numerical result as Article-V1 confirmatory evidence.
9. Presenting E01 sampling and E01 regret, or E02 regret and E02 disclosure, as independent confirmations (C.5, C.6).
10. Presenting any human educational effect, developmental persistence, intervention benefit, or calibrated BFLPE threshold as demonstrated. **Amended 17 August 2026:** this item prohibits *human* effect claims. Discussion of intervention-like **model** manipulations — their frozen magnitudes, their ordering within a shared estimand, and the observable each would require — is governed by `ARTICLE_V1_LEVERAGE_DISCUSSION_AUTHORITY.md` and is permitted under its four-part rule. Items 1–9 above are unchanged.

---

## J. Freeze status

| Item | Status |
|---|---|
| Frozen E01–E05 numerical evidence | **FROZEN AND VERIFIED** — 10/10 summary artifacts hash-match at freeze time |
| Estimand and inferential-unit definitions | **FIXED** (Section C) |
| Maximum defensible wording | **FIXED** (Section D) |
| E05 G2 / temperature exclusion | **RETIRED AS AN ARTICLE-V1 INFERENCE** — descriptive reporting only (Section E) |
| M4/E06 scope leakage | **RESOLVED BY EDITORIAL SCOPE** — deferred future work only |
| Stale manuscript sources | **EXPLICITLY RETIRED AS AUTHORITIES**; rewrite later from frozen evidence (Section G) |
| E01–E03 generator-source provenance | **LIMITATION DOCUMENTED, NOT RESOLVED** (Section F) |
| E04–E05 generator-source provenance | **RECOVERED** |
| Interpretation notes | **RECOVERED AND ACTIVE** — G-05 closed; two carve-outs (Section H) |
| Named Article-V1 authorities | **COMPLETE** — none missing |

Article skeleton construction may proceed from this freeze and its subordinate
authorities. Any later manuscript number not in Section D requires a new
adjudicated matrix row; it may not be introduced from prose, memory, or a
legacy chapter.

**Final status:** `READY_FOR_SHORT_ARTICLE`.
