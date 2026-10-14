# Formal statement catalogue

Generated from theorem-catalog.jsonl. Historical layers are not rewritten.

## CL-T01: Multiplicative weights and additive event log weights

**ALGEBRAIC_THEOREM**

Matching fixed rules multiply event weights; their logarithms add.

Assumptions: Positive baseline and multipliers; H=L=0; fixed rule occurrences.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t01). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py), [kernel.py](../../constraint-lab/src/rs_constraint_lab/kernel.py)
Coherence: `F8D-LOG-ADDITIVITY`, `F8D-ADDITIVE-FEATURE-GRAMMAR`, `F8G-FORMAL-ADDITIVE-LOGIT-GRAMMAR`
Dependencies: none
Source generations: 008D, 008G
Boundary: Zero prohibit is outside logarithmic algebra.
Notes: Zero prohibit is outside logarithmic algebra.

## CL-T02: Rule-order commutativity, not idempotence

**ALGEBRAIC_THEOREM**

Rule permutations preserve exact weights and kernels; duplicate occurrences still multiply repeatedly.

Assumptions: Exact arithmetic; Same factor map and rule multiset.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t02). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py), [grammar.py](../../constraint-lab/src/rs_constraint_lab/grammar.py)
Coherence: `F8D-LOG-ADDITIVITY`, `F8G-FORMAL-ADDITIVE-LOGIT-GRAMMAR`
Dependencies: CL-T01
Source generations: 008D, 008G
Boundary: Structurally simple census sets forbid repeated structural identity; backend multisets do not deduplicate.
Notes: Structurally simple census sets forbid repeated structural identity; backend multisets do not deduplicate.

## CL-T03: Six pair-slot normalised law

**ALGEBRAIC_THEOREM**

One weighted admissible pair slot has q(action)=m/(m+5), all alternatives 1/(m+5).

Assumptions: Six pair slots; Other five weights 1; Immediate pair-event conditioning.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t03). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8C-CLOSED-FORM-CMI`, `F8C-TWO-COORDINATES`
Dependencies: CL-T01
Source generations: 008C, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T04: Complementary equal-gate elimination

**ALGEBRAIC_THEOREM**

Equal same-direction factors on G and NOT G equal an unconditional factor, including the full kernel.

Assumptions: Binary complementary gate; Equal positive multipliers; Same action and direction.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t04). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8D-COMPLEMENTARY-ELIMINATION`, `F009-TWO-LEVEL-COLLAPSE`
Dependencies: CL-T01
Source generations: 007B, 008D, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T05: Equal-direction elimination

**ALGEBRAIC_THEOREM**

Equal form and dissolve factors on the same gate remove action-bit dependence of slot weight but retain gate dependence.

Assumptions: One action slot; Same positive multiplier and gate in both directions.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t05). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8D-DIRECTION-ELIMINATION`
Dependencies: CL-T01
Source generations: 008D, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T06: K2 literal additive-gate bound

**ALGEBRAIC_THEOREM**

Same-action one-literal rules give c+aG1+bG2 and zero second discrete log-weight derivative.

Assumptions: Fixed admissible direction; Pure literal fragment; One-action gauge.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t06). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8D-NO-GATE-PRODUCT`, `F8D-ADDITIVE-FEATURE-GRAMMAR`, `F8G-FORMAL-K-INTERACTION-HIERARCHY`
Dependencies: CL-T01
Source generations: 008D, 008E, 008G
Boundary: Not a bound for count predicates, probabilities or arbitrary higher-K rules.
Notes: Not a bound for count predicates, probabilities or arbitrary higher-K rules.

## CL-T07: K3 conjunction and polarity sign

**ALGEBRAIC_THEOREM**

A non-neutral two-distinct-literal rule has literal second derivative ln(m); raw-bit coefficient changes sign with each absent literal.

Assumptions: Two distinct satisfiable gate variables; Admissible action; m>0 and m!=1; Non-action gates span their full cube under fixed action admissibility.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t07). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-K3-CONJUNCTION-INTERACTION`, `F8E-K2-K3-NONREPRESENTABILITY`, `F8G-FORMAL-K-INTERACTION-HIERARCHY`
Dependencies: CL-T01
Source generations: 008E, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T08: Scoped general conjunction degree

**ALGEBRAIC_THEOREM**

A non-neutral rule over r distinct jointly satisfiable literals has nonzero degree-r raw-gate coefficient ln(m)*(-1)^number_absent.

Assumptions: Distinct gate variables; Joint satisfiability; Positive non-neutral factor; Admissible action; Non-action gates span their full cube under fixed action admissibility.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t08). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-GENERAL-K-INTERACTION`, `F8F-GENERAL-K-SCOPE`, `F8E-CARDINALITY-VS-K`, `F8G-FORMAL-K-INTERACTION-HIERARCHY`
Dependencies: CL-T01
Source generations: 008E, 008F, 008G
Boundary: Contradiction, repeated variable, neutral multiplier or cross-rule cancellation defeats naive syntactic degree claims.
Notes: Contradiction, repeated variable, neutral multiplier or cross-rule cancellation defeats naive syntactic degree claims.

## CL-T09: Unique Boolean Mobius expansion

**ALGEBRAIC_THEOREM**

Every real function on r Boolean gates has unique multilinear coefficients given by alternating subset sums.

Assumptions: Finite Boolean cube; Real-valued table.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t09). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-BOOLEAN-LOGIT-BASIS`, `F8G-FORMAL-BOOLEAN-BASIS`
Dependencies: none
Source generations: 008E, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T10: Corner-indicator basis

**ALGEBRAIC_THEOREM**

Complete literal corners are mutually exclusive basis vectors, transformed to monomials by expanding absent literals.

Assumptions: r distinct Boolean gates; All cube corners available.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t10). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-CORNER-BASIS`, `F8E-BOOLEAN-LOGIT-BASIS`, `F8G-FORMAL-BOOLEAN-BASIS`
Dependencies: CL-T09
Source generations: 008E, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T11: Continuous one-action weight expressivity

**ALGEBRAIC_THEOREM**

Arbitrary positive corner multipliers construct any positive action-weight table with at most 2^r rules and K=r+1.

Assumptions: One fixed action and admissible direction; Arbitrary positive factors; Unbounded rule budget; Literal parser permits all selected non-action gates.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t11). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-BOOLEAN-LOGIT-BASIS`, `F8E-CORNER-BASIS`, `F8G-FORMAL-BOOLEAN-BASIS`
Dependencies: CL-T10
Source generations: 008E, 008G
Boundary: Continuous algebraic completeness is not W4 coverage or arbitrary full-kernel universality.
Notes: Continuous algebraic completeness is not W4 coverage or arbitrary full-kernel universality.

## CL-T12: Restricted full current-state expressivity

**ALGEBRAIC_THEOREM**

The unbounded literal parser/backend constructs every positive event-weight table on its finite single-toggle support using K<=D and J<=D*2^D.

Assumptions: O=2 or O=3 independent relation bits; Both event directions and all non-action literals; Positive slot baselines; Custom positive factor map; No experiment-runner J/W bound.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t12). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py), [constraints.py](../../constraint-lab/src/rs_constraint_lab/constraints.py), [spec.py](../../constraint-lab/src/rs_constraint_lab/spec.py)
Coherence: `F8D-ADDITIVE-FEATURE-GRAMMAR`, `F8E-BOOLEAN-LOGIT-BASIS`, `Q-H-POSITIVE`, `Q-META-CONSTRAINT`, `F8G-FORMAL-CURRENT-STATE-EXPRESSIVITY`, `F8G-FORMAL-COMPILATION-TEST`
Dependencies: CL-T10, CL-T11
Source generations: 008G
Boundary: Not arbitrary support, self-loop, multibit, history or standard finite-alphabet experiment expressivity.
Notes: Not arbitrary support, self-loop, multibit, history or standard finite-alphabet experiment expressivity.

## CL-T13: Rule cardinality preserves a fixed feature span

**ALGEBRAIC_THEOREM**

Adding more terms from a fixed feature family cannot create an absent log-weight monomial.

Assumptions: Fixed multiplicative current-state grammar; Fixed primitive feature family and gauge.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t13). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-CARDINALITY-VS-K`, `F8D-GATE-DIMENSION`, `F8G-FORMAL-RULE-CARDINALITY-DISTINCTION`
Dependencies: CL-T01, CL-T09
Source generations: 008D, 008E, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T14: Count-token counterexample to a blanket K bound

