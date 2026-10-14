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

## CL-T52: Coarsest strongly lumpable observation refinement

**ALGEBRAIC_THEOREM**

Exact iterative block-signature splitting terminates at the unique coarsest strongly lumpable refinement of a finite observation partition.

Assumptions: Finite rational stochastic kernel; Initial partition covers every state exactly once.
Scope: Arbitrary augmented initial laws; generic utility, not generally all-word minimal hidden-model realisation.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t52). Termination by strictly increasing block count; fixed-point signatures define a quotient; induction shows every strongly lumpable observation refinement refines every intermediate partition and hence the fixed point.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-PREDICTIVE-COMPRESSION-LADDER`, `F8IP-MINIMALITY-SCOPE`
Dependencies: none
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T53: Minimal labelled-mask history and synchronization

**ALGEBRAIC_THEOREM**

For RECENT-REVERSAL, non-neutral labelled-mask prediction requires all six histories per mask (384 states), synchronized by two masks; neutral collapses to 64 states and one observation.

Assumptions: N4 RECENT-REVERSAL; m>0; Current labelled mask preserved; Pair-event clock.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch. All positive m, with m=1 separated.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t53). Different h assign the m weight to different labelled successors, so one-step observed rows differ iff m!=1. Consecutive masks recover h by one-hot XOR. Positive stationary predecessor witnesses exclude order one.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-TWO-SNAPSHOT-SYNCHRONIZATION`
Dependencies: CL-T52, CL-T33
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T54: Simultaneous marked-graph S4 quotient

**ALGEBRAIC_THEOREM**

Simultaneous vertex relabelling of pair mask, history slot and candidate event commutes with RECENT-REVERSAL and defines a strong S4 orbit quotient.

Assumptions: N4 RECENT-REVERSAL; m>0; S4 acts on p and h together.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch. Strong lumpability for arbitrary augmented starts.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t54). Equality e=h and the xor toggle/update h'=e commute with relabelling. Orbit summation preserves aggregate rows. Stabiliser action on h identifies fixed-current-graph pair roles.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-GRAPH-STRUCTURAL-HISTORY`, `F8IP-QUOTIENT-CORRECTNESS`
Dependencies: CL-T30
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T55: Minimal structural-role history and graph-class synchronization

**ALGEBRAIC_THEOREM**

For every positive non-neutral m the coarsest graph-class-preserving refinement consists of 28 marked-pair roles; class pairs synchronize it and stationary class order is exactly two. Neutral collapses to 11 first-order classes.

Assumptions: CL-F08 N4 role enumeration and toggle-class injectivity; RECENT-REVERSAL, m>0; Pair-event clock.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch. Count is finite N4 structure; algebra covers all positive non-neutral m.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t55). S4 supplies sufficiency. At fixed graph n_G(c)+(m-1) times the indicator of remembered-toggle class determines the row; distinct roles have distinct toggle classes, giving immediate row separation for m!=1. Previous/current class pairs identify roles. One-edge positive-predecessor witness excludes order one.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-GRAPH-STRUCTURAL-HISTORY`, `F8IP-GRAPH-28-STATE-REFINEMENT`, `F8IP-TWO-SNAPSHOT-SYNCHRONIZATION`, `F8IP-COARSE-GRAINED-ORDER2`
Dependencies: CL-T52, CL-T54, CL-F08
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T56: Minimal directional edge-count memory

**ALGEBRAIC_THEOREM**

Count prediction closes exactly on twelve legal (k,r=p_h) states; interior r rows differ iff m!=1, two counts synchronize, and stationary count order is exactly two non-neutrally and one neutrally.

Assumptions: Six pair slots; RECENT-REVERSAL, m>0; Current count preserved; Pair-event clock.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch. All m>0; neutral has seven count states.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t56). Aggregate dissolution k+(m-1)r and formation 6-k+(m-1)(1-r), divide by m+5; next r is event direction. Interior row difference (m-1)/(m+5) proves minimality. Count increment recovers r; positive count-zero/two predecessor witness excludes first order.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-EDGE-DIRECTION-HISTORY`, `F8IP-EDGE-12-STATE-REFINEMENT`, `F8IP-TWO-SNAPSHOT-SYNCHRONIZATION`, `F8IP-COARSE-GRAINED-ORDER2`
Dependencies: CL-T52, CL-T31
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T57: All-order parity history erasure

