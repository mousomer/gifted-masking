# PowerPoint storyboard: 12-minute slot

Revised 6 October 2026. **Eleven main slides, 11 minutes of planned speaking, one minute reserved.** Eight backup slides sit outside the timed talk. Timing is a rehearsal target. The author-directed first four slides are documented in [OPENING_AND_M0_PLAN.md](OPENING_AND_M0_PLAN.md), including diagram drafts, exact theory and simulation distinctions, and visual plans. The eleven main slides are now built and visually reviewed. The earlier S01 draft remains preserved. Exact delivered titles, text, tables, notes, and native chart values are recorded in [RENDERED_CONTENT.json](main_deck_20261006/RENDERED_CONTENT.json); the body/visual descriptions below remain the conceptual authoring plan.

The detailed explanations remain in [SIMULATION_GUIDE.md](SIMULATION_GUIDE.md). [SLIDE_SPEC.json](SLIDE_SPEC.json) contains the structured plan; [SOURCE_INDEX.json](SOURCE_INDEX.json) resolves source IDs. Main-slide notes below form the short spoken narrative. Full equations, designs, and additional findings stay in the guide and backups.

## Timing

| Slide | Topic | Duration | Cumulative finish |
| --- | --- | ---: | ---: |
| S01 | What mechanisms could explain masking? | 0:35 | 0:35 |
| S02 | A close second | 0:30 | 1:05 |
| S03 | Learning from social experience | 0:45 | 1:50 |
| S04 | M0: masking or authenticity | 1:20 | 3:10 |
| S05 | M1 / E02: more participation can mean less expression | 1:25 | 4:35 |
| S06 | M2 / E03: persistent consequences change optimal behaviour | 1:40 | 6:15 |
| S07 | M3 / E04: finding a receptive context does not ensure repeated use | 1:40 | 7:55 |
| S08 | M3 / E05: learned and objective boundaries differ | 1:15 | 9:10 |
| S09 | M4 / E06: behaviour changes receptivity | 0:45 | 9:55 |
| S10 | What the evidence establishes | 0:35 | 10:30 |
| S11 | Similar concealment can require different explanations | 0:30 | 11:00 |
| Reserve | Pauses or one question | 1:00 | 12:00 |

Start the conclusion at 10:30 and finish at 11:00. Keep the first four slides within 3:10. The 35-second evidence slide and 30-second conclusion accommodate Dash. Rehearse with the figures; backup slides remain outside the timed talk.

## Main talk

### S01. What mechanisms could explain masking?

**Section:** Opening. **Time:** 35 seconds (0:00–0:35).

**On-slide content**

- Research documents ability concealment among gifted learners.
- Patterns vary across age and social settings.
- What mechanisms could explain how masking emerges and changes over time?

**Visual:** Generated transparent illustration of a young child standing apart from four interacting peers. Saved as assets/child_apart_from_peers.png; prompt and provenance in assets/ASSET_SOURCES.json.

**Visible sources:** Swiatek (1995) · Chan (2005) · Foust, Rudasill & Callahan (2006)

**Speaker notes:** Research documents gifted learners concealing their abilities and managing how much others see. Patterns vary across age and social settings. The image introduces that social situation while leaving its explanation open. Our question is what mechanisms could make masking emerge and change over time. We will examine candidate processes through simple computational models, moving from individual learning to persistent social consequences and different peer contexts. These are explanations to investigate, rather than a diagnosis of any particular child.

**Sources:** OPENING_LITERATURE, LITERATURE_AUDIT, ARTICLE, RDS, OPENING_M0_PLAN. Resolve source IDs through SOURCE_INDEX.json.

**Detailed production plan:** [Opening and M0 plan](OPENING_AND_M0_PLAN.md).

### S02. A close second

**Section:** Illustration. **Time:** 30 seconds (0:35–1:05).

**On-slide content**

- “Second. Close second, yeah!”
- Social expectations can shape how much ability a child displays.

**Visual:** Actual still from the school race in The Incredibles (2004), with Dash among the other runners. Saved as assets/dash_school_race.jpg; source and quotation URLs in assets/ASSET_SOURCES.json.

