# atlas-006 execution record

The cells were run after `plans/atlas-006.json` was frozen and pushed. The plan file was not edited. This record does not interpret the cells. Comparisons are in `reports/atlas-006-observations.md`.

| Fact | Value |
| --- | --- |
| Round | `atlas-006` |
| Freeze commit | `6e77689` |
| Definitions commit named by the plan | `ba8661b95da2863094438626d33b28a36d9072cb` |
| Engine | `rrc-0.4.0` |
| Grammar | `incident-count-v1` on the templates, `opening-prohibit-multiply-v1` on the bit instruments |
| Plan hash | `9b551e3e24afb1bdf21c243f52e6a08cb4d287880ce14553d92170cd2ee3cdcb` |
| Output | `relational-complexity/results/atlas-006/` |
| Report | `relational-complexity/reports/atlas-006.md` |
| Items | 15 |
| Complete | 15 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify --round atlas-006 --out results/atlas-006` printed `verified` before this record was written.

## How it ran

Two invocations, each with `--max-items 8` and `--budget-seconds 60`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 1.252 s | 7 |
| 2 | 7 | 1.154 s | 0 |

Every invocation exited 0. Completed items were not repeated.

## Omissions

`ge 1` and `eq 0` were not run. Other thresholds, prohibit counts, form and dissolve, and factors other than 3 were not run. Common-neighbour counts, history, hyperedges, and composition were not in the plan. Complete carriers were not run. States inside a cell were not sampled. The fifteen lists are the matched menu, not every count.

## What this commit is

This commit is the calculation record.
