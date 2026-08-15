# E06 core-standard deterministic-compression amendment

**Implementation authority:** explicit user instruction, 13 August 2026  
**Execution authority:** none; standard still requires a later independent
`E06_STANDARD_GO.md`  
**Qualification:** refused

## Narrow contract amendment

For the E06 core standard only, replace the staged primary path

```text
results/raw/<run_id>_units.csv
```

with

```text
results/raw/<run_id>_units.csv.gz
```

The logical decompressed payload remains the exact ordered 55-column UTF-8 CSV
specified by `E06_SMOKE_APPROVAL.md`. No field, row, model, seed, traversal,
inference rule, scenario, or decision rule changes. The existing smoke package
and every prior scientific artifact remain byte-identical and uncompressed.

## Deterministic gzip contract

- gzip level 9;
- `mtime=0`;
- empty original-filename header;
- UTF-8 CSV bytes with Python `csv` newline semantics;
- one gzip member and no trailing bytes;
- deterministic master → scenario → path → child row order.

The standard manifest must record, separately:

- compressed path, byte count, and SHA-256;
- logical decompressed CSV byte count and SHA-256;
- compression algorithm/settings;
- independent decompression/raw/cell replay status.

Validation must reject malformed gzip, noncanonical gzip headers, concatenated
members, trailing bytes, changed logical CSV, schema/order faults, and every
existing raw semantic corruption. Validators must stream; full raw
materialization remains prohibited.

## Resource gate

Before independent GO review, an exact-cardinality non-scientific fixture must
emit 52,000 field-shaped rows with 36,000 22-segment records and 16,000
11-segment records. Its varying numeric tokens must be deterministic and
high-entropy enough not to obtain a misleading repetition-only compression
ratio. Record compressed and logical sizes, runtime, RSS, algorithm/settings,
fixture version, and source/config fingerprints.

Readiness requires all of the following:

- projected wall time ≤ 600 seconds;
- stored compressed raw ≤ 150 MiB;
- all stored artifacts ≤ 200 MiB;
- peak RSS ≤ 512 MiB;
- logical uncompressed CSV bound ≤ the original formal 400-MiB raw stop;
- standard and qualification remain unexecuted.

If the fixture fails, no GO may be issued and compression settings may not be
tuned against scientific results.
