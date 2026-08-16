# Article V1 Short-Article Skeleton

**Status:** architecture fixed; manuscript prose not drafted

**Scope:** E01–E05 only; E06/M4 deferred

**Target main-text length:** approximately 7,200 words within the 6,000–8,000-word constraint

## Word allocation

| Section | Target words |
|---|---:|
| Abstract | 225 |
| 1. Introduction | 1,050 |
| 2. Model framework and methods | 1,450 |
| 3. Results | 2,400 |
| 4. Cross-experiment synthesis and Discussion | 1,350 |
| 5. Limitations | 500 |
| 6. Conclusion | 225 |
| **Total** | **7,200** |

The allocation leaves approximately 800 words of headroom below 8,000 for
journal-specific transitions, declarations, or small section imbalance. It is
not permission to expand every subsection.

## Abstract — 225 words

- **PURPOSE:** State the sequential-learning problem, the explicit-benchmark
  contribution, the E01–E05 progression, the three major results, and the
  bounded model conclusion.
- **PRIMARY CLAIMS:** Learned concealment/reduced authenticity need not imply
  that concealment is objectively advantageous within the specified model;
  explicit static and dynamic comparators make the divergence measurable.
- **EXPERIMENTS:** E01–E05, with E03–E05 carrying most result weight.
- **SOURCE MATERIAL ALREADY AVAILABLE:** Short-article brief; argument
  architecture; current findings; historical DOCX Abstract only as a negative
  template because its numbers and M4 scope are stale.
- **REQUIRED FIGURE/TABLE:** None.
- **MOVE TO SUPPLEMENT:** All design detail, secondary effects, sensitivities,
  and provenance mechanics.
- **MATERIAL STILL MISSING:** A new 200–250-word Abstract written only after the
  body is extracted and reconciled.

## 1. Introduction — 1,050 words

### 1.1 Ability concealment as a sequential-learning problem — 300 words

- **PURPOSE:** Establish that some gifted learners manage ability visibility,
  without a deficit stereotype or prevalence claim.
- **PRIMARY CLAIMS:** Concealment is one possible, context-dependent branch of
  gifted social coping and visibility management; existing research describes
  strategies better than trial-by-trial persistence.
- **EXPERIMENTS:** Motivates all; no result yet.
- **SOURCE MATERIAL:** `LITERATURE_REVIEW_CHAPTER.md` opening, stigma, coping,
  and persistence sections; `ARTICLE_V1_LITERATURE_AUDIT.md` §§5.1–5.7.
- **FIGURE/TABLE:** Figure 1 may be cited at the end, not explained here.
- **SUPPLEMENT:** Extended construct genealogy and broader source-family notes.
- **MISSING:** A compact transition from gifted visibility management to the
  finite-feedback question.

### 1.2 Why observed masking is insufficient to establish objective optimality — 300 words

- **PURPOSE:** Define the identification problem: the same behaviour can reflect
  current objective value, history-restricted information, dynamic state, or
  search failure.
- **PRIMARY CLAIMS:** Behaviour alone does not reveal the relevant environmental
  optimum; high masking is not automatically irrational or adaptive.
- **EXPERIMENTS:** Conceptual preview of E01, E03, and E04.
- **SOURCE MATERIAL:** `LITERATURE_REVIEW_CHAPTER.md` “Existing evidence…” and
  hot-stove sections; Formal Methods “Three meanings of value”; Discussion
  “policy outcome” concept after correction.
- **FIGURE/TABLE:** Figure 1.
- **SUPPLEMENT:** Full prior-art distinctions and oracle/information-matched
  comparator discussion.
- **MISSING:** Short integrated identification paragraph; existing sources are
  too dispersed for direct reuse.

### 1.3 Explicit objective benchmarks — 250 words

- **PURPOSE:** Introduce the methodological contribution before describing
  individual models.
- **PRIMARY CLAIMS:** M0/M1/M3 use exact static expected-reward comparators; M2
  uses an exact full-information dynamic-programming comparator; “objective” is
  model-relative, not human welfare.
- **EXPERIMENTS:** E01–E05.
- **SOURCE MATERIAL:** Formal Methods “Three meanings of value”; analytic table;
  analytic authority §§3–6.
