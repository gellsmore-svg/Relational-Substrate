# GT-E4 Open-Thetical synthesis (GT-P007)

*This covers:*
- *E4A: plan `f5b3b50`, results `06e5f36`, reflection `8127d24`;*
- *E4B: plan `9a1c539`, results `64e183f`;*
- *`docs/e4-configurable-scaffold.md` and `docs/e4-formal-witness-floors.md`.*

*Layers: [O] observation, [M] mathematics, [RS] interpretation. [P] none. [T] not engaged.*

## 1. What was done

- **A configurable held reference.** It is defined by a set of held relations, with the default the original triangle. It was added without touching the grammar, and verified by:
  - exhaustive kernel equality with the rule-string implementation;
  - relabelling covariance;
  - automorphism symmetry;
  - bit-for-bit reproduction of published triangle cells.
- **E4A:** K2, P3 and K3 × N=5, 6 × six families, 36 cells, of which 12 are triangle replications.
- **E4B:** the star K1,3 and the path P4 at N=6 × six families, 12 cells. It was chosen after the E4A reflection.

## 2. Findings by strength

**Robust (both sizes, every σ > 0 family, both clocks, covariant, within-cell controls) [O]:**
- **Attachment goes where the permanent floor is low.**
  - Within P3, the floor-0 middle attracts about twice the floor-1 ends (attachment per slot 0.29–0.37 against 0.14–0.22).
  - Within the star, the floor-0 centre attracts about four times the floor-2 leaves (0.36–0.37 against 0.085–0.093).
  - Under P4, where the floor is uniform, the orbits are level for PATHF (ends 0.146, inner 0.155). Inner vertices still attract more under PATHH (0.128 against 0.159) and CSPH (0.092 against 0.151). That is a smaller, state-dependent orbit effect with no floor difference behind it.
  - These contrasts are made inside one cell, so source size, density, probe count and the null cannot explain them.
- **A free source chord switches its endpoints' neighbour off.** When the P3 chord forms, the middle's internal witnesses rise from 0 to 2 and its attachment collapses (PATHF N=5: 0.41 to 0.14). Under σ > 0 rules the held path suppresses the chord itself (occupancy 0.23–0.29, against 0.5 under NULL).
- **The handover orientation is the same under all five references;** its magnitude varies.

**Present but qualified [O]:**
- **Native gathering in raw margins.** Under K2, every σ > 0 family is above its own null in both clocks at both sizes (+0.008 to +0.124). Under the star, PATHF and PATHH are above null (+0.032 to +0.085). This is the first label-covariant instance.
- **That gathering is mostly density composition.** Standardised against each reference's own null density profile, it is near zero or negative (K2 PATHF/PATHH: −0.030 to +0.021; star: −0.031 to −0.004), except CSPH under K2: +0.055 / +0.068 at N=5, +0.009 / +0.031 at N=6.
- **The standardised margin is partly counterfactual at N=6.** 18–31% of the null weight lies on free-edge counts of low mass (atlas overlap diagnostics).

**Negative [O]:**
- **P4 and K3 (no floor-free vertex): σ > 0 path families are below null** in raw and standardised forms (P4 PATHF −0.088, PATHH −0.077; K3 as published).
- **CSPH is below null under every four-vertex reference** (star −0.060, P4 −0.251) and under P3 at N=5 (−0.043).
- **The overall margin does not follow the total floor.** The star (total 6) gathers where P4 (total 4) does not. P3 has a floor-free site but stays slightly negative.

**Mathematics [M]:**
- **F1:** the floor formula for any held graph.
- **F2:** only K2 has zero floor everywhere.
- **F4:** per-slot constant factors are orientation-neutral (generalising T8).
- **F5:** why event-order magnitudes move without any change of affinity.

## 3. Competing explanations (GT-P007 §2)

