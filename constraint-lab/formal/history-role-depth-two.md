# Ordered Depth-Two History Roles

The fixed represented recurrent state is z=(P,h1,h2): six pair bits and the
two most recent pair slots. Ordinary X additionally contains four independent
triad bits. All temporal and stationary analysis below uses pair epochs.
See [history-depth.md](history-depth.md) for depth semantics and
[axis-compilation.md](axis-compilation.md) for the strict semantic compiler.

## Ordered Role Orbits

S4 acts on all three slots (h1,h2,e) simultaneously. Independent enumeration
partitions all 216 triples into 12 orbits, with four of size six and eight
of size 24. Independent Burnside counting gives
(216+6*8+3*8)/24=12: only identity, transpositions and double transpositions
fix pair slots. The machine atlas retains full labelled orbit memberships.

R00=(0,0,0), R01=(0,0,1), R02=(0,0,5), R03=(0,1,0),
R04=(0,1,1), R05=(0,1,2), R06=(0,1,3), R07=(0,1,4),
R08=(0,1,5), R09=(0,5,0), R10=(0,5,1), R11=(0,5,5).
Pair slots are 01,02,03,12,13,23 in that order.

The three pairwise SAME/ADJ/DISJ descriptors distinguish every role except
R05/R06: both have all-ADJ pairs of distinct slots. R05's three edges share
one vertex (STAR); R06's three edges form a TRIANGLE. This distinction is
ternary, not present in the three pairwise relation labels.

<a id="role-basis"></a>
## Restricted Invariant Basis

An S4-invariant real-valued function on triples is constant on each orbit.
Conversely any orbit-constant function is invariant. The 12 indicators are
independent (disjoint nonempty supports) and span this invariant-function
space. Candidate presence d=P_e is invariant and both values occur with
each triple. The restricted domain (h1,h2,e,d) therefore has 24 orbit cells.
This is not completeness for arbitrary dependence on P, triads or time.

SECOND-RECENT selects R00/R04/R11; RECENT-REVERSAL selects R00/R03/R09.
These union identities are verified mechanically, not used to define roles.

## Controller Semantics

ANY selects one role; FORM/DISSOLVE additionally require candidate absence/
presence before toggle. A selected pair has weight m>0; all other events
have weight one, including every triad event. If either history slot is
unavailable all events have weight one. Register update is (e,h1) for pairs,
identity for triads. The common palette is m=1/4,1,4; one neutral baseline.
These are fixed programmes, H_pair=2 and ontology L=0.

<a id="quotient"></a>
## Exact Pair Closure And Symmetry

Let W=sum_e w_e at fixed (P,h1,h2). Triad-only excursions preserve all
weights and the pair/history state. Their absorption sum is
sum_n (4/(W+4))^n w_e/(W+4)=w_e/W. This proves exact pair closure,
independently of raw triad bits. Pair transition is
(P,i,j)->(P xor 2^e,e,i).

The invariant feature and candidate presence make weights, denominators and
updated targets covariant under every simultaneous vertex permutation.
Consequently aggregate transition masses into each S4 orbit are constant
on source orbits. This is strong lumpability, not minimality.

The 2304 states have 120 augmented S4 orbits: 16 of size six, 24 of size
twelve and 80 of size 24. Burnside independently gives
(2304+6*64+3*64)/24=120. Exact member-block sums must be verified for every
generated controller before quotient use. Quotient stationarity is lifted
uniformly inside each orbit, then checked against the entire sparse chain.

Positive support implies irreducibility: XOR-toggle a prefix ending at
Q xor 2^j xor 2^i, then append j,i to reach any target (Q,i,j).
Parity flips every step; a diagonal-history state has a positive two-step
return, so the common period is two. Unique stationarity plus covariance
implies S4 invariance. No pointwise fixed-parity convergence is asserted.

<a id="history-only"></a>
## History-Only Material Uniformity

