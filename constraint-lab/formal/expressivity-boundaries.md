# Expressivity boundaries

## Four distinct representation layers

1. **Backend semantics:** fixed occurrences multiply factors; duplicates have multiplicity.
2. **Literal parser core:** O=2/O=3, any supported action slot, both directions and conjunctions over all other supported relation bits; no intrinsic K ceiling; custom factor names accepted.
3. **Normal form:** historical primary censuses require structurally simple sets; stacked-weight comparisons are separate.
4. **Experiment runner:** W4/W3/W16 named alphabets and J in {1,2,3}, plus frozen cell-specific K/A limits.

A theorem about layer 2 with unbounded positive parameters is not a theorem that layer 4 has already enumerated or can request that entire family.

## Current-state expressivity: proved with restrictions

[CL-T12](derivations.md#cl-t12) gives a constructive proof of all strictly positive current-state event-weight functions on the existing finite single-toggle support. Direction encodes the action bit; a full conjunction encodes every other bit. The upper bound is K<=D, J<=D*2^D. This is not a new census and does not require a G0 computation.

A desired positive kernel with that support can use its probabilities as weights. Kernels with multibit transitions, extra states or self-loops are outside this support theorem. Arbitrary history dependence is outside a fixed current-state representation. Rational parameters are exact in the backend; arbitrary reals are the algebraic idealisation, and irrational numerical references require precision/error reporting.

## K, J and interaction

One action plus r distinct satisfiable literals has K=r+1 and nonzero top gate coefficient if non-neutral. A sum of features cannot manufacture a missing monomial in log weights. It can manufacture non-additive probability or observable effects through normalisation.

A count predicate is a compound feature, not one Boolean gate. The explicit count>=1 counterexample has K=2 and degree 2 over two remaining pair bits. Therefore the formal K/order hierarchy is **literal-only**, not a blanket theorem about every token in the DSL. Historical claims remain visible and receive a scope relation.

## Continuous parameters versus finite W4

Continuous completeness follows from either corner or monomial bases. W4 coefficients lie on a log-base-2 integer lattice. Non-dyadic multipliers are impossible using finite positive W4 products. Structural simplicity additionally bounds how many features can stack at a corner.

[CL-T21](derivations.md#cl-t21) proves selected minimal [J,max-K] vectors without enumeration. It distinguishes constant 8 as continuous [1,1], structurally simple W4 [3,2], and stacked W4 [2,1]. A constant 3 is not a W4 product at any finite J. The earlier 625-table basis grids are narrower than the whole structurally simple family.

Minimum J and minimum maximum-K are separate optimisation coordinates. General targets can have tradeoffs; these selected examples attain both stated minima jointly. The empty baseline's [0,0] is a bookkeeping convention, not a claim that K=0 is a new primitive rule.

## What H adds

Let x contain **all** ordinary material relation bits, including hidden triads. A fixed ordinary collection assigns one future row to x. If two reachable histories end at the same x yet a common controller assigns distinct future distributions, no increase of K or J at unchanged x can reproduce both rows.

Finite history can often be encoded in an augmented Markov state. That is a representation change, not compilation into the same ordinary state. Preserving the exact event support and event clock may require additional update semantics; do not silently insert stuttering or multibit updates.

## What L adds

A dynamical constraint state eta can change coefficients, polarity, existence, scope or rule interpretation under a common program. Two separately chosen static constraint sets already give different kernels at L=0 and are not an L witness.

If eta is a function of ordinary x and the resulting law has existing positive support, CL-T12 compiles it into a larger fixed ordinary grammar (continuous/unbounded budgets). If independent reachable eta values give different futures at identical x, extra represented state is needed. This proves a state-boundary issue, not automatic irreducibility of every meta syntax.

## Permanent compilation test

Before introducing an axis, specify:
- represented state and what counts as identical current state;
- event/update support and clock;
- visible projection, initial priors and demanded process equivalence;
- alphabet and allowed K/J budget;
- whether compilation may augment state.

Then either provide a construction and representation tradeoff, or an exact non-compilability witness. Aggregate fit, larger CMI or a novel syntax name is insufficient. Hard zero support requires a separate extension of the positive theorem.
