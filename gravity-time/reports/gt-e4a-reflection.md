# GT Round E4A — reflection and the E4A → E4B selection

*Prompt GT-P007.*
- *Written after the E4A results (result `06e5f36`, payload `f050380ac32e`, frozen plan `f5b3b50`), and before any E4B code, plan or cell.*
- *Numbers are from `reports/round-e4a-tables.json`; every cell is in `reports/gt-e4a-atlas.md`.*
- *Layers: [O] observation, [M] mathematics, [RS] interpretation; [P] none; [T] none.*

## 1. What E4A observed

**Validation [O].** All 36 cells completed, and every frozen identity held:
- the witness-floor census matches the analytic floor at every state (36/36);
- NULL under each scaffold is uniform with zero margins (6/6);
- PCOMP and CLOSEW are reversible (12/12);
- PCOMP's continuous-time margin vanishes (6/6);
- CLOSEW follows its Gibbs law (6/6);
- all 12 K3 cells reproduce the published E0B values (12/12);
- numerical acceptance, including the rule-string kernel check under each scaffold (36/36).

**Findings.**

1. **Native K2 gives positive raw margins for every σ > 0 path family, in both clocks, at both sizes** [O]. Margins are against K2's own NULL, r0 = 2(N−2)/M:

   | Family | N=5, continuous / per event | N=6, continuous / per event |
   | --- | --- | --- |
   | PATHF weak_suppress | +0.048 / +0.026 | +0.026 / +0.008 |
   | PATHH weak_favour | +0.073 / +0.068 | +0.065 / +0.064 |
   | CSPH | +0.115 / +0.099 | +0.124 / +0.124 |

   - Under K3 the same families are at −0.107, −0.044 and +0.046 at N=5 (continuous).
   - No rule reads source membership. This is the first native, label-covariant instance of these rules giving above-null attachment.
2. **Corrected for crowding, native K2's advantage mostly vanishes** [O].
   - The null-density-standardised margins, continuous / per event, are:
     - PATHF: N=5 +0.001 / −0.004; N=6 −0.023 / −0.025;
     - PATHH: N=5 +0.005 / +0.021; N=6 −0.030 / −0.016;
     - CSPH: N=5 +0.055 / +0.068; N=6 +0.009 / +0.031.
   - So for the single path families, K2's raw advantage is mostly **density composition**: the rule keeps the graph sparse, and sparse states favour attachment. This is the pattern GT-F34 found for CSPH under K3.
   - Only CSPH keeps a positive standardised margin in both clocks at both sizes, and it shrinks with N.
   - Overlap caveat: at N=6 the null's free-edge weight lying on low-mass counts reaches 0.18–0.24 for these cells (atlas). The standardised margin is partly counterfactual there.
3. **Inside P3 the vertex with fewer permanent witnesses attracts more** [O]. This is the cleanest covariant test of the witness mechanism, because it compares two source orbits of the same scaffold in the same states:

   | Family | N=5, middle (floor 0) / endpoints (floor 1) | N=6, middle / endpoints |
   | --- | --- | --- |
   | PATHF | 0.332 / 0.177 | 0.288 / 0.146 |
   | PATHH | 0.337 / 0.170 | 0.303 / 0.141 |
   | CSPH | 0.365 / 0.224 | 0.329 / 0.171 |

   Values are attachment occupancy per eligible slot, continuous clock. NULL has 0.500 at both orbits, and CLOSEW 0.81 / 0.80 (no difference).
4. **The free chord switches the middle off** [O].
   - When the P3 chord (0,2) is present, the middle's internal witnesses go from 0 to 2 (census), and its attachment collapses: PATHF N=5 0.411 without the chord, 0.138 with it; CSPH 0.539 against 0.213. The endpoints barely change (PATHF 0.179 against 0.170).
   - Under σ > 0 path rules the chord is itself rarely present: 0.23–0.29, against 0.50 under NULL, because the held path 0–1–2 witnesses its formation.
   - The attachment fraction conditional on the chord differs sharply (PATHF N=5: 0.435 with it, 0.871 without).
5. **P3 is not "between" K2 and K3 for every family** [O].
   - For PATHF and PATHH the raw margins order K2 > P3 > K3 at both sizes.
   - For CSPH at N=5, P3 (−0.043) is **below** K3 (+0.046) in the continuous clock. CSPH's closure term rewards attachments to two source vertices that are linked, and P3 links fewer of them.
   - Detachment orders K2 < P3 < K3 in every path family (for example PATHF N=5: 0.32, 0.36, 0.53).
6. **Direction persists; its magnitude depends on the reference** [O]. The handover keeps the E0 orientation in every σ > 0 cell under every scaffold. Its index under K2 and P3 is about half that under K3 (CSPH N=5: 0.019, 0.018, 0.036). Irreversible flux changes little (0.08–0.16).
7. **Controls behaved as their mathematics requires** [O]. CLOSEW and PCOMP show no handover or flux. PCOMP's per-event margin is positive (+0.002 to +0.009), consistent with the E3B C2 lesson: symmetric rates leave the continuous law uniform but not the jump law.

## 2. Mathematics added (derived after E4A, labelled) [M]

