# atlas-013 observations

A map of one verified sample. Not a conclusion. Not an instruction to choose a threshold.

Plan hash `5f39cf2cc5f5d8bd7975422eb0cd039544d606ef47e3fde38c07654bd79dc010`. Definitions commit `9068c99`. Freeze `eb53086`. All 5 items completed in one invocation, 0.782646 seconds. Verify printed `verified`. The generated table is `reports/atlas-013.md`. Its Hash column is a 12-character prefix. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. The empty list uses grammar `opening-prohibit-multiply-v1`. The four prohibits use `incident-count-v1`. Occupation on the two unique cells uses `integer_pi_proportional_to_total_weight`. The three uniform lists have no unique occupation, and no mean is reported for them. `results/atlas-006` and `results/atlas-012` were not rerun.

Every cell has 8 states and 3 edges. The kernel hash equals the weight hash. The compilation gate reports current-state single-toggle weights and `new_primitive` false. The carrier is the star `(0,1)`, `(0,2)`, `(0,3)`. Every subgraph of a star is a forest, so in every state the component count is `4` minus the present-edge count. That identity is the carrier. It is not a property of the prohibit.

## Tables

The empty list is the constant-1 three-edge table, hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. That is the EQ-015 weight table. The structure hash is `6c959c90bc45976a55a7d874b0e0e4a6c4c31cf14f231e39417136e5ddf1e1d1`, the same structure hash stored on the atlas-008 star cells. The atlas-008 chain structure hash is different. Mean edges `3/2`. Mean components `5/2`. Marginal `1/2` on each edge. EQ-015 does not claim that the carrier geometry is the table. The component mean `5/2` is this star. It is not the N=3 complete-carrier component mean.

`A13-eq1` is a uniform `eq 1` prohibit, declared cardinality 3, effective cardinality 3, removal-sensitive count 3. Hash `1f82f333586889368e6492f1d1e050aa9bfe371d399299433a7b6b7080a45695`. Twelve weight cells are 0 and twelve are positive. No row is all zeros. Deadlocks 0. Recurrent classes 2. The stored successors put masks `{0,1,2,4}` in one class and masks `{3,5,6,7}` in the other. There is no transient state. Occupation status `not_unique`.

`A13-eq2` and `A13-ge2` are one table, hash `3811f60d68e33785a86d79fd47e1030351152dd33251b252e9cf164537db574c`. EQ-028 records that equality. Each list has declared cardinality 3, effective cardinality 3, and removal-sensitive count 3. Six weight cells are 0 and eighteen are positive. The only zero row is state 7, the full star. Deadlocks 1. Recurrent classes 2: state 7 alone, and the other seven states together. Occupation status `not_unique`.

`A13-one` prohibits only `(0,1)` at `eq 2`. Declared cardinality 1, effective cardinality 1, removal-sensitive count 1. Hash `559a60132ec515f31a30395d46d560d4672a104e447331beaeaea53dfd6e4f6f`. Two weight cells are 0. No zero row. One recurrent class. Mean edges `31/22`. Mean components `57/22`. Marginals `1/2`, `5/11`, `5/11`, in carrier order. The two unconstrained edges share a marginal. Comparing this cell with a uniform list changes the declared cardinality. That comparison is joint.

## Support

Each prohibit writes 0 or leaves the baseline 1. No cell multiplies a positive weight. `max_positive_k` is 0 because a prohibit is not a positive feature. `expansion_k` is 3 on every count feature, and declared J stays 1 for each feature. The `eq 1` list has `expansion_j` 2 on each edge. The threshold-2 lists have `expansion_j` 1 on each edge. Those expansion numbers are not a literal count.

`action` is `either`, and the incident count reads the other edges. `empirical_bit_independent` is true on every cell. That does not keep the support full. The uniform lists delete transitions. The `eq 1` support has two closed sets. From a single present edge, each absent edge sees exactly one present neighbour, so the prohibit blocks every step that would add a second edge. From a state with two present edges, each present edge sees exactly one other present edge, so the prohibit blocks every step that would remove an edge, while the missing edge sees two present neighbours and can still be added. The set with fewer than two edges and the set with at least two edges do not meet. The threshold-2 prohibit blocks an edge only when both others are present, which is state 7 for every column. State 7 does not communicate with the other states. These classes are the support of the stated guards.

The single `eq 2` prohibit blocks one edge in that same full state and leaves the other two edges free, so the state space stays one class.

## What the slice does not say

ATLAS-Q02 stays open. The round asked whether these lists change support, rates, or both. On this star they change support and do not rescale a positive weight. That is one effect and one carrier. A multiply is not in the slice. `eq 0` and `ge 0` are not in the slice. A neighbourhood larger than 2 is not in the slice: on the three-edge star the incident count cannot exceed 2, so `eq 2` and `ge 2` match the same states. EQ-028 does not claim that equality for a larger neighbourhood. The atlas-006 factor-3 multiplies were not rerun. PAT-002 is not this grammar. No pattern is opened from the class split or from the mean `31/22`.
