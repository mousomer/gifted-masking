# Stage 2 Operational Runbook: Close Essential Evidence Gaps

**Stage:** 2 of 9  
**Status:** Ready for execution  
**Scientific owner:** `gpt-5.6-sol`, `xhigh` reasoning  
**Implementation owner:** `gpt-5.6-terra`, `high` reasoning  
**Release-gate reviewer:** `gpt-5.6-sol`, `xhigh` reasoning in a separate pass  
**Repository root:** `/Users/omer/workspace/personal/repos/gifted-masking`  
**Required Python:** `/Users/omer/workspace/venvs/venv314/bin/python`

## 1. Mission

Close the evidence gaps for claims C1-C8 by implementing and executing the six
prespecified experiments E01-E06. Produce deterministic, machine-readable,
seed-replicated evidence that either supports, narrows, or excludes each claim.

Stage 2 does not exist to maximize favorable outcomes. Null, adverse, unstable,
and model-artifact results are valid completions when they are correctly
implemented, verified, and reported.

## 2. Authority Order

Before taking any Stage 2 action, read these files completely in this order:

1. repository `AGENTS.md`;
2. `projects/frontiers_article/RDS.md`;
3. `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`;
4. `projects/frontiers_article/CLAIM_LEDGER.md`;
5. `projects/frontiers_article/CURRENT_STATE.md`;
6. repository `ARCHITECTURE.md`;
7. repository `CURRENT_STATE.md` and `BACKLOG.md`.

If instructions conflict, repository safety and model-semantics rules prevail,
followed by the RDS, experiment specifications, and this runbook. Stop and
record the conflict instead of silently resolving it through implementation.

## 3. Stage Inputs

The execution agent must locate and inspect:

- maintained model kernels under `src/gifted_masking/models/`;
- shared learner and parameter code under `src/gifted_masking/`;
- maintained experiment and reproducibility infrastructure;
- tests under `tests/`;
- existing raw, summary, manifest, and benchmark artifacts under `results/`;
- E01-E06 designs and decision rules in the experiment specification;
- exact claim language and evidence selectors in the claim ledger.

Do not infer that an existing artifact satisfies a Stage 2 requirement merely
because it has a similar name. Verify its model, parameters, seeds, unit of
analysis, and uncertainty method.

## 4. Hard Boundaries

The following are prohibited unless a separate design change is explicitly
approved:

1. Changing M0-M4 baseline semantics, default parameters, reward equations,
   state transitions, action indexing, or RNG behavior.
2. Rewriting the models to increase the likelihood of a desired conclusion.
3. Treating an experiment-only intervention as part of a baseline model.
4. Tuning parameters after observing results and then presenting the tuned run
   as prespecified evidence.
5. Replacing independent-master-seed uncertainty with child-level resampling.
6. Pairing administrative child indices across independently seeded conditions.
7. Running a publication-tier sweep before smoke and standard checkpoints pass.
8. Running an unbounded Cartesian sweep.
9. Suppressing null, adverse, or unstable findings.
10. Updating article prose or figures before the relevant evidence gate closes.
11. Calling M2 grid coverage human prevalence.
12. Calling an analytic BFLPE threshold a learned behavioral crossover.
13. Calling M4 path separation hysteresis unless every E06 hysteresis rule
    passes.
14. Introducing a new runtime dependency without recording its package,
    constraint, purpose, and rejected alternative.
15. Using system Python or a repository-local virtual environment.

## 5. Required Working Discipline

### 5.1 Before every implementation batch

1. State a concise plan and batch-specific acceptance criteria.
2. Inspect `git status --short` and preserve unrelated worktree changes.
3. Compare the proposed change with `ARCHITECTURE.md`, the RDS, and the
   experiment specification.
4. Identify every model semantic that must remain unchanged.
5. Identify the exact tests and artifacts that will demonstrate success.

### 5.2 During implementation

- Use `apply_patch` for source and documentation edits.
- Prefer pure functions and explicit validated configuration.
- Keep experiment-only logic behind named configuration modes.
- Preserve deterministic output ordering.
- Record every seed derivation and stochastic component.
- Store objective reward separately from subjective learning value.
- Keep actual and counterfactual outcomes distinct.
- Add small tests before standard or publication-scale runs.
- Profile smoke runs before approving larger tiers.