**ALGEBRAIC_THEOREM**

Parity is a two-state deterministic alternating quotient for every multiplier; given initial parity every finite parity path law is independent of history and m.

Assumptions: Exactly one pair bit toggled per pair epoch; Initial parity declared.
Scope: All m>0; arbitrary augmented initial law with the same parity marginal.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t57). Each toggle flips parity, so R_t=R_0 xor (t mod 2) pathwise. Initial two-block partition is strongly lumpable; preserving current parity prohibits a one-block refinement.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-PARITY-HISTORY-ERASURE`, `F8IP-COARSE-GRAINED-ORDER2`, `F8IP-ONE-STEP-INVISIBILITY-PERSISTS`
Dependencies: CL-T30
Source generations: 008I
Boundary: Pair-event clock only; triad events do not necessarily flip pair parity on the full-event clock. No physical erasure claim.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T58: Stationary quotient laws and one-step projected invisibility

**ALGEBRAIC_THEOREM**

Uniform augmented occupancy pushes exactly to quotient masses; edge-role masses are C(5,k-r)/64 and stationary one-step observed rows equal H0 at mask, class, count and parity.

Assumptions: CL-T31 uniform joint stationary law; Certified strong quotients; Stationary pair-event epochs.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch. Stationary equality, not arbitrary-start history averaging.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t58). Quotient balance follows by pushforward. Fixing h leaves five independent fair bits, giving binomial edge-role masses. Conditional r mean k/6 yields neutral Ehrenfest count row. Uniform h at each p gives 1/6 slot law, and deterministic projection preserves adjacent joint equality.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-ONE-STEP-INVISIBILITY-PERSISTS`
Dependencies: CL-T31, CL-T56, CL-T57
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-T59: Commuting predictive quotient ladder

**ALGEBRAIC_THEOREM**

The non-neutral 384->28->12->2 and neutral 64->11->7->2 predictive ladders are nested deterministic strong lumpings whose kernels and stationary pushforwards commute.

Assumptions: N4 RECENT-REVERSAL, m>0; Certified nested mask/role/count/parity partitions.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch. Strong quotient identity, not matching counts alone.

Proof: [predictive-state.md](../../constraint-lab/formal/predictive-state.md#cl-t59). Each target datum is constant on source blocks. Direct strong-lumping identities imply equal source rows into unions of target blocks, giving the same direct target kernel. Stationary pushforwards compose.
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json)
Coherence: `F8IP-PREDICTIVE-COMPRESSION-LADDER`, `F8IP-QUOTIENT-CORRECTNESS`
Dependencies: CL-T54, CL-T55, CL-T56, CL-T57, CL-T58
Source generations: 008I
Boundary: Declared observation-preserving fixed-state strong refinement; not an arbitrary hidden-state encoding, minimal ontology or physical history law.
Notes: Alternative predictive-state 8I. IDs reserved above all accessible related-branch IDs; historical rows unchanged. Prior exposure disclosed; new verification follows pushed freeze.

## CL-F08: Exact predictive refinement and synchronization certificates

**FINITE_EXHAUSTIVE_RESULT**

All twelve projection/grade refinements match independent structural partitions; the N4 marked-pair atlas has 28 roles with distinct predecessor classes per current class, 28 legal class pairs and 12 count pairs, and all nine quotient arrows commute exactly.

Assumptions: Exact Fraction kernels at m=1/4,1,4; Frozen pushed I0 plan; S4/Aut(G) independent orbit routes.
Scope: N4/O3 independent hypergraph, RECENT-REVERSAL, H_pair=1, pair-event clock; fixed 384-state recurrent representation. Alternative predictive-state 8I; not the role-grammar branch.

