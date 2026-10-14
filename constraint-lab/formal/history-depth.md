# History depth: SECOND-RECENT and strict H1 insufficiency

Generation 8L, after the committed/pushed H2-0 plan and exact execution.
All temporal-order statements below use PAIR-EVENT EPOCHS unless explicitly
described as full-event rows. Proofs cover positive m; finite checks use
1/4,1,4. [State taxonomy](state-taxonomy.md), [strong refinement](predictive-state-theory.md)
and [compiler classes](axis-compilation.md) retain their 8K scope.

## 1. Semantic H_pair=d and two-slot state

H_pair=d means the declared summary retains the d most recent pair events in
ordered last-event semantics. It is not number of variables, bits, register
alphabet or refinement rounds. For d=2, H=(h1,h2), most recent first.
Sentinel null records unavailable history; valid stages are (null,null),
(e,null), and two labelled slots. Pair e updates (e,h1); triads preserve both.
The recurrent alphabet has 36 ordered values, including equal slots.

X remains the complete six pair/four independent triad-bit representation.
Z=(X,h1,h2) is closed and first-order Markov (CL-T64). H_pair=2 is sufficient
for this fixed controller. No constraint state eta or L-positive dynamics occurs.

## 2. Controller, covariance and event clocks

SECOND-RECENT(m) assigns weight m only to candidate pair e=h2; all other
ordinary toggles have weight one. Unavailable h2 gives all unit weights.
It reads no h1, ordinary bits, clock or labels as privileged constants.
Any vertex-induced pair bijection g preserves e=h2 iff g(e)=g(h2).
Mapping X,h1,h2 and events together conjugates the update and preserves weights.
The full-event denominator is m+9; the pair-conditioned denominator is m+5.
At sentinel they are ten and six respectively.

<a id="cl-t68"></a>
## 3. CL-T68: Same-(X,h1) common-start divergent futures

Choose a=01,b=12,c=23, all distinct. Start at X=0,H=(null,null).
The paths a,b,c and b,a,c consist entirely of legal formations, with equal
event count/multiset and one common fixed program. Endpoints both have
X*=path 01-12-23, triads zero, h1=c; their h2 values are b and a.

First and second full-event probabilities are 1/10, since h2 is unavailable
before both. At the third event h2 is the first slot, different from c.
Thus each full path has probability 1/[100(m+9)]>0.
At pair epochs each has probability 1/[36(m+5)]>0.
This pair-word probability marginalises intervening triad-only events and their
endpoint triad masks. The asserted byte-identical zero-triad full endpoint
belongs to the specified consecutive FULL-event histories, not to every full
realisation of the marginalized pair word.
The serialized complete ordinary endpoint is identical: ten bits, baseline,
all ten candidate toggle slots and fixed empty ordinary-rule collection.
Only the second history coordinate differs.

For m!=1, the two projected full-event rows differ at a/b by
absolute (m-1)/(m+9), and pair rows by absolute (m-1)/(m+5).
All other coordinates agree. They coincide at m=1.
For D=m+9 or m+5, their equal-prior JS is exactly

    [m ln(2m/(m+1)) + ln(2/(m+1))] / D.

The mixture on the exchanged coordinates has mass (m+1)/(2D); the unchanged
coordinates contribute zero. This derives the formula without reference values.

<a id="cl-t69"></a>
## 4. CL-T69: Strict semantic H1 non-compilability

Fix the compiler class: state EXACTLY (X,h1), with h1 the most recent pair slot;
unchanged ordinary single-toggle support, event clock and observed material;
arbitrary positive K/J allowed. No hidden state, persistent random seed, phase,
history recoding, enlarged alphabet or per-history program is admissible.
Equivalence means EVERY reachable history-conditioned ordinary future row,
not merely one-time occupancy, averaged rows or a fitted statistic.

One fixed kernel K1(X,h1;.) supplies one row at (X*,c).
CL-T68 requires two unequal rows there for m!=1, contradiction.
No K/J expansion repairs missing represented information. Forgetting h2 is
not strongly lumpable either: the a/b successor blocks have unequal sums.
For m=1, projected rows are h2-independent and history erasure is strongly lumpable.

The necessary depth is relative to this last-pair semantics (CL-M04).
A 36-valued augmented current variable can encode (h1,h2), so raw kernel
compilation is possible. That is not semantic H_pair=1 and does not establish
absolute non-Markovianity, global HMM minimality or minimum physical memory.

<a id="cl-t70"></a>
## 5. CL-T70: Exact pair-event closure and augmentation

Triad-only excursions leave p,h1,h2 and all pair weights unchanged.
For a recurrent register their total full hazard is 4/(m+9); summing excursions
before pair e gives

    [w_e/(m+9)] sum_(k>=0) [4/(m+9)]^k = w_e/(m+5).

