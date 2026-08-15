# Article V1 Literature Audit

**Canonical hand-off reference — revised 15 August 2026**

**Authority status:** Article-V1 literature authority for hand-off, corrected 15 August 2026 after the model-analysis consistency audit. This file is derived from the reviewed literature-audit reference document produced on 14 August 2026. It records the adjudicated scientific state; raw AI2 Asta dossiers are provenance inputs, not authorities.

**Use:** Read this document to determine what prior literature establishes, which mechanisms are generic background, how the giftedness constructs are grounded, what terminology is defensible, and which novelty-critical questions remain open. Do not treat it as manuscript prose.

---

# Executive summary

**The literature search has materially changed the scientific
position.** The weak contribution thesis—roughly, that a reinforcement
learner can come to conceal/mask even when a more authentic action has
higher objective value—does not survive the generic learning-theory
audit. Endogenous sampling, hot-stove effects, self-confirming
incomplete learning, finite-horizon softmax path dependence, and the
benefits of richer feedback are all established mechanisms. The paper
therefore cannot claim novelty from basic under-exploration or from
showing that forced sampling/counterfactual feedback improves learning.

**At the same time, the giftedness application is better grounded than
initially feared.** There is direct empirical evidence that some gifted
children and adolescents manage information about their abilities,
conceal or minimize giftedness, conform to peers, and alter visible
intellectual behavior for social reasons. The Coleman/Cross
stigma-of-giftedness tradition and Swiatek social-coping programme
provide a genuine gifted-specific empirical base. The most defensible
conceptual hierarchy is broader social coping, within which
information/visibility management and concealment form one strategy
family.

**The novelty question has therefore moved from “does gifted concealment
exist?” to “does the formal environmental structure add something beyond
generic RL?”** The two most important unresolved literature questions
are now (i) persistent social-state dynamics—disclosure/concealment that
changes later acceptance, stigma, reputation, or social state—and (ii)
costly search among heterogeneous contexts when receptive contexts are
scarce and initially unknown. These are the searches most likely to
determine whether the persistent-state and receptive-context experiments
carry the main scientific contribution.

**The evidence also imposes several hard interpretive constraints.** A
full-information optimum is a legitimate oracle benchmark but does not
by itself identify an attainable information-constrained optimum. For an
exactly two-action softmax probability, fixed temperature changes the
steepness of the curve but not the Q-equality location of its 50% point.
That theorem does **not** apply directly to E05's eight-action,
across-child modal-arm statistic and therefore does not rule out
temperature/action-set normalization as contributors there. Treating graded
disclosure levels as unrelated tabular actions is a substantive
representation assumption because structured-bandit methods can share
information across related actions. BFLPE/social-comparison literature
motivates comparison costs but does not calibrate the model cost
parameter as a human BFLPE measure or establish behavioral retreat at
the model threshold.

| **Literature area**                       | **Current status**                    | **What is established**                                                                                                                                         | **Consequence for the paper**                                                                                             |
|-------------------------------------------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Incomplete learning / endogenous sampling | CLOSED for generic mechanism          | Choice-dependent observation can sustain wrong off-path beliefs; early adverse outcomes can suppress future sampling.                                           | E01 basic mechanism is background/supporting demonstration, not mechanism novelty.                                        |
| Counterfactual / full feedback            | CLOSED for generic mechanism          | Richer feedback breaks the avoidance→ignorance loop and improves identification in many settings.                                                               | Information-restoration effects should not be sold as a novel solution.                                                   |
| Softmax / finite-horizon RL               | CLOSED for main learner objection     | Finite-horizon path dependence and under-sampling are expected; Boltzmann exploration has known tuning and regret limitations.                                  | Avoid “trap/lock-in” language unless stronger evidence is separately established.                                         |
| Graded action representation              | MOSTLY RESOLVED                       | Independent arms waste information when actions have ordinal/metric structure; structured bandits can generalize.                                               | E02 has a strong representation-based alternative explanation; disclosure-specific novelty remains to be searched.        |
| Gifted concealment / social coping        | SUBSTANTIALLY RESOLVED                | Intentional visibility management/concealment is directly documented in some gifted youth; social coping is measurable.                                         | Giftedness remains a credible empirical application, but prevalence and persistence must not be inferred.                 |
| Peer/context dependence                   | SUPPORTED, not dynamically calibrated | Visibility, conformity and social coping vary by peer/school context; gifted-group settings can both reduce concealment pressure and raise comparison pressure. | Context-sensitive rewards/states are empirically motivated, but transition probabilities and persistence are theoretical. |
| Active search for receptive contexts      | WEAK–MODERATE empirical grounding     | Preference for similar/intellectual peers and some environment-changing behavior are documented; systematic sequential search is not.                           | E04’s sequential search mechanism remains a theoretical abstraction pending formal prior-art search.                      |
| BFLPE / comparison costs                  | CLOSED as background motivation       | High-achievement reference groups can lower academic self-concept and affect emotions/motivation.                                                               | Supports a comparison-cost ingredient, not a calibrated model parameter or behavioral retreat claim.                      |
| Persistent-state formal prior art         | OPEN — HIGHEST PRIORITY               | Current searches do not adjudicate dynamic concealment with persistent endogenous social consequences.                                                          | This search can materially change E03’s novelty class.                                                                    |
| Scarce receptive-context formal prior art | OPEN — HIGH PRIORITY                  | Current literature does not establish whether scarce unknown receptive contexts are already a standard formal mechanism.                                        | This search can materially change E04’s novelty class.                                                                    |

