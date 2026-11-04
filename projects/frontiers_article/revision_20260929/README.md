# Supported-claims scientific revision — 29 September 2026

## Read the revision

- [Main manuscript](MANUSCRIPT.md): the rewritten Abstract, six chapters,
  educational implications, six figure captions, declarations, and references.
- [Supplementary Methods](SUPPLEMENTARY_METHODS.md): S1–S10, exact definitions,
  restored outcomes, executed sensitivity results, seeds, and provenance.
- [Claim map](CLAIM_MAP.md): all 23 reviewed claims mapped to sections,
  experiment records, and mathematical authorities.
- [Revision QA](REVISION_QA.md): checks performed, repairs, and remaining
  production work.

This is a new scientific revision using the existing E01–E05 evidence. The
older manuscript, supplement, audited records, and submission previews remain
unchanged in their original locations. It is not a refreshed journal-submission
package. The revised manuscript is the active author-review version.

## Figures

**To change figure text:** start with [the editing guide](FIGURE_EDITING_GUIDE.md)
and [the per-figure text catalog](figure_text.py). All six current functions are
collected in [generate_figures.py](generate_figures.py). The guide includes a
function directory, label examples, and a separate single-figure preview command.

The six figures cover mechanisms, weighting/information, graded expression,
dynamic thresholds/persistence, receptive-context use, and learned/objective
boundaries. PNG displays are in `figures/`; vector PDFs are in
`../../../output/pdf/revision_20260929/`. [Captions](FIGURE_CAPTIONS.md) and
[machine-readable provenance](FIGURE_PROVENANCE.json) identify the plotted
quantities, selectors, source hashes, and output hashes.

`generate_figures.py` selects and aggregates existing archived tables and
evaluates exact displayed formulas. It does not simulate learners, refit PAVA,
bootstrap intervals, or change archived evidence. Existing NumPy and Matplotlib
are used; no dependency was added for this revision.

## Recheck without rerunning experiments

From the repository root:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/verify_revision.py
```

The command is read-only. To intentionally regenerate only this revision's
figure displays from hash-pinned sources:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/generate_figures.py
```

This second command overwrites the revision's own six PNG/PDF pairs and figure
provenance record, not earlier figures or simulation results. The full
repository `scripts/verify.sh` is not the editorial check: it runs a robustness
suite and rewrites scientific artifacts. See [the revision design](REVISION_PLAN.md)
for the accepted verification substitute and preservation strategy.
