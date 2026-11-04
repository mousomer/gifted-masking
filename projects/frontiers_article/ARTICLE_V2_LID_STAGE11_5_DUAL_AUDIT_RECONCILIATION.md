# Article V2 — Stage 11.5 Dual-Audit Reconciliation and Bounded Repair

**Stage:** `ARTICLE_V2_LID_STAGE11_5_AUDIT_REPAIR`

**Date:** 21 August 2026

**Scope:** authority reconciliation, bounded public-text repair, Figure 1
presentation repair, and content-addressed candidate replacement. No experiment,
estimator, configuration, frozen evidence, or stochastic fixture is in scope.

## 1. Independent audit records

The Sol and Claude Fable reports were produced independently. Fable was blind to
the Sol report. Neither report is modified by Stage 11.5, and absence from the
other auditor's report is not treated as evidence against a finding.

| Audit | Report | SHA-256 | Original result |
|---|---|---|---|
| Formal Sol | `ARTICLE_V2_LID_STAGE11_INDEPENDENT_SCIENTIFIC_AUDIT.md` | `1d5f3986a0389d6013dca6323ffeca97b18c7fce2bbc8adb622b83c16b96cfa4` | P0 0; P1 1; P2 2; P3 2; `READY_AFTER_BOUNDED_REPAIRS` |
| Independent Claude Fable | `ARTICLE_V2_LID_STAGE11B_CLAUDE_FABLE_INDEPENDENT_AUDIT.md` | `c413cabccff320395f953e868f9a9bbed1104b876d4b1b9c6205c7b6efc595eb` | P0 0; P1 1; P2 2; P3 9; `ADVISORY_MAJOR_ISSUES_FOUND` |

The original 62-input Stage 11 package manifest remains the historical identity
of the candidate both auditors reviewed. Its verified SHA-256 is
`4bcc1136652e219ee7b5047f14646b3ece0aefe183e875d962b46be3943018a5`,
and the pre-repair read-only check returned `62/62 VALID`.

## 2. Design-source and authority comparison

The repair boundary follows the active V2 current state and the Article V1
authority hierarchy rather than the historical RDS where they differ. The RDS
requires a reproducible short article, a permanent evidence archive, and no
experiment or model redesign during manuscript construction. The active V2
state further bounds Stage 11.5 to title synchronization, Figure 1 layout,
archival-identifier handling, and hash reconciliation. Frozen result files,
the evidence matrix, experiment manifests, estimators, source configs, and raw
tables remain controlling and immutable.

For E04, the controlling chain is the frozen effects table, evidence-matrix row
`E04-C6-MULTIPLE`, and the manuscript evidence freeze. All define the four
secondary quantities as within-master differences in the per-`log2(K)` slope
relative to the one-good-context regime. For E03, the controlling chain is the
frozen stable-cell table plus the maintained four-of-five classification rule.

## 3. Complete finding reconciliation