- **FIGURE/TABLE:** Figure 1; optional compact analytic-anchor table if word and
  layout budgets permit.
- **SUPPLEMENT:** Proofs and full analytic table.
- **MISSING:** None beyond compression.

### 1.4 Article progression and contributions — 200 words

- **PURPOSE:** Preview the unequal-weight sequence: E01 foundation, E02 short
  extension, E03/E04 major results, E05 culmination.
- **PRIMARY CLAIMS:** `history -> endpoint discovery -> dynamic disagreement ->
  social discoverability -> boundary displacement`.
- **EXPERIMENTS:** E01–E05.
- **SOURCE MATERIAL:** Short-article brief; argument architecture; Figure 1.
- **FIGURE/TABLE:** Figure 1.
- **SUPPLEMENT:** None.
- **MISSING:** One concise roadmap paragraph.

## 2. Model framework and methods — 1,450 words

### 2.1 Common learner and measurement framework — 300 words

- **PURPOSE:** Define environmental reward, learned Q values, `lambda=1`, stable
  softmax, selected-action update, finite horizon, final 20%, five master seeds,
  and inferential-unit rules.
- **PRIMARY CLAIMS:** Headline phenomena do not arise from explicit loss
  aversion; final-window classifications are finite-horizon summaries, not
  absorbing policies.
- **EXPERIMENTS:** All.
- **SOURCE MATERIAL:** Formal Methods §§“Three meanings,” “Shared finite
  learner,” “Time,” and common computational design.
- **FIGURE/TABLE:** Figure 1; compact model/experiment table optional.
- **SUPPLEMENT:** Full notation, domain conventions, scale identity, seed
  derivation, implementation stability, exact windows, and complete parameters.
- **MISSING:** None; compression only.

### 2.2 E01: adverse-history environment — 150 words

- **PURPOSE:** Define M0 rewards, objective boundary principle, forced first
  authentic outcome strata, and information-restoration conditions.
- **PRIMARY CLAIMS:** E01 isolates later sampling after controlled initial
  acceptance/rejection; regret is a translation of action counts.
- **EXPERIMENTS:** E01.
- **SOURCE MATERIAL:** Formal Methods M0 and E01; analytic M0 propositions.
- **FIGURE/TABLE:** Figure 2a.
- **SUPPLEMENT:** Full reward derivation, subjective lambda boundary, seed
  streams, and secondary sensitivity cells.
- **MISSING:** None.

### 2.3 E02: disclosure/endpoints environment — 150 words

- **PURPOSE:** Define five independent disclosure arms, affine reward, endpoint
  optimum, and paired binary/graded rejected-stratum comparison.
- **PRIMARY CLAIMS:** Intermediate actions do not generalize and are not strict
  static optima.
- **EXPERIMENTS:** E02.
- **SOURCE MATERIAL:** Formal Methods M1 and E02; analytic M1 propositions.
- **FIGURE/TABLE:** Figure 2b–c.
- **SUPPLEMENT:** Complete arm grid, acceptance function derivation,
  common-random-number construction, and regret identity.
- **MISSING:** None.

### 2.4 E03: dynamic-state environment and DP comparator — 275 words

- **PURPOSE:** Define Neutral/Accepted/Stigmatized states, reward-first
  transitions, state-action Q learning, exact full-information discounted
  comparator, and aggregate Neutral-action classifier.
- **PRIMARY CLAIMS:** Dynamic value can reverse static ordering; comparator is
  an oracle, not information matched.
- **EXPERIMENTS:** E03.
- **SOURCE MATERIAL:** Formal Methods M2 and E03; analytic M2 §§5.1–5.10; E03
  interpretation §§3–9.
- **FIGURE/TABLE:** Figure 3.
- **SUPPLEMENT:** Full transition/reward table, kernels, Bellman equations,
  enumeration validation, visit-adequacy/tie mechanics, sentinels, thresholds,
  and harsh boundary.
- **MISSING:** None; careful compression required.

### 2.5 E04: receptive-context search — 275 words

- **PURPOSE:** Define K contexts, good/bad receptivity, K-invariant objective,
  primary final-window argmax statistic, and four architectures.
- **PRIMARY CLAIMS:** Availability and discovery are distinct; E04 changes a
  representation-dependent finite search problem without changing full-
  information best value.
