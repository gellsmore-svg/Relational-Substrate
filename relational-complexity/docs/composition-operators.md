# Two typed composition operators

Status: the two operators are definitions and validation fixtures. They are not scientific cells. Atlas-008 calculated the three label maps below on five baseline carriers. No engine change. `rrc-0.4.0` is unchanged. The functions are `src/rrc/composition.py`. The checks are `tests/test_composition.py`.

Neither operator is the definition of relational composition. A third reading, a label map of an existing chain, is recorded below. It adds no state.

## Line graph

| Field | Value |
| --- | --- |
| Input | A finite simple undirected graph, as an ordered edge list. An optional `vertex_count` names the vertex set `0 .. n-1`. |
| Operator | `L`. One vertex per input edge, numbered in input order. Two vertices are adjacent when the input edges share an endpoint. |
| Output | A simple undirected graph. The bare output is the vertex count and the edge list. The augmented output also stores the input edges as vertex labels. |
| State | None. Both outputs are functions of the input. |
| Reapplication | Defined on the bare edge list. Isolated vertices of an intermediate graph are not edges, so they are not vertices of the next line graph. A path of `m` edges reaches the empty edge list after `m` applications. A cycle of length at least 3, listed in order around the cycle, has a line graph with the same edge set on the same index set. The indexed edge list may list the closing edge earlier. Further applications stay on five vertices and five edges for the five-cycle used in the fixture. |
| Recoverability | The augmented labels are the input edges, so the input edge set is the label set. That recovery is the labels, not a compression. The bare output does not determine the input: a triangle and a three-edge star have the same bare line graph, three pairwise adjacent vertices. Whitney's theorem says this pair is the exception among connected simple graphs. Isolated input vertices are absent from both outputs. |
| Dynamics | None. The operator does not return a transition law. |
| Order | The bare index list depends on the input edge order. The set of adjacencies between labelled input edges does not. |
| Mathematics | Line graphs. Whitney, *Congruent graphs and the connectivity of graphs*, Amer. J. Math. 54 (1932), for the connected exception. Iteration on paths and cycles is textbook graph theory. EQ-014 is a different statement and is not rerun. |

## Intersection graph and nerve

| Field | Value |
| --- | --- |
| Input | An ordered cover: a list of blocks. A block is a list of elements. Elements are integers, strings, or tuples. |
| Operator | The intersection graph has one vertex per block and an edge when the two blocks have an element in common. The nerve has a face for every set of blocks whose common intersection is nonempty. The intersection graph is the 1-skeleton, together with isolated block vertices that an edge list does not show. |
| Output | A simple graph, or a simplicial complex on the block index set. The bare output drops the blocks. The augmented output stores them. |
| State | None. |
| Reapplication | Undefined for both operators. A graph is not a cover. A complex is not a cover. No encoding of edges as blocks is introduced in order to apply the operator again. |
| Other composition | `line_graph` accepts the bare intersection graph, because that bare output is a simple graph. The result is composition of two operators. It is not a second application of the cover operator. |
| Recoverability | The three covers `{{1,2},{2,3},{1,3}}`, `{{1,2},{1,3},{1,4}}`, and `{{1},{1,2},{1,2,3}}` have the same bare intersection graph, the complete graph on three vertices. The first nerve has no face on all three blocks. The other two nerves are the full 2-simplex and have the same faces. The augmented blocks separate them. A nested cover and an overlapping cover can therefore share a bare nerve. The bare graph does not determine the cover. |
| Surjectivity | Every finite simple graph is the intersection graph of some cover. One standard cover gives each vertex the indices of its incident edges and a private element. The fixture checks a path and a graph with an isolated vertex. This is not a new theorem. Surjectivity of the nerve onto every simplicial complex is not computed. |
| Dynamics | None. |
| Cost | A nerve of more than 12 blocks is refused. The cap is the enumerated subcollections, not a change in the definition. |
| Mathematics | Intersection graphs and the nerve of a cover. The cover is not stored as a tree. |

