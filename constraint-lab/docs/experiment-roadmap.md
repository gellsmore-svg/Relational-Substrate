# Experiment roadmap

This document is the plan of record for which cells exist. Numerical findings belong in `reports/`. Nothing below is a result.

## Generation 0 — correctness

Specification: `experiments/specs/generation-000.json`.

```text
E(N=2, A≤2, O=2, G=0, S=0, H=0, K≤3, L=0, semantics=graph, W=W4)
  cardinalities {1, 2, 3}
E(N=3, A≤3, O=2, G=0, S=0, H=0, K≤2, L=0, semantics=graph, W=W4)
  cardinalities {1, 2}
```

Trajectory horizon 16, seeds `{0, 1}`. Rise-then-release horizon 4. Sensitivity alphabets `W3` and `W16`.

Unsearched in this generation: `N > 3`, the `N = 3` triple, `K > 2` at `N = 3`, hypergraph, simplicial, `G, S, H, L > 0`, `O > 2`.

CI runs this cell. It checks enumeration, normalisation, canonicalisation, the `N = 2` null-soft theorem, the hand-computed `N = 3` rows, replay, and the accounting identity.

## Generation 1 — first exhaustive grammar census

Specification: `experiments/specs/generation-001.json`.

```text
E(N=2, A≤2, O=2, G=0, S=0, H=0, K≤3, L=0, graph, W4)  cards {1,2,3}
E(N=3, A≤3, O=2, G=0, S=0, H=0, K≤3, L=0, graph, W4)  cards {1,2,3}
E(N=4, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, graph, W4)  cards {1,2}
E(N=5, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, graph, W4)  card  {1}
```

`N = 5` is included for singletons only. The state space has 1,024 points, which is inside float64 stationary analysis. Pairs at `N = 5` are unsearched. Triples at `N = 4` are unsearched: the labelled grammar at `K ≤ 2` has 660 constraints, and the triple combinations are a later decision, not a silent omission. The coverage manifest of the run states the exact combination counts.

Reference expressions are sanity checks inside the exhaustive grammar. They are not a search filter:

```text
form(0-2) | present(0-1) & present(1-2) => strong_favour
form(0-2) | present(0-1) & present(1-2) => strong_suppress
form(0-2) | present(0-1) & present(1-2) => prohibit
dissolve(0-1) | present(0-2) & present(1-2) => strong_favour
form(0-2) | present(0-1) => strong_suppress
form(0-2) | present(0-1) => strong_favour
```

Predeclared screens: dissolution shift `0.1`, closing bias `0.1`, rise-then-release excess `0.05`. These flags are not retuned after the census.

Also unsearched: `N > 5`, `K` above the per-cell bound, repeated copies of one constraint, hypergraph and simplicial semantics, `G, S, H, L > 0`, `O > 2`, non-multiplicative composition, and an additive implementation kept distinct from the multiplicative monoid.

## Generation 2 — candidates, not a commitment

The smallest justified next cell is chosen in the Generation 1 report, after the census. Candidates, in roughly increasing expressive cost:

1. A threshold literal (`count_at_least`) at `H = 0`, `N = 3`, so a constraint can see occupation without seeing history.
2. `H = 1` at `N = 3`, memory of the previous state, still pairwise and pre-geometric.
3. One irreducible triadic hyperrelation at `N = 3`, as its own semantics, compared with the pairwise graph on the same entities.
4. `N = 4` triples at `K ≤ 2`, only if the pair census shows the grammar is still changing with cardinality in a way a triple could resolve.
5. `N = 5` pairs, only with an explicit size calculation and a stated sampling rule if the canonical pair count is beyond an exact stationary solve.

Geometry (`G ≥ 1`) waits until a pre-geometric motif is stable enough that an embedding would be a real comparison rather than a new foundation.

## Generation 3 — one independent triadic relation

Specification: `experiments/specs/generation-003.json`.

```text
E(N=3, A≤3, O=3, G=0, S=0, H=0, K≤2, L=0, semantics=hypergraph, W=W4)
  cardinalities {1, 2}
```

The semantics are independent hypergraph. The triple is its own bit. This cell does not search simplicial face-closure, count predicates, `N = 4`, or cardinality 3. `rho3 = 1/2` and `rho3 = 2` are a sensitivity check inside the same shards. They are not a second census.

After that cell, one bounded extension was executed: `experiments/specs/generation-003b.json`, singletons at `K ≤ 3`. A constraint that reads both a pair and the triad has `K = 3`, so it is absent from the `K ≤ 2` grammar. The `K ≤ 3` pair combinations are 288,420 labelled and 50,365 canonical structurally-simple sets. The triple combinations are 72,874,120 labelled. Neither was executed. The reason is in the Generation 3 report. At the close of Generation 3, `N = 4` had not been executed.

## Generation 3c — two clocks on the Generation 3 kernels

Specification: `experiments/specs/generation-003c.json`. Analysis `memory-clock-reanalysis`. Same cell as Generation 3: `N = 3`, `O = 3`, `K ≤ 2`, cardinalities `{1, 2}`, independent hypergraph. This is a reanalysis. It does not replace Generation 3 or Generation 3b, and it does not edit their reports.

The two clocks are full-event-clock memory and pair-event-epoch memory. Alphabet sensitivity was not part of this reanalysis. `rho3 = 1/2` and `rho3 = 2` are recomputed inside the same shards for the clock statuses, the pair-jump boolean, and the triad-rate boolean.

## Generation 4 — N=4 singleton reconfiguration

Specification: `experiments/specs/generation-004.json`.

```text
E(N=4, A≤4, O=3, G=0, S=0, H=0, K≤2, L=0, semantics=hypergraph, W=W4)
  cardinality {1}
```

Independent hypergraph. Four triadic bits, not one, and not a popcount. `K ≤ 1` is the subset of this cell that cannot express a triadic condition on a pairwise action. Cardinality 2 was counted and not executed: 85,175 canonical structurally-simple pairs. The one-step same-edge-count flux ranking is part of the specification and stays in the record. Simplicial semantics stay in `docs/simplicial-design.md`.

The Generation 4 report recommends a later targeted cardinality-2 grid and does not execute it. `H`, `S`, `G`, and `L` stay 0.

## Later

History-dependent choreography, constraints that rewrite constraints (`L > 0`), geometric embeddings, and cross-substrate recurrence of a motif discovered here. A recurrence across substrates would be recorded as substrate-robust recurrence to the degree observed. It would not be called a proof of universality.
