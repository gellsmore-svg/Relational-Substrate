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

## 11. Verified I0 statements

The draft above is retained as pre-execution context. I0 was separately frozen
and pushed at 872dd1344c60325d8d545d13c38c13c85d8483d1, canonical plan hash
328be1bf7dbac354d5bc4d0510c76555bbe638e8485d8089f63bea0898d9825c.
New target execution before that freeze was zero, but related branch exposure
was nonzero: this is not a blind round. Exact results are committed separately
at 2c8e214; the report records the exposure, methods and complete artifact map.

<a id="cl-t52"></a>
### CL-T52: Coarsest strongly lumpable observation refinement

For a finite stochastic rational kernel and initial observation partition,
splitting by vectors of total probability into current blocks terminates at the
unique coarsest strongly lumpable refinement. Every proper split increases the
number of blocks, bounded by state count. At stability the equal signatures
define a stochastic quotient. If Q is any strongly lumpable refinement of the
initial partition, inductively each intermediate block is a union of Q blocks:
states sharing a Q block have equal sums into those unions, so no subsequent
split separates them. Thus Q refines the fixed point, proving coarseness.

This is not a theorem of globally minimal hidden Markov representation, nor
does strong lumpability generally coincide with future-word equivalence.
Published chronology and signatures certify stability; explicit merge
obstructions supplement rather than replace the coarseness argument.

<a id="cl-t53"></a>
### CL-T53: Exact labelled-mask refinement

For m>0, m!=1, fixed p has six distinct next labelled-mask rows, since h selects
the distinct successor p xor 2^h with weight m instead of one. Therefore any
observation-preserving predictive equivalence separates the six histories.
All 384 singletons suffice and are necessary. At m=1 all h rows agree and
the original 64 p blocks are strongly lumpable. Two labelled observations
recover the toggled slot exactly; at non-neutral m a single p does not.
Positive stationary predecessor histories have unequal futures, so projected
stationary Markov order is exactly two; neutral order is one.

<a id="cl-t54"></a>
### CL-T54: S4 marked-pair quotient

For g in S4, T((gp,gh),(g(p xor 2^e),ge))=q_(gh)(ge)=q_h(e).
Both the equality test e=h and the deterministic update h'=e commute with g.
Summing over a destination orbit gives equal aggregate rows for orbit mates,
so simultaneous S4 orbits on (p,h) form a valid strong lumping for all m>0.
An orbit may equivalently be described by the unlabelled current graph and
an Aut(G) orbit of its marked unordered pair: first move p to a canonical
representative, then compare h under the stabiliser. Transforming p without h
is not this quotient.

<a id="cl-t55"></a>
### CL-T55: Structural-role minimality and class synchronization

The independent N4 structural certificate CL-F08 enumerates 28 marked-pair
orbits, and for each fixed current class the remembered-toggle class is
different for every such role. Let n_G(c) be the number of its six toggles
leading to class c. The next class law of a marked role is

    [n_G(c)+(m-1)1{class(G xor h)=c}]/(m+5).

Distinct roles therefore have different immediate observed rows for every
positive m!=1, while CL-T54 supplies sufficiency. This proves minimality among
current-class-preserving strong refinements AND future-word equivalences on
the declared state set. The 28-state count is finite N4 combinatorics, not
a universal graph-size theorem.

The same toggle identifies the predecessor class. CL-F08 verifies that
(previous class,current class) is a bijection to the 28 roles. Thus two
observations synchronize the refinement and determine every future class law.
First order fails: current one-edge graph reached from empty gives probability
m/(m+5) of next empty; reached from two-edge matching gives 1/(m+5).
Both predecessor pairs have stationary probability 1/64. Stationary order and
synchronization length are exactly two non-neutrally. At m=1 the 11 graph
classes are already a strong quotient, so both quantities are one.

<a id="cl-t56"></a>
### CL-T56: Directional count refinement and synchronization

At k present pairs, r=p_h is one or zero. There are k dissolution candidates
and 6-k formation candidates; the remembered candidate adds m-1 to the
appropriate total. Hence the exact quotient rows are

    (k,r) -> (k-1,0) with [k+(m-1)r]/(m+5)
    (k,r) -> (k+1,1) with [6-k+(m-1)(1-r)]/(m+5).

Zero-probability boundary targets are omitted. Only (0,0),(6,1) and both r
values at k=1..5 are legal: twelve states. Their rows depend on no further
label or shape information, proving strong lumpability for all m>0.
For each interior k the r rows differ in next-count probability by
(m-1)/(m+5), proving non-neutral minimality. At m=1 they merge to seven k states.

