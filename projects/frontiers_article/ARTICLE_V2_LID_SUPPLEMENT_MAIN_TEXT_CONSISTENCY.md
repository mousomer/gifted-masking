# Article V2 — Supplement/Main-Text Consistency Matrix

**Audit date:** 21 August 2026

**Scope:** active main manuscript and V2 Supplementary Methods; E01–E05 only

**Verdict:** CONSISTENT

This record checks whether a technically competent reader can identify the
exact statistic and procedure behind each main-text result by reading the main
Methods together with the supplement. Repository authority, rather than either
narrative artifact alone, resolves any future discrepancy.

## Claim and method mapping

| Main claim/method | Main-text location | Supplement location | Controlling authority | Consistency result |
| --- | --- | --- | --- | --- |
| Main and Supplement display the exact final “Does Not Uniquely Reveal” title | title | display title | Stage 10.5 title decision | CONSISTENT |
| Common $Q_0$, $\alpha$, $\tau$, $\lambda$; subjective reward transform; selected-action update; stable softmax | §§2.1, 2.7 | §§S1.1–S1.4 | ARTICLE_V1_MODEL_METHODS.md; standard configs | CONSISTENT |
| Final window is last $\lceil .2T\rceil$ steps | §§2.1, 2.7 | §S1.4 | ARTICLE_V1_MODEL_METHODS.md | CONSISTENT |
| E01 reward equation and exact $p^*=43/60$ | §2.2 | §S2.1 | ARTICLE_V1_MODEL_METHODS.md; analytic-results authority | CONSISTENT |
| E01 initial accepted/rejected conditioning and subsequent-authentic-sampling estimator | §§2.2, 3.1 | §S2.2 | E01 config, manifest, interpretation note, evidence freeze | CONSISTENT |
| E01 pseudo-regret is algebraically linked to sampling | §§2.2, 3.1 | §S2.2 | manuscript evidence freeze §C.5 | CONSISTENT |
| E01 forced exploration and counterfactual feedback | §§2.2, 3.1; Figure 2B | §S2.3 | E01 config, manifest, effects artifact | CONSISTENT |
| E01 five-master Student-$t$ inference | §§2.7, 3.1 | §S2.4 and §S7 | inferential audit; E01 effects artifact | CONSISTENT |
| E02 five levels are independent arms and the objective is affine/end-point optimal | §§2.3, 3.2, 4.3 | §S3.1 | model methods; E02 config and implementation contract | CONSISTENT |
| E02 continued non-zero disclosure, full-authentic rate, and unique-modal endpoint statistics | §§2.3, 3.2; Figure 2C | §S3.2 | E02 evidence and interpretation authorities | CONSISTENT |
| E02 common-random-number architecture pairing | §2.3 | §S3.2 and §S7 | E02 manifest; inferential audit | CONSISTENT |
| E03 Neutral/Accepted/Stigmatized reward-before-transition kernel | §2.4; Figure 3A | §S4.1 | model methods; M2 transition authority | CONSISTENT |
| E03 $\gamma=.9$ Q-learning update and $D_N(V)$ | §2.4 | §S4.2 | model methods; E03 config | CONSISTENT |
| E03 full-information value iteration comparator | §§2.4, 4.4 | §S4.3 | model methods; analytic-results and policy-enumeration audits | CONSISTENT |
| E03 $21\times17$ grid, Neutral-visit adequacy, tie/inadequacy rules, and four-of-five stability | §§2.4, 3.3 | §S4.4 | E03 config, classifier authority, evidence freeze | CONSISTENT |
| E03 $243/357$ denotes tested-grid learned–objective disagreement; the seven inconclusive cells comprise five inadequate-across-all-master cells plus two failures of the four-of-five rule | §3.3; Figure 3B | §S4.4 | frozen E03 cells/stability artifacts | CONSISTENT |
| E04 four architectures and context/action indexing | §2.5 | §§S5.1–S5.2 | model methods; E04 config; maintained estimator code | CONSISTENT |
| E04 full-information opportunity remains $K$-invariant in the one-good-context design | §§2.5, 3.4 | §S5.1 | model methods; E04 interpretation note | CONSISTENT |
| E04 primary estimator uses deterministic first-index argmax; a learner qualifies only when that indexed arm is good-context authenticity | §§2.5, 3.4; Figure 4A | §S5.3 | Stage 9 correction; maintained metric mean_settled_any_good_auth_argmax | CONSISTENT |
| E04 fixed/random identity, two-good, proportional-25%, global-mask, and fixed-known-good controls; the multiple-good secondary values are changes in the per-$\log_2 K$ slope | §§2.5, 3.4 | §§S5.3–S5.4 | E04 effects, evidence row E04-C6-MULTIPLE, canonical cells/equivalence table | CONSISTENT |
| E04 strict unique-mode result is a diagnostic, not replacement estimator | §3.4 | §S5.3 | E04 evidence freeze | CONSISTENT |
| E05 $R_M=.75$, $R_G=1.15-.85b_f$, advantage $.40-.85b_f$, and $b_f^*=8/17$ | §§2.6, 3.5 | §S6.1 | model methods; E05 analytic artifact | CONSISTENT |
| E05 learned response is a multi-action across-learner modal first-index-argmax fraction | §§2.6, 3.5; Figure 4B | §S6.2 | E05 interpretation/evidence authority | CONSISTENT |
| E05 non-increasing equal-weight PAVA, strict in-range .5 inversion, interpolation, and plateau midpoint | §2.6 | §S6.3 | E05 model methods and transition artifact | CONSISTENT |
| E05 10,000-resample complete-master-curve bootstrap | §§2.6, 2.7, 3.5 | §S6.4 and §S7 | E05 manifest and inferential audit | CONSISTENT |
| E05 hierarchical crossing is left-censored below .30 and is not extrapolated | §§2.6, 3.5; Figure 4B | §§S6.3–S6.4 | E05 transition artifact | CONSISTENT |
| Master seeds, semantic stream namespaces, and top-level inferential units | §2.7 | §S7 | five manifests; inferential audit | CONSISTENT |
| Secondary evidence remains secondary and does not identify a headline mechanism | Results/Discussion hierarchy | §S8 | evidence freeze and interpretation notes | CONSISTENT |
| Artifact verification is distinct from figure regeneration and experiment reproduction | §2.7; Limitations; Data/code statement | §S9 | evidence freeze; generator-source provenance audit; figure provenance | CONSISTENT |
| E01–E03 exact historical generator source states are unrecovered | §2.7; Limitations | §S9.1 | generator-source provenance audit/index | CONSISTENT |

