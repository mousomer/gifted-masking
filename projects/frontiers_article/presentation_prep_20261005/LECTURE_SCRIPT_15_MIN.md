# What mechanisms could explain masking?

**A 15-minute lecture for the eleven-slide first set.** Prepared 6 October 2026.

Read the prose aloud. Bracketed directions are presentation cues. Timings include brief pauses and pointing to the diagrams. This expanded script follows the delivered slide order and supersedes the earlier 12-minute timing for this lecture. The PowerPoint's embedded notes still contain the original shorter version. Exact duration requires rehearsal.

| Slide | Delivered title | Time | Duration |
| --- | --- | --- | ---: |
| 1 | What mechanisms could explain masking? | 0:00–1:05 | 1:05 |
| 2 | A close second | 1:05–1:50 | 0:45 |
| 3 | Learning from social experience | 1:50–3:10 | 1:20 |
| 4 | M0 · Masking or authenticity | 3:10–5:10 | 2:00 |
| 5 | M1 · Participation and full expression differ | 5:10–6:40 | 1:30 |
| 6 | M2 · Persistent social consequences | 6:40–8:55 | 2:15 |
| 7 | M3 · Context is part of the choice | 8:55–10:55 | 2:00 |
| 8 | M3 · Social comparison changes the boundary | 10:55–12:25 | 1:30 |
| 9 | M4 · Behaviour changes future receptivity | 12:25–13:40 | 1:15 |
| 10 | What changes across the models? | 13:40–14:20 | 0:40 |
| 11 | Different mechanisms imply different questions | 14:20–15:00 | 0:40 |

## Slide 1 — What mechanisms could explain masking?

[Look at the audience, then briefly indicate the child apart from the group.]

A child may be capable of much more than they choose to show. They may avoid answering, downplay an achievement, or hide an interest that makes them stand out.

Research on gifted learners documents this kind of ability concealment. Patterns differ across ages and social settings. That gives us a phenomenon to explain, but observing concealment does not tell us which process produced it.

The child in this picture could be holding back for several reasons. Perhaps they expect rejection. Perhaps earlier experiences still shape their expectations. Perhaps expressing themselves has consequences that last beyond one interaction.

Today, I will use five simple computational models to examine possible mechanisms. Each makes a different assumption about learning or the social environment, and asks what behaviour follows.

## Slide 2 — A close second

[Indicate Dash and pause before the quotation.]

In The Incredibles, Dash can run much faster than the other children. During the school race, his family encourages him to finish a close second.

He has to manage how much of his ability becomes visible. His performance reflects both his capacity and the social instruction he receives.

Here the message is explicit: hold back enough to fit in.

Our models examine how similar restraint might develop through experience, even when nobody gives that instruction directly. What might a child learn from the reactions that follow expression?

## Slide 3 — Learning from social experience

[Follow the diagram from left to right.]

The learner chooses an action, experiences an outcome, and updates its expectation about that action. Those expectations influence the next choice.

We call each learned expectation a Q-value. You can think of it as an estimate of how rewarding an action has been. Better-valued actions become more likely, while exploration continues.

The learning rate determines how strongly a new experience changes that estimate. A separate parameter can give negative outcomes extra weight. That changes how the learner values an outcome, while leaving the environment's reward unchanged.

In the basic setup, feedback concerns only the chosen action. If I conceal my ability, I do not discover how others would have reacted had I expressed it. Avoidance can therefore limit the information available to correct an expectation.

Each simulation step represents an interaction. We have not calibrated these steps to chronological age, so the models examine learning over experience without directly predicting an age trajectory.

## Slide 4 — M0 · Masking or authenticity

[Point to the two branches, then to their rewards.]

M0 is a two-armed bandit. There are two choices: masking and authenticity. The social environment stays fixed, and today's action does not change tomorrow's acceptance probability.

At the reference settings, masking gives a certain reward of zero point seven five. That represents a social benefit reduced by a cost of concealment.

Authenticity gives one point six if accepted, and minus one point four if rejected. The probability of acceptance is p.

From these rewards, we can calculate which action pays more on average. Authenticity becomes better when acceptance exceeds about seventy-two percent. At seventy-five percent acceptance, its average reward is zero point eight five, compared with zero point seven five for masking.

[Move from THEORY to SIMULATIONS.]

The simulations ask whether a learner discovers that advantage through experience. Across the two tested acceptance probabilities, initial rejection reduces subsequent authentic sampling by about two point six percentage points, compared with initial acceptance.

That difference concerns sampling after the first interaction. The final-window comparison does not establish a lasting effect of initial history alone.