**Visible sources:** The Incredibles (2004), Pixar / Walt Disney Pictures

**Visible qualification:** Film illustration of explicit social instruction; parental instructions are not directly implemented in the current models.

**Speaker notes:** Dash could easily win this race. His family encourages him to participate, but also to hold back and finish a close second. His performance reflects both his ability and instructions about how much of it to reveal. Here, the instruction is explicit. Our question is what other mechanisms could produce similar restraint, including through repeated social experience.

**Sources:** OPENING_M0_PLAN. Resolve source IDs through SOURCE_INDEX.json.

**Detailed production plan:** [Opening and M0 plan](OPENING_AND_M0_PLAN.md).

### S03. Learning from social experience

**Section:** Foundations. **Time:** 45 seconds (1:05–1:50).

**On-slide content**

- Outcomes update expectations about an action.
- Higher-valued actions become more likely, with continued exploration.
- The models vary the available choices and their social consequences.

**Visual:** Editable choice → outcome → value update → next choice diagram. Plain-language labels. Use the diagram in OPENING_AND_M0_PLAN.md; mathematical updates remain in notes/backup.

**Visible qualification:** Environmental reward and learned value are distinct

**Speaker notes:** The shared assumption is that experience changes expectations. A learner chooses an action, receives an outcome, and updates the value it assigns to that action. Actions with higher learned values become more likely, but exploration continues. In the basic model, the learner receives feedback only about the action it chose. Avoiding an action can therefore restrict new information about it. Later models change the choices or the social consequences; M2 also learns about future value. A simulation step is an interaction, not a calibrated year of a child’s life.

**Sources:** CORE, PARAMS, ARTICLE, OPENING_M0_PLAN. Resolve source IDs through SOURCE_INDEX.json.

**Detailed production plan:** [Opening and M0 plan](OPENING_AND_M0_PLAN.md).

### S04. M0: masking or authenticity

**Section:** M0 / E01. **Time:** 80 seconds (1:50–3:10).

**On-slide content**

- Two-armed bandit: certain masking reward; probabilistic authentic reward.
- Theory: authenticity has higher expected payoff when p > 0.717.
- Simulations: initial rejection reduces subsequent authentic sampling by 2.58 pp.
- Simulations: extra feedback reduces final masking by 11.81 pp.

**Visual:** Editable two-arm diagram in the top half: masking → 0.75; authenticity → accepted with p, 1.60, or rejected with 1−p, −1.40; update chosen value. Lower left: analytic threshold and p=.75 example (auth .85 vs mask .75). Lower right: two archived effect contrasts and confidence intervals, explicitly labelled by outcome/window. Staged reveal if practical; static layout must remain readable. See OPENING_AND_M0_PLAN.md.

**Visible qualification:** p=.75/.85, equally pooled. Sampling: −2.58 pp [−3.58,−1.59]; feedback final masking: −11.81 pp [−12.66,−10.97]. Final-window history CI spans zero.

**Speaker notes:** M0 is a two-armed bandit. At each interaction, the learner chooses masking or authenticity. Masking always pays 0.75. Authenticity pays 1.6 when accepted and minus 1.4 when rejected; acceptance has probability p. That probability stays fixed. The payoff equations show that authenticity has the higher average reward whenever p exceeds about 0.717. At p=0.75, its expected reward is 0.85, compared with 0.75 for masking. That is the objective benchmark. The simulations ask what a learner discovers from limited experience. Across the tested p=0.75 and 0.85 conditions, initial rejection reduces subsequent authentic sampling by 2.58 percentage points. Giving authentic feedback even while the learner masks reduces final masking by 11.81 points, without awarding the unchosen payoff. The initial-history comparison alone does not establish a lasting final-window difference. The supported mechanism is that experience and access to information can change action selection even when authenticity is objectively worthwhile.

**Sources:** M0, E01_CODE, E01_PRIMARY, E01_INTERVENTIONS, FIG4, ARTICLE, E01_CONFIG, OPENING_M0_PLAN. Resolve source IDs through SOURCE_INDEX.json.

