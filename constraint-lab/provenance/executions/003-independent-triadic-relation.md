# Execution 003 — independent triadic relation

This is the execution record for prompt 003. It is not a review. The next external review is pending and is not written here.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 003 |
| path | `constraint-lab/provenance/prompts/003-v0.3-higher-order-relations.md` |
| sha256 | `9ac0de2c5d4cdd33749fec03a232f2d35fe5f6dbead9b0f572cafce4e23cbccb` |
| bytes | 25995 |
| date | 2026-10-03 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting branch | `research/constraint-lab-v0.2` |
| starting commit | `0170189f134002a3563768fbd62d7104d76757d0` |

The prompt file was not edited after it was stored. Prompts 001 and 002 remain `content_status: pending_verbatim_import`. Their wording was not reconstructed.

## Result

Branch `research/constraint-lab-v0.3`.

The inclusive commit range produced by the prompt, through the analysis commit, is:

```text
66624837de14772bdad4d65b7a8e98ce525a0d65
b100754accd3be0b21d2f55f5e72b5925b13e318
ca679de546a50ad75928101d43920b2cd50ba4e0
bc26b4a97cf60ee4eebe7174e5b0c9e3fad9f252
a8a81a36f0e42d143b74a1fd6ac6f6b2d17d61f6
```

The ledger line that points at this record is the close-out commit after `a8a81a36f0e42d143b74a1fd6ac6f6b2d17d61f6`. That close-out commit is not inside the range above, because a commit cannot contain its own hash.

Experiment ids:

- `generation-003-independent-triadic-relation`
- `generation-003b-k3-singletons`

Reports and notes:

- `constraint-lab/reports/generation-003-independent-triadic-relation.md`
- `constraint-lab/docs/simplicial-design.md`

## What ran

Generation 3A. Specification hash `26bc5fcafd9dd868171659f20f132bb27965e63c0bf26659414d42fd228ada17`. Eleven shards. Workers 2. Quarantined 0. Status COMPLETE. The completing resume recorded wall clock 162.102 seconds and shard-work 293.272 seconds. An opening invocation completed shard `9a6439ef6d1573d3b107d03d` and stopped. Its receipt SHA-256 stayed `2f20d5ec38faf042a6893a91a88b5a58ce797341ebc674be70596cb5b85b5f47` after resume. That opening wall clock was 4.237 seconds and is not inside the 162.102 second field. Summary SHA-256 `f90a84da22cdf9dc0d447ed08c75084b2023b9987033c92f3f2e0b14bb6bd9fe`. The summary's `git_commit` is `ca679de546a50ad75928101d43920b2cd50ba4e0`, which was HEAD while the shards ran. The published artifacts are in the following research commit.

7,385 canonical structurally-simple sets were analysed. Cardinality 1: 80. Cardinality 2: 7,305.

Generation 3B. Specification hash `3107a2f57cf8c56f8ca56cc40da8e451dfd9bd97407874305e3a7cc7c3f5da99`. One shard. Workers 2. Wall clock 8.204 seconds. Summary SHA-256 `7a925a1eeb28bfca6bb1934a69409f8e51c5ea439035f95fd0db1bfcc96cc526`. 180 canonical singletons at `K ≤ 3`.

`K ≤ 3` pairs were counted and not executed: 288,420 labelled combinations, 50,365 canonical structurally-simple sets. Triples were not walked: 72,874,120 labelled combinations. `N = 4` was not executed. Simplicial semantics were not executed.

## Divergences from the prompt

These are recorded here. The prompt was not rewritten to match them.

- Cross-order labels are stored as ASCII `P->P`, `P->T`, `T->P`, `T->T`, and `mixed`.
- The reducibility vocabulary adds `OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR` beside the four classes named in the prompt. The count in both experiments was 0. It is not a claim of absolute irreducibility outside the comparison domain.
- `FULLY_REDUCIBLE` means the two conditional pairwise jump kernels are the same kernel in the Generation 1b index, and the unnormalised triad weight does not depend on the pair configuration within a triad bit. That weight may still differ between triad absent and triad present. A fully reducible set can still have coarse-grained memory after the triad is hidden. The class is not called dynamical independence.
- `rho3 = 1/2` and `rho3 = 2` are recomputed inside the primary shards. They are not a second census. Shard identity records `rho3 = "1"` only.
- The screened dissolution shift is the conditional probability that the next pair event is a dissolution, compared with the occupied-pair baseline `m/3`. The free triadic toggle is not scored as a shift away from that baseline.
- Published summaries store counts and hashes. The Generation 3A family JSONL is about 12 MB and remains under gitignored `generated/`, above the 2 MB family-index limit. The kernel-id list is under that limit and is committed.
- Generation 3B executed only the `K ≤ 3` singletons. The engine's `K_max` re-includes the lower-`K` singletons, so the 180 sets are `K = 1` (20), `K = 2` (60), and `K = 3` (100).

## Continuous integration

The workflow file on this branch is `.github/workflows/ci.yml`. Push to `main` and to `research/**`, and pull requests, run two jobs: `constraint-lab` (pytest, then Generation 0 only) and `books` (`bash -n scripts/build-epubs.sh`, plus a presence check for the EPUB filter and sources).

`gh run view 37123342566` reports conclusion success, event push, branch `research/constraint-lab-v0.2`, head `0170189f134002a3563768fbd62d7104d76757d0`, title "research: record the occupation-threshold generation", URL https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/37123342566. An earlier successful run on the same branch is 37120773968. The external v0.2 review's statement that no run was visible is not the state `gh` reported on 2026-10-03.

This branch had not been pushed when this record was written, so there is no Actions run for `research/constraint-lab-v0.3`. That absence is not a claim that the workflow is broken. Before the provenance commit, `python -m pytest -q` in `constraint-lab` reported 40 passed in 6.33 seconds, and `bash -n scripts/build-epubs.sh` succeeded. This record does not invent a v0.3 Actions result.

## Review

`review_ids` for prompt 003 stays empty. A later ChatGPT reading should be a new file under `constraint-lab/provenance/reviews/` and a new ledger line. It should not be written into this record.
