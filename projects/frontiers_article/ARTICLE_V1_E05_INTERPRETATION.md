# Article V1 — E05 Scientific Interpretation Note

**Status:** Article-V1 supporting reference  
**Date:** 15 August 2026  
**Authority basis:** `ARTICLE_V1_CURRENT_STATE.md`, `ARTICLE_V1_ANALYTIC_RESULTS.md`, `ARTICLE_V1_LITERATURE_AUDIT.md`, `ARTICLE_V1_CLAIM_LEDGER.md`, `HANDOFF.md`

## Purpose

This note records the post-audit scientific interpretation of E05. It distinguishes:

1. what the frozen experiment actually showed;
2. what the maintained M3 mathematics proves;
3. what the exact objective comparison-cost boundary means;
4. what the learned 50% crossover means;
5. why fixed common softmax temperature cannot by itself explain the displacement;
6. what mechanisms remain plausible;
7. what E05 does and does not establish scientifically; and
8. what Article V1 may and may not claim.

This note does not authorize new simulation, seed extension, threshold re-estimation, sensitivity sweeps, or mechanism-decomposition experiments.

---

# E05 — Learned Versus Objective Comparison-Cost Crossover

## 1. Scientific question

E05 asks whether the learner stops favoring authenticity in the receptive context at the same comparison-cost level at which authenticity ceases to be objectively optimal.

The central comparison is between two different objects:

```text
objective boundary
vs
learned behavioural boundary
```

The objective boundary is an exact property of the environmental reward model.

The learned boundary is an empirical property of the finite-horizon learner.

E05 therefore asks:

> How far can the learner's behavioural transition occur from the exact objective transition under the maintained architecture and finite learning process?

---

## 2. Frozen experimental result

For the flat `K=4` architecture:

- learned 50% crossing:
  \[
  0.312852;
  \]

- master-seed bootstrap 95% interval:
  \[
  [0.307836,\;0.316918];
  \]

- exact objective comparison-cost boundary:
  \[
  \frac{8}{17}
  \approx0.470588.
  \]

Therefore the learned response crosses 0.5 substantially **before** the exact objective switch.

The displacement is approximately

\[
0.470588-0.312852
\approx0.157736.
\]

At the learned crossing, good-context authenticity still has positive objective advantage.

Using

\[
R_G-R_M
=
0.40-0.85\,bf,
\]

at

\[
bf=0.312852,
\]

the objective authenticity advantage is

\[
0.40-0.85(0.312852)
\approx0.134.
\]

Thus the learner is behaviorally at its 50% crossing while the environment still favors authenticity by about `0.134` expected reward units.

The hierarchical response is already below `0.5` at the lower dense boundary of the approved range.

Its crossing is therefore **left-censored** and is not estimated.

---

# 3. Exact objective comparison-cost boundary

In M3,

\[
R_G(bf)
=
p_{\mathrm{good}}(b+a-bf)
+
(1-p_{\mathrm{good}})(a-r).
\]

Under the frozen defaults,

\[
p_{\mathrm{good}}=\frac{17}{20},
\]

\[
b=1,\qquad
a=\frac35,\qquad
c=\frac14,\qquad
r=2.
\]

Therefore,

\[
R_G(bf)
=
\frac{23}{20}
-
\frac{17}{20}bf.
\]

Masking yields

\[
R_M
=
b-c
=
\frac34.
\]

The objective indifference point solves

\[
R_G(bf)=R_M.
\]

Hence

\[
\frac{23}{20}
-
\frac{17}{20}bf
=
\frac{15}{20},
\]

so

\[
17bf=8.
\]

Therefore,

\[
\boxed{
bf^*_{\mathrm{obj}}
=
\frac{8}{17}
\approx0.470588
}
\]

This is exact.

For

\[
bf<\frac{8}{17},
\]

good-context authenticity is objectively better than masking.

For

\[
bf>\frac{8}{17},
\]

masking is objectively better.

