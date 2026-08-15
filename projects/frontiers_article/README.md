# Article V1 — Authority Index

## Purpose and evidence boundary

This directory contains the editable, active publication authorities for
Article V1 of the gifted-masking project.

> **Article V1 confirmatory evidence is E01-E05 only.**
>
> E06 is excluded. M4 may appear only as model architecture or future-work
> context. Track B is frozen until the Article V1 submission freeze.

The dated hand-off snapshot at
`doc-reviews/handoff_august2026/Gifted_Masking_Article_V1_Handoff_Pack_REVISED_2026-08-15/`
is immutable provenance. The files listed below under *Active scientific
authorities* are its editable repository adoption.

## Authority hierarchy

```text
maintained model/config contracts + frozen E01-E05 artifacts
        ↓
analytic, evidence, inferential, literature, and consistency-audit authorities
        ↓
evidence/source ledgers
        ↓
claim ledger
        ↓
current-state and next-stage authorities
        ↓
manuscript prose, figures, and abstract
```

Claim-ledger decisions govern what may be written. They may narrow evidence but
may never contradict model/config contracts, frozen artifacts, or the analytic,
evidence, inferential, literature, and consistency-audit authorities. If
authorities conflict, preserve the lower-layer mathematical or evidential fact
and narrow the higher-layer claim.

## Active scientific authorities

Read these in the order appropriate to the question; `HANDOFF.md` gives the
canonical hand-off read order.

1. [HANDOFF.md](HANDOFF.md) — current operating boundary, authority model, and
   hand-off constraints.
2. [ARTICLE_V1_CURRENT_STATE.md](ARTICLE_V1_CURRENT_STATE.md) — publication
   state, evidence boundary, and open blockers.
3. [ARTICLE_V1_ANALYTIC_RESULTS.md](ARTICLE_V1_ANALYTIC_RESULTS.md) — exact
   reward, learner, and dynamic-programming results.
4. [ARTICLE_V1_EVIDENCE_AUDIT.md](ARTICLE_V1_EVIDENCE_AUDIT.md) — frozen
   evidence and artifact audit.
5. [ARTICLE_V1_INFERENTIAL_AUDIT.md](ARTICLE_V1_INFERENTIAL_AUDIT.md) —
   inferential and replication audit.
6. [ARTICLE_V1_LITERATURE_AUDIT.md](ARTICLE_V1_LITERATURE_AUDIT.md) —
   literature, construct, and novelty constraints.
7. [ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md](ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md) —
   mathematical/implementation consistency corrections and gap register.
8. [ARTICLE_V1_EVIDENCE_MATRIX.csv](ARTICLE_V1_EVIDENCE_MATRIX.csv) — frozen
   evidence-to-claim mapping.
9. [ARTICLE_V1_SOURCE_LEDGER.csv](ARTICLE_V1_SOURCE_LEDGER.csv) — source and
   provenance ledger.
10. [ARTICLE_V1_CLAIM_LEDGER.md](ARTICLE_V1_CLAIM_LEDGER.md) — the
    publication-facing decision ledger.
11. [ARTICLE_V1_NEXT_STAGE.md](ARTICLE_V1_NEXT_STAGE.md) — authorized sequence
    of remaining work.
12. [ARTICLE_V1_EXECUTION_PLAN.md](ARTICLE_V1_EXECUTION_PLAN.md) — evidence
    execution and release-plan record.

The immediate Article V1 task after this adoption is P2, bounded
historical-source recovery/provenance audit. It must not rerun stochastic
evidence or start E06/Track B.

## Historical / non-authoritative material

The following are retained for provenance, implementation history, or source
material. They do **not** override the Article V1 authority set:

- [CURRENT_STATE.md](CURRENT_STATE.md) and [CLAIM_LEDGER.md](CLAIM_LEDGER.md),
  which are older Stage-2 governance records.
- [RDS.md](RDS.md), [BACKLOG.md](BACKLOG.md),
  [STAGE2_EXPERIMENT_SPECIFICATIONS.md](STAGE2_EXPERIMENT_SPECIFICATIONS.md),
  [STAGE2_EXECUTION_LOG.md](STAGE2_EXECUTION_LOG.md), and
  [MANUSCRIPT_INTEGRATION_MAP.md](MANUSCRIPT_INTEGRATION_MAP.md), which are
  historical planning or implementation records unless an active authority
  explicitly adopts a compatible detail.
- The old Results, Discussion, Literature, and Model Cascade source chapters
  under `doc-reviews/frontiers_submission/`, plus manuscript DOCX snapshots.
- E06 instruction, implementation, approval, checkpoint, and review documents.
- Old one-seed, pre-E01-E05, or superseded analysis notes and figures.

Article V1 Results and Discussion must later be rebuilt from the frozen
evidence matrix, analytic authority, inferential audit, and frozen claim
ledger. Legacy manuscript chapters are historical source material and must not
be used as numerical authority.

## Scope safeguards

- The active authority files may not authorize a model-semantic change,
  experiment rerun, new seed, new sensitivity sweep, or Track-B work by
  implication.
- E01-E05 protected output hashes reconcile, and current model semantics,
  validators, and reconstructions support the frozen evidence. The exact dirty
  generator source tree for those historical frozen runs is not reconstructible
  from Git plus manifests alone; manifests retain fingerprints, but not all
  historical source bytes. This is an open
  `ARTIFACT_PROVENANCE_GAP_OPEN`, not evidence corruption.
- M4/E06 numerical findings must not support any Article V1 Results,
  Discussion, or confirmatory conclusion.