### 5.3 After every implementation batch

1. Run targeted tests.
2. Run `./scripts/verify.sh` before declaring the batch complete.
3. Run raw-to-summary reconciliation.
4. Inspect generated manifests and a sample of primary rows.
5. Update affected architecture, state, backlog, and experiment documentation.
6. Report changed files, tests, artifacts, runtime, warnings, and open risks.

## 6. Model And Handoff Contract

Stage 2 must use separate scientific-design, implementation, and review passes.

### Pass A — Scientific approval

**Model:** `gpt-5.6-sol`  
**Effort:** `xhigh`

For the next experiment only:

1. Audit the corresponding E01-E06 specification against current code and
   evidence.
2. Resolve implementation ambiguities without changing the research question.
3. Freeze the smoke configuration, raw schema, summaries, tests, and decision
   rule.
4. Estimate expected compute and identify sentinel cases.
5. Write a short approval record or return the specification for correction.

Sol approves scientific design; it does not waive repository verification.

### Pass B — Bounded implementation and smoke execution

**Model:** `gpt-5.6-terra`  
**Effort:** `high`

Terra may implement only the approved experiment and shared infrastructure
required for it. It must stop after producing the smoke checkpoint. It may not
continue to a standard run on its own.

### Pass C — Smoke-gate review

**Model:** `gpt-5.6-sol`  
**Effort:** `xhigh`

Review the smoke checkpoint in a separate pass. Verify semantics, raw rows,
summaries, determinism, baseline reproduction, and runtime. Return exactly one
decision:

- `GO_STANDARD`;
- `FIX_IMPLEMENTATION`;
- `REVISE_SPECIFICATION`;
- `NARROW_OR_STOP_CLAIM`.

Only `GO_STANDARD` authorizes a standard run.

### Pass D — Standard execution

**Model:** `gpt-5.6-terra`  
**Effort:** `high`

Run the approved standard configuration unchanged across all prescribed master
seeds. Produce primary rows, summaries, effects, manifests, and a report. Stop
before publication-tier sensitivity work.

### Pass E — Claim adjudication

**Model:** `gpt-5.6-sol`  
**Effort:** `xhigh`

Apply the prespecified decision rules. Do not optimize or rerun merely because
the conclusion is unfavorable. Return exactly one evidence disposition:

- `SUPPORTED`;
- `SUPPORTED_IN_NARROW_DOMAIN`;
- `DESCRIPTIVE_ONLY`;
- `NOT_SUPPORTED`;
- `IMPLEMENTATION_INVALID`.

Update the claim ledger only after this adjudication.

## 7. Stage 2 Execution Sequence

### Step 0 — Preflight and baseline freeze

1. Read all authority files in Section 2.
2. Inspect repository status and note pre-existing changes.
3. Run the current verification command before editing.
4. Record the current commit, dirty state, Python version, and package versions.
5. Identify the maintained baseline entry points for M0-M4.
6. Confirm the existing headline values and artifact paths used by the claim
   ledger.
7. Write the Stage 2 implementation plan and acceptance criteria into the
   active work log or checkpoint report.

**Stop condition:** baseline verification fails or the maintained source of
truth cannot be identified.

### Step 1 — Shared article-experiment infrastructure

Implement the minimum shared infrastructure needed by E01 first:

1. validated article-experiment configuration loading;
2. explicit smoke and standard configuration records;
3. deterministic seed hierarchy by master seed, cell, learner, and stochastic
   component where required;
4. CLI orchestration for `article-experiment`;
5. primary-unit CSV, cell summary, effect summary, report, and manifest output;
6. stable row ordering and output hashing;
7. raw-to-summary recomputation;
8. normalized deterministic rerun comparison;
9. validation failures for missing seed, grid, horizon, final window, and output
   metadata.

Preferred command after implementation:

```text
/Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli \
  article-experiment --config configs/frontiers_article/<config>.json
```

Use explicit configuration files. Do not rely on undocumented CLI overrides.
If separate smoke and standard files are used, name both clearly and ensure the
manifest records the selected tier.

Required tests before E01 smoke:

- baseline reproduction for the same seed and parameters;
- deterministic rerun;
- cell-order independence;
- worker-count independence if parallel execution is introduced;
- raw-to-summary equality to `1e-12` for deterministic summaries;
- final-window indexing at exact and non-integer fractions;
- manifest completeness and invalid-config rejection;
- proof that experiment-only modes do not change the baseline path.

**Gate 1:** targeted tests and full verification pass.

### Step 2 — E01 smoke: early outcome and information restoration

1. Implement only the E01 modes described in the specification.
2. Preserve actual objective payoff separately from subjective and
   counterfactual learning signals.
3. Use the smoke tier: small `n`, short `T`, one master seed.
4. Inspect accepted and rejected initial-outcome strata manually.
5. Verify that forced exploration changes action sampling, not reward equations.
6. Verify that counterfactual feedback changes learning information but is not
   added to environment return.
7. Confirm all E01-required raw fields and summaries exist.
8. Measure runtime and project standard-tier cost.
9. Produce the checkpoint defined in Section 9.

Stop after the smoke checkpoint. Sol must issue `GO_STANDARD` before E01
standard execution.

### Step 3 — E01 standard and adjudication

After `GO_STANDARD`:

1. run the frozen standard configuration with five independent master seeds;
2. compute seed-level effects and intervals;
3. verify all decision-rule inputs directly from primary rows;
4. run deterministic regeneration and repository verification;
5. submit results to Sol for claim adjudication;
6. update C1-C3 wording only after adjudication.

Do not retune exploration rates, learner defaults, or thresholds after viewing
the standard result. Prespecified sensitivities remain allowed and labeled.

### Step 4 — E02: binary versus graded disclosure

Repeat Passes A-E for E02.

Mandatory checks:

- M0 and M1 endpoints have matched objective payoffs;
- learner parameters and initial exposure are identical;
- intermediate actions remain independent Q-values;
- any-disclosure, full-authentic discovery, regret, and endpoint selection are
  reported separately;
- increased mean disclosure alone is not treated as improved discovery;
- action-space dilution is retained if observed.

Update C4 immediately after adjudication. Do not carry protective wording into
later drafting if the discovery or regret gate fails.

### Step 5 — E03: M2 regime replication

Repeat Passes A-E for E03, beginning with exact-grid smoke/sentinel checks.

Mandatory checks:

- reproduce the original seed and 226/357 calculation before replication;
- retain the original exact-grid denominator separately from sensitivity cells;
- run value iteration with declared tolerance for every reported cell;
- use neutral-state counts for learned neutral action;
- mark ties and inadequate-visit cells inconclusive;
- report per-seed grid fractions and per-cell classification frequency;
- keep learned-policy failure separate from objective-policy masking;
- do not rebuild the manuscript M2 figure before the stable-cell summary exists.

If the original seed does not reproduce, classify this as an implementation or
provenance problem before running additional seeds.

### Step 6 — E04: M3 search architectures and context identity

Repeat Passes A-E for E04.

Mandatory checks:

- test action decoding for every architecture and K;
- store randomized good-context identity per learner;
- emit K=1 equivalent cases once with explicit equivalence metadata;
- compare full K curves, not only K=1 and K=8 endpoints;
- report architecture-by-K contrasts;
- apply the prespecified practical-equivalence band to controls;
- report one-good, two-good, and proportional-good variants separately;
- treat loss under randomized identity as evidence of an index or initialization
  artifact, not a reason to redesign the randomization.

### Step 7 — E05: dense BFLPE crossover

Repeat Passes A-E for E05.

Mandatory checks:

- include the exact analytic threshold anchor;
- verify BFLPE cost applies only to accepted authenticity in a good context;
- show analytic objective advantage and learned response separately;
- preserve architecture-specific results;
- estimate a learned transition only if the response and crossing criteria pass;
- if no crossing exists, report the curve and endpoint change without a learned
  threshold.

### Step 8 — E06: M4 path diagnostics

Repeat Passes A-E for E06.

Mandatory checks:

- preserve the declared reward-then-receptivity update order;
- continue both Q-values and receptivity on inherited ramps;
- initialize cold-start controls independently and identically at every point;
- include reversal-only stochastic controls;
- verify zero receptivity-bounds violations;
- declare the loop-area integration convention;
- report transition locations only when crossed;
- compare both ramp speeds and the long-horizon sentinel;
- retain “schedule-specific path dependence” unless every hysteresis condition
  passes.