# 1. Scope, provenance, and evidential discipline

The current evidence base combines several kinds of material:

- AI2 Asta literature dossiers covering social learning/peer norms,
  BFLPE/social comparison, self-confirming learning, counterfactual
  feedback, hot-stove effects, softmax/Boltzmann exploration,
  finite-horizon Q-learning, structured action spaces, gifted
  concealment, stigma/social coping, context dependence, and peer
  preference.

- Targeted primary-source verification for the Coleman/Cross and Swiatek
  research traditions using publisher records.

- An adversarial generic-RL synthesis generated by Asta, which was
  useful as a challenge but was judged to overstate several conclusions
  and is therefore not treated as authoritative.

- The computational project’s current experimental architecture
  (E01–E05), used only to determine which literature results matter for
  claim boundaries; the present document does not re-adjudicate
  simulation evidence.

**Important source-quality caveat.** Several Asta dossiers mix direct
paper excerpts with secondary summaries and model-generated connective
text. Older gifted-literature dossiers also produced bibliographic
errors before primary verification. Consequently, this document
distinguishes “literature finding” from “verified primary record.” A
claim can be scientifically plausible yet still need primary
bibliographic verification before manuscript citation.

| **Terminology used in this audit:** “Directly grounded” means the literature directly reports or measures the relevant human construct. “Plausible mapping” means the model variable has a reasonable empirical analogue but the exact state/action/dynamic is not directly measured. “Indirect only” means the literature supports surrounding phenomena but not the modeled construct itself. These are construct-validity labels, not novelty labels. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 2. Generic incomplete learning and endogenous sampling

## 2.1 Self-confirming learning is established prior art

**Core result.** Self-confirming equilibrium and related
incomplete-learning work establish that agents can hold beliefs that are
correct on the realized path while remaining wrong about unobserved
contingencies. When action choice determines which evidence is
generated, false beliefs about unchosen actions can survive indefinitely
because experience never contradicts them. The Fudenberg–Levine
tradition therefore supplies a direct theoretical antecedent for the
generic logic “behavior determines evidence; missing evidence permits
stable off-path error.”

**Implication.** The mere existence of a learner whose own choices
restrict its future information is not novel. Likewise, a learned policy
differing from a full-information policy is not by itself evidence of a
special social mechanism. The substantive question must be whether the
social-state or context-search structure changes the phenomenon in a
scientifically meaningful way.

Current source basis: Self-Confirming Equilibrium, Learning, and
Observational Equivalence under Incomplete Information; McLennan/SCE
dossier; Fudenberg & Levine (1993) as the load-bearing primary
reference.

## 2.2 Hot-stove / sampling-asymmetry effects

**Core result.** The hot-stove literature describes the same qualitative
loop as the basic adverse-feedback result: an early bad outcome lowers
an option’s perceived value, reduced choice leads to reduced sampling,
and reduced sampling limits corrective evidence. The mechanism does not
require intrinsic loss aversion; ordinary adaptive sampling can generate
the asymmetry, while asymmetric loss/gain updating may amplify it in
some tasks.

**What is safely established.** Early adverse experience can produce
prolonged finite-horizon avoidance or under-sampling. It is safer to
describe this as sampling suppression, path dependence, or a hot-stove
effect than as irreversible lock-in. Fixed positive softmax typically
leaves the option with non-zero probability; the empirical issue is that
the probability may become too small to produce meaningful corrective
sampling within the available horizon.

**What is not established by this literature.** The generic hot-stove
result does not establish that one social rejection causes durable human
masking, that a specific developmental trajectory becomes irreversible,
or that the project’s exact effect magnitude is expected under all
learners.

## 2.3 Counterfactual and full feedback

**Core result.** Bandit feedback reveals the outcome of the chosen
action while leaving forgone outcomes unobserved. Full or counterfactual
feedback changes the problem by allowing learning about avoided
alternatives without sampling them. The literature therefore directly
predicts that richer feedback can reduce self-reinforcing sampling
errors.

