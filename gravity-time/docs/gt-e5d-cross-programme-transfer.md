# Candidate transfer note for the Constraint Laboratory (GT-P012, E5D)

*Suggestions only. No CL branch or record was edited. GT and CL share the 8G lineage, so nothing here is independent validation.*

## T-25. Lifting a two-pool projection without symmetrising (for XQ::01)

- **Claim (T16–T19).** A stationary-flux lift on a multi-dimensional projection is stationary under macro-flux conservation alone. It preserves projected circulation, and it is reversible iff no macro current exists.
- **Relevance.** CL's Kpi on (P, h1) is a stationary-conditional kernel. Where CL considers a coarse comparator on a two-component projection, directed fluxes should be kept rather than symmetrised.
- **Scope (eight dimensions):**

  | Dimension | GT | CL |
  | --- | --- | --- |
  | State | graph | (P, h1, h2) |
  | Clock | CT | epochs |
  | Projection | (ℓ, r) counts | (P, h1) |
  | Lift | uniform within cells | conditional on h2 |
  | Transition law | differs | differs |
  | Support | differs | differs |
  | Horizon | differs | differs |
  | Intervention | none | none |
  | Conditioning | stationary | stationary |

## T-26. Finer projections can explain one effect and leave another (methodological)

- **Observation.** In GT, the finer NL projection explained PATHF entirely and PATHH hardly at all.
- **Relevance.** CL residuals against Kpi might likewise split by family when the projection is refined.

## Integration suggestion

Cite plan `c74d896`, results `6749346`, and findings GT-F98 to GT-F103 under CL's own governance.