A second comparison changes access to information. The learner receives feedback about authenticity even when it chooses masking, without receiving the unchosen reward. Final masking falls by about eleven point eight percentage points.

These results show how behaviour can depend on the information experience supplies, even when the underlying opportunity stays the same.

## Slide 5 — M1 · Participation and full expression differ

[Indicate the five disclosure levels, then the two bars.]

M1 introduces partial expression. Instead of choosing between nothing and everything, the learner can disclose a quarter, half, or three quarters.

Each level has its own learned value. Success with partial expression does not automatically improve the learner's estimate of full expression. Learning is specific to the selected action.

We compare these five choices with the binary setup, following initial rejection.

The frequency of some disclosure increases by about twenty-five and a half percentage points across the subsequent interactions. But full authenticity decreases by almost thirty-three percentage points in the final measurement window.

Those bars describe different outcomes and different windows. They show that more participation can coexist with less full expression.

The payoff is linear in disclosure, and full expression still has the highest expected reward in these settings. The intermediate options give the learner additional behaviours it can settle into.

For empirical work, this suggests measuring how much someone expresses as well as whether they participate. It also raises a question about generalization: does success with a small disclosure change expectations about a larger one?

## Slide 6 — M2 · Persistent social consequences

[Point first to the state boxes, then to “Mask / Authentic.”]

M2 introduces consequences that persist. The learner can be in one of three social states: neutral, accepted as themselves, or stigmatized.

These are conditions of the environment. The actions remain masking and authenticity in every state. The learner therefore stores six values: two possible actions in each of three states.

From neutral, accepted authenticity establishes acceptance. Rejection creates stigma. Acceptance can continue across interactions, while turnover can return the learner to neutral. Stigma can also persist, with possibilities for escape or successful redemption.

An action now affects both the immediate outcome and future opportunities. The learner's update therefore includes an estimate of future value.

We need a benchmark that includes those future consequences too. We calculate the optimal policy for a decision-maker who knows the model's rewards and transitions.

[Indicate the threshold table.]

Under the reference settings, authenticity becomes optimal in neutral at an acceptance probability of about thirty-eight percent, compared with seventy-two percent in M0. With greater recovery from stigma, that threshold falls to about twenty-seven percent.

Persistent acceptance can make taking the initial risk worthwhile. Recovery can reduce the future cost of rejection.

Yet in 243 of 357 tested parameter settings, the finite learners favour masking in neutral while the dynamic benchmark favours authenticity. Those are settings, not a percentage of children.

The disagreement also persists through five thousand interactions at five selected settings, although some parameter changes reduce it.

M2 therefore separates two explanations: concealment may be justified by lasting consequences, or learning may favour concealment where the model's dynamic optimum favours expression. We need the benchmark to distinguish them.

## Slide 7 — M3 · Context is part of the choice

[Point across the group columns.]

M3 gives the learner a choice of social context. One group is more receptive, while the others are less receptive.

In the basic version, choosing a group and choosing a behaviour form one combined action. With four groups, there are eight actions: mask or be authentic in each group.

Unlike M2, there is no evolving social standing. Group receptivities stay fixed. The group is part of the action being selected, and each group–behaviour pair has its own learned value.

We increase the number of groups while keeping the best available reward unchanged.

[Indicate the curves and the two endpoint numbers.]

With sixteen groups, final masking reaches about eighty-four percent in the flat model. Yet almost every learner has already experienced acceptance in the receptive group at least once.

Successful encounter does not ensure sustained use. One positive experience also does not give the learner complete knowledge of that group's rewards.

The representation of choices matters. Choosing the group first and then the behaviour produces a similar increase. But with one shared masking action and separate authentic actions for each group, masking stays near twenty-six percent.

That change affects both how experience is shared and the initial allocation of choices. We cannot attribute the difference entirely to one of those features.

The result is conditional: adding contexts can change behaviour substantially, but its effect depends on how the learner represents and learns about those choices.

## Slide 8 — M3 · Social comparison changes the boundary

[Indicate the two vertical boundaries.]

The next experiment adds a comparison cost to accepted authenticity in the receptive group. This represents the possibility that expressing ability among stronger peers carries a cost of comparison. It is an assumed payoff mechanism.

The equations tell us exactly when that cost removes the receptive group's advantage over masking: about zero point four seven one.

The simulated population crosses its behavioural boundary earlier, near zero point three one three. The uncertainty interval is approximately zero point three zero eight to zero point three one seven.

We need to define that boundary carefully. It is where half the learners have authenticity in the receptive group as their most frequent individual action in the final window.

It does not measure the onset of majority masking. Several separate masking actions can together occupy most interactions, even while one authentic action is the most frequent individual choice.

