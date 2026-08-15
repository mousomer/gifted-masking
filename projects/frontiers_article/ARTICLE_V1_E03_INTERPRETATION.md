# Article V1 — E03 Scientific Interpretation Note

**Status:** Article-V1 supporting reference  
**Date:** 15 August 2026  
**Authority basis:** `ARTICLE_V1_CURRENT_STATE.md`, `ARTICLE_V1_ANALYTIC_RESULTS.md`, `ARTICLE_V1_LITERATURE_AUDIT.md`, `ARTICLE_V1_CLAIM_LEDGER.md`, `HANDOFF.md`

## Purpose

This note records the post-audit scientific interpretation of E03. It distinguishes:

1. what the frozen experiment actually showed;
2. what the maintained M2 mathematics proves;
3. what the exact full-information dynamic comparator means;
4. why persistent social state changes the optimization problem relative to E01/M0;
5. where finite-horizon learner/oracle disagreement should be expected;
6. what E03 does and does not establish about persistent suboptimal concealment; and
7. what Article V1 may and may not claim.

This note does not authorize new simulation, an information-matched optimum, new sensitivity sweeps, or Track-B work.

---

# E03 — Persistent Social State and the Dynamic Optimum

## 1. Scientific question

E03 asks whether a learner can favor concealment in a social environment where the consequences of disclosure are not exhausted by the immediate reward.

M2 introduces persistent social state:

- `N` — Neutral;
- `A` — Accepted;
- `S` — Stigmatized.

The available actions are:

- `M` — Mask / conceal;
- `A_u` — Authentic / reveal ability.

The key structural change from M0/E01 is:

```text
action
    ↓
immediate social outcome
    ↓
persistent later social state
    ↓
future rewards and future action values
```

The objectively best action therefore cannot generally be determined from immediate expected reward alone.

---

## 2. Frozen experimental result

Under the frozen default M2 learner, a broad set of tested parameter cells showed:

```text
learned neutral-state behavior = masking
while
exact full-information dynamic optimum = authenticity
```

The publication-facing analysis uses the frozen five-seed standard analysis and the exact tested-grid classification.

The figure `243/357` refers only to the number of tested parameter-grid cells satisfying the reported classification. It is not:

- a prevalence estimate;
- a probability that a gifted learner masks;
- a measure of the volume of all possible parameter space;
- evidence that 68% of people or learners would show the effect.

The defensible E03 statement is:

> Under the frozen M2 learner, learned neutral-state masking differed from the exact full-information dynamic optimum across a broad region of the tested parameter grid.

The experiment does **not** establish:

> The learner failed to find the best policy attainable under its own information constraints.

That stronger statement would require an information-matched optimum, which Article V1 does not currently define or compute.

---

## 3. Exact M2 environmental structure

### 3.1 Immediate rewards

Under the frozen defaults:

#### Neutral state

Masking:

\[
r_N(M)=b-c=0.75.
\]

Authenticity:

\[
r_N(A_u)
=
p(b+a)+(1-p)(a-r)
=
-1.4+3p.
\]

The immediate neutral-state crossover is therefore exactly the M0 threshold:

\[
p=\frac{43}{60}\approx0.7167.
\]

#### Accepted state

Masking:

\[
r_A(M)=0.75.
\]

Authenticity:

\[
r_A(A_u)=1.60.
\]

Authenticity has an immediate advantage of

\[
1.60-0.75=0.85.
\]

#### Stigmatized state

Masking:

\[
r_S(M)=b_2-c=0.25.
\]

Authenticity:

\[
r_S(A_u)
=
-1.9+1.75p.
\]

For all

\[
p\in[0,1],
\]

\[
-1.9+1.75p\le -0.15 < 0.25.
\]

So under the default reward parameters, masking always has the higher **immediate** expected reward in the stigmatized state.

Any full-information reason to choose authenticity while stigmatized must therefore come from **future value**, not immediate reward.

---

## 4. Exact transition structure

