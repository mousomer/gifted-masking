# Article V1 — Stage 3 Extraction Packets

**Working status:** drafting aid; not a scientific authority.

**Binding evidence order:** evidence freeze and matrix → consistency audit and
analytic authority → interpretation notes → reusable historical prose. Scope is
E01–E05 only; E06/M4 is excluded.

## Introduction — target 1,050 words

- **Claim IDs:** FRAME-01, SYN-02, DOMAIN-01.
- **Authority:** literature audit; Formal Methods §§1–3; short-article brief.
- **Use:** gifted social-coping/visibility management; the identification
  problem; objective versus learned value; E01→E05 roadmap.
- **Do not use:** deficit stereotypes, prevalence language, a claim that the
  models estimate a human learning rule, or M4 as part of this article.
- **Figure route:** introduce Figure 1 only as a progression schematic.
- **Gap:** compact transition from substantive setting to oracle-comparator
  method.

## Main Methods — target 1,450 words

- **Claim IDs:** FRAME-01, E02-A, E03-01, E04-A, E05-01/02/04.
- **Authority:** Formal Methods; Analytic Results; evidence freeze §D.
- **Retain:** common Q learner, stable softmax, final-window estimands, model
  definitions, static/DP benchmarks, E03 classifier, E04 architectures, E05
  response/PAVA/censoring, replication units and uncertainty.
- **Move out:** full kernels, reward tables, grids, seeds, implementation
  mechanics, all derivations, full bootstrap and provenance machinery.
- **Do not use:** a binary-softmax interpretation of the E05 crossing.

## E01 Results — target 250 words

- **Claim IDs:** E01-01–05.
- **Authority/data:** freeze `E01-C2-*`; hot-stove effects CSV.
- **Numbers:** sampling −0.025837 [−0.035753, −0.015922]; final mask −0.000343
  [−0.011605, +0.010918]; forced exploration +0.046590; counterfactual
  feedback +0.118135.
- **Interpretation:** early rejection reduced sampling but did not detect a
  persistent final-window masking difference. Regret is the exact action-count
  translation `Delta R_norm = -(1999/2000) Delta A`.
- **Figure:** 2A. **Do not use:** a final-mask persistence claim.

## E02 Results — target 300 words

- **Claim IDs:** E02-01–04, E02-A.
- **Authority/data:** freeze `E02-C4-*`, `E02-S1-ARM-REWARDS`.
- **Numbers:** nonzero disclosure +0.255040 [0.253004, 0.257077]; full endpoint
  −0.328692 [−0.342037, −0.315348]; optimal-endpoint modal probability
  −0.221740 [−0.288755, −0.154724].
- **Interpretation:** independent graded actions alter information allocation;
  M1 expected reward is affine and strict static optima are endpoints.
- **Figure:** 2B–C. **Do not use:** a welfare claim from normalized regret or a
  disclosure-specific psychological mechanism.

## E03 Results — target 600 words

- **Claim IDs:** E03-01–03.
- **Authority/data:** freeze `E03-C5-*`; M2 effects/stable-cell tables.
- **Numbers:** `n=160`, `T=1000`; 243/357 tested cells; 350/357 stable;
  7 inconclusive for inadequate Neutral visits.
- **Interpretation:** aggregate final-window Neutral action counts favour mask
  while full-information DP selects authenticity. This is tested-grid coverage
  with a defined classifier, not prevalence, individual behaviour, Q ordering,
  or information-matched regret.
- **Figure:** 3. **Do not use:** `226/357`, `.950`, lock-in, or a learned
  threshold.

## E04 Results — target 650 words

- **Claim IDs:** E04-01–04, E04-A.
- **Authority/data:** freeze `E04-C6-*`; architecture effects/curves.
- **Numbers:** flat K16−K1 −0.2340 [−0.246417, −0.221583]; hierarchical −0.4704
  [−0.511031, −0.429769].
- **Interpretation:** the primary outcome is final-window argmax classification
  as authentic in a good context. K does not change the one-good-context
  full-information optimum; controls bound a conjunction of scarce receptivity,
  representation, and finite discovery.
- **Figure:** 4A. **Do not use:** “settled”, literal human context search, or
  architecture-general effect magnitude.

## E05 Results — target 600 words

- **Claim IDs:** E05-01–05.
- **Authority/data:** freeze `E05-C7-*`; crossover analytic/transitions data.
- **Numbers:** objective `8/17=0.470588`; learned flat PAVA crossing 0.312852
  [0.307836, 0.316918]; objective advantage about 0.134; hierarchical response
  0.1176 at `.30` and left-censored below the fitted range.
- **Interpretation:** the response is an across-child final-window modal-arm
  fraction, not a softmax probability, Q equality, or psychological threshold.
  Quantitative mechanism decomposition is unresolved.
- **Figure:** 4B or split Figure 5. **Do not use:** G2 or temperature exclusion.

## Synthesis and Discussion — target 1,350 words

- **Claim IDs:** SYN-01, SYN-02, DOMAIN-01, E05-05.
- **Authority:** interpretation notes; literature audit; claim map.
- **Required new prose:** E01/E02 cross-mechanism dissociation; bounded E04
  giftedness bridge; authority-correct E05 paragraph; domain implication.
- **Distinguish:** model result, interpretation, domain implication, and human
  empirical claim. **Do not use:** intervention or prevalence inference.

## Limitations and Conclusion — targets 500 and 225 words

- **Authority:** Formal Methods scope; freeze §§E–F; consistency audit.
- **Must include:** stylized/reference parameters, oracle status, finite learner
  and tested-axis conditionality, construct mapping, no prevalence/intervention
  inference, E01–E03 provenance limit, and unresolved E05 decomposition.
- **Conclusion:** two paragraphs maximum; restate only routed contribution.

## Figure and supplement routes

- Figure 1 remains a main-text model-progression schematic.
- Figure 2 requires caption/presentation restructuring so dependent E01 regret
  is subordinate; no data change is authorized.
- Figure 3 retains tested-grid/non-prevalence language.
- Figure 4 retains exact E04 outcome wording and E05 hierarchical censoring;
  an optional layout split requires a later presentation-only decision.
- Supplementary Methods receives complete equations, kernels, parameters,
  classifiers, seeds, and bootstrap details; repository documentation retains
  hashes, validators, build instructions, and provenance archaeology.
