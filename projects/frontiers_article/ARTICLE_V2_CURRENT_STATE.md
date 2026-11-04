# Article V2 — Current State

**ARTICLE VERSION:** V2

**TARGET JOURNAL:** *Learning and Individual Differences*

**SOURCE EVIDENCE:** Frozen Article V1 E01–E05 evidence base

**E06/M4:** DEFERRED; outside V2 numerical Results and confirmatory Discussion
claims unless a later explicit authority changes that decision.

## Current status

**STATUS:** `INTEGRATED_ILLUSTRATED_ARTICLE_COMPLETE`

**READINESS:** `SINGLE_ARTICLE_READY_FOR_AUTHOR_REVIEW`

**NEXT:** `AUTHOR_REVIEW_OF_INTEGRATED_ARTICLE`

**ACTIVE V2 MANUSCRIPT:** `integrated_article_20261004/ARTICLE.md`

**TECHNICAL METHODS:** Internal Appendix A in the same article; no separate
supplement is needed to read this edition.

## Integrated illustrated article — 4 October 2026

The author requested a single article with more figures. The completed
edition is `integrated_article_20261004/ARTICLE.md`, governed by RDS 0.11.
It contains the essential supplementary methods and an internal technical
appendix, ten inline figures, and matching 32-page editable DOCX/PDF deliverables.
The earlier September manuscript and supplement remain preserved source
editions. All 23 supported claims are retained, with newly visible complete
dynamic-grid and sensitivity outcomes.

Checkpoint: governance preflight passed; 66 focused tests, read-only numerical
and source checks, native-equation production checks, and every-page visual
inspection passed. Ten figures are available as PNG/SVG, with all editable
wording in one catalog. E01–E05 are unchanged. The artifact-writing
full simulation verifier is outside this editorial scope; its governance hook
and relevant read-only tests were run separately and are reported explicitly.
The next step is author review; this does not close the earlier persistent-deposit
or journal-submission controls. See `integrated_article_20261004/QA.md`.

## Supported-claims revision — 29 September 2026

**Presentation tooling, 1 October 2026:** The author requested a clearly
documented figure-generation and text-editing entry point. Work is limited
to the active revision's display layer under RDS 0.10; scientific sources,
historical figures, and manuscript text remain unchanged. Status:
`FIGURE_TEXT_INTERFACE_COMPLETE`. The active text catalog is
`revision_20260929/figure_text.py`; the function directory, edit examples,
and safe preview commands are in `revision_20260929/FIGURE_EDITING_GUIDE.md`.
All 14 new tooling tests and 33 existing targeted tests passed. Default
regeneration is byte-identical for all six PNG/PDF pairs, with unchanged
plotted-data records and input hashes. Read-only revision verification and
rendered visual checks passed. See the dated addendum in `REVISION_QA.md`.

The author authorized the chapter-by-chapter rewrite using the 23-claim review
and three contribution categories. The design and acceptance criteria are in
`revision_20260929/REVISION_PLAN.md`. Earlier V2 source, audited manifests,
submission previews, and E01–E05 evidence are preserved. The new revision is
not the historical Stage 11.5 candidate or a submission-ready production
package. The records below are retained as historical stage records.

Implementation and QA are complete: all six chapters, 26 numbered main
subsections, educational implications, S1–S10, all 23 claims, and six revised
figures are aligned. The 144-word Abstract and five keywords are present.
Read-only validation passed 33 protected outputs, 18 evidence-matrix
references, 33 targeted tests, all claim routes, numerical anchors, caption
identities, and figure provenance. All six final PDFs passed rendered visual
inspection. No experiment or estimator was rerun. See
`revision_20260929/REVISION_QA.md` for verification and the remaining
author-review/production steps.

**EDITORIAL_GOVERNANCE:** `CLAIM_CALIBRATION_POLICY_ACTIVE` (Stage 3.5,
2026-08-20)

## Stage 12 submission-production record

Stage 12 performed the authorized production and verification work on 21
August 2026 without changing the Stage 11.5 scientific candidate. The repaired
candidate manifest remains exact at
`1ef1a5252891d7f69c8e4f112765256d4a41dd51381ef4672d15b06801168124`
and validates 67/67 inputs. The frozen manuscript and Supplement hashes remain
`217d259929f5d0c585bf9da1de3c33befb8403b57a79a0c4f5257627ab0f5199`
and
`a413ee282e108dc225d8e2f29b74263dbdb514eb5cc6af89eeec64267dc929ce`.

Current official *Learning and Individual Differences* requirements were
checked on 21 August 2026. The 6,264-word primary text is within the 8,000-word
maximum, but the scientifically frozen 221-word Abstract exceeds the current
150-word hard limit. Stage 12 was not authorized to revise the Abstract, so the
controlling readiness verdict is `BLOCKED_BY_JOURNAL_WORD_LIMIT`.

A controlled package now exists under `submission_v2/`: a double-anonymized
manuscript DOCX/PDF preview, separate pending-confirmation title page, required
highlights, Supplementary Methods DOCX/PDF, four separate vector figure PDFs,
cover-letter draft, metadata and declaration controls, final production QA,
submission manifest, and a non-activated scientific-freeze record. Visual QA
covered all 36 main pages, all 18 Supplement pages, every other rendered page,
and all four upload figures. Equations, tables, references, captions, links,
and scientific qualifiers passed. Figure 3A remained legible at production
scale and required `NO_CHANGE`.

The exact local E01-E05 evidence payload is
`submission_v2/archive/ability_concealment_e01_e05_evidence.zip`, SHA-256
`71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb`.
Its 101 manifest-bound payload files pass independent hash validation and the
ZIP is structurally valid. The package excludes E06/M4 and former Figure 6,
retains all 33 protected outputs, and preserves the established distinction
between `ARTIFACT_VERIFIED` E01-E05 outputs and
`HISTORICAL_SOURCE_STATE_UNRECOVERED` E01-E03 generator states.

No repository authority selected a persistent archive provider. Zenodo was
inspected but no authenticated deposit, DOI, or persistent URL was created.
The archive therefore also remains `BLOCKED_BY_ARCHIVAL_IDENTIFIER`. Author
confirmation is required for author/order, affiliations, corresponding-author
metadata, ORCIDs, CRediT, funding, competing interests, acknowledgements,
originality/concurrent submission, the AI-use declaration, archive provider
and license, deposit publication, and any reviewers.

Read-only validation passed 33/33 protected outputs and 18/18 evidence-matrix
references. No experiment, robustness suite, stochastic fixture, alternate
estimator, or figure generator ran. The Git index was empty, but no selective
checkpoint was created because the final-readiness conditions failed. No push,
PR, external archive publication, or journal submission occurred. The detailed
41-item report is
`submission_v2/qa/ARTICLE_V2_LID_STAGE12_FINAL_QA.md`.

## Stage 11.5 dual-audit reconciliation and bounded-repair record

Stage 11.5 completed on 2026-08-21 under
`ARTICLE_V2_LID_STAGE11_5_AUDIT_REPAIR`. It preserved the independent Formal
Sol and Claude Fable reports unchanged. Their SHA-256 values remain
`1d5f3986a0389d6013dca6323ffeca97b18c7fce2bbc8adb622b83c16b96cfa4`
and
`c413cabccff320395f953e868f9a9bbed1104b876d4b1b9c6205c7b6efc595eb`,
respectively. Fable was blind to the Sol report; absence from the other report
was not used against any finding.

The Sol audit retained its P0/P1/P2/P3 counts of 0/1/2/2 and
`READY_AFTER_BOUNDED_REPAIRS` verdict. The Fable audit retained 0/1/2/9 and
`ADVISORY_MAJOR_ISSUES_FOUND`. Reconciliation classified the title and
Data/Code findings as `SAME_ISSUE_DIFFERENT_SEVERITY`, Figure 1 as
`CONVERGENT`, the confirmed E04 slope-semantics and E03 five-plus-two findings
as `FABLE_ONLY`, and the two Sol P3 observations as `SOL_ONLY`. No unresolved
`CONTRADICTORY_ASSESSMENT` remains.

Authority inspection confirmed that E04's +0.05064, +0.02524, +0.06044, and
+0.11224 quantities are changes in the estimated per-$\log_2 K$ slope relative
to the one-good-context regime. Public Results wording was corrected without
changing the four values, the primary −0.234000/−0.470400 contrasts, estimator,
first-index `argmax`, data, confidence intervals, evidence matrix, or figures.
Authority also confirmed that E03's seven inconclusive cells comprise five
cells with inadequate Neutral exposure in all masters plus two cells with only
one or two adequate agreeing masters, below the four-of-five stability rule.
Main text, Supplement, and caption now preserve that 5+2 reason without
changing 107/243/7 or 243/357.

The Supplement title now exactly matches the final main title. Figure 1 was
regenerated through the new deterministic `--figure 1` presentation-only path;
PDF and PNG visual inspection found no remaining overlap and confirmed the
conceptual hierarchy and E01–E05 mapping. Its new PDF/PNG hashes are
`02ab24130d8554eb95725bdb64fcb8b6f091ed94e3e5d4af6834b6c2c7cdd54f`
and
`68b4794f12ee09f4bd9a43a6660e6a13c2aa8c5b199d5142408688cdee9ae391`.
All six Figure 2–4 PDF/PNG hashes remain unchanged.

The public project repository was verified at
`https://github.com/mousomer/gifted-masking`; no defensible DOI, Zenodo, OSF,
or other persistent archival identifier exists in current authority. The
Data/Code placeholder was replaced by a truthful public-repository statement.
The exact content-addressed evidence deposit and persistent identifier remain
`REQUIRED_BEFORE_SUBMISSION` in Stage 12.

The eight modified audited inputs are recoverable under
`audit_snapshots/stage11_pre_repair/`; snapshot-manifest SHA-256
`b399002f733a3d142163278e4b248c09322785aa6c63df9cf52ca7d75941ebad`
verifies 9/9 files, including the preserved generator source. The original
Stage 11 manifest remains unchanged at
`4bcc1136652e219ee7b5047f14646b3ece0aefe183e875d962b46be3943018a5`.
It verified 62/62 immediately before repair and now differs at exactly the
eight approved inputs.

The complete authority decisions and focused delta audit are in
`ARTICLE_V2_LID_STAGE11_5_DUAL_AUDIT_RECONCILIATION.md`, SHA-256
`59d9fbaec87a6660986fb3cc99c666c8cb2f99d4c3b970b51fa86cd777743f30`.
The repaired candidate is content-addressed by
`ARTICLE_V2_LID_STAGE11_5_REPAIRED_CANDIDATE_PACKAGE.md`, SHA-256
`1ef1a5252891d7f69c8e4f112765256d4a41dd51381ef4672d15b06801168124`;
all 67 declared scientific, presentation, audit, and provenance inputs verify.

