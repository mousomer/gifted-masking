# Results and discussion — speaker notes

Eight slides. Planned narration: 11 minutes. Append after your existing introduction and model slides.

## 1. Feedback changes behaviour under unchanged opportunities

**Time:** 0:00–1:30 within this section.

M0 lets us separate learning from changes in the opportunity itself. On the left, initial rejection reduces subsequent authentic sampling by about two point six percentage points, compared with initial acceptance. But the final-window masking contrast is close to zero, with an interval that spans zero. This history comparison therefore does not establish a lasting final-window difference. On the right, we change what initially rejected learners can experience or learn. Requiring authenticity on five percent of later interactions reduces final masking by about four point seven points. Providing authentic feedback even on masking trials reduces it by about eleven point eight points. The unchosen reward is not added to the learner’s actual return. The two interventions have different intensities, so this comparison does not rank them as practical treatments. What the model establishes is that experience and access to information can change later allocation while environmental payoffs remain fixed.

**Sources:** projects/frontiers_article/publication_v1/data/e01_primary_effects.csv; projects/frontiers_article/publication_v1/data/e01_intervention_effects.csv.

**Reference note:** History: rejection minus acceptance. Information: intervention minus baseline in the rejected stratum. History sampling uses steps 1–1999; masking uses the last 400 of T=2000 steps. n=500/cell/master.

## 2. More participation can coexist with less full expression

**Time:** 1:30–2:45 within this section.

The graded model offers intermediate disclosure levels, each with an independent learned value. Here we compare those options with binary choice after initial rejection. Any disclosure increases by twenty-five and a half percentage points over subsequent interactions. Full authenticity, however, falls by nearly thirty-three points in the final window. These are different outcomes measured over different windows. More participation can therefore coexist with less full expression. In these tested cells, the expected payoff still increases linearly with disclosure, so full expression remains the objectively best endpoint. The result does not show that an intermediate level becomes objectively optimal. It also does not model a ladder on which success at one level automatically teaches the learner about the next. An empirical study would need to measure both the degree of expression and whether learning transfers between levels.

**Sources:** projects/frontiers_article/publication_v1/data/e02_primary_effects.csv.

**Reference note:** Any disclosure is d>0 over steps 1–1999. Full authenticity is d=1 during the final 400 steps. Effects +25.504040052777677 pp and −32.86922325725828 pp.

## 3. Learned choices can disagree with the dynamic optimum

**Time:** 2:45–4:45 within this section.

For M2, the benchmark includes future social consequences. The map compares learned neutral-state choices with the optimal dynamic policy. Each square is one setting of acceptance probability and recovery from stigma. The rust region contains 243 of the 357 settings. In those cells, adequate neutral-state observations favour masking while the benchmark favours authenticity. The blue region shows agreement, and gray cells are inconclusive. These are counts of parameter settings, not percentages of children. The threshold table explains why the benchmark matters. In the static model, authenticity becomes worthwhile above about point seven one seven. With persistent social states, the reference threshold falls to about point three eight four, and to point two six nine with greater recovery. Persistent acceptance creates future value, and recovery reduces the cost of stigma. The finite learner still has to discover those consequences through experience. The benchmark already knows the environment. At five selected disagreement settings, the difference persists through five thousand interactions, with documented sensitivity exceptions. We therefore have evidence of disagreement over the tested horizons, rather than proof of permanent entrenchment.

**Sources:** projects/frontiers_article/publication_v1/data/e03_grid_map.csv; projects/frontiers_article/publication_v1/data/e03_objective_thresholds.csv; src/gifted_masking/analysis/m2_optimal.py.

**Reference note:** 243 learned-suboptimal-mask, 107 agreement, 7 inconclusive. All 243 disagreement cells agree across every master. Dynamic thresholds are numerical bracket midpoints, not confidence intervals. Oracle uses untransformed reward and an infinite discounted horizon, gamma=.9.

## 4. Finding a receptive group does not ensure sustained expression

**Time:** 4:45–6:30 within this section.

The best available reward stays fixed as we add groups, but learned allocation changes. In the flat representation, each group has separate masking and authentic actions. With sixteen groups, final masking reaches eighty-four percent. Yet almost every learner has already experienced acceptance in the receptive group at least once. The two percentages have different denominators: one measures late actions, and the other counts learners with a success anywhere in the full run. Successful encounter does not ensure sustained use, and one success does not supply complete knowledge. The curves show why representation matters. Choosing a group and then a behaviour gives a similar increase in masking. Pooling masking into one shared action keeps masking near twenty-six percent. That change affects both information sharing and the initial allocation of choices, so it does not isolate one pure psychological mechanism. The supported conclusion is conditional: the effect of more contexts depends strongly on how the learner represents those choices. It cannot be generalized into a claim that more contexts always cause masking.

