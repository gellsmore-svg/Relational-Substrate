# atlas-002 execution record

The cells were run after `plans/atlas-002.json` was frozen and pushed. The plan file was not edited. This record does not interpret the cells. Comparisons are in `reports/atlas-002-observations.md`.

| Fact | Value |
| --- | --- |
| Round | `atlas-002` |
| Freeze commit | `c3d316d` |
| Definitions commit named by the plan | `c4e404a01f24d278659832103c6c53b8bd3f5bdb` |
| Engine | `rrc-0.2.0` |
| Grammar | `opening-prohibit-multiply-v1` |
| Plan hash | `937573af07c6d5b40e43802b4f32bac76b32c66eefbca7a68aaab8d15a8bb26e` |
| Output | `relational-complexity/results/atlas-002/` |
| Report | `relational-complexity/reports/atlas-002.md` |
| Items | 16 |
| Complete | 16 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify --round atlas-002 --out results/atlas-002` printed `verified` before this record was written.

## How it ran

Two invocations, each with `--max-items 8` and `--budget-seconds 60`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 1.314 s | 8 |
| 2 | 8 | 1.336 s | 0 |

Every invocation exited 0. Completed items were not repeated.

## Omissions

N=5 carriers were not run. The complete carrier was not repeated. Both-polarity prohibits, duplicate text, count predicates, history, hyperedges, and composition were not in the plan. Nothing was sampled.

## What this commit is

This commit is the calculation record.
