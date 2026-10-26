# atlas-001 execution record

The cells were run after `plans/atlas-001.json` was frozen and pushed. The plan file was not edited. This record does not interpret the cells. Hash comparisons live in `atlas/equivalences.jsonl`, `atlas/patterns.jsonl`, and `reports/atlas-001-observations.md`.

| Fact | Value |
| --- | --- |
| Round | `atlas-001` |
| Freeze commit | `6286a63` |
| Definitions commit named by the plan | `c4e404a01f24d278659832103c6c53b8bd3f5bdb` |
| Engine | `rrc-0.2.0` |
| Grammar | `opening-prohibit-multiply-v1` |
| Plan hash | `646aa4fd2e3f45ac1dc4e1dbd11db5aff108da77e4818199cd5432b3c00bea7f` |
| Output | `relational-complexity/results/atlas-001/` |
| Report | `relational-complexity/reports/atlas-001.md` |
| Items | 24 |
| Complete | 24 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify --round atlas-001 --out results/atlas-001` printed `verified` with those counts before this record was written.

## How it ran

Three invocations, each with `--max-items 8` and `--budget-seconds 60`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 1.330 s | 16 |
| 2 | 8 | 1.365 s | 8 |
| 3 | 8 | 1.345 s | 0 |

Every invocation exited 0. Completed items were not repeated.

Each item has `status.json`, `result.json`, and `receipt.json`. The receipt stores the plan hash, the spec hash, and the sha256 of the result bytes. The manifest stores the same plan hash.

## Omissions

The batch is not every literal placement on three or four nodes. N=5, listed carriers, count predicates, history, independent hyperedges, and composition depth at least 1 were not run. No item was sampled.

## What this commit is

This commit is the calculation record.
