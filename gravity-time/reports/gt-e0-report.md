# GT-E0 — open-thetical rounds E0A and E0B

Programme GT, prompt GT-P002, method OTR 1.0 (`research-methods/open-thetical-research.md`). Two frozen, exact rounds on the O=2 pair grammar of the Constraint Laboratory. No new primitive, history register, metric or clock was added. Trajectories were sampled only for the atlas.

| Round | Plan commit | Plan hash | Result commit | Tables payload | Cells | Wall |
| --- | --- | --- | --- | --- | --- | --- |
| E0A | `2e5c97e` | `c98414e1…9dfa` | `c31ef92` | `18fa301b…98cf` | 48 | 550 s |
| E0B | `50c4b2c` | `ad28c5b1…2c32` | `d99f972` | `f02c7c95…cb80` | 36 | 727 s |
| E0C | not run | — | — | — | — | — |

Supporting documents:
- [`../docs/e0-coverage-and-selection.md`](../docs/e0-coverage-and-selection.md): the coverage audit and the E0A selection.
- [`gt-e0a-reflection.md`](gt-e0a-reflection.md): the E0A reflection and the E0A→E0B decision note.
- [`gt-e0-atlas.md`](gt-e0-atlas.md): the behavioural atlas, every cell, with selected replayable trajectories.

Both plans were committed and pushed before their cells ran. The journey records the question before execution and the result afterwards (steps 5–8).

Layers: **[O]** formal-system observation, **[M]** mathematical mechanism or inference, **[RS]** RS / global-coherence interpretation, **[P]** physical comparison, **[T]** theological premise.

## 1. The sequence, and why each step was taken

1. **Audit, before any code.** The audit found a theorem [M] that explains G0's O5. Every single-witness, label-covariant template composition is reversible, and its stationary law is triple-local Gibbs, exp(θ·(E, W, T)). So every G0/G1 basin was a potential with no stationary direction. The grammar also admits non-gradient two-witness templates, which no GT cell had entered.
2. **E0A** crossed that boundary. It used 12 family-grades: gradient anchors; cooperating, opposing and competing compositions; soft and hard repulsion; and four non-gradient PATH cells. Each was run in HELD and FREE at N=5 and 6, through new reversibility, event-order, relaxation, autocorrelation and class-occupancy channels.
3. **E0A's result changed the question.** Stationary arrows appeared, but only in repulsive or saturated cells. Equal local ratios stopped fixing occupancy. And without a reference structure, the arrow was invisible.
4. **E0B was chosen because of that.** It used:
   - attractive closure combined with the two unsaturated non-gradient terms, at both closure grades, forming equal-ratio pairs;
   - a control in which the rules are non-gradient but the ratio is gradient (PCOMP);
   - a weak closure anchor (CLOSEW);
   - replication of three E0A cells;
   - a new emergent hub-frame channel.

   None of these was planned before E0A was read.
5. **E0C was not run** (§6).

## 2. E0B frozen expectations

| Id | Statement | Outcome |
| --- | --- | --- |
| Y1 | PCOMP reversible, uniform law | holds, 4/4 |
| Y2 | E0A cells replicate within 1e-12 | holds, 12/12 |
| Y3 | CLOSEW follows its predicted Gibbs law | holds, 4/4 |
| Y4 | composite rates non-gradient | holds, 16/16 |
| Y5 | hub frame silent on reversible cells | holds, 12/12 |

E0A's expectations X1–X3 and X5 held. X4 failed in 4/16 cells through saturation (reflection §1).

## 3. Observations across both rounds [O]

The E0A observations O1–O12 are in the reflection. The E0B observations are listed here, with the cross-round picture.

**B1. Selective basin and stationary arrow can coexist, narrowly** (GT-F26).
- Only one composite shows both: strong closure plus dissolution-acting non-gradient support (CSPH).
- HELD N5: attachment 0.904 against null 0.857, with irreversible flux 0.090.
- HELD N6: 0.759 against 0.75, with flux 0.137.
- The probe is still detached 52–55% of the time, against 4–7% under NULL. The "basin" is selectivity among present relations, not concentration of occupancy.
- The margin shrinks with N, from +0.047 to +0.009.
- Every other composite stays below null: CSPF, CWPF and CWPH.

**B2. Under irreversibility, kinetics sets basin depth** (GT-F27).
- Within each equal-ratio pair, the dissolution-acting version is more selective in every cell.
- At HELD N6: CSPH 0.759 against CSPF 0.611, and CWPH 0.683 against CWPF 0.565.
- The occupancy L1 between pair members runs from 0.11 to 0.49.

