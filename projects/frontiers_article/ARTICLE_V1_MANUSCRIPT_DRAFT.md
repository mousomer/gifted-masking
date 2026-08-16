# Learning, concealment, and objective benchmarks: a computational model cascade

**Stage 3 working manuscript.** This authority-reconciled draft is for the
scientific consistency audit and contains only the models and experiments in
the fixed Article V1 scope.

## Abstract

Some gifted young people manage the visibility of their ability across social
settings, but observed lower visibility does not establish whether concealment
is currently advantageous, learned from adverse experience, or sustained by
restricted information. We develop a cascade of reinforcement-learning models
that compares finite learned behaviour with explicit full-information
benchmarks. In E01, an initially rejected authentic action reduced later
authentic sampling, although a persistent final-window masking difference was
not detected. In E02, independently learned graded-disclosure actions increased
nonzero disclosure but reduced discovery and use of the objectively optimal
full-authentic endpoint. In E03, aggregate final-window Neutral actions favoured
masking in 243 of 357 tested persistent-state cells where the dynamic oracle
favoured authenticity; this is tested-grid coverage, not prevalence. In E04,
the full-information value of a receptive context was K-invariant while its
final-window use varied across finite-learning representations. In E05, the
flat learner's operational comparison-cost crossing (`.313`, 95% bootstrap
interval `.308–.317`) preceded the exact objective crossover (`8/17≈.471`).
Together, the models show that immediate value, dynamic value, discoverability,
and learned behavioural boundaries are distinct within the specified
environments. They do not estimate human prevalence, diagnose gifted learners,
or establish intervention effects. Instead, they provide explicit mechanisms
and benchmarks for testing why lower-visibility strategies can persist when a
more authentic alternative remains objectively valuable.

## 1. Introduction

### 1.1 Ability visibility as a sequential-learning problem

Giftedness is not a uniform social-emotional condition. Reviews and
community-sample evidence caution against treating high cognitive ability as a
general deficit or assuming that all high-ability young people encounter the
same peer difficulties (Lavrijsen and Verschueren, 2023; Tourreix et al.,
2023). At the same time, a substantial giftedness literature documents that
some young people manage how visible their ability, interests, or performance
is in social settings. The stigma-of-giftedness tradition describes conditional
concerns about being treated differently when exceptional ability becomes
known, while social-coping studies identify strategies including denial,
conformity, helping, selective disclosure, and changes in social interaction
(Coleman and Cross, 1988; Cross et al., 1993; Swiatek, 1995). These strategies
vary across settings, social groups, and developmental circumstances rather
than constituting a single trait.

We use *concealment* or lower-visibility behaviour as a bounded operational
term for the low-visibility end of that strategy family. It does not equate
privacy, strategic self-presentation, or temporary conformity with pathology,
and it does not import clinical meanings of masking. The substantive question
is narrower: how might a lower-visibility response remain learned when more
authentic expression would have greater value in the specified social
environment? This question concerns the temporal relation between action,
social feedback, and later action—not whether a person is inherently risk
averse or whether any observed concealment is maladaptive.

The available literature describes strategies and context dependence more
readily than it identifies the sequential process that sustains one strategy.
The same visible endpoint can arise because an environment remains unreceptive,
because early adverse feedback discourages further testing, because an
individual lacks a useful intermediate action, because a receptive setting is
hard to identify, or because the immediate and future values of a response
differ. Cross-sectional observations of low visibility cannot distinguish these
possibilities. They also cannot establish whether a response is objectively
advantageous under a defined environment.

### 1.2 Why observed masking is insufficient to establish objective optimality

Reinforcement learning provides a compact way to formalize this identification
problem. In hot-stove learning, an early negative sample from a variable action
can reduce subsequent sampling of that action; the resulting absence of
corrective evidence can preserve avoidance even without a fixed aversion to
risk (March, 1996; Denrell and March, 2001). This is established generic
learning theory, not a new explanation unique to giftedness. Its relevance here
is methodological: the outcome of a learner's choice changes the information
available for later learning.

Observed action, however, is not itself a value function. In a static
environment, an action may have lower estimated value because it has been
sampled unfavourably despite a greater expected environmental reward. In a
stateful environment, a seemingly costly action may improve later state and
therefore have higher dynamic value. In a heterogeneous environment, a good
option can exist while remaining difficult to identify and use. These are
different propositions. Conflating them turns either low masking or high
masking into an unsupported conclusion about adaptation.

