# Article V1 Existing-Content Inventory

**Stage:** short-article architecture and evidence routing

**Status at inventory:** `READY_FOR_SHORT_ARTICLE`

**Scope:** E01–E05 only; E06/M4 deferred

## Task classification

```text
TASK TYPE:
Manuscript architecture / content inventory / evidence routing.

SCIENTIFIC STATUS:
No new experiment.
No new numerical inference.
No model change.
No artifact regeneration.
No new scientific claim.

ARTICLE STATUS:
E01–E05 science frozen.
E06/M4 deferred.

TARGET:
Short first research article, approximately 6,000–8,000 words.

STAGE OUTPUT:
Article skeleton
+ reuse/compression map
+ claim/evidence/figure map
+ true gap list.
```

## Inventory answer

Substantial article-writing work is already complete. The repository contains:

- a 14-page, 5,205-word rendered Frontiers manuscript with full article
  structure, but stale evidence and M4/E06 scope;
- a newer 7,093-word Formal Model and Methods authority with complete M0–M3 and
  E01–E05 methods;
- 3,675 words of historical literature-review prose and a 5,754-word active
  literature audit;
- 2,596 words of historical Results, 3,605 words of historical Discussion, and
  a 2,770-word structured current-findings synthesis;
- four deterministic E01–E05 publication figures in PNG and PDF, 1,108 words of
  captions, source-data CSVs, an analytic table, provenance, and generation
  scripts;
- four experiment-level interpretation notes totalling approximately 10,300
  words.

The next manuscript stage is therefore extraction, compression, and authority
correction. It is not greenfield writing.

## Significant content sources

