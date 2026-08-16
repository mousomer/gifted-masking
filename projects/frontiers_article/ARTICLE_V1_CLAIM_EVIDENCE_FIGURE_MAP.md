# Article V1 Claim–Evidence–Figure Map

**Status:** routing authority complete; manuscript extraction may begin

**Scope:** E01–E05 only. E06/M4 is deferred.

## Use rule

Every quantitative sentence in the manuscript must trace to the frozen evidence
matrix and the exact artifact below. Analytic statements must trace to
`ARTICLE_V1_ANALYTIC_RESULTS.md`. Historical prose is never evidence. “Ready”
means evidentially ready, not necessarily ready as prose.

## Planned claim map

| ID | Planned claim | Section | Experiment | Claim type | Evidence authority | Exact artifact/data | Analytic comparator | Figure/table | Existing prose source | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| FRAME-01 | Learned behaviour and the relevant objective benchmark are distinct quantities. | Intro/Methods | E01–E05 | framing | Formal Methods; methodological position | n/a | experiment-specific static or DP oracle | Fig. 1 | argument architecture; literature chapter | READY — NEEDS COMPRESSION |
| E01-01 | Initial authentic rejection suppresses subsequent authentic sampling over the tested horizon. | Results 3.1 | E01 | empirical contrast | Evidence matrix `E01-C2-SAMPLING` | `results/summaries/frontiers_hot_stove_v1_effects.csv` | M0 static expected-value optimum | Fig. 2A | E01 interpretation note | READY — NEEDS REWORDING |
| E01-02 | The corresponding normalized pseudo-regret change is an algebraic translation of sampling, not independent welfare evidence. | Results 3.1 | E01 | derived/constraint | Evidence matrix `E01-C2-REGRET`; freeze §B | `results/summaries/frontiers_hot_stove_v1_effects.csv` | exact reward-gap identity | text or supplement | E01 note; consistency audit | READY — NEEDS REWORDING |
| E01-03 | Forced authentic exploration weakens the sampling disparity in the tested intervention. | Results 3.1 | E01 | empirical contrast | `E01-C2-FORCED-MASK`, `E01-C2-FORCED-REGRET` | `results/summaries/frontiers_hot_stove_v1_effects.csv` | M0 optimum | supplement | E01 note | READY |
| E01-04 | Counterfactual feedback weakens the sampling disparity in the tested intervention. | Results 3.1 | E01 | empirical contrast | `E01-C2-CF-MASK`, `E01-C2-CF-REGRET` | `results/summaries/frontiers_hot_stove_v1_effects.csv` | M0 optimum | supplement | E01 note | READY |
| E01-05 | E01 does not show a reliable persistent final-window mask-rate contrast. | Results 3.1 | E01 | bounded null/qualification | `E01-C2-FINAL-MASK`; freeze §B | `results/summaries/frontiers_hot_stove_v1_effects.csv` | n/a | text | E01 note | READY — NEEDS REWORDING |
| E02-01 | Five independent graded-disclosure actions increase selection of some nonzero disclosure after rejection. | Results 3.2 | E02 | empirical contrast | `E02-C4-EXPLORATION` | `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` | M1 affine payoff | Fig. 2B | E02 interpretation note | READY |
| E02-02 | The same representation reduces full-authentic endpoint selection. | Results 3.2 | E02 | empirical contrast | `E02-C4-FULL-ENDPOINT` | `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` | M1 endpoint optimum | Fig. 2C | E02 note | READY |
| E02-03 | It also reduces modal selection of the objectively optimal endpoint. | Results 3.2 | E02 | empirical contrast | `E02-C4-MODAL` | `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` | M1 endpoint optimum | text/supplement | E02 note | READY |
| E02-04 | E02 normalized regret equals disclosure distance `1-d`; it is not a separate welfare result. | Results 3.2 | E02 | derived/constraint | `E02-C4-REGRET`; freeze §C | `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` | exact distance identity | supplement | E02 note; audit | READY — NEEDS REWORDING |
| E02-A | With the specified linear acceptance function, expected reward is affine in disclosure, so strict objective optima lie at endpoints. | Methods/Results | E02 | analytic | Analytic Results M1; `E02-S1-ARM-REWARDS` | `results/summaries/frontiers_m1_binary_graded_v1_arms.csv` | exact M1 equation | text/equation | Formal Methods; E02 note | READY |
| E03-01 | At `n=160`, `T=1000`, 243 of 357 tested grid cells meet the exact aggregate final-window Neutral-action/DP disagreement definition. | Results 3.3 | E03 | tested-grid classification | `E03-C5-GRID`; freeze §D | `results/summaries/frontiers_m2_regime_replication_v1_effects.csv` | exact full-information DP policy | Fig. 3 | E03 note; current findings | READY — NEEDS REWORDING |
| E03-02 | The classification is stable in 350 of 357 cells under the specified visit-adequacy check. | Results 3.3 | E03 | robustness | `E03-C5-STABILITY` | `results/summaries/frontiers_m2_regime_replication_v1_stable_cells.csv` | same DP comparator | supplement | E03 note | READY |
| E03-03 | Dynamic thresholds and selected gamma/learner-sensitivity contrasts are conditional on the tested axes. | Results/Supplement | E03 | sensitivity | `E03-C5-THRESHOLDS`, `E03-C5-GAMMA`, `E03-C5-ALPHA-TAU`, `E03-C5-HARSH` | `results/summaries/frontiers_m2_regime_replication_v1_thresholds.csv`; `results/summaries/frontiers_m2_regime_replication_v1_cells.csv` | Bellman/DP threshold | supplement | E03 note | READY — NEEDS COMPRESSION |
| E04-01 | In flat `2K`, the change from `K=1` to `K=16` in final-window argmax classification as authentic in a good context is `-0.2340` (95% CI `[-0.246417,-0.221583]`). | Results 3.4 | E04 | empirical axis response | `E04-C6-FLAT` | `results/summaries/frontiers_m3_search_architectures_v1_effects.csv` | one-good-context objective is K-invariant | Fig. 4A | E04 note | READY — NEEDS REWORDING |
| E04-02 | In the hierarchical architecture, the corresponding change is `-0.4704` (95% CI `[-0.511031,-0.429769]`). | Results 3.4 | E04 | architecture contrast | `E04-C6-HIER` | `results/summaries/frontiers_m3_search_architectures_v1_effects.csv` | K-invariant objective | Fig. 4A | E04 note | READY |
| E04-03 | Global-mask and fixed-known-good controls separate action duplication and discovery burden from objective availability. | Results 3.4 | E04 | ablation | `E04-C6-CONTROLS` | `results/summaries/frontiers_m3_search_architectures_v1_effects.csv` | K-invariant objective | Fig. 4A/supplement | E04 note | READY — NEEDS COMPRESSION |
| E04-04 | Random good-context identity and multiple-good-context controls support an abundance/discoverability interpretation within the tested designs. | Results 3.4 | E04 | ablation | `E04-C6-IDENTITY`, `E04-C6-MULTIPLE` | `results/summaries/frontiers_m3_search_architectures_v1_effects.csv` | abundance-sensitive opportunity count | supplement | E04 note | READY — NEEDS COMPRESSION |
| E04-A | Under the specified one-good-context objective, K changes discovery burden but not the full-information best payoff. | Methods/Results | E04 | analytic | Analytic Results M3 | `results/summaries/frontiers_m3_search_architectures_v1_curves.csv` for response series | exact K-invariance result | Fig. 4A/text | Formal Methods; E04 note | READY |
| E05-01 | The exact objective comparison-cost crossover is `8/17` (about 0.470588) at the reference parameters. | Results 3.5 | E05 | analytic | `E05-C7-ANALYTIC`; Analytic Results | `results/summaries/frontiers_m3_bflpe_crossover_v1_analytic.csv` | exact M3 `bf*` | Fig. 4B | E05 note | READY |
| E05-02 | The across-child final-window modal-classification fraction in the flat model crosses 0.5 at about 0.312852 (bootstrap interval `[0.307836,0.316918]`), below the objective crossover. | Results 3.5 | E05 | estimated transition | `E05-C7-CROSSING` | `results/summaries/frontiers_m3_bflpe_crossover_v1_transitions.csv` | `bf*=8/17` | Fig. 4B | E05 note | READY — NEEDS REWORDING |
| E05-03 | The resulting learned/objective threshold gap is about 0.134 in the frozen comparison. | Results 3.5 | E05 | derived contrast | `E05-C7-GAP` | `results/summaries/frontiers_m3_bflpe_crossover_v1_analytic.csv` | exact objective crossover | Fig. 4B | E05 note | READY |
| E05-04 | The hierarchical transition is left-censored on the tested grid and must not be reported as an observed crossing. | Results 3.5 | E05 | censoring qualification | `E05-C7-HIER-CENSOR` | `results/summaries/frontiers_m3_bflpe_crossover_v1_transitions.csv` | objective crossover | Fig. 4B | E05 note | READY — NEEDS REWORDING |
| E05-05 | The displacement is established, but its quantitative decomposition is unresolved; fixed temperature remains a candidate contributor. | Discussion 4.5 | E05 | interpretation boundary | Freeze §E; consistency audit | frozen E05 artifacts collectively | n/a | none | corrected E05 note only | READY — NEEDS REWORDING |
| SYN-01 | E01 and E02 form a cross-mechanism dissociation, not a controlled sign reversal or two independent welfare effects. | Discussion 4.1–4.2 | E01/E02 | synthesis | freeze §§B–C; analytic results | frozen E01/E02 artifacts | M0 gap and M1 affine theorem | Fig. 2 | brief; audit | GENUINE WRITING GAP |
| SYN-02 | Across E01–E05, immediate value, dynamic value, discoverability, and learned boundary location are separable. | Abstract/Discussion | E01–E05 | bounded synthesis | brief; freeze; experiment authorities | all frozen standard artifacts | all explicit comparators | Figs. 1–4 | argument architecture; current findings | READY — NEEDS COMPRESSION |
| DOMAIN-01 | Concealment in these models need not imply that authentic expression lacks objective value; history, information acquisition, dynamic consequences, search structure, or learning properties can contribute. This is a model implication, not a human empirical finding. | Discussion 4.6 | E01–E05 | domain implication | literature audit; Formal Methods scope | n/a | n/a | none | literature chapter; historical Discussion | GENUINE WRITING GAP |