- **EXPERIMENTS:** E04.
- **SOURCE MATERIAL:** Formal Methods M3/E04; E04 interpretation; analytic M3.1.
- **FIGURE/TABLE:** Figure 4a.
- **SUPPLEMENT:** Exact action indexing, hierarchical updates, randomized
  identity, multiple/proportional good contexts, unique-modal diagnostics, and
  full curves.
- **MISSING:** None.

### 2.6 E05: environmental and behavioural thresholds — 300 words

- **PURPOSE:** Define accepted-good-context comparison cost, exact objective
  crossover, across-child modal-classification response, PAVA/0.5 crossing,
  master-curve bootstrap, and left censoring.
- **PRIMARY CLAIMS:** Objective and learned thresholds are different estimands;
  E05 does not measure a softmax probability or Q equality.
- **EXPERIMENTS:** E05.
- **SOURCE MATERIAL:** Formal Methods M3 crossover and E05; analytic M3.2–M3.4;
  freeze §E.
- **FIGURE/TABLE:** Figure 4b, or Figure 5 if split for readability.
- **SUPPLEMENT:** Full bf grid, PAVA inversion, bootstrap validity rule,
  endpoint anchors, diagnostics, and mechanism-candidate discussion.
- **MISSING:** None.

## 3. Results — 2,400 words

### 3.1 Adverse experience suppresses authentic sampling — E01 — 250 words

- **PURPOSE:** Establish the finite-feedback foundation briefly.
- **PRIMARY CLAIMS:** Initial rejection reduces later authentic sampling;
  final-mask contrast spans zero; forced authentic exploration and
  counterfactual feedback improve correction.
- **EXPERIMENTS:** E01.
- **SOURCE MATERIAL:** Evidence matrix E01 rows; freeze D.1; E01 interpretation
  §§2–3 and claim boundary; current findings §4.1.
- **FIGURE/TABLE:** Figure 2a.
- **SUPPLEMENT:** Intervention regret translations and lambda sensitivity.
- **MISSING:** Authority-corrected concise Results prose. Historical Results
  cannot be copied directly.

### 3.2 Additional disclosure options can reduce optimal-endpoint discovery — E02 — 300 words

- **PURPOSE:** Present the short extension and E01/E02 contrast.
- **PRIMARY CLAIMS:** Nonzero disclosure rises while full-authentic final-window
  selection and optimal-endpoint modal behaviour fall; affine objective retains
  endpoint optima.
- **EXPERIMENTS:** E02, with one closing E01/E02 dissociation sentence.
- **SOURCE MATERIAL:** Evidence matrix E02 rows; freeze D.2; E02 interpretation;
  current findings §4.2.
- **FIGURE/TABLE:** Figure 2b–c.
- **SUPPLEMENT:** Redundant normalized-regret translation and arm tables.
- **MISSING:** Authority-corrected Results prose and exact qualifier that this is
  not a controlled sign reversal.

### 3.3 Learned behaviour can disagree with the dynamic optimum — E03 — 600 words

- **PURPOSE:** Present the first dynamic-comparator result and make the
  classifier legible without turning the grid count into a headline prevalence.
- **PRIMARY CLAIMS:** `243/357` tested cells meet the exact aggregate Neutral-
  action/full-information-DP disagreement definition; 350 stable, seven visit-
  inconclusive; the comparator is independently verified.
- **EXPERIMENTS:** E03.
- **SOURCE MATERIAL:** Evidence matrix E03 rows; freeze D.3; E03 interpretation;
  current findings §4.3; Figure 3 caption.
- **FIGURE/TABLE:** Figure 3.
- **SUPPLEMENT:** Selected dynamic thresholds, sensitivities, harsh sentinel,
  and detailed stability table.
- **MISSING:** New concise explanation of the map that avoids prevalence and
  individual-policy language while showing why dynamic value matters.

### 3.4 Objective availability does not imply social discoverability — E04 — 650 words

- **PURPOSE:** Present the second major result and the control logic.
- **PRIMARY CLAIMS:** Flat `S16-S1=-0.2340` and hierarchical `-0.4704` under one
  fixed good context, with five-master Student-t intervals; global-mask and
  known-good controls are practically near zero; identity and abundance
  controls support a representation-dependent burden under scarce receptivity.