| Path | Content type | Approximate size | Scientific status | Usefulness | Destination | Reuse potential | Notes |
|---|---|---:|---|---|---|---|---|
| `projects/frontiers_article/ARTICLE_V1_MODEL_METHODS.md` | Formal Model / Methods | 7,093 words; 588 lines | Active frozen authority | High | Main + Supplement | Compress | Principal modern Methods source. Complete M0–M3, learner, E01–E05 methods, inference, and provenance. |
| `doc-reviews/frontiers_submission/gifted_masking_frontiers_original_research_assertive_revision.docx` | Full manuscript | 14 rendered pages; 5,205 extracted words; 4 figures; 3 tables | Historical | Medium | Source-only | Rewrite for current authority | Exact 14-page file. Layout is usable, but Abstract/Methods/Results/Discussion contain `226/357`, `.950`, one-seed inference, and M4/E06. |
| `doc-reviews/frontiers_submission/gifted_masking_frontiers_original_research.docx` | Earlier full manuscript | 4,976 extracted words; 3 tables | Historical | Low–medium | Source-only | Rewrite | Earlier version of the same programme-level article; superseded by assertive revision and frozen evidence. |
| `doc-reviews/frontiers_submission/LITERATURE_REVIEW_CHAPTER.md` | Introduction/literature | 3,675 words; 131 lines | Historical | High for prose, subordinate for claims | Main + Supplement/background notes | Compress + correct | Strong giftedness, stigma, social-coping, hot-stove, context, and BFLPE prose. Bibliographic and novelty claims must be checked against active literature audit. |
| `projects/frontiers_article/ARTICLE_V1_LITERATURE_AUDIT.md` | Literature authority | 5,754 words; 793 lines | Active authority | High | Main routing + repository | Source for facts | Defines permitted citations, terminology, novelty limits, and model-to-human boundaries. No new search is required in this stage. |
| `doc-reviews/frontiers_submission/MODEL_CASCADE_CHAPTER.md` | Model narrative | 3,108 words; 145 lines | Historical | Medium | Main Methods/Discussion source | Compress + rewrite | Useful conceptual explanations of learner and M0–M3 progression. M4 section is excluded; equations and claims must defer to current Methods/analytic authorities. |
| `doc-reviews/frontiers_submission/RESULTS_BY_FINDING_CHAPTER.md` | Results prose | 2,596 words; 89 lines | Explicitly stale historical source | Medium | Main Results source-only | Rewrite | Useful rhetorical sequencing, but old E03/E04 values, inference, and M4 findings prevent direct reuse. |
| `doc-reviews/frontiers_submission/DISCUSSION_CHAPTER.md` | Discussion/limitations/conclusion | 3,605 words; 129 lines | Explicitly stale historical source | Medium–high | Main Discussion source-only | Compress + rewrite | Conceptual organization is reusable. Remove M4, stale M2/E04 claims, human-prediction overreach, and old statistical limitations. |
| `doc-reviews/frontiers_submission/ARTICLE_V1_CURRENT_FINDINGS_AND_CONCLUSIONS_2026-08-15.md` | Structured findings synthesis | 2,770 words; 377 lines | Subordinate/historical synthesis | High | Results + Discussion source | Compress + reword | Strong E01–E05 role and boundary summary. Its remaining-literature-work and provisional-novelty state is not the current routing authority. |
| `projects/frontiers_article/ARTICLE_V1_E01_E02_INTERPRETATION.md` | Interpretation | 2,461 words | Subordinate active | High | Results + Discussion | Compress | Use claim boundaries and E01/E02 dissociation; freeze overrides independent-regret framing. |
| `projects/frontiers_article/ARTICLE_V1_E03_INTERPRETATION.md` | Interpretation | 2,845 words | Subordinate active | High | Results + Discussion + Supplement | Compress | Strong explanation of dynamic value and comparator; avoid prevalence, information-matched, or irreversibility language. |
| `projects/frontiers_article/ARTICLE_V1_E04_INTERPRETATION.md` | Interpretation | 2,706 words | Subordinate active | High | Results + Discussion + Supplement | Compress | Strong scarcity/discovery/representation conjunction and control interpretation. |
| `projects/frontiers_article/ARTICLE_V1_E05_INTERPRETATION.md` | Interpretation | 2,304 words | Subordinate active with binding supersession notice | Medium | Results + Discussion | Rewrite for current authority | Threshold framing is useful. Temperature/G2 exclusion sections are `DO NOT USE`. |
| `projects/frontiers_article/ARTICLE_V1_ANALYTIC_RESULTS.md` | Analytic proofs | 6,974 words; 1,040 lines | Active authority | High | Main equations + Supplementary derivations | Compress/source | Supplies exact M0/M1/M2/M3 comparators; M4 section remains Track-B only. |
| `projects/frontiers_article/ARTICLE_V1_EVIDENCE_MATRIX.csv` | Claim/evidence matrix | 33 data rows; 2,887 words | Highest claim authority | High | Routing only | Direct source | Exact selectors, artifacts, inferential units, values, intervals, and wording ceilings. |
| `projects/frontiers_article/ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` | Consistency audit | 6,794 words; 370 lines | Active authority | High | Routing + limitations | Direct source | Governs E03 definition, regret identities, E04 argmax ties, E05 correction, and stale-prose handling. |
| `projects/frontiers_article/ARTICLE_V1_CLAIM_LEDGER.md` | Claim decisions | 1,462 words; 82 lines | Active authority | High | Routing | Direct source | Provides KEEP/NARROW/CUT boundaries. |
| `projects/frontiers_article/MANUSCRIPT_INTEGRATION_MAP.md` | Paragraph reuse plan | 4,060 words; 241 lines | Historical planning | Medium | Repository planning | Source | Existing paragraph-level allocation is useful but predates the short-article and E01–E05 authority freeze. |
| `projects/frontiers_article/publication_v1/figures/FIGURE_CAPTIONS.md` | Figure captions | 1,108 words; 119 lines | Deterministic publication output | High | Main figure captions | Compress/reword | Numerically current. Some captions are too long for main text and Figure 2/4 labels need authority-aware simplification. |
| `projects/frontiers_article/publication_v1/tables/analytic_results_v1.md` | Analytic table | 741 words; 30 lines | Deterministic publication output | High | Supplement or compact main table | Direct/compress | Exact M0–M3 analytic anchors and interpretation constraints. |
| `PAPER_REVISION_NOTES.md` | Revision history | 161 lines before Stage 1 banner | Explicitly stale | Low | Repository history | Source-only | Identifies the old manuscript and changes; not scientific evidence. |

## The “14-page Methods” identification

No separate 14-page Formal Model/Methods DOCX or PDF was found. Two related
completed sources exist and should not be conflated:

1. `projects/frontiers_article/ARTICLE_V1_MODEL_METHODS.md` is the current
   7,093-word Formal Model and Methods authority. It is the principal source for
   main and supplementary Methods.
2. `doc-reviews/frontiers_submission/gifted_masking_frontiers_original_research_assertive_revision.docx`
   is a complete historical manuscript that renders to exactly 14 pages. Its
   main-text word-count line reports 4,071 words; extracted document text is
   5,205 words including front/back matter. It contains a substantial Methods
   section but is not itself the current Methods authority.

The 14-page DOCX was rendered read-only and representative pages were visually
inspected. It is structurally usable but scientifically stale.

## Long Formal Model/Methods routing map

