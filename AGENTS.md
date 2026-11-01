# AGENTS.md — Simulation Code Review and Robustness Rules

## Project context

This repository contains simulation code for a reinforcement-learning model ladder about masking, authenticity, and peer adaptation.

The code is expected to implement:

- M0: two-armed masking/authenticity bandit.
- M1: graded-disclosure action space.
- M2: stigma-state MDP with Q-learning.
- M3: peer-group/context search with optional BFLPE comparison cost.
- M4: endogenous peer receptivity feedback.
- A shared learner core using Q-values, softmax action selection, learning rate alpha, temperature tau, initial value q0, and loss-aversion lambda.
- Population simulations using independent random seeds.
- Final-window metrics such as mask rate, mask-lock/auth-lock/mixed classification, modal arm, basin fractions, bistability index, and regret where applicable.

The scientific goal is to verify whether the simulated claims are mathematically, statistically, and computationally robust. Secondary goal is to produce relevant graphs.

## Non-negotiable working rules

1. Do not silently change model semantics.
2. Do not rewrite the simulation to make expected conclusions appear stronger.
3. Do not change parameter defaults without explicitly documenting why.
4. Do not change random-number behavior without documenting reproducibility consequences.
5. Do not collapse distinct mechanisms across M0–M4.
6. Do not treat visual smoothness as evidence of robustness.
7. Do not run very large sweeps unless explicitly asked. Prefer smoke tests, small deterministic reproductions, and a clear scaling plan.
8. Do not introduce new runtime dependencies without listing:
   - package name,
   - version constraint,
   - reason,
   - alternative avoided.
9. Separate:
   - code correctness,
   - mathematical correctness,
   - statistical robustness,
   - interpretation/claims.
10. When uncertain, state the uncertainty and propose a test.
11. Always use the workspace virtual environment at `/Users/omer/workspace/venvs/venv314` for Python
    commands, verification, installs, and experiment runs. Treat system Python
    as bootstrap-only only if the workspace venv itself must be repaired; do not
    create repo-local virtual environments without explicit user approval.
    The checked-in GitHub Actions workflow is the hosted-CI exception: it uses
    its pinned setup-python interpreter through `GOVERNANCE_PYTHON`. This does
    not change the required shared interpreter for local work.

## Environment rules

- Use `/Users/omer/workspace/venvs/venv314/bin/python` and `/Users/omer/workspace/venvs/venv314/bin/python -m pip` for repo commands.
- Run repository verification via `./scripts/verify.sh` from the repo root, ensuring it resolves Python through the workspace venv.
- If required packages are missing, install them into `/Users/omer/workspace/venvs/venv314` or ask before using any other environment.

## Review posture

Be adversarial but constructive. Assume the current code may contain:

- off-by-one errors in final-window calculations,
- RNG coupling between children or parameter cells,
- shape/broadcasting errors in vectorized NumPy code,
- hidden dependence on global random state,
- parameter mutation across runs,
- wrong softmax normalization,
- numerical instability in softmax,
- incorrect loss-aversion handling around zero rewards,
- incorrect M2 state transition logic,
- incorrect M3 action indexing,
- overclaimed M4 hysteresis,
- unsupported “optimality” or “regret” claims.

Do not merely summarize the files. Audit them.

## Required review structure

For every reviewed file, produce:

1. Purpose of the file.
2. Public functions/classes and their role.
3. Hidden assumptions.
4. State mutation and RNG behavior.
5. Inputs, outputs, and artifact paths.
6. Mathematical logic implemented.
7. Failure modes.
8. Tests that currently exist.
9. Tests that are missing.
10. Recommended changes.

## Scientific validation targets

Validate the implementation against these model-level checks.

### M0 — two-armed bandit

Expected rewards:

- Masking: E[mask] = b - c.
- Authenticity: E[auth] = p * (b + a) + (1 - p) * (a - r).
- Equivalent: E[auth] = a + p*b - (1-p)*r.
- Objective indifference:
  - b - c = a + p*b - (1-p)*r.
  - r*(p) = (a + c)/(1-p) - b, where p != 1.

Default sanity check:

- b = 1.0
- a = 0.6
- c = 0.25
- r = 2.0
- E[mask] = 0.75
- E[auth] = -1.4 + 3p
- objective p* = 2.15 / 3 ~= 0.7166667

