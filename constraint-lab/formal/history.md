# History as state

## Analytic phase

This document was drafted before H0 freeze. Its symbolic results are externally
predeclared analytic expectations; non-neutral exact/numerical W4 verification
remains unopened at drafting. A post-H0 appendix records verification and catalogue
links. This is model mathematics, not an assertion about physical historical ontology.

## 1. Material state versus history state

The complete ordinary material state x has six pair and four independent triad bits.
The register h is None (start sentinel) or one of six pair slots. Locally write
z_H=(x,h), to avoid silently replacing 8G's z notation for other pair coordinates.

The register is present state on the augmented representation, with a historical
origin. It is not contained in x or an unreported material variable. S=0 and L=0
remain: no new entity-state channel or dynamical constraint object is introduced.

## 2. H_pair=1 semantics

H_pair=1 means one remembered **pair event**, not six time steps or the last full
event. Pair event e sets h'=e; a triad event leaves h'=h. All events toggle precisely
one ordinary relation bit. A repeated pair slot restores the preceding pair mask,
even if triad bits have changed during the wait.

Full state indexing is 7*x+(0 for None, otherwise h+1); this describes 7168 possible
augmented states but no dense full kernel is needed. After the first pair event,
the pair-epoch representation has 64*6=384 recurrent states, indexed 6*p+h.

## 3. Reversal-memory controller

RECENT-REVERSAL(m), m>0, gives pair slot h weight m and every other full slot unit
weight. None gives all ten unit weights. The fixed ordinary constraint set is empty;
the history controller is one common static program, not separate rules chosen for
the two paths.

For non-sentinel h, full probabilities have denominator m+9. Immediate pair
conditioning has denominator m+5. The policy is label-covariant: simultaneous
relabelling of pair coordinates, event slots and h preserves equality e=h.

## 4. Same-state divergent futures

Start x0 with only 01 present and all triads absent, h0=None. Histories M=(23,12)
and E=(12,23) each contain two formation events and no hidden event. Both are legal
and each has full-event path probability 1/[10(m+9)].

Both endpoints have pair mask 41 (01,12,23) and triad mask zero, identical material
bytes, support, baseline and fixed ordinary constraints. They differ only in h:
slot 12 versus slot 23. The historical S4 canonical class representative is 13;
the specified labelled path is 41. No old canonical mask is redefined.

For m!=1, the remembered-slot probabilities exchange m/D and 1/D, D=m+9 (full)
or m+5 (pair). Thus rows differ at the same x. Equal-prior row JS is
[m ln(2m/(m+1))+ln(2/(m+1))]/D: only the two exchanged coordinates contribute.
All common coordinates contribute zero.

At this two-full-event endpoint, only the two permutations of those changed pair
slots can reach x* from x0. Equal path probabilities therefore also justify the
equal history prior after conditioning on that endpoint, not a fitted prior.

Dissolution of the path's middle edge yields a matching; end-edge dissolution
yields a two-edge path. Both history-conditioned edge-count laws have weights
(m+2,3)/(m+5) on (2,4), but their class laws differ. 'Pure shape witness' means a
shape difference with zero edge-count information, not zero labelled remainder.

## 5. Strong lumpability

History erasure sends (x,h) to x. The aggregate probability into x'=x xor 2^e is
the event probability for e. At the common endpoint, histories a and b give
m/(m+9) versus 1/(m+9) into the block for e=a when m!=1. This violates strong
lumpability. Pair-clock erasure similarly differs by (m-1)/(m+5).

At m=1, full probabilities 1/10 and pair probabilities 1/6 are independent of h,
including the sentinel. History erasure then is strongly lumpable.

Non-lumpability means there is no first-order quotient valid for every augmented
initial law. It alone does not prove failure under every specially selected prior;
the stationary material order-two result below supplies a separate stronger witness.
This instantiates the 8A/CL-T20 whole-transition-law quotient principle.

## 6. Fixed-state non-compilability

