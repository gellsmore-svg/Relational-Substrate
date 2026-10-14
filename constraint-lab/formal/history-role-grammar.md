# Historical role grammar

## Pre-freeze definitions and generic reduction

This section records semantics, symbolic covariance and structural enumeration
before I0 freeze. Actual non-neutral I0 stationary, projection, feedback,
fingerprint and temporal calculations remain unopened at drafting. Post-freeze
proofs and verification links will be appended separately.

The ordinary material state still has six pair/four independent triad bits.
At pair epochs, augmented state is (p,h), p in 0..63 and h in 0..5. A pair
event e sends (p,h) to (p xor 2^e,e). Triad events preserve p and h.
No S, L, geometry, deeper H or new relation channel is introduced.

rho(e,h) is SAME, ADJACENT or DISJOINT by equality/intersection of the two
unordered vertex pairs. Counts per h are (1,4,1), mechanically enumerated.
Direction is FORM on an absent candidate bit and DISSOLVE on a present one.
The eleven declared single-feature predicates use only rho, direction or their
conjunction. Weights are m^phi, phi Boolean, m>0. At the initial sentinel,
history-relation predicates are inactive and current-only predicates still apply.

## Exact pair-event closure

Let W(p,h) be the sum of the six positive pair weights. At fixed p,h each
triad-only event leaves W unchanged, regardless of triad mask. Its total
full-event probability is 4/(W+4)<1. The next-pair slot probability is

```text
sum_{k>=0} [4/(W+4)]^k w_e/(W+4) = w_e/W.
```

Absorption occurs almost surely. The pair event updates only p,h as above, so
the exact next-pair process closes on 384 recurrent augmented states. This does
not assume a triad prior. Direct raw-triad block solves are separately frozen
as post-freeze checks. No dense full 7168-state kernel is required.

## Symbolic S4 covariance

A vertex permutation preserves equality and vertex intersection of pairs, and
preserves whether the relabelled candidate is present in the relabelled mask.
Therefore it preserves every feature value. It permutes the weight vector and
its sum, hence the normalised row and deterministic register/toggle update.
Thus simultaneous vertex relabelling is a kernel automorphism for every m>0.
By CL-T20 its orbits form a valid strongly lumpable quotient. I0 additionally
checks aggregate rows for every one of the 384 states for every primary cell.

## Structural orbit enumeration

Enumerating all 24 vertex permutations partitions 384 states into 28 orbits,
with total size 384. Keeping a remembered edge fixed leaves endpoint swaps and
the swap of the other two vertices. The four adjacent edge bits form a 2x2
binary matrix modulo row/column swaps. Its seven patterns have counts
1,1,3,1,1 at occupancy 0,1,2,3,4. The independent remembered and disjoint bits
give 2*2*7=28 orbits, an independent structural derivation.

The diagnostic tuple (R,A_h,D_h,C_h) has 24 distinct values. Four pairs of
orbits collide when A_h=2,C_h=0: two adjacent bits at one endpoint and two
diagonal bits are different configurations. R and D_h independently give four
such collisions. They remain distinct orbits. The exact enumeration is in
exploration/generation-008i/structural-orbits.json; it is a declared pre-freeze
structural observation, not an I0 non-neutral dynamical result.

## Reading the future atlas

Stationary solves use exact rational 28-orbit balance and exact full lift checks.
Conditional shape information must allow unequal model priors inside each
edge-count block. KU uniformly averages h at each p; Kpi uses stationary h|p.
They are distinct. Reversibility of augmented, quotient and stationary projected
kernels is kept separate. Fingerprints distinguish exact full law, quotient law,
stationary joint, stationary material and one-step projected statistics.

Any post-freeze structural effect is a behavioural observation, not a stronger
capability theorem than CL-T28. Current-only structural effects are not H
discoveries. Finite augmentation still restores first-order Markov form.

## Verified I0/I1 appendix

I0 froze at 035601e215bf6f0c4621d818ffa22b713d0b5d67, then published all 22
cells at 2b001561abba3e21bc6489bcfdca1249b31519aa. Its full reading selected
two complementary I1 probes. I1 froze separately at
2315728e5acd1facb093d7daf09dc0d4cf2a9b47; it reused eight observed I0 inputs,
with zero new stationary solves. Frozen science/source files remain unchanged.
The following are reusable algebraic statements, not 22 controller-specific
theorems. Finite exact palette values and numerical information stay in tables.

