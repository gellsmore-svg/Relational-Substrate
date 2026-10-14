# Strong predictive refinement: theory

This is a general finite-process synthesis, not a new laboratory round.
[Taxonomy](state-taxonomy.md) fixes symbols; [counterexamples](predictive-state-counterexamples.md)
separate notions that cannot be identified. Existing CL-T52 supplies the core
existence theorem. New results below are standard finite-chain mathematics
integrated with explicit laboratory scope, not claims of mathematical discovery.

## 1. Process and observation partitions

Let (Z,T) be a finite homogeneous Markov kernel. Add mu only for prior-dependent
statements. For deterministic phi:Z->Y let Pi_Y be its nonempty fibres.
Write Pi <= Gamma to mean Pi REFINES Gamma (Pi is finer).
Different maps with the same fibres define the same partition up to output
renaming, provided their observation meaning is transported.

For block B set T(z,B)=sum_(u in B) T(z,u).
A partition Pi is strongly lumpable iff T(z,B) is independent of z within each
source block, for every target block B. Its quotient is
bar-T(A,B)=T(z,B), z in A.

## 2. What strong lumpability guarantees

With rho(z) the block map, the quotient B_t=rho(Z_t) is a homogeneous first-order
Markov chain with bar-T for EVERY initial mu. Equal block sums remove the hidden
conditional distribution inside each block from the next-block law.
Conversely, requiring one common quotient row for every starting state in a
block forces those sums to agree, by taking point-mass initial laws.

This prior-free requirement is stronger than Markovity for a single prior.
A raw observation can be Markov under some mu despite non-lumpability, and can
fail even at stationary mu. Do not infer either from its one-step conditional
matrix alone.

## 3. Coarsest strong refinement (CL-T52 retained)

Define Ref_T(Pi_Y)=widehat-Pi_Y as the coarsest strongly lumpable refinement of
Pi_Y on this FIXED state space. The qualifier is indispensable.

Start at Pi_0=Pi_Y. Split each current block by exact signatures
(T(z,B):B in Pi_n). Every proper split raises block count, so at most
|Z|-|Pi_0| proper iterations occur. The stable partition is strongly lumpable.
For any eligible strong refinement Q, induction gives Q <= Pi_n: each current
block is a union of Q blocks, and Q-mates agree on sums into those unions.
Consequently Q <= widehat-Pi_Y. This universal property proves coarseness and
uniqueness, not just the inability to merge a pair of final blocks.

The Fraction implementation in refinement.py is reused unchanged. The theorem
does not require rational transition entries; exact rational arithmetic is the
implementation standard for the existing laboratory kernels and proof fixtures.

<a id="cl-t60"></a>
## 4. CL-T60: Observation-coarsening monotonicity

Suppose Y2=f(Y1), so Pi_1 <= Pi_2. Ref_T(Pi_1) is itself a strongly lumpable
refinement of Pi_2. By the universal property of Ref_T(Pi_2),

    Ref_T(Pi_1) <= Ref_T(Pi_2).

The direction is FINER to COARSER. In particular
|Ref_T(Pi_1)| >= |Ref_T(Pi_2)|. No stationarity, positivity, irreducibility or
aperiodicity is needed. This is about partitions of one fixed chain, not about
the state count of arbitrary differently encoded hidden models.

The operator is also idempotent, Ref_T(Ref_T(Pi))=Ref_T(Pi), and
Ref_T(Pi)<=Pi. Treat the family of observation partitions and its image as
predictive-refinement POSETS. The selected family is not assumed closed under
lattice meet/join; no stronger lattice terminology is needed here.

Conditional mutual information is a different, distribution-dependent object.
Coarsening its conditioning variable changes the comparison, so CL-T60 is not
a conditional-MI monotonicity theorem.

<a id="cl-t61"></a>
## 5. CL-T61: Induced quotient maps and commutation

Let A<=B be strongly lumpable partitions of the SAME (Z,T). Map each fine block
a to its containing coarse block b=f(a). If c is a coarse target, then for z in a,

    sum_(a' subset c) bar-T_A(a,a')
      = sum_(u in c) T(z,u)
      = bar-T_B(b,c).

