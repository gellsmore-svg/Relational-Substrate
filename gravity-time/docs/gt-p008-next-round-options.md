# Next-round options after GT-P008 (proposals only)

*GT-P008, deliverable 5. Written 2026-10-15.*
- *Nothing here is frozen, hashed or executed. There is no E5 data.*
- *Each candidate would need a separate human authorisation, then a frozen and pushed plan, before any cell is computed (8G discipline).*
- *Costs are estimated from published cell timings (E0A FREE N=6: build ≈ 4 s, stationary ≈ 0.4 s, 32,768 states; E4 HELD N=6: ≈ 2 min including all channels).*

## What the options must respond to

From the derivation (`docs/e4-sorting-mechanism-derivation.md`):
- The floor is an exact local lever (S2).
- The first-order sorting index is floor + (7 − N)·(held degree) (S4b). It predicts within-reference signs at W4 post hoc (16/16) but implies weak-coupling reversals of the floor order (S4c).
- Overall margins change sign between weak and W4 strength (S7b).
- PATHF and PATHH differ only at second order (S5).
- The residue's reinforcing sign is explained only by a conjectured feedback (C1).

From the architecture review (`docs/reference-architecture-review.md`):
- An emergent reference at finite N can only be metastable (R1–R3).
- The first missing piece is a **definition**: a grammar-generated motif predicate with a lifetime ratio Λ against NULL, in both clocks. It needs no new machinery.

## Candidates

### A. Strength continuation on published geometries (mechanism, Workstream A)

- **Design.**
  - Scaffolds K3, P3, S4, P4 at HELD N = 5, 6 (as published).
  - PATHF, PATHH, CSPH, with factors e^(g·ε) on a frozen grid ε ∈ ln 2·{⅛, ¼, ½, ¾} (ε = ln 2 is published and not recomputed).
  - Measure the orbit log-odds contrasts in both clocks, the raw and standardised margins, and the exact residue (S2) per orbit.
- **Questions.**
  - Where does the first-order index stop predicting magnitudes?
  - Where does the K3 N=5 margin cross zero (S7b)?
  - Does the PATHF/PATHH split grow as ε² (S5)?
  - When does the residue change sign?
- **Work.** About 4 scaffolds × 2 sizes × 3 families × 4 strengths: about 80 cells, roughly 1–2 h on 4 workers. It is a **grade sweep**, which GT-P008 excludes without separate authorisation.

### B. Floor-reversal test on purpose-built held graphs (mechanism, sharp falsification)

- **Design.**
  - The connected held graph G* = {01, 02, 03, 12, 14}, and one other reversal case from S4c ({01, 02, 03, 04, 12, 13}), at HELD N = 6. Each has 5 source vertices, 1 probe and 10 free slots, so 1,024 states.
  - PATHF, PATHH, CSPH, NULL, CLOSEW and PCOMP at W4, plus one weak strength (ε = ln 2/8) to confirm the first-order sign.
- **Question.** At W4, does the **higher-floor** vertex out-attract the lower-floor one, as the first-order index predicts? This tests C2.
- **Work.** About 24 cells of 1,024 states each: seconds per cell, under 10 minutes in total. It needs two new scaffold presets (configuration, not grammar).

### C. FREE persistence feasibility (architecture, Workstream B): **recommended**

