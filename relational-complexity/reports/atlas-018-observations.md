# Atlas-018: when two interface copies preserve the identified dynamics

## What was recovered

This is a completed recovery increment, not a new execution. Three existing
uncommitted Atlas-018 items were found during the 26 October audit and adopted
after verification. No worker was called to rerun them. The selection is
`docs/2026-10-26-otr-selection.md`; the original plan is unchanged.

The freeze is `8923de6565937a99a185f817526816ba50690def`, the definitions commit
is `81389d9d50eafe53ccd0e6eee339602989f13886`, and the canonical plan hash is
`2468bf59c1fce72fb909482dc94e1abeae30e627f0bd71e4536ed8b10b7a27e0`.
Engine `rrc-0.4.0`, strict method `event-kernel-0.2.0`, and clock
`one_declared_event` are unchanged. The three items are complete; failed,
timed-out, unresolved, pending and invalid counts are zero for this round.

The existing verifier reports `verified`. The separate standard-library checker
in `provenance/atlas-018-independent-check.py` imports no RRC engine code. It
checks the input identities, byte receipts, event semantics, event aggregation,
all 576 probability entries, and the image correspondence. Its saved evidence
is `provenance/atlas-018-independent-verification.json`. Six adversarial software
fixtures distinguish valid data from rehashed semantic drift and false image
claims. These checks are not six further scientific cells.

## Fixed question and comparison

Does identifying a shared interface have the same dynamics as maintaining two
copies? The answer depends on the update law, the image and the comparison clock.
A state-space bijection onto the agreement image is insufficient on its own.

The identified state is `(x0, x1, x2)`; the duplicated state is `(y0, a, b, y3)`.
All coordinates are declared bits, not newly discovered entities. The fixed map
is `i(x0, x1, x2) = (x0, x1, x1, x2)`, with integer image
`[0, 1, 6, 7, 8, 9, 14, 15]`. Agreement is the condition `a = b`.

| Frozen item | States | Declared events | Enabled per row | Stored image result |
| --- | --- | --- | --- | --- |
| `A18-identified` | 8 | 24 single-bit toggles | 3 | No image comparison requested |
| `A18-free` | 16 | 64 single-bit toggles | 4 | Not invariant; no restricted rows |
| `A18-coupled` | 16 | 48 events: two outer toggles and one joint-copy move per state | 3 | Invariant; restricted rows conjugate to identified law |

Every declared weight is 1. No row halts, no no-op is declared, and every row
is completed by `normalised_events`. No occupation or stationary distribution
was requested or computed.

## Observations from the frozen records

For the identified law, the three successors of state `s` are `s xor 1`,
`s xor 2` and `s xor 4`, each with probability `1/3`. For the free four-bit law,
the successors are the four individual bit flips, each with probability `1/4`.
Two outer flips preserve agreement and two individual-copy flips break it.
Consequently each agreement state leaks total mass `1/2` in one declared step.
The stored restricted rows are null: renormalising the surviving mass would
define a different, conditioned law, not rescue the original restriction.

For the coupled law, successors are `s xor 1`, `s xor 8` and `s xor 6`, each
with probability `1/3`. The last move flips both copies simultaneously. All
three moves preserve `a = b`. Under `i`, they are exactly the three identified
toggles, with the same probabilities. The stored restricted rows equal the
identified rows for all eight image states, not just one witness transition.

Thus the coupled process restricted to agreement matches the identified
process. The full state spaces have 16 and 8 states and are not bijective.
The free process fails the same invariant-image test. These are scoped
comparisons, not a ranking of the systems by complexity or scientific value.

## Post-execution analysis: the alternative encoding

The following is an exact analysis of the stored coupled law, not another
frozen computation. Introduce `d = a xor b` and recode the full state as
`F(y0, a, b, y3) = (y0, a, y3, d)`. Its inverse is
`(y0, a, y3, d) -> (y0, a, a xor d, y3)`, so no state is discarded.

An outer-left move flips only the first recoded bit. An outer-right move flips
only the third. The joint-copy move flips the second and leaves `d` unchanged.
Each still has probability `1/3`. Therefore the full coupled kernel is
conjugate to three ordinary toggle coordinates plus a frozen fourth coordinate.
The independent checker compares all 256 entries under this permutation.
Both disagreement sectors are invariant copies of the same three-bit law.
Keeping only `(y0, a, y3)` gives an exact eight-state quotient even across both
sectors: every state in one quotient block has the same next-block law.

This does not make the original joint event a one-bit move in its original
named coordinates. `F` is an XOR recoding, not a carrier automorphism or a
permutation of the four bit positions. The event-kind interpretation changes.
Kernel conjugacy under a declared encoding, same-coordinate one-step support,
and labelled-event equivalence are different claims. No new temporal clock
or independent dynamical entity follows from the recoding. EQ-033 records the
kernel-level identity with this boundary.

## Challenge and integration

Atlas-017 compared a one-bit toggle with a coupled pair that halted off its
agreement image. Atlas-018 does not repeat those two rows: it checks a complete
three-bit interface inclusion, and the present coupled law also moves within
the disagreement sector. The historical Atlas-017 results and their older
method identifier remain untouched. The comparison supports checking whole
invariant images rather than isolated matching transitions.

The negative free-copy result is also important: the same inclusion and state
sets need not preserve a transition law. A different encoding is not permission
to hide this failure under the originally declared map. Nothing here establishes
that all joint-event laws admit this recoding, that additional independent
coordinates generally become autonomous, or that Relational Substrate ontology
is empirically verified. This is elementary finite Markov-kernel algebra, not a
new general theorem of Markov theory.

ATLAS-Q01 through ATLAS-Q15 stay open. In particular this one invariant-image
sample does not classify composition maps (Q10), successive quotients (Q13),
or independent higher-order state (Q15). The broad coverage regions remain open;
`COV-INTERFACE-INVARIANCE-SAMPLE` is a partial sample. No probability observed
here becomes the target of a further experiment.

## Next choice and stopping point

The increment ends with adopted evidence, an independent audit and a scoped
encoding result. Atlas-019 and Atlas-020 remain deferred and unadopted, with
their existing local outputs unchanged. Their presence does not impose an
obligation to run or publish them.

A useful later question is when a state-dependent coupling destroys the
recoding or the closed projection. Another is a genuinely nontrivial successive
quotient. Each needs a fresh information-value choice and, if computation is
selected, a separate immutable plan before its scientific results are observed.
Neither is scheduled by the present fractions or by a duty to close a question.
