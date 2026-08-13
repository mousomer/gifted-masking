# E04 Standard Execution Authorization

**Decision:** `GO_STANDARD`  
**Date:** 2026-08-12  
**Scope:** exact frozen E04 baseline standard execution only

The E04 smoke gate independently verified the four maintained M3 architecture
semantics, exact 55-cell canonicalization of 120 requested cells, comparator
actions and regret calculations, RNG-family isolation, strict raw/curve/effect
and streaming validation, deterministic normalized regeneration, and complete
provenance. Cached versus uncached smoke artifacts were byte-identical.

This record authorizes exactly
`configs/frontiers_article/e04_m3_search_architectures_standard.json`: the
frozen baseline design with five reserved master seeds (`2026081401` through
`2026081405`), `n=500`, `T=2000`, final-window fraction `.2`, one worker, and
the approved 55 canonical executable cells. The readiness audit projects
137,500 primary rows, 275 million learner-steps, about 186.5 MiB raw output,
about 442.5 MiB conservative peak RSS, and under 10 minutes per generation.

No config mutation, sensitivity design or execution, publication-tier work,
claim adjudication, ledger update, manuscript edit, or figure substitution is
authorized. Stop after deterministic standard artifacts, reconciliation,
post-run verification, and a truthful standard execution report.
