# Article V1 — Next Stage Execution Plan

**As of:** 15 August 2026  
**Starting condition:** model-analysis consistency audit complete; numerical E01-E05 evidence intact; publication blockers remain.

This plan supersedes the earlier hand-off sequence that moved directly to literature completion. The new audit requires authority adoption and a bounded provenance disposition first.

# Stage H0 — Adopt the revised hand-off authorities

**Status:** COMPLETE in P0/P1.

## Goal

Make the repository, not chat history or detached DOCX files, the publication-state authority.

## Actions

Install under the canonical Article-V1 documentation location:

- `HANDOFF.md`
- `ARTICLE_V1_CURRENT_STATE.md`
- `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md`
- `ARTICLE_V1_ANALYTIC_RESULTS.md`
- `ARTICLE_V1_LITERATURE_AUDIT.md`
- `ARTICLE_V1_CLAIM_LEDGER.md`
- `ARTICLE_V1_SOURCE_LEDGER.csv`
- `ARTICLE_V1_NEXT_STAGE.md`
- `HANDOFF_CONSISTENCY_AUDIT.md`

Update the project README so these are clearly marked active. Mark older conflicting `CURRENT_STATE.md`, `CLAIM_LEDGER.md`, old manuscript chapters, and E06 instructions as historical/superseded for publication interpretation.

## Prohibitions

No code, config, artifact, figure, or stochastic run changes.

## Exit gate

A new agent can clone the repo, follow `HANDOFF.md`, and find all named authorities without chat context.

# Stage H1 — Generator-source provenance recovery

**Status:** P2 FORENSICS COMPLETE / PARTIAL RECOVERY. E04 and E05 are
`HISTORICAL_SOURCE_RECOVERED`; E01–E03 are
`ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`. The exit gate remains open for
E01–E03 pending P2B or explicit owner acceptance.

## Goal

Resolve the historical dirty-source gap for frozen E01-E05 evidence without changing scientific design.

## Phase A — forensic recovery only

Search for exact historical source bytes/patches using:

- Git reflog;
- dangling/unreachable commits and blobs;
- stashes;
- old worktrees and local branches;
- Codex/workspace snapshots;
- editor/local-history files;
- filesystem backups;
- run-specific source archives;
- any patch/source bundle matching manifest dirty-diff/source fingerprints.

Create:

`ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md`

with at least:

```text
experiment
run_commit
recorded_source_fingerprint
recorded_dirty_diff_hash
historical_source_recovered
recovered_location
recovered_hash
current_source_relation
disposition
```

## Phase B — disposition

If exact historical source is recovered:

`HISTORICAL_SOURCE_RECOVERED`

Archive it immutably. No rerun is required.

If not recovered:

`ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`

Do not pretend the historical source is known. Prepare a **separate authorization request** for deterministic provenance reproduction from:

- current maintained source;
- frozen configs;
- frozen seeds;
- exact expected protected-output hashes.

Such a reproduction is provenance repair, not new scientific design, but it still requires explicit authorization because it executes the experiments.

## Exit gate

Before submission, each E01-E05 run must have either:

- `HISTORICAL_SOURCE_RECOVERED`; or
- `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE` plus a clean reproduction anchor approved and completed.

# Stage H2 — Four bounded literature searches

No broad literature accumulation.

## Search A — persistent social-state prior art

Question:

> Has prior formal work modeled concealment/disclosure where actions change persistent reputation, stigma, acceptance, exclusion, or related social state under incomplete learning?

Must distinguish:

- ordinary MDP state;
- generic incomplete learning;
- specifically social/reputation/stigma state;
- static disclosure from state-changing dynamic disclosure;
- full-information oracle from information-constrained optimum.

## Search B — scarce receptive-context prior art

Question:

> Has prior formal work modeled agents who must discover rare favorable/receptive audiences, partners, groups, or contexts under uncertainty?

Must distinguish:

- larger action count;
- fixed number vs fraction of favorable contexts;
- known-good controls;
- matching/search/contextual-bandit analogues;
- literal mobility from abstract repeated context selection.

## Search C — graded/partial disclosure

Question:

> After accounting for generic independent-arm sample allocation, is there a disclosure-specific formal mechanism relevant to the E02 result?

Look for ordered/continuous/partial disclosure, selective revelation, and whether models share information across neighboring disclosure levels.

## Search D — terminology

Resolve the relationship among:

- masking;
- camouflaging;
- concealment;
- visibility/information management;
- compensation;
- conformity;
- social coping;
- partial disclosure.

Do not transfer autism empirical findings into giftedness; use adjacent literature only for terminology/construct comparison.

