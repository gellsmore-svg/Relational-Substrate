# Four representations of a present line graph

Status: definitions and validation fixtures. No scientific cell is attached to this note. Atlas-008 stored the position-indexed map and is not rerun. The engine string stays `rrc-0.4.0`. The weight compiler is unchanged. The functions are `src/rrc/composition.py`. The checks are `tests/test_composition.py`.

Each map sends a carrier state to a label. The label is a function of the present edges. None of the four adds a coordinate. Exact means strong lumpability of that label under the integer weight table. A positive defect rules out strong lumpability of that partition. It does not rule out every history-dependent description.

## Five operations

A permutation is not one operation. These five are different.

1. A permutation of the original node names that keeps each carrier edge in the same list position. The i-th edge is rewritten with the new names of its endpoints. Which positions share an endpoint does not change.
2. A permutation of positions in the carrier-edge list. The same edges may appear, and the i-th position may now be a different edge.
3. A graph isomorphism. A numbering of the vertices of one simple graph onto another. It need not preserve a fixed carrier, and it need not preserve list positions.
4. An automorphism of a fixed carrier. A numbering of that carrier's vertices that preserves its edge set. The three-edge path has two: the identity and the reversal. An end edge and the middle edge are not in one orbit.
5. A general permutation of edge bits that is not induced by any carrier automorphism. Swapping the middle edge of the three-edge path with one end edge is an example. It permutes toggle coordinates. It is not operation 4.

R2 is unchanged by operation 1 and can change under operation 2. R1 changes under operation 1 and is unchanged by operation 2. R3 follows the isomorphism type of the line graph, which is operation 3. R4 is unchanged by operation 4. Operation 5 is a statement about weight tables and bit coordinates. It is not an automorphism of the carrier, and it is not a renumbering of line-graph vertices.

## R1 — relationship-labelled line graph

| Field | Value |
| --- | --- |
| Input | The edges present in one carrier state. |
| Operator | One vertex for each present edge. The vertex name is that edge. Two vertices are adjacent when the edges share an endpoint. Names are sorted, so the carrier edge order does not change the label. |
| Output | An edge-labelled line graph. |
| State | None. |
| Reapplication | Undefined. The vertices are edges, and `line_graph` accepts integer endpoints. No encoding is added in order to apply it again. |
| Recoverability | The vertex names are the present edges, so the present edge set is the label. Given the carrier, the bitset is recovered. The recovery is the retained names. |
| Dynamics | The label separates the carrier states. A partition into singletons is strongly lumpable for every weight table on those states. EQ-022 records that fact. The exactness retains the present edges. |
| Preserved by | Operation 2. Reordering the carrier edge list. The vertex names are the edges, and the names are sorted. |
| Changed by | Operation 1. A permutation of the original node names. This is not a reordering of the edge list. |

The bare line graphs of a triangle and a three-edge star are the same unlabelled graph. The labelled line graphs keep different edge names.

## R2 — position-indexed line graph

| Field | Value |
| --- | --- |
| Input | The carrier edge list and one present subset. |
| Operator | `line_graph` of the present edges in carrier order. Vertices are `0 .. k-1` in that order. |
| Output | The bare edge list and the line-graph vertex count. |
| State | None. |
| Reapplication | The static bare line graph accepts `line_graph` again. This observation map does not declare a second label. |
| Recoverability | The bare list does not determine which carrier edges were present. |
| Dynamics | Whatever strong lumpability says for this partition. |
| Preserved by | Operation 1. A node-name permutation that keeps each carrier edge in the same list position. The endpoints of a listed edge move together, so the bare index list is unchanged. |
| Changed by | Operation 2. A permutation of positions in the carrier-edge list. The line-graph vertices are numbered in that list order, so the bare list can change. |

This is the `present_line_graph` map stored by atlas-008.

## R3 — canonical unlabelled line graph

| Field | Value |
| --- | --- |
| Input | The bare line graph of the present edges, including isolated line-graph vertices. |
| Operator | The lexicographically least edge list over every numbering of those vertices. Isolated vertices stay in the vertex count. |
| Output | A canonical simple graph. |
| State | None. |
| Reapplication | Defined. The canonical graph is already the least edge list, so the second application returns the same graph. That is idempotence, not a further level. |
| Recoverability | The certificate does not determine the input graph. A triangle and a three-edge star have one certificate. Whitney's exception is that pair among connected simple graphs. It is not a new theorem. |
| Dynamics | The class is an observation of the carrier chain. It is strongly lumpable only when the defect is zero. |
| Preserved by | Any numbering of the line-graph vertices, any order of the carrier edges, and any permutation of the original node labels. |
| Changed by | A change that alters the isomorphism type, or the number of line-graph vertices. |
| Cost | The search enumerates every permutation. It is refused above 8 vertices. The refusal is not a canonical form. An independent backtracking search agrees with the certificate on every simple graph of order 4. |

An ordinary hash of an edge list is not this certificate.

