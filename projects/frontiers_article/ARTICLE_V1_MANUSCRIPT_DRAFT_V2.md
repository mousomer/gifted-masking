# Learning, concealment, and objective benchmarks: a computational model cascade

**Stage 3 working manuscript, revision 2.** This draft implements
`ARTICLE_V1_DRAFT_REVIEW_RESULTS_TONE_INTERVENTION.md` against the frozen
evidence base. Every quantitative statement traces to
`ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md` or `ARTICLE_V1_ANALYTIC_RESULTS.md`
at its adjudicated ceiling wording. The §4.5 leverage discussion is governed by
`ARTICLE_V1_LEVERAGE_DISCUSSION_AUTHORITY.md`. No evidence, model, config, or
artifact was altered in producing it.

## Abstract

Some gifted young people manage how visible their ability is across social
settings, but an observed low-visibility strategy does not by itself identify
why it persists. We develop a cascade of reinforcement-learning environments in
which the objectively best action is known exactly, and compare it with what a
finite learner does. Three exact results structure the comparison. First, a
learner-side weighting of negative outcomes moves the behavioural boundary from
an acceptance probability of .469 to 1 while the environment is untouched; in
simulation, raising that weight from .5 to 2.5 changed final concealment by
0.403 (95% CI [0.395, 0.411]) with objective payoffs held fixed. Second, making
social standing persistent moves the objective authenticity boundary from
p = .717 to between .384 and .269 as adverse standing becomes easier to leave,
so the same action is objectively wrong in a one-shot setting and objectively
right once it can change future standing. Third, once acceptance is achieved,
authentic action is optimal for every parameter configuration of the model.
Against these benchmarks, finite learners diverged in four distinct ways: early
rejection reduced later authentic sampling (−0.026 [−0.036, −0.016]);
independent graded disclosure levels raised continued engagement (+0.255) while
reducing discovery of the objectively optimal endpoint (−0.329); a receptive
context that remained objectively available became harder to find as
alternatives multiplied (−0.234 flat, −0.470 hierarchical); and a learned
comparison-cost boundary arrived at .313 [.308, .317] while the environment did
not turn until 8/17 = .471, with authenticity still holding a third of its
maximum objective advantage at the point learners abandoned it. The models also
identify candidate points of leverage — within the model, making foregone outcomes
observable reduced concealment about 2.5 times as much as creating opportunities
to act, and making adverse standing escapable changed what was optimal rather than
only what was learned — while showing that the weighting parameter is a larger
mover than any of them and confounds inference from behaviour to environment. They
specify the four quantities that would have to be measured together to distinguish
these mechanisms in people.

## 1. Introduction

### 1.1 Ability visibility as a sequential-learning problem

Giftedness is not a uniform social-emotional condition. Reviews and
community-sample evidence caution against treating high cognitive ability as a
general deficit or assuming that all high-ability young people encounter the
same peer difficulties (Lavrijsen and Verschueren, 2023; Tourreix et al., 2023).
At the same time, a substantial literature documents that some young people
manage how visible their ability, interests, or performance is in social
settings. The stigma-of-giftedness tradition describes conditional concerns
about being treated differently when exceptional ability becomes known, and
social-coping research identifies strategies including denial, conformity,
helping, selective disclosure, and altered social interaction (Coleman and
Cross, 1988; Cross et al., 1991; Swiatek, 1995). These strategies vary across
settings, social groups, and developmental circumstances rather than
constituting a single trait.

We use *concealment*, or lower-visibility behaviour, as a bounded operational
term for the low-visibility end of that strategy family. It does not equate
privacy, strategic self-presentation, or temporary conformity with pathology,
and it does not import clinical meanings of masking. The substantive question is
narrower: how can a lower-visibility response remain learned when more authentic
expression would have greater value in the specified social environment? This
question concerns the temporal relation between action, social feedback, and
later action.

The available literature describes strategies and context dependence more
readily than it identifies the sequential process that sustains one strategy.
The same visible endpoint can arise because an environment is genuinely
unreceptive, because early adverse feedback discouraged further testing, because
an individual weights bad outcomes heavily, because a useful intermediate action
divides limited experience, because a receptive setting is hard to identify, or
because the immediate and future values of a response differ. Cross-sectional
observation of low visibility does not separate these possibilities, and it does
not establish whether the response is advantageous under a defined environment.

### 1.2 Why observed concealment does not identify its cause

Reinforcement learning provides a compact way to formalize this identification
problem. In hot-stove learning, an early negative sample from a variable action
reduces subsequent sampling of that action, and the resulting absence of
corrective evidence can preserve avoidance without any fixed aversion to risk
(March, 1996; Denrell and March, 2001). This is established generic learning
theory. Its relevance here is methodological: the outcome of a learner's choice
determines the information available for later learning.

The identification problem is sharper than the hot-stove effect alone suggests,
and one of our exact results states how sharp. In the simplest environment we
study, the acceptance probability at which a learner's own updates stop favouring
authenticity is

```
p*_λ = [(b − c) + λ(r − a)] / [(b + a) + λ(r − a)],
```

where λ is the weight the learner applies to negative outcomes. This quantity is
strictly increasing in λ and approaches 1 as λ grows. At the reference payoffs it
sweeps from .469 to 1 while the environment — every reward, every probability —
stays exactly as it was. A single observation of how often someone conceals is
therefore consistent with almost any receptivity, unless the weighting is
independently known. Observed behaviour is not a value function, and in this
model it is not even a bounded estimate of one.

Three further distinctions follow. In a static environment, an action may carry
a lower learned value because it was sampled unfavourably, despite a greater
expected environmental reward. In a stateful environment, a seemingly costly
action may improve later standing and therefore have higher dynamic value. In a
heterogeneous environment, a good option can exist while remaining hard to
identify and use. Conflating these turns either low or high concealment into an
unsupported conclusion about adaptation.

This article therefore compares finite learned behaviour with an explicit
full-information benchmark in every environment. The benchmark is an oracle
relative to stated rewards and transitions; it is not a claim about human
welfare, moral desirability, or what a learner could know at the moment of
choice. We use "objective" only in this conditional, model-relative sense.

### 1.3 Contribution and model progression