<a id="cl-t36"></a>
### CL-T36: generic history/present pair-event closure

For any strictly positive pair weights w_e(p,h) independent of triad state, with
unit triad weights and history preserved during triad events, the geometric
argument above gives q_e=w_e/W. The deterministic next pair update is
(p,h)->(p xor 2^e,e). Therefore the pair-epoch chain closes exactly on (p,h).
The argument allows arbitrary present/history interactions within these
assumptions; it generalises CL-T30. It does not justify a triad quotient when
the controller reads triads or changes h during their events.

<a id="cl-t37"></a>
### CL-T37: S4 role covariance and valid quotient

Each declared predicate preserves rho and direction under simultaneous vertex
permutation. The weight vector, denominator and update commute with that action,
so the whole kernel is covariant for all m>0. For states in one orbit, mapping
destinations by the same permutation preserves every destination orbit and its
total probability. Thus aggregate block rows agree, proving strong lumpability
onto the 28 marked-edge orbits (CL-T20), independently of an initial prior.

The independent stabiliser derivation above gives 28=2*2*7 orbits; the four
descriptor collisions do not merge dynamical states. CL-F06 records exhaustive
structural verification. All I0 block rows and all 24 vertex permutations were
also checked exactly after freeze, not inferred from graph isomorphism alone.

<a id="cl-t38"></a>
### CL-T38: regular history-only stationary uniformity