Using state order `(N, A, S)`:

### From Neutral

Masking keeps the agent Neutral:

\[
P(\cdot\mid N,M)=(1,0,0).
\]

Authenticity moves the agent to:

\[
P(\cdot\mid N,A_u)=(0,p,1-p).
\]

Thus authenticity creates a consequential transition:

```text
Neutral
  ├── accepted with probability p      → Accepted
  └── rejected with probability 1-p    → Stigmatized
```

### From Accepted

Both actions have the same transition distribution:

\[
P(\cdot\mid A,M)
=
P(\cdot\mid A,A_u)
=
(\delta,1-\delta,0).
\]

The state persists with probability `1-delta` and returns to Neutral with probability `delta`.

### From Stigmatized

Masking:

\[
P(\cdot\mid S,M)
=
(\eta,0,1-\eta).
\]

Authenticity has a chance of redemption into Accepted:

\[
P(\cdot\mid S,A_u)
=
((1-p/2)\eta,\;p/2,\;(1-p/2)(1-\eta)).
\]

This creates the second genuinely dynamic feature of M2:

> An authentic action that is immediately costly can still be dynamically valuable because it creates a chance of reaching the high-value Accepted state.

---

## 5. Accepted-state authenticity is exactly dominant

From the Accepted state, masking and authenticity have **identical transitions**.

Therefore their continuation values cancel:

\[
Q(A,A_u)-Q(A,M)
=
(b+a)-(b-c)
=
a+c.
\]

Under the frozen parameters,

\[
a+c=0.85>0.
\]

So authenticity is strictly optimal in the Accepted state for every:

- `p`;
- `eta`;
- `delta`;
- `gamma`;
- `b2`;
- `r2`;

provided `a+c>0`.

This is exact.

Consequently, the full-information optimization problem only needs to determine the optimal action in:

- Neutral;
- Stigmatized.

The Accepted-state action is already solved.

---

# 6. Why the M0 threshold no longer determines the optimum

In E01/M0, the objective comparison is static:

\[
\Delta_0(p)
=
E[R_A]-R_M
=
3p-2.15
\]

under the default parameters.

In M2, the neutral-state dynamic difference is:

\[
D_N(V)
=
Q(N,A_u;V)-Q(N,M;V)
\]

with exact decomposition

\[
\boxed{
D_N(V)
=
\Delta_0(p)
+
\gamma
\left[
pV_A+(1-p)V_S-V_N
\right]
}
\]

The first term,

\[
\Delta_0(p),
\]

is the immediate M0 reward difference.

The second term,

\[
\gamma
\left[
pV_A+(1-p)V_S-V_N
\right],
\]

is the future-value consequence of leaving Neutral.

This means the M2 dynamic optimum can disagree with the M0 static optimum.

In particular, when

\[
p<\frac{43}{60},
\]

the immediate reward comparison favors masking:

\[
\Delta_0(p)<0.
\]

Yet authenticity is still dynamically preferable whenever

\[
\gamma
\left[
pV_A+(1-p)V_S-V_N
\right]
>
-\Delta_0(p).
\]

Therefore a region can exist in which:

```text
immediate reward says MASK
but
full dynamic value says AUTHENTIC
```

This is one of the scientifically important regions of E03.

---

# 7. The stigmatized-state redemption mechanism

The exact authenticity-minus-mask difference in the Stigmatized state is

\[
D_S(V)
=
Q(S,A_u;V)-Q(S,M;V).
\]

It decomposes as

\[
\boxed{
D_S(V)
=
\left[r_S(A_u)-(b_2-c)\right]
+
\gamma\frac{p}{2}
\left[
V_A-\{\eta V_N+(1-\eta)V_S\}
\right]
}
\]

The first term is the immediate reward difference.

Under the frozen defaults, this first term always favors masking.

The second term is the **redemption value**:

\[
\gamma\frac{p}{2}
\left[
V_A-\{\eta V_N+(1-\eta)V_S\}
\right].
\]