The contribution is an existence-and-structure model cascade with exactly
specified comparators, not a calibrated psychological model. M0 is a two-action
risky-authenticity bandit that isolates history-dependent sampling and
negative-outcome weighting. M1 adds graded disclosure while preserving the static
endpoint geometry. M2 adds Accepted and Stigmatized social states, so the
relevant objective becomes a dynamic policy. M3 adds heterogeneous contexts that
must be discovered and, within that environment, a comparison-cost axis. The
sequence is logical rather than developmental, and no model step maps to a fixed
unit of human time.

Five frozen experiments instantiate this progression. E01 asks whether an initial
rejection changes later authentic sampling, and separately how far a learner's
weighting of negative outcomes moves observed concealment when the environment is
fixed. E02 asks whether independently learned disclosure levels change discovery
of an objectively best endpoint. E03 compares aggregate final-window action
patterns with an exact full-information dynamic policy in the persistent-state
model, and locates the objective boundary itself. E04 asks whether an objectively
favourable context is equally discoverable across action architectures. E05
compares the environmental comparison-cost crossover with a learner's operational
behavioural crossover. Figure 1 summarizes the formal progression and the
benchmark assigned to each rung.

The synthesis is bounded but not modest. Immediate reward, dynamic value,
discoverability, and a learned behavioural boundary are four distinct quantities,
and the cascade measures the distance between them in each case. Because the
environments are exactly specified, the models also rank candidate points of
leverage against one another and state what each would require to be tested in
people. The experiments do not estimate the prevalence of concealment, establish
a causal mechanism in gifted populations, or evaluate an educational
intervention.

## 2. Model framework and methods

### 2.1 Modelling objective and common learner

We use a sequence of deliberately simplified reinforcement-learning environments
to ask when a finite learner reduces authentic expression even though a
full-information benchmark favours it. The numerical parameters define a
normalized reference scale rather than estimates of psychological utility, social
transition rates, or the prevalence of any response.

Three quantities are distinguished throughout. Environmental reward is the payoff
generated by an environment and defines the objective comparison. Learned value
is a finite learner's estimate based on selected experience. The full-information
benchmark is an oracle that knows the relevant payoff and, for the stateful
model, transition structure.

All learners start with action values of zero and use a constant learning rate
`alpha=0.1` and softmax temperature `tau=0.25`. A realized reward `R` is
transformed only before the learning update: `v_lambda(R)=R` for nonnegative
outcomes and `lambda R` otherwise. At the reported baseline `lambda=1`, so the
learner update and environmental reward coincide and negative-outcome weighting
does not explain the headline results; λ is varied deliberately in one E01
condition reported in §3.2. For a selected stateless action `x`,

\[
Q_{t+1}(x)=Q_t(x)+\alpha[v_\lambda(R_t)-Q_t(x)].
\]

At each step the learner samples available actions with a numerically stable
softmax,

\[
P(X_t=x)=\frac{\exp\{Q_t(x)/\tau\}}
{\sum_{x'}\exp\{Q_t(x')/\tau\}}.
\]

The row maximum is subtracted before exponentiation in implementation. The finite
horizon is an operational number of model steps, not a calendar unit.
Final-window summaries use the last 20% of a run and describe end-of-episode
behaviour rather than asymptotic convergence. Standard E01, E02, E04, and E05
runs use `n=500` learners, `T=2000`, and five independent master seeds. E03 uses
`n=160` and `T=1000` per grid cell because its outcome is a fixed-grid
classifier.

### 2.2 M0 and E01: adverse history and negative-outcome weighting

M0 offers masking `M` and authenticity `A`. Masking has deterministic reward
`R_M=b-c`; authenticity is accepted with probability `p` and otherwise rejected:

\[
R_A=\begin{cases}b+a,&\text{accepted},\\a-r,&\text{rejected}.\end{cases}
\qquad
\mathbb E[R_A]-R_M=a+c-(1-p)(b+r).
\]

With the common reference values `(b,a,c,r)=(1.0,0.6,0.25,2.0)`, masking returns
0.75, authenticity has expectation `-1.4+3p`, and the static objective boundary
is `p=43/60≈.7167`.

The learner's own boundary is a different quantity. Under the reference sign
regime — masking and accepted authenticity nonnegative, rejected authenticity
negative — only the rejection outcome is transformed, so the learner's expected
transformed reward equalizes at

\[
p^*_\lambda=\frac{(b-c)+\lambda(r-a)}{(b+a)+\lambda(r-a)}
=\frac{15+28\lambda}{32+28\lambda},
\]

with derivative `h(a+c)/(b+a+λh)² > 0` for `h=r-a>0`. The boundary is therefore
strictly increasing in λ and tends to 1 (Table 1). At `λ=1` it equals the
objective boundary 43/60 exactly; away from `λ=1` the two separate by
construction.

**Table 1.** Learner-side acceptance boundary as a function of negative-outcome
weighting, at the reference payoffs. The environmental boundary is 43/60 ≈ .717
throughout.

| λ | 0 | 0.5 | 1 | 2 | 2.5 | 5 |
|---|---|---|---|---|---|---|
| p\*_λ | .4688 | .6304 | **.7167** | .8068 | .8333 | .9012 |

E01 has two arms. The history arm conditions on an initially accepted or rejected
authentic outcome in the tested `p=.75/.85` domain and compares later authentic
sampling; within the rejected stratum it also evaluates two information-restoring
manipulations, 5% forced authentic exploration and counterfactual authentic
feedback. The weighting arm holds the environment at `p=.65` and varies λ from .5
to 2.5. The primary history estimand is later sampling; the related normalized
objective pseudo-regret is an exact action-count translation of it, satisfying
`Delta R_norm = -(1999/2000) Delta A` at `T=2000`, and is reported as a change of
units rather than a second result.

### 2.3 M1 and E02: graded disclosure and endpoints

M1 replaces the two actions with independent tabular values for disclosure levels
`d` on a grid containing zero and one, where `d=0` is the masking endpoint and
`d=1` is full authenticity. Acceptance is `1-(1-p)d`, yielding

\[
\mathbb E[R(d)]=b-c+d\{a+c-(1-p)(b+r)\}.
\]

Expected reward is affine in disclosure, and its slope is exactly the M0
authenticity-minus-masking gap. Except at exact indifference, every strict static
optimum lies at an endpoint, and the optimum's value is invariant to how many
intermediate levels the grid contains. Intermediate disclosure is therefore not
made objectively optimal by this specification, and adding levels changes the
learner's problem without changing the objective one.

A second exact consequence governs the regret statistic. When the slope is
positive the unique endpoint is `d=1`, the objective regret of choosing `d` is
`s(1-d)`, and normalizing by the endpoint gap gives normalized regret exactly
`1-d`. E02's regret contrast is therefore mean endpoint distance in different
units, not an independent welfare signal.

