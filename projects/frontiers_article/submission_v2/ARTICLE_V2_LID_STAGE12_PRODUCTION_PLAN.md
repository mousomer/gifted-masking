# Article V2 L&ID Stage 12 Production Plan

**Authorized state:** `ARTICLE_V2_LID_STAGE12_SUBMISSION_PRODUCTION`

**Scientific authority:**
`projects/frontiers_article/ARTICLE_V2_LID_STAGE11_5_REPAIRED_CANDIDATE_PACKAGE.md`

**Candidate manifest SHA-256:**
`1ef1a5252891d7f69c8e4f112765256d4a41dd51381ef4672d15b06801168124`

**Pre-production validation:** `67/67 VALID`

## Production boundary

Allowed changes are limited to journal formatting, typography, file naming,
reference punctuation, declarations, final public repository/archive
identifiers, and production-only figure layout repairs that do not change
scientific content. The title, Abstract, E01-E05 results, equations, estimators,
confidence intervals, interpretations, and Figure 1-4 scientific content are
frozen. No experiment, robustness suite, stochastic fixture, or alternate
estimator may run.

## Current journal requirements

Checked **21 August 2026** against the official Elsevier/ScienceDirect *Learning
and Individual Differences* Guide for Authors and current Elsevier artwork
instructions:

- https://www.sciencedirect.com/journal/learning-and-individual-differences/publish/guide-for-authors
- https://shop.elsevier.com/journals/learning-and-individual-differences/1041-6080
- https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-overview
- https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing

| Requirement | Stage 12 interpretation |
| --- | --- |
| Article type | Full length original research |
| Primary text | Maximum 8,000 words; excludes Abstract, Educational Relevance and Implications, tables, figures, references, and other materials |
| Abstract | Maximum 150 words; concise, factual, standalone, normally without references |
| Keywords | 1-5 English keywords |
| Highlights | Required separate editable file; 3-5 bullets; maximum 85 characters including spaces per bullet |
| Review model | Double anonymized; separate title page and anonymized manuscript |
| Title page | Title, authors, affiliations, acknowledgements, Declaration of Interest, full corresponding-author address and email |
| Manuscript source | Editable DOC/DOCX; single-column Word layout; PDF is preview only, not source |
| Main manuscript | Anonymized body with references, figures, and tables; no author or affiliation identifiers |
| Sections | Clearly numbered sections and subsections; Abstract unnumbered |
| References | APA Seventh Edition; alphabetical then chronological; DOI links encouraged; citation/reference bijection required |
| Figures | Separate, sequentially named files with captions; vector PDF/EPS preferred for charts; TIFF for bitmap; accepted PDF/EPS/TIFF/JPEG/Office |
| Figure sizing | Finished text normally 7 pt, never below 6 pt for subscripts/superscripts; 90/140/190 mm common widths |
| Bitmap resolution | 1000 dpi line art, 500 dpi combination art, 300 dpi halftone at final size |
| Figure fonts | Arial/Helvetica, Courier, Symbol, Times/Times New Roman recommended; embed nonstandard fonts |
| Supplement | Accurate, relevant, separately uploaded, clearly labelled; editable source retained |
| Research data | Option B: deposit and cite/link data where possible; otherwise explain why sharing is not possible |
| Data statement | Encouraged at submission and published with the article |
| CRediT | Corresponding author must provide actual contributor roles using the current taxonomy |
| Funding | Disclose sources and sponsor role; use the official no-specific-grant formulation if confirmed |
| Competing interests | Complete Elsevier Declaration of Interests; title page includes the statement |
| Generative AI | Any non-basic AI-assisted manuscript preparation must be declared before References using Elsevier's required section and author-approved wording |
| Accepted submission files | Editable Word/LaTeX source; separate figures and supplementary files; system creates the review PDF |

No separate hard limit for the Educational Relevance and Implications statement
was located in the current official guide. Its length is excluded from the
8,000-word primary-text limit.

## Production outputs

1. Separate anonymized manuscript DOCX and PDF preview.
2. Separate title-page DOCX and PDF preview after author metadata is verified.
3. Supplementary Methods DOCX and PDF.
4. Separate Figure 1-4 vector PDF upload files plus technical/visual audit.
5. Required highlights file.
6. Cover letter, metadata sheet, declarations status, and author-action list.
7. Exact E01-E05 evidence archive, archive README, checksum manifest, and
   persistent identifier.
8. Final submission manifest, final scientific freeze record, and documented
   candidate-to-submission transformation trace.

## Acceptance criteria

- Candidate and historical hashes match expected identities.
- Scientific source files remain byte-identical unless a separately recorded,
  production-only and meaning-neutral edit is explicitly authorized.
- Abstract is at most 150 words, keywords are reduced to at most five, and
  primary text is at most 8,000 words without arbitrary scientific cutting.
- Double-anonymized manuscript and title page satisfy the journal split.
- Every DOCX and PDF is rendered and inspected page by page; equations,
  tables, references, captions, and figures are intact.
- Figure 1 is the repaired Stage 11.5 file; Figure 3A is reviewed at print
  scale and changed only if an actual collision is observed.
- The public archive is E01-E05-only, content-addressed, and deposited under a
  real persistent identifier; no identifier is invented.
- Public repository/archive statements and Supplement S9 make compatible
  claims about `ARTIFACT_VERIFIED` outputs and the unrecovered E01-E03
  historical source state.
- Reference bijection, equation checks, E03/E04/E05 semantics, regression
  searches, internal-workflow searches, 33/33 protected-output validation, and
  18/18 evidence-matrix validation all pass.
- Required author metadata, CRediT, funding, competing-interest, originality,
  concurrent-submission, and AI-use declarations are either author-verified or
  explicitly marked `AUTHOR_CONFIRMATION_REQUIRED`; none are guessed.
- A final selective commit uses explicit paths only and is created only when
  the index is isolated and all final task-owned files are ready.