| Finding | Sol | Fable | Classification | Controlling authority | Decision | Bounded disposition |
|---|---:|---:|---|---|---|---|
| Supplement title omits “Uniquely” | P1 | P2 | `SAME_ISSUE_DIFFERENT_SEVERITY` | final manuscript title; Stage 10.5 title decision | `ACCEPT_REPAIR` | Make Supplement title exactly match the main title. |
| Figure 1 labels, boxes, and connectors overlap | P2 | P2 | `CONVERGENT` | Figure 1 caption and conceptual invariants; direct PDF/PNG inspection | `ACCEPT_REPAIR` | Change layout only and regenerate Figure 1 alone. |
| Data/Code statement retains archival-ID placeholder | P2 | P3 | `SAME_ISSUE_DIFFERENT_SEVERITY` | public GitHub origin is verified; no DOI/Zenodo/OSF identifier exists in repository authority | `ACCEPT_REPAIR_WITH_STAGE12_ARCHIVE_ROUTE` | Name the verified public project repository truthfully; require content-addressed deposit and persistent ID before submission. |
| E04 density controls called outcome changes | — | P1 | `FABLE_ONLY` | E04 frozen effects; `E04-C6-MULTIPLE`; evidence freeze | `ACCEPT_REPAIR` | Relabel unchanged values as changes in the per-`log2(K)` slope. |
| E03 seven-cell internal composition omitted | — | P3 | `FABLE_ONLY` | E03 frozen stable-cell table; four-of-five rule | `ACCEPT_CLARIFICATION` | State that five cells were inadequate in all masters and two failed stability with only 1–2 adequate masters. Preserve 107/243/7. |
| Five master streams are a thin Monte Carlo basis | P3 | — | `SOL_ONLY` | disclosed inferential unit and fixed-master design | `OPTIONAL_NO_CHANGE` | Existing limitation is accurate; no new simulation is authorized. |
| Future archive could expose generator-source scope more directly | P3 | — | `SOL_ONLY` | current provenance record; E04/E05 recovered bundles; E01–E03 limitation | `DEFER_TO_STAGE12_PRODUCTION` | Add a top-level public archive index during final evidence deposit. |
| Mixed magnitude/sign presentation in E02/E04 | — | P3 | `FABLE_ONLY` | signed frozen estimands are numerically correct and locally defined | `OPTIONAL_NO_CHANGE` | Stylistic harmonization is outside the bounded repair. |
| E05 display-equation period and following fragment | — | P3 | `FABLE_ONLY` | numerical statement and crossing authority are correct | `OPTIONAL_NO_CHANGE` | Typography only; no scientific correction required. |
| Acknowledgements stray bold markup | — | P3 | `FABLE_ONLY` | author-supplied acknowledgement text | `DEFER_TO_STAGE12_PRODUCTION` | Route copyediting to submission production; do not alter author-supplied content here. |
| Cross surname/initial ambiguity under strict APA style | — | P3 | `FABLE_ONLY` | current citations resolve by year and reference bijection passes | `DEFER_TO_STAGE12_PRODUCTION` | Route journal-style normalization to Stage 12; add no citation. |
| E05 temporal-flavoured vocabulary | — | P3 | `FABLE_ONLY` | adjacent prose explicitly states cost-axis, non-temporal semantics | `REJECT_AFTER_AUTHORITY_CHECK` | No prohibited temporal interpretation survives; changing supported prose would add no precision. |
| Figure 3A minor label collisions | — | P3 | `FABLE_ONLY` | direct visual assessment: legibility defect is minor and non-misleading | `DEFER_TO_STAGE12_PRODUCTION` | Do not expand the Stage 11.5 visual boundary beyond Figure 1. |
| E01 information-manipulation framing could gain a half-sentence | — | P3 | `FABLE_ONLY` | E01 Results already separate the null final-window contrast from information interventions | `OPTIONAL_NO_CHANGE` | Auditor itself finds current framing defensible; avoid unneeded prose. |

There are no P0 findings and no contradictory scientific assessments that
remain unresolved by authority. Fable identified no concrete P1/P2 journal-fit
defect, so the manuscript's `ADEQUATE_LID_FIT` positioning is not reopened.

## 4. Confirmed authority results

### E04 secondary density controls

The authority check confirms that the values are changes in the estimated
per-`log2(K)` slope relative to the one-good-context condition:

| Condition | Flat | Hierarchical |
|---|---:|---:|
| Two good contexts minus one good context | +0.05064 | +0.02524 |
| Proportional 25% receptive minus one good context | +0.06044 | +0.11224 |

The primary flat and hierarchical `K=16` minus `K=1` contrasts remain
`-0.234000` and `-0.470400`. The fixed-known-good and global-mask controls,
first-index `argmax` estimator, data, confidence intervals, and figures are not
changed by this repair.

### E03 seven-cell composition

The frozen stable-cell table contains five low-receptivity, zero-escape cells
with no adequate master classification and two further zero-escape cells
(`p=0.25` and `p=0.30`) with only one and two adequate masters, respectively.
The latter therefore fail the prespecified four-of-five stability rule. The
publication partition remains 107 agreement, 243 disagreement, and seven
inconclusive cells.

### Data and code availability

The configured origin is the public, non-archived GitHub repository
`https://github.com/mousomer/gifted-masking`. Repository authority and targeted
identifier searches contain no defensible persistent archival DOI, Zenodo
record, or OSF record for this project. The public statement may identify the
current project repository but must route the exact submission evidence deposit
and persistent identifier to Stage 12 as `REQUIRED_BEFORE_SUBMISSION`.

## 5. Approved change set and pre-repair preservation

The audited inputs approved to change are limited to the main manuscript,
Supplementary Methods, Figure 1 PDF/PNG, standalone captions, Figure provenance,
Figure/text consistency matrix, and Supplement/main consistency matrix. The
pre-repair copies and their manifest are stored under
`audit_snapshots/stage11_pre_repair/`. The deterministic visualization source
is also preserved there because it gains a Figure-1-only entry point. The
snapshot manifest SHA-256 is
`b399002f733a3d142163278e4b248c09322785aa6c63df9cf52ca7d75941ebad`,
and its nine declared files verify `9/9 VALID`.

No other Stage 11 package input is approved for modification. In particular,
both audit reports and the original Stage 11 package manifest remain immutable.

## 6. Post-repair matrix