| Current subsection | Destination | Reason/action |
|---|---|---|
| Modelling objective and methodological position | `MAIN — COMPRESS` | Retain existence-and-structure purpose, uncalibrated scale, M0–M3 sequence, and deferred endogeneity in approximately 100 words. |
| Three meanings of value | `MAIN — RETAIN NEARLY AS IS`, compressed | Essential identification framework: environmental reward, learned value, full-information comparator. |
| Notation and reference scale | `MAIN — COMPRESS` + `SUPPLEMENT` | Main: core symbols and common reference payoffs. Supplement: full notation table, scaling identity, evidence levels, and parameter roles. |
| Parameter governance and domain conventions | `SUPPLEMENT` | Important conditionality but too detailed for 1,200–1,600-word main Methods. |
| Shared finite learner: reward transform and Q update | `MAIN — COMPRESS` | Retain equations, `lambda=1`, constant alpha, and selected-action update. |
| Shared finite learner: action selection | `MAIN — COMPRESS` | Retain stable softmax and positive sampling; multi-action 0.5 identity belongs in Supplement unless needed solely to block E05 misuse. |
| Time and final-window summaries | `MAIN — COMPRESS` | Retain finite horizon, 20% window, and E03 `T=1000` exception. Exact indexing can move to Supplement. |
| M0 full definition and learner-side lambda boundary | `MAIN — COMPRESS` + `SUPPLEMENT` | Main: rewards and objective boundary principle. Supplement: subjective crossover derivation and sensitivity details. |
| M1 full definition | `MAIN — COMPRESS` | Main needs disclosure grid, independent Q values, affine reward, endpoint optimum. Full derivation and general grid theorem to Supplement. |
| M2 states, rewards, transition order | `MAIN — COMPRESS` + `SUPPLEMENT` | Main: three states, reward-first order, action-induced persistence. Full reward/transition table and kernels to Supplement. |
| M2 state-action learner and full-information comparator | `MAIN — RETAIN NEARLY AS IS`, compressed | Essential to understand E03. Main must state Q-table, gamma/next-state max, value iteration, oracle status, and aggregate Neutral-action classifier. Policy enumeration detail to Supplement. |
| M3 environment and objective reward classes | `MAIN — COMPRESS` | Retain good/bad contexts, comparison-cost placement, and K-invariant objective. Exact class arithmetic to Supplement. |
| M3 action representations | `MAIN — COMPRESS` + `SUPPLEMENT` | Main names and conceptually defines all four E04 architectures. Detailed update mechanics and action indexing to Supplement. |
| M3 objective comparison-cost crossover | `MAIN — RETAIN NEARLY AS IS`, compressed | Essential E05 environmental benchmark `8/17`. General derivation to Supplement. |
| Formal progression | `MAIN — COMPRESS` | Supplies Figure 1 narrative; avoid duplicating Introduction and Discussion. |
| Common computational design, replication, uncertainty | `MAIN — COMPRESS` + `SUPPLEMENT` | Main: n/T, five master seeds, final window, Student-t/curve bootstrap inferential units. Full seed namespaces and selectors to Supplement. |
| E01 methods | `MAIN — COMPRESS` | Initial-outcome strata and information-restoration conditions. Detailed stream construction to Supplement. |
| E02 methods | `MAIN — COMPRESS` | Binary/graded paired architecture and rejected stratum. Full common-random-number construction to Supplement. |
| E03 methods | `MAIN — RETAIN NEARLY AS IS`, compressed | Primary classifier, visit adequacy, `n=160`, `T=1000`, and exact DP comparator are essential. Sensitivities and harsh sentinel to Supplement. |
| E04 methods | `MAIN — COMPRESS` | Primary argmax statistic, K values, four architectures, and controls. Detailed identity/abundance variants to Supplement. |
| E05 methods | `MAIN — COMPRESS` + `SUPPLEMENT` | Main: objective and learned response definitions, PAVA crossing, master bootstrap, censoring. Full grid and inversion algorithm to Supplement. |
| Reproducibility and artifact provenance | `REPOSITORY / REPRODUCIBILITY` + brief main limitation | Main gets one concise disclosure; hashes, validators, generators, and reconstruction details remain repository-only. |
| Scope of modelling framework | `MAIN — COMPRESS` + `LIMITATIONS` | Reuse core boundary language without repeating technical Methods. |

## Figure and source-data inventory

