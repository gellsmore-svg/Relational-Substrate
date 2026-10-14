# Generation 8H: history as state

## A. External Review 008G

[Review 008G](../provenance/reviews/008G-chatgpt-review-v0.8g.md) targets
`research/constraint-lab-v0.8g-formal-integration` at
`22e252e560cc711d337b6ae506b0fb76728247d6`. It records 11 commits beyond 8F,
45 catalogue entries, snapshot run 38438048094 (301 tests), and successful
final-head run 38439269919. No G0 computation or new stochastic experiment opened.
The inspection scope includes chronology, grammar, expressivity, the literal-only
K/order correction, stationary factorisation and its counterexample boundary,
equivalence/quotients, H/L compilation, coherence and provenance.

## B. Why H now

CL-T12 constructs any positive current-state event-weight table on existing finite
O2/O3 single-toggle support, with K<=D and J<=D*2^D in the unbounded positive-factor
backend. It supplies one row per x under one fixed program. Increasing K/J cannot
give that same x two history-conditioned rows. This round tests that precise
boundary, without changing material variables or challenging the autonomous
single-action stationary factorisation theorem by increasing N.

## C. Provenance and frozen H0 plan

Branch: `research/constraint-lab-v0.8h-history-as-state`, based exactly on the
reviewed 8G head. Repository commands and edits execute as cello.
Review 008G and Prompt 008H storage precede implementation in commit `2a29df1`.
The Prompt 008G authored artifact is externally reported as 45,624 bytes,
SHA256 `e2b9ba3c4bef322b060b48d7629d29b439d1f2636b5e6e35db6e4e7c158a5a62`.
Its preserved agent transcription is 45,632 bytes,
SHA256 `81703b51e2d869da5fda862d9528c854846cdf8b037f54aac6ad400a7f1e704e`.
These are distinct representations.

Stored [Prompt 008H](../provenance/prompts/008H-v0.8h-agent-input.md): 46,117 bytes,
SHA256 `b55eb3a4d0050a32a1560fe5faaf5303683cff0d4540ab9abd7dd6a6451725b3`.
It is an agent transcription, not an independently byte-verified authored artifact;
authored metadata and the byte relationship remain unknown. It is preserved.

The [frozen plan](../exploration/generation-008h/round-h0-plan.json) was committed
and pushed at `e9f8f3b5b6fae99932ce6a289b6d15c39336a4c4` before non-neutral execution.
Canonical plan hash: `77fc2950ea394245cb0bcd441b35fed608c413961d41d8f44fa0e2ccd34ceb3a`.
File SHA256: `62c95c57e5d0fe03a91198c5d90f1164e5be2b035b3e28e6f76bb7ff05ba4ff8`.
The freeze receipt records zero actual non-neutral pre-freeze H0 cells. Symbolic
proofs were labelled externally predeclared analytic expectations; neutral
six-slot plumbing was pre-observed, and the non-neutral synthetic fixture used
three slots with multiplier 2. No target-grade exact/numerical check ran pre-freeze.

H0 has 11 atomic deterministic items: three witnesses, three kernels, three
temporal analyses, non-lumpability and augmentation. Work includes 6,912 rational
epoch transition entries, 1,008 raw-triad absorption rows, 6,048 quotient checks,
6,912 consistent material triples, 41,472 two-step augmented paths and 71,680
deterministic full-state updates. Budget: 60 seconds total, 10 MB, one worker;
actual item times total about 1.51 seconds, each below 0.25 seconds. No supervisor
or stochastic trajectory was needed. Exact results were committed at `10292af`.
The session resumed from that intact checkpoint; no plan or result was rewritten.

Probabilities and balance identities use fractions. Information uses 160 decimal
digits; floating eigenvalue checks use NumPy. Frozen rational gaps are exact;
information/eigenvalue tolerance is 1e-13. Maximum observed information formula gap
is 2e-160 and floating eigenvalue gap 4.441e-16. All rational validation gaps are zero.
See the [summary and hashed outputs](generation-008h-round-h0-tables.json) and
[validation](tables/generation-008h-validation.json).

## D. History-state semantics

N=4, O=3, G=S=L=0, independent hypergraph. Ordinary x has all six pair and four
triad bits. The separate register h is the sentinel None or a pair slot 0..5.
Augmented state is z_H=(x,h). H_pair=1 means one remembered pair event, not six
steps and not a redefinition of the programme's entire H axis.

A pair event e toggles its bit and sets h'=e. A triad event toggles its triad bit
and preserves h. The register therefore survives intervening triad-only events.
No new entity-state channel, geometry or dynamical constraint object is introduced.

## E. Reversal-memory controller

