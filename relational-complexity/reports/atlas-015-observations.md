# atlas-015 observations

A map of one verified sample. The question stays open.

Plan hash `75f36e40fc647bb953c64d7d91e65820db40e8bd459bfea6bf0c07b7392e1b0b`. Definitions commit `081d52a`. Freeze `a74e9fb`. All 20 items completed in one invocation, 3.161905 seconds. Verify printed `verified`. The generated table is `reports/atlas-015.md`. Its Defect column is a float. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. Grammar `opening-prohibit-multiply-v1`. `results/atlas-001`, `results/atlas-008`, and `results/atlas-012` were not rerun. The structure hash below was compared with the hash already stored on the atlas-008 chain cell and the atlas-012 baseline.

Every item has 8 states and 3 edges. The carrier is `(0,1)`, `(1,2)`, `(2,3)`. The blocks are `[(0,1),(1,2)]` and `[(1,2),(2,3)]`. They share `(1,2)`, and each carrier edge sits in a block. The family is an overlapping cover. It is not a partition. The kernel hash equals the weight hash. `new_state` is false. No item declares a second map, so `further_label` is `undefined`. The four maps of one law share one weight table. There are five tables.

## Four partitions

The maps are functions of the present edges and the fixed family. The weight table does not choose the blocks. Each law therefore has the same four partitions.

The bare active intersection has 3 labels. Adjacency is potential overlap: the fixed edge sets meet, whether or not the shared edge is present. The bare realised graph has 4 labels. It joins the two blocks only when `(1,2)` is present. The labelled realised blocks have 5 labels: they keep which block is active, and state 1 is separated from state 4. The shared-edge count has 2 labels, the presence of `(1,2)`.

State 5 is edges `(0,1)` and `(2,3)`, with `(1,2)` absent. Both blocks are active. The potential graph has two vertices and one edge. The realised graph has two vertices and no edge. That one state is why the potential partition and the realised partition differ.

## Five weight tables

The empty list is the EQ-015 table, hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. Every cell is 1. The structure hash is `e6f7386ece69cd8888eca2be7cbc621dc46a80b61c6ddebb9f0a18abfceea8cc`, the structure hash of the atlas-008 chain cell and the atlas-012 baseline.

The prohibit of `(1,2)` when `(0,1)` is present has hash `fe1f4d4e5e5fcac700a7efc7ec32acb0dfcc1c21f5bb401f6b27738b527b2d7c`. Four cells are 0, all in the column of `(1,2)` and all in states where `(0,1)` is present: `(1,1)`, `(3,1)`, `(5,1)`, `(7,1)`. The other cells are 1.

The prohibit of `(0,1)` when `(1,2)` is present has hash `d65a9800e618e62c49e0199f0d5cac3ca201448067180dbbbe4139a641958007`. Four cells are 0, all in the column of `(0,1)` and all in states where `(1,2)` is present: `(2,0)`, `(3,0)`, `(6,0)`, `(7,0)`. The other cells are 1. This matrix is the atlas-001 cell `A-N3-02-pro-present`. The complete graph on three vertices lists `(0,1)`, `(0,2)`, `(1,2)`. That cell prohibits the first listed edge when the second is present. The chain prohibits the first listed edge when its second edge, `(1,2)`, is present. Both rules leave the third edge at weight 1. The carriers differ, and the condition edges `(0,2)` and `(1,2)` are different pairs. The shared object is the matrix. EQ-031 records that bit-position identity. Atlas-001 stored no overlap map.

The multiply by 3 of `(1,2)` when `(2,3)` is present has hash `fa10bdcc43d20cf87f97823c9a8b9ec9aefc370aabebd884ec98038b6123e915`. States with `(2,3)` present have weight 3 in the column of `(1,2)`. Every cell is positive.

The multiply by 3 of `(2,3)` when `(0,1)` is present has hash `92189689622ad7ebd818c01b8ab01236265258c1cacdf43adf9de5c3f124311c`. States with `(0,1)` present have weight 3 in the column of `(2,3)`. Every cell is positive. The rule names the two end edges. It does not name `(1,2)`.

The two prohibits change support. The two multiplies change positive weights. None of the four lists is an atlas-012 multiply.

## What is strongly lumpable

The shared-edge count is exact under the empty list, defect `0/1`. Every row is `(1,1,1)`, so the probability of toggling `(1,2)` is `1/3` in every state. It is also exact under the prohibit of `(0,1)` when `(1,2)` is present. Inside the absent block every row is still `(1,1,1)`. Inside the present block every row is `(0,1,1)`, so the probability of toggling `(1,2)` is `1/2` throughout that block. The guard is the observed bit, and the prohibited event is a different edge.

The same count has defect `1/3` under the prohibit of `(1,2)` when `(0,1)` is present. The witness pair is states 0 and 1, pairwise L1 `2/3`. State 0 can add `(1,2)`. State 1 cannot, because `(0,1)` is present. The guard is not a function of the observed bit.

Under the multiply of the shared edge the count has defect `4/15`. The witness pair is states 0 and 4, pairwise L1 `8/15`. `(2,3)` is absent in state 0 and present in state 4, and both states have `(1,2)` absent. Under the multiply of `(2,3)` the count has defect `2/15`. The witness pair is states 0 and 1, pairwise L1 `4/15`. The rule changes the row sum when `(0,1)` is present, so the probability of toggling the unnamed shared edge changes with it. That is a difference of transition probabilities inside one observation block. It is not an intervention, and no intervention operator is defined.

The active intersection, the realised graph, and the labelled realised blocks are not strongly lumpable on any of the five tables. On the empty list the active defect is `4/5`, witness states 2 and 5, pairwise L1 `4/3`. The realised defect is `1/2`, witness states 2 and 3, pairwise L1 `2/3`. The labelled defect is also `1/2`, with the same witness pair, and the partition still has 5 labels rather than 4. The shared multiply gives both the realised graph and the labelled blocks defect `9/10`, with different witness pairs: states 2 and 7 for the bare graph, states 2 and 6 for the labelled blocks. A shared fraction is not an identity of the two partitions.

## What the slice does not say

ATLAS-Q14 stays open. The four maps answer it for this one cover and these five laws. They do not classify every block family. The family does not change over time. No map adds a coordinate. No pattern is opened from `4/5`, `1/2`, `1/3`, `4/15`, `2/15`, `9/10`, `3/4`, `13/15`, `22/15`, or `16/15`. The path and triangle fixture defects were not recomputed. The atlas-012 means were not recomputed.
