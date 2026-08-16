# Research Design Specification: Frontiers Article

**Sub-project:** Gifted Masking — Frontiers Original Research Article  
**Target:** *Frontiers in Psychology*, Educational Psychology  
**Article type:** Original Research  
**Status:** Active  
**Version:** 0.6
**Current stage:** short-article architecture and evidence routing complete
**Article V1 status:** `READY_FOR_MANUSCRIPT_EXTRACTION`

## 1. Purpose

This RDS governs the conversion of the maintained reinforcement-learning model
ladder and existing article materials into a complete, reproducible, and
submission-ready Original Research article.

The article's central contribution is a progression of ability-concealment
learning environments in which behavioural findings are evaluated against
explicit analytic or dynamic-programming objective benchmarks. This makes
distinct forms of learned-objective divergence measurable rather than inferred.
The primary Article V1 evidence set is E01–E05. M4/E06 is deferred to future
work and is not a primary result of this article.

## 2. Authority And Relationship To Repository Design

This document is the design source of truth for:

- article scope and narrative;
- claim-to-evidence requirements;
- required analyses and robustness gates;
- manuscript structure and word budget;
- main and supplementary figures;
- article-specific reproducibility artifacts;
- Frontiers submission readiness.

It is not authoritative for model semantics. Model equations, transitions, RNG
rules, and maintained implementation behavior remain governed by repository
`AGENTS.md`, the preserved legacy scripts, `ARCHITECTURE.md`, and verified model
code. If the article requires a semantic model change, that change must be
proposed and reviewed separately before this RDS is updated.

## 3. Research Objective

The short Article V1 will present five linked evidential steps:

1. Early adverse feedback can suppress later authentic sampling even when
   authenticity has the higher objective value.
2. Information-restoring interventions test whether reduced sampling restricts
   corrective experience, without treating E01 final masking as a finding.
3. Graded disclosure can reduce the exposure cost of exploration without being
   a generally optimal endpoint under the current linear reward model.
4. Stigma persistence and multidimensional context search enlarge the
   conditions under which masking is learned or maintained.
5. Comparison cost can displace a learned behavioural boundary from the exact
   objective boundary.

The models identify candidate mechanisms. They do not estimate prevalence in
gifted children, establish clinical categories, or demonstrate educational
intervention effects.

## 4. Intended Contribution To Educational Psychology

The manuscript must foreground learning from peer feedback, avoidance,
exploration, motivation, self-presentation, and context-dependent information.
Gifted education supplies the substantive setting; the theoretical contribution
is a sequential-learning account of how educational environments may stabilize
reduced visibility.

Every applied implication must connect explicitly to at least one core
educational-psychology construct and be written as a testable prediction rather
than an established human effect.

## 5. Scope

### 5.1 In scope

- M0–M3 as represented by frozen E01–E05 evidence;
- analytic reward and policy benchmarks;
- frozen E01–E05 Monte Carlo evidence and existing uncertainty estimates;
- deterministic figure generation and source-data export;
- selective use of the preserved long-form chapters as source material;
- a Frontiers-compliant DOCX, PDF, figures, tables, supplement, and archive.

### 5.2 Out of scope

- empirical claims about the prevalence of masking in real children;
- causal claims about educational interventions;
- psychometric validation or clinical classification;
- silent changes to model semantics or default parameters;
- fitting the models to human participant data;
- large exploratory sweeps without a prespecified claim or decision rule;
- decorative imagery that does not communicate theory or evidence.
- M4/E06 as a primary Article V1 result;
- new experiments, result regeneration, or model redesign during manuscript
  construction.

## 6. Working Inputs And Output Authority

### 6.1 Manuscript inputs

- The assertive Frontiers DOCX is the formatting base.
- The literature, model-cascade, results-by-finding, and discussion Markdown
  chapters are long-form source material.
- The existing submission figures are draft evidence displays, not immutable
  publication artifacts.

### 6.2 Evidence inputs

