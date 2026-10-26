# Formalism

## Substrate of Generation 1

`N` labelled entities. Undirected pairwise relations. Each relation is present or absent. There is no coordinate, distance, or metric (`G = 0`). The state is the bitset of present edges, in lexicographic edge order `(i, j)` with `i < j`.

```text
M = N(N-1)/2
labelled states = 2^M
```

| N | M | labelled states |
| --- | --- | --- |
| 2 | 1 | 2 |
| 3 | 3 | 8 |
| 4 | 6 | 64 |
| 5 | 10 | 1,024 |
| 6 | 15 | 32,768 |
| 7 | 21 | 2,097,152 |

A primitive event toggles one edge. Formation and dissolution are the two directions of the same toggle.

## Baseline kernel

The unconstrained weight of every toggle is 1. From a state with no deadlock the kernel is uniform on the `M` toggles:

```text
μ₀(τ | S) = 1/M
```

This is the simple random walk on the `M`-dimensional hypercube. It is irreducible. Every toggle changes the parity of the number of present edges, so the chain has period 2. The transition matrix is doubly stochastic, and the unique stationary distribution is the uniform distribution on the `2^M` states. A point mass does not converge to that distribution in total variation, because the two parity classes alternate. The Cesàro averages, and the ensemble started from the stationary distribution, are the equilibrium objects used in the reports.

The entropy rate of the baseline is `log2(M)` bits per step. At `N = 2`, `M = 1`, the walk is a deterministic flip and the entropy rate is 0.

The baseline is symmetric between formation and dissolution. It is not a degree-preserving rewiring, and it does not prefer construction.

## Constraint as reweighting

For a finite set `C` of constraints, the constrained kernel is

```text
μ(τ | S, C)  ∝  μ₀(τ | S)  ×  Π_i w_i(τ, S)
```

with the usual normalisation on each state. Because `μ₀` is constant on the toggles, this is the normalisation of the product of the constraint factors. History `H_t` is part of the conceptual formula. Generation 1 has `H = 0`, so no constraint reads a previous state.

### Why multiplication

Several representations were considered.

- Multiplicative weights. The identity element is 1. Independent constraints compose by multiplication. A hard exclusion is the multiplicative zero.
- Additive log-weights. For strictly positive weights this is the same monoid, written additively, and the normalised kernel is a softmax. The implementation stores the multiplicative form. An additive implementation that agreed on every positive weight would define the same kernel.
- Transition rates in continuous time. Equivalent for the embedded jump chain when every state has the same baseline rate. Continuous time is a later representational choice, not a Generation 1 primitive.
- Hard admissibility predicates. These are the special case `weight = 0`.
- Categorical or rewrite presentations. Left available for a later semantics. Generation 1 does not need them, because the state space is the hypercube and the event is a single toggle.

Multiplication is the primitive. The words permit, suppress, exclude, favour, require, and invert are descriptive. In this generation they are not a second effect algebra. `prohibit` is weight 0. Every other declared name is a positive factor.

### Weight alphabet

Grades are the integers `{-2, -1, 0, +1, +2}`. `prohibit` has no grade; its factor is 0. Neutral has grade 0 and factor 1. Neutral is the identity, so it is not enumerated: a grammar that included it would rediscover the baseline under a longer name.

The primary alphabet `W4` uses base `r = 2`:

```text
prohibit         0
strong_suppress  1/4
weak_suppress    1/2
neutral          1
weak_favour      2
strong_favour    4
```

`W3` uses base 3 (`1/9, 1/3, 3, 9`) and `W16` uses base 4 (`1/16, 1/4, 4, 16`), on the same grades. For a fixed grade assignment and any `r > 1`, the argmax toggle set at each state is independent of `r`. Ties are kept. The support of the kernel depends only on which factors are zero. Numerical probabilities are not invariant. The sign of a probability difference from the baseline is not invariant once several constraints compete and the row is normalised. Sensitivity checks therefore report modal identity and support identity, and they report magnitudes separately.

Dyadic `W4` is primary because it is the smallest integer base greater than 1, the factors are binary, and the two soft grades are visibly distinct from the identity.

### Halt

If every toggle weight on a state is 0, the admissible set is empty. The engine does not invent a relational self-loop. For communicating-class and stationary analysis the Markov completion adds a self-loop of probability 1, flagged `self_loop_marked_kernel_undefined`. That loop is a halt. It is not counted as a relational event, and a singleton halt class has period 1. Moving recurrent classes of the toggle chain have period 2 while every admissible event is a real toggle.

A single `form(e) => prohibit` deadlocks the states in which `e` is the only missing edge that the constraint can see; it does not by itself deadlock the empty state unless `M = 1`. Forbidding every formation requires one prohibit per edge.

### Memoryless composition

At `H = 0` and `L = 0` the active set is the whole constraint set in every state. Constraints that do not match the current incidence contribute the empty product, factor 1. Repeated copies of one constraint are not searched. Repetition would rescale a grade and is recorded as an unsearched region. Distinct weight names are distinct constraints.

## Canonical labelling

Two labelled objects that differ by a permutation of the entity names are one class. For `N ≤ 5` the laboratory enumerates `S_N` exactly and stores the edge-index image of every permutation. A constraint id-tuple is canonical when it equals the lexicographically least sorted image of itself under those permutations. Nauty, Traces, and graph-library canonical labelling are deferred. `|S_5| = 120`, which is small enough that the exact tables are easier to test than a general graph-isomorphism library.

The canonical representative is the least id tuple. It is a valid normal-form expression. It is not claimed to be the lexicographically least expression string.

A constraint-set id is

```text
sha256(alphabet name, newline, expressions in sorted order)[:16]
```

The engine version is stored beside the id and is not mixed into it. A replay run id does include the engine version, so a trajectory name changes when the engine changes.

## Exact analysis

For every kernel that receives a heavy analysis the engine builds the transition graph, finds strongly connected components (Tarjan), marks recurrent classes, computes the period as the gcd of return levels (a singleton class has period 1), solves the stationary distribution on each recurrent class, and mixes those distributions by the absorption probabilities from a declared start state (the empty state, unless a report says otherwise).

State spaces of size at most 16 use rational Gaussian elimination. Larger spaces use a float64 solve and record the residual `‖πP − π‖_∞`. If the solve fails, the residual exceeds `1e-8`, or a component is negative beyond that tolerance, the engine falls back to a Cesàro average and labels the method `cesaro`.

Also recorded, where defined: entropy rate, total-variation distance of the long-run occupancy from the uniform distribution, a reversibility defect (the largest one-edge flow asymmetry), and the short-horizon rise-then-release path probability described in [observables.md](observables.md).

## Stochastic trajectories

Monte Carlo is used to walk a particular path through a kernel whose transition graph is already known, and to keep an event trace a person can read. Each event stores the state before, the candidate toggles, the baseline weight, the constraints that matched, the resulting weights, the normaliser, the integer drawn by `random.Random.randrange`, the selected event, and the state after. At `H = 0` there is no constraint-state change. A halt ends the trajectory.

Replay regenerates the event list from the stored specification hash, expressions, alphabet, initial state, seed, and horizon, and compares it with the stored list.