**ALGEBRAIC_THEOREM**

At O=2,N=3 on a form-admissible action, one K2 count>=1 token equals G1+G2-G1G2 and has interaction order 2.

Assumptions: Two remaining pair bits; Action bit fixed absent; O=2 count semantics.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t14). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py), [constraints.py](../../constraint-lab/src/rs_constraint_lab/constraints.py)
Coherence: `F8E-CARDINALITY-VS-K`, `F8F-GENERAL-K-SCOPE`, `F8G-FORMAL-COUNT-SCOPE`
Dependencies: CL-T09
Source generations: 008G
Boundary: The K-1 degree hierarchy applies to pure literal conjunctions, not the entire count-token DSL.
Notes: The K-1 degree hierarchy applies to pure literal conjunctions, not the entire count-token DSL.

## CL-T15: Next-pair resolvent and stationary arrival weighting

**ALGEBRAIC_THEOREM**

If P=T+B and rho(T)<1, E=(I-T)^-1 B; full-event stationary pi induces epoch stationary rho proportional to pi B.

Assumptions: Finite kernel; T hidden-only and B pair-event transitions; Almost-sure pair arrival and rho(T)<1.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t15). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F003-CLOCK-SPLIT`, `F8C-CHECKPOINT-EPOCH`, `F8F-COMPLEMENT-PERIOD`, `F8G-FORMAL-STATIONARY-FACTORISATION`
Dependencies: none
Source generations: 003C, 008C, 008F, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T16: Nested projection information chain

**ALGEBRAIC_THEOREM**

I(M;mask)=I(M;edges)+I(M;class|edges)+I(M;mask|class) for deterministic nested projections.

Assumptions: Class is a function of mask; Edge count is a function of class; Well-defined finite joint distribution.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t16). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-INTERACTION-ROUTING`, `F8C-PROJECTION-GEOMETRY`
Dependencies: none
Source generations: 008C, 008F, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T17: Pair-epoch parity and period two

**ALGEBRAIC_THEOREM**

One-bit pair epochs flip parity; irreducibility and positive two-step reverse moves imply period exactly two.

Assumptions: Positive finite single-toggle support; At least one pair slot; Next-pair absorption.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t17). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-COMPLEMENT-PERIOD`
Dependencies: CL-T15
Source generations: 008F, 008G
Boundary: Bipartiteness alone only implies even return lengths, not period exactly two.
Notes: Bipartiteness alone only implies even return lengths, not period exactly two.

## CL-T18: Autonomous single-action stationary factorisation

**ALGEBRAIC_THEOREM**

One action depending only on its bit and hidden bits yields action occupancy times uniform other pair bits under both full and pair-arrival stationary clocks.

Assumptions: Action weight w(b,y)>0 independent of other pairs z; Other pair and hidden flip rates symmetric unit; Complete independent-bit support.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t18). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-SHAPE-WASHES-OUT`, `F8F-INTERACTION-ROUTING`, `F8G-FORMAL-STATIONARY-FACTORISATION`
Dependencies: CL-T15
Source generations: 008F, 008G
Boundary: Explicit other-pair-conditioned action counterexample in derivations; does not cover multiple coupled actions.
Notes: Explicit other-pair-conditioned action counterexample in derivations; does not cover multiple coupled actions.

## CL-T19: Stationary shape-given-edge invariance

**ALGEBRAIC_THEOREM**

In the factorised family, graph-class conditional probabilities at fixed edge count are orbit sizes divided by binomial(p,k), independent of action occupancy.

Assumptions: CL-T18 hypotheses; Vertex group transitive on pair slots; Declared unlabelled graph classes.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t19). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-SHAPE-WASHES-OUT`, `F8F-INTERACTION-ROUTING`, `Q-SCALE-N`, `F8G-FORMAL-SHAPE-INVARIANCE`
Dependencies: CL-T18
Source generations: 008F, 008G
Boundary: Scales beyond N=4 within the same family; N alone or XOR alone cannot defeat this theorem.
Notes: Scales beyond N=4 within the same family; N alone or XOR alone cannot defeat this theorem.

## CL-T20: Strong-lumpability symmetry criterion

**ALGEBRAIC_THEOREM**

Kernel-automorphism orbits are strongly lumpable; visible isomorphism alone does not justify quotienting a fixed labelled law.

Assumptions: Entire transition law preserved; State partition and clock declared.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t20). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F011-QUOTIENT-INVALID`, `F8F-INCIDENCE-SILENT`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`
Dependencies: none
Source generations: 008A, 008F, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T21: Selected two-gate minimal representation vectors

**ALGEBRAIC_THEOREM**

Analytic lower bounds and constructions give baseline, scalar, switch, two-level, AND, XOR and XNOR [min J,min max-K], with separate W4 exceptions.

Assumptions: One admissible action; At most two raw gates; Structurally simple positive literal grammar; Specified target factors and no extra weighted actions.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t21). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-CARDINALITY-VS-K`, `F8E-XOR-XNOR-FROM-K3`, `F8G-FORMAL-RULE-CARDINALITY-DISTINCTION`
Dependencies: CL-T06, CL-T07, CL-T10
Source generations: 008E, 008G
Boundary: No representation census: selected cases proved algebraically; see continuous/W4 and stacked distinctions.
Notes: No representation census: selected cases proved algebraically; see continuous/W4 and stacked distinctions.

## CL-T22: W4 arithmetic boundary

**ALGEBRAIC_THEOREM**

Every finite positive W4 product is an integer power of two; arbitrary real tables are unreachable even with unbounded multiplicity.

Assumptions: W4 soft multipliers only; Positive weights; Unit baseline.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t22). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8E-W4-COVERAGE`, `F8G-FORMAL-BOOLEAN-BASIS`
Dependencies: CL-T01, CL-T10
Source generations: 008E, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T23: Centered lower-order projection

**ALGEBRAIC_THEOREM**

The uniform-corner projection of cU1U2 is -c/4+(c/2)U1+(c/2)U2; the residual has zero mean and first moments.

Assumptions: Uniform independent gate corners; Log-weight inner product.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t23). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-PROJECTION-PERSISTS`
Dependencies: CL-T09
Source generations: 008F, 008G
Boundary: Outside the stated feature, support, positivity and clock assumptions; no physical universality claim.

## CL-T24: Unique positive balanced-drift root

**ALGEBRAIC_THEOREM**

2p(r)+p(r^2)=2p(1)+p(m) has a unique positive root, continuous through r=1 at m=1.

