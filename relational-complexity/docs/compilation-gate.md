# Compilation gate for the opening model

The permanent test is the one in `constraint-lab/docs/scientific-plan-discipline.md` (commit `1b9d93d5`) together with `constraint-lab/formal/expressivity-boundaries.md` (commit `9fe848a9`).

## What RRC-001 wants to represent

A finite set of labelled nodes. A state is a simple undirected graph on those nodes: each potential pair is present or absent. One step toggles one pair. The weight of that toggle is a function of the current graph. Empty weight rows halt.

The scientific questions are about hiding part of that graph, not about adding a transition type.

## Gate answers

| Proposed behaviour | Represented state | Event support and clock | Verdict |
| --- | --- | --- | --- |
| Unconstrained toggle | Current pair bits. Identical state means identical bitset | Single pair toggle. One event per toggle. Halt is a marked self-loop | Already the laboratory baseline. No new mechanism |
| Weight depends on the number of common neighbours of the toggled pair | Same pair bits. The count is a function of those bits | Same support, except hard zeros may delete some toggles | Current-state weight. Not a new axis |
| Hard ban on forming a pair with no common neighbour | Same | Support shrinks. CL-T12 covers strictly positive weights only. Hard zero is the laboratory's existing `prohibit` | Trade-off recorded: this is admissibility inside the same support family, not a new primitive. CL-T12's positive-weight construction does not by itself include the zeros |
| Two microstates share an external bit pattern and have different next-step laws | The external pattern is a projection, not the state | The full chain is still current-state Markov | The projection fails strong lumpability. Restoring a Markov description means keeping more of the current state, or proving a sufficient statistic. That is a representation change. It is not history and it is not a new event type |
| The lumped interface chain, when it is Markov | Blocks of the full state | One step still flips at most one pair, so the interface changes by at most one visible bit, or stays | If the block row is a function of the block, the interface is a lazy single-toggle chain whose weights may differ from the original rule. Same event shape, possibly transformed weights. If the row is not a function of the block, there is no closed interface grammar of this form |

CL-T12 says every strictly positive current-state weight function on this single-toggle support can be compiled into the existing grammar if K and J are allowed to grow (bound K≤D, J≤D·2^D, D the number of pair bits). A soft common-neighbour factor is such a function. Expanding "at least one common neighbour" as a disjunction over wedges uses O(N) literals per pair. That cost is the trade-off. It is not evidence of a new fundamental mechanism.

A count literal is a compound feature. The expressivity note says the formal K hierarchy is literal-only. RRC therefore does not quote a K number for the wedge rule as if the count were one Boolean gate.

## What would fail the gate

The following are not opened in RRC-001, because each needs a witness rather than a new name:

- A next-step law that depends on which history reached the current graph, while the rule claims to read only the current graph. The expressivity note already says no increase of K or J at unchanged current state can match two different rows.
- A transition that toggles two pairs at once, or that adds a self-loop as a real event.
- An independent hyperedge that is not a function of the pair bits.

If a later observation cannot be compiled, RRC writes the witness (two reachable situations, same declared state, different future rows) before changing the engine.

## A listed activity bit

Two pair bits and one further bit can be written as three listed edges. The further bit is then ordinary pair state. It is not a new event type, and it is not a new primitive.

The fixture in `src/rrc/coordinate_examples.py` uses bits `(pair0, pair1, activity)`. The weight of toggling pair0 is 3 when the activity bit is present and 1 when it is absent. The other pair toggle stays at weight 1. The activity toggle has weight 1 when pair0 is present and weight 0 when pair0 is absent. States 1 and 5 share the pair bits `01` and differ in the activity bit. The probability of toggling pair0 is `1/3` in state 1 and `3/5` in state 5. The pair bits alone do not determine that probability. The same eight rows are the four-node chain `[[0,1],[1,2],[2,3]]` at baseline 1, with one multiply by 3 of `(0,1)` when `(2,3)` is present and one prohibit of `(2,3)` when `(0,1)` is absent. EQ-027 records that equality for this table.

The count of the two pair bits is a derived coordinate. Each pair mask has one count, and masks 1 and 2 share the count 1. That count agrees on states 1 and 5, so it does not restore the two rows.

An empty constraint list on the same three edges gives weight 1 to every toggle. The probability of toggling pair0 is then `1/3` in both state 1 and state 5. A freely toggling third bit is not a witness that the extra coordinate changes the pair-toggle probability.

A step that flips two bits at once leaves the single-toggle support. From state 0 the single-toggle successors are states 1, 2, and 4. State 5, the joint flip of bit 0 and bit 2, is not among them. No current-state weight table on this support assigns that step a positive probability. History at an unchanged current state is the other failure named above. Neither case is given an engine change here.

These comparisons are fixtures. They are not a frozen round. `rrc-0.4.0` is unchanged. ATLAS-Q15 stays open. The equality is not a theorem about every higher-order coordinate. The same verdicts apply to the families in `docs/state-event-families.md`. That note is not a frozen round. The fixtures in `docs/event-kernel.md` name events and normalise their integer weights. They are not a frozen round, and they are not a new primitive of `rrc-0.4.0`.