A fixed H=0 kernel on unchanged x has one row at x*. Matching both history-
conditioned rows would require that row to equal two unequal vectors. Contradiction
for m!=1. This applies irrespective of K/J expansion on unchanged x.

CL-T12 can construct any positive row for x but cannot assign two different rows
to that same x under one fixed ordinary program. The histories also have the same
event count and multiset; time count or aggregate incidence cannot substitute for
their order.

## 7. State augmentation

The controller's next probabilities and deterministic update depend only on (x,h),
so the augmented process is first-order Markov. This is representation-relative
memory, not absolute non-Markovianity or irreducible time.

Compiling a finite register into explicit current variables changes represented
state. Its simultaneous register/material update need not be a single-bit event
in a binary encoding. Markov restoration is not a claim that CL-T12 automatically
compiles arbitrary augmented update support into the unchanged toggle grammar.

## 8. Exact pair-event quotient

For fixed pair mask/history, hidden-only transitions change neither coordinate.
Their total full-event probability is 4/(m+9), independent of hidden state; event e
has full probability w_e/(m+9). Sum over any number of hidden events to obtain
w_e/(m+5). The sentinel similarly gives 1/6.

Equivalently, solve (I-T)Q=B on all 16 raw triad states. Constant pair-absorption
right-hand sides and T's constant row sum give the same projected law for every
raw triad mask. No uniform-triad prior or graph-only hidden quotient is assumed.

The closed epoch update is (p,h)->(p xor 2^e,e). The transient sentinel is handled
separately. All six slots are always possible because m>0.

## 9. Stationary augmented law and occupancy

For destination (p',j), predecessors are (p' xor 2^j,i), i=0..5. Their weights sum
to [m+5]/[m+5]=1. Therefore uniform pi(p,h)=1/384 satisfies pi E=pi by direct balance.

Every finite slot sequence is possible, giving communication between all recurrent
states. Repeating the remembered slot twice gives a two-step return; pair parity
forces even returns, so the chain has period two. Stationarity is unique, but a
fixed-parity start does not converge at every epoch to the full uniform vector.
Parity-conditioned limits and Cesaro occupancy must not be confused.

Uniform joint occupancy proves pair/history independence, not merely uniform
marginals. The pair marginal is 1/64 per mask, so graph-class and edge-count
occupancy match H=0. Under stationary history averaging,
sum_h q_h(e)/6=1/6. The one-step **pair-clock** material transition agrees with H=0.

This is not a claim of full-event one-step agreement: the full normaliser m+9
changes pair-versus-triad hazard. Conditional shape differences and stationary
history-marginalised occupancy equality answer different questions.

## 10. Temporal correlations and initial-history decay

The six-slot event/history matrix is
Q=Pi+lambda(I-Pi), lambda=(m-1)/(m+5), Pi_ij=1/6.
The uniform mode has eigenvalue 1, and the five independent zero-sum modes have
eigenvalue lambda. The stationary history law is uniform. Positive/negative lambda
means slot persistence/anti-persistence, not psychological behaviour.

Q^k=Pi+lambda^k(I-Pi). Conditional on initial slot i, diagonal probability is
(1+5 lambda^k)/6 and other probabilities (1-lambda^k)/6. TV to uniform is
(5/6)|lambda|^k. For finite m>0, |lambda|<1: initial history is forgotten even
though current h continues to alter the next slot.

At stationary uniform h, consecutive-event MI is ln(6)+a ln(a)+5b ln(b), with
a=m/(m+5), b=1/(m+5). Repeating the slot occurs with probability a, equal to
Pr(P_{k+1}=P_{k-1}). H-neutral iid slots give 1/6 and zero consecutive-slot MI.
Static occupancy alone cannot test memory.

## 11. Projected Markov order

After one observed pair transition, P_k xor P_{k-1} is one-hot and identifies h_k.
Therefore the next pair law depends only on these two snapshots, independently of
earlier snapshots. This proves order at most two after the first transition.

