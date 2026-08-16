# Article V1 Master Plan

**Freeze date:** 16 August 2026
**Document class:** authoritative long-term writing roadmap
**Current milestone:** `ARTICLE_V1_ARGUMENT_ARCHITECTURE_FROZEN`
**Next milestone:** `MODEL_METHODS_FROZEN`
**Scientific boundary:** maintained M0–M3 and frozen E01–E05 evidence

This plan governs the dependency order, responsibilities, claim boundaries, and
review gates for Article V1. It is not manuscript prose and does not reopen
frozen findings. The shorter controlling intellectual map is
[ARTICLE_V1_ARGUMENT_ARCHITECTURE.md](ARTICLE_V1_ARGUMENT_ARCHITECTURE.md).

## 1. Current project state

Stage 1 begins from repository branch `codex/frontiers-stage2-e06` at
`d22febd83e7e2e5594faf3a2aa8c36aac42c6bfa`. The frozen E01–E05 evidence,
analytic authority, four-figure publication layer, claim ledger, parameter
audit, and methodological position are present. The parameter-audit and
methodological-position files were untracked at the start of this stage and are
prerequisites of this architecture freeze.

The scientific evidence is not being rerun or reconsidered. Article V1 has four
maintained model rungs, five evidence families, four main figures, exact
objective comparators, and an explicit parameter position. The next task is to
write and freeze the Formal Model/Methods authority from this architecture
before any Results chapter is drafted.

## 2. Article-V1 scientific identity

Article V1 is an **existence-and-structure computational modelling paper**.
It demonstrates theoretically important ways in which finite-horizon learned
behaviour can diverge from an exact full-information objective benchmark.

It is not:

- a quantitatively calibrated psychological model;
- a fitted model of gifted children;
- a prevalence or population model;
- a complete characterization of the full parameter space;
- an empirical parameter-estimation study;
- a demonstration of irreversible or hysteretic masking.

Stylization limits external quantitative inference, but it permits controlled
existence claims, exact benchmark comparisons, tested-region claims, and
structural results. This is a substantive positive position, not an apology.

## 3. Frozen methodological position

The methodological position is governed by
[ARTICLE_V1_METHODOLOGICAL_POSITION.md](ARTICLE_V1_METHODOLOGICAL_POSITION.md).
The following rules bind every chapter:

1. No current parameter is quantitatively calibrated from gifted-child data.
2. Exact arbitrary reference values are legitimate coordinates for a stylized
   existence-and-structure model when clearly disclosed.
3. Provenance explains where a value came from; it does not justify that value.
4. The scientific content lies primarily in structural assumptions, qualitative
   relations, exact objective benchmarks, tested axes/regions, and contrasts
   between models and learners.
5. Results have three evidence levels: point/reference existence (Level 1),
   tested-region/axis evidence (Level 2), and structural/analytic results
   (Level 3). Level 2 applies only to dimensions actually swept.
6. Full-information comparators are oracles, not information-matched optima.
7. Baseline `lambda=1` is loss-neutral. Baseline phenomena must not be
   attributed to explicit loss aversion.
8. Five structural-rationale debts remain disclosed future work rather than V1
   blockers: M1 exact linear acceptance, deterministic M2 stigma entry, M2
   redemption `p/2`, M2 full-value restoration, and M3 hierarchical dual update.

## 4. Central research question

> **How can finite experience and progressively richer social-learning
> structures shift learned behaviour away from authenticity—including toward
> concealment—even when the corresponding full-information objective benchmark
> in the specified model continues to favour authenticity?**

This wording is deliberately about “how can,” not a complete “under exactly
which parameters” characterization. It accommodates E01’s sampling precursor,
E02’s action-representation result, E03’s dynamic-policy contrast, E04’s
context-discovery result, and E05’s learned/objective crossover separation
without promising mechanisms or robustness that were not tested.

## 5. Central contribution

> **Article V1 demonstrates, using exact objective benchmarks and a controlled
> M0–M3 progression, that learned concealment or reduced authenticity need not
> imply that concealment is objectively advantageous within the specified
> model.**

The contribution is stronger than “reinforcement learning can produce
masking.” The paper shows why behaviour and objective value must be separated,
and how the separation changes when the action set becomes graded, current
outcomes affect future social state, receptive contexts must be discovered, and
comparison cost changes. These structures are not all causally isolated; the
paper establishes a progression of bounded model results.

## 6. Model progression M0–M3

