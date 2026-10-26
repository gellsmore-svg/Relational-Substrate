# Candidate transfer note for the Constraint Laboratory (GT-P010, E5B)

*Suggestions only. No laboratory record, branch or file was edited or cherry-picked, and the central synthesis on `main` was not modified (see `gt-p010-shared-synthesis-handoff.md`).*
- *GT results are in the O=2 single-pair-toggle grammar at FREE N = 5, 6.*
- *Earlier notes: T-1 to T-16.*
- *Pinned CL reference for comparison: `e650d71` (008N, closed, unreviewed).*

## T-17. A layer-traffic comparator: the stationary-conditional projection onto a count (for CL-Q05, XQ::01)

- **Claim (T11, proved).**
  - NK sets b_k = J[k,k+1] / ((M−k) p_k) and d_{k+1} = J[k,k+1] / ((k+1) p_{k+1}), where J[k,k+1] is the target's stationary upward flux across the cut between counts k and k+1.
  - NK is reversible and covariant, with law p_|x| / C(M,|x|).
  - It matches the count profile, every adjacent-layer flux, E[q | k], the mean rate and the jump-clock profile. It does not match within-layer arrangement.
- **Relation to CL.** CL's Kpi (CL-T85, CL-T89) is the stationary-conditional kernel on a projected state (P, h1). NK is its GT analogue on the projection "edge count", lifted uniformly within each layer.
- **Transfer conditions.**
  - Single toggles, so the count changes by ±1.
  - A positive stationary law.
  - CL's projection drops a hidden history coordinate at event epochs, which NK does not do. Do not call NK a matched-source control.
- **Evidence.** In GT, NK removed PCOMP's ×25 apparent persistence against ND entirely, and most of CLOSEW's (GT-F83, GT-F85).

## T-18. Replacement as a hitting functional, with a feasibility theorem first (for CL-Q03, XQ::04)

- **Claim.**
  - Complete renewal (reach a state where the property holds and no entry participant takes part, before exit) is a hitting probability on the killed jump chain.
  - It needs no rule to read the observer: the 8G gate is not engaged.
  - Feasibility must be decided first (T10). Otherwise a structurally impossible renewal reads like a dynamical zero.
- **Caveat.** For single-participant entry sets, renewal equals departure and can be met by a single toggle (GT-F87).

## T-19. Projection choice outweighs clock choice for persistence classifications (methodological)

- **Observation.** Between ND and NK, 28 of 90 lifetime classifications changed, in both directions. Across the CT, jump and anchor-local counts, only 3 of 30 rows disagreed (GT-F89).
- **Relevance.** CL passage and persistence contrasts should state the projection their control matches before comparing clocks.

## T-20. What does not transfer as is

- **The anchor-local event count.** CL's clocks are event epochs in which triad events are hidden. A local count there would need its own definition and a time-change argument (XQ::03).
- **E5B magnitudes.** These are properties of GT's W4 templates at N ≤ 6.

## Integration suggestion

Any adopted item should enter the laboratory's catalogue under its own governance, citing:
- the frozen plan `fc3ec7d` and the results commit `fcb17ae`;
- findings GT-F83 to GT-F90;
- GT and CL share the 8G kernel and validator lineage, so this is not independent validation.
