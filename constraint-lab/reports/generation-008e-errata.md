# Generation 8E: scope qualification

External Review 008E qualifies the historical general-r theorem. The Generation
8E report, its published tables and its immutable snapshot remain unchanged.

The intended statement is: a non-neutral ordinary rule whose r condition literals
refer to r distinct gate variables and are jointly satisfiable contributes an
r-way conjunctive feature and has non-zero top interaction order r over those
variables, on an admissible action and over the independently available gates.

For such literals, the action log multiplier is ln(m) times their product. Its
top raw-gate coefficient is ln(m) times the product of the literal signs. This
coefficient is non-zero when m differs from 1.

The parser accepts `present(T) & absent(T)` on the same triad. This conjunction
is unsatisfiable, never matches and contributes a zero local law, not order 2.
Repeating a satisfiable gate variable also does not introduce a new independent
variable. Consequently syntactic condition count alone cannot establish order.

The E0 census already required two distinct triads and non-neutral W4 grades, so
its 80 local interaction results are unaffected. The historical finding
`F8E-GENERAL-K-INTERACTION` retains its wording and is marked `qualified`.
`F8F-GENERAL-K-SCOPE` supplies the qualification through a `qualifies` relation.

Evidence: `provenance/reviews/008E-chatgpt-review-v0.8e.md` and the historical
`F8E-PARSER-SAME-TRIAD` finding.
