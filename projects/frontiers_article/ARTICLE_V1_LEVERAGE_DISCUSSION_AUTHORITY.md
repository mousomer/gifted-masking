# Article V1 — leverage and intervention discussion authority

**As of:** 17 August 2026
**Status:** governing authority for Article-V1 discussion of intervention-like
model manipulations. Supersedes the blanket reading of the prior prohibitions
listed in §6 below. Does not alter any frozen evidence, estimand, inferential
unit, ceiling wording, model, config, or artifact.

---

## 1. Why this document exists

The prior authorities prohibited "intervention effects" without distinguishing
two different things:

1. **A human intervention effect estimate** — that some manipulation would
   change concealment in real students, by some amount, with some reliability.
   Nothing in the frozen evidence supports this, and it stays prohibited.

2. **A model-internal leverage statement** — that within a fully specified
   environment, manipulating a named model quantity moved a named model outcome
   by a frozen amount, and that two such manipulations can be ordered.

The second is not a weaker version of the first. It is a different claim, about
the model rather than about people, and it is exactly what an
existence-and-structure paper is for. Prohibiting it removed the article's
ability to say what its own environments imply, and left seven frozen,
adjudicated contrasts unused.

The permission below is deliberately narrow enough that an adversarial reviewer
cannot read a human efficacy claim out of a compliant sentence.

---

## 2. The permission

**Article V1 may state, in Discussion, that the frozen model manipulations
identify candidate points of leverage, may order them by their frozen effect
magnitudes within a shared estimand, and may name the observable each would
require to be tested in people.**

A compliant leverage statement has four parts, all four required:

| Part | Requirement |
|---|---|
| **Model locus** | Names the model quantity manipulated (`eta`, `bf`, `lambda`, the information channel, the receptive-context distribution, the action representation). |
| **Frozen magnitude** | Quotes a frozen estimate at its ceiling wording, with its interval where one exists. |
| **Directional framing** | States the claim as a *prediction* or *candidate target*, never as an established effect. |
| **Named observable** | States what would have to be measured in people for the prediction to be tested or contradicted. |

A statement missing the fourth part is a model result, not a leverage statement,
and belongs in Results.

### 2.1 Ordering is permitted, with a condition

Two manipulations may be ranked against each other **only when they share an
estimand, a stratum, and a scale**, and **only when their frozen intervals are
disjoint**. The E01 pair (forced exploration versus counterfactual feedback on
final-window mask rate, rejected stratum, pooled selector) satisfies this; the
publication build asserts the disjointness at extract time and fails closed if it
ever ceases to hold.

Cross-experiment magnitudes are **not** commensurable and may not be ranked.
E01 mask-rate reductions, E04 K-slope changes, and E05 boundary displacements are
different quantities. They may be tabulated side by side as candidates for
attention, with the non-commensurability stated in the same table.

### 2.2 One scope paragraph, not per-sentence hedging

The leverage section carries **one** scope paragraph covering every lever. Prior
practice attached a disclaimer to each individual manipulation, which produced
the tone problem documented in
`ARTICLE_V1_DRAFT_REVIEW_RESULTS_TONE_INTERVENTION.md` §B without adding any
scientific protection. One clear scope statement placed once is the standard.

### 2.3 Levers that operate on the benchmark

A manipulation that changes the *objective* boundary rather than the learner's
distance from it — currently only `eta` in M2 — may be described as such, and may
be described as the more robustly established kind of lever, because it is
deterministic rather than estimated. It may not be described as more *effective*,
which would be a comparison of magnitudes across incommensurable axes.

---

## 3. What remains prohibited

Unchanged from the prior authorities:

1. Any statement that a manipulation would change concealment **in people**, by
   any amount, or with any reliability.
2. Any efficacy, benefit, or recommendation claim addressed to educational
   practice, presented as established.
3. Any calibrated human magnitude — a comparison-cost threshold, a receptivity
   level, a weighting parameter, or a dose — read off a model quantity.
4. Any claim that the model identifies *which* mechanism operates in a person.
5. Ranking of magnitudes across experiments with different estimands (§2.1).
6. Presenting a leverage prediction as a finding of the article rather than as a
   consequence of its models.
7. Everything in `ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md` §I items 1–9, which
   this document does not touch.

---

## 4. Worked compliant and non-compliant examples