At exact equality, the objective is tied.

---

# 4. Why 8/17 is the relevant global boundary

Under the frozen defaults,

\[
R_B=-0.8
\]

for authenticity in a bad context, while

\[
R_M=0.75.
\]

Thus bad-context authenticity is far below masking throughout the E05 region.

The relevant competition near the E05 threshold is:

```text
good-context authenticity
versus
masking
```

not:

```text
good-context authenticity
versus
bad-context authenticity
```

The `8/17` line is therefore the full-information global switch between:

- good-context authenticity below the boundary;
- masking above the boundary.

This makes it a clean objective comparator.

---

# 5. What the learned 50% crossing means

The learned crossing is not a reward equality.

It is a behavioral statistic derived from the frozen learner.

For the flat architecture,

\[
bf^*_{\mathrm{learned}}
\approx0.312852.
\]

Thus:

\[
\boxed{
bf^*_{\mathrm{learned}}
<
bf^*_{\mathrm{obj}}
}
\]

with

\[
0.312852
<
0.470588.
\]

This means the finite-horizon learner has already shifted to its 50% behavioral point while the objective environment still favors authenticity.

The discrepancy is therefore a real learned/objective misalignment.

---

# 6. Why fixed common softmax temperature cannot explain the shift by itself

For a binary softmax,

\[
P(A)
=
\frac{e^{Q_A/\tau}}
{e^{Q_A/\tau}+e^{Q_M/\tau}}.
\]

Equivalently,

\[
P(A)
=
\frac{1}
{1+\exp(-(Q_A-Q_M)/\tau)}.
\]

For every finite common

\[
\tau>0,
\]

\[
P(A)=0.5
\]

if and only if

\[
Q_A=Q_M.
\]

Therefore fixed common temperature changes the **steepness** of the behavioral response, but does not change the binary Q-equality location of the 50% point.

Thus the explanation

> The crossing shifted because softmax temperature was fixed at a particular value

is analytically invalid as a complete binary explanation.

Temperature alone is ruled out.

---

# 7. Multi-action caveat

The flat M3 architecture contains more than two actions globally.

For a general multi-action softmax,

\[
\pi_i
=
\frac{e^{Q_i/\tau}}
{\sum_j e^{Q_j/\tau}}.
\]

The condition

\[
\pi_i=0.5
\]

is

\[
e^{Q_i/\tau}
=
\sum_{j\ne i}e^{Q_j/\tau}.
\]

Equivalently,

\[
Q_i
=
\tau
\log\left(
\sum_{j\ne i}e^{Q_j/\tau}
\right).
\]

Thus a multi-action 50% probability point is not generally equivalent to pairwise equality with one competitor.

This limits how far the binary identity can be used.

The exact authority nevertheless supports the negative conclusion:

> fixed common temperature alone does not quantitatively explain the observed E05 displacement.

---

# 8. What mechanisms remain plausible?

The frozen evidence does not identify a unique cause of the displacement.

The following remain plausible contributors.

## 8.1 Finite-sample Q estimation

The learner has a finite horizon.

The learned value of good-context authenticity can differ from its true expected value because of limited and noisy sampling.

This alone can move the behavioral transition away from the objective boundary.

---

## 8.2 Endogenous under-sampling

As comparison cost rises, authenticity becomes less attractive.

The learner samples it less often.

Reduced sampling limits corrective evidence.

The process can therefore become self-reinforcing:

```text
lower estimated authenticity value
    ↓
less authenticity sampling
    ↓
less corrective evidence
    ↓
persistently low learned value
```

This is an established generic mechanism.

---

## 8.3 Receptive-context search burden

The learner must not only estimate the value of authenticity.

It must also identify which context is receptive.

E05 therefore inherits part of the E04 problem:

```text
discover the good context
+
learn its authentic value
```

Some of the displacement may reflect search cost rather than a pure known-context reward comparison.

---

## 8.4 Multi-action normalization

