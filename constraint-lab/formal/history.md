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
