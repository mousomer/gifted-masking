# Article V1 draft review — unused results, tone, and intervention analysis

**Status:** Editorial review only. No evidence, model, config, artifact, or figure
is altered by this document. All numbers below are quoted from
`ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md`, `ARTICLE_V1_EVIDENCE_MATRIX.csv`, and
`ARTICLE_V1_ANALYTIC_RESULTS.md` at their frozen values.

**Reviewed:** `ARTICLE_V1_MANUSCRIPT_DRAFT.md` (744 lines, 6,107 words) against the
33-row evidence matrix and the analytic authority.

---

## 0. Diagnosis in one paragraph

The three problems are one problem. **The draft leads with the results that require
the most hedging and buries the results that require none.** `243/357` is an
aggregate simulation classifier over a frozen grid; the evidence freeze states
explicitly that it is "not a headline number" and "belongs in supplement or
tested-grid provenance" (`ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md`, E03
boundaries). It is nonetheless in the abstract, the §3.3 heading, and §4.2 — and it
is disclaimed five separate times to pay for that placement. Meanwhile the exact,
deterministic, independently verified results — the M2 dynamic thresholds, the M2
Accepted-state dominance theorem, the λ-threshold family — are either compressed
into a single vague clause or omitted entirely. Promote the deterministic results
to the headline positions and the hedging load falls away on its own, because
deterministic results do not need to be hedged. The tone problem is downstream of
the results-selection problem.

Word budget: 6,107 used against a 6,000–8,000 target. There is room for roughly
1,900 words — enough for everything recommended below.

---

## Part A — Results that are frozen, adjudicated, and unused

### A.1 Fully missing adjudicated claims

Nine rows of the evidence matrix carry `reconciliation_status = INCLUDE` and appear
nowhere in the draft.

| Claim ID | Value | 95% CI | Currently in draft |
|---|---|---|---|
| **E01-C3-LAMBDA** | **+0.402990** final mask, λ .5→2.5 at p=.65 | [+0.395366, +0.410614] | **Absent** |
| E01-C3-GAP | −0.001067 (gap-in-gap null) | [−0.015031, +0.012898] | Absent |
| E01-C2-FORCED-REGRET | +0.057954 | [+0.045614, +0.070293] | Absent |
| E01-C2-CF-REGRET | +0.141318 | [+0.132369, +0.150267] | Absent |
| E02-C4-REGRET | −0.029761 | [−0.033874, −0.025648] | Alluded to, no number |
| **E03-C5-THRESHOLDS** | **η=0: .38391; η=.2: .33875; η=.8: .26898** | deterministic, bisection width 6.1e−05 | **One vague clause** |
| E03-C5-HARSH | Q(auth−mask) = −0.4062934363 | five-master consistent | Mentioned, no number |
| E05-C7-ENDPOINT | −0.9400 | [−0.957993, −0.922007] | Mentioned, no number |
| E04-C6-MULTIPLE | four values | four CIs | Values given, CIs dropped |

Two of these are not minor omissions.

### A.2 The λ result is the paper's own thesis, and it is missing

**E01-C3-LAMBDA: at p = .65, raising λ from .5 to 2.5 increased final masking by
0.403 [0.395, 0.411] with the objective payoff structure held exactly fixed.**

This pairs with an exact analytic result the draft also omits — Propositions M0.3
and M0.4, the loss-weighted subjective crossover:

```
p*_λ = [(b−c) + λ(r−a)] / [(b+a) + λ(r−a)]   = (15 + 28λ) / (32 + 28λ)  at defaults
```

strictly increasing in λ, with p*_λ → 1 as λ → ∞:

| λ | 0 | 0.5 | 1 | 2 | 2.5 | 5 |
|---|---|---|---|---|---|---|
| p*_λ | .4688 | .6304 | **.7167** | .8068 | .8333 | .9012 |

At λ = 1 the subjective boundary coincides exactly with the objective boundary
43/60. Away from λ = 1 it sweeps from .469 to 1 — **more than half the receptivity
range — while the environment is untouched.**