Enumeration: 384 recurrent states, four projections, three grades; 24 S4 permutations; independent pair-orbit, (k,r) and generic-refinement routes; exact count 12. Verifier: [gen008i_predictive_exec.py](../../constraint-lab/src/rs_constraint_lab/gen008i_predictive_exec.py)
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json), [generation-008i-predictive-orbits.json](../../constraint-lab/reports/tables/generation-008i-predictive-orbits.json)
Coherence: `F8IP-PREDICTIVE-COMPRESSION-LADDER`, `F8IP-GRAPH-28-STATE-REFINEMENT`, `F8IP-EDGE-12-STATE-REFINEMENT`, `F8IP-TWO-SNAPSHOT-SYNCHRONIZATION`, `F8IP-QUOTIENT-CORRECTNESS`, `F8IP-MINIMALITY-SCOPE`
Dependencies: CL-T52, CL-T54
Source generations: 008I
Boundary: Finite N4 counts; m-neutral collapse checked separately. No new controller or graph size executed.
Notes: 1986 merge certificates; membership comparison under state reordering and across non-neutral grades; prior related exposure disclosed.

## CL-N08: Projected stationary temporal conditional information

**NUMERICAL_KERNEL_RESULT**

At m=1/4 and 4, class/count temporal CMI is positive; neutral and parity have exact conditional-independence identities, and independent information evaluations meet the frozen tolerance.

Assumptions: Exact rational stationary triple tables; Pair-event clock; Natural logarithms.
Scope: N4 RECENT-REVERSAL m=1/4,1,4; four declared projections.

Method: 160-digit Decimal logs on exact triples; inverse-event versus two-forward exact enumeration; independent quotient-row KL; labelled CL-T34 event-MI formula
Domain: Twelve stationary projected CMI cells
Tolerances: `{"formula_enumeration_gap": "1e-25", "rational_triple_identity": "exact"}`
Evidence: [predictive-state.md](../../constraint-lab/formal/predictive-state.md), [generation-008i-predictive-state.md](../../constraint-lab/reports/generation-008i-predictive-state.md), [test_v08i_predictive.py](../../constraint-lab/tests/test_v08i_predictive.py), [generation-008i-predictive-round-i0-tables.json](../../constraint-lab/reports/generation-008i-predictive-round-i0-tables.json), [generation-008i-predictive-temporal-information.json](../../constraint-lab/reports/tables/generation-008i-predictive-temporal-information.json)
Coherence: `F8IP-TEMPORAL-INFORMATION-SURVIVES`
Dependencies: CL-T34, CL-T55, CL-T56, CL-T57, CL-T58, CL-F08
Source generations: 008I
Boundary: No generic monotonicity of conditional MI under coarsening conditioning; numerical decimals are not exact irrational expressions.
Notes: Maximum quotient KL gap 1e-160; labelled formula gap 1.62e-158. External rounded values are review checks, not inputs.

## CL-T60: Strong-refinement monotonicity under observation coarsening

**ALGEBRAIC_THEOREM**

For a fixed finite kernel T, Pi_1 finer than Pi_2 implies Ref_T(Pi_1) finer than Ref_T(Pi_2); strong block count cannot increase under deterministic observation coarsening.

Assumptions: Finite homogeneous stochastic T; Deterministic observations on the same Z; Refinement means finer than.
Scope: Prior-free; arbitrary finite probabilities, with Fraction fixtures for exact implementation checks.

Proof: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md#cl-t60). Ref_T(Pi_1) is an eligible strongly lumpable refinement of Pi_2; the coarsest-refinement universal property gives the direction. Idempotence and Ref_T(Pi)<=Pi follow from the same definition.
Evidence: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-PREDICTIVE-REFINEMENT`, `F8K-OBSERVATION-COARSENING-MONOTONICITY`
Dependencies: CL-T52
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T61: General induced strong quotient and commuting ladder

**ALGEBRAIC_THEOREM**

Nested strongly lumpable partitions of one finite chain induce a strong quotient map between their quotient chains, with direct and staged quotient kernels identical.

Assumptions: Same base chain; Both partitions strongly lumpable; Fine partition refines coarse partition.
Scope: Prior-free; no positivity, irreducibility, period or stationary-law requirement.

Proof: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md#cl-t61). Sum fine-target block probabilities within a coarse block; the sum equals the direct coarse row by base strong lumpability, independent of fine source block. Stationary pushforwards then compose.
Evidence: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-PREDICTIVE-REFINEMENT`, `F8K-QUOTIENT-LADDER`
Dependencies: CL-T20
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T62: Strong-block trace implication with strict converse failure

