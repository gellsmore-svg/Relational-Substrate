# atlas-017 observations

A map of one verified sample. The question stays open.

Plan hash `61b502a25bf1689d9e7f7c6bac461fffed24983cde804c7ec6ba785c8b4ce143`. Definitions commit `e189bd2`. Freeze `070fc79`. All 6 items completed in one invocation, 0.983487 seconds. Verify printed `verified`. The generated table is `reports/atlas-017.md`. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. Method `event-kernel-0.1.0`. Clock `one_declared_event`. `new_primitive` is false on every cell. No occupation is stored. No stationary distribution is stored. No carrier weight table is stored. `results/atlas-016` was not rerun.

The state of each cell is the integer mask named in the plan. No cell adds a coordinate. The question of the round is ATLAS-Q06. It stays open. ATLAS-Q15 is not this round's question, and it stays open. No intervention operator is defined.

## Six laws

`A17-g0` is the two-bit catalogue with every toggle weight equal to 1. Eight events. Every row is `normalised_events`, and every state has two enabled events. From state 0 the probabilities are `0`, `1/2`, `1/2`, `0`. State 3 receives `0`. From state 1 the probabilities are `1/2`, `0`, `0`, `1/2`. From state 2 they are `1/2`, `0`, `0`, `1/2`. From state 3 they are `0`, `1/2`, `1/2`, `0`. Every positive off-diagonal target differs from its source by one bit. This is the ordinary one-step single-toggle support. The same catalogue is the free product of two copy toggles, so that reading is not a second cell.

`A17-g1` uses the same four states and the same clock. From each state the events are a toggle of bit 0 with weight 1 and a joint step by xor 3 with weight 1. Eight events. Every row is `normalised_events`. From state 0 the probabilities are `0`, `1/2`, `0`, `1/2`. From state 1 they are `1/2`, `0`, `1/2`, `0`. From state 2 they are `0`, `1/2`, `0`, `1/2`. From state 3 they are `1/2`, `0`, `1/2`, `0`. On each row one positive target differs by one bit and one differs by two bits. State 3 is outside the one-step single-toggle successors of state 0. A path of two single toggles still reaches it: state 0 to state 1, then state 1 to state 3. No universal impossibility is claimed.

`A17-identified` is one bit, toggled both ways with weight 1. From state 0 the probability of state 1 is `1`. From state 1 the probability of state 0 is `1`. Each step has Hamming distance 1.

`A17-coupled` names only the joint step from state 0 to state 3 and the joint step back. The probability of each of those steps is `1`. Hamming distance is 2. States 1 and 2 have no event. Their completions are `halt_self_loop`, the enabled count is 0, and the probability `1` sits on the diagonal. That diagonal is a completion, not an event.

The declared image sends identified state 0 to duplicated state 0 and identified state 1 to duplicated state 3. Agreement on the duplicated states is `{0, 3}`. The coupled probabilities on that image match the identified probabilities. The widths are 1 and 2, so this is not a bit permutation of one table. The free-product law does not stay on the agreement set: from state 0 its probabilities on states 1 and 2 are `1/2` and `1/2`, and its probability on state 3 is `0`.

`A17-halt` is one state and an empty event list. The probability is `1`. The completion is `halt_self_loop`. The enabled count is 0. `A17-noop` is that state with one noop of weight 1. The probability is `1`. The completion is `noop_event`. The enabled count is 1. The two probability rows match. The completions do not. A halt self-loop is not an event.

## What the slice does not say

The all-ones catalogue and the identified toggle reduce to the one-step single-toggle grammar on the states and clock named here. The joint cell and the coupled cell are outside that one-step support. They are not a new coordinate, and they are not a new primitive of `rrc-0.4.0`. A different clock, a split intermediate state, or another encoding may reproduce a joint step. This sample does not test those reductions, and it does not deny them. The image agreement is a comparison of these two stored rows. It is not a registered equivalence. No pattern is opened. The probabilities `1/2` and `1` are the stored rows of this sample. They are not a follow-up target. ATLAS-Q06 stays open: the library is larger than these six catalogues. ATLAS-Q15 stays open. No intervention operator is defined.
