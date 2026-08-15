# Article V1 Model-Analysis Consistency Audit

**Audit date:** 2026-08-15  
**Scientific scope:** maintained learner and M0-M4 semantics; frozen E01-E05 standard artifacts; Article-V1 interpretation boundaries  
**Excluded from evidence generation:** E06, stochastic experiment reruns, new seeds, new model variants, and Track B  
**Files modified by this audit:** this report only

## A. Executive verdict

**PUBLICATION_BLOCKING_GAP_FOUND**

The maintained learner and all M0-M4 model blobs exactly match the hand-off mathematical reference. The frozen E01-E05 outputs also byte-match every output hash recorded in their manifests, and the headline statistics can be reconstructed from the frozen tables. The numeric E01-E05 results are therefore intact.

Publication is nevertheless blocked by interpretation and provenance gaps:

1. **BLOCKER - E05 binary-softmax theorem misapplication.** The reported E05 `.5` crossing is not a binary softmax probability. It is the across-child fraction whose final-window modal arm is the single good-context authentic arm in a flat eight-action policy. Proposition G2 therefore cannot rule out fixed-temperature/action-set normalization as a contributor to this measured crossing. The empirical crossing remains valid; the causal exclusion does not.
2. **BLOCKER - M4/E06 scope leakage.** The active Article-V1 plan excludes M4/E06 confirmatory results, but the current Results and Discussion source chapters still report numerical M4 path results and use them in the article conclusion.
3. **HIGH - current manuscript sources remain stale.** They retain legacy one-seed/child-bootstrap results, `226/357`, obsolete E04 endpoint comparisons, older sample sizes and RNG descriptions, and claims superseded by E01-E05.
4. **HIGH - exact frozen generator source is not recoverable from current Git state.** E01-E05 manifest source fingerprints do not match the current tree or committed post-run tree. The protected artifacts and current validators pass, but the exact dirty source bundle that generated them is identified only by hashes, not retained bytes or a reconstructible patch.
5. **HIGH - requested interpretation authorities are missing.** `HANDOFF.md`, the six named `ARTICLE_V1_*` authority files, the source ledger, and all four named interpretation notes were not supplied or found. A literal sentence-by-sentence audit of those absent notes is impossible. The 29 local candidate claims in `ARTICLE_V1_EVIDENCE_MATRIX.csv` were audited instead.
6. **HIGH - E03 “learned policy” is often too broad.** The `243/357` classifier uses aggregate final-window Neutral-state action counts across 160 learners, with visit-adequacy and tie rules. It is not a Q-order classifier, an individual-policy prevalence, or an information-matched optimum comparison.
7. **HIGH - E01 does not demonstrate persistent final masking after one rejection.** The final-mask contrast is `-0.000343`, with interval `[-0.011605, 0.010918]`. This is failure to detect an increase, not proof of exact equivalence and not support for a persistent-mask subregion.
8. **MEDIUM - E01 sampling and normalized regret are algebraically redundant.** In the authenticity-optimal binary cells, normalized pseudo-regret is exactly the fraction of suboptimal mask actions. Because the first action is forced authentic, `0.025824 = -(1999/2000)(-0.025837)` up to stored precision. These are not independent mechanism and welfare confirmations.
9. **MEDIUM - E02 normalized regret is also a disclosure-distance identity.** In the affine, authenticity-optimal strata, normalized regret equals the horizon mean of `1-d`. It is a valid objective-loss scale but not independent evidence beyond mean disclosure intensity.
10. **MEDIUM - E04/E05 modal metrics count deterministic argmax ties.** The primary `argmax` outcome does not require a unique modal arm. Frozen strict-unique diagnostics support the same direction, but those checks are post hoc and must not silently replace the prespecified estimands.

The top five blockers before manuscript continuation are therefore: (1) remove the E05 temperature exclusion or test an appropriate counterfactual; (2) remove all M4/E06 Results evidence from V1; (3) rewrite from the E01-E05 evidence matrix rather than legacy chapters; (4) resolve/archive the exact generator-source provenance; and (5) supply or retire the missing interpretation authorities.

## B. Provenance state

### B.1 Repository state

| Item | Observed state | Audit consequence |
| --- | --- | --- |
| Branch | `codex/frontiers-stage2-e06` | Article audit is being performed on an E06-oriented branch; this does not change E01-E05 artifacts. |
| HEAD | `441cfe44856d0cbc3da57089cbe91755b0cc4780` | Exactly equals the mathematical hand-off reference commit. |
| Worktree | Dirty | Existing changes are concentrated in E06/M4 governance, `experiments/e06.py`, `tests/test_article_e06.py`, and E06 smoke artifacts; this audit did not modify them. |
| E01-E05 model/config/artifact paths | No pre-existing local modifications | The protected E01-E05 files inspected here were not dirty. |
| New hand-off documents | Untracked `.docx` files under `doc-reviews/handoff_august2026/` | Read as candidate hand-off authorities; not edited. |
| New Article-V1 audit set | Untracked files under `projects/frontiers_article/` | Used as the current local evidence/adjudication set because the specifically named hand-off Markdown files are absent. |

### B.2 Model/core semantic comparison

Current Git blob hashes exactly equal the mathematical-reference blobs:

| File | Reference/current blob | Semantic status |
| --- | --- | --- |
| `src/gifted_masking/core.py` | `f25723fed941a4c6cd8338f076a1b2d97d67041f` | Exact match; no semantic change |
| `src/gifted_masking/models/m0.py` | `a142fc04aee3451bca50d110d3ea0fda1c0972e4` | Exact match; no semantic change |
| `src/gifted_masking/models/m1.py` | `e64546cad9db5d376326ea3dea461daf0b926c10` | Exact match; no semantic change |
| `src/gifted_masking/models/m2.py` | `91df8ae77a3555b060732ff059eb94f2bd525e33` | Exact match; no semantic change |
| `src/gifted_masking/models/m3.py` | `d4b38cb0620460d096d7fd6f1b005b00a7c1949a` | Exact match; no semantic change |
| `src/gifted_masking/models/m4.py` | `df61944a8b3f71a1a339399486ad23b3e022ee0d` | Exact match; Track-B mathematics only |

No hand-off result is invalidated by a maintained model semantic change.

### B.3 Frozen artifact identity

Every publication-bearing output named by the five manifests was rehashed. All recorded hashes match. Primary identities are:

