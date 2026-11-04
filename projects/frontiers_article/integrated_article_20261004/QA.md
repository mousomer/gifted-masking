# Integrated article acceptance record

Date: 4 October 2026. Status: **complete for integrated author review**.
This is an editorial/figure-production acceptance record, not a new experiment
adjudication or a journal-submission release.

## Delivered scope

- One 32-page article with six main chapters, integrated educational relevance,
  an internal technical appendix, declarations, and 15 references.
- All C01–C23 supported claims retained. The contribution categories remain
  expected demonstrations, literature-anticipated directions, and less-obvious
  combinations/magnitudes; they do not stand in for evidence strength.
- Ten inline figures, up from six: new state-transition and decision-architecture
  diagrams, complete dynamic-grid classification, and complete sensitivity matrix.
- Native editable Word document and matching PDF, exported from that DOCX.
  Ten embedded images, ten unique captions, 278 native equations, 14 displayed.
- One local figure-text catalog, safe selected previews, ten PNG/SVG pairs,
  deterministic provenance, build metadata, and documented regeneration commands.

The source contains 11,608 whitespace words including captions, front/back
matter and equations; approximately 9,200 narrative/appendix words. Essential
methods and evidence are self-contained; the reader need not open a supplement.

## Scientific and source checks

The article was reviewed against the preceding manuscript, supplementary
methods, 23-claim map, and frozen source tables. Restored content includes direct
final-window intensity, all dynamic-grid categories, all 15 sensitivity settings,
solver/adequacy definitions, complete context/cost designs, and exact seed ranges.
Explicit M1 realized rewards, M2 initialization, and context-abundance rounding
were checked against maintained model definitions and added for completeness.

`verify_integrated.py` passes:

- All 19 preceding-revision files byte-identical to the pre-change snapshot.
- All 33 protected E01–E05 outputs and 18 evidence-matrix references intact.
- All 23 claim routes, ten inline figures in order, 42 numerical anchors,
  ten matching captions, and all master-seed ranges present.
- Seventeen figure source hashes and 20 figure output hashes match.
- Current article, builder, images, DOCX and PDF match build metadata.
- Native Word Title/equations and complete PDF captions/appendix verified.

The dynamic grid contains exactly 357 unique cells: 243 suboptimal-mask,
107 agreement and seven inconclusive. The sensitivity display uses exactly
375 records: 15 settings × five disagreement sentinels × five master seeds.
Twelve rows retain 25/25 classifications; alpha=.03 retains 18/25, tau=.6
21/25, and gamma=.5 10/25. The matrix keeps each exception's cell location.

Every inherited panel's values, selectors and notes match prior provenance
after figure renumbering. Numerical artist fingerprints are unchanged. A
deterministic repeat matched all 20 new PNG/SVG hashes. No stochastic experiment,
bootstrap, model fit, uncertainty estimator, or historical artifact was rerun.

## Executed checks

- `./gov check`, `./gov resolve`, and task-specific `./gov explain`: passed;
  FEATURE/development route, article RDS 0.11 scope.
- `./scripts/verify-governance.sh`: passed. Existing sanitation warnings concern
  parent traversal and spaced filenames; no governance failures were bypassed.
- `tests.test_publication_v1` and `tests.test_revision_figure_text`: 53 passed.
- `tests.test_integrated_article_figures`: nine passed, covering complete data,
  inherited values, text propagation, preview isolation and path guards.
- `tests.test_integrated_article_document`: four passed, covering the native
  overbar repair, expression/control preservation, idempotence and fail-closed
  handling of malformed input. **Total: 66 focused tests.**
- Preserved `verify_revision.py` and new `verify_integrated.py`: passed.

All Python commands used `/Users/omer/workspace/venvs/venv314/bin/python`.
Existing packages and tools were used; no dependency was installed. A proposed
PDF text check initially encountered unavailable pdfplumber; it was changed to
the already installed pypdf and passed. Matplotlib/Fontconfig cache warnings did
not prevent rendering or test completion.

The declared full `./scripts/verify.sh` was **not run**: it starts a full
robustness simulation and rewrites scientific `results/` artifacts. Such a run
is outside this editorial task's authorization and unnecessary to verify these
presentation changes. The governance hook and focused checks do not claim full
repository product acceptance. Model semantics, defaults, random-number
behaviour, and archived evidence are unchanged; no architectural drift occurred.

## Every-page visual review

The accepted PDF is the bundled-LibreOffice export of the accepted DOCX.
The skill renderer produced original-resolution 150-dpi page PNGs. Every page
was viewed, not merely a thumbnail contact sheet:

| Pages | Review |
| --- | --- |
| 1–3 | Title/authors/abstract, citations, heading hierarchy, prose continuity and footers clean. |
| 4–6 | Overview, Methods, outcome table and equations readable; no clipped table rows or figure text. |
| 7–11 | Model equations, state and architecture diagrams, cost grid, seed table and captions readable. |
| 12–15 | E01/E02 results and figures readable; Figure 5's long caption intentionally continues onto page 15 with its opening kept beside the image. |
| 16–19 | Dynamic thresholds, complete grid, sensitivity matrix and numerical Results clean. |
| 20–21 | Six-panel context figure and full caption fit page 20; crossing figure and caption legible. |
| 22–26 | Synthesis, Discussion and educational subsections flow correctly; no orphaned headings. |
| 27–30 | Conclusion and internal technical appendix complete; equations, seed/provenance text and source-family list readable. |
| 31–32 | Declarations, availability statement and all references/DOI wrapping complete and within margins. |

Initial layout review corrected schematic arrow-label collisions and Figure 9
legend overlap. Long-caption flow avoided large blank page bottoms without
shrinking figures. A Word-to-PDF issue rendered four literal overbar accents as
acute-like marks. The builder now translates only those U+203E accents into
native editable top bars, preserving their mathematical bases. All four repaired
pages (7, 13, 27, 29) were re-inspected; horizontal bars now render correctly.

Final render directory:
`output/qa/integrated_article_20261004/render_20261004T195827364658Z/`.
The other 28 final page PNGs are byte-identical to the previously inspected
`render_20261004T195422615979Z/` pages. The final document has no clipping,
overlapping text, missing figures, broken equations or blank pages.

## Remaining boundaries

Author review remains appropriate before submission. The persistent evidence
deposit and historical E01–E03 generator-source reconstruction remain the
previously disclosed separate issues; this integrated edition does not claim to
close them. Earlier manuscripts, submissions, figures and scientific evidence
are preserved. No publication, external upload, commit or submission occurred.
