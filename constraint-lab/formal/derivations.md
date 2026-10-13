# Derivations and scope

All results in this document concern the literal, fixed-current-state model with positive multipliers unless stated otherwise. They are not proofs about the RS ontology or physical reality. The canonical catalogue states assumptions and historical evidence separately.

<a id="cl-t01"></a>
<a id="cl-t02"></a>
## CL-T01 and CL-T02: composition and order

The kernel loops over matching rules and multiplies each factor into the baseline slot weight. Thus
\(w_e=b_e\prod_i m_i^{\phi_i}\) and \(\ell_e=\log b_e+\sum_i(\log m_i)\phi_i\).
Finite products commute, as do the sums. Exact rational evaluation is order independent. Floating-point summation can have roundoff-order differences.

Canonicalisation sorts rule representations and minimises their joint vertex images; it does not make multiplication idempotent. Duplicate backend occurrences contribute repeatedly. The structurally simple census normal form excludes repeated structural identity. Alphabet labels and factor values must be included when interpreting syntax.

<a id="cl-t03"></a>
## CL-T03: the six-slot law

With six pair slots, one admissible slot has weight m and the other five have weight 1. Conditioning the next full event to be a pair event gives
\(q_m(e_*)=m/(m+5)\) and \(q_m(e)=1/(m+5)\) otherwise. Inactive m=1 gives 1/6 each. This is not the next-pair epoch resolvent: hidden events may occur before that epoch.

<a id="cl-t04"></a>
## CL-T04: complementary gate elimination

For a binary gate g, exactly one of g and 1-g is active. Two same-action, same-direction rules at multiplier m give \(m^g m^{1-g}=m\) whenever the action is admissible. When inadmissible, both rules fail their direction guard. All event weights agree with an unconditional rule of that direction, hence full kernels agree as well.

<a id="cl-t05"></a>
## CL-T05: direction elimination

Equal factors on form(e_*)|g and dissolve(e_*)|g give weight \(m^g\) for the slot irrespective of its current bit. Exactly one direction is admissible. Dependence on g remains, and normalised probabilities remain coupled to the denominator. This does not eliminate the event's form/dissolve interpretation.

<a id="cl-t06"></a>
## CL-T06: one-literal additive bound

Fix one admissible action direction and two raw gate bits. Every one-literal rule contributes either \(\lambda g_i\) or \(\lambda(1-g_i)\); unconditional rules contribute constants. Summing gives
\(\ell=c+a g_1+b g_2\), so \(\Delta_{12}\ell=0\). This is a bound on log weights in a fixed feature family, not on normalised probabilities, full-state action guards, count predicates, or higher-K conjunctions.

<a id="cl-t07"></a>
<a id="cl-t08"></a>
## CL-T07 and CL-T08: conjunction degree

Let U_i=g_i for a present literal and U_i=1-g_i for an absent literal. A rule on r distinct gates contributes \(\lambda\prod_i U_i\) on its admissible action. The coefficient of \(\prod_i g_i\) is
\(\lambda(-1)^{n_{\mathrm{absent}}}\), which is nonzero when m!=1. In literal coordinates its top discrete derivative is \(\lambda\).

For r=2, \(\ell_{11}-\ell_{10}-\ell_{01}+\ell_{00}=\log m\) in literal coordinates. The raw-bit sign is positive for zero or two absent literals and negative for one.

Distinct gates guarantee each full corner assignment is possible in the independent hypergraph. Contradictory literals on the same gate have zero feature. Repetition can reduce degree (g*g=g). The parser rejects identical repeats but accepts present(g)&absent(g). Neutral factors and cancellation among rules can also remove top interaction. The theorem concerns one non-neutral, satisfiable rule, not syntactic condition count alone.

<a id="cl-t09"></a>
## CL-T09: Boolean/Mobius basis

For a table f on \(\{0,1\}^r\), write 1_B for the corner with precisely B active. Set
\[
\theta_B=\sum_{C\subseteq B}(-1)^{|B|-|C|}f(1_C).
\]
Then \(f(g)=\sum_{B\subseteq[r]}\theta_B\prod_{i\in B}g_i\).
At corner 1_D, exchanging subset sums leaves f(1_D): the inner alternating sum vanishes unless C=D. The triangular corner-to-coefficient transform has diagonal 1, proving uniqueness. The empty product is 1.