## Canonicalisation is not iteration

Calling the canonicaliser again is not the same operation as building another line graph.

- Canonicalising a graph that is already canonical returns the same edge list. `second_application` is `defined_and_idempotent`. That is idempotence of the numbering.
- Applying `line_graph` to the graph represented by that certificate builds a different graph. The certificate of the three-edge path on four vertices is `[[0,1],[0,2],[1,3]]`, another numbering of that path. Its line graph has three vertices and edges `[[0,1],[0,2]]`. The edge lists differ.
- Iterating the line-graph operator applies that construction again. `iterate_line_graph` records step 0 as the input. One further application of this line graph is a single edge.
- Iterating an observation function would send a label through the same map again. No observation map in this note declares that second label.
- Iterating a dynamical quotient would take a quotient kernel, when one exists, and lump it by a further partition. No such second quotient is constructed here. `observation_law` either returns the quotient rows of one label of the carrier chain or leaves those rows undefined.

A second canonicalisation is the same graph. It is not a new relational level, and it is not evidence that the line-graph operator has been iterated.

## R4 — carrier-automorphism orbit

| Field | Value |
| --- | --- |
| Input | A fixed carrier and the present edge set. |
| Operator | The lexicographically least image of that edge set under a vertex permutation that preserves the carrier. The minimum is the sorted edge list, so the carrier's list order does not choose it. |
| Output | One edge subset of the same carrier. |
| State | None. |
| Reapplication | Undefined. The automorphism group belongs to the carrier, and the representative does not determine that carrier. |
| Recoverability | The representative is one member of the orbit. The orbit does not determine which member was present. |
| Dynamics | Under an empty constraint list, a positive integer baseline, and `halt_self_loop`, the baseline kernel commutes with the carrier automorphisms. The orbit partition of a group-equivariant chain is strongly lumpable. EQ-023 records that application. A constraint that breaks the symmetry is outside it. |
| Preserved by | Carrier automorphisms, and reordering the carrier edge list. |
| Changed by | A node permutation that is not an automorphism of the carrier. The integer coordinates of the representative move. |
| Cost | The same cap of 8 vertices. Above the cap the search is refused. |

R4 is not the unlabelled isomorphism class of the present graph, and it is not R3. An end edge and a near-centre edge of a path are isomorphic as graphs. They are different orbits of the path.

## Four-cycle baseline, recomputed

The carrier is the four-cycle with edges `(0,1), (1,2), (2,3), (0,3)`, empty constraints, baseline 1. The fixture recomputes the maps. Atlas-008 already stored the position-indexed cell: 8 labels, defect `1/2`. The degree cell stored there has 6 labels and defect 0. Those files were not rewritten.

| Representation | Labels | Defect |
| --- | --- | --- |
| R2 position-indexed line graph | 8 | `1/2` |
| R3 canonical line graph | 6 | 0 |
| R4 carrier orbit | 6 | 0 |
| Degree sequence | 6 | 0 |
| Edge count | 5 | 0 |

R3, R4, and the degree sequence are one partition on this carrier. The edge count is coarser: it merges the two-edge states that are a path with the two-edge states that are a matching. R2 is finer than R3. Two present graphs whose line graphs are the same path on three vertices can have different position-indexed edge lists. The witness in the fixture is the present edges `{0,2,3}` and `{0,1,2}`.

The quotient kernel of R3 is stored by the fixture as exact fractions. From the empty graph the next class is the one-edge class, with probability 1. From one edge the next class is empty with probability `1/4`, an adjacent pair with probability `1/2`, and an opposite pair with probability `1/4`. From either two-edge class the next class is one edge or three edges, each with probability `1/2`. From three edges the next class is an adjacent pair with probability `1/2`, an opposite pair with probability `1/4`, and the full cycle with probability `1/4`. From the full cycle the next class is three edges, with probability 1.

## Where the same baseline separates the maps

On the triangle and on the three-edge star, R2, R3, R4, the degree sequence, and the edge count are one partition. Each is exact. Those carriers are the controls where the representations agree.

On the three-edge chain, R2, R3, and the degree sequence are one partition, with 5 labels and defect `4/9`. R4 has 6 labels and is exact. The canonical line graph merges an end edge with the middle edge. Those two states have different next-orbit laws. The carrier reversal keeps them apart.

On the four-edge path, R3 and the degree sequence are one partition, with 7 labels and defect `1/3`. R2 has 8 labels and the same defect. The partitions differ. The shared defect does not identify the maps. R4 has 10 labels and is exact. EQ-023 covers that exactness. It does not cover the defect of R2 or R3.

## One constraint outside EQ-023

The same four-cycle, with one multiply by 3 of edge `(0,1)` when edge `(1,2)` is present, uses the same R4 partition. The defect is `11/24`. The quotient is undefined. The orbit label does not stay exact after the law stops commuting with the carrier automorphisms. This is one table, not a census of constraints.