**ALGEBRAIC_THEOREM**

An observation-preserving strong block has identical finite future observed-word laws, but all-word equality need not imply common strong-refinement membership.

Assumptions: Finite homogeneous labelled Markov chain; Deterministic observation; Strong partition refines the observation.
Scope: Known-state future-word equivalence, not causal-state observed-history minimisation.

Proof: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md#cl-t62). Induct on word likelihood functions using equal block sums. The seven-state CE-TRACE has the same B then equal absorbing C/D mixtures from two states, but successor branching separates them under strong refinement.
Evidence: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-TRACE-STRONG-DISTINCTION`
Dependencies: CL-T20
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T63: Synchronization upper bound and supported Markov-order witness

**ALGEBRAIC_THEOREM**

If a strong quotient block is determined by the last s observed symbols on every compatible supported history, observed stationary Markov order is at most s; supported same-(s-1)-suffix row differences give equality for s>=2.

Assumptions: Declared compatible-history law; Worst-case finite suffix synchronization; Stationarity for stationary least-order terminology; First-order means least positive order.
Scope: Conditional finite-past implication also holds without stationarity after the observation window. Converse and state-count bounds are not asserted.

Proof: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md#cl-t63). Condition next output first on the strong quotient state; substitute its deterministic suffix representation. A lower-order law would equate every same-shorter-suffix row, contradicting the witness. CE-WEAK and CE-EVEN refute tempting converses.
Evidence: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-SYNCHRONIZATION-MARKOV-BOUND`
Dependencies: CL-T20, CL-T62
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T64: Finite recursively updated history Markov augmentation

**ALGEBRAIC_THEOREM**

A closed homogeneous event/material law depending only on current finite (X,H), together with a finite recursive update, induces an exact first-order kernel on (X,H).

Assumptions: Finite X,H and event alphabet; Full-past conditional event/material law closes on current (X,H); Declared deterministic or stochastic normalized update.
Scope: Prior-free representation theorem given an initial joint law; not existing-support grammar compilation.

Proof: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md#cl-t64). Sum W(e,x'|x,h) against the update indicator/kernel. Nonnegative rows normalize to one and depend only on current augmented state; iterated conditioning reproduces the joint path law.
Evidence: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-STATE-TAXONOMY`, `F8K-HISTORY-AUGMENTATION`, `F8K-H-L-BOUNDARY`
Dependencies: none
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T65: Finite closed constraint-state kernel flattening

**ALGEBRAIC_THEOREM**

A finite constraint-state process under one fixed meta-programme flattens to a fixed finite kernel on (X,H,eta) when the current product is jointly sufficient and its update homogeneous.

Assumptions: Finite represented coordinates and events; Closed homogeneous joint next-event and update law; All relevant interpreter/driver/clock state included.
Scope: Raw finite-state kernel representation, not automatic ontology-preserving or support-preserving compilation.

Proof: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md#cl-t65). The CL-T64 conditional-update summation applies to the full product. Finiteness or marginal Markovity of eta alone does not ensure the hypothesis; CE-CLOSURE refutes that stronger claim.
Evidence: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-STATE-TAXONOMY`, `F8K-CONSTRAINT-STATE-FLATTENING`, `F8K-H-L-BOUNDARY`, `Q-L-COMPILER-SEMANTICS`
Dependencies: CL-T64
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T66: Preserved ordinary-support obstruction to compilation

**ALGEBRAIC_THEOREM**

A grammar restricted to one preserved ordinary bit flip per unchanged clock tick cannot match a source one-step row assigning positive mass to an ordinary jump of different Hamming distance.

Assumptions: Ordinary coordinates and observation preserved; Exactly one ordinary bit changes per grammar event; Clock preserves one event per target tick.
Scope: Any allowed hidden variables, factors or K/J within this declared support class.

