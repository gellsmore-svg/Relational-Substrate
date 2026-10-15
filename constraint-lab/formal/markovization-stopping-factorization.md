# Stationary Markovization and Stopping Factorization

Generation 008O. Row distributions and row-stochastic kernels throughout. This
document proves finite-chain algebra. The separate frozen F0 census applies it
to the existing N4 one-role H2 processes; it introduces no transition law.

## Projection And Lifting

Let a finite irreducible chain have state space Z, kernel T and strictly positive
stationary row pi2. A surjection psi:Z->S defines C[z,s]=1{psi(z)=s}.
Set pi1=pi2 C and L[s,z]=1{psi(z)=s} pi2(z)/pi1(s).
Dimensions are T,Pi:|Z|x|Z|; C:|Z|x|S|; L:|S|x|Z|.

Summing a conditional law gives LC=I_S. Consequently Pi=CL is idempotent,
pi2 Pi=pi2, and x Pi replaces a row's within-fibre conditional by the stationary
conditional, preserving its coarse marginal. Pi is an algebraic conditional reset,
not an additional physical event. It is generally not a symmetric matrix.

The stationary-adjacent-matched coarse kernel is K=LTC: its stationary joint
flow is pi1(s)K(s,s')=sum_{z in s,u in s'}pi2(z)T(z,u). Thus pi1 K=pi1.
Also KL=LT Pi. For x=x Pi, one lifted comparator step is x T Pi.
This is stationary Markovization, **not** a strong quotient (CL-T82/CL-T89).

## Stopping Operators

Let A be a nonempty proper stopping set saturated by psi fibres and B its
complement. Projection and lifting respect these blocks. Let Q=T_BB,
P=Pi_B, R=T_BA G, where G is a coarse-measurable return-target readout.
For a source row mu1 on S_A and a declared first-step route subkernel, put
a=mu1 L_A T_AB^d. These are route-joint, not route-conditioned, rows.
If conditional route rows are desired, divide by their common positive route mass.

Define Ar=(I-Q)^-1 and Mr=(I-QP)^-1. Both inverses exist: finite irreducibility
makes the original killed chain transient. Every fine positive path projects to
a positive K path, so K is also irreducible and its killed kernel K_B=L_B Q C_B
is transient. QP=(Q C_B)L_B and K_B=L_B(Q C_B) share their nonzero spectra.
This argument is important: transience of Q alone does not justify an arbitrary reset.

For coarse target G=C_A G1, K_BA G1=L_B R. Expanding the killed series gives
P Mr=C_B(I-K_B)^-1 L_B. Therefore ordinary H1 absorption, starting from a C_B,
is exactly a P Mr R. H2 absorption is a Ar R. A final reset on A does not change
the coarse target readout. Hidden-history-sensitive targets would need a different formula.

## Resolvent Identity

The correctly ordered identity is

```text
Ar - P Mr = Ar (I-P) Mr.
```

Proof: multiply the left-hand difference by I-Q on the left. Using QP Mr=Mr-I,
the result is I-P Mr+QP Mr=(I-P)Mr. Multiply by Ar. The algebra needs the
inverses, but not P's idempotence; idempotence supplies its reset interpretation.

Hence the exact stopping defect is

```text
Delta R_d = a Ar (I-P) Mr R = U V = U W,
U = a Ar(I-P), V = Mr R, W = (I-P)V.
```

The last equality follows from U P=0. This is an iff criterion: the declared
route-source-target passage agrees precisely when this product vanishes.
It is a typed **stopping-Markovization non-commutation defect**, not an
unqualified same-space commutator. Stop the fine chain and read its targets,
versus first stationary-Markovize and then stop the coarse chain, from matched sources.

## Task-Specific Equality

A disjoint primary diagnostic hierarchy, on the complete selected route-side domain:

- U=0: upstream occupation annihilation (N0).
- U!=0 and W=0: target insensitivity (N1).
- U!=0 and W!=0, but UW=0: bilinear orthogonality (N2).
- UW!=0: active control.

An explicit sign-reversing involution may refine N2, but a zero sum alone is not
a symmetry proof. Reachable-support W=0 is weaker than W=0 on the complete
domain. Initial entrance balance aP=a is **not** U=0 after killed propagation.

Strong lumpability of psi suffices for equality of every coarse observed path
and almost-sure stopping functional (from any matched source). The coarse row
is then prior-free; K=LTC is that same row. A single product UW=0 does not imply
strong lumpability or full path equality.

## Length-Resolved Defect

For n>=2 events and j=n-2, the exact coefficient is

```text
Delta F_(d,n) = a [Q^j - P(QP)^j] R
              = a sum_(ell=0)^j Q^ell (I-P)(QP)^(j-ell) R.
```

The finite identity follows by telescoping: adjacent Q^ell(QP)^(j-ell)
terms cancel, leaving Q^j-P(QP)^j. It does not assume matrices commute.

### H2 Stationary Entrance

