# Article V2 — supported-claims scientific revision

Date: 29 September 2026

## Authorization and design

The author requested implementation of the chapter-by-chapter plan following
the supported-claims review and three-category scientific contribution review.
This is a new scientific revision, not a formatting-only continuation of Stage
12. It supersedes the earlier editorial emphasis for this revision only.
The maintained model contracts and frozen E01–E05 artifacts continue to govern
all mathematics, definitions, estimands, and numerical statements.

Active revision files are `MANUSCRIPT.md`, `SUPPLEMENTARY_METHODS.md`,
`CLAIM_MAP.md`, and the `figures/` display layer in this directory. Earlier V2
source files, audit packages, submission previews, and scientific evidence are
preserved in place. E06/M4 remains excluded from numerical Results.

Comparison with the V2 reframe map shows that weighting and dynamic thresholds
were already admissible but underrepresented. The new contribution hierarchy
uses familiar mechanisms as compact demonstrations, gifted-literature
expectations as motivation, and the six surprising themes as the main narrative.
Secondary outcomes remain labelled secondary; editorial prominence does not
retroactively change the experiment design.

## Work plan

1. Rewrite all six main chapters, Abstract, educational implications, and
   figure captions around C01–C23; retain author declarations.
2. Expand supplementary definitions and results for all restored outcomes.
3. Create six deterministic figures using existing archived results, with no
   experiment, bootstrap refit, alternate estimator, or new sensitivity run.
4. Map all 23 claims to main text, supplement, and source evidence.
5. Verify protected hashes, numerical/semantic consistency, reference routing,
   figure-source agreement, and figure readability; update project state.

## Acceptance criteria

- C01–C23 each has an explicit Results and supplementary/source home.
- Abstract emphasizes the non-obvious results and is at most 150 words as an
  editorial target inherited from the previous production check; this is not a
  fresh certification of current journal rules.
- Engagement, intensity, endpoint use, modal classification, actual masking,
  successful encounter, and accumulated objective loss are not conflated.
- E03 sensitivity statements name five sentinels and separately tested changes.
- E05 uses expected reward and modal-population crossing terminology correctly.
- Direct, affirmative model-result statements replace repetitive disclaimers.
- Existing equations, seeds, configurations, simulation code, and evidence
  artifacts are unchanged; there is no new empirical claim about children.
- Every new figure uses traceable deterministic selections/aggregations and
  is rendered and visually inspected.

## Verification decision

`scripts/verify.sh` was inspected. It runs the full robustness suite and writes
into `results/`, followed by further model analyses. Running it would change
scientific artifacts unrelated to this editorial revision. Use the existing
read-only protected-output/evidence-matrix validators plus revision-specific
structural, algebraic, figure, and reference checks instead. Record exact
commands and outcomes in `REVISION_QA.md`.

## Baseline preservation

The pre-edit working manuscript hash is
`7742f7542541d61ee74fb22183b400e796f8a8d2c770dae1d9883a0d079df1f9`;
the pre-edit working supplement hash is
`341a91b2ff5386c54a86d761de25e60e1f02da280802e8d8865f8f12daea6a26`.
Both differ already from their hashes in the historical Stage 11.5 manifest.
This revision does not repair or silently recertify that earlier candidate.
It preserves the as-found files and starts a separately identified revision.

No journal submission, archive deposit, commit, or external message is part of
this task. Production DOCX/PDF previews in `submission_v2/` remain historical.