Why this matters more than anything else currently in the draft: §1.2 is titled
"Why observed masking is insufficient to establish objective optimality," and this
is the cleanest possible proof of exactly that. A 40-percentage-point swing in
observed masking, produced entirely by a learner-side asymmetry, with the payoff
structure held constant. Every other experiment argues the identification problem
indirectly; this one exhibits it.

**Framing constraint (important, do not get this wrong).** At p = .65,
Δ₀ = 3(.65) − 2.15 = −0.20 < 0, so masking *is* the objective optimum there. This
is therefore **not** a suboptimality result and must not be written as one. It is an
identification result: the same environment supports a 40-point range of observed
masking depending on a learner parameter, so an observed masking rate constrains the
environment almost not at all unless λ is known or measured. Written that way it is
both bolder and safer than anything currently in §1.2.

E01-C3-GAP (−0.001067, CI spanning zero) belongs immediately beside it: loss
weighting shifts the *level* of masking dramatically but did not measurably amplify
the *early-rejection gap*. Two distinct channels, cleanly separated. That is a real
dissociation and it is currently on the floor.

**Placement:** new Results subsection §3.2 (renumbering the rest), or a second
paragraph block in §3.1. Analytic table into Methods §2.2 or the analytic-results
table. Approx. 250 words.

### A.3 The M2 dynamic thresholds are the strongest E03 result and are one clause

The draft says only: *"Dynamic objective thresholds varied with the escape
parameter."* (§3.3)

The frozen values:

| η | Objective dynamic threshold p* | Below static M0 threshold 43/60 = .7167 by |
|---|---|---|
| 0 | .38391 | .333 |
| .2 | .33875 | .378 |
| .8 | .26898 | .448 |

Bisection width 6.1e−05. Deterministic. And independently verified: the 15 August
consistency audit enumerated all four relevant deterministic stationary policies
(reduced from 2³ = 8 by Proposition M2.2), evaluated each by exact matrix inverse
V^π = (I − γP^π)⁻¹r^π across all 357 frozen cells, and found a **maximum absolute
discrepancy of 8.99 × 10⁻¹⁰** against the production value iteration.

This supports a strong, fully deterministic sentence:

> Making social standing persistent moved the objective authenticity boundary from
> p = .717 to between .384 and .269 depending on the escape rate — a band of
> receptivity 0.33 to 0.45 wide in which concealment is objectively correct in the
> one-shot environment and objectively wrong once the same action can change future
> standing.

That sentence needs no hedge. It is exact arithmetic on a stated model, verified to
nine decimal places by an independent method. It is also the paper's actual thesis
("immediate value ≠ dynamic value") stated as a measured quantity rather than as a
claim about a simulation classifier.

**Recommendation:** this becomes the §3.3 headline and the E03 abstract sentence.
`243/357` moves to a supporting sentence or the supplement, per the freeze's own
instruction. This single swap removes the need for roughly half the disclaimers in
§3.3 and §4.2.

### A.4 Proposition M2.2 — Accepted-state dominance — is absent

Exact, parameter-free, holds for every γ, p, η, δ, b2, r2 and every continuation
value function:

```
Q(Accepted, Authentic) − Q(Accepted, Mask) = (b+a) − (b−c) = a + c > 0
```

Both actions have identical transition rows from Accepted, so the future-value terms
cancel exactly.

Plain statement: **there is no parameter configuration of this model in which
concealment is optimal once you have been accepted.** Concealment can only ever be
optimal as a response to *uncertain* standing. That is a clean, quotable, exact
result, it reduces the policy search space from 8 to 4 (which is what makes the
independent verification above cheap), and it is currently nowhere in the manuscript.

**Placement:** Methods §2.4 (one sentence) and Discussion §4.2 (one sentence).
Approx. 80 words.

### A.5 Smaller unused analytic material

