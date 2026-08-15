# E04 Frozen Generator Source

- **Experiment / run:** E04 / `frontiers_m3_search_architectures_v1`
- **Original recorded commit:** `e0e9a738986dd440180a228b024b0807336cd957` (dirty worktree)
- **Recovered Git object:** unreachable root tree `53f905a2902496bf129e8125c718d78d48695d29`
- **Expected source fingerprint:** `8599406b776d23f9357d89664f456d84f45e3a3783df1c830c1772ceb86750ae`
- **Recovered source fingerprint:** `8599406b776d23f9357d89664f456d84f45e3a3783df1c830c1772ceb86750ae`
- **Recovery method:** enumerate relevant blobs from unreachable root trees, reconstruct the ordered ten-path source bundle outside production paths, and apply the E04 fingerprint algorithm exactly.
- **Source kind:** unreachable Git tree and blobs; not a reachable commit, reflog commit, stash, retained worktree, or external archive.
- **Verification:** `HISTORICAL_SOURCE_RECOVERED`; byte-exact fingerprint match.

The `source/` directory preserves only the files that enter E04's recorded source fingerprint. It is historical provenance, not active production code, and was not executed during recovery. See `SOURCE_PROVENANCE.json` for the exact algorithm and file inventory.