## Result-claim completeness check

| Main Results subsection | Exact statistic identifiable from main + supplement? | Missing definition |
| --- | --- | --- |
| §3.1 E01 | YES | None |
| §3.2 E02 | YES | None |
| §3.3 E03 | YES | None |
| §3.4 E04 | YES | None |
| §3.5 E05 | YES | None |

## Boundary checks

- E01 pseudo-regret is not presented as independent evidence.
- E02 contains no cross-level generalization and no interior static optimum.
- E03 uses reward-before-transition ordering and a full-information,
  infinite-horizon oracle.
- E03 tested-grid coverage is not prevalence.
- E04 uses the maintained deterministic first-index argmax, not “any tied
  good-authentic arm qualifies.”
- E04 does not imply that more contexts generically cause masking.
- E05 uses the multi-action modal-response/PAVA estimator and contains no
  binary-softmax or G2 reasoning.
- E05's comparison-cost axis is not temporalized.
- E06/M4 contributes no numerical result, estimator, or figure.

No BLOCKED_BY_SUPPLEMENT_AUTHORITY condition was found.

## Stage 11.5 bounded-repair verification

The Supplement display title now exactly matches the main title. E03's public
seven-cell category now preserves its five-plus-two stability composition, and
E04's four multiple-good-context values are identified as changes in the
estimated per-$\log_2 K$ slope rather than outcome-level changes. These repairs
change no estimator, result value, evidence artifact, or E05 route. All rows
above remain `CONSISTENT`.

## Stage 10.5 reconciliation verification

The post-citation reconciliation changed no method, estimator, result, or
main–supplement route. The title was narrowed from “Does Not Reveal” to “Does
Not Uniquely Reveal”; the Abstract already used the corresponding
underidentification claim and required no change. Introduction §1.2 now
distinguishes established equifinality from the article's concrete
learning-and-opportunity decomposition. Discussion §4.4 now distinguishes
established dynamic disclosure theory from E03's persistent-state and
finite-learner/full-information comparison. Environmental legibility remains
a model-derived descriptive term with partial overlap and open empirical
operationalization. Submission-facing provenance wording was cleaned without
changing any reproduction classification. All rows above remain `CONSISTENT`.
