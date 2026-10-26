# atlas-004 execution record

The cells were run after `plans/atlas-004.json` was frozen and pushed. The plan file was not edited. This record does not interpret the cells. Comparisons are in `reports/atlas-004-observations.md`.

| Fact | Value |
| --- | --- |
| Round | `atlas-004` |
| Freeze commit | `5181cc6` |
| Definitions commit named by the plan | `26bf891ddf064ee4b90097dadf343bb7672720a0` |
| Engine | `rrc-0.3.0` |
| Grammars | `opening-prohibit-multiply-v1`, `incident-neighbour-v1` |
| Plan hash | `f6a9680feb02700b5dd8aa9fe024dfe1668d51bdfcbc8aaf5c64607d6c8391fe` |
| Output | `relational-complexity/results/atlas-004/` |
| Report | `relational-complexity/reports/atlas-004.md` |
| Items | 18 |
| Complete | 18 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify --round atlas-004 --out results/atlas-004` printed `verified` before this record was written.

## How it ran

Three invocations, each with `--max-items 8` and `--budget-seconds 60`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 1.356 s | 10 |
| 2 | 8 | 1.357 s | 2 |
| 3 | 2 | 0.348 s | 0 |

Every invocation exited 0. Completed items were not repeated.

## Omissions

N=5 was not run. The complete carrier was not repeated. Factor sweeps, both-polarity prohibits, count predicates, history, hyperedges, and composition were not in the plan. States inside a cell were not sampled. The four carriers are not every graph on four nodes.

## What this commit is

This commit is the calculation record.