- **Design (to be frozen only after human approval of the definitions).**
  - FREE N = 5, 6 under the published families NULL, PATHF ws, PATHH wf, CSPH, CLOSEW and PCOMP; FREE has no scaffold.
  - Declared motif predicates, as candidates for human selection:
    - P_tri: A is a triangle;
    - P_star: A = centre plus three leaves, all present;
    - P_2p: A is a two-path.
  - For one representative instance per S_N-orbit (sufficient by R1), compute **exactly**, from the generator, in both clocks:
    - the mean lifetime: first passage from P(A) to not-P(A);
    - the mean recurrence time;
    - the mean constituent turnover time;
    - Λ = lifetime / turnover;
    - the NULL Λ at matched density (the same predicate, with NULL rates reweighted to the cell's density profile, defined before freezing).
  - **Controls:**
    - (i) NULL;
    - (ii) the lagged hub frame: select the max-degree vertex at t, measure its degree and attachment at t + Δ for declared Δ, against a random vertex;
    - (iii) PCOMP, whose continuous law is uniform but whose kinetics differ.
- **Questions.**
  - Does any σ > 0 or closure family maintain a motif beyond its parts (Λ above NULL's at matched density)?
  - Does the instantaneous hub persist beyond selection?
  - Does Λ rise from N = 5 to 6? That is a trend only; no symmetry-breaking claim is possible (R3c).
- **Work.**
  - About 2 sizes × 6 families × 3 predicates: 36 exact lifetime computations.
  - Each is a sparse linear solve on ≤ 32,768 states (seconds).
  - Kernel builds ≈ 4 s each; under 30 minutes in total. Memory < 1 GB.

### D. Second-order theory (pure mathematics; no computation)

- **Design.** Expand π_ε to second order around the uniform law in the Walsh basis, where 𝓛_0 is diagonal. Derive:
  - the PATHF − PATHH occupancy split (S5 says it starts at ε²);
  - the second-order residue;
  - the exact-zero slopes (P3 N=5, K3 N=6 and star N=6 margins).
- **Work.** Analysis only, with N=4 synthetic fixtures. **Allowed under the current mandate type** (it is a consolidation), but not started here.

### E. Larger N (not recommended now)

N = 7 under K2 or the star (the size dependence of raw gathering). No mechanism-specific observable requires it yet, and E1 showed that size can reverse the sign of margins (GT-F36).

### F. No experiment: improve definitions first

Write and review the motif, identity and lifetime definitions for C as a document. Freeze nothing until the definitions are accepted.

## Comparison (no combined score)

| | A. Strength continuation | B. Floor reversal | C. FREE persistence | D. Second-order theory | F. Definitions first |
| --- | --- | --- | --- | --- | --- |
| **Information value** | Moderate: maps where first order fails and where K3 suppression appears | High per cell: one sharp yes/no on floor-only against index | High for Lens A: first evidence on whether the grammar maintains anything without imposition | Moderate: closes S5 and the residue analytically | Low alone; enabling |
| **Plausible outcomes** | Smooth departure from first order; a sign change located; residue sign change located | Index wins (C2 survives, floor-only refuted at W4); floor wins (C2 refuted, feedback dominates); tie | Λ ≈ NULL for every family (a null: no endogenous reference at N ≤ 6); Λ > NULL for closure families only (persistence by potential, GT-F05); Λ > NULL for σ > 0 families (persistence with an arrow) | Closed forms, or an intractable expansion | Agreed definitions |
| **Mechanism novelty** | Low (extends E4) | Moderate (tests a derived prediction) | High (new regime) | Moderate | — |
| **Artefact discrimination** | Good for strength artefacts; none for reference artefacts | Good: within-cell and within-reference, but still held | Good if matched-density NULL Λ and the lagged hub control are frozen; risk of predicate choice | Exact | — |
| **Interpretability** | Clear | Clear but narrow: 1 probe, a special graph | Clear if Λ is the only primary quantity | Technical | — |
| **Cost / memory / risk** | 1–2 h; a grade sweep (needs authorisation) | Minutes; new presets | Under 30 min; < 1 GB; the main risk is definitional | Analyst time | Low |
| **Cross-programme relevance** | Low | CL-Q04 (incidence-sensitive coupling) | **CL-Q05** (persistence, passage); CL-Q03 (does identity need history? no, as long as it is tracked) | CL-Q04 | CL-Q03 |
| **Impact on the two-lens gap map** | Bottom-up only | Bottom-up only | Opens the first top-down prerequisite (a metastable reference) | Bottom-up only | Prepares C |

## Recommendation

- **Principal: C, FREE persistence feasibility, preceded by a short definition review (F).**
  - The governing question asks what a system must be capable of before a held reference can be replaced. The architecture review shows the first such capability is metastable persistence of a grammar-generated motif: measurable now, exactly, at N ≤ 6, in both clocks, with no new machinery.
  - The null outcome (no family maintains anything beyond NULL) is informative. It would say that held references are not stand-ins for anything these rules produce, and that held-reference sorting results should not be carried over to emergent references.
- **Fall-back: B, the floor-reversal test.** If the human researcher prefers to close Workstream A first, B is the cheapest decisive test. It falsifies either the floor-only reading or conjecture C2 within minutes of computation.
- **D can proceed in any later consolidation** without an experiment.
- **A and E are not recommended now.**

## Human decision gates

1. **Choose:** C (with F first), B, D, or none.
2. **If C:** approve the motif predicates (P_tri, P_star, P_2p, or others), the matched-density NULL construction for Λ, the lag set Δ for the hub control, the threshold language ("Λ above NULL" only, with no tuned cut-off), the families and sizes (FREE N = 5, 6; no N = 7).
3. **If B:** approve the two new presets and the weak-strength confirmation point.
4. **In all cases:** an authorising prompt, a pushed frozen plan, and execution only after the freeze. Stop after one round for review.

## Not proposed

New primitives; history or meta axes; source-labelled rules; N = 7; grade sweeps beyond A's four points (if authorised); multi-source dynamics.
