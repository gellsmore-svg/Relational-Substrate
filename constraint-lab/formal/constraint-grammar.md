# Constraint grammar

## 1. State and event space

For N labelled entities, O=2 contains one bit for each unordered pair; O=3 appends one bit for each unordered triad. Slots are lexicographic pairs followed by lexicographic triads. At N=4, D=6+4=10 and there are 1024 full states. Independent hypergraph means no simplicial face-closure condition, not statistical independence of event histories.

A baseline event toggles exactly one relation bit. There is one candidate event per slot in every state, interpreted as form if absent and dissolve if present. O>3 is not implemented. Fixed current-state semantics here have G=S=H=L=0.

## 2. Constraint syntax

In the literal fragment:

```text
direction ::= form | dissolve
literal   ::= present(relation) | absent(relation)
rule      ::= direction(action_relation) [| literal (& literal)*] => factor_name
collection ::= rule occurrences
```

Both pair and triad actions and conditions are accepted at O=3. Conditions may name any other relation slot, but not the action itself. Direction already tests the action bit. Literal ordering is canonicalised. Identical repeated literals are rejected; contradictory literals on the same relation are accepted and never match.

The full O=2 DSL also admits a single count predicate (count >=, <= or == threshold). The O=3 parser rejects count predicates. Parser tokens name factors; the kernel looks their values up in a factor map. The standard experiment specification restricts factor names to its finite alphabet, whereas the parser itself does not.

## 3. Weight semantics

Let \(\phi_i(x,e)\) be 1 exactly when event, direction guard and all conditions of rule i match. With the implemented slot-constant baseline weights \(b_e>0\) and positive multipliers:

\[
w(e\mid x,\mathcal C)=b_e\prod_{i=1}^J m_i^{\phi_i(x,e)}.
\]

The unnormalised full-event law is divided by the sum over all D candidate slots. All integrated single-action formulas take baseline weights to be 1.

Zero prohibit is supported elsewhere in the DSL but excluded from positive-log algebra, full-support irreducibility and expressivity theorems. If all event weights vanish, the implementation records deadlock and completes the Markov kernel with a self-loop; that completion is not a relational event.

## 4. Logit representation

\[
\ell_e(x)=\log b_e+\sum_i \lambda_i\phi_i(x,e),\qquad \lambda_i=\log m_i.
\]

This additive expression is a model-level meaning of 'constraints as language': syntax selects features, semantics assigns log weights, composition sums features, and interpretation produces transitions. Probabilities are not additive because normalisation couples all event slots.

Full q equality permits a common state-dependent weight scale. In the one-action analyses the other slots are fixed to unit weights, removing that gauge ambiguity.

## 5. Expression complexity

The implemented count is K=1+number of literal tokens+number of count predicates. A non-neutral, satisfiable conjunction of r distinct raw Boolean gates contributes degree r, with K=r+1 in the literal fragment. Syntactic K does not guarantee degree: contradictions vanish, cancellations can remove top coefficients, and count predicates may read several bits with one token.

## 6. Rule cardinality

J counts simultaneous occurrences. Multiplication is commutative, but it is not idempotent: repeating a matching rule squares its multiplier. The backend accepts repeated occurrences. Historical primary censuses use distinct labelled sets with a structurally simple normal form excluding repeated action/condition identity even at different grades.

Increasing J at fixed primitive feature family sums more terms from that family. It cannot create a new log-weight monomial outside the family's span. It can still cause nonlinear probability and global observable effects.

## 7. Boolean feature hierarchy

Every real table on r Boolean gates has a unique multilinear expansion. Conjunction monomials of degrees 0 through r supply a basis; complete literal corners supply another. Increasing maximum K makes higher-degree individual features available, subject to parser scope and alphabet. See [derivations](derivations.md).

This is local log-weight expressivity, not arbitrary transition-support universality.

## 8. Equivalence notions

Canonical syntax, weight tables, normalised event laws, full kernels, conjugate kernels and declared projected processes are different objects. Aggregate statistic equality is weaker still. [Equivalences](equivalences.md) states the hierarchy and its clock/initial-prior requirements.

## 9. Symmetry

Vertex permutations relabel both states and rules. For a fixed labelled rule collection, only actual kernel automorphisms are symmetry quotients. Independent hidden-bit permutations can preserve a law while failing to preserve vertex incidence. Visible graph isomorphism alone need not define a Markov quotient.

## 10. Local-to-global pipeline

Syntax -> active features -> event log weights -> normalised probabilities -> kernel -> clocked dynamics -> state distribution -> projection -> statistic.

No topology creates a missing local log-weight monomial. Normalisation and dynamics can nevertheless transform how it becomes observable. The mechanism audit is in [local-to-global](local-to-global.md).

## 11. Projection hierarchy

Labelled pair mask -> graph isomorphism class -> edge count are nested deterministic projections. Their law-label information has an exact chain decomposition. Projection can erase distinctions and need not preserve Markov structure.

## 12. Memory versus current efficacy

A current hidden gate can affect the next event even when its initial value is no longer discriminable in a later visible graph. Hidden current-state dependence is not H>0. Full-event and next-pair-event clocks must be distinguished.

## 13. Boundaries of current-state grammar

The unbounded literal parser plus arbitrary positive factor map can construct every positive event-weight table on its fixed single-bit-toggle support, using direction to encode the action bit and conditions for all other bits. The bounded experiment runner cannot be silently identified with this larger representation core.

This gives neither arbitrary transition support nor different futures for identical complete current states under one fixed rule collection. Finite W4 coverage is separate from continuous algebraic completeness.

## 14. Open axes H and L

H asks for dependence on different histories ending at the same complete current material state. L asks for dynamical constraint-state configurations under a common program, not merely two different static rule sets. Either may become ordinary Markov state after augmentation; such augmentation changes the representation and must preserve the declared clock/support if claimed equivalent.

## 15. Scope and non-claims

All theorems specify finite state space, positive factors, feature fragment and clock. Numerical results retain their original domain and tolerance. There is no claim of physical spacetime emergence, ultimate receiver, design, theology, or nature implementing this DSL. Book changes are deferred to explicit later work.
