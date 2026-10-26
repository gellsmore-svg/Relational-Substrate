# Event kind and update semantics

Status: typed validation. It is not a frozen round and not a scientific cell. The atlas engine stays `rrc-0.4.0`. `event-kernel-0.1.0` is unchanged. `event-kernel-0.2.0` is a separate method. It is not a new primitive of `rrc-0.4.0`. No intervention operator is defined. Atlas-017 was not rerun.

`kernel` stores `event-kernel-0.1.0`. Its kind check is the old one. A no-op must stay in its source state. A toggle or a joint must change the state. The label is not checked against Hamming distance. A toggle from state 0 to state 3 is accepted. A kind named `transition` is rejected.

`strict_kernel` stores `event-kernel-0.2.0`. The caller passes a bit width or passes none. The function does not infer a bit width from a power-of-two state count.

| Declared width | Kind | Rule |
| --- | --- | --- |
| Width `w`, with `n_states = 2^w` | `noop` | Source and target are the same state |
| Width `w` | `toggle` | Hamming distance is exactly one bit |
| Width `w` | `joint` | Hamming distance is at least two bits |
| Width `w` | `transition` | The state changes. The distance is not a claim |
| No width | `noop` | Source and target are the same state |
| No width | `transition` | The state changes. The indices are not bits |
| No width | `toggle` or `joint` | Rejected |

A joint has no smaller cap than the width. Both states already lie in the mask, so the distance is at most `w`. A flip of every bit is a joint when `w` is at least 2. On a one-bit mask every change has distance 1, so a joint is rejected.

A weight of 0 is still parsed. A zero-weight toggle whose distance is not 1 is rejected. A zero-weight toggle whose distance is 1 is kept in the event list and adds no mass. The row then completes by `halt_self_loop` unless some other positive event is present.

Two events with the same source and target add their positive weights. Their kinds stay on the event list. The probability row does not recover the kinds. A joint and a transition can share one probability matrix and remain different records. Duplicate names are rejected. Listing the events in another order leaves the sums unchanged.

The six Atlas-017 catalogues meet these checks. The stored results still say `event-kernel-0.1.0`. The worker item calls `kernel`, not `strict_kernel`. This note adds no ledger row and no equivalence. Typed couplings that call `strict_kernel` are in `docs/coupled-models.md`. They are not a frozen round.
