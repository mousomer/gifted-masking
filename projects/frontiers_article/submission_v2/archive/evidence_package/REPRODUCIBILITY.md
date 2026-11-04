# Reproducibility and Validation

## What can be validated directly

`MANIFEST.sha256` binds every file in this evidence package. The five JSON
experiment manifests independently bind the 33 protected E01-E05 outputs.
The article evidence matrix binds its cited result artifacts and exact claim
limits. These checks are read-only and do not execute a simulation.

From the extracted archive root:

```sh
shasum -a 256 -c MANIFEST.sha256
```

For additional repository validators, obtain the maintained source repository
and use the documented workspace environment and verification command:

```sh
git clone https://github.com/mousomer/gifted-masking.git
cd gifted-masking
./scripts/verify.sh
```

The repository's Python environment and dependency instructions are in its
README and `AGENTS.md`. Running the test suite validates maintained code; it is
not a claim of bit-identical regeneration of the archived E01-E03 outputs.

## Historical source status

- E01-E03: archived outputs, configs, manifests, evidence records, and hashes
  are available, but the exact historical generator source state was not
  recovered.
- E04-E05: fingerprint-exact historical generator-source bundles are included
  with their own provenance records.

## Experiment identity

The five experiment manifests record normalized configurations, parameter
values, master-seed hierarchies, package versions, platform information,
commands used historically, output paths, and output hashes. The primary
simulation environment recorded Python 3.14.6 on macOS arm64 with NumPy 2.4.6;
E01, E02, E04, and E05 also record Matplotlib 3.10.8.

## Scientific evidence boundary

Only E01-E05 support the article. E06/M4 and unrelated exploratory work are not
included and should not be inferred from this package.