Proof: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md#cl-t66). Every target row has support only at ordinary Hamming distance one. A positive source mass outside that invariant contradicts row equality; CE-SUPPORT retains all single-bit moves and adds a two-bit move.
Evidence: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-COMPILATION-CLASS`
Dependencies: CL-T12
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T67: Stationary one/two-time Markov representation without path equivalence

**ALGEBRAIC_THEOREM**

Any deterministic finite observation of a stationary finite chain has a stationary current-observation Markov kernel matching its one-time and adjacent two-time laws, but not necessarily longer words.

Assumptions: Finite stationary chain mu T=mu; Deterministic observation; Conditional rows defined on positive stationary observation support.
Scope: Prior-dependent representation; zero-mass rows arbitrary. Does not imply weak lumpability.

Proof: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md#cl-t67). Define Q_mu by the stationary adjacent joint divided by pi_Y; row normalization and pi_Y balance follow by summation. CE-EVEN or canonical 8H/8I show a triple mismatch despite matching pairs.
Evidence: [predictive-state-theory.md](../../constraint-lab/formal/predictive-state-theory.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-STATIONARY-WEAK-DISTINCTION`
Dependencies: none
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-M04: Compiler-relative axis-novelty contract

**METHODOLOGICAL_PRINCIPLE**

Axis novelty claims must declare baseline state, support, clock, observation, permitted compiler transformations, grammar/alphabet/K/J budgets, equivalence and priors, and distinguish process, representation, semantic, compression and observational novelty.

Assumptions: A declared source/target modelling task; No unqualified irreducibility claim.
Scope: Permanent methodology, not a theorem of physical ontology or an executed H2/L result.

Argument/next test: Open.
Evidence: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-STATE-TAXONOMY`, `F8K-COMPILATION-CLASS`, `F8K-NOVELTY-TAXONOMY`, `F8K-H-L-BOUNDARY`, `F8K-H2-NEXT-CAPABILITY`, `Q-L-COMPILER-SEMANTICS`, `Q-H2-LAST-PAIR-COMPILER`
Dependencies: CL-M01, CL-T28, CL-T64, CL-T65, CL-T66
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-M05: Scoped explanatory compression discipline

**METHODOLOGICAL_PRINCIPLE**

A small sufficient representation may aid explanation relative to declared predictions and equivalence, but state count, history alphabet/depth, synchronization, order and compilation costs must not be summed or treated as ontology.

Assumptions: Prediction target and equivalence explicit; Costs reported separately.
Scope: Model-design principle; usefulness is not a universal mathematical fact.

Argument/next test: Open.
Evidence: [axis-compilation.md](../../constraint-lab/formal/axis-compilation.md), [generation-008k-predictive-state-synthesis.md](../../constraint-lab/reports/generation-008k-predictive-state-synthesis.md), [test_v08k.py](../../constraint-lab/tests/test_v08k.py), [predictive-state-counterexamples.md](../../constraint-lab/formal/predictive-state-counterexamples.md), [predictive-state-literature-map.md](../../constraint-lab/formal/predictive-state-literature-map.md)
Coherence: `F8K-NOVELTY-TAXONOMY`, `F8K-EXPLANATORY-COMPRESSION`
Dependencies: CL-M03, CL-T52, CL-T60, CL-T63
Source generations: 008K
Boundary: Declared finite representation and equivalence. No physical ontology, unrestricted minimal HMM, or unexecuted H2/L empirical claim.
Notes: Standard mathematics integrated as synthesis, not a mathematical priority claim. Tiny exact proof fixtures are not new laboratory scientific cells. Reserved above all three pinned branch namespaces.

## CL-T68: Same-(X,h1) depth-two divergent futures

**ALGEBRAIC_THEOREM**

The common-start (a,b,c)/(b,a,c) witness has identical complete X, h1 and last two masks, equal positive path probabilities, and different ordinary full/pair rows iff m!=1.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t68). Common-start path calculation and exchanged row coordinates; JS follows from their two-coordinate mixture.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-SAME-X-H1-DIVERGENT-FUTURES`
Dependencies: CL-T64
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T69: Strict semantic H1 non-compilability

**ALGEBRAIC_THEOREM**