This article therefore compares finite learned behaviour with an explicit
full-information benchmark in each environment. The benchmark is an oracle
relative to stated rewards and transitions; it is not a claim about human
welfare, moral desirability, or what a learner could know at the moment of
choice. The comparison allows the analysis to measure a learned–objective
divergence where one is defined, and to distinguish that divergence from an
environment in which lower visibility is itself the objective policy.

### 1.3 Contribution and model progression

The contribution is an existence-and-structure model cascade, not a calibrated
psychological model. M0 is a two-action risky-authenticity bandit that isolates
history-dependent sampling. M1 adds graded disclosure while preserving the
static endpoint geometry. M2 adds Accepted and Stigmatized social states, so
the relevant objective becomes a dynamic policy. M3 adds heterogeneous contexts
that must be discovered and, within that environment, a comparison-cost axis.
The sequence is logical rather than developmental, and no model step is mapped
to a fixed unit of human time.

Five frozen experiments instantiate this progression. E01 asks whether an
initial rejection changes later authentic sampling. E02 asks whether
independently learned disclosure levels change discovery of an objectively best
endpoint. E03 compares aggregate final-window action patterns with an exact
full-information dynamic policy in the persistent-state model. E04 asks whether
an objectively favourable context is equally discoverable across action
architectures. E05 compares the environmental comparison-cost crossover with a
learner's operational behavioural crossover. Figure 1 summarizes the formal
progression and the benchmark assigned to each rung.

The intended synthesis is deliberately bounded. Immediate reward, dynamic
value, discoverability, and a learned behavioural boundary are not
interchangeable. The experiments do not estimate the prevalence of masking,
establish an empirical causal mechanism in gifted populations, or evaluate an
educational intervention. Instead, they make several candidate explanations
for persistent lower visibility separable enough to state what evidence would
be needed to distinguish them empirically.

The comparison also establishes a reporting discipline. An analytic statement
can hold for every value in a formula's stated domain, whereas a simulated
contrast supports only the axes, learner settings, horizons, and estimands that
were executed. A full-information best action is not an instruction to a
learner without the oracle's information. Conversely, an end-of-episode learner
pattern is not evidence that the environmental payoff structure makes the same
action best. We use “objective” only in this conditional model-relative sense:
not as a moral recommendation, psychological welfare claim, or instruction to
reveal more than one judges safe.

This perspective makes a practical ambiguity explicit. A low-visibility action
can reflect current adaptation to an unreceptive setting, restricted learning
after earlier feedback, or difficulty identifying a favourable alternative.
These accounts require different empirical measurements despite producing a
similar observed endpoint. Explicit benchmarks cannot determine which account
describes a person, but they prevent a single behavioural observation from
being treated as if it had already done so.

## 2. Model framework and Methods

### 2.1 Modelling objective and common learner

We use a sequence of deliberately simplified reinforcement-learning
environments to ask when a finite learner can reduce authentic expression even
though a full-information benchmark favours it. The numerical parameters define
a normalized reference scale; they are not estimates of psychological utility,
social transition rates, or the prevalence of any response in gifted learners.
The models are therefore existence-and-structure analyses. They isolate
relations among feedback, representation, persistent social state, and context
discovery that can be evaluated exactly within their stated environments.

Three quantities are distinguished throughout. Environmental reward is the
payoff generated by an environment and defines the objective comparison.
Learned value is a finite learner's estimate based on selected experience. The
full-information benchmark is an oracle that knows the relevant payoff and,
for the stateful model, transition structure. It is not an information-matched
optimum, a welfare prescription, or a claim about what a person should do.

All learners start with action values of zero and use a constant learning rate
`alpha=0.1`, softmax temperature `tau=0.25`, and loss-neutral reward transform
`lambda=1`. A realized reward `R` is transformed only before the learning
update: `v_lambda(R)=R` for nonnegative outcomes and `lambda R` otherwise.
Thus, at the reported baseline, the learner update and environmental reward
coincide; loss aversion does not explain the headline results. For a selected
stateless action `x`,

\[
Q_{t+1}(x)=Q_t(x)+\alpha[v_\lambda(R_t)-Q_t(x)].
\]

At each step the learner samples available actions with a numerically stable
softmax,

\[
P(X_t=x)=\frac{\exp\{Q_t(x)/\tau\}}
{\sum_{x'}\exp\{Q_t(x')/\tau\}}.
\]

The row maximum is subtracted before exponentiation in implementation. The
finite horizon is an operational number of model steps, not a calendar unit.
Final-window summaries use the last 20% of a run; they describe end-of-episode
behaviour, not asymptotic convergence. Standard E01, E02, E04, and E05 runs
use `n=500` learners, `T=2000`, and five independent master seeds. E03 uses
`n=160` and `T=1000` per grid cell because its outcome is a fixed-grid
classifier. Student-t intervals across the five master estimates are reported
for applicable contrasts; E05 uses a master-curve bootstrap described below.

