# E06 second corrective pre-verification checkpoint

Status: `READY_FOR_USER_FULL_VERIFICATION`.

This bounded pass corrected only the external sealing boundary, its synthetic
tests, pending-evidence reconciliation, and E06 handoff documentation. It did
not change maintained M4 semantics, any frozen config, RNG consumption, or the
eight frozen scientific smoke artifacts.

The sealer now derives full-suite test counts and runtimes directly from a
strict complete verification log; accepts only the exact
`verification_exit_code=0\n` exit record; and recomputes normalized config,
approval, complete ordered source fingerprints, Git/head/branch/dirty binding,
all eight scientific artifact hashes/bytes, focused logs, and deterministic
regeneration evidence before atomically updating manifest/report provenance.

The synthetic temporary-package test accepts one complete evidence bundle and
rejects 26 corruption cases, including altered verification logs/exit records,
`01`, wrong command, caller totals, incomplete or failed suites, stale sources,
source/config/approval/Git/dirty drift, changed scientific artifacts, missing
or altered focused evidence, missing deterministic evidence, normalized
scientific mismatch, already-sealed packages, and inconsistent pending state.

Focused evidence passed: E06 10 tests in 12.473 seconds; M4 4 in 0.240;
core/determinism 7 in 0.203; post-artifact 4 in 7.804. Two independent fresh
smoke roots with distinct Matplotlib caches byte-match one another and the
canonical raw, five summaries, PNG, and warnings file. Their normalized
manifests/reports also match under the exact runtime/path/timestamp/Git rules
recorded in the v2 machine index.

The canonical report and manifest remain
`verification.status=pending_user_full_verification` and `seal_state=unsealed`;
focused and deterministic preverification evidence are now validated. The
core projection is 229.699 seconds, 126.661 MiB raw, 140.829 MiB total, and
121.828 MiB peak RSS, within frozen limits. Qualification remains refused.

Run only the user-owned round-2 command in
`results/reports/E06_USER_FULL_VERIFICATION_ROUND2_INSTRUCTIONS.md` next. Do
not run E06 standard or qualification.