| Possibility | Outcome |
| --- | --- |
| P1 triangle-specific inhibition | **Supported for the inhibition, qualified for gathering.** Witness floors redistribute attachment and suppress it at high-floor sites, but removing them gives mainly density-composition gathering |
| P2 source size / combinatorics | **Not dominant.** Within-cell orbit contrasts are independent of size. S4 against P4 at equal k, K and r0 differ in sign |
| P3 topology beyond the floor | **Supported.** The chord's state-dependent witnesses matter (P3), and the overall margin is not a function of total floor |
| P4 clock / density artefact | **Supported for the cross-scaffold margins.** Raw gathering largely vanishes after density standardisation. Clocks agree in sign for raw margins |
| P5 structure-sensitive dynamics | **Supported.** The handover magnitude roughly halves under K2/P3 against K3; flux differs little |
| P6 no general gathering | **Partly supported.** No robust standardised gathering, except CSPH under K2 (small at N=6) |
| P7 unexpected | **Floor-guided sorting of attachment between source sites.** P3's CSPH below the triangle. A chord suppressed by the held path that witnesses it. A residual inner-vertex preference under the uniform-floor P4 (PATHH, CSPH) |

## 4. E3B, revisited

- **What survived.** The triangle's floor suppresses attachment, natively and covariantly, and the sign of the raw margins flips once no floor remains (K2).
- **What did not survive as a native result.** "These rules gather once the floor is removed" holds only in raw margins, and mostly as density composition. The E3B instrument's neutralised K3 law has larger, partly standardised-positive margins, which no native reference reproduces.
- **Mathematically still true.** T7 and T8, now generalised as F1 and F4.

## 5. Dual-lens journey

| Bottom-up capability (Lens B) | Top-down prerequisite (Lens A) |
| --- | --- |
| **Proved:** floors of any held reference (F1); K2 the only floor-free connected reference (F2); orientation-neutrality of per-slot factors (F4) | A reference's internal structure is part of the dynamics; "a source" is never neutral |
| **Observed:** attachment is sorted among source sites by floor; a free chord can switch a site off; raw gathering under floor-free references, mostly density composition | *Source–probe dependence* is now structure-dependent and mostly occupancy composition, not a robust density-independent preference |
| **Still absent:** displacement of anything identified; drift; acceleration; a non-circular separation; mutual interaction; scaling | *Identity, displacement, metric, acceleration, interaction, calibration:* **undefined.** No gravitational reading is supported |

## 6. Interpretation, kept separate [RS]

- **A reference is not a place; it is a structure, and structure sorts where relations form.** The model shows a precise version: sites of a held structure that are themselves less supported (lower witness floor) attract more new relations under rules that suppress formation along supported paths. In relational terms, support can make a site less available, not more. This is an interpretation, not a physical claim.
- **"Gathering" decomposes.** In these toy rules, apparent gathering mostly reflects where the system spends its density, not a density-independent preference. Any future gravity-motivated account built on such rules would need a mechanism that survives density standardisation.

## 7. Next options (compared, none run)

| Candidate | Information value | Discriminates | Cost | Notes |
| --- | --- | --- | --- | --- |
| **A. Formal derivation of floor-guided sorting:** a closed form, or bounds, for orbit attachment as a function of floor at small N (P3, star), including the chord | High: it would turn the robust observation into a mechanism with a proof domain | Floor-driven against kinetic-competition explanations | Low | Recommended |
| B. Density-matched comparison: K2 at N against K3 at N+1 (equal probe count), analysed with occupancy/preference decomposition | Moderate: separates density composition from preference | P4-type artefacts | Low (largely existing data) | Post hoc on E4A data unless frozen |
| C. N=7 under K2/star | Moderate | Size dependence of raw gathering | Moderate | Not authorised |
| D. An architecture review of what a "reference" should be (held, emergent, or none) before more scaffold rounds | High for Lens A | Whether held references can bridge to anything physical at all | Low | Pause option |
| E. A displacement definition proposal | Low now | — | Low | Still premature |

**Recommendation: A, with D as a short companion.** The robust result is floor-guided sorting, and it is close enough to the grammar to admit a derivation. The weak result (raw gathering) is mostly density composition, so further gathering experiments without a new mechanism are low value. An architecture pause on references is worth taking before investing in larger scaffolds.