Assumptions: p(w)=w/(w+5); m>0; Uniform balanced gates.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t24). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-DRIFT-MATCHED-RESIDUAL`
Dependencies: CL-T03
Source generations: 008F, 008G
Boundary: One balanced moment is not stationary or dynamically experienced weighting.
Notes: One balanced moment is not stationary or dynamically experienced weighting.

## CL-T25: Independent hidden-bit conjugacy

**ALGEBRAIC_THEOREM**

Selected hidden-bit permutations and literal-complement maps fixing pair labels conjugate the autonomous baseline laws and their pair projections under uniform hidden priors.

Assumptions: Independent symmetric hidden flips; Mapped feature coordinates and polarities; Mapped priors; Pair labels fixed.
Scope: Declared finite fixed-current-state DSL; see assumptions, not an ontology theorem.

Proof: [derivations.md](../../constraint-lab/formal/derivations.md#cl-t25). Constructive derivation or exact identity in the linked proof section; implementation fixtures in test_formal.py.
Evidence: [derivations.md](../../constraint-lab/formal/derivations.md), [test_formal.py](../../constraint-lab/tests/test_formal.py)
Coherence: `F8F-INCIDENCE-SILENT`, `F8G-FORMAL-INCIDENCE-SCOPE`
Dependencies: CL-T01, CL-T15
Source generations: 008F, 008G
Boundary: Does not preserve arbitrary incidence-coupled laws.
Notes: Does not preserve arbitrary incidence-coupled laws.

## CL-F01: Two-K2 exhaustive local atlas

**FINITE_EXHAUSTIVE_RESULT**

3,584 weighted two-rule systems split into effective gate dimensions 0:16, 1:960, 2:2608.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Generation 8D two-K2 T-to-P W4 labelled systems

Enumeration: Generation 8D two-K2 T-to-P W4 labelled systems; exact count 3584. Verifier: [explore08d.py](../../constraint-lab/src/rs_constraint_lab/explore08d.py)
Evidence: [generation-008d-weighted-systems.json](../../constraint-lab/reports/tables/generation-008d-weighted-systems.json), [generation-008d-two-gate-composition-atlas.md](../../constraint-lab/reports/generation-008d-two-gate-composition-atlas.md)
Coherence: `F8D-GATE-DIMENSION`, `F8D-INFORMATION-NOT-DIMENSION`
Dependencies: none
Source generations: 008D
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-F02: K3 census and K2 nonmatches

**FINITE_EXHAUSTIVE_RESULT**

288 labelled rules, 20 S4 orbits and 80 W4 systems have nonzero conjunction interaction; none matches the 3,584 two-K2 local laws.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Generation 8E N4 pair actions with two distinct triad conditions, W4; comparison to 8D

Enumeration: Generation 8E N4 pair actions with two distinct triad conditions, W4; comparison to 8D; exact count 80. Verifier: [explore08e.py](../../constraint-lab/src/rs_constraint_lab/explore08e.py)
Evidence: [generation-008e-comparison-8d.json](../../constraint-lab/reports/tables/generation-008e-comparison-8d.json), [generation-008e-interaction.json](../../constraint-lab/reports/tables/generation-008e-interaction.json)
Coherence: `F8E-K3-CONJUNCTION-INTERACTION`, `F8E-K2-K3-NONREPRESENTABILITY`
Dependencies: CL-T06, CL-T07
Source generations: 008D, 008E
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-F03: Restricted W4 basis coverage

**FINITE_EXHAUSTIVE_RESULT**

The two predeclared four-feature W4-or-neutral coefficient grids each yield 625 tables with intersection 279.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 8E monomial and corner bases with each of four coefficients from five declared levels

Enumeration: 8E monomial and corner bases with each of four coefficients from five declared levels; exact count 625. Verifier: [explore08e.py](../../constraint-lab/src/rs_constraint_lab/explore08e.py)
Evidence: [generation-008e-basis.json](../../constraint-lab/reports/tables/generation-008e-basis.json)
Coherence: `F8E-W4-COVERAGE`
Dependencies: CL-T09, CL-T10
Source generations: 008E
Boundary: No claim beyond the declared support, parameter palette, clock and observable.
Notes: Not a census of all W4 structural identities or arbitrary rule cardinality.

## CL-F04: Incidence motif law conjugacy verification

**FINITE_EXHAUSTIVE_RESULT**

All 48 labelled F0 laws reduce to 16 cached canonical laws by hidden-bit permutations fixing pair labels; B/O/N are projected-dynamically identical in that family.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 8F 12 targets times K3/ENDPOINT/PROJECTION/DRIFT

Enumeration: 8F 12 targets times K3/ENDPOINT/PROJECTION/DRIFT; exact count 48. Verifier: [explore08f.py](../../constraint-lab/src/rs_constraint_lab/explore08f.py)
Evidence: [generation-008f-law-equivalence.json](../../constraint-lab/reports/tables/generation-008f-law-equivalence.json), [generation-008f-polarity-conjugacy.json](../../constraint-lab/reports/tables/generation-008f-polarity-conjugacy.json)
Coherence: `F8F-INCIDENCE-SILENT`, `F8G-FORMAL-INCIDENCE-SCOPE`
Dependencies: CL-T25
Source generations: 008F
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-N01: Apparent memory depends on clock

**NUMERICAL_KERNEL_RESULT**

8B initial information decay and 3C full-versus-pair clock separation are finite-model results, not universal forgetting theorems.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 3C N3 and 8B fixed N4 palette at committed horizons

Method: Deterministic finite-kernel propagation and declared projections
Domain: 3C N3 and 8B fixed N4 palette at committed horizons
Tolerances: `{"information_floor_8b": 1e-10}`
Method caveat: 3C threshold details remain in its own report; no shared retrospective floor is imposed.
Evidence: [generation-003c-memory-clock-refinement.md](../../constraint-lab/reports/generation-003c-memory-clock-refinement.md), [generation-008b-information-calibration.md](../../constraint-lab/reports/generation-008b-information-calibration.md)
Coherence: `F003-CLOCK-SPLIT`, `F015-TRANSIENT-CLASS-MEMORY`, `F018-LOCAL-VERSUS-INITIAL`
Dependencies: CL-T15
Source generations: 003C, 008B
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-N02: Controlled passage and composition

**NUMERICAL_KERNEL_RESULT**

Controlled passage effects remain after occupancy matching in 4a; 5 shows observable composition is not a sum of single-rule effects.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 4a 160 kernels and 5 predeclared matched pairs

Method: Committed deterministic finite-kernel passage and control calculations
Domain: 4a 160 kernels and 5 predeclared matched pairs
Tolerances: `{"effect_floor": 1e-08, "gen005_iterative_committor_tolerance": 1e-12}`
Evidence: [generation-004a-reconfiguration-sensitivity.md](../../constraint-lab/reports/generation-004a-reconfiguration-sensitivity.md), [generation-005-targeted-tp-pp-pairs.md](../../constraint-lab/reports/generation-005-targeted-tp-pp-pairs.md)
Coherence: `F004-PASSAGE-AFTER-OCCUPANCY`, `F005-COMPOSITION-NOT-SUM`, `F008-COMPOSITION-REPRESENTATION`
Dependencies: CL-T01
Source generations: 004A, 005
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-N03: 7B aggregate control collapse

**NUMERICAL_KERNEL_RESULT**

42/42 logical aggregate fit problems meet 1e-8; all 52 stored solutions lie on equal complementary coefficients, without full process equivalence being implied by fitting.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 7B 42 predeclared logical problems, 52 stored fits

Method: Deterministic bounded aggregate control fitting
Domain: 7B 42 predeclared logical problems, 52 stored fits
Tolerances: `{"joint_fit_tolerance": 1e-08}`
Evidence: [generation-007b-two-level-pair-face-control.md](../../constraint-lab/reports/generation-007b-two-level-pair-face-control.md)
Coherence: `F009-TWO-LEVEL-COLLAPSE`, `F006-SCALAR-AGGREGATE`, `F007-SELECTIVITY-SURVIVES`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`
Dependencies: CL-T04
Source generations: 007B
Boundary: No claim beyond the declared support, parameter palette, clock and observable.
Notes: The equal-coefficient local collapse is algebraic; the fitted diagonal outcome is numerical.

## CL-N04: Information estimator calibration

**NUMERICAL_KERNEL_RESULT**

8B plugin information exceeds exact finite-state reference under the tested balanced finite samples; symmetry-aware raw-state reference repairs the interpretation.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 8B 336 estimator cells on the frozen palette

Method: Exact-reference finite-kernel calculations plus historical Monte Carlo calibration, not new sampling
Domain: 8B 336 estimator cells on the frozen palette
Tolerances: `{"reported_reference_reproduction_gap": 2.81e-16}`
Evidence: [generation-008b-information-calibration.md](../../constraint-lab/reports/generation-008b-information-calibration.md)
Coherence: `F013-PLUGIN-OVERSTATES`, `F011-QUOTIENT-INVALID`
Dependencies: CL-T20
Source generations: 008A, 008B
Boundary: No claim beyond the declared support, parameter palette, clock and observable.
Notes: Includes historical sampling; not every output is an algebraic identity.

## CL-N05: Persistent tiny projection residual

**NUMERICAL_KERNEL_RESULT**

K3-versus-PROJECTION stationary pair JS is 2.811226056e-5 at m=1/4 and 6.210311362e-6 at m=4; both exceed the 1e-12 information floor.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 8F frozen single-action N4 strong-grade palette