| Candidate | Files/source | Classification | Article role | Required action |
|---|---|---|---|---|
| Model progression | `publication_v1/figures/Figure_1_model_progression.{png,pdf}`; `scripts/figures.py` | `READY FOR MAIN` | Figure 1 | Reuse; caption compress. |
| E01/E02 foundation | `Figure_2_early_feedback_and_graded_disclosure.{png,pdf}` | `READY BUT NEEDS REDESIGN` | Figure 2 | Remove or visually subordinate algebraically redundant regret rows; avoid “welfare” wording; preserve null final-mask interval. |
| E03 map | `Figure_3_persistent_state_contrast_map.{png,pdf}` | `READY FOR MAIN` | Figure 3 | Reuse; caption must keep tested-grid/non-prevalence definition prominent. |
| E04/E05 combined | `Figure_4_discovery_and_comparison_cost.{png,pdf}` | `READY BUT NEEDS REDESIGN` | Figure 4, or split if journal readability requires | Replace vague “settled” axis wording with final-window argmax classification; retain hierarchical left-censoring and controls. A fifth figure is optional, not missing science. |
| Old directional contrasts | `doc-reviews/frontiers_submission/figures/Figure_1_directional_contrasts.tif` | `SUPPLEMENT ONLY / STALE` | Historical comparison | Source-only; old estimates and inference require replacement. |
| Old M2 maps | `Figure_2_m2_suboptimal_masking_regime.tif`, `Figure_2_m2_thresholds.tif` | `REDUNDANT / STALE` | None or historical supplement | Superseded by publication Figure 3. |
| Old M3 ablation | `Figure_3_m3_action_space_ablations.tif` | `STALE` | None | Superseded by publication Figure 4a. |
| Old M4 ramp | `Figure_4_m4_ramp_paths.tif` | `REMOVE FROM V1` | Track B only | Preserve historically; never route to Article V1. |
| Legacy simulation PNGs | `simulations_old/**` and root `fig4_m3_dimensionality.png` | `STALE` | Repository history | Do not reuse numerically. |

Current source-data tables already cover all four proposed main figures under
`projects/frontiers_article/publication_v1/data/`. The build scripts are
`publication_v1/scripts/{extract,analytic,figures,captions}.py`; the manifest
and `PROVENANCE.json` record their inputs. No main scientific figure is
genuinely missing. Only targeted redesign/export work remains.

## Proposed supplement architecture

### Supplementary Methods

- full notation, parameter table, domains, and scale/temperature identity;
- shared learner details and numerical softmax implementation;
- complete M0/M1 reward derivations and loss-weighting sensitivities;
- M2 reward table, transition kernels, Bellman equations, policy enumeration,
  visit adequacy, sensitivity sentinels, and harsh boundary;
- M3 action indexing, hierarchical dual updates, global-mask and known-good
  implementations, randomized identity, and abundance variants;
- exact E01–E05 configurations, grids, hyperparameters, seed hierarchy, and
  common-random-number construction;
- exact final-window, tie, classifier, PAVA, bootstrap, and censoring procedures;
- full analytic derivations from `ARTICLE_V1_ANALYTIC_RESULTS.md`.

### Supplementary Results

- E01 forced/counterfactual regret translations and lambda sensitivities;
- E02 normalized-regret translation and any non-headline arm summaries;
- E03 stability, selected thresholds, gamma/alpha/tau sentinels, harsh boundary,
  and unique/tie diagnostics;
- E04 global-mask, known-good, identity, two-good, proportional-good, and
  strict-unique-modal diagnostics;
- E05 endpoint contrast, response diagnostics, and hierarchical censoring
  details beyond the main-figure annotation;
- analytic-results table and expanded figure captions.

### Repository technical documentation

- artifact and config hashes;
- manifest schema, validator commands, and CLI invocation;
- exact generator-source recovery/provenance archaeology;
- deterministic publication build internals;
- governance history, approvals, execution logs, and internal handoffs.

## Quantitative reuse estimate

Estimated main-text sourcing after authority correction:

| Category | Approximate share | Basis |
|---|---:|---|
| Reusable with light editing | 15% | Core definitions, limitation formulations, and some literature framing already match current authorities. |
| Reusable after compression | 50% | Formal Methods, literature review, current-findings synthesis, and interpretation notes are accurate but much longer than the target. |
| Requires substantial rewrite | 25% | Historical Results/Discussion and the 14-page manuscript have useful structure but stale numbers, inference, and M4 scope. |
| Genuinely new | 10% | New Abstract, short-article transitions, integrated synthesis, concise limitations/conclusion, and prose bridging the selected evidence sequence. |

Approximately 65% of the main article can therefore be sourced through light
editing or compression, another 25% has reusable conceptual material requiring
authority-driven rewriting, and only about 10% is genuinely greenfield prose.