<a id="cl-t10"></a>
<a id="cl-t11"></a>
## CL-T10 and CL-T11: corner basis and one-action expressivity

Corner indicators \(\chi_u(g)=\prod_i[g_i=u_i]\) are mutually exclusive and sum to 1. Thus \(f=\sum_u f(u)\chi_u\). Expanding the absent literals gives the Mobius transformation; evaluation on corners gives its inverse.

For any strictly positive desired action-weight table w(u), assign multiplier w(u)/b to the complete corner rule u. Exactly one rule matches on an admissible action. This requires up to \(2^r\) rules with K=r+1 and arbitrary positive factors, not a finite-grade theorem. It applies to one fixed action and leaves other event weights unchanged.

<a id="cl-t12"></a>
## CL-T12: full current-state event-weight expressivity, with restrictions

There are D relation bits. For every event slot e and full state x, create one rule:
- form(e) if x_e=0, otherwise dissolve(e);
- condition on the complete assignment of the other D-1 relation bits;
- assign multiplier w_e(x)/b_e, where the baseline b_e is positive and constant for that slot.

For a given (x,e), exactly its one corner rule matches. No condition mentions the action bit; direction encodes it. Structural identities are distinct. This constructs any positive event-weight table with K<=D and J<=D*2^D, omitting neutral factors if desired.

The O=2/O=3 literal parser admits the needed non-action conditions, both directions and all supported slot types. Custom positive factor names are accepted by the parser/backend. This proves representational completeness for positive kernels with the existing single-toggle hypercube support, including any desired positive q on that support by choosing w=q.

It does NOT prove arbitrary Markov-kernel universality, support changes, self-loops, multibit events, historical dependence, or unrestricted expressivity of the standard experiment runner. That runner fixes finite named alphabets and J in {1,2,3}. Rational tables are implemented exactly by Fraction; arbitrary real factors describe an ideal positive-real semantics, and irrational implementation is approximate.

<a id="cl-t13"></a>
<a id="cl-t14"></a>
## CL-T13 and CL-T14: cardinality and the count-predicate boundary

A sum of features from a vector space stays in that space. Increasing J at fixed primitive feature family cannot introduce a monomial outside its span, although normalisation can introduce probability-level interactions.

The K-1 degree bound is false for the full token grammar. At O=2,N=3, fix an admissible form action bit to 0 and let the other two pair bits be g1,g2. The K=2 predicate count>=1 has feature
\(g_1\lor g_2=g_1+g_2-g_1g_2\), of degree 2. Count tokens can read many raw bits. This explicit algebraic counterexample qualifies the scope of the literal hierarchy without rewriting historical findings.

<a id="cl-t15"></a>
## CL-T15: pair-event epoch clock

Write the full-event transition matrix P=T+B, separating hidden-only transitions T and pair transitions B. If a pair event is eventually reached with probability 1 and rho(T)<1, then
\[
E=\sum_{j\ge0}T^jB=(I-T)^{-1}B.
\]
This is the next-pair-arrival kernel on full states. The immediate pair-conditioned local law only renormalises slot probabilities at the current state and does not include hidden excursions.

For a full-event stationary row vector pi, pi B=pi(I-T). Hence the normalised pair-arrival distribution rho=pi B/(pi B 1) obeys rho E=rho. This arrival distribution is not generally pi and is not the pre-pair-event context weighting used for event CMI.

With positive factors on a finite state space, the probability of a pair event has a positive minimum, giving geometric absorption and rho(T)<1. Hard prohibitions can invalidate this assumption.

<a id="cl-t16"></a>
## CL-T16: deterministic projection information chain

Let X be a labelled pair mask, Y its graph class and Z its edge count. Because Z is a function of Y and Y a function of X, the chain rule gives
\[
I(M;X)=I(M;Z)+I(M;Y\mid Z)+I(M;X\mid Y).
\]
Also \(I(M;Y)=I(M;Z)+I(M;Y\mid Z)\). No Markov assumption or fitted model is needed. For a binary equal-prior law label, each marginal information is an equal-prior Jensen-Shannon divergence. Conditional remainders are nonnegative in exact arithmetic; roundoff near zero is not a negative scientific finding.

<a id="cl-t17"></a>
## CL-T17: parity and period