### 2.2 M0 and E01: adverse-history environment

M0 offers masking `M` and authenticity `A`. Masking has deterministic reward
`R_M=b-c`; authenticity is accepted with probability `p` and otherwise
rejected:

\[
R_A=\begin{cases}b+a,&\text{accepted},\\a-r,&\text{rejected}.\end{cases}
\qquad
\mathbb E[R_A]-R_M=a+c-(1-p)(b+r).
\]

With the common reference values `(b,a,c,r)=(1.0,0.6,0.25,2.0)`, masking
returns 0.75, authenticity has expectation `-1.4+3p`, and the static objective
boundary is `p=43/60`. E01 conditions on an initially accepted or rejected
authentic outcome in the tested `p=.75/.85` domain, then compares later
authentic sampling. It also evaluates two information-restoring model
manipulations within the rejected stratum: 5% forced authentic exploration and
counterfactual authentic feedback. The primary E01 estimand is later sampling;
the related normalized objective pseudo-regret is an action-count translation,
not an independent result.

### 2.3 M1 and E02: graded disclosure/endpoints

M1 replaces the two actions with independent tabular values for disclosure
levels `d` on a grid containing zero and one. Here `d=0` is the masking endpoint
and `d=1` is full authenticity. Acceptance is `1-(1-p)d`, yielding

\[
\mathbb E[R(d)]=b-c+d\{a+c-(1-p)(b+r)\}.
\]

Expected reward is therefore affine in disclosure. Except at exact
indifference, a strict static optimum is an endpoint; intermediate disclosure
is not made objectively optimal by the linear specification. E02 compares the
binary architecture with five independent disclosure arms after an initial
rejection, using matched random-number streams within master seed and
receptivity. It measures continued nonzero disclosure, final-window selection
of `d=1`, and whether `d=1` is the unique modal final-window arm.

### 2.4 M2 and E03: persistent social state and a dynamic comparator

M2 makes the environment stateful. The explicit states are Neutral, Accepted,
and Stigmatized. Authentic acceptance from Neutral moves to Accepted, whereas
rejection moves to Stigmatized; masking does not itself change state. Accepted
authenticity has reliable reward unless turnover returns the system to Neutral.
Stigmatized outcomes use the specified `b2`, `r2`, and reduced redemption
probability, with escape governed by `eta`. Reward is generated before the
next-state transition. The learner stores `Q(s,a)` and updates the selected
state-action pair with

