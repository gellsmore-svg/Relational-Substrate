# Generation 002 — occupation-threshold predicates

Engine `0.2.0`, semantic version `0.2.0`, normalisation `structural-unique-v1`, grammar `pairwise-count-v1`.
Census commit `112b6b11d0f5b901a755b6ba5c9e740032006536`.
Specification hash `04c477360e7227f9af4ea26fe86530b148f8407ad6983d48e75cee8941659a8a`.
Python 3.12.3, NumPy 2.5.3, platform `linux`.
Wall clock 13.169 seconds. Shard-work sum 20.220 seconds. Workers 2. Shards 18.
Summary SHA-256 `69be84acd3390405c3100f9b2ed2d35deb545752d26363e943301a9be426d4ab`.
Comparison index: Generation 1b, `generated/generation-001b-structurally-normalised`.

The cited run is the uninterrupted directory `generated/generation-002-occupation-threshold`. An earlier invocation was stopped after four shards and resumed. Its scientific projection matches this one. The record of that stop is `docs/execution-resilience.md`.

## A. Grammar

Graph semantics. `N = 3`, `G = S = H = L = 0`, `O = 2`, `K ≤ 2`, `A ≤ 3`, alphabet `W4`, cardinalities `{1, 2}`. Composition `structural-simple`. Analysis is heavy on every canonical simple set, with exact rational stationary values.

A count literal reads the number of present pairwise edges in the whole state (`state.bit_count()`). It is not scoped to a subset of edges, it is not a rise in `O`, and it is not a hyperedge. The forms are `count>=q`, `count<=q`, and `count==q`. At most one count literal per constraint. `K` is 1 plus the number of edge conditions plus the number of count literals. A count literal adds no entities to the arity.

Edge constraints are generated first, so the edge-only grammar order is unchanged. Count constraints follow.

Logical redundancies are excluded from the grammar and still accepted by the parser:

- `count>=0` and `count<=M` are tautologies. `M = 3`.
- A threshold outside `0..M` is unsatisfiable.
- `form` already implies the edge is absent, so the occupied count is at most `M−1`. `form | count>=M` and `form | count==M` are unsatisfiable. `form | count<=M−1` is a tautology.
- `dissolve` already implies the count is at least 1. `dissolve | count<=0` and `dissolve | count==0` are unsatisfiable. `dissolve | count>=1` is a tautology.
- `count==q` is not the same constraint as one inequality. Under multiplicative composition, `count>=q` and `count<=q` together apply the weight twice on the states where both match. `count==q` applies it once.

At this cell the accounting is:

| Piece | Count |
| --- | ---: |
| Edge structural normal forms (`K ≤ 2`) | 30 |
| Edge labelled | 150 |
| Count candidates before redundancy | 72 |
| Count tautologies | 18 |
| Count unsatisfiable | 12 |
| Count structural | 42 |
| Structural identities in the grammar | 72 |
| Labelled constraints | 360 |

`42 + 18 + 12 = 72`. Labelled constraints are `72 × 5 = 360`.

| Card | Labelled | Simple labelled | Stacked labelled | Canonical simple | Stacked canonical | Removed by symmetry |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 360 | 360 | 0 | 100 | 0 | 260 |
| 2 | 64,620 | 63,900 | 720 | 12,220 | 200 | 52,200 |

`C(360, 2) = 64,620`. `C(72, 2) × 25 = 63,900`. Coverage holds: `100 + 260 = 360` and `12,220 + 52,200 + 200 = 64,620`. The plan's symmetry estimate `simple / 3!` was 60 for cardinality 1. The census count is 100. Stabilizers make the estimate low, and the plan labels it as an estimate.

Cardinality 3 was not run.

## B. What the cell contains

Qualitative families 2,501. Exact kernels 7,559. Observable signatures 7,408. Structural families 1,438. Screened families 2,464. Baseline-equivalent families 1. Every family is period 2. Deadlocks 0. Support matches the baseline in 1,063 families. Families with more than one exact kernel: 2,158 of 2,501. The widest has 59 kernels and 109 sets; the lex-smallest member is the singleton `dissolve(0-1) => strong_favour`.

