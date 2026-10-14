# Predictive state under coarse-graining

Initial draft: externally predeclared analytic expectations and generic
mathematical arguments, not new non-neutral execution. Related branch exposure
is explicitly recorded in the charter. Verified appendices/catalogue follow I0.

## 1. Observations and predictive equivalence

The recurrent state is z=(p,h), six pair bits and one remembered pair slot.
Observe P=p, C=graph isomorphism class(p), K=popcount(p), or R=K mod 2.
All times are pair-event epochs. Ordinary full O3 material state still has ten
bits; the exact 8H pair-epoch reduction preserves the declared memory semantics.

Observable-preserving future-word equivalence requires the same current Y and
the same laws for every finite future Y word. A strongly lumpable refinement of
Y is sufficient to represent such futures but can be stricter than word-law
equivalence in an arbitrary hidden chain. The algorithm below computes the
coarsest strong-lumping refinement, not a globally minimal hidden-state model.

## 2. Exact refinement method

Start with equal-Y blocks. For each state sum its rational transition weights
into each current block; split a block by distinct vectors. Repeat to stability.
At stability all block members share a quotient row, yielding a first-order
quotient for every augmented initial distribution. Termination follows because
a strict split increases block count in a finite set.

For coarseness: any strongly lumpable refinement Q of the initial observation
partition refines every intermediate partition by induction. If states share
a Q block, their sums into unions of Q blocks agree, so the next split cannot
separate them. Thus the fixed point is the coarsest such refinement. This is
not inferred merely from absence of pairwise merges.

Publish chronology, membership, sparse row signatures and explicit obstructions
to merging distinct stable blocks sharing current Y. Where their immediate
observed rows already differ, this also proves future-word inequivalence.
This stronger condition is a target, not built into the generic algorithm.

## 3. Labelled-mask expectation

At fixed p, remembering h distinguishes successor p xor 2^h with probability
m/(m+5), versus 1/(m+5) elsewhere. This is favoured for m>1 and suppressed
for m<1, not always elevated. For non-neutral m, six labelled rows differ;
the candidate minimal refinement has 384 singleton blocks. At m=1, 64 p blocks
are already strongly lumpable.

## 4. Marked graph and symmetry

A vertex permutation must act on p and h simultaneously. Equality e=h is
preserved, and a toggled state maps to the corresponding relabelled toggle.
Thus the kernel is covariant and S4 orbits form a valid quotient. Group orbits
need not be minimal just because they are valid. Independently compute graph
automorphisms and their six-pair orbits, and compare generic refinement.

At fixed graph G, the next class row is
[n_G(c)+(m-1)1{class(G xor h)=c}]/(m+5).
If distinct marked-pair roles have distinct toggle classes, their observed rows
differ for every m!=1. The N4 structural certificate must establish that
condition and its proposed 28-role count.

## 5. Directional edge-count memory

Let r=p_h. If r=1 the last pair event formed that pair; if r=0 it dissolved it.
Aggregate dissolution weight is k+(m-1)r; formation weight is
6-k+(m-1)(1-r). Divide by m+5. Next roles are (k-1,0) and (k+1,1).
Legal (k,r) states number twelve as an expectation. At every interior k, the
two dissolution probabilities differ by (m-1)/(m+5), proving a lower bound
if both role classes are present. At neutral m the seven k blocks suffice.

## 6. Parity erasure

Every pair event flips exactly one bit, so R_(t+1)=1-R_t and
R_t=R_0 xor (t mod 2). Conditional on initial parity, the entire finite observed
path law is independent of m and h. This algebraic expectation gives all-order
erasure, not merely zero triple CMI; generic refinement supplies an exact check.

## 7. Synchronization length and Markov order

Synchronization length is the shortest number of consecutive observations
whose positive histories determine the current minimal refinement block.
It is not the number of blocks, alphabet size or a bit cost.

Two labelled masks recover h via their one-bit XOR. Class pairs are proposed
to recover the marked role in N4; count pairs recover r from the sign of their
increment. These implications require exact pair-to-block checks. Non-neutral
one-step witnesses plus synchronization imply stationary order exactly two.
Neutral refinements may synchronize with one observation. Parity always does.
No infinite-order or arbitrary-controller conclusion follows.

## 8. Stationary pushforward and one-step invisibility

Use the 8H theorem pi(p,h)=1/384, verify direct balance, and push it through
each certified quotient. Candidate edge-role masses are C(5,k-r)/64.
Averaging r at fixed k yields dissolution probability k/6 and formation
(6-k)/6. Stationary adjacent labelled pair laws already equal H0; deterministic
pushforward preserves this equality for C,K,R. One-step equality is not
all-path equality except where a separate proof, such as parity, applies.

## 9. Temporal conditional information

Construct exact stationary triples using previous p=p_current xor 2^h and the
next-event row. Independently sum two forward augmented transitions. Compute
I(Y_previous;Y_next|Y_current) with high-precision natural logarithms.
A separate stable-quotient conditional-row KL calculation supplies a second
information route when synchronization is verified. Labelled CMI is also
checked against CL-T34's event-slot formula. No general CMI monotonicity under
simultaneous coarse-graining of conditioning and measured variables is assumed.

## 10. Scope

All minimality is relative to a fixed 384-state chain and current-observation
partition. Quotient validity is for arbitrary augmented starts; stationary CMI,
one-step invisibility and stationary first-order failures have their stated prior.
No physical identity, minimal ontology, observer-created history, irreducible
time, design, theology or TCR completion is established. History alphabet,
temporal depth, state count, synchronization and information remain separate.