The finding is that this learned boundary occurs while authenticity in the receptive group still has an objective advantage. The mathematical and behavioural thresholds answer different questions.

## Slide 9 — M4 · Behaviour changes future receptivity

[Follow the feedback diagram, then indicate the update table.]

M4 allows behaviour to change the environment itself.

The two actions are still masking and authenticity. The environment now has a changing acceptance probability, p at time t. Acceptance after authenticity raises future receptivity. Rejection and masking lower it, according to specified rates.

Those directions are model assumptions. Each outcome uses the current receptivity, which then updates for the next interaction.

The learner still stores just two action values. It does not keep a separate estimate for every level of receptivity. This differs from M2, where values explicitly depend on social state.

The resulting feedback could produce different trajectories from different histories. Establishing hysteresis would require a controlled test that changes a parameter in both directions and compares the paths.

The mechanism is implemented, but formal E06 results remain deferred. This slide presents a candidate feedback process, with its evidence still to be established.

## Slide 10 — What changes across the models?

[Read across the table without reading every cell.]

Across the models, three distinctions matter: what can be chosen, what the environment carries forward, and what the learner remembers.

M1 expands the behaviours. M2 conditions learning on social state. M3 includes context in the choice. M4 makes receptivity change through interaction, while the learner still uses two action values.

The reported E01 to E05 findings use five independent master replications. They establish behaviour in these specified models. Identifying the corresponding processes in people requires empirical tests.

## Slide 11 — Different mechanisms imply different questions

[Pause briefly, then address the audience.]

When we observe concealment, several explanations remain possible. A child may lack corrective experience, learn to express only partially, face lasting consequences, or struggle to use a receptive context consistently.

What does the child expect? Which experiences change that expectation? Does learning transfer between situations? What consequences persist?

The models turn a broad observation into specific mechanisms we can test, helping explain why displayed ability sometimes falls short of what a child can do.

---

## Presenter reference notes — do not read aloud

The script follows [the delivered slide content](main_deck_20261006/RENDERED_CONTENT.json). The [simulation guide](SIMULATION_GUIDE.md) contains equations, full configurations, uncertainty definitions, and source links. The [source index](SOURCE_INDEX.json) records file identities. The [opening literature review](SLIDE_01_SOURCES.md) supports the qualified age wording; the talk does not claim a universal decrease with age or an absence of earlier mechanism accounts.

| Slides | Numerical or interpretive authority |
| --- | --- |
| 1–2 | Opening literature record and [asset sources](assets/ASSET_SOURCES.json). Dash is a fictional illustration of explicit instruction, not evidence for the learning mechanism. |
| 3–4 | Guide sections 2–3; M0 reward equations and E01 archived effects. Initial rejection minus acceptance: −2.58 pp [−3.58, −1.59] for post-initial authentic sampling. Counterfactual feedback minus baseline: −11.81 pp [−12.66, −10.97] for final masking. Both pool p=.75/.85 at lambda=1. |
| 5 | Guide section 4; E02, rejected stratum, p=.75/.85 pooled. Any disclosure: +25.50 pp [25.30, 25.71] over post-initial interactions. Full authenticity: −32.87 pp [−34.20, −31.53] over the final window. Graded minus binary. |
| 6 | Guide section 5; E03 value-iteration thresholds .383942 at eta=0 and .269012 at eta=.8, versus static .716667. The 243/357 count refers to grid cells and aggregates adequate Neutral-state actions. The optimal benchmark knows the model and optimizes an infinite discounted horizon; the learner has finite experience. Five selected disagreement settings persist to T=5000, with documented sensitivity exceptions. |
| 7 | Guide section 6; E04 fixed-identity, one-good-context means. At K=16, flat final masking .841906 and full-run accepted-good-context encounter .9972 have different denominators. Global-mask choice also changes initial masking probability from one half to 1/(K+1); this is not a pure information-sharing intervention. |
| 8 | Guide section 7; E05 flat K=4, lambda=1, five masters. Objective threshold .470588. Learned modal-population crossing .312852 [95% bootstrap interval .307836, .316918]. Cost applies only to accepted authenticity in the good group. |
| 9 | Guide section 8; M4 reward and Q update use current p, then receptivity updates. Reference bounds [.05,.95]. Receptivity evolves separately for each learner; no coupled peer population is simulated. Formal E06 evidence and confirmed hysteresis remain deferred. |
| 10–11 | Model comparison and empirical questions, not estimated intervention effects in children. |

The allocated 15 minutes include diagram explanation and brief pauses, with no separate question period. Use the elapsed-time cues during rehearsal. Confidence intervals need not be read aloud except for the central crossing on slide 8; they remain visible in the deck or recorded here.