**B3. An emergent frame makes direction legible without a scaffold** (GT-F28). In FREE mode the hub-frame event asymmetry is 0.032–0.049, against 0.001–0.006 in the class-free projection. In HELD the hub frame roughly reproduces the source frame.

**B4. The handover orientation is invariant** (GT-F29).
- Source frame: in every arrow-bearing cell, with or without a basin, "form attachment, then dissolve adjacent probe–probe" exceeds its time reverse, by about 2×.
- Hub frame, the emergent analogue: "form hub-incident, then dissolve non-hub" exceeds its reverse.
- Where a basin exists (CSPH), the circulation runs at higher attachment counts but keeps its orientation.

**B5. The arrow belongs to the ratio, not to the rule syntax** (GT-F30). PCOMP's rules are both two-witness, but the ratio is identically 1. It is exactly reversible and uniform. It also concentrates activity near the source under the continuous clock (ρ 4.7 at N5, 18.9 at N6) while the jump clock gives ρ 0.67. The **sign** of the near/far comparison depends on the clock.

**B6. Composites did not saturate.** With the path term present, expected edges are 3.4–5.4 even at strong closure. In these composites the non-gradient term dominates density.

**Cross-round summary of regimes:**

| Regime | Arrow | Basin (selectivity above null) | Example |
| --- | --- | --- | --- |
| Gradient attractive | none | yes | CLOSE, HOLD, SPLIT, CLOSEW |
| Gradient repulsive | none | anti | ANTI, EXCL |
| Gradient opposing | none | none, but activity concentrated | COMPETE |
| Non-gradient rules, gradient ratio | none | none, but activity concentrated | PCOMP |
| Non-gradient, saturated | hidden (rates only) | trivial | PATHF+, PATHH− at N=6 |
| Non-gradient, unsaturated | yes | anti | PATHF−, PATHH+ |
| Gradient attractive + non-gradient | yes | weak or anti, depending on channel and grade | CSPH (weak basin), CSPF, CWPF, CWPH (anti) |

## 4. Explanatory analysis [M]

- **Reversibility.** It is decided by the rate ratio r_ab(x) alone. If log r is the gradient of a configuration function, the chain satisfies detailed balance and π_ct ∝ exp H. Single-witness label-covariant templates always give a gradient (audit §3). Two-witness templates with asymmetric roles do not, because Δ_ac P(ab) ≠ Δ_ab P(ac). PCOMP confirms the criterion from the other side: non-gradient rules whose ratio is constant are reversible. **Known mathematics:** Kolmogorov's criterion, and exponential-random-graph laws for local Glauber dynamics. **New here:** its application to this grammar and the explicit boundary.
- **Equal ratio, different law.** For a non-reversible chain, the stationary law solves global balance and depends on the full rate matrix. Formation-acting and dissolution-acting terms change the escape rates of different states differently, so the stationary weights move. That they move in a consistent direction (dissolution-acting is more selective) is observed, not derived.
- **The handover.** A PATH term ties a probe–probe relation's kinetics to the two-paths through it. Once a probe attaches to the source, its probe–probe relation gains a two-path into the source, so the probe–probe relation's dissolution is promoted, or its re-formation suppressed. The cycle "probe–probe forms → attachment forms → probe–probe dissolves → attachment dissolves" is the elementary Kolmogorov asymmetry, realised as an order of events. This is a mechanism sketch, not a full decomposition.
- **Activity without basin.** COMPETE and PCOMP multiply forward and backward rates of a relation by the same factor, so detailed balance and π are untouched, but the local clock speeds up wherever support exists. Under the jump clock the same effect is renormalised by the total rate, which flips PCOMP's sign. This is G0's X-CLOCK in a sharper form.
- **Saturation (X4).** Two-witness templates have 2(N−2)(N−3) witnesses per pair. A per-witness factor of 2 compounds to complete-graph capture, which removes stationary flux even though the rates stay non-gradient.
- **Representational variants.**
  - CLOSE(m), HOLD(1/m) and the SPLIT composite are one stationary object with three kinetics.
  - `absent` literals compile to DENS plus inverse ADJ (audit §3).
  - Each labelled stationary law is constant on symmetry orbits (S_N in FREE, S_3 × S_(N−3) in HELD), so the class tables are lossless; the symmetry check passes ≤ 1e-10 in every cell.

## 5. Which findings are robust, fragile, confounded or representational