- **M3.4 / §6.5–6.6:** R_B = −0.80 versus R_M = 0.75 — bad-context authenticity is
  never the objective competitor anywhere near the E05 range. So 8/17 is not a
  pairwise tie, it is the **global** full-information switch between the unique
  good-authentic arm and the K masking arms. Strengthens E05 at no cost; one
  sentence in §2.6 or §3.5.
- **M1.4:** normalized regret = 1 − d exactly. The draft asserts this without the
  derivation or the E02-C4-REGRET number (−0.029761). Give both; it converts a
  hand-wave into a proof.
- **Independent M2 verification (8.99e−10):** currently the manuscript's only
  statement about verification is the §5 apology about generator-source provenance.
  A verified comparator is a strength and should be stated as one.
- **E04-C6-MULTIPLE CIs:** the draft gives +.05064 / +.02524 / +.06044 / +.11224
  bare. All four have frozen Student-t intervals. Reviewers notice asymmetric CI
  reporting.

---

## Part B — Tone

### B.1 The measurement

| Section | Sentences containing a disclaimer negation |
|---|---|
| §3.2 (E02) | 5 / 13 — **38%** |
| §5 Limitations | 6 / 19 — 32% |
| §3.4 (E04) | 9 / 29 — 31% |
| §4.4 | 3 / 10 — 30% |
| §3.3 (E03) | 10 / 35 — 29% |
| §3.5 (E05) | 6 / 21 — 29% |
| **Whole draft** | **71 / 320 — 22%** |

("does not," "do not," "cannot," "is not," "are not," "must not," "should not,"
"did not," "neither," "nor.")

Roughly one sentence in three in the Results section retracts the sentence before
it. The Limitations section is *less* apologetic than four of the five Results
subsections — which is diagnostic: the hedging has migrated out of the section built
to hold it.

Repetition counts: `243/357` disclaimed at lines 19–20, 393, 604, 710 — **five
times**. "prevalence" appears **nine times** in 6,107 words.

### B.2 The three editable rules

**Rule 1 — one scope sentence per result, placed last.** Not interleaved. Every
result gets exactly one bounding sentence at the end of its paragraph block. If the
same bound is needed twice, it belongs in Limitations only.

**Rule 2 — nothing is disclaimed in both Results and Limitations.** Pick one. §5
exists precisely so §3 does not have to carry this. `243/357` currently appears with
its disclaimer in the abstract, §3.3 (×3), §4.2, and §5.

**Rule 3 — replace denial lists with positive definitions.** A four-item denial
tells the reader what the number is not; a definition tells them what it is, and
implies the denials.

> **Current (§3.3):** "It is not human prevalence, learner prevalence, a natural
> phase-space volume, or a Q-value classifier."
>
> **Proposed:** "The count is defined over cells: a cell enters when aggregate
> final-window Neutral action counts favour masking, value iteration favours
> authenticity, and the visit-adequacy criterion is met."

Same information, no defensive posture, 9 words shorter.

### B.3 Four specific rewrites

**Abstract, E03 sentence.**

> *Current:* "In E03, aggregate final-window Neutral actions favoured masking in 243
> of 357 tested persistent-state cells where the dynamic oracle favoured
> authenticity; this is tested-grid coverage, not prevalence."
>
> *Proposed:* "In E03, making social standing persistent moved the objective
> authenticity boundary from p = .717 to between .384 and .269 as the escape rate
> rose, and learned end-of-episode behaviour tracked neither boundary."

Leads with a deterministic result, drops the disclaimer with the claim that needed
it, and states the dissociation the experiment was built to show.

**Abstract, closing.**

> *Current:* "They do not estimate human prevalence, diagnose gifted learners, or
> establish intervention effects. Instead, they provide explicit mechanisms and
> benchmarks..."
>
> *Proposed:* "The models specify what would have to be measured — action, social
> response, subsequent sampling, and changing standing over time — to tell these
> mechanisms apart in people, and which of them is worth targeting first."

The current version spends its final sentence on what the paper is not. Abstracts
are read for what a paper is.

**§3.1 closing.**

