# Article V1 Analytic Results and Proofs

**Canonical hand-off mathematical reference — revised 15 August 2026**

**Authority status:** Article-V1 mathematical authority for hand-off, revised after the 15 August model-analysis consistency audit and tied to repository commit `441cfe44856d0cbc3da57089cbe91755b0cc4780`. It distinguishes exact model consequences, learner identities, exact dynamic-programming benchmarks, simulation findings, and open mathematical questions.

**Scope boundary:** M0-M3 and the general softmax lemmas are Article-V1 relevant. M4 is retained strictly as Track-B mathematical context and is not Article-V1 confirmatory evidence.

**15 August 2026 consistency correction:** this authority incorporates the model-analysis audit. In particular, it limits Proposition G2 to two-action softmax probabilities, adds the exact E01/E02 regret identities, and records an independent deterministic verification of the M2 objective envelope.

---

**Repository provenance used for this reference**

| **Item**         | **Value**                                |
|------------------|------------------------------------------|
| Repository       | mousomer/gifted-masking                  |
| Reference commit | 441cfe44856d0cbc3da57089cbe91755b0cc4780 |
| M0 blob          | a142fc04aee3451bca50d110d3ea0fda1c0972e4 |
| M1 blob          | e64546cad9db5d376326ea3dea461daf0b926c10 |
| M2 blob          | 91df8ae77a3555b060732ff059eb94f2bd525e33 |
| M3 blob          | d4b38cb0620460d096d7fd6f1b005b00a7c1949a |
| M4 blob          | df61944a8b3f71a1a339399486ad23b3e022ee0d |
| Core blob        | f25723fed941a4c6cd8338f076a1b2d97d67041f |

# Contents and proof registry

> 1\. Scope, notation, and interpretive levels
>
> 2\. General learner lemmas: subjective reward and softmax
>
> 3\. M0: binary masking/authenticity model
>
> 4\. M1: graded disclosure model
>
> 5\. M2: persistent social-state MDP
>
> 6\. M3: heterogeneous contexts and comparison cost
>
> 7\. M4: endogenous receptivity dynamics (Track B context only)
>
> 8\. Cross-model identities and structural correspondences
>
> 9\. Consequences for E01-E05 interpretation
>
> 10\. What is proved, what is simulated, and what remains open
>
> Appendix A. Exact default arithmetic
>
> Appendix B. Machine-verification targets
>
> Appendix C. Provenance and change-control checklist

| **ID** | **Result**                                 | **Status**                              | **Use**                |
|--------|--------------------------------------------|-----------------------------------------|------------------------|
| G1     | Softmax positivity and odds ratio          | Exact learner identity                  | V1 interpretation      |
| G2     | Binary softmax 50% crossover               | Exact learner identity                  | E05                    |
| G3     | Reward-scale / temperature equivalence     | Exact learner identity                  | Learner limitation     |
| M0.1   | Objective reward gap and p crossover       | Exact analytic                          | M0 / E01 baseline      |
| M0.2   | Objective rejection-cost boundary          | Exact analytic                          | Model geometry         |
| M0.3   | Loss-weighted subjective crossover         | Exact analytic, sign-regime conditional | Learner interpretation |
| M0.4   | Loss-weight monotonicity                   | Exact analytic, sign-regime conditional | Learner interpretation |
| M1.1   | Affine reward in disclosure level          | Exact analytic                          | E02                    |
| M1.2   | Endpoint-optimum theorem                   | Exact analytic                          | E02                    |
| M1.3   | M0-M1 objective-boundary identity          | Exact analytic                          | E02                    |
| M2.1   | Exact transition/reward operators          | Exact model contract                    | E03                    |
| M2.2   | Accepted-state authenticity dominance      | Exact analytic                          | E03                    |
| M2.3   | Policy evaluation by matrix inverse        | Exact analytic                          | E03 benchmark          |
| M2.4   | Bellman contraction / unique V\*           | Standard exact theorem applied to M2    | E03 benchmark          |
| M2.5   | Neutral dynamic-gap decomposition          | Exact identity                          | E03 interpretation     |
| M2.6   | Stigmatized redemption-value decomposition | Exact identity                          | E03 interpretation     |
| M3.1   | Full-information objective is K-invariant  | Exact analytic                          | E04                    |
| M3.2   | General comparison-cost crossover          | Exact analytic                          | E05                    |
| M3.3   | Default crossover bf\*=8/17                | Exact analytic                          | E05                    |
| M3.4   | Good-authentic vs bad-authentic boundary   | Exact analytic                          | E04/E05                |
| M4.1   | Receptivity interval invariance            | Exact under k in \[0,1\]                | Track B only           |
| M4.2   | Pure-masking geometric recurrence          | Exact analytic                          | Track B only           |
| M4.3   | Pure-authentic expected drift              | Exact one-step expectation              | Track B only           |
| M4.4   | Pure-authentic mean-drift fixed point      | Mean-field analytic                     | Track B only           |
| M4.5   | Coupled policy-receptivity drift           | Exact conditional expectation           | Track B only           |

# 1. Scope, notation, and interpretive levels

The models use the same basic reward primitives but progressively add
disclosure levels, persistent state, heterogeneous social contexts, and
endogenous receptivity. The exact mathematics below is useful only if
the level of interpretation is kept explicit.

| **Symbol**  | **Meaning**                                                               | **Default where applicable** |
|-------------|---------------------------------------------------------------------------|------------------------------|
| b           | baseline benefit associated with social participation / acceptance        | 1.0                          |
| a           | authenticity/display increment                                            | 0.6                          |
| c           | masking/concealment cost                                                  | 0.25                         |
| r           | rejection penalty magnitude                                               | 2.0                          |
| λ           | multiplicative weight applied by the learner to negative observed rewards | 1.0                          |
| α           | Q-learning step size                                                      | 0.1                          |
| τ           | softmax temperature                                                       | 0.25                         |
| γ           | discount factor in M2                                                     | 0.9                          |
| p           | acceptance/receptivity probability                                        | varies                       |
| d           | graded disclosure level in M1, d in \[0,1\]                               | grid-dependent               |
| η           | escape probability from stigmatized state in M2                           | varies                       |
| δ           | turnover probability from accepted to neutral in M2                       | 0.02                         |
| b2          | masking baseline while stigmatized in M2                                  | 0.5                          |
| r2          | failed-authenticity penalty while stigmatized in M2                       | 2.5                          |
| K           | number of social contexts in M3                                           | varies                       |
| p_good      | acceptance probability in receptive context                               | 0.85                         |
| p_bad       | acceptance probability in non-receptive contexts                          | 0.20                         |
| bf          | comparison cost applied to accepted authentic reward in good context      | varies                       |
| p_min,p_max | receptivity bounds in M4                                                  | 0.05, 0.95                   |
| k_m,k_a,k_r | M4 receptivity movement rates after masking, acceptance, rejection        | varies; k_a=.12, k_r=.04     |

