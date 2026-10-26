# XOR recoding and predictive closure

**Status:** Analytic results with independent software checks, 26 October 2026.
**Analysis identifier:** `xor-mask-analysis-0.1.0`.
**Scope:** Finite declared bit-state laws; not a new stochastic engine method,
scientific atlas round, physical primitive or ontology claim.

## Objects and equivalences

Let the full state space be the binary vector space `V = GF(2)^w`, with `w >= 1`.
An event direction is a nonzero mask `m`; its update is `s -> s XOR m`.
Let `M` be the set of distinct directions. Distinct event names with the same
direction must first be aggregated for a kernel-level comparison. Their labels
are not thereby declared equivalent.

At state `s`, direction `m_i` has a nonnegative integer weight `q_i(s)`.
If the row total is positive, divide by that total. If the total is zero,
complete by a halt self-loop, not a declared event. The observation clock is
one declared event. No additional states, time rescaling or intermediate moves
are allowed unless explicitly stated.

A coordinate permutation, an invertible binary-linear state map, an arbitrary
state permutation, an injective encoding into a larger cube, a noninjective
observation, and a labelled-event correspondence are different operations.
The first result concerns binary-linear maps. The last section gives two
stronger obstructions for particular supports, not a general nonlinear classifier.

## A. Exactly when directions can become coordinate axes

There is an invertible binary-linear map `L` that sends every distinct direction
in `M` to a different standard coordinate vector if and only if `M` is linearly
independent over `GF(2)`.

**Necessity.** If a nonempty XOR of directions is zero, linearity takes that
relation to a zero XOR of distinct coordinate vectors. No such relation exists
among distinct coordinate vectors. Invertibility also prevents two distinct
directions from receiving the same image.

**Sufficiency.** Extend the independent directions to a basis of `V`. Define
`L` by sending the selected directions, in their declared order, to the first
coordinate vectors and the remaining basis vectors to the rest. A basis map is
invertible, and `L(s XOR m_i) = L(s) XOR e_i` for every state.

An affine offset does not change the direction argument. With `r = |M|`, the
last `w-r` new coordinates are invariant under all selected moves. If every
direction has positive weight at every state, the support components are the
cosets of the span of `M`. State-dependent prohibitions can fragment that support
further. The empty direction set is the all-halt case.

This is elementary basis extension, not a newly discovered general theorem.
For a kernel-level necessity claim, use the directions that are actually enabled:
a never-enabled syntactic direction does not obstruct a kernel representation.
The algebraic per-direction statement itself does not depend on the weights.

**What A does not imply.** The transformed weights may depend on every recoded
coordinate. One-coordinate support is not statistical independence of coordinate
processes. A dependent direction set rules out this class of linear recoding;
that fact alone does not rule out every nonlinear state encoding. Original
carrier meaning and event-kind labels are not automatically preserved.

Atlas-018 directions `[1, 6, 8]` are independent on four bits. EQ-033 is one
choice of the resulting basis. Adding direction `2` to those directions gives
rank four, so a different basis makes all four directions coordinate toggles.
The old disagreement coordinate then need not be invariant. Failure of the old
map is therefore not, by itself, a new expressive primitive.

## B. Exactly when inactive coordinates can be discarded

After an independent-direction recoding write the state as `(z,d)`, where `z`
has `r` active coordinates and `d` has the invariant remaining coordinates.
The observation is `pi(z,d) = z`. This is a particular projection, not an
arbitrary search over observations.

The projection is strongly lumpable if and only if, at each fixed `z`, both
the normalised active-direction probability vector and the halt probability
are independent of `d`.

Equivalently, each fixed-`z` block must satisfy one of:

1. Every weight vector is zero, so all rows halt at that observed state.
2. Every weight vector is nonzero and all vectors lie on the same positive ray.

For case 2 this means all pairs of hidden states `d,d'` and directions `i,j`
satisfy `q_i(z,d) q_j(z,d') = q_j(z,d) q_i(z,d')`. A block mixing a zero vector
and a nonzero vector is not permitted. Cross-product equality alone is not enough
in that mixed case because every cross product involving the zero vector vanishes.