> *Current:* "E01 is consequently a supporting hot-stove demonstration..."
>
> *Proposed:* "E01 establishes the baseline the rest of the cascade is measured
> against: an information-restriction effect on sampling large enough to detect,
> with no persistent endpoint effect from a single rejection."

"Supporting demonstration" is the author demoting their own experiment. E01 is the
control that licenses every later comparison; say that.

**§5 opening.**

> *Current:* "Several limitations are integral to the interpretation."
>
> *Proposed:* "Four boundaries define what these results support."

Same content, structural rather than penitent, and it commits to a count so the
section cannot sprawl.

### B.4 What must not change

The genuine scope discipline stays. Every ceiling wording in the evidence freeze is
a real constraint and none of the above violates one. The change is **placement and
frequency**, not permissiveness: say each bound once, in the right place, and stop
re-litigating it. A paper that states its limits once and clearly reads more
confident *and* more rigorous than one that states them five times.

---

## Part C — Intervention analysis

### C.1 The gap

The models contain **seven distinct intervention levers, each with a frozen effect
size**, and the draft assembles none of them. E01's two information manipulations
are described as "manipulations of the model's information channel, not estimates of
human intervention effects" and dropped. η in E03, the good-context supply in E04,
and bf in E05 are all levers presented purely as sensitivity axes. The word
"intervention" appears in the draft only in denials.

This is a real loss. The paper's whole argument is that four different mechanisms
produce the same observable, and that they require different responses. That
argument is *only* actionable if the different responses are stated.

### C.2 Proposed §4.5 "Where the model says leverage lies"

Replaces the current §4.5, which restates the synthesis a third time. Approx. 700
words.

| Lever | Model operation | Frozen effect | What it would mean to measure |
|---|---|---|---|
| **Counterfactual feedback** | learner observes the foregone authentic outcome | **−0.118** final mask [.110, .127]; −0.141 regret | making the outcome of *undisclosed* ability observable — structured feedback, peer report, debrief |
| **Forced exploration** | 5% of trials forced authentic | −0.0466 final mask [.033, .060]; −0.0580 regret | recurring low-stakes disclosure occasions independent of choice |
| **Escapable stigma** | raise η, 0 → .8 | objective threshold **.384 → .269** | whether adverse standing can be exited; group re-composition, reputational reset |
| **Receptive-context density** | 1 → 2 good contexts; proportional-25% | +.0506 / +.0252; +.0604 / +.1122 | number *and proportion* of settings where ability is welcome |
| **Comparison cost** | reduce bf | learner abandons at .313, objective boundary .471 | salience of within-group comparison |
| **Negative-outcome weight** | λ .5 → 2.5 | **+0.403** final mask, environment fixed | rejection sensitivity; the largest single mover in the cascade |
| **Graded options** (anti-lever) | independent disclosure arms | +.255 engagement, **−.329** endpoint use, −.222 modal | offering partial-disclosure options without linking evidence across them |

Five claims worth making assertively from this table:

**1. Information dominates opportunity.** Counterfactual feedback (−0.118) is
2.5× forced exploration (−0.0466), and the two manipulations cost the same in the
model. The bottleneck is not access to the authentic action — the learner can always
select it. It is that declining to act destroys the evidence that would have
corrected the estimate. **Interventions that create disclosure opportunities are
weaker than interventions that reveal what disclosure would have produced.**
Falsifiable and directly testable.

**2. Interventions calibrated to the objective boundary will be a third too weak.**
E05: the learner abandons good-context authenticity at bf = .313 while it still
retains **33.5%** of its maximum objective advantage (0.134 of 0.40). An intervention
aimed at the environmental crossover 8/17 = .471 lands well past the point where
behaviour has already gone. **Target the behavioural boundary, not the objective
one; the gap is the intervention's required overshoot.** Novel, quantitative,
and follows directly from the frozen E05 numbers.

