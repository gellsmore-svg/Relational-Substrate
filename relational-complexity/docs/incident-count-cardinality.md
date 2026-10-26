# Uniform ge-2 multiply and effective cardinality

Status: scoped identity, checked by `tests/test_count_cardinality.py`. Not a new scientific round. Not a property of every count.

Atlas-006 stored the same count on its five uniform `ge 2` lists. PAT-011 records that observation. Those cells were not rerun. This note proves the count for the family named below, including actions and carriers the round did not use, and records two lists that leave the family.

## Family

The carrier is a simple undirected graph. Its edges are listed in a fixed order. On every carrier edge there is exactly one constraint: multiply by an integer factor `f >= 2`, with action `either`, `form`, or `dissolve`, when at least two other carrier edges that share an endpoint with the event are present. The relation is `ge` and the threshold is 2. The baseline `b` is an integer `>= 1`. No other constraint is present. The composer is `prohibit_then_product`. The kernel is row gcd under `halt_self_loop`. A zero row stays zero. This family has no zero row.

The neighbourhood of an edge is the set used by `incident_neighbour`: every other carrier edge that shares an endpoint. Its size is the degree of that edge in the line graph of the carrier. EQ-014 is a different statement. It counts deadlock states of one prohibit template. It is not used here.

## Statement

Let `W` be the set of carrier edges whose neighbourhood has size at least 2.

Weight-effective cardinality and the raw removal-sensitive count equal `|W|`. The kernel-removal-sensitive count equals `|W|`. Kernel-effective cardinality equals `|W|`, except for one dissolve case named below.

Effective cardinality is the size of a smallest sublist that reproduces the object. The removal-sensitive count is leave-one-out. On the weight table those two counts agree. On the kernel they do not always agree.

## Argument

An edge whose neighbourhood has size 0 or 1 has present-neighbour count at most 1 in every state. The guard never holds. Deleting that constraint leaves every integer weight unchanged, and leaves the reduced kernel unchanged.

An edge `e` in `W` has a state in which its guard holds. For `either` or `form`, place any two neighbours of `e` present and keep `e` absent. For `dissolve`, keep `e` present as well. In that state the column of `e` equals `f*b` under the full list and equals `b` after the constraint on `e` is deleted. The raw tables differ. Every sublist that omits `e` differs from the full table in that column, so the smallest weight sublist is exactly the constraints on `W`. Each of those constraints is removal-sensitive.

The same state separates the kernel from the leave-one-out kernel. Each column is positive. The leave-one-out row agrees with the full row in every column except `e`, where the entries are `b` and `f*b`. Equal positive columns force the two row-gcds to agree, and the column of `e` then forces `f = 1`. That is outside the family. The reduced rows differ. The kernel-removal-sensitive count is `|W|`.

Kernel-effective cardinality can still be smaller than that leave-one-out count. A sublist that omits `e` and keeps any other constraint fails the same gcd comparison in a state where `e` fires and some edge does not. The only remaining candidate is the empty list. The empty list reproduces the kernel exactly when every row is a constant vector: in every state the set of edges whose guards hold is empty or is the entire edge set.

For `either` and for `form`, that constant-row condition fails whenever `W` is nonempty. In the state with exactly two neighbours of a wide edge present and that edge absent, the wide edge fires. Each of those two neighbours has at most one present neighbour, so it does not fire. `form` also refuses a present edge. The row is not constant. The empty list fails. Kernel-effective cardinality equals `|W|`.

For `dissolve`, the constant-row condition can hold. It holds exactly when the carrier's edges are a triangle or a three-edge star. Isolated vertices add no edge and do not change the edge set. In both graphs the line graph is the complete graph on three vertices, every neighbourhood has size 2, and the only state in which any guard holds is the state in which every edge is present. That row is the constant `f*b`. Every other row is the constant `b`. The kernel is the baseline kernel, so kernel-effective cardinality is 0, while `|W|` is 3 and the integer table is not the baseline table. Deleting one of the three constraints makes the full-present row unequal across columns, so the kernel-removal-sensitive count stays 3.

No other simple graph does this. A graph with four or more edges has an edge `e` and two neighbours `a` and `b`. In the state where exactly `e`, `a`, and `b` are present, `e` fires, and any further edge is absent, so that further edge does not fire. The row is not constant. A graph whose edges are not one of those two three-edge graphs, and which still has a narrow edge, produces a non-constant row as soon as one wide edge fires. The two three-edge graphs are the whole exception.

## Where a broader reading stops

A second copy of the same multiply on one edge of a triangle makes the product `f^2` on that edge. Both copies are required, and so are the multiplies on the other two edges. Declared length 4. `|W|` is 3. Effective cardinality and kernel-effective cardinality are 4.

A prohibit with the same guard, added beside the uniform multiplies on a triangle, zeros the prohibited column whenever the guard holds. The multiply on that edge no longer changes the table or the kernel. Effective cardinality stays 3, which is still `|W|`. The failure is the other reading: a constraint whose event lies in `W` can be redundant once the list is not the uniform family.

The `eq 1` template is a different guard. On the three-edge chain, `|W|` for threshold 2 is 1, and the uniform `eq 1` list does not have effective cardinality 1. The check computes that list. It does not execute `plans/atlas-006.json`.

A common-neighbour count is not this neighbourhood. A threshold other than 2, a missing edge, a factor of 1, and any composer other than `prohibit_then_product` are outside the statement. Equality of these cardinalities is not equality of a weight hash with its kernel hash. Occupation is not part of the statement. The identity does not appoint the next round.