| Model | Question made newly answerable | Formal anchor | Manuscript role |
|---|---|---|---|
| M0 | Can finite adverse experience suppress sampling of an objectively worthwhile authentic action? | `Delta_0(p)=a+c-(1-p)(b+r)` and general `p*` | Minimal objective-versus-learning problem and E01 baseline. |
| M1 | What changes when disclosure is graded rather than binary? | `E[R(d)]` is affine; strict optima are endpoints | Shows that action vocabulary changes learning without creating an interior objective optimum. |
| M2 | What changes when current action changes future social state? | Exact Bellman optimum, Accepted-state dominance, Neutral dynamic-gap decomposition | Makes M2 the central conceptual step and supplies the E03 dynamic comparator. |
| M3 | What changes when the favourable context exists but must be discovered? | One-good-context objective `K`-invariance and general `bf*` | Separates option availability from finite discovery; contains E04 and E05. |

The sequence `M0 -> M1 -> M2 -> M3` is frozen. M2 is not “another
simulation”: it changes the mathematical object being optimized. M3 is not a
variant of M2: it introduces heterogeneous-context discovery rather than
persistent within-context state. E05 is a comparison-cost axis inside M3.

M4/E06 remains outside Article V1 evidence. It may be named only under
limitations, future structural work, or model extensions, without numerical V1
Results.

## 7. Experiment/evidence hierarchy E01–E05

### Supporting/minimal results

**E01** establishes the minimal early-feedback precursor: an initial rejected
authentic action reduces subsequent authentic sampling and raises the exactly
linked normalized-regret translation. It does not establish a persistent
final-mask contrast. E01 is background/supporting rather than headline
mechanism novelty.

**E02** establishes that five independent graded disclosure actions produce
more nonzero disclosure after rejection while reducing full-authentic and
optimal-endpoint selection. The Level-3 affine theorem prevents an
“objectively optimal compromise” reading. E02 is a representation-sensitive
supporting result, not evidence that graded disclosure solves masking.

### Results carrying the main argument

**E03** is the strongest direct result. In `243/357` tested grid cells,
aggregate final-window Neutral behaviour favours masking while exact
full-information dynamic programming favours authenticity; `107` cells match
and `7` are inconclusive. This is tested-grid coverage, not prevalence,
individual-policy frequency, or natural phase-space volume.

**E04** is the central discovery result. In the reference heterogeneous-context
environment, increasing the search problem strongly reduces receptive-context
authentic settling for flat and hierarchical learners, while the
one-good-context full-information optimum is `K`-invariant. The interpretation
is the conjunction of scarcity, discovery, finite sampling, and maintained
representation. The unswept `p_good`, `p_bad`, and `tau` dimensions remain
reference coordinates.

**E05** is the strongest quantitative displacement result. The flat `K=4`
modal-response crossing `0.312852` precedes the exact objective crossover
`8/17 ~= 0.470588`; authenticity retains about `0.134076` of objective
advantage at the learned crossing. The result is descriptive under the frozen
architecture. Its mechanism is unresolved, and the hierarchical crossing is
left-censored in the approved range.

## 8. Evidence levels

| Proposition | Level | Exact scope |
|---|---|---|
| M0 general objective boundary | 3 | Structural under the maintained reward equation. `43/60` is its reference realization. |
| M1 affine objective and endpoint result | 3 | Structural conditional on the exact linear acceptance function. |
| M2 Bellman comparator and exact identities | 3 | Structural/full-information dynamic-programming results for the maintained M2. |
| E01 early-feedback contrast | 1 | Two controlled receptivity cells and frozen learner settings. |
| E02 graded/binary contrasts | 1 | Frozen five-arm independent representation and selected cells. |
| E03 classification map | 2 in `p, eta` | Level 1 in all unswept payoff and learner dimensions. |
| M3 one-good-context `K`-invariance | 3 | Structural for fixed reward classes and one good context. |
| E04 `K` response | 2 in tested `K`/representation/control axes | Level 1 in unswept receptivity and learner settings. |
| General M3 objective `bf*` formula | 3 | Structural for `p_good>0` under the maintained comparison-cost placement. |
| E05 response/crossing | 2 in tested `bf` | Level 1 in architecture, `K`, horizon, learner settings, and other unswept dimensions. |

No simulation magnitude or location may be promoted to Level 3. No unswept
dimension may be described as robust.

## 9. Logical spine

1. Finite adverse experience can suppress later sampling of an objectively
   worthwhile action without creating a detectable final-mask contrast.
2. A graded independent action set can change disclosure behaviour and make
   endpoint identification harder without changing the endpoint-optimal static
   objective.
