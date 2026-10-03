# Execution 004 — memory clocks and N=4 reconfiguration

This is the execution record for prompt 004. It is not a review. Review 004 is pending and is not written here.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 004 |
| agent_input_path | `constraint-lab/provenance/prompts/004-v0.4-n4-higher-order-reconfiguration.md` |
| agent_input_sha256 | `f261527e522cc780f0937097b7de7706f7953f8bf69c59837442bbb7e1cf76ef` |
| agent_input_bytes | 32011 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship | `unknown` |
| date | 2026-10-03 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting branch | `research/constraint-lab-v0.3` |
| starting commit | `e04e0d4dcf979197b62d8d73fd747a0a2084c2b6` |

The stored file is the only representation available. It is the agent input. No separate authored Markdown file was found, so none was imported and none was reconstructed. The prompt file was not edited after it was stored.

Review 003, which this prompt required, is `constraint-lab/provenance/reviews/003-chatgpt-review-v0.3.md`. It is linked to prompt 003. It is not a review of the results below.

## Result

Branch `research/constraint-lab-v0.4`.

The inclusive commit range produced by the prompt, through the analysis commit, is:

```text
c7c5b6a870125a996044732ea18397954051dd87
90ad68fc0e55333335412dfa3af5c7081b60c918
e1db08ed6ecb53e69a9e558c27b2843c70e8ed14
f076f80612d8605eda9e7c04207e4c66d8e45dd6
aa0e6ea47b6ade629c2290cdefe030923ff87de1
```

The ledger line that points at this record is the close-out commit after `aa0e6ea47b6ade629c2290cdefe030923ff87de1`. That close-out commit is not inside the range above, because a commit cannot contain its own hash.

Experiment ids:

- `generation-003c-memory-clock-refinement`
- `generation-004-n4-higher-order-reconfiguration`

Reports:

- `constraint-lab/reports/generation-003c-memory-clock-refinement.md`
- `constraint-lab/reports/generation-004-n4-higher-order-reconfiguration.md`

Generation 3 and Generation 3b reports, specifications, and generated artifacts were not edited.

## What ran

Generation 3c. Specification hash `b3940305e0c8ed69e9a80faa39d98964893f52563a2f13645c8f338ee22e4020`. Eleven shards. Workers 2. Quarantined 0. Failed 0. The invocation that executed the shards ran for 129.27 seconds and stopped in the merge. The completing invocation merged the existing receipts in 0.210 seconds. Summary field `runtime_seconds` is 0.210. Shard-work is 248.268 seconds. Summary SHA-256 `37c2d96c698f73431ae80d09170eae1b3d84f6e9fbfdcd4f2bbd9b0fd2ae1630`. Row table SHA-256 `bb5a535b4291e53d07ead37c6a3016e63035c0e66141ffbfd9201ea13ee177a8`. 7,385 canonical sets. The summary `git_commit` is `90ad68fc0e55333335412dfa3af5c7081b60c918`, the plan-time commit.

Generation 4. Specification hash `d64a9cccc12ec4a58a886227a52ba3b2b35a9506978a521b3766835de8f4a7f9`. Nineteen shards. Shard items 100. Workers 2. Quarantined 0. Failed 0. Two coordinator invocations. Shard `011ccc9fe91e` finished at `2026-10-03T17:46:16Z` after 90.221 seconds. The remaining receipts finish from `2026-10-03T17:47:38Z` to `2026-10-03T17:49:36Z`. Summary field `runtime_seconds` is 217.686, the sum of the two coordinator walls on the resume path. Shard-work is 313.631 seconds, the sum of the 19 receipt elapsed times. Summary SHA-256 `6f941c19ae73ae0caf1157d6e4bdf7ccec2e775f9598e00db8e98765b110ea2a`. Row table SHA-256 `12ff748721ca076ba922c0c1330ed75ce291157771dcfc7b340378cc81bb4c49`. 160 canonical weighted singletons. The summary `git_commit` is `90ad68fc0e55333335412dfa3af5c7081b60c918`, the plan-time commit. The plan header was not rewritten after the analysis commit.

Cardinality 2 at `N = 4` was counted and not executed: 85,175 canonical structurally-simple pairs. The targeted grid recommended in the Generation 4 report was not started.

## Divergences from the prompt

These are recorded here. The prompt was not rewritten to match them.

- Cross-order labels are stored as ASCII `P->P`, `P->T`, `T->P`, `T->T`, and `mixed`.
- `K ≤ 1` is the subset of rows inside the Generation 4 census. It does not have a separate experiment id.
- At `N = 4` the stationary solve is float64. Residuals are stored. The numbers are not called exact. The unconstrained uniformity claim is the hypercube symmetry, stated separately from the float solve.
- The horizon-16 mean is a truncated lower bound on every Generation 4 row. Unresolved mass stays above `1e-8`, including on the baseline passage. No finite mean first-passage time is reported.
- The one-step same-edge-count flux ranking is zero on every analysed kernel because a pair event changes the edge count by one. The measure and the horizon were not changed after that result. The horizon-16 focused passage is reported as the predeclared multi-step observable, not as a replacement ranking.
- Axis E under `W3` and `W16` compares variant kernels with the `W4` Generation 1b catalogue. `outside` in that probe is an exact kernel-id mismatch. Support of positive toggle weights did not change.
- Sensitivity probes did not recompute the horizon-16 hit. Survival of that passage under `rho3` and under the alphabets is not claimed.
- Published summaries store the plan-time `git_commit`. They were not re-merged to insert the later analysis commit into that field.

## Local checks

Before the close-out commit, `python -m pytest -q` in `constraint-lab` reported 49 passed in 10.11 seconds. `bash -n scripts/build-epubs.sh` succeeded. These checks do not include the Generation 3, Generation 3c, or Generation 4 censuses. CI runs Generation 0 only.

## Continuous integration

This branch had not been pushed when this record was written, so there is no Actions run for `research/constraint-lab-v0.4`. That absence is not a claim that the workflow is broken. A later ledger line may record a run id after a push. This record does not invent one.

The workflow file on this branch is `.github/workflows/ci.yml`. Push to `main` and to `research/**`, and pull requests, run two jobs: `constraint-lab` (pytest, then Generation 0 only) and `books` (`bash -n scripts/build-epubs.sh`, plus a presence check for the EPUB filter and sources).

Review 003 records `gh run view 37131636102` as conclusion success on `research/constraint-lab-v0.3` at `e04e0d4dcf979197b62d8d73fd747a0a2084c2b6`. That run is not a run of this branch.

## Review

`review_ids` for prompt 004 stays empty. A later external reading should be a new file under `constraint-lab/provenance/reviews/` and a new ledger line. It should not be written into this record.
