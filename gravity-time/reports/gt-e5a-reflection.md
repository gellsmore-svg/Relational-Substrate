# GT-E5A reflection: persistence, turnover and the comparator problem

*GT-P009 Phase 5. Written after the frozen round: plan `1dc43c6`, results `59eb682`.*
- *Labels:*
  - **[T]** theorem (finite model, with proof);
  - **[O]** observation of the frozen round;
  - **[P]** post hoc (derived or noticed after seeing results, checked on the published tables);
  - **[C]** conjecture;
  - **[RS]** separate interpretive layer.
- *Numbers come from `reports/round-e5a-tables.json` and `gt-e5a-atlas.md`.*

## 1. Do intact motifs, flexible organisations and selected hubs persist in different ways?

Yes. They are three distinct kinds.

| Kind | What persists | What the round shows |
| --- | --- | --- |
| Intact motif | A fixed labelled set of relations | [T4] It cannot persist through replacement of its own relations. Every exit is a required-edge dissolution. [O] In CT it outlives ND in 1/30 rows: the PATHH star, ×1.004 at N=5 and ×1.093 at N=6. JT lengths exceed ND in 22/30, but JT is not density-matched for most families (§3) |
| Flexible anchored organisation | A labelled anchor's property (a closing link, a degree threshold) while partners change | [O] Outlives ND in both clocks in 18/30 rows, and has Ω above ND in 28/30. **The largest effects come from PCOMP (no structural preference) and CLOSEW (near-certain prevalence)**, so they are qualified (§2) |
| Selected hub | The degree advantage of a vertex chosen once | [O] Decays toward zero everywhere ([T8]). It is slower than ND in both clocks under PATHF, PATHH and CSPH, and faster than ND in JT under CLOSEW and PCOMP |

## 2. Survival through turnover versus durable fixed edges

- **Intact motifs ([T4], verified exactly).** The required-edge internal flux is 0 in all 24 target and ND laws, and the required-edge exit share is 1. Their CT lifetime is therefore a statement about how fast required edges dissolve.
  - **[P] Form-only families.** Under a family that changes only formation rates (PATHF, CLOSEW), every present edge dissolves at rate 1. An intact motif with r required edges then has exit rate exactly r in every state of A, so L_CT = 1/r exactly. The table values for PATHF and CLOSEW are 1/3, 1/3 and 1/2, the same as N0.
  - *Proof:* the exit flux is Σ_{x∈A} π(x)·r = r·π(A). ∎
  - So "the triangle lasts one third of a unit" under CLOSEW is not organisation. CLOSEW's intact rows look *shorter* than ND only because ND slows dissolution (deaths < 1 where φ increases) to reproduce the dense profile.
- **Flexible organisations.** These do survive *some* turnover. Ω > 0 holds even under NULL; it is a property of the predicates (definitions §6). The question is whether the rules add to it.
  - [O] Against ND, Ω is higher in 28/30 rows. The two exceptions are PATHF F_TRI at N = 5 and 6.
  - [L] Ω counts toggles, not replacements. PCOMP's Ω of 199 per F_2PATH episode at N=6 is mostly flicker: fast back-and-forth at path-rich slots. This round cannot say whether any episode replaced all its entry partners.

## 3. Clocks, sizes and the validity of ND

- **[P] What ND matches, exactly.**
  - By exchangeability, each slot's toggle flux equals 2J_edge, so E_π[q] = 2M·J_edge.
  - At matched density, the mean-rate calibration therefore forces **ND's CT edge present-lifetime to equal the target's.** This was verified on all 12 items to 7×10^−15.
  - So the CT ρ ratio against ND equals the CT lifetime ratio against ND.
  - **ND matches density and average edge lifetime. It differs only in how rates are arranged across states.**
- **[P] PATHF is fully matched.** PATHF's φ_k is non-increasing, so every ND death rate is 1 (min(1, ·) = 1). Then:
  - the per-k balance gives E[q | k] equal in target and ND, so the **JT density also matches** (L1 2×10^−14);
  - c = 1 exactly;
  - the dissolution kinetics are identical.

  PATHF against ND is the only comparison in the round matched in density in both clocks, in mean rate, in edge lifetime and in dissolution rule.
- **Where ND is and is not a valid control.**

  | Family | CT density / activity | JT density L1 (target vs ND) | Rate heterogeneity of target | ND as a control |
  | --- | --- | --- | --- | --- |
  | NULL | exact (ND = NULL) | 0 | none | identity check |
  | PATHF | matched | ≈ 0 | low (rates ≤ 1) | **valid in both clocks** |
  | CLOSEW | matched | 0.45–0.47 | formation 2^t, up to 2^4 | CT partially valid; JT diagnostic |
  | PATHH | matched | 0.42–0.43 | dissolution up to 2^24 | CT confounded by heterogeneity; JT diagnostic |
  | CSPH | matched | 0.59–0.60 | up to 2^24 | as PATHH |
  | PCOMP | matched (law identical to NULL) | 1.29–1.74 | both directions up to 2^24; c = 44 and 4,609 | **demonstrates the confound** |