Required M0 checks:

- p = 0 gives E[auth] = a - r.
- p = 1 gives E[auth] = b + a.
- r = 0 makes rejected authenticity nonnegative if a >= 0.
- loss aversion must not be applied to a nonnegative realized reward.
- softmax must be numerically stable.
- empirical acceptance frequencies should converge to p within Monte Carlo tolerance.

### Loss aversion

Subjective reward transform:

- If realized reward R >= 0, v = R.
- If realized reward R < 0, v = lambda * R.

Required checks:

- Use a variable name like `R` or `reward` for realized reward, not `r`, to avoid collision with rejection penalty.
- Verify lambda affects learning updates only, not the environment’s objective payoff.
- Verify subjective indifference formula is only applied in regions where rejected-authentic reward is negative.
- Test lambda = 1 exactly reproduces baseline.
- Test lambda > 1 increases avoidance of negative outcomes.
- Test 0 < lambda < 1 decreases avoidance of negative outcomes.
- Decide and document behavior for lambda = 0 and lambda < 0. Prefer rejecting lambda < 0.

### M1 — graded disclosure

Expected reward for disclosure level d:

E(d) = a*d - c*(1-d) + b*[1 - (1-p)*d] - r*[(1-p)*d]

Simplified:

E(d) = b - c + d * [a + c - (1-p)*(b+r)]

Required checks:

- d = 0 must equal masking payoff b - c.
- d = 1 must equal full-authenticity expected payoff.
- Acceptance probability must be 1 - (1-p)*d and must stay in [0, 1].
- Disclosure grid must include exactly 0 and 1.
- If using independent Q-values per disclosure level, do not claim the code models smooth generalization unless it actually does.
- Check whether intermediate disclosure is objectively optimal under current linear payoff; usually it is not except at indifference. If the paper claims “ladder climbing,” the code should distinguish lower-variance exploration from static optimality.

### M2 — stigma MDP

Required checks:

- States are explicit and enumerated:
  - neutral,
  - accepted-as-self,
  - stigmatized.