The sign of K_current-K_previous determines r, so twelve legal ordered count
pairs biject to these states. Current count one has positive stationary
predecessors zero and two with masses 1/64 and 5/64; next-count-zero rows differ
by m/(m+5) versus 1/(m+5). Thus stationary order and synchronization are exactly
two non-neutrally, one neutrally. No deeper history is needed for this controller.

<a id="cl-t57"></a>
### CL-T57: All-order parity erasure

Every supported pair-epoch event toggles one bit. Therefore
R_(t+1)=1-R_t and R_t=R_0 xor (t mod 2), for every path and every m>0.
Both parity blocks have deterministic transition to the other block, making
the initial two-block observation partition strongly lumpable and minimal
subject to preserving current parity. The complete path law given initial
parity is independent of m and h at ALL orders, not just through a tested depth.
At stationarity two alternating words each have mass 1/2, and parity is
first-order, not iid. No claim about physical information destruction follows.

<a id="cl-t58"></a>
### CL-T58: Stationary pushforward and one-step invisibility

CL-T31 gives uniform joint law 1/384. Its exact pushforward onto any certified
quotient is stationary, because aggregate block transitions commute with
pushforward. Marked-role mass equals |S4 orbit|/384.
For fixed h, counting the other five bits gives

    pi(k,r=1)=C(5,k-1)/64, pi(k,r=0)=C(5,k)/64

on legal domains. Thus P(K=k)=C(6,k)/64 and E(r|k)=k/6.
Substituting into CL-T56 gives dissolution k/6 and formation (6-k)/6.
More generally h is conditionally uniform at each p, so the stationary
one-step labelled pair-toggle law is the neutral 1/6 row. Deterministic
projection preserves the equality of stationary adjacent joint laws for
class, count and parity, hence their stationary conditional one-step rows.
This does not imply full process equality: CL-T55/T56 show class/count triples
differ from H0 at non-neutral m. Parity equality has a separate all-order proof.

<a id="cl-t59"></a>
### CL-T59: Commuting predictive quotient ladder

At non-neutral m the maps are (p,h) -> marked S4 role -> (k,p_h) -> parity.
The latter two quantities are constant on each source block. CL-T54,
CL-T56 and CL-T57 give direct strong lumpings from the full chain.
Because source blocks have equal rows into every union of target blocks, the
induced source-to-target map is also a strong lumping, and its kernel equals
the direct target kernel. Pushforward of stationary masses then commutes.
Thus the 384->28->12->2 ladder commutes for every m>0,m!=1.
At m=1 the same argument applies to 64->11->7->2, using the neutral toggle
symmetries. This is not inferred from state counts or presumed group minimality.

<a id="cl-f08"></a>
### CL-F08: Finite exhaustive certificates

At m=1/4,1,4, generic exact refinement, reversal of state enumeration, and
independent identity/S4/(k,r)/parity partitions agree in all twelve cells.
Non-neutral P,C,K split once; parity and all neutral partitions never split.
There are 1,986 explicit same-observation merge obstructions with immediate
next-observation distinctions. All 384 augmented states are covered exactly;
24 vertex permutations pass covariance at all grades (165,888 comparisons).

Fixed-graph automorphism pair-orbit counts at canonical masks
0,1,3,7,11,12,13,15,30,31,63 are 1,3,4,2,2,2,4,4,2,3,1.
The 28 graph-pair and 12 count-pair maps are bijective to the non-neutral
refinements, and the nine adjacent quotient arrows commute exactly.
The machine artifacts include stable membership, row signatures, complete
chronology, pair atlases, masses, rational triples and all merge witnesses.
No decimal or fitted threshold decides any block count.

<a id="cl-n08"></a>
### CL-N08: Stationary temporal conditional information

Exact stationary triples independently built from inverse last-toggle and two
forward transitions agree. Their CMI and an independent quotient-row KL
evaluation agree to 1e-160, within frozen 1e-25. Natural logs are evaluated at
160 decimal digits. At m=1/4 and m=4 respectively, class CMI is
0.027880834445930219... and 0.107413011778490127... nats; count CMI is
0.010556456186247042... and 0.051700561590490643... nats.
Labelled CMI agrees with CL-T34 event-slot MI to 1.62e-158.
Neutral and parity zeros also have exact conditional-independence certificates.
No universal monotonicity law under coarsening the conditioning variable is
asserted. See the report and full-decimal temporal-information table.