Authenticity can therefore be dynamically optimal while stigmatized only because it creates a chance of reaching Accepted.

This is not a stateless bandit effect.

The agent must value a costly current action because it changes its distribution over future social states.

---

# 8. What does the full-information dynamic optimum mean?

The E03 comparator is computed by exact discounted dynamic programming.

For a stationary deterministic policy `pi`,

\[
V^\pi
=
r^\pi+\gamma P^\pi V^\pi,
\]

so

\[
V^\pi
=
(I-\gamma P^\pi)^{-1}r^\pi.
\]

The Bellman optimality operator has a unique fixed point for

\[
0\le\gamma<1.
\]

Thus the full-information optimum is mathematically well defined.

It assumes the planner knows:

- all transition probabilities;
- all reward functions;
- the discount factor;
- the state dynamics.

It answers:

> What policy maximizes expected discounted objective reward if the model is known exactly?

It does **not** answer:

> What is the best policy a finite learner could discover from the particular observations it actually receives?

That distinction is central.

Conceptually,

\[
V(\pi_F^*)-V(\pi_L)
=
\underbrace{
V(\pi_F^*)-V(\pi_I^*)
}_{\text{information gap}}
+
\underbrace{
V(\pi_I^*)-V(\pi_L)
}_{\text{learner gap}}.
\]

Article V1 currently computes the full-information oracle `pi_F^*` and the learned policy `pi_L`.

It does not compute `pi_I^*`, the best policy under information constraints matching the learner.

Therefore E03 establishes an **oracle/learner discrepancy**, not a clean decomposition of why that discrepancy exists.

---

# 9. Why should learner/oracle disagreement be expected?

There are several reasons.

## 9.1 Delayed value is harder to learn than immediate reward

When the optimal action is already better immediately, learning requires estimating an ordinary reward difference.

When authenticity is optimal **only because of future state transitions**, the learner must estimate:

1. the immediate cost of authenticity;
2. the probability of entering Accepted versus Stigmatized;
3. the long-run value of Accepted;
4. the long-run cost of Stigmatized;
5. the possibility of escaping or redeeming from Stigmatized.

The correct preference can therefore depend on a multi-step value difference even when one-step experience favors masking.

This creates an obvious finite-horizon learning burden.

## 9.2 Early rejection can alter both value estimates and state visitation

A rejected authentic action from Neutral does more than generate a negative reward.

It also moves the process into the Stigmatized state.

Thus:

```text
bad authentic outcome
    ↓
negative immediate reward
    +
entry into a lower-value state
    ↓
different future observations and opportunities
```

This is structurally stronger than the E01 hot-stove mechanism, where an early bad outcome changes the learner's estimate but does not create a persistent environmental state.

## 9.3 The learner must experience rare or delayed beneficial transitions

If Accepted is valuable but difficult to reach, the benefit of authenticity may be under-sampled.

Similarly, if redemption from Stigmatized requires authentic attempts, avoiding authenticity can prevent the learner from observing the transition that would justify it.

This creates an endogenous observation problem layered on top of the dynamic state problem.

---

# 10. Where should disagreement be strongest?

The exact phase boundaries have **not** been derived analytically for Article V1, so no closed parameter region should be claimed.

Nevertheless, the mathematics identifies plausible high-risk regimes.

## 10.1 Near a dynamic policy boundary

Whenever

\[
D_N(V)\approx0,
\]

the full-information Q-values of mask and authenticity are close.

Small finite-sample estimation errors can then reverse the learned ordering.

This is the dynamic analogue of the vulnerable boundary region in E01/E02.

## 10.2 Where immediate reward favors masking but dynamic value favors authenticity

The particularly informative regime is:

\[
\Delta_0(p)<0
\]

but

\[
D_N(V)>0.
\]

Equivalently,

\[
p<\frac{43}{60}
\]

while

\[
\gamma
\left[
pV_A+(1-p)V_S-V_N
\right]
>
-\Delta_0(p).
\]