At stationarity all legal previous transitions into a fixed P_k have positive
probability. Different recovered slots give different next rows for m!=1, proving
order one fails and the material pair process has exactly order two. At m=1 it is
the ordinary first-order pair toggle chain, while event slots are iid.

This finite order refers to the pair-event clock. Arbitrarily many intervening
triad events prevent identifying the last pair slot from just the last two
full-event snapshots; no finite full-clock order claim is made here.

## 12. Scope and non-claims

The memory register is explicit and finite. Richer current augmented state contains
the relevant memory. This does not prove that 'the present does not contain the
past', physical law is non-Markovian, time is irreducible, or nature uses this
controller. Reversal preference is not repair, adaptation, fragility, design or
theology. TCR is not proved.

K is simultaneous ordinary current-state expression complexity; J composes those
features; H admits prior process information not determined by ordinary x;
L would make constraint configuration itself dynamical. This fixed historical
controller is L=0. Future S encoding, longer H, scale or meta depth requires a
separate representation/compilation question and frozen scope.

## 13. Verified H0 appendix

H0 was frozen and pushed at e9f8f3b5b6fae99932ce6a289b6d15c39336a4c4.
The subsequent exact calculations, published at 10292af, verify the predeclared
expectations for m=1/4,1,4. The following proofs are algebraic statements under the
declared model, independently of the finite palette verification. The earlier
draft-phase text is retained as drafting provenance, not a claim that H0 remains
unopened. The [report](../reports/generation-008h-history-as-state.md) and hashed
tables distinguish finite exact identities from numerical information/eigenvalues.

<a id="cl-t26"></a>
### CL-T26: same-state divergent futures

For every m>0, M=(23,12) and E=(12,23) from (x0,None) have probability
1/[10(m+9)]>0. The first event has probability 1/10 and the distinct second slot
has probability 1/(m+9). Toggle commutation yields identical all-ten-bit x*,
but h is 12 versus 23. Into x* xor 2^3 (slot 3, pair 12), full probabilities are m/(m+9)
and 1/(m+9). Pair conditioning yields m/(m+5) and 1/(m+5). Thus both rows
diverge iff m!=1. No hidden current triad or different fixed program explains it.

<a id="cl-t27"></a>
### CL-T27: history erasure and strong lumpability

Strong lumpability requires equal aggregate probability into each x' block for
every augmented state in the same x block. CL-T26 supplies a violated block for
non-neutral m, on both clocks. At m=1, full and pair rows are uniformly 1/10
and 1/6 for every h, including None; all projected block rows agree. Hence
history erasure is strongly lumpable iff m=1. By CL-T20 and the 8A quotient
principle, a graph/statistic match cannot substitute for whole-block equality.
Failure excludes a first-order quotient valid for arbitrary augmented initial
laws, while a stationary-prior Markov-order claim needs the additional CL-T33.

<a id="cl-t28"></a>
### CL-T28: fixed-state H0 non-compilability

Suppose a fixed first-order K0 on unchanged x reproduces every projected
history-conditioned row. At x*, K0(x*,.) must equal both rows in CL-T26.
For m!=1 they differ, a contradiction. This is independent of K/J budgets.
CL-T12 allows any single positive row on existing support; it cannot give one
fixed program two rows at the identical x. The theorem does not exclude
state augmentation, altered support or marginal-only agreement.

<a id="cl-t29"></a>
### CL-T29: Markov restoration by augmentation

The event row is a function of current h, and the deterministic update maps
(x,h,e) to (x xor 2^e, e if pair else h). Thus (x,h) is first-order Markov.
History relative to x becomes current represented state after augmentation.
A binary encoding might require simultaneous material/register bit updates;
this proof neither invokes unchanged-support CL-T12 nor adds an S channel to H0.

<a id="cl-t30"></a>
### CL-T30: exact pair-event closure

Fix pair mask p and h. Triad-only events preserve both. For h!=None their total
probability is r=4/(m+9)<1, with event-e mass w_e/(m+9) on every raw triad mask.
Summing r^k w_e/(m+9) for k>=0 yields w_e/(m+5). The sentinel likewise gives
(1/10)/(1-4/10)=1/6. The next pair event occurs almost surely. Its update depends
only on (p,h), establishing the exact epoch kernel on 384 recurrent states.
This closure uses event semantics and constant row sums, not a chosen triad prior.