For m!=1 no fixed first-order kernel on exactly (X,most-recent pair h1) reproduces all conditioned SECOND-RECENT ordinary rows, independent of positive K/J; unrestricted augmented kernel encoding remains possible.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t69). One represented endpoint requires two unequal rows. Excluded compiler transformations are explicit; no unrestricted augmentation impossibility is claimed.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-H1-NONCOMPILABILITY`, `F8L-DEPTH-NOT-ALPHABET`
Dependencies: CL-T68, CL-M04
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T70: Two-slot exact pair-event closure and Markov sufficiency

**ALGEBRAIC_THEOREM**

Triad-only excursions sum out exactly; the closed recurrent transition is (p,i,j)->(p xor 2^e,e,i) with q_j(e), and the augmented full representation is first-order Markov.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t70). Geometric pair absorption under unit triads preserves both history slots; the finite shifted product state closes.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-PAIR-EVENT-QUOTIENT`, `F8L-H2-MARKOV-SUFFICIENCY`
Dependencies: CL-T30, CL-T64
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T71: SECOND-RECENT uniform stationary joint and period

**ALGEBRAIC_THEOREM**

For every positive m, the 2304-state recurrent pair chain is irreducible with unique uniform stationary law, independent uniform pair/history marginals and period two.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t71). Direct column sums prove uniformity; an XOR-prefix followed by target h2,h1 proves reachability; parity and a diagonal-history two-step return prove period.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-H2-STATIONARY-INVARIANCE`
Dependencies: CL-T70
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T72: Two-round labelled predictive refinement minimality

**ALGEBRAIC_THEOREM**

For positive m!=1, coarsest labelled-mask strong refinement is 64->384->2304 singleton states. Neutral gives 64; all same-mask history pairs are future-distinct non-neutrally, including delayed separation at fixed h2.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t72). Different h2 separates immediate rows; fixed h2/different h1 separates a common positive two-event observed word after register shifting.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-H2-PREDICTIVE-2304`, `F8L-MULTIROUND-REFINEMENT`
Dependencies: CL-T52, CL-T62, CL-T70
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T73: Lag-two slot order and stationary subsequence factorisation

**ALGEBRAIC_THEOREM**

The pair-slot process has stationary order exactly two for m!=1 and is iid uniform at m=1. Under stationary product initialisation even and odd subsequences are independent six-slot first-order chains.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t73). The conditional law reads E_(t-1), same-current/different-previous slots rule out order one; finite path products factor over index parity.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-EVENT-ORDER2`
Dependencies: CL-T71
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T74: Labelled pair-mask exact order three

**ALGEBRAIC_THEOREM**

At stationary pair epochs SECOND-RECENT labelled masks have order exactly three for m!=1 and one neutrally; three masks recover the shifted register and the common-start witness excludes order two.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t74). Consecutive XORs recover h1/h2; supported same-last-two-mask histories have unequal next rows.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-PAIR-MASK-ORDER3`
Dependencies: CL-T63, CL-T68, CL-T70
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T75: Adjacent null and lag-two conditional-information identity

**ALGEBRAIC_THEOREM**

At stationary pair epochs adjacent slots are independent and three-mask CMI is exactly zero, while lag-two slot MI equals four-mask conditional information and is positive iff m!=1.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t75). Exact stationary joint sums give adjacent 1/36 and lagged q_j(e)/6. Mask XOR recovery transports the lagged conditional information; exact triple law equals H0.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-ADJACENT-TEMPORAL-NULL`, `F8L-LAG2-TEMPORAL-MEMORY`
Dependencies: CL-T71, CL-T73, CL-T74
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-T76: Pure graph-shape depth-two witness

**ALGEBRAIC_THEOREM**

At the canonical identical-(X,h1) endpoint, middle/end h2 have equal next edge-count laws but unequal graph-class laws iff m!=1; equal-prior class information equals class-given-count information.

Assumptions: m>0; non-neutral conclusions require m!=1; Fixed SECOND-RECENT, six pair and four triad slots, one common program; Declared semantic compiler, pair-event clock and stationary law where stated.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Proof: [history-depth.md](../../constraint-lab/formal/history-depth.md#cl-t76). Mechanically classified six pair toggles yield the four class rows and common dissolution/formation totals; information chain rule removes the zero count term.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-H2-PURE-SHAPE`
Dependencies: CL-T68, CL-T70
Source generations: 008L
Boundary: No absolute non-Markovianity, arbitrary hidden-model minimality, full-clock order or physical-memory claim. Neutral distinctions collapse.
Notes: Symbolic all-positive-m derivation is separate from the three-grade exact checks and numerical logs.