At sentinel the same argument gives 1/6. Absorption is certain because positive
pair mass remains bounded away from zero for fixed m>0.
Raw triad state therefore sums out exactly, even though those bits may toggle.
No dense full augmented kernel is needed.

The recurrent pair chain is (p,i,j)->(p xor 2^e,e,i), with q_j(e).
It has 64*36=2304 states, six positive successors per state.
Index convention: (p*6+i)*6+j. This is an exact first-order pair-epoch process.
It is not a proof of a finite order for the raw full-event material projection.

<a id="cl-t71"></a>
## 6. CL-T71: Uniform stationary law, irreducibility and period

For target (p',e,i), predecessors are (p' xor 2^e,i,j), j=0..5.
Their incoming transition probabilities sum to sum_j q_j(e)=1.
Consequently pi(p,i,j)=1/2304 satisfies stationarity exactly.
The history-pair marginal is 1/36, pair-mask marginal 1/64, and the joint
factorises: material and the ordered history pair are independent.
This is a joint-balance proof, not inference from uniform marginals.

For any start (p,i,j) and target (p',i',j'), first toggle the set of bits with XOR
p xor p' xor 2^j' xor 2^i', then append j',i'. Positivity makes this path legal,
and it reaches the target regardless of the starting register. The same final
two events give reachability from sentinel. Thus there is one recurrent
communicating class and one stationary law.

Every epoch flips material parity, excluding odd returns. At diagonal history
(i,i), toggling i twice returns to the same augmented state with positive
probability. Irreducibility transfers the common period: exactly two.
A non-diagonal state need not itself have a two-step return. Stationarity does
not imply pointwise convergence from a fixed parity class.

Material count mass is binomial(6,k)/64 and class mass is labelled class size/64,
identical to neutral occupancy. Averaging h2 gives next slot probability 1/6.

<a id="cl-t72"></a>
## 7. CL-T72: Labelled strong predictive minimality and delayed separation

Different current masks are separated by the declared current observation.
At fixed p, different j immediately give different observed rows for m!=1.
At fixed p,j and i!=i', immediate rows AGREE, but any common positive next
event e shifts the second slot to i/i'. The next event f=i then has unequal
probability. The two-step observed WORD identifies both e and f from toggles,
so its probability differs without cancellation.

Thus all 36 history pairs at every p are future-distinct. A strongly lumpable
observation-preserving block implies equal future words (CL-T62), so no merge
is possible; the singleton partition is sufficient. The coarsest strong
refinement therefore has 2304 states for all positive m!=1.
At m=1 the material projection itself is strong, yielding 64 blocks.

Generic CL-T52 iteration starts at p. First signatures depend exactly on j,
giving 384 blocks (p,j). The next signatures distinguish i because successor
second-history equals i, giving 2304 singleton blocks. The independent
implementation actually produces 64->384->2304, not a special H2 shortcut.
Reverse state enumeration gives identical membership at both non-neutral grades.
The state-membership SHA256 is
fb74830e486e25d5caa7ec95f9eb74c3c60553034927350629194f37bd92da3c.

Compact certificates cover every same-mask history pair: 34,560 pairs have
different h2 and immediate observed signatures; 5,760 share h2 and differ
after the first split. Generic merge certificates are separately hashed.
Coarseness rests on the CL-T52 universal property and future-word proof,
not merely inability to merge a selected pair. Two rounds are not a general
definition of history depth. This is not unrestricted hidden-model minimisation.

<a id="cl-t73"></a>
## 8. CL-T73: Slot order two and even/odd factorisation

After event E_t, h1=E_t and h2=E_(t-1). Hence

    Pr(E_(t+1)=e | past) = q_(E_(t-1))(e).

Two slot observations suffice. For non-neutral m, fixing current E_t=i and
changing the supported previous slot j changes the next row, excluding order
one under the uniform stationary history law. Neutral slots are iid uniform
(order one under the programme's least-positive-order convention).

Finite stationary slot path probabilities are 1/36 times products of q factors
linking indices distance two. Splitting even and odd indices factorises the
path law into two independent stationary six-slot first-order chains with
the same q matrix as 8H. This is explanatory algebra only; no decay atlas runs.
Independent initial histories in this factorisation are a stationary assumption,
not a universal statement for arbitrary correlated initial registers.

<a id="cl-t74"></a>
## 9. CL-T74: Pair-mask order exactly three non-neutrally

From (P_(t-2),P_(t-1),P_t), the last two one-hot differences recover h2 and h1.
The next row is therefore determined by those three masks, without earlier
past. CL-T63 gives observed order at most three.

The canonical histories have last two masks {a,b},{a,b,c} identical and
different earlier masks {a}/{b}, with unequal next rows. These compatible
triples have positive stationary mass because all augmented states do.
Thus order at most two is impossible, proving stationary order exactly three
for all m>0,m!=1. At m=1 the material process is first-order uniform toggling.
This applies to LABELLED pair masks on the pair-event clock, not a graph/count
atlas or a full-clock order claim.

<a id="cl-t75"></a>
## 10. CL-T75: Exact adjacent nulls and lag-two conditional information

The uniform joint law gives

    Pr(E_t=i,E_(t+1)=e)=sum_j q_j(e)/36=1/36,
    Pr(E_(t-1)=j,E_(t+1)=e)=q_j(e)/6.

Adjacent slots are exactly independent. Lag-two repetition is m/(m+5).
Lag-two MI is ln6+a ln a+5b ln b, with a=m/(m+5), b=1/(m+5);
it is positive iff m!=1 by equality conditions for independent finite tables.

Given current (p,i,j), prior masks are p xor 2^i and then p xor 2^i xor 2^j.
Their joint with the next mask has mass q_j(e)/2304.
Summing j yields uniform compatible three-mask words, each 1/2304.
Therefore stationary material one-, two- AND three-time laws match H0,
and I(P_(t-1);P_(t+1)|P_t)=0 by exact conditional independence.

Condition on (P_(t-1),P_t), which fixes i; j remains uniform and determines
P_(t-2). Next mask identifies e. The conditional information

    I(P_(t-2);P_(t+1)|P_(t-1),P_t)

therefore equals I(E_(t-1);E_(t+1)), the lag-two formula above.
The non-neutral distinction first appears in labelled four-time words.
The saved 13,824 quadruple probabilities agree exactly with an independent
three-forward-transition enumeration from uniform stationarity.

<a id="cl-t76"></a>
## 11. CL-T76: Pure shape at fixed X and h1

At the common path, h2=b is the middle edge versus h2=a an end edge.
Mechanical graph classification gives next pair-event class rows:

| Class | Middle h2 | End h2 |
| --- | --- | --- |
| Two-edge path | 2/(m+5) | (m+1)/(m+5) |
| Two-edge matching | m/(m+5) | 1/(m+5) |
| Triangle plus pendant | 2/(m+5) | 2/(m+5) |
| Four-cycle | 1/(m+5) | 1/(m+5) |

Both dissolve with total weight m+2 and form with weight three.
Their next count laws agree exactly, hence equal-prior
I(history choice;next count|X,h1)=0.
Class rows differ iff m!=1, so class information and class-given-count information
coincide and are positive then. This is a LOCAL conditional witness;
stationary history-marginalised material occupancy remains neutral.
Immediate JS magnitudes match 8H's algebra, but h1 is now held fixed: depth and
magnitude are distinct coordinates.

## 12. Finite and numerical evidence

CL-F09 records the three-grade exact finite verification: 12 durable items,
three 2304-state kernels, six refinement runs including reverse enumerations,
all exact absorption/stationarity/covariance/conditional certificates.
CL-N09 records 160-digit natural-log information, not rational state counts.
The frozen information gap bound is 1e-25; observed maximum is below 3e-157.
Reference decimal candidates were used only after freeze as checks, never inputs.

<a id="cl-m06"></a>
## 13. Diagnostic discipline

CL-M06: temporal tests should match the declared mechanism/depth/compiler
question. A fixed adjacent lag or three-time CMI can be blind to this H2
controller. This does not mandate arbitrarily deep tests or define a master
memory score. H2 capability does not establish structural utility beyond a
deliberately engineered delayed-copy law.

## 14. Scope and non-claims

Ordinary state, history depth, alphabet, predictive block count, Markov order,
synchronization, information magnitude and refinement iterations stay separate.
No L-positive rule dynamics, H3, N5, geometry, new entity channel, Monte Carlo,
weak-grade sweep, broad graph/count atlas or book edit occurs.
Q-L-COMPILER-SEMANTICS remains open. These model results do not establish
physical memory, irreducible time, event stacks in nature, purpose, repair,
adaptation, design, theology or TCR.

## 15. Validation-only engineering amendment

Post-freeze combined tests exposed an untyped-cache key collision between an
invalid boolean slot and a valid integer slot. Legal scientific states use only
int/None, so the issue was input validation, not the transition law.
Amendment A seals typed probability caches under a separate committed/pushed
plan and version. It explicitly retains prior target exposure; it is not blind.
All twelve scientific result payload hashes and all four summary-table hashes
match v1 EXACTLY. Original plans/results remain immutable and the original
verifier passes at its own result commit. See the amendment and replay receipts
under exploration/generation-008l. No tolerance, controller or claim changes.
