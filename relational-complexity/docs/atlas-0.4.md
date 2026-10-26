# Engine rrc-0.4.0

Status: definition and validation. This note is not a scientific cell. Atlas-006 later ran under this string.

`rrc-0.3.0` remains the engine of atlas-003, atlas-004, and atlas-005. Those plans keep their own strings. `run` refuses them. `verify` still accepts their results. Designated-edge tables and `incident_neighbour` tables compiled here match the tables those rounds stored.

`rrc-0.4.0` adds one predicate, `incident_count`. It reads the same neighbourhood as `incident_neighbour`: every other carrier edge that shares an endpoint with the event, in carrier order, on the current presence bits. It does not read a common-neighbour count. A common neighbour is a node adjacent to both endpoints. That function is still outside this engine.

## Condition

`when.kind` is `incident_count`. The condition does not take `edge` or `polarity`. `when.relation` is `eq` or `ge`. `when.threshold` is an integer greater than or equal to 0. A Boolean is rejected. The effect and the action are the opening composer: `prohibit` or `multiply`, and `either`, `form`, or `dissolve`.

The guard counts how many neighbourhood bits are present, then applies the relation, then the action. Declared cardinality stays the length of the constraint list. One count is one declared constraint.

Grammar id `incident-count-v1` when every constraint is this kind. A list that also contains `designated_edge` or `incident_neighbour` is `mixed-current-state-v1`. A list of only `incident_neighbour`, or that kind mixed only with designated edges, keeps the `rrc-0.3.0` grammar ids. An empty list stays `opening-prohibit-multiply-v1`.

## Identities

`ge 1` is the present polarity of `incident_neighbour`. `eq 0` is the absent polarity. Both identities include the empty neighbourhood: `ge 1` never matches, and `eq 0` matches in every state. EQ-017 records them. The evidence is `tests/test_count.py`. It is a method identity, not a cell.

On a neighbourhood of one edge, `eq 1` and `ge 1` are the same guard. On a neighbourhood of two or more edges they are not. For the middle edge of the three-edge chain, the neighbours are the two end edges. With a multiply by 3:

- state `0b101`, both neighbours present: `ge 1` weighs 3, `eq 1` weighs 1, `ge 2` weighs 3;
- state `0b001`, one neighbour present: `ge 1` weighs 3, `eq 1` weighs 3, `ge 2` weighs 1.

`ge 0` holds in every state. It is one empty conjunction. It is not the absent polarity once the neighbourhood can be nonempty.

For one multiply on every carrier edge, factor at least 2, threshold `ge 2`, and no other constraint, weight-effective cardinality equals the number of edges whose neighbourhood has size at least 2. EQ-020. The dissolve kernel has one exception. The argument and the counterexamples are in `docs/incident-count-cardinality.md`. That identity is not a cell.

A threshold the neighbourhood cannot reach never matches. Its expansion is empty.

## Expansion

The count is a compound feature. It is not one literal, and `max_positive_k` still ignores it. Positive weights remain current-state single toggles. The result field `new_primitive` stays false. A prohibit expansion is the existing hard zero, not the positive CL-T12 construction.

`expansion_j` is the number of exact minterms. `expansion_k` follows the incident-neighbour convention, `1 + m` plus one when the action is `form` or `dissolve`, except where the note below says the conjunction is empty.

For neighbourhood size `m`:

- `ge 0`: `expansion_j` is 1 and `expansion_k` is 1, plus the action literal. No neighbourhood literal appears.
- `eq 0` and `m = 0`: `expansion_j` is 1 and `expansion_k` is 1, plus the action literal.
- `eq k` with `0 < k <= m`: `expansion_j` is the binomial coefficient `C(m, k)` and `expansion_k` is `1 + m`, plus the action literal.
- `ge k` with `0 < k <= m`: `expansion_j` is the sum of `C(m, i)` from `i = k` to `m`, and `expansion_k` is the same `1 + m` plus the action literal. For `k = 1` that sum is `2^m - 1`, matching present polarity.
- a threshold above `m`, and `ge 1` at `m = 0`: `expansion_j` and `expansion_k` are 0.

On the middle edge, `m = 2`, so `eq 1` has `expansion_j` 2, `ge 2` has 1, and `ge 1` has 3. Declared J stays 1.

An imposed dependency arc still runs from each incident neighbour to the event. A mutual pair of count constraints on adjacent edges can set `imposed_rule_dependency.has_cycle`. That flag is rule text. It is not an observed cascade.

A uniform template copied onto every carrier edge is checked for path reversal. A rule on one named edge is a designated instrument.

## Still excluded

History, independent hyperedges, multi-pair events, and any count other than this incident-edge count. A common-neighbour count is one of those excluded counts. Continuous-time rates are not a clock of this engine. Atlas-006 froze uniform `eq 1` and `ge 2` multiplies with this predicate. Other thresholds, prohibit counts, and a common-neighbour count are not those cells.
