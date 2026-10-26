# Engine rrc-0.3.0

Status: definition and validation. No scientific cell uses this engine yet.

`rrc-0.1.0` is RRC-001. `rrc-0.2.0` is atlas-001 and atlas-002. Those plans keep their own strings. `run` refuses them. `verify` still accepts their results.

`rrc-0.3.0` keeps the opening composer. A designated-edge list compiled here has the same integer table as under `rrc-0.2.0`. The new fields are the kernel fingerprint, the incident-neighbour predicate, stored weights, and a structure hash of the present graph.

## Kernel

The clock is `halt_self_loop` only.

For a state `x` and a candidate event `e`, `P(e | x) = w(e, x) / sum_f w(f, x)` when the row sum is positive. A zero row stays the zero row. The self-loop is the existing halt convention. It is not a relational event.

`reduce_weight_table` divides each positive row by the gcd of its entries, in integer arithmetic. A zero row is left as zeros. Negative weights are rejected. Tables of different shapes are not equal.

`kernel_sha256` is the existing canonical hash of that reduced table. The method name on the result is `row_gcd_halt_self_loop`. This fingerprint is not a continuous-time rate and not a relabelling.

Two empty constraint lists with baselines `k` and `1`, for an integer `k > 1`, have different integer tables and the same kernel. That identity is EQ-008. It is a method check, not a cell.

`kernel_effective_cardinality` and `kernel_removal_sensitive_count` repeat the existing ablation on the reduced table. Above 16 declared constraints both are null and `kernel_ablation_method` is `not_computed_above_16`. Declared J stays the length of the list. `kernel_method` on the result is the fingerprint method. It is not the ablation method.

## Incident neighbour

Grammar id `incident-neighbour-v1` when every constraint uses this condition. A mix with designated edges is `opening-plus-incident-v1`. An empty list stays `opening-prohibit-multiply-v1`.

`when.kind` defaults to `designated_edge` when `when.edge` is present, so an existing spec is unchanged. `incident_neighbour` rejects a designated edge.

The neighbourhood is every other carrier edge that shares an endpoint with the event. It is read in carrier order, on current presence. Polarity `present` matches when at least one such edge is present. Polarity `absent` matches when none is. This is a state-dependent OR or NOR. A static fact that two named edges share a vertex is not this predicate.

On a three-edge chain the end edge has one incident neighbour, so the predicate matches a designated rule on that neighbour. On a three-edge branch the first listed edge is incident to both other edges, so the OR differs from reading only the second listed edge. On a disconnected pair the event has an empty neighbourhood: present polarity never matches, and absent polarity matches in every state.

The predicate is not a new dynamical primitive. Positive weights remain current-state single toggles inside CL-T12 by expansion. Declared J stays 1. `max_positive_k` counts designated-edge features only, so an OR is not recorded as one literal.

For present polarity and neighbourhood size `m > 0`, `expansion_j` is `2^m - 1` exact minterms and `expansion_k` is `1 + m`, plus one when the action is `form` or `dissolve`. Each neighbourhood state matches one conjunction, so the product composer applies the factor once. A product of single-literal multiplies would stack the factor.

For absent polarity, the expansion is one conjunction: `expansion_j` is 1 and `expansion_k` is `1 + m`, plus the action literal.

When `m` is 0 and the polarity is present, `expansion_j` and `expansion_k` are 0 and the guard never matches. When `m` is 0 and the polarity is absent, `expansion_j` is 1 and the guard matches in every state. That is an unconditional multiply or prohibit of the event.

A prohibit expansion is the existing hard zero. It is not the positive CL-T12 construction.

A count of incident edges remains IDEA-C08. It is not this Boolean predicate.

An imposed dependency arc runs from each incident neighbour to the event. An empty neighbourhood adds no arc. Mutual incident constraints on adjacent edges can make `imposed_rule_dependency.has_cycle` true. That flag is rule text. It is not an observed oscillation.

A uniform template applied to every carrier edge is the label-free instrument. A rule on one named edge is a designated-label instrument. Permutation covariance is tested for the uniform template. It is not claimed for a named edge.

## Structure hash

`structure_sha256` hashes, for every state, the non-increasing degree sequence, the non-increasing component sizes with isolates included, the component count, whether the present graph has a cycle, and the number of present edges. The method name is `present_degree_components_cycle`.

On a forest carrier, every state has `components = n - present edges` and `has_cycle` false. That identity is a validation check. It is not a scientific finding.

Atlas-001 and atlas-002 results do not carry this hash. They are not rewritten.

## Stored weights

A new `atlas_core` result stores the integer weight table. `verify` checksums it when the result engine is not `rrc-0.1.0` or `rrc-0.2.0`: the shape, `weight_sha256`, `kernel_sha256`, and a 64-hex `structure_sha256`. It does not recompile the constraints.

## Still excluded

History, independent hyperedges, count predicates treated as one literal, and multi-pair events. Continuous-time rates are not a clock of this engine.
