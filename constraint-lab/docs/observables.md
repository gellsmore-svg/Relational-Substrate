# Observables

Observables describe the kernel and the paths it assigns positive probability. The names below are structural.

## Light observables (every canonical set)

- Deadlock states: admissible set empty, halt completion in force.
- Recurrent classes and their periods.
- How many recurrent classes are reachable from the empty state.
- Maximum and mean absolute one-step change in dissolution probability relative to the baseline `m/M`, skipping deadlock states (a halt has no dissolution probability).
- Closing bias, only when `M = 3`. On each of the three states with exactly two edges present, measure the probability of forming the missing edge. The baseline value is `1/3`. The bias is the mean of those three probabilities, minus `1/3`. A two-edge deadlock contributes 0.
- Whether the support map equals the baseline support map. Strictly positive weights leave the full hypercube support. Only a zero factor removes an edge of that graph.
- Modal map: at each state, the toggles of maximal weight, ties kept, or `halt`. The modal family hash is the hash of that map. A combined family id also folds in the support hash, so two grammars that share a mode map and differ by a prohibition land in different families.

## Heavy observables

Computed for every singleton, and for the first-seen member of every family.

- Long-run occupancy from the empty state, mixed across reachable recurrent classes by absorption weights.
- Mean edge density, edge-count occupancy, mean number of connected components.
- Entropy rate, in nats and in bits.
- Total variation of the long-run occupancy from the uniform measure.
- Reversibility defect: the largest absolute imbalance of stationary flow across a single toggle and its reverse.
- Halt mass.
- For `N = 3`, mass on the complete triangle (state 7). The baseline value is `1/8`.
- For `N = 4`, mass on the three perfect matchings, states `33`, `18`, and `12` in lexicographic edge order (edges `01+23`, `02+13`, `03+12`). The baseline value is `3/64`.
- Rise-then-release probability, from the empty state, over horizon `T` (the specification field `rise_release_horizon`), only when the labelled state count is at most 64. A path matches when its edge-count sequence has indices `i < j < k` with `count[j] ≥ count[i] + 2` and `count[k] ≤ count[j] − 1`. The reported excess is this probability minus the same probability on the baseline. The baseline already has substantial mass on such paths, because the hypercube walk rises and falls.

At `m = 0` the baseline forms with probability 1. At `m = M` the baseline dissolves with probability 1. A density-dependent reweighting can separate from the baseline only at intermediate occupation, or by changing which intermediate states are reachable.

## Screens

The specification declares three thresholds before the run. They are flags, not discoveries. Generation 1 uses:

```text
max |dissolution shift|  ≥ 0.1
|closing bias|           ≥ 0.1
|rise-then-release excess| ≥ 0.05
```

A weak favour already moves some toggle probabilities by more than 0.1, so the shift screen is coarse. Reports quote the histogram of the shift, not only the count of families that cross the flag. The rise-excess screen uses the family exemplar. The shift and closing screens use the range across the whole family.

## Families

A family gathers canonical sets with the same `N`, the same modal map, and the same support map. Tags:

- `baseline-equivalent` — the successor list equals the baseline successor list;
- `structural` — the support is a proper subgraph of the hypercube;
- `measure` — full support, kernel not identical to the baseline;
- `screened` — a predeclared flag fired, and the family is not baseline-equivalent.

A family may carry both `structural` and `screened`, or both `measure` and `screened`.

## Trajectory observables stored on an exemplar

For each event: state before, candidates, baseline weight, matching constraint factors, resulting weight, normaliser, integer draw, selected toggle or halt, state after. The run id hashes the engine version, specification hash, constraint-set id, initial state, PRNG name, seed, and horizon.

## What is deliberately not an observable

No score named for construction, repair, sacrifice, inversion, or self-transformation is computed. Component count, matching mass, triangle mass, halt mass, and the rise-then-release excess are the quantities from which a later interpretation may or may not propose those names.