<a id="cl-t31"></a>
### CL-T31: stationary uniformity and one-step invisibility

For a destination (p',j), only predecessors (p' xor 2^j,i) contribute. Their
transition probabilities sum over i to (m+5)/(m+5)=1, so every column as well as
every row sums to one. Uniform pi=1/384 satisfies direct balance. Positive slot
probabilities allow any toggle sequence to reach a target mask, followed by j,j
to end at history j without changing it. This proves irreducibility and unique
stationarity. Pair parity flips each step, and repeating the current slot gives
a two-step return; the period is two.

The joint distribution is explicitly pi(p,h)=(1/64)(1/6), so history and mask
are independent, not merely marginally uniform. Pair-mask, edge-count and class
occupancy match H0. The stationary one-step projected slot probability is
sum_h q_h(e)/6=1/6. This is a pair-clock equality; full-event pair hazard changes.
Stationary occupancy equality does not assert pointwise convergence from fixed
parity or equality of higher-order process laws.

<a id="cl-t32"></a>
### CL-T32: slot eigenstructure and initial-history forgetting

Let Pi be the uniform rank-one matrix. Direct substitution gives
Q=Pi+lambda(I-Pi), lambda=(m-1)/(m+5). Pi is the identity on the constant mode;
I-Pi is the identity on the five-dimensional zero-sum space. Hence eigenvalues
are 1 and lambda (multiplicity five), and Q^k=Pi+lambda^k(I-Pi).
For finite m>0, -1/5<lambda<1, hence |lambda|<1. Starting at i yields the
diagonal/off-diagonal probabilities in section 10 and TV=(5/6)|lambda|^k.
Initial-slot information in h_k tends to zero; current non-neutral h still
changes the next event. No identical decay rate for all material observables
is implied.

<a id="cl-t33"></a>
### CL-T33: exact projected pair-mask order

After an observed pair transition, P_k xor P_{k-1}=2^h_k, so any legal last two
pair snapshots determine the next row q_h_k. Earlier snapshots add no conditional
information: order is at most two under every compatible law. Under stationary
pi, for a fixed current mask each previous neighbour occurs with positive mass.
Different incoming slots give different next rows for m!=1 by CL-T26's row
argument. Order one therefore fails at stationarity, proving exact order two.
For m=1 the pair-mask toggle chain is first-order (event slots are iid). This
does not assign a finite Markov order on the full-event snapshot clock.

<a id="cl-t34"></a>
### CL-T34: temporal backtracking and event information

Two consecutive toggles restore a pair mask iff their slots coincide. With
a=m/(m+5), b=1/(m+5), this event has probability a. At stationary uniform history
the joint slot law is Q_ij/6 and both marginals are uniform. Direct KL evaluation
gives I(E_k;E_{k+1})=ln 6+a ln a+5b ln b. It is zero iff m=1 and positive
otherwise, since KL vanishes only when the conditional row is uniform.
Backtracking differs from the H0 value 1/6 iff m!=1. These two-time signatures
coexist with CL-T31's one-time and stationary one-step projected equalities.

<a id="cl-t35"></a>
### CL-T35: pure shape discrimination at equal edge-count law

At x*, the historical graph classifier maps the three dissolutions to
(two-edge path, matching, two-edge path), and the three formations to
(triangle+pendant, four-cycle, triangle+pendant). Summing exact event weights
gives the two class laws in report section H. Both assign dissolution weight
m+2 and formation weight 3, proving identical next edge-count laws.
The matching masses m/(m+5) and 1/(m+5) differ iff m!=1, proving shape
discrimination. Since class determines edge count, the information chain rule
gives I(history;class)=I(history;class|edge count) under the equal history prior.