- `results/raw/` contains primary maintained simulation units.
- `results/summaries/` contains recomputed estimates and benchmark results.
- `results/manifests/` contains run and reproducibility metadata.
- Repository tests and analytic scripts establish implementation invariants.

### 6.3 Final outputs

- one submission-ready manuscript DOCX;
- one visually verified PDF;
- separate main-figure TIFF files;
- supplementary material;
- editable manuscript tables;
- figure source-data tables and deterministic generation scripts;
- an archived code and evidence release with a permanent identifier;
- a completed Frontiers submission checklist.

## 7. Article Design

### 7.1 Required structure and word budget

| Section | Target words | Function |
| --- | ---: | --- |
| Abstract | 220-250 | Problem, approach, strongest results, conclusion |
| Introduction | 1,600-1,800 | Literature, persistence gap, questions, model logic |
| Materials and Methods | 1,200-1,600 | Concise models, tested domain, measures, analysis, reproducibility |
| Results | approximately 1,600-2,000 | Outcomes, benchmarks, and uncertainty |
| Discussion | approximately 1,400-1,800 | Interpretation, contribution, and limitations |
| Conclusion | no more than two paragraphs | Bounded synthesis only |
| **Main text** | **approximately 6,000-8,000** | Short first research article |

The literature review and long-form chapters remain source material rather than
current manuscript authority. The existing long Formal Model and Methods
authority is preserved for later separation into concise main Methods,
Supplementary Methods, and repository reproducibility/technical documentation;
it is not the intended main-text Methods section.

### 7.2 Narrative contract

The manuscript will:

1. state each outcome before its limitation;
2. distinguish objective value, optimal dynamic policy, and learned policy;
3. report effect magnitude and tested-domain size where available;
4. explain the mechanism after reporting the result;
5. consolidate translation limits late in the Discussion;
6. avoid using caveats to obscure supported results;
7. avoid presenting model-domain results as population prevalence.

### 7.3 Results subsection contract

Every finding follows the same sequence:

1. outcome;
2. how it was established;
3. relative and absolute magnitude;
4. analytic or experimental benchmark;
5. uncertainty and robustness;
6. local limitation.

## 8. Evidence Contract

### 8.1 Evidence classes

- **Proved analytically:** follows from stated equations or solved dynamic
  optimization under explicit assumptions.
- **Demonstrated computationally:** reproduced across a declared simulation
  domain with uncertainty and independent seeds.
- **Observed descriptively:** present in a maintained run but missing required
  robustness or a direct mechanism test.
- **Educational hypothesis:** a testable implication for human settings not
  established by the simulations.

The article must use these classes consistently. Simulation evidence must not
be described as a mathematical proof, and analytic thresholds must not be
described as learned behavioral crossovers without a behavioral test.

### 8.2 Publication evidence minimum

Every headline stochastic result must report:

- exact parameter domain;
- number of simulated learners per cell;
- horizon and final-window definition;
- master-seed and child/cell RNG strategy;
- point estimate and effect-size definition;
- uncertainty interval;
- replication across at least three independent master seeds;
- sensitivity or ablation appropriate to the mechanism;
- source-data and manifest paths.

### 8.3 Required claim-closing analyses

The execution authority for these analyses is
`STAGE2_EXPERIMENT_SPECIFICATIONS.md`. It fixes the design, outputs,
uncertainty, and claim decision rules established at the Stage 1 gate. Changes
to those decision rules require an RDS and claim-ledger update before a run.

#### Hot-stove mechanism

- Condition trajectories on early accepted versus rejected authentic attempts.
- Compare ordinary learning with an information-restoring intervention such as
  forced exploration or counterfactual feedback.
- Primary criterion: restored information materially reduces final masking or
  regret in an authenticity-optimal domain.

#### M1 graded disclosure

- Compare binary and graded action spaces directly.
- Report exploration risk, full-authenticity discovery, and endpoint behavior.
- Do not claim smooth generalization unless a separate generalization mechanism
  is implemented and labeled.

#### M2 suboptimal-masking regime

