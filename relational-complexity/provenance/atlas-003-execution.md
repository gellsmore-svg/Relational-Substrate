# atlas-003 execution record

The cells were run after `plans/atlas-003.json` was frozen and pushed. The plan file was not edited. This record does not interpret the cells. Comparisons are in `reports/atlas-003-observations.md`.

| Fact | Value |
| --- | --- |
| Round | `atlas-003` |
| Freeze commit | `e75d18a` |
| Definitions commit named by the plan | `26bf891ddf064ee4b90097dadf343bb7672720a0` |
| Engine | `rrc-0.3.0` |
| Grammar | `opening-prohibit-multiply-v1` |
| Plan hash | `05de332578ff435f6e25eb2550db0a92ca576fdda187c99c8861fb9fdb77fc26` |
| Output | `relational-complexity/results/atlas-003/` |
| Report | `relational-complexity/reports/atlas-003.md` |
| Items | 13 |
| Complete | 13 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify --round atlas-003 --out results/atlas-003` printed `verified` before this record was written.

## How it ran

Two invocations, each with `--max-items 8` and `--budget-seconds 60`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 1.397 s | 5 |
| 2 | 5 | 0.909 s | 0 |

Every invocation exited 0. Completed items were not repeated.

## Omissions

N=4 and N=5 were not run. Incident predicates were not in the plan. Cardinalities 5 and 10 were not in the sample. Both-polarity prohibit pairs, count predicates, history, hyperedges, and composition were not in the plan. States inside a cell were not sampled. The 13 lists are not every list.

## What this commit is

This commit is the calculation record.