### Step 9 — Publication-tier decision

After E01-E06 standard adjudication, produce one runtime and evidence-gap
report. For each requested publication-tier sentinel, state:

- which still-supported claim it refines;
- why standard evidence is insufficient;
- exact parameter cells and seeds;
- estimated runtime and storage;
- stopping rule;
- expected manuscript or figure consequence.

Publication-tier work requires explicit approval. Do not interpret general
permission to complete Stage 2 as permission for an unrestricted large sweep.

### Step 10 — Stage closure

1. Update every C1-C10 ledger row with final evidence disposition, exact artifact
   selectors, effect estimates, uncertainty, and maximum wording.
2. Record null, adverse, and unstable results in the report and ledger.
3. Update RDS status, current state, backlog, architecture, and affected docs.
4. Run full verification and deterministic artifact regeneration.
5. Produce the Stage 2 completion report in the format in Section 10.
6. Submit the completion package to Sol/xhigh for the Stage 2 release gate.

Do not advance the RDS to Stage 3 until every Stage 2 completion criterion is
explicitly passed or waived by narrowing/excluding the affected claim.

## 8. Stop And Escalation Conditions

Stop the current experiment and report the blocker when any of these occurs:

- baseline results change under a supposedly isolated experiment mode;
- reward, transition, action, or RNG semantics are ambiguous;
- deterministic reruns do not match;
- cell order or worker count changes results;
- raw summaries cannot be reconstructed from primary rows;
- required fields or manifest metadata are missing;
- neutral-state visits are insufficient for M2 classification;
- an analytic benchmark disagrees with its implementation;
- smoke runtime makes the standard tier materially larger than projected;
- a new dependency or semantic extension appears necessary;
- the worktree contains overlapping changes that cannot be preserved safely;
- a result is favorable only after an unplanned parameter change;
- a publication-tier run is requested without a reviewed cost checkpoint.

Do not mark Stage 2 blocked merely because a result is null or unfavorable.
Scientific claim narrowing is a successful Stage 2 outcome.

## 9. Required Smoke Checkpoint

After every E01-E06 smoke run, write a compact checkpoint containing:

1. experiment and run ID;
2. model, effort, commit, and dirty-state hash;
3. implemented files and isolated experiment modes;
4. smoke config, `n`, `T`, final window, and seed;
5. targeted and full verification results;
6. baseline reproduction result;
7. determinism and cell-order result;
8. raw-to-summary reconciliation result;
9. manual semantic inspection findings;
10. produced artifact paths;
11. wall time, memory/storage estimate, and standard-tier projection;
12. warnings, failed checks, and interpretation risks;
13. recommended gate decision.

The checkpoint must not contain manuscript prose or claim promotion.

## 10. Required Stage 2 Completion Report

The completion report must contain:

### Outcome summary

- one sentence for each C1-C10 disposition;
- a list of claims strengthened, narrowed, retained as descriptive, or excluded.

### Experiment inventory

For E01-E06, report:

- run ID and exact config;
- model and intervention/architecture;
- parameter domain;
- `n`, `T`, final window, and master seeds;
- primary estimate and uncertainty;
- decision-rule result;
- manifest, raw, summary, report, and figure paths;
- runtime and warnings.

### Correctness and reproducibility

- tests added or changed;
- full verification result;
- deterministic rerun result;
- raw-to-summary result;
- baseline non-regression result;
- unresolved technical limitations.

### Manuscript consequences

- exact claim-ledger updates;
- Results subsections enabled or removed;
- main and supplementary figures enabled or removed;
- wording that is now prohibited;
- evidence still requiring publication-tier approval.

### Change summary

- changed file list;
- short summary by file;
- diffstat;
- explicit statement of whether model semantics, defaults, or RNG behavior
  changed.

## 11. Stage 2 Completion Gate

Stage 2 passes only when:

- all E01-E06 smoke configurations pass semantic, RNG, schema, and summary
  checks;
