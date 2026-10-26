# GT Rounds G0 and G1 — relational basins and relative recurrence rates

Programme GT, Mode B. Two frozen rounds of exact kernel analysis on the O=2 pair grammar of the Constraint Laboratory: G0 (basin census) and G1 (recurrence rates). Nothing new was added: no primitive, no grammar, no metric, no clock beyond the declared conventions, no trajectory sampling.

| Round | Plan commit | Plan hash | Result commit | Tables |
| --- | --- | --- | --- | --- |
| G0 | `b45f10b` | `30fba33a…92a` | `97c2daa` | `round-g0-tables.json`, payload `7df3b521…25ca2` |
| G1 | `331d519` | `1707f178…67c4` | `3dccd0a` | `round-g1-tables.json`, payload `c1b18236…58d8` |

Both plans were committed and pushed before execution. Journey steps 1 and 3 have a null result commit, and steps 2 and 4 name the result commits. Tests pin the chronology and the payload hashes.

## 1. What was run

**G0** had 40 cells:
- N ∈ {5, 6};
- two modes: HELD, with the entities {0,1,2} held as a triangle (declared scaffold), and FREE, with no held structure;
- six label-covariant families, each instantiated over every witness:
  - NULL;
  - DENS: `form(a-b) => m`, K1;
  - ADJ: `form(a-b) | present(a-c) => m`, K2;
  - CLOSE: `form(a-b) | present(a-c) & present(b-c) => m`, K3;
  - HOLD: `dissolve(a-b) | present(a-c) & present(b-c) => m<1`, K3;
  - LOCK: the same as HOLD with `=> prohibit`, K3.

**G1** had 18 HELD cells: NULL, DENS, ADJ, CLOSE and HOLD at both grades and both sizes.

**Execution:**
- **G0:** 39 of 40 items ran, then the process was killed out of memory on `FREE-N6-LOCK`. The dense absorption matrix for 32,767 transient states does not fit. A post-freeze solver change (`226abe1`) switched sets above 4,096 states to an iterative solve. That path agrees with the dense path to about 1e-12 on every set small enough for both. Only the remaining item was run afterwards. This changed the solver, not an estimand.
- **G1:** 18 items, the largest taking 8.7 s.

**Pre-freeze exposure:** recorded in each plan. G0's implementation was exercised on N=4 fixtures, on N=6 FREE NULL (timing), and on N=5 FREE DENS (solver comparison only). G1 was exercised on an N=4 fixture.

## 2. Observations

**O1. Frozen G0 targets hold.**
- **T1:** DENS leaves the density-controlled attachment fraction (the share of present free relations that join a probe to the source) exactly at null, within 3e-14.
- **T2:** DENS leaves triangles given edge count exactly at the uniform conditional mean, within 5e-13.
- **T3:** NULL is uniform.
- **T4:** LOCK is absorbing in both modes, and its only absorbing state is the complete graph.

**O2. Relational selectivity beyond density.** ADJ, CLOSE and HOLD raise the attachment fraction above null under both clocks. Examples are CLOSE-weak at N=5 (0.8601 against 0.8571) and HOLD-weak at N=5 (0.8671). The margins are small, and they shrink toward null at strong grades as the graph saturates toward complete. In FREE mode, CLOSE and HOLD raise triangles given edge count well above the uniform law (up to 2.6× at low edge counts). ADJ raises it slightly, and DENS not at all.

**O3. The frozen drift criterion is confounded.** DENS passes the "inward drift beyond null" criterion purely by densification: its shell-2 drift is −0.68 against the null's −0.43 at N=5. Continuous-time drift is per unit time, so it scales with total rate, which per-witness multiplication makes very large for ADJ (−12,269 at N=6). So the frozen labels "relational_basin / partial / clock_dependent" are reported as computed, but they rest on the attachment criterion. The drift criterion does not separate attraction from density.

**O4. Retention, not approach.** At N=5, HOLD's continuous-time frontier drift equals NULL's exactly (−3.0). Its jump-clock inward drift is entirely normalisation: suppressed dissolution makes formations a larger share of each event. Its basin comes from reduced escape of supported relations.

**O5. A relational potential.** This is a reading taken after G0 and verified on fresh kernels. For every template, the continuous-time stationary law is

```text
pi_ct(x) = m^S(x) / Z
S = edges (DENS), wedges (ADJ), triangles (CLOSE, HOLD with m -> 1/m)
```

within 9e-15. This is the standard detailed-balance construction of an exponential-random-graph law. CLOSE(m) and HOLD(1/m) share one stationary law, and G1 confirmed that to gap 0.

**O6. Capture and arrest.** LOCK is certainly absorbed into the complete graph, after an expected 8.9 (HELD N=5), 14.6 (HELD N=6), 15.2 (FREE N=5) and 20.5 (FREE N=6) events. At that state no event is admissible and nothing further happens.

**O7. G1 predictions.**
- P1 (shared continuous basin) holds, gap 0.
- P3 (the jump clock separates the pair) holds.
- P2 failed in 3 of 4 cells. P2 predicted that CLOSE raises and HOLD lowers the continuous-time near/far activity ratio ρ = A(shell 1)/A(shell 2). HOLD lowers it in every cell. CLOSE also lowers it in three cells, and raises it only at N=5 weak (1.034).

