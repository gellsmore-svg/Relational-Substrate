# E1 design alternatives — REVIEW DRAFT, NOT A FROZEN PLAN

Prompt GT-P003, deliverable 5. **This document is not an execution manifest.** No E1 plan has been frozen or pushed, and no E1 cell has been run. The cells, expectations and budgets below are proposals for the author's review. A frozen plan would be generated later as `gravity-time/plans/round-e1-plan.json`, committed and pushed before any cell runs, in the same form as the E0A and E0B plans.

Background: `docs/e1-scale-confound-audit.md` (confounds), `docs/e1-observables.md` (what can be measured), `docs/e1-held-free-feasibility.md` (cost).

## What E0 left uncertain

1. **GT-Q07.** Does CSPH's attachment selectivity, together with its stationary arrow, survive as N grows? On published data it is clock-dependent and density-dependent (GT-F34): the continuous margin is +0.046 → +0.009, the jump margin +0.073 → +0.065, and the null-density-standardised continuous margin +0.023 → −0.073.
2. **Handover persistence.** Does the source-relative handover cycle keep its orientation at N=7? It was invariant across all non-gradient cells at N≤6 (GT-F29).
3. **Equal-ratio gap.** Does the occupancy gap between equal-ratio rules (L1 up to 0.49) keep growing?
4. **Hub-frame legibility in FREE.** Is the FREE-mode arrow still visible relative to the emergent hub?
5. **Radial structure (G2) in a non-gradient setting.** Activity and occupancy by shells 1–4.
6. **The new question this review raised.** How much of any N-dependence is the growing witness load of a fixed grade (audit, sections 2–3)?

## Option A — native fixed-grade scale test, HELD N=7