In a multi-action softmax, the policy probability of one action depends on the value of all alternatives.

Even if good-context authenticity is better than every individual competitor, the combined probability mass of the alternatives can suppress its behavioral probability.

This may contribute to an early 50% crossing.

The project does not currently quantify this contribution.

---

## 8.5 Constant-step-size stochastic learning

The maintained learner uses constant learning rate.

The conditional expected Q update is mean-reverting toward expected transformed reward, but the finite-horizon stochastic Q process need not sit exactly at that target.

Noise and recency weighting can therefore contribute to the observed shift.

---

## 8.6 Representation architecture

The flat learner maintains separate context-action values.

A learner that knew the good context, generalized across contexts, or used a different representation could have a different crossover.

The observed threshold is therefore architecture-specific.

---

# 9. What mechanism is actually ruled out?

One claim is ruled out analytically:

\[
\boxed{
\text{fixed common binary softmax temperature alone}
}
\]

cannot move the 50% Q-equality location.

This is a useful negative result.

But excluding one explanation does not identify the true one.

The current scientific state is:

```text
the displacement is established
+
temperature alone is insufficient
-
the quantitative mechanism is unresolved
```

---

# 10. Is the displacement large?

Relative to the frozen objective scale, it is nontrivial.

The threshold difference is approximately

\[
0.157736.
\]

More importantly, at the behavioral crossing the objective authenticity advantage is still approximately

\[
0.134.
\]

Therefore the learner is not crossing precisely where the environmental payoff difference is nearly zero.

That makes the E05 result scientifically interesting.

But the project does not currently have a theorem saying how large the displacement should be under the maintained learner.

So `0.157736` must remain an observed configuration-specific quantity.

---

# 11. Where should learned/objective displacement be easiest to obtain?

Article V1 has not proved a displacement phase diagram.

The following are theoretical expectations only.

## 11.1 Limited horizon

A shorter horizon leaves less time for Q estimates to correct.

Finite-horizon learner/objective mismatch should therefore be easier to sustain.

---

## 11.2 Sparse sampling of the objectively best action

Conditions that reduce sampling of good-context authenticity can increase learned-value error:

- many contexts;
- early unfavorable authentic outcomes;
- competing actions with similar learned values;
- weak effective exploration.

---

## 11.3 Near the objective boundary

As

\[
bf\to\frac{8}{17}^{-},
\]

\[
R_G-R_M
=
0.40-0.85\,bf
\to0^+.
\]

Small Q-estimation errors can then reverse the learned ordering.

Some learner/objective mismatch near the boundary is therefore unsurprising.

The more notable E05 observation is that the learned 50% crossing occurs much earlier, at a point where the objective advantage remains about `0.134`.

---

# 12. Relation to BFLPE and social-comparison cost

The `bf` parameter is a model comparison cost.

BFLPE/social-comparison literature motivates the possibility that a socially or intellectually receptive environment can still impose comparison-related costs.

But:

\[
bf
\]

is not an empirically calibrated BFLPE variable.

Therefore the literature supports:

```text
comparison cost is a plausible ingredient
```

but not:

```text
bf is a measured BFLPE quantity
```

and not:

```text
bf = 0.312852 is a human threshold
```

The E05 crossing is a model result only.

---

# 13. Does E05 show persistent suboptimal masking?

E05 shows suboptimal finite-horizon behavior relative to the objective boundary.

At the learned crossing:

```text
learner behavior is already at 50%
while
objective authenticity is still better
```

So the learner is behaviorally conservative relative to the environment.

However, E05 does not show:

- an absorbing masking state;
- irreversibility;
- a persistent-state transition;
- a universal retreat threshold.

Its main scientific object is **boundary displacement**, not lock-in.

---

# 14. Comparison with E01–E04