Method: 80-digit multiplier references and float64 deterministic epoch/stationary analysis
Domain: 8F frozen single-action N4 strong-grade palette
Tolerances: `{"information_floor": 1e-12, "local_reference_gap": 1e-13, "stationary_residual": 1e-11}`
Evidence: [generation-008f-stationary-bridge.json](../../constraint-lab/reports/tables/generation-008f-stationary-bridge.json), [generation-008f-numeric-validation.json](../../constraint-lab/reports/tables/generation-008f-numeric-validation.json), [generation-008f-stationary-context.json](../../constraint-lab/reports/tables/generation-008f-stationary-context.json)
Coherence: `F8F-PROJECTION-PERSISTS`, `F8F-LOCAL-GLOBAL-DECOUPLING`
Dependencies: CL-T23, CL-T15
Source generations: 008F
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-N06: Projection routing and drift-matched occupancy

**NUMERICAL_KERNEL_RESULT**

Path-first admissible dissolution exposes shape remainder; stationary shape is below floor, while DRIFT-matched laws still differ in edge and labelled occupancy.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: 8C canonical three-edge sources and 8F three sources/checkpoints 1,2,4,8,16,32,64

Method: Deterministic epoch propagation and nested equal-prior JS decomposition
Domain: 8C canonical three-edge sources and 8F three sources/checkpoints 1,2,4,8,16,32,64
Tolerances: `{"balanced_drift_gap": 1e-14, "chain_rule_gap": 1e-12, "information_floor_8f": 1e-12}`
Evidence: [generation-008f-checkpoint-bridge.json](../../constraint-lab/reports/tables/generation-008f-checkpoint-bridge.json), [generation-008f-stationary-bridge.json](../../constraint-lab/reports/tables/generation-008f-stationary-bridge.json), [generation-008c-mechanistic-decomposition.md](../../constraint-lab/reports/generation-008c-mechanistic-decomposition.md)
Coherence: `F8F-FIRST-PATH-SHAPE`, `F8F-PATH-NOT-UNIVERSAL`, `F8F-SHAPE-WASHES-OUT`, `F8F-DRIFT-MATCHED-RESIDUAL`, `F8C-PATH-CONVERTS-SLOT`
Dependencies: CL-T16, CL-T19, CL-T24
Source generations: 008C, 008F
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-I01: Current efficacy is not historical memory

**MODEL_INFERENCE**

A current hidden gate can remain effective after initial-gate information is lost in the tested visible projections.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Interpretation of current versus initial variables in 8B-8F

Argument/next test: The variables and conditioning differ; positive current CMI is not an initial-memory claim.
Evidence: [generation-008c-mechanistic-decomposition.md](../../constraint-lab/reports/generation-008c-mechanistic-decomposition.md), [generation-008f-interaction-to-topology-bridge.md](../../constraint-lab/reports/generation-008f-interaction-to-topology-bridge.md)
Coherence: `F018-LOCAL-VERSUS-INITIAL`, `F8C-CURRENT-SURVIVES`, `F8F-LOCAL-GLOBAL-DECOUPLING`, `F8G-FORMAL-INTEGRATION-RS`
Dependencies: CL-N01, CL-N05
Source generations: 008B, 008C, 008F
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-I02: Bounded occupancy and pairwise scope

**MODEL_INFERENCE**

Early bounded pairwise results and Generation 8 occupancy observations constrain this programme, not all pairwise theories or physical systems.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Interpretation of Generations 1 and 8 historical domains

Argument/next test: Evidence includes exhaustive bounded rules and historical stochastic trajectories; neither is a universal expressivity theorem.
Evidence: [generation-001-pregeometric-pairwise.md](../../constraint-lab/reports/generation-001-pregeometric-pairwise.md), [generation-008-exploration-synthesis.md](../../constraint-lab/reports/generation-008-exploration-synthesis.md)
Coherence: `F001-PAIRWISE-RISE`, `F010-OCCUPANCY-AXIS`, `F012-RAW-CONTEXT-AXIS`
Dependencies: none
Source generations: 001, 008
Boundary: No claim beyond the declared support, parameter palette, clock and observable.
Notes: Generation 8 trajectory observations retain their observational layer; no new Monte Carlo was run.

## CL-M01: Compilation before ontology-axis claims

**METHODOLOGICAL_PRINCIPLE**

Before claiming a new axis, declare preserved state, support, clock, projection, priors and budgets, and test compilation into ordinary current-state rules.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: A representation change is not automatically new dynamical expressivity.
Evidence: [expressivity-boundaries.md](../../constraint-lab/formal/expressivity-boundaries.md), [open-problems.md](../../constraint-lab/formal/open-problems.md)
Coherence: `Q-H-POSITIVE`, `Q-META-CONSTRAINT`, `F8E-ORDINARY-K-SUPPLIES-INTERACTION`, `F8G-FORMAL-H-L-DISTINCTION`, `F8G-FORMAL-COMPILATION-TEST`
Dependencies: CL-T12
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-M02: Freeze actual scientific cells before execution

**METHODOLOGICAL_PRINCIPLE**

Plumbing tests before a scientific freeze should use synthetic/historical fixtures; actual exposed cells require declaration.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: 8E qualification and 8F zero-target prefreeze pattern distinguish provenance from scientific correction.
Evidence: [008F-chatgpt-review-v0.8f.md](../../constraint-lab/provenance/reviews/008F-chatgpt-review-v0.8f.md), [generation-008e-errata.md](../../constraint-lab/reports/generation-008e-errata.md)
Coherence: `F8F-PREFREEZE-SCIENCE-GATE`
Dependencies: none
Source generations: 008E, 008F, 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-M03: Evidence dimensions are not one score

**METHODOLOGICAL_PRINCIPLE**

Magnitude, robustness, temporal character, structural role, projection sensitivity and epistemic layer remain distinct.

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: A tiny persistent projection residue can be structurally diagnostic without ranking ontology.
Evidence: [README.md](../../constraint-lab/coherence/README.md), [local-to-global.md](../../constraint-lab/formal/local-to-global.md)
Coherence: `F8F-PROJECTION-PERSISTS`, `F8F-RS-BRIDGE-INTERPRETATION`, `F8G-FORMAL-INTEGRATION-RS`
Dependencies: none
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-Q01: General minimal representation frontier

**OPEN_QUESTION**

What are the joint K/J representation frontiers for arbitrary small target tables under each alphabet and normal form?

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: Analytic lower bounds first; separately frozen bounded searches only if needed.
Evidence: [open-problems.md](../../constraint-lab/formal/open-problems.md)
Coherence: `F8E-CARDINALITY-VS-K`, `F8E-W4-COVERAGE`
Dependencies: CL-T21, CL-T22
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-Q02: Genuine same-current-state history witness

**OPEN_QUESTION**

Can a common H>0 rule distinguish futures of two reachable histories ending in the identical complete ordinary relational state?

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: Identical full material x, different last-event histories, fixed common controller and clock.
Evidence: [open-problems.md](../../constraint-lab/formal/open-problems.md)
Coherence: `Q-H-POSITIVE`, `F018-LOCAL-VERSUS-INITIAL`, `F8G-FORMAL-H-L-DISTINCTION`
Dependencies: CL-T12, CL-M01
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-Q03: Dynamic rule state versus compilable meta syntax

**OPEN_QUESTION**

Which proposed L>0 mechanisms cannot be compiled into a fixed ordinary current-state law without adding constraint state?

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: Same full material x, different reachable constraint states under one common program; explicit compilation test.
Evidence: [open-problems.md](../../constraint-lab/formal/open-problems.md)
Coherence: `Q-META-CONSTRAINT`, `F8G-FORMAL-H-L-DISTINCTION`
Dependencies: CL-T12, CL-M01
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-Q04: Breaking autonomous incidence silence and shape wash-out

**OPEN_QUESTION**

Which incidence-aware, pair-coupled or multiple-action mechanisms defeat the single-action symmetry/factorisation assumptions?

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: Name the broken hypothesis before scaling N; no N5 or XOR round opened.
Evidence: [open-problems.md](../../constraint-lab/formal/open-problems.md)
Coherence: `Q-SCALE-N`, `F8F-INCIDENCE-SILENT`, `F8F-SHAPE-WASHES-OUT`
Dependencies: CL-T19, CL-T25
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-Q05: Transition-enabling dissolution