**O8. Near-source slowing.**
- ρ < 1 in all 16 non-null cells under the jump clock, and in 15 of 16 under the continuous clock, including the density control.
- At one shared stationary law (N=5, strong grades), CLOSE gives ρ_ct 0.637 and HOLD 0.039. At N=6 they give 0.262 and 0.011.

**O9. Inward share.** Among probe-distance-changing moves, the inward share at shell 2 is above null for every non-null family, DENS included. That follows from the observable's construction: inward moves are formations.

## 3. Inferences

**I1. Basins in the existing grammar are potentials.** A basin-like stationary concentration around a held relational structure arises from minimal label-covariant templates, with no metric, direction or source named in any rule. The mechanism is a relational potential. Each template is equivalent, under continuous time, to a scalar function of the configuration (a count of edges, wedges or triangles), and stationary occupancy favours configurations of high potential. Attachment to the held triangle raises the triangle and wedge counts, so it is favoured. The source is "attractive" because of how it participates in the counted motif, not because of any rule about it.

**I2. Only incidence-reading templates give selectivity.** Selectivity beyond density requires a template that reads incident relations: ADJ (K2) or a closure motif (K3). DENS cannot produce it, as CL-T18 and T1 predicted. This partly answers CL-Q04: these pair-coupled templates break the autonomous factorisation. K3 closure is not needed for selectivity, since ADJ also gives it. It is needed for triangle clustering beyond the uniform conditional law, which ADJ barely produces.

**I3. Admissibility and tendency are kinetically distinct.**
- Hard admissibility (LOCK) produces capture and total arrest, not a stationary basin.
- Soft admissibility (HOLD) and tendency (CLOSE) can share an identical stationary law and differ only in kinetics: retention versus approach.
- The A→D question has a precise answer here. Soft admissibility yields a statistical tendency in occupancy, but not in approach rate under continuous time. The jump-clock appearance of approach is normalisation.

**I4. A shared basin does not fix a clock signature.** Within this model, near-source slowing of local activity accompanies every basin tested, the density control included, so it is an occupancy effect: relations already in their favoured state leave it at the slow rate. Its magnitude is set by kinetics, not by the stationary potential. CLOSE and HOLD share π exactly and differ by a factor of about 16 in ρ_ct. H-U is therefore supported only in a weak form: the constraint that makes the basin also changes relative recurrence rates. It is contradicted in the strong form: the rate change is not determined by the basin.

**I5. Conclusions depend on the clock.** Stationary attachment, drift and activity differ between the jump clock (lab kernel normalisation) and the continuous clock. Both are declared scaffolding, and neither is privileged by the model. Any temporal claim must name its clock.

## 4. RS / global-coherence interpretation

Inside this model, three proposals of the RS baseline become concrete and are distinguished:

- relational primacy: a basin with no primitive centre or direction;
- the admissibility/tendency distinction: capture versus retention versus approach;
- time as the ordering of actualisation: clock-dependent rates.

The model offers a candidate reading of "potential" as a function of relational configuration, derived from rule weights, not imposed.

It also records a constraint on any RS account of gravitational clock rates. In physics the clock-rate difference is fixed by the potential. In this grammar it is not: the same potential admits very different rate signatures, depending on how the weights are split between formation and dissolution. An RS account in which clock rates follow from a relational potential would therefore need an additional principle linking kinetics to potential, such as a symmetric splitting of the weight between the two directions. It is not supplied by the current grammar. This is recorded as a proposal for later review, not as an amendment.

Nothing here shows that gravity is a relational potential, that nature uses these templates, or that the toy shells are physical distances. The held source is scaffolding, and relational distance is a derived observable. The design premise is upstream of all this and is neither tested nor supported by it.

## 5. Negative and null results

- The frozen G0 drift criterion does not discriminate attraction from density (O3).
- P2 failed in 3 of 4 cells (O7).
- No family produced a basin without the declared held scaffold in a way that distinguishes a centre: FREE mode shows clustering, not localisation.
- At strong grades the graph saturates, and relational selectivity vanishes into near-completeness.
- LOCK produces arrest, not a basin.

## 6. Open questions

- **Kinetic convention:** is there a principled rate rule under which local recurrence rate is a function of the relational potential alone, and what would justify it ontologically? The candidates are a symmetric √m split and a heat-bath rule.
- **Radial dependence (G2):** at N=7, after a vectorised, validated kernel, does attachment or activity have a stable dependence on relational distance across several shells?
- **Source dependence (G3):** does basin depth scale with the held structure's motif content (triangle, 4-clique, path)?
- **Unscaffolded localisation:** can a basin with a centre emerge in FREE mode, for example by symmetry breaking in finite-time occupancy?
- **Arrest as a limit on event succession:** does total admissibility arrest bear on the open candidate T-LIMIT?
- **Inertia and free fall:** at H=0 the next-step law depends only on current relations. Is a velocity-like register (H>0) needed, under the laboratory's compilation test?