| Experiment | Raw SHA-256 | Primary summary SHA-256 | Manifest SHA-256 | Status |
| --- | --- | --- | --- | --- |
| E01 | `a4e78dcf4094e03ed36fbb0e3cfbebecdc427247810cc359d6a4b5bfa362dc01` | effects `4ce67da8b48e8d770388db9e2c6ebe240b868c0696ba90678cc9940de02684d8` | `3f48573a2df3c08c0b7e1c2310836ca740966ad2cae1cef12f6b8dddde514e34` | PASS |
| E02 | `3640b1a83605791916ec150be66ef578bc100cee08b6b61f909d2a7ff2220619` | effects `11d29c72508649a174b285957dfec3752edff76a099aa76de9f6fe3a4e515a8a` | `be541067611990b0d9dc5388ee731152ea3eac27fd5a66fcceba45c4b13e834e` | PASS |
| E03 | `9561ff20d91cd07cc57f61db9bdb60072ea8b381bcb43968825932c30da6d150` | effects `5a1ee392560e94695dfe0d04ff89caeafdb0b58fa2b70e6def365726d66ab3af`; stable `91814ab4430f63bc5e46596c61718e1fec6705d355b6cab3d8c18d29c1dfaea7` | `18aa7b6993af0c9f0df0d5cbc0e50b467959a13d17aaec156b1c8e5cb8242646` | PASS |
| E04 | `621227ffeac600ffbfc85852ef2784d4e409880e329ff4b6d947553e2b4e419e` | effects `dd426992f0a1a0ae05542756dc6dca918fbf56a589347676a93a309d08a41d44` | `abf6fa747869ab1e2258d3321dcb0a888d06b5a61edd88e4661791a88c249d71` | PASS |
| E05 | `9de41835a72986fc5ca7cbd591a16ed3781a3cfdd24f194d126b27012bafb947` | transitions `96b8d8dc1cf27e3a226282e4d8755effde74e855d81b8f8bbc6db6515c607097`; effects `33eb752c89d87ce79ef13bfe196623fb4d4f53c4fff63e03b84af413a68200d5` | `cc600fd4158ea447e6b08024c545489e5b02f64522a1b37314d22745fbe190d3` | PASS |

Config byte hashes and manifest `config_sha256` values intentionally differ: the former hash the literal file and the latter hash normalized JSON. Both reconcile to the same frozen values.

### B.4 Generator-source provenance qualification

The manifests record runs from commit `e0e9a738...` with a dirty worktree. The E01-E05 experiment/config files did not exist in that commit and were later committed. Current source fingerprints differ from all five recorded run fingerprints. The manifests retain dirty-diff hashes and source-fingerprint hashes, but not the exact dirty patch/bytes needed to reconstruct those fingerprints.

This does **not** create a model-semantics mismatch: model blobs match, raw and derived artifacts match their protected hashes, and current fail-closed validators pass. It does create an `ARTIFACT_PROVENANCE_GAP`: a third party cannot recover the exact generator source tree solely from Git plus the manifest.

### B.5 Authority availability

Available and read:

- `ARTICLE_V1_SCIENTIFIC_ANALYTIC_RESULTS_AND_PROOFS_2026-08-14.docx`;
- `Gifted_Masking_Literature_Audit_Current_State_2026-08-14.docx`;
- `projects/frontiers_article/ARTICLE_V1_EXECUTION_PLAN.md`;
- `ARTICLE_V1_EVIDENCE_AUDIT.md`, `ARTICLE_V1_EVIDENCE_MATRIX.csv`, and `ARTICLE_V1_INFERENTIAL_AUDIT.md`;
- `CLAIM_LEDGER.md`, `CURRENT_STATE.md`, `RDS.md`, E01-E05 configs, manifests, reports, raw/derived tables, implementation, and tests.

Not found:

- `HANDOFF.md`;
- `ARTICLE_V1_CURRENT_STATE.md`;
- `ARTICLE_V1_LITERATURE_AUDIT.md`;
- `ARTICLE_V1_ANALYTIC_RESULTS.md`;
- `ARTICLE_V1_CLAIM_LEDGER.md`;
- `ARTICLE_V1_NEXT_STAGE.md`;
- `ARTICLE_V1_SOURCE_LEDGER.csv`;
- `ARTICLE_V1_E01_E02_INTERPRETATION.md`, `ARTICLE_V1_E03_INTERPRETATION.md`, `ARTICLE_V1_E04_INTERPRETATION.md`, and `ARTICLE_V1_E05_INTERPRETATION.md`.

The statement matrix below is complete for the 29 local candidate claims in `ARTICLE_V1_EVIDENCE_MATRIX.csv`; it cannot be a literal sentence audit of absent files.

## C. Experiment verdict table

| Experiment | Model contract | Evidence | Inference | Current interpretation | Overall |
| --- | --- | --- | --- | --- | --- |
| E01 | PASS | PASS | PASS_WITH_QUALIFICATION: five master effects; accepted/rejected strata are not paired children | GAP: sampling/regret pass, final-mask persistence does not; regret is algebraically redundant with action sampling | PASS_WITH_QUALIFICATION |
| E02 | PASS | PASS | PASS_WITH_QUALIFICATION: five paired master effects with equal p weighting | GAP if called ladder climbing, smooth generalization, or independent welfare improvement | PASS_WITH_QUALIFICATION |
| E03 | PASS | PASS | PASS_WITH_QUALIFICATION: grid cells are not independent inferential units; zero-width seed interval is selected-stream stability only | GAP unless “learned masking” is defined as aggregate final-window Neutral action majority versus full-information DP | PASS_WITH_QUALIFICATION |
| E04 | PASS | PASS | PASS_WITH_QUALIFICATION: five master-level K contrasts; prespecified metric permits non-unique argmax ties | GAP if called generic performance decline, pure scarcity identification, or literal sequential peer search | PASS_WITH_QUALIFICATION |
| E05 | PASS | PASS | PASS for the empirical PAVA/bootstrap crossing | CONTRADICTION for applying binary G2 to an eight-action, across-child modal response; numerical flat result remains valid | CONTRADICTION / BLOCKER |

## D. Statement-level audit

Source abbreviations: `EV` = `projects/frontiers_article/ARTICLE_V1_EVIDENCE_MATRIX.csv`; `A` = hand-off analytic DOCX; `CL` = `projects/frontiers_article/CLAIM_LEDGER.md`. Configs are the corresponding `configs/frontiers_article/*_standard.json` files. Every simulation row below uses the frozen effect/transition selector stated in `EV` and the five experiment-specific master seeds.

### D.1 E01