RECENT-REVERSAL(m), m>0, gives pair slot h multiplier m and every other event unit
weight; all ten weights are unit at the sentinel. The controller is label-covariant
because it tests equality with whichever pair slot was most recently toggled.
Repeating that pair slot reverses the most recent pair change, even across triad
events. m=4 favours this reversal; m=1/4 suppresses it; m=1 is H-neutral.

For non-sentinel h the full-event row has remembered weight m/(m+9) and nine
weights 1/(m+9). Conditioning on a pair event divides by pair mass (m+5)/(m+9),
giving q_h(h)=m/(m+5), q_h(e!=h)=1/(m+5). The sentinel gives 1/10 full and 1/6 pair.

## F. Common-start same-endpoint witness

Start x0 has only edge 01, all triads zero, h0=None. M forms 23 then 12; E forms
12 then 23. Both use one program, one m, one baseline, support and full-event clock.
They have equal length and event multiset; only order differs. Both end with
01-12-23, labelled pair mask 41, triad mask zero. The existing canonical S4 class
representative is 13; the labelled witness mask is not a redefinition of it.
The complete material bytes are `2900` in the recorded little-endian encoding.
All ten bits, support, baseline and empty fixed ordinary constraint set coincide.
Endpoint histories are slots 3 (12) and 5 (23).

Each full-event path has positive probability 1/[10(m+9)] for every m>0:
2/185, 1/100, 1/130 for m=1/4,1,4 respectively. Only these two event orders can
reach this endpoint in two full events; their equality also justifies the equal
conditional history prior used in the information comparison.

## G. Immediate divergent future rows

At the common endpoint, the full rows exchange probabilities m/(m+9) and 1/(m+9)
on slots 12 and 23. Pair rows exchange m/(m+5) and 1/(m+5). Rows differ iff m!=1.
Only those two coordinates contribute to equal-prior JS, giving

```text
JS_D(m) = [m ln(2m/(m+1)) + ln(2/(m+1))] / D
D_full = m+9; D_pair = m+5.
```

The values below were calculated from rational rows, independently checked against
the symbolic formula, and then compared with the external review references.
All information units are nats. Display rounding does not replace the saved precision.

| m | Full-row max gap | Pair-row max gap | Full-row JS | Pair-row JS | Shape JS |
| --- | --- | --- | --- | --- | --- |
| 1/4 | 3/37 | 1/7 | 0.0260465887867240 | 0.0458916088147041 | 0.0312623185951735 |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 4 | 3/13 | 1/3 | 0.0741325988545221 | 0.1070804205676430 | 0.0904370516073113 |

## H. Pure graph-shape witness

Mechanical graph classification of the six pair toggles gives:

| Event | Resulting shape | Historical class representative |
| --- | --- | --- |
| dissolve 01 | two-edge path | 3 |
| dissolve 12 | two-edge matching | 12 |
| dissolve 23 | two-edge path | 3 |
| form 02 | triangle + pendant | 15 |
| form 03 | four-cycle | 30 |
| form 13 | triangle + pendant | 15 |

For both histories, next edge-count probabilities are (m+2)/(m+5) for 2 edges
and 3/(m+5) for 4 edges. Thus I(history; next edge count)=0 exactly.

| Shape | M: middle last | E: end last |
| --- | --- | --- |
| two-edge path | 2/(m+5) | (m+1)/(m+5) |
| two-edge matching | m/(m+5) | 1/(m+5) |
| triangle + pendant | 2/(m+5) | 2/(m+5) |
| four-cycle | 1/(m+5) | 1/(m+5) |

The graph class determines edge count, so the information chain rule yields
I(history; class)=I(history; class | edge count). For equal history priors this is
the shape JS in section G. It is a shape effect beyond density, while some labelled
slot information is additionally lost by class projection. Full rows, pair rows,
class laws and exact path controls are in the [witness table](tables/generation-008h-witness.json).

## I. Strong lumpability failure

For projection (x,h)->x, the block x'=x xor 2^3 (slot 3, pair 12) receives m/(m+9) from z_M
and 1/(m+9) from z_E. This is a whole transition-block witness, not merely a
different summary statistic. Strong lumpability fails for m!=1. It holds for m=1,
including the sentinel. The pair-clock block gaps are 1/7 and 1/3 at the strong
grades. This instantiates 8A's F011-QUOTIENT-INVALID principle and CL-T20:
valid quotients must preserve the whole transition law.

## J. Fixed-state non-compilability

A fixed first-order H=0 kernel K0 on unchanged x must assign one row to x*.
Matching every history-conditioned future would require this one row to equal
both distinct projected rows. Contradiction for m!=1, irrespective of ordinary
K/J budget. The claim is restricted to unchanged ordinary state and all conditioned
rows; it does not prohibit enlarged-state representations or special marginal fits.

