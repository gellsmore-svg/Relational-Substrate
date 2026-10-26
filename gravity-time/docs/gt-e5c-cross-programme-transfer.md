# Candidate transfer note for the Constraint Laboratory (GT-P011, E5C)

*Suggestions only. No CL branch, record or file was edited. Earlier notes: T-1 to T-20. GT and CL share the 8G kernel and validator lineage, so nothing here is independent validation.*

## T-21. First-hit conditioning before post-event survival (for CL passage tasks)

- **Claim (T12, GT-F97).** When a functional is measured *after* a stopping event (renewal here; a first return or class entry in CL), the starting law must be the exact first-hit distribution, φ = μ (I − P_BB)⁻¹ P_{B→R}, not the stationary law restricted to the target set.
- **Evidence.** In GT the two laws differed by L1 0.3–1.7.
- **Relevance.** CL first-return and MFPT analyses already use stationary-conditioned sources (CL-T85). Any *post-return* functional would need this conditioning.

## T-22. Counting a subset of events without discarding the rest (for XQ::03)

- **Claim (T13).** If the excluded events cannot end the observed condition, the kernel between counted events is K = (I − P_rem)⁻¹ P_loc. It is exact; dropping the remote events would not be.
- **Contrast with CL.** CL's pair epoch hides triad events, which *can* change the observed material state. The GT construction applies only when the excluded events are provably inert for the stopping condition.

## T-23. Separate reaching from surviving (methodological)

- **Observation (GT-F92).** An unconditional "reach and survive" probability can rise purely because reaching is easier, while conditional survival falls and returns dominate.
- **Relevance.** CL controlled-passage contrasts should report both the reach probability and conditional continuation whenever a two-stage task is defined.

## T-24. Feasibility after the stopping event (T14)

- **Claim.** Structural feasibility must be checked for the post-event task as well as for the event itself. In GT, F_2PATH at N=5 cannot survive one local event after renewal.

## Integration suggestion

Cite the frozen plan `469ee28`, the results commit `5080199` and findings GT-F91 to GT-F97 under the CL catalogue's own governance.