Sensitivity on the 100 canonical singletons, two alphabets: 200 checks, modal unchanged 200, support unchanged 200.

The baseline family has 16 members and one kernel. All 16 are genuine global cancellations, and the shard results stored every example. Each pair is two count literals on one action whose grades are reciprocal, so the product is 1 on every state the action can match. The lex-smallest is `dissolve(0-1) | count<=1 => strong_favour` with `dissolve(0-1) | count==1 => strong_suppress`. The same pattern occurs for weak grades, for `count==3` against `count>=3` on a dissolve, and for `count<=0` against `count==0` and `count==2` against `count>=2` on a form. No singleton in the cell is the baseline. Local cancellations: 224. The example list is capped.

Reference rows, all in the grammar, none equal to the baseline as a singleton. Each kernel id is present in the Generation 1b kernel index, and each qualitative id is present in the Generation 1b qualitative index.

| Expression | Density | Triangle | Kernel relative to Generation 1b |
| --- | --- | --- | --- |
| `form(0-1) \| count>=2 => strong_favour` | `13/24` | `11/64` | same kernel as the three-literal wedge `form(0-1) \| present(0-2) & present(1-2) => strong_favour` |
| `form(0-1) \| count>=1 => strong_favour` | `91/162` | `23/135` | an existing Generation 1b kernel |
| `dissolve(0-1) \| count>=2 => strong_favour` | `379/810` | `4/45` | an existing Generation 1b kernel |

At `N = 3`, `form(AB) | count>=2` matches only the state in which the other two edges are present. That is the wedge. The compact count literal and the named incidence condition are the same kernel.

## C. New behavioural territory

The comparison is over canonical sets that contain a count literal. There are 10,430 such sets. The classes overlap. The partition of those sets is the first three rows.

| Class | Sets | Distinct ids |
| --- | ---: | ---: |
| Kernel already in Generation 1b | 9,776 | — |
| New kernel, qualitative family already in Generation 1b | 200 | — |
| New qualitative family | 454 | 189 families |
| New exact kernel (the last two rows) | 654 | 654 kernels |
| New observable signature | 639 | 639 signatures |
| Kernel id present while its qualitative id is absent | 0 | — |

`9,776 + 654 = 10,430`. `200 + 454 = 654`. Of the 654 new kernels, 15 share an observable signature that Generation 1b already had. A larger syntax is mostly an existing kernel: 9,776 of 10,430 count-sets reproduce one.

The 189 new qualitative families split by whether the support id and the modal id themselves occur anywhere in Generation 1b:

| Support id in Generation 1b | Modal id in Generation 1b | Families |
| --- | --- | ---: |
| yes | yes, but not this pair | 50 |
| yes | no | 109 |
| no | yes | 12 |
| no | no | 18 |

Every new qualitative set is cardinality 2. No cardinality-1 count constraint opens a qualitative family outside Generation 1b.

### New supports

Thirty canonical sets have a support family that does not occur in Generation 1b, including its cardinality-3, `K ≤ 3` edge census. They are thirty families, thirty kernels, all period 2, no deadlock, none baseline, all tagged structural. Every constraint in them is a prohibit. Soft grades did not open a support outside Generation 1b.

The thirty are pairs of count-gated prohibitions:

- two dissolve-prohibits on two edges, with `count<=2`, `count==2`, or `count>=2`;
- a dissolve-prohibit on one edge and a form-prohibit on the same edge or another, gated by a count;
- two form-prohibits on two edges, gated by `count<=1`, `count==1`, or `count>=1`.

The lex-smallest is `dissolve(0-1) | count<=2 => prohibit` with `dissolve(0-2) | count<=2 => prohibit`. These supports are the new transition structures in this cell. The other 159 new qualitative families reweight a support Generation 1b already had, or pair an existing support token with an existing modal token in a combination Generation 1b did not.

## D. Constructive dissolution