3. Persistent consequences make the objective dynamic; a substantial
   structured tested region shows aggregate learned masking against an exact
   authenticity-favouring dynamic optimum.
4. Heterogeneous contexts make discovery a prerequisite for exploiting
   authenticity; a good context can remain objectively best while finite
   learners become less likely to find and settle on it.
5. Comparison cost within M3 produces a learned transition before objective
   indifference, without identifying a unique mechanism for the displacement.
6. Learned concealment is therefore not a sufficient readout of objective
   advantage in the maintained environments.

This six-step sequence is the controlling one-page argument. Chapter prose may
expand it but may not add a seventh scientific claim without authority review.

## 10. End-of-paper belief target

### What the paper establishes

1. Learned behaviour and exact full-information objective value can diverge in
   the maintained stylized models.
2. The divergence is demonstrated at reference points and along explicitly
   tested axes/regions, not inferred from a single anecdotal run.
3. Persistent state makes continuation value necessary and yields the paper's
   strongest direct learner/objective region result.
4. Availability of a receptive context is not equivalent to finite discovery
   of that context.
5. A learned behavioural crossover need not equal an exact objective crossover.

### What the paper suggests

6. Observed concealment may reflect finite evidence acquisition, action
   representation, dynamic consequences, or discovery burden rather than an
   environment in which concealment is objectively best.

### What the paper explicitly does not establish

7. Human prevalence, empirical calibration, a complete divergence-set theorem,
   information-matched learner inefficiency, mechanism decomposition for E05,
   or M4 hysteresis.

## 11. Explicit non-claims

- E01 is not evidence that one rejection causes persistent final masking.
- E01 sampling and regret are not independent confirmations.
- E02 does not create an interior objective optimum, demonstrate smooth
  generalization, solve masking, or provide independent welfare evidence.
- `243/357` is not prevalence or natural parameter-space volume.
- The E03 full-information comparator is not information-matched.
- E04 does not show that `K` intrinsically causes masking, that scarcity alone
  is isolated, or that M3 literally models human movement among peer groups.
- E05’s learned crossing is not an analytic law or calibrated human threshold.
- Binary-softmax Proposition G2 does not explain or exclude the mechanism of
  E05’s eight-action across-child modal statistic.
- The baseline is not loss-averse: `lambda=1`.
- No numerical parameter is empirically calibrated; provenance is not
  justification.
- M4/E06 is not Article V1 evidence.

## 12. Main figure architecture

| Figure | First section | Main scientific purpose | Supports | Must not imply |
|---|---|---|---|---|
| 1 | Formal Model | Orient M0–M3 and their exact benchmark progression. | Why each rung changes the question/comparator. | Simulation evidence, empirical development, or an M4 rung. |
| 2 | Results I | Pair E01/E02 supporting behaviour with the M1 affine anchor. | Finite feedback and action representation matter. | Persistent E01 masking, independent regret confirmation, an optimal compromise, or graded welfare improvement. |
| 3 | Results II | Show the central E03 contrast region and exact objective Neutral Q gap. | Substantial structured tested-region disagreement. | Prevalence, information-matched failure, or causal decomposition. |
| 4 | Results III–IV | Connect E04 discovery burden with E05 learned/objective displacement inside M3. | Good-option availability differs from discovery; learned crossover can precede objective crossover. | A pure `K` effect, general robustness, hierarchical threshold, or identified displacement mechanism. |

The package is `SUFFICIENT_WITH_MINOR_EDITORIAL_CHANGE`. Four figures are
enough. No new figure is authorized unless a later chapter review identifies a
literal comprehension failure that cannot be solved by ordering, cross-reference,
or caption editing.

## 13. Manuscript dependency structure

```text
Argument architecture
        -> Formal Model / Methods
        -> Results
        -> Discussion
        -> Literature framing
        -> Parameter / technical appendix
        -> Introduction
        -> Abstract
        -> Integrated manuscript
        -> Submission package
```

Each downstream authority may consume only frozen upstream authorities. Results
cannot redefine a model; Discussion cannot strengthen Results; literature
framing cannot predetermine the completed argument; Introduction and Abstract
must summarize the stabilized manuscript rather than lead it.

## 14. Ten-stage manuscript plan

1. **Argument architecture** — freeze question, contribution, progression,
   evidence hierarchy, figures, claims, and boundaries. **Complete.**
2. **Formal Model / Methods** — write the formal and procedural authority,
   verify equations and parameter references, then freeze.
3. **Results** — report findings in scientific order from frozen artifacts,
   without re-teaching model semantics.
