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