**Novelty consequence.** A result showing that forced sampling or
counterfactual information improves learning should be treated as a
control or mechanism check, not as a new general solution. It may still
be useful scientifically because it diagnoses an information-acquisition
mechanism in the project’s environment, but the remedy itself is
established prior art.

# 3. Softmax/Boltzmann Q-learning and finite-horizon path dependence

## 3.1 Known limitations of Boltzmann exploration

The softmax/Boltzmann literature yields several constraints on
interpretation:

- Standard Q-learning convergence results are asymptotic and depend on
  adequate visitation of state–action pairs and appropriate
  learning-rate conditions. They do not guarantee recovery within a
  finite simulation horizon.

- Boltzmann exploration is sensitive to temperature schedules and reward
  scale. Naive schedules can over-explore inferior actions or commit too
  early to a suboptimal arm. Cesa-Bianchi et al. (2017) is particularly
  important because it formalizes shortcomings of ordinary Boltzmann
  exploration rather than treating softmax as automatically well
  behaved.

- A fixed positive temperature can keep actions technically possible
  while still making some action probabilities negligibly small in
  finite time. Positive probability is therefore not equivalent to
  adequate information acquisition.

- Softmax is value-directed rather than uncertainty-directed. It does
  not automatically target the least-known action, which is relevant
  when the scientific claim is about information acquisition rather than
  reward exploitation.

**Interpretive consequence.** The project should present the maintained
learner as a deliberately simple learner whose finite-horizon behavior
is part of the experimental object. It should not imply that the
observed failure mode would persist under all competent learners,
UCB-like uncertainty-aware exploration, Thompson sampling, model-based
planning, or structured generalization.

## 3.2 Fixed temperature and the 50% crossover

For a plain two-action softmax policy,**P(A) = exp(Q_A/τ) /
\[exp(Q_A/τ) + exp(Q_B/τ)\]**

and therefore**P(A) = 0.5 ⇔ Q_A = Q_B.**

**Key conclusion.** Changing a common fixed temperature changes the
steepness/sensitivity of an **exactly binary softmax probability** but not
the Q-equality location of that binary 50% point.

**E05 correction.** The frozen E05 statistic is not a binary softmax
probability. In flat `K=4` it is the across-child fraction whose
final-window modal arm is the single good-context authentic arm among
eight actions. The binary theorem therefore cannot be used to conclude
that temperature is irrelevant to the observed E05 crossing. Fixed
temperature, action-set normalization, endogenous sampling, learned
Q-value distributions, and their interactions remain possible
contributors unless separately decomposed.

**Multi-action caveat.** With three or more actions, one action’s
probability is normalized against the entire action set. A 50% choice
point therefore no longer has the same pairwise interpretation as in the
binary case.

## 3.3 Full-information versus information-constrained benchmarks

**The full-information optimum remains a legitimate oracle comparator.**
It answers what an agent would do if it knew the relevant
reward/transition structure. However, a gap between a learned policy and
that oracle does not by itself show that the learner failed to find a
policy it could reasonably have learned under the actual information
stream.

Conceptually, the total gap can be decomposed as:**V(π\*F) − V(πL) =
\[V(π\*F) − V(π\*I)\] + \[V(π\*I) − V(πL)\]**

*where π\*F is the full-information optimum, π\*I the best
information-constrained policy, and πL the learned policy.* The project
currently has the first and third objects in some experiments but not an
information-matched optimum. For E03 specifically, the publication-facing classifier is aggregate
final-window Neutral-state behavior rather than an individual Q-order
policy. Therefore the safe statement is “aggregate final-window
Neutral-state behavior favored masking while the full-information
dynamic optimum favored authenticity,” not “the learner failed to
discover an attainable better policy.”

| **Correction to the adversarial Asta synthesis:** The Asta synthesis called the full-information benchmark “invalid.” That is too strong. It is valid as an oracle/upper-bound comparator; what is invalid is interpreting the entire gap as learner inefficiency without separating the information gap. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 4. Graded actions and action-space representation

**The structured-bandit literature creates a serious alternative
explanation for any graded-disclosure result.** A tabular learner treats
each disclosure level as an independent arm. If the actions are actually
ordered or metrically related, this representation throws away
structure: observing the outcome of one level provides no direct update
to nearby levels. Lipschitz, linear, Gaussian-process, continuum-armed,
and other structured-bandit approaches exist specifically to exploit
such relationships.

The current literature therefore supports four conclusions:

- Increasing the number of independent actions generally increases the
  amount of information required to identify the best action at a fixed
  sample budget.

- The exact difficulty increase is not simply “K times harder”; it
  depends on reward gaps, noise, horizon, algorithm, and structure. The
  earlier Asta claim that moving from two to five arms makes the problem
  exactly 2.5× harder should be rejected.