**Sources:** results/summaries/frontiers_m3_search_architectures_v1_curves.csv; results/summaries/frontiers_m3_search_architectures_v1_effects.csv.

**Reference note:** At K=16 flat final masking=.841906, full-run accepted-good-context encounter=.9972. Shared-mask architecture also changes initial mask probability from 1/2 to 1/(K+1).

## 5. The learned boundary occurs before objective indifference

**Time:** 6:30–8:00 within this section.

The comparison-cost experiment changes the reward for accepted authenticity in the receptive group. The equations place objective indifference at about point four seven one. The flat four-group population crosses its behavioural boundary earlier, near point three one three, with the displayed confidence interval. At that learned crossing, authenticity in the receptive group still has an objective advantage. The vertical axis needs care: it counts learners whose most frequent individual final-window action is authenticity in the good group. Crossing fifty percent therefore has a specific modal meaning. It is not the onset of majority masking. Four separate masking actions can together occupy most interactions even when one authentic action is individually the most frequent. These boundaries answer different questions: when the opportunity loses its expected-payoff advantage, and when the learned population crosses the defined behavioural threshold. The difference is a result for this architecture and finite learning horizon.

**Sources:** projects/frontiers_article/publication_v1/data/e05_response_vs_bf.csv; projects/frontiers_article/publication_v1/data/e05_crossings.csv.

**Reference note:** Learned crossing=.31285211267605634; 95% CI [.307836, .316918] rounded. Objective=.47058823529411764. Curves connect archived pooled values; no refit or bootstrap.

## 6. Could behaviour change future social receptivity?

**Time:** 8:00–8:45 within this section.

A further possibility is that behaviour changes future social opportunities. M4 implements that feedback. Accepted authenticity raises later receptivity, while rejection and masking lower it at specified rates. These directions are assumptions that define the model. Current receptivity determines the present outcome before it updates. The environment therefore evolves, while the learner still keeps only two action values and does not condition them on receptivity. Such a feedback process could make histories matter. Formal E06 results remain deferred, however, and hysteresis has not been established. This is a candidate mechanism for further testing.

**Sources:** src/gifted_masking/models/m4.py; src/gifted_masking/experiments/e06.py.

**Reference note:** Receptivity is bounded in [.05,.95]. It evolves separately for each learner. Current p determines reward; Q then updates and next p follows. Learner stores two action-only values.

## 7. Similar concealment can arise through different processes

**Time:** 8:45–10:00 within this section.

The results give several explanations for similar visible concealment. Under fixed opportunities, experience and access to feedback affect what the learner discovers. With partial disclosure, separate action values can support participation without full expression. Persistent social consequences change the value of an action itself, which requires a dynamic benchmark. With multiple contexts, successful encounter and sustained use depend on how choices represent and share experience. These findings should not be collapsed into one universal cause. They also show why a single measure of masking is insufficient: participation, intensity, contextual encounter and repeated use answer different questions. The results establish behaviour in specified computational models. Identifying the corresponding processes in children requires observations or experiments that distinguish these explanations.

**Sources:** projects/frontiers_article/integrated_article_20261004/ARTICLE.md.

**Reference note:** E01–E05 each use five master replications. Broader parameter and human generalization are not established. M4 remains a separate candidate extension.

## 8. What should we measure next?

**Time:** 10:00–11:00 within this section.

These models suggest what an empirical study would need to measure. First, ask what the child expects before an interaction, and compare that expectation with the feedback they actually receive. Second, examine which experiences change those expectations. Third, test whether learning transfers: does success with a small disclosure, or in one setting, change expression elsewhere? Finally, track what persists. Social standing and recovery opportunities may affect later choices beyond the immediate response. Repeated observations should record the degree of expression and the context, rather than treating all participation as equivalent. The contribution is a set of mechanisms and distinguishing predictions that we can now test.

**Sources:** projects/frontiers_article/integrated_article_20261004/ARTICLE.md.

**Reference note:** Empirical implications are hypotheses, not established intervention effects in children.

