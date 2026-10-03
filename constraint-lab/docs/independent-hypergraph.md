# Independent hypergraph

Generation 3 adds one relation and does not add a place, a clock, or an entity-state channel.

## Slots

At `N = 3` the entities are `A`, `B`, and `C`, stored as `0`, `1`, and `2`. The four independent bits are:

```text
bit 0    AB     (0, 1)
bit 1    AC     (0, 2)
bit 2    BC     (1, 2)
bit 3    ABC    (0, 1, 2)
```

`ABC` present does not imply `AB`, `AC`, or `BC`. `AB ∧ AC ∧ BC` does not imply `ABC`. The labelled state space is the 4-dimensional Boolean hypercube: 16 states, four toggles from every non-halting state.

`S_3` fixes the triple and permutes the three pairs. The coarse classes are the pairwise isomorphism type crossed with the triadic bit. At `N = 3` the pairwise isomorphism type is the pair-edge count, so there are eight classes: empty, one pair, wedge, and triangle, each with the triad absent and present. States are not grouped by the total number of present relations. Empty pairs plus the triad is not the same class as one pair and no triad.

## Axes

Relation order `O` is the maximum cardinality of an independently existing relation. Generation 3 has `O = 3`.

Constraint arity `A` is the number of distinct entities named by the constraint. `form(0-1-2)` has `A = 3` with no other condition.

Geometric dimension stays `G = 0`. There is no embedding.

State-space dimension `S` keeps its existing meaning: finite channels other than the binary incidence of a named relation. The triadic bit is relational incidence. It is not counted in `S`. Generation 3 has `S = 0`, `H = 0`, and `L = 0`.

## Baseline

The primary baseline gives every slot toggle weight 1, including the triad. Formation and dissolution are symmetric. `rho3` is the relative baseline weight of the triadic toggle. The primary census uses `rho3 = 1`. The values `1/2` and `2` are a sensitivity check inside the same shards, not a second census.

## Grammar

Conditions may read a pair present or absent, or the triad present or absent. Count literals are refused in this grammar so they cannot treat the triad bit as another pair. The cross-order class of a constraint is `P->P`, `P->T`, `T->P`, `T->T`, or `mixed`.

## Comparison with the pairwise grammar

An edge-only rule on this kernel is not the Generation 1b kernel. The triad toggle is a fourth event. The comparison is the pairwise conditional jump kernel: at each triad bit, renormalise the three pair weights. Under `rho3 = 1`, an edge-only rule's two jump kernels equal the Generation 1b kernel of the same edge grammar.

Reducibility is stated only inside the Generation 1b `N = 3`, `K ≤ 3`, cardinalities `{1, 2, 3}`, structural-simple, pairwise-edge index, plus the unconstrained pairwise baseline. A miss against that index is `OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR`, not a claim of absolute irreducibility.

## What this file does not decide

Simplicial face-closure is a different semantics. It is not executed here. Whether forming a 2-simplex creates absent faces, whether formation is prohibited until the faces exist, whether deleting a face deletes the simplex, and whether simplex dissolution is independent of face dissolution are questions for a later design note. None of those rules is compiled into these 16 states.