## K. State augmentation and restored Markov form

On (x,h), next probabilities and the deterministic update depend only on current
augmented state. The process is first-order Markov. The ordinary material
projection lacks this sufficiency. Finite memory can be stored in a larger present
state; this result proves neither absolute non-Markovianity nor irreducible time.
Moving the register to an explicit future S channel would be a representation
change, with support/update obligations, rather than unchanged-x compilation.

## L. Exact pair-event quotient

Triad-only events change neither pair mask nor h. Their total full-event
probability is 4/(m+9), independent of raw triad state. Summing any number of
such excursions before event e gives [w_e/(m+9)]/[1-4/(m+9)]=w_e/(m+5).
This proves closure on (pair_mask,h) before applying the reduction. Exact raw-state
absorption solves verify it for all 16 triad masks at pair masks 0,41,63 and every
history including the sentinel: 1,008 rows, zero rational discrepancy.

After the first pair event there are 64*6=384 states. Transition e sends
(p,h)->(p xor 2^e,e) with q_h(e). Sparse rational kernels are published;
no dense 7,168-state full augmented kernel was constructed.

## M. Event-slot Markov chain

After a pair event E_k=h_k. The six-state matrix Q has diagonal a=m/(m+5),
off-diagonal b=1/(m+5). It is symmetric and doubly stochastic, with uniform
stationary history. Q=Pi+lambda(I-Pi), Pi_ij=1/6, lambda=(m-1)/(m+5).
The eigenvalues are 1 and lambda with multiplicity five.

| m | lambda | Repeat / material backtrack | Consecutive-event MI |
| --- | --- | --- | --- |
| 1/4 | -1/7 | 1/21 | 0.0675173754283374 |
| 1 | 0 | 1/6 | 0 |
| 4 | 1/3 | 4/9 | 0.2106657190562314 |

Negative lambda is anti-persistence of slot identity; positive lambda is persistence.
These describe temporal correlations without psychological or purposive meaning.
I(E_k;E_{k+1})=ln 6+a ln a+5b ln b, checked against the enumerated stationary joint.

## N. Stationary augmented law

For each destination (p',j), predecessors are (p' xor 2^j,i), i=0..5. Incoming
probabilities sum to (m+5)/(m+5)=1. Thus pi(p,h)=1/384 satisfies pi T=pi exactly
for every m>0. Every pair slot sequence has positive probability. One can reach
any target mask and then append j,j without changing that mask to end at history
j; hence the recurrent chain is irreducible and stationary pi is unique.

Every transition flips mask parity, and repeating a slot permits a two-step return,
so the period is two. A fixed-parity start does not converge pointwise to uniform
over both parities. Stationary law, parity-conditioned limits and Cesaro occupancy
are distinct. Exact column balance, marginal and independence checks pass for all
three grades; uniformity is not inferred solely from symmetry intuition.

## O. Stationary material occupancy

The joint law explicitly factorises: pi(p,h)=(1/64)(1/6). Pair masks are uniform,
and history is independent of mask. Labelled-mask, edge-count and graph-class
occupancy therefore equal H-neutral baseline occupancy for every m>0.
Conditional shape discrimination at x*,h and stationary history-marginalised
occupancy equality concern different conditioning; they are compatible.

## P. One-step projected material law

At stationary pair epochs, averaging q_h(e) over independent uniform h gives
[m+5]/[6(m+5)]=1/6 for each e. The one-step projected pair transition equals H0
exactly. This is a pair-clock result: the full-event pair-versus-triad hazard
(m+5)/(m+9) changes with m, so no full-event one-step agreement is asserted.

## Q. Two-step temporal witness

P_k xor P_{k-1} identifies the last pair slot. Material backtracking is exactly
slot repetition: Pr(P_{k+1}=P_{k-1})=m/(m+5). H0 gives 1/6. The two non-neutral
values 1/21 and 4/9 differ despite identical stationary occupancy and stationary
one-step pair laws. History changes process grammar without changing one-time
stationary material structure in this model. Static occupancy cannot test this H.

## R. Projected Markov order

Given a legal previous/current pair-mask pair, h_k is recovered from their one-hot
XOR. Hence the next row depends on those two snapshots and no earlier snapshot.
All 2,304 consistent triples per grade verify zero order-two sufficiency gap.
At stationary current mask 0, previous masks 1 and 2 recover different h and give
different next rows for m!=1; both pasts have positive probability. Order one fails,
so the pair-mask process is exactly order two. It is first-order at m=1.
The statement concerns pair epochs after an observed pair transition, not a
finite-order claim for snapshots on the full-event clock with arbitrary triad waits.

## S. Initial-history decay

