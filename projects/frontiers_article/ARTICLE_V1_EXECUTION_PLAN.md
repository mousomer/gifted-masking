# Article V1 Execution Plan

**STATUS: ACTIVE**  
**ACTIVE DELIVERABLE: ARTICLE V1**  
**DATE: 2026-08-13**

> **Authority integration notice — 2026-08-15:** This plan is an operational
> authority within the Article V1 hierarchy; it does not override the revised
> hand-off, analytic, evidence, inferential, literature, consistency-audit,
> ledger, current-state, or next-stage authorities adopted in this directory.
> When this older plan conflicts with those authorities, the Article V1
> authority index and `HANDOFF.md` control.

## Article V1 authority

ARTICLE V1 USES:

- M0–M4 model definitions;
- E01–E05 adjudicated evidence;
- analytic results already established;
- existing model/literature source material.

ARTICLE V1 DOES NOT USE:

- E06 as confirmatory evidence;
- the unexecuted E06 standard;
- new learner classes;
- new M4 experiments;
- the future intervention programme;
- Track-B research.

Historical instructions elsewhere in the repository that tell agents to
continue E06 are not active execution instructions for Article V1.

M4 may be described as part of the model architecture. Article-V1 Results must
not present an E06 result. Existing pre-E06 M4 material is architecture or
schedule-specific exploratory context only and is not confirmatory Article-V1
evidence.

## Authority order for current execution

1. Repository model/config contracts and frozen E01-E05 artifacts establish
   maintained semantics and numerical evidence.
2. `ARTICLE_V1_ANALYTIC_RESULTS.md`,
   `ARTICLE_V1_EVIDENCE_AUDIT.md`,
   `ARTICLE_V1_INFERENTIAL_AUDIT.md`,
   `ARTICLE_V1_LITERATURE_AUDIT.md`, and
   `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` govern analytic,
   evidential, inferential, literature, and interpretation constraints.
3. `ARTICLE_V1_EVIDENCE_MATRIX.csv` and
   `ARTICLE_V1_SOURCE_LEDGER.csv` map those constraints to evidence and
   provenance.
4. `ARTICLE_V1_CLAIM_LEDGER.md` governs what may be written; it may narrow,
   but never contradict, the authorities above.
5. `ARTICLE_V1_CURRENT_STATE.md` and
   `ARTICLE_V1_NEXT_STAGE.md` govern current status and authorized sequence.
6. This execution plan schedules operational work only within that hierarchy.
   `E05_MAIN_RESULTS.md`, `CLAIM_LEDGER.md`, `RDS.md`,
   `MANUSCRIPT_INTEGRATION_MAP.md`, and Stage 2 records are historical or
   implementation records unless an active authority explicitly adopts a
   compatible detail.
7. Repository `AGENTS.md` and `ARCHITECTURE.md` continue to control model,
   reproducibility, safety, and verification semantics.

The RDS defines a longer E01–E06 route. Article V1 narrows the active delivery
scope to already adjudicated E01–E05 evidence so that an initial defensible
paper can be prepared without executing E06. This changes execution priority,
not model definitions, past adjudications, RNG behavior, or historical records.

## Current stage boundaries

This stage is an evidence and governance audit. It may create audit documents
and minimal current-state/backlog pointers. It must not modify model code,
experiment configurations, RNG utilities, E01–E05 artifacts, figures, or the
manuscript.

Later Article-V1 stages may prepare the submission only after they use the
content-addressed evidence matrix and resolve every `UNRESOLVED` or `CUT`
entry. Track B remains locked by `RESEARCH_PROGRAMME.md` until Article V1 has
reached submission freeze.

## Stage V1-01 acceptance criteria

- Every candidate E01–E05 publication claim is tied to a local SHA-256 or is
  explicitly marked `MISSING_LOCAL`.
- Inferential units, independent replicate counts, seed IDs, pairing, and
  interval methods are traced to both generator code and artifact rows.
- E01/E02 commensurability, E03 comparator wording, and E05 seed extension are
  classified without new simulation.
- Stale manuscript/source values are listed for later rewrite, narrowing, or
  removal; no manuscript prose is rewritten in this stage.
- Current-state files cannot redirect an agent to E06 or Track B.
- The final diff contains governance/audit documents and minimal state/backlog
  pointers only.

## Next authorized decision

P2, bounded historical-generator-source recovery/provenance audit, is the next
Article V1 task. It begins with forensic recovery only and does not authorize
stochastic evidence reruns, literature work, manuscript drafting, figure
regeneration, evidence generation, E06, or Track B. The later V1-02 literature
work follows only after the P2 provenance disposition named in
`ARTICLE_V1_NEXT_STAGE.md`.