- Replicate the classified regime across independent seeds.
- Report the fraction of the tested grid and its classification uncertainty.
- Benchmark learned behavior against value iteration.
- Test horizon and learner-parameter sensitivity.

#### M3 search burden

- Compare flat, hierarchical, global-mask, and known-good-context architectures.
- Report K-response curves, not only endpoint contrasts.
- Add randomized good-context identity and multiple-good-context variants before
  making a broad contextual-search claim.

#### BFLPE comparison cost

- Sweep densely around the analytic objective crossover.
- Plot the analytic threshold separately from the learned behavioral transition.
- Report threshold-location uncertainty for the learned response.
- Preserve the completed E05 result as a paired analytic--simulation finding:
  the flat-2K learned `.5` response crossing is `bf=0.312852` (95% master-seed
  bootstrap interval `0.307836--0.316918`), whereas the exact objective payoff
  crossover is `8/17 = 0.470588`. Manuscript revisions must state that the
  learned retreat occurred while good-context authenticity still had positive
  objective advantage; they must not replace this result with the obsolete
  `bf=0` versus `.80` endpoint contrast alone.
- Keep the architecture boundary attached to that result: the tested
  hierarchical response was already below `.5` at the lower dense-grid
  boundary, so no hierarchical learned crossing was estimable and the flat
  numerical transition is not architecture-general.

#### M4 endogenous receptivity

- Replicate ascending and descending ramps across independent seeds.
- Test ramp-speed and horizon sensitivity.
- Report path separation or loop-area summaries.
- Use “path dependence” unless transition separation and robustness justify a
  stronger hysteresis claim.
- Keep the core E06 path-dependence package separate from the longer-horizon
  hysteresis-qualification package. The latter requires a separate GO and may
  run only if the core result passes every prespecified eligibility gate.

The preceding E06 programme design is preserved as historical future-work
planning only. It is superseded for primary Article V1 scope by Section 5.1 and
does not authorize E06 analysis or manuscript inclusion.

## 9. Figure And Table Program

### 9.1 Main figures

| Figure | Purpose | Required status |
| --- | --- | --- |
| 1. Model cascade and learning loop | Show the information-restriction mechanism and what M0–M3 add | New vector figure; no new simulation |
| 2. History and endpoint discovery | Present frozen E01 sampling/information-restoration and E02 graded-action results | Frozen E01–E02 evidence only |
| 3. Dynamic policy disagreement | Present frozen E03 aggregate Neutral-action/DP disagreement with tested-grid boundaries | Frozen E03 evidence only |
| 4. Context discovery and boundary displacement | Present frozen E04 architectures and E05 analytic/learned crossovers | Frozen E04–E05 evidence only |

The current directional-contrast forest plot becomes supplementary. The
standalone M2 threshold plot is redundant with the combined M2 figure.

### 9.2 Tables

1. Model cascade: inherited components, new mechanism, tested question, outcome.
2. Tested domain: parameters, grids, `n`, `T`, final window, seeds, metrics.
3. Findings: estimate, benchmark, evidence class, robustness, permitted claim.

### 9.3 Figure quality contract

Each figure must have:

- one explicit scientific claim;
- a checked-in source-data file;
- a deterministic generation command;
- uncertainty where applicable;
- consistent action, state, and mechanism colors;
- redundant non-color encodings;
- legible text at final publication size;
- a complete caption and accessible alt text;
- no embedded title that merely repeats the caption.

No decorative or generated illustration is planned. Figure 1 may be adapted as
a graphical abstract after the scientific figures are stable.

## 10. Delivery Stages And Gates

### Stage 1 — Establish the source of truth

**Status:** Complete on 11 August 2026.

**Work**

- designate the RDS and claim ledger;
- map all article candidates and chapters to the final architecture;
- reconcile numerical and wording discrepancies;
- freeze model and outcome terminology.

**Deliverables**

- completed claim ledger;
- paragraph-level manuscript map;
- resolved list of evidence gaps.

**Exit gate**

Every intended headline claim has a named evidence source, required analysis,
and permitted wording.

