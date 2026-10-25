# State, event, and interface families

Status: typed fixtures. They are not a frozen round and not a scientific cell. The engine stays `rrc-0.4.0`. No weight table is compiled here. ATLAS-Q15 stays open. `IDEA-L22` stays partial. `IDEA-L23` stays open and is not selected. `COV-HIGHER-ORDER-STATE` and `COV-DYNAMICAL-PROPAGATION` stay open.

The functions are `src/rrc/state_families.py`. The checks are `tests/test_state_families.py`. The activity table used as the extended-state example remains EQ-027. That equality is a reduction to listed edges. It is not a new primitive.

The families below are separate. A shared word such as "state" does not make two readings the same object. Each reading records its input, output, state, transition law, event support, constraints, permitted relabelling, recoverability, and further composition.

## Derived coordinate

| Field | Value |
| --- | --- |
| Input | A pair mask in `0 .. 3`, the presence bits of edges `(0,1)` and `(1,2)`. |
| Output | The number of present bits. |
| State | The pair mask. The count is a value of that mask. |
| Transition law | None. The count does not add a step. |
| Event support | None. |
| Constraints | None. |
| Permitted relabelling | Swapping the two pair bits preserves the count. The geometric names move: bit 0 named `(0,1)` becomes the bit named `(1,2)`. A permutation is an equivalence of a weight table only when the events and the weights move with the bits. The count witness has no weight table. |
| Recoverability | The count is not injective. Masks 1 and 2 both have count 1. |
| Further composition | A function of the count is a function of the mask. |
| Classification | `reducible_observation`. No new bit. |

## Extended state

| Field | Value |
| --- | --- |
| Input | Three listed bits `(pair0, pair1, activity)`. |
| Output | The three-bit state. There are 8 states. |
| State | Ordinary pair state once the third bit is a listed edge. |
| Transition law | Current-state weights on single toggles. The eight activity rows are EQ-027. |
| Event support | One-bit toggles of the three listed bits. |
| Constraints | The activity rows. The pair bits do not determine the row. |
| Permitted relabelling | A bit permutation carries the event columns and the weights. The geometric names are part of the declaration that moves with the permutation. |
| Recoverability | States 1 and 5 share the pair mask `01` and differ in the third bit. The derived count of that mask is 1 for both states, so the count does not separate them. |
| Further composition | A label of the three-bit state is a label of listed pair state. |
| Classification | `reducible_to_listed_bit`. |

Both of the following hold. They are different claims. Relative to the two pair bits, states 1 and 5 share the projected mask and differ in the third coordinate. Relative to the three listed bits, the activity table is ordinary pair state. EQ-027 records the second claim for this table. A freely toggling third bit, with every weight equal to 1, gives the same pair-toggle probability at both values of that bit. That free bit is not a witness of interaction.

## Joint event

| Field | Value |
| --- | --- |
| Input | The same three-bit state as the extended family. |
| Output | A proposed next state. |
| State | Unchanged. The step does not add a bit. |
| Transition law | No current-state weight on the one-step single-toggle support assigns this step a positive probability. |
| Event support | The permitted support in this scope is one bit flip in one step. |
| Constraints | None added. |
| Permitted relabelling | A bit permutation preserves Hamming distance. |
| Recoverability | The target is a state of the same 8-element space. |
| Further composition | Two successive single toggles are the existing clock, applied twice. |
| Classification | `outside_one_step_single_toggle`. |

From state 0 the one-step successors are states 1, 2, and 4. State 5 flips bit 0 and bit 2 together. The Hamming distance is 2, so state 5 is not a one-step successor. The paths `0 → 1 → 5` and `0 → 4 → 5` each use two single toggles. An extra intermediate state, or a clock that observes only every second toggle, can carry the same pair of bit changes. This scope is the same three-bit state, the one-step clock, and the single-toggle support. No universal impossibility is claimed. History at an unchanged current state is a different gate failure and is not given an engine change.

## Identified interface

| Field | Value |
| --- | --- |
| Input | Edges `(0,1)`, `(1,2)`, `(2,3)`. |
| Output | One carrier state of 3 bits. There are 8 states. |
| State | Listed pair state. |
| Transition law | Current-state weights on single toggles of the three edges. This witness puts no constraint on those weights. |
| Event support | One-bit toggles. |
| Constraints | None in this witness. |
| Permitted relabelling | A carrier automorphism moves edges, events, and weights together. |
| Recoverability | Each edge is one bit of the state. |
| Further composition | A label of this state is a label of listed pair state. |
| Classification | `reducible_to_listed_carrier`. |

