# E05 Frozen Generator Source

- **Experiment / run:** E05 / `frontiers_m3_bflpe_crossover_v1`
- **Original recorded commit:** `e0e9a738986dd440180a228b024b0807336cd957` (dirty worktree)
- **Recovered Git object:** unreachable root tree `53f905a2902496bf129e8125c718d78d48695d29`
- **Expected source fingerprint:** `f229a17da2c710d3c76ea5ca571fbf170a21e7c4c6c9c15cadda0366cfa19c02`
- **Recovered source fingerprint:** `f229a17da2c710d3c76ea5ca571fbf170a21e7c4c6c9c15cadda0366cfa19c02`
- **Recovery method:** enumerate relevant blobs from unreachable root trees, reconstruct the ordered eleven-path source bundle outside production paths, and apply the E05 fingerprint algorithm exactly.
- **Source kind:** unreachable Git tree and blobs; not a reachable commit, reflog commit, stash, retained worktree, or external archive.
- **Verification:** `HISTORICAL_SOURCE_RECOVERED`; byte-exact fingerprint match.

The `source/` directory preserves only the files that enter E05's recorded source fingerprint. It is historical provenance, not active production code, and was not executed during recovery. See `SOURCE_PROVENANCE.json` for the exact algorithm and file inventory.
