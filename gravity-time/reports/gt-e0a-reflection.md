# GT Round E0A — intermediate coherence reflection and E0A → E0B decision

Programme GT, prompt GT-P002, method OTR 1.0.
- **Frozen plan:** `2e5c97e` (hash `c98414e1…9dfa`), pushed before execution.
- **Tables:** `round-e0a-tables.json`, result commit `c31ef92`, payload `18fa301b…98cf`.
- **Execution:** 48/48 cells, 550 s total, 40 s for the largest cell. Validation ok: every stationary residual ≤ 1e-12 and every symmetry check ≤ 1e-10. No post-freeze code change.

Layers are marked [O] observation, [M] mathematical mechanism or inference, [RS] interpretation. Nothing here is a physical claim.

## 1. Frozen expectations

| Id | Statement | Outcome |
| --- | --- | --- |
| X1 | gradient cells reversible, real spectrum | **holds**, 32/32 cells (irreversible flux ≤ 6.5e-14) |
| X2 | gradient cells follow the predicted triple-Gibbs law | **holds**, 32/32 |
| X3 | CLOSE-strong, HOLD-strong, SPLIT share one law | **holds**, 4/4 mode×N |
| X4 | every PATH cell non-reversible (flux > 1e-6) | **fails in 4/16**: PATHF weak_favour and PATHH weak_suppress at N=6, both modes. Flux is 3e-13 to 3e-11, while the maximum square affinity is log 8 = 2.08 |
| X5 | NULL autocorrelation 1/2, localisation index 1 | **holds** |

**Why X4 failed.** This is a post-hoc explanation [M]. The favour-sign PATH cells saturate:
- Expected edges are 15.000 of 15 at N=6, and P(distance 1) is 1 − O(1e-16).
- The rates are non-gradient everywhere off the complete graph, so the affinity is non-zero. But the stationary mass there is negligible, so the flux cannot be irreversible.
- At N=5 the same cells sit only just above the floor (flux 3e-6 and 8e-5).

The audit chose the weak grade to avoid saturation. That was insufficient for the favour sign: a two-witness template has 2(N−2)(N−3) witnesses, and even a factor of 2 per witness compounds to complete-graph capture. The failure is recorded as computed, and the expectation is not reworded. It is a finding about the **X-saturation** artefact, and also a lesson: irreversibility of the rates (affinity) and irreversibility of the stationary process (flux) are different properties.

## 2. What actually occurred

**[O1] The gradient half of the grammar behaved exactly as derived.** Every single-witness composition was reversible, with π_ct equal to the predicted exp(θ·(E, W, T)) law. That includes cooperating (SPLIT), opposing (COMPETE), competing (FRUST), soft repulsion (ANTI) and hard exclusion (EXCL). Its event order is time-symmetric (pattern asymmetry ≤ 6e-15), and its spectrum is real.

**[O2] Non-gradient cells off saturation carry a large stationary arrow.** The two unsaturated sign choices are PATHF weak_suppress and PATHH weak_favour (dissolution promoted by second-neighbourhood support):
- 9–16% of stationary flux is irreversible;
- entropy production is 0.037–0.074 nats per mean event;
- the projected net current is 3–13% of flux.

**[O3] In HELD the arrow is a circulation around the source.** The net projected current runs in the cycle:

| Step | (free-edge count, attachments) | Event |
| --- | --- | --- |
| start | (0, 0) | — |
| 1 | (1, 0) | a probe–probe relation forms |
| 2 | (2, 1) | an attachment forms |
| 3 | (1, 1) | the probe–probe relation dissolves |
| 4 | (0, 0) | the attachment dissolves |

The event-order pattern "form attachment, then dissolve adjacent probe–probe" exceeds its time reverse "form probe–probe, then dissolve adjacent attachment" by 2.6× (0.043 against 0.017 at N=6). Event-order asymmetry in HELD is 0.06–0.10.

**[O4] In FREE the same arrow is nearly invisible to the class-free event projection.** Pattern asymmetry is 0.005–0.006, while the full irreversible flux is 10–14%. Projection loss is large: with no reference structure, the slot classes that make the cycle legible do not exist.

**[O5] Equal local ratios no longer fix occupancy.** PATHF weak_suppress and PATHH weak_favour have identical rate ratios r_ab(x) = 2^(−P(ab)). Their stationary laws differ by class-level L1 of 0.10 (FREE N5), 0.17 (FREE N6), 0.18 (HELD N5) and 0.32 (HELD N6). In the gradient triad the same comparison is ≤ 1e-14. So G1's decomposition, "the ratio fixes the basin, the split fixes the kinetics", holds only in the reversible class. Under irreversibility, whether a constraint acts on formation or on dissolution changes **where** the system sits, not only how fast it moves.