Independently summing the two differing slot contributions gives row JS
[m ln(2m/(m+1))+ln(2/(m+1))]/D, with D=m+5 or m+9 on the respective clocks.
For the differing path/matching class masses, let D=m+5. Their JS is

```text
[2 ln(4/(m+3)) + (m+1) ln(2(m+1)/(m+3))
 + m ln(2m/(m+1)) + ln(2/(m+1))] / (2D).
```

The other two classes are shared and contribute zero. This derives the numerical
shape references from classified laws rather than treating the references as input.

### Finite and numerical verification, and remaining question

CL-F05 records the bounded rational H0 checks; CL-N07 separately records the
160-digit information values and floating eigenvalue cross-checks. CL-Q02
remains the historical 8G open entry. Its scoped existence question is answered
by CL-T26, while the broad Q-H-POSITIVE is only partially answered.

CL-Q06 asks which minimal state augmentation restores first-order sufficiency
for this controller. The six-valued last-pair register is sufficient; a general
hidden-state minimisation problem is not opened. Relevant history functions,
greater necessary depth, occupancy-changing memory and coarse-graining survival
remain separate future questions.

## Generation 8I predictive-state addition

The historical 8H derivation and its then-open questions above are retained.
The alternative predictive-state 8I determines the coarsest strongly lumpable
refinement of four declared observations on the same 384-state process.
History representation depends on observation scale: labelled pair identity,
current graph automorphism role, last formation/dissolution, then none under
parity. Non-neutral minimal counts are 384/28/12/2; neutral 64/11/7/2.
Class/count order-two synchronization and parity all-order erasure are proved
in [predictive-state formalism](predictive-state.md), CL-T52..T59 and CL-F08.
CL-Q06 remains the historical open entry; its specific preserved-observation
question receives a bounded answer, not a general hidden-model minimisation.

## Generation 8K synthesis addition

The [state taxonomy](state-taxonomy.md) distinguishes historical origin from
predictive sufficiency and hidden CURRENT coordinates. The
[general predictive theory](predictive-state-theory.md) places strong refinement,
trace equivalence, stationary matching, synchronization and observed order in
separate scopes. Stationary adjacent-law matching in 8H is not weak lumpability.

[Axis compilation](axis-compilation.md) generalises the augmentation argument
under explicit closed-joint-law assumptions (CL-T64/T65). Finite constraint
state can also flatten; neither H nor L is absolutely beyond Markov state.
Support/clock/category-preserving compilers ask different questions.
H2 and L sketches are written but unexecuted. The proposed H2 witness holds
complete X and last pair fixed while varying the second-last pair. Any necessity
claim excludes enlarged history alphabets and hidden-state recoding explicitly.

## Generation 8L: depth-two capability, after separate freeze

The prior paragraphs preserve 8K's historical state. H2-0 now executes the
SECOND-RECENT design: same complete X and same most-recent pair, different
second-most-recent pair and future row. Pair-clock material order is three;
adjacent event MI and three-time material CMI are exact nulls, while lag-two
event MI and four-time conditional information are positive non-neutrally.
Uniform pair-epoch occupancy remains unchanged. See
[history depth](history-depth.md) for compiler restrictions, exact proofs,
finite verification and explicit absence of a raw full-clock order claim.

## Generation 8M: Ordered History And Present Action

The [ordered-role grammar](history-role-depth-two.md) reads structural relations
among h1,h2,e, optionally conjoined with current candidate presence. All rules
remain fixed L=0 programmes. The invariant basis has 12 roles including the
ternary STAR/TRIANGLE split. Strict H2 necessity, persistent visible structure
and specified matched-H1 discrepancies are different claims. Neither statistical
dependence nor stationary occupancy alone proves necessary historical depth.

## Generation 8N: Matched Structural Access

[Controlled passage](history-controlled-passage.md) compares H2 with the unique
first-order kernel on exactly (P,h1) matching its full stationary adjacent law.
Stationary source-class conditionals match on (P,h1). Return routing, excursion
length, cross-class access time and competing-target probability are distinct
functionals; none assigns purpose or value to a topology.