The stored flag `post_release_new_edge` is true for 2,045 of the 10,430 count-sets. The flag means a count literal favours a dissolve, the dissolve has positive probability, and some later reachable state carries an edge the pre-dissolve state lacked. It is not a screen and it is not a finding of constructive dissolution. Isomorphic reconnection sets it. So does deleting the last edge and then forming some other edge under the baseline support.

At `N = 3` the isomorphism type of a simple graph is its edge count. A high-occupation dissolve (`count>=2` or `count==2`, factor greater than 1, probability above the baseline `1/3`) was inspected on the stored motifs. 824 canonical sets have such a witness on a state with at least two edges. From a two-edge state the dissolve lands on a one-edge state. The next toggle either restores a two-edge graph, which is the same isomorphism type, sometimes under a different labelling, or deletes the remaining edge. The triangle is a further formation away. It is reachable after the release in 820 of the 824 sets, because the support still allows the formations the baseline allows. In the other four the walk is confined to a sparser graph. That is loss of edges.

A two-step walk that follows a maximum-probability successor does not land on the triangle for these witnesses. Most of those maxima are ties, so there is not a unique modal continuation. The paths that do introduce a new edge at the first step after release land on another two-edge graph.

The minimum grammar that merely sets the flag is the singleton `dissolve(0-1) | count<=1 => strong_favour`. It favours dissolving the last edge. From the empty state the chain can form any edge, including one the original state lacked, and can reach a two-edge graph or the triangle. That is regrowth after clearing a single edge. The support is the full hypercube. The same flag is true under `W3` and `W16` for all 2,045 sets: a positive grade stays above 1 and prohibit stays 0 on every base in `{2, 3, 4}`, so the support question does not depend on the base.

No grammar in the searched cell shows the sequence the question asked for: an organised state, a high-occupation increase in dissolution, then a later organisation that is not an isomorphic reconnection and not mere loss. A hard oscillation is present and is not that sequence. `dissolve(0-1) => prohibit` with `dissolve(0-2) => prohibit` has entropy 0, period 2, and no deadlock: the wedge `{0-1, 0-2}` moves to the triangle with probability 1, and the triangle moves back by dissolving `1-2` with probability 1. The kernel id is already in Generation 1b. It is a deterministic toggle of one edge.

## E. Other exact values in this cell

These extremes include edge-only pairs. They are not all caused by a count literal.

| Observable | Value | Lex-smallest grammar |
| --- | --- | --- |
| Closing bias max | `1/3` | two dissolve-prohibits |
| Closing bias min | `−2/9` | `dissolve(0-1) => strong_favour`, `form(0-1) => prohibit` |
| Rise excess max | `5/18` | `dissolve(0-1) => prohibit`, `form(0-1) => strong_favour` |
| Rise excess min | `−2/3` | two form-prohibits |
| Shift max | `2/3` | two dissolve-prohibits |
| Entropy max | `log2(3)` | the baseline count pair in section B |
| Entropy min | 0 | the deterministic wedge/triangle cycle in section D |

The rise-excess maximum of Generation 1b is `1/3` and needs a cardinality-3 edge grammar. This cell stops at cardinality 2, and its maximum is `5/18`.

Family-maximum quantiles. Closing: `−0.2222`, `−0.04444`, 0, `0.07407`, `0.1111`, `0.2481`, `1/3`. Rise excess: `−2/3`, `−0.09259`, 0, `0.07407`, `0.1111`, `0.2222`, `5/18`. Shift: 0, `1/6`, `1/3`, `1/3`, `1/3`, `2/3`, `2/3`.

## F. What was not searched

Cardinality 3. Any `N` other than 3. `K > 2`. Stacked-weight composition. A count scoped to a subset of edges. Hypergraph or simplicial semantics. Positive `G`, `S`, `H`, `L`, or `O` above 2.

## Commands

```bash
.venv/bin/python -m rs_constraint_lab plan experiments/specs/generation-002.json
.venv/bin/python -m rs_constraint_lab run experiments/specs/generation-002.json \
  --out generated/generation-002-occupation-threshold --workers 2 \
  --compare-to generated/generation-001b-structurally-normalised --publish .
.venv/bin/python -m rs_constraint_lab verify generated/generation-002-occupation-threshold
```
