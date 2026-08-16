# Article V1 Short-Article Brief

**Document class:** Stage 2 routing document; not a new scientific authority

**Status:** routing complete; `READY_FOR_MANUSCRIPT_EXTRACTION`

**Primary evidence:** E01–E05 only

**Deferred:** E06/M4 future work

If this brief conflicts with the manuscript evidence freeze, evidence matrix,
or model-analysis consistency audit, those authorities win.

## A. Manuscript objective

Build a normal 6,000–8,000-word first research article demonstrating measurable
learned–objective divergence in a controlled progression of
ability-concealment learning environments. The article’s central methodological
contribution is the repeated comparison of finite learned behaviour with an
explicit analytic or dynamic-programming objective benchmark. The paper should
show that immediate value, dynamic value, discoverability, and a learned
behavioural boundary are distinct quantities rather than treating observed
concealment as evidence that concealment is objectively preferable.

This is an existence-and-structure computational modelling article. It is not
a calibrated model of gifted children, a prevalence estimate, an intervention
evaluation, or a comprehensive report on the entire research programme.

## B. Evidential scope

**PRIMARY ARTICLE V1: E01–E05 ONLY.** These five frozen experiments and their
exact objective anchors are sufficient for the first article. No new E01–E05
experiment, seed, inference, result regeneration, model variant, or scientific
investigation is required before manuscript construction.

**E06/M4 is deferred.** It may be named as future work because it introduces
endogenous environment–behaviour feedback and materially enlarges the
conceptual scope. Deferral does not mean that E06 is invalid, failed,
disproven, unusable, abandoned, or deleted. No E06 numerical result may support
the primary Article V1 Results or conclusion.

## C. Scientific progression

| Experiment | Manuscript function | Required boundary |
|---|---|---|
| E01 | History-dependent sampling: initial rejection reduces later authentic sampling; information-restoring manipulations improve correction. | The final-mask contrast is approximately null. Sampling and normalized pseudo-regret are algebraically linked, not independent discoveries. |
| E02 | Endpoint discovery: independent graded actions increase nonzero disclosure while reducing full-authentic and optimal-endpoint behaviour. | Expected reward is affine in disclosure. Intermediate disclosure is not generally a strict static optimum, and normalized regret is the disclosure-distance statistic `1-d`. |
| E03 | Dynamic policy disagreement: aggregate final-window Neutral action counts favour masking in tested cells where the exact full-information DP comparator selects authenticity. | The correct count is `243/357` at `n=160`, `T=1000`, subject to visit adequacy. It is tested-grid coverage, not prevalence, child frequency, or a Q-ordering classifier. |
| E04 | Social/context discoverability: finite learners become less likely to classify an authentic action in a good context as the final-window argmax as the maintained discovery problem expands. | Use the exact final-window argmax definition. Keep `flat_2k`, `hierarchical`, `global_mask`, and `fixed_known_good` identifiable. The one-good-context full-information optimum is K-invariant. |
| E05 | Learned/objective boundary displacement: the flat behavioural response crosses 0.5 before objective environmental indifference. | The crossed response is an across-child modal-classification fraction, not a softmax probability or Q-value equality. The displacement is demonstrated; its decomposition is unresolved. |

The conceptual sequence is:

```text
history
-> endpoint discovery
-> dynamic disagreement
-> social discoverability
-> boundary displacement
```

## D. Main conceptual synthesis

```text
immediate value
!= dynamic value
!= discoverability
!= learned behavioural boundary
```

E01 and E02 supply an important cross-mechanism dissociation. In E01, forced
authentic exploration or counterfactual feedback restores missing information
after adverse experience and improves correction. In E02, adding independently
learned compromise actions preserves partial expression while reducing
discovery of the optimal endpoint. These are different interventions in
different models, not a controlled sign reversal, and the synthesis must not be
anchored on pooled regret.

Do not add a broader synthesis claim unless it is already permitted by the
freeze, evidence matrix, consistency audit, claim ledger, and relevant
interpretation authority.

