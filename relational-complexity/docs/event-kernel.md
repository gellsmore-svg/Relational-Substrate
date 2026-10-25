# Event kernel

Status: typed fixtures. They are not a frozen round and not a scientific cell. The atlas engine stays `rrc-0.4.0`. The method in `src/rrc/event_kernel.py` is `event-kernel-0.1.0`. It is not a new primitive of that engine. No intervention operator is defined. ATLAS-Q15 stays open. EQ-027 is not rerun.

The clock is one declared event. Each event names its source, its target, its kind, and a nonnegative integer weight. Weights that share a source and a target are added. A positive row is divided by its sum with rational arithmetic. A weight of 0 adds nothing. Listing the same events in another order leaves the sums unchanged.

A row with no positive weight is completed by `halt_self_loop`. That self-loop is not an event. A no-op is a declared event whose target is its source. Both records can put probability `1` on the diagonal. The completions stay different.

## Comparison

| Family | State | Declared events | One-step law on the witness | Reading |
| --- | --- | --- | --- | --- |
| Single toggle | One row per mask | Flip one named bit | The probability is that bit's weight over the row sum | The existing one-step support |
| Halt row | The same states | No positive weight | Probability `1` on the source, and the completion is `halt_self_loop` | A completion, not an event |
| No-op | The same states | A no-op of positive weight | Probability `1` on the source, and the completion is `noop_event` | An event, including when the probability matches the halt row |
| Summed names | Three states in the witness | Two names for one target, weights `1` and `3`, and a second target of weight `2` | Probabilities `2/3` and `1/3` | The weights add before the division |
| Joint event beside one toggle | Two bits | Flip bit 0, and flip both bits, each of weight `1` | From state 0 the probabilities are `1/2` to state 1 and `1/2` to state 3 | State 3 has Hamming distance 2. It is outside the one-step single-toggle support. Two single toggles can reach it |
| Identified interface | One shared bit | One toggle of weight `1` | Probability `1` to the other state | Ordinary one-bit support |
| Free copies | Two copy bits | One toggle of either copy, weight `1` | From state 0 the probabilities are `1/2` and `1/2` to the two single-copy states | The step leaves the agreement set |
| Coupled copies | Two copy bits | Flip both copies, weight `1` | Probability `1` from state 0 to state 3 | The same shared-bit change as the identified toggle. Hamming distance is 2 |

The single-toggle row is the control. On two bits with every weight equal to `1`, state 0 moves to state 1 or state 2, each with probability `1/2`. State 3 receives probability `0` in that one step.

The joint witness uses the same two bits and the same clock. State 0 moves to state 1 or state 3, each with probability `1/2`. State 3 is the joint flip. The one-step single-toggle successors of state 0 are states 1 and 2. The two laws differ on this state space and this clock. A path of two single toggles still reaches state 3. No universal impossibility is claimed. A larger state that splits the joint step into two microsteps is a different clock or a different state space.

The identified carrier is one bit. Its toggle has probability `1`. The duplicated carrier is two copies of that bit. Agreement is states 0 and 3. The map sends the identified states onto that pair. The coupled update follows the map: identified state 0 goes to identified state 1, and duplicated state 0 goes to duplicated state 3. The free product from state 0 moves to state 1 or state 2 and leaves the agreement set. The map is a bijection of those two state sets. The coupled law matches the identified law on the image. The free-product law does not.

## What this note leaves open

No atlas round is frozen. No stationary distribution is stored. No ledger row is added. No equivalence is added. Atlas-016 is not rerun, and its fractions are not targets. A joint event in this note is a support difference under the named clock. It is not a claim that every encoding reduces, and it is not a claim that none does. No intervention operator is defined.