- **Why.** It asks questions 1, 2, 3 and 5 directly, for the same declared model at a new size. It completes the native sequence N = 5, 6, 7.
- **What varies.** N (7, against the published 5 and 6).
- **What is held fixed.** Families and grades (E0B's W4 grades); the HELD scaffold; the start state (source triangle only); both clocks; the class-free, source-relative and hub frames; and every channel in the validation matrix, plus the additions.
- **Cells (8).** CSPH strong_favour+weak_favour, CSPF strong_favour+weak_suppress, CWPH weak_favour+weak_favour, CWPF weak_favour+weak_suppress, PATHF weak_suppress, PATHH weak_favour, NULL, CLOSEW weak_favour; all HELD N7 under W4.
- **What we would see.**
  - Margins in four forms, plus the a/k profile and the normalised margin.
  - Distance distribution and the detached-probe-count distribution.
  - Shell activity in both clocks.
  - Irreversible flux, entropy production and square affinities.
  - Event-order asymmetry and its top patterns, i.e. the handover.
  - Hub structure and the hub-frame arrow.
  - Class tables (144 permutations) and the Gibbs-projection distance.
  - Autocorrelation times, which are new at this size.
  - The engaged witness census.
- **Informative contrasts.**
  - Handover persists while selectivity vanishes in every form: the arrow and the basin separate further.
  - Selectivity persists in the jump clock only: a kinetic, per-event preference with no time-weighted occupancy advantage.
  - Raw margin positive, standardised margin negative: a sparse-regime preference, as at N6.
  - The handover changes orientation or disappears: a new finite-size regime.
  - A probe-only hub becomes common beyond its null rate (0.108 at N7).
  - None of these: the record says so.
- **Possible artefacts left unresolved.** Witness amplification is only measured (engaged census), not controlled. The fall in source share is confounded with N.
- **Cost.** 8 HELD N7 cells. Measured fixture: 136 s and 450 MB per cell for the full pipeline (NULL; CLOSE strong_favour). Extrapolated scientific cells: 2–6 minutes each (feasibility note), so 15–50 minutes for the eight. A 3× margin gives a cap of about 2.5 hours.
- **What next.** An outcome in which "witness amplification" remains the leading candidate would point to option B's bracket as the next round. A handover change would point to mechanism work (GT-Q06).

## Option B — option A plus a within-grammar strength bracket (recommended)

- **Why.** Question 6. Option A alone cannot say whether an N6→N7 change is what a stronger rule would have done at N6.
- **Added cells.** The six non-NULL families of option A, under the existing sensitivity alphabets W3 (all log-factors × 1.585) and W16 (× 2), at N = 5 and 6, all HELD. That is 6 × 2 × 2 = 24 cells, each at most 4,096 states. NULL is alphabet-invariant and is not repeated.
- **Calibration on a step whose ends are already known.**
  - N5-W16 doubles every log-factor, which exactly matches the path-witness maximum from N5 to N6 (12 × 2 = 24).
  - Comparing N5-W16 with the published N6-W4 tests whether "a stronger rule at the smaller size" reproduces the published N5→N6 changes in margin, flux and handover.
  - The test is declared before running and read in both directions: the bracket may or may not explain the published step.
- **What varies.** N at fixed W4 (native sequence), and the alphabet at fixed N (bracket).
- **What is held fixed.** Grades and orderings (W3 and W16 keep both), the scaffold, the start, the clocks and the channels.
- **What we would see.**
  - For each channel, its strength response at N5 and N6 (W4 → W3 → W16).
  - The N=7 native value, and the N=7 engaged log-weight ratio against N6.
- **Informative contrasts.**
  - The N7 change lies within the strength response at N6, in the same direction, and the engaged-load ratio is in the bracketed range: amplification stays a candidate.
  - The N7 change runs opposite to the strength response: amplification is unlikely to be the main cause.
  - The N5-W16 versus N6-W4 calibration fails: the bracket is a poor model of size change even where both ends are known, and the N7 reading must say so.
- **Possible artefacts left unresolved.**
  - The bracket scales closure and path together, so it cannot reproduce the changed closure/path balance of composites. The single-component families (PATHF, PATHH, CLOSEW) are its clean cases.
  - The W3 and W16 kernels are exact Fractions in `build_kernel` but floats in `gtkernel` (relative error 1e-14).
- **Cost.** Option A plus 24 cells of at most 4,096 states. Each takes under 1 minute including GTH-referee-grade checks (N6 HELD validation: under 50 s with the referee, about 1 s without). That adds under 30 minutes.
- **What next.** It separates "the rule got stronger" from "the system got bigger" as far as the grammar allows. Whatever it finds about witness load is the right input to any later decision about a size-normalised family. Such a family would be a grammar change and an ontology proposal; it is not proposed here.

## Option C — mechanism first, no N=7

- **Why.** If the confounds made an N=7 result uninterpretable, a richer N≤6 study might teach more: component ablations of the handover, density-resolved currents, hub persistence in FREE N6 (autocorrelation is now available there), and the W3/W16 bracket alone.
- **Cost.** Small (minutes).
- **What it gives up.** GT-Q07 and G2 at a new size, which are the questions E0 explicitly left open. It also fails to use the machinery built for N=7.
- **Assessment.** The audit shows that most N=7 confounds can be measured or bracketed (identifiability table, audit section 6). Option C's main advantage therefore does not hold. Its components are better folded into option B (bracket) or kept for a later round (ablations, GT-Q06).

## Option D — option B plus a FREE N=7 tranche

- **Why.** Question 4, and the FREE half of every E0 comparison. HELD cannot answer whether organisation emerges without a scaffold.
- **Cells.** FREE N7 NULL, CSPH, PATHH weak_favour and CLOSEW, all under W4. NULL is rerun inside the frozen round as the identity check, although its values are theorem-fixed.
- **Cost.** Measured fixture (FREE N7 NULL, full pipeline): 25 minutes and 3.2 GB. Extrapolated design cells: 30–80 minutes each, so 2–5 hours for the four, run one at a time (`docs/e1-held-free-feasibility.md`).
- **Assessment.** Feasible on this machine within one sitting. It is the only route to the question of unscaffolded emergence at N=7. The cost risk is the iteration-count extrapolation, which is bounded by the cap and the unresolved-cell rule. Two FREE cells at once would fit in memory, but with little margin.

## Recommendation

Option B, with HELD N=7 first. It answers the open E0 questions at a new size. It is the only option that can say anything about effective rule strength, and it does so with instruments the grammar already has. It is expected to take about 1–1.5 hours of computation for HELD and the bracket together.

The FREE tranche (option D) is recommended as a second tranche of the same frozen round, run after HELD under its own 6-hour cap, if several hours of computation are acceptable to the author. Otherwise defer it to a FREE-only round, and take a first look at hub persistence at N=6, where it is now computable in seconds.

Under OTR the choice rests on discrimination, not on the chance of a gravitational-looking result.
- Option B produces several outcome patterns that would each change the next round: arrow without basin, kinetic-only selectivity, sparse-regime selectivity, amplification-explained change, or a new pattern.
- It keeps the negative and fragile channels visible: detachment, standardised margins, null hub rates.
- It removes nothing from the published E0 comparison set.

## Proposed frozen elements (for the plan, if authorised)

**Frozen expectations** (identities and structural theorems only; no expected sign for any margin):
- **Z1 — NULL.** At HELD N7, π is uniform (L1 to uniform ≤ 1e-9); irreversible flux ≤ 1e-9; both margins |·| ≤ 1e-9 in both clocks.
- **Z2 — Gradient control.** CLOSEW at every N and alphabet follows its predicted triple-Gibbs law (L1 ≤ 1e-9) and is reversible.
- **Z3 — Non-gradient rates.** Every CSPH, CSPF, CWPH, CWPF, PATHF and PATHH cell has maximum square affinity > 1e-6. Stationary flux is not predicted (saturation can separate them, E0A X4).
- **Z4 — Replication.** The N5 and N6 W4 values of every option-A family are re-derived by `gtobs` and agree with the published tables within the validation tolerances. Differences are allowed only where the referee shows E0 wrong (section 3 of the validation note).
- **Z5 — Solver.** Every cell resolves: residual ≤ 1e-12, two starts agree within 1e-10 L1, autocorrelation series below 1e-13 relative without the cap. A cell that fails is reported unresolved, not estimated.

**Open questions without prediction:** GT-Q07, handover orientation at N7, the equal-ratio gap, shell structure, hub-frame legibility (if FREE is included), engaged witness ratio, bracket calibration.

**Stop conditions:** a solver failure in a cell (recorded, round continues); the wall cap (proposed 4 h for HELD with the bracket, plus the FREE tranche if included); no grade, alphabet or threshold change after the freeze.

**Pre-freeze exposure to declare:**
- HELD N7 PATHF weak_suppress chain built for timing (E1 kernel step; no law computed).
- Theorem-fixed fixtures run in GT-P003: HELD and FREE N7 NULL, HELD and FREE N7 CLOSE strong_favour. Costs and solver checks only; CLOSE is not a proposed cell.
- Post hoc channels on published N5/N6 cells: engaged witness census, margin decomposition, hub structure.
- The NULL baselines at N7 (uniform law, theorem).