- If disclosure levels are semantically ordered, treating them as
  independent actions is a substantive modeling assumption rather than a
  neutral implementation detail.

- A result in which intermediate actions remain sampled while the best
  endpoint is selected less often can therefore arise from
  independent-arm representation and finite-sample dilution without any
  disclosure-specific psychology.

**What remains scientifically open.** The generic representation
objection does not fully adjudicate whether graded or partial disclosure
has a domain-specific theoretical literature, or whether the particular
conjunction “more continued nonzero disclosure, less full-endpoint
selection, no welfare improvement” is already known in
disclosure/revelation models. That requires the remaining
graded/partial-disclosure prior-art search.

# 5. Gifted-specific empirical literature: concealment and social coping

## 5.1 The existence of deliberate concealment is now supported

**The central construct-validity question is no longer whether gifted
concealment exists at all.** The retrieved literature contains direct
reports of gifted children/adolescents hiding or minimizing abilities,
conforming to peers, managing information about giftedness, withholding
visible signs of achievement, or otherwise trying to appear less
different in order to preserve ordinary social interaction or peer
acceptance.

**The strongest currently usable evidence comes from two connected
traditions.** First, Coleman and Cross’s stigma-of-giftedness work
directly describes gifted adolescents managing information about
themselves to minimize their visibility as gifted students. Second, the
Swiatek social-coping programme operationalizes gifted-specific coping
dimensions and shows that denial, conformity/popularity management, peer
acceptance, and related strategies are measurable rather than merely
anecdotal.

| **Primary-source correction: Coleman & Cross:** The verified 1988 article is Laurence J. Coleman & Tracy L. Cross, “Is Being Gifted a Social Handicap?”, Journal for the Education of the Gifted, 11(4), 41–56, DOI 10.1177/016235328801100406. It interviewed 15 gifted/talented adolescents twice in a summer programme. The abstract reports that many, but not all, experienced giftedness as a social handicap and that some managed information about themselves to minimize visibility as gifted students. Earlier Asta reconstruction that treated this as a book chapter was incorrect. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| **Primary-source extension: Cross, Coleman & Terhaar-Yonkers:** The 1991 study “The Social Cognition of Gifted Adolescents in Schools: Managing the Stigma of Giftedness” (Journal for the Education of the Gifted, 15(1), 44–55; DOI 10.1177/016235329101500106) developed a scenario-based student attitude questionnaire from the original phenomenological interviews. It analyzed responses from 1,465 students over two years and found systematic use of multiple coping strategies across school situations. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.2 Swiatek: social coping is broader than concealment

**Verified 1995 result.** Mary Ann Swiatek’s “An Empirical Investigation
of the Social Coping Strategies Used by Gifted Adolescents” (Gifted
Child Quarterly, 39(3), 154–160; DOI 10.1177/001698629503900305) studied
highly gifted adolescents identified through the Study of Mathematically
Precocious Youth and attending a rigorous summer programme. The primary
abstract reports five factors: denial of giftedness,
popularity/conformity, peer acceptance, fear of failure, and activity
level.

**1998 extension.** Swiatek & Dorr’s revision of the Social Coping
Questionnaire explicitly frames the instrument as measuring strategies
used by gifted adolescents to control the information others have about
them, supporting the broader conclusion that gifted social coping
includes visibility/information-management strategies.

**Conceptual consequence.** The computational action should not be
described as modeling “gifted social coping” as a whole. The more
accurate hierarchy is:

- Gifted social coping (broad construct)

- Information / visibility management (strategy family)

- Concealment or minimization of visible ability/giftedness (narrower
  strategy)

**Important measurement distinction.** Denial of the gifted label and
concealment of demonstrated ability are related but not identical
constructs. Swiatek 1995 directly supports
denial/conformity/peer-acceptance dimensions; it should not be cited as
though “hiding actual ability” were itself the named 1995 factor without
checking the relevant items or later revisions.

## 5.3 Peer acceptance, stigma, and social motivation

The gifted literature supports the following with different levels of
strength:

- Gifted students can perceive visible high ability or the gifted label
  as socially differentiating or stigmatizing.

- Some students explicitly report managing visibility in order to
  preserve normal social interactions, reduce peer comparison, avoid
  jealousy/rejection, or fit peer norms.

- A forced-choice tension between achievement/visibility and peer
  acceptance appears in the literature, but it is not universal; many
  gifted students maintain friendships and some are well accepted or
  popular.

- The literature is stronger on perceived or reported peer costs than on
  experimentally identified causal effects of an objective rejection
  event on later concealment.