- each executed standard experiment uses at least five independent master seeds;
- every headline stochastic effect has seed-level uncertainty and source rows;
- E03 separates learned suboptimal masking from optimal-policy masking;
- E04 includes K curves, randomized identity, and multiple-good variants;
- E05 separates analytic and learned crossovers;
- E06 reports path separation, loop area, speeds, horizons, and controls;
- the claim ledger records supported, narrowed, descriptive, unsupported, or
  invalid outcomes without favorable-result tuning;
- artifacts regenerate deterministically;
- `./scripts/verify.sh` passes;
- Sol/xhigh approves the Stage 2 completion package.

If an experiment is scientifically valid but its result does not support the
claim, the experiment requirement is complete and the claim must be narrowed or
excluded. Missing or invalid evidence cannot be waived through prose.

## 12. Copy-Ready Launch Prompts

### 12.1 Sol/xhigh — approve the next experiment

```text
Act as the scientific owner for Stage 2 of the Frontiers article sub-project.
Read AGENTS.md, projects/frontiers_article/RDS.md,
projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md,
projects/frontiers_article/CLAIM_LEDGER.md, and
projects/frontiers_article/runbooks/STAGE2_EVIDENCE.md completely.

Audit experiment <E01-E06> against the maintained code and current evidence.
Freeze its smoke configuration, required raw schema, summaries, tests,
decision rules, and compute estimate. Do not implement it and do not change
model semantics or defaults. Return either APPROVED_FOR_SMOKE with an exact
implementation contract, or REVISE_SPECIFICATION with concrete blockers.
```

### 12.2 Terra/high — implement and run smoke only

```text
Implement only the APPROVED_FOR_SMOKE contract for experiment <E01-E06> under
projects/frontiers_article/runbooks/STAGE2_EVIDENCE.md. Use the required
workspace Python environment. Preserve all baseline model semantics, defaults,
and RNG behavior. Add small tests first, run targeted tests and
./scripts/verify.sh, execute only the smoke configuration, inspect raw rows and
manifests, and produce the required smoke checkpoint. Stop after the checkpoint;
do not run the standard or publication tier and do not update manuscript claims.
```

### 12.3 Sol/xhigh — review smoke checkpoint

```text
Review the <E01-E06> smoke checkpoint and its code, tests, configs, primary
rows, summaries, manifest, and runtime against the RDS, experiment
specification, and Stage 2 runbook. Attempt to find semantic drift,
nondeterminism, invalid comparisons, incorrect units, or missing metadata.
Return exactly one gate decision: GO_STANDARD, FIX_IMPLEMENTATION,
REVISE_SPECIFICATION, or NARROW_OR_STOP_CLAIM. Cite the evidence for the
decision and do not rewrite manuscript prose.
```

### 12.4 Terra/high — execute approved standard run

```text
The <E01-E06> smoke gate returned GO_STANDARD. Execute the frozen standard
configuration exactly as approved. Use all prescribed independent master seeds,
produce primary rows, summaries, effects, manifests, and the experiment report,
then run deterministic regeneration, raw-to-summary reconciliation, and
./scripts/verify.sh. Stop before publication-tier work. Report artifacts,
runtime, warnings, file changes, and diffstat without adjudicating the claim.
```

### 12.5 Sol/xhigh — adjudicate experiment evidence

```text
Adjudicate the completed <E01-E06> standard evidence against its prespecified
decision rules. Read primary rows and manifests rather than relying only on the
report. Return one disposition: SUPPORTED, SUPPORTED_IN_NARROW_DOMAIN,
DESCRIPTIVE_ONLY, NOT_SUPPORTED, or IMPLEMENTATION_INVALID. State the maximum
defensible claim wording and exact artifact selectors. Update the claim ledger
and project state only if the implementation is valid. Do not tune parameters
or request an unplanned rerun to improve the conclusion.
```

### 12.6 Sol/max or Sol/xhigh — final Stage 2 release gate

```text
Audit the complete Stage 2 package under the RDS and Stage 2 runbook. Verify
E01-E06 dispositions, independent-seed uncertainty, baseline non-regression,
deterministic regeneration, raw-to-summary reconciliation, claim-ledger
wording, and repository verification. Attempt to falsify every strengthened
claim. Return STAGE2_COMPLETE only if every completion criterion is met or the
affected claim has been explicitly narrowed or excluded. Otherwise return
STAGE2_NOT_COMPLETE with the earliest failed gate and exact corrective action.
```