| ID | Exact statement | Evidential level | Model/config/evidence/analytic source | Inferential unit | Verdict | Gap / severity | Maximum defensible wording | New science? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01-C2-SAMPLING | Initial rejection reduced later authentic sampling in the tested M0 domain. | INFERENTIAL_RESULT | `article.py:simulate_e01_cell,_e01_effects`; E01 config; EV selector `rejected_minus_accepted_post_initial_authentic_rate`; A M0 | master-specific rejected-minus-accepted stratum contrast, equal-weight p=.75/.85; n=5 masters | PASS | NONE | Initial rejection reduced post-initial authentic action rate by `0.025837` in the tested p=.75/.85 domain. | NO |
| E01-C2-REGRET | Initial rejection increased normalized objective pseudo-regret. | INFERENTIAL_RESULT | `article.py:simulate_e01_cell`; E01 config/effects | same five master contrasts | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / MEDIUM | Rejection increased static objective pseudo-regret normalized by `T*|E_auth-E_mask|` by `0.025824`; in these binary cells this is exactly the whole-horizon suboptimal-mask fraction and is not independent of sampling. | NO |
| E01-C2-FINAL-MASK | One initial rejection did not measurably increase final-window masking. | INFERENTIAL_RESULT | E01 effects; final steps 1600-1999 | same five master contrasts | PASS_WITH_QUALIFICATION | TERMINOLOGY_OVERREACH / MEDIUM if called “genuinely null” | No increase was detected: rejected-minus-accepted `-0.000343`, 95% t interval `[-0.011605,0.010918]`. No equivalence margin was tested. | NO |
| E01-C2-FORCED-MASK | Forced authentic exploration reduced final masking after rejection. | INFERENTIAL_RESULT | E01 effects, forced condition | rejected-stratum baseline-minus-intervention per master; n=5 | PASS_WITH_QUALIFICATION | CAUSAL_OVERREACH / LOW outside model | Five-percent forced authentic exploration reduced model final masking by `0.046590` in the rejection stratum. | NO |
| E01-C2-FORCED-REGRET | Forced authentic exploration reduced regret after rejection. | INFERENTIAL_RESULT | E01 effects | same | PASS_WITH_QUALIFICATION | TERMINOLOGY_OVERREACH / LOW | It reduced normalized objective pseudo-regret by `0.057954`; this is a model information manipulation, not a human intervention estimate. | NO |
| E01-C2-CF-MASK | Counterfactual authentic feedback reduced final masking after rejection. | INFERENTIAL_RESULT | E01 effects, counterfactual condition | same | PASS_WITH_QUALIFICATION | CAUSAL_OVERREACH / LOW outside model | Counterfactual authentic feedback reduced model final masking by `0.118135` after rejection. | NO |
| E01-C2-CF-REGRET | Counterfactual authentic feedback reduced regret after rejection. | INFERENTIAL_RESULT | E01 effects | same | PASS_WITH_QUALIFICATION | TERMINOLOGY_OVERREACH / LOW | It reduced normalized objective pseudo-regret by `0.141318` in the tested model stratum. | NO |
| E01-C3-LAMBDA | Greater negative-outcome weighting increased final masking without changing objective payoff. | INFERENTIAL_RESULT | `core.py:subjective_value`; E01 maintained p=.65 cells | lambda 2.5-minus-.5 contrast per master; n=5 | PASS | NONE | At p=.65, increasing lambda from .5 to 2.5 increased final masking by `0.402990`; lambda changes updates, not environmental rewards. | NO |
| E01-C3-GAP | Loss weighting did not measurably amplify the controlled early-rejection mask gap. | INFERENTIAL_RESULT | E01 effects | difference-in-differences per master; n=5 | PASS_WITH_QUALIFICATION | TERMINOLOGY_OVERREACH / LOW | The amplification contrast was `-0.001067`, interval `[-0.015031,0.012898]`; no amplification was detected. | NO |

### D.2 E02

| ID | Exact statement | Evidential level | Model/config/evidence/analytic source | Inferential unit | Verdict | Gap / severity | Maximum defensible wording | New science? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E02-C4-EXPLORATION | Graded arms increased nonzero disclosure relative to binary full-authentic resampling after rejection. | INFERENTIAL_RESULT | `m1.py`; `e02.py:simulate_e02_cell,_e02_effects`; A M1; E02 config/effects | paired architecture contrast within master/p/rejected stratum; n=5 masters | PASS_WITH_QUALIFICATION | TERMINOLOGY_OVERREACH / MEDIUM if called “protective” | Independent graded arms increased `d>0` post-rejection action rate relative to binary `d=1` by `0.255040`. This is exposure distribution, not endpoint discovery. | NO |
| E02-C4-FULL-ENDPOINT | Graded arms reduced full-authentic final-window selection. | INFERENTIAL_RESULT | E02 effects | same, final steps 1600-1999 | PASS | NONE | Graded-minus-binary full-authentic final-window rate was `-0.328692` in authenticity-optimal p=.75/.85 strata. | NO |
| E02-C4-MODAL | Graded arms reduced optimal-endpoint modal probability. | INFERENTIAL_RESULT | E02 effects; per-child unique modal rule | same | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / LOW if equated with partial disclosure | Probability that a unique final-window modal action was the optimal `d=1` endpoint was lower by `0.221740`; this does not by itself identify which nonoptimal action was modal. | NO |
| E02-C4-REGRET | Graded arms did not improve pooled normalized regret. | INFERENTIAL_RESULT | `e02.py` regret formula/effects; A affine M1 result | same | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / MEDIUM | Binary-minus-graded normalized pseudo-regret was `-0.029761`, so graded was worse. In these affine authenticity-optimal cells normalized regret is exactly mean endpoint distance `1-d`, not an independent outcome. | NO |

### D.3 E03

