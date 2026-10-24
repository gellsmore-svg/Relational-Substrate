# What the RRC-001 engine does not yet do

Read at the opening of the atlas continuation. This is a gap list, not a claim that any missing piece is a new dynamical primitive.

## Already available

- Complete pairwise carrier, edge order matching the Constraint Laboratory.
- Named families: unconstrained, state-independent rates, hard wedge, soft wedge, soft-wedge star boost.
- Exact strong lumpability, three augmentations, lumpable closure, recurrent classes.
- Parity-balanced stationary iteration, with a dense check at or below 1,024 states.
- Resumable item store, watchdog, plan hash, verify, report.

## Not available, and required for a constraint atlas

| Need | Why the current engine is short | Compilation status |
| --- | --- | --- |
| A list of elementary constraints with an explicit composition rule | Families are closed names. Cardinality and literals are not fields of a result | The list, once it is current-state weights on single toggles, is inside CL-T12 when every weight stays positive, and inside the existing prohibit when a weight is zero |
| Declared cardinality separate from K and J | The wedge families fold a count into one name. The expressivity note says a count is not one literal | Bookkeeping. Not a new event |
| Effective cardinality by ablation | Not computed | Same weights, cheaper description. An equivalence, not a new law |
| A hash of the weight table | Items cannot be compared without reading one another’s prose | Identity of integer tables |
| A carrier that is not the complete pair set | `build_weights` always allocates every pair. A chain on five nodes would be stored as a complete graph with ten bits | Restricting which pairs exist as bits shrinks the state. It does not add an event type. It is not a picture of the complete graph |
| Common-core observables other than lumpability and a path index | The path index was an instrument. The atlas core has to say what it measures | Definitions belong in the grammar note before cells run |
| History, independent hyperedges, multi-pair events | Excluded by the opening gate | Still excluded. An idea may name them. An experiment may not use them until a witness shows the current state cannot represent the behaviour |

## What the first code increment should add

A declarative compiler from a constraint list to an integer weight table, a carrier argument, the bookkeeping fields above, and one item type that reports the common core. No lumpability grid, no path index, and no replay of the wedge families in the first atlas batch.

## Status after the opening compiler

`src/rrc/constraints.py` compiles `opening-prohibit-multiply-v1`, including a listed carrier. `atlas_core` items report the common core in `docs/atlas-grammar.md`. Atlas-001 and atlas-002 used `rrc-0.2.0`. RRC-001 remains `rrc-0.1.0`: `run` refuses that plan, and `verify` compares a result with the engine string in its own plan.

## Status after rrc-0.3.0

`rrc-0.3.0` adds `kernel_sha256` under `row_gcd_halt_self_loop`, the `incident-neighbour-v1` predicate, stored integer weights, and `structure_sha256`. The definitions are in `docs/atlas-0.3.md`. Designated-edge tables of the opening composer are unchanged. Atlas-003, atlas-004, and atlas-005 later ran under this string. This paragraph does not freeze a plan.

Still excluded at that string: history, independent hyperedges, count predicates treated as one literal, and multi-pair events. Lumpability is not part of the atlas core. Continuous-time rates are not a clock.

## Status after rrc-0.4.0

The live engine string is `rrc-0.4.0`. It adds `incident_count` on the incident-neighbourhood bits: relation `eq` or `ge`, and an integer threshold. The definition is `docs/atlas-0.4.md`. `ge 1` matches incident present, and `eq 0` matches incident absent. That identity is EQ-017, a unit test, not a cell. Designated-edge tables and incident-neighbour tables are unchanged. Atlas-006 later ran fifteen cells under this string. This paragraph does not freeze a plan.

A common-neighbour count is still not compiled. History, independent hyperedges, and multi-pair events stay excluded. A count is still not one literal.