**Model-mapping consequence.** A model variable representing adverse
peer response is empirically motivated. However, the exact probability
of rejection, the update strength after rejection, and the persistence
of a “stigmatized” state are theoretical model choices unless separately
calibrated. The literature does not justify treating one rejection event
as a validated developmental transition.

## 5.4 Context-dependent visibility

**Context dependence is one of the better-supported parts of the gifted
literature.** The dossiers report concealment/conformity strategies
varying by school environment, peer culture, gender, and national
context. Gifted-only or homogeneous settings can allow freer expression
of ideas and greater peer fit, while high-achievement environments can
simultaneously increase competition and social-comparison pressure. Thus
“receptive context” should not be equated mechanically with “gifted
classroom.”

**Evidence-strength caveat.** Much of the context evidence comes from
cross-sectional comparisons, interviews, reviews, or retrospective
reports rather than repeated within-person observation of the same
student across multiple contexts. Therefore the broad concept is well
motivated, but the project’s exact context transition/search dynamics
remain theoretical.

## 5.5 Peer preference and search for receptive environments

**The literature is stronger for peer preference than for active
sequential search.** Gifted youth are reported to prefer intellectually
similar peers, older peers, high-achieving friends, small like-minded
circles, or settings in which intellectual interests are normalized.
Some studies also report changing environment or distancing from
poor-fit contexts as coping. Network studies provide evidence of
selective friendship formation based on valued traits.

**However, the model concept “search among multiple unknown contexts
until a receptive one is discovered” is only a plausible mapping at
present.** Children and adolescents often have limited agency over
school placement; preference, homophily, reactive escape, and deliberate
sequential search are not the same phenomenon. There is currently little
direct evidence tracking a systematic search process with unknown
receptivity.

## 5.6 Persistence over time is not established

**This is a hard limitation.** The current gifted literature is largely
cross-sectional, qualitative, or questionnaire based. It supports the
existence of concealment strategies but does not establish their
longitudinal persistence, metastability, or irreversibility. Therefore
human-language claims such as “locked into masking,” “persistent masking
state,” or “developmental trap” require evidence beyond what has been
retrieved.

## 5.7 Current terminology boundary

The gifted literature currently supports the following hierarchy of
terms, from broadest to narrowest:

- social coping

- information / visibility management

- concealment / hiding giftedness or ability

- denial of giftedness

- conformity / blending in

**“Masking” is not yet the best-established technical term in the
retrieved gifted literature.** It may remain useful as accessible
project language, but the formal paper should define it explicitly and
anchor it to the older gifted vocabulary rather than assuming
equivalence with neurodivergent masking/camouflaging. The dedicated
masking/camouflaging terminology audit is still outstanding, so no
genealogy of the term should yet be asserted.

# 6. Social learning, peer influence, and norms: background rather than novelty

**The social-learning dossier provides a broad psychological bridge.**
People learn from observation, imitation, teaching, advice, and peer
interaction; peer groups transmit norms and can influence academic
engagement, prosocial/aggressive behavior, and identity-linked behavior.
Social information is weighted by context, similarity, trust, status,
and relationship history.

**What this contributes.** It makes peer-derived reward and norm
sensitivity plausible ingredients in a social learning model. It also
reinforces the idea that peer context is not a homogeneous scalar: who
the peers are and how socially salient they are can matter.

**What it does not contribute.** The dossier is not close formal prior
art for the project’s incomplete-feedback or persistent-state
mechanisms. It should be used as background/context, not as evidence of
computational novelty. Observational social learning is also distinct
from the project’s primary individual trial-and-error feedback mechanism
unless social information is explicitly modeled.

# 7. BFLPE and social-comparison costs

**The BFLPE literature gives a strong empirical basis for
context-dependent comparison costs.** Equally able students can report
lower academic self-concept in higher-achieving schools/classes because
self-evaluation is formed relative to the local reference group. This
has been studied across selective and gifted contexts, and gifted
placements can simultaneously offer academic/enrichment benefits while
imposing comparison-related self-concept costs.

The current audit supports the following bounded use:

- A social-comparison cost associated with being surrounded by
  high-achieving peers is empirically well motivated.

- Gifted and selective settings are legitimate application contexts for
  this mechanism.

- BFLPE primarily establishes self-concept/reference-group effects;
  downstream emotion, motivation, aspirations, and performance
  consequences have evidence, but a specific concealment/retreat choice
  is not the core established outcome.

- The project parameter representing comparison cost is model-imposed.
  It must not be described as an empirically calibrated BFLPE measure or
  given a human-scale interpretation without calibration.

- The behavioral threshold at which the learner retreats in the
  simulation is not a known BFLPE threshold.

**Interpretive opportunity.** BFLPE can motivate why “receptive context”
is not simply equivalent to “higher-ability context”: one context may be
socially safer for intellectual visibility yet more costly through
upward comparison. This makes the social environment multidimensional
rather than monotonically good or bad.