| Finding | Character |
| --- | --- |
| Single-witness reversibility, triple-Gibbs law (GT-F12) | **robust**: theorem, verified on 36 gradient cells across rounds |
| Non-gradient stationary arrow off saturation (GT-F13) | **robust** within N≤6 and weak grades; replicated (GT-F31) |
| Handover orientation (GT-F15, GT-F29) | **robust** across all arrow cells, both frames; mechanism only sketched |
| Equal ratio ≠ equal occupancy; dissolution-acting more selective (GT-F17, GT-F27) | **robust** in sign across 12 pairs; magnitude grade-dependent |
| Basin and arrow together (GT-F26) | **fragile**: one composite, small margin shrinking with N, selectivity not occupancy |
| Activity concentration without basin (GT-F19, GT-F30) | robust in existence; magnitude and even sign **clock-confounded** |
| Kinetic-triad relaxation order (GT-F20) | **clock-confounded**: reverses between clocks |
| FREE arrow invisibility (GT-F16) | **projection artefact**: recovered by the hub frame (GT-F28) |
| Saturated PATH cells (GT-F14) | **confounded** by X-saturation |
| No emergent centre (GT-F22) | negative at N≤6, one competing-motif grade pair |
| Local persistence above global in sparse cells (GT-F23) | observed; mechanism open (GT-Q06) |
| KL projection for saturated gradient cells | **methodological failure**: unreadable (GT-F24) |
| CLOSE/HOLD/SPLIT, absent-literal compilations | **representational** equivalences |

## 6. E0B → E0C decision: stop

After E0B, the one consequential ambiguity is whether the selective basin-with-arrow survives as N grows (GT-Q07). Its margin falls from +0.047 to +0.009 between N=5 and N=6.

Answering that needs N ≥ 7: 262,144 HELD states and 840 path rule instances, beyond the laboratory's per-state Python kernel builder. A vectorised template kernel, validated against `build_kernel`, is new machinery. It is already on the roadmap for G2.

Further composites at N ≤ 6 would only move W4 grades toward a larger attachment margin. That is outcome tuning, so it was not done. The round sequence stops under OTR §4 ("identified a barrier requiring substantial new machinery"). The stop is recorded as GT-F32 and journey step 8.

## 7. RS / global-coherence interpretation [RS]

These are interpretations of model results under the CBO v2.4 baseline. They are not tests of it.

- **Admissibility and tendency.** The baseline distinguishes forbidding from favouring. E0 shows a third, orthogonal distinction inside favouring: whether a tendency is the gradient of a relational configuration function. Gradient tendencies make potentials: basins with no direction of succession. Non-gradient tendencies make a stationary order of succession.
- **Time as the ordering of actualisation.** This is a working interpretation, not a theory. In this grammar, ordering exists in every trajectory. A *directed* stationary ordering, one that distinguishes forward from backward in steady state, arises only from non-gradient constraint. Any RS account that ties temporal direction to constraint structure would need a non-gradient component. This is recorded as a proposal for review (ontology-proposals OP-5), not as an amendment.
- **Persistence and identity.** The handover motif is a candidate relational form of "conditioning other actualisations": an attachment to a reference structure is followed by the release of the peripheral relation that supported it. It ties to the laboratory's open CL-Q05 (transition-enabling dissolution).
- **Spatiality.** Direction of succession was legible relative to an emergent reference (the current hub) as well as an imposed one. That is weak support, in-model only, for the proto-spatial family of options, in which reference arises from configuration. It says nothing about metric distance (S-DIST is untouched).
- **G1's clock constraint is sharpened.** The earlier record says an RS account linking clock rates to a potential needs an added principle linking kinetics to potential. E0 adds two things. First, local activity can be independent of occupancy altogether (COMPETE, PCOMP). Second, under irreversibility, kinetics feeds back into occupancy itself (H-KO). So "potential" and "rate" are not separable primitives once direction exists.

**Not claimed:**
- that gravity is a relational potential;
- that the arrow of time is a non-gradient constraint;
- that the held source is mass;
- that the toy shells are distances.

[P] No physical comparison was made in E0. [T] The design premise is upstream, and it is neither tested nor supported.

## 8. Cross-programme links (Constraint Laboratory)

These are proposals only. No laboratory record was edited.

