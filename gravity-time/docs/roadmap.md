# Phased experiment programme

Every phase is frozen and pushed before execution. A later phase opens only when an earlier result justifies it, and the reason is recorded in the journey.

## G0 — Relational basin census (this branch)

**Question.** Does any minimal, label-covariant, relation-reading rule template on the O=2 pair grammar produce a stable relational basin, as opposed to density, boundary, combinatorial or clock artefacts?

**Systems.**
- N ∈ {5, 6}.
- Mode HELD: entities {0,1,2} form a held triangle, whose three relations are prohibited from dissolving (declared scaffold). The process starts from that triangle alone and is analysed on its reachable class.
- Mode FREE: no held structure, the full state space, starting from the empty graph.

**Families.** Each family is instantiated over every ordered witness.

| Family | Template | K | Grades | Candidate |
| --- | --- | --- | --- | --- |
| NULL | none | — | — | X-ENTROPIC baseline |
| DENS | `form(a-b) => m` | 1 | 2, 4 | X-DENS control; CL-T18 predicts no relational attraction |
| ADJ | `form(a-b) | present(a-c) => m`, and the same with `present(b-c)` | 2 | 2, 4 | H-D (K2) |
| CLOSE | `form(a-b) | present(a-c) & present(b-c) => m` | 3 | 2, 4 | H-D, H-K3 |
| HOLD | `dissolve(a-b) | present(a-c) & present(b-c) => m` | 3 | 1/2, 1/4 | H-AD |
| LOCK | `dissolve(a-b) | present(a-c) & present(b-c) => prohibit` | 3 | — | H-A |

**Observables.** All are exact and are frozen in the plan:
- recurrent-class and absorbing structure;
- jump-chain and continuous-time stationary laws;
- probe-to-source distance distribution (HELD);
- attachment fraction, the share of present free relations that join a probe to the source (HELD);
- attachment and distance conditional on free-edge count;
- radial drift E[Δd | d];
- clustering (triangle count) conditional on edge count (FREE);
- absorption probability and expected time to absorption where a condition absorbs.

**Discrimination tests.**
1. **Relational attraction beyond density:** the attachment fraction differs from null. DENS must equal null exactly (CL-T18).
2. **Inward drift beyond null:** the radial drift at d ≥ 2 is more negative than under null.
3. **Basin versus capture:** stationary concentration within a recurrent class is distinguished from absorption.
4. **Clock robustness:** a basin statement holds under both the jump-chain and continuous-time stationary laws, or it is flagged as clock-dependent.
5. **K3 versus K2:** whether CLOSE and ADJ give different profiles at matched grades.

## G1 — Relative recurrence rates (temporal); opened only after a G0 basin

**Question (H-U).** In a condition where G0 shows a non-artefact basin, does the same constraint change how often local relations near the source actualise compared with far ones?

**Observables, defined now and frozen only in a G1 plan.**
- The stationary toggle rate of the slots incident to a probe, by distance shell, under both clocks.
- The relative rate ratio between shells. This is clock-free in the sense that both rates are counted on one history.
- The sign and size of the ratio against NULL.

**Discrimination.**
- H-U predicts a rate difference tied to the same rule that makes the basin.
- X-CLOCK predicts that the sign or existence depends on the clock convention.
- T-TENSION is a candidate interpretation of a slowing. It is not assumed.

## G2 — Radial structure and emergent direction

N=7, after a vectorised template kernel is validated against `build_kernel`. Distance shells 1–4.

- Drift and attachment as functions of shell (S-DIST).
- Whether a gradient of tendency defines a direction (S-DIR).
- Whether the profile has any fixed functional form. Matching an inverse-square law is not a target to be fitted.

## G3 — Source dependence and two-body structure

- Basin depth as a function of the held structure's size and shape (triangle, 4-clique, path). This is the analogue of dependence on the source, without any mass primitive.
- Two held structures: whether probes are shared, and whether the structures approach each other in FREE dynamics.
- Escape and transition-enabling dissolution (CL-Q05).

## G4 — Free fall, inertia and conservation analogues

Open. These are defined only if G0–G3 yield a stable, source-dependent, radially structured tendency. The candidates are:
- whether a probe's next-step law depends only on current relations (no inertia at H=0, per CL-T18-type results);
- whether an H>0 velocity-like register is needed;
- which quantities are conserved.

H>0 enters only through the laboratory's compilation test (8G CL-M01, 8H).

## G5 — Unification test

A joint test across phases: a single template family must account for the basin, the radial dependence and the recurrence-rate difference, with no per-phenomenon rule. If no family does, record which phenomena separate.

## E0 — Open-thetical rounds (GT-P002, executed)

Method OTR 1.0. E0A (plan `2e5c97e`) crossed the gradient / non-gradient boundary of the grammar. E0B (plan `50c4b2c`) was chosen from E0A's result: attractive plus non-gradient composites, a PCOMP control and an emergent hub frame. E0C was not run, because the remaining question needs N≥7. Report: `reports/gt-e0-report.md`.

What changed for the phases below:

- **Kinetic convention (GT-Q01)** is demoted. A rule making rate a function of potential presupposes reversibility, and E0 showed that under irreversibility kinetics sets occupancy (OP-6).
- **G2 (radial structure)** stays a candidate. In the gradient class its answer follows from a known potential, so it is informative mainly in non-gradient composites. It needs the same N≥7 kernel as the recommended next step.
- **G3 (source dependence)** stays a candidate. For gradient templates it is predictable from the motif potential.
- **G4 (inertia)** is unchanged. A directed order exists at H=0 for non-gradient rules, so "direction needs history" must be checked against H=0 compilations first.

## Recommended next experiment: E1 — scale test of the handover and of basin–arrow coexistence

1. **Machinery, as a separate commit with its own tests.** A vectorised label-covariant template kernel that computes rates by motif counting instead of per-rule matching. Validate it against `build_kernel` on every E0 cell at N=5 and 6 to 1e-12. Use sparse stationary solves to reach N=7 (HELD 262,144 states; FREE 2,097,152 states, sparse iteration only).
2. **A frozen round at N=7, with the same grades as E0B.**
   - Cells: CSPH and CSPF, CWPH and CWPF, PATHF weak_suppress and PATHH weak_favour, with NULL and CLOSEW controls; HELD first.
   - Questions: Does the CSPH selectivity margin survive (GT-Q07)? Does the handover orientation persist? Does the equal-ratio occupancy gap keep growing? Is the hub-frame arrow still legible?
   - The radial channel (attachment and activity by shell 1–4) comes for free, so G2 is asked in the non-gradient setting.
3. **Stop rule.** If the margin crosses null at N=7, record coexistence as a finite-size effect and do not tune grades.

Alternatives kept open, in order: an O=3 laboratory question (does the single-witness Gibbs theorem extend to triad relations?); the mechanism of local persistence (GT-Q06); a second held structure (G3), only after E1.
