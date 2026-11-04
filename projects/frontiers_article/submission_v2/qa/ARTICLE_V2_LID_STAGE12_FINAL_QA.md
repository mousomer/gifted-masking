# Article V2 L&ID Stage 12 Final Production QA

**Checked:** 21 August 2026

**Authorized stage:** `ARTICLE_V2_LID_STAGE12_SUBMISSION_PRODUCTION`

**QA status:** `BLOCKED_BY_JOURNAL_WORD_LIMIT`

This report closes the work that can be completed without changing the frozen
scientific candidate, inventing author declarations, or publishing an external
archive record. The generated DOCX/PDF files are controlled previews, not
submission-ready files.

## 1. Candidate and historical authority

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Stage 11.5 repaired-candidate manifest | `1ef1a525...` | `1ef1a5252891d7f69c8e4f112765256d4a41dd51381ef4672d15b06801168124` | PASS |
| Candidate contents | 67/67 valid | 67/67 valid | PASS |
| Sol audit | `1d5f3986...` | exact match | PASS |
| Fable audit | `c413cabc...` | exact match | PASS |
| Stage 11.5 reconciliation | `59d9fbae...` | exact match | PASS |
| Article V1 manuscript | `cd27687b...` | exact match | PASS |

The frozen manuscript source remains
`217d259929f5d0c585bf9da1de3c33befb8403b57a79a0c4f5257627ab0f5199`.
The frozen Supplementary Methods remains
`a413ee282e108dc225d8e2f29b74263dbdb514eb5cc6af89eeec64267dc929ce`.

## 2. Current journal requirements

The current requirements were checked on 21 August 2026 against the official
*Learning and Individual Differences* Guide for Authors and current Elsevier
artwork instructions:

- https://www.sciencedirect.com/journal/learning-and-individual-differences/publish/guide-for-authors
- https://shop.elsevier.com/journals/learning-and-individual-differences/1041-6080
- https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-overview
- https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing

The compact requirements checklist is in
`submission_v2/ARTICLE_V2_LID_STAGE12_PRODUCTION_PLAN.md`. The decisive limits
are 8,000 primary-text words and 150 Abstract words. The journal requires one
to five keywords, three to five highlights of no more than 85 characters,
double-anonymized review, an editable Word manuscript, a separate title page,
separate figure files, declarations, and a research-data statement.

## 3. Word counts

Counts use Pandoc plain-text conversion followed by a heading-excluded word
tokenization. Hyphenated and en-dash compounds count as one word. Abstract
keywords, reference lists, and figure captions are excluded from the indicated
subtotals.

| Component | Words | Journal comparison |
| --- | ---: | --- |
| Title | 15 | Recorded |
| Abstract | 221 | **FAIL — hard maximum 150** |
| Introduction | 1,215 | Included in primary subtotal |
| Methods | 1,378 | Included in primary subtotal |
| Results | 1,508 | Included in primary subtotal |
| Discussion | 1,606 | Included in primary subtotal |
| Limitations | 367 | Included in primary subtotal |
| Conclusion | 190 | Included in primary subtotal |
| Primary subtotal | 6,264 | PASS — maximum 8,000 |
| Educational Relevance and Implications | 648 | Excluded from the journal's primary limit |
| Total excluding references/captions | 7,133 | Recorded |
| Figure captions | 565 | Excluded |
| Main reference list | 409 | Excluded |
| Supplementary Methods | 3,539 | Recorded |

The Abstract is scientifically frozen at Stage 12. It was not shortened
without authorization. This forces the verdict
`BLOCKED_BY_JOURNAL_WORD_LIMIT`.

## 4. Archive verification

The local archive is
`submission_v2/archive/ability_concealment_e01_e05_evidence.zip`, SHA-256
`71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb`.
It contains one manifest plus 101 manifest-bound payload files. The archive
includes the five frozen configurations, five experiment manifests, all 33
protected outputs including raw unit tables, the evidence matrix, analytic and
inferential authorities, interpretation/provenance records, publication-source
figure tables, figure captions/provenance/generator, E04/E05 recovered source
bundles, the Supplementary Methods, and public reproducibility documentation.

Independent copy validation passed 101/101 manifest entries. ZIP structural
validation reported no errors. The archive excludes E06/M4 evidence, the former
cross-estimand Figure 6, superseded drafts, and unrelated worktree material.
The public README distinguishes `ARTIFACT_VERIFIED` E01-E05 outputs from
`HISTORICAL_SOURCE_STATE_UNRECOVERED` E01-E03 generator states.

No persistent provider was selected by repository authority. Zenodo was
inspected but the session was unauthenticated; no upload, record, DOI, or
persistent URL was created. Provider, creator metadata, license, and the
external publication action require author confirmation. Consequently the
separate blocker `BLOCKED_BY_ARCHIVAL_IDENTIFIER` also remains.

## 5. Submission conversion and visual QA