**3. Expanding the option set can reduce use of the best option.** E02: graded arms
raised continued engagement by +0.255 and simultaneously cut full-authentic
final-window selection by −0.329 and optimal-endpoint modal discovery by −0.222. A
"graduated disclosure" programme whose intermediate steps do not let evidence
generalise across levels buys breadth by spending depth. This is a **concrete
warning to practice**, it is counterintuitive, and the affine-reward theorem (M1.2)
proves the intermediate levels create no compensating objective benefit. The draft
currently has this result and declines to draw the inference.

**4. Density, not count.** E04's K decline nearly vanishes under proportional-25%
receptivity (+.0604 flat, +.1122 hierarchical). The model's target is not fewer
settings — it is a higher *proportion* of receptive ones. One receptive setting
among sixteen is a search problem; four among sixteen largely is not.

**5. Recovery routes change what is optimal, not merely what is learned.** This is
the strongest of the seven and the one no other lever shares. Raising η from 0 to .8
lowers the *objective* threshold from .384 to .269. Every other lever moves
behaviour toward a fixed benchmark; **making adverse standing escapable moves the
benchmark itself**, so that authenticity becomes objectively correct across an
additional 11.5 points of receptivity. Deterministic, verified to 8.99 × 10⁻¹⁰, no
simulation uncertainty at all.

And the honest counterweight, which should be stated in the same section rather than
hidden: **the largest single mover in the entire cascade is the learner, not the
environment.** λ .5 → 2.5 produces +0.403, an order of magnitude larger than any
environmental lever tested. Within this model, negative-outcome weighting is
simultaneously the highest-leverage target and the largest confound for reading
environments off behaviour. Stating both halves is what makes the section rigorous
rather than promotional.

### C.3 How to keep this defensible

One scope paragraph closing §4.5, covering all seven levers at once — instead of the
current pattern of a disclaimer per lever:

> These are manipulations of stipulated model environments, not estimates of
> intervention effects in people. Their value is comparative and directional: they
> rank candidate targets within a specified structure and name the measurement each
> would require. An intervention study motivated by this ranking would need repeated
> observation of action, social response, subsequent sampling, and changing standing
> — the same four quantities that separate the mechanisms in the first place.

That is one paragraph doing the work currently spread across a dozen interleaved
retractions, and it converts the paper's central limitation into its central
research recommendation.

### C.4 A falsification table is the safe way to be bold

Adding a short table of the form *"lever → model prediction → observation that would
contradict it"* lets §4.5 make strong directional claims while remaining a modelling
paper. It is the standard move for computational work entering an applied field, it
pre-empts the obvious reviewer objection, and it costs about 150 words.

---

## Summary of recommended changes

| # | Change | Words | Priority |
|---|---|---|---|
| 1 | Promote E03 dynamic thresholds (.384/.339/.269) to abstract + §3.3 headline; demote 243/357 per the freeze's own instruction | ~0 net | **Highest** |
| 2 | Add E01-C3-LAMBDA (+0.403) and the p*_λ family as an identification result | ~250 | **Highest** |
| 3 | New §4.5 intervention-leverage section with the seven-lever table | ~700 | **High** |
| 4 | Add Proposition M2.2 (Accepted-state dominance) | ~80 | High |
| 5 | Add the 8.99e−10 independent verification as a strength | ~50 | High |
| 6 | Apply the three tone rules; target Results negation density below 15% | ~−200 | High |
| 7 | Restore the seven missing numbers and four dropped CIs | ~150 | Medium |
| 8 | Add M3.4 global-switch point and M1.4 derivation | ~100 | Medium |
| 9 | Falsification table | ~150 | Medium |

Net: roughly +1,280 words, landing near 7,400 — inside the 6,000–8,000 budget.

**Governance note.** Every item above uses a frozen, adjudicated value at its ceiling
wording. Nothing here requires a new run, a new configuration, or a re-analysis.
Items 1, 2, 6, and 7 arguably move the draft *closer* to the evidence freeze than it
currently sits, since the freeze already designates 243/357 as non-headline and
already carries the nine unused claims at INCLUDE status.