**OPEN_QUESTION**

When does controlled dissolution enable a distinct configuration rather than merely remove one?

Assumptions: Historical domain and method retained; not extrapolated beyond cited scope..
Scope: Research-method or explicitly open scope.

Argument/next test: Matched occupancy/support passage controls; no purpose inferred from fragility.
Evidence: [open-problems.md](../../constraint-lab/formal/open-problems.md)
Coherence: `F004-PASSAGE-AFTER-OCCUPANCY`
Dependencies: none
Source generations: 008G
Boundary: No claim beyond the declared support, parameter palette, clock and observable.

## CL-T26: History-conditioned same-state divergent futures

**ALGEBRAIC_THEOREM**

Two legal equal-probability event-order histories from one augmented start end at identical complete material x but have different full and pair future rows iff m!=1.

Assumptions: Common controller, m, baseline, support and clock; x0 has only 01, no triads; h0=None; Histories form(23),form(12) and the reverse order.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t26). Commuting toggles reach pair mask 41 and zero triads. Path probabilities are 1/[10(m+9)]. Remembered slots exchange m/D and 1/D with D=m+9 or m+5.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `Q-H-POSITIVE`, `F8G-FORMAL-H-L-DISTINCTION`, `F8H-SAME-STATE-DIVERGENT-FUTURES`, `F8H-CURRENT-VS-INITIAL-MEMORY`, `F8H-H-QUESTION-RESOLUTION`, `Q-H-CONSEQUENTIAL-FUNCTIONS`
Dependencies: none
Source generations: 008H
Boundary: Both rows coincide at m=1; comparing distinct programs or different initial registers is not this witness.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T27: Non-lumpability of history erasure

**ALGEBRAIC_THEOREM**

The full-event and pair-epoch projections forgetting h are strongly lumpable iff m=1.

Assumptions: Projection (x,h)->x or (pair_mask,h)->pair_mask; Strong lumpability means equality into every projected transition block.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t27). At x*, the block toggling 12 receives m/D versus 1/D. At m=1 all full/pair rows are uniformly independent of h, including the sentinel.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `F011-QUOTIENT-INVALID`, `F8H-NONLUMPABLE-MATERIAL-PROJECTION`, `F8H-TEMPORAL-TESTS-REQUIRED`, `Q-H-COARSE-GRAINING`
Dependencies: CL-T26, CL-T20
Source generations: 008H
Boundary: Non-lumpability rules out a quotient valid for arbitrary augmented initial laws; a selected prior requires a separate process test.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T28: Unchanged-state H0 non-compilability

**ALGEBRAIC_THEOREM**

For m!=1 no fixed first-order kernel on unchanged complete ordinary x reproduces every history-conditioned projected future row.

Assumptions: One fixed kernel on the unchanged ordinary state space; All reachable history-conditioned rows must be reproduced.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t28). K0(x*,.) would need to equal the two unequal CL-T26 rows simultaneously, contradicting row uniqueness.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `F8G-FORMAL-CURRENT-STATE-EXPRESSIVITY`, `F8G-FORMAL-COMPILATION-TEST`, `Q-H-POSITIVE`, `F8H-FIXED-STATE-NONCOMPILABILITY`, `F8H-RS-HISTORY-INTERPRETATION`
Dependencies: CL-T26, CL-T12
Source generations: 008H
Boundary: State augmentation, altered update support and marginal-only matching are outside this impossibility theorem.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T29: State augmentation restores Markov form

**ALGEBRAIC_THEOREM**

RECENT-REVERSAL is first-order Markov on the finite augmented state (x,h).

Assumptions: The register is explicit augmented state; Pair updates set h to the slot; triad updates preserve h.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t29). The next event row and deterministic augmented update depend only on current (x,h).
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `F8G-FORMAL-H-L-DISTINCTION`, `F8G-FORMAL-COMPILATION-TEST`, `F8H-AUGMENTED-MARKOV-RESTORATION`, `F8H-RS-HISTORY-INTERPRETATION`
Dependencies: none
Source generations: 008H
Boundary: An S encoding or binary multibit update is a representation change; no absolute non-Markovianity or irreducible time is established.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T30: Exact pair-event quotient closure

**ALGEBRAIC_THEOREM**

Summing triad-only excursions gives the exact next-pair kernel on (pair_mask,h), with 384 recurrent states and q_h(e)=m/(m+5) for e=h, otherwise 1/(m+5).

Assumptions: Triad toggles preserve pair mask and h; Unit triad weights; pair weights do not read triad state; The initial sentinel gives uniform pair slots.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t30). The geometric excursion sum [w_e/(m+9)]/[1-4/(m+9)] equals w_e/(m+5); pair absorption occurs almost surely.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `F011-QUOTIENT-INVALID`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `F8H-PAIR-EPOCH-CLOSURE`
Dependencies: CL-T29
Source generations: 008H
Boundary: Different history updates or triad-dependent hazards need a new closure proof; no raw-triad prior is assumed.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T31: Uniform stationary pair/history law and one-step material equality

**ALGEBRAIC_THEOREM**

The recurrent pair-epoch chain has unique uniform stationary joint law pi(p,h)=1/384, independent mask/history, H0 material occupancy and H0 stationary one-step projected pair rows.

Assumptions: m>0; pair-epoch clock after the sentinel; Stationary initial law for the projected one-step comparison.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t31). Each destination has six predecessors with incoming sum one. Positive slot sequences give irreducibility; parity and a two-step return give period two. Uniform joint law implies independent uniform marginals and averaged slot probability 1/6.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `Q-H-POSITIVE`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `F8H-STATIONARY-OCCUPANCY-INVARIANCE`, `F8H-PROCESS-GRAMMAR-WITHOUT-OCCUPANCY`, `Q-H-PERSISTENT-STRUCTURE`
Dependencies: CL-T30
Source generations: 008H
Boundary: Period two prevents pointwise convergence from fixed parity. Full-event pair-versus-triad hazard and multi-time laws need not match H0.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T32: History-slot eigenstructure and initial-history decay

**ALGEBRAIC_THEOREM**

The six-slot matrix has eigenvalues 1 and lambda=(m-1)/(m+5) of multiplicity five; Q^k=Pi+lambda^k(I-Pi), and TV from a fixed initial slot is (5/6)|lambda|^k.

Assumptions: Pi is the uniform six-slot rank-one matrix; Pair-event clock; finite m>0.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t32). Q=Pi+lambda(I-Pi) acts diagonally on constant and zero-sum subspaces; |lambda|<1. Its powers yield the exact conditional row and TV.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `F018-LOCAL-VERSUS-INITIAL`, `F8C-CURRENT-SURVIVES`, `F8H-CURRENT-VS-INITIAL-MEMORY`
Dependencies: CL-T30
Source generations: 008H
Boundary: Decay concerns initial-slot information in current h, not all initial-condition information in every material multi-time observable.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T33: Exactly order-two projected pair-mask process

**ALGEBRAIC_THEOREM**

After an observed pair transition the material pair process has order at most two; at stationary law it has exactly order two for m!=1 and is first-order for m=1.

Assumptions: Pair snapshots observe every pair toggle; Positive stationary law for the order-one failure witness.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t33). The one-hot XOR of previous/current masks identifies h. All earlier snapshots are conditionally irrelevant, while distinct incoming slots into the same current mask give unequal next rows for non-neutral m.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `Q-H-POSITIVE`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `F8H-ORDER2-PROJECTED-PROCESS`, `F8H-TEMPORAL-TESTS-REQUIRED`, `Q-H-DEPTH`
Dependencies: CL-T26, CL-T30, CL-T31
Source generations: 008H
Boundary: No finite Markov-order claim is made for full-event snapshots containing arbitrarily long triad-only waits.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T34: Temporal backtracking and consecutive-slot information

**ALGEBRAIC_THEOREM**

Stationary pair-mask backtracking is m/(m+5), and consecutive-event MI is ln 6+a ln a+5b ln b, with a=m/(m+5), b=1/(m+5); MI vanishes iff m=1.