**Detailed production plan:** [Opening and M0 plan](OPENING_AND_M0_PLAN.md).

### S05. M1 / E02: more participation can mean less expression

**Section:** M1 / E02. **Time:** 85 seconds (3:10–4:35).

**On-slide content**

- Five disclosure levels replace the binary choice
- Any disclosure rises by 25.50 points
- Full-authentic endpoint use falls by 32.87 points

**Visual:** Native horizontal contrast chart for two quantities only, with 95% intervals. Small action-set label d=0,.25,.5,.75,1. Move variance curves and additional outcomes to the appendix/guide.

**Visible qualification:** Independent arms; rejected stratum, p=.75/.85 pooled. Any disclosure: +25.50 pp [25.30,25.71], post-initial. Full authenticity: −32.87 pp [−34.20,−31.53], final window.

**Speaker notes:** M1 introduces partial disclosure: a learner can express a quarter, half, or three quarters, as well as nothing or everything. Each level has its own learned value. Success at a partial level does not automatically teach the learner that full expression is safe. E02 compares these five actions with binary choice following initial rejection. Graded options increase the frequency of some disclosure by twenty-five and a half percentage points, but reduce final-window full-authentic use by nearly thirty-three points. Average disclosure intensity also falls in the pooled comparison. The environmental payoff remains linear, so full authenticity is still the best endpoint in these cells. The important distinction is between participation and expression: providing more ways to participate does not automatically produce fuller expression.

**Sources:** M1, E02_CONFIG, E02_PRIMARY, E02_EFFECTS, FIG5, ARTICLE. Resolve source IDs through SOURCE_INDEX.json.

### S06. M2 / E03: persistent consequences change optimal behaviour

**Section:** M2 / E03. **Time:** 100 seconds (4:35–6:15).

**On-slide content**

- Actions can establish acceptance or adverse social standing
- Recovery lowers the objective receptivity threshold
- Learned masking still disagrees with the optimum in 243 of 357 cells

**Visual:** Three-state diagram with only the main branches. Beside it use a small threshold comparison: static .717; dynamic .384 at eta=0 and .269 at eta=.8. Use a single 243/357 annotation, not a second full figure.

**Visible qualification:** 243/357 counts parameter cells, not learners. Neutral-state classification uses exposure criteria. Full-information discounted benchmark; finite-horizon persistence.

**Speaker notes:** M2 adds social memory to the environment. A learner can be Neutral, Accepted, or Stigmatized. An action now affects both its current reward and future opportunities. Successful authenticity can establish acceptance, while rejection can produce persistent adverse standing. Escape allows recovery. We therefore calculate the optimal policy from the known rewards and transitions, rather than judging behaviour by immediate payoff alone. Under the reference model, the receptivity needed to make authenticity optimal in Neutral falls from about point seven one seven in the static model to point three eight four, and to point two six nine with greater recovery. Yet the finite learners still favour masking where the dynamic optimum favours authenticity in 243 of 357 tested parameter cells. That disagreement persists at five selected settings through five thousand steps. Persistence is demonstrated over those tested horizons, with explicit sensitivity exceptions.

**Sources:** M2, M2_ORACLE, E03_THRESHOLDS, E03_GRID, E03_CONFIG, FIG2, FIG6, ARTICLE. Resolve source IDs through SOURCE_INDEX.json.

### S07. M3 / E04: finding a receptive context does not ensure repeated use

**Section:** M3 / E04. **Time:** 100 seconds (6:15–7:55).

**On-slide content**

- One receptive context remains available as K increases
- At K=16, flat learners show 84.19% final masking
- 99.72% nevertheless experienced acceptance there
- A shared masking action keeps masking near 26%

**Visual:** One native chart of masking versus K for flat, hierarchical, and global-mask architectures, from Figure 9A. Add the flat K=16 ever-acceptance statistic as a clearly labelled annotation. Use three compact architecture labels instead of a second full diagram.

**Visible qualification:** One good context, fixed identity. Encounter: fraction of learners over the whole run. Masking: final-window action fraction. Endpoint values are descriptive means.