**[O6] The unsaturated non-gradient cells are anti-basins.**
- In HELD the probe is detached 53–55% of the time, against 4–7% under NULL.
- The attachment fraction falls to 0.54–0.64 (null 0.75) at N=6.
- Near/far activity ρ is above 1 (1.1–1.4) under both clocks.

So E0A observed a stationary arrow only in a repulsive regime. Whether an arrow can coexist with a basin is **untested**, because the attractive-sign PATH cells saturated.

**[O7] COMPETE gives activity structure with no basin.** Its stationary law equals NULL exactly (L1 ≤ 7e-14). Yet:
- near-source activity is 4.7–5.3× far activity under the continuous clock, and 1.8–2.4× under the jump clock;
- immediate reversal roughly doubles (0.24 against 0.14 in HELD N5);
- relaxation per mean event is 4–8× slower.

G1 saw only near-source slowing and read it as an occupancy effect. Here is near-source **speed-up** at zero occupancy contrast.

**[O8] The kinetic triad orders differently under the two clocks.** CLOSE, SPLIT and HOLD share one law:
- Per mean event, the relaxation gaps are 0.14, 0.68 and 1.40 (FREE N5), so CLOSE relaxes slowest.
- Per unit time (gap × mean rate) they are 2.77, 1.87 and 0.64, so CLOSE relaxes fastest.
- Immediate reversal follows approach > split > retention in every cell (0.45 / 0.39 / 0.30 FREE N5).

**[O9] Repulsion is a sign mirror, and hard is stronger than soft.** At N=6, attachment is ANTI 0.68 and EXCL 0.64, against a null of 0.75; at N=5 the figures are 0.81 and 0.76 against 0.857. EXCL's exclusion is admissibility without arrest: a recurrent class of 349 states at HELD N6, with no absorption, unlike LOCK.

**[O10] No emergent centre.** FRUST (wedges rewarded, triangles cost two wedge-units) lowers attachment slightly (0.74 against 0.75). Its FREE degree variance is below NULL's at matched N (0.46 against 0.60 at N=5), and the full-centre probability follows density. No cell produced degree heterogeneity above NULL.

**[O11] Local persistence exceeds global persistence only in sparse cells.** The localisation persistence index τ(degree)/τ(edges) is above 1 only in sparse, triangle-poor cells:
- PATHF−/PATHH+ FREE N5: 2.20 and 2.07;
- EXCL: 1.49; ANTI: 1.34.

It is below 1 in the attractive cells (CLOSE 0.72). It is not associated with a basin, and its mechanism is not yet explained.

**[O12] Weak oscillation is not a general mark of irreversibility.** PATHF weak_suppress has many complex modes (2,258 at HELD N6), but they are weakly oscillatory (maximum |Im|/|Re| 0.09). Its equal-ratio partner PATHH weak_favour has none in HELD. Irreversibility does not imply visible cyclic return.

## 3. Surprises, including disappointing ones

1. X4's failure: the "gentle" weak grade still saturated the favour-sign non-gradient cells.
2. **O5.** We expected a possible small difference. It is large (L1 up to 0.32), and it removes the clean kinetic/occupancy separation G1 rested on.
3. **O3.** The arrow has a concrete, source-relative order: a probe–probe link is handed over to an attachment.
4. **O7.** Activity concentration can be completely independent of occupancy.
5. A disappointment: every irreversible cell we could observe was repulsive, and FRUST gave no centres.
6. A methodological failure. The moment-matched triple-Gibbs KL did not converge for the saturated gradient FREE cells: it reports 2.63 and 1.20 nats where the true value is 0. Those six values are numerical failures of a descriptive projection, flagged `converged: false` in the tables, and must not be read. The predicted-law check (X2), which needs no fitting, holds for them.

## 4. Explanations [M]

- **O1** is the audit §3 theorem.
- **O2 and O5:** for non-reversible chains, π is the solution of global balance, which depends on the full rates, not on the ratios. Known in general, new for this grammar.
- **O3:** the PATH rules make a probe–probe relation's dissolution, or the suppression of its formation, depend on the two-path through it. Once a probe attaches, its probe–probe relation gains a two-path into the source. The Kolmogorov asymmetry derived in the audit (Δ_ac P(ab) ≠ Δ_ab P(ac)) becomes an ordered handover. A full mechanistic decomposition is not done.
- **O7:** COMPETE multiplies both directions of supported relations by 4^w. Detailed balance is untouched; the clock runs faster wherever support exists, and near the held triangle support always exists.
- **O8:** per-event normalisation against per-time rates. This is G0's X-CLOCK, seen again in relaxation.

