# Supported-claims revision — verification and handoff

Date: 29 September 2026

## Scope and scientific outcome

The author-authorized chapter-by-chapter rewrite restores all C01–C23 to the
main manuscript, aligns S1–S10 and six revised figures, and changes the
argument from primarily underidentification to specific mechanisms and
non-obvious findings. Familiar demonstrations and gifted-literature
expectations supply context; the graded trade-off, representation interaction,
successful-encounter/sustained-use separation, dynamic-threshold relocation,
sentinel persistence, and modal-boundary displacement lead the contribution.

This is a manuscript/presentation revision. There was no model, default,
seed strategy, experiment, raw-result, inference-method, or bootstrap change.
The preceding submission DOCX/PDF artifacts were not regenerated or represented
as the new text. No external submission, archive deposit, commit, or push ran.

## Checks performed

| Check | Result |
| --- | --- |
| Previous as-found manuscript and supplement preserved | PASS: 2/2 SHA-256 identities match the pre-edit baseline in REVISION_PLAN.md. |
| Frozen E01–E05 experiment outputs | PASS: 33/33 hash and byte-count matches using existing validators. |
| Content-addressed evidence-matrix references | PASS: 18/18 matches. |
| Existing targeted publication/extraction/algebra tests | PASS: 33 tests. |
| Main structure and supplement | PASS: six main chapters, 26 numbered main subsections, educational implications, S1–S10, and back matter. |
| Claim coverage and contribution categories | PASS: C01–C23 each mapped once; 14/2/7 primary category counts. |
| Restored numerical anchors | PASS: 25 section-specific number checks plus manual review of all main/supplement estimates, intervals, conditions, and denominators. |
| Exact reference mathematics | PASS: nine threshold, variance, reward, and crossover assertions. |
| Abstract and keywords | PASS: 144 whitespace-counted Abstract words; five keywords. This is an editorial check, not new certification of journal requirements. |
| References | PASS: 14 main reference entries, all cited in the body, with 14 distinct DOI links; added Zeidner–Schleyer reference verified against primary bibliographic sources. |
| Main–supplement consistency | PASS after two precise wording repairs listed below. |
| Figure data and file identities | PASS: 11 hash-pinned inputs, 12 figure outputs, and the generator SHA-256 validate. |
| Figure captions | PASS: all six manuscript caption sections match the separate figure-caption file. |
| Figure visual QA | PASS: all six final vector PDFs were rendered with Poppler and inspected page by page; headings, legends, annotations, axes, and captions are legible and unclipped. All six PDFs are single-page, unencrypted, and text-extractable. |

**Completion verdict:** `SCIENTIFIC_REVISION_READY_FOR_AUTHOR_REVIEW`.
The requested chapter-by-chapter implementation and its proportionate checks
are complete. Submission production remains a separate next stage.

## Independent scientific consistency review

A separate reader checked C01–C23 across the main manuscript, supplement,
claim map, and supported-claims review. All numerical values, intervals,
conditioning, time windows, replication counts, and parameter meanings aligned.
Two wording issues were identified and repaired:

1. Methods now state that independent policy enumeration checked the
   value-iteration benchmark over the 357 baseline grid cells. It does not
   imply that the fine bisection endpoints themselves were independently
   checked by that comparison.
2. Discussion now states that additional experience did not close the
   substantial dynamic-optimality gap at the five sentinels. It does not
   incorrectly rule out the modest improvement seen at two sentinels.

The main-text C14 claim uses five disagreement sentinels, not the sixth
boundary control or an extended-horizon full-grid replication. Supplement
S4.7 lists all 15 separately executed reference/sensitivity rows and their
25-cell-master classification counts, including the learning-rate,
temperature, and discount exceptions. The direct final-window E02 intensity
contrast is separately labelled from the full-horizon regret translation.

## Commands and verification boundary

Required Python: `/Users/omer/workspace/venvs/venv314/bin/python`.

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B -m unittest tests.test_publication_v1.FrozenEvidenceTest tests.test_publication_v1.E01ExtractionTest tests.test_publication_v1.E02ExtractionTest tests.test_publication_v1.E03ExtractionTest tests.test_publication_v1.E04ExtractionTest tests.test_publication_v1.E05ExtractionTest tests.test_publication_v1.AnalyticTableTest -v
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/verify_revision.py
```

The standard repository `scripts/verify.sh` was inspected but deliberately
not run: it executes the full robustness suite and additional model analyses,
writing into `results/`. Those actions are outside this editorial task and
would compromise its preserved-evidence boundary. The commands above are the
documented proportionate substitute; no failing test was bypassed.

## Remaining production steps

The scientific rewrite is a new candidate for author review, not a claim that
the earlier independent audit automatically certifies its changed text.
After author review, rebuild the anonymized submission DOCX/PDF and supplement
from these sources, refresh current journal rules and word counting, and
resolve the existing archive identifier and author-declaration requirements.
These external/production steps are not needed to complete the requested
chapter-by-chapter manuscript implementation.

The older Stage 11.5 manifest is not silently recertified: the as-found old
working manuscript and supplement already differed from its recorded hashes
before this task. Their exact pre-edit state is preserved and recorded in
REVISION_PLAN.md. Unrelated pre-existing worktree changes were left intact.

## Figure text editing implementation on 1 October 2026

The author requested a clearly documented collection of image-generating
functions so wording can be changed easily. All six active builders remain
together in `generate_figures.py`; visible wording is now in `figure_text.py`,
grouped by figure and panel, with shared labels defined once. The editing
guide lists the functions and helpers, demonstrates label changes and preview
commands, and distinguishes active files from historical simulation-driven
generators. RDS 0.10 records the presentation-layer scope and acceptance criteria.

The new CLI lists figures and renders selected previews only into an isolated
temporary directory. Canonical builds remain all-six. Text keys/types/template
placeholders and source hashes are checked before rendering. Preview path
checks cover directory and output-file symlink escapes, including the manifest.
New provenance binds the text catalog as well as generator, inputs, and outputs;
the revision checker rejects an unrendered text edit or preview provenance.

Verification results:

- PASS: 14 focused tests in `tests/test_revision_figure_text.py`, including
  pre-refactor numerical-artist fingerprints for all six figures, edited text
  reaching the artists, invalid catalog/selection/source rejection, preview
  isolation, symlink safety, CLI routing, and provenance.
- PASS: the same 33 targeted publication/extraction/algebra tests listed above.
- PASS: all 12 default regenerated PNG/PDF files are byte-for-byte identical
  to the pre-refactor files. Every prior input hash, plotted-data record,
  selector, and scientific note in provenance is identical. Only rendering
  source hashes and new build/text-catalog metadata changed in provenance.
- PASS: `verify_revision.py`, including 33 protected outputs, 18 evidence
  references, all 23 claim routes, captions, and the new text-catalog hash.
- PASS: a mocked unrendered catalog edit was rejected by the read-only
  verifier with the expected error; the test changed no file.
- PASS: all six regenerated PDFs were rendered with Poppler and inspected;
  headings, axes, notes, legends, and tick labels retain the reviewed layout.
- PASS: whitespace checks for changed tracked governance documents.

The following focused command supplements the existing verification commands:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B -m unittest tests.test_revision_figure_text -v
```

No scientific calculation, model, default, RNG sequence, archived evidence,
caption, manuscript text, or historical figure was changed. No dependency was
added and no experiment or estimator was run. The full repository verification
was again excluded for the artifact-writing reasons documented above. The PDF
workflow required rendered visual verification in addition to source-level
and file-hash checks. This tooling task is complete; author review and later
submission production remain the manuscript's next steps.