Q^k=Pi+lambda^k(I-Pi). Starting with history i gives probability
(1+5 lambda^k)/6 at i and (1-lambda^k)/6 elsewhere. TV to uniform is
(5/6)|lambda|^k. Exact matrix powers at k=0,1,2,4,8,16,32,64 verify this identity.
Since |lambda|<1 for every finite m>0, initial-slot information decays. This is
forgetting of the initial history slot in h_k, not a claim that every material
multi-time observable loses all initial-condition information at that same rate.

## T. Current history efficacy versus initial-history memory

For non-neutral m, current h continues to change the next row while h_k forgets h0.
This is the H>0 counterpart of F018-LOCAL-VERSUS-INITIAL and F8C-CURRENT-SURVIVES.
Possessing a history register does not mean retaining the initial register forever.
No master memory score combines row JS, shape JS, backtracking, MI, decay,
occupancy, lumpability or Markov order.

## U. Observations

FINITE EXACT RESULT: six legal common-start paths in the three-grade palette have
equal paired probabilities and byte-identical material endpoints. Non-neutral
rows and graph-class laws differ; edge-count laws agree exactly. All rational
kernel balance, quotient and temporal identities pass. NUMERICAL RESULT:
160-digit information and floating eigenvalues agree with analytic expressions
within frozen tolerances. FORMAL THEOREM: the symbolic arguments in
[history.md](../formal/history.md) hold under their declared assumptions for m>0,
rather than extrapolation from three finite cases.

## V. Inferences

The unchanged ordinary material representation is insufficient as a first-order
Markov state for this controller. Increasing current-state K/J cannot fix the
conditional-row contradiction. History has a temporal signature even when static
and stationary one-step pair statistics match baseline. Augmentation restores
Markov sufficiency. These are model inferences with explicit representation/clock.

## W. RS / global-coherence interpretation

The same present ordinary relational configuration can receive different future
possibilities when process-carried historical information is admitted in the law.
The declared x omits h; the richer present (x,h) contains the relevant memory.
This establishes no natural memory law, physical non-Markovianity, primitive time,
design, theology, adaptation, repair, controlled fragility or direct TCR proof.

## X. Next options and H1 decision

H0 answers the intended boundary cleanly. No H1 follow-up is opened. The attention
coordinates below are ordinal 0..5, never summed: CN contextual novelty, RD routing
diversity, RC recurrence/return structure, EC explanatory compression, CG coherence
relevance, CB computational boundedness. These direct attention, not confidence.

| Candidate, unopened | CN | RD | RC | EC | CG | CB |
| --- | --- | --- | --- | --- | --- | --- |
| Minimal sufficient register for this controller | 3 | 1 | 3 | 5 | 5 | 5 |
| H2: a mechanism requiring two remembered pair events | 5 | 3 | 4 | 4 | 5 | 4 |
| Recent construction order and controlled dissolution | 4 | 5 | 4 | 3 | 4 | 3 |
| Survival of history effects under class coarse-graining | 4 | 4 | 4 | 4 | 5 | 4 |
| History producing persistent visible occupancy structure | 5 | 4 | 5 | 4 | 5 | 3 |
| L>0 common-program dynamic rule-state witness | 5 | 3 | 3 | 4 | 5 | 3 |
| N=5 with a specified richer-topology hypothesis | 3 | 4 | 3 | 2 | 3 | 2 |
| Scoped book/formal synthesis without new experiments | 2 | 1 | 1 | 5 | 5 | 5 |

The next formal question is the minimal augmentation needed to restore first-order
Markovity. Last pair slot is sufficient here with six values; a general hidden-state
minimisation problem is outside H0. L, N5 and book edits do not open automatically.

## Y. Coherence-map update

The close-out adds separate nodes for same-state futures, non-lumpability,
fixed-state non-compilability, augmentation, pure shape, stationary invariance,
temporal correlation, exact order two, current-versus-initial memory and the
methodological/interpretive consequences. Links use the exact motivating IDs
listed in the frozen plan. Q-H-POSITIVE is retained and marked qualified (partially
answered), with its original statement/layer preserved and a resolution record.
CL-Q02 remains a historical 8G open entry; new verified entries answer its scoped
existence question rather than rewriting that historical entry.

Sharper open questions concern history functions/minimal augmentation, necessary
depth, persistent occupancy effects and survival under coarse-graining. Canonical
JSONL ledgers generate current-map.md/current-map.mmd and the immutable
[through-008H snapshot](../coherence/snapshots/through-generation-008h.md).
Snapshot and canonical-ledger SHA256 values are recorded in Execution 008H after
generation; no circular self-hash is embedded in the snapshot. The catalogue,
generated views, provenance and final closing-head CI are checked at close-out.