## Observations of an existing chain

These maps are not the two operators above. The input is a carrier edge list and a weight table the current compiler already builds. The output is a label of each carrier state.

| Map | Label |
| --- | --- |
| Present line graph | Bare line graph of the edges present in that state, including the line-graph vertex count. |
| Present edge count | The number of present edges. |
| Present degree sequence | The non-increasing degree sequence of the present graph, isolated vertices included. `present_graph` already computed this sequence. |

No map adds a coordinate. Each label is a function of the current bitset. The augmented present-edge set would be the bitset itself. The bare line-graph label is not that set: on the triangle, eight states give four labels.

The toggle law is the integer weight table. A zero row is a self-loop. A positive row chooses one edge with probability proportional to its weight. This is `halt_self_loop`. Strong lumpability is the existing `lumpability` test. Exact means that defect is zero. A positive defect is not an approximate closure.

On the unconstrained baseline, every edge has weight 1 in every state. The next edge count then depends only on the current count: from `k` present edges among `m`, the count decreases with probability `k/m` and increases with probability `(m-k)/m`. The edge-count map is strongly lumpable for every carrier under this baseline. The fixture checks the triangle, the three-edge chain, the three-edge star, the four-edge path, and the four-cycle.

The other two maps do not follow from that fact.

| Carrier | Edge count | Degree sequence | Present line graph |
| --- | --- | --- | --- |
| Triangle, three-edge star | Exact. On the star the three maps are the same partition. | Exact. Same partition as the edge count on these two carriers. | Exact. Same partition as the edge count. |
| Three-edge chain | Exact. Four labels. | Not exact. Defect `4/9`. Five labels. Same partition as the line-graph map on this carrier only. | Not exact. Defect `4/9`. |
| Four-edge path | Exact. | Not exact. Defect `1/3`. Seven labels. Not the line-graph partition. | Not exact. Defect `1/3`. Eight labels. |
| Four-cycle | Exact. | Exact. Six labels. Not the line-graph partition. | Not exact. Defect `1/2`. Eight labels. |

Equal defects on the four-edge path are equal numbers for two different partitions. They are not an identity of the maps. The chain agreement is this carrier. The four-cycle separates the degree sequence, which is exact, from the line-graph label, which is not.

No constrained weight table is in this fixture. No second observation is composed with a lumpable quotient: the edge-count chain is a Markov chain on `0 .. m`, and a further label of that chain is not declared. RRC-001's two-subset cut is not used.

## Edge-count identity

The edge-count paragraph above is not limited to weight 1. The assumptions are an empty constraint list, a baseline that is an integer at least 1, and `halt_self_loop`. Every row is that constant. From `k` present edges among `m`, the present edges are the decreases and the absent edges are the increases. The next count is `k/m` toward `k-1` and `(m-k)/m` toward `k+1`. It depends only on `k`, so the present-edge-count label is strongly lumpable on every finite simple carrier. EQ-021 records that identity. The test checks the weights, including baseline 5 on two disjoint edges. Atlas-008's five edge-count cells have defect 0. The degree sequence and the present line graph are outside the identity. A constrained table is outside it. A second label of the count chain is not declared.

## Fixed covers

`docs/cover-observations.md` defines three observations of a cover that stays fixed while the present edges change. A count and an active intersection graph are not covers, so a second application is undefined. The note has fixtures and no frozen cell.

## Position index and canonical form

The present-line-graph row above is the position-indexed bare line graph. A canonical unlabelled line graph, a relationship-labelled line graph, and a carrier-automorphism orbit are different maps. `docs/representations.md` defines them. On the unconstrained four-cycle the fixture recomputes 8 labels and defect `1/2` for the position-indexed map, and 6 labels and defect 0 for the canonical map. Atlas-008 already stored the position-indexed cell. That result file is unchanged.