Assumptions: Stationary uniform history on the pair clock; Exactly one pair bit toggles at each pair epoch.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t34). Two toggles restore a mask iff slots repeat. The joint slot law Q_ij/6 has uniform marginals; direct KL gives the expression and strict positivity away from neutral.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `Q-H-POSITIVE`, `F018-LOCAL-VERSUS-INITIAL`, `F8H-TEMPORAL-CORRELATION`, `F8H-CURRENT-VS-INITIAL-MEMORY`, `F8H-PROCESS-GRAMMAR-WITHOUT-OCCUPANCY`, `F8H-TEMPORAL-TESTS-REQUIRED`
Dependencies: CL-T31, CL-T32
Source generations: 008H
Boundary: A temporal process statistic is distinct from a one-time occupancy or a master memory score.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-T35: Same-state pure shape witness at equal edge-count law

**ALGEBRAIC_THEOREM**

At the path endpoint, middle-last and end-last histories have identical next pair-event edge-count law but unequal graph-class law iff m!=1; equal-prior class information equals shape-given-edge information.

Assumptions: Path 01-12-23, no triads; Historical exact N=4 graph classifier; Equal history prior from equal-probability common-start paths.
Scope: RECENT-REVERSAL(m), m>0, N=4 O=3 independent relations; H_pair=1, G=S=L=0.

Proof: [history.md](../../constraint-lab/formal/history.md#cl-t35). Classify the six actual toggles. Both count laws have masses (m+2,3)/(m+5); matching masses differ by (m-1)/(m+5). Class determines count, so the information chain rule removes the zero count term.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `Q-H-POSITIVE`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `F8H-PURE-SHAPE-WITNESS`, `Q-H-COARSE-GRAINING`
Dependencies: CL-T26, CL-T16
Source generations: 008H
Boundary: This is conditional next-step shape discrimination, compatible with unchanged stationary history-marginalised occupancy.
Notes: Symbolic predeclared expectation before freeze; post-freeze finite rational and numerical checks are separate CL-F05/CL-N07. Representation-relative model statement.

## CL-F05: Frozen H0 exact finite verification

**FINITE_EXHAUSTIVE_RESULT**

All rational controls and identities in the 11 frozen H0 items pass for m=1/4,1,4, including the common-start witness, 384-state balance, raw-triad quotient and order-two checks.

Assumptions: Frozen H0 plan and exact rational controller; No non-neutral target execution before committed/pushed freeze.
Scope: Three multipliers and the enumerated H0 domains only.

Enumeration: 11 H0 atomic items; 6912 epoch transition entries, 1008 raw-triad absorption rows, 6912 consistent material triples, 41472 two-step paths and 71680 deterministic updates.; exact count 11. Verifier: [gen008h_exec.py](../../constraint-lab/src/rs_constraint_lab/gen008h_exec.py)
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py), [generation-008h-round-h0-tables.json](../../constraint-lab/reports/generation-008h-round-h0-tables.json), [generation-008h-validation.json](../../constraint-lab/reports/tables/generation-008h-validation.json)
Coherence: `Q-H-POSITIVE`, `F8H-SAME-STATE-DIVERGENT-FUTURES`, `F8H-NONLUMPABLE-MATERIAL-PROJECTION`, `F8H-AUGMENTED-MARKOV-RESTORATION`, `F8H-PURE-SHAPE-WITNESS`, `F8H-PAIR-EPOCH-CLOSURE`, `F8H-STATIONARY-OCCUPANCY-INVARIANCE`, `F8H-ORDER2-PROJECTED-PROCESS`, `F8H-H-QUESTION-RESOLUTION`
Dependencies: CL-T26, CL-T27, CL-T29, CL-T30, CL-T31, CL-T32, CL-T33, CL-T34, CL-T35
Source generations: 008H
Boundary: The finite checks do not prove all-m statements; those use CL-T26..T35. Irrational information values and float eigenvalues are separately CL-N07.
Notes: All rational validation gaps zero; zero stochastic trajectories.

## CL-N07: H0 numerical information and eigenvalue checks

**NUMERICAL_KERNEL_RESULT**

From exact rational H0 rows, 160-digit information evaluations and floating eigenvalues agree with independently derived formulas within frozen 1e-13 tolerances.

Assumptions: Exact probability tables; Natural logarithms, equal history prior for row/shape JS; NumPy eigvalsh for the numerical cross-check.
Scope: m=1/4,1,4 in H0; numerical values, not a parameter census.

Method: 160-digit Decimal logarithms from Fraction probabilities; enumerated JS/MI compared with formulas; exact eigenbasis identity plus floating eigvalsh cross-check.
Domain: Full/pair row JS, graph-class JS, consecutive-event MI and six-slot eigenvalues for three grades.
Tolerances: `{"eigenvalue_gap": "1e-13", "information_formula_gap": "1e-13"}`
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py), [generation-008h-witness.json](../../constraint-lab/reports/tables/generation-008h-witness.json), [generation-008h-history-chain.json](../../constraint-lab/reports/tables/generation-008h-history-chain.json), [generation-008h-validation.json](../../constraint-lab/reports/tables/generation-008h-validation.json)
Coherence: `Q-H-POSITIVE`, `F8H-SAME-STATE-DIVERGENT-FUTURES`, `F8H-PURE-SHAPE-WITNESS`, `F8H-TEMPORAL-CORRELATION`
Dependencies: CL-T32, CL-T34, CL-T35, CL-F05
Source generations: 008H
Boundary: Display rounding is not exact irrational equality; external reference values are review checks rather than stored scientific input.
Notes: Maximum information formula gap 2e-160; floating eigenvalue gap 4.441e-16.

## CL-Q06: Minimal state augmentation for recent-reversal memory

**OPEN_QUESTION**

What is the minimal augmented state that restores first-order Markov sufficiency for this specific projected pair process, under an explicitly declared encoding and clock?

Assumptions: RECENT-REVERSAL, non-neutral m; The six-valued last-pair slot is already known sufficient.
Scope: Specific finite controller; no general hidden-state minimisation task opened.

Argument/next test: Declare preserved material projection and update support, then seek a scoped minimality argument; H0 executes no follow-up.
Evidence: [history.md](../../constraint-lab/formal/history.md), [generation-008h-history-as-state.md](../../constraint-lab/reports/generation-008h-history-as-state.md), [test_v08h.py](../../constraint-lab/tests/test_v08h.py)
Coherence: `Q-H-POSITIVE`, `Q-H-MINIMAL-STATE`
Dependencies: CL-T29, CL-T33
Source generations: 008H
Boundary: At m=1 the register is unnecessary. General H functions, arbitrary hidden-state models and L mechanisms are separate questions.
Notes: Historical CL-Q02 is retained; CL-T26 answers its scoped existence question.

## CL-T36: Generic history/present pair-event closure

**ALGEBRAIC_THEOREM**

Positive pair weights depending only on current pair mask and remembered pair slot close exactly on (p,h) after summing unit triad-only excursions that preserve both coordinates.

Assumptions: Four unit triad toggles, unread by controller; h'=e after a pair toggle, preserved after triad toggles; W(p,h)>0.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t36). Geometric absorption gives [w_e/(W+4)]/[1-4/(W+4)]=w_e/W, with almost sure next-pair arrival.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8H-PAIR-EPOCH-CLOSURE`, `F011-QUOTIENT-INVALID`, `F8I-VALID-ROLE-QUOTIENT`
Dependencies: CL-T30
Source generations: 008I
Boundary: Triad-dependent weights or history updates require a new closure argument; no dense full augmented kernel or triad prior is assumed.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T37: Historical role S4 covariance and valid orbit quotient

**ALGEBRAIC_THEOREM**

All eleven role predicates are S4 covariant under simultaneous vertex relabelling of p,h,e; their 28 state orbits give a valid dynamical quotient for all m>0.