**Gate record**

- `CLAIM_LEDGER.md` freezes six primary, two secondary, and two excluded
  claims, with exact artifact selectors and current DOCX paragraph anchors.
- `MANUSCRIPT_INTEGRATION_MAP.md` assigns every prose paragraph in the four
  long-form sources to the final article architecture.
- `STAGE2_EXPERIMENT_SPECIFICATIONS.md` converts all evidence gaps into E01-E06
  designs with seed, uncertainty, output, and stop/go rules.
- Stage 1 did not change model code, model semantics, default parameters, or
  random-number behavior. Repository verification regenerated maintained
  artifacts, but no E01-E06 evidence run or new parameter sweep was executed.

### Stage 2 — Close essential evidence gaps

**Work**

- execute Stage 2 through `runbooks/STAGE2_EVIDENCE.md`;
- run the analyses in Section 8.3;
- create manifests and primary-unit outputs;
- compute uncertainty and sensitivity summaries;
- narrow claims that fail their gates.

**Deliverables**

- final machine-readable analysis artifacts;
- evidence-resolution report;
- updated claim ledger.

**Exit gate**

Every headline claim is either publication-supported or explicitly narrowed.

### Stage 3 — Lock article architecture

**Work**

- assign each source paragraph to keep, compress, move, merge, or remove;
- fix section and subsection order;
- enforce the word budget and remove mechanism duplication.

**Deliverables**

- paragraph-level article outline;
- section word budgets;
- citation coverage plan.

**Exit gate**

Each mechanism is introduced once, specified once, reported once, and
interpreted once.

### Stage 4 — Complete Materials and Methods

**Work**

- specify shared learner, M0–M3, analytic benchmarks, tested domain, outcome
  measures, uncertainty, seed hierarchy, software, and reproducibility;
- add model-cascade and tested-domain tables.

**Deliverable**

- reproducible Materials and Methods section.

**Exit gate**

An independent reader can identify the exact simulation and analysis supporting
every result.

### Stage 5 — Produce figures and tables

**Work**

- generate approximately four to five E01–E05 main figures and the supplementary program;
- export source data;
- write captions and alt text;
- visually inspect all figures at final size.

**Deliverables**

- submission figures;
- editable tables;
- supplementary figures;
- generation scripts and source data.

**Exit gate**

Each main figure communicates one supported finding and regenerates
deterministically from archived inputs.

### Stage 6 — Write final Results

**Work**

- write by finding using the Results contract;
- reconcile all values with final artifacts;
- remove interpretation reserved for Discussion.

**Deliverable**

- final Results section.

**Exit gate**

Every reported number matches its source artifact and uses the correct unit,
denominator, benchmark, and uncertainty.

### Stage 7 — Integrate Introduction and Discussion

**Work**

- compress literature into the Introduction;
- add explicit questions or hypotheses;
- interpret results without numerical repetition;
- state educational predictions;
- consolidate limitations late in the Discussion.

**Deliverables**

- final Introduction;
- final Discussion and conclusion;
- final Abstract drafted from the completed article.

**Exit gate**

The article leads with supported outcomes, fits Educational Psychology, and
does not imply human prevalence, causality, or intervention efficacy.

### Stage 8 — Full manuscript audit

**Work**

- mathematical audit;
- statistical and reproducibility audit;
- interpretation and claim audit;
- citation and literature audit;
- figure/table/text consistency audit;
- adversarial reviewer pass.

**Deliverables**

- resolved audit checklist;
- clean candidate manuscript.

**Exit gate**

No blocker or major scientific, reproducibility, or editorial issue remains.

### Stage 9 — Assemble submission package

**Work**

- update the Frontiers Word template;
- complete authorship and declaration fields;
- render and inspect every PDF page;
- deposit code and artifacts;
- finalize counts, legends, alt text, and checklist.

**Deliverables**

- submission DOCX and PDF;
- separate figures and supplement;
- permanent evidence archive;
- completed submission checklist.

**Exit gate**

All upload files are final, internally consistent, visually verified, and free
of placeholders.

