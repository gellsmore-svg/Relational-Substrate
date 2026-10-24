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
