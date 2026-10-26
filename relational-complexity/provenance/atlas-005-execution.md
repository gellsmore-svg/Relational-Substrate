# atlas-005 execution record

The cells were run after `plans/atlas-005.json` was frozen and pushed. The plan file was not edited. This record does not interpret the cells. Comparisons are in `reports/atlas-005-observations.md`.

| Fact | Value |
| --- | --- |
| Round | `atlas-005` |
| Freeze commit | `a29fbbd` |
| Definitions commit named by the plan | `26bf891ddf064ee4b90097dadf343bb7672720a0` |
| Engine | `rrc-0.3.0` |
| Grammar | `opening-prohibit-multiply-v1` |
| Plan hash | `2ab849ad8e43bd643685feea729533fcb3815d6f898a58aa19e236da57142f45` |
| Output | `relational-complexity/results/atlas-005/` |
| Report | `relational-complexity/reports/atlas-005.md` |
| Items | 12 |
| Complete | 12 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify --round atlas-005 --out results/atlas-005` printed `verified` before this record was written.

## How it ran

Two invocations, each with `--max-items 8` and `--budget-seconds 60`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 2.015 s | 4 |
| 2 | 4 | 1.655 s | 0 |

Every invocation exited 0. Completed items were not repeated.

## Omissions

Complete N=4 and complete N=5 were not run. Incident predicates, count predicates, history, hyperedges, and composition were not in the plan. Cardinality 10 was run on the 5-node chain only. States inside a cell were not sampled. The 12 lists are not every list.

## What this commit is

This commit is the calculation record.
