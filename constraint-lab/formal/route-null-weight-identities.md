# Route-Null Weight Identities

Date: 2026-10-15. The parameter m is the positive multiplier of one selected role/direction event weight. Unselected weights are 1. Normalization is 6+(m-1)s, where s is the number of selected candidate events. For example R01 can select four events, so its row denominator is not universally m+5. These proofs vary this single allowed m symbolically, not arbitrary independent event weights.

Sources are stationary conditional graph-class sources, routes are joint UP/DOWN contributions, targets are the complete graph-class vector on the return layer. Statements below do not extend to labelled targets, arbitrary hidden priors, changed directions or arbitrary weights. Neutral m=1 is included as an equality; nonzero factor classifications need not survive neutral degeneration.

## Occupation Identity Used Throughout

Use row convention and the unchanged 8O definitions Q=T_BB, P=Pi_B (a conditional reset, not the material bit mask), U=b_c(I-P), V=(I-QP)^(-1)T_BA G, W=(I-P)V. In full coordinates U_z=b_z-(b_S/pi_S)pi_z. "Invariant" below means S4-invariant, not stationary for a transient killed chain. A killed occupation always comes from the specified return-layer source, with no additional injection at deeper layers.

Write b_c=a_c(I-Q)^(-1). Source first-step balance gives a_c P=a_c. On an entrance-only coarse-fibre-saturated subset E with no killed predecessor, b_c|E=a_c|E, hence U_c|E=0. Also pi_B=sum_c pi(c)b_c for a complete layer's graph classes, from stationary block balance and transience. All arguments are on original fine states; invariant masses are divided by orbit size when checked against orbit certificates.

<a id="disjoint"></a>
## Eighty Disjoint-Support Certificates: All Positive m

It suffices to consider k=2 DOWN for ANY and FORM roles R00,R01,R02,R03,R09. Complement transports ANY to k=4 UP and FORM to DISSOLVE k=4 UP. There are 80 previously observed rows at the two published grades, not 80 independent parameter theorems.

The killed sparse side has counts 0 and 1. Divide count-1 states into E, with h1 absent, and J, with h1 present (h1 is then the sole present edge). E is entrance-only: an internal transition into count 1 is a formation, whose new h1 is present. Thus U_E=0.

At count 0, every successor belongs to J. The lifted Kpi hitting vector on J is constant over the six possible h1 labels because J is one coarse S4 orbit. Consequently V at count 0 is history independent and W_0=0.

For R03 and R09, the only selected candidate is h1. On J it is a dissolution, never an exit formation. The five exit formations have unit weights and graph-class ratio 4 path : 1 matching. On count 0 every next state belongs to J. The constant vector (4/5,1/5) solves both killed hitting equations, so W_J=0. R00 also permits this argument on J.

For R00,R01,R02 an independent regeneration argument covers the equal-history gate. From E, the only internal event dissolves its sole edge f; the former h1=i is absent and differs from f. At the resulting empty state (f,i), history slots differ, so all six formation weights are 1. S4 covariance makes f uniform. The first entry into J therefore has uniform ordered (e,f) distribution over 36 pairs, scaled by a source-dependent scalar. There is no other E-to-J route, and E cannot be revisited. After this common entrance the killed process is fixed, hence each b_c restricted to J is a scalar multiple of one common row. Stationary block balance gives the same conditional row for pi_J. Therefore U_J=0. Together U_E=0, U_J=0 and W_0=0 give pointwise U_z W_z=0.

The proof needs only positive finite m, covariance and the gate/selector identities; it never infers a support zero from two grades. The all-m conclusion is the route-null identity and a disjoint-factor sufficient mechanism, not that every individual U or W support is unchanged with m.

<a id="fibre"></a>
## Twenty-Four Fibre Certificates: All Positive m

Consider FORM R04 (ADJ valence v=4) or R11 (DISJ valence v=1), k=3 UP. DISSOLVE k=3 DOWN is its complement transport. The selected event is h2, provided its relation to h1 is the specified distinct relation. Put D=m+5 and delta=m-1.

The killed domain has counts 4,5,6. At count 4, states with h1 present are entrance-only, so U=0. In a remaining coarse fibre, the two missing slots are i=h1 and j. Only h2=j can activate the selector, so V has just two possible values in that fibre: active j and inactive others.

First W vanishes at counts 5 and 6 for graph-class readouts. Let g6 be the coarse hitting vector at full material, and g_JA,g_JD the two coarse hitting vectors at count 4 with absent h1, classified by relation of its two missing slots. At count 5 with h1 equal to its missing slot, formation cannot activate a distinct-relation selector, so all weights are 1. Its five dissolution successors consist of four ADJ and one DISJ missing-slot pairs. Stationarity of the harmonic equations gives
g6=(4 g_JA+g_JD)/5.
At any count-5 fine state, dissolution weights are all 1 and the only potentially biased formation leads to g6. Its continuation therefore equals g6 regardless of history. At count 6 all successors have the same value. Thus W_5=W_6=0.

It remains to show U=0 on the single active coordinate of each count-4 absent-h1 fibre. For the S4-invariant killed occupation b_c from a specified source class let x be its total count-6 mass, and y its mass on one fixed count-4 coarse fibre (missing i,j; h1=i). This y is the same for every ordered distinct (i,j): inflow is dissolution of present i from count 5 missing j, and every dissolution has the same probability within that row, independently of i. The common probability is 1/6 or 1/D, not universally 1/6. All such states have no other killed predecessor. Covariance alone would not equate ADJ and DISJ fibre masses.

The active fine coordinate h2=j arises by two successive dissolutions from count 6, so its mass is x/36. Let beta be the mass of one active count-5 state (missing i, h1=j present, h2=i, with relation(i,j) selected). Inflow comes from forming j in the preceding count-4 fibre:
beta=y/6 + 5 delta x/(216 D).

For a fixed count-5 material mask let f be its total occupation. There are v active history states, each of mass beta; all other states have unit-weight rows. Flux to one count-4 coarse fibre and flux to count 6 give
y=f/6+v beta(1/D-1/6),
x/6=f/6+v beta(m/D-1/6).
Subtract and substitute:
x/6-y=v beta delta/D,
x/y=36D[6D+v delta]/[36D^2-5v delta^2].

The denominator has coefficients (36-5v)m^2+(360+10v)m+(900-5v), strictly positive for m>0 and v in {1,4}; the numerator is positive too. The stationary restriction obeys the same equations. Hence x/y=pi6/pi_S, so b_active=(b_S/pi_S)pi_active and U_active=0. Since sum of U over each fibre is zero and W has only two levels there, the fibre product sum is zero.

This proves the entire target vector null for all positive m and all three stationary source classes. Their signed algebraic span follows by linearity of the homogeneous flux equations, without division by y for a signed combination that might have y=0. Such signed rows are not additional physical priors. It is not an opposite-pair sign reversal. The observed five-orbit 4:-1:-1:-1:-1 numerical proportion is an exact finite certificate; the proof needs only two-level readout and active-coordinate centering and does not claim that proportion is a universal new representation law.

## Benchmark and Unresolved Boundary

The 96 outer-side target-insensitive rows already have the all-positive-m unit-opposite-direction exit-ratio proof (CL-T95); 8P uses it as a benchmark, not a new theorem. Together these arguments cover the locations of all 200 8O route nulls, but do not prove the absence of additional nulls at other m, nor classify active rows away from the two published grades.

Q-H2-ROLE-FACTORIZATION remains broader: general stationary shape/feedback factorization and arbitrary role combinations are not solved. No new actual parameter point was run.