The deterministic production builder imports no experiment or stochastic
entry point. It produced a single-column, double-anonymized Word manuscript,
separate title page, highlights, Supplementary Methods, and previews. Main
manuscript: 36 pages. Supplement: 18 pages. Title page, highlights, and cover
letter: one page each.

Every rendered page was inspected. Equations, headings, captions, tables,
links, page numbering, symbols, and references are present and legible. No
table or figure is clipped. DOI wrapping is acceptable; `Klimecká` is intact.
Figure 3A labels remain legible at upload/print scale, so the production
outcome is `NO_CHANGE`.

The equation review covered $43/60$, the E02 affine disclosure expression, the
E03 dynamic-value relation, $0.40-0.85b_f$, $8/17$, subscripts, Greek symbols,
$\log_2 K$, deterministic first-index `argmax`, and PAVA wording. No visual
conversion corruption remains. Plain-text PDF extraction inserts spacing into
some display equations; that is an extraction artifact, not a rendered-page
defect.

The final vector figure PDFs are one page each, use widths of 522 points, and
contain embedded/subset fonts. Figure 1 matches both required repaired hashes:
PDF `02ab24130d8554eb95725bdb64fcb8b6f091ed94e3e5d4af6834b6c2c7cdd54f`;
source PNG `68b4794f12ee09f4bd9a43a6660e6a13c2aa8c5b199d5142408688cdee9ae391`.
Figures 2-4 are byte-identical to the repaired candidate.

## 6. Candidate-to-submission trace

The trace is:

`Stage 11.5 repaired candidate -> frozen Markdown source -> blinded production Markdown -> DOCX -> PDF preview`.

The Supplement production source is byte-identical to the frozen Supplement.
The main production source differs only through these declared
production transformations:

1. remove author/affiliation/correspondence lines from the blinded manuscript;
2. reduce seven keywords to the permitted five without changing scientific prose;
3. disambiguate the 1993 and 2019 Cross citations with `T. L.` and `J. R.` initials;
4. embed unchanged frozen Figure 1-4 images after their unchanged captions;
5. move author declarations to the separate title page; and
6. replace identifying/deposit language in the blinded review copy with a
   bounded anonymized availability statement.

Title, Abstract, Introduction, Methods, Results, Discussion, Educational
Relevance, Limitations, Conclusion, numerical claims, equations, and figure
caption wording otherwise match the repaired scientific source. No unexplained
scientific-text difference was observed.

## 7. Focused scientific production checks

| Check | Result |
| --- | --- |
| E04 secondary values | PASS: +0.051, +0.025, +0.060, +0.112 all remain changes in estimated per-$\log_2 K$ slope relative to the stated one-good-context regime. |
| E03 grid result | PASS: 243/357 remains tested parameter cells, not prevalence; 107 agreement and seven inconclusive are retained. |
| E03 5+2 nuance | PASS: five all-master-inadequate plus two stability-failing cells is explicit in main text/caption and detailed in the Supplement. |
| E05 Abstract values | PASS: 0.313 and 0.471 are present. |
| E05 detailed values | PASS: 0.312852, $8/17=0.470588$, and 0.157736 are present. |
| E05 interpretation | PASS: comparison-cost axis, non-temporal wording, no G2 inference, and hierarchical left censoring are retained. |
| Main references | PASS: 13/13 cited and listed. |
| Supplement reference | PASS: Best and Chakravarti (1990) is cited and is the only supplement-only entry. |
| Cross ambiguity | PASS: in-text initials distinguish T. L. Cross (1993) from J. R. Cross (2019); reference author sets and years remain correct. |
| Former Figure 6 | `FORMER_FIGURE6_EXCLUDED_NO_SEPARATE_AUTHORITY`. |

## 8. Regression and workflow-language searches

The prohibited-regression search over the manuscript, Supplement, title page,
highlights, cover letter, and public archive surface found no scientific
regression. Four contextual hits were manually inspected: E06/M4 appears only
in two archive-scope exclusion statements; “give up” appears only in explicit
non-temporal disclaimers in the manuscript and Supplement; and
“binary-softmax” appears only in the Supplement sentence stating that no such
identity was used. The stale title and every stale number/claim were absent.

The internal-workflow search over the same submission-facing surface returned
zero hits. Frozen authority files inside the evidence compendium retain their
historical audit/provenance vocabulary by design; they are immutable evidence
records, not submission prose or the public archive README.

## 9. Declarations and author metadata

| Item | Classification |
| --- | --- |
| Author names/order | `AUTHOR_CONFIRMATION_REQUIRED` |
| Affiliations/corresponding details/ORCID | `AUTHOR_CONFIRMATION_REQUIRED` |
| CRediT roles | `AUTHOR_CONFIRMATION_REQUIRED` |
| Funding | `AUTHOR_CONFIRMATION_REQUIRED` |
| Competing interests | `AUTHOR_CONFIRMATION_REQUIRED` |
| Originality/concurrent submission | `AUTHOR_CONFIRMATION_REQUIRED` |
| Generative-AI declaration | `AUTHOR_CONFIRMATION_REQUIRED` |
| Acknowledgements typography | `VERIFIED`; factual author approval remains required |
| Suggested/opposed reviewers | `AUTHOR_INPUT_REQUIRED_FOR_REVIEWERS` if used |
| Archive provider/license/publication | `BLOCKED_BY_ARCHIVAL_IDENTIFIER` |