The last expression depends only on b, not which a it contains. Thus the
quotient on A strongly lumps through f, giving exactly the direct B kernel.
This proves direct-versus-staged kernel commutation by block sums. Stationary
pushforward agreement is a consequence if a stationary law is supplied, not
a substitute for the kernel proof.

For indicator matrix D_rho(z,b)=1{rho(z)=b}, the exact kernel square is
T D_rho = D_rho bar-T. These are stochastic-kernel arrows, not a claim that
the transition itself is a deterministic state map or a causal intervention.
The [generated diagrams](predictive-quotient-square.mmd) contrast this valid
square with a raw observation whose bottom Markov arrow need not exist.

## 6. Projection dependence and the 8I instance

widehat-Pi_Y depends on (Z,T), the observation partition and the STRONG
equivalence requirement; it is not an intrinsic function of the process alone.
For deterministic observation coarsening, CL-T60/61 produce a nested quotient
ladder automatically.

The 8I non-neutral ladder 384->28->12->2 and neutral 64->11->7->2 are a
verified instance (CL-T53..T59, CL-F08), not inputs to these general proofs.
The structural meaning identity->role->direction->none is specific to
N4 RECENT-REVERSAL at pair epochs. No additional count/CMI solve is run in 8K.

<a id="cl-t62"></a>
## 7. CL-T62: Strong-block equality implies trace equality, strictly

Define trace/future-word equivalence from KNOWN states z,z' by equal current
phi and equal probability for every finite future observed word.
For empty word put v_empty(z)=1; recursively,

    v_(a w)(z)=sum_u T(z,u) 1{phi(u)=a} v_w(u).

If a strong partition refines Pi_Y and v_w is constant on its blocks, then
1{phi=a}v_w is also block-constant. Equal block sums imply v_(a w) is constant.
Induction proves all observed future words agree within each strong block.

The converse fails in the seven-state counterexample CE-TRACE: two known states
have exactly the same all-order words but different branching mixtures into
three structurally distinct successor blocks. Its proof covers ALL lengths;
a few finite-word checks are not substituted for that proof.

Consequently the strong refinement need not equal the coarsest trace-equivalence
partition, and trace equivalence need not itself be strongly lumpable.
In 8I they coincide on the declared state set because distinct same-observation
stable blocks already have different immediate observed rows (CL-F08).
That special fact must not be generalised.

## 8. Prior-dependent notions and stationary Markovisation

A belief b over Z predicts future word w by sum_z b(z)v_w(z). Two beliefs
supported inside the same current-observation fibre may have identical future
predictions even though their hidden configurations or supports differ.
Specify b, mu and filtering conventions; this is not a strong partition claim.

For this synthesis, weak lumpability means that the projected process is a
homogeneous first-order Markov chain under one DECLARED initial law mu.
Stationary weak lumpability adds mu T=mu. It requires every compatible observed
past to give the same next row at fixed current observation. One-step matching
under stationary averaging does NOT satisfy that condition by itself.
The positive four-state CE-WEAK is stationary weakly but not strongly lumpable.
8H/8I's non-neutral mask/class/count processes are NOT stationary weakly
lumpable: their positive conditional information/order-two witnesses rule it out.

<a id="cl-t67"></a>
### CL-T67: Stationary one/two-time Markov representation

For any stationary finite (Z,T,mu) and deterministic Y, define

    pi_Y(y)=sum_(phi(z)=y) mu(z),
    Q_mu(y,y') =
      sum_(phi(z)=y,phi(u)=y') mu(z) T(z,u) / pi_Y(y)

on positive-mass y. Rows outside stationary support can be chosen arbitrarily;
they do not determine a unique representation there.
The numerator is exactly Pr(Y_t=y,Y_(t+1)=y'), so the stationary Q_mu chain
matches the one-time and adjacent two-time observed laws. Summing the numerator
over y proves pi_Y Q_mu=pi_Y. This requires no weak or strong lumpability.

Longer words need not agree: canonical non-neutral RECENT-REVERSAL and its
neutral one-step representation have identical adjacent mask/class/count laws
but different triples (CL-T31, CL-T55/T56, CL-N08). Thus the implication to
full process equality is false. This re-establishes the general algebra underlying
the divergent 8J Kpi matching result without importing its scientific tables.