## E. Main-text constraints

- Main text: approximately 6,000–8,000 words.
- Main Methods: approximately 1,200–1,600 words.
- Main figures: approximately four to five.
- Conclusion: no more than two paragraphs.

The existing long Formal Model and Methods authority is preserved, but it is
not the target main-text Methods section. A later stage will separate it into
concise main Methods, Supplementary Methods, and repository
reproducibility/technical documentation. Do not perform that compression while
building the skeleton.

## F. Authority pointers

Use these in precedence order for manuscript decisions:

1. [ARTICLE_V1_EVIDENCE_MATRIX.csv](ARTICLE_V1_EVIDENCE_MATRIX.csv) — exact
   claim, artifact, estimand, inferential-unit, and wording-ceiling authority.
2. [ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md](ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md) — mathematical and interpretive corrections.
3. [ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md](ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md) — manuscript-facing integration and hard prohibitions.
4. [ARTICLE_V1_ANALYTIC_RESULTS.md](ARTICLE_V1_ANALYTIC_RESULTS.md) — analytic and dynamic-programming anchors.
5. [ARTICLE_V1_LITERATURE_AUDIT.md](ARTICLE_V1_LITERATURE_AUDIT.md) — construct, citation, and novelty boundaries.
6. [ARTICLE_V1_CLAIM_LEDGER.md](ARTICLE_V1_CLAIM_LEDGER.md) — publication wording decisions.
7. [ARTICLE_V1_E01_E02_INTERPRETATION.md](ARTICLE_V1_E01_E02_INTERPRETATION.md), [ARTICLE_V1_E03_INTERPRETATION.md](ARTICLE_V1_E03_INTERPRETATION.md), [ARTICLE_V1_E04_INTERPRETATION.md](ARTICLE_V1_E04_INTERPRETATION.md), and [ARTICLE_V1_E05_INTERPRETATION.md](ARTICLE_V1_E05_INTERPRETATION.md) — subordinate per-experiment framing notes. The E05 note’s temperature/G2 exclusion is superseded.

Historical Results, Discussion, and revision-note files are source material
only. Never copy a number or claim from them without re-deriving it against the
authorities above.

## G. Critical traps

- No `226/357`, `63.3%`, or unsupported E03 `.950` statement in active Article
  V1 prose. Use `243/357` only with its exact tested-grid definition and do not
  headline it as prevalence.
- No independent-regret overclaim in E01 or E02. In E01,
  `Delta R_norm = -(1999/2000) Delta A` for the relevant cells. In E02,
  normalized regret is `1-d` in the authenticity-optimal affine cells.
- No vague E04 “settling.” Prefer “final-window argmax classification as
  authentic in a good context,” and define the deterministic argmax procedure.
- No suggestion that the proximity of the E04 hierarchical `0.4704` effect to
  `8/17` is meaningful.
- No E05 binary-softmax, Q-equality, or G2 temperature-exclusion argument.
- No extrapolated hierarchical E05 crossover. The response is already below
  0.5 at `bf=0.30`; report the crossing as left-censored below the resolved
  range.
- No non-unit-`lambda` explanation of headline E01–E05 results. Their headline
  configurations use `lambda=1`; retain legitimate labelled sensitivity cells.
- No E06/M4 primary result, hysteresis claim, or endogenous-receptivity result.
- No claim that all original experiments are exactly source-reproducible from
  Git. E04/E05 generator source was recovered; the exact historical dirty
  generator state for E01–E03 was not fully retained.
- No claim that the models establish human prevalence, calibrated thresholds,
  educational treatment effects, or irreversible behaviour.

## H. Next stage

> Build the short-article skeleton and claim/evidence/figure map before drafting prose.

That stage should allocate the word budget, assign each intended claim to a
frozen authority and evidence row, decide which results belong in approximately
four to five main figures versus supplementary material, and stop. It must not
write the manuscript, compress Methods, regenerate figures, or reopen E06/M4.