# 8. Integrated literature implications for E01–E05

| **Experiment**                             | **Literature status**                        | **What the literature explains**                                                                                                                                                                       | **Current implication**                                                                                                                                                             |
|--------------------------------------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| E01: restricted feedback / early rejection | Generic mechanism established                | Hot-stove, endogenous sampling, self-confirming learning, finite-horizon softmax all explain the basic sampling effect.                                                                                | Use as baseline/mechanism demonstration. Do not headline “trap” or persistent final masking. Forced/counterfactual restoration is a known remedy.                                   |
| E02: graded disclosure                     | Strong generic representation challenge      | More independent actions require more sampling; tabular representation does not generalize across graded levels.                                                                                       | Do not interpret as disclosure-specific without prior-art search. Potential value is a negative result: preserving nonzero exploration need not improve endpoint discovery/welfare. |
| E03: persistent social state               | Not adjudicated by current generic-RL search | Dynamic state transitions are genuinely additional structure, but we have not yet searched the closest disclosure/stigma/reputation MDP prior art.                                                     | Highest-priority novelty search. Keep exact full-information dynamic benchmark wording.                                                                                             |
| E04: scarce receptive-context search       | Not adjudicated by generic K-scaling         | Gifted literature supports peer/context preference, but active search is weakly grounded; formal scarce-good-context prior art not yet searched.                                                       | Second highest-priority novelty search. Preserve controls separating K from scarcity/discovery.                                                                                     |
| E05: learned/objective crossover           | Mixed / mechanism unresolved                 | The binary softmax theorem is true but does not apply to E05's eight-action across-child modal statistic. Finite sampling, temperature/action-set normalization, learned-value distributions, and comparator differences can all contribute; the observed magnitude is not decomposed. BFLPE motivates a comparison cost only. | Use as a descriptive quantitative result unless later work isolates mechanism. Do not claim temperature is ruled out and do not call bf calibrated BFLPE. |

# 9. Claims the literature currently permits—and claims it does not

## 9.1 Currently defensible

- Some gifted children and adolescents deliberately manage or reduce the
  visibility of giftedness/ability in peer settings.

- Gifted social coping is a recognized and measurable construct, and
  concealment/denial/conformity are part of that broader strategy space.

- Peer jealousy, rejection concerns, social comparison, and desire for
  ordinary peer interactions are documented in the gifted literature as
  perceived social pressures associated with visibility management.

- Context matters: the social costs and benefits of displaying ability
  vary across peer and school environments.

- Early adverse outcomes can suppress later sampling under partial
  feedback; this is consistent with established
  hot-stove/endogenous-sampling mechanisms.

- Richer feedback or forced exploration can reduce
  information-acquisition failures, but that remedy is generic rather
  than novel.

- A finite-horizon tabular softmax learner is learner-specific;
  asymptotic convergence results do not erase finite-time path
  dependence.

- A full-information dynamic optimum is a valid oracle comparator,
  provided the paper does not equate its gap with failure relative to an
  information-matched attainable optimum.

- In an exactly binary softmax probability, fixed temperature affects slope, not the 50% Q-value crossover location. This fact does **not** identify the mechanism of E05's eight-action modal-response crossing.

- Graded actions represented as independent arms impose a strong
  representation assumption; structured learners could share information
  across nearby disclosure levels.

- BFLPE supports context-dependent comparison costs in gifted/selective
  environments.

## 9.2 Not currently defensible

- “Gifted children generally mask” or any population-prevalence estimate
  based on the simulation or convenience samples.

- “One rejection causes persistent masking” or equivalent causal
  developmental language.

- “The learner is irreversibly trapped/locked in” based on
  finite-horizon softmax simulations alone.

- “The learned policy fails to find the best policy available under its
  own information constraints” when only the full-information optimum
  has been computed.

- “Graded disclosure itself makes learning worse” without separating
  action-count/representation effects from domain structure.

- “The behavioral crossover gap is caused by softmax temperature.”

- “Softmax temperature has been ruled out as a contributor to the E05 modal-response crossing.”

- “The comparison-cost parameter is empirically calibrated BFLPE.”

- “Gifted students systematically search through peer contexts until
  they find a receptive one.” The current evidence supports preference
  and some context change, not a well-characterized sequential search
  process.

- “Gifted concealment is longitudinally persistent.” The current
  literature does not establish persistence over time.

- “Masking” is the canonical gifted-literature term or historically
  imported from autism. The terminology genealogy remains to be audited.

# 10. Source-verification lessons from the search process

The literature process itself produced several methodological lessons
relevant to the final audit:

- AI-assisted literature dossiers are useful for search breadth and
  mechanism clustering, but not reliable enough to accept bibliographic
  details or novelty verdicts without inspection.

