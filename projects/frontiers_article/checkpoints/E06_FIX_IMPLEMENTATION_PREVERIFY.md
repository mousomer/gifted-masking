# E06 FIX_IMPLEMENTATION pre-full-verification checkpoint

**Status:** `READY_FOR_USER_FULL_VERIFICATION`

This checkpoint closes only the remaining derived-artifact validation gate.
The canonical smoke manifest remains at
`verification.status=pending_user_full_verification`; no full repository
verification was run by Codex.

1. **Tier, run, config, and approval.** The only execution was diagnostic
   smoke `frontiers_m4_path_diagnostics_v1_smoke` with
   `configs/frontiers_article/e06_m4_paths_smoke.json` and
   `approvals/E06_SMOKE_APPROVAL.md`. Config SHA-256 is
   `475a8630acc73ab21520fd90024f85712b0002aec52d39d18e74e96cb8e4c40b`;
   approval SHA-256 is
   `9fc0434c86da23815afc3327f79c0e9824918417839aadda39dc1ba061cb76f7`.
2. **Frozen design and counts.** S00 remains `n=64`, 120 steps/segment,
   final window 96--119, five numeric km values, one master seed, five packed
   path families, 320 primary rows, and 345,600 learner steps. Derived rows
   are cells 45, paths 20, loops 8, transitions 8, and effects 6.
3. **Maintained-M4 replay.** The E06-local recorder remains parity-tested
   against maintained M4: stable softmax, one acceptance draw for every
   action, objective reward, selected-Q update, and then receptivity update.
   Its action/outcome/reward diagnostics, state continuity/reset checks, and
   zero post-update bounds violations remain valid.
4. **Path/control semantics.** Inherited paths retain p and both Q values;
   reversal and cold starts reset both; disabled-feedback paths retain nominal
   km while applying actual km zero. No model semantics or defaults changed.
5. **Seed and pairing boundary.** Namespace-6 semantic segment seeds,
   inherited/reversal pairing, and namespace-60 bootstrap-helper isolation
   remain unchanged and focused tests pass.
6. **Raw reconciliation.** Packed raw validation remains fail-closed for
   schema, identity/order, counts, rates, objective rewards, p/Q continuity,
   finiteness, boundaries, and final state reconciliation.
7. **Derived validation correction.** `validate_e06_derived(raw_rows, cells,
   paths, loops, transitions, effects, config)` now requires the exact frozen
   config and validated raw rows, independently reconstructs every table, and
   compares ordered schemas, identities, cardinalities, order, and finite
   numerical values at absolute tolerance `1e-12`. It verifies aligned numeric
   km paths, gaps, loop areas/separation/control excess, cold endpoint,
   disabled-placebo effects, transition/censoring/bootstrap fields, and smoke
   noneligibility. It runs both on materialized rows and on parsed CSV outputs
   before the final manifest. Streaming validation is correctly recorded as
   `not_applicable_materialized_packed_rows`: no streaming writer exists and
   the frozen raw/RSS projections remain within limits.
8. **Adversarial proof and noninference.** Focused tests confirm rejection of
   cell/effect values and identities, path gaps/km alignment, signed/absolute
   loop areas, control excess, transition estimate/status/eligibility, row
   reordering, duplicates, missing/foreign rows, NaN, and infinity. Smoke
   intervals stay blank, bootstrap replicate count stays zero, and every
   `decision_eligible` field is false; no unavailable value is zero-filled.
9. **Deterministic regeneration.** Fresh root
   `/private/tmp/e06_regen_derived_final` byte-matched raw, all five derived
   CSVs, PNG, and warnings. The normalized canonical manifest and report also
   matched after removal only of documented timing/projection fields.
10. **Focused verification.** E06: 7 tests passed; M4: 4; core/determinism:
    7; focused post-artifact E06 contract: 7. Logs with stdout/stderr, exit
    code, and elapsed seconds are under `results/reports/e06_preverification_logs/`.
    Full repository verification was intentionally not run.
11. **Phase-separated capacity.** The conservative core projection is 181.547
    seconds, 126.661 MiB raw, 140.829 MiB total artifacts, and 119.625 MiB
    peak RSS—within the frozen 600 s/400 MiB/500 MiB/2 GiB limits.
    Qualification is separately projected at 579.400 seconds and remains
    refused, regardless of that estimate.
12. **Provenance and artifacts.** Source fingerprint SHA-256 is
    `8b404d6cb3493d48c2469881e798772ff93bd415caaeec64b0e41beec734e4a6`.
    The canonical manifest, raw/derived artifacts, report, warnings, figure,
    focused logs, row counts, byte counts, and hashes are indexed in
    `results/manifests/frontiers_m4_path_diagnostics_v1_smoke_preverification.json`.
    No unresolved warning remains beyond user-owned full verification.
13. **Boundary and user action.** Run exactly the copy-ready command in
    `results/reports/E06_USER_FULL_VERIFICATION_INSTRUCTIONS.md`, preserve its
    log, and then provide it with this checkpoint and assessment index to a
    fresh independent Sol review. Standard, qualification, C8/C9 adjudication,
    claim evidence/ledger, article prose, and Figure 4 remain explicitly
    refused.

Files changed in this remaining correction: `src/gifted_masking/experiments/e06.py`,
`tests/test_article_e06.py`, regenerated approved E06 smoke artifacts,
focused logs, this checkpoint, the machine assessment index, and the user
verification instructions.