| ID | Exact statement | Evidential level | Model/config/evidence/analytic source | Inferential unit | Verdict | Gap / severity | Maximum defensible wording | New science? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E03-C5-GRID | Default M2 learner masked where the full-information dynamic optimum selected authenticity in a stable tested-grid regime. | FROZEN_SIMULATION_RESULT | `m2.py`; `m2_optimal.py`; `e03.py:classify_e03_cell,summarize_e03_standard_classifications`; E03 grid/effects/stable tables; A M2 | one 357-cell classification fraction per master; n=5 masters | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / HIGH | In 243 of 357 frozen cells, aggregate final-window Neutral action counts favored masking while objective value iteration favored authenticity; all five selected masters gave that cell count. | NO |
| E03-C5-STABILITY | Exact-grid classification was stable across masters except seven inadequate-visit cells. | FROZEN_SIMULATION_RESULT | E03 stable table | 4-of-5 cell label across five masters | PASS | NONE | 350/357 cells had a stable classification; seven low-p, eta=0 cells were inconclusive because Neutral visits failed the prespecified adequacy rule. | NO |
| E03-C5-THRESHOLDS | Objective M2 authenticity becomes Neutral-state optimal below the static M0 threshold. | FULL_INFORMATION_DP_RESULT | `m2_optimal.py:solve_m2_value_iteration`; E03 thresholds; A M2 | deterministic DP per eta | PASS | NONE | Objective thresholds are bracketed near `.38394`, `.33878`, and `.26901` for eta 0, .2, and .8, versus static `43/60`; no learned threshold was estimated. | NO |
| E03-C5-GAMMA | Learned-suboptimal classification depends on discounting. | FROZEN_SIMULATION_RESULT | E03 sentinel cells | prespecified sentinel classifications across five masters | PASS_WITH_QUALIFICATION | TERMINOLOGY_OVERREACH / LOW | At gamma=.5 three sentinels changed because the objective DP action changed to masking; this is not improved learning. | NO |
| E03-C5-ALPHA-TAU | Specified alpha and tau perturbations changed some sentinel classifications. | FROZEN_SIMULATION_RESULT | E03 sentinel cells | sentinel by master | PASS_WITH_QUALIFICATION | PARAMETER_REGION_OVERREACH / MEDIUM | Named alpha=.03 and tau=.6 cases changed specific sentinels; no general monotonic learner claim follows. | NO |
| E03-C5-HARSH | Objective M2 masking despite static M0 authenticity occurred at one harsh sentinel. | FROZEN_SIMULATION_RESULT | E03 harsh cells and objective DP | five master classifications at p=.75 plus deterministic DP | PASS_WITH_QUALIFICATION | PARAMETER_REGION_OVERREACH / HIGH if generalized to a region | At `b2=0,r2=8,delta=.3,eta=0,p=.75`, objective Neutral Q(auth-mask) was `-0.406293`; do not extrapolate a closed structural-lock region. | NO |

### D.4 E04

| ID | Exact statement | Evidential level | Model/config/evidence/analytic source | Inferential unit | Verdict | Gap / severity | Maximum defensible wording | New science? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E04-C6-FLAT | Increasing K reduced good-authentic settling in flat 2K search. | INFERENTIAL_RESULT | `e04.py:simulate_e04_cell,e04_effects`; E04 config/effects; A M3 K invariance | K16-minus-K1 argmax fraction per master; n=5 | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / MEDIUM | In fixed-one flat 2K, the fraction whose final-window argmax arm was good-authentic fell by `0.234000`; the metric permits ties. | NO |
| E04-C6-HIER | Increasing K reduced good-authentic settling in hierarchical search. | INFERENTIAL_RESULT | same, hierarchical path | same | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / MEDIUM | The corresponding hierarchical argmax-fraction change was `-0.470400`; do not call it generic “performance.” | NO |
| E04-C6-CONTROLS | K effects were practically absent when masking was global or the good context was known. | INFERENTIAL_RESULT | E04 effects | per-master global-mask endpoint; known-good structural control | PASS_WITH_QUALIFICATION | ARCHITECTURE_OVERREACH / MEDIUM | Global-mask changed by `+0.0088`, inside the prespecified equivalence band; known-good is structurally K-invariant. Global-mask changes the whole action set, not duplicate-mask normalization alone. | NO |
| E04-C6-IDENTITY | Search decline survived randomized receptive-context identity. | INFERENTIAL_RESULT | E04 randomized-minus-fixed slopes | per-master slope difference | PASS | NONE | Randomizing good-context labels did not materially change flat or hierarchical K slopes; this rules against a fixed-label artifact in this design. | NO |
| E04-C6-MULTIPLE | More receptive contexts attenuated search burden. | INFERENTIAL_RESULT | E04 two-good and proportional-25 effects | per-master slope contrasts | PASS_WITH_QUALIFICATION | CAUSAL_OVERREACH / MEDIUM | Two good contexts attenuated slopes and proportional-25 slopes were near zero. Combined controls support representation-dependent burden under scarcity; the original K manipulation alone does not identify scarcity. | NO |

### D.5 E05

| ID | Exact statement | Evidential level | Model/config/evidence/analytic source | Inferential unit | Verdict | Gap / severity | Maximum defensible wording | New science? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E05-C7-ANALYTIC | Objective good-context authenticity equals masking at bf=8/17. | EXACT_MODEL_RESULT | `m3.py:expected_reward_for_action`; `e05.py:analytic_values`; A M3 | deterministic | PASS | NONE | Under frozen payoffs, `R_G-R_M=.40-.85bf`; global full-information crossover is exactly `8/17`. | NO |
| E05-C7-CROSSING | Flat-2K learned response crossed .5 before objective indifference. | INFERENTIAL_RESULT | `e05.py:simulate_e05_cell,_transition_rows,e05_bootstrap_transition`; E05 config/transitions | one complete 16-point dense modal-response curve per master; n=5, bootstrap resamples masters | PASS_WITH_QUALIFICATION | ANALYTIC_OVERREACH / BLOCKER for G2 causal exclusion | The fraction of learners whose final-window argmax was arm 1 crossed .5 at `.312852` (`.307836-.316918`) before `.470588`. This is an eight-action aggregate modal statistic, not binary softmax `P(A)`. | NO for descriptive claim; YES to isolate cause |
| E05-C7-GAP | Authenticity retained about .134 objective advantage at the learned crossing. | EXACT_MODEL_RESULT | exact `.40-.85bf` evaluated at empirical crossing | conditional deterministic transform of bootstrap-estimated crossing | PASS_WITH_QUALIFICATION | STATISTIC_DEFINITION_GAP / LOW | Conditional on the point crossing, advantage is `0.134076`; transforming its bootstrap bounds gives approximately `[0.130620,0.138340]`, which captures crossing Monte Carlo uncertainty only. | NO |
| E05-C7-ENDPOINT | Flat good-auth modal response declined sharply from bf=0 to .80. | INFERENTIAL_RESULT | E05 effects | paired endpoint effect per master; n=5 | PASS | NONE | Argmax fraction changed by `-0.9400` (`-0.957993,-0.922007`); keep secondary to the dense transition. | NO |
| E05-C7-HIER-CENSOR | No hierarchical learned crossing was estimable inside the dense range. | INFERENTIAL_RESULT | E05 transitions | five hierarchical curves/bootstrap | PASS | NONE | Hierarchical response was already `.1176` at bf=.30; the in-range crossing is left-censored, not absent globally. | NO |