- **Clocks.**
  - PATHH and CSPH are mostly *shorter* than ND in CT but longer in JT, for both intact and flexible rows. That is a clock-dependent conclusion, not a robust one.
  - CLOSEW and PATHF give the same sign in both clocks.
- **Sizes (finite-size observations only).**
  - CLOSEW flexible ratios grow from N = 5 to 6: F_2PATH 1.80 → 2.76, F_STAR 1.19 → 2.17.
  - PCOMP's grow sharply.
  - PATHF's are flat (F_STAR 1.075 → 1.103; F_2PATH 1.066 → 1.042).
  - CSPH's shrink (F_2PATH 1.19 → 1.09; F_TRI 1.08 → 0.98).
  - No phase or symmetry-breaking claim is possible (R3).

## 4. Competing explanations

| Mechanism | Evidence for | Evidence against or limits | Verdict |
| --- | --- | --- | --- |
| **Kinetic heterogeneity** (activity concentrated in dense, path-rich states; a global clock inflated by distant activity) | PCOMP: law identical to NULL, ND = NULL × c, yet flexible lifetimes are ×1.2–25 in CT (5 of 6 rows; F_STAR at N=5 is ×0.93) and ×2.3–31 in JT. The effect grows with c | Cannot apply to PATHF (rates ≤ 1, fully matched) | **Established as sufficient [T by example, O]** to produce "longer than ND". **The main confound** |
| **Prevalence and composition** | CLOSEW F_2PATH and F_STAR are true 96–99% of the time, so episodes are rare and long | ND has the same density and nearly the same prevalence (0.97–0.99), so prevalence alone does not explain ×2–3 | Contributes; not sufficient |
| **Density** | — | Matched by construction in CT | Excluded in CT |
| **Kinetic slowing of edges** | — | Edge CT lifetime is identical to ND's ([P]), and equals 1 under PATHF and CLOSEW | Excluded as an explanation of ND contrasts |
| **Closure-driven recovery** (CLOSEW) | Lives ×2.2–2.8 at N=6 with edges no slower, more turnover (Ω 147 vs 52) and fewer entries per unit time (0.06 vs 0.16). Closure favours re-forming links next to existing ones | Formation rates up to 2^4 are themselves heterogeneous (partly the PCOMP confound). A reversible Gibbs law (GT-F05 lineage) | **[C] Leading candidate** for persistence through turnover |
| **Path-driven directional circulation** (PATHF, PATHH, CSPH: published σ > 0) | Hub memory is slower than ND in both clocks for all three | PATHH and CSPH predicates are clock-dependent. PATHF predicate effects are small. No channel here measures circulation of turnover | **[C] Open.** The circulation link is not shown |
| **Hub-selection bias** | Initial gaps are larger in path families (1.03–1.61 against ND 0.94–1.19) | Every gap decays toward zero ([T8]) | Selection explains the start; memory differs by family |
| **Pre-existing correlation structure** | The E0A/E0B N=5 degree autocorrelation times were already above NULL for path families (e.g. PATHF 0.72 vs 0.5) | — | The slow hub memory is **consistent with published channels**; it is not wholly independent |

## 5. Negative, anomalous, fragile and qualified outcomes (all kept)

- **Negatives:**
  - No intact motif persists beyond ND in CT except the PATHH star (×1.004 and ×1.093).
  - PATHF flexible triangles are shorter than ND, with fewer turnovers, at both sizes.
- **Anomaly:** PCOMP's large "persistence" in a law with no structural preference (the main unexpected finding).
- **Clock-fragile:** PATHH and CSPH rows reverse between clocks.
- **Numerically qualified:** CT lag channels of PATHH N=6 and CSPH N=6. Row-sum and stationarity errors reached 9.7×10^−9 and 6.6×10^−9 against the frozen 10^−9 tolerance. All other lag checks held, including the independent semigroup check (2.4×10^−10). No contrast drawn here is smaller than 10^−3.
- **Secondary channel:** all 144 killed-chain solves converged. The first-passage route reproduces every L within 2.6×10^−10. Residual life obeys the Palm bound everywhere and exceeds L for heavy-tailed predicates (CLOSEW F_2PATH N=6: 21.4 vs 16.8).

## 6. Is there a reasonable motif-persistence signal?