Read-only post-repair validation returned 33/33 protected E01–E05 outputs and
18/18 evidence-matrix references. Main and Supplement references remain 13 + 1
= 14 unique, with byte-identical reference sections and unchanged citation-year
tokens. The Abstract and main title are byte-identical to the audited candidate.
Public text contains no workflow/auditor language, no stale stronger title, and
no substantive prohibited regression. No experiment, robustness suite,
stochastic fixture, or Figures 2–4 generator ran. Only Figure 1 was regenerated.

P3 items not repaired were adjudicated individually: thin master coverage and
E01 framing are `OPTIONAL_NO_CHANGE`; E05 temporal-vocabulary concern was
`REJECT_AFTER_AUTHORITY_CHECK`; public archive indexing, acknowledgements
copyediting, strict citation-initial style, and Figure 3A layout were routed to
Stage 12 production. L&ID positioning, Limitations, citations, title selection,
and Abstract were not reopened.

Stage 12 must complete the permanent evidence identifier, final journal file
naming and formats, DOCX/PDF conversion, submission metadata, final author
declarations and copyediting confirmation, cover letter, graphical-file
requirements, and supplement upload package. These are production items and do
not block Stage 11.5 closure. Candidate verdict:
`READY_WITH_STAGE12_PRODUCTION_ITEMS`; governance readiness:
`READY_FOR_STAGE12`.

## Stage 11 independent scientific audit record

Stage 11 was completed on 2026-08-20 against the immutable 62-input package
defined by `ARTICLE_V2_LID_STAGE11_AUDIT_PACKAGE.md`, manifest SHA-256
`4bcc1136652e219ee7b5047f14646b3ece0aefe183e875d962b46be3943018a5`.
The manifest itself matched that identity, and all 62 declared inputs passed
read-only hash verification before substantive analysis (`62/62 VALID`).

The audit report is
`ARTICLE_V2_LID_STAGE11_INDEPENDENT_SCIENTIFIC_AUDIT.md`. It independently
reconstructed the E01 and E02 headline contrasts from raw learners; the E03
Bellman comparator and aggregate classifier; E04/E05 deterministic first-index
`argmax` semantics; and the E05 reward boundary, pooled PAVA crossing, and
displacement. It visually inspected the four frozen main figures and checked
the central literature claims against original publisher records. No
experiment, stochastic entry point, publication builder, or figure generator
was run. No audited package input was modified.

The audit counts and verdict are:

| Severity | Count |
| --- | ---: |
| P0 — submission blocker | 0 |
| P1 — major correction required | 1 |
| P2 — minor scientific/editorial correction | 2 |
| P3 — optional improvement | 2 |

The central thesis verdict is `SUPPORTED_WITH_MINOR_QUALIFICATION`. E01–E05
are each `SUPPORTED`; the cross-experiment conclusion is
`SUPPORTED_SYNTHESIS`; provenance is
`PROVENANCE_ADEQUATE_WITH_DISCLOSED_LIMITATION`; and L&ID fit is
`ADEQUATE_LID_FIT`.

The submission verdict is `READY_AFTER_BOUNDED_REPAIRS`. The P1 is a
main/supplement title contradiction: supplement line 3 retains “Does Not
Reveal” rather than the calibrated final “Does Not Uniquely Reveal.” The P2s
are overlapping labels/boxes in frozen Figure 1 and the unresolved public
archival-identifier placeholder. Stage 11 did not repair these defects.

The exact next stage is `ARTICLE_V2_LID_STAGE11_5_AUDIT_REPAIR`. It must remain
bounded to title synchronization, Figure 1 layout repair and hash
reconciliation, plus routing of the archival identifier to Stage 12 if it is
not yet available. Stage 12 submission production must not begin until the
bounded repairs receive an independent consistency reconciliation.

Final static validation retained `62/62 VALID` package hashes and
`git diff --check` passed with no output. Final Git status remains heavily
dirty as inherited: 52 entries comprising 18 modified, six deleted, and 28
untracked paths. The new Stage 11 report and the updated V2 current-state file
are untracked. Nothing was staged, committed, pushed, reset, cleaned, stashed,
or branch-switched.

## Stage 10.5 post-citation reconciliation record

Stage 10.5 was completed on 2026-08-20 as a bounded editorial consistency
pass. It reconciled the two Stage 10 positioning additions, title scope,
Educational Relevance redundancy, environmental-legibility terminology,
main/supplement reference routing, and submission-facing provenance language.
No experiment, stochastic entry point, publication builder, or figure
generator was run. No result, equation, threshold, confidence interval,
estimator, configuration, implementation file, frozen evidence artifact,
figure, or standalone caption changed.

### Title decision

Four formulations were considered:

1. “Ability Concealment Does Not Reveal the Environment...”;
2. “Ability Concealment Does Not Uniquely Reveal the Environment...”;
3. “Ability Concealment Does Not Uniquely Identify the Environment...”; and
4. “When Ability Concealment Does Not Reveal the Environment....”

The selected title is:

> **Ability Concealment Does Not Uniquely Reveal the Environment: Learning and
> Social Opportunity in Gifted Learners**

The original failed the technical acceptance test because “does not reveal”
could imply that concealment contains zero information about the environment.
The selected formulation retains the title's readable reveal/environment
parallel while making the non-unique-identification claim explicit. “Does Not
Uniquely Identify” was equally precise but more technical; “When...” weakened
the article's general inference framing. The Abstract already states that
observed behaviour may underidentify its sources and required no change.

### Scholarly integration

Introduction 1.2 now gives one clean progression: the empirical inference
problem, equifinality as the established developmental principle, and the
article-specific decomposition. The new text explicitly attributes the
general principle to Cicchetti and Rogosch (1996) and defines the present
contribution as specifying how current reward structure, learning history,
action representation, persistent social dynamics, and contextual
discoverability create observational ambiguity in ability concealment. The
nearby opening paragraph was compressed to avoid repeating the same list.

Discussion 4.4 now states that antecedent goals, disclosure events, and
postdisclosure outcomes are an established dynamic process in Chaudoir and
Fisher (2010). E03 is then positioned at the correct novelty level: it applies
that logic to ability concealment through persistent social states and a
finite-learner versus full-information dynamic comparison. The two-sentence
positioning paragraph remains subordinate to the subsection's substantive
answer about dynamically adaptive masking and learned–oracle disagreement.

The Stage 10 queue described a duplicated “A practical target...” line in
Educational Relevance. Direct inspection found only one occurrence; deleting
it would have removed the section's actionable content. The actual redundant
recap was the following sentence, “This moves the focus from the number of
opportunities to their behavioural usability,” which repeated the subsection
heading and opening availability/discoverability contrast. That recap was
removed. The five-part mechanism-matched structure remains intact.

### Environmental legibility and public text

Environmental legibility remains `PARTIAL_OVERLAP` and model-derived. The
Discussion now calls it a “model-derived descriptive term”; Educational
Relevance states its practical recognition requirement without redefining it
as a validated construct; and Limitations retains the single qualification
that its relation to established constructs and empirical operationalization
remain open. No neighbouring construct was treated as equivalent and no
repeated disclaimer was added.

Submission-facing provenance was reconciled without weakening reproducibility:

- the main manuscript now uses archived-result language rather than internal
  evidence-freeze or planning language;
- the supplement replaces the internal `V2` generator label, repository path,
  readiness tokens, and pending-authority token with public scientific prose;
- archived hashes, manifests, the distinction between presentation and
  experiment reproduction, and the E01–E03 historical generator-state limit
  remain explicit; and
- scans of the manuscript and supplement find no stage labels, branch/worktree
  language, `READY_` tokens, governance terms, E06/M4 notices, or Codex text.

### Reference routing and formatting

The final routing is:

- main manuscript: 13 references, all cited in public main text;
- supplement-only: Best and Chakravarti (1990), cited only for PAVA/isotonic
  regression; and
- total unique references: 14.

Separate main and supplement bijection checks pass. Phillipson, Bird,
Cross–Coleman–Terhaar-Yonkers, Hornstra, Kerr/Huffman, and Spears have no
dangling text or reference entry. Cicchetti and Rogosch support only the
equifinality positioning; Chaudoir and Fisher support only the dynamic
disclosure positioning. The in-text spelling `Klimecka` was reconciled to the
reference-author spelling `Klimecká`. No value-iteration citation placeholder
exists, and no technical reference was added to the main list. The Stage 10
measurement inventory remains in the scholarly audit rather than the public
manuscript.

### Word budget

Counts use the established manuscript-count authority and Stage 10 section
baselines, with exact whitespace-word deltas for the bounded replacements.

| Section | Stage 10 | Stage 10.5 | Change |
| --- | ---: | ---: | ---: |
| Abstract | 221 | 221 | 0 |
| Introduction | 1,272 | 1,271 | -1 |
| Methods | 1,416 | 1,399 | -17 |
| Results | 1,535 | 1,535 | 0 |
| Discussion | 1,662 | 1,670 | +8 |
| Limitations | 370 | 370 | 0 |
| Conclusion | 192 | 192 | 0 |
| **Primary-text subtotal** | **6,447** | **6,437** | **-10** |
| Educational Relevance | 709 | 691 | -18 |
| **Total excluding references and figure captions** | **7,377** | **7,349** | **-28** |

The Abstract, Results, and Conclusion are unchanged. The title is 15 words
under the existing title-count convention.

### Supplement consistency and Stage 11 package

`ARTICLE_V2_LID_SUPPLEMENT_MAIN_TEXT_CONSISTENCY.md` records the Stage 10.5
recheck. All E01–E05 rows remain `CONSISTENT`, including E01 sampling,
E02 independent arms, E03 classifier/oracle, E04 first-index `argmax`, and E05
PAVA crossing semantics.

The immutable Stage 11 candidate is defined in
`ARTICLE_V2_LID_STAGE11_AUDIT_PACKAGE.md`, SHA-256
`4bcc1136652e219ee7b5047f14646b3ece0aefe183e875d962b46be3943018a5`.
It content-addresses 62 inputs: the main manuscript and supplement; all eight
Figure 1–4 PDF/PNG files and three figure-support records; the evidence freeze,
evidence matrix, interpretation notes, analytic/inferential/consistency audits,
Stage 10 scholarly audit, and supplement-main consistency matrix; plus the five
experiment manifests and all 33 protected E01–E05 outputs. It explicitly
excludes E06/M4, superseded figures, unlisted working notes, and former Figure
6. Stage 11 has not begun.