In this laboratory a successor z'=(P',e,i) determines its predecessor material
mask P' xor 2^e. For a stationary source conditional only on its material class c,
the source-class and route indicators depend only on successor (P',e).
Stationary incoming balance therefore gives
a(z')=pi2(z') 1{predecessor class c, declared route}/pi2(c).
Within each coarse fibre it is proportional to pi2. Thus aP=a, for every positive
fixed controller with this update, not merely the tested grades. This statement
does not extend automatically to history-conditioned or nonstationary starts.

Consequently the two-event residual a(I-P)R vanishes before target aggregation.
Odd returns to an edge-count layer are impossible by single-toggle parity.
The first possible nonzero even coefficient is

```text
Delta F_(d,4) = a Q(I-P)QP R + a Q^2(I-P)R.
```

The omitted initial insertion a(I-P)(QP)^2R is zero. These are exact formulas,
not a theorem that every controller must have an active four-event coefficient.
The latter universal-in-palette observation belongs to 8N's finite census.

## Symmetry And Ranks

Equivariant kernels and stationary laws, invariant sources/routes/stopping sets,
and invariant readouts permit exact restriction to simultaneous-S4 invariant sectors.
Rows there are orbit **masses**; observable columns are invariant values. An orbit
contribution is U_orbit W_orbit,target, not an unweighted representative-state product.
All newly solved equations are also checked on the original 2304/384 sparse states.

Full rank(I-P)=|Z_B|-|S_B|; multiplying on the left by invertible Ar preserves rank.
The analogous invariant-sector ranks use B orbit counts, and need not equal full
ranks. W has invariant columns, so its full column rank equals its sector rank.
Ranks of source-restricted U and UW are separate, exact descriptors, not scores.

For a verified state permutation D transporting models, sources, stopping sets and
targets, T'=D^-1 T D, P'=D^-1 P D, Q'=D_B^-1 Q D_B. Both resolvents conjugate;
a'=a D_B, R'=D_B^-1 R D_target, and Delta'=Delta D_target. Complement transports
FORM/DISSOLVE, k<->6-k, UP<->DOWN. The opposite-pair involution transports
R05/R06, fixes other roles, preserves counts/routes and swaps star/triangle labels.
Transporting a null to another model/task is not an internal cancellation proof.

## Destination Aggregation

Postcomposing a destination-resolved coefficient with the all-ones target column
gives its return-time marginal. A nonzero vector v with v 1=0 is erased by this
projection. For the twenty known 8N four-event timing nulls, F0 separates whether
each insertion already sums to zero or the insertion scalars cancel. Eventual-return
normalization alone does not force a fixed-length timing zero. No symmetry or
conservation attribution follows merely from v 1=0.

## Verification And Scope

### Complete F0 Mechanism Census

All 1008 non-neutral source-route rows are retained: 808 active, 200 null.
There are no N0 propagated-upstream-zero rows. The exact null split is:

| Mechanism | Rows | Exact certificate |
| --- | --- | --- |
| Complete-side target insensitivity N1 | 96 | U!=0, W=0 |
| N2 with disjoint factor support | 80 | U,W!=0; every individual orbit/target product is zero |
| N2 with within-H1-fibre cancellation | 24 | Nonzero individual products; each H1-fibre sum is zero |

UP and DOWN each contain 48/40/12 rows of these three types. No null is left
as an unexplained aggregate signed sum across H1 fibres. The last type is an
exact finite orthogonality certificate, not an all-m role-factorization theorem.
The frozen opposite-pair sign-reversal test explains none of these nulls;
vertex covariance and inter-model conjugacy do not by themselves explain cancellation.

The 80 disjoint-support cases are roles R00,R01,R02,R03,R09: ANY at k2/DOWN
and k4/UP, FORM at k2/DOWN, DISSOLVE at k4/UP, for both grades and both sources.
The 24 fibre cancellations are R04/R11 FORM k3/UP and DISSOLVE k3/DOWN, for
both grades and all three sources. For example the FORM R04 suppressive star
source has five nonzero orbit contributions within one H1 fibre: in a common
vector direction their exact coefficients are proportional to 4,-1,-1,-1,-1.
This is not a two-orbit sign-reversing involution. The complete rational records,
not this descriptive example, are the certificate.

### Extremal Direction-Side Target Insensitivity

The 96 N1 rows have a simple stronger explanation, valid for all positive
formation-only or dissolution-only weights with unit opposite-direction weights.
For FORM k4/UP, B has edge counts five and six. From a five-edge graph any
return to four edges deletes one of its five present edges. All these deletion
weights are equal; four choices give triangle+pendant and one gives C4.
Internal excursions to six edges cannot change this class proportion. Thus the
constant harmonic target column pair (4/5,1/5) satisfies every fine and coarse
killed equation. V is constant and W=0, for arbitrary history-dependent
positive formation weights. Almost-sure return makes that solution unique.
Complement gives DISSOLVE k2/DOWN, target proportions (two-edge path,matching)
=(4/5,1/5). These account for all 96 rows: 24 models times two sources per side.
This post-census analytic corollary requires no new model or diagnostic execution.

All 20 non-neutral four-event timing cancellations are insertionwise target
aggregation zeros, not cancellation between the two potentially surviving
insertion scalars. Their destination vectors are nonzero. A general all-m
identity determining precisely those role/source combinations remains open.

Three independent forms of justification are retained: the matrix proof above,
noncommuting synthetic rational fixtures (plus common neutral), and the full frozen
derived census against hash-pinned 8N route laws. Language-model agreement is not proof.
F0 reuses old harmonic certificates, verifies their killed equations, and solves only
new left-occupation equations by Dixon and independently fraction-free FLINT.

This establishes finite stochastic-process distinctions. It establishes neither
physical memory/time nor purpose, benefit, gravity or a common CL/GT mechanism.
The hub is planning context only; its records are not evidence for these statements.
