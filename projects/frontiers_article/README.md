# Frontiers Article Sub-project

## Purpose

Develop the maintained gifted-masking simulations into a complete, reproducible
Original Research article for the Educational Psychology section of *Frontiers
in Psychology*.

## Source Of Truth

The sub-project is governed by:

1. [`RDS.md`](RDS.md) for article scope, evidence requirements, stage gates,
   manuscript design, and publication acceptance criteria.
2. [`CLAIM_LEDGER.md`](CLAIM_LEDGER.md) for the evidential status and permitted
   wording of each article claim.
3. [`CURRENT_STATE.md`](CURRENT_STATE.md) for the active stage and immediate
   next actions.
4. [`BACKLOG.md`](BACKLOG.md) for executable work items.
5. [`MANUSCRIPT_INTEGRATION_MAP.md`](MANUSCRIPT_INTEGRATION_MAP.md) for the
   paragraph-level disposition of the four source chapters.
6. [`STAGE2_EXPERIMENT_SPECIFICATIONS.md`](STAGE2_EXPERIMENT_SPECIFICATIONS.md)
   for claim-closing experiment designs and decision rules.
7. [`runbooks/STAGE2_EVIDENCE.md`](runbooks/STAGE2_EVIDENCE.md) for the exact
   Sol/Terra execution sequence, checkpoints, stop rules, and launch prompts.

The RDS also assigns a primary Codex model, reasoning effort, and independent
release-gate reviewer to each delivery stage.

Model semantics remain governed by the repository-level `AGENTS.md`, preserved
legacy simulations, and `ARCHITECTURE.md`. This sub-project may request new
experiments and analyses, but it must not silently redefine M0-M4.

## Working Inputs

- `doc-reviews/frontiers_submission/gifted_masking_frontiers_original_research_assertive_revision.docx`
  is the current submission-format base.
- `doc-reviews/frontiers_submission/LITERATURE_REVIEW_CHAPTER.md`
- `doc-reviews/frontiers_submission/MODEL_CASCADE_CHAPTER.md`
- `doc-reviews/frontiers_submission/RESULTS_BY_FINDING_CHAPTER.md`
- `doc-reviews/frontiers_submission/DISCUSSION_CHAPTER.md`
- `results/` contains maintained analysis artifacts.

The four Markdown chapters are source material. They are not four additional
standalone sections to paste into the article.

## Expected Delivery Path

The RDS defines nine stages:

1. establish the source of truth;
2. close essential evidence gaps;
3. lock article architecture;
4. complete Materials and Methods;
5. produce figures and tables;
6. write final Results;
7. integrate Introduction and Discussion;
8. run the full manuscript audit;
9. assemble the Frontiers submission package.

Stage 1 is complete. Stage 2 is active; its experiments have been specified but
not yet implemented or run. The Stage 2 operational runbook is ready.