### D.6 Current prose statements outside the 29-row matrix

| Statement/location | Level | Verdict | Gap class / severity | Maximum defensible replacement |
| --- | --- | --- | --- | --- |
| `RESULTS_BY_FINDING_CHAPTER.md:3,27` and `DISCUSSION_CHAPTER.md:3` use `226/357`, `63.3%`, and legacy mean mask `.950` as a central result. | HUMAN_INTERPRETATION | CONTRADICTION | STALE_NUMBER + INFERENTIAL_UNIT_MISMATCH / HIGH | Use the bounded E03 operational result if needed; do not headline `243/357` or call it prevalence. |
| `RESULTS_BY_FINDING_CHAPTER.md:15-45` and Discussion limitations retain one-run child-bootstrap numbers and old n/T/seed descriptions. | HUMAN_INTERPRETATION | CONTRADICTION | STALE_NUMBER + ARTIFACT_PROVENANCE_GAP / HIGH | Rewrite from E01-E05 config, manifest, and effect rows experiment by experiment. |
| `RESULTS_BY_FINDING_CHAPTER.md:37` says intermediate disclosure “allowed” continued informative sampling as an exploratory bridge. | HUMAN_INTERPRETATION | GAP | CAUSAL_OVERREACH / HIGH | E02 shows more `d>0` actions but worse full-endpoint selection and pooled regret; lower exposure as the cause/benefit is plausible, not isolated. |
| `RESULTS_BY_FINDING_CHAPTER.md:63-69` and `DISCUSSION_CHAPTER.md:69-77` report M4 numerical path results. | HUMAN_INTERPRETATION | CONTRADICTION | SCOPE_VIOLATION / BLOCKER | Remove from Article-V1 Results/confirmatory Discussion; retain M4 equations as future/Track-B architecture only. |
| `DISCUSSION_CHAPTER.md:93-99` presents E02-E04-M4 statements as human predictions. | HUMAN_INTERPRETATION | PASS_WITH_QUALIFICATION / M4 contradiction | CAUSAL_OVERREACH; SCOPE_VIOLATION for M4 / HIGH-BLOCKER | Label E01-E05 translations as model-derived hypotheses; omit M4-derived prediction from V1. |
| Hand-off analytic DOCX Section 2.3/Table 8 and literature DOCX Section 3.2 use the binary 50% theorem to constrain the learned/objective E05 gap. | EXACT_LEARNER_IDENTITY applied to interpretation | CONTRADICTION | ANALYTIC_OVERREACH / BLOCKER | G2 applies only to a two-action softmax probability. E05's modal-population crossing needs its own decomposition; fixed tau/action-set normalization is not ruled out. |

## E. Exact model verification

### E.1 Shared learner

- `subjective_value` implements `phi_lambda(R)=R` for `R>=0` and `lambda*R` for `R<0`; `lambda<0` is rejected. Lambda affects only the Q target, not objective reward fields.
- `lambda=0` is accepted by the transform and maps negative rewards to zero. `m0.subjective_indifference_r` is not domain-safe at `lambda=0` or `p=1` and can divide by zero; it is not used in E01-E05 frozen production evidence.
- Q updates use constant alpha. Stateless models use `Q_a <- Q_a + alpha(phi(R)-Q_a)`. M2 uses `Q(s,a) <- Q(s,a)+alpha[phi(R)+gamma max Q(s',.)-Q(s,a)]`.
- Softmax divides Q by positive temperature, subtracts each row maximum, exponentiates, normalizes across all available actions, and samples by cumulative probabilities. It is numerically stable for finite Q.
- For exactly two actions, `P(A)=.5 iff Q_A=Q_M`. For K actions, `pi_i=.5 iff Q_i=tau log(sum_{j!=i} exp(Q_j/tau))`. E05 does not directly measure either quantity: it thresholds an across-child final-window modal classification.

### E.2 M0

Implementation gives:

`R_M=b-c`, `E[R_A]=p(b+a)+(1-p)(a-r)`, and `Delta_0=a+c-(1-p)(b+r)`.

At defaults, `R_M=.75`, `E[R_A]=-1.4+3p`, and `p*_obj=43/60=.716666...`. Endpoints p=0 and p=1 yield `a-r` and `b+a`. If r=0 and a>=0, rejected authenticity is nonnegative and is not loss-weighted.

Under `a-r<0`, the learner-side transformed-reward boundary is

`p*_lambda=[(b-c)-lambda(a-r)]/[(b+a)-lambda(a-r)]`.

At defaults it is `(15+28lambda)/(32+28lambda)`: `.63043` at lambda=.5, `43/60` at lambda=1, and `.83333` at lambda=2.5. It is an update-target boundary, not a finite-horizon behavioral threshold.

### E.3 M1

Implementation gives `q(d)=1-(1-p)d` and

`E[R(d)]=b-c+d[a+c-(1-p)(b+r)]`.

The grid includes exact 0 and 1. The expected reward is affine, so every strict static optimum is an endpoint and the objective optimum/value is invariant to action count when endpoints remain present. Q-values are independent by arm: there is no interpolation, shared parameter, or generalized update.

### E.4 M2

With state order Neutral, Accepted, Stigmatized, transition rows are:

| Current state | Mask | Authentic |
| --- | --- | --- |
| Neutral | `(1,0,0)` | `(0,p,1-p)` |
| Accepted | `(delta,1-delta,0)` | `(delta,1-delta,0)` |
| Stigmatized | `(eta,0,1-eta)` | `((1-p/2)eta,p/2,(1-p/2)(1-eta))` |

Reward is determined first from the current state/action/outcome. Accepted turnover changes the next state only. In Stigmatized, redemption to Accepted takes precedence; eta escape is then applied only if the next state remains Stigmatized. The production DP table matches that order.

Accepted-state actions have identical transitions, so `Q(A,auth)-Q(A,mask)=a+c=.85` exactly. Neutral and Stigmatized dynamic-gap decompositions in the hand-off authority match implementation.

Independent deterministic verification enumerated the four relevant stationary policies (Accepted fixed to authenticity) for all 357 frozen p/eta cells. The componentwise policy-value envelope matched production value iteration with maximum absolute discrepancy `8.99e-10`; no cell exceeded `2e-8`.

