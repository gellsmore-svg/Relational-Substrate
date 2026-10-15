# GT Round E3A — reflection and the E3A → E3B selection

*Prompt GT-P006.*
- *Written after the E3A results (result `595f4a7`, payload `1db9daa0ddff`, frozen plan `ab5f341`), and before any E3B code, plan or cell.*
- *Numbers are from `reports/round-e3a-tables.json`; every cell is in `reports/gt-e3a-atlas.md`.*
- *Layers: [O] observation, [M] mathematics, [RS] interpretation; [P] none; [T] none.*

## 1. What E3A observed

**Validation.**
- 29 of 29 analyses completed: 27 cells (8 on published kernels with new channels, 19 new) and 2 scans.
- Every identity and theorem check held: square identity I1/I2 27/27; support theorems S1 8/8; soft support S2 16/16; rate-symmetric controls S3 4/4; EXCL S4 2/2; scan diagonals S5 2/2.
- Two cells with W16 strong suppression failed the frozen numerical acceptance. They are kept and flagged *numerically qualified*:
  - **FREE N=5 PFD strong+strong (W16).** The law agrees with GTH to 2.6e-10 in L1, just over the 1e-10 tolerance; the law is exactly uniform by theorem, and the uniformity check holds at 1e-9. The fixed-point recovery reference did not converge within its cap, since recovery times reach 17,800 events.
  - **HELD N=5 PF strong (W16).** The recovery reference differs by 7e-8 on values near 270, which is 3e-10 relative, against a frozen tolerance that was absolute.
  - A **post hoc** residual check of both linear solves gives relative residuals near 1e-15 (execution record). The flags stand.

**Findings.**

1. **The hard zero continues the soft formation ladder** [O]. Along path-formation factors 1/2, 1/4, 1/9, 1/16 and 0 (FREE N=5):

   | Factor | Partner index | Flux | Witnessed releases: expected recovery time | Direct-recovery share |
   | --- | --- | --- | --- | --- |
   | 1/2 | 0.072 | 0.11 | 2.24 | 0.49 |
   | 1/4 | 0.104 | 0.18 | 2.82 | 0.25 |
   | 1/9 | 0.112 | 0.21 | 3.16 | 0.11 |
   | 1/16 | 0.111 | 0.22 | 3.27 | 0.06 |
   | 0 (hard) | 0.108 | 0.23 | 3.40 | 0 |

   - The orientation, flux and absence duration of the hard mode lie at the end of the soft ladder; N=4 shows the same pattern.
   - The hard mode differs **qualitatively** only in support: one-way edges, gate distance ≈ 2, and direct recovery exactly 0.
   - No limit is claimed. Positive and zero support are different kinds of chain, but the aggregate observables are continuous in practice.
2. **One-way release's orientation is the σ account with the hard component counted** [O, M sketch].
   - Hard path-form exclusion behaves as path-formation suppression with σ → +∞ on witnessed formations.
   - Adding opposing dissolution (soft σ −log 2, −log 4, −log 16) lowers the partner index from +0.070 to +0.035 to +0.007 (N=5; N=4 similar), but never reverses it.
   - This reinterprets E2B's "counterexample to σ" (GT-F51). It was a counterexample to σ computed over *soft* components only; counting the hard formation ban as unbounded positive σ restores agreement in every E2B and E3A cell.
   - This is an empirical regularity plus a heuristic reading, **not a theorem**.
3. **One-way steps and two-way circulation can pull in opposite directions** [O].
   - With the strongest opposing dissolution (W16), the part of the partner index carried by event pairs containing a one-way step is **negative**: N=4 −0.0026, N=5 −0.0006.
   - The two-way part stays positive: +0.012 and +0.0075.
   - In the plain hard cell, both parts are positive and of similar size (N=5: one-way +0.057, two-way +0.051).
   - So the aggregate can be carried by soft circulation while the hard one-way steps run against it.
4. **Absence persists longer after a witnessed release** [O].
   - In every path-suppressing cell, a relation released while path-witnessed takes longer to come back than one released unwitnessed. Hard cell, N=5: 3.40 against 2.50 time units. Soft 1/16: 3.27 against 2.43.
   - Under NULL the two are equal (1.00), so the difference is the rule, not the structure.
   - Under EXCL witnessed releases are slightly *faster* (1.72 against 1.84), because the closure exclusion acts on other relations.
5. **Two mechanisms of persistent absence** [O].
   - **Gate-limited.** In hard cells, recovery requires breaking a witness first (direct share 0; gate distance ≈ 2).
   - **Rate-limited.** In soft cells, recovery can happen directly, only slowly. The direct share falls from 0.49 to 0.06 down the ladder, so even soft recovery becomes mostly gate-clearing at strong suppression.
   - **Extreme case.** In the saturated soft σ < 0 cell (FREE N=5 PFD weak+strong), absences are rare but last very long once witnessed: 3,174 time units, against 112 unwitnessed. These are metastable holes in a nearly complete graph.
6. **The held source acts as a soft witness too** [O].
   - Under HELD N=5 path-formation suppression, a released attachment takes 18.96 time units to return at factor 1/4, and 259.77 at factor 1/16. A probe–probe relation takes about 1.
   - Recovery of attachments is 100% direct, because the source's own relations cannot be broken.
   - The numbers sit just above 4² = 16 and 16² = 256 (post hoc reading).
7. **GT-Q12 grid: no counterexample** [O]. Over 81 synthetic factor pairs at FREE N=4 (72 judged) and N=5 (56 judged; 16 below the 1e-12 floor, all at saturation), the partner index never disagreed in sign with σ. This is evidence within the grid only.

## 2. Mechanism derived after the results (labelled post hoc) [M]