\[
Q(s,a)\leftarrow Q(s,a)+\alpha\{v_\lambda(R)+\gamma\max_{a'}Q(s',a')-Q(s,a)\},
\]

where `gamma=.9`. The objective comparator is value iteration over the known
reward and transition model, not a static M0 threshold.

E03 spans a frozen 21-by-17 receptivity-by-escape grid. For each cell, the
reported classifier compares aggregate final-window Neutral-state action counts
with the full-information dynamic policy, subject to a prespecified Neutral
visit-adequacy rule. A cell is labelled learned–objective disagreement only
when aggregate Neutral counts favour masking and value iteration favours
authenticity. This is an action-level aggregate classifier; it is not an
individual policy label, an ordering of Q values, or an estimate of a human or
learner prevalence.

### 2.5 M3 and E04: heterogeneous-context discovery

M3 contains `K` contexts: one receptive context with probability `p_good` and
`K-1` unreceptive contexts with `p_bad`. In the reference design,
`p_good=.85`, `p_bad=.2`, and `bf=0` for E04. Masking has the common payoff
across contexts. Authenticity uses the context-specific acceptance probability;
comparison cost `bf` is subtracted only from accepted authenticity in the good
context. With one fixed good context, increasing `K` changes the multiplicity
of bad alternatives but not the distinct objective payoff classes or their
maximum. The full-information objective is consequently K-invariant.

E04 compares four representations: `flat_2k`, a single softmax over joint
context–behaviour arms; `hierarchical`, a context softmax followed by a
behaviour softmax with both value tables receiving the realized reward;
`global_mask`, one shared masking action plus context-specific authentic arms;
and `fixed_known_good`, a two-arm problem without context choice. The primary
outcome is the mean, across learners, of an indicator that the argmax of a
child's final-window action counts is an authentic action in a good context.
Ties are permitted by this defined argmax procedure. This is called
final-window argmax classification below; it is not convergence or a literal
model of human relocation between peer groups.

### 2.6 E05: objective and learned comparison-cost crossings

E05 holds `K=4` and one good context fixed while varying `bf`. At the reference
parameters, masking has expected reward `.75` and accepted good-context
authenticity has expected reward `1.15-.85bf`; their exact objective equality
is therefore `bf*=8/17=0.470588`. This is a static environmental boundary, not
a learned threshold. The reported learned response is the across-child fraction
whose final-window modal arm is the good-context authentic arm in the flat
eight-action architecture. Equal-weight nonincreasing pooled-adjacent-violators
(PAVA) fits are calculated on the dense `.30` to `.65` cost grid, and the
reported value is the fitted 0.5 crossing. Five complete master curves are
resampled for its 10,000-resample bootstrap interval. The monotonic fit is an
estimator constraint, not a proof that each learner or master curve is
monotonic. The hierarchical response is reported as left-censored when it is
already below .5 at the lower fitted boundary; no crossing is extrapolated.

Full equations, transition kernels, parameter tables, grid definitions,
stream construction, tie mechanics, sensitivity conditions, PAVA details, and
provenance records are routed to Supplementary Methods and repository
documentation.

All reported effect estimates preserve their experiment-specific inferential
unit. E01, E02, and E04 summarize five independent master-seed estimates rather
than treating individual learners as independent experiment replications. E03
preserves a fixed grid per master, and its stable-cell rule prevents inadequate
Neutral-state exposure from being silently classified. E05 resamples complete
master curves so uncertainty in the fitted crossing reflects run-level response
curves rather than merely the number of simulated children. These choices do
not convert a reference configuration into a population estimate; they make
the uncertainty statement match the preserved design.

## 3. Results

### 3.1 Early rejection reduced subsequent authentic sampling (E01)

E01 provides the minimal restricted-feedback result. Across the five master
seeds, learners assigned an initially rejected authentic outcome sampled
authenticity less often over subsequent steps than learners assigned an
initially accepted outcome (rejected minus accepted `-0.025837`, 95% CI
`[-0.035753,-0.015922]`; Figure 2A). In the stated M0 environment,
authenticity is objectively preferable at the tested receptivities. The result
therefore documents a finite learning-history difference in sampling, not a
change in the environmental payoff comparison.

The normalized objective pseudo-regret contrast was `+0.025824`
`[+0.015914,+0.035735]`, but it is not a second corroborating outcome. In this
design it is exactly linked to the sampling contrast,
`Delta R_norm=-(1999/2000)Delta A`; it restates the same action-history
difference in objective-loss units. Importantly, the final-window masking
contrast was `-0.000343` (`[-0.011605,+0.010918]`). Thus the experiment did
not detect an increase in final-window masking after a single initial
rejection; the interval crossing zero is not evidence of equivalence.

The two model information manipulations were directionally consistent with the
sampling account. Within the rejection stratum, 5% forced authentic exploration
reduced final-window masking by `0.046590` (`[0.033230,0.059951]`), and
counterfactual authentic feedback reduced it by `0.118135`
(`[0.109683,0.126587]`). These are manipulations of the model's information
channel, not estimates of human intervention effects. E01 is consequently a
supporting hot-stove demonstration: early adverse feedback can reduce later
sampling and delay correction, without establishing a persistent final-mask
effect in the tested conditions.

### 3.2 Independent graded actions reduced optimal-endpoint discovery (E02)

E02 asks what changes when the visibility continuum is represented as five
independently learned actions rather than binary endpoints. Following initial
rejection, the graded architecture increased continued nonzero disclosure by
`0.255040` (95% CI `[0.253004,0.257077]`) relative to binary resampling of
full authenticity (Figure 2B). This is an exposure-distribution result: more
learners continued some nonzero disclosure. It does not show that an
intermediate level was objectively preferable.

The same graded representation reduced full-authentic final-window selection by
`0.328692` (`[-0.342037,-0.315348]`) and reduced the probability that the
objectively optimal endpoint was the unique modal final-window arm by `0.221740`
(`[-0.288755,-0.154724]`; Figure 2C). The analytic comparison is decisive for
interpretation. Because M1 expected reward is affine in `d`, full authenticity
is the strict objective endpoint whenever the corresponding binary environment
favours it; intermediate actions are not an unmodelled compromise optimum.

The graded arms instead change how finite experience is allocated. An outcome
at one disclosure level does not update neighbouring levels, so partial actions
can receive experience while the full-authentic endpoint remains relatively
under-sampled. E02 therefore complements E01 rather than replicating it.
E01 changes the history of information about one risky action; E02 changes the
action representation through which information is acquired. The normalized
regret statistic is disclosure distance `1-d` in authenticity-optimal cells and
is not treated as a second welfare result. The result is representation
conditional: it does not establish a disclosure-specific psychological
mechanism or predict the same behaviour for a learner that generalizes across
ordered disclosure levels.

### 3.3 Aggregate learned Neutral actions disagreed with the dynamic optimum (E03)

E03 introduces a different question: when authentic action changes future
social state, what should count as the relevant objective comparison? The
answer is not the static M0 reward threshold. In M2, authentic acceptance can
move the environment into an Accepted state with reliable authentic reward,
whereas rejection can move it into a Stigmatized state; the value of a Neutral
choice consequently includes future rewards and transitions. Figure 3 compares
finite learner behaviour with the exact full-information discounted MDP policy
computed by value iteration under the same rewards and transition equations.
The comparison is an oracle benchmark: it knows environmental contingencies
that the learner must sample to estimate.

At `n=160` learners and `T=1000` steps per cell, the frozen 21-by-17
receptivity-by-escape grid produced 243 of 357 cells in which aggregate
final-window Neutral-state action counts favoured masking while the
full-information dynamic policy selected authenticity. The fraction,
`243/357=0.680672`, was identical across the five master seeds. It is a count
of cells satisfying a jointly defined classification, not a frequency of
individual learners. Specifically, a cell enters the count only when the
aggregate Neutral final-window action count favours masking, value iteration
favours authenticity, and the maintained visit-adequacy criterion is met.

The classifier was stable in 350 of 357 cells under the prespecified four-of-
five-master rule. Seven low-receptivity, `eta=0` cells were inconclusive because
Neutral visits did not meet the adequacy criterion. They were not forced into a
masking or authenticity category. The map should therefore be read as a
tested-grid summary of this learner, horizon, classifier, and M2 environment.
It is not human prevalence, learner prevalence, a natural phase-space volume,
or a Q-value classifier. Nor does it establish that the learner failed relative
to an information-matched optimum; it shows a divergence from a known-model,
full-information dynamic policy.

For a general reader, the central contrast is between an action's immediate
outcome and its role in changing future opportunity. In Neutral, masking can
provide a predictable immediate payoff, while authentic action can have a
negative immediate realization but also a chance to create an Accepted state
with later benefit. Value iteration incorporates that future branch directly.
A finite Q learner must encounter, remember, and propagate those contingent
outcomes through its state-action values while its own earlier choices affect
which states it revisits. The result does not identify which component—finite
sampling, state visitation, constant-step learning, or the oracle information
advantage—accounts for a given cell. It establishes the disagreement under the
specified joint design.

The frozen sensitivity results delimit rather than generalize the map. Dynamic
objective thresholds varied with the escape parameter, and selected changes to
`gamma`, `alpha`, or `tau` reclassified named sentinel cells. At `gamma=.5`,
some reclassifications reflected a change in the objective policy itself, not
better learner performance. No learned Neutral transition threshold was
estimated from the preserved data. A separately labelled harsh boundary
demonstrates that masking can be dynamically objective in a different M2
configuration; it does not turn the reference-grid result into a universal
structural-lock-in region. E03's supported conclusion is consequently narrow
but important: in a persistent-state environment, observed end-of-run action
counts can differ from the relevant dynamic objective benchmark.

The distinction is easiest to see by asking what a final-window Neutral count
does and does not summarize. It reports which action was more frequent during
the observed tail of the finite episode among those moments classified as
Neutral. It does not report the probability that every learner uses masking,
the action chosen in Accepted or Stigmatized states, the value of an
unobserved policy, or the amount of discounted loss relative to the oracle.
The visit criterion matters for the same reason: a cell with too little Neutral
exposure cannot support a reliable statement about its Neutral action pattern.
Keeping this classifier explicit makes the map interpretable without turning a
useful model comparison into a stronger population claim.

The M2 result also supplies a caution for the surrounding literature. A
longitudinal observation that an adolescent becomes less visibly authentic after
a negative response could reflect changing beliefs in a fixed environment,
changing opportunities caused by social state, or a combination. The present
model cannot identify those processes in people, but it shows that they imply
different formal benchmarks. A study designed to discriminate them would need
repeated actions, responses, state-relevant contextual measures, and a clear
account of what information was available at each decision.

### 3.4 A favourable context was not equally discoverable across representations (E04)

E04 asks whether objective availability of a receptive context is sufficient
for a finite learner to use authentic behaviour there. The one-good-context M3
environment supplies an exact baseline: increasing `K` creates additional bad
contexts but leaves the distinct payoff classes and the full-information best
expected reward unchanged. Any `K` response therefore cannot be attributed to
a reduced maximum objective opportunity. The empirical question is whether a
finite learner identifies and repeatedly selects authentic action in the good
context under the representation through which it learns.

The primary outcome is final-window argmax classification as authentic in a
good context: for each learner, final-window action counts are compared by
argmax, and the indicator is one when the resulting action is authentic in a
receptive context. It is neither an asymptotic convergence statement nor a
claim that a person has permanently chosen a social group. In the flat `2K`
architecture, increasing the number of contexts from one to 16 changed this
outcome by `-0.2340` (95% CI `[-0.246417,-0.221583]`; Figure 4A). Under the
hierarchical architecture, in which context and behaviour are represented in
separate but jointly rewarded tables, the corresponding contrast was `-0.4704`
(`[-0.511031,-0.429769]`). These are architecture-specific estimates; the
larger hierarchical decline must not be read as a general ranking of learning
architectures.

The control set constrains the interpretation. In `fixed_known_good`, there is
no context choice and the structural K effect is exactly zero. In `global_mask`,
one masking action is shared across contexts while authentic actions remain
context-specific; its K contrast was `+0.0088` (`[0.002090,0.015510]`),
statistically distinguishable from zero but practically near zero under the
prespecified band. These controls show that the result is not simply a change
in the objective maximum and is sensitive to how joint actions are represented.
They do not isolate a single duplicate-mask or normalization mechanism because
global masking also changes cardinality, initial mass, competition, and reward
allocation.

Randomising the good-context identity did not materially change the K decline:
the random-minus-fixed slope contrasts were `-0.00292`
(`[-0.012269,0.006429]`) for flat and `+0.00140`
(`[-0.012620,0.015420]`) for hierarchical learning. Adding receptive contexts
weakened the decline: with two good contexts the change relative to one good
was `+0.05064` for flat and `+0.02524` for hierarchical; in the tested
proportional-25% design the corresponding changes were `+0.06044` and
`+0.11224`. Together, these results support a bounded conjunction:
representation-dependent finite discovery burden is most evident in the
tested scarce-receptivity design. The one-good-context manipulation alone
confounds increasing K with reducing the good fraction to `1/K`, so it does not
separately establish a causal effect of “more contexts” or scarcity alone.

E04 thus separates two propositions that can otherwise be conflated. A good
authentic option may remain objectively available under full information while
its discovery and final-window use by a finite learner vary with the action
architecture and distribution of receptive contexts. The model does not
represent literal student movement between classrooms, friendship groups, or
educational placements. Its contribution is the more limited formal claim that
the structure of alternatives and their discoverability can matter even when a
favourable option remains in the environment.

The contrast between the four architectures is informative precisely because it
changes the learner's representation while holding the frozen environmental
payoffs fixed. `flat_2k` requires a learner to acquire a value for each joint
context-behaviour arm. `hierarchical` separates context and behavioural
selection but updates both selected representations from the same outcome.
`global_mask` makes the low-visibility option share evidence across contexts,
and `fixed_known_good` removes context identification entirely. None is
claimed to be a literal cognitive architecture. Together they instead show
that the apparent K effect is not a consequence of the objective maximum
falling with K, and that it cannot be reduced to the number of arms alone.
The observed patterns remain conditional on the specified learner and scarce
receptivity configurations.

### 3.5 Learned and objective comparison-cost boundaries separated (E05)

E05 varies a comparison cost within M3 to compare an exact environmental
boundary with an operational behavioural boundary. At the reference payoffs,
masking returns `.75`, while accepted authenticity in the good context returns
`1.15-.85bf`. The full-information objective crossover is therefore exactly
`bf*=8/17=0.470588` (Figure 4B): below that value, good-context authenticity
has the higher expected reward; above it, masking does. This is a property of
the stipulated payoff equation, not an estimate of learner preference or a
human comparison-cost threshold.

The learned quantity is different. In the flat eight-action (`K=4`) model, we
calculated for each cost the across-child fraction whose final-window modal arm
was the good-context authentic action. We pooled the five master curves and
used a nonincreasing PAVA fit over the dense `.30`–`.65` range. The fitted
response crossed .5 at `bf=0.312852`, with a 10,000-resample master-curve
bootstrap interval `[0.307836,0.316918]`. Thus the reported .5 crossing occurs
well before the objective indifference point. At the learned point crossing,
good-context authenticity still retained an objective advantage of about
`0.134076`; the transformed bounds inherited from the crossing were about
`[0.130620,0.138340]`.

This contrast should not be collapsed into a familiar two-action softmax
statement. The response is an across-child final-window modal-classification
fraction, not a per-trial softmax probability, a direct policy probability, or
a binary Q-value equality. The PAVA constraint summarises the observed
population response; it does not prove monotonicity of individual histories or
identify the mechanism of the shift. The objective line was a tested analytic
anchor, not a target provided to the fitting procedure.

The hierarchical response was already below .5 at the lower dense-boundary
value `bf=.30`: its isotonic response there was `.1176`, and none of 10,000
bootstrap resamples yielded an in-range crossing. Its crossing is therefore
left-censored below the resolved range, not absent globally and not comparable
as a point estimate with the flat crossing. The endpoint contrast from `bf=0`
to `.80` provides supportive context but does not replace the dense transition
estimator.

E05 establishes a learned–objective crossover displacement in this learner and
reference configuration. It does not apportion that displacement among
temperature, multi-action normalization, finite sampling, endogenous
under-sampling, context discovery, constant-step learning, or representation.
Those factors remain possible contributors, and the frozen evidence does not
identify their quantitative shares. The result is consequently neither a
universal behavioural threshold nor a calibrated claim about social comparison
in gifted populations.

## 4. Cross-experiment synthesis and Discussion

### 4.1 History, information, and action representation

The five experiments distinguish several reasons why an observed low-visibility
action can persist without establishing that it is the best environmental
choice. E01 is the minimal information-history case. A rejected authentic
outcome lowers subsequent sampling of the action that could correct the
estimate, a familiar hot-stove pattern in which choice alters later evidence
(March, 1996; Denrell and March, 2001). Its information-restoring manipulations
show that changing the model's evidence channel can improve correction. Yet E01
does not demonstrate a stable final-window masking difference. Its value in
the article is therefore foundational: it separates a trajectory-level
learning consequence from a claim about a persistent behavioural endpoint.

E02 provides a complementary, rather than confirmatory, manipulation. It
leaves the static endpoint logic intact but expands the learner's independent
action representation. More nonzero disclosure after rejection coexists with
less discovery and use of the full-authentic endpoint. The two results should
not be translated into a mechanism-independent recommendation to increase or
decrease access to authenticity-related actions. E01 restores missing
information about an existing risky alternative; E02 divides finite evidence
across several actions that do not generalize to one another. Their shared
lesson is that behaviour can change through information acquisition and action
representation even while the objective comparison remains fixed. Their
different designs are a cross-mechanism dissociation, not statistically
independent replications of the same treatment effect.

### 4.2 Immediate and dynamic value

M2 changes the mathematical object to be evaluated. The M0 and M1 comparisons
are static expected rewards; M2 requires a policy that values state-dependent
future consequences. Consequently, describing masking as “suboptimal” in E03
is meaningful only relative to the stated full-information dynamic-programming
oracle. The `243/357` map does not say that a corresponding share of learners
or people masks irrationally. It demonstrates that, under a precisely
specified classifier and tested region, aggregate end-of-run Neutral choices
can favour masking where the known-model dynamic policy favours authenticity.

This distinction matters substantively. The same immediately safer choice can
be adaptive in an environment with persistent adverse consequences and
non-optimal in one where authentic success opens valuable future states.
Indeed, the harsh M2 sentinel preserved in the supplement shows that masking
can be dynamically objective in another parameter configuration. The model
therefore resists both symmetric overinterpretations: a high observed masking
rate does not itself establish maladaptive avoidance, but a more favourable
immediate authentic payoff does not settle a dynamic question either. Empirical
work inspired by this distinction would need repeated information about action,
response, later context, and persistence—not only a cross-sectional measure of
concealment.

### 4.3 Availability and discoverability

E04 extends the identification problem from time to alternatives. The
full-information objective is K-invariant in the one-good-context design, but
finite learners' final-window argmax classifications change as the context
structure and representation change. This is not evidence that real students
literally search a menu of peer groups or that one learning architecture is a
psychological process. It is a formal demonstration that the structure of
available alternatives and the cost of discovering them can matter separately
from whether a favourable alternative exists.

This abstraction is relevant to giftedness because social coping and visibility
management are documented as context-sensitive rather than uniform (Coleman
and Cross, 1988; Cross et al., 1993; Swiatek, 1995). The model suggests a
testable hypothesis: when social receptivity is uneven and information about
contexts is local, opportunities for authentic expression may be harder to
identify or use than their objective availability alone would imply. It does
not identify a literal search mechanism, a school-placement intervention, or a
causal pathway in any gifted population. The E04 controls further caution
against a single-factor story: its supported result is representation-dependent
finite discovery burden under scarce receptivity in the tested environments.

### 4.4 Behavioural and objective boundaries

E05 makes the distinction between environment and learned response visible at a
single reference configuration. The objective `8/17` line is a payoff
indifference result. The earlier flat learned crossing is an estimator-defined
summary of across-child end-of-run modal classifications. Their difference
shows that a finite learner's behavioural transition need not occur where a
fully informed environment changes its optimal action. That is the article's
most direct boundary-displacement result.

The difference should not be made cleaner than the evidence permits. Because
the response is multi-action and population-level, the binary-softmax
half-probability identity cannot attribute or exclude a temperature effect.
Neither the existing curves nor the analytic result quantify contributions
from exploration, action competition, representation, finite horizon, or
learning rate. The hierarchical result is left-censored, adding an explicit
reason not to generalize a single flat crossing across architectures. E05
therefore supports a configuration-specific learned–objective displacement,
not a causal decomposition or a human threshold.

### 4.5 Implications for ability visibility

Taken together, the models provide a bounded mechanism-level hypothesis for
understanding persistent concealment-like strategies in high-capability
individuals. A low-visibility response can be learned even when an alternative
has greater objective value within a stipulated environment, because early
history can restrict information, an action representation can dilute endpoint
learning, current choice can have dynamic consequences, receptive alternatives
can be difficult to discover, and an operational behavioural boundary can
differ from environmental indifference. This proposition concerns the
constructed environments, not a diagnosis, prevalence estimate, or claim that
gifted people instantiate the models literally.

The giftedness literature supplies the substantive motivation and the necessary
restraint. Some gifted young people report managing the visibility of ability,
conformity, or disclosure across social settings, but giftedness does not imply
a uniform social-emotional profile or a universal need to conceal (Cross et al.,
2014; Cross et al., 2019; Tourreix et al., 2023). The appropriate empirical
next step is to measure sequences of visible action, perceived and observed
response, later sampling of related actions, and changing opportunities across
contexts. Such data could distinguish current adaptation to an adverse
environment from restricted information, dynamic consequences, or discovery
constraints—mechanisms that look similar in a single end-point observation.

## 5. Limitations

Several limitations are integral to the interpretation. First, the models are
stylized and use a normalized reference payoff scale. Their parameters are not
calibrated estimates of the social value of authenticity, the cost of
concealment, the probability of acceptance, comparison costs, or psychological
time. The model actions are constructs for analysing visibility management, not
direct measures of behaviour, identity, privacy, or clinical masking.
Accordingly, the results do not estimate prevalence in gifted populations,
diagnose individuals, or establish educational intervention effects.

Second, the full-information static and dynamic benchmarks are oracles. They
provide a clear reference for the specified environments, but they are not
information-matched optima that a finite learner could necessarily attain.
Learner–oracle differences are not decomposed into separately identified
contributions from observation, exploration, state uncertainty, finite horizon,
or update efficiency. The learner family is also narrow: tabular values,
constant learning rate, fixed-temperature softmax choice, and the stated action
representations. E02 in particular is conditional on independent disclosure
arms and does not establish what a learner with structured generalization would
do.

Third, simulation claims are conditional on executed grids, horizons, and
inferential units. E03's `243/357` result is tested-grid coverage under a
specific aggregate classifier, not a prevalence estimate or a full parameter
characterization. E04's K response depends on scarce receptivity and action
architecture. E05's crossing is based on five master curves and an
estimator-defined PAVA response; its mechanism decomposition is unresolved,
and its hierarchical transition is left-censored below the fitted range. A
model limitation is allowed to remain a limitation rather than being repaired
by unexecuted sensitivity analyses.

Finally, the frozen result artifacts are preserved and hash-validated, but the
exact historical generator-source worktree for E01–E03 was not fully recovered
from Git alone. E04 and E05 have fingerprint-exact archived generator bundles.
This provenance limitation constrains exact historical source reconstruction;
it does not authorize replacement runs or change the scope of the frozen
evidence.

## 6. Conclusion

This model cascade separates learned behaviour from the relevant objective
benchmark rather than treating observed concealment as evidence that
concealment is objectively preferable. Across the E01–E05 progression, early
adverse feedback altered later sampling, independent graded actions altered
endpoint discovery, persistent state changed the relevant dynamic optimum,
context structure changed discoverability, and an operational learned boundary
preceded environmental indifference. The central lesson is therefore
structural: immediate value, dynamic value, discoverability, and a learned
behavioural boundary are distinct quantities.

The article does not claim a calibrated account of gifted students or a
universal mechanism of masking. Instead, it offers explicit environments and
comparators that generate testable hypotheses about how visibility-management
strategies may persist. Empirical work can build on this distinction by
observing behaviour, social feedback, subsequent sampling, and contextual
opportunities over time, while retaining the possibility that lower visibility
is sometimes a current adaptation rather than a learning error.
