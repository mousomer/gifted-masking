# Masking mechanisms lecture

Methods followed by results. Planned duration 15 minutes; 16 slides.

## 1. What mechanisms could explain masking?

Introduction · 45 seconds

Gifted children may conceal their abilities or moderate their performance in response to social expectations. The literature documents concealment, but its patterns vary with age and setting. Our question is what processes could produce this behaviour. We examine possible learning mechanisms: what someone chooses to express may depend on earlier feedback, the available actions, and how the social environment responds. These simulations describe possible processes. They are not fitted developmental trajectories, and one interaction does not represent one year.

Sources: Opening slides from masking_mechanisms_first_set.pptx

## 2. A close second

Introduction · 25 seconds

Dash gives us a familiar illustration. He can run much faster than everyone else, but his family encourages him to finish a close second. The issue is displayed ability rather than underlying ability. Here the instruction is explicit. Our models instead ask how similar restraint could develop through repeated experience.

Sources: Opening slides from masking_mechanisms_first_set.pptx

## 3. Learning from social experience

Introduction · 45 seconds

The shared process is straightforward. The learner chooses an action, receives an outcome, and updates its expectation for that action. Higher-valued actions become more likely, while some exploration continues. A learning rate controls how quickly expectations change, and a temperature controls how strongly choice follows those expectations. Negative realized rewards can receive extra weight through loss aversion. Usually only the chosen action is updated. We first define all five models, then turn to their results. These are distinct extensions of a baseline, not one model that accumulates every mechanism.

Sources: Opening slides from masking_mechanisms_first_set.pptx

## 4. M0  Two actions in a fixed environment

Methods · 55 seconds

M0 is a two-armed bandit. On each interaction the learner either masks or expresses authenticity. Masking produces a certain reward: the belonging benefit minus the cost of concealment, here point seven five. Authenticity is accepted with probability p and gives one point six; rejection gives minus one point four. These rewards are defined in model units. Receptivity stays fixed, and an action does not create a persistent social state. The learner stores two values and updates the chosen one. E01 compares initial rejection with initial acceptance, then tests forced authentic experience and additional authentic feedback. Those manipulations change the information or experience available to the learner.

Sources: src/gifted_masking/models/m0.py; src/gifted_masking/core.py; configs/frontiers_article/e01_hot_stove_standard.json

## 5. M1  Graded disclosure

Methods · 45 seconds

M1 changes the action space. Instead of only masking and full authenticity, the learner chooses among five disclosure levels from zero to one. Each level has its own learned value. Acceptance probability falls with disclosure according to the displayed rule. The masking cost declines as disclosure increases, while the authenticity benefit increases. The environment still has fixed receptivity and no persistent social state. Crucially, updating the value of one level does not update neighbouring levels. E02 compares this graded action space with the binary model, measuring any disclosure, full authenticity, and disclosure intensity separately.

Sources: src/gifted_masking/models/m1.py; configs/frontiers_article/e02_binary_graded_standard.json

## 6. M2  Persistent social states

Methods · 75 seconds

M2 changes the environmental state space. There are three states: Neutral, Accepted, and Stigmatized. The actions are still Mask and Authentic in every state. The learner therefore has six values, arranged as three rows and two columns. From Neutral, accepted authenticity leads to Accepted and rejection leads to Stigmatized. In Accepted, authenticity pays reliably, although peer turnover can return the learner to Neutral. In Stigmatized, masking pays less and rejected authenticity costs more. Authenticity can redeem the learner with probability p over two; if stigma remains, escape can return the learner to Neutral. Rewards are paid before those next-state transitions. The Q-learning update includes future value through the discount factor gamma. E03 compares learned neutral-state choices with a full-information optimal policy, which is computed from the same transition and reward rules.

Sources: src/gifted_masking/models/m2.py; src/gifted_masking/analysis/m2_optimal.py; configs/frontiers_article/e03_m2_regime_standard.json

## 7. M3  Choosing a group and a behaviour

Methods · 70 seconds

M3 makes context part of the choice. There are K groups, with one receptive group and less receptive alternatives. Their acceptance probabilities remain fixed. In the flat model, each action combines a group and a behaviour, giving two K actions: mask in group one, be authentic in group one, and so on. Choosing a group is not entering an M2-style persistent social state. The learner stores a separate value for each pair. E04 varies the number of groups and compares this representation with choosing the group first, or sharing one masking action across groups. E05 adds a comparison cost only to accepted authenticity in the receptive group. We assess successful encounter, subsequent masking, modal actions, and objective payoff separately.

Sources: src/gifted_masking/models/m3.py; configs/frontiers_article/e04_m3_search_architectures_standard.json; configs/frontiers_article/e05_m3_bflpe_crossover_standard.json

## 8. M4  Behaviour changes receptivity

Methods · 55 seconds

M4 returns to two actions but lets the environment change. Current receptivity determines the outcome. After reward and learning, accepted authenticity raises receptivity toward its upper bound. Rejection and masking lower it toward its lower bound, at separately specified rates. Each simulated learner has its own receptivity trajectory. The important distinction is on the right: the environment carries a continuous variable, p over time, but the learner still stores only two action values. It does not condition those values on current receptivity. This is an endogenous, nonstationary bandit. The arrows and update rules define a candidate feedback mechanism; they are assumptions to be examined.

Sources: src/gifted_masking/models/m4.py; src/gifted_masking/experiments/e06.py

## 9. Feedback changes behaviour under unchanged opportunities

Results · 80 seconds