**Speaker notes:** M3 asks the learner to choose where to interact as well as whether to express itself. One context is receptive, while the others are less receptive. The best available reward stays fixed as we add contexts. In the flat representation, each context has separate masking and authentic actions. At sixteen contexts, final masking reaches eighty-four percent, even though almost every learner has already experienced acceptance in the receptive context. First success therefore does not guarantee sustained later use. Representation matters: choosing a context and then a behaviour shows a similar masking increase, but pooling masking into one shared action keeps masking near twenty-six percent. We cannot conclude that more contexts universally cause masking. The supported result is that how choices share experience changes how an available opportunity gets used.

**Sources:** M3, E04_CONFIG, E04_CURVES, E04_EFFECTS, FIG9, ARTICLE. Resolve source IDs through SOURCE_INDEX.json.

### S08. M3 / E05: learned and objective boundaries differ

**Section:** M3 / E05. **Time:** 75 seconds (7:55–9:10).

**On-slide content**

- Comparison cost reduces accepted authenticity in the good context
- Learned modal-population crossing: .313
- Objective payoff crossover: .471

**Visual:** Native response curve based on Figure 10A with two labelled vertical boundaries and the archived learned-crossing interval. Keep the response-axis definition explicit.

**Visible qualification:** Flat K=4, lambda=1. Learned crossing .312852, 95% CI [.307836,.316918]. Modal-population crossing, not majority-masking onset.

**Speaker notes:** E05 adds a comparison cost to accepted authenticity in the good context. We can calculate exactly when that cost removes the good context’s objective advantage: approximately point four seven one. But the flat four-context learner population crosses its behavioural boundary much earlier, near point three one three. At that point, authenticity still has positive objective advantage. The behavioural boundary is specific: it is where half the learners have the good-authentic action as their most frequent individual action. It is not where total masking first becomes a majority. Several separate mask actions can together account for most behaviour even when one authentic action is individually the most frequent. This distinction lets us measure a learned boundary without confusing it with environmental indifference.

**Sources:** M3, E05_CROSSINGS, E05_RESPONSE, E05_CELLS, FIG10, ARTICLE. Resolve source IDs through SOURCE_INDEX.json.

### S09. M4 / E06: behaviour changes receptivity

**Section:** M4 / E06. **Time:** 45 seconds (9:10–9:55).

**On-slide content**

- Accepted authenticity increases future receptivity
- Rejection and masking decrease it under the specified rules
- The formal continuation experiment remains deferred

**Visual:** Native three-row direction-of-change table. No response curve or simulated loop. Visibly label this slide 'Implemented extension; E06 deferred'.

**Visible qualification:** Implemented extension; E06 deferred. No confirmed hysteresis claim.

**Speaker notes:** M4 closes a feedback loop. Acceptance after authenticity raises future receptivity; rejection and masking lower it according to specified rates. Current receptivity determines the outcome before it updates. The learner still stores action values rather than values conditioned on receptivity, so this is an endogenous, nonstationary bandit. Its proposed experiment carries learning and receptivity through increasing and decreasing control values, with reset and placebo comparisons. Diagnostic smoke work exists, but the formal E06 evidence remains deferred. Hysteresis is not yet established.

**Sources:** M4, E06_CODE, E06_SMOKE, E06_STANDARD, CURRENT_STATE. Resolve source IDs through SOURCE_INDEX.json.

### S10. What the evidence establishes

**Section:** Evidence. **Time:** 35 seconds (9:55–10:30).

**On-slide content**

- E01–E05 use five independent master replications
- Benchmarks distinguish environmental value from learned behaviour
- Results apply to specified models and tested conditions

**Visual:** Native two-column table: established model result versus remaining test. Limit to generalization across actions, broader sensitivity, and E06 qualification.

**Visible qualification:** Model-relative evidence; sensitivity is bounded. Historical E01–E03 generator-source reconstruction remains incomplete.

**Speaker notes:** Read each model along three columns: what can be chosen, what the environment carries forward, and what the learner remembers. M2 explicitly conditions its choices on social state. M3 chooses a context–behaviour pair. M4 changes the environment, but still learns two action values. E01 to E05 each use five master replications. These results establish model behaviours; human mechanisms require empirical tests.