E02 compares the binary architecture with five independent disclosure arms after
an initial rejection, using matched random-number streams within master seed and
receptivity. It measures continued nonzero disclosure, final-window selection of
`d=1`, and whether `d=1` is the unique modal final-window arm.

### 2.4 M2 and E03: persistent social state and a dynamic comparator

M2 makes the environment stateful, with explicit states Neutral, Accepted, and
Stigmatized. Authentic acceptance from Neutral moves to Accepted; rejection moves
to Stigmatized; masking does not itself change state. Accepted authenticity has
reliable reward unless turnover `delta` returns the system to Neutral.
Stigmatized outcomes use the specified `b2`, `r2`, and halved redemption
probability, with escape from Stigmatized governed by `eta`. Reward is generated
before the next-state transition. The learner stores `Q(s,a)` and updates the
selected state-action pair with

\[
Q(s,a)\leftarrow Q(s,a)+\alpha\{v_\lambda(R)+\gamma\max_{a'}Q(s',a')-Q(s,a)\},
\]

where `gamma=.9`. The objective comparator is value iteration over the known
reward and transition model.

Two exact properties make that comparator tractable and interpretable. First, the
Neutral dynamic gap decomposes as

\[
D_N(V)=\Delta_0(p)+\gamma[pV_A+(1-p)V_S-V_N],
\]

the static M0 reward gap plus the value of changing standing. The second term can
reverse the first in either direction, which is what makes M2 a different
question rather than a rescaled M0. Second, in the Accepted state both actions
have identical transition rows, so their future-value terms cancel exactly and

\[
Q(\text{Accepted},\text{Authentic})-Q(\text{Accepted},\text{Mask})=(b+a)-(b-c)=a+c>0
\]

for every discount factor, every `p`, `eta`, `delta`, `b2`, `r2`, and every
continuation value function. Concealment is never optimal once acceptance has
been achieved. This reduces the relevant deterministic stationary policy set from
2³ = 8 to 2² = 4 and makes exact policy enumeration cheap enough to serve as an
independent check on the production comparator.

E03 spans a frozen 21-by-17 receptivity-by-escape grid. For each cell, the
reported classifier compares aggregate final-window Neutral-state action counts
with the full-information dynamic policy, subject to a prespecified Neutral
visit-adequacy rule. A cell is labelled learned–objective disagreement only when
aggregate Neutral counts favour masking and value iteration favours authenticity.
This is an action-level aggregate classifier, not an individual policy label or a
prevalence estimate.

### 2.5 M3 and E04: heterogeneous-context discovery

M3 contains `K` contexts: one receptive context with probability `p_good` and
`K-1` unreceptive contexts with `p_bad`. In the reference design `p_good=.85`,
`p_bad=.2`, and `bf=0` for E04. Masking has the common payoff across contexts.
Authenticity uses the context-specific acceptance probability, and comparison
cost `bf` is subtracted only from accepted authenticity in the good context. With
one fixed good context, increasing `K` changes the multiplicity of bad
alternatives but not the set of distinct objective payoff classes
`{R_M, R_G, R_B}` or their maximum. The full-information objective is therefore
K-invariant, and any decline with `K` is a property of the learner rather than of
what is achievable.

E04 compares four representations: `flat_2k`, a single softmax over joint
context–behaviour arms; `hierarchical`, a context softmax followed by a behaviour
softmax with both value tables receiving the realized reward; `global_mask`, one
shared masking action plus context-specific authentic arms; and
`fixed_known_good`, a two-arm problem without context choice. The primary outcome
is the mean, across learners, of an indicator that the argmax of a learner's
final-window action counts is an authentic action in a good context, with ties
permitted by the defined argmax procedure. We call this final-window argmax
classification; it is not convergence, and it does not model literal movement
between peer groups.

### 2.6 E05: objective and learned comparison-cost crossings

E05 holds `K=4` and one good context fixed while varying `bf`. At the reference
parameters masking has expected reward `.75` and accepted good-context
authenticity has expected reward `1.15-.85bf`, so exact objective equality is
`bf*=8/17=0.470588`. Bad-context authenticity has expected reward `-0.80`
throughout and never competes near this range; the good-versus-bad boundary lies
at `39/17≈2.294`. The 8/17 line is therefore not a pairwise tie but the global
full-information switch between the unique good-authentic arm and the `K` masking
arms.

The reported learned response is the across-learner fraction whose final-window
modal arm is the good-context authentic arm in the flat eight-action
architecture. Equal-weight nonincreasing pooled-adjacent-violators (PAVA) fits
are calculated on the dense `.30` to `.65` cost grid, and the reported value is
the fitted 0.5 crossing. Five complete master curves are resampled for a
10,000-resample bootstrap interval. The monotonic fit is an estimator constraint
rather than a claim that each learner or master curve is monotonic. The
hierarchical response is reported as left-censored when it is already below .5 at
the lower fitted boundary, and no crossing is extrapolated.

### 2.7 Inferential units

All reported effect estimates preserve their experiment-specific inferential
unit. E01, E02, and E04 summarize five independent master-seed estimates rather
than treating individual learners as independent replications. E03 preserves a
fixed grid per master, and its stable-cell rule prevents inadequate Neutral-state
exposure from being silently classified. E05 resamples complete master curves so
uncertainty in the fitted crossing reflects run-level response curves rather than
the number of simulated learners. Student-t intervals across the five master
estimates are reported for applicable contrasts.

Full equations, transition kernels, parameter tables, grid definitions, stream
construction, tie mechanics, sensitivity conditions, PAVA details, and provenance
records are routed to Supplementary Methods and repository documentation.

## 3. Results

### 3.1 Early rejection reduced subsequent authentic sampling (E01)

Across the five master seeds, learners assigned an initially rejected authentic
outcome sampled authenticity less often over subsequent steps than learners
assigned an initially accepted outcome (rejected minus accepted `-0.025837`, 95%
CI `[-0.035753,-0.015922]`; Figure 2a). In the stated M0 environment,
authenticity is objectively preferable at both tested receptivities, so the
contrast records a difference in what learners sampled rather than any change in
the environmental payoff comparison. Expressed in objective-loss units, the same
difference is `+0.025824` `[+0.015914,+0.035735]`; the two are algebraically
linked by `Delta R_norm = -(1999/2000) Delta A` and are one result in two units.

A single rejection did not produce a persistent endpoint effect. The
final-window masking contrast was `-0.000343` `[-0.011605,+0.010918]`, and no
equivalence margin was tested.

Restoring information reversed part of the sampling effect, and the two channels
were not equally effective. Within the rejection stratum, 5% forced authentic
exploration reduced final-window masking by `0.046590`
`[0.033230,0.059951]` and normalized regret by `0.057954`
`[0.045614,0.070293]`. Counterfactual authentic feedback — letting the learner
observe what the unchosen authentic action would have returned — reduced final
masking by `0.118135` `[0.109683,0.126587]` and regret by `0.141318`
`[0.132369,0.150267]`, roughly 2.5 times the forced-exploration effect at
equivalent model cost. §4.5 develops the implication.

E01 establishes the baseline against which the rest of the cascade is measured:
an information-restriction effect on sampling large enough to detect and to
reverse, with no persistent endpoint effect from a single adverse outcome. These
are manipulations of the model's information channel within a stipulated
environment.

### 3.2 Negative-outcome weighting moved observed concealment by 0.40 with the environment fixed (E01)

The second E01 arm holds the environment exactly constant and varies only how the
learner weights bad outcomes. At `p=.65`, raising λ from .5 to 2.5 increased
final-window masking by `0.402990` (95% CI `[0.395366,0.410614]`; Figure 2c).
Every environmental quantity — reward magnitudes, acceptance probability,
horizon — was identical across the two conditions.

The analytic boundary in Table 1 explains the size of the effect and extends it.
At `λ=.5` the learner's own indifference point is `.630`, so `p=.65` sits above
it and the learner's updates favour authenticity; at `λ=2.5` the boundary is
`.833`, so the same `p=.65` sits below it and the same updates favour masking.
The two conditions therefore straddle a boundary that the environment never
crossed. Over the full range `λ∈[0,∞)` this learner-side boundary sweeps from
`.469` to 1 — more than half the receptivity range — with the environment fixed
throughout.

The direction of the divergence matters, and it is not the intuitive one. At
`p=.65` the objective gap is `3(.65)-2.15=-0.20`, so masking is the objectively
correct action in both conditions. The `λ=2.5` learner therefore conforms to the
objective optimum, masking on 99.2% of final-window steps, while the `λ=0.5`
learner departs from it, continuing to sample authenticity on roughly 41% of
steps because its own transformed-reward target (`0.795`) exceeds the masking
reward (`0.75`) even though the environmental expectation (`0.55`) does not.
Reducing the weight on adverse outcomes did not move this learner toward the
objective optimum; it moved it away.

This is therefore an identification result rather than a leverage result, and it
should not be read as an argument for lowering negative-outcome weighting. The
supported claim is narrower and more consequential for inference: a
40-percentage-point difference in observed concealment, in either direction
relative to the optimum, carries almost no information about the environment that
produced it. Any inference from an observed concealment rate to the receptivity of
a setting requires the weighting to be known or independently measured.

The weighting acted on the level of concealment rather than on the history effect
of §3.1. The high-λ minus low-λ difference in the controlled early-rejection gap
was `-0.001067` `[-0.015031,+0.012898]`, an interval spanning zero. Loss
weighting and adverse history are therefore separable channels in this model:
one sets where the behavioural boundary sits, the other perturbs sampling around
it. Both estimates are conditional on the reference sign regime, in which only
the rejection outcome is transformed.

### 3.3 Independent graded actions reduced optimal-endpoint discovery (E02)

E02 asks what changes when the visibility continuum is represented as five
independently learned actions rather than binary endpoints. Following initial
rejection, the graded architecture increased continued nonzero disclosure by
`0.255040` (95% CI `[0.253004,0.257077]`) relative to binary resampling of full
authenticity (Figure 3a). More learners continued to disclose something.

The same representation reduced discovery of the objectively best endpoint on
every measure. Full-authentic final-window selection fell by `0.328692`
`[-0.342037,-0.315348]`, the probability that the objectively optimal endpoint
was the unique modal final-window arm fell by `0.221740`
`[-0.288755,-0.154724]`, and pooled normalized regret was worse by `0.029761`
`[-0.033874,-0.025648]` under the prespecified contrast.

The analytic comparison makes this decisive rather than ambiguous. Because M1
expected reward is affine in `d`, full authenticity is the strict objective
endpoint whenever the corresponding binary environment favours it, and the
value of the optimum does not depend on how many intermediate levels exist.
Intermediate actions are not an unmodelled compromise optimum that the graded
learners might have found instead. They are additional claims on a fixed budget
of experience: an outcome at one disclosure level does not update neighbouring
levels, so partial actions accumulate evidence while the full-authentic endpoint
remains relatively under-sampled.

E02 therefore complements E01 rather than replicating it. E01 changes the history
of information about one risky action; E02 changes the action representation
through which information is acquired. The result is conditional on independent
tabular arms and does not predict the behaviour of a learner that generalizes
across ordered disclosure levels.

### 3.4 Persistent standing moved the objective boundary, and learned behaviour tracked neither boundary (E03)

When authentic action changes future social state, the relevant objective
comparison is no longer the static M0 reward threshold, and the size of that
difference is exactly computable. Under the frozen M2 transition model the
objective boundary for Neutral-state authenticity brackets at

| Escape rate η | Objective threshold p\* | Below the static boundary 43/60 = .7167 by |
|---|---|---|
| 0 | [.3839111, .3839722] | .333 |
| .2 | [.3387451, .3388062] | .378 |
| .8 | [.2689819, .2690430] | .448 |

with bisection width `6.1e-05`. Making standing persistent therefore opens a band
of receptivity between .33 and .45 wide in which concealment is objectively
correct in the one-shot environment and objectively incorrect once the same
action can change future standing. Within the tested values, the easier adverse
standing is to leave, the wider that band becomes: raising η from 0 to .8 lowers
the objective threshold by a further `.115`.

The decomposition in §2.4 identifies where this comes from. The Neutral gap is
the static M0 gap plus `gamma` times the value of changing standing, and the
second term dominates across this band. The Accepted state supplies most of it:
authentic action there is optimal for every parameter configuration, with an
exact advantage of `a+c=0.85` per step and no dependence on the continuation
values. Reaching acceptance is worth paying for even when the immediate expected
reward of the attempt is negative.

These are deterministic properties of a stated model, and they were verified
independently. Using the Accepted-state dominance result to fix one action, the
four remaining deterministic stationary policies were evaluated in closed form by
`V^pi=(I-gamma P^pi)^{-1} r^pi` for every one of the 357 frozen cells and
compared against the production value iteration. The maximum absolute discrepancy
over the entire grid was `8.99e-10`, and no cell exceeded `2e-8`.

Finite learners tracked neither boundary. At `n=160` and `T=1000` per cell, the
frozen 21-by-17 grid produced 243 of 357 cells in which aggregate final-window
Neutral-state action counts favoured masking while the full-information dynamic
policy selected authenticity, a fraction identical across all five master seeds.
The classifier was stable in 350 of 357 cells under the prespecified
four-of-five-master rule; seven low-receptivity, `eta=0` cells were inconclusive
because Neutral visits did not meet the adequacy criterion, and were not forced
into either category. The count is defined over cells: a cell enters when
aggregate Neutral final-window counts favour masking, value iteration favours
authenticity, and the visit-adequacy criterion is met. It is tested-grid coverage
under one learner, horizon, and classifier.

The frozen sensitivity results delimit the map. Selected changes to `gamma`,
`alpha`, or `tau` reclassified named sentinel cells: at `gamma=.5` the first
three of five dynamic-authenticity sentinels became learner–objective agreements
in all five masters, which reflects a change in the objective policy itself
rather than better learning. A separately labelled harsh boundary
(`b2=0`, `r2=8`, `delta=.3`, `eta=0`, `p=.75`) reverses the direction entirely:
there the objective Neutral gap is `-0.4062934363` and value iteration selects
masking in all five masters, despite static M0 favouring authenticity at that
receptivity. Dynamic structure does not uniformly favour authenticity. It
relocates the boundary, and the direction of relocation depends on whether
adverse standing can be left.

### 3.5 A favourable context was not equally discoverable across representations (E04)

E04 asks whether objective availability of a receptive context is sufficient for
a finite learner to use authentic behaviour there. The one-good-context M3
environment supplies an exact baseline: increasing `K` creates additional bad
contexts but leaves the distinct payoff classes and the full-information best
expected reward unchanged, so any `K` response is a property of the learner
rather than of a shrinking opportunity.

In the flat `2K` architecture, increasing the number of contexts from one to 16
changed final-window argmax classification as authentic in a good context by
`-0.2340` (95% CI `[-0.246417,-0.221583]`; Figure 5a). Under the hierarchical
architecture, in which context and behaviour are represented in separate but
jointly rewarded tables, the corresponding contrast was `-0.4704`
`[-0.511031,-0.429769]`. These are architecture-specific estimates and do not
rank learning architectures in general.

The controls locate the effect. In `fixed_known_good` there is no context choice
and the structural K effect is exactly zero. In `global_mask`, where one masking
action is shared across contexts while authentic actions remain context-specific,
the K contrast was `+0.0088` `[0.002090,0.015510]` — distinguishable from zero
but practically negligible under the prespecified band. Randomizing which context
is the receptive one did not materially change the decline: the random-minus-fixed
slope contrasts were `-0.00292` `[-0.012269,0.006429]` for flat and `+0.00140`
`[-0.012620,0.015420]` for hierarchical learning, ruling out a fixed-label
artifact in this design.

Receptive-context abundance mattered more than context count. With two good
contexts the change relative to one was `+0.05064` `[0.045204,0.056076]` for flat
and `+0.02524` `[0.012988,0.037492]` for hierarchical; in the tested
proportional-25% design the corresponding recoveries were `+0.06044`
`[0.055044,0.065836]` and `+0.11224` `[0.104787,0.119693]`. Holding the
proportion of receptive contexts fixed largely removes the decline that adding
contexts otherwise produces.

The supported claim is a conjunction: a representation-dependent finite discovery
burden, most evident under scarce receptivity. The one-good-context manipulation
confounds increasing `K` with reducing the good fraction to `1/K`, so it does not
separately establish an effect of context count or of scarcity alone, and the
global-mask control changes cardinality, initial mass, competition, and reward
allocation together rather than isolating one of them. Within those limits, E04
separates two propositions that are otherwise easily conflated: a good authentic
option can remain objectively available under full information while its
discovery and use by a finite learner vary with how alternatives are represented
and how densely receptive settings are distributed.

### 3.6 Learned and objective comparison-cost boundaries separated (E05)

E05 varies a comparison cost within M3 to compare an exact environmental boundary
with an operational behavioural one. At the reference payoffs masking returns
`.75` while accepted good-context authenticity returns `1.15-.85bf`, so the
full-information objective crossover is exactly `bf*=8/17=0.470588` (Figure 5b).
Below that value good-context authenticity has the higher expected reward; above
it, masking does.

The learned response turned much earlier. In the flat eight-action (`K=4`) model,
the pooled PAVA fit of the across-learner good-context modal fraction crossed .5
at `bf=0.312852`, with a 10,000-resample master-curve bootstrap interval
`[0.307836,0.316918]` and all 10,000 resamples yielding a valid in-range
crossing. Learners abandoned good-context authenticity at roughly two-thirds of
the cost the environment required. At that point authenticity still held an
objective advantage of about `0.134076` (transformed bounds
`[0.130620,0.138340]`) — **33.5% of the maximum advantage of `0.40` available at
`bf=0`.** The behavioural boundary arrived while a third of the option's value was
still on the table.

Two boundary results frame the estimate. Across the full endpoint range the flat
modal fraction fell by `0.9400` `[-0.957993,-0.922007]` from `bf=0` to `bf=.80`,
confirming that the dense-range crossing sits inside a response that traverses
nearly the whole interval rather than at the edge of a flat curve. The
hierarchical response, by contrast, was already below .5 at the lower dense
boundary `bf=.30`, where its isotonic value was `.1176`, and none of 10,000
bootstrap resamples produced an in-range crossing. Its crossing is left-censored
below the resolved range — earlier still, not absent — and is not comparable as a
point estimate with the flat crossing.

The response is an across-learner final-window modal-classification fraction, not
a per-trial softmax probability, a policy probability, or a binary Q-value
equality, so the binary-softmax half-probability identity does not apply to it
and cannot be used either to attribute or to exclude a temperature effect. E05
establishes a learned–objective crossover displacement in this learner and
reference configuration and measures its size; it does not apportion that
displacement among temperature, multi-action normalization, finite sampling,
endogenous under-sampling, context discovery, or representation.

## 4. Discussion

### 4.1 History, information, and action representation

The cascade distinguishes several reasons why an observed low-visibility action
persists without establishing that it is the best environmental choice. E01 gives
the minimal information-history case: a rejected authentic outcome lowers
subsequent sampling of the action that could correct the estimate, the familiar
hot-stove pattern in which choice determines later evidence (March, 1996;
Denrell and March, 2001). Its information-restoring manipulations show that the
effect is reversible within the model, and that the two available channels are
not equally strong.

E01's weighting arm makes a different and larger point. The λ boundary is an
exact statement that the location of a learner's behavioural transition is a free
parameter with respect to the environment, and the simulated 0.403 difference
shows that the free parameter has room to move observed behaviour across most of
its range. Any empirical design that infers environmental receptivity from
observed concealment rates, without an independent handle on negative-outcome
weighting, is under-identified in exactly this way. That the same manipulation
left the early-rejection gap unchanged (`-0.001067`, interval spanning zero)
indicates the two channels are separable rather than two descriptions of one
sensitivity.

E02 supplies a complementary manipulation rather than a confirmatory one. It
leaves the static endpoint logic intact and expands the learner's independent
action representation, and the outcome splits: more nonzero disclosure after
rejection, less discovery and use of the full-authentic endpoint. E01 restores
missing information about an existing risky alternative; E02 divides finite
evidence across several actions that do not generalize to one another. Their
shared lesson is that behaviour changes through information acquisition and
action representation even while the objective comparison stays fixed. Their
different designs make them a cross-mechanism dissociation, not independent
replications of one treatment effect.

### 4.2 Immediate and dynamic value

M2 changes the mathematical object to be evaluated. M0 and M1 compare static
expected rewards; M2 requires a policy that values state-dependent future
consequences. The size of that change is now quantified rather than asserted: the
objective boundary moves from .717 to between .384 and .269 across the tested
escape rates, so an entire band of receptivity a third to nearly half the scale
wide changes its objective answer purely because the action can alter future
standing.

Two features of that band deserve emphasis. First, its floor is set by the
Accepted state, where authentic action is optimal for every parameter
configuration of the model — a result that holds for all discount factors and all
continuation values, and that has no analogue in the static environments.
Concealment in this model can only ever be optimal as a response to uncertain
standing, never as a response to secure standing. Second, the band widens as
adverse standing becomes easier to leave. Escapability is not a background
condition; it is part of what determines the right answer.

The direction is not uniform, and the harsh sentinel is the necessary
counterweight: with severe stigma and no escape, the objective Neutral gap is
`-0.4063` and value iteration selects masking even where static M0 favours
authenticity. The model therefore resists both symmetric overinterpretations. A
high observed concealment rate does not establish maladaptive avoidance, and a
more favourable immediate authentic payoff does not settle a dynamic question
either. Describing concealment as suboptimal in E03 is meaningful only relative
to the stated full-information dynamic oracle, and the `243/357` map is coverage
of a tested grid under one classifier, not a share of learners or of people.

### 4.3 Availability and discoverability

E04 extends the identification problem from time to alternatives. The
full-information objective is K-invariant in the one-good-context design, yet
finite learners' final-window classifications change substantially as context
structure and representation change. This is a formal demonstration that the
structure of available alternatives, and the cost of discovering them, matter
separately from whether a favourable alternative exists.

The abstraction is relevant to giftedness because social coping and visibility
management are documented as context-sensitive rather than uniform (Coleman and
Cross, 1988; Cross et al., 1991; Swiatek, 1995). It suggests a testable
hypothesis: when receptivity is unevenly distributed and information about
settings is local, opportunities for authentic expression may be harder to
identify and use than their objective availability implies. The abundance
controls sharpen the target — recovery was largest when the *proportion* of
receptive contexts was held fixed rather than when their number rose — but the
model does not represent literal student movement between classrooms, friendship
groups, or placements, and the design does not isolate a single mechanism behind
the decline.

### 4.4 Behavioural and objective boundaries

E05 makes the environment/learner distinction visible at a single reference
configuration and puts a number on it. The objective `8/17` line is a payoff
indifference result. The flat learned crossing at `.313` is an estimator-defined
summary of across-learner end-of-run modal classifications. Their separation
means a finite learner's behavioural transition need not occur where a fully
informed environment changes its optimal action, and here it occurs while a third
of the option's objective advantage remains.

The difference should not be made cleaner than the evidence permits. Because the
response is multi-action and population-level, the binary-softmax identity cannot
attribute or exclude a temperature effect, and neither the curves nor the
analytic result quantify contributions from exploration, action competition,
representation, finite horizon, or learning rate. The left-censored hierarchical
result adds an explicit reason not to generalize a single flat crossing across
architectures.

### 4.5 Where the model locates leverage

Because each environment is exactly specified, the cascade does more than
separate mechanisms: it ranks candidate points of intervention against a common
benchmark and states what each would require to be tested. Table 2 collects the
levers that appear in the frozen experiments.

**Table 2.** Intervention levers present in the model cascade, with their frozen
effects and the measurement each would require.

| Lever | Model operation | Frozen effect | Required measurement |
|---|---|---|---|
| Counterfactual feedback | learner observes the foregone authentic outcome | −0.118 final concealment [.110, .127]; −0.141 regret | whether the outcome of undisclosed ability becomes observable |
| Forced exploration | 5% of trials forced authentic | −0.047 final concealment [.033, .060]; −0.058 regret | frequency of low-stakes disclosure occasions independent of choice |
| Escapable adverse standing | raise η from 0 to .8 | objective threshold .384 → .269 | whether adverse standing can be exited, and how fast |
| Receptive-context density | 1 → 2 good contexts; proportional-25% | +.051 / +.025; +.060 / +.112 | number *and proportion* of settings where ability is welcome |
| Comparison cost | reduce `bf` | learner abandons at .313; environment turns at .471 | salience of within-setting comparison |
| Graded options (adverse) | independent disclosure arms | +.255 engagement, −.329 endpoint use, −.222 modal | whether partial-disclosure options share evidence across levels |
| *Negative-outcome weighting* | *λ .5 → 2.5* | *+0.403 concealment, environment fixed* | *not a lever — the principal confound; see below* |

Magnitudes are comparable only within a shared estimand, stratum, and scale. The
two E01 rows meet that condition and are ordered below; the E03, E04, and E05 rows
are different quantities in different models and are listed as candidates for
attention rather than ranked against one another.

Five implications follow, each stated as a model prediction with a named
observable.

**Information dominates opportunity.** Counterfactual feedback was roughly 2.5
times as effective as forced exploration at equivalent model cost. The bottleneck
in these environments is not access to the authentic action — a softmax learner
can always select it — but that declining to act destroys the evidence that would
have corrected the estimate. The prediction is that interventions revealing what
disclosure would have produced outperform interventions that merely create
occasions to disclose. This is directly testable and would be contradicted if
opportunity-creating designs matched information-revealing ones.

**Interventions calibrated to the objective boundary will be roughly a third too
weak.** In E05 the learner abandoned the good option at `bf=.313` while it still
retained 33.5% of its maximum objective advantage. An intervention that reduces
comparison cost to just below the environmental crossover `8/17` lands well past
the point where behaviour has already moved. The general form of this prediction
— target the behavioural boundary, and treat its distance from the objective
boundary as the required overshoot — is the most directly practical consequence
of the whole cascade, and the one most in need of empirical calibration.

**Expanding the option set can reduce use of the best option.** E02's graded arms
raised continued engagement while cutting endpoint selection and optimal-endpoint
discovery, and the affine-reward theorem proves the intermediate levels create no
compensating objective benefit in this specification. A graduated-disclosure
design whose steps do not let evidence generalize across levels buys breadth by
spending depth. The prediction is falsifiable and specific: it should disappear
for a learner, or a programme, in which experience at one level informs
neighbouring levels.

**Density, not count.** The K decline was largely removed when the proportion of
receptive contexts was held fixed, with recoveries of `+0.060` and `+0.112` in
the proportional-25% design. The implied target is not fewer settings but a
higher fraction of receptive ones. One receptive setting among sixteen is a
search problem; four among sixteen substantially is not.

**Escapability changes what is optimal, not only what is learned.** This is the
one lever in the table that operates on the benchmark. Every other manipulation
moves behaviour toward a fixed objective boundary; raising the escape rate lowers
the objective boundary itself, from .384 to .269, making authentic action
objectively correct across an additional 11.5 points of receptivity. It is also
the most robustly established, being deterministic and verified to `8.99e-10`
rather than estimated. The corresponding empirical question is whether adverse
social standing in a given setting is in fact exitable, and on what timescale.

The honest counterweight belongs in the same table. **The largest single mover in
the entire cascade is the learner, not the environment**, and it is not a lever.
The λ contrast produced `+0.403`, an order of magnitude larger than any
environmental manipulation tested here, but §3.2 shows that at the tested cell the
low-weighting learner departs from the objective optimum rather than approaching
it. Negative-outcome weighting therefore enters this table as the **principal
confound** rather than as a target: it moves observed concealment further than
anything else available, in a direction that does not track the objective
benchmark. Any study attempting to read a setting's receptivity from concealment
behaviour, or to attribute a change in concealment to one of the environmental
levers above, has to measure or control it first.
Distinguishing a setting that is genuinely unreceptive from a learner who weights
rejection heavily is the central measurement problem this cascade poses, and no
manipulation of the environment resolves it.

These are manipulations of stipulated model environments, not estimates of
intervention effects in people. Their value is comparative and directional: they
rank candidate targets within a specified structure and name the observable each
would require. A study motivated by this ranking would need repeated observation
of action, social response, subsequent sampling, and changing standing over time
— the same four quantities that separate the mechanisms in the first place.

### 4.6 Implications for ability visibility

Taken together, the models provide a bounded mechanism-level account of how
persistent concealment-like strategies can be sustained in high-capability
individuals. A low-visibility response can be learned even when an alternative
has greater objective value within a stipulated environment, because early
history can restrict information, a learner's weighting of adverse outcomes can
relocate the behavioural boundary by more than half the receptivity range, an
action representation can dilute endpoint learning, current choice can carry
dynamic consequences, receptive alternatives can be hard to discover, and an
operational behavioural boundary can arrive before environmental indifference.
This concerns the constructed environments, not a diagnosis, a prevalence
estimate, or a claim that gifted people instantiate the models literally.

The giftedness literature supplies both the motivation and the restraint. Some
gifted young people report managing the visibility of ability, conformity, or
disclosure across social settings, but giftedness does not imply a uniform
social-emotional profile or a universal need to conceal (Cross et al., 2019;
Tourreix et al., 2023). The empirical step these models point to is measurement
of sequences: visible action, perceived and observed response, later sampling of
related actions, and changing opportunities across contexts. Such data could
distinguish current adaptation to an adverse environment from restricted
information, negative-outcome weighting, dynamic consequences, or discovery
constraints — mechanisms that look alike in a single endpoint observation and
that Table 2 shows would call for different responses.

## 5. Limitations

Four boundaries define what these results support.

**The models are stylized and the scale is normalized.** Parameters are not
calibrated estimates of the social value of authenticity, the cost of
concealment, acceptance probability, comparison cost, or psychological time.
Model actions are constructs for analysing visibility management, not direct
measures of behaviour, identity, privacy, or clinical masking. The results do not
estimate prevalence in gifted populations, diagnose individuals, or establish
educational intervention effects; Table 2 ranks levers within the model, and its
rows are hypotheses for empirical work rather than effect estimates.

**The benchmarks are oracles, and the learner family is narrow.** The
full-information static and dynamic comparators know the payoff and transition
structure. They are exact, and the M2 comparator was independently verified to
`8.99e-10` across the frozen grid, but they are not information-matched optima
that a finite learner could necessarily attain. Learner–oracle differences are
not decomposed into contributions from observation, exploration, state
uncertainty, finite horizon, or update efficiency. The learner uses tabular
values, a constant learning rate, fixed-temperature softmax selection, and the
stated action representations. E02 in particular is conditional on independent
disclosure arms and does not establish what a learner with structured
generalization would do. The λ results are conditional on the reference sign
regime in which only the rejection outcome is transformed.

**Simulation claims are conditional on executed grids, horizons, and inferential
units.** E03's `243/357` is tested-grid coverage under one aggregate classifier,
not a prevalence estimate or a full parameter characterization, and its
sensitivity cells show that named perturbations of `gamma`, `alpha`, and `tau`
reclassify specific sentinels. E04's K response depends on scarce receptivity and
action architecture, and its controls do not isolate a single mechanism. E05's
crossing rests on five master curves and an estimator-defined PAVA response; its
mechanism decomposition is unresolved and its hierarchical transition is
left-censored below the fitted range. These limitations are reported as
limitations rather than repaired by unexecuted sensitivity analyses.

**Provenance is complete for artifacts, partial for generator source.** The
frozen result artifacts are preserved and hash-validated. E04 and E05 have
fingerprint-exact archived generator bundles; the exact historical
generator-source worktree for E01–E03 was not fully recovered from Git alone.
This constrains exact historical source reconstruction. It does not authorize
replacement runs or change the scope of the frozen evidence.

## 6. Conclusion

This cascade separates learned behaviour from the relevant objective benchmark
rather than treating observed concealment as evidence about which is preferable,
and it measures the distance between them in each environment. Persistent
standing moved the objective boundary by up to .45 in receptivity units, and made
authentic action optimal without exception once acceptance was secured. A
learner-side weighting of adverse outcomes moved observed concealment by 0.40
across a range where the environment never changed. Independent graded actions
raised engagement while reducing discovery of the objectively best endpoint. A
receptive context that remained objectively available became harder to find as
alternatives multiplied. And a learned comparison-cost boundary arrived while a
third of the option's objective advantage was still available. Immediate value,
dynamic value, discoverability, and a learned behavioural boundary are four
distinct quantities, and each pair can come apart.

The article does not offer a calibrated account of gifted students or a universal
mechanism of concealment. It offers explicit environments, exact comparators, and
a ranking of where those environments locate leverage — with the standing caveat
that the largest mover in the cascade is a property of the learner rather than of
the setting. Empirical work can build on this by observing action, social
feedback, subsequent sampling, and contextual opportunity over time, while
retaining the possibility that lower visibility is sometimes a current adaptation
rather than a learning error.

## References

Coleman, L. J., and Cross, T. L. (1988). Is being gifted a social handicap?
*Journal for the Education of the Gifted* 11(4), 41–56.
doi: 10.1177/016235328801100406

Cross, J. R., O'Reilly, C., Kim, M., Mammadov, S., and Cross, T. L. (2019). A
cross-cultural study of the social experience of giftedness. [N = 90 across five
countries; **author list and journal record to be publisher-verified before
submission**.]

Cross, T. L., Coleman, L. J., and Terhaar-Yonkers, M. (1991). The social
cognition of gifted adolescents in schools: managing the stigma of giftedness.
*Journal for the Education of the Gifted* 15(1), 44–55.
doi: 10.1177/016235329101500106

Denrell, J., and March, J. G. (2001). Adaptation as information restriction: the
hot stove effect. *Organization Science* 12(5), 523–538. [**Volume, issue, and
pages to be publisher-verified before submission.**]

Lavrijsen, J., and Verschueren, K. (2023). High cognitive ability and mental
health: findings from a large community sample of adolescents. [**Author list and
journal record to be publisher-verified before submission**; repository sources
cite this as "Lavrijsen et al., 2023".]

March, J. G. (1996). Learning to be risk averse. *Psychological Review* 103(2),
309–319. [**Volume, issue, and pages to be publisher-verified before
submission.**]

Swiatek, M. A. (1995). An empirical investigation of the social coping strategies
used by gifted adolescents. *Gifted Child Quarterly* 39(3), 154–160.
doi: 10.1177/001698629503900305

Tourreix, E., et al. (2023). Non-cognitive specificities of intellectually gifted
children and adolescents: a systematic review of the literature. [**Author list
and journal record to be publisher-verified before submission.**]

### Citation verification status

Verified against `ARTICLE_V1_LITERATURE_AUDIT.md` and the repository source
dossiers in `doc-reviews/docs_august2026/` on 17 August 2026. The dossiers are
AI-generated research syntheses, not primary sources; they were used only to
corroborate year, title, and claim attribution through the published excerpts they
quote, never as bibliographic authority in their own right.

| Reference | Status |
|---|---|
| Coleman and Cross 1988 | Publisher-verified in the literature audit (DOI, JEG 11(4), 41–56). One dossier records it as a book chapter; the audit explicitly corrects that reconstruction. |
| **Cross et al. 1991** | **Year corrected.** Revision 1 of this manuscript cited "Cross et al., 1993". The audit's publisher-verified record is Cross, Coleman and Terhaar-Yonkers **1991**, and two independently published sources quoted in the dossiers cite it as 1991 alongside Swiatek 1995 for precisely the strategy list this sentence supports. A separate "Cross et al. 1993" does appear in some citation lists for the stigma-of-giftedness paradigm; it is not the source for this claim and is not verified here. |
| Swiatek 1995 | Publisher-verified in the audit (DOI, GCQ 39(3), 154–160); corroborated by two quoted published citations. |
| Cross et al. 2019 | Title and design corroborated (N = 90, five countries, interviews across age groups). Lead author appears as J. R. Cross. Full record unverified. |
| Lavrijsen and Verschueren 2023 | Title corroborated. Repository sources render the citation as "Lavrijsen et al., 2023"; the author list needs checking before the two-author form is used. |
| Tourreix et al. 2023 | Title and systematic-review design corroborated. Full record unverified. |
| March 1996; Denrell and March 2001 | Attribution corroborated repeatedly in quoted published text; **no bibliographic metadata for either appears in the repository sources.** Both records above are from general knowledge and must be checked against the publishers. |

---

## Figures

Figures 1–6 are built by the deterministic publication layer
(`projects/frontiers_article/publication_v1/`) from frozen evidence only; captions
are generated from the same CSVs the panels plot. Run:

```bash
.venv/bin/python projects/frontiers_article/publication_v1/scripts/build_publication_v1.py
```

| Figure | Content |
|---|---|
| 1 | Model progression and the exact benchmark fixing each rung. |
| 2 | E01: adverse history (a), the two information channels with their disjoint intervals (b), and the λ boundary against a fixed environment (c). |
| 3 | E02: graded-disclosure contrasts (a) and the affine M1 objective that bounds them (b). |
| 4 | E03: objective boundary relocation with the three exact brackets (a), the classification map (b), and the exact Neutral Q gap (c). |
| 5 | E04 K response (a) and E05 comparison-cost displacement (b). |
| 6 | Cross-experiment synthesis: every boundary the cascade computes (a) and the candidate leverage magnitudes (b). |

If the editor holds to a five-figure main text, Figures 5 and 6 are the merge
candidates; Figure 6 is a synthesis of numbers already plotted elsewhere and can
move to the supplement without loss of evidence.