The comparator is full-information objective DP. It is not `pi_I*`, does not share the learner's information limits, and does not by itself separate information cost from algorithmic inefficiency.

### E.5 M3

Implementation gives `R_M=.75`, `R_G=1.15-.85bf`, and `R_B=-.8` under defaults. Increasing K with one fixed good context changes multiplicities only; the distinct value set and `max(R_M,R_G,R_B)` are K-invariant. Good versus mask crosses at `8/17`; good versus bad crosses at `39/17`, so bad authenticity is not the competitor in E05's range.

Action semantics:

- flat: one softmax over 2K joint context-behavior arms;
- hierarchical: one K-way context softmax followed in the same trial by a two-way behavior softmax conditional on context; both Q tables receive the same realized reward;
- global mask: one mask arm plus K context-authentic arms;
- fixed known good: a two-arm problem with no context choice.

The model is repeated joint/context choice with learned values, not literal human movement through available peer groups. Global-mask changes action count, initial aggregate probabilities, competition, and update allocation; it does not isolate duplicate-mask normalization alone.

### E.6 M4 - Track B only

The maintained implementation applies reward and the selected Q update first, then updates receptivity. Receptivity is clipped to `[p_min,p_max]`. For coefficients in `[0,1]`, each un-clipped update is already a convex combination within the interval.

Under pure masking, deterministic verification matched

`p_t-p_min=(1-k_m)^t(p_0-p_min)`

to `2.22e-16` after 37 steps in a check case. Exact two-outcome evaluation of authentic drift matched `p*k_a(p_max-p)-(1-p)k_r(p-p_min)` with zero numerical discrepancy. These are Track-B mathematical checks only, not Article-V1 evidence.

## F. Artifact/statistic verification

| Number | Exact meaning | Artifact/config/analysis | Inferential unit and uncertainty | Verdict |
| --- | --- | --- | --- | --- |
| E01 `-0.025837` | rejected-minus-accepted post-initial authentic action rate, steps 1-1999, equal-weight p=.75/.85, controlled baseline lambda=1 | E01 effects row; E01 config; `_e01_effects` | five master-specific stratum contrasts; Student-t `[-.035753,-.015922]` | PASS |
| E01 `+0.025824` | rejected-minus-accepted cumulative static objective pseudo-regret divided by `T*abs(gap)` | same | five masters; `[.015914,.035735]` | PASS_WITH_QUALIFICATION: exactly scaled negative of preceding sampling contrast |
| E01 `-0.000343` | rejected-minus-accepted final-window mask rate, steps 1600-1999 | same | five masters; `[-.011605,.010918]` | PASS: no detected increase; not equivalence |
| E02 `+0.255040` | graded `d>0` post-initial rate minus binary `d=1` post-initial rate, rejected t0 stratum, equal-weight p=.75/.85 | E02 effects; `_e02_effects` | five paired master effects; `[.253004,.257077]` | PASS_WITH_QUALIFICATION |
| E02 `-0.328692` | graded-minus-binary final-window full-authentic action rate in the same authenticity-optimal strata | same | five paired master effects; `[-.342037,-.315348]` | PASS |
| E02 `-0.221740` | graded-minus-binary probability that the unique final-window modal arm is the cell's objective endpoint; here d=1 | same | five paired master effects; `[-.288755,-.154724]` | PASS |
| E03 `243/357` | per master, 243 cells where aggregate final-window Neutral mask count exceeds authentic count, visits are adequate, and DP says authentic; 243 also stable across all five | E03 cells/effects/stable; 21 p x 17 eta grid | five selected master grid fractions; stored t interval collapses to point | PASS_WITH_QUALIFICATION: tested grid, not prevalence |
| E04 `-0.2340` | K16-minus-K1 change in mean `settled_any_good_auth_argmax` for flat 2K, fixed identity, one good context | E04 effects; `e04_effects` | five master endpoint contrasts; `[-.246417,-.221583]` | PASS_WITH_QUALIFICATION: behavior fraction, nonunique argmax |
| E04 `-0.4704` | same outcome/contrast for hierarchical architecture | same | five masters; `[-.511031,-.429769]` | PASS_WITH_QUALIFICATION |
| E05 `0.312852` | bf where equal-n nonincreasing PAVA of pooled `modal_good_auth_argmax_fraction` crosses .5 in flat 2K, dense bf=.30-.65 | E05 transitions/config; `_transition_rows` | five complete master curves | PASS |
| E05 `[.307836,.316918]` | 2.5/97.5 percentiles of 10,000 architecture-isolated resamples of five complete master curves | `e05_bootstrap_transition` | master curve is resampling unit; 10,000/10,000 valid | PASS |
| E05 `8/17` | exact environmental equality `R_G=R_M=.75` under defaults; bad authenticity remains -.8 | E05 analytic table; `analytic_values` | deterministic | PASS |
| E05 `~.134` | `.40-.85(.312852)=.1340757`, conditional on empirical point crossing | exact transform; no independent artifact row | inherits crossing uncertainty; transformed bounds `[.130620,.138340]` | PASS_WITH_QUALIFICATION |

### F.1 Critical regret identities

For E01 p=.75/.85, authenticity is optimal and each mask action incurs exactly `abs(E_auth-E_mask)` pseudo-regret. Therefore

`normalized_regret = number_of_mask_actions / T`.

The forced t=0 action is authentic in both strata, so

`rejected-minus-accepted normalized regret = -(T-1)/T * (rejected-minus-accepted post-initial authentic rate)`.

With T=2000, this exactly maps `-0.025837042306...` to `+0.025824123785...`. The prose may discuss the same behavior in action-frequency or normalized-objective-loss units, but must not treat them as independent replications.

For E02 in p=.75/.85, M1's affine slope is the endpoint gap, so per-step normalized regret is exactly `1-d`. Thus the normalized-regret architecture contrast is a horizon-average disclosure-distance contrast. It is objectively meaningful, but it is not independent evidence for a separate welfare mechanism.

## G. Gap register

