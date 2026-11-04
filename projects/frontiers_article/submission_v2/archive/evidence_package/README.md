# Ability Concealment Publication Evidence Archive

This archive contains the exact E01-E05 computational evidence supporting
*Ability Concealment Does Not Uniquely Reveal the Environment: Learning and
Social Opportunity in Gifted Learners*.

## Included

- the five frozen E01-E05 standard configurations and experiment manifests;
- all 33 protected E01-E05 raw, summary, diagnostic-figure, and report outputs;
- the article evidence matrix and the analytic, inferential, and
  interpretation records needed to understand those artifacts;
- the source tables consumed by the final article figures and their provenance
  record;
- the final Supplementary Methods source;
- exact recovered historical generator-source bundles for E04 and E05;
- reproducibility and provenance instructions; and
- a SHA-256 manifest covering every file in the package.

## Excluded

- E06/M4, which is not evidence for this article;
- unrelated exploratory work and large sweeps;
- superseded manuscript and figure drafts;
- the former cross-estimand Figure 6, for which no separate comparability
  authority was established; and
- current-code artifacts that are not part of the publication evidence
  boundary.

## Provenance boundary

All 33 protected E01-E05 outputs are `ARTIFACT_VERIFIED`: their bytes match the
hashes stored in the frozen experiment manifests and evidence records.

The exact historical generator source was recovered for E04 and E05 and is
included under `projects/frontiers_article/provenance/frozen_generator_sources/`.
For E01-E03, the historical generator source state remains
`HISTORICAL_SOURCE_STATE_UNRECOVERED`. Those results are supported by their
content-addressed outputs, configurations, manifests, analytic checks, and
validation records; the archive does not claim that the present repository can
reproduce them bit for bit from the unrecovered historical source state.

Current maintained procedures and deterministic figure presentation are
separate from historical bit reproduction. See `REPRODUCIBILITY.md` and
Supplementary Methods S9.

## Public source repository

The maintained project repository is:

https://github.com/mousomer/gifted-masking

## Integrity

Run the command below from the extracted archive root:

```sh
shasum -a 256 -c MANIFEST.sha256
```

The archive container checksum and persistent record identifier are reported
in the article's final Data and Code Availability statement and submission
manifest. Container-level byte identity is asserted only when the deposited
download has been retrieved and compared directly.