## 11. Verification

### 11.1 Repository verification

All implementation or analysis changes must pass:

```bash
./scripts/verify.sh
```

Python commands must use `/Users/omer/workspace/venvs/venv314`.

### 11.2 Manuscript verification

- extract and compare every reported numeric result with source artifacts;
- verify equations and analytic thresholds independently;
- check citations against the claims they support;
- render the DOCX and inspect every page image;
- audit figure dimensions, resolution, color mode, text size, and alt text;
- confirm that manuscript, figures, tables, and supplement use identical
  terminology and parameter labels.

## 12. Risks And Controls

| Risk | Consequence | Control |
| --- | --- | --- |
| Four source chapters are pasted together | Repetition and excessive length | Paragraph-level integration map and section budgets |
| Strong wording outruns the tested domain | Reviewer rejection or misleading claim | Claim ledger and evidence-class labels |
| One seed is treated as publication robustness | Unstable headline effects | Independent-master-seed gate |
| Analytic crossover is treated as learned behavior | Incorrect behavioral conclusion | Separate analytic and simulation panels |
| M2 grid share is read as human prevalence | Invalid population inference | Always state “share of tested grid” |
| M3 context count is treated as inherently harmful | Model-artifact interpretation | Mandatory action-space controls |
| M4 path dependence is labeled hysteresis | Overclaim | Ramp-speed, threshold, and loop diagnostics |
| Figures cannot be regenerated | Weak reproducibility | Script plus source-data contract |
| Submission format drives scientific compression | Lost definitions or evidence | Complete evidence audit before template assembly |

## 13. Global Acceptance Criteria

The sub-project is complete only when:

- the article is a single coherent Original Research manuscript;
- the main text remains comfortably below the 12,000-word ceiling;
- all model equations and transitions match the maintained implementation;
- every headline claim has an analytic proof or direct, replicated simulation;
- central stochastic results include uncertainty and independent seeds;
- M1 has a direct binary-versus-graded comparison;
- the hot-stove mechanism has an information-restoration test;
- M2 is benchmarked against the optimal dynamic policy across the reported
  domain;
- M3 conclusions survive the required action-space controls;
- M4 language matches the achieved path-dependence or hysteresis evidence;
- every figure has reproducible source data and generation code;
- the submission DOCX and PDF pass structural and visual QA;
- code and evidence are archived with a permanent identifier;
- author and declaration placeholders are resolved.

## 14. Change Control

Changes to article scope, headline claims, required evidence, stage gates, or
main-figure composition require an RDS update and corresponding changes to the
claim ledger and sub-project backlog.

Changes to model semantics require a separate repository-level design decision,
tests, documentation updates, and explicit disclosure in the manuscript. This
RDS cannot authorize a semantic change by itself.

## 15. Codex Model And Reasoning Assignment

### 15.1 Routing principles

OpenAI describes `gpt-5.6-sol` as the flagship-capability model and
`gpt-5.6-terra` as the intelligence-and-cost-balanced model. Reasoning effort is
assigned independently. This sub-project therefore uses:

- **Sol** for scientific design, competing-claim reconciliation, interpretation,
  high-stakes prose, and adversarial review;
- **Terra** for bounded implementation, deterministic document assembly,
  plotting, and checklist work when inputs and acceptance criteria are fixed;
- **high** as the normal quality-first effort;
- **xhigh** where several plausible scientific interpretations or experiment
  designs must be compared;
- **max** only for the final adversarial audit, where missed errors have the
  greatest downstream cost.

Official guidance recommends Sol for frontier capability, Terra for a balance
of intelligence and cost, medium as a general starting point, high or xhigh
when measured quality improves, and max only for the hardest quality-first
workloads: <https://developers.openai.com/api/docs/guides/latest-model>.

### 15.2 Stage assignments