| Non-compliant | Compliant |
|---|---|
| "Counterfactual feedback is 2.5× more effective than forced exploration at reducing concealment." | "Within the model, counterfactual feedback reduced final-window masking by 0.118 [0.110, 0.127] against 0.047 [0.033, 0.060] for forced exploration on the same stratum and scale — about 2.5 times as much, with disjoint intervals. The prediction is that designs revealing the outcome of undisclosed ability outperform designs that only create occasions to disclose; testing it requires observing both disclosure opportunities and the responses to disclosures not made." |
| "Schools should raise the proportion of receptive settings." | "The K decline was largely removed when receptive contexts were held at a fixed proportion (+0.060 flat, +0.112 hierarchical), so the model's target is the proportion of receptive settings rather than their number. The corresponding measurement is the distribution of receptivity across a student's actual settings, not their count." |
| "Making stigma escapable is the most effective intervention." | "Raising the escape rate from 0 to .8 lowers the *objective* boundary from .384 to .269, so it changes what is optimal rather than the learner's distance from it. This is the one lever in the table that is deterministic rather than estimated. Whether adverse standing is in fact exitable, and on what timescale, is the observable it implies." |
| "Graded disclosure options harm students." | "In this specification, adding independent graded arms raised engagement by 0.255 while lowering optimal-endpoint selection by 0.329, and the affine-reward theorem shows the intermediate levels create no offsetting objective benefit. The prediction is that a graduated-disclosure design whose steps do not let evidence generalize across levels trades endpoint discovery for breadth; it should disappear where experience at one level informs neighbouring levels." |

---

## 5. Routing changes

| Item | Was | Now |
|---|---|---|
| `E01-C2-FORCED-MASK`, `E01-C2-FORCED-REGRET` | supplement | **Results §3.1 and Discussion leverage section** |
| `E01-C2-CF-MASK`, `E01-C2-CF-REGRET` | supplement | **Results §3.1 and Discussion leverage section** |
| `E01-04`, `E01-05` in `ARTICLE_V1_CLAIM_LEDGER.md` | `KEEP / BACKGROUND_ONLY` | **`KEEP / LEVERAGE`** — contribution-bearing in Discussion under §2 |
| `E01-C3-LAMBDA` | unrouted | **Results, as an identification result** (see §7) |
| `E03-C5-THRESHOLDS` | sensitivity supplement | **Results §3.4 headline** |
| E03 `eta`, E04 abundance controls, E05 `bf` | sensitivity axes only | **also admissible as leverage loci** under §2 |

No estimate, interval, estimand, or ceiling wording changes. This is a routing
and framing authority only.

---

## 6. Amended prior statements

The following are hereby read as subject to this document. Each has been
annotated in place with a pointer here.

- `ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md` §I item 10.
- `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md`, "PLAUSIBLE BUT UNTESTED",
  human-intervention-benefit bullet.
- `CLAIM_LEDGER.md` C10.
- `ARTICLE_V1_CLAIM_LEDGER.md` rows E01-04 and E01-05.
- `ARTICLE_V1_CLAIM_EVIDENCE_FIGURE_MAP.md` rows E01-03 and E01-04.
- `ARTICLE_V1_SHORT_ARTICLE_SKELETON.md` Discussion-implications section.
- `ARTICLE_V1_STAGE3_EXTRACTION_PACKETS.md` Discussion packet.
- `RDS.md` §"out of scope", causal-intervention bullet.

In every case the prohibition on **human** intervention claims is retained
verbatim. Only the blanket reading — that no intervention-like model manipulation
may be discussed at all — is superseded.

---

## 7. Note on E01-C3-LAMBDA

The weighting result is **not** a leverage statement and must not be written as
one, despite being the largest single contrast in the cascade.

At the tested cell `p=.65` the objective gap is `3(.65) − 2.15 = −0.20`, so
masking is the objective optimum. The `lambda=0.5` learner therefore *diverges*
from the objective optimum and the `lambda=2.5` learner *conforms* to it. Writing
this as "reducing negative-outcome weighting reduces concealment" would imply that
the reduction is an improvement, which at this cell it is not.

The licensed framing is **identification**: a learner-side parameter moves
observed concealment across most of its range with the environment held exactly
fixed, so an observed concealment rate constrains the environment only weakly
unless the weighting is independently known. This is a constraint on inference
from behaviour, and it belongs in Results beside the exact `p*_lambda` boundary.

It may additionally be named in the leverage discussion as **the principal
confound** for every other lever in the table, which is a statement about
identification, not about efficacy.