Assumptions: rho uses pair equality/intersection; Direction reads candidate presence; Positive weights m^phi and deterministic single-toggle/register update.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t37). Vertex maps preserve rho, direction, denominator and update. Kernel automorphism orbits have identical aggregate block rows. A marked-edge stabiliser gives 2*2*7=28 orbits.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F011-QUOTIENT-INVALID`, `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `F8I-VALID-ROLE-QUOTIENT`
Dependencies: CL-T20, CL-T36
Source generations: 008I
Boundary: The diagnostic tuple has collisions and is not substituted for the actual orbit partition; no larger symmetry is presumed.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T38: Regular history-only joint uniformity

**ALGEBRAIC_THEOREM**

A p-independent doubly stochastic slot matrix gives uniform stationary joint law on pair mask and history. Positive symmetric regular SAME/ADJACENT/DISJOINT weighting satisfies this and has unique stationary occupancy with period two.

Assumptions: Slot law independent of p; Doubly stochastic slot matrix; strictly positive for irreducibility/uniqueness; Pair toggle and h'=event.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t38). Each destination (p',j) has predecessors (p' xor 2^j,i), with incoming sum one. Symmetric regular class counts 1,4,1 make Q doubly stochastic. Positive slot sequences and j,j suffix prove communication; parity and a two-step return prove period two.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8H-STATIONARY-OCCUPANCY-INVARIANCE`, `Q-H-CONSEQUENTIAL-FUNCTIONS`, `F8I-HISTORY-ONLY-STATIONARY-SILENCE`
Dependencies: CL-T36
Source generations: 008I
Boundary: Not a theorem for p-reading cross controllers or pointwise convergence from fixed parity.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T39: One-pair memory order bound and first-order criterion

**ALGEBRAIC_THEOREM**

For any current-pair/last-pair-slot law, the pair-mask process has order at most two after an observed pair transition. Under positive stationary augmented law it is first-order iff the row is h-independent at every p, otherwise exactly order two.

Assumptions: One pair bit toggles each epoch; Register equals last pair slot; All slots positive for the stationary necessity argument.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t39). One-hot XOR recovers h. At stationary law all previous neighbours into a fixed p have positive mass, so unequal recovered-history rows violate order one. Equality is exactly history-erasure lumpability.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8H-ORDER2-PROJECTED-PROCESS`, `F8H-NONLUMPABLE-MATERIAL-PROJECTION`, `F8I-CURRENT-ONLY-HISTORY-CORRELATION`, `F8I-ORDER-ATLAS`, `F8I-REPRESENTATION-READING`
Dependencies: CL-T33, CL-T36
Source generations: 008I
Boundary: Pair-event clock and compatible observed transitions; no full-event finite-order or absolute non-Markovianity claim.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T40: Stationary S4 invariance and coarse history-label silence

**ALGEBRAIC_THEOREM**

Unique stationary S4-covariant laws are S4 invariant. Material masks are class-uniform; invariant material observables are independent of the labelled history slot. Two such material models have zero labelled remainder beyond graph class.

Assumptions: Unique finite stationary augmented law; S4 kernel covariance; History slots form one transitive S4 orbit.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t40). Relabelled pi is stationary and hence equal by uniqueness. Invariant g(p) is fixed while h is transitive, yielding pi(g,h)=pi(g)/6. Uniform conditional mask laws inside each class eliminate model/mask conditional information.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8G-FORMAL-EQUIVALENCE-HIERARCHY`, `Q-H-COARSE-GRAINING`, `F8I-COARSE-HISTORY-INFORMATION-ZERO`
Dependencies: CL-T37, CL-T16
Source generations: 008I
Boundary: Does not force I(P;H), model/class information or shape-given-edge information to vanish; remembered-label information differs from relational role information.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T41: Uniform and stationary history projection identities

**ALGEBRAIC_THEOREM**

KU is stochastic. Kpi weighted by stationary h|p preserves pi_P exactly, and Kpi-KU equals the conditional-history deviation from uniform weighted against each normalised event row.

Assumptions: Finite stationary augmented law; Positive material marginal; KU uses uniform h; Kpi uses actual stationary h|p.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t41). Sum the augmented stationary flow over projected destinations; subtract uniform versus conditional row averages for the feedback identity.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8G-FORMAL-COMPILATION-TEST`, `F8H-FIXED-STATE-NONCOMPILABILITY`, `F8I-CURRENT-ONLY-HISTORY-CORRELATION`, `F8I-HISTORY-PRESENT-FEEDBACK`, `F8I-MATCHED-KU-DIFFERENT-STRUCTURE`, `F8I-REPRESENTATION-READING`
Dependencies: CL-T36
Source generations: 008I
Boundary: Stationary one-step representation is weaker than matching every conditioned history row. Correlation alone need not cause a KU discrepancy; KU is only one comparator.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T42: Augmented last-event bookkeeping irreversibility

**ALGEBRAIC_THEOREM**

A strictly positive toggle/register process with at least two slots is non-reversible on augmented state even if the material law is H0.

Assumptions: Positive stationary mass on recurrent augmented states; h'=event; Exactly one bit toggles.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t42). An event e!=h sends (p,h) to (p xor 2^e,e). Returning material p requires toggling e and therefore cannot restore h. The reverse augmented arrow is absent, violating detailed balance.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8H-AUGMENTED-MARKOV-RESTORATION`, `F8H-TEMPORAL-TESTS-REQUIRED`, `F8I-REGISTER-IRREVERSIBILITY-BOUNDARY`
Dependencies: none
Source generations: 008I
Boundary: No assertion about every quotient, Kpi reversibility, thermodynamics or a memory-strength measure.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T43: SAME-direction stationary factorisation and coordinate symmetry

**ALGEBRAIC_THEOREM**

For d slots, SAME_FORM has pi(p,h)=[1/(2d)]r^(|p|-p_h)(1-r)^(d-1-|p|+p_h), r=(m+d-1)/(m+2d-1). SAME_DISSOLVE is its complement. Material occupancy depends only on edge count despite non-neutral historical efficacy.

Assumptions: d>=2 and m>0; SAME x declared current direction, unit alternatives; Single toggle and h'=event.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t43). Full coordinate permutations preserve the law. The candidate normalises and balances directly by separating destination remembered bit R=0 or 1 and counting other-present/absent bits. Positivity gives uniqueness. Conditional on h, R is uniform and other bits iid Bernoulli(r).
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `Q-H-PERSISTENT-STRUCTURE`, `Q-H-CONSEQUENTIAL-FUNCTIONS`, `F8I-SAME-SYMMETRY-FACTORIZATION`
Dependencies: CL-T36, CL-T39
Source generations: 008I
Boundary: A larger dynamical bit-coordinate symmetry is not graph isomorphism or geometry. The formula is scoped to SAME-direction controllers; DISJ has explicit violating generators.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-T44: Singleton-selector uniform-history equivalence

**ALGEBRAIC_THEOREM**

Any bijective history-slot selector f in a single direction-gated feature has the same KU as SAME. In particular SAME and DISJ cross controllers at N=4 have identical KU for every positive m.

Assumptions: Feature weights e=f(h) and the declared current direction; f bijective; history uniformly averaged at each fixed p; Normalised event rows, not averaged raw weights.
Scope: Generation 8I declared positive pair-toggle/history grammar, with clock and representation assumptions stated.

Proof: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md#cl-t44). q_f(p,h,e)=q_SAME(p,f(h),e), including its denominator. Reindex the uniform history sum. Relabelling history alone changes update to g'=f(e), so this does not conjugate the full program.
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [test_v08i.py](../../constraint-lab/tests/test_v08i.py), [test_v08i_followup.py](../../constraint-lab/tests/test_v08i_followup.py)
Coherence: `F8G-FORMAL-COMPILATION-TEST`, `Q-H-CONSEQUENTIAL-FUNCTIONS`, `F8I-EXACT-EQUIVALENCE-LEVELS`, `F8I-SINGLETON-KU-EQUIVALENCE`, `Q-H-SELECTOR-CLASSIFICATION`
Dependencies: CL-T41, CL-T36
Source generations: 008I
Boundary: Not equality of conditioned rows, full processes or true stationary laws; two-grade I1 counterexamples distinguish them. No general irreducible-history claim.
Notes: Reusable proof, distinct from finite grade-specific stationary/information observations. I0 and I1 were separately frozen; historical statements retained.

## CL-F06: Marked-edge orbit and diagnostic-collision enumeration

