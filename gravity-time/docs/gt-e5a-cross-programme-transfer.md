# Candidate transfer note for the Constraint Laboratory (GT-P009, E5A)

*These are suggestions only. No laboratory record, branch or file was edited or cherry-picked.*
- *GT results are in the O=2 single-pair-toggle grammar at FREE N = 5, 6.*
- *Earlier GT notes: T-1 to T-12 (`e3-`, `e4-`, `gt-p008-cross-programme-transfer.md`).*

## T-13. Stationary-flux episode lifetimes (for CL-Q05): exact, cheap, and checkable

- **Claim.** For any finite ergodic CTMC and any set A of states, the mean entrance-episode lifetime is π(A)/J_A, where J_A is the stationary boundary flux (entry flux = exit flux). In jump counts it is E_π[q 1_A]/J_A.
  - No first-passage inversion is needed.
  - The killed-chain solve gives an independent check, which agreed within 2.6×10^−10 on 144 E5A cases.
- **Relevance.** Persistence and passage contrasts in the laboratory (`passage.py`) can report entrance-episode lifetimes beside occupancy.
- **Do not confuse with residual life.** The occupation-sampled residual life is a different quantity: by Palm inversion it is E[L²]/(2E[L]) ≥ L/2.
- **Provenance.** `gravity-time/docs/e5-definitions-and-null-construction.md` T1–T2; findings GT-F74 to GT-F82.

## T-14. A comparator that matches density and mean rate is not a kinetic control (for CL-Q05): observation plus identity

- **Claim.**
  - In an exchangeable chain at matched density, matching the mean event rate forces the average edge lifetime to match (E[q] = 2M·J_edge; post hoc identity, GT-F79).
  - Even so, the GT equal-ratio family PCOMP has NULL's stationary law, yet its flexible-pattern lifetimes are up to 25 times those of such a comparator (GT-F78).
- **Relevance.** If the laboratory measures fragility or persistence against a "matched null", it should declare the null's rates and check whether lifetimes differ because of where activity sits.
- **Provenance.** `gravity-time/reports/gt-e5a-reflection.md` §3–§4.

## T-15. Fixed relation sets cannot persist through replacement; formation-only rules fix their lifetime (for CL-Q05): theorem

- **Claim.**
  - A predicate that requires a fixed set of relations has zero within-episode turnover of those relations (T4).
  - Under rules acting only on formation, with unit dissolution rates, its continuous-time lifetime is exactly 1/r for r required relations (GT-F75).
- **Transfer conditions.** Single-toggle chains, and dissolution rates independent of the state for the formation-only part. The laboratory should check both for its templates before citing this.

## T-16. Identity tracking still needs no history axis (for CL-Q03 and the 8G gate): methodological

- **Claim.** Everything E5A measured, and the proposed replacement-completion measure, are read-only observables on trajectories. Nothing suggests that rules must read history. The 8G compilation gate is not engaged.
- **Provenance.** Reflection §8; definitions §8.

## Integration suggestion

Any adopted item should enter the laboratory's own catalogue under its governance, citing:
- GT file paths;
- the frozen plan commit `1dc43c6` and result commit `59eb682`;
- finding IDs GT-F74 to GT-F82.