Here the learner cannot succeed by estimating immediate rewards alone.

It must learn the future-state value correctly.

A finite-horizon learner is therefore especially vulnerable to choosing masking even though the exact dynamic optimum is authenticity.

## 10.3 High discount factor

Increasing `gamma` increases the importance of future state.

When the optimality of authenticity depends on reaching or preserving favorable future social state, larger `gamma` can increase the difference between:

- immediate reward ranking;
- dynamic objective ranking.

This does not automatically mean the learner performs worse, but it makes the optimization problem more genuinely dynamic.

## 10.4 Persistent Accepted state

A smaller turnover probability `delta` makes Accepted more persistent.

That can make successful authenticity more valuable because reaching Accepted yields a longer stream of high rewards.

This can expand regimes in which authenticity is dynamically worthwhile even when its immediate Neutral reward is weak.

## 10.5 Persistent or costly Stigmatized state

Lower escape probability `eta`, lower `b2`, or larger `r2` can make Stigmatized more costly.

This has competing consequences:

- it can make initial authentic risk objectively less attractive;
- but when authenticity is required for redemption, it can make correct long-run planning more dependent on understanding future transitions.

The direction of the full policy boundary is therefore not safely inferable from one parameter alone.

The exact phase-boundary problem remains open.

---

# 11. Does E03 show persistent suboptimal masking?

E03 is stronger than E01 in one important sense.

E01 found a trajectory effect:

```text
early rejection
→ less later authenticity
→ higher regret
```

but no detectable overall final-mask difference.

E03 instead reports a **learned-policy versus dynamic-optimum classification** over the tested grid.

Thus E03 establishes that, under the frozen finite-horizon learner, there are many tested conditions in which:

\[
\text{learned neutral-state preference = mask}
\]

while

\[
\text{full-information optimal neutral-state action = authentic}.
\]

This is genuine end-of-training policy disagreement.

However, the word **persistent** must be used carefully.

M2 contains persistent **environmental state** by construction.

E03 does not prove that the learner is permanently or irreversibly locked into masking.

With finite positive softmax exploration and a longer horizon, further sampling can remain possible.

Therefore the defensible wording is:

> finite-horizon learned masking differs from the full-information dynamic optimum in many tested M2 conditions.

Not:

> the learner enters an irreversible persistent masking state.

---

# 12. Is E03 merely another hot-stove effect?

No, although hot-stove/endogenous-sampling effects can contribute.

The distinction is:

## E01

```text
same stateless objective
+
early adverse observation
→ value-estimation/sampling distortion
```

## E03

```text
action changes persistent environment state
+
future state changes future rewards
+
learner must estimate delayed transition value
→ learned policy can differ from dynamic oracle
```

The dynamic state means the objectively optimal action itself depends on future consequences.

That feature is absent from E01.

The exact neutral-state decomposition makes this explicit:

\[
D_N(V)
=
\underbrace{\Delta_0(p)}_{\text{static reward}}
+
\underbrace{
\gamma[pV_A+(1-p)V_S-V_N]
}_{\text{persistent-state value}}
\]

E03 is therefore not reducible to the M0 threshold.

---

# 13. Relation to established theory

Generic reinforcement-learning and incomplete-learning theory makes a finite-horizon learner/oracle discrepancy unsurprising in principle.

The hand-off literature audit therefore does not permit the claim:

> A learner can differ from a full-information optimum, and this is formally novel.

What remained unresolved at hand-off was narrower:

> Whether close formal prior art already combines disclosure/concealment with persistent endogenous reputation/stigma/acceptance state and the specific learner/full-information comparison used here.

Accordingly, E03's contribution status must remain tied to the formal prior-art adjudication in the Article-V1 literature stage.

Regardless of novelty class, the computational result itself remains scientifically usable because M2 explicitly isolates persistent social-state structure and compares the frozen learner against an exact dynamic benchmark.

---