For any positive q(e|i,j) independent of P and stationary history law nu,
the product pi(P,i,j)=nu(i,j)/64 is stationary. Incoming mass to (P',e,i)
is sum_j nu(i,j)q(e|i,j)/64=nu(e,i)/64. Irreducibility makes it unique.
Hence material is uniform and independent of the ordered history pair.
This holds for every ANY role, without requiring nu itself uniform.
It does not imply event independence or equality of material path laws.

<a id="complement"></a>
## FORM/DISSOLVE Complement

Complement P->P xor 63 preserves ordered roles and register updates, exchanges
candidate absence/presence and commutes with pair toggles. It conjugates
FORM and DISSOLVE kernels at the same role and grade. Unique stationary
laws transport exactly; counts map k->6-k and graph classes to complements.
Both partners remain separately executed and retained.

<a id="strict-h2"></a>
## Strict H2 Versus Semantic H1

Forgetting h2 strongly lumps iff each fixed (P,h1) has one next pair row.
Every one-role selector is supported on just one relation type of (h1,h2).
For some compatible (h1,h2), its selected candidate subset is nonempty and
proper; for an older history outside that relation type it is empty.
At m!=1 the former row is nonuniform and the latter uniform. ANY therefore
requires h2. FORM uses the same witness at empty P; DISSOLVE at full P.
All states are reachable by positive support. This proves strict H2 for
every non-neutral one-role cell, irrespective of arbitrary positive K/J
in a strict fixed-(X,h1) compiler. Neutral rows ignore history.

This is not failure of unrestricted augmentation or every arbitrary H1
recoding. A 36-valued coordinate can encode the ordered pair but lies outside
the declared last-pair semantics. Persistent occupancy alone does not prove
this depth-specific row distinction.

<a id="comparators"></a>
## Two Matched H1 Representations

KU(e|P,i)=sum_j q(e|P,i,j)/6 averages already normalised rows. It has update
(P,i)->(P xor 2^e,e) and its own stationary law. It is a counterfactual
uniform local averaging, not the generally non-Markov true projection.

Kpi(e|P,i)=sum_j pi(j|P,i)q(e|P,i,j) uses the actual stationary conditional
older history. For s=(P,i), pi_s(s)Kpi(s,s') is exactly the true stationary
adjacent s joint, by summing over j. Summing incoming s proves stationarity.
All recurrent s have positive mass here. The full 384-state residual and
adjacent-law identity are checked, not inferred from the 28-state solve.

Kpi must therefore capture stationary material occupancy: no occupancy
result can refute every H1 representation. It is not a strong lump or
all-conditioned-row compiler. Longer-word separation is the relevant
loss of process information for this specified comparator.

Material L1/L2 laws match by projection. Moreover current h1 is the unique
slot of P_prev xor P. Thus an adjacent s path determines precisely a
three-mask path and vice versa; stationary material L3 laws also match.
Potential distinctions first occur at L4. Equality through frozen L6 is
not all-order equality unless another proof establishes it.

Uniqueness corollary: if a fixed first-order kernel B on exactly s=(P,h1)
matches both pi_s and the true adjacent s joint J, positivity forces
B(s,s')=J(s,s')/pi_s(s)=Kpi(s,s') on every state. Therefore a longer observed
word difference excludes EVERY such stationary-adjacent-matched strict H1
kernel, not just an arbitrary selected representative. This does not exclude
H1 models matching only material occupancy, or compilers with extra hidden
state, changed clocks or a different represented history alphabet.

For this positive-support two-slot grammar, strict h2 row dependence also
guarantees a material L4 difference: a three-mask word reconstructs the
current (P,h1,h2) and has positive mass. A nonconstant h2 row family cannot
all equal its stationary conditional average. Multiplying the differing row
by that positive triple mass separates a four-mask word. This assertion is
about labelled masks; C/K separation remains a finite observed result here.

<a id="decomposition"></a>
## Persistent Structural Decomposition

Classify exact rational distributions before logs: material silent, density
only, shape only, or density and shape. Shape equality means conditional
class distributions at each count equal, certified by cross multiplication.
Full positive support makes these conditionals defined.

KL(pi_C||pi_C0)=KL(pi_K||pi_K0)+sum_k pi_K(k)KL(pi(C|k)||pi0(C|k)).
Since both material laws are internally class-uniform, the labelled-mask
KL equals class KL. This also applies to the S4-invariant KU comparison.
The identities are checked through direct conditional and projected routes.

I(P;H2|H1) is stationary dependence beyond h1, not causation. Expected
KL(pi(h2|P,h1)||Uniform6) includes nonuniform history marginal effects and
must not be substituted for that conditional MI. Neither is a master score.

## Exact Word Representation

Stationary forward words use lengths one through six and projections P,C,K.
All 64*6^(L-1) positive mask words are represented by simultaneous-S4 word
orbits, sorted lexicographically with per-labelled-word rational masses and
orbit sizes. This canonical encoding reconstructs the complete distribution.
Coarse words sum the full census, not selected representatives.
Every model/length normalises exactly. Separate direct hidden-state forward
propagation through L4 checks the synchronised-word implementation.

Information uses natural logs, nats, 160 digits; exact rational equality
decides visibility. Conditional MI, JS, state count, depth and synchronization
remain separate. No stochastic scientific trajectories are generated.

## Scope

These are finite-model mathematical statements and frozen observations.
They establish no physical memory, purpose, repair, adaptation, boundary,
design, dynamic constraint state or irreducible time. STAR/TRIANGLE are
structural labels, not functional interpretations. Future controlled passage
requires its own source, target, occupancy controls and frozen estimands.

Exact rational solving uses the pinned python-flint 0.8.0 binding; its
[matrix API](https://fredrikj.net/python-flint/fmpq_mat.html) distinguishes
Dixon and fraction-free routes. Decimal logarithms use pinned mpmath 1.3.0.

<a id="opposite-pair"></a>
## Separately Frozen M1: A Larger Slot Conjugacy

After the entire M0 census, M1 checked an explanation for R05/R06's equal
scalar profiles despite unequal class laws. Define sigma(e) as the unique
pair disjoint from e: slot map (5,4,3,2,1,0), and permute pair bits by sigma.
This involution commutes with vertex relabelling because disjointness is
preserved, but is not induced by a vertex permutation.

It preserves pairwise SAME/ADJ/DISJ and candidate presence after transforming
P. It exchanges the all-adjacent STAR and TRIANGLE roles and fixes the other
ten roles. It also commutes with pair toggles and the history shift.
Consequently it conjugates R05/R06 kernels for every positive m and each
action family. Uniqueness transports stationary laws. Uniform-h2 averaging
and stationary conditional averaging commute with this change of variables,
so KU and Kpi transport too. This proves all finite path-law transport when
the observation map is transported, not labelled same-kernel equality.

On unlabelled graph classes sigma exchanges only three-star and
triangle-plus-isolate. It preserves edge count. Thus R05/R06 have identical
edge distributions but may differ in shape. Their H2-vs-Kpi word divergence
values agree under a common alphabet bijection even when their raw class
laws differ. This is an invariant of information, not identity of structure.

The separately frozen finite check covers all six family/grade pairs, every
2304-state kernel/stationary entry, H1 comparator rows and all 25,263
labelled-word orbits through L6 per pair. It independently reconstructs
144 immutable M0 word-distribution hashes. No new stationary solve or
controller was introduced. See the M1 plan and exact permutation receipt.

## Generation 8N: Reuse Without New Controllers

The 73 immutable M0 payloads, source hashes and symmetry data are inputs to
[controlled passage](history-controlled-passage.md). No 8M cell is altered.
Kpi is the relevant adjacent-matched comparator, not KU. All roles and both
grades receive the same complete sibling-shape task family, irrespective of
their stationary structural category or effect magnitude.