| Dimension | E01 | E02 | E03 | E04 | E05 |
|---|---|---|---|---|---|
| Main question | Early rejection | Graded actions | Persistent social state | Scarce receptive contexts | Learned vs objective threshold |
| Exact anchor | M0 objective threshold | M1 endpoint theorem | Dynamic Bellman optimum | M3 K-invariance | M3 `bf*=8/17` |
| Main effect | Reduced sampling + regret | Reduced endpoint discovery | Learned/oracle disagreement | Search burden | Left-shifted behavioral crossover |
| End-of-horizon distortion | Not detected overall | Yes | Yes | Yes | Yes, as threshold displacement |
| Main generic mechanisms | Hot-stove | Independent-arm dilution | Finite-horizon dynamic learning | Rare-good search | Finite sampling/search/normalization |
| Strongest safe role | Baseline | Representation-sensitive demonstration | Main synthesis result | Main application result | Quantitative supporting result |
| Main unresolved issue | Persistent-mask subregion | Structured learner | Information-matched optimum | Search scaling | Mechanism of displacement magnitude |

---

# 15. Final interpretation of E05

> In the frozen flat `K=4` M3 experiment, the learner's 50% behavioral crossing occurs at `bf ≈ 0.312852`, substantially below the exact objective comparison-cost boundary `8/17 ≈ 0.470588`. At the learned crossing, good-context authenticity still retains an objective advantage of approximately `0.134`. Exact softmax analysis rules out fixed common binary temperature as a sufficient explanation for the displacement. Finite sampling, endogenous under-sampling, receptive-context search, multi-action normalization, constant-step-size stochastic learning, and representation effects remain plausible contributors, but Article V1 does not identify their quantitative shares. E05 is therefore a learner- and configuration-specific quantitative result showing learned/objective misalignment, not a universal behavioral threshold or formal novelty claim.

---

# 16. Article-V1 claim boundary for E05

## Supported

- The exact objective comparison-cost boundary is
  \[
  bf=\frac{8}{17}.
  \]

- The frozen flat `K=4` learned crossing is approximately
  \[
  0.312852.
  \]

- The master-seed bootstrap 95% interval is approximately
  \[
  [0.307836,0.316918].
  \]

- The learned crossing occurs substantially before objective indifference.

- At the learned crossing, good-context authenticity remains objectively superior by approximately `0.134`.

- Fixed common binary softmax temperature alone cannot explain a shifted 50% Q-equality location.

- The hierarchical crossing is left-censored in the approved range and must not be estimated.

## Supported only with qualification

- E05 may be described as a finite-horizon learned/objective threshold displacement.

- The observed threshold is specific to the frozen learner, architecture, horizon, reward scale, and analysis.

- Several generic mechanisms remain plausible contributors.

- E05 can support the broader claim that learned behavior can diverge materially from exact objective structure.

## Not supported

- `0.312852` is a universal threshold.

- The displacement is caused by softmax temperature.

- The displacement is formal novelty.

- `bf` is an empirically calibrated BFLPE measure.

- `0.312852` is a human social-comparison or concealment threshold.

- The magnitude generalizes to other learners, horizons, architectures, or reward scales.

- The hierarchical threshold has been estimated.

- The exact mechanism producing the displacement is known.

- E05 proves persistent or irreversible masking.

---

# 17. Main scientific lesson

E05 changes the question from:

```text
When does the objective environment stop favoring authenticity?
```

to:

```text
When does the learner behave as though authenticity has stopped being preferable?
```

The exact environmental answer is:

\[
\boxed{
bf^*_{\mathrm{obj}}
=
\frac{8}{17}
\approx0.470588
}
\]

The frozen learned answer is:

\[
\boxed{
bf^*_{\mathrm{learned}}
\approx0.312852
}
\]

Therefore:

\[
\boxed{
\text{behavioral transition occurs before objective indifference}
}
\]

The result is scientifically useful because the objective and learned thresholds are independently defined.

Its limitation is equally important:

\[
\boxed{
\text{the displacement is established;
its quantitative mechanism and generality are not}
}
\]

That is E05's role in Article V1.