## Search stopping rule

Each search ends as:

- `RESOLVED`
- `PARTIALLY_RESOLVED`
- `UNRESOLVED`

with a reason. No fifth broad search unless one of these returns a specific publication-critical unresolved source.

# Stage H3 — Final V1-02 synthesis

Create/update:

- `ARTICLE_V1_NOVELTY_AUDIT.md`
- `ARTICLE_V1_CONSTRUCT_AUDIT.md`
- `ARTICLE_V1_CITATION_CLAIM_MAP.csv`
- `ARTICLE_V1_STAGE02_DECISION.md`

For each E01-E05 classify one primary role:

- `FORMAL_NOVELTY`
- `APPLICATION_NOVELTY`
- `SYNTHESIS_NOVELTY`
- `STRUCTURAL_RESULT`
- `SUPPORTING_DEMONSTRATION`
- `BACKGROUND_ONLY`
- `UNRESOLVED`

Mandatory adversarial question:

> If masking/authenticity were renamed Action A/Action B, what remains scientifically distinctive?

Then choose exactly one gifted framing:

- `GIFTED_CENTRAL`
- `GIFTED_APPLICATION`
- `GIFTED_TOO_WEAK`

Finally write:

1. a maximum 1-3 sentence technical contribution;
2. a safer version.

If no defensible contribution survives, stop before manuscript drafting.

# Stage H4 — V1-03 adversarial claim freeze

Review every row in `ARTICLE_V1_CLAIM_LEDGER.md`.

Final decision per scientific claim:

- `KEEP`
- `NARROW`
- `BACKGROUND_ONLY`
- `SUPPLEMENT_ONLY`
- `CUT`

No `MAYBE`.

Automatic prohibitions include:

- persistent final masking from one rejection;
- independent evidential counting of E01 sampling + regret;
- independent welfare interpretation of E02 regret;
- E03 prevalence or information-matched failure;
- K-alone/scarcity-alone E04 causation;
- E05 temperature exclusion;
- M4/E06 confirmatory V1 evidence.

## Exit gate

No manuscript scientific assertion may be introduced without a frozen claim ID.

# Stage H5 — Rebuild manuscript from authorities

Do **not** patch the stale Results/Discussion chapters line by line.

## Results source order

1. frozen evidence matrix/artifacts;
2. claim ledger;
3. analytic authority;
4. consistency audit.

## Methods source order

1. frozen configs;
2. maintained model source;
3. experiment reports/manifests;
4. inferential audit;
5. provenance disposition.

## Introduction / Discussion

Only after novelty and claims are frozen.

M4 may appear only as explicitly future/Track-B context if retained at all.

## Figures

Regenerate only after Results are frozen and deterministic figure-source provenance is established.

# Stage H6 — Final submission audit

Run separate:

1. numerical audit — every number maps to artifact + selector + transform + inferential unit;
2. citation audit — every literature claim maps to source ledger;
3. mathematical audit — every theorem/equation maps to analytic authority;
4. claim audit — every scientific assertion maps to frozen claim ID;
5. provenance audit — historical-source/reproduction disposition is explicit.

Search explicitly for stale material:

- `226/357`;
- `63.3%`;
- one-seed/child-bootstrap wording;
- obsolete E04 K comparisons;
- old sample-size/RNG descriptions;
- M4/E06 numerical Results;
- language ruling temperature out for E05.

# Stage H7 — Submission freeze

Create `ARTICLE_V1_SUBMISSION_FREEZE.md` containing:

- commit SHA;
- manuscript hash;
- figure/table hashes;
- evidence-manifest hashes;
- analytic-authority hash;
- literature-audit hash;
- source-ledger hash;
- claim-ledger hash;
- provenance disposition.

Only after this freeze may Track B resume.

# Work prohibited now

Unless a later explicit gate authorizes it, do not:

- run E06;
- use M4 numerical results as V1 evidence;
- extend E05 seeds;
- run exploratory E01-E05 sensitivities;
- change models, reward functions, learner architecture, RNG hierarchy, or configs;
- create an information-matched M2 optimum as an unreviewed V1 addition;
- run the full repository verification script if it triggers stochastic robustness generation or E06 work outside the authorized scope;
- draft from stale Results/Discussion chapters;
- use the binary softmax theorem to exclude temperature from E05.

# Immediate next task

**P2B — separately authorized clean deterministic reproduction anchors for
E01–E03.**

The revised authorities are installed and the historical-source disposition is
recorded in `ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md`. The bounded
literature searches begin only after P2B is completed, unless the project owner
explicitly accepts the remaining E01–E03 provenance limitation for submission.
