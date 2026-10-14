# Coarse process memory: mathematical framework

This initial framework contains symbolic derivations predeclared by Prompt 008J,
not pre-freeze A/C word results. Catalogue integration follows exact verification.
All processes and words here use stationary pair-event epochs.

## Material matching

Let pi(p,h) be stationary for an augmented kernel T, and pi_P its marginal.
Define Kpi(p,p')=sum_h pi(h|p) sum_h' T((p,h),(p',h')) where pi_P(p)>0.
Then sum_p pi_P(p)Kpi(p,p')=pi_P(p') by stationary balance. Moreover
Pr_H(P_0=p,P_1=p')=pi_P(p)Kpi(p,p') is exactly the stationary Kpi adjacent
joint. Summation over fibres of any deterministic material observation preserves
one- and two-time equality. Nothing establishes equality at longer lengths.

## Passive-register path equivalence

If the next material row is independent of h, write it Q(p,p'). Conditional on
the entire augmented past the next material law is Q. Iterated conditioning
therefore yields Pr(P_0,...,P_n)=pi_P(P_0) product_t Q(P_t,P_{t+1}).
Kpi=Q on stationary support. A passive deterministic register, including last
pair-slot bookkeeping, does not change this material finite-dimensional law.
This proves all-length equality, not merely a zero triple conditional MI.

## Kpi covariance and graph classes

An invariant stationary joint and a covariant augmented kernel give
Kpi(gp,gp')=Kpi(p,p'). S4 orbit aggregation is representative-independent:
sum_{p' in B}Kpi(gp,p')=sum_{p' in B}Kpi(p,p').
The eleven graph classes are the S4 material orbits, so this projection is
strongly lumpable and first-order for every initial law. Edge count merges
several classes and requires its own block-row test; class covariance alone
does not make edge count Markov.

## Exact observed words

For a stationary row pi, hidden kernel T and deterministic output y,
Pr(y_0,...,y_{L-1})=pi D[y_0] T D[y_1] ... T D[y_{L-1}] 1.
Sparse forward filtering retains positive hidden endpoint masses per reachable
observed prefix. Marginalising those masses gives exact rational words.
A valid role quotient preserves these invariant observed path measures.

## Process information chain

With equal prior on H and Kpi, word JS equals I(M;Y^L). Since E^L=f(C^L),
I(M;C^L)=I(M;E^L)+I(M;C^L|E^L).
Conditional block priors need not be equal. Compute the conditional term
directly from the rational model/class-word/edge-word joint, not by assuming
equal model priors within edge-word fibres. Data processing follows.

## Absolute history-label silence for invariant finite windows

Uniqueness and S4 covariance make the stationary augmented law invariant.
Thus every finite stationary augmented path distribution is invariant under
simultaneous vertex permutation. An invariant material observation word W is
fixed by this action, while the six history labels at any declared time are
transitive. Hence Pr(H_t=h,W=w) has the same value for every h. Summing over h
gives Pr(H_t=h,W=w)=Pr(W=w)/6; for positive W, the conditional label law is
uniform. This holds for every finite stationary window, including past/future
observations. It does not assert independence of a relational role orbit from W.

## Memory statements and limits

Fine historical dependence, hidden-current-state projection memory and H-vs-Kpi
coarse word differences are distinct. Nonzero stationary triple CMI witnesses
failure of order one; zero alone is not an all-past proof. Strong lumpability
does provide an all-initial-laws order-one proof. Finite-depth conditional rows
give witnesses or bounded consistency, not infinite-order conclusions.

The represented (p,h) process is first-order Markov. No irreducible history,
physical memory, observer causation, purpose, design, theology or TCR inference.

## CL-T45: stationary matched one- and two-time laws

The material-matching argument above proves both pi_P Kpi=pi_P and equality of
the adjacent material joint. Deterministic projection is pushforward of these
equal measures, preserving equality for words of lengths one and two. This
does not say the underlying conditioned material rows or longer paths agree.
Exact checks cover all 23 existing systems and both coarse projections.

## CL-T46: passive-register finite-path equivalence

Iterated conditioning in the passive-register argument above proves equality
of every finite material path measure when the material next row is independent
of the register. Deterministic updates of the register need not be reversible.
Any deterministic material output inherits equality. B and neutral instantiate
this theorem; correlation with the recorded register is not a counterexample.

## CL-T47: covariant stationary Markov projection and graph-class quotient

For every g, invariance of pi and covariance of T let us reindex the conditional
history sum, yielding Kpi(gp,gp')=Kpi(p,p'). Summation over an S4 orbit gives a
representative-independent row. Graph-class Kpi is thus exactly first-order for
all initial laws. Every generated Kpi was checked under all 24 permutations,
all 64 sources and all six supported destinations, and every class member was
tested in block aggregation. Edge count is not covered by that orbit argument.

## CL-T48: finite invariant windows hide absolute history labels

The finite stationary path-invariance argument above proves
Pr(H_t=h,W=w)=Pr(W=w)/6 for any finite S4-invariant material word W, with t at
any declared finite relative position. For positive W, Pr(H_t=h|W)=1/6.
Uniqueness is sufficient for invariant stationarity; explicitly invariant
stationarity suffices without uniqueness. A non-invariant initial law or
label-sensitive output is outside scope. Relational role may still be known.

## CL-T49: density-path and shape-sequence information chain

For the rational joint Pr(M,C^L), E^L=f(C^L). The chain rule applied to
(C^L,E^L), whose joint contains no information beyond C^L, gives
I(M;C^L)=I(M;E^L)+I(M;C^L|E^L). Conditional nonnegativity gives data processing.
The implementation evaluates the conditional term directly with the actual
within-edge-word model priors; equal global priors do not imply equal block
priors. Precision/tolerance are numerical validation, not theorem assumptions.

## CL-F07: K4 class-pair reconstruction certificate

At a pair epoch, the previous pair mask is p xor 2^h. Enumerate the 384 marked
states (p,h). The map to (class(p xor 2^h),class(p)) is constant on each S4
role orbit, and its 28 images are distinct. The complete 28-pair certificate is
in reports/items/generation-008j-j1/J1-CLASS-PAIR-ROLE.json; every one of the 384
states was checked, not just representatives. This is a finite exact result.
It is not asserted for N=5, multibit events or larger history.

## CL-T50: graph-class order at most two by role reconstruction

Assume a first-order augmented pair process with h'=e after a single pair-bit
toggle and a valid simultaneous-S4 role quotient. At epoch t after a pair
transition, (C_{t-1},C_t) determines the role orbit by CL-F07. The next-class
law depends only on that orbit, since the role quotient is Markov. Therefore
Pr(C_{t+1}|C_0,...,C_t)=Pr(C_{t+1}|C_{t-1},C_t).
This is an all-past result, not an extrapolation from zero finite-depth CMI.
At stationary pair epochs it applies throughout. Under arbitrary starting
registers it applies after the first actual pair update. In the tested palette,
positive first-order witnesses establish exactly order two for the 18 A/C
systems; passive B and neutral remain first-order.

## CL-T51: SAME edge-count/action-role closure

Let d be the pair-slot count, k the present-bit count and R=p_h. For the SAME
ANY, FORM or DISSOLVE controller, aggregate formation weight is d-k, plus
(m-1)(1-R) if SAME is weighted on formation. Dissolution weight is k, plus
(m-1)R if SAME is weighted on dissolution. Call these F,D. Toggling an absent
bit yields (k+1,1); toggling a present bit yields (k-1,0). Hence (k,R) is a
strongly lumpable 2d-state quotient with rows F/(F+D),D/(F+D).
Because R=1 exactly when the previous count increment was +1, two consecutive
counts determine the role. The count process is order at most two.

For d>=2, strictly positive m and positive stationary support, compare k=1,
R=0 versus R=1. SAME_ANY dissolution probabilities are 1/(m+d-1) versus
m/(m+d-1); SAME_FORM gives 1/(m+d-1) versus 1/d; SAME_DISSOLVE gives 1/d
versus m/(m+d-1). They differ iff m!=1. Both histories have positive mass,
so order one fails for non-neutral m. At m=1 the baseline count chain is
first-order. N=4 checks use d=6, 12 roles and all six SAME cells plus neutral;
N=3 m=2 plumbing was synthetic and pre-freeze.

No ADJ/DISJ closure is inferred: all twelve tested ADJ/DISJ (k,R) block tests
fail. Their edge-count order lower bounds of at least five remain bounded
observations, not a general infinite-order theorem.