| ID | Severity | Gap class | Affected claim | Actual evidence / why wording is wrong or uncertain | Maximum defensible replacement | Documentation-only? | New science required? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G-01 | BLOCKER | ANALYTIC_OVERREACH | E05: fixed temperature alone cannot explain measured .5 displacement | Response is across-child modal-arm fraction in flat K=4/8 actions, not binary softmax probability. G2 does not apply. | Report descriptive learned/objective separation only; list temperature/action-set normalization among unresolved contributors. | Yes to remove exclusion | Yes to isolate contribution |
| G-02 | BLOCKER | SCOPE_VIOLATION | M4 confirms V1 path dependence/endogenous feedback | Active V1 plan excludes E06/M4 Results, but current chapters report numerical M4 results and conclusions. | M4 architecture/equations are future/Track-B context only. | Yes | NO |
| G-03 | HIGH | STALE_NUMBER | Current Results/Discussion E01-E04 values | Chapters use legacy `226/357`, child bootstrap, old n/T/seeds, old E04 K=8 effects, and old direct-ablation claims. | Rewrite from the content-addressed E01-E05 matrix and configs. | Yes | NO |
| G-04 | HIGH | ARTIFACT_PROVENANCE_GAP | Exact reproducibility of frozen generators | Manifest source fingerprints do not match current/committed source; exact dirty run tree is not retained. | Archive exact source bytes/patch matching each manifest fingerprint or issue a provenance amendment after approved reproduction. | No | A deterministic reproduction/provenance action is required; no new scientific design |
| G-05 | HIGH | ARTIFACT_PROVENANCE_GAP | Complete statement audit | Named hand-off Markdown and interpretation-note files are absent. | Supply them or formally retire them in favor of the local evidence matrix. | Yes | NO |
| G-06 | HIGH | STATISTIC_DEFINITION_GAP | E03 “learned policy” | Classifier is aggregate final-window Neutral action majority with visit adequacy, not Q ordering or individual policy. | “Aggregate final-window Neutral behavior favored masking while full-information DP favored authenticity.” | Yes | NO |
| G-07 | HIGH | EMPIRICAL_OVERREACH | E01 persistent final masking / persistent p subregion | Final-mask interval spans zero; only p=.75/.85 were tested for controlled initial outcome. | Sampling suppression and normalized pseudo-regret increased; persistent final masking was not detected. | Yes | YES for a persistent subregion claim |
| G-08 | MEDIUM | STATISTIC_DEFINITION_GAP | E01 two headline outcomes as separate evidence | Regret and post-initial sampling contrasts are algebraically the same action-frequency information. | Present one primary estimand and translate it into the other unit explicitly. | Yes | NO |
| G-09 | MEDIUM | STATISTIC_DEFINITION_GAP | E02 pooled regret as independent welfare confirmation | Affine M1 makes normalized regret exactly mean `1-d` in authenticity-optimal strata. | Treat as normalized objective endpoint distance, not independent mechanism evidence. | Yes | NO |
| G-10 | MEDIUM | ARCHITECTURE_OVERREACH | E04 global-mask isolates duplicate masking | It also changes action cardinality, initial aggregate policy mass, competition, and updates. | It tests a shared-mask action representation; it does not isolate one mathematical normalization term. | Yes | YES for pure component attribution |
| G-11 | MEDIUM | STATISTIC_DEFINITION_GAP | E04/E05 “settled” | Primary argmax flags use deterministic `argmax` even when modal ties exist. | Say “final-window argmax classification”; optionally report prespecified unique-modal results after adjudication. | Yes | NO for clarification; adjudication needed for new headline |
| G-12 | MEDIUM | INFERENTIAL_UNIT_MISMATCH | E03 zero-width 95% interval | All five selected master grid fractions equal 243/357; interval collapse is not zero Monte Carlo/model uncertainty. | “Identical across the five selected master streams”; do not advertise exact precision. | Yes | More masters needed for tail precision |
| G-13 | MEDIUM | CAUSAL_OVERREACH | E04 scarcity causes effect | One-good K manipulation makes good fraction 1/K. Only combined controls distinguish raw K from scarcity/representation. | “Combined controls support representation-dependent search burden under scarce receptivity.” | Yes | YES for clean causal decomposition |
| G-14 | MEDIUM | TERMINOLOGY_OVERREACH | literal sequential peer-group search | Flat selects a joint arm; hierarchical makes two softmax choices per trial. No availability, movement, or human search process is modeled. | Describe context/action selection as an abstract repeated search problem. | Yes | Human/process model evidence required |
| G-15 | LOW | STATISTIC_DEFINITION_GAP | subjective threshold helper at lambda=0/p=1 | `subjective_indifference_r` divides by `lambda(1-p)` without domain validation. Frozen evidence avoids these edges. | State domain/sign regime explicitly; add validation in a future code task. | No | NO |

### G.1 Additional scientifically valid results not foregrounded by the task

The following are supported by exact identities or frozen E01-E05 artifacts. Items marked **post hoc** are valid audit diagnostics but are not automatically confirmatory manuscript claims.

1. **E01 information restoration is separately supported.** Five-percent forced authenticity reduced rejection-stratum final masking by `.046590` and normalized pseudo-regret by `.057954`; counterfactual feedback reduced them by `.118135` and `.141318`. These results were in the local evidence matrix but not in the task's headline-number list. They diagnose the model's information channel; they are not human intervention effects.
2. **E01 negative weighting has a large main effect but no detected interaction with the controlled initial outcome.** Lambda 2.5-minus-.5 final masking at p=.65 is `.402990`, while the high-minus-low rejection-gap interaction is `-.001067` with interval spanning zero. This separates a general transformed-reward effect from amplification of one initial rejection.
3. **E01 normalized regret is an exact action-count identity.** The `+.025824` result contains no information beyond the `-.025837` post-initial authentic-rate result once T and the forced first action are known. This is a scientifically useful simplification for reporting and prevents double counting.
4. **E02 normalized regret is an exact disclosure-distance identity.** In the authenticity-optimal affine cells it equals mean `1-d`; the result is best interpreted as objective endpoint distance, not an independent welfare construct.
5. **M2 value iteration has an independent all-grid policy-enumeration check.** Four relevant deterministic policies reproduced the DP envelope for all 357 cells to maximum error `8.99e-10`. This strengthens code/mathematics consistency but does not change the information-mismatch boundary.
6. **The M2 objective threshold moves monotonically downward across the three frozen eta checks.** The exact DP brackets are about `.384`, `.339`, and `.269` for eta 0, .2, and .8. This is a deterministic selected-eta result, not a closed general theorem over eta.
7. **E04's headline survives a strict unique-modal definition (post hoc frozen diagnostic).** Recomputing the same five master endpoint contrasts from the stored `mean_settled_any_good_auth_unique` field gives flat `-0.2412` (Student-t `[-0.2520,-0.2304]`) and hierarchical `-0.4812` (`[-0.5191,-0.4433]`). This shows the primary direction is not created by ties, but the unique metric was not the prespecified headline effect.
8. **E05's flat crossing survives a strict unique-modal response (post hoc frozen diagnostic).** Using stored `modal_good_auth_unique_fraction` with the same dense grid, PAVA, and master bootstrap gives point `.31033` and interval approximately `[.30503,.31412]`, close to the prespecified argmax result `.31285`. This does not repair the G2 issue: it remains an across-child modal statistic, not a binary softmax probability.
9. **E05's objective advantage can carry the crossing interval by exact transformation.** Mapping the published crossing interval through `.40-.85bf` gives `[.130620,.138340]`. This is conditional Monte Carlo uncertainty inherited from the crossing, not new model-specification uncertainty.
10. **E04's controls support a conjunction, not a single cause.** Random label identity leaves slopes essentially unchanged; global-mask and known-good controls remove the large K decline; two-good attenuates it; proportional-25 nearly removes it. The defensible scientific result is “representation-dependent burden when receptive contexts are scarce,” not “K alone” or “scarcity alone.”