No planned main-text claim has an unresolved evidence route. “Needs substantial
rewrite” above describes prose/interpretation debt, not absent evidence.

## Non-negotiable annotations

### E03 annotation

`243/357` is a count of tested parameter-grid cells under the exact aggregate
final-window Neutral-action and visit-adequacy definition. It is **not** a
population prevalence, an individual-child proportion, a natural phase-space
volume, or evidence that 243 cells are equally probable in nature.
It is also **not** a Q-order classifier.

### E01 dependence annotation

The E01 normalized pseudo-regret contrast is exactly tied to authentic sampling:
`Delta R_norm = -(1999/2000) Delta A`. It must be presented as a translation,
not as an independent outcome.

### E05 annotation

The frozen evidence demonstrates a learned/objective crossover displacement.
It does **not** identify a unique mechanism, calibrate comparison cost to human
data, or rule out fixed softmax temperature. The retired binary-softmax/G2
exclusion must not reappear.
The learned response is **not** a softmax probability, a direct policy
probability, or a binary Q-value equality.

## Cross-experiment synthesis routing

| Synthesis term | Primary support | Exact role |
|---|---|---|
| Immediate value | M0/M1 analytic authorities; E01/E02 | Static objective reward and finite information acquisition/action representation. |
| Dynamic value | M2 analytic/DP authority; E03 | Current action changes future state; Bellman value is the relevant comparator. |
| Discoverability | M3 K-invariance; E04 | A favourable option can remain objectively available while finite discovery changes. |
| Learned behavioural boundary | M3 analytic crossover; E05 | Across-child modal-classification response crosses before environmental indifference. |

