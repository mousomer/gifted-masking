# Article V2 L&ID — Stage 12R Abstract Compression Audit

**Performed:** 21 August 2026

**Authorized stage:** `ARTICLE_V2_LID_STAGE12R_SUBMISSION_UNBLOCKING_AND_FINAL_ACTIVATION`

**Scope:** bounded Abstract-only scientific compression. No other manuscript
text, no figure, no numerical result, no reference, and no Supplement content
was changed by this audit.

## 1. Pre-edit candidate verification

Verification was completed **before** any edit. No candidate drift was found,
so `BLOCKED_BY_CANDIDATE_DRIFT` was not raised.

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Stage 11.5 repaired-candidate manifest | `1ef1a5252891d7f69c8e4f112765256d4a41dd51381ef4672d15b06801168124` | exact match | PASS |
| Repaired candidate contents | 67/67 VALID | 67/67 VALID | PASS |
| Protected E01–E05 outputs | 33/33 VALID | 33/33 VALID (E01 5/5, E02 6/6, E03 8/8, E04 7/7, E05 7/7) | PASS |
| Evidence-matrix references | 18/18 VALID | 18/18 VALID | PASS |
| Archive payload manifest | 101/101 VALID | 101/101 VALID | PASS |
| Evidence ZIP SHA-256 | `71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb` | exact match | PASS |
| Stage 12 submission-manifest SHA-256 | `3c6a25d544e987dcfcd3aa2be22096834714832da47902cd3eb5724cf17f2f15` | exact match | PASS |
| Pre-edit manuscript SHA-256 | `217d259929f5d0c585bf9da1de3c33befb8403b57a79a0c4f5257627ab0f5199` | exact match | PASS |
| Supplement SHA-256 | `a413ee282e108dc225d8e2f29b74263dbdb514eb5cc6af89eeec64267dc929ce` | exact match | PASS |
| Stage 11.5 reconciliation SHA-256 | `59d9fbaec87a6660986fb3cc99c666c8cb2f99d4c3b970b51fa86cd777743f30` | exact match | PASS |

## 2. Word counts and counting convention

The convention is the Stage 12 convention: Pandoc Markdown → plain-text
conversion, heading-excluded, keyword line excluded, hyphenated and en-dash
compounds counted as one word.

| Quantity | Value |
| --- | ---: |
| Pre-edit Abstract, Stage 12 recorded count | 221 |
| Pre-edit Abstract, reproduced Pandoc count | **219** |
| Post-edit Abstract, reproduced Pandoc count | **144** |
| Post-edit Abstract, raw whitespace count | 144 |
| Journal hard maximum | 150 |
| Margin | 6 words |

**Recorded discrepancy.** The Stage 12 QA recorded 221 words for the
pre-edit Abstract. The reproducible Pandoc count under the stated convention is
219. The 2-word difference is a historical counting artifact in the Stage 12
record. It is immaterial: both counts exceed 150, and both counting methods
return 144 for the revised Abstract. The discrepancy is recorded rather than
silently corrected, and the Stage 12 QA document is left unaltered as a
historical record.

## 3. Content hashes

| Artifact | SHA-256 |
| --- | --- |
| Pre-edit Abstract block (4 paragraphs, lines 13–19) | `70db69f373065d4d7d08453a035ac2c884098e0cfb9f47afc54d38490820dd7f` |
| Post-edit Abstract block (1 paragraph, line 13) | `b9fc239c6a871d39f67aa3d53eb2f6610ec70558d45e3c589099cdc587321123` |
| Pre-edit manuscript source | `217d259929f5d0c585bf9da1de3c33befb8403b57a79a0c4f5257627ab0f5199` |
| Post-edit manuscript source | `802aee6ffaa9d8b429f90d27b55858dc8f6913e91a918b005f8f50092f1e31bc` |

The predecessor Stage 11.5 repaired-candidate manifest is **not** updated. It
retains the historical identity of the audited candidate. After this authorized
edit, that manifest necessarily reports exactly one intentional delta, at
`projects/frontiers_article/ARTICLE_V2_LID_MANUSCRIPT_DRAFT.md`, and 66/67
otherwise-unchanged inputs. Both hashes are recorded above so the transition is
fully reconstructible.

## 4. Candidate generation and scoring

Five candidate compressions were produced internally. Only the selected
candidate was written into the manuscript.