Because the active manuscript, supplement, governance files, figure package,
and Stage 11 package remain untracked in a heavily dirty worktree, the
operational recommendation is
`CHECKPOINT_RECOMMENDED_BEFORE_INDEPENDENT_AUDIT`. No checkpoint, commit,
stage, push, or PR action was performed.

### Validation and identity

- Main manuscript SHA-256:
  `4282ff16f18591553b862461499c28e493700911cbfa7cccf093dc95e5664a63`.
- Supplement SHA-256:
  `a7124c8cf363ba96db8b6c640ef40627044321f3b8c61870e5049b3c6f5ed9f5`.
- Main references: 13; supplement-only references: 1; total unique: 14.
- Protected E01–E05 outputs: 33/33 valid.
- Evidence-matrix references: 18/18 valid.
- Stage 11 manifest entries: 62/62 hash-valid.
- All eight Figure 1–4 hashes retain the Stage 7/10 values.
- Standalone captions retain SHA-256
  `aec20cfeede5934d0825907405e11b322eeb4b3130e2c03dfc21613fad5845f9`.
- Article V1 remains byte-identical at
  `cd27687bdb5f3144172822ba2ff996f59efcdbf5398a905564a8177a345cdae9`.
- Stale-concept hits are limited to explicit negations of a temporal “give up”
  interpretation and binary-softmax identity; no substantive stale claim is
  present.
- No public-text novelty claim exceeds the Stage 10 compositional and
  application-specific conclusion.
- `git diff --check` and final status are recorded after this governance
  update.

No Stage 10.5 blocker was found. Readiness is `READY_FOR_STAGE11`; next is
`ARTICLE_V2_LID_STAGE11_INDEPENDENT_SCIENTIFIC_AUDIT`.

## Stage 10 supplement and citation-completion record

Stage 10 was completed on 2026-08-20 as two coordinated, documentation-led
workstreams. No experiment, stochastic entry point, publication builder, or
figure generator was run. No model code, experiment code, configuration,
result artifact, publication-source table, figure, or caption was changed.

### Stage 10A — Supplementary Methods

The final V2 supplement is
`ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md`. It is a submission-oriented
scientific artifact assembled from `ARTICLE_V1_MODEL_METHODS.md`, the five
standard configs and manifests, the manuscript evidence freeze, analytic and
inferential audits, experiment interpretation notes, generator-source
provenance audit/index, publication-source records, and V2 figure provenance.
It does not overwrite Article V1 supplementary planning material.

The final structure is:

1. S1 Common learner and simulation conventions;
2. S2 E01 — feedback-history experiment;
3. S3 E02 — graded action representation;
4. S4 E03 — persistent-state environment and dynamic oracle;
5. S5 E04 — contextual search architectures;
6. S6 E05 — learned and environmental boundary estimation;
7. S7 Randomization, seed hierarchy, and inferential units;
8. S8 Secondary estimands and sensitivity analyses;
9. S9 Evidence provenance and reproduction; and
10. S10 Supplementary figure and table inventory.

The supplement fixes the complete headline technical route: common learner
parameters and stable softmax; E01's exact $43/60$ boundary and
sampling–pseudo-regret identity; E02's five independent arms and affine
endpoint objective; E03's reward-before-transition kernel, Bellman operator,
convergence/tie tolerances, 21-by-17 grid, adequacy rule, four-of-five
stability, and seven inconclusive cells; E04's four representations,
zero-based indexing, canonicalization, and deterministic first-index
`argmax`; and E05's exact $8/17$ environmental crossover, multi-action modal
response, equal-weight non-increasing PAVA, strict in-range inversion,
complete-master-curve bootstrap, and hierarchical left censoring.

`ARTICLE_V2_LID_SUPPLEMENT_MAIN_TEXT_CONSISTENCY.md` maps every main Results
claim and method to its supplement definition and controlling authority.
All five result subsections return `CONSISTENT`; no
`BLOCKED_BY_SUPPLEMENT_AUTHORITY` condition remains.

Secondary routing preserves E01 information-channel effects, E02 adverse
endpoint/modal results, E03 sentinels and learner/dynamic sensitivity, E04
identity/good-count/architecture/tie diagnostics, and E05 master-curve,
PAVA/bootstrap, endpoint, and strict-mode diagnostics as secondary. The
cross-estimand former Figure 6 remains
`SUPPLEMENTARY_CANDIDATE_PENDING_AUTHORITY`.

### Stage 10B — citation, terminology, construct, and novelty verification

The audit artifact is
`ARTICLE_V2_LID_STAGE10_CITATION_NOVELTY_AUDIT.md`. It records the existing
repository literature corpus, three locally extracted source packets, targeted
publisher/DOI/primary-source checks, the current L&ID reference authority, a
sentence-level citation classification, terminology and neighbouring-construct
decisions, candidate empirical measures, technical-citation decisions, a
novelty matrix, the main-text change gate, and the Stage 10.5 queue.

The current official *Learning and Individual Differences* Guide for Authors
was inspected on 2026-08-20. It requires APA Seventh Edition citation style,
alphabetical/chronological reference ordering, complete bidirectional
text/reference correspondence, correct bibliographic metadata, and DOI links
where available.

Citation-support outcome:

- every retained giftedness/social-coping claim is directly supported or
  already uses the narrower wording its source warrants;
- no `CITATION_MISMATCH`, unresolved `VERIFICATION_REQUIRED`, or
  `BLOCKED_BY_CITATION_SUPPORT` item remains;
- equifinality was identified as established adjacent terminology and required
  one `NECESSARY_POSITIONING` sentence in Introduction 1.2;
- dynamic disclosure feedback was identified as established prior art and
  required one `NECESSARY_POSITIONING` sentence in Discussion 4.4; and
- no result, estimator, equation, figure, or interpretation ceiling changed.

The main reference list moved from 17 entries to 13. Added:

- Chaudoir and Fisher (2010), DOI 10.1037/a0018193; and
- Cicchetti and Rogosch (1996), DOI 10.1017/S0954579400007318.

Removed as uncited:

- Bird (2004);
- Cross, Coleman, and Terhaar-Yonkers (2014);
- Hornstra et al. (2023);
- Kerr and Huffman (2018);
- Phillipson (2010); and
- Spears (2025).

The remaining 11 inherited entries were normalized to current APA-like L&ID
format and completed with DOI URLs. Every main-text citation now maps to one
valid main reference and every main reference is cited. The supplement has one
separate, legitimately cited technical reference: Best and Chakravarti (1990),
DOI 10.1007/BF01580873.

Phillipson (2010) was resolved as Sivaneswary Phillipson's sole-authored
“Modeling parental role in academic achievement: Comparing high-ability to
low- and average-ability students,” *Talent Development & Excellence, 2*(1),
83–103; no DOI was found in the authoritative institutional record. It was
removed because no surviving manuscript or supplement claim uses it.

### Construct and prior-art decisions

- **Terminology:** `ability concealment` remains a defensible umbrella;
  gifted literature more commonly uses social coping, stigma/information
  management, denial, conformity, and hiding giftedness. Model `masking`
  remains narrowly defined and is not treated as clinical or autistic
  camouflaging. Decision: `NO_CHANGE`.
- **Underidentification:** equifinality is established as a general
  developmental principle. V2's contribution is the gifted-concealment
  application and explicit five-part computational decomposition, not the
  general principle itself.
- **Environmental legibility:** `PARTIAL_OVERLAP` with affordances,
  psychological safety, climate/support, person–environment fit, belonging,
  and physical-environment legibility. No close equivalent jointly covers
  existence, awareness, predicted receptivity, access cost, and identification
  accuracy. Existing model-derived/open-operationalization wording is retained.
- **Graded disclosure:** disclosure depth is established, and generic
  action-representation dependence is not novel. The paired
  continued-nonzero/full-endpoint trade-off under independent ordered arms is
  application-specific. Decision: `NO_CHANGE`.
- **Persistent state:** disclosure feedback and postdisclosure consequences are
  established. E03 contributes the specific ability-concealment state model
  and finite-learner/full-information decomposition. Decision:
  `NECESSARY_POSITIONING`.
- **Context discovery:** niche selection, fit, and contextual peer acceptance
  are established adjacent ideas. Finite discovery of an unknown receptive
  option under four explicit representations remains the model-specific
  contribution. Candidate citations were `OPTIONAL_ENRICHMENT` and were not
  inserted.

Candidate future measures were recorded for gifted social coping/visibility,
event-coded behaviour, rejection expectations, feedback histories,
sociometric peer acceptance, school belonging, school/classroom climate,
teacher/classmate support, and a new discoverability/legibility measure.
No validated direct environmental-legibility measure was found.

PAVA decision: `CITE_IN_SUPPLEMENT`, using Best and Chakravarti (1990).
Value-iteration decision: `NO_CITATION_NEEDED`, because the supplement now
specifies the Bellman operator, initialization, convergence and tie
tolerances, iteration cap, reward basis, and independent policy-enumeration
check.

The novelty audit found no `BLOCKED_BY_NOVELTY_CONFLICT` or
`MAJOR_STAGE10_SCHOLARLY_CONFLICT`. The article's defensible novelty is
compositional: it combines established learning and developmental principles
into a mechanism-sensitive computational account of gifted ability
concealment.

### Main-text footprint and Stage 10.5 queue

The title, Abstract, Methods, Results, Limitations, Conclusion, Educational
Relevance, figures, and captions were unchanged. The only body changes were
the two necessary-positioning paragraphs in Introduction 1.2 and Discussion
4.4. The Stage 9 primary-text baseline was 6,375 words; the two inserted
paragraphs add 72 whitespace-delimited words, giving 6,447. Abstract remains
221 words and Educational Relevance remains 709 words. Total excluding
references and figure captions is 7,377 words.

The active manuscript SHA-256 changed only for those two paragraphs and the
reference repair, from
`7ccbd6a5550de3f8e4119fc79911e4db0851230c981c97a587fef33e8874eae3`
to
`800de4724da7868aac3935cbfe9f6460dc491e260a0ad75ae277ece0fd04e469`.

Route to
`ARTICLE_V2_LID_STAGE10_5_POST_CITATION_RECONCILIATION`:

1. reconcile the two positioning sentences against the full manuscript;
2. confirm final main/supplement reference routing;
3. decide the optional title precision issue (`Does Not Reveal` versus `does
   not uniquely identify`) without automatic change;