The shared edge `(1,2)` occurs once. A toggle of that edge is one event.

## Duplicated interface

| Field | Value |
| --- | --- |
| Input | Four bits: `(0,1)`, copy A of `(1,2)`, copy B of `(1,2)`, and `(2,3)`. |
| Output | One product state of 4 bits. There are 16 states. |
| State | Listed pair state of those four bits. |
| Transition law | The free product toggles one of the four bits. The coupled update flips both copies in one step. |
| Event support | One-bit toggles on the free product. |
| Constraints | Agreement of the two copies is the subset in which copy A equals copy B. That subset has 8 states. It is not an extra bit. |
| Permitted relabelling | Swapping the two copy bits preserves agreement. |
| Recoverability | On an agreement state, either copy and the two outer bits recover the identified 3-bit state. |
| Further composition | The map `(e0, e1, e2) → (e0, e1, e1, e2)` is a bijection from the identified carrier onto the agreement set. One toggle of the identified shared edge matches the joint flip of both copies. |
| Classification | The free product is `single_toggle_on_more_bits`. The coupled update is `outside_one_step_single_toggle`. |

The widths are 3 and 4. The correspondence is not a bit permutation of one table. Toggling one copy leaves the agreement set. Toggling both copies stays in the agreement set and has Hamming distance 2. From state 0 that coupled update lands on state 6, which is not a one-step successor of the 4-bit free product. States in which the copies differ are states of the free product. A free extra copy is not, by itself, an interaction. The identified coupling is ordinary one-toggle grammar on the 3-bit carrier.

## Changing block family

| Field | Value |
| --- | --- |
| Input | Carrier edges `(0,1)` and `(1,2)`, and a declared family of blocks. |
| Output | The present-edge mask, or that mask together with a family bit. |
| State | A fixed instrument stores the mask only: 4 states, and one family for every mask. The encoded state is `mask | (family << 2)`: 8 states. |
| Transition law | The encoded family bit is a listed coordinate with the single-toggle law. The fixed instrument has no family event. |
| Event support | One-bit toggles of whichever state was declared. |
| Constraints | None in this witness. |
| Permitted relabelling | Renaming the family bit is a listed-bit permutation when the event moves with the bit. |
| Recoverability | The mask does not determine the family. Mask 0 with the split family and mask 0 with the joined family are different declarations. |
| Further composition | Applying one family to every mask is the fixed instrument. A second family is a different instrument, or a bit in the encoded state. |
| Classification | The family bit alone is `reducible_to_listed_bit`. Changing an edge bit and the family bit in one step is `outside_one_step_single_toggle`. |

The split family is the two blocks `[(0,1)]` and `[(1,2)]`, so the block count is 2. The joined family is the one block `[(0,1), (1,2)]`, so the block count is 1. Encoding them as states 0 and 4 keeps the present edges empty and changes only the family bit. The Hamming distance is 1, and state 4 is a one-step successor of state 0. State 5 turns on edge `(0,1)` and switches to the joined family. The Hamming distance from state 0 is 2, so state 5 is not a one-step successor. The paths `0 → 1 → 5` and `0 → 4 → 5` each use two single toggles.

Potential intersection and realised intersection are observations of one fixed family. In `src/rrc/composition.py` those readings are `active_intersection_labels` and `realised_intersection_labels`. They are not a family that changes with the state. A partial family is not a full cover. Overlapping blocks are not a tree.

## Intervention

No intervention operator is defined. The record in `intervention_report` stores no operator, no distribution, and no comparison law. Propagation stays undefined. A static dependency path is bookkeeping on a constraint list. It is not a cascade, and no length is preferred. A difference of toggle weights inside one current-state table is a conditional weight. It becomes an intervention only when a comparison law is declared independently of the observed table. That declaration is not made here. `IDEA-L23` is not selected.

## What this note leaves open

The gate in `docs/compilation-gate.md` is unchanged. A joint two-bit step and a history-dependent row at an unchanged current state still fail that gate. Neither failure is given an engine change. The duplicated coupled update fails the gate only under the 4-bit one-step single-toggle representation. The same change of the shared edge is one toggle in the identified representation. Expressivity claims stay inside the representation and the clock that were named.

No atlas round is frozen. Atlas-014 and atlas-015 are not rerun. Their defects are not targets. No ledger row is added. No equivalence is added. Exact one-step probabilities for a declared event list are in `docs/event-kernel.md`. That note is not a frozen round.
