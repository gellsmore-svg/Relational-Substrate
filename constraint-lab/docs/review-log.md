# Review log

Engine under review: `0.1.0` at `fd7758d0be29877b6a306455fd81ca3eca49df8b`.
Generation 1 summary: `experiments/manifests/generation-001-pregeometric-pairwise-summary.json`.
Both passes were made on that output. No measurement code was changed afterward, so there is no second numerical census. The comparisons below are against independent recomputation from the same commit, not against a retuned run.

## Pass 1 — correctness of the census

Checked, and held:

- Accounting partitions sum to the raw template count, and labelled constraints equal normal forms times 5, for every cell.
- Canonical counts plus symmetry removals equal the combination counts. `C(270,3) = 3,244,140` and `C(660,2) = 217,470` match the manifest.
- Canonical state counts are 2, 4, 11, 34 for `N = 2, 3, 4, 5`, the number of undirected graphs on that many vertices.
- Baseline entropy rates match `log2(M)`: 0, `log2(3)`, `log2(6)`, `log2(10)`. Baseline density is 1/2. Triangle mass is 1/8. The three perfect matchings at `N = 4` sum to 3/64. Period is 2. Total variation from uniform is 0 at `N ≤ 3` and numerical dust at `N ≥ 4`.
- The hand row for `form(0-1) | present(0-2) & present(1-2) => strong_favour` gives probability `2/3` of closing the matching wedge. The mean closing bias over the three wedges is `1/9`.
- `W3` and `W16` left every singleton modal map and every support map unchanged: 20, 120, 100, and 100 checks at `N = 2, 3, 4, 5`.
- Inside `W4`, `weak_*` and `strong_*` of one sign share a family id. `prohibit` does not.
- `N = 5` float64 residuals on the 50 singleton stationaries are at most `2.3e-15`. The iterative component search was required; the recursive one overflowed the stack on the 1,024-state hypercube. That fix is inside `fd7758d`, before this run.
- Replay of `exemplars/01fce7a65bc87c75.json` regenerated the stored event list.
- The `N = 2` canonical sets, 175 of them, partition into four families whose counts sum to 175.

Weakness found: at `N = 4` the cancelling pair that is exactly the baseline kernel reports a dissolution shift of one unit in the last place (`1.1e-16`), because the shift observable converts fractions to float and `m/6` is not dyadic. The exact flag `equivalent_to_baseline` is true and the shift on the `N = 3` cancel pair is `0`. This is a presentation error in one float column. It does not move a family, a tag, or a stationary comparison. Left as recorded. A fraction-valued shift would be a later tidy, not a new generation.

## Pass 2 — what the census is allowed to mean

Checked:

- Motif files carry the observed sentence. Their inference and speculation fields point at this report and do not contain a scientific claim.
- The predeclared 0.1 screens flag 79,731 of 80,155 families at `N = 3` and 3,942 of 4,018 at `N = 4`. The threshold was not edited after the run. The histograms are the discriminative record. The screen is a coarse flag and the report treats it as one.
- Family indexes of 108 MB (`N = 3`, `K ≤ 3`) and 4.9 MB (`N = 4`, `K ≤ 2`) stayed in `generated/` and out of git. Summaries, singleton tables, motif files, and exemplars were published. Regeneration of the large indexes is the Generation 1 command, about 170 seconds for the `N = 3` cell on this machine.
- The rise-then-release excess of the soft path-closing rule is exactly 0, while its stationary triangle mass moves from `1/8` to `11/64`. The path predicate and the stationary observable answer different questions. Both are reported. The predicate was not replaced after it failed to move.
- The largest rise-then-release excesses belong to hard prohibitions that trap the walk. That is written as an observation, not renamed as a discovery of constructive dissolution.

No tooling change followed this pass. The next generation can be chosen from these outputs.

## Earlier instrument changes, before the cited run

These are not a before/after on Generation 1. They landed in `fd7758d` and the census was run once, after them.

- Two-edge deadlocks contribute 0 to the closing bias, matching the definition in `docs/observables.md`.
- A family is screened from its shift and closing range, not from the exemplar alone. Rise excess remains exemplar-only, and the manifest says so.
- Strongly connected components are iterative. Period uses breadth-first levels.
- Family records stored for publication omit the repeated evaluation paragraph. The full index is committed only under 2 MB.