4. **Discussion** — interpret behaviour/objective separation, conditionality,
   real-world relevance, limitations, and future programmes.
5. **Literature framing** — locate the exact stabilized contribution using the
   approved literature authorities; no architecture-leading narrative.
6. **Parameter / technical appendix** — consolidate exact values, grids,
   transition tables, provenance, sensitivity status, tolerances, and
   reproducibility detail.
7. **Introduction** — state the completed problem, gap, question, and bounded
   contribution.
8. **Abstract** — compress the stabilized paper; introduce no new claim.
9. **Integrated manuscript pass** — remove repetition, reconcile terms,
   figures, tables, equations, citations, and claim IDs.
10. **Submission package** — render, audit, hash, and freeze all deliverables.

Items 5 and 6 remain in this order. The final literature narrative should
locate the already-stabilized scientific contribution; the appendix then
records exact technical coordinates supporting that narrative.

## 15. Stage gates

| Gate | Required decision |
|---|---|
| `ARCHITECTURE_FROZEN` | Question, contribution, M0–M3/E01–E05 roles, figures, and boundaries fixed. |
| `MODEL_METHODS_FROZEN` | Equations, semantics, comparators, experiment methods, and parameter references verified. |
| `RESULTS_FROZEN` | Every result maps to frozen evidence and obeys its wording ceiling. |
| `DISCUSSION_FROZEN` | Interpretation adds meaning without upgrading evidence or repeating Results. |
| `LITERATURE_FRAMING_FROZEN` | Citations locate the final contribution; no unsupported novelty or construct claim remains. |
| `APPENDIX_FROZEN` | Exact parameters, methods, provenance, limitations, and sensitivity status are complete. |
| `INTRODUCTION_FROZEN` | Question and contribution match the frozen paper. |
| `ABSTRACT_FROZEN` | All claims and numbers map to the integrated manuscript. |
| `MANUSCRIPT_INTEGRATED` | Cross-section consistency and repetition review pass. |
| `SUBMISSION_READY` | Final numerical, mathematical, citation, claim, provenance, and render audits pass. |

No agent should generate a complete Article V1 manuscript before the
Model/Methods, Results, Discussion, literature framing, and appendix have
individually stabilized. A premature full draft would harden framing before its
dependencies are reviewed and encourage later preservation of prose that only
looks authoritative.

## 16. Methods responsibilities

Use the section strategy **Formal Model and Methods** unless journal formatting
requires separate adjacent `Formal Model` and `Methods` sections.

The chapter must establish, before Results:

- model variables, objective rewards, learner Q update, numerically stable
  softmax action selection, `alpha`, `tau`, `q0`, and baseline `lambda=1`;
- environmental objective reward versus learner-side transformed/learned value;
- M0 general expected-reward gap and objective boundary before `43/60`;
- M1 disclosure grid, exact linear acceptance assumption, affine expected
  reward, and endpoint consequence;
- M2 states, reward/transition order, Q-learning update, discounting, and exact
  full-information dynamic comparator;
- M3 context/action representations, reward classes, comparison-cost placement,
  one-good-context `K`-invariant objective, and general/reference crossover;
- full-information oracle status of comparators;
- stylized status of M2 states and the five structural-rationale debts;
- experiments, outcomes, final windows, inferential unit, uncertainty methods,
  seed strategy, artifact provenance, and historical reproducibility limitation;
- arbitrary-reference interpretation and the separation of provenance from
  justification.

Exact numerical provenance should be summarized only where essential and
otherwise deferred to the appendix.

## 17. Results responsibilities

Results report what happened and how it compares with the already-defined
objective anchors. They do not repeatedly explain model semantics.

Frozen conceptual units:

1. **Finite adverse feedback changes subsequent sampling** — E01, including
   the no-detectable-final-mask boundary and linked regret identity.
2. **Graded independent actions alter disclosure without creating an interior
   optimum** — E02 plus a concise reference to the Methods theorem.
3. **Persistent consequences generate a learner/dynamic-objective contrast
   region** — E03 as the central result.
4. **A valuable context can remain undiscovered as the reference search problem
   expands** — E04 with full control conditionality.
5. **Learned comparison-cost transition precedes objective indifference** —
   E05 descriptively, without mechanism proof.

Every number must map to a frozen source row. Every interval must name the
master-seed inferential unit. No M4/E06 result is permitted.

## 18. Discussion responsibilities

Discussion answers what the results mean:

