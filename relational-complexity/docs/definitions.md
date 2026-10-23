# Definitions for RRC-001

Stage C. These are the meanings the first frozen round uses. Other meanings stay open and are not computed under these names.

## Chosen

**Relational state.** N labelled nodes, `N >= 2`. A state is a simple undirected graph: each unordered pair is present or absent. Pairs are ordered `i < j` lexicographically, as in the Constraint Laboratory. No coordinates are stored.

**Structural size.** For a carrier, structural size is N, the number of nodes. It is not the number of present edges, not the number of blocks, and not a path length.

**Experimenter-designated structure.** A node subset written in the plan. Internal pairs have both ends in the subset. Interface pairs are all the others. A composed pair of structures is two disjoint subsets; hidden pairs are the pairs inside either subset; the interface is the cut. This is an instrument. It is not inferred.

**Open structure definitions, not used in RRC-001.** Connected components of the current graph. Persistent motifs. Symmetry orbits. Behavioural equivalence classes discovered by search rather than declared. A finite external interface found by optimising a statistic. Any of these may name different objects. RRC-001 does not call its subsets by those names.

**Consequential observable, interface items.** The next-step law of the block that contains the current state. The block is the interface bit pattern, or that pattern plus one declared augmentation.

**Consequential observable, propagation items.** The stationary probability that each pair is present, and the stationary probability of toggling that pair in one step. Depth is the smaller endpoint index on the declared path `0—1—…—(N-1)`. That index is a scaffold.

**Strong lumpability.** Every state in a block has the same total probability of moving into each block. The interface process is then Markov for every initial distribution.

**Exact behavioural equivalence, in this round.** Strong lumpability. The defect is the zero rational. A float rendering of that rational is not the test.

**Defect magnitude.** The maximum, over states, of the L1 distance between that state's next-block law and the mean law of its block. Zero if and only if the partition is strongly lumpable. This is not total variation of a stationary marginal, and it is not weak lumpability.

**Approximate equivalence.** Not claimed. A positive defect is a failure of exactness, reported with its rational magnitude. No threshold turns a positive defect into "close enough to equivalent".

**Augmentations.** Refinements of the interface partition by a function of the hidden pairs:

| Name | Extra coordinate |
| --- | --- |
| `interface` | none |
| `edge_count` | number of present hidden pairs |
| `parity` | that number modulo 2 |
| `interface_wedge_counts` | the common-neighbour count of each interface pair |

**Lumpable closure.** The coarsest strong-lumpability refinement of the interface partition obtained by splitting blocks whose states disagree about the next-block law. Its block count is the size of the exact current-state description that still reports the interface. It is computed only when the plan sets `closure` true.

**Recursive composition.** The two-subset partition above, one constructed step from a single subset to two subsets on a shared cut. It is not a discovered hierarchy and it is not six levels of composition.

**Grammar forms the engine may report.**

| Form | Meaning |
| --- | --- |
| `unconstrained_lazy` | The interface is Markov, one step flips at most one interface pair, and every interface pair has the same toggle probability in every block |
| `reweighted_single_toggle` | The interface is Markov and the event shape is unchanged, but the toggle probabilities are not that constant |
| `not_markovian_on_interface` | The event shape still flips at most one pair, and the interface law is not a function of the interface block |
| `outside_grammar` | Some positive-weight step changes more than one interface bit |

A positive defect is `not_markovian_on_interface`, not a transformed grammar. `reweighted_single_toggle` is a transformed weight system with the same event shape. `unconstrained_lazy` is the original unconstrained grammar plus a holding probability.

**Halt.** A state with every weight zero is completed by a self-loop named `halt_self_loop`. The loop is not a relational event.

**Stationary method.** Parity-balanced iteration: the average of a distribution and its image. Tolerance is frozen in the plan. Two starts must agree. A dense solve is required when the state count is at most the plan's dense limit. Disagreement leaves the item `unresolved`. The tolerance is not widened.

## Not chosen

- Weak lumpability.
- Equivalence of stationary marginals as a substitute for lumpability.
- History variables. Hidden pairs are current state.
- An independent hyperedge, or a transition that toggles two pairs.
- Sampling.
- N=7 or larger exhaustive kernels.
- Any identification among six constituent nodes, six edges along a path, six levels of composition, and six units of context.

## What the tests already fixed, before the round

Declared pre-observation, so the frozen items of these kinds are replications rather than unopened cells:

- Unconstrained weights, N=4, subset `{0,1,2}`: exact lumpability, grammar `unconstrained_lazy`, one recurrent class. Checked in `tests/test_identities.py`.
- The same identity at N=3 and N=4 against `build_kernel` in the laboratory: every toggle has probability `1/C(N,2)`.
- State-independent unequal rates, N=3, subset `{0,1}`: exact, grammar `reweighted_single_toggle`.
- Propagation identity at N=3: occupation stays 1/2; the far pair's toggle rate moves from 1/3 to 1/11 under incident weight 5.
- Wedge weights on the empty graph, the single pair, the two-pair path and the triangle at N=3. No lumpability was computed for those rules.
- A four-state synthetic kernel that is not lumpable, and one that is. Not a scientific rule.

No soft-wedge or hard-wedge lumpability number, and no propagation profile for the soft wedge, has been computed.