## CL-F09: Frozen H2-0 exact finite verification

**FINITE_EXHAUSTIVE_RESULT**

Twelve frozen atomic items verify the common-start H2 witness, three 2304-state kernels, non-neutral 64/384/2304 and neutral 64 refinements, exact stationary/null/order certificates and independent word reconstructions.

Assumptions: Committed and pushed H2-0 plan precedes all new N4 non-neutral targets; Palette exactly 1/4,1,4.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Enumeration: Four atomic analysis types times three grades; six generic refinement runs including reverse enumeration; 13824 transitions and 497664 forward quadruple terms per grade; exact count 12. Verifier: [gen008l_exec.py](../../constraint-lab/src/rs_constraint_lab/gen008l_exec.py)
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-H2-PREDICTIVE-2304`, `F8L-MULTIROUND-REFINEMENT`, `F8L-EVENT-ORDER2`, `F8L-PAIR-MASK-ORDER3`, `F8L-ADJACENT-TEMPORAL-NULL`, `F8L-H2-STATIONARY-INVARIANCE`, `F8L-PAIR-EVENT-QUOTIENT`
Dependencies: CL-T68, CL-T69, CL-T70, CL-T71, CL-T72, CL-T73, CL-T74, CL-T75, CL-T76
Source generations: 008L
Boundary: Exact finite verification does not independently prove all-m or physical claims.
Notes: Frozen plan and all full rational item outputs remain durable; raw triad states checked by exact absorption.

## CL-N09: H2 row, shape and lag-two information values

**NUMERICAL_KERNEL_RESULT**

At m=1/4,4, lag-two event MI/four-mask CMI are approximately 0.06751737542833736 and 0.21066571905623145 nats; row/shape JS values are evaluated from exact probabilities with 160-digit natural logs. Neutral and adjacent nulls have separate exact certificates.

Assumptions: Exact rational frozen outputs; 160 decimal digits, natural logarithm.
Scope: N4 O3 independent hypergraph, fixed SECOND-RECENT, H_pair=2, ontology L=0. Temporal/stationary statements use pair-event epochs; full-event claims limited to rows/witness paths. Strict semantic H1 compiler and declared priors.

Method: 160-digit Decimal logarithms from exact joints; closed formulas versus independently enumerated stationary words
Domain: H2-0 palette m=1/4,1,4; full/pair witness rows, local graph shape and pair-epoch lag-two information
Tolerances: `{"information_formula_enumeration_gap": "1e-25", "rational_probabilities": "exact"}`
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-LAG2-TEMPORAL-MEMORY`, `F8L-H2-PURE-SHAPE`
Dependencies: CL-T68, CL-T75, CL-T76
Source generations: 008L
Boundary: Numeric information values are not state counts, memory-depth scores or general monotonicity claims.
Notes: External decimal candidates used only after freeze as checks; maximum information gap below 3e-157.

## CL-M06: Mechanism-matched temporal diagnostics

**METHODOLOGICAL_PRINCIPLE**

Temporal tests should match the declared history mechanism and compiler: one fixed lag or three-time conditional test can be exactly blind to depth-two dependence. This does not prescribe arbitrary-depth searches.

Assumptions: Candidate temporal mechanism and compiler explicit.
Scope: Research methodology informed by SECOND-RECENT's exact adjacent nulls and lag-two effects; not an obligation to test all depths.

Argument/next test: Open.
Evidence: [history-depth.md](../../constraint-lab/formal/history-depth.md), [generation-008l-history-depth-two.md](../../constraint-lab/reports/generation-008l-history-depth-two.md), [generation-008l-h2-0-tables.json](../../constraint-lab/reports/generation-008l-h2-0-tables.json), [history_depth.py](../../constraint-lab/src/rs_constraint_lab/history_depth.py), [test_v08l.py](../../constraint-lab/tests/test_v08l.py)
Coherence: `F8L-TEMPORAL-DIAGNOSTIC-SCOPE`
Dependencies: CL-T75
Source generations: 008L
Boundary: Controller-specific lag-depth alignment is not a general theorem for arbitrary H_pair=d.
Notes: No master memory score or automatic H3 escalation.

