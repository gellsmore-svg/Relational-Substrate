# GT-P012 coverage and integrity audit

| Requirement | Status | Evidence |
| --- | --- | --- |
| Live heads verified before work | yes | `docs/gt-p012-starting-audit.md` (`666a9b9`): GT `a81c505`, hub `38c2501`, PR #9 `42a474a`; no charter files |
| Prompt stored verbatim | yes | `provenance/prompts/GT-P012-agent-input.md`, sha256 `336f19c5…9384` (the author's file) |
| Definitions and proofs before freeze | yes | `docs/e5d-local-traffic-comparator.md` (T16–T19), commit `3746ef1` |
| Fixtures before freeze (no science cell) | yes | 8 NL fixtures (including a non-reversible circulating chain) and 6 runner tests; 897 tests; CI 38808827539 |
| Freeze pushed before execution | yes | `c74d896` (plan_hash `6a83dbb7…1fe7`); journey step 30 `5246cce`; committed and local plan bytes identical |
| Executed once | yes | 21:23:52Z to 21:30:23Z; 12/12 complete; 18/18 analyses |
| Frozen checks | all pass | E5C replication (target/ND/NK), NL identities, macro conservation, durability checks, NULL fixed point |
| Matrix completeness, no selection | yes | F_TRI × 12 laws including the NULL, CLOSEW, CSPH and PATHF negatives; F_2PATH × six N=6 laws |
| Structural labels | yes | F_TRI size N−2 STRUCTURALLY_IMPOSSIBLE; N5 F_2PATH excluded (T14) |
| Unresolved channels | none | — |
| Earlier records untouched | yes | E5A–E5C files, plans and snapshots unchanged; new findings are appended |
| Scope | yes | only `gravity-time/` and new `constraint-lab` code and tests; no CL/SC branch, no books, no ontology change |
| Semantic issues | noted | "residual beyond NL" is projection-relative; D1 and D3 are not separable here |
