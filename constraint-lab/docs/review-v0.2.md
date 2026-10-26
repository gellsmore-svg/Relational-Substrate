# Review v0.2

Engine `0.2.0`, semantic version `0.2.0`. Generation 1b summary `experiments/manifests/generation-001b-structurally-normalised-summary.json`. Generation 2 summary `experiments/manifests/generation-002-occupation-threshold-summary.json`. Both censuses had already finished when this review was written. No kernel, census membership, family identity, or exact observable changed, so neither census was rerun. There is no scalar score.

## Execution robustness

The shard runner completed Generation 1b (883 shards, 0 quarantined, coverage identity held) and Generation 2 (18 shards, 0 quarantined). The Generation 2 stop after four shards, the unchanged receipts, and the equal scientific projection are in `docs/execution-resilience.md`.

One recording bug showed up while the manifests were being checked. `merge_directory` published `runtime_seconds` from its own assembly stopwatch, about 0.003 seconds, and `run_spec` then wrote the real coordinator wall clock only into `generated/.../summary.json`. The published manifests were corrected from those generated summaries: 1117.1 seconds and 13.169 seconds. The repair publishes after that clock is set, and a later merge keeps the stored value. `tests/test_resilience.py` covers the publish and the later merge. Shard-work sums were already right. The science block does not include the clock.

`stationary_residual` on the rational path is a stored `0.0`, not a measured residual. The count-template tautology bucket can be inflated when `K ≥ 3` and a count literal is combined with several edge-condition subsets. Generation 1b does not use count literals. Generation 2 uses `K ≤ 2`, where the bucket sums to the candidate count (`42 + 18 + 12 = 72`). Neither was treated as a census error.

## Grammar correctness

Structural identity excludes the weight. The primary census drops a second grade on that identity. The edge-grammar order is unchanged, and the edge pair used by the older tests is stable. `A_max` filters the grammar. Declared axes outside the implemented values are refused. Count literals are appended after the edge grammar. The Generation 2 size, 360 labelled constraints and 64,620 pairs, matches the closed form `C(72, 2) × 25 = 63,900` simple pairs plus 720 stacked pairs.

`form(0-1) | count>=2 => strong_favour` has the same kernel id as the Generation 1b wedge `form(0-1) | present(0-2) & present(1-2) => strong_favour`. That is the expected collapse at `N = 3`: the only two-edge state in which edge `0-1` is absent is the state where the other two edges are present.

## Combinatorial coverage

Generation 1b's `canonical_including_stacked` equals the committed Generation 1 canonical count in every cell: 10/45/120, 60/6,330/544,550, 50/9,845, and 50. Analysed + stacked canonical + removed by symmetry equals the labelled combination count in every cardinality of both generations. Generation 2 cardinality 3 was not run. The symmetry estimate `simple / N!` is labelled as an estimate; at `N = 3` cardinality 1 it said 60 and the census found 100.

## Exact-arithmetic correctness

On `N ≤ 3` the stationary distribution, absorption, edge density, triangle mass, dissolution shift, closing bias, and rise-then-release probability are stored as exact fractions. The wedge fractions `13/24` and `11/64` recur in Generation 2's count form of that rule. Entropy is a float. At `N = 4` the shift maximum is the fraction `25/42` rather than the Generation 1 float near `0.595`. The `N = 4` stationary distribution itself remains float64, because the state space has 64 states. The one-ulp shift on the Generation 1 reciprocal pair is absent here because that pair is stacked and is not analysed.

## Symmetry and canonicalisation

Exact kernels, support tokens, and modal tokens are reduced under `S_N` before they are hashed. The Generation 1 16-hex family id is a different object and is not compared as a string. Relabelled copies of the reference wedge share the canonical expression `form(0-1) | present(0-2) & present(1-2) => strong_favour`. Count literals are invariant under relabeling. The forty genuine global cancellations at `N = 3` were stored in full and four of them, including mixed form/dissolve triples, were rebuilt and matched the baseline successor table.

## Family definitions

Support family, modal family, qualitative family, exact-kernel family, and observable signature are separate ids. At `N = 3`, 391,991 kernels sit in 61,929 qualitative families and 379,177 signatures. An exact-kernel match implies the qualitative family and the signature at this `N`. The converse is false. At `N = 5`, twenty families contain two kernels and the signature count equals the family count, so a strong grade and a weak grade of one pattern can share a signature while their entropy differs. Entropy is not in the signature, by the definition that logarithmic quantities are not rational.

Within-family ranges are part of the family record. The widest `N = 3` qualitative family contains 1,042 kernels. Reading only the lex-smallest member would hide that span.

## Observable adequacy

The predeclared screens flag almost every family in both large cells. They are the Generation 1 thresholds and were not refit. The histograms and the exact endpoints are the discriminative record. Rise-then-release and stationary triangle mass still answer different questions: the wedge moves triangle mass from `1/8` to `11/64` and leaves the short-path excess at 0. The observable signature's omission of entropy is visible at `N = 5`, where two kernels in one family differ by about 0.026 bits and share a signature.

## Interpretive leakage

The flag `post_release_new_edge` counts 2,045 Generation 2 sets. The report does not call that constructive dissolution. At `N = 3` the flag is compatible with isomorphic reconnection and with regrowth after deleting a single edge. The inspection against the stated sequence is in the Generation 2 report, and the result is negative.

The word "screened" is a threshold flag, not a class of phenomena. Baseline-equivalent sets are reported separately from local reciprocal products, and local products are reported separately from genuine global cancellation. Generation 1's reciprocal pair is described as a stacked grade, not as two constraints.

## New behavioural territory

Of 10,430 canonical sets that contain a count literal, 9,776 reproduce a Generation 1b kernel. The new kernels are 654 sets, 654 distinct kernels, in 189 qualitative families. Thirty of those families have a support that the Generation 1b edge census does not contain. All thirty are pairs of count-gated prohibitions. Soft occupation weights did not add a support. No cardinality-1 count constraint added a qualitative family.

## Global-coherence relevance

The laboratory still has no certificate of a designed runtime. What this version adds is a separation between a structural rule and a stacked grade, and a first predicate that reads the occupation of the whole pairwise state. The supports that predicate adds, inside this cell, are hard truncations. They do not exhibit organisation, high-occupation release, and a later non-isomorphic organisation. That is an observation about this grammar, not a claim about global coherence.