Finding 6 points to a structural fact. It is derived here and has to be tested, since it was found by reading results.

- **T7 (source-witness floor).** In HELD (source {0,1,2} fixed), every attachment slot (p,s) has exactly two path witnesses lying wholly inside the source: (s, s′, s″) and (s, s″, s′). These are present in every state and never change.
  - So every path component multiplies every attachment's formation rate (path_form) or dissolution rate (path_dissolve) by a constant m².
  - Under suppression m = 1/4 that is 1/16, which matches the observed recovery near 16 + δ.
- **T8 (the floor is orientation-neutral).** A constant factor on all formations (or all dissolutions) of one slot class cancels in every cycle: in any closed cycle each slot is formed as often as it is dissolved, in both directions. So the floor changes **no cycle affinity**, and in particular not the square identity. It changes occupancy only.
  - For σ > 0 families (path_form suppress, path_dissolve favour), the floor acts **against attachment**.
  - For σ < 0 families it acts **toward** attachment.
- **Consequence (conjecture to test).** E1's observation that every arrow-carrying rule with the E0 handover orientation repels probes from the source (GT-F18) may be a **scaffold artefact**. The same σ that sets the handover direction also sets the sign of a constant source-witness bias on attachment.
  - If so, the non-gradient families' failure to gather (GT-F36, B12 on the bridge map) is at least partly produced by the held triangle's internal paths, not by the rules alone.

## 3. What changed in the explanation

| Before E3A | After E3A |
| --- | --- |
| One-way release is a distinct mechanism, unexplained, overriding σ (GT-F51, GT-Q11) | Its orientation, flux and absence durations lie at the extreme of soft formation suppression. Only support topology (one-way edges, gate ≥ 2, zero direct recovery) is qualitatively new. "Override" means the hard ban counts as unbounded σ |
| Recovery: possible (T3), kinetics unknown | Measured: witnessed releases stay absent longer. Two mechanisms, gate-limited and rate-limited; metastable holes in saturated cells |
| The held source as a hard witness (GT-F53) | Also a soft witness, with an exact constant floor (T7). That floor may explain the repulsion of every σ > 0 rule (post hoc; to test) |
| GT-Q12: 36/36 cells | Plus 128 grid points with no counterexample (still no proof) |

**Confounded or representational.**
- The partner index of hard cells mixes one-way and two-way contributions, now separated.
- Absence duration is measured in continuous time, using the cells' own rates. Comparisons across rules mix rate scale and gate structure, so the direct-recovery share is the cleaner discriminator.
- T7 is exact. Its effect on attachment margins is the open quantitative question.

**Lens A (bridge map).**
- P4 (persistent structure) gains a concrete capability: persistent absence with two distinct mechanisms. It is not persistence of an identified object.
- P1 / P8: the reference structure is not neutral, and the source-as-witness may be biasing every source–probe measurement made with path rules. **That makes the B12 → P8 "contradicted" link suspect.** It may be a scaffold result, not a result about the rules.
- P6 / P7 (displacement, acceleration): unchanged. Still not defined.

## 4. Selecting E3B

Candidates were compared factor by factor, with no combined score.

| Candidate | Information value | What it discriminates | Cost | Risk |
| --- | --- | --- | --- | --- |
| **Source-witness neutralisation** (T7/T8): each HELD path family against its counterfactual kernel with the two wholly-internal source witnesses removed from attachment rates | **High.** It decides whether the absence of gathering in path families (GT-F18, GT-F36, B12) is a scaffold artefact. It is directly relevant to the gravity question, and tests a post hoc mechanism with a frozen prediction | Scaffold-induced repulsion against rule-intrinsic repulsion; T8 orientation-neutrality | Low (HELD N=5, 6) | The neutralised kernel is not a grammar rule (it treats source edges specially). It is an *instrument*, not a model, and must be labelled |
| Hard-ban orientation reversal search (larger N, other opposing terms) | Moderate | Whether the extended σ reading ever fails | Moderate–high (N=6 FREE) | Grid-chasing |
| Persistence-of-absence mechanisms (gate- against rate-limited, holding-time distributions) | Moderate | Already largely separated by the E3A direct-recovery share | Low | Little new |
| GT-Q12 symbolic proof at N=4 | Moderate | Proof against counterexample | Uncertain (algebra) | May not close |
| Directed displacement bridge | Low now | No non-circular displacement observable exists | — | Would be premature (bridge map) |

**Choice: E3B tests the source-witness floor.** It follows directly from what E3A revealed, and it bears most directly on the top-down question the programme started with: why the rules that order succession never gather.

**Design principles fixed here, before writing E3B:**
- **Cells.** HELD N=5 and N=6, W4 grades:
  - single path families of both σ signs (path_form weak_suppress and weak_favour; path_dissolve weak_favour and weak_suppress);
  - the E0B/E1 composites CSPH and CWPH;
  - PCOMP (σ = 0, floor on both formation and dissolution);
  - CLOSEW and NULL as controls with no path component.
- **Kernels.** Each cell is computed on its original kernel and on the **neutralised instrument kernel**: attachment rates divided by the floor factor m^(±2) per path component.
- **Frozen identities:**
  - T7: every attachment slot has exactly two wholly-internal source witnesses in every state;
  - T8: every cycle affinity is unchanged by neutralisation (square-identity residual ≤ 1e-12 against the original);
  - controls without path components are unchanged;
  - PCOMP's neutralised law equals its original law.
- **Open, no prediction.** The shift in attachment margins (four forms, both clocks); the handover index; flux; detachment. Does any σ > 0 family gather once the floor is removed?
- **E3B is adaptively chosen** and is not independent confirmation. Held out for a future test: N=7, FREE references, and other source structures.