**FINITE_EXHAUSTIVE_RESULT**

The 384 augmented K4 pair/history states partition into 28 S4 orbits. The diagnostic tuple (R,A_h,D_h,C_h) has 24 values and four two-orbit collisions.

Assumptions: Simultaneous vertex relabelling of pair mask and marked history edge; Historical edge ordering and graph classifier preserved.
Scope: Structural N=4 enumeration, explicitly observed before I0 as authorised.

Enumeration: 384 pair-mask/history states under all 24 vertex permutations; independent stabiliser orbit count.; exact count 384. Verifier: [history_roles.py](../../constraint-lab/src/rs_constraint_lab/history_roles.py)
Evidence: [history-role-grammar.md](../../constraint-lab/formal/history-role-grammar.md), [structural-orbits.json](../../constraint-lab/exploration/generation-008i/structural-orbits.json), [test_v08i.py](../../constraint-lab/tests/test_v08i.py)
Coherence: `F011-QUOTIENT-INVALID`, `F8I-VALID-ROLE-QUOTIENT`
Dependencies: CL-T37
Source generations: 008I
Boundary: Diagnostic descriptors are not treated as sufficient coordinates or a valid quotient by themselves.
Notes: No non-neutral scientific cell was executed for this structural enumeration.

## CL-T45: Stationary material one/two-time matching and deterministic coarse pushforward

**ALGEBRAIC_THEOREM**

Kpi preserves the stationary material marginal and adjacent two-time joint of its source augmented process; every deterministic material projection inherits exact word equality at lengths one and two.

Assumptions: Stationary finite augmented law pi(p,h); Kpi is the pi(h|p)-weighted material row on positive marginal support.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t45). Expand the stationary adjacent joint and sum over h; push forward equal measures along deterministic maps.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-MATCHED-ONE-TWO-TIME`, `F8J-REPRESENTATION-READING`
Dependencies: CL-T41
Source generations: 008J
Boundary: No claim of conditioned-row or longer path equality.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-T46: Passive deterministic register finite-path equivalence

**ALGEBRAIC_THEOREM**

If the material future row is register-independent, projecting a passive deterministic register gives exactly the same finite material/coarse path measures as the corresponding Kpi chain at every word length.

Assumptions: Future material row independent of register; Passive deterministic update; matching initial material marginal.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t46). Iterated conditioning factors the material path law into its initial marginal and register-independent transition rows.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-PASSIVE-REGISTER-PATH-EQUALITY`
Dependencies: CL-T45
Source generations: 008J
Boundary: Register/material correlation and bookkeeping irreversibility need not vanish.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-T47: Covariant stationary Kpi and exact graph-class Markov quotient

**ALGEBRAIC_THEOREM**

Invariant stationary augmented law and S4-covariant dynamics imply S4-covariant Kpi; graph classes are a strongly lumpable eleven-state material orbit quotient.

Assumptions: Simultaneous S4 covariance; Invariant stationary joint and positive material support; K4 graph classes are S4 material orbits.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t47). Reindex conditional history sums under g, then aggregate Kpi destinations over invariant S4 orbits.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-KPI-CLASS-MARKOV`
Dependencies: CL-T37, CL-T40, CL-T45
Source generations: 008J
Boundary: Edge count merges distinct orbits and needs a separate lumpability test.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-T48: Absolute history-label silence in invariant finite stationary windows

**ALGEBRAIC_THEOREM**

Every absolute remembered-pair label is independent of any finite stationary S4-invariant material observation word; its conditional probability is 1/6.

Assumptions: Stationary S4-invariant path measure (uniqueness plus covariance suffices); History-label action transitive on six pair slots; Observation word invariant under simultaneous relabelling.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t48). Stationary path invariance equates the six joint masses Pr(H_t=h,W=w); summing labels yields Pr(W=w)/6.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-INVARIANT-WINDOW-LABEL-SILENCE`
Dependencies: CL-T40
Source generations: 008J
Boundary: Does not imply relational role silence; non-invariant starts or label-sensitive words lie outside scope.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-T49: Class-word density-path and shape-sequence information chain

**ALGEBRAIC_THEOREM**

For E^L=f(C^L), I(M;C^L)=I(M;E^L)+I(M;C^L|E^L), with nonnegative conditional term and data processing.

Assumptions: Deterministic edge-word projection of class word; Joint model/word law; equal global model prior for JS interpretation.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t49). Apply the information chain rule to (C^L,E^L), which contains exactly the information in C^L.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-SHAPE-SEQUENCE-SIGNAL`, `F8J-SNAPSHOT-SHAPE-VS-PROCESS-SHAPE`
Dependencies: none
Source generations: 008J
Boundary: Equal global priors do not imply equal within-edge-word priors.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-T50: K4 graph-class order at most two by marked-role reconstruction

**ALGEBRAIC_THEOREM**

A valid S4 marked-pair role chain with h'=e and one-bit pair toggles has graph-class output of order at most two once an actual pair transition has occurred.

Assumptions: K4 single-pair toggles; Valid first-order simultaneous-S4 role quotient; Class-pair reconstruction certificate CL-F07.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t50). Two consecutive classes identify the current role orbit by CL-F07; the quotient's next-class law depends only on that orbit.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-CLASS-EXACT-ORDER-TWO`, `F8J-REPRESENTATION-READING`, `Q-H-CLASS-PAIR-GENERALISATION`
Dependencies: CL-T37, CL-F07
Source generations: 008J
Boundary: Not a larger-N theorem. Exactly order two also requires a positive first-order witness; no infinite-memory conclusion for coarser edge output.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-T51: SAME count and remembered-bit quotient with exact edge order

**ALGEBRAIC_THEOREM**

SAME ANY/FORM/DISSOLVE admits a 2d-state (k,p_h) quotient with aggregate formation/dissolution weights; edge count is order at most two, exactly two for positive non-neutral m and d>=2 with positive stationary support.

Assumptions: Single pair-bit toggle and last-slot update; SAME features only; positive m; d>=2 and positive stationary support for failure of order one.
Scope: Declared finite pair-event state/projection assumptions; not an ontology theorem.

Proof: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md#cl-t51). Count absent/present weights F,D. The next roles are (k+1,1),(k-1,0); the last count increment recovers p_h. Compare the two feasible k=1 roles to refute order one iff m!=1.
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [test_v08j.py](../../constraint-lab/tests/test_v08j.py), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-SAME-EDGE-ORDER-TWO`, `F8J-REPRESENTATION-READING`
Dependencies: CL-T36
Source generations: 008J
Boundary: No ADJ/DISJ closure; their tested (k,R) projections fail.
Notes: Reusable algebraic result, separate from finite two-grade observations; exact J0 and independently frozen J1 evidence identified in report.

## CL-F07: K4 consecutive-class marked-role reconstruction certificate

**FINITE_EXHAUSTIVE_RESULT**

All 384 augmented K4 states map constantly and injectively from 28 simultaneous-S4 role orbits to (class(p xor 2^h),class(p)); there are 28 distinct pairs and zero collisions.

Assumptions: Six labelled K4 pair slots and one marked history slot; Historical graph classifier and simultaneous vertex action.
Scope: Finite exact K4 structural certificate from separately frozen J1.

Enumeration: All 384 (p,h) states, 28 complete orbit fibres and every pair-image collision test; exact count 384. Verifier: [gen008j_followup.py](../../constraint-lab/src/rs_constraint_lab/gen008j_followup.py)
Evidence: [coarse-process-memory.md](../../constraint-lab/formal/coarse-process-memory.md), [J1-CLASS-PAIR-ROLE.json](../../constraint-lab/reports/items/generation-008j-j1/J1-CLASS-PAIR-ROLE.json), [test_v08j_followup.py](../../constraint-lab/tests/test_v08j_followup.py)
Coherence: `F8J-CLASS-PAIR-ROLE-RECONSTRUCTION`, `Q-H-CLASS-PAIR-GENERALISATION`
Dependencies: CL-T37
Source generations: 008J
Boundary: No N5, multibit-event or deeper-history extension is asserted.
Notes: A finite certificate used by CL-T50, not a general graph reconstruction theorem.