Each pair epoch toggles exactly one pair bit, so edge-count parity alternates. All returns take even numbers of epochs. With positive single-toggle support the epoch chain is irreducible, and a pair toggle followed by its reverse has positive probability, providing a two-step return. Its period is exactly 2.

A unique stationary vector exists, but a fixed-parity source cannot converge at every epoch to that full vector. Under these positive-support assumptions E^2 is irreducible and aperiodic within each parity class; the limits are stationary vectors conditioned on parity. Bipartiteness alone, without the two-step-return and irreducibility assumptions, does not prove period exactly 2.

<a id="cl-t18"></a>
## CL-T18: stationary factorisation for autonomous single-action laws

Assume x=(b,z,y), with b a distinguished pair bit, p-1 other pair bits z and h hidden bits y. The action rate w(b,y)>0 ignores z; every other pair bit has symmetric unit flip rate; hidden bits have unit flip rates. The finite independent-bit support is complete.

Use the auxiliary continuous-time generator whose off-diagonal rates are the unnormalised event weights. This is a mathematical lift, not an additional physical clock or ontology axis. Its embedded jump chain is precisely P. The generator splits into the (b,y) core and independent symmetric z flips. Its stationary distribution is
\(\mu(b,z,y)=\sigma(b,y)/2^{p-1}\), where sigma is the unique stationary core distribution.

Let Z(b,y)=w(b,y)+p-1+h be the full row total. The embedded-chain stationary vector is proportional to mu*Z, so it still factorises in z. Applying CL-T15, the pair-arrival mass is proportional to
\[
[\sigma(1-b,y)w(1-b,y)+(p-1)\sigma(b,y)]/2^{p-1}.
\]
It too has a uniform z factor. Marginalising y gives
\[
\rho_{\rm pair}(b,z)=
\begin{cases}a/2^{p-1}&b=1\\(1-a)/2^{p-1}&b=0.\end{cases}
\]
This proves the factorisation for the whole declared 8F single-action family, including continuous comparators, not merely the tested grades. One action may have different form and dissolve rates provided both depend only on (b,y).

**Required narrowing:** 'only one pair bit has state-dependent rates' alone is insufficient if that rate reads z. For an explicit counterexample, let form(b) have rate 1 at z0=0 and 3 at z0=1, dissolve(b) and all other rates 1. The two-bit continuous-time core has stationary weights (3,4,2,5)/14 in order (b,z0)=(0,0),(1,0),(0,1),(1,1), as direct balance equations verify. Embedding p=6,h=4, full-event core occupancy is (30,40,24,50)/144. Pair-arrival core occupancy is (18,24,16,30)/88: z0 has marginals 21/44 and 23/44, not uniform. This is a symbolic balance construction, not a new kernel search.

<a id="cl-t19"></a>
## CL-T19: shape-given-edge invariance

Under CL-T18 let an unlabelled graph class have k edges and n_Y labelled masks. Vertex permutations act transitively on pair slots. Double-counting occupied slots over the orbit shows each slot is present in fraction k/p of its masks. Thus
\[
P(Y)=\frac{n_Y}{2^{p-1}}\left[a\frac{k}{p}+(1-a)(1-\frac{k}{p})\right].
\]
The same expression with n_Y replaced by binomial(p,k) gives P(k). Therefore \(P(Y\mid k)=n_Y/\binom pk\), independently of a. Two laws in this family have zero stationary shape-given-edge model information, even with nonzero edge and labelled information.

This structural result is not uniquely N=4. Merely increasing N or replacing AND by XOR within the same autonomous single-action family cannot defeat it. Pair-coupled/multiple-action laws lie outside the proof.

<a id="cl-t20"></a>
## CL-T20: valid symmetry quotient

For a state partition, a Markov quotient independent of within-block initial weighting exists under strong lumpability: for any x,x' in the same block, sums of P to each destination block agree. Kernel-automorphism orbits satisfy this condition by permuting destination blocks. A visible graph quotient that ignores fixed labelled constraints may fail it, as repaired in 8A.

Simultaneously relabelling rules and states is covariance. It does not make every vertex permutation an automorphism of one fixed labelled rule collection.

<a id="cl-t21"></a>
## CL-T21: selected minimal representations