| Stage | Primary model | Effort | Release-gate reviewer | Why |
| --- | --- | --- | --- | --- |
| 1. Source of truth | `gpt-5.6-sol` | `high` | `gpt-5.6-sol`, `xhigh` for disputed claims | Reconciliation requires scientific judgment across manuscripts, code artifacts, and analytic benchmarks |
| 2. Evidence gaps | `gpt-5.6-sol` for design; `gpt-5.6-terra` for approved implementation and runs | `xhigh` for design; `high` for implementation | `gpt-5.6-sol`, `xhigh` | This is the highest-risk scientific-design stage; routine execution becomes bounded after specifications are approved |
| 3. Article architecture | `gpt-5.6-sol` | `high` | `gpt-5.6-sol`, `high` in a clean review pass | Deciding what to remove or merge affects the argument and cannot be treated as mechanical compression |
| 4. Materials and Methods | `gpt-5.6-sol` | `high` | `gpt-5.6-sol`, `xhigh` for equation-to-code audit | Precision about equations, transitions, tested domains, and inference is publication-critical |
| 5. Figures and tables | `gpt-5.6-terra` | `high` | `gpt-5.6-sol`, `high` | Plot production is bounded by figure contracts; Sol reviews whether each visual actually supports its claim |
| 6. Final Results | `gpt-5.6-sol` | `xhigh` | `gpt-5.6-sol`, `xhigh` in a separate numeric/claim pass | Results require exact quantitative synthesis and disciplined separation of result from interpretation |
| 7. Introduction and Discussion | `gpt-5.6-sol` | `high` | `gpt-5.6-sol`, `xhigh` for final claim and literature pass | Theoretical synthesis, novelty, educational relevance, and calibrated language require frontier judgment |
| 8. Full manuscript audit | `gpt-5.6-sol` | `max` | Human author decision on any unresolved blocker | This is the hardest quality-first task and the final place to detect cross-section scientific or interpretive failure |
| 9. Submission package | `gpt-5.6-terra` | `high` | `gpt-5.6-sol`, `high` for release approval | Template assembly and checklist execution are bounded; final approval still requires claim and presentation review |

### 15.3 Operating rules

1. Release-gate review is a separate pass with the stage deliverables, RDS gate,
   and claim ledger supplied explicitly.
2. Stage 2 implementation may use Terra only after Sol approves the experiment
   specification, metrics, seed design, and pass/fail rule.
3. Stage 5 may use Terra to generate figures, but Sol decides whether a figure
   belongs in the main article, supplement, or nowhere.
4. Stage 8 starts from a clean review context and attempts to falsify the
   article's headline claims before improving prose.
5. Stage 9 cannot reopen scientific claims. A scientific discrepancy returns
   the work to the earliest affected stage.
6. Do not increase effort merely because a task is long. Increase it when the
   task has ambiguous evidence, interacting constraints, or high cost of an
   undetected error.
7. Resolve model-output conflicts against the RDS, code evidence, and analytic
   benchmarks rather than model seniority alone.

### 15.4 Default assignment outside the stage table

- Use `gpt-5.6-sol` with `high` effort for scientific or editorial decisions.
- Use `gpt-5.6-terra` with `high` effort for deterministic production tasks.
- Use `gpt-5.6-terra` with `medium` effort only for low-risk inventory,
  formatting, filename checks, and already-specified repetitive transformations.
- Reserve `max` for Stage 8 or a Stage 2 design dispute that materially changes
  the study.

## 16. Revision History

| Version | Date | Change |
| --- | --- | --- |
| 0.1 | 2026-08-10 | Initialized article scope, evidence contract, stages, and publication gates. |
| 0.2 | 2026-08-11 | Closed Stage 1 with exact claim/evidence mapping, paragraph-level source integration, frozen terminology and claim hierarchy, and executable E01-E06 Stage 2 specifications; advanced the active stage to Stage 2. |
| 0.3 | 2026-08-11 | Assigned Sol/Terra ownership, reasoning effort, and independent release-gate review for all nine stages. |
| 0.4 | 2026-08-11 | Added the gated Stage 2 operational runbook with role handoffs, smoke-first execution, stop conditions, reporting contracts, and copy-ready prompts. |