No declaration or missing metadata was inferred. The cover letter therefore
does not assert originality or absence of concurrent consideration, and its
production note must be removed only after author confirmation.

## 10. Frozen evidence and repository actions

The established read-only repository validators passed:

- protected E01-E05 outputs: **33/33 VALID**;
- evidence-matrix references: **18/18 VALID**.

No experiment, robustness suite, stochastic fixture, alternate estimator, or
figure generator ran. The repository-wide verification script was not run
because this stage expressly forbids stochastic fixtures; the authorized
read-only validators and production-integrity checks were used instead.

The Git index was empty and safe. No selective checkpoint was created because
the task-owned package is not final: the hard Abstract limit, persistent
identifier, and required author confirmations remain unresolved. No push, PR,
journal submission, or archive publication occurred.

## 11. Required 41-item final report

1. Candidate manifest: exact expected hash; 67/67 valid.
2. Journal source/date: official URLs above; 21 August 2026.
3. Title: *Ability Concealment Does Not Uniquely Reveal the Environment: Learning and Social Opportunity in Gifted Learners*.
4. Abstract: 221 words; hard 150-word limit failed.
5. Primary text: 6,264 words; 8,000-word limit passed.
6. Educational Relevance: 648 words.
7. References: 13 main.
8. Supplement: 3,539 words; one supplement-only reference.
9. Archive: E01-E05 exact evidence boundary described in Section 4.
10. Archive provider: none selected; Zenodo inspected only.
11. Persistent identifier/DOI: none; not fabricated.
12. Archive checksum: `71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb`.
13. Data/Code statement: pending real identifier; controlled draft in `declarations/`.
14. Manuscript source: `ARTICLE_V2_LID_MANUSCRIPT_DRAFT.md`; SHA-256 `217d2599...`.
15. DOCX: blinded blocked preview; SHA-256 `88149d40...`.
16. PDF: blinded blocked preview; SHA-256 `e0f4c4d2...`.
17. Supplement: DOCX `054b436a...`; PDF `0e3f1ff5...`.
18. Figures: hashes recorded in the submission manifest.
19. Figure 3A: `NO_CHANGE` after actual-scale review.
20. Author/affiliations: confirmation required.
21. CRediT: confirmation required.
22. Funding: confirmation required.
23. Conflicts/declarations: confirmation required.
24. Acknowledgements: rendering verified; factual approval required.
25. Cross ambiguity: resolved with initials.
26. Cover letter: pending-confirmation DOCX/PDF/Markdown; hashes in manifest.
27. Metadata sheet: pending confirmation; SHA-256 `50d69f9c...`.
28. Blind package: produced; title page remains pending confirmation.
29. Submission manifest: `ARTICLE_V2_LID_FINAL_SUBMISSION_MANIFEST.md`.
30. Scientific freeze: `ARTICLE_V2_LID_FINAL_SCIENTIFIC_FREEZE.md`, blocked/not activated.
31. Reference bijection: 13/13 main and 1/1 supplement pass.
32. Equation render: pass.
33. Prohibited regression: pass after contextual-hit review.
34. Internal workflow language: zero submission-facing hits.
35. Frozen evidence: 33/33 valid.
36. Evidence matrix: 18/18 valid.
37. Scientific source to conversion: pass with six declared production-only transformations.
38. Git checkpoint: not created because final-readiness conditions failed.
39. Push: no.
40. Author actions: approve a <=150-word Abstract revision; confirm metadata,
    declarations, CRediT, funding, conflicts, acknowledgements, originality,
    AI-use disclosure, archive provider/license/metadata/publication, and any reviewers.
41. Readiness verdict: `BLOCKED_BY_JOURNAL_WORD_LIMIT`.

## 12. Acceptance checklist

- [x] Repaired candidate and historical authorities validate.
- [x] Current journal requirements verified.
- [x] Exact local E01-E05 evidence package built and independently validated.
- [ ] Persistent archive identifier obtained.
- [ ] Final public Data/Code statement contains a real identifier.
- [x] Blinded manuscript/title-page/highlights previews generated.
- [x] Supplement DOCX/PDF generated.
- [x] Figures 1-4 satisfy the inspected technical requirements.
- [x] Figure 1 repaired version used; Figure 3A accepted without change.
- [x] Cover-letter draft and metadata sheet produced.
- [ ] Required author metadata and declarations confirmed.
- [x] Acknowledgement markup and Cross ambiguity resolved.
- [x] Reference bijection, equations, scientific qualifiers, and visual QA pass.
- [ ] Abstract meets the 150-word limit.
- [x] No experiments or stochastic fixtures ran.
- [ ] Selective final checkpoint created.

**Final verdict:** `BLOCKED_BY_JOURNAL_WORD_LIMIT`
