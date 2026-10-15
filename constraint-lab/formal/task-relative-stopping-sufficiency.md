# Task-Relative Stopping Sufficiency

Date: 2026-10-15. General finite-chain algebra, with a separately scoped CL application. This is a finite linear-systems criterion, not a claim of new general mathematics.

## Examples Before Definitions

A process may have exactly the same eventual 50:50 destination split as its conditional-reset comparator, but a different distribution of waiting lengths. A different process can have the same geometric return-time law at every length while its internal coarse paths differ. Finally, two nonzero destination changes can sum to zero when the task records only whether return occurred.

The exact synthetic fixtures in stopping_sufficiency.py demonstrate these three distinctions. They are not CL scientific cells. All priors called stationary are solved and checked by both FLINT and independent Fraction Gauss-Jordan elimination.

<a id="criterion"></a>
## Finite Stationary Construction

Let T be an n-by-n finite irreducible row-stochastic matrix with positive stationary row pi2. A surjective map psi to s coarse states has deterministic matrix C (n-by-s). Put pi1=pi2 C and L[u,z]=pi2[z]/pi1[u] on its fibre, zero otherwise (s-by-n). Direct fibre summation proves LC=I, Pi=CL is idempotent and pi2 Pi=pi2. Then Kpi=LTC and pi1[u]Kpi[u,v] is exactly the stationary coarse adjacent flow. Kpi L=LT Pi; this is stationary conditional reset, not strong lumpability.

A and its complement B must be fibre saturated. The comparator killed kernel is L_B Q C_B. Its lifted continuation is QP with P=C_B L_B. Coarse irreducibility follows because every fine positive path induces a coarse positive path. Both fine and coarse killed chains hit a nonempty stopping set almost surely; finite irreducibility bounds the survival probability geometrically over a sufficiently long block. Thus both are transient. QP and L_B Q C_B have the same nonzero spectrum (rectangular product identity), so the lifted killed inverse exists too. This inference would not hold for an arbitrary unrelated reset without checking transience.

For target map G on A that is coarse measurable, R=T_BA G; incoming a on B is compared with aP. The original killed continuation is aQ^jR, and the lifted comparator is aP(QP)^jR. A stationary class/route entrance in CL additionally satisfies aP=a, but this is not required for the general algebra below.

## Typed Task and All-Length Criterion

Use row distributions. On a finite killed domain B of size b, Q is b-by-b; P is an idempotent b-by-b conditional reset. The CL construction additionally makes Q and QP nonnegative transient substochastic matrices. M is r-by-b, with rows spanning a declared finite family of entrance/route rows; R is b-by-q and gives declared exit readouts, including the exit subkernel. Physical source rows are nonnegative, normalized or route-joint subprobabilities. Signed linear combinations below are algebraic tests, not extra physical priors.

For j>=0 define D_j=M[Q^j-P(QP)^j]R. The event length is j+2 in the CL first-return convention. Put

```text
H = diag(Q, QP)           (2b x 2b)
E = [M, -MP]              (r x 2b)
F = [R; R]                (2b x q)
D_j = E H^j F.            (r x q)
```

Let K be the row span of E, EH, EH^2, ... . Let O be the column span of F, HF, H^2F, ... . K is right-H invariant and O is left-H invariant. Then the following are equivalent:

- all D_j vanish;
- every row of K annihilates F;
- E annihilates every column of O;
- K and O are orthogonal under ordinary row-column pairing.

Proof: each condition says E H^j F=0 for every j; multiplying the generators on the appropriate side proves invariance and both implications. If the row span through power t does not grow when power t+1 is added, it is closed under H, so an exact finite basis decides equality. This is a necessity-and-sufficiency criterion, not merely a sufficient dimension count.

Cayley-Hamilton gives the safe bound: testing j=0,...,2b-1 suffices. A smaller bound is the degree of an annihilating polynomial for H on its reachable restriction (or its reachable/observable realization). The minimal polynomial need not have degree 2b; the generic bound is not claimed sharp. In a fixed task, equality at fewer arbitrary horizons is not an all-length certificate unless a proved recurrence or closure supplies the missing implication.

For a source subspace, use its basis as M. For a readout family, concatenate its columns as R. Taking linear spans loses no equality tests while P,Q and the source convention stay fixed. Changing the prior used to define P is a different task, not a linear combination in this theorem. Requiring equality for every nonnegative unit entrance is equivalent to testing all coordinate rows; restricted stationary-class entrances generally span a smaller space.

<a id="eventual"></a>
## Eventual and Finite Horizons

If Q and QP are transient, summing the absolutely convergent series yields

```text
sum_j D_j
 = M[(I-Q)^(-1)-P(I-QP)^(-1)]R
 = M(I-Q)^(-1)(I-P)(I-QP)^(-1)R.
```

Thus all-length equality implies eventual equality. The converse fails because different lengths can cancel. A single eventual equality also need not persist under disaggregating target columns, changing sources, conditioning on route, or observing an intermediate state.

These statements concern killed terminal/length observations. Even equality for every such length does not imply equality of all coarse path words or strong lumpability. An intermediate observation inserts additional diagonal readout operators between transitions; those are not included in the displayed realization. Strong lumpability is a sufficient all-source, all-coarse-path condition, not a conclusion from this restricted task criterion.

## CL Specialization and Scope

Use the unchanged 8O C,L,Pi and stationary sources. A and B must be unions of coarse fibres; Q=T_BB and P=Pi_B. R=T_BA G. Route d supplies a_d, not its conditional normalization unless explicitly declared. M can contain the seven stationary source-class/route rows on each relevant layer. An invariant-sector reduction is valid for invariant sources and terminal readouts only; it does not certify labelled intermediate observations or full-state ranks.

No 8P all-length census on the actual CL atlas is performed. The generic criterion is supplied as a formal interface. Existing 8O data remain finite certificates unless supplemented by the separate all-weight proofs.