- **CL-T18 / CL-T19** (autonomous factorisation). GT-F12 is a pair-coupled generalisation of the reversibility-type structure: incidence-reading single-witness templates are reversible Gibbs. Proposed laboratory question: *does every label-covariant single-witness K≤3 composition at O=3 also give a triple-local Gibbs law?*
- **CL-Q04** (breaking incidence silence). Two-witness asymmetric templates are the minimal ordinary-grammar mechanism found here that breaks reversibility, not merely factorisation. Proposed as a refinement of CL-Q04.
- **CL-Q05** (transition-enabling dissolution). The handover (GT-F15, GT-F29) is a concrete stationary instance and is proposed as evidence for CL-Q05.
- **CL-N01** (apparent memory depends on clock). GT-F20 and GT-F30 extend clock dependence to relaxation order and to the sign of a rate ratio.
- **CL-M01** (compilation before ontology claims). Satisfied: every E0 mechanism is ordinary current-state grammar.
- **8H** (history as state). E0 shows that a directed order exists at H=0 when rules are non-gradient. So any 8H claim that history is needed for direction should be checked against non-gradient H=0 compilations. Proposed for the 8H reviewers; nothing on 8H was touched.

## 9. Completion questions

**1. What was explored, and why was that a good open-thetical choice?**
- The boundary between gradient and non-gradient constraint in the existing grammar: cooperating, opposing and competing compositions; soft and hard repulsion; attractive-plus-non-gradient composites; an emergent reference frame. HELD and FREE throughout, N=5 and 6, exact.
- Why it was a good choice: the audit showed that every G0/G1 basin lay on one side of that boundary. Crossing it could illuminate several lenses at once: D, B, C, K, E, R and X. It also needed no new primitive, and nulls were informative: no arrow would itself have been a finding.

**2. What was actually observed, including weak and unexpected behaviour?**
- Gradient constraints never produce a stationary arrow. Non-gradient constraints do, and it takes the form of a source- or hub-relative handover.
- Equal local ratios give different occupancies under irreversibility, and the dissolution-acting term is more selective.
- Activity can concentrate near the source with no basin at all.
- A frozen expectation failed through saturation. The KL projection failed numerically in saturated cells.
- No emergent centre formed.
- Basin and arrow coexist only weakly, in one composite, with a margin that shrinks with N.

**3. How did E0A change the choice of E0B?** These E0B choices would not have been made beforehand:
- Composites of attractive closure with exactly the two non-gradient components that E0A found unsaturated. The favour-sign components were dropped because E0A showed they saturate.
- Equal-ratio pairing inside the composites, because E0A's O5 showed equal ratios no longer fix occupancy.
- PCOMP, because E0A raised the question of whether the arrow belongs to the rules or to the ratio.
- The hub-frame channel, because E0A's FREE arrow was invisible in the class-free projection.
- Strong PATH grades and density-offset desaturation were explicitly rejected, both on E0A's evidence.

**4. Which candidate mechanisms were illuminated, and which assumptions weakened?**
- **Illuminated:**
  - H-R (stationary arrow needs non-gradient support);
  - H-KO (kinetics sets occupancy under irreversibility);
  - the handover;
  - activity-without-basin;
  - the emergent-frame legibility of direction.
- **Weakened:**
  - the tacit G1 separation of basin (ratio) from kinetics (split), which holds only for reversible chains;
  - the reading of near-source slowing as generic (COMPETE and PCOMP speed up);
  - lens E at N ≤ 6 (no emergent centre);
  - the expectation that "gentle" grades avoid saturation.
- **Qualified:** basin and arrow are not exclusive, but their coexistence is fragile.

**5. Robust, fragile, confounded or representational?** See §5.

**6. What is the most informative next direction, and how does it connect?** The scale test of the handover and of basin–arrow coexistence. Its first step is a **vectorised, validated template kernel** that reaches N=7 (and N=8 where sparse). Then a frozen round should ask, at the same grades:
- whether the CSPH selectivity margin survives, vanishes or inverts (GT-Q07);
- whether the handover orientation and its hub-frame legibility persist;
- whether the equal-ratio occupancy gap grows (it grew from N=5 to N=6 in every pair).

The same kernel is what G2 (radial structure) needs. So this route also lets G2 be asked properly in a non-gradient setting, where the radial profile is not just a consequence of a known potential.

Connections:
- **Laboratory:** CL-Q04 and CL-Q05, and the O=3 Gibbs question (§8).
- **RS ontology:** the proposal that directed temporal ordering requires non-gradient constraint (§7, ontology-proposals OP-5).

The kinetic-convention study (GT-Q01) is now less informative than before. Under irreversibility, kinetics is no longer separable from occupancy, so a "convention" that makes rate a function of potential presupposes reversibility.

Roadmap: [`../docs/roadmap.md`](../docs/roadmap.md) §E0 and after.