- **EXPERIMENTS:** E04.
- **SOURCE MATERIAL:** Evidence matrix E04 rows; freeze D.4; E04 interpretation;
  Figure 4 caption; current findings §4.4.
- **FIGURE/TABLE:** Figure 4a.
- **SUPPLEMENT:** Full K curves, randomized identity, two-good/proportional-good
  estimates, and strict unique-modal diagnostics.
- **MISSING:** Authority-corrected Results prose that explains the conjunction
  without claiming K or scarcity alone is causal.

### 3.5 Learned and objective behavioural boundaries separate — E05 — 600 words

- **PURPOSE:** Deliver the culminating quantitative result.
- **PRIMARY CLAIMS:** Objective `8/17≈0.470588`; learned flat crossing
  `≈0.312852` with master-curve bootstrap `[0.307836,0.316918]`; objective
  authenticity advantage remains `≈0.134`; hierarchical crossing is left-
  censored below the resolved range; decomposition is unresolved.
- **EXPERIMENTS:** E05.
- **SOURCE MATERIAL:** Evidence matrix E05 rows; freeze D.5/E; analytic M3;
  corrected E05 note; Figure 4 caption; current findings §4.5.
- **FIGURE/TABLE:** Figure 4b or separate Figure 5.
- **SUPPLEMENT:** Endpoint contrast, exact estimator diagnostics, and response
  curves beyond the main range.
- **MISSING:** New Results prose that replaces the historical endpoint-only and
  G2 explanations.

## 4. Cross-experiment synthesis and Discussion — 1,350 words

This section is concept-led. It must not replay the Results experiment by
experiment. Target approximately 225 words per subsection, with flexibility to
merge 4.1/4.2 or 4.4/4.5 during extraction.

### 4.1 History and information acquisition — approximately 225 words

- **PURPOSE:** Interpret E01 as restricted feedback and information restoration.
- **CLAIMS/EXPERIMENTS:** E01; mechanism is generic prior art, article function
  is foundation rather than novelty.
- **SOURCE:** Literature audit §§2.1–2.3; E01 interpretation; historical
  Discussion hot-stove section after correction.
- **FIGURE/TABLE:** Refer back to Figure 2 only if needed.
- **SUPPLEMENT:** Extended prior-art discussion.
- **MISSING:** Short synthesis linking history to later structural models.

### 4.2 More behavioural options are not automatically corrective — approximately 225 words

- **PURPOSE:** State the E01/E02 cross-mechanism dissociation.
- **CLAIMS/EXPERIMENTS:** E01 information restoration versus E02 independent-arm
  expansion; not a controlled sign reversal.
- **SOURCE:** E01/E02 interpretation combined lesson; short-article brief.
- **FIGURE/TABLE:** Refer back to Figure 2 only if needed.
- **SUPPLEMENT:** Structured/generalizing learner future work.
- **MISSING:** One compact synthesis paragraph.

### 4.3 Immediate and dynamic value differ — approximately 225 words

- **PURPOSE:** Explain why M2 changes the relevant objective and why oracle
  disagreement is informative but not information matched.
- **CLAIMS/EXPERIMENTS:** E03 and analytic M2.
- **SOURCE:** E03 interpretation §§6–9, 13–17; Formal Methods; analytic authority.
- **FIGURE/TABLE:** Refer back to Figure 3.
- **SUPPLEMENT:** Bellman/decomposition derivations.
- **MISSING:** Compression only.

### 4.4 Objective availability and discoverability differ — approximately 225 words

- **PURPOSE:** Explain the E04 availability/discovery distinction and bounded
  relevance to peer-context preference.
- **CLAIMS/EXPERIMENTS:** E04; representation + scarcity + finite sampling.
- **SOURCE:** E04 interpretation; literature audit §§5.4–5.5; historical
  Discussion context-search section after correction.
- **FIGURE/TABLE:** Refer back to Figure 4a.
- **SUPPLEMENT:** Detailed control interpretation and prior-art boundary.
- **MISSING:** Authority-corrected giftedness bridge avoiding literal search.

### 4.5 Behavioural and objective thresholds differ — approximately 225 words