## H. Scientific-boundary summary

### PROVED

- The maintained learner applies loss weighting only to negative realized rewards and uses a numerically stabilized all-action softmax.
- M0 objective gap is `a+c-(1-p)(b+r)`; the default objective threshold is exactly `43/60`.
- Under the stated sign regime, the M0 learner-side transformed-reward threshold increases with lambda and is distinct from the objective threshold when lambda differs from 1.
- M1 expected reward is affine in disclosure; all strict static optima are endpoints; action count does not change the full-information static optimum when 0 and 1 are present.
- M2 transition and reward operators match the hand-off model; Accepted-state authenticity dominates masking by exactly `a+c`; the Neutral/Stigmatized dynamic-gap identities match event order.
- M2 value iteration is a valid full-information objective comparator for the frozen finite discounted MDP and agrees with four-policy enumeration on all 357 frozen cells.
- M3's distinct objective reward classes and full-information best value are K-invariant under the one-good-context design.
- The M3 default good-authentic/mask crossover is exactly `8/17`; bad-context authenticity is not the competing optimum near E05.
- Binary softmax has a Q-equality 50% crossover; the corresponding multi-action condition depends on all alternatives.
- M4 interval invariance, pure-mask recurrence, and conditional authenticity drift follow from the maintained update rule; these are Track-B mathematics only.
- In E01's binary authenticity-optimal cells, normalized pseudo-regret is exactly the suboptimal-mask fraction. In E02's affine authenticity-optimal cells, normalized regret is exactly mean `1-d`.

### DEMONSTRATED

- E01: one initial rejection reduced later authentic sampling and increased the equivalent normalized pseudo-regret action-frequency measure, but no final-window masking increase was detected.
- E01: forced authentic exploration and counterfactual authentic feedback reduced masking and normalized pseudo-regret after rejection in the tested model; greater lambda increased masking without changing objective payoffs.
- E02: independent graded arms increased nonzero disclosure but reduced full-authentic final-window selection, optimal-endpoint modal probability, and pooled normalized endpoint-distance performance in rejected p=.75/.85 strata.
- E03: under the frozen default learner, 243/357 tested cells had aggregate final-window Neutral masking while full-information DP favored authenticity; 350/357 classifications were stable and seven were visit-inconclusive. This is tested-grid coverage, not prevalence.
- E03: specified gamma, alpha, and tau perturbations changed named sentinel classifications; the default result is learner-setting conditional.
- E04: fixed-one good-context argmax settling declined from K=1 to K=16 in flat and hierarchical architectures. Combined global-mask, known-good, randomized-identity, two-good, and proportional-good controls bound the result to representation-dependent burden under scarce receptivity.
- E05: the flat K=4 across-child modal-good-auth argmax fraction crossed .5 at bf `.312852` with master-bootstrap interval `.307836-.316918`, while the objective crossover was `.470588`. The hierarchical crossing was left-censored below the dense range.
- Post-hoc frozen tie checks show E04 endpoint directions and the E05 flat crossing persist under strict unique-modal definitions; they are robustness diagnostics, not automatically adjudicated headlines.

### PLAUSIBLE BUT UNTESTED

- A finite-horizon persistent-mask subregion near the M0 threshold; E01 did not demonstrate one.
- Intermediate disclosure acts as a lower-risk exploratory bridge that improves later endpoint learning; E02 shows altered exposure but adverse endpoint/regret outcomes under independent arms.
- The E03 full-information gap decomposes into an information cost and an algorithmic inefficiency; no information-matched optimum exists.
- E04 effects are caused specifically by scarcity, duplicate mask normalization, or literal sequential search; the controls support a bounded conjunction but do not isolate one unique mechanism.
- E05's displacement magnitude is caused by hot-stove sampling, fixed temperature, multi-action normalization, or another single mechanism. The current experiment does not decompose it.
- Any human educational effect, prevalence, developmental persistence, intervention benefit, or calibrated BFLPE threshold.
- M4 bistability, hysteresis, irreversible entrenchment, or Article-V1 endogenous-receptivity evidence.

### PROHIBITED / UNSUPPORTED

- Applying binary-softmax Proposition G2 directly to E05's eight-action across-child modal-response crossing.
- Saying fixed temperature alone has been ruled out as a contributor to the measured E05 crossing.
- Treating `243/357` (or legacy `226/357`) as human prevalence, learner prevalence, or intrinsic phase-space volume.
- Calling the E03 comparator information-matched or claiming the learner failed relative to the best policy attainable under its own information constraints.
- Claiming one early rejection caused persistent final masking in E01 or that an exact null was established.
- Claiming graded disclosure improves endpoint discovery, welfare, or smooth generalization in E02.
- Claiming K alone proves scarcity causes masking, that global-mask isolates only duplicate normalization, or that the model literally implements human peer-group search.
- Estimating a hierarchical E05 crossing outside the approved dense range.
- Using any M4/E06 numerical result as Article-V1 confirmatory evidence.
- Continuing manuscript drafting from the current stale Results/Discussion sources before the blocker corrections above are applied.

**Exact next Codex task after this review:** perform a documentation-only Article-V1 correction pass that (1) removes the E05 G2/temperature exclusion, (2) removes M4/E06 Results and Discussion evidence, (3) rewrites E01-E05 prose from the 29 audited matrix rows with exact statistic definitions and inferential units, (4) labels the generator-source provenance gap, and (5) does not change code, configs, artifacts, figures, or scientific claims beyond the maximum defensible wording in this report.

