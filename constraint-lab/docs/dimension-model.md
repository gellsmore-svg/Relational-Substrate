# Dimension model

Several quantities are easy to call “dimension”. They are different axes, and a generation names each of them.

## A — constraint / relation arity

`A` is the number of distinct entities named by a constraint, or by a constraint set (the union of the entities its members name).

```text
C(x)           A = 1
C(x, y)        A = 2
C(x, y, z)     A = 3
```

On the pairwise substrate a single edge already has `A = 2`. A condition on a second edge can raise `A` without raising the relation order.

## G — geometric dimension

`G` is the dimension of an explicit embedding.

```text
G = 0    no coordinates, no distance, no direction, no metric
G = 1, 2, 3, 4, ...    an embedding of that dimension, introduced as an extra constraint family
```

Generation 1 has `G = 0`. Geometry, when it arrives, is an additional representational layer. The baseline kernel does not secretly use a distance.

## S — additional local state channels

`S` counts finite-valued channels attached to entities, to relations, or to constraints, other than the binary incidence bit of a relation.

```text
S = S_entity + S_relation + S_constraint
```

The bit that says “this pair relation is present” is the relation itself. It is not a channel in `S`. Counting every edge bit as a dimension would make `S` a disguised copy of the hypercube, and the axis would no longer be able to record an extra field such as a threshold register or a constraint weight that itself changes.

Generation 1 has `S_entity = S_relation = S_constraint = 0`.

## Further axes

| Symbol | Meaning in this laboratory |
| --- | --- |
| `N` | Number of labelled entities |
| `O` | Maximum relation order. Pairwise generation uses `O = 2` |
| `H` | History depth. `H = 0` means the kernel is memoryless |
| `K` | Expression complexity: 1 for the action literal, plus one per condition |
| `L` | Meta-constraint depth. `L = 0` means constraints do not rewrite constraints |
| `W` | Named weight alphabet (`W4`, `W3`, `W16`) |
| `T` | Trajectory horizon, or the rise-then-release horizon, as declared on the spec |
| `R` | Seeds used when a trajectory is sampled |

A semantics flag sits beside the coordinate: `graph`, `hypergraph`, or `simplicial`. These are not three encodings of one object.

- **Graph.** Independent binary incidences. The presence of `R(A,B,C)` is not a primitive.
- **Hypergraph.** An irreducible hyperrelation `R(A,B,C)` need not imply `R(A,B)`, `R(A,C)`, or `R(B,C)`.
- **Simplicial complex.** A higher simplex carries its faces.

Generation 1 executes `graph` only. A specification that names `hypergraph` or `simplicial` is refused, with an explicit error, rather than compiled down to pairs.

## Choreography

The kernel asks a choreography object which constraints are active. At `H = 0`, `L = 0` the answer is the whole set. The call already passes a history tuple and a constraint-state map. A later generation can gate, order, or rewrite constraints there. Those generations are unsearched. The object exists so the kernel does not have to be replaced when `H` or `L` becomes positive.

## Reading a coordinate

```text
E(N=4, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, semantics=graph, W=W4)
```

means: four entities, constraints naming at most four of them, pairwise relations, no geometry, no extra channels, no memory, expressions of at most two literals, no meta-constraints, graph semantics, dyadic weights. The cardinality of the constraint set (one constraint, a pair, a triple) is part of the cell and is reported beside `K`.
