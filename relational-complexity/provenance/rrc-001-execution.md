# RRC-001 execution record

The cells were run after the plan was frozen and pushed. The plan file was not edited.

| Fact | Value |
| --- | --- |
| Round | `rrc-001` |
| Freeze commit | `92ae7425e8b711ba8b24c7905c0208eeea129d33` |
| Definitions commit named by the plan | `2053b8bddc94b3a9b1d5db712f4c91c6518a681b` |
| Engine | `rrc-0.1.0` |
| Plan hash | `172ff5ce99e0fca96ce3c5cb94e6fc1d9518f0352007740a174935488fe95382` |
| Output | `relational-complexity/results/rrc-001/` |
| Atlas | `relational-complexity/reports/rrc-001-atlas.md` |
| Items | 29 |
| Complete | 29 |
| Failed, timeout, unresolved, invalid, pending | 0 |

`verify` printed `verified` with those counts before this record was written.

## How it ran

Five bounded invocations, each with `--max-items 8` and `--budget-seconds 160`:

| Invocation | Newly completed | Wall clock | Pending after |
| --- | --- | --- | --- |
| 1 | 8 | 0.93 s | 21 |
| 2 | 8 | 13.15 s | 13 |
| 3 | 8 | 50.35 s | 5 |
| 4 | 5 | 4.10 s | 0 |
| 5 | 0 | 0.005 s | 0 |

Every invocation exited 0. The fifth invocation found nothing left to run. Completed items were not repeated.

Each item has `status.json`, `result.json`, and `receipt.json`. The receipt stores the plan hash, the spec hash, and the sha256 of the result bytes. The manifest stores the same plan hash.

## What this commit is

This commit is the calculation record. It does not interpret the cells. `generated/preflight.json` remains untracked disposable timing output and is not part of the result.