## 5. Lens register after E0A

| Lens | What E0A did to it |
| --- | --- |
| D | Directional tendency in stationary succession exists only for non-gradient rules (O2, O3). Every G0 "direction" was occupancy |
| A / A→D | Hard exclusion of formation gives admissibility without arrest (O9). A→D remains occupancy-only in the gradient class |
| B | Retention against approach is a kinetic distinction in the gradient class. Under irreversibility it changes occupancy (O5) |
| C | Opposing rules can cancel in occupancy and still structure activity (O7). Competing motifs gave no new structure (O10) |
| K | Strengthened and split: K-gradient (pure kinetics) and K-irreversible (kinetics also sets occupancy) |
| E | Weakened at these sizes: no emergent centre (O10). O11 is unexplained |
| R (new) | Established in model. A stationary arrow requires non-gradient rules, and its legibility depends on a reference projection (O4) |
| X | Saturation was confirmed as a hazard even at weak grades (X4). Clock dependence was confirmed in relaxation (O8). Projection loss is large in FREE (O4) |

## 6. E0A → E0B decision note

**What was learned.** The grammar divides cleanly. Its gradient half gives basins with no arrow. Its non-gradient half gives arrows, but at the grades E0A tried, only in repulsive regimes or at saturation. And irreversibility removes the clean separation of basin from kinetics.

**Competing explanations now live:**
- **(a) Exclusion.** Arrow and basin are mutually exclusive in this grammar: the PATH mechanism that makes the arrow always repels.
- **(b) Grade.** The arrow-without-basin pairing is a grade artefact. A composite of an attractive gradient term and a non-gradient term at intermediate strength might show both.
- **(c) Projection.** The FREE arrow's invisibility is a projection choice. A frame defined by emergent structure (current hubs), instead of the imposed source, might make it legible without a scaffold.
- **(d) Kinetics fixes basin depth.** If (b) holds, then the formation-acting and dissolution-acting versions of an equal-ratio composite would give basins of different depth. That would carry O5 into the attractive regime.

**E0B choice.** One adjustment that discriminates (a) from (b), tests (c) on existing and new kernels, and tests (d):

1. **Attractive gradient + non-gradient composites.** Closure favour, at both grades, combined with the two unsaturated non-gradient components (PATHF weak_suppress, PATHH weak_favour). That is four composites, forming two equal-ratio pairs. Does attachment rise above null while the flux stays irreversible? Does the arrow keep the O3 orientation or reverse? Do equal-ratio composites differ in basin depth?
2. **A control where non-gradient rules give a gradient ratio** (PCOMP: PATHF favour + PATHH favour, ratio ≡ 1). It is derived reversible and uniform, and tests whether the arrow belongs to the rules or to the ratio.
3. **A weak closure anchor** (CLOSEW), needed to compare composites with their gradient part at the same grade.
4. **Replication** of NULL and the two E0A arrow cells, with an unchanged pipeline. Their E0A values must be reproduced exactly.
5. **One new observation channel on every cell:** event order and projected current in an **emergent hub frame** (slot incident to a current maximum-degree vertex or not), for FREE and HELD. This addresses (c) without a new primitive.

**Why it has information value.** The composites can return basin+arrow, basin only, arrow only (repulsion wins) or saturation. Each outcome separates (a) from (b). The equal-ratio pairs test (d) in either case. PCOMP is a negative control on the mechanism. The hub frame tests scaffold dependence of direction, a central GT question (lens E, prompt Q4 and Q6).

**Seemingly obvious alternatives, not chosen:**
- **Strong-grade or finer-grade PATH alone.** W4 has no grade between 1 and 2, and favour-sign PATH saturates even at 2.
- **Desaturating PATH-favour with density suppression.** A K1 term at 1/4 cannot offset up to 2^24 per pair at N=6, and choosing a balancing factor would be tuning on E0A outcomes.
- **G2 at N=7.** It does not address the arrow/basin question that E0A opened.
- **Explaining O11 first.** It is interesting but secondary: it is not tied to basins or arrows.
- **A history register.** 8H owns it.

Grade choice in E0B is made from E0A's recorded regimes (both closure grades, both unsaturated PATH signs). No grade is chosen to produce a desired attachment value. The decision is made before any E0B cell is computed.
