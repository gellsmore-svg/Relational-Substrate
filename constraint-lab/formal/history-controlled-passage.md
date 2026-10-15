# History-Controlled Passage

Controlled here means explicitly matched experimental controls, not purpose.
This document uses 8K's compiler-relative state/equivalence framework. Ordinary
X retains six pair and four independent triad bits. At recurrent pair epochs,
triad-blind 8M controllers close on Z=(P,h1,h2). There is no dynamic eta (L=0).

## Matched Sources

Let pi2 be the positive stationary H2 law and pi1(P,h1)=sum_j pi2(P,h1,j).
The stationary-conditional Kpi-H1 law is

```text
Kpi(e|P,i) = sum_j pi2(j|P,i) K2(e|P,i,j).
mu2_c(z) = pi2(z) 1{C(P)=c} / pi2(C=c).
mu1_c(s) = pi1(s) 1{C(P)=c} / pi1(C=c).
```

Summing mu2 over j gives mu1 exactly. Consequently mask, class, count and h1
source marginals agree. For every P,i,e the common stationary flow is
pi1(P,i)Kpi(e|P,i)=sum_j pi2(P,i,j)K2(e|P,i,j). Restriction to C(P)=c and
division by its common mass proves source-conditioned first-step labelled
material equality and hence equal initial UP/DOWN masses (CL-T85). Target
occupancy also agrees. These controls do not imply longer path equality.

## Structural Layers

Use canonical repository classes. The nontrivial N4 layers have two, three,
two graph classes at k=2,3,4. Include every ordered distinct sibling pair:
ten MFPT tasks. For each of three k=3 sources order the other two classes by
canonical representative; the first is competing target A and the second B.
No class is a desired or valued topology.

## Positive First Return

For A={z:K(P)=k}, B its complement, let tau=inf{t>=1:Z_t in A}.
Finite irreducibility implies hitting A almost surely and spectral radius
of Q=T_BB less than one. Single toggles give T_AA=0, so

```text
G = (I-Q)^-1 T_BA
F = T_AB G.
R_k(c,c') = sum_{z:C(z)=c} mu_c(z) sum_{u:C(u)=c'} F(z,u).
```

Only target-class indicator columns of G are needed; this is exactly the
aggregation of the full hidden-state return matrix, not a graph-class
Markov approximation. R_k describes ONE return from the stationary source.
Successive returned classes need not themselves form a first-order chain;
do not iterate R_k to obtain multi-return laws without a sufficiency proof.

## Restricted Invariant Law

Write stationary balance in blocks. Since
pi_B=pi_A T_AB+pi_B Q, one has pi_B=pi_A T_AB(I-Q)^-1.
Substitute in pi_A=pi_A T_AA+pi_B T_BA to obtain pi_A F=pi_A.
Normalise by pi(A). Aggregating source/target classes gives nu_k R_k=nu_k,
where nu_k(c)=pi(C=c|K=k) (CL-T86). This establishes invariant one-return
weights despite a potentially non-Markov class-return sequence. Both compared
models have exactly the same nu_k; a routing residual is not layer occupancy.

## Length And Direction

For n>=2, F_n=T_AB Q^(n-2)T_BA. All odd n vanish: each toggle flips count
parity. Freeze even n=2,4,6,8,10,12 and tail F-F2-...-F12. The tail is an
exact nonnegative mass, not a fitted truncation correction. Restrict T_AB to
first successors of count k+1 or k-1 to obtain UP/DOWN; their sum is F.
Equal initial route masses do not force equal destination contributions.
Total cancellation can conceal route differences; equal totals can conceal
length differences. These are distinct exact classifications.

Stationary material triples of H2 and Kpi agree (CL-T82). Divide their
common joint by Pr(C0=c)>0, then sum triples with K0=K2=k and target class c'.
K1 cannot equal k under single-toggle support. This proves identical F2
pieces (CL-T87), not just equal total two-step return probability. Four
events is the earliest POSSIBLE return distinction, not a universal effect.