| **Interpretive levels.** Every result should be tagged as one of: (i) objective/environmental reward identity; (ii) learner-side transformed-reward or softmax identity; (iii) full-information dynamic-programming benchmark; (iv) finite-horizon simulation finding; or (v) human/construct interpretation. Exact algebra at levels (i)-(iii) does not establish level (v). |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 2. General learner lemmas: subjective reward and softmax

> *Maintained implementation: src/gifted_masking/core.py \| blob SHA
> f25723fed941a4c6cd8338f076a1b2d97d67041f*

## 2.1 Negative-reward transform

The maintained learner transforms the observed scalar reward before
updating the selected Q-value. For λ \>= 0:

φ_λ(x) = x if x \>= 0; φ_λ(x) = λx if x \< 0.

| **Consequence.** λ modifies the learner update only. It does not alter the environmental/objective reward function used in analytic objective comparisons. Therefore an objective threshold and a learner-side subjective threshold are distinct quantities whenever λ != 1. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 2.2 Proposition G1 - softmax positivity, ordering, and odds ratios

π_i(Q;τ) = exp(Q_i/τ) / Σ_j exp(Q_j/τ), τ \> 0.

**Proposition G1.** For finite Q-values and τ\>0: (a) every action has
strictly positive probability; (b) Q_i\>Q_j iff π_i\>π_j; and (c)
π_i/π_j = exp((Q_i-Q_j)/τ).

**Proof.** Exponentials of finite real numbers are positive, the common
denominator is positive, and division of the two softmax probabilities
cancels that denominator. Because exp is strictly increasing, the
probability ordering is identical to the Q ordering. QED.

| **Interpretive limit.** A fixed-temperature softmax rule does not create an absorbing action by itself: every action remains selectable at every finite Q. However, the odds ratio is exponential in the Q gap, so a negatively valued action can become practically rare within a finite horizon. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 2.3 Proposition G2 - binary 50% crossover

π_A = 1 / (1 + exp(-(Q_A-Q_M)/τ)).

**Proposition G2.** For exactly two actions and any common finite τ\>0,
π_A = 1/2 if and only if Q_A = Q_M. Temperature changes the slope of the
response curve but not the Q-value location of the 50% crossover.

**Proof.** Set π_A=1/2. Then 1+exp(-(Q_A-Q_M)/τ)=2, hence
exp(-(Q_A-Q_M)/τ)=1. The exponential equals 1 only when its exponent is
zero, so Q_A=Q_M. The converse is immediate. QED.

| **Scope limit for E05.** Proposition G2 applies only when the measured quantity is a two-action softmax probability. E05 does **not** measure that quantity: its flat `K=4` response is the across-child fraction whose final-window modal arm is the single good-context authentic arm in an eight-action policy. G2 therefore cannot rule out fixed temperature, action-set normalization, or their interaction with learned Q-values as contributors to the observed E05 crossing. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 2.4 Proposition G3 - reward scale and temperature are coupled

**Proposition G3.** For any scale s\>0, softmax(sQ,τ)=softmax(Q,τ/s).
Adding a common constant κ to all Q-values leaves probabilities
unchanged.

**Proof.** Substitute sQ_i/τ = Q_i/(τ/s). For translation,
exp((Q_i+κ)/τ) contributes the same multiplicative factor exp(κ/τ) to
numerator and denominator, which cancels. QED.

| **Scientific implication.** A nominal temperature has meaning only relative to the scale of learned values. Cross-model comparisons that alter reward scale without a corresponding temperature interpretation can alter exploration even when ordinal preferences are unchanged. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 2.5 K-action 50% condition

π_i = 1/2 iff exp(Q_i/τ) = Σ\_{j≠i} exp(Q_j/τ).

Equivalently: Q_i = τ log(Σ\_{j≠i} exp(Q_j/τ)).

Thus the binary equality rule Q_i=Q_j does not extend to K\>2. The
probability of one action depends on the entire competing action set.
This is important whenever a behavioural 0.5 threshold is defined in a
multi-action architecture.

## 2.6 Conditional mean Q-update identity

For a stateless action with transformed-reward mean μ_a = E\[φ_λ(R_a)\],
the maintained update, conditional on selecting action a, is

Q_a(t+1) = Q_a(t) + α\[φ_λ(R_t) - Q_a(t)\].

E\[ΔQ_a \| a selected, Q_a\] = α(μ_a - Q_a).

Therefore μ_a is the fixed point of the conditional mean update. With
constant α and stochastic rewards, this is not a proof that the
stochastic Q process converges to a point; it identifies the mean
reversion target conditional on continued sampling. The selection
process determines whether enough corrective samples arrive within a
finite horizon.

# 3. M0: binary masking/authenticity model

> *Maintained implementation: src/gifted_masking/models/m0.py \| blob
> SHA a142fc04aee3451bca50d110d3ea0fda1c0972e4*

M0 is a stateless two-action environment. Masking yields a deterministic
reward. Authenticity yields an accepted or rejected reward.

R_M = b - c.

R_A = b + a with probability p; R_A = a - r with probability 1-p.

## 3.1 Proposition M0.1 - objective expected reward and linear gap

E\[R_A\] = p(b+a) + (1-p)(a-r) = a + pb - (1-p)r.

Δ_0(p) = E\[R_A\] - R_M = a + c - (1-p)(b+r).

**Proposition M0.1.** The objective authenticity-minus-masking gap is
affine and strictly increasing in p whenever b+r\>0, with slope b+r.

**Proof.** Expand E\[R_A\] and subtract b-c. Collecting terms gives
a+c-(1-p)(b+r). Differentiating with respect to p gives b+r. QED.

## 3.2 Proposition M0.2 - exact objective acceptance crossover

p\*\_obj = 1 - (a+c)/(b+r) = (b-c-a+r)/(b+r), provided b+r ≠ 0.

**Proposition M0.2.** Under b+r\>0, authenticity is objectively
preferred for p\>p\*\_obj, masking for p\<p\*\_obj, and the two are
indifferent at equality.

**Proof.** Set Δ_0(p)=0 and solve the linear equation. Monotonicity from
Proposition M0.1 determines the side of the inequality. QED.

Defaults: p\*\_obj = 1 - 0.85/3 = 43/60 ≈ 0.7166667.

