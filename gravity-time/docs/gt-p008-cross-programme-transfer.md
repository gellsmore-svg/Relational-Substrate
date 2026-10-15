# Candidate transfer note for the Constraint Laboratory (GT-P008)

*These are suggestions only. No laboratory record, branch or file was edited or cherry-picked.*
- *GT results are in the O=2 single-pair-toggle grammar.*
- *Where a proof transfers, its conditions are stated. Otherwise the item is methodological.*
- *Earlier GT notes: `e3-cross-programme-transfer.md` (T-1 to T-4) and `e4-cross-programme-transfer.md` (T-5 to T-7).*

## T-8. Stationary balance and exact factor accounting (for CL-Q04): a theorem with stated conditions

- **Claim.** For any finite irreducible single-toggle chain whose toggle rates do not read the toggled slot itself:
  - E_π[(1 − x_e)F_e] = E_π[x_e D_e];
  - hence occ/(1 − occ) = E[F_e | x_e = 0] / E[D_e | x_e = 1].
- **Consequence.** A state-independent factor on a slot's formation (or dissolution) enters its stationary odds exactly. Everything else enters through conditional means that depend on the whole law.
- **Transfer conditions.** The proof uses only these two hypotheses (single toggles; rates independent of the toggled slot). It applies to O=3 pair and triad slots if the laboratory's templates satisfy them. The laboratory should check this for each template family before citing it.
- **Provenance.** `gravity-time/docs/e4-sorting-mechanism-derivation.md` S1 and S2. Verified on random rates and on published GT tables to 2e-14.

## T-9. First-order laws around a uniform reference (for CL-Q04): a theorem with conditions

- **Claim.** If every base rate is 1, so that the reference law is uniform, the first-order stationary correction depends only on the first-order log rate ratios.
  - Two rule sets with equal local ratios therefore share their continuous-time law to first order.
  - They differ at first order in the per-event clock.
- **Transfer conditions.** Uniform base rates. The laboratory's non-uniform baseline weights (for example, ρ3 sensitivity runs) change the reference law, so the statement must be re-derived with that law in place of the uniform one.
- **Provenance.** Derivation S5 and S6. Verified at N=4 with synthetic factors.

## T-10. Persistence as a ratio of time scales; exchangeability limits (for CL-Q05): methodological plus a short proposition

- **Claim.**
  - In a finite, label-covariant, irreducible model, no labelled structure can persist indefinitely, and every vertex has identical stationary statistics (R1, R2).
  - Unbounded persistence needs imposition, a loss of irreducibility (frozen-in classes), or a limit with diverging lifetimes (R3).
  - So "a structure that persists" is quantified by a lifetime-to-turnover ratio Λ against a matched-density null, in each clock.
- **Relevance to CL-Q05.**
  - The laboratory's passage and committor tools (`passage.py`) compute the first-passage quantities that Λ needs.
  - Controlled-fragility contrasts could report Λ for the source class instead of, or beside, occupancy.
- **Provenance.** `gravity-time/docs/reference-architecture-review.md` §2 and §3.2.

## T-11. Identity tracking does not by itself call for a history axis (for CL-Q03 and the 8G gate): methodological

- **Claim.**
  - Tracking which structure is "the same" across events is an observable on trajectories (pairs of consecutive states). The dynamics does not read it, so it raises no expressivity question.
  - A history register becomes relevant only if the *rules* must respond to identity beyond the full current state. The laboratory's same-full-current-state history witness is then the right first test.
- **Provenance.** Architecture review §3.3 and §3.10.

## T-12. Sorting is not monotone in a structure's support (for CL-Q04): theorem plus observation

- **Claim.**
  - Under the GT path families at first order, a held structure favours attachment by an index combining permanent support (floor) and held degree. Explicit structures exist where the more-supported site is favoured (S4c).
  - At W4 strength, the floor's exact lever plus a reinforcing residue dominate in the tested P3 and star cases.
- **Relevance.** If the laboratory compares sources of different internal structure, support counts alone are not a sufficient summary.
- **Provenance.** Derivation S4b, S4c and §4; secondary analyses §2 and §6.

## Integration suggestion

Any adopted item should enter the laboratory's own catalogue under its governance, with GT provenance: file, commit and finding ID (GT-F67 to GT-F72; see `gravity-time/coherence/current-map.md`).
