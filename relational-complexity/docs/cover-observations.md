# Observations of a fixed cover

Status: definitions and validation fixtures. No scientific cell is attached to this note. The static intersection graph and the static nerve are unchanged. The engine string stays `rrc-0.4.0`. The functions are `src/rrc/composition.py`.

The operator accepts an ordered family of blocks. A block is a set of carrier edges. The family is chosen with the carrier. It is not a state variable, and it is not required to be a partition or a tree. The present edges change. The family does not.

The usual mathematical words are not interchangeable.

- A full cover is a family whose union is the whole carrier.
- A partial family is a family whose union misses at least one carrier edge. Atlas-011 stored three omission lists on the triangle. Each omits one edge. Those lists are partial families. The stored cells were not rewritten, and this note does not rerun them.
- A partition is a full cover whose blocks are pairwise disjoint and nonempty.
- An overlapping cover is a full cover with at least one nonempty pairwise intersection.
- A nested family contains a block that properly contains another block. Equal blocks are not nested.
- A dynamically active subfamily is the subcollection of blocks that contain a present edge. It depends on the state. The block definitions do not.

Potential overlap and realised overlap are different conditions. Two blocks potentially overlap when their fixed edge sets meet. That condition does not read the present edges. Two blocks have realised overlap in a state when a shared edge is present. The three maps below do not test realised overlap. `active_intersection` and `labelled_active_blocks` join active blocks when the fixed sets meet, even if the shared edge is absent.

Intersection here means a shared carrier edge. Two blocks that share a vertex and no edge are disjoint for these maps. That is different from the line graph, which joins edges that share a vertex.

## Maps

| Map | Label | What it drops |
| --- | --- | --- |
| `cover_count` | The number of present edges in each block, in cover order. | Which edges inside a block are present. |
| `active_intersection` | The bare intersection graph of the blocks that contain at least one present edge, plus the number of those blocks. | Which blocks are active, and which edges made them active. |
| `labelled_active_blocks` | The indices of the active blocks, and the pairs of those indices whose blocks share an edge. | Which edges made a block active. |

None adds a coordinate. A second application is undefined: a count tuple and an intersection graph are not covers. No encoding is added to apply the operator again.

## One path, two covers

The carrier is the four-edge path. The partition is `{{e0,e1},{e2,e3}}`. It is a full cover and a partition. The overlapping family is `{{e0,e1,e2},{e1,e2,e3}}`. It is a full overlapping cover, and it is not nested. Neither family is a partial family.

On the empty constraint list the partition count has 9 labels and defect 0. The states with only `e0` and only `e1` share the count `(1,0)`. The quotient of that label is defined. The overlapping count separates those two states and merges only `e1` with only `e2`. It has 10 labels and defect 1. The quotient is undefined. Each cover keeps a distinction the other drops. Exactness and separation are different properties of the two maps.

The blocks of the partition share a vertex and no edge. When `e0` and `e3` are the present edges, both blocks are active and the active intersection graph has two vertices and no edge. The same present edges on the overlapping cover produce an edge, because those blocks share carrier edges.

The bare active intersection graph gives the same label to only `e0` and only `e3`. The labelled active-block map keeps the block index and separates them.

One multiply by 3 of `e0` when `e1` is present uses the same partition-count label. The defect is `1/4`. The baseline exactness does not survive that law. This is one table.

These numbers are fixtures. They are not a frozen round.

## Realised overlap

Potential overlap is fixed by the blocks. Realised overlap also requires a present shared edge. `realised_intersection` is the bare graph of the active blocks with that stricter adjacency. `labelled_realised_blocks` keeps the block indices. `realised_overlap_count` counts the present edges in each pairwise intersection. None of the three replaces `active_intersection` or `labelled_active_blocks`.

On the four-edge path, the overlapping family shares two edges. When only the two end edges are present, both blocks are active and the potential graph has an edge. The realised graph has two vertices and no edge. One present shared edge and two present shared edges have the same bare realised graph and different counts.

The blocks of opposite edges on the four-cycle are disjoint. Realised adjacency and potential adjacency are both empty, so those graphs agree. The shared-edge count is the constant 0.

The triangle family `{{(0,1),(1,2)},{(1,2),(0,2)}}` has one possible shared edge. Its realised labelled graph is not the potential labelled graph. Under the empty list the realised labelled graph has 5 labels and defect `1/2`. Under one multiply by 3 of `(0,1)` when `(1,2)` is present it has 5 labels and defect `3/10`. The count of that shared edge has 2 labels and defect 0 under both laws. The guard of that multiply is the shared edge, so the weights are constant on each value of the count. These are fixtures. They are not a frozen round. A block family that changes over time is not one of these maps.