Now we turn to results, beginning with M0. At the acceptance probabilities tested here, authenticity has the higher objective expected reward. On the left, initial rejection reduces subsequent authentic sampling by about two point six percentage points compared with initial acceptance. The final-window masking interval includes zero, so this history comparison does not establish a lasting difference. On the right, initially rejected learners receive additional experience or information. Five percent forced authenticity reduces final masking by about four point seven points. Authentic feedback on masking trials reduces it by about eleven point eight points. These interventions have different intensities and cannot be ranked as practical treatments from this comparison. The supported finding is that experience and information can change learned allocation while environmental payoffs stay fixed.

Sources: projects/frontiers_article/publication_v1/data/e01_primary_effects.csv; projects/frontiers_article/publication_v1/data/e01_intervention_effects.csv

## 10. More participation can coexist with less full expression

Results · 65 seconds

In M1, adding intermediate choices increases any disclosure by twenty-five and a half percentage points after the initial interaction. Yet full authenticity falls by almost thirty-three points in the final window. Those measures have different definitions and time windows. More participation therefore does not necessarily mean more full expression. In these tested settings, the expected payoff still increases linearly with disclosure, so full expression remains the best objective endpoint. The result is about allocation among independently learned actions. It does not demonstrate that partial disclosure is objectively optimal, or that success at one level automatically teaches the learner to move to the next.

Sources: projects/frontiers_article/publication_v1/data/e02_primary_effects.csv

## 11. Learned choices can disagree with the dynamic optimum

Results · 100 seconds

The M2 map compares learned choices in Neutral with the optimal dynamic policy. Each square is a parameter setting. In the 243 rust cells, learned choices favour masking while the optimal policy favours authenticity. Blue means agreement; gray means insufficient evidence for classification. These are counts of parameter settings, not percentages of children. The threshold table shows why a dynamic benchmark matters. In the static comparator, authenticity becomes worthwhile above about point seven one seven. Under the reference M2 conditions, the threshold falls to about point three eight four, and to point two six nine with greater recovery from stigma. Persistent acceptance creates future value; recovery reduces the cost of rejection. The optimal benchmark knows these possibilities. A finite learner must discover them through experience. Tests at selected disagreement settings extend to five thousand interactions, with documented sensitivity exceptions. This supports disagreement over the tested horizons, not proof of permanent entrenchment.

Sources: projects/frontiers_article/publication_v1/data/e03_grid_map.csv; projects/frontiers_article/publication_v1/data/e03_objective_thresholds.csv; src/gifted_masking/analysis/m2_optimal.py

## 12. Finding a receptive group does not ensure sustained expression

Results · 80 seconds

For M3, increasing the number of groups changes allocation even though the best available payoff stays fixed. With sixteen groups, the flat model masks on eighty-four percent of final-window interactions. Yet almost every learner has already experienced acceptance in the good group. Encounter and sustained use are different outcomes, with different denominators. The architecture comparison is crucial. Flat and hierarchical choices both show increasing masking. Sharing one masking action keeps masking near twenty-six percent. That change affects both information sharing and initial choice probabilities, so it does not isolate one psychological process. The finding is conditional: the effect of adding contexts depends strongly on how the learner represents the choices.

Sources: results/summaries/frontiers_m3_search_architectures_v1_curves.csv; results/summaries/frontiers_m3_search_architectures_v1_effects.csv

## 13. The learned boundary occurs before objective indifference

Results · 70 seconds

The comparison-cost result separates two boundaries. Expected rewards are equal at an objective cost of about point four seven one. The learned population crosses the displayed behavioural boundary earlier, near point three one three. Authenticity in the good group therefore retains an objective advantage at that learned crossing. The vertical axis is the fraction of learners whose most frequent individual action is authenticity in the good group. Its fifty-percent crossing is not the onset of majority masking. Multiple masking actions can together account for most interactions even when one authentic action is the most frequent individual action. The difference between these boundaries is specific to this representation and learning horizon.

Sources: projects/frontiers_article/publication_v1/data/e05_response_vs_bf.csv; projects/frontiers_article/publication_v1/data/e05_crossings.csv

## 14. M4  Formal results remain deferred

Results status · 20 seconds

For M4, there is no confirmatory E06 result to report. Implementation and diagnostic checks are available, but formal results remain deferred. Whether the feedback produces robust hysteresis, rather than transient path dependence, is still an open test.

Sources: projects/frontiers_article/ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md; projects/frontiers_article/presentation_prep_20261005/SIMULATION_GUIDE.md; src/gifted_masking/experiments/e06.py

## 15. Similar concealment can arise through different processes

Discussion · 40 seconds

Similar concealment can arise through different processes. M0 concerns what experience and feedback teach. M1 separates participation from the intensity of expression. M2 shows why persistent consequences require a dynamic benchmark. M3 separates encountering an opportunity from using it repeatedly. M4 adds a possible feedback from behaviour to the environment, with results still deferred. A single measure of masking cannot tell these explanations apart. The contribution is a set of distinct mechanisms and predictions to test.

Sources: projects/frontiers_article/integrated_article_20261004/ARTICLE.md

## 16. What should we measure next?

Discussion · 30 seconds

Empirical work should record expectations before an interaction and the feedback that follows. It should measure the degree of expression and the setting, and test whether learning transfers between them. Repeated observations can show which social consequences persist. These measurements would help distinguish the candidate mechanisms. The simulations provide those questions; observations of children must establish which processes actually operate.

Sources: projects/frontiers_article/integrated_article_20261004/ARTICLE.md