4. remove the duplicated “A practical target...” sentence in Educational
   Relevance as narrow editorial cleanup;
5. retain environmental legibility's `PARTIAL_OVERLAP` and model-derived
   status; and
6. leave the measures inventory in the audit unless the authors explicitly
   authorize an empirical-design expansion.

This historical Stage 10 queue is fully resolved by the Stage 10.5 record
above; it is retained here to preserve the decision sequence.

### Provenance and validation

Read-only frozen-evidence verification passed:

- 33/33 protected E01–E05 outputs match their manifests;
- 18/18 evidence-matrix-referenced files match;
- all eight V2 Figure 1–4 PDF/PNG hashes retain the Stage 7 values;
- standalone figure captions remain
  `aec20cfeede5934d0825907405e11b322eeb4b3130e2c03dfc21613fad5845f9`;
  and
- Article V1 remains byte-identical at
  `cd27687bdb5f3144172822ba2ff996f59efcdbf5398a905564a8177a345cdae9`.

Artifact identity is `ARTIFACT_VERIFIED` for all protected E01–E05 outputs.
E04/E05 historical source bundles remain fingerprint-exact. E01–E03 remain
`HISTORICAL_SOURCE_STATE_UNRECOVERED`; the supplement accurately states that
their claims are governed by frozen result artifacts, hashes, configs, and
verification records rather than a present-code bit-identical reproduction
claim.

`git diff --check` passed before the governance update and is rerun at final
validation. The stale-claim scan found only explicit negations of temporal
“give up” and binary-softmax interpretations; no substantive stale claim
reappeared. No experiment reran, no figure regenerated, and no implementation
file changed.

Bounded gaps are limited to the targeted rather than systematic nature of the
prior-art search, the absence of a validated direct legibility measure, the
final archival repository/supplement links, and the Stage 10.5 reconciliation
items above. None blocks the next stage.

## Identity and provenance

Article V2 is a journal-specific redesign derived from the frozen Article V1
E01–E05 evidence and manuscript corpus. V2 Stage 1 changes article framing,
architecture, terminology routing, and evidence routing, but introduces no new
experimental evidence. Article V1 remains intact as the source manuscript and
evidence lineage.

`ARTICLE VERSION != EVIDENCE VERSION.` Moving from Article V1 to Article V2
does not create a new experiment, result hash, evidence freeze, artifact
namespace, or scientific-authority hierarchy. V2 consumes the frozen V1
E01–E05 evidence base, V1 interpretation notes, V1 Methods/source material,
and V1 result artifacts directly; it must not overwrite the V1 manuscript.

## Authority routing

The V2 Stage 1 blueprint is
`ARTICLE_V2_LID_STAGE1_REFRAME_MAP.md`. Scientific facts remain governed by the
frozen V1 evidence matrix and artifacts, V1 manuscript evidence freeze,
analytic/evidence/inferential/literature/consistency audits, claim ledger, and
per-experiment interpretation notes under their existing precedence rules.
Article V2 may reorganize their presentation but may not strengthen, rerun,
rename, duplicate, or replace them.

## Manuscript-shell migration record

The integrated V2 shell was created on 2026-08-20 from bounded, explicitly
ranked sources:

- the current named V1 corpus,
  `Sion & Moussaffi-Running Second 18.Aug.2026 1949.md`, supplied outside the
  repository, was selected as the chronological prose source after both it and
  the committed `ARTICLE_V1_MANUSCRIPT_DRAFT.md` were inspected;
- the latest supplied `chapter fixes.md` supplied the complete replacement
  Results chapter and the consolidated role-based educational-relevance
  material;
- frozen E01–E05 artifacts, the manuscript evidence freeze, scientific audits,
  and experiment interpretation authorities overrode both prose sources where
  they conflicted;
- `ARTICLE_V1_MANUSCRIPT_DRAFT_V2.md` was inspected as uncommitted derivative
  manuscript work but was not promoted to evidence authority.

The Article V1 manuscript remains unchanged. V2 Results have been migrated
from the current V2 source with the frozen E01 final-window contrast, exact E05
boundary quantities, and E03 tested-grid semantics restored; the E04 outcome
was preserved pending the later estimator-gloss correction. The Introduction,
Methods, Discussion, Limitations, and
Conclusion are source-migrated rather than final. The autobiographical
Introduction paragraph was excluded from the evidentiary Introduction while
its source history and Acknowledgements context were preserved.

Figures were inventoried only. No figure file, generator, publication-source
table, frozen evidence artifact, model code, configuration, or result artifact
was edited by this stage. No experiment was rerun and no figure was
regenerated.

## Stage 2 Introduction rewrite record

The L&ID-oriented Introduction rewrite was completed on 2026-08-20.

- Final Introduction length: 1,234 words.
- Inherited Stage 1 Introduction length: 1,282 words.
- The 48-word reduction was achieved while adding the required six-subsection
  architecture and explicit E01–E05 questions; inherited anecdotal,
  cascade-first, and repeated-caveat material was removed.
- The new organizing problem is observational underidentification: current
  social conditions, learned expectations, and observed behaviour are
  explicitly distinguished.
- Stable person differences are separated from history-induced behavioural
  heterogeneity, action-representation differences, persistent-state
  differences, and contextual discoverability.
- Environmental/objective, learned, and dynamic value are separated, with
  `objective` retained only in its model-relative oracle sense.
- Availability is separated from discoverability, and learned boundaries are
  separated from objective boundaries without a temporal interpretation.
- E01–E05 are introduced as research questions rather than as five equivalent
  psychological mechanisms or a model-cascade contribution.

No bibliography entry was added or removed. The existing Cross et al. (2019)
citation was brought into the Introduction from the reference corpus.
Introductory citations to Bird (2004), Spears
(2025), and Kerr and Huffman (2018) were removed with the retired title
anecdote and unsupported broad construct mapping; their reference-list entries
remain pending the later citation audit. Existing Coleman, Cross, Swiatek,
Klimecka, Lavrijsen and Verschueren, Tourreix et al., March, Denrell, and Le
Mens and Denrell sources were retained or reorganized.

Bounded literature gaps remain unchanged: masking terminology,
graded-disclosure-specific prior art, persistent-state disclosure/reputation
prior art, and scarce-receptive-context discovery prior art require later
targeted verification. They are novelty/terminology gaps, not missing support
for the present Introduction.

The active Results and every manuscript chapter from Methods onward remained
byte-identical across this rewrite (`sha256` of the extracted Section 2-onward
content: `8fb9d53497c136a8abc6b72f4c53b026c2ca687e35b567527fa52d70a8ad041d`).
The manuscript provenance/front matter before the Introduction also remained
byte-identical. No figure, supplementary file, source file, configuration,
experiment artifact, evidence record, or Article V1 manuscript file was
changed. No experiment was rerun and no figure was regenerated.

## Stage 3 Methods repair, verification, and compression record

The L&ID-oriented Methods repair was completed on 2026-08-20 after the
maintained model implementations, frozen E01–E05 configurations and evidence,
analytic and inferential audits, interpretation notes, and Supplementary
Methods plan were inspected under the established authority hierarchy.

- Inherited Stage 2 Methods length: 1,243 words.
- Final Methods length: 1,416 words (the same token-counting rule used for the
  1,243-word inherited baseline).
- Final architecture: common learner and evidential scope; E01 feedback
  history; E02 action representation; E03 persistent state and dynamic value;
  E04 context representation; E05 learned and environmental boundaries; and
  simulation design, inference, and reproducibility.
- No stochastic experiment was rerun. No figure was generated, regenerated,
  or edited. No code, configuration, frozen artifact, manifest, or Article V1
  file was changed.

### Equation and quantity verification