## Main-figure disposition

| Figure | Current files | Article role | Disposition | Required change |
|---|---|---|---|---|
| 1. Model progression | `publication_v1/figures/Figure_1_model_progression.{png,pdf}` | M0→M3 and comparator logic | **READY FOR MAIN** | Caption compression only. |
| 2. Early feedback and graded disclosure | `Figure_2_early_feedback_and_graded_disclosure.{png,pdf}` | E01/E02 supporting results | **READY BUT NEEDS REDESIGN** | De-emphasize/remove redundant regret panels; avoid independent-welfare wording. |
| 3. Persistent-state contrast map | `Figure_3_persistent_state_contrast_map.{png,pdf}` | E03 central dynamic result | **READY FOR MAIN** | Preserve exact classifier and non-prevalence annotation. |
| 4. Discovery and comparison cost | `Figure_4_discovery_and_comparison_cost.{png,pdf}` | E04/E05 central results | **READY BUT NEEDS REDESIGN** | Replace vague “settled” wording with exact final-window argmax classification; preserve E05 censoring. Optional split for readability only. |

No additional scientific main figure is required. A fifth figure would be a
layout split of current Figure 4, not a missing evidence product. Sensitivity,
ablation, and diagnostic plots belong in the supplement.

## Frozen source-data routing

The deterministic publication layer in `projects/frontiers_article/publication_v1`
contains the four figure files, captions, manifest/provenance records, and the
source-data tables derived from the frozen result artifacts. The exact result
CSVs named in the map remain the numerical authority. Figure pixels and old TIF
exports are not evidence authorities; the legacy M4/E06 TIF is excluded.
