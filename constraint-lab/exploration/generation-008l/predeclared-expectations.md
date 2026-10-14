# H2-0 externally predeclared analytic expectations

Written before any new N4 non-neutral H2 target execution. These are symbolic
derivations of Prompt 008L's candidates, not results or theorem catalogue entries.
The numerical reference values in the prompt are review checks, not inputs.

## Covariance and clocks

A vertex permutation induces a bijection g on pair slots. e=h2 iff g(e)=g(h2).
Simultaneously mapping pair mask, h1, h2 and candidate pair therefore preserves
weights and shift update. Unit triad weights transform trivially. No edge label
is privileged. Each full step toggles one ordinary bit.

Before h2 exists, the full row is 1/10. Later total weight is m+9, pair total
m+5 and triad total four. Triad excursions preserve all pair coordinates and
history; their geometric sum gives (w_e/(m+9))/(1-4/(m+9))=w_e/(m+5).
The sentinel case gives (1/10)/(1-4/10)=1/6. Full versus pair probabilities
and clocks are not interchangeable.

## Common-start witness and compiler

Let a=01,b=12,c=23. A=a,b,c and B=b,a,c from empty X and (null,null)
end at the same path, zero triads and h1=c, but h2=b/a. At each first two full
steps h2 is unavailable; c differs from the stored first slot at step three.
Candidate path probabilities: 1/[100(m+9)] full, 1/[36(m+5)] pair.
The last two material masks agree; the third-back slice differs.

At this identical (X,h1), the row at a/b is exchanged between weight m and one.
For m!=1 no fixed first-order strict-H1 kernel can give both rows, independent
of positive K/J. The contract preserves X, h1 meaning, support, clock and
observation, and excludes extra hidden coordinates/time/seed/recoding.
The product state (X,h1,h2) is closed and Markov. One arbitrary 36-valued
coordinate could encode it under a broader compiler, not semantic H_pair=1.

For two exchanged weighted coordinates, their JS mixture has coordinate mass
(m+1)/(2D); all other contributions vanish. Hence candidate JS is
[m ln(2m/(m+1))+ln(2/(m+1))]/D, with D=m+5 or m+9.
Mechanical graph classification, not naming alone, must produce the supplied
middle-edge/end-edge shape rows. Both histories have dissolution weight m+2,
formation weight three; edge-count information must be exactly zero.

## Recurrent pair process and stationarity

Index state (p,i,j) by (p*6+i)*6+j. Pair e maps it to (p xor 2^e,e,i),
with q_j(e)=(m if e=j else 1)/(m+5).
For destination (p',e,i), predecessors are (p' xor 2^e,i,j) over all six j.
Sum_j q_j(e)=1. Thus the candidate joint law is uniform 1/2304 by column
balance; the 36-history marginal is also uniform by the same sum. Pair/history
independence follows from the JOINT factorisation, not uniform marginals alone.

All weights are positive. To reach target (p',i',j'), toggle a prefix whose XOR
is p xor p' xor 2^j' xor 2^i', then append j',i'. This reaches every state
from every recurrent state; the same final-two construction reaches every
recurrent state from the sentinel start. Uniform stationarity is unique.
Parity flipping excludes odd returns. At any diagonal history (i,i), toggling
i twice returns to the SAME augmented state with positive probability.
Irreducibility then implies common period two. Non-diagonal history need not
itself admit a two-step return. Stationarity does not imply pointwise convergence
from a fixed parity start.

Averaging uniform h2 gives stationary next slot 1/6. Material occupancy,
edge-count and graph-class occupancy therefore match the neutral baseline.

## Predictive separation and generic refinement

For fixed p, different j yield distinct immediate labelled rows for m!=1.
For the same j but i!=i', choose any common next event e. Its probability is
positive and identical. Successors have second-history slots i/i'; a following
event f=i has different probability. The observed two-step WORD determines e,
so cancellation cannot hide the distinction. Thus all 36 histories are
future-distinct at fixed p. Strong blocks imply equal words (CL-T62), excluding
all such merges; singleton refinement is sufficient.

The generic algorithm is expected to first split by (p,h2), then by (p,h1,h2):
64->384->2304. Neutral stays 64. Neither count nor partition memberships are
algorithm inputs. The CL-T52 universal property gives coarseness; pairwise
merge obstructions are auditable additional certificates, not its sole proof.
Two strict splitting rounds need not equal history depth in general.

## Lag-selective temporal predictions

At pair epochs h1=E_t, h2=E_(t-1); future E_(t+1) reads only E_(t-1).
The stationary law of h1,h2 is independent uniform. Consequently
Pr(E_t=i,E_(t+1)=e)=1/36 EXACTLY, but
Pr(E_(t-1)=j,E_(t+1)=e)=q_j(e)/6.
Candidate lag-two repetition is m/(m+5), with MI
ln(6)+a ln(a)+5b ln(b), a=m/(m+5), b=1/(m+5).
The slot process is order at most two; same current slot and distinct supported
previous slots exclude order one when m!=1. Neutral slots are iid uniform.

Under stationary two-slot uniform initialisation, finite slot path probabilities
factor as (1/36) times the product of lag-two q factors. Separating even and odd
indices yields two independent stationary six-slot first-order chains.
This is a symbolic explanatory decomposition, not a new decay atlas.

## Material order and conditional information

Given three consecutive masks (p2,p1,p), recover h1 from p1 xor p and h2 from
p2 xor p1. This proves all-past order at most three at pair epochs.
The A/B witness gives identical last two masks and different next rows with
positive probability, excluding order two under the stationary law as well.

From current uniform state, preceding masks are p xor 2^h1 and then
p xor 2^h1 xor 2^h2. Enumerate the next step with mass q_h2(e)/2304.
Summing h2 gives each compatible (previous,current,next) triple mass 1/2304.
Thus the stationary triple law equals H0 and
I(P_prev;P_next|P_current)=0 by exact conditional independence.

For the four-mask joint, conditioning on (P_prev,P_current) fixes h1 while
h2 remains uniform. P_prevprev identifies h2, next mask identifies e. Therefore
I(P_prevprev;P_next|P_prev,P_current) equals the lag-two event MI.
A separate three-forward-step stationary word enumeration must agree exactly.
Neutral output is first-order; non-neutral labelled pair output is expected
order exactly three. No full-event material Markov-order claim follows.

## Status and stopping rule

All preceding assertions are predeclared symbolic expectations until H2-0 runs.
Non-neutral counts, rows, kernels, witness outputs, information values and
order verifications remain unopened until committed/pushed freeze.
Unexpected witness, refinement or null-test results are retained and diagnosed,
not repaired by switching labels, rounding away dependence or forcing counts.