- The Asta generic-RL synthesis overreached by classifying every result
  as fully generic, calling the full-information benchmark invalid, and
  treating sample-complexity scaling as an exact multiplicative K
  effect. These conclusions were narrowed in this audit.

- The initial Asta Coleman/Cross verification misidentified the 1985 and
  1988 publications. Publisher verification corrected the record:
  Coleman (1985) is Schooling the Gifted (book), and Coleman &
  Cross (1988) is the Journal for the Education of the Gifted article
  “Is Being Gifted a Social Handicap?”.

- Swiatek 1995 is now publisher-verified. Dossier summaries that
  attribute all later “hiding giftedness” language directly to the 1995
  factor structure should be avoided; later revisions/related work
  provide the stronger information-management framing.

- Striking older claims (for example, specific Gross percentages or
  detailed behaviors such as reducing vocabulary/lying about grades)
  should either be verified in the original source before manuscript use
  or omitted. They are not necessary to establish the existence of
  gifted concealment.

# 11. Remaining literature work

**Broad retrieval should now stop.** The remaining work consists of four
bounded searches that can still change the paper’s framing or novelty
classification.

**1. Persistent-state prior art — highest priority**  
Search dynamic disclosure/concealment in which revealing information
changes persistent future social state: stigma, reputation, acceptance,
exclusion, identity status, or other endogenous state transitions.
Determine whether comparable formal models already establish
learned/full-information policy divergence.

**2. Scarce receptive-context search prior art**  
Search heterogeneous-audience/context models in which only some contexts
are receptive, receptivity is initially unknown, and the agent must
search/match/select among contexts. Distinguish context count from
scarcity/discovery cost.

**3. Graded/partial disclosure prior art**  
Search partial, incremental, continuous, or selective
disclosure/revelation models. Determine whether the specific “broader
exploration but poorer endpoint identification” pattern has a
disclosure-specific analogue beyond generic independent-arm effects.

**4. Masking/camouflaging terminology audit**  
Compare masking, camouflaging, concealment, compensation, assimilation,
self-presentation, impression management, social coping, and disclosure.
Use neurodivergence literature for terminology boundaries only; do not
transfer empirical findings to giftedness.

**After those searches:** freeze the literature dossier and run the
V1-02 synthesis/novelty adjudication. Only a clearly identified,
publication-blocking literature gap should trigger further retrieval.

# 12. Current provisional scientific boundary

**The literature now strongly argues against a contribution framed as
“simple RL discovers that masking can persist despite a better authentic
action.”** That underlying learning mechanism is generic.

**A potentially defensible contribution, if the remaining prior-art
searches support it, is narrower and structural:** known
incomplete-learning mechanisms may acquire distinct consequences when
embedded in social environments where disclosure changes persistent
future social state and/or where acceptance depends on finding scarce
receptive contexts. Gifted concealment provides a grounded application
in which visibility management, peer acceptance, context dependence, and
comparison costs are empirically meaningful.

**This is not yet a frozen novelty claim.** The persistent-state and
receptive-context searches could show that these mechanisms already have
close formal analogues, in which case they must be reframed as
application/synthesis rather than formal novelty. Conversely, if close
analogues are not found after a bounded primary-source search, E03/E04
may become the main structural contribution while E01/E02/E05 play
baseline, negative, or illustrative roles.

# Appendix A. Current key source families and verification status