- Q-table shape is state x action.
- Q-learning update uses:
  Q(s,a) <- Q(s,a) + alpha * (v + gamma * max_a' Q(s',a') - Q(s,a))
- Masking must not accidentally change state unless explicitly specified.
- From neutral, authentic acceptance transitions to accepted; rejection transitions to stigmatized.
- Accepted state has reliable authenticity payoff unless peer turnover delta resets to neutral.
- Stigmatized state uses b2, r2, p/2 redemption, and eta escape exactly as specified.
- State transition order must be documented:
  - Is eta escape applied before or after action?
  - Is delta turnover applied before or after reward?
  - Does transition affect current reward or next-step state only?
- Compute optimal MDP policy by value iteration or policy iteration for selected cells.
- Do not call masking “suboptimal” in M2 unless learned policy is compared to the optimal MDP policy.
- Report dynamic regret, not only mask rate.

### M3 — peer-group/context search

Required checks:

- There are K groups.
- One group is good pond with p_good.
- K-1 groups have p_bad.
- There are 2K arms only if the model intentionally combines context choice and behavior choice.
- Action indexing from arm to group and behavior must be tested.
- Masking payoff must be identical across groups unless intentionally varied.
- Authenticity uses the correct group-specific p_g.
- BFLPE comparison cost bf is subtracted only from accepted-authentic payoff in the good pond, unless explicitly specified otherwise.
- Analytic BFLPE crossover:
  bf* = [p_good*(b+a) + (1-p_good)*(a-r) - (b-c)] / p_good
- Default sanity check:
  p_good = 0.85, b = 1.0, a = 0.6, r = 2.0, c = 0.25
  bf* ~= 0.470588

Required M3 ablations:

- Current 2K-arm formulation.
- Hierarchical formulation:
  1. choose group,
  2. choose mask/authentic within group.
- Global-mask formulation:
  - one masking action shared across contexts,
  - K authentic-in-group actions.
- Fixed-known-good-pond formulation:
  - removes search burden and isolates authenticity risk.
- Random good-pond identity per child with recorded identity.
- Multiple good ponds, not only one.

Do not conclude that “larger K causes masking” until the result survives the action-space ablations.

### M4 — endogenous receptivity

Required checks:

- p_t is bounded in [p_min, p_max] after every update.
- Accepted authenticity increases p_t by ka*(p_max - p_t).
- Rejected authenticity decreases p_t by kr*(p_t - p_min).
- Masking decreases p_t by km*(p_t - p_min).
- p_t update order is explicit:
  - reward first, then p_t update;
  - or p_t update first, then reward.
- Learner state must be described accurately:
  - If Q-values do not condition on p_t, call this a nonstationary/endogenous bandit, not ordinary stateful Q-learning.
- If claiming hysteresis, run a real hysteresis test:
  - ramp a control parameter up,
  - then ramp it down,
  - show different transition paths.
- Distinguish:
  - stochastic path dependence,
  - bistability,
  - hysteresis,
  - irreversible entrenchment.

Required M4 ablations:

- km = 0.
- ka = 0.
- kr = 0.
- ka < kr.
- ka = kr.
- ka > kr.
- p0 near p_min.
- p0 near p_max.
- high lambda and low lambda.
- high tau and low tau.
- long horizon T sensitivity.

## Statistical robustness requirements

Every reported simulation result should include:

1. Exact parameter grid.
2. Number of children/seeds per cell.
3. Number of time steps T.
4. Final-window fraction.
5. RNG seed strategy.
6. Point estimate.
7. Monte Carlo uncertainty:
   - standard error,
   - bootstrap confidence interval,
   - or binomial interval for lock probabilities.
8. Replication across independent master seeds.
9. Sensitivity to:
   - n,
   - T,
   - final-window fraction,
   - alpha,
   - tau,
   - lambda,
   - q0,
   - gamma for M2,
   - p/r grid resolution.
10. Edge-case behavior.

Do not rely on a single seed, single grid, or single calibration.

## Reproducibility requirements

A robust simulation framework should produce:

- A run manifest JSON for every experiment.
- Git commit hash if available.
- Python version.
- OS/platform.
- Package versions.
- Exact parameter values.
- Random seed hierarchy.
- Start/end timestamps.
- Output paths.
- Code version or config hash.
- A machine-readable results table.
- A human-readable summary report.

Preferred artifact layout:

```text
results/
  manifests/
    <run_id>.json
  raw/
    <run_id>.parquet
  summaries/
    <run_id>_summary.csv
  figures/
    <run_id>_<figure_name>.png
  reports/
    <run_id>_report.md
```
If parquet dependencies are unavailable, CSV is acceptable.

Testing requirements

Add or recommend tests in this order:

Pure function tests for reward equations.
Softmax probability tests.
Loss-aversion transform tests.
RNG determinism tests.
M0 analytic threshold tests.
M1 endpoint and monotonicity tests.
M2 transition tests.
M2 value-iteration benchmark tests.
M3 action-indexing tests.
M3 BFLPE crossover tests.
M4 p_t bounds and update-order tests.
Small-population deterministic smoke tests.
Regression tests for key published figures or summaries.

Use small tests first. Do not run full sweeps inside unit tests.

Performance requirements

Before optimizing:

Profile the existing code.
Identify O(nTgrid) costs.
Confirm vectorized operations are correct.
Avoid premature parallelism.
Prefer reproducibility over speed.

If adding parallel execution:

Ensure independent RNG streams per parameter cell.
Ensure results are invariant to worker count.
Ensure deterministic ordering of output rows.
Record parallel configuration in the manifest.
Required deliverables from Codex

For this review task, produce these files unless told otherwise:

CODE_REVIEW.md
file-by-file audit,
correctness risks,
statistical risks,
reproducibility risks,
interpretation risks.
ROBUST_SIMULATION_PLAN.md
proposed robust experiment suite,
test matrix,
required ablations,
uncertainty estimation,
compute-cost tiers,
deliverables,
implementation plan.
VALIDATION_CHECKLIST.md
concrete pass/fail checklist for accepting results as robust.
Optional only if low risk:
tests/test_model_invariants.py
tests/test_reproducibility.py

Do not perform large refactors unless explicitly asked after the review.

Acceptance criteria

The review is acceptable only if it answers:

Does the code match the mathematical specification?
Are all random processes reproducible?
Are phase maps robust to seed, horizon, population size, and grid resolution?
Are M2 “structural lock-in” claims benchmarked against optimal MDP policies?
Are M3 context-search conclusions robust to action-space ablations?
Is M4 hysteresis actually demonstrated, or only path dependence?
Are uncertainty intervals reported?
Are edge cases handled?
Are claims separated from model-specific artifacts?
What exact work remains before treating the simulations as publishable?
Tone and output style

Be precise. Avoid vague praise. Use tables where helpful. Mark severity as:

Blocker
Major
Moderate
Minor

Every major finding must include:

evidence from code,
why it matters,
proposed test or fix,
risk if ignored.

---

## Historical task templates (examples, not current assignments)

The following prompts are retained examples. They do not authorize execution or
restrict a later explicit task. Active shared dispatch resumes after them.

# 2. One-off Codex task prompt

Paste this as the actual Codex task after the repo has the three files available.

````markdown
Review the simulation code in this repository and produce a robust simulation plan.

There are three simulation-related files. If their names are obvious from the repo tree, identify them yourself. If more than three candidates exist, inspect the repo and select the three files that implement the model logic, experiment/sweep logic, and plotting/output logic. State which three files you selected and why.

Do not modify model code in this first pass. You may create Markdown review documents. You may create small test files only if they do not require refactoring and do not change existing behavior.

## Objective

Audit whether the code correctly implements the reinforcement-learning model ladder:

- M0: two-armed bandit.
- M1: graded disclosure.
- M2: stigma MDP.
- M3: peer-group/context search and BFLPE.
- M4: endogenous receptivity.

Then design a robust simulation framework that would make the reported conclusions reproducible, statistically defensible, and resistant to implementation artifacts.

## First, inventory the code

Create a section called `Code inventory` with:

| File | Role | Key functions/classes | Inputs | Outputs | RNG use | Mutable global state |
|---|---|---|---|---|---|---|

Include exact function names.

## Then, audit correctness

For each file, review:

1. Mathematical equations.
2. Reward calculation.
3. State transitions.
4. Action indexing.
5. Q-value update logic.
6. Softmax implementation.
7. Loss-aversion transform.
8. RNG handling.
9. Vectorization shape assumptions.
10. Final-window metric calculation.
11. Plot/data coupling.
12. Reproducibility.

Classify findings as:

- Blocker
- Major
- Moderate
- Minor

Each finding must include:

- location,
- evidence,
- why it matters,
- proposed test or fix.

## Required mathematical checks

Verify or write small checks for these.

### M0

Expected values:

- E[mask] = b - c.
- E[auth] = p*(b+a) + (1-p)*(a-r).
- Objective threshold at defaults:
  - b = 1.0
  - a = 0.6
  - c = 0.25
  - r = 2.0
  - p* ~= 0.7166667.

Check:

- p = 0.
- p = 1.
- r = 0.
- r < a.
- lambda = 1.
- lambda > 1.
- lambda < 1.

### M1

Check:

- d = 0 equals masking.
- d = 1 equals authenticity.
- all acceptance probabilities are in [0, 1].
- the disclosure grid includes 0 and 1.
- intermediate disclosure is interpreted as lower-variance exploration, not necessarily static optimality.

### M2

Check:

- Q-learning update uses gamma and next-state max.
- state transitions match the spec.
- transition ordering is explicit.
- masking does not accidentally reset stigma.
- accepted state and stigmatized state payoffs are correct.
- an optimal MDP benchmark is added or planned.

Important: do not endorse “suboptimal structural lock-in” unless the code compares learned behavior against an optimal MDP policy.

### M3

Check:

- 2K action indexing is correct.
- good pond and bad pond probabilities are assigned correctly.
- BFLPE cost is applied only where intended.
- bf* at defaults is approximately 0.470588.
- conclusions survive action-space ablations.

Required ablation plan:

1. existing 2K-arm model,
2. hierarchical context-then-behavior model,
3. global-mask model,
4. known-good-pond model,
5. multiple-good-pond model.

### M4

Check:

- p_t bounds after every update.
- accepted authenticity increases p_t.
- rejected authenticity decreases p_t.
- masking decreases p_t.
- update ordering is explicit.
- code does not call this stateful Q-learning if Q-values do not condition on p_t.
- hysteresis is tested with parameter ramp-up/ramp-down, not inferred only from split trajectories.

## Required robustness plan

Create `ROBUST_SIMULATION_PLAN.md` with these sections.

### 1. Simulation tiers

Define three compute tiers:

| Tier | Purpose | n per cell | T | Grid size | Replicates | Use |
|---|---:|---:|---:|---:|---:|---|
| smoke | catch bugs | small | small | tiny | few | CI |
| standard | reproduce figures | medium | medium | paper-sized | several | normal analysis |
| publication | robustness claims | large | long | dense/sampled | many | final results |

Choose reasonable values after inspecting runtime.

### 2. Reproducibility design

Plan:

- explicit config files,
- master seed,
- independent RNG streams per parameter cell,
- deterministic output ordering,
- run manifest JSON,
- package/environment capture,
- Git commit hash,
- result table with one row per child or one row per cell plus uncertainty summaries.

### 3. Unit and invariant tests

List tests for:

- reward equations,
- softmax,
- loss aversion,
- RNG determinism,
- M0 threshold,
- M1 endpoints,
- M2 transitions,
- M2 optimal policy benchmark,
- M3 action indexing,
- M3 BFLPE crossover,
- M4 p_t update bounds,
- final-window classification.

### 4. Statistical uncertainty

Specify:

- confidence intervals for lock probabilities,
- uncertainty for mean mask rate,
- bootstrap or binomial intervals,
- independent master-seed replication,
- threshold-location uncertainty,
- effect-size reporting.

### 5. Sensitivity analysis

Plan sweeps over:

- n,
- T,
- final-window fraction,
- alpha,
- tau,
- lambda,
- q0,
- gamma,
- p/r grid resolution,
- M2 eta,
- M3 K and p_good/p_bad,
- M4 ka/kr/km/p0.

Include both one-at-a-time sensitivity and joint sensitivity using Latin hypercube or Sobol-style sampling if feasible.

### 6. Model-specific ablations

Include:

- M1 with and without action generalization.
- M2 learned policy versus optimal MDP policy.
- M3 current 2K action formulation versus global-mask and hierarchical formulations.
- M4 endogenous p_t with km = 0, ka = 0, kr = 0, ka < kr, ka = kr, ka > kr.
- M4 true hysteresis ramp test.

### 7. Artifact outputs

Plan outputs:

```text
results/
  manifests/
  raw/
  summaries/
  figures/
  reports/
```

Each run should produce:

manifest JSON,
raw results,
cell summaries,
figures,
warnings,
runtime metadata.
8. Acceptance criteria

Define what must be true before claims can be treated as robust:

all invariants pass,
deterministic reruns match exactly,
key results survive at least three independent master seeds,
uncertainty intervals are reported,
M3 result survives action-space ablations,
M4 hysteresis is tested directly,
M2 optimal-policy benchmark exists,
conclusions are rewritten where simulations do not support them.
Required final files

Create:

CODE_REVIEW.md
ROBUST_SIMULATION_PLAN.md
VALIDATION_CHECKLIST.md

Optional, only if easy and safe:

tests/test_model_invariants.py
tests/test_reproducibility.py

Do not refactor the simulation code yet. End with a concise summary of the top five blockers and the exact next Codex task that should be run after this review.

````

---

# 3. Optional follow-up prompt after Codex produces the review

Use this after you inspect `CODE_REVIEW.md`.

````markdown
Now implement only the low-risk robustness infrastructure from the review.

Scope allowed:

1. Add deterministic config loading.
2. Add run manifests.
3. Add small invariant tests.
4. Add smoke-test CLI.
5. Add result-summary output.
6. Add uncertainty calculations for existing simulations.

Scope not allowed:

1. Do not change model semantics.
2. Do not change default parameters.
3. Do not alter published figure logic except to separate data generation from plotting.
4. Do not add large new sweeps.
5. Do not implement M3/M4 ablations yet unless they are isolated behind explicit config flags.

After changes:

- run the smoke tests,
- run the invariant tests,
- show the diff,
- summarize any behavior changes,
- state whether deterministic reruns match exactly.
````

<!-- BEGIN workspace-governance managed dispatch -->
Use `./gov check` before work and `./gov resolve` for governed context.
The adopted pack is pinned in `.governance/fleet.json`. Existing local
instructions and stronger verification duties continue to apply.
Run the declared project verifier; its managed hook checks the pack first.
<!-- END workspace-governance managed dispatch -->