- behaviour is not a direct readout of objective value;
- finite action-dependent evidence acquisition can shape learning trajectories;
- action representation changes exploration and identification;
- persistent consequences require dynamic valuation;
- context availability differs from context discovery;
- learned and objective transitions are distinct objects;
- human masking must not be interpreted through simulation frequencies;
- model conclusions are conditional on simplified structures and arbitrary
  reference coordinates;
- structural robustness, formal characterization, and empirical calibration are
  separate future programmes.

Discussion must not repeat numerical Results, claim E05 mechanism identification,
convert model implications into human predictions, or use M4/E06 evidence.

## 19. Literature strategy

Literature informs architecture early; the final literature narrative is written
late. Existing audited literature may motivate qualitative model relations and
terminology during Model/Methods drafting. No new Stage-1 search is authorized.

After Results and Discussion stabilize, literature framing should:

- distinguish generic hot-stove, bandit, search, and representation prior art
  from the paper’s existence-and-structure synthesis;
- ground gifted visibility management and context heterogeneity without
  calibrating model parameters;
- motivate comparison cost without treating `bf` as measured BFLPE;
- locate the exact completed contribution rather than preselecting a novelty
  story.

## 20. Parameter-appendix strategy

The appendix carries exact choices that would obstruct the conceptual Methods
narrative:

- payoff constants and learner defaults;
- dimensionless/scale relationships;
- every E01–E05 range and grid;
- `n`, `T`, final windows, master seeds, RNG hierarchy, and inferential unit;
- computational tolerances and deterministic comparator checks;
- arbitrary-reference status, provenance, and justification taxonomy;
- completed and unexecuted sensitivity;
- exact M2 transition table and transition order;
- `RATIONALE_UNKNOWN` structural assumptions;
- general formulas before reference realizations;
- E01–E03 historical generator-source limitation;
- E03 grid-measure qualification and E05 hierarchical censoring.

The appendix must never present exact provenance as scientific justification or
turn reference values into calibrated quantities.

## 21. Future-work boundary

### A. Structural robustness / model comparison

Alternative M1 acceptance functions and structured generalization; probabilistic
or graded M2 stigma entry; alternative redemption and restoration functions;
alternative M3 hierarchical updates; other explicit structural ablations. These
tests may assess whether current results depend on `RATIONALE_UNKNOWN` choices,
but they are not current V1 evidence.

### B. Formal characterization

Study the divergence set

```text
Theta_div = {theta : pi_L(theta) != pi_O(theta)}
```

including boundaries, monotonicity, connectedness, asymptotics, dimensional
reduction, limiting cases, and the mechanism/geometry of learned crossover
displacement. Article V1 supplies selected exact benchmarks, not a complete
theory of this set.

### C. Empirical calibration

```text
real observations
    -> observable definitions
    -> model summaries
    -> effective parameter or regime inference
    -> uncertainty
    -> empirical parameter distribution
    -> real-world regime frequency
```

This programme requires validated observables, longitudinal/contextual data,
identifiability analysis, fitting, and uncertainty. Only then could a
real-world frequency question be asked. Bootstrapping quantifies uncertainty
around an estimator; it does not itself identify psychological parameters.

M4/endogenous receptivity is also future model-extension work. It is not a
fourth future-work programme and contributes no V1 numerical evidence.

## 22. Governance / authority rule

The manuscript-construction authority order is:

```text
Frozen scientific evidence / artifacts
        -> Methodological position
        -> Argument architecture
        -> Master plan
        -> Frozen chapter authorities
        -> Integrated manuscript
```

No later prose document may silently override frozen evidence. If prose
conflicts with evidence, prose loses. A later authority may narrow a claim but
may not strengthen it beyond its evidence level without a new explicit review.

Chapter work must begin with a plan and acceptance criteria, update its relevant
authority before integration, update current-state/backlog pointers, and pass
deterministic verification. No stochastic run or semantic/parameter change is
authorized by this roadmap.

## 23. Exact next stage

**Stage 2 — Formal Model / Methods.**

Create a chapter authority—not yet a complete manuscript—that defines the
formal M0–M3 progression, shared learner, exact objective comparators,
experiment/inference methods, parameter interpretation, and reproducibility
boundary listed in Section 16. Verify every equation against
[ARTICLE_V1_ANALYTIC_RESULTS.md](ARTICLE_V1_ANALYTIC_RESULTS.md), every semantic
claim against the maintained model and consistency audit, and every numeric
method detail against frozen configs/manifests and the parameter register.

Stage 2 must stop at `MODEL_METHODS_FROZEN`. It must not draft Results,
Discussion, Introduction, literature review, Abstract, or a complete manuscript.