- **Floor for any connected held graph H.** The fixed floor at source vertex s equals the number of ordered held 2-paths starting at s, that is, Σ over held neighbours c of s of (deg_H(c) − 1).
  - Check: K3 gives 2 at each vertex; P3 gives endpoints 1, middle 0; K2 gives 0.
  - Proof: a witness (s, c, d) with both edges held needs (s,c) held and (c,d) held with d ∉ {s, p}, and d is never the probe p, because (c,p) is not held.
- **K2 is the only connected held reference with zero floor everywhere.**
  - Zero floor at every s needs deg_H(c) ≤ 1 for every held neighbour c of every s, so every component of H is a single edge.
  - Any connected reference with k ≥ 3 has a vertex of positive floor.
  - So one cannot remove the floor while enlarging a connected source. One can only redistribute it.
- **Corollary.** Floor heterogeneity *within* one scaffold is the natural covariant instrument (as P3 showed). Examples at k = 4: the star K1,3 has centre 0 and leaves 2; the path P4 has 1 at every vertex.

## 3. Has the E3B interpretation survived?

| E3B claim (instrument) | Native E4A |
| --- | --- |
| The triangle's internal witnesses suppress attachment | **Supported natively.** P3's floor-0 orbit attracts about twice its floor-1 orbit in the same states; forming the chord collapses the middle; K2 > P3 > K3 in raw margins for the path families |
| Without the floor, σ > 0 families gather above null | **Qualified.** Native K2 is above null in raw margins (sign agrees with E3B), but mostly not after density standardisation, except CSPH. Magnitudes are smaller than E3B's neutralised K3 (for example PATHF N=6: native K2 +0.026 against neutralised K3 +0.073). The two laws were never expected to match (different k, M and witnesses) |
| Gathering coexists with the arrow | **Natively, in raw margins: yes under K2.** For CSPH also standardised (small at N=6). The arrow is weaker under K2/P3 |

The E3B inference that depended on the instrument is "these rules gather once the floor is gone". Natively, what survives is a density-composition gathering (raw margins), plus a robust witness-floor ordering of attachment between source orbits. T7 and T8 remain mathematically true, and the floor formula above generalises T7.

## 4. What the change is attributable to

| Factor | Evidence |
| --- | --- |
| Permanent witness floor | Strong: within-P3 orbit contrast; chord conditioning; K2 > P3 > K3 ordering for PATHF/PATHH |
| Source size / r0 | Present but not dominant: margins are against each scaffold's own null; K2 at N=5 and K3 at N=6 have equal probe counts (3) and still differ sharply (PATHF +0.048 against −0.206) |
| Density composition | Large: standardised margins are much smaller than raw ones under K2 |
| State-dependent witnesses (chord) | Large within P3 |
| Clock | Secondary: signs agree across clocks for K2 raw margins; standardised margins differ in sign between clocks only near zero |

## 5. Bridge-map consequences

- **B12 → P8 "scaffold-confounded" (E3).** Now **partly resolved natively.** The suppression is real and witness-mediated. Gathering without a floor is mostly density composition, except for CSPH.
- **A new native capability.** Source-orbit selectivity: a reference's internal structure sorts where relations attach, in proportion to its permanent witness floor.
- **Unchanged.** Displacement, identity and acceleration remain undefined.

## 6. Selecting E4B

Candidates were compared factor by factor, with no combined score.

| Candidate | Information value | Discriminates | Cost | Risk |
| --- | --- | --- | --- | --- |
| **Four-vertex references at equal size: star K1,3 (floors 0, 2, 2, 2) against path P4 (floors 1, 1, 1, 1), N=6** | **High.** It separates floor *heterogeneity* from floor *amount* at fixed k = 4 and K = 3; replicates the within-scaffold orbit ordering in a new geometry (adaptive, not independent); and tests whether a uniform floor (P4) removes orbit selectivity | Floor redistribution against size and edge count; uniform against heterogeneous floors | Low (N=6, 4,096 states) | Only 2 probes at N=6; N=7 is not authorised |
| P3 with the chord held absent | Moderate: isolates the chord | Chord dynamics against floor | Needs a new boundary semantics (held-absent relations), which GT-P007 discourages without separate justification | Engineering |
| Opposite-σ families under K2 | Low: they saturate (E2) | — | Low | Little information |
| Density-composition decomposition of K2 margins | Moderate, but a post hoc analysis of E4A data, not a round | — | — | — |
| No E4B | — | — | — | Leaves the floor-amount question open |

**Choice: E4B compares star K1,3 and path P4 at N=6.**

**Design principles fixed here, before writing E4B:**
- **Cells.** Families NULL, PATHF weak_suppress, PATHH weak_favour, CSPH and CLOSEW, plus PCOMP. Two scaffolds at N=6: 12 cells.
- **Same measurements as E4A.** The orbits are star centre against leaves, and P4 ends against inner vertices. Dynamic chords: star leaf–leaf (3 chords); P4 (0,2), (1,3), (0,3).
- **Frozen identities.**
  - Floor census: star centre 0, leaves 2; P4 all 1.
  - NULL, PCOMP and CLOSEW identities.
  - Numerical acceptance.
- **Open questions, no prediction:**
  - Does the star centre out-attract its leaves for σ > 0 families?
  - Does P4 show orbit selectivity without floor heterogeneity?
  - Which scaffold has the larger raw and standardised margins?
- **E4B is adaptively chosen.** It is not confirmation of E4A's P3 finding.