| Equation / quantity | Manuscript value | Source authority | Verified |
|---|---|---|---|
| Stateless selected-action update | $Q_{t+1}(x)=Q_t(x)+\alpha[v_\lambda(R_t)-Q_t(x)]$ | `core.py`; `ARTICLE_V1_MODEL_METHODS.md` | YES |
| Reward transform | $R$ for $R\geq0$; $\lambda R$ for $R<0$ | `core.py`; analytic and consistency audits | YES |
| M0 masking reward | $b-c$ | `models/m0.py`; analytic authority | YES |
| M0 authenticity expectation | $p(b+a)+(1-p)(a-r)$ | `models/m0.py`; analytic authority | YES |
| M0 objective boundary | $1-(a+c)/(b+r)=43/60$ at reference values | `ARTICLE_V1_ANALYTIC_RESULTS.md`; direct arithmetic | YES |
| M1 affine disclosure reward | $b-c+d[a+c-(1-p)(b+r)]$ | `models/m1.py`; analytic authority | YES |
| M2 Q-learning update | selected $Q(s,x)$ with $\gamma\max_{x'}Q(s',x')$ | `models/m2.py`; model Methods authority | YES |
| M2 Neutral dynamic advantage | $\Delta_0(p)+\gamma[pV_A+(1-p)V_S-V_N]$ | `ARTICLE_V1_ANALYTIC_RESULTS.md` | YES |
| E03 discount factor | $\gamma=.9$ | frozen E03 standard configuration | YES |
| M3 reward classes | $R_M=b-c$; $R_G=p_{good}(b+a-b_f)+(1-p_{good})(a-r)$; corresponding $R_B$ | `models/m3.py`; analytic authority | YES |
| E05 masking reward | $.75$ | frozen payoffs; direct arithmetic | YES |
| E05 good-authentic reward | $1.15-.85b_f$ | frozen E05 configuration; direct arithmetic | YES |
| E05 environmental boundary | $.40/.85=8/17=.470588\ldots$ | analytic authority; direct arithmetic | YES |

Direct arithmetic also confirmed the M1 endpoints at $p=.85$: $d=0$ gives
$.75$ and $d=1$ gives $1.15$. Every headline equation and parameter passed;
there is no unresolved equation blocker. The provisional prose-only M1 and M2
descriptions were replaced with the exact affine reward and model-specific
dynamic-value equations. M3 reward classes and the E05 advantage equation were
restored explicitly, and the E01 pseudo-regret relation was identified as an
exact action-count translation rather than an independent outcome.

### Estimator and classifier verification

- E01 later sampling covers steps 1 through $T-1$; final-window masking is a
  secondary persistence check; forced exposure and counterfactual feedback are
  information-channel manipulations.
- E02 uses five independently learned disclosure arms with no neighbouring-arm
  generalization; non-zero disclosure, final-window $d=1$ rate, and the unique
  modal objective endpoint remain distinct estimands.
- E03 uses aggregate final-window Neutral action counts, not learner $Q$
  ordering or individual classification. Neutral adequacy requires at least
  160 visits from at least 32 learners; inadequacy or a count tie is
  inconclusive. Stability requires the same non-inconclusive class in at least
  four of five masters.
- E04 and E05 use deterministic first-index `argmax` resolution when final-
  window action counts tie. Their primary metrics permit non-unique modes and
  are not unique-mode, convergence, or binary-choice-probability estimands.
- E05 applies an equal-master, equal-point-weight non-increasing PAVA fit and
  resamples five complete master curves 10,000 times. Its strict in-range rule,
  plateau midpoint, interpolation, and below-range left censoring were retained.

### Main-text and Supplementary Methods routing

| Material | Main text | Supplementary Methods / repository record |
|---|---:|---:|
| Common learner and headline parameters | full operative definition | extended configuration tables |
| Core reward and update equations | full operative equations | derivations and invariant checks |
| M2 state/reward/transition concept | concise complete ordering | full transition kernel and value-iteration implementation |
| E03 oracle and classifier | definition and adequacy thresholds | implementation tolerances, diagnostics, and full grids |
| E04 architectures and primary tie rule | concise definitions | pseudocode, ablation matrices, and strict-mode diagnostics |
| E05 objective equation and crossing estimator | operative summary | full grid, PAVA inversion, bootstrap-validity details |
| Seed and random-stream construction | inferential unit only | complete seed hierarchy and stream construction |
| Sensitivity conditions and secondary estimands | only result-critical controls | full parameter and estimand tables |
| Provenance, hashes, and reproduction commands | explicit route and limitation pointer | detailed provenance/validation record and commands |

Detailed generator provenance was compressed out of main Methods without being
hidden: Supplementary Methods and Data/Code Availability are the primary route,
and the existing Limitations disclosure remains unchanged. The existing V1
Supplementary Methods plan was used as authority and was not modified; a final
journal supplement still needs to be assembled from that plan.

Unresolved bounded tasks are final supplement assembly and the later citation
audit for whether value iteration or PAVA needs a technical citation under
journal convention. At the close of Stage 3, the protected Stage 1/2 Results
§3.4 gloss still conflicted with the maintained deterministic first-index
`argmax` estimator. Stage 9 subsequently corrected that prose-only mismatch;
the frozen estimator and numbers were never changed. No new citation or
literature claim was introduced at Stage 3.

Section 1 remained byte-identical (`sha256`
`f8b2b23cc8a059467e61db8bbd1ee342dc49bdfb47d6a1ec3a2b666e12f0a00b`).
Section 3 onward remained byte-identical (`sha256`
`271d2853cc1ee933e51893ab8a158aa194009dbcbc0c70ba4f74bbf5effa9eb8`).

## Standing Editorial Governance — Claim Calibration and Disclaimer Discipline

Article V2 states scientifically bounded claims directly. State scope once;
state results directly; retain a local qualification only when removing it
would materially change the scientific meaning or invite a known material
misinterpretation. General modelling and human-generalization limitations are
introduced concisely in the modelling framework, centralized in Limitations,
and stated once in Educational Relevance when implications are introduced.
They are not to be appended reflexively to individual findings.

### Qualification classes

| Class | Rule | Required examples |
|---|---|---|
| A — result-defining | Keep beside the result. | E01 later sampling with no detected persistent final-window masking; E02 independent-arm condition; E03 tested-grid rather than prevalence reading; E04 representation-dependent scarce-receptivity result rather than a generic K law; E05 comparison-cost rather than temporal ordering and unresolved displacement mechanism. |
| B — statistic/method-defining | State once in Methods or at the statistic. | E03 full-information rather than information-matched oracle; E04 deterministic first-index `argmax`; E05 eight-action modal-arm outcome rather than binary softmax probability and hierarchical left censoring. |
| C — general model limitation | Centralize; do not repeat after each finding. | Non-calibrated parameters, non-calendar model steps, simulation-to-human generalization, intervention validity, model-relative objective value, and prevalence limits. |

Before adding a caution outside Limitations, apply the local qualification test:

> If this sentence were removed, would a technically competent reader be
> likely to misunderstand the actual experimental claim?

If yes, retain or compress it as Class A or B. If no, delete it, move it to
Limitations, or replace it with a calibrated verb. Permitted inferential verbs
include *shows*, *demonstrates* (for a directly established model result),
*supports*, *suggests*, *is consistent with*, *implies within the model*,
*provides a mechanism by which*, *motivates the hypothesis that*,
*distinguishes*, and *identifies*. The manuscript must not repeatedly apologize
for using a computational model: once the scope is established, Results and
Discussion should reason confidently within it.

### Chapter distribution and protected guardrails

Introduction may contain one concise modelling-scope statement and one
model-relative definition of objective. Methods define equations, estimands,
oracle, parameters, and inference without apologetic prose. Results retain only
result- or statistic-defining constraints. Discussion uses calibrated but
assertive interpretation. Educational Relevance may state once that implications
are model-derived hypotheses and intervention targets, not validated protocols;
role-specific subsections should then state implications directly. Limitations
is the primary home for construct validity, calibration, learner-family,
oracle, temporal, intervention-validity, tested-grid, and provenance limits.
Conclusion uses at most one brief scope statement.

This policy does not relax scientific authority. E01 must not be described as
persistent final masking after one rejection. E02 remains conditional on
independent action values. E03 `243/357` remains tested-grid coverage rather
than learner or human prevalence, and its oracle remains non-information-
matched. E04 remains a representation/scarcity/discoverability conjunction,
not a generic more-contexts theorem. E05 remains non-temporal, multi-action,
and mechanism-unresolved; the G2/binary-softmax temperature exclusion remains
prohibited. E06/M4 remain outside V2 numerical Results and confirmatory
Discussion claims.

### Stage 4 handoff and later consolidation

Stage 4 must synthesize and interpret findings rather than repeat Results or
surround each inference with generic caveats. It may use statements such as
“This result suggests…”, “Together, E01 and E02 support…”, “E04 implies…”,
and “These findings motivate…” when the remainder of the sentence stays within
the evidence authority. General simulation-to-human limitations belong in the
existing Limitations section unless a local Class A or B qualification is
needed to prevent a specific known misinterpretation.

After the substantive Discussion, Educational Relevance, Limitations, and
Conclusion rewrites, and before the final independent scientific audit, run
`MANUSCRIPT_WIDE_CLAIM_CALIBRATION_AND_DISCLAIMER_CONSOLIDATION`. That pass must
classify every hit from the standing vocabulary (`does not`, `do not`, `not a`,
`not an`, `cannot`, `can't`, `should not`, `not necessarily`, `doesn't`, `not
establish`, `not imply`, `not prove`, `not an estimate`, `not a claim`, `not
calibrated`, `not literal`, `not prevalence`, `only a model`) as
`KEEP_RESULT_DEFINING`, `KEEP_STATISTIC_DEFINING`,
`KEEP_SINGLE_SCOPE_STATEMENT`, `MOVE_TO_LIMITATIONS`, `DELETE_REDUNDANT`, or
`REWRITE_WITH_CALIBRATED_VERB`. It must not delete negations mechanically and
must re-check every E01–E05 guardrail after consolidation.

### Stage 3.5 diagnostic baseline

The following raw phrase counts are diagnostic only; they include overlaps in
the audit vocabulary and, where present, internal comments. They are not a
quality score.

| Section | Disclaimer-like hits |
|---|---:|
| Introduction | 19 |
| Methods | 10 |
| Results | 11 |
| Discussion | 14 |
| Educational Relevance | 14 |
| Limitations | 8 |
| Conclusion | 2 |

Manual sampling confirms that several Results hits are necessary Class A/B
qualifications. The inherited Discussion is overqualified for its intended
interpretive role, though the role-based Educational Relevance material has an
equal raw density and will also need consolidation. This is an editorial
finding, not authorization to remove required E01–E05 boundaries now.

Stage 3.5 made no manuscript-text patch. At close, the protected Stage 2
Introduction and Stage 1/2 Results-plus-later-section hashes still matched the
Stage 3 record. The current Methods-only digest was captured as
`300e08f939961ce0c95757d46d35ba8706157b4b15bde45441af93804789a5ee` for
later reconciliation; it was not altered by this governance stage.

## Stage 4 Discussion rewrite record

The L&ID-oriented Discussion rewrite was completed on 2026-08-20 under the
active claim-calibration policy and frozen E01–E05 authority.

- Inherited Discussion length: 974 words.
- Final Discussion length: 1,626 words.
- Disclaimer-vocabulary hits: 14 before; 3 after. The three retained hits are
  Class A result-defining qualifications for E03 adaptation versus learned
  error and E05 causal non-identification.
- Final architecture: masking as an underidentified behavioural phenotype;
  history-induced versus stable person differences; action representation;
  persistent social consequences and dynamic adaptation; availability versus
  discoverability; learned versus environmental boundaries; and an empirical
  measurement programme.

The new synthesis separates current social environment, learned expectation,
and observed behaviour. It shows how similar concealment can arise through
genuinely adaptive response, restricted sampling, independent-action evidence
fragmentation, persistent-state learning, undiscovered receptivity, or a
displaced learned boundary. Conversely, the same opportunity structure can
produce heterogeneous behaviour through different histories without requiring
different stable traits.

The substantive-statement audit classified the chapter as follows:

| Statement class | Discussion content | Adjudication |
|---|---|---|
| Direct E01–E05 synthesis | underidentification; history-restricted sampling; representation trade-off; dynamic adaptation/error; discoverability; boundary displacement | Retained |
| Model-supported interpretation | behavioural heterogeneity without changed stable traits; environmental legibility; separate measurement of environment, expectation, history, and behaviour | Retained with calibrated verbs |
| Literature-supported interpretation | heterogeneous and context-sensitive gifted social coping/ability visibility | Retained with existing citations |
| Empirical prediction/hypothesis | legibility and sequential measurement can distinguish mechanisms | Retained as an empirical programme, not a reported human effect |
| Intervention implication | information, expectations, environment, persistence, and legibility as conceptual targets | Deferred to Stage 5; no role-specific guidance added |
| Unsupported | none | Removed or not introduced |

Important inherited material retained includes hot-stove/endogenous-sampling
logic and its existing citations; the complementary rather than confirmatory
E01/E02 relationship; the distinction between static and dynamic value; the
possibility that masking is dynamically adaptive in some M2 configurations;
context-sensitive gifted social-coping citations; the availability-versus-
discoverability distinction; and the need for sequential, context-linked
measurement. The rewrite removed experiment-by-experiment recap, repeated
effect sizes and classifier counts, the harsh-sentinel detour, duplicated
simulation-to-human disclaimers, intervention-exclusion lists, and repeated
restatements of material already carried by Results or Limitations.

The following local constraints remain explicit: E01 changed subsequent
sampling but did not yield a detectable persistent final-window masking
difference; E02 is conditional on independent arms; E03 distinguishes learned
error from dynamically adaptive masking relative to a full-information oracle;
E04 depends on the tested representation and scarcity structure; and E05 is a
comparison-cost rather than temporal displacement whose causal decomposition
remains unresolved. The Discussion contains no E06/M4 evidence and no
G2/binary-softmax inference.

Generic calibration, human-generalization, intervention-validity, oracle,
prevalence, learner-family, and provenance caveats remain centralized in the
existing Limitations. `ROUTE_TO_STAGE6_LIMITATIONS`: make the E04 context-choice
abstraction explicit as repeated modelled choice rather than literal observed
movement/search, and evaluate whether the model-derived *environmental
legibility* construct needs a construct-validity qualification. No Section 5
prose was changed at this stage.

Citation completion remains bounded to later work. The existing hot-stove and
gifted social-coping/context citations were reused without adding a source.
Stage 10 should verify whether *environmental legibility* overlaps an
established construct and identify validated measures, if available, for
ability visibility, expected social response, feedback history, and contextual
receptivity. Until then, environmental legibility remains explicitly a
model-suggested empirical construct rather than a literature-backed label.

Protected content remained byte-identical across the rewrite:

| Protected content | SHA-256 before and after |
|---|---|
| Section 1 | `f8b2b23cc8a059467e61db8bbd1ee342dc49bdfb47d6a1ec3a2b666e12f0a00b` |
| Section 2 | `300e08f939961ce0c95757d46d35ba8706157b4b15bde45441af93804789a5ee` |
| Section 3 | `75c17af5e9d76cbc150d62f9c60cbc3bff0fd7b89ad90cd90780e9231c0eba5e` |
| Section 5 onward | `333a2b68ffd530844235043800e1323d6d76d3b1ae8fbac2083a2362c5a83d62` |

No Abstract, Introduction, Methods, Results, Educational Relevance,
Limitations, Conclusion, reference, figure, configuration, code, or evidence
artifact was edited. No experiment was rerun and no figure was regenerated.

## Stage 5 Educational Relevance rewrite record

The educational-implications rewrite was completed on 2026-08-20 under the
active claim-calibration policy and the completed Discussion synthesis.

- Inherited Educational Relevance length: 662 words.
- Final Educational Relevance length: 709 words.
- Disclaimer-vocabulary hits: 15 before; 3 after. The opening sentence is the
  sole general intervention-validity statement. The remaining local wording
  preserves the E02 choice-architecture boundary and the E05 finding that
  withdrawal alone does not locate the environmental boundary.
- Final organization: start with mechanism rather than masking; assess
  expectations as well as behaviour; make receptive opportunities legible;
  treat choice architecture as part of the learning environment; and match the
  intervention target to the inferred mechanism.

The central educational principle is that concealment should not be used by
itself to infer either current social conditions or the appropriate response.
Assessment is organized around current conditions, learned expectations,
feedback history, observed behaviour, available receptive alternatives, and
their discoverability. The rewritten section recognizes both adaptive
concealment under current adverse conditions and learned concealment that no
longer fits current conditions; reducing masking is therefore not a universal
objective.

Role-specific implications were retained without separate repetitive essays.
Parents can compare current and earlier experiences when asking what a child
expects; teachers can examine classroom and peer consequences while making
opportunities visible; counsellors can use mismatches between predicted and
observed responses as diagnostic information. These are model-derived
assessment/intervention targets, not asserted educational or clinical protocols.

The recommendation audit classified the section as follows:

| Recommendation class | Content | Adjudication |
|---|---|---|
| `DIRECT_MODEL_IMPLICATION` | mechanism-matched assessment; separate current conditions, expectations, history, behaviour, availability, and discoverability | Retained |
| `MODEL_DERIVED_HYPOTHESIS` | corrective information, credible new evidence, and environmental legibility as possible targets | Retained with calibrated language |
| `LITERATURE_SUPPORTED_EDUCATIONAL_PRACTICE` | none newly asserted | None added |
| `UNSUPPORTED` | permanent-first-experience, persistence coaching, more-choice-is-harmful, universal disclosure, concentrated-group superiority, and counterfactual-feedback treatment claims | Removed or not introduced |

The existing Stage 6 route remains: make the E04 context-choice abstraction
explicit as repeated modelled choice rather than literal observed movement or
search, and evaluate the construct-validity qualification for *environmental
legibility*. Stage 10 citation completion should examine the same construct,
plus validated measures for learned social expectations, ability visibility,
contextual receptivity, and feedback history. No citation was added here.

Protected content remained byte-identical across the rewrite:

| Protected content | SHA-256 before and after |
|---|---|
| Section 1 | `f8b2b23cc8a059467e61db8bbd1ee342dc49bdfb47d6a1ec3a2b666e12f0a00b` |
| Section 2 | `300e08f939961ce0c95757d46d35ba8706157b4b15bde45441af93804789a5ee` |
| Section 3 | `75c17af5e9d76cbc150d62f9c60cbc3bff0fd7b89ad90cd90780e9231c0eba5e` |
| Section 4 | `e07bdc2c8846102cde3b3a2b6fa0c31fe3449888151f19fa26b11a4f7606b89b` |
| Limitations and Conclusion | `2dce210c67410b09ba1ebf53f2755aa90bea6739f06b5a7766e44976616b9120` |
| Figure inventory onward | `ee45e49538a93f2237a27304dc221a35707e4d976e1f04680c05c527f159257b` |

No Abstract, Introduction, Methods, Results, Discussion, Limitations,
Conclusion, reference, figure, configuration, code, or evidence artifact was
edited. No experiment was rerun and no figure was regenerated.

## Stage 6 Limitations and Conclusion rewrite record

The V2 Limitations and Conclusion rewrite was completed on 2026-08-20 under
the active claim-calibration policy and frozen E01–E05 authority.

- Limitations: 349 words inherited; 370 words final.
- Conclusion: 181 words inherited; 192 words final.
- Final Limitations architecture: stylized decision problem and construct
  validity; restricted learner family and representation; abstract social
  states, contexts, and environmental legibility; full-information oracle and
  model-relative objective; and external inference, time, intervention, and
  provenance scope.
- Disclaimer-vocabulary hits: 2 in Limitations (`not calibrated` and `not
  prevalence`); 0 in Conclusion. Both retained Limitations phrases state
  distinct, general scope boundaries economically.

The rewrite centralizes the manuscript's generic limitations without weakening
its formal contribution. It identifies model parameters as design variables,
learner-family and representation dependence as conditions of the result,
social states and contexts as abstractions, the E03 oracle as an intentional
full-information benchmark, grids as design spaces rather than population
distributions, and E05 as non-temporal. The single intervention-validity
statement retains educational implications as model-derived targets requiring
empirical testing.

The routed Stage 4/5 issues are resolved in main-text Limitations: E04 is
explicitly an abstract repeated context-and-behaviour choice, not observed
movement between institutional or peer settings; *environmental legibility* is
explicitly a model-derived descriptive label whose construct relation and
operationalization require future work. The provenance limitation is retained
in one sentence: exact historical generator states for E01–E03 are not fully
recoverable, so frozen artifacts, hashes, and verification records govern the
results rather than a claimed current-code reconstruction.

The Conclusion now foregrounds underidentification: concealment is not
self-interpreting, learned behaviour and environmental opportunity can diverge,
and empirical studies should measure conditions, expectations, feedback
history, behaviour, subsequent sampling, and contextual access separately. It
does not enumerate E01–E05, add an intervention proposal, or end with a
generic disclaimer.

### Primary-text word count

| Section | Words |
|---|---:|
| Introduction | 1,236 |
| Methods | 1,416 |
| Results | 1,568 |
| Discussion | 1,626 |
| Limitations | 370 |
| Conclusion | 192 |
| **Primary-text subtotal** | **6,408** |

Educational Relevance is separate at 709 words. The present primary-text
subtotal remains comfortably below an 8,000-word working ceiling; no earlier
chapter was changed for length at this stage.

Stage 10 routes remain explicit: investigate whether *environmental
legibility* overlaps an existing construct; identify measures for ability
visibility, learned social expectations, feedback history, contextual
receptivity, and discoverability; determine journal-format citation needs for
PAVA, value iteration, and related methods; and finalize historical
generator-state and Data/Code Availability disclosure.

Protected content remained byte-identical across the rewrite:

| Protected content | SHA-256 before and after |
|---|---|
| Section 1 | `f8b2b23cc8a059467e61db8bbd1ee342dc49bdfb47d6a1ec3a2b666e12f0a00b` |
| Section 2 | `300e08f939961ce0c95757d46d35ba8706157b4b15bde45441af93804789a5ee` |
| Section 3 | `75c17af5e9d76cbc150d62f9c60cbc3bff0fd7b89ad90cd90780e9231c0eba5e` |
| Section 4 | `e07bdc2c8846102cde3b3a2b6fa0c31fe3449888151f19fa26b11a4f7606b89b` |
| Educational Relevance | `30b0a05df3808b1e9c04fce6489c1cf50497514d5d27bf6c3b7bf48a451f6320` |
| Figure inventory onward | `ee45e49538a93f2237a27304dc221a35707e4d976e1f04680c05c527f159257b` |

No Abstract, Introduction, Methods, Results, Discussion, Educational
Relevance, reference, figure, configuration, code, or evidence artifact was
edited. No experiment was rerun and no figure was regenerated.

## Stage 8 Abstract, Title, and Keywords record

Stage 8 was completed on 2026-08-20 from the completed V2 body, final Figure
1–4 captions, and frozen E01–E05 authority. It changed only the manuscript
title, abstract, and keywords, plus this governance record. No Results prose,
figure caption, numerical result, reference, source figure, frozen artifact,
or Article V1 file was changed; no experiment was rerun and no figure was
regenerated.

- **Old title:** `Running Second: A Computational Model Cascade for Gifted Peer Dynamics`.
- **RECOMMENDED_TITLE / final title:** `Ability Concealment Does Not Reveal the Environment: Learning and Social Opportunity in Gifted Learners`.
- **Title decision:** the title leads with the V2 inference problem, ability
  concealment, learning, social opportunity, and gifted learners. It does not
  suggest prevalence research, clinical diagnosis, an intervention trial, or
  calibrated human parameters.
- **Running Second decision:** `RETIRE`. The phrase depended on the removed
  autobiographical/cinematic framing, has low scholarly discoverability, and
  obscures the V2 contribution.
- **Underidentified decision:** retain `underidentify` in the abstract and
  `underidentified behavioural phenotype` in the body, but not in the title.
  The final title communicates the same inference problem in more accessible
  language.

Internal title shortlist and top-three ranking:

| Rank | Candidate | Main advantage | Principal drawback | Decision |
|---:|---|---|---|---|
| 1 | **Ability Concealment Does Not Reveal the Environment: Learning and Social Opportunity in Gifted Learners** | Makes the inference problem, population, construct, learning, and environment visible without using specialist jargon | At 14 words, it is longer than a compact keyword title | **Selected** |
| 2 | Ability Concealment, Learned Expectations, and Social Opportunity in Gifted Learners | Concise and highly searchable | Does not state as clearly why those quantities must be separated | Alternative |
| 3 | When Masking Does Not Reveal the Environment: Learning and Ability Concealment in Gifted Learners | Expresses the central contrast memorably | `masking` is more vulnerable to clinical ambiguity than the preferred construct term | Alternative |

The final unstructured abstract is **221 words**. It identifies the study as
controlled reinforcement-learning work in gifted learners, states the
underidentification problem, covers feedback history, independent action
representation, persistent social state, contextual discoverability, and
learned/environmental boundary separation, and ends with the measurement
implication rather than a generic limitation. Its only numerical synthesis is
the E05 comparison-cost crossing: learned 0.313 versus stipulated environmental
0.471, rounded directly from frozen values 0.312852 and 0.470588235. The final
keywords are: `giftedness`; `ability concealment`; `masking`; `reinforcement
learning`; `learned expectations`; `social feedback`; `individual differences`.

Abstract claim audit:

| Sentence/function | Classification | Frozen support / adjudication |
|---|---|---|
| Gifted learners may reduce ability visibility in social settings | `BACKGROUND` | Existing Introduction framing; no prevalence claim |
| Behaviour alone can underidentify the learner–environment relationship | `SYNTHESIS` | Figure 1 and E01–E05 cross-model synthesis |
| Controlled reinforcement-learning experiments separate five structures | `METHOD` | Methods §§2.1–2.7 |
| Comparators use stipulated payoffs or a full-information dynamic benchmark | `METHOD` | Methods §§2.4 and 2.6 |
| Adverse initial outcome changed sampling, without detected persistent final masking | `FROZEN_RESULT` | E01 |
| Independent graded actions sustained non-zero disclosure but reduced endpoint use | `FROZEN_RESULT` | E02 |
| Persistent state produced learned–dynamic-oracle divergence in some tested conditions | `FROZEN_RESULT` | E03 |
| Available receptive context became less discoverable under particular representations | `FROZEN_RESULT` | E04 |
| Learned comparison-cost crossing 0.313 was below stipulated crossover 0.471 | `FROZEN_RESULT` | E05 |
| Concealment cannot uniquely diagnose current adaptation, expectation, or discoverability | `SYNTHESIS` | E01–E05 |
| Empirical studies should measure the named quantities separately | `EMPIRICAL_IMPLICATION` | Conclusion and Discussion §4.7 |

No abstract sentence is classified `UNSUPPORTED`. The disclaimer-density audit
found only the E01 result-defining phrase “without a detected persistent
final-window masking effect” and the synthesis phrase “cannot uniquely
identify”; both are necessary statements of the result and inference problem,
not generic defensive qualification. The stale front-matter search found no
substantive hit for the prohibited V1, E06/M4, G2, temporal, context-count, or
obsolete-numerical language.

The primary-text subtotal remains **6,408 words** under the established
manuscript word-count rule; Educational Relevance remains **709 words**.
With the 221-word abstract, the total excluding references and figure captions
is **7,338 words**. The title is 14 words.

Protected body after Stage 8 remains byte-identical to the Stage 7 baseline:

| Content | SHA-256 |
|---|---|
| Introduction | `f8b2b23cc8a059467e61db8bbd1ee342dc49bdfb47d6a1ec3a2b666e12f0a00b` |
| Methods | `300e08f939961ce0c95757d46d35ba8706157b4b15bde45441af93804789a5ee` |
| Results | `7c75214749dcbe269996ffa2b59103eab6c5318d47be2abd40c2396e44610251` |
| Discussion | `e07bdc2c8846102cde3b3a2b6fa0c31fe3449888151f19fa26b11a4f7606b89b` |
| Limitations | `3d0d750c54c28cd9f302987708f05bb8235b51d85aa4ccd5602c6543349c6c47` |
| Conclusion | `a512a8ece5bcd5369f80a5091e84f8f5972777a2e253b97b4167ee64c919b2c7` |
| Educational Relevance | `ee969126d2212bd38f44b9f3689ef430fca062d4c4cb3372b2303aa28baf8c0d` |
| Figure captions | `2354d29a504f6d214af09faeeab07c1e88440231b2244d2b876bc58f142e7a87` |

Article V1 remains byte-identical at
`cd27687bdb5f3144172822ba2ff996f59efcdbf5398a905564a8177a345cdae9`.

At the close of Stage 8, the remaining bounded work was the E04 Results
tie-semantics correction and manuscript-wide claim calibration. Stage 9 has
now completed that work. Stage 10 must complete supplement assembly and the
citation, terminology, construct, and novelty checks recorded below.
Journal-specific submission conversion remains Stage 12.

## Stage 9 claim calibration and consistency record

Stage 9 was completed on 2026-08-20 as a surgical manuscript-consistency pass.
Repository authority, frozen experiment records, maintained estimator code,
the E04 interpretation note, the V1 evidence matrix and inferential audit, and
the V2 figure provenance/consistency records were inspected before editing.
Narrative smoothness did not override any of those sources. No experiment was
rerun; no result, equation, parameter, estimator, table, figure, or reference
entry was changed.

### Mandatory E04 estimator correction

Results §3.4 previously described the primary E04 outcome as ties-permitted in
the sense that any maximum-count good-authentic arm qualified. That gloss
conflicted with the maintained estimator, frozen metric
`mean_settled_any_good_auth_argmax`, Methods §2.5, and Figure 4A. The Results
definition now states the actual rule: deterministic first-index `argmax` is
applied to each learner's final-window joint-action counts, the learner
qualifies only when that selected indexed arm is authentic in a good context,
and non-unique modes remain eligible because ties resolve to the first indexed
arm. This is not a unique-modal classifier. The correction changes no frozen
number and no generated figure.

### Five-experiment claim matrix

| Experiment | Manuscript claim retained | Required local boundary | Consistency decision |
|---|---|---|---|
| E01 | Initial rejection reduced subsequent authentic sampling | No detected persistent final-window masking increase; pseudo-regret is algebraically linked | `CONSISTENT` |
| E02 | Independent graded arms sustained non-zero disclosure while reducing full-authentic endpoint discovery | Arms learn independently; intermediate disclosure is not an interior static optimum | `CONSISTENT` |
| E03 | Finite learned Neutral behaviour disagreed with the full-information dynamic optimum in 243/357 tested cells | Tested-grid coverage, seven inconclusive cells, and a stronger full-information rather than information-matched comparator | `CONSISTENT` |
| E04 | Receptive opportunity can remain available while being difficult to discover under tested scarcity and representations | No generic context-count law; deterministic first-index `argmax`; architecture-specific magnitudes | `CONSISTENT_AFTER_PROSE_CORRECTION` |
| E05 | The flat eight-action learned response crossed 0.5 below the exact comparison-cost crossover | Parameter-axis ordering is non-temporal; hierarchical crossing is left-censored; mechanism is unresolved | `CONSISTENT` |

The manuscript uses `objective` only for value under the stipulated model or
full-information dynamic oracle. It distinguishes currently adaptive masking
from learned–objective divergence and does not apply `maladaptive` as a blanket
label. `Environmental legibility` remains a model-derived educational label
for whether receptive settings, people, or opportunities can be identified;
Limitations continues to require empirical construct development and
operationalization.

### Disclaimer consolidation

A literal diagnostic scan used the established disclaimer phrase set:
`does not`, `do not`, `not a`, `not an`, `cannot`, `can't`, `should not`,
`not necessarily`, `doesn't`, `not establish`, `not imply`, `not prove`,
`not an estimate`, `not a claim`, `not calibrated`, `not literal`,
`not prevalence`, and `only a model`. Counts are diagnostic substring hits and
may overlap; they are not a prose-quality score.

| Section | Before | After | Decision |
|---|---:|---:|---|
| Abstract | 1 | 1 | Retain inference-defining language |
| Introduction | 19 | 19 | Retain construct and research-question boundaries |
| Methods | 10 | 10 | Retain estimator and evidence definitions |
| Results | 12 | 9 | Remove three repeated generic human/prevalence caveats; retain result- and statistic-defining qualifications |
| Discussion | 3 | 3 | Retain synthesis boundaries |
| Educational Relevance | 3 | 3 | Retain the practical scope sentence and mechanism distinctions |
| Limitations | 2 | 2 | Retain centralized human-calibration and prevalence boundaries |
| Conclusion | 0 | 0 | No change |
| Figure captions | 0 | 0 | Replace the uncaptured generic treatment caveat with the positive classification `model information manipulations` |

The Stage 9 instruction quoted an 11-hit Results baseline, but the direct
pre-edit Stage 8 snapshot contained 12 hits under the established literal
phrase set; 12 is therefore the authority-preserving before count used here.
Meaningful hits were classified as follows:

- `KEEP_RESULT_DEFINING`: E01's non-detected final-mask effect; E02's
  independent-arm boundary; E03's learned–objective comparator; E04's
  representation/scarcity boundary; and E05's non-temporal, unresolved-cause
  boundary.
- `KEEP_STATISTIC_DEFINING`: E01's algebraically linked pseudo-regret; E03's
  tested-cell/action-count/inadequacy rules; E04's first-index tie rule; and
  E05's modal-arm, PAVA, and left-censoring definitions.
- `KEEP_SINGLE_SCOPE_STATEMENT`: the model-relative objective definition,
  centralized Limitations calibration, and the opening Educational Relevance
  scope sentence.
- `DELETE_REDUNDANT`: the three generic Results caveats about prevalence,
  human treatment effects, and developmental timescale.
- `REWRITE_WITH_CALIBRATED_VERB`: the inaccurate E04 ties gloss and Figure 2's
  generic treatment disclaimer.
- `MOVE_TO_LIMITATIONS`: none; the relevant generic caveats were already
  centralized there in Stage 6.

The additional connective scan found one `however` in Results before and
after and no `although` in any audited section. That `however` introduces the
two-sided E02 finding rather than a generic disclaimer. Generic model-to-human
calibration is now concentrated in Limitations and the bounded Educational
Relevance scope statement, while local qualifications remain next to the
statistics they define.

### Submission-facing cleanup and Stage 10 routing

Two internal HTML comments were removed from the manuscript: the V2 lineage /
E01–E05 production header and the Stage 1 citation-audit flag block. Their
authority is preserved here rather than exposed in submission-facing prose.
The citation block's unresolved items are routed intact to Stage 10:

1. verify the incomplete Phillipson (2010) bibliographic entry;
2. verify DOI completeness and consistency across journal articles;
3. apply final *Learning and Individual Differences*/Elsevier reference style
   after prose freeze;
4. recheck sentence-level support for giftedness and social-coping claims; and
5. audit literature specific to the underidentification/individual-differences
   reframe without adding speculative citations.

Stage 10 must also assemble the final Supplementary Methods from the existing
plan and decide, under journal convention, whether value iteration and PAVA
require technical citations. No unverified reference was added in Stage 9.

### Word counts, hashes, and preservation

- Primary text (Introduction through Conclusion, excluding Educational
  Relevance): **6,375 words**, down 33 words from the Stage 8 baseline of
  6,408.
- Abstract: **221 words**, unchanged.
- Educational Relevance: **709 words**, unchanged.
- Total excluding references and figure captions: **7,305 words**.
- Results SHA-256:
  `7d49b666b53cdadadaa57826941b81d55c0b6850e68870997b19c423daeb083a`.
- Embedded Figure captions SHA-256:
  `46f6c88d0f117be2a751ec252c4a77ef97cd2137641f396fdbde8ddac30ae09a`.
- Standalone `v2_figures/FIGURE_CAPTIONS.md` SHA-256:
  `aec20cfeede5934d0825907405e11b322eeb4b3130e2c03dfc21613fad5845f9`.
- Full active manuscript SHA-256:
  `7ccbd6a5550de3f8e4119fc79911e4db0851230c981c97a587fef33e8874eae3`.
- Article V1 remained byte-identical:
  `cd27687bdb5f3144172822ba2ff996f59efcdbf5398a905564a8177a345cdae9`.

Abstract, Introduction, Methods, Discussion, Limitations, Conclusion, and
Educational Relevance retained their Stage 8 section hashes. All eight final
Figure 1–4 PDF/PNG hashes retained the Stage 7 values. Direct frozen-evidence
verification passed for all **33/33** protected E01–E05 outputs and all
**18/18** evidence-matrix references. No generator was invoked and no figure
was regenerated.

## Stage 7 Figure Finalization record

Stage 7 was completed on 2026-08-20 as a deterministic presentation and
provenance task. The final V2 main-text package contains exactly four figures:

1. `v2_figures/figures/Figure_1_underidentification_architecture.pdf/.png`
2. `v2_figures/figures/Figure_2_history_and_action_representation.pdf/.png`
3. `v2_figures/figures/Figure_3_persistent_state_and_disagreement.pdf/.png`
4. `v2_figures/figures/Figure_4_discoverability_and_boundary_displacement.pdf/.png`

Figure 1 is a newly authored conceptual underidentification architecture and
E01–E05 mechanism map (`CONCEPTUAL_FIGURE_NO_NUMERICAL_EVIDENCE`). Figures 2–4
are deterministic assemblies from SHA-256-pinned publication-source tables;
their required visual spot checks are recorded in
`v2_figures/FIGURE_TEXT_CONSISTENCY_MATRIX.md`, and their input/output hashes,
generator path, command, and old-asset routing are recorded in
`v2_figures/FIGURE_PROVENANCE.md`. The generator,
`v2_figures/generate_v2_figures.py`, imports no experiment module or stochastic
entry point. No frozen artifact, result table, source evidence, maintained V1
generator, or Article V1 manuscript was changed, and no experiment was rerun.

The V2 manuscript now contains publication-ready captions for Figures 1–4 and
no longer contains the provisional Stage 1 figure inventory. The only Section
3 change is a non-substantive cross-reference correction: the E02 continued
disclosure result is plotted in Figure 2C, not Figure 2B. At the close of Stage
7, the known E04 Results tie-semantics wording mismatch remained in the Stage 9
consistency queue, while Figure 4 already used and labelled the maintained
deterministic first-index `argmax` estimator accurately. Stage 9 subsequently
resolved the prose mismatch.

Protected prose checks after Stage 7:

| Content | SHA-256 result |
|---|---|
| Introduction | `f8b2b23cc8a059467e61db8bbd1ee342dc49bdfb47d6a1ec3a2b666e12f0a00b` (unchanged) |
| Methods | `300e08f939961ce0c95757d46d35ba8706157b4b15bde45441af93804789a5ee` (unchanged) |
| Results | `7c75214749dcbe269996ffa2b59103eab6c5318d47be2abd40c2396e44610251`; normalization of only the permitted `Figure 2C` → `Figure 2B` reference restores `75c17af5e9d76cbc150d62f9c60cbc3bff0fd7b89ad90cd90780e9231c0eba5e` |
| Discussion | `e07bdc2c8846102cde3b3a2b6fa0c31fe3449888151f19fa26b11a4f7606b89b` (unchanged) |
| Limitations | `3d0d750c54c28cd9f302987708f05bb8235b51d85aa4ccd5602c6543349c6c47` (unchanged) |
| Conclusion | `a512a8ece5bcd5369f80a5091e84f8f5972777a2e253b97b4167ee64c919b2c7` (unchanged) |
| Educational Relevance | `ee969126d2212bd38f44b9f3689ef430fca062d4c4cb3372b2303aa28baf8c0d` (unchanged) |

Article V1 remains byte-identical at
`cd27687bdb5f3144172822ba2ff996f59efcdbf5398a905564a8177a345cdae9`.

Old assets were retained and explicitly routed: current E01/E02/E03/E04–E05
display files were merged conceptually into V2 Figures 2–4; the former cascade
diagram and recoverable deleted package are duplicate historical displays; and
the cross-estimand Figure 6 synthesis is supplementary/non-main pending a
separate authority decision. Supplementary routing retains seed diagnostics,
secondary outcomes, E03 stability/sentinel material, E04 sensitivities, and
E05 master-curve/PAVA/bootstrap diagnostics. No asset was deleted or reset.

Visual inspection of all PDF/PNG deliverables checked panel order, clipping,
axis language, legends, threshold positions, grayscale category distinctions,
uncertainty display, and stale V1 terminology. Figure 2 uses frozen
across-master Student-*t* intervals; Figure 4 distinguishes descriptive E04
master ranges from its inset intervals and preserves E05 complete-master-curve
bootstrap semantics. Figure 3 explicitly separates seven inconclusive cells
and describes `243/357` as tested parameter cells. Figure 4 treats its
horizontal axis as comparison cost, reports the exact $8/17$ objective
crossover, and calls the hierarchical result left-censored below the tested
range.

The bounded gaps recorded at Stage 7 were journal-specific final submission
dimensions and format conversion (Stage 12), citation/novelty completion
(Stage 10), the historical E01–E03 generator-state limitation already
disclosed in Limitations, and the then-pending E04 Results tie-semantics
correction. Stage 9 subsequently resolved the latter; the remaining items do
not block the completed four-figure V2 package.

## Stage 1 repository baseline

- Branch: `codex/frontiers-stage2-e06`
- Starting HEAD: `501fc5a10be081f7da3ad02a9055d1d2c8cc0422`
- Dirty paths inspected before manuscript editing: 44
- `PREEXISTING_MANUSCRIPT_WORK`: the untracked
  `ARTICLE_V1_MANUSCRIPT_DRAFT_V2.md` and existing hand-off document outputs
- `PREEXISTING_FIGURE_WORK`: modified publication scripts, captions,
  manifest/provenance, modified/deleted tracked figure assets, new
  publication-source CSVs, and untracked replacement figures under
  `publication_v1/`
- `PREEXISTING_GOVERNANCE_WORK`: existing Article V1 evidence, authority,
  claim-routing, and design/governance edits
- `TASK_OWNED`: this current-state file, the V2 Stage 1 reframe map, and the
  new V2 manuscript shell
- `UNRELATED`: remaining temporary and non-article dirty paths; none was
  modified, reset, staged, stashed, or discarded by this stage

## Known bounded gaps

- Targeted novelty and terminology verification remain incomplete for the
  specified E02/E03/E04 contribution framing.
- Final bibliographic verification is required for the citations selected for
  the V2 manuscript.
- The original dirty generator worktrees for E01–E03 are unrecoverable from
  Git alone. Frozen artifacts remain hash-valid; E04/E05 generator-source
  recovery is complete.
- The repository contains pre-existing uncommitted manuscript/figure and
  governance work. It remains derivative/provisional until its authority and
  provenance are explicitly recorded.

## Inherited scientific guardrails

- E01: retain the finite-horizon/restricted-feedback sampling result and the
  final-window persistence null; do not claim permanent masking.
- E03: `243/357` is defined tested-grid coverage, not a human or population
  frequency, individual-policy prevalence, or information-matched comparison.
- E04: preserve the tested final-window argmax definition and the bounded
  representation/scarcity/discoverability interpretation; do not state a
  generic search-complexity theorem.
- E05: retain the learned-versus-objective boundary separation, but do not use
  the binary-softmax/G2 temperature-exclusion argument or assert a causal
  explanation for the gap.
- E06/M4: remain outside V2 numerical Results and confirmatory Discussion
  claims.

## Next-stage boundary

`ARTICLE_V2_LID_STAGE7_FIGURE_FINALIZATION` may evaluate, redesign, and verify
the selected V2 figures only against frozen E01–E05 evidence, approved
publication-source tables, and the completed manuscript claims. It must not
rerun experiments, derive new results from pixels, alter frozen artifacts, or
use Figure 6 without separately resolving its authority and cross-estimand
noncommensurability. Captions, source-data selectors, axis language, and
accessibility must preserve the E03 tested-grid, E04 argmax/representation, and
E05 multi-action/censoring constraints. The known E04 Results tie-semantics
wording remains assigned to the later manuscript-wide consistency pass.