## 3.3 Objective rejection-cost boundary

r\*\_obj(p) = (a+c)/(1-p) - b, for p\<1.

This is the maintained \`objective_indifference_r\` relation. For a
fixed p, rejection penalties below or above this line change the static
objective ordering, subject to the sign convention that r is a
nonnegative penalty magnitude.

## 3.4 Proposition M0.3 - loss-weighted subjective crossover

Assume the default sign regime: b-c \>= 0, b+a \>= 0, and a-r \< 0. Then
masking and accepted authenticity are not transformed, while rejected
authenticity is multiplied by λ.

μ_A^λ = p(b+a) + (1-p)λ(a-r).

p\*\_λ = \[(b-c) - λ(a-r)\] / \[(b+a) - λ(a-r)\].

**Proposition M0.3.** Under the stated sign regime and a positive
denominator, p\*\_λ is the acceptance probability at which the expected
transformed reward of authenticity equals the positive masking reward.
It is a learner-side update boundary, not an environmental objective
boundary unless λ=1.

**Proof.** Set p(b+a)+(1-p)λ(a-r)=b-c, isolate p, and divide by
(b+a)-λ(a-r). QED.

Defaults: p\*\_λ = (0.75 + 1.4λ)/(1.6 + 1.4λ) = (15+28λ)/(32+28λ).

At λ=1: p\*\_λ = 43/60, exactly the objective boundary.

## 3.5 Proposition M0.4 - loss weighting raises the subjective threshold

Write h=r-a\>0 under the sign regime. Then

p\*\_λ = (b-c + λh)/(b+a + λh).

d p\*\_λ / dλ = h(a+c) / (b+a+λh)^2.

**Proposition M0.4.** If h\>0 and a+c\>0, the subjective acceptance
threshold is strictly increasing in λ. As λ→∞, p\*\_λ→1.

**Proof.** Differentiate the quotient. The numerator simplifies to
h\[(b+a)-(b-c)\] = h(a+c), which is positive under the stated
assumptions. The limiting ratio of leading λ terms is 1. QED.

| **λ** | **Default p\*\_λ** |
|-------|--------------------|
| 0     | 0.46875            |
| 0.5   | 0.63043            |
| 1     | 0.71667            |
| 2     | 0.80682            |
| 5     | 0.90116            |

| **Critical distinction.** The formulas above do not prove the finite-horizon behavioural crossing of the Q-learner. They identify objective and expected-transformed-reward boundaries. Finite sampling, constant α, softmax action selection, initialization, and feedback structure remain separate. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|


## 3.6 Proposition M0.5 - E01 normalized pseudo-regret is an action-count identity

In the E01 controlled cells at `p=.75` and `.85`, authenticity is the
unique static objective optimum. Let

\[
g = E[R_A]-E[R_M] > 0.
\]

The experiment's cumulative objective pseudo-regret increments by `g`
exactly when the learner selects Mask and by zero when it selects
Authentic. Therefore, over a horizon of length \(T\),

\[
\text{normalized pseudo-regret}
=
\frac{g\,N_M}{Tg}
=
\frac{N_M}{T},
\]

where \(N_M\) is the number of Mask actions.

In the controlled-initial-outcome comparison, the first action is forced
Authentic in both accepted and rejected strata. If
\(\bar A_{\text{post}}\) denotes the authentic-action rate over steps
\(1,\ldots,T-1\), then

\[
\frac{N_M}{T}
=
\frac{T-1}{T}\left(1-\bar A_{\text{post}}\right).
\]

Hence the rejected-minus-accepted contrasts satisfy exactly

\[
\Delta \text{Regret}_{\text{norm}}
=
-\frac{T-1}{T}\,
\Delta \bar A_{\text{post}}.
\]

For `T=2000`, the frozen E01 sampling contrast `-0.025837...` maps to the
reported regret contrast `+0.025824...` up to stored precision.

**Interpretive consequence.** E01 sampling suppression and normalized
pseudo-regret are the same behavioral information expressed in different
units. They may both be reported, but they must not be counted as
independent confirmations of the mechanism.

# 4. M1: graded disclosure model

> *Maintained implementation: src/gifted_masking/models/m1.py \| blob
> SHA e64546cad9db5d376326ea3dea461daf0b926c10*

M1 replaces the binary action by a disclosure level d in a finite grid
spanning exactly 0 to 1. The acceptance probability decreases linearly
with disclosure:

q(d) = 1 - (1-p)d.

base(d) = ad - c(1-d) = -c + d(a+c).

## 4.1 Proposition M1.1 - expected reward is affine in disclosure

E\[R(d)\] = q(d)\[base(d)+b\] + \[1-q(d)\]\[base(d)-r\].

E\[R(d)\] = b-c + d\[a+c-(1-p)(b+r)\].

**Proposition M1.1.** The full-information static expected reward is
affine in d. Its slope is exactly the M0 authenticity-minus-masking
objective gap Δ_0(p).

**Proof.** Substitute q(d) and base(d), then collect the terms
multiplying d. The constant term is b-c and the coefficient is
a+c-(1-p)(b+r)=Δ_0(p). QED.

## 4.2 Proposition M1.2 - endpoint-optimum theorem

**Proposition M1.2.** If the action set contains d=0 and d=1, then every
strict static objective optimum lies at an endpoint. If Δ_0(p)\>0, d=1
is optimal; if Δ_0(p)\<0, d=0 is optimal; if Δ_0(p)=0, every disclosure
level is exactly indifferent.

**Proof.** An affine function on a closed interval achieves its maximum
at an endpoint unless its slope is zero, in which case it is constant.
Because the finite disclosure grid includes both endpoints, the same
result holds on the grid. QED.

| **E02 consequence.** Adding intermediate disclosure levels does not create a new static objective optimum under the maintained reward model. Any E02 difference between binary and graded conditions is therefore a learning/action-representation effect, not a change in the full-information static optimum. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 4.3 Proposition M1.3 - M0 and M1 share the same objective boundary

Slope = 0 iff p = 1-(a+c)/(b+r) = p\*\_obj.

Defaults: slope = 3p - 2.15 = 3(p - 43/60).

**Proof.** The M1 slope equals Δ_0(p) by Proposition M1.1, so its zero
is exactly the M0 objective indifference point. QED.

## 4.4 Action-count invariance of the objective optimum

Let D_L be any disclosure grid with L\>=2 that contains 0 and 1. Because
the reward is affine, the maximum objective expected reward over D_L is
identical for every L:

max\_{d∈D_L} E\[R(d)\] = max{E\[R(0)\], E\[R(1)\]}.

| **Interpretation.** Changing the number of graded actions alters the learner problem while leaving the static objective optimum unchanged. This cleanly separates action-space/sample-allocation effects from objective-value effects. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|


## 4.5 Proposition M1.4 - normalized regret equals mean endpoint distance in authenticity-optimal cells

Let the M1 affine slope be

\[
s = a+c-(1-p)(b+r).
\]

When \(s>0\), the unique objective endpoint is \(d=1\). Because

\[
E[R(d)] = E[R(0)] + sd,
\]

the objective regret of choosing disclosure \(d\) instead of \(1\) is

\[
E[R(1)]-E[R(d)] = s(1-d).
\]

Normalizing by the endpoint gap \(s=E[R(1)]-E[R(0)]\) gives

\[
\boxed{\text{normalized regret}(d)=1-d.}
\]

Averaged over the horizon, normalized regret is therefore exactly the
mean endpoint distance \(1-\bar d\) in the authenticity-optimal E02
cells.

**Interpretive consequence.** The frozen E02 normalized-regret contrast
is objectively meaningful, but it is not an independent welfare signal
beyond mean disclosure intensity under this affine reward model.

# 5. M2: persistent social-state MDP

> *Maintained implementation: src/gifted_masking/models/m2.py \| blob
> SHA 91df8ae77a3555b060732ff059eb94f2bd525e33*

M2 introduces three persistent states: Neutral N, Accepted A, and
Stigmatized S. Actions are Mask M and Authentic A_u (subscripted here to
distinguish the action from the Accepted state). The model is a finite
discounted MDP under the full-information benchmark.

## 5.1 Exact one-step reward functions

r_N(M) = b-c.

r_N(A_u) = p(b+a) + (1-p)(a-r).

r_A(M) = b-c, r_A(A_u) = b+a.

r_S(M) = b2-c.

r_S(A_u) = (p/2)(b+a) + (1-p/2)(a-r2).

## 5.2 Proposition M2.1 - exact transition rows

Using state order (N,A,S), the action-conditioned transition rows are:

| **Current state** | **Mask transition** | **Authentic transition**      |
|-------------------|---------------------|-------------------------------|
| N                 | (1, 0, 0)           | (0, p, 1-p)                   |
| A                 | (δ, 1-δ, 0)         | (δ, 1-δ, 0)                   |
| S                 | (η, 0, 1-η)         | ((1-p/2)η, p/2, (1-p/2)(1-η)) |

| **Proof.** These rows follow directly from the event order in \`transition_step\`: neutral authenticity branches by acceptance; accepted-state turnover is independent of action; stigmatized authenticity redeems with probability p/2 and otherwise has the same escape-versus-stay mechanism as masking. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.3 Proposition M2.2 - authenticity strictly dominates masking in the Accepted state

**Proposition M2.2.** If a+c\>0, authenticity is strictly optimal in the
Accepted state for every discount factor γ, every p, η, δ, b2, r2, and
every continuation value function.

Q(A,A_u) - Q(A,M) = (b+a)-(b-c) = a+c \> 0.

**Proof.** Both actions have exactly the same transition distribution
from the Accepted state: δ to Neutral and 1-δ back to Accepted.
Therefore their future-value terms cancel. The reward difference is a+c.
QED.

| **Reduction.** The full-information optimal policy needs no search over the Accepted-state action when a+c\>0. Only the Neutral and Stigmatized decisions can switch, reducing the relevant deterministic stationary policy set from 2^3=8 to 2^2=4. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.4 Proposition M2.3 - exact policy evaluation

For any stationary deterministic policy π, construct the 3x3
row-stochastic matrix P^π by selecting the appropriate row for each
state and the expected reward vector r^π. The discounted value vector
satisfies

V^π = r^π + γP^πV^π.

V^π = (I - γP^π)^(-1) r^π, 0 \<= γ \< 1.

**Proposition M2.3.** The inverse exists for every stationary policy
when 0\<=γ\<1.

**Proof.** A row-stochastic matrix has spectral radius at most 1.
Therefore the spectral radius of γP^π is at most γ\<1. Hence I-γP^π is
nonsingular and its inverse is the convergent Neumann series Σ\_{t\>=0}
γ^t(P^π)^t. QED.

| **Verification route.** Because there are only four relevant policies when a+c\>0, exact matrix evaluation of all four provides an independent benchmark for value iteration. This is a useful future machine-verification test even if value iteration remains the production implementation. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.5 Proposition M2.4 - Bellman contraction and unique full-information optimum

(TV)(s) = max_a { r(s,a) + γ Σ\_{s'} P(s'\|s,a)V(s') }.

**Proposition M2.4.** For 0\<=γ\<1, the Bellman optimality operator is a
γ-contraction in the sup norm. It has a unique fixed point V\*, and
value iteration converges to V\* from any initial bounded value vector.

**Proof sketch.** For any V,W and each action, the expected future-value
difference is bounded by γ\|\|V-W\|\|∞. Taking a maximum over actions
cannot increase that bound. Thus \|\|TV-TW\|\|∞ \<= γ\|\|V-W\|\|∞.
Banach's fixed-point theorem gives uniqueness and convergence. QED.

| **Benchmark meaning.** This is a full-information optimum: the planner knows the transition and reward model. It is not an optimum under the simulated learner's information channel, prior, sample budget, or update rule. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.6 Reduced Bellman equations

Because Accepted-state authenticity is dominant, the optimality
equations can be written as:

V_A = (b+a) + γ\[(1-δ)V_A + δV_N\].

V_N = max{ (b-c)+γV_N, r_N(A_u)+γ\[pV_A+(1-p)V_S\] }.

V_S = max{ (b2-c)+γ\[ηV_N+(1-η)V_S\],
r_S(A_u)+γ\[(p/2)V_A+(1-p/2)(ηV_N+(1-η)V_S)\] }.

V_A = \[(b+a)+γδV_N\] / \[1-γ(1-δ)\].

This substitution reduces any fixed policy regime to a small linear
system in V_N and V_S. Exact symbolic regime boundaries are therefore in
principle obtainable, although Article V1 currently uses value iteration
rather than a closed-form phase-boundary theorem.

## 5.7 Proposition M2.5 - Neutral dynamic-gap decomposition

D_N(V) = Q(N,A_u;V)-Q(N,M;V)

D_N(V) = Δ_0(p) + γ\[pV_A + (1-p)V_S - V_N\].

**Interpretation.** The first term is exactly the M0 static reward gap.
The second is the dynamic value of entering Accepted or Stigmatized
states rather than remaining Neutral. Therefore dynamic M2 can reverse
the M0 static ordering in either direction.

| **Dynamic-authenticity override condition.** If Δ_0(p)\<0 (static M0 favors masking), authenticity can nevertheless be dynamically preferable whenever γ\[pV_A+(1-p)V_S-V_N\] \> -Δ_0(p). |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.8 Proposition M2.6 - Stigmatized redemption-value decomposition

D_S(V) = Q(S,A_u;V)-Q(S,M;V).

D_S(V) = \[r_S(A_u)-(b2-c)\] + γ(p/2)\[V_A - {ηV_N+(1-η)V_S}\].

**Proof.** If authenticity fails to redeem, its next-state distribution
over Neutral versus Stigmatized is identical to masking: η and 1-η.
Authenticity adds a p/2 chance of moving instead to Accepted.
Subtracting the two Q expressions therefore leaves the immediate reward
difference plus p/2 times the value advantage of Accepted over the mask
continuation distribution. QED.

| **Interpretation.** Even when authenticity has lower immediate expected reward in the Stigmatized state, it can be optimal because of redemption value. This is a genuine dynamic-state mechanism and cannot be inferred from a stateless bandit calculation. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.9 Default immediate-reward geometry

Neutral: r_N(M)=0.75; r_N(A_u)=-1.4+3p; crossover p=43/60.

Accepted: r_A(M)=0.75; r_A(A_u)=1.60; authenticity advantage=0.85.

Stigmatized: r_S(M)=0.25; r_S(A_u)=-1.9+1.75p.

For p in \[0,1\], -1.9+1.75p \<= -0.15 \< 0.25, so under the defaults
masking always has the higher immediate expected reward while
stigmatized. Any optimal authenticity in S must therefore be justified
by the future redemption term, not immediate reward.


## 5.10 Independent deterministic verification of the M2 objective envelope

The 15 August 2026 model-analysis consistency audit independently
enumerated the four relevant deterministic stationary policies after
using Proposition M2.2 to fix the Accepted-state action to Authentic.
For every one of the 357 frozen `p × eta` cells, each policy value was
computed by exact finite-state policy evaluation,

\[
V^\pi=(I-\gamma P^\pi)^{-1}r^\pi,
\]

and the componentwise maximum across the four policy values was compared
with the maintained value-iteration output.

The maximum absolute discrepancy over the entire frozen grid was

\[
\boxed{8.99\times10^{-10}}.
\]

No cell exceeded \(2\times10^{-8}\).

This is an independent deterministic verification of the
**full-information objective comparator** used by E03. It does not
construct an information-matched optimum and therefore does not remove
the comparator-interpretation limitation.

Selected frozen objective threshold brackets for Neutral-state
authenticity are approximately:

\[
p^*(\eta=0)\approx0.384,\qquad
p^*(\eta=.2)\approx0.339,\qquad
p^*(\eta=.8)\approx0.269.
\]

These are deterministic selected-parameter results, not a closed theorem
that the threshold is monotone in \(\eta\) for all parameter values.

# 6. M3: heterogeneous contexts and comparison cost

> *Maintained implementation: src/gifted_masking/models/m3.py \| blob
> SHA d4b38cb0620460d096d7fd6f1b005b00a7c1949a*

M3 has K contexts. One designated good/receptive context has acceptance
probability p_good; the remaining contexts have p_bad. Each context has
mask and authentic actions in the flat representation. Comparison cost
bf is applied only to the accepted authentic reward in the good context.

## 6.1 Exact expected reward classes

R_M = b-c for every context.

R_G(bf) = p_good(b+a-bf) + (1-p_good)(a-r).

R_B = p_bad(b+a) + (1-p_bad)(a-r) for every bad context.

## 6.2 Proposition M3.1 - full-information objective value is independent of K under one-good-context design

**Proposition M3.1.** For K\>=1 with exactly one good context and fixed
p_good,p_bad,bf, the set of distinct expected reward values is {R_M,
R_G, R_B}. Increasing K only changes the multiplicity of R_M and R_B; it
does not change the full-information optimal value max{R_M,R_G,R_B}.

**Proof.** Every mask action has reward R_M, the single good-context
authentic action has R_G, and every other authentic action has R_B.
Replicating bad contexts duplicates existing expected values but creates
no new value. QED.

| **E04 consequence.** With one good context held fixed, any deterioration with K is not caused by the objective best reward becoming smaller. It reflects search, representation, sampling allocation, or action-set normalization. This is why controls that alter the number/proportion/identity of good contexts are scientifically important. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 6.3 Proposition M3.2 - general good-context comparison-cost crossover

R_G(bf) = (a-r) + p_good(b+r-bf).

bf\*\_GvsM = \[p_good(b+a)+(1-p_good)(a-r) - (b-c)\] / p_good,
p_good\>0.

Equivalent: bf\*\_GvsM = \[a-r + p_good(b+r) - (b-c)\] / p_good.

**Proposition M3.2.** For p_good\>0, R_G is affine and strictly
decreasing in bf with slope -p_good. The formula above is the unique
comparison cost at which good-context authenticity and masking have
equal objective expected reward.

**Proof.** Expand R_G and set it equal to b-c. Because the coefficient
of bf is -p_good\<0, there is a unique solution. QED.

## 6.4 Proposition M3.3 - default exact crossover bf\*=8/17

Defaults: p_good=17/20, b=1, a=3/5, c=1/4, r=2.

R_G(bf) = (17/20)(8/5-bf) + (3/20)(-7/5) = 23/20 - (17/20)bf.

R_M = 3/4 = 15/20.

23/20 - (17/20)bf = 15/20 ⇒ 17bf = 8 ⇒ bf\* = 8/17 ≈ 0.4705882353.

**Proposition M3.3.** Under the frozen default objective parameters,
good-context authenticity is objectively better than masking for
bf\<8/17, tied at 8/17, and worse for bf\>8/17.

## 6.5 Proposition M3.4 - good-authentic versus bad-authentic boundary

R_G - R_B = (p_good-p_bad)(b+r) - p_good·bf.

R_G \> R_B iff bf \< \[(p_good-p_bad)(b+r)\]/p_good.

Defaults: threshold = \[(0.85-0.20)·3\]/0.85 = 39/17 ≈ 2.29412.

Defaults: R_B = 0.2·1.6 + 0.8·(-1.4) = -0.8.

Since R_B=-0.8 and R_M=0.75 under the defaults, bad-context authenticity
is never the objective competitor near the E05 range. Thus the 8/17 line
is not merely a pairwise equality; it is the global full-information
switch between the unique good-authentic arm and the K masking arms
under the default one-good-context design.

## 6.6 Objective ties and multiplicity at the crossover

At bf=8/17 under the defaults, the good-authentic action and every
masking action have the same expected reward 0.75, while every
bad-authentic action remains at -0.8. Hence the objective optimum is
non-unique at the exact boundary. Below it, good-authentic is uniquely
optimal. Above it, the K masking actions are tied for objective optimum.

| **E05 distinction.** The exact 8/17 boundary is an environmental payoff boundary. The learned flat-architecture crossing near 0.313 is a simulation-estimated eight-action modal-response transition. The current mathematics does not prove the size or cause of that displacement. Proposition G2 remains an exact theorem about a two-action softmax probability, but it does not exclude temperature/action-set normalization as contributors to the E05 statistic. The exact objective line remains 8/17. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 7. M4: endogenous receptivity dynamics - Track B context only

> *Maintained implementation: src/gifted_masking/models/m4.py \| blob
> SHA df61944a8b3f71a1a339399486ad23b3e022ee0d*

| **V1 status.** The equations in this section are exact consequences of the maintained M4 update rule, but M4 is not Article-V1 confirmatory evidence. These results must not be used to claim human hysteresis, irreversible entrenchment, or an empirical endogenous-receptivity effect. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Let p_t be current receptivity. The update is action- and
outcome-dependent:

Accepted authenticity: p\_{t+1}=p_t + k_a(p_max-p_t).

Rejected authenticity: p\_{t+1}=p_t - k_r(p_t-p_min).

Masking: p\_{t+1}=p_t - k_m(p_t-p_min).

## 7.1 Proposition M4.1 - interval invariance

**Proposition M4.1.** If p_t∈\[p_min,p_max\] and each of k_a,k_r,k_m
lies in \[0,1\], then every un-clipped update remains in
\[p_min,p_max\]; the explicit clip is therefore inactive in exact
arithmetic under those conditions.

**Proof.** Each update is a convex combination of p_t and one boundary.
For example accepted authenticity gives (1-k_a)p_t+k_a p_max; masking
gives (1-k_m)p_t+k_m p_min. Convex combinations of points in the
interval remain in the interval. QED.

## 7.2 Proposition M4.2 - pure-masking geometric recurrence

p\_{t+1}-p_min = (1-k_m)(p_t-p_min).

p_t-p_min = (1-k_m)^t (p_0-p_min).

**Proposition M4.2.** For 0\<k_m\<1, repeated masking drives receptivity
monotonically and geometrically toward p_min. For k_m=0 receptivity is
unchanged; for k_m=1 it reaches p_min in one step.

**Proof.** Subtract p_min from the masking recurrence and iterate. QED.

Half-life in steps: t_1/2 = ln(1/2) / ln(1-k_m).

Steps to \|p_t-p_min\| \<= ε: t \>= ln(ε/\|p_0-p_min\|) / ln(1-k_m),
with inequality interpreted using ln(1-k_m)\<0.

## 7.3 Proposition M4.3 - pure-authentic expected drift

Conditional on current p and always choosing authenticity, acceptance
occurs with probability p. Under k_a,k_r∈\[0,1\], clipping is inactive
and

F_A(p) := E\[p\_{t+1}-p_t \| p, authentic\]

F_A(p) = p k_a(p_max-p) - (1-p)k_r(p-p_min).

**Proof.** Weight the accepted increment +k_a(p_max-p) by probability p
and the rejected decrement -k_r(p-p_min) by probability 1-p, then add.
QED.

## 7.4 Proposition M4.4 - quadratic mean-drift fixed point

F_A(p) = (k_r-k_a)p^2 + \[k_a p_max - k_r(1+p_min)\]p + k_r p_min.

**Mean-drift fixed point.** Any interior p satisfying F_A(p)=0 is a
fixed point of the deterministic mean map p↦p+F_A(p). This is not by
itself the stationary distribution or an almost-sure fixed point of the
stochastic process.

If k_a ≠ k_r: roots follow the quadratic formula with A=k_r-k_a, B=k_a
p_max-k_r(1+p_min), C=k_r p_min.

If k_a = k_r = k: p\* = p_min / (1+p_min-p_max), when the denominator is
nonzero.

With default k_a=0.12, k_r=0.04, p_min=0.05, p_max=0.95, the quadratic
is

-0.08 p^2 + 0.072 p + 0.002 = 0,

with roots approximately -0.0269696 and 0.9269696.

Only p≈0.92697 lies inside \[0.05,0.95\]. For the mean map,
F_A'(p\*)≈-0.076315, so the local derivative of p+F_A(p) is
approximately 0.923685, indicating local stability of the mean-field
fixed point. This remains a mean-field diagnostic, not a proof about the
full stochastic learner-environment system.

## 7.5 Proposition M4.5 - coupled expected receptivity drift under the actual softmax policy

π_A(Q;τ) = 1 / (1 + exp(-(Q_A-Q_M)/τ)).

E\[Δp \| p,Q\] = π_A(Q;τ) F_A(p) - \[1-π_A(Q;τ)\] k_m(p-p_min).

**Proposition M4.5.** The one-step conditional mean receptivity drift is
the softmax-weighted mixture of the pure-authentic and pure-masking
drifts.

**Proof.** Condition first on which action is sampled. The law of total
expectation gives the authenticity probability times F_A(p), plus the
masking probability times -k_m(p-p_min). QED.

| **Why hysteresis is not proved.** The action probability depends on evolving Q-values, and Q-updates depend on stochastic rewards generated from p. The resulting coupled stochastic system is not reduced to the one-dimensional mean map above. Schedule-dependent path separation in a simulation is therefore not, by itself, a theorem of bistability or hysteresis. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 7.6 Instantaneous objective boundary versus forward-looking M4 objective

At any fixed current p, the one-step reward comparison is exactly the M0
comparison and crosses at p=43/60 under defaults. But a planner that
internalizes how current action changes future p faces a different
dynamic-control problem. Article V1 does not currently define or solve
that full-information M4 control problem, and no M4 objective phase
boundary should be inferred from the one-step M0 line.

# 8. Cross-model identities and structural correspondences

| **Identity**                 | **Exact statement**                                                                  | **Scientific use**                                                         |
|------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| M0 ↔ M1                      | M1 reward slope in d equals M0 authenticity-minus-mask gap Δ_0(p).                   | Shows graded levels do not change static objective boundary.               |
| M0 ↔ M2 Neutral              | M2 Neutral immediate reward comparison is exactly M0.                                | Separates static reward from persistent-state future value.                |
| M0 ↔ M3 good context at bf=0 | R_G(0) equals M0 authentic expected reward evaluated at p=p_good.                    | Shows bf is an additional good-context accepted-reward cost.               |
| M0 ↔ M4 instantaneous reward | At current p_t, M4 one-step rewards are M0 rewards with p=p_t.                       | Shows endogeneity enters through p dynamics, not immediate reward formula. |
| M1 action count              | Changing number of disclosure levels leaves static optimum value unchanged.          | Separates representation/sample allocation from objective reward.          |
| M3 context count             | Changing K under one-good-context design leaves full-info objective value unchanged. | Separates context search from objective reward.                            |
| Binary softmax               | τ cannot move the Q-equality location of a **binary softmax probability** crossover. | Does not by itself constrain E05's eight-action across-child modal statistic. |

## 8.1 Static-versus-dynamic hierarchy

- M0: static binary reward problem.

- M1: static reward remains affine; action representation becomes
  graded.

- M2: reward primitives remain familiar, but persistent states make
  future value part of the objective.

- M3: objective reward classes are simple, while search/representation
  grows with context multiplicity.

- M4: current reward remains M0-like, but the environment variable p
  becomes action-dependent and endogenous.

# 9. Consequences for E01-E05 interpretation

| **Experiment** | **Analytic constraint**                                                                                                                          | **What it permits**                                                                                   | **What it forbids**                                                                                          |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| E01            | M0 objective boundary and learner-side subjective boundary are distinct; finite-horizon sampling is not analytically fixed by either.            | Use M0 as objective baseline and learner-update geometry.                                             | Do not infer persistent final masking from the static threshold or from loss weighting alone.                |
| E02            | M1 expected reward is affine; endpoints contain every static optimum; optimum value is level-count invariant.                                    | Interpret graded effects as learning/action-representation effects under the maintained reward model. | Do not claim intermediate levels create a superior static objective policy.                                  |
| E03            | M2 has an exact full-information discounted optimum; Accepted-state authenticity is dominant; dynamic terms can reverse static Neutral ordering. | Say aggregate final-window Neutral behavior favored masking while the full-information dynamic optimum favored authenticity where adjudicated. | Do not call the aggregate action-count classifier an individual learned policy or an information-matched failure; π_I\* is not computed. |
| E04            | Under one-good-context M3, objective best value is independent of K.                                                                             | Use the combined controls to support a bounded representation-dependent burden under scarce receptivity. | Do not attribute the effect to K alone, scarcity alone, duplicate-mask normalization alone, or literal human movement among groups. |
| E05            | Exact objective bf\*=8/17; Proposition G2 applies only to a two-action softmax probability, whereas E05 uses an eight-action across-child modal-arm fraction. | Compare the empirical modal-response crossing with the distinct analytic objective anchor, carefully. | Do not use G2 to rule out temperature/action-set normalization as contributors, and do not claim the displacement mechanism is identified. |

## 9.1 Exact versus empirical numbers

| **Quantity**                      | **Type**                          | **Value/status**                                             |
|-----------------------------------|-----------------------------------|--------------------------------------------------------------|
| M0/M1 objective p crossover       | Exact analytic                    | 43/60 ≈ 0.716667                                             |
| M3/E05 objective bf crossover     | Exact analytic                    | 8/17 ≈ 0.470588                                              |
| E05 flat learned crossing         | Simulation/inference              | 0.312852; 95% master-seed bootstrap \[0.307836, 0.316918\]   |
| E03 policy classification         | Simulation vs exact DP comparator | Adjudicated on frozen tested grid; not a prevalence quantity |
| M4 mean-drift root under defaults | Mean-field analytic context only  | p≈0.926970; not V1 evidence                                  |

# 10. What is proved, what is simulated, and what remains open

## 10.1 Results suitable as mathematical authorities

- M0 objective reward gap, p crossover, and r-indifference formula.

- M0 expected transformed-reward crossover under the stated sign regime,
  plus its monotonicity in λ.

- M1 affine expected reward, endpoint-optimum theorem, and equality of
  the M0/M1 objective boundary.

- M2 exact transition/reward operators, Accepted-state dominance, exact
  policy evaluation, Bellman contraction, and dynamic-gap
  decompositions.

- M3 K-invariance of the full-information objective under
  one-good-context design, general bf crossover, exact default 8/17
  result, and good-vs-bad authentic boundary.

- Binary and K-action softmax identities, including the
  fixed-temperature 50% result.

- M4 pure-masking recurrence and conditional expected receptivity
  drifts, explicitly restricted to Track-B/context status.

## 10.2 Simulation findings that are not proofs

- E01 rejection-conditioned changes in subsequent authentic sampling and
  regret.

- E02 preservation of nonzero disclosure alongside reduced full-endpoint
  discovery and pooled regret result.

- E03 number/geometry of learned-policy versus full-information-policy
  classifications on the frozen tested grid.

- E04 learned burden as K and receptive-context scarcity/representation
  vary.

- E05 learned flat-architecture crossover near 0.313 and the
  hierarchical left-censored result.

- Any M4 path-schedule or hysteresis-style diagnostic.

## 10.3 Open mathematical problems - do not silently convert to established results

| **Open item**                      | **Required result**                                                                                                                                                                                                                 |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| O1 - Information-matched optimum   | Construct π_I\* for M2 under the learner's prior/observation/sample constraints, or explicitly define a bounded-rational benchmark. Needed to decompose the full-information gap into information cost versus learner inefficiency. |
| O2 - Closed M2 phase boundaries    | Exploit the four-policy reduction and solve exact inequalities in p,η,γ,b2,r2,δ for Neutral and Stigmatized optimal actions. Current V1 uses exact numerical DP rather than a closed theorem.                                       |
| O3 - E05 displacement mechanism    | Explain quantitatively why the maintained eight-action modal-response statistic crosses near 0.313 while the objective line is 8/17. The binary G2 theorem is inapplicable to this statistic; temperature, action-set normalization, endogenous sampling, and learned-value effects remain unresolved contributors. |
| O4 - Structured-disclosure learner | Compare M1 independent-action tabular learning to a learner that generalizes over d. The endpoint theorem is exact, but the observed graded-learning effect is learner-representation dependent.                                    |
| O5 - M4 full-information control   | Define a planner that internalizes action effects on p and solve or characterize the optimal dynamic policy.                                                                                                                        |
| O6 - M4 bistability/hysteresis     | Prove fixed points, stability, or bifurcations of an explicitly defined deterministic approximation, and separately characterize the stochastic process. Current schedule-dependent simulations do not establish hysteresis.        |
| O7 - Escape-time theory            | For fixed τ\>0, replace irreversible language with hitting/escape-time quantities where appropriate; derive scaling with value gaps, τ, persistence parameters, and horizon.                                                        |

| **Hand-off rule.** A future agent may extend this document only by stating assumptions, proving the result, and identifying whether the proof is environmental, learner-side, dynamic-programming, or mean-field. Numerical observations should remain in evidence/results documents, not be promoted into theorem language. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# Appendix A. Exact default arithmetic

| **Quantity**                               | **Exact / simplified form** | **Decimal**   |
|--------------------------------------------|-----------------------------|---------------|
| Mask reward b-c                            | 3/4                         | 0.75          |
| Accepted authentic reward b+a              | 8/5                         | 1.60          |
| Rejected authentic reward a-r              | -7/5                        | -1.40         |
| M0/M1 gap Δ_0(p)                           | 3p - 43/20                  | 3p - 2.15     |
| M0/M1 p crossover                          | 43/60                       | 0.7166667     |
| M2 stigmatized mask reward b2-c            | 1/4                         | 0.25          |
| M2 stigmatized authentic expected reward   | -19/10 + (7/4)p             | -1.9 + 1.75p  |
| M3 good-auth reward                        | 23/20 - (17/20)bf           | 1.15 - 0.85bf |
| M3 bad-auth reward                         | -4/5                        | -0.80         |
| M3 bf crossover good-auth vs mask          | 8/17                        | 0.4705882     |
| M3 bf crossover good-auth vs bad-auth      | 39/17                       | 2.2941176     |
| M4 default pure-auth mean root in interval | numeric quadratic root      | 0.9269696     |

## A.1 Useful exact identities

Δ_0(p) = a+c-(1-p)(b+r).

With defaults: Δ_0(p)=0.85-3(1-p)=3p-2.15.

M1: E\[R(d)\] = 0.75 + d(3p-2.15).

M3: R_G(bf)-R_M = 0.40 - 0.85bf.

Therefore bf\*=0.40/0.85=40/85=8/17.

# Appendix B. Machine-verification targets

The following checks are cheap deterministic tests that can protect the
mathematical contract from regression. They do not require scientific
simulation.

| **ID** | **Contract**             | **Suggested deterministic assertion**                                                                                                             |
|--------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| B1     | M0 expected reward       | For random parameter tuples, compare \`expected_rewards\` to the closed forms and assert Δ_0 equality.                                            |
| B2     | M0 objective crossover   | At p=p\*\_obj assert expected gap≈0; perturb p on both sides and verify sign when b+r\>0.                                                         |
| B3     | M0 subjective boundary   | Under the sign regime, compute expected transformed reward directly and compare with p\*\_λ / r\*\_λ formulas.                                    |
| B4     | M1 affine reward         | For random d values, finite-difference second derivative should be zero to tolerance; endpoints reproduce M0 rewards.                             |
| B5     | M1 endpoint optimum      | For arbitrary L\>=2, exhaustive grid maximum must equal endpoint maximum.                                                                         |
| B6     | M2 transitions           | Enumerate each state/action and compare analytical transition probabilities/rewards with Monte-Carlo-free branch logic or exact constructed rows. |
| B7     | M2 accepted dominance    | Assert both action transition rows equal in Accepted and reward difference equals a+c.                                                            |
| B8     | M2 policy enumeration    | Evaluate four relevant deterministic policies by matrix inverse and compare optimal V with production value iteration.                            |
| B9     | M3 K invariance          | For K=1,2,4,16 with one good context, exhaustive expected-reward maxima must match.                                                               |
| B10    | M3 8/17 anchor           | At defaults and bf=8/17, good-auth and mask expected rewards must both equal 0.75 exactly within floating tolerance.                              |
| B11    | M3 competitor ordering   | At defaults assert bad-auth=-0.8 and remains below mask; verify good-vs-bad boundary 39/17.                                                       |
| B12    | Softmax binary crossover | For arbitrary τ\>0 and equal Qs, probability exactly 0.5; perturb Q gap and verify ordering.                                                      |
| B13    | Softmax scaling          | Assert probabilities(Q\*s,τ) = probabilities(Q,τ/s) for s\>0.                                                                                     |
| B14    | M4 pure mask             | Compare iterative \`update_receptivity\` under mask to closed form p_min+(1-k_m)^t(p0-p_min).                                                     |
| B15    | M4 authentic drift       | For chosen p, compare analytic F_A(p) with exact two-outcome expectation of the update rule.                                                      |

# Appendix C. Provenance and change-control checklist

| **File**                        | **Reference blob SHA**                   | **Analytic sections depending on it**             |
|---------------------------------|------------------------------------------|---------------------------------------------------|
| src/gifted_masking/core.py      | f25723fed941a4c6cd8338f076a1b2d97d67041f | Section 2; learner-side interpretation throughout |
| src/gifted_masking/models/m0.py | a142fc04aee3451bca50d110d3ea0fda1c0972e4 | Section 3; M0 cross-model identities              |
| src/gifted_masking/models/m1.py | e64546cad9db5d376326ea3dea461daf0b926c10 | Section 4                                         |
| src/gifted_masking/models/m2.py | 91df8ae77a3555b060732ff059eb94f2bd525e33 | Section 5                                         |
| src/gifted_masking/models/m3.py | d4b38cb0620460d096d7fd6f1b005b00a7c1949a | Section 6                                         |
| src/gifted_masking/models/m4.py | df61944a8b3f71a1a339399486ad23b3e022ee0d | Section 7 only; Track B context                   |

| **Invalidation rule.** Any semantic change to the listed reward functions, transition order, subjective-value transform, softmax rule, comparison-cost placement, or receptivity update invalidates the corresponding proofs until re-derived. Pure refactors that preserve semantics should be guarded by the deterministic checks in Appendix B. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## C.1 Publication-use checklist

- When quoting 43/60, state that it is the static objective acceptance
  crossover under the frozen M0/M1 reward parameters.

- When quoting 8/17, state that it is the exact M3 good-context
  objective comparison-cost crossover under the frozen defaults.

- When discussing E03, use “full-information dynamic optimum” unless and
  until an information-matched benchmark exists.

- When discussing E05, keep the analytic 8/17 line and the learned
  ~0.313 crossing conceptually separate.

- Do not use M4 mean-field or recurrence results as Article-V1
  confirmatory evidence.

- Do not describe finite-horizon softmax behaviour as irreversible
  merely because recovery is slow or unobserved in a finite run.

- Do not interpret a tested-grid fraction as a prevalence or intrinsic
  measure of phase-space volume.

**End of reference document**