| Repair | Before | Authority | After | Validation |
|---|---|---|---|---|
| E04 density controls | outcome change | frozen E04 slope estimand | unchanged values labelled as per-`log2(K)` slope changes | `PASS` |
| Supplement title | missing “Uniquely” | final main title | exact main/Supplement title match | `PASS` |
| Figure 1 | overlapping labels/boxes/connectors | conceptual caption and invariants | layout repaired; content unchanged | `PASS` |
| Data/Code | unresolved placeholder | verified public repository; no persistent ID | public repository named; archive/ID required before submission | `PASS_WITH_STAGE12_ROUTE` |
| E03 inconclusive cells | seven causes compressed | frozen classifier and stability table | five inadequate-all-master + two stability failures | `PASS` |

## 7. Focused delta-audit record

| Delta check | Result |
|---|---|
| Original manifest before repair | `62/62 VALID` |
| Original manifest after repair | Exactly eight approved deltas; 54 unchanged inputs remain valid |
| Audit report identities | Sol and Fable SHA-256 values unchanged |
| Original package-manifest identity | `4bcc1136...3018a5` unchanged |
| Figure 1 PDF | Changed as expected to `02ab24130d8554eb95725bdb64fcb8b6f091ed94e3e5d4af6834b6c2c7cdd54f` |
| Figure 1 PNG | Changed as expected to `68b4794f12ee09f4bd9a43a6660e6a13c2aa8c5b199d5142408688cdee9ae391` |
| Figures 2–4 | All six PDF/PNG hashes unchanged |
| Figure 1 visual inspection | PDF and PNG pass: no overlap, readable at publication width, connectors clear of labels |
| Figure 1 conceptual inspection | Many-to-one convergence, history-dependent divergence, information/expectation mediator, observed-behaviour endpoint, and E01–E05 mapping preserved |
| Generator boundary | Only `generate_v2_figures.py --figure 1` ran; no experiment or numerical figure path ran |
| Protected E01–E05 outputs | `33/33 VALID` |
| Evidence-matrix references | `18/18 VALID` |
| Main/supplement consistency | `CONSISTENT`; E03 5+2 and E04 slope semantics explicitly reconciled |
| Citation/reference bijection | Reference sections byte-identical; 13 main + 1 supplement-only = 14 unique; body year/citation tokens unchanged |
| Abstract | Byte-identical; SHA-256 `e35cf97a4bfbf6ad39206d5079bba52d2d2b4c8872bd0698b7b46a7871b76d6f` |
| Main title | Unchanged |
| Supplement title | Exact match to main title |
| Manuscript whitespace-word count | 8,165 before; 8,214 after; +49 from bounded E03/E04/Data-Code wording |
| E04 semantic search | All four rounded public values occur together with explicit per-`log2(K)` slope semantics; no public outcome-change label remains |
| Numerical regression search | No `-0.023`, `226/357`, or `226 of 357`; maintained E03/E05 values occur only with authoritative meanings |
| Prohibited-regression search | Two hits only, both explicit negations of temporal “give up”/binary-softmax readings |
| Public internal-language audit | No Stage 11, Sol, Fable, Codex, worktree, branch, readiness, governance, or audit-severity language |
| Public stale-title search | Zero obsolete-title hits in manuscript and Supplement |
| Reference counts | Main 13; Supplement-only 1; total unique 14 |
| `git diff --check` | `PASS` at delta-audit time |

The repaired-candidate manifest is intentionally created after this record is
finalized so it can content-address this reconciliation without a circular
hash dependency. Its path and SHA-256 are recorded in `ARTICLE_V2_CURRENT_STATE.md`.

## 8. Audit convergence statement

The title, Figure 1, and Data/Code issues converged across the two audits, with
different severities for the title and Data/Code item. Sol-only accepted work
is limited to routing the optional public-archive provenance index to Stage 12;
the thin-master observation remains an accurate disclosed limitation and does
not authorize simulation. Fable-only accepted work consists of the confirmed
E04 slope-label repair and E03 five-plus-two clarification. All other P3 items
are optional, rejected after authority inspection, or production-routed as the
table records. No unresolved P0/P1 or audit conflict remains.

## 9. Stage 12 production queue

The following items remain production-only and do not reopen Stage 11.5
science: exact content-addressed evidence deposit and persistent archival
identifier (`REQUIRED_BEFORE_SUBMISSION`); final journal filenames and file
formats; DOCX/PDF conversion; submission metadata; final CRediT, funding,
conflict-of-interest, and author-supplied copyediting confirmation; cover
letter; graphical-file requirements; supplement packaging; Figure 3A minor
layout review; strict journal-style citation-initial normalization; and a
top-level public provenance index.

**Stage 11.5 readiness:** `READY_WITH_STAGE12_PRODUCTION_ITEMS`

**Next:** `ARTICLE_V2_LID_STAGE12_SUBMISSION_PRODUCTION`