| **Source family**                                          | **Verification state**                       | **Current role**                                                                                                                                                                                            |
|------------------------------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fudenberg & Levine / self-confirming equilibrium           | Primary paper identified through dossier     | Load-bearing for choice-dependent observation and off-path belief persistence. Full bibliographic verification still advisable before manuscript reference list.                                            |
| Cesa-Bianchi et al. 2017, Boltzmann Exploration Done Right | Primary/theory source in dossier             | Load-bearing generic-RL challenge to naive Boltzmann exploration.                                                                                                                                           |
| Hot-stove / Denrell tradition                              | Mixed primary/secondary in dossier           | Load-bearing for adverse outcome → under-sampling mechanism; exact original Denrell/March references should be verified before final manuscript citation.                                                   |
| Counterfactual/full feedback literature                    | Mixed primary/secondary in dossier           | Supports richer-feedback mechanism; use strongest primary sources rather than dossier connective prose.                                                                                                     |
| Structured/Lipschitz bandits                               | Primary sources quoted in dossier            | Load-bearing for E02 action-representation limitation.                                                                                                                                                      |
| Coleman & Cross 1988                                       | PRIMARY PUBLISHER VERIFIED                   | Correct record: Journal for the Education of the Gifted 11(4), 41–56; DOI 10.1177/016235328801100406; 15 adolescents interviewed twice.                                                                     |
| Cross, Coleman & Terhaar-Yonkers 1991                      | PRIMARY PUBLISHER VERIFIED                   | Scenario-based stigma-management study; Journal for the Education of the Gifted 15(1), 44–55; DOI 10.1177/016235329101500106; 1,465 students over two years.                                                |
| Swiatek 1995                                               | PRIMARY PUBLISHER VERIFIED                   | Gifted Child Quarterly 39(3), 154–160; DOI 10.1177/001698629503900305; five factors in primary abstract.                                                                                                    |
| Swiatek & Dorr 1998                                        | PRIMARY PUBLISHER VERIFIED (abstract/record) | Revision of SCQ; explicitly frames coping as strategies controlling information others have about gifted adolescents.                                                                                       |
| Cross et al. 2019 cross-cultural gifted social experience  | Dossier-level direct quotation               | N=90 across five countries; direct reports of visibility awareness, peer jealousy/rejection concerns, hiding abilities/conforming. Exact bibliographic metadata should be verified before final references. |
| Tourreix et al. 2023 systematic review                     | Dossier-level                                | Useful secondary synthesis of gifted social coping/context variation.                                                                                                                                       |
| Gifted peer preference/context studies                     | Mixed primary/secondary in dossier           | Supports preference/context selection more strongly than active sequential search.                                                                                                                          |
| Marsh/BFLPE tradition                                      | Primary and review sources in dossier        | Load-bearing background for social-comparison costs in high-achievement settings.                                                                                                                           |
| Lee et al. 2020 gifted/selective BFLPE application         | Dossier-level quotation                      | Useful gifted-specific application of reference-group comparison; verify bibliographic record before manuscript reference list.                                                                             |

# Appendix B. Unresolved questions that can still reverse framing

**Persistent-state prior art:** Is there already a substantially
comparable formal model of disclosure/concealment that changes a
persistent stigma/reputation/acceptance state and produces divergence
between learned behavior and a full-information dynamic optimum?

**Receptive-context search prior art:** Is costly discovery of rare
favorable social contexts already formalized in search, matching,
disclosure, contextual-bandit, or audience-selection literature in a way
that substantially overlaps the project?

**Graded disclosure:** Does partial/graded disclosure have established
formal learning results beyond generic K-arm sample dilution and
representation effects?

**Terminology:** Which term—masking, concealment, visibility management,
camouflaging, self-presentation—best matches the modeled action without
importing unsupported constructs from another population?

**E05 magnitude:** How much of a stable learned/objective threshold
displacement should be expected under the maintained finite-horizon
learner, and is the observed magnitude structurally informative or
merely learner-specific?

**Gifted persistence:** Are there longitudinal studies showing
persistence or transition of concealment strategies over months/years?
Current evidence does not establish this; unless a targeted source
appears, it should remain a limitation rather than a search priority for
V1.

# Appendix C. AI2 Asta dossiers incorporated in this audit

- Self-Confirming Equilibrium, Learning, and Observational Equivalence
  under Incomplete Information

- Counterfactual Feedback, Exploration, and Self-Confirming Beliefs in
  Bandit Learning

- Hot-Stove Effect, Sampling Asymmetry, and Feedback in Reinforcement
  Learning

- Convergence and Limitations of Fixed-Temperature Softmax Boltzmann
  Q-Learning

- Boltzmann Temperature Schedules, Reward Scaling, and Q-Learning
  Convergence

- Finite-Horizon Q-Learning with Softmax: Early Rewards, Initialization,
  Path Dependence, and Under-Sampling

- Structured and Lipschitz Bandits Over Continuous and Related Action
  Spaces

- Softmax Temperature, 50% Thresholds, and Q-Value Differences

- Full-Information and Information-Constrained Optimal Policies in
  Reinforcement Learning

- Gifted Youth Concealing Ability: Motives, Behaviors, and Research
  Traditions

- Giftedness Stigma, Social Coping, and Measurement in Gifted Education

- Gifted Adolescents’ Ability Visibility, Peer Context, and School
  Settings

- Gifted Youths’ Peer Preferences, Social Niche Selection, and Receptive
  Contexts

- Swiatek Social Coping Strategies in Gifted Students

- Coleman 1985 and Coleman-Cross 1988 Stigma of Giftedness Citations and
  Findings

- Swiatek 1995 Gifted Adolescents’ Coping Strategies and Peer Acceptance

- Social Learning, Peer Influence, and Social Norms

- BFLPE, Social Comparison Costs, and Academic Self-Concept in Gifted
  and Selective Settings

Note: inclusion in this appendix means the dossier informed the audit;
it does not mean every claim or citation inside the dossier was
accepted. Primary-source corrections and narrower interpretations take
precedence where noted above.