**Proof.** From `(z,d)`, each active direction reaches the distinct observation
`z XOR e_i`, and a halted row reaches `z` itself. The outgoing block probabilities
are exactly those normalised direction probabilities and the halt probability.
Strong lumpability is equality of these block rows for all states with the same
observation, which proves necessity and sufficiency. On nonzero rows, equality
after division by each row total is equivalent to positive proportionality of
the nonnegative weight vectors. An all-zero row has halt probability one, while
a nonzero row has halt probability zero, establishing the remaining boundary.

This argument does not require irreducibility, a unique stationary law, or a
chosen initial distribution. Failure means no common exact first-order quotient
for every starting distribution under this observation. It does not exclude
special initial-distribution behaviour, a different observation, retaining more
state, or a history-dependent description.

The consequences go in both directions. Hidden state may change every raw event
weight by a common factor without changing the observed law. Conversely, relative
weight changes can destroy closure even when support and all event masks stay
the same. A frozen hidden coordinate can remain consequential for prediction;
it need not evolve to matter. No causal intervention is inferred from this fact.

## C. Two support obstructions that survive nonlinear injective encoding

These examples use positive weight on every named direction at every state.
Only off-diagonal support is considered. A purported encoding must assign each
original state a distinct bit state, and every original transition must remain
a single-bit transition in one observed step. The target may have more bits.
Many-to-one encodings, latent copies, intermediate states and changed clocks
are outside this claim.

**Three-direction circuit.** Directions `{1,2,3}` on two bits contain the relation
`1 XOR 2 XOR 3 = 0` and give a triangle, for example `0 -> 1 -> 2 -> 0`.
Every one-bit step changes parity, so a hypercube is bipartite and contains no
triangle. No injective state encoding into any finite cube can preserve those
three edges as one-bit steps. This is stronger than the linear-dependence test
for this particular support.

**Four-direction circuit.** Directions `{1,2,4,7}` on four bits have a minimal
four-term dependence, and every mask has odd Hamming parity. Thus this support
is bipartite; an odd-cycle check does not reject it. States 0 and 3 have the
four common neighbors `{1,2,4,7}`. Two distinct vertices of any hypercube have
at most two common neighbors: if they share one, their difference must flip
two coordinates, and only either of those two flips can reach a common neighbor.
Four distinct common neighbors therefore rule out the same kind of injective
one-bit encoding, regardless of the target bit width.

The four-bit support consists of two copies of `K(4,4)`; its degree is four,
as is that of the ordinary four-cube. The latter supplies a matched positive
control without either obstruction. A support obstruction need not be an
odd cycle or a simple degree mismatch. These two circuits do not classify all
dependent-mask supports or all allowed changes of representation.

## Verification and established mathematics

`provenance/xor-mask-analysis-check.py` imports only the standard library.
Pivot-based binary rank is checked against exhaustive nonempty-subset XORs.
Constructed basis maps are checked on every state and declared edge in the
bounded domain. Exact `Fraction` block aggregation is compared with an integer
cross-product/halt criterion. The proofs establish the general statements;
the finite fixtures validate implementations and boundary cases.

The fixed-direction support is a familiar cubelike Cayley graph, rather than
a new graph category; see Bernasconi, Godsil and Severini, *Quantum Networks on
Cubelike Graphs* (2008), Section I, [arXiv:0808.0510](https://arxiv.org/abs/0808.0510).
Only that graph definition is used here, not their quantum-dynamical results.

For the distinction between strong lumpability for every initial distribution
and weaker initial-distribution-dependent behaviour, see Geiger and Temmel,
*Lumpings of Markov Chains, Entropy Rate Preservation, and Higher-Order Lumpability*,
Definition 7, [arXiv:1212.4375](https://arxiv.org/abs/1212.4375). The direct block-row
proof above is self-contained and does not import additional assumptions from
their entropy results. No claim of novelty for basis extension, hypercube parity
or the general theory of lumpability is made.
