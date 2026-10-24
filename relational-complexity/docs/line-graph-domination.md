# Incident prohibition and line-graph total domination

Status: scoped identity, checked by `tests/test_domination.py`. Not a new scientific round. Not a property of every grammar.

## Rule

The carrier is a simple undirected graph. Its edges are listed in a fixed order. On every carrier edge `e` there is one constraint: prohibit either toggle of `e` when at least one other carrier edge that shares an endpoint with `e` is present. Baseline is 1. The composer is `prohibit_then_product`. The clock is `halt_self_loop`.

The predicate is `incident_neighbour` with polarity `present`. It reads current presence. A static note that two edges share a vertex is not, by itself, the weight.

## Statement

Let `L` be the line graph of the carrier: one vertex per carrier edge, and an edge of `L` when the two carrier edges share an endpoint.

In state `S`, the weight of event `e` is 0 when the open neighbourhood of `e` in `L` meets `S`, and 1 otherwise. The row of `S` is entirely zero exactly when every vertex of `L` has a neighbour in `S`. That is the definition of a total dominating set of `L`. Members of the set do not dominate themselves.

Under `halt_self_loop` a zero row is completed by a self-loop, so these states are absorbing. The engine counts them as deadlock states.

## Counts checked against an independent enumeration

| Carrier | Line graph | Deadlocks |
| --- | --- | --- |
| Three-edge chain | Path on three vertices | 3 |
| Three-edge branch, and a triangle | Complete graph on three vertices | 4 |
| Four-edge cycle | Cycle on four vertices | 9 |
| Two disjoint edges | Two isolated vertices | 0 |
| Two adjacent edges | One edge | 1 |

The two disjoint edges have no total dominating set, because an isolated vertex of `L` has no neighbour. The present-polarity guard on an empty neighbourhood never matches, so those columns stay at baseline and no row is zero. The same count comes from both readings.

The three-edge chain has 3 deadlock states and more than 3 recurrent classes. A recurrent class is not the same object as a total dominating set.

The triangle and the three-edge branch have the same weight table. Their line graphs are the same complete graph on three vertices, and the rule depends on that adjacency only.

Atlas-004 stored deadlock counts for `A4-chain-inc-pro`, `A4-branch-inc-pro`, `A4-cycle-inc-pro`, and `A4-disconnected-inc-pro` agree with this enumeration. Those cells were not rerun.

## Where the identity stops

The deadlock set changes when the template is not on every edge. Dropping one chain constraint leaves a column at baseline, so there is no zero row, while total dominating sets of the full line graph still exist.

A multiply does not write zeros. Polarity `absent` is a different predicate. Action `form` or `dissolve` zeros only one direction. A designated-bit prohibit is not this neighbourhood. Equality of deadlock counts is not equality of weight tables once the line graphs differ.

The identity is not a theorem about occupation, about the incident multiply template, or about any other composer. It does not make domination theory the next round. EQ-014 records it as a method identity.
