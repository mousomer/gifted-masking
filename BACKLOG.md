# Backlog

## Hosted software verification

- [x] Add a pinned, read-only GitHub Actions workflow for the existing offline
  software verifier, with ephemeral outputs and no artifact publication.
- [x] Allow the explicitly selected hosted interpreter without changing local
  shared-environment policy or any original verifier obligation.
- [x] Expose the existing offline verifier as a pull-request check; Actions run
  results remain the authority for hosted execution status.

## Software verification isolation

- E06 mechanism tests isolate source/Git fixtures and source-freshness mutations.
- M2 determinism tests isolate generated outputs from canonical results.
- Governance adoption certifies declared software checks only. Scientific
  package sealing, standard/qualification execution, and claim acceptance keep
  their existing separate gates; this update imports no later local research
  history, derived artifacts, or real scientific records.

## Completed In This Restructure

- [x] Preserve legacy scripts instead of deleting them.
- [x] Define a modular package architecture.
- [x] Separate core simulation code from plotting imports.
- [x] Add a verification entrypoint.
- [x] Add baseline robustness and perturbation suites.
- [x] Make repo-local `.venv` usage an explicit policy in `AGENTS.md`.
- [x] Add RNG determinism tests across M0-M4.
- [x] Add maintained M3 ablation formulations.
- [x] Add an explicit M4 ramp-up/ramp-down path experiment.
- [x] Produce a claim-audited Frontiers in Psychology Original Research manuscript using the official Word template.
- [x] Add 300-dpi RGB submission figures, editable manuscript tables, figure alt text, and a section-specific submission checklist.
- [x] Recompute manuscript contrasts with independent within-condition bootstrap intervals.
- [x] Revise the Frontiers manuscript around assertive, quantitative findings and add an M2 phase-map figure showing the breadth of learned suboptimal masking.
- [x] Initialize `projects/frontiers_article/` with an RDS, claim ledger,
      current-state tracker, and nine-stage article backlog.
- [x] Add isolated E01 article-experiment smoke infrastructure and execute the
      approved diagnostic smoke configuration without changing M0 semantics.
- [x] Add isolated approved E02 binary-versus-independent-graded smoke
      infrastructure, artifacts, and regression coverage without changing M0
      or M1 semantics.
- [x] Harden the E02 smoke gate with strict frozen-config validation,
      provenance checks, linear stable-policy diagnostics, and repeat smoke
      equivalence verification.
- [x] Add isolated E04 M3 architecture/identity/multiple-good smoke
      infrastructure, canonical 120-to-55 equivalence metadata, and execute
      only the approved diagnostic smoke.
- [x] Implement and execute the approved E06 M4 continuation-path diagnostic
      smoke with packed raw rows, state/reset controls, strict reconstruction,
      deterministic regeneration, and a sealed pending-review checkpoint.

## Next Work

- [x] Obtain the E02-specific smoke-gate decision and execute the frozen E02
      standard package with deterministic regeneration and verification.
- [ ] Obtain separate E02 claim adjudication before any claim/ledger update,
      sensitivity work, or manuscript edit.
- [ ] Obtain the separate E01 smoke-gate decision before any E01 standard run;
      do not update claims from the diagnostic smoke.
- [ ] Expand M2 lock-in mapping beyond the current coarse `p`/`eta` grid to
      learner-parameter perturbations and threshold-local refinement.
- [ ] Obtain E04 smoke review before any E04 standard execution; do not infer
      a context-search claim from the diagnostic checkpoint.
- [ ] Tighten the M4 hysteresis experiment into a stronger claim test with
      explicit acceptance criteria for path separation.
- [x] Obtain the independent E06 Sol smoke review after user-owned repository
      verification; the decision was `FIX_IMPLEMENTATION` and no GO was issued.
- [ ] Make E06 raw validation reconstruct every frozen scalar, seed, traversal,
      reset, and p/Q continuity field; complete the canonical 13-item report and
      verification/provenance seal; then repeat the independent smoke review.
- [ ] Add richer report templates and comparison dashboards.
- [ ] Fill author-supplied manuscript fields and archive the exact analysis release with a permanent DOI.
- [ ] Replicate headline contrasts and M4 ramps across at least three independent master seeds before submission.
- [ ] Replace descriptive within-run Monte Carlo intervals with a seed-replicated uncertainty analysis for publication claims.
- [ ] Convert CSV outputs to a columnar format if the repo later accepts an
      additional dependency for that purpose.