| Candidate | Words | ≤150 | E01 | E02 | E03 | E04 | E05 | Underident. | No new claim | Readability | Outcome |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A — mechanism list rephrased to E02-specific wording | 145 | yes | ok | ok | ok | ok | ok | ok | ok | good | rejected: mechanism list drifted from the authority's "action representation" scope term |
| B — two merged two-result sentences | 151 | **no** | ok | ok | ok | ok | ok | ok | ok | fair | rejected: over the hard limit |
| C — one sentence per result, short conclusion | 144 | yes | ok | ok | ok | ok | ok | ok | ok | good | superseded by E |
| D — C plus "rather than infer them from concealment" | 150 | yes (exactly) | ok | ok | ok | ok | ok | ok | ok | good | rejected: zero margin against portal counting variation |
| **E — selected** | **144** | **yes** | **ok** | **ok** | **ok** | **ok** | **ok** | **ok** | **ok** | **high** | **selected** |

Candidate E restores the frozen source's own wording wherever the compression
did not require a change ("subsequent", "but reduced", "When actions changed
future social state"), so per-sentence drift from the audited text is minimized.

## 5. Sentence-by-sentence delta audit

Old sentence numbering follows the frozen 4-paragraph Abstract.

| # | Old sentence (abridged) | Disposition | Classification |
| ---: | --- | --- | --- |
| S1 | "Gifted learners may reduce the visibility of ability in social settings, yet similar concealment need not reflect the same learner–environment relationship." | retained verbatim | `PURE_COMPRESSION` (no change) |
| S2 | "Observed behaviour alone may therefore underidentify whether lower visibility reflects current social conditions, learned expectations, the available action representation, or difficulty recognizing receptive alternatives." | removed as a separate sentence; its content is carried by the final conclusion sentence, which names current social conditions, learned expectations, and discoverability of receptive opportunities | `MECHANISM_GROUPED` |
| S3 | "We used five controlled reinforcement-learning experiments with finite learners to separate the effects of social-feedback history, independently learned disclosure options, persistent social consequences, contextual discoverability, and learned versus environmental decision boundaries." | retained, tightened to "Five controlled reinforcement-learning experiments with finite learners separated …"; the second list item is stated as the authority's scope term "action representation" | `MECHANISM_GROUPED` |
| S4 | "Each experiment compares learned actions with the stipulated payoff structure or, where relevant, a full-information dynamic benchmark." | removed | `REDUNDANT_WITH_BODY` — §7 first priority; both comparators survive explicitly in the retained result sentences ("full-information dynamic optimum", "stipulated environmental crossover") |
| S5 | E01 result | retained verbatim | `PURE_COMPRESSION` (no change) |
| S6 | E02 result | retained verbatim | `PURE_COMPRESSION` (no change) |
| S7 | E03 result | retained verbatim | `PURE_COMPRESSION` (no change) |
| S8 | E04 result | retained verbatim | `PURE_COMPRESSION` (no change) |
| S9 | "In the comparison-cost experiment, the learned behavioural crossing was 0.313, below the stipulated environmental crossover of 0.471." | tightened to "The learned comparison-cost crossing was 0.313, below the stipulated environmental crossover of 0.471." (−4 words) | `PURE_COMPRESSION` |
| S10 | "These controlled models show why concealment cannot uniquely identify current adaptation, learned expectation, or the discoverability of receptive opportunities." | merged with S2 into "Observed concealment therefore does not uniquely identify current social conditions, learned expectations, or the discoverability of receptive opportunities" | see §5.1 |
| S11 | "Empirical studies should measure current social conditions, feedback history, expectations, behavioural expression, subsequent sampling, and contextual access separately rather than infer them from concealment alone." | compressed to "empirical studies should measure these separately" | `REDUNDANT_WITH_BODY` — §7 fourth priority; the full six-item programme is retained in §4.7 |

### 5.1 Explicit inspection of the one item requiring it

The only phrase that could be read as a removed claim is **"current
adaptation"** in S10, replaced by "current social conditions" in the merged
conclusion sentence.

Inspection outcome: **not `CLAIM_REMOVED`**; classified `MECHANISM_GROUPED`.
Justification, checked explicitly:

1. §5 of the governing authority specifies the required Conclusion as exactly
   three items — "current conditions, learned expectations, or opportunity
   discoverability" — and the revised sentence states all three.
2. "current social conditions" is not new wording; it is the frozen Abstract's
   own phrase from S2.
3. The adaptiveness claim is **not** removed from the Abstract. It is stated
   more directly, and as a result rather than an inference, by the retained E03
   sentence: "learned masking diverged from the full-information dynamic
   optimum in some tested conditions."
4. The body retains the distinction in full, including §4.4 ("Persistent social
   consequences change what is objectively adaptive") and §4.7 ("… separate …
   current adaptation from learned avoidance").

No other removed phrase was classified `CLAIM_REMOVED`. No result-defining
distinction was deleted to satisfy the word limit.

## 6. Post-revision invariant audit (§11)

| Invariant | Required | Revised Abstract text | Result |
| --- | --- | --- | --- |
| Problem | similar concealment can arise from different learner–environment relationships | "similar concealment need not reflect the same learner–environment relationship" | PASS |
| Design | five controlled reinforcement-learning experiments | "Five controlled reinforcement-learning experiments with finite learners" | PASS |
| Mechanistic scope | all five mechanisms, grouping permitted | "social-feedback history, action representation, persistent social consequences, contextual discoverability, and learned versus environmental decision boundaries" | PASS |
| E01 | reduced later authentic sampling, **no** detected persistent final-window masking increase | "reduced subsequent authentic sampling without a detected persistent final-window masking effect" | PASS — no implication of persistent endpoint masking |
| E02 | two-sided: sustained non-zero disclosure **and** reduced full-authentic endpoint | "sustained non-zero disclosure but reduced selection of the full-authentic endpoint" | PASS — both sides visible |
| E03 | divergence from the full-information dynamic optimum, condition-qualified | "learned masking diverged from the full-information dynamic optimum in some tested conditions" | PASS — dynamic comparator explicit |
| E04 | availability ≠ discovery, representation-qualified | "became less discoverable as contextual search expanded under particular action representations" | PASS — representation qualification retained |
| E05 | 0.313 vs 0.471, comparison-cost framing, non-temporal | "The learned comparison-cost crossing was 0.313, below the stipulated environmental crossover of 0.471." | PASS — both values correct; "below", not "before" |
| Conclusion | concealment does not uniquely identify current conditions, learned expectations, or discoverability | "Observed concealment therefore does not uniquely identify current social conditions, learned expectations, or the discoverability of receptive opportunities" | PASS |

## 7. Prohibited-claim audit (§6)

Programmatic scan of the revised Abstract for every prohibited construct:

| Prohibited claim | Present? |
| --- | --- |
| human prevalence claim | NO |
| treatment efficacy | NO |
| clinical recommendation | NO |
| permanence of early rejection | NO — the E01 sentence explicitly negates persistence |
| "children stop trying" / give-up language | NO |
| temporal interpretation of E05 | NO — "below", comparison-cost axis |
| generic "more contexts cause more masking" | NO — the E04 claim is about discoverability and is representation-qualified |
| G2 / binary-softmax mechanism claim | NO |
| E06 / M4 | NO |
| "concealment contains no information about the environment" | NO — the claim is "does not uniquely identify" |
| "authenticity is always optimal" | NO — divergence is qualified "in some tested conditions" |

No new claim of any kind was introduced. Every result statement in the revised
Abstract maps to a frozen E01–E05 evidence statement retained unchanged in the
Results section.

## 8. Change containment

A full-text diff excluding the Abstract block returns empty:
title, keywords, Introduction, Methods, Results, Discussion, Educational
Relevance, Limitations, Conclusion, figure captions, declarations, Data/Code
statement, and References are byte-identical to the pre-edit source. The
Supplement was not touched and retains
`a413ee282e108dc225d8e2f29b74263dbdb514eb5cc6af89eeec64267dc929ce`.

The primary text is unchanged and therefore remains the Stage 12 figure of
**6,264 words**, within the 8,000-word maximum.

## 9. Verdict

`ABSTRACT_COMPRESSION_SCIENTIFICALLY_EQUIVALENT`

`BLOCKED_BY_ABSTRACT_COMPRESSION` is **not** raised. The 150-word limit is met
with a 6-word margin while every required scientific invariant is preserved.

## 10. Final Abstract text (144 words)

> Gifted learners may reduce the visibility of ability in social settings, yet
> similar concealment need not reflect the same learner–environment
> relationship. Five controlled reinforcement-learning experiments with finite
> learners separated social-feedback history, action representation, persistent
> social consequences, contextual discoverability, and learned versus
> environmental decision boundaries. An adverse initial authentic outcome
> reduced subsequent authentic sampling without a detected persistent
> final-window masking effect. Independently learned graded options sustained
> non-zero disclosure but reduced selection of the full-authentic endpoint.
> When actions changed future social state, learned masking diverged from the
> full-information dynamic optimum in some tested conditions. An available
> receptive context became less discoverable as contextual search expanded
> under particular action representations. The learned comparison-cost crossing
> was 0.313, below the stipulated environmental crossover of 0.471. Observed
> concealment therefore does not uniquely identify current social conditions,
> learned expectations, or the discoverability of receptive opportunities;
> empirical studies should measure these separately.