**Sources:** ARTICLE, E03_CONFIG, CURRENT_STATE. Resolve source IDs through SOURCE_INDEX.json.

### S11. Similar concealment can require different explanations

**Section:** Conclusion. **Time:** 30 seconds (10:30–11:00).

**On-slide content**

- Experience changes what gets sampled
- Representation changes what gets learned
- Persistent consequences change what is worthwhile

**Visual:** Large editable takeaway text. Optional small labels linking experience to E01, representation to E02/E04, and opportunity value to E03/E05. No new chart.

**Visible qualification:** Empirical implications are testable hypotheses

**Speaker notes:** Similar concealment can arise through different processes. The models suggest questions to test: what does the child expect, which experiences change that expectation, does learning transfer between situations, and what consequences persist? The contribution is a set of candidate mechanisms and predictions for empirical study.

**Sources:** ARTICLE, RDS. Resolve source IDs through SOURCE_INDEX.json.

## Backup slides: outside the timed talk

### A01. Reference parameters and run designs

**Section:** Technical appendix. **Time:** 90 seconds only if requested.

**On-slide content**

- Shared payoffs: b=1, a=.6, c=.25, r=2
- Learner: α=.1, τ=.25, λ=1, Q0=0
- M2 adds γ=.9, b2=.5, r2=2.5, δ=.02
- E01/E02/E04/E05: n=500, T=2000; E03 baseline: n=160, T=1000

**Visual:** Editable table retaining all five master-seed ranges from the guide.

**Speaker notes:** Reference kernel defaults and executed experiment settings differ. The exact config is the experiment authority. The final window is ceil(.2T) steps. The E03 sensitivity horizons and populations are separate runs. E06 smoke is one master and must never be placed in the five-master confirmatory row.

**Sources:** PARAMS, E01_CONFIG, E02_CONFIG, E03_CONFIG, E04_CONFIG, E05_CONFIG, E06_SMOKE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A02. Static reward and weighting boundaries

**Section:** Technical appendix. **Time:** 120 seconds only if requested.

**On-slide content**

- Δ0(p)=a+c−(1−p)(b+r)
- p*=1−(a+c)/(b+r)
- p*λ=(b−c+λ(r−a))/(b+a+λ(r−a))
- The transformed formula assumes the specified reward signs

**Visual:** Native editable equations and a short reference-value table for λ=.5,1,2,2.5.

**Speaker notes:** The subjective threshold assumes nonnegative mask and accepted rewards and negative rejected authenticity. The helper permits lambda=0 in the transform, while formulas dividing by lambda need separate handling. At r<a the rejected reward is positive, so multiplying it by lambda would be incorrect. A transformed-expectation threshold does not guarantee a finite learner population crosses there.

**Sources:** M0, CORE, ARTICLE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A03. Graded disclosure has an affine objective

**Section:** Technical appendix. **Time:** 120 seconds only if requested.

**On-slide content**

- E[R(d)]=b−c+dΔ0(p)
- Var[R(d)]=(b+r)²(1−p)d[1−(1−p)d]
- At authenticity-optimal cells, normalized regret equals 1−mean(d)
- The intensity identity uses the full trajectory

**Visual:** Editable equations and the p=.75 worked half/full disclosure table.

**Speaker notes:** At half disclosure the two realized rewards are 1.175 and −1.825, with acceptance .875. At full disclosure they are 1.6 and −1.4, with acceptance .75. The lower-variance description holds for the reported .75/.85 cells. The variance function is not monotonically increasing in d for every receptivity, so preserve that qualification.

**Sources:** M1, E02_CODE, ARTICLE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A04. M2 transition ordering and dynamic benchmark

**Section:** Technical appendix. **Time:** 120 seconds only if requested.

**On-slide content**

- Neutral authentic outcomes establish the next state
- Turnover applies only to current Accepted states
- Escape applies only to non-redeemed Stigmatized paths
- The oracle uses untransformed reward and discounted continuation

**Visual:** Full native state/action/reward/transition table and the Bellman equation. Use two slides only if the user explicitly approves a different slide count.