# 14. Comparison with E01 and E02

| Dimension | E01 | E02 | E03 |
|---|---|---|---|
| Main structural change | Restricted feedback after early rejection | Graded independent actions | Persistent social state |
| Objective problem | Static two-action | Static graded, but endpoint-optimal | Dynamic MDP |
| Main learning difficulty | Correcting adverse early evidence | Identifying endpoint across more independent actions | Learning delayed state-transition value |
| Final policy distortion | Not detected overall | Detected away from optimal endpoint | Detected relative to full-information dynamic optimum |
| Exact benchmark | Static M0 objective | Static M1 endpoint theorem | Exact Bellman/value-iteration optimum |
| Main generic alternative | Hot-stove/endogenous sampling | Sample dilution/representation | Generic finite-horizon MDP/incomplete learning |
| Distinct structural content | None beyond feedback | Action representation | Persistent endogenous social consequences |
| Strongest safe interpretation | Temporary learning cost | Endpoint-identification failure | Learner/oracle dynamic-policy disagreement |

---

# 15. Final interpretation of E03

> In the frozen M2 experiment, a finite-horizon learner selected masking in the Neutral state across many tested conditions where exact dynamic programming selected authenticity. M2 differs fundamentally from the stateless baseline because authentic action changes persistent future social state, so the full objective contains both immediate reward and continuation value. The exact mathematics shows that future Accepted/Stigmatized-state value can reverse the static M0 preference, including regimes where immediate reward favors masking but the dynamic optimum favors authenticity. E03 therefore demonstrates a finite-horizon learner/full-information dynamic-policy discrepancy in a persistent-state social environment. It does not establish irreversibility, prevalence, an information-matched learner failure, or a closed-form parameter region for the discrepancy.

---

# 16. Article-V1 claim boundary for E03

## Supported

- M2 is a genuine persistent-state dynamic optimization problem rather than a stateless bandit.
- Accepted-state authenticity is exactly dominant under `a+c>0`.
- Neutral-state dynamic value can reverse the static M0 reward ordering.
- Stigmatized-state authenticity can be justified by future redemption value even when its immediate reward is inferior.
- Under the frozen learner, learned Neutral-state masking differs from the exact full-information dynamic optimum across a broad region of the tested grid.
- The full-information optimum is a legitimate oracle benchmark.
- Persistent social state is a structurally meaningful difference from E01/M0.

## Supported only with qualification

- The tested-grid disagreement can be described as finite-horizon suboptimal masking **relative to the full-information dynamic objective**.
- `243/357` may be reported only as a count/fraction of the frozen tested grid.
- Persistent-state structure may carry contribution weight only after the formal prior-art adjudication is closed.

## Not supported

- `243/357` is prevalence.
- The learner failed to find the best policy attainable under its own information constraints.
- M2 proves irreversible or permanent masking.
- The experiment identifies a calibrated human stigma transition process.
- The M2 states correspond directly to empirically measured longitudinal gifted states.
- A closed analytic phase boundary for learner/oracle disagreement has been established.
- The exact cause of every E03 mismatch cell is known.
- The full-information gap can currently be decomposed into information cost versus learner inefficiency.
- M4/endogenous receptivity evidence may be used to strengthen E03 for Article V1.

---

# 17. Main scientific lesson

E03 changes the question from:

```text
Can early bad evidence make the learner avoid a good action?
```

to:

```text
Can the learner correctly value an action whose main benefit or cost
comes from changing the future social state?
```

The core structural equation is:

\[
\boxed{
\text{dynamic action value}
=
\text{immediate reward}
+
\text{future social-state value}
}
\]

The scientifically important E03 regime is therefore not merely one in which authenticity has a slightly higher one-step payoff.

It is the harder regime in which:

```text
masking looks better immediately
but
authenticity is better dynamically
```

because successful authenticity can enter or preserve a more valuable future social state, while authenticity under stigma may also create redemption value.

That is the conceptual step from E01 to E03.
