# Mathematical architecture

This note is the opening architecture. Stage C names which definitions RRC-001 actually uses. The engine must not silently add a definition that this note and the frozen plan do not list.

## Elementary system

- Nodes are distinguishable labels `0 .. N-1`.
- A potential relation is an unordered pair. There are `C(N,2)` pairs.
- A state is the subset of pairs that are present, stored as a bitset in laboratory edge order.
- A step selects one pair with probability proportional to a current-state weight and toggles it.
- If every weight is zero, the state halts. The chain used for classification adds a self-loop and records the halt. The self-loop is not a relational event.
- No coordinate embedding, Euclidean distance, or spatial adjacency is part of the state.

N, the rule, and the partition are independent parameters.

## Rules under consideration for the first round

The plan, not this note, freezes the numbers.

| Family | Weight of toggling pair `{a,b}` | Current state only |
| --- | --- | --- |
| `unconstrained` | 1 | yes |
| `state_independent_rates` | a declared positive integer that may depend on the pair and not on which other pairs are present | yes |
| `hard_wedge_formation` | 0 when `{a,b}` is absent and `a`,`b` have no common neighbour; 1 otherwise | yes |
| `soft_wedge` | a declared integer `c` when `a`,`b` have at least one common neighbour; a declared integer `b0` otherwise | yes |
| `soft_wedge_local_boost` | the soft-wedge weight, multiplied by a declared integer when the pair touches a designated node | yes |

A common neighbour is a node joined to both endpoints by present pairs. That is graph adjacency in the current relation, not a position.

## Structures

RRC-001 designates a structure by a node subset written in the plan. That designation is an experimental instrument. It is not an inferred community, a motif discovered by search, or an equivalence class.

Internal pairs are pairs with both ends inside the subset. Interface pairs are the other pairs. For a single subset the interface is the cut plus every pair in the complement. For two designated triads the hidden pairs are the pairs inside either triad, and the interface is the cut between them.

These partitions can disagree with other structure definitions (components of the current graph, persistent motifs, symmetry orbits, behaviourally defined lumps). Those other definitions stay open. They are not computed under the same name.

## Effective description

An effective description in this round is a partition of the full state space. The interface partition groups microstates that share the same interface bits. An augmentation refines that partition by a function of the hidden bits (count, parity, or the common-neighbour counts of the interface pairs).

For each partition the engine records:

1. The observable preserved under discussion: the next interface bits, or the next augmented block.
2. Whether preservation is exact (strong lumpability, defect zero) or only a measured L1 defect.
3. The initial conditions covered: every distribution, because the criterion is strong lumpability. No stationary exception is claimed.
4. Whether the reduced transition is Markov: yes exactly when the defect is zero.
5. What is lost: the hidden bits that the partition deletes, and any distinction the defect shows was consequential.
6. Whether the reduction survives a further composition: only the two-triad cell speaks to that, and only if it is run.

Statistical closeness of stationary marginals is a different observable and is not labelled equivalence.

## Recursive composition

The hierarchy `pairs → designated subset → two subsets sharing a cut` is constructed and labelled as constructed. It is not discovered.

At a level where the defect is zero, the engine records whether the block chain is a lazy single-toggle chain on the interface bits, and whether those toggle probabilities are constant across interface edges. Constant probabilities mean the unconstrained grammar has survived, up to a holding probability. Unequal probabilities mean the event shape survived and the weights changed. A positive defect means this interface has no closed current-state grammar.

## Propagation instrument

Consequential reach is not the hop count in the complete graph of potential pairs. For propagation items the plan may declare the path index `0—1—…—(N-1)`. The depth of a pair is the smaller endpoint index. That index is a scaffold. The measured quantities are the change in stationary presence of each pair, and the change in stationary toggle rate, between a base rule and a locally boosted rule. A change that is the same at every depth is a global normalisation effect, not depth-dependent transmission.

## What the engine refuses to infer

- A bound that was not attained inside the computed sizes.
- Exactness from an approximate stationary distance.
- A grammar identity from a shared motif count.
- An ontological reading from either.