- **PURPOSE:** Interpret E05 without mechanistic decomposition or calibration.
- **CLAIMS/EXPERIMENTS:** E05; BFLPE motivates comparison cost but does not
  calibrate `bf`; fixed temperature remains a possible contributor.
- **SOURCE:** Freeze §E; literature audit §§3.2, 7–9; corrected E05 note.
- **FIGURE/TABLE:** Refer back to Figure 4b or Figure 5 if split.
- **SUPPLEMENT:** Candidate-contributor discussion.
- **MISSING:** New concise paragraph because historical prose used the retired
  temperature exclusion.

### 4.6 Implications for gifted ability concealment — approximately 225 words

- **PURPOSE:** State model-derived implications and empirical questions without
  intervention or prevalence claims.
- **CLAIMS/EXPERIMENTS:** Domain implication supported jointly by E01–E05.
- **SOURCE:** Literature audit giftedness sections; historical Discussion
  educational implications after correction; Formal Methods scope.
- **FIGURE/TABLE:** None.
- **SUPPLEMENT:** Broader empirical programme.
- **MISSING:** Authority-corrected applied synthesis using concealment/visibility-
  management terminology rather than assuming “masking” is canonical.

## 5. Limitations — 500 words

- **PURPOSE:** Consolidate the few limitations that govern interpretation,
  without becoming another Methods section.
- **PRIMARY CLAIMS:** Stylized uncalibrated model; full-information oracle;
  finite-horizon constant-step learner; tested-axis conditionality; classifier
  and inferential units; no human prevalence/intervention inference; partial
  E01–E03 generator-source reproducibility; E05 mechanism unresolved; E06/M4
  deferred.
- **EXPERIMENTS:** E01–E05.
- **SOURCE MATERIAL:** Formal Methods scope; freeze C/F/I; consistency audit;
  current-state provenance; historical Discussion limitations only after
  replacing one-seed and missing-ablation statements.
- **FIGURE/TABLE:** None.
- **SUPPLEMENT:** Full parameter, sensitivity, and provenance detail.
- **MISSING:** A newly compressed limitations section; facts already exist.

## 6. Conclusion — 225 words; maximum two paragraphs

- **PURPOSE:** Restate the benchmark contribution and bounded synthesis, then
  identify empirical validation/future M4 work without expanding scope.
- **PRIMARY CLAIMS:** Concealment in these models need not imply absence of
  objective value in authentic expression; history, endpoint discovery,
  dynamic consequences, context discoverability, and learned boundary location
  are separable.
- **EXPERIMENTS:** E01–E05.
- **SOURCE MATERIAL:** Short-article brief; argument architecture; current
  findings; historical conclusion only for broad rhetorical shape.
- **FIGURE/TABLE:** None.
- **SUPPLEMENT:** None.
- **MISSING:** Two new short paragraphs written after Results/Discussion.

## GENUINE REMAINING WRITING GAPS

These are greenfield integration gaps, not missing science and not content that
is merely too long.

| Required section | Required content/claim | Authority supplying facts | Approximate new words |
|---|---|---|---:|
| Abstract | Complete short-article abstract after body stabilization | Freeze, evidence matrix, final body | 225 |
| Introduction 1.2/1.4 | Compact identification problem and E01–E05 roadmap | Formal Methods, brief, argument architecture | 250 |
| Results transitions | Transitions connecting E01→E02→E03→E04→E05 without equal weighting | Brief, skeleton, evidence map | 150 |
| Results 3.3 | Concise explanation of the E03 map and classifier for a general reader | E03 authority set | 150 |
| Discussion 4.2 | E01/E02 cross-mechanism dissociation paragraph | Brief and E01/E02 note | 175 |
| Discussion 4.4 | Gifted-context bridge that does not literalize context search | Literature audit and E04 note | 175 |
| Discussion 4.5 | E05 interpretation after retiring G2/temperature exclusion | Freeze §E and evidence | 175 |
| Discussion 4.6 | Bounded domain implication using safe terminology | Literature audit and Formal Methods scope | 175 |
| Conclusion | Maximum two short paragraphs | Integrated article | 225 |
| **Estimated genuinely new prose** | | | **approximately 1,600 words before compression/overlap** |

The remainder of the article should be extracted, compressed, merged, or
authority-corrected from existing work. No scientific discovery is required.
