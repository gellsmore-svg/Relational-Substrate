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

1. **Machinery, as a separate commit with its own tests.** *(Done 2026-10-14: `docs/e1-kernel.md`. Bit-exact against `build_kernel` on all E0 cells at N=4–6; HELD N7 solves in about 11 s and FREE N7 in about 150 s. Observable scaling remains.)* A vectorised label-covariant template kernel that computes rates by motif counting instead of per-rule matching. Validate it against `build_kernel` on every E0 cell at N=5 and 6 to 1e-12. Use sparse stationary solves to reach N=7 (HELD 262,144 states; FREE 2,097,152 states, sparse iteration only).
2. **A frozen round at N=7, with the same grades as E0B.**
   - Cells: CSPH and CSPF, CWPH and CWPF, PATHF weak_suppress and PATHH weak_favour, with NULL and CLOSEW controls; HELD first.
   - Questions: Does the CSPH selectivity margin survive (GT-Q07)? Does the handover orientation persist? Does the equal-ratio occupancy gap keep growing? Is the hub-frame arrow still legible?
   - The radial channel (attachment and activity by shell 1–4) comes for free, so G2 is asked in the non-gradient setting.
3. **Stop rule.** If the margin crosses null at N=7, record coexistence as a finite-size effect and do not tune grades.

Alternatives kept open, in order: an O=3 laboratory question (does the single-witness Gibbs theorem extend to triad relations?); the mechanism of local persistence (GT-Q06); a second held structure (G3), only after E1.

## Proposed clarifications to E1 (GT-P003, pending human review)

These proposals leave the E1 text above unchanged. They take effect only if the author adopts them when authorising the E1 freeze. The reasoning is in `docs/e1-scale-confound-audit.md`, and the plain-English summary is in `reports/gt-e1-prefreeze-review.md`.

1. **Status of step 1.** Observable scaling is done (`docs/e1-observables.md`). No E1 plan is frozen, and no E1 cell has been run.
2. **Stop rule, restated.** A null crossing of the CSPH margin at N=7 is a valid observation for that fixed-grade (W4), finite-N model, in the stated clock and standardisation.
   - On its own it does not distinguish intrinsic size dependence from witness amplification, a lower attachment ceiling (r0 falls from 0.75 to 0.667), or a density shift.
   - It is not repaired by tuning a grade or alphabet after the fact.
   - Any follow-up sensitivity test is designed and frozen as a separate round.
   - Fragile or negative outcomes are findings. They are not failures of the wider RS ontology.
   - The words "finite-size effect" are used only once the alternatives above have been examined, not as an automatic label.
3. **Margin forms.** Report the margin raw and null-density standardised, in both clocks, with the normalised form (af − r0)/(1 − r0) and the full a/k profile. On published data the CSPH margin's fragility is specific to the continuous clock (jump: +0.073 → +0.065). At N=6 it is already negative after density standardisation (−0.073 continuous, −0.034 jump). See GT-F34.
4. **Strength control.** Consider the existing W3/W16 sensitivity alphabets at N ≤ 6 as a separately labelled bracket on witness amplification, calibrated on the published N5→N6 step (`docs/e1-design-alternatives.md`, option B).

## E1 status (GT-P004)

The sections above are unchanged.
- **Option B adopted.** The human researcher authorised option B. GT-P004 section 5 states the stop-rule reading, which matches clarification 2 above. All four margin forms were reported side by side, with none primary.
- **Frozen and executed.** The plan was frozen at `4ba2839`. All 32 authorised cells and 16 baseline re-derivations completed, with result commit `730ef32`.
- **Results.** CSPH's coexistence does not survive to N=7, and the handover is invariant. Strengthening is not a good proxy for size. See `reports/gt-e1-report.md`.
- **Recommended next (not executed).** A handover-mechanism investigation (`reports/gt-e1-reflection.md`, section 6). FREE N=7 remains a separate future decision. No further round is opened by GT-P004.

## E2 status (GT-P005)

The sections above are unchanged.
- **E2A** (frozen `1974678`, results `32ac7f6`): a mechanism-diversity atlas of 46 cells.
- **E2B** (frozen `9448f95`, results `ecb3e73`): the hard/soft interface, 18 cells. It was chosen after the E2A reflection (`b90c3ac`).
- **Results.** The handover's local orientation is an identity, A = σ·Δdeg. The aggregate follows σ in 36/36 cells without one-way transitions. σ < 0 reverses the handover. Soft "enabling" is an opportunity effect. Strict enabling needs hard admissibility and is neither necessary nor sufficient for direction. Hard path-form exclusion gives a one-way release mode that overrides σ.
- **Recommended next (not run).** The one-way release mechanism (GT-Q11), with an aggregate-orientation theorem attempt (GT-Q12). Source-structure control gained value; FREE N=7 lost value.
- **Not authorised by GT-P005:** E2C, FREE N=7.

## E3 status (GT-P006)

The sections above are unchanged.
- **Bridge map.** Written before E3A, revised after it (`docs/foundational-bridge-map.md`).
- **E3A** (frozen `ab5f341`, results `595f4a7`): release and recovery.
  - Under hard formation bans nothing is lost, and shortest recovery = 1 + witness hitting set (theorems).
  - The hard ban sits at the end of the soft suppression ladder.
  - Persistence of absence comes in two kinds: gate-limited and rate-limited.
  - No GT-Q12 counterexample on 128 grid points.
- **E3B** (frozen `1bc7c18`, results `1fbaf5a`; chosen after the E3A reflection `1e5ebc3`): the held triangle's internal witnesses impose an exact, orientation-neutral bias against attachment (T7, T8). With it divided out (an instrument), every σ > 0 path family gathers while keeping its arrow.
- **Recommended next (not run).** A covariant source-structure control: a held structure without internal two-paths (GT-Q14). Displacement is still undefined (GT-Q15).
- **Not authorised by GT-P006:** E3C and N=7. Making the scaffold configurable is an architectural change, so it has been requested for authorisation rather than started.

## E4 status (GT-P007)

The sections above are unchanged.
- **Configurable held scaffold.** Implemented: a set of held relations, with the triangle as default and the grammar untouched.
- **E4A** (frozen `f5b3b50`, results `06e5f36`): K2, P3 and K3.
- **E4B** (frozen `9a1c539`, results `64e183f`; chosen after the E4A reflection `8127d24`): the star K1,3 and the path P4.
- **Results.**
  - Floor-guided sorting of attachment within references (robust).
  - Native raw gathering under floor-free references, mostly density composition.
  - The handover orientation is invariant across all five references.
- **Recommended next (not run).** A derivation of floor-guided sorting (GT-Q16), and an architecture review of references (GT-Q17).
- **Not authorised:** E4C and N=7.

## GT-P008 status (consolidation; no experiment)

The sections above are unchanged.
- **Workstream A, sorting mechanism** (`docs/e4-sorting-mechanism-derivation.md`):
  - the floor is an exact odds lever (S2);
  - the first-order index is floor + (7 − N)·held degree, with weak-coupling reversals (S4c);
  - PCOMP sorts per event only (S2b, S6);
  - margins change sign with strength (S7b).
- **Workstream B, reference architecture** (`docs/reference-architecture-review.md`):
  - four regimes;
  - no labelled centre at finite N (R1–R3);
  - an emergent reference needs a persistence definition first.
- **Recommended next (not authorised, not run):**
  - principal: option C, FREE persistence feasibility, with definitions agreed first;
  - fall-back: option B, the floor-reversal test (`docs/gt-p008-next-round-options.md`).
- **No E5 cell was computed.**
