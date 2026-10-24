# Observations of a fixed cover

Status: definitions and validation fixtures. No scientific cell is attached to this note. The static intersection graph and the static nerve are unchanged. The engine string stays `rrc-0.4.0`. The functions are `src/rrc/composition.py`.

A cover is an ordered list of blocks. A block is a set of carrier edges. The cover is chosen with the carrier. It is not a state variable, and it is not required to be a partition or a tree. Blocks may overlap. The present edges change. The cover does not.

Intersection here means a shared carrier edge. Two blocks that share a vertex and no edge are disjoint for these maps. That is different from the line graph, which joins edges that share a vertex.

## Maps

| Map | Label | What it drops |
| --- | --- | --- |
| `cover_count` | The number of present edges in each block, in cover order. | Which edges inside a block are present. |
| `active_intersection` | The bare intersection graph of the blocks that contain at least one present edge, plus the number of those blocks. | Which blocks are active, and which edges made them active. |
| `labelled_active_blocks` | The indices of the active blocks, and the pairs of those indices whose blocks share an edge. | Which edges made a block active. |

None adds a coordinate. A second application is undefined: a count tuple and an intersection graph are not covers. No encoding is added to apply the operator again.

## One path, two covers

The carrier is the four-edge path. The partition cover is `{{e0,e1},{e2,e3}}`. The overlapping cover is `{{e0,e1,e2},{e1,e2,e3}}`.

On the empty constraint list the partition count has 9 labels and defect 0. The states with only `e0` and only `e1` share the count `(1,0)`. The quotient of that label is defined. The overlapping count separates those two states and merges only `e1` with only `e2`. It has 10 labels and defect 1. The quotient is undefined. Each cover keeps a distinction the other drops. Exactness and separation are different properties of the two maps.

The blocks of the partition share a vertex and no edge. When `e0` and `e3` are the present edges, both blocks are active and the active intersection graph has two vertices and no edge. The same present edges on the overlapping cover produce an edge, because those blocks share carrier edges.

The bare active intersection graph gives the same label to only `e0` and only `e3`. The labelled active-block map keeps the block index and separates them.

One multiply by 3 of `e0` when `e1` is present uses the same partition-count label. The defect is `1/4`. The baseline exactness does not survive that law. This is one table.

These numbers are fixtures. They are not a frozen round.