- **Within this finite model, two qualified candidates:**
  - **PATHF centre organisations** (F_STAR, F_2PATH): ×1.04–1.10 in CT and ×1.01–1.07 in JT against a fully matched ND, at both sizes, with roughly doubled turnover for F_STAR. Small, but against the cleanest comparator in the round. **A reasonable but weak signal.**
  - **CLOSEW flexible organisations:** ×1.1–2.8, both clocks, growing with N. **A strong signal against ND**, but exposed to the heterogeneity confound and observed at near-certain prevalence.
- **Neither is an emergent reference:**
  - each is anchored to a labelled vertex or edge;
  - each episode ends;
  - identity through full replacement is undefined;
  - no pattern is distinguished in the stationary law (exchangeability).

## 7. GT-Q18 to Q20 and the bridge map

- **GT-Q19 (a metastable FREE reference): partially answered.**
  - No persistence of intact motifs, and no self-made centre.
  - Weak-to-moderate, comparator-dependent persistence of anchored flexible organisation, with turnover.
  - The comparator problem is now explicit (GT-Q21).
- **GT-Q18 (floor reversal at W4) and GT-Q20 (the residue mechanism):** not addressed. These are held-reference questions; E5A is FREE.
- **Bridge map (revision 4, appended):**
  - the persistence step moves from "undefined" to "partially answered, comparator-dependent";
  - "identity through replacement" stays undefined;
  - a new established capability: lifetime is not a function of the stationary law ([P], via PCOMP and NULL).

## 8. Architecture implications

- **The first missing piece has moved.** GT-P008 said it was a definition of a candidate pattern. E5A shows that a pattern definition is not enough without a **kinetics-aware comparator**.
  - Stationary density, and even the average edge lifetime, do not fix lifetimes.
  - Any comparator must declare where activity sits.
- **Two cheap measurement fixes, no new state or rule:**
  - an **anchor-local clock:** count only events on slots incident to the anchor;
  - a **replacement-completion measure:** whether every entry partner has been replaced, which suppresses flicker.

  Both are read-only analysers (8G not engaged). Replacement completion is a trajectory observable; it needs no history state in the rules (T-11 of the GT-P008 transfer note).
- **The 8G gate.** Nothing here suggests that history or meta state is needed. All observed differences come from current-state kinetics.

## 9. Future directions, compared factor by factor (no aggregate score)

| | A. E5B: local clock + replacement completion (same 12 laws) | B. Floor-reversal test (GT-P008 option B) | C. A stronger current-state rule that compiles (e.g. a degree-dependent formation template) | D. Stop motif work |
| --- | --- | --- | --- | --- |
| **Question** | Do the CLOSEW and PATHF signals survive heterogeneity and flicker? | Does the first-order index or the floor decide sorting at W4? | Can a compilable rule make persistence unambiguous? | — |
| **Information value** | High: decides whether E5A's positive rows are organisation | High for Workstream A; independent of persistence | Moderate: risks building in the answer (a rule that rewards the predicate) | Records a clear null for intact motifs and centres |
| **Artefact discrimination** | Directly targets the identified confound | Good (within-cell) | Weak unless pre-registered against the same comparators | — |
| **Cost** | Minutes (kernels and laws reused; event counting in the jump chain) | Under 10 min, two new presets | Needs a new family and a grammar check | None |
| **Risk** | The local clock is still one convention; it must be declared before seeing results | Narrow (1 probe, special graphs) | Insertion of the desired behaviour | Possible premature closure |
| **Cross-programme relevance** | CL-Q05 (passage, persistence), CL-Q03 (no history needed) | CL-Q04 | CL 8G | — |
| **Authorisation** | Needs a new prompt (E5B not authorised) | Needs a new prompt | Needs a new prompt and a grammar review | — |

**Recommendation (not frozen, not executed).**
- **Principal: A.**
  - Same 12 laws.
  - Flexible predicates only.
  - Primary channels:
    - lifetime in anchor-local events;
    - replacement completion (the fraction of entrance episodes in which every entry partner has left at least once before exit);
    - Ω net of immediate reversals.
  - Comparators: N0, ND, and a second declared comparator matching the target's per-state total rate profile by edge count (E[q | k]). It is declared now, to be frozen only after authorisation.
- **Fallback: B.**
- C is not recommended without a separate grammar review.
- D is acceptable if the human researcher judges the intact and centre nulls sufficient.

## 10. RS reading (separate layer, conjectural)

- **[RS]** If the grammar is read as a lens on relational actualisation, E5A suggests something about persistence. What persists is not a fixed set of relations: those cannot outlive their own replacement. It is, at most, a *property maintained through replacement*, and only where rules re-form what was lost (closure).
- Whether such a property is "the same thing" over time is exactly what the grammar does not yet define.
- This is an interpretive reading. It is not evidence about physical bodies, time or gravity.