## Cross-Class Access

For a target class D solve on the valid hidden-state Markov representation:

```text
m(z)=0 on D;  m(z)=1+sum_u T(z,u)m(u) off D.
MFPT(c->D)=sum_z mu_c(z)m(z), c!=D.
q(z)=1 on A; q(z)=0 on B; q(z)=sum_u T(z,u)q(u) elsewhere.
```

The source average of q is the K3 competing-target probability. Neither a
committor nor an MFPT is inferred by pretending C is first-order. First
return asks the next destination at a repeated density; MFPT asks time to
a particular sibling. They are not interchangeable.

## Kac Control

For a positive recurrent finite stationary chain and nonempty D, start from
pi conditioned on D. The induced return chain has invariant pi|D/pi(D).
In a two-sided stationary path, the return intervals partition time, and
the frequency of visits is pi(D); the mean interval under the induced
stationary return law is therefore 1/pi(D). Equivalently, decompose stationary
occupation into excursions from D and normalise their total expected length.
Thus E[tau_D^+]=1/pi(D) (CL-T88), without requiring D to be a singleton or
the chain to be aperiodic. Computationally use m_D above and average
1+T m_D on D. H2/Kpi same-class means must match; cross-class MFPT need not.

## Matched H1 Exclusion

For positive pi1, a fixed first-order kernel B on exactly S=(P,h1) matching
the full stationary adjacent joint J must obey B(s,s')=J(s,s')/pi1(s).
This is uniquely Kpi. If a passage functional under its stipulated stationary
source differs from H2, no kernel in THAT matched class reproduces both
the adjacent joint and passage (CL-T89). The conclusion does not exclude
H1 models matching occupancy only, arbitrary hidden recodings, enlarged
state, phase, clocks or different semantic history alphabets. This is an
application of CL-M04, not absolute non-Markovianity.

## Passage Transport

If a state bijection g conjugates two kernels and pushes their stationary
laws forward, it maps each path with the same probability and maps hitting
and return stopping times to corresponding sets. Summing finite first-hit
paths (nonnegative convergent series), or applying uniqueness of the finite
Dirichlet solutions, transports return pieces, tails, MFPT and committors
(CL-T90). Kpi commutes with these bijective stationary conditionals.
Complement transports FORM to DISSOLVE and k to 6-k, swapping UP/DOWN.
Opposite-pair involution transports STAR/R05 to TRIANGLE/R06, preserves count
and direction and swaps star/triangle class labels. Reversing competing
target order replaces q by 1-q. Transported-alphabet equality is not equality
of labelled laws, and conjugacy partners are not independent replications.

### Symmetry-Forced Committor Nulls

Complement is a self-conjugacy for every ANY role: it changes neither role
nor a history-only row. It fixes class P4 and exchanges star with triangle.
Its unique stationary source law on P4 is invariant. Path transport therefore
forces the P4-to-star-before-triangle probability to equal its complement:
q=1/2, for both H2 and Kpi, for every positive m. For direction-coupled roles
other than R05/R06, the opposite-pair involution is a self-conjugacy with the
same class exchange, again forcing q=1/2. For R05/R06 it instead transports
between two different controllers; it does not force each individual q to
be one half. These all-m corollaries explain the 64 exact P0 committor nulls;
positivity of the remaining finite-palette residuals is a separate observation.

## Verification And Scope

P0 consumes hash-pinned 8M inputs. Exact solutions on verified S4 quotients
are checked by Dixon and fraction-free routes, then lifted to every full
2304/384-state sparse equation. Rational identities determine zero/nonzero;
160-digit natural logs describe row JS with independent entropy identity.
Finite palette outcomes are separately CL-F11, log magnitudes CL-N11.
No graph-class return process minimality, new history necessity, arbitrary
compiler exclusion, task value, function, repair, agency, physical memory,
emergent boundary or L-positive constraint dynamics follows.