Consider one fixed admissible action direction, at most two distinct binary non-action gates, positive factors, no counts or extra state, and the structurally simple literal grammar. The vector records minimum J and minimum maximum-K separately; these examples attain both minima jointly.

| Desired multiplier table | Continuous vector [J,K] | W4 vector [J,K] |
| --- | --- | --- |
| Unit baseline | [0,0] (empty-collection convention) | [0,0] |
| Constant m!=1 in W4 | [1,1] | [1,1] |
| One-gate switch (1,m), m in W4 | [1,2] | [1,2] |
| Complementary levels m0,m1 distinct and both non-unit in W4 | [2,2] | [2,2] |
| AND-selected m in W4 | [1,3] | [1,3] |
| XOR-selected m in W4 | [2,3] | [2,3] |
| XNOR-selected m in W4 | [2,3] | [2,3] |
| Constant 8 (one gate available) | [1,1] | [3,2] |
| Constant 3 | [1,1] | Impossible in W4 |

For constants, a nonzero law needs at least one rule. A nonconstant single-gate law needs K>=2. Two distinct non-unit complementary levels cannot be produced by one conjunction rule (which leaves multiplier 1 somewhere). AND is one two-literal feature and has nonzero second difference, so K>=3. XOR/XNOR have nonzero second difference and support on two opposite corners, not a single conjunction support, so K>=3 and J>=2; two corner rules attain these bounds.

For constant 8, W4 log-base-2 coefficients are +/-1 or +/-2. Two rules cannot give constant exponent 3: at each corner both would have to be positive and active, hence both unconditional with the same structural identity, forbidden here. One unconditional 4 and complementary gate rules of weight 2 attain [3,2]. If stacked-weight normal form is allowed, two unconditional rules of weights 4 and 2 attain [2,1]. Repeated identical occurrences are another backend representation, not a structurally simple set.

These lower bounds are proofs, not an exhaustive representation census. Different target parameters or allowing counts, extra gates, alternate slot normalisation or other weighted actions changes the problem.

<a id="cl-t22"></a>
## CL-T22: finite alphabet limitations

Any finite W4 product is \(2^n\) for integer n, so a non-dyadic multiplier such as 3 is unreachable regardless of J. In the structurally simple r-gate literal family there are 3^r distinct condition identities (each gate absent, present or unused). At one corner only 2^r identities match, bounding the absolute log-base-2 exponent by 2*2^r. This is a finite representation family, unlike the arbitrary-real Boolean basis theorem.

Allowing unbounded stacked multiplicity reaches arbitrary integer corner exponents by complete corner rules, but still not all positive real tables. The historical 625/625/279 basis coverage result is a narrower finite exhaustive domain, not all W4 representations.

<a id="cl-t23"></a>
## CL-T23: orthogonal projection

For target \(\ell=cU_1U_2\), the projection onto span{1,U1,U2} under uniform corners is
\(-c/4+(c/2)U_1+(c/2)U_2\).
Subtracting yields \(c(U_1-1/2)(U_2-1/2)\). Its mean and centred first moments vanish by independent uniform bits. This is a log-weight projection, not a probability or stationary-weight projection.

<a id="cl-t24"></a>
## CL-T24: drift root uniqueness

Let p(w)=w/(w+5). The function F(r)=2p(r)+p(r^2) is continuous and strictly increasing for r>0, with limits 0 and 3. The target 2p(1)+p(m) lies strictly between 1/3 and 4/3 for m>0. A unique positive root therefore exists and depends continuously on m. At m=1 it is r=1. Matching this gate-average probability matches balanced local edge drift for a fixed direction, not experienced gate weighting or global occupancy.

<a id="cl-t25"></a>
## CL-T25: hidden-coordinate conjugacy

For the independent unit-bit baseline and a one-action law depending on two selected hidden bits, any permutation carrying the selected hidden coordinates (and their literal signs) to another such pair while fixing all pair labels maps every event weight and successor to its counterpart. Complementing a hidden bit additionally swaps its present/absent literal while leaving its symmetric flip unchanged.

This proves full-kernel and epoch conjugacy. Uniform hidden priors are invariant, and the pair projection is fixed, so the entire projected pair process agrees for mapped laws and common source masks. The historical 48-law verification establishes that the tested BOTH/ONE/NEITHER systems lie in this family. It is not a theorem for arbitrary incidence-coupled rules.