**Speaker notes:** Both accepted-state actions share the same transition probabilities, so authenticity dominates there by .85. The remaining four deterministic policies supply an independent envelope check. The finite learner and full-information oracle do not have equal information. Dynamic disagreement classification is not a reported cumulative dynamic-regret estimator.

**Sources:** M2, M2_ORACLE, FIG2, E03_CONFIG, ARTICLE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A05. Complete E03 sensitivity outcomes

**Section:** Technical appendix. **Time:** 120 seconds only if requested.

**On-slide content**

- Five disagreement sentinels and five masters give 25 classifications
- Baseline plus 14 separate perturbations
- Exceptions occur at α=.03, τ=.6, and γ=.5
- The boundary/agreement control is outside this denominator

**Visual:** Figure 8's complete 15-row matrix. Rebuild as an editable table or retain an unclipped readable full figure if author prefers.

**Speaker notes:** The full set changes n, T, final-window fraction, alpha, tau, lambda, Q0, and gamma one at a time. All remaining classifications in the exception rows agree with the oracle and none are inconclusive. This evidence is stronger than a single horizon but narrower than robustness to arbitrary joint changes.

**Sources:** FIG8, E03_CELLS, E03_CONFIG, ARTICLE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A06. A modal authentic arm can coexist with majority masking

**Section:** Technical appendix. **Time:** 90 seconds only if requested.

**On-slide content**

- Illustrative final counts: good-authentic arm 120
- Four separate masking arms have 70 selections each
- The authentic arm is individually modal
- Total masking is 280/400 = 70%

**Visual:** Native five-category count chart. Clearly label it a constructed arithmetic example, with other arms at zero.

**Visible qualification:** Constructed arithmetic example

**Speaker notes:** The example has 400 final-window actions, one good-authentic arm selected 120 times, and four mask arms selected 70 times each. Authenticity is the most frequent single arm, but total masking is 70%. This explains why a learned modal-population threshold cannot be read as the onset of majority masking. These counts illustrate a measurement distinction and are not a sampled trajectory.

**Sources:** M3, E05_CODE, ARTICLE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A07. Replication and source provenance

**Section:** Technical appendix. **Time:** 120 seconds only if requested.

**On-slide content**

- Semantic cell/family IDs determine stream identity
- E02 pairs architectures; E05 pairs costs within architecture
- Scalar contrasts use five master estimates
- E04/E05 historical source bundles are recovered; E01–E03 remain incomplete

**Visual:** Native experiment/stream/inference table based on Appendix A of the article.

**Speaker notes:** Vectorized child draws belong to cell or family streams, not separately recorded child generators. Changing population size can change a child's later draws. Whole-curve bootstrap preserves E05's across-cost pairing. Artifact integrity and historical-source reconstruction are separate claims. The manifest's historical environment should not be confused with the interpreter used for this presentation preparation.

**Sources:** ARTICLE, CORE, E01_CODE, E02_CODE, E05_CODE. Resolve source IDs to paths and citations through SOURCE_INDEX.json.

### A08. E06 controls and qualification requirements

**Section:** Technical appendix. **Time:** 120 seconds only if requested.

**On-slide content**

- Inherited state versus reset-at-every-segment paths
- Active km versus actual km=0 placebo
- Fast versus slow ramps and longer dwell times
- Independent masters, valid crossings, and uncertainty before adjudication

**Visual:** Native table comparing smoke, staged standard, and staged qualification designs. Mark both latter tiers unexecuted/deferred.

**Visible qualification:** Deferred designs, not completed findings

**Speaker notes:** Smoke has no bootstrap inference. The staged standard includes nine scenarios and five masters, with primary segment lengths 500 and 1000. Qualification adds longer segments and learner-parameter changes. Standard and qualification require separate authorization and evidence adjudication. Keep path dependence, bistability, finite ramp loops, and irreversible entrenchment distinct.

**Sources:** E06_CODE, E06_SMOKE, E06_STANDARD, E06_QUALIFICATION, E06_DESIGN. Resolve source IDs to paths and citations through SOURCE_INDEX.json.
