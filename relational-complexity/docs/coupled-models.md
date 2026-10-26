# Coupled bit models

Status: typed readings. They are not a frozen round and not a scientific cell. The engine stays `rrc-0.4.0`. The method is `event-kernel-0.2.0`. It is not a new primitive of `rrc-0.4.0`. No intervention operator is defined. Atlas-017 was not rerun. This note adds no ledger row and no equivalence.

The functions are `src/rrc/coupled_models.py`. The checks are `tests/test_coupled_models.py`. Derived counts, the three-bit activity table, and the 3-bit versus 4-bit interface stay in `docs/state-event-families.md`. This note uses two declared bits and the clock `one_declared_event`.

Bit 0 and bit 1 are coordinates only inside a reading that names them. A projection is a partition of that reading's states. A defect of 0 is strong lumpability of that partition. A positive defect rules out strong lumpability of that partition. It does not exclude every history-dependent description. Where the projection is not exact, the quotient rows are absent. No row is filled in for them.

## Five readings

| Reading | Events | Classification |
| --- | --- | --- |
| Independent product | Toggle either bit. Weights 2 and 5 do not depend on the other bit | Ordinary single-toggle row |
| Rescaled rates | The same toggles. Weights 4 and 10 when bit 1 is 1 | Ordinary single-toggle row |
| Support constraint | Bit 0 toggles only while bit 1 is 1 | Ordinary single-toggle row |
| Coupled agreement | One joint step between states 0 and 3 | Outside the one-step single-toggle support |
| Family bit | The family is absent, listed, or flipped with the edge | Three different objects |

## Independent product

Every state offers a toggle of bit 0 with weight 2 and a toggle of bit 1 with weight 5. The normalised probability of the bit-0 toggle is `2/7`. The normalised probability of the bit-1 toggle is `5/7`. Each one-bit projection is exact. The quotient on bit 0 is `5/7` on the diagonal and `2/7` on the off-diagonal. The quotient on bit 1 exchanges those two values. The second bit is extra state relative to the first, and it is still an ordinary listed bit. Neither projection is a new process.

## Rescaled rates

When bit 1 is 0 the weights remain 2 and 5. When bit 1 is 1 they are 4 and 10. The integer row from state 0 is weights 2 and 5. The integer row from state 2 is weights 10 and 4. The normalised probabilities are the same as the independent product, including `2/7` and `5/7`, and both projections stay exact. The integer table depends on bit 1. The normalised one-bit laws do not. That cancellation is a fact about these weights. It is not a new event kind.

## Support constraint

When bit 1 is 0 the only event toggles bit 1, with weight 1. When bit 1 is 1, bit 1 toggles with weight 5 and bit 0 toggles with weight 2. Every event has Hamming distance 1. State 0 has one enabled event and state 2 has two.

The projection onto bit 1 is exact. Label 0 moves to label 1 with probability `1`. Label 1 moves to label 0 with probability `5/7` and stays with probability `2/7`. The projection onto bit 0 is not exact. Its defect is `2/7`, and its quotient rows are absent. Bit 1 is required for a Markov description of this kernel under that partition. Bit 1 remains a listed bit of the same four-state law. The support constraint is a hard zero in a current-state weight table.

## Agreement and conjugacy

The one-bit toggle sends state 0 to state 1 and state 1 to state 0, each with probability `1`. The coupled list is the atlas-017 coupled list: a joint from state 0 to state 3 and a joint from state 3 to state 0. The map `0 → 0`, `1 → 3` lands on `{0, 3}`. That image is invariant. The restricted rows equal the one-bit rows. The reversed map `0 → 3`, `1 → 0` is also a conjugacy, because this law is a two-cycle. Matching both orientations does not make every bijection a conjugacy.

The map `0 → 0`, `1 → 1` is injective and its image is `{0, 1}`. State 0 moves to state 3, so that image is not invariant. No restricted row is built for it. A bijection of states is not a dynamical correspondence.

States 1 and 2 have no event. Each completes by `halt_self_loop`, so `{1, 2}` is invariant, and its law is halt. Halt on that pair is not the one-bit toggle.

The free product is the atlas-017 all-ones catalogue: one toggle of either bit from every state. The same map onto `{0, 3}` has an image that is not invariant, because state 0 can move to state 1 or state 2. No restricted row is built. Reachability is a different clock. The paths `0 → 1 → 3` and `0 → 2 → 3` use two single toggles and still reach state 3 from state 0. The joint target is not a one-step successor. No universal impossibility is claimed.

The projection of the joint law onto either bit has defect `1`. Those quotient rows are absent. The full four-state law is not the one-bit law. Only the invariant image matches.

## Family membership

This carrier is one edge. A fixed instrument stores that edge and not a family coordinate, so it has 2 states. The earlier changing-family witness uses two edges and has 4 states without the family bit. The counts differ because the carriers differ.

Encoding the family as bit 1 gives 4 states. Toggling the edge and toggling the family bit are one-bit events. That bit is `reducible_to_listed_bit`. The split family has block count 2 and the joined family has block count 1. Those counts are a reading of the bit. They are not another state coordinate.

One joint event from state 0 to state 3 flips the edge bit and the family bit together. The Hamming distance is 2, so the target is outside the one-step single-toggle support. The event kind is the joint kind of `event-kernel-0.2.0`. It is the same distance claim as one step of the coupled list, read here as an edge plus a family bit. It is not a new primitive of `rrc-0.4.0`.

## What this note leaves open

No intervention operator is defined. A finite-horizon contrast and a sequential quotient are not computed. `COV-HIGHER-ORDER-STATE` and `COV-DYNAMICAL-PROPAGATION` stay open. ATLAS-Q01 through ATLAS-Q15 stay open. `IDEA-L23` stays open and is not selected. The fractions `2/7` and `5/7`, and the defects `2/7` and `1`, are values of these readings. They are not targets. Atlas-017 was not rerun.