Let q_h(e) depend only on symmetric regular SAME/ADJACENT/DISJOINT classes,
with positive class weights. Their counts 1,4,1 are the same for every h, so
the normaliser is constant and Q_he=Q_eh. Q is stochastic and symmetric,
hence doubly stochastic. For destination (p',j), predecessors are
(p' xor 2^j,i), i=0..5; incoming column sum is sum_i Q_ij=1.
Uniform pi(p,h)=1/384 is stationary. More generally this last argument only
requires a p-independent doubly stochastic slot matrix.

Strictly positive slot laws allow any toggle sequence, then j,j to retain
the target mask and finish at target history j. This proves irreducibility,
unique stationarity and period two (parity flips; repeating h twice returns).
Thus all A features are stationary-material silent for every m>0, not merely
the two grades. This does not imply first-order material dynamics or extend
to p-dependent cross features.

<a id="cl-t39"></a>
### CL-T39: H_pair=1 order bound and exact first-order criterion

For any law q(p,h) with exactly one pair toggle and h'=e, two consecutive
material masks recover h by their one-hot XOR. Therefore the next pair row
depends on at most two snapshots after an observed pair transition.

With all slot probabilities positive, the augmented support is irreducible as
in CL-T38 and its stationary law is positive. For a fixed current p, every
previous neighbour p xor 2^h occurs with positive stationary probability and
recovers that h. Consequently stationary order one holds iff q(p,h) is
independent of h for every p, equivalently strong lumpability of history
erasure. If any two such rows differ, order is exactly two. This is a
conditional-row criterion, not a consequence of event MI. No finite full-event
snapshot order is asserted.

<a id="cl-t40"></a>
### CL-T40: stationary symmetry and coarse history-label silence

If a finite kernel is S4 covariant and has unique stationary pi, relabelling
pi gives another stationary vector; uniqueness makes it equal to pi.
Marginal pair probabilities are therefore equal on each graph class.
For any S4-invariant g(p), simultaneous relabelling leaves g fixed and acts
transitively on the six history labels. Thus pi(g,h) is the same for every h:
pi(g,h)=pi(g)/6, while pi(h)=1/6.

Hence I(edge count;H)=I(graph class;H)=0, even though I(P;H) may be positive.
This concerns the name of the remembered slot, not all relational information
carried by its role within p. Across two S4-invariant material models, mask
conditioned on graph class is the same uniform orbit law, so
I(model;mask|class)=0 exactly. It does not force class or conditional shape
discrimination across models to vanish.

For numerical conditional information, model priors inside an edge-count block
need not be equal. The direct rational-joint KL implementation allows those
unequal priors; the independently computed information chain checks CL-T16.

<a id="cl-t41"></a>
### CL-T41: uniform versus stationary Markov projections

KU(p,p')=(1/6)sum_h K((p,h),projected p') is a stochastic current-state kernel.
Given stationary pi with positive pi_P, define Kpi using pi(h|p) instead.
Then

```text
sum_p pi_P(p) Kpi(p,p')
 = sum_{p,h} pi(p,h) K((p,h),projected p')
 = pi_P(p').
Kpi(p,p') - KU(p,p')
 = sum_h [pi(h|p)-1/6] K((p,h),projected p').
```

Thus stationary one-step material statistics are representable by Kpi even
when no fixed current-state row matches every conditioned history row.
Correlation between p,h does not by itself imply a KU occupancy discrepancy:
the weighted row difference can vanish, as current-only controls illustrate.
KU is one declared comparator, not a theorem of irreducible history.

<a id="cl-t42"></a>
### CL-T42: last-event bookkeeping and augmented irreversibility

For any positive toggle/register law with at least two slots, take source (p,h)
and event e!=h. Its destination is (p xor 2^e,e). Returning to material p
requires toggling e, but that leaves history e, not h. The reverse augmented
transition has probability zero. Positive stationary source mass makes detailed
balance impossible. For six slots there are 384*5=1920 such one-way arrows.

This holds even for a material H0 process with an observational last-event
register. It does not entail irreversibility of every quotient or of Kpi,
thermodynamics, purposiveness or a history-effect magnitude.

<a id="cl-t43"></a>
### CL-T43: SAME-direction symmetry and exact stationary factorisation

Take d>=2 pair slots with the SAME_FORM law: weight m on e=h only when the
candidate is absent, unit alternatives, update h'=e. Arbitrary simultaneous
permutations of the d bit coordinates, history labels and event labels preserve
the whole law. This dynamical coordinate symmetry is larger than graph vertex
relabelling; it introduces no geometry.

Write R=p_h, k=|p|, r=(m+d-1)/(m+2d-1). The unique stationary joint law is

```text
pi(p,h) = [1/(2d)] r^(k-R) (1-r)^(d-1-k+R).
```

Conditional on h, its bit R is uniform and independent of d-1 iid Bernoulli(r)
other bits. This normalises exactly. To prove balance, destination (p,j) has
predecessors (p xor 2^j,i). Let n1=k-R and n0=d-1-n1.

If R=0, the i=j contribution divided by pi(p,j) is 1/d; other-present
coordinates contribute n1/d; other-absent coordinates contribute
n0*r/[(1-r)(m+d-1)]. Since r/(1-r)=(m+d-1)/d, the sum is
(1+n1+n0)/d=1.

If R=1, the i=j contribution is m/(m+d-1); other-absent coordinates give
n0/(m+d-1); other-present coordinates give n1*(1-r)/(d*r)
=n1/(m+d-1). Their sum is one. Positive support gives unique stationarity;
period two still requires the earlier convergence qualification.

For SAME_DISSOLVE, complementing every bit replaces r by 1-r and leaves
history labels unchanged. Marginal pi_P depends only on k, so every mask in an
edge layer is equally likely: there is no stationary shape difference beyond
edge count. Mean edge count is 1/2+(d-1)r. At d=6, I1 verified both grades
and directions against exact full balance and the independent I0 solve.
Generators produce all 720 coordinate permutations; DISJ has explicit violating
generators. Shape silence does not remove SAME's non-neutral order-two memory.

<a id="cl-t44"></a>
### CL-T44: singleton-selector uniform-average equivalence

Let f be a bijection of history slots, and weight candidate e by m iff
e=f(h) and its current direction is the declared one. The fully normalised
row is exactly q_f(p,h,e)=q_SAME(p,f(h),e), including its p-dependent
denominator. Changing variable h'=f(h) proves

```text
(1/d) sum_h q_f(p,h,e) = (1/d) sum_h' q_SAME(p,h',e).
```

For N=4, the unique disjoint-pair map is a bijection, so SAME and DISJ cross
features have identical KU for every m>0 and either direction. This is a
current-state-average equivalence, not equality of full augmented laws.
Under history relabelling g=f(h), the update is g'=f(e), whereas SAME uses
g'=e. A row bijection alone therefore does not conjugate the full program.
I1's two-grade stationary counterexamples and positive paired conditional
shape information exhibit the distinction. No general classification of all
history functions or all current-state comparators follows.

## Integration boundary

The actual 22-cell stationary observations, reversibility and grade-specific
information remain finite/numerical evidence. Reusable proofs above have explicit
assumptions. They do not promote history to physical ontology, prove irreducible
time, infer purpose/repair/adaptation, or merge OTR with an RS truth claim.
The book integration assessment of 8I science awaits external review.
