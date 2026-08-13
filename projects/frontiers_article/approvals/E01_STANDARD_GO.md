# E01 Standard Execution Authorization

**Decision:** `GO_STANDARD`  
**Date:** 2026-08-12  
**Reviewer:** separate `gpt-5.6-sol`, `xhigh` smoke-gate pass  
**Scope:** frozen E01 five-seed standard execution only

The corrected E01 smoke package passed semantic, RNG, baseline, deterministic
regeneration, summary, figure, provenance, validation, runtime, and repository
verification checks. This record authorizes execution of exactly:

`configs/frontiers_article/e01_hot_stove_standard.json`

The frozen standard contract uses five reserved master seeds, `n=500`,
`T=2000`, final-window fraction `.2`, one worker, the approved M0 payoffs and
learner values, and the exact ten E01 cells. It projects 25,000 primary rows and
50 million learner-steps.

This decision does not authorize configuration changes, sensitivity or
publication-tier runs, claim adjudication, claim-ledger updates, or manuscript
changes. The implementation pass must stop after deterministic standard
artifacts, reconciliation, verification, and its execution report are complete.
