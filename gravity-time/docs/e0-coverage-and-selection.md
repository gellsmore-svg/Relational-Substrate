# GT-E0 coverage, novelty and E0A selection audit

Prompt GT-P002, method OTR 1.0. Written on 2026-10-14 before any E0A code, plan or scientific cell. Branch head at writing: `62d53fa`, which descends from the G0/G1 close-out `f6b3d24`.

## 1. Live baseline, verified

- **Branch.** `research/gravity-time-admissibility` was clean, and local equalled remote at `f6b3d24`.
- **PR #6.** Open draft against `research/constraint-lab-v0.8g-formal-integration`. CI runs `38475547258` and `38475181462` both passed (constraint-lab, books).
- **Local suite.** 319 tests passed in 128 s (`constraint-lab/.venv`, numpy 2.5.3, no scipy).
- **8H.** `research/constraint-lab-v0.8h-history-as-state` has 7 commits beyond 8G. The last is `e9f8f3b` (2026-10-13 22:12, "freeze H0 plan before non-neutral history calculations"). It has not closed. GT is not rebased onto it and reads nothing from it as a result.
- **CBO.** The v2.4 research baseline (`main`) is read as an interpretive constraint only, as charter §2 records. Nothing from it enters a rule.

## 2. What has been explored

### 2.1 Constraint Laboratory (read-only)

| Strand | Cell / scope | What it settled that bears on GT |
| --- | --- | --- |
| Gen 1–7B (Mode A) | Pair and triad grammars N≤5, K≤3, W4 grades | Catalogue of motifs; controlled passage survives occupancy matching (CL-N02); apparent memory depends on clock (CL-N01) |
| Gen 8 (Mode B) | N=4, O=3 independent hypergraph, sampled trajectories | Edge-count layer organises occupancy; sampled routes share motifs; no private route per system |
| 8A / 8B | Context repair; information calibration | Plug-in MI from trajectories is estimator bias until a permutation null or the exact kernel says otherwise. **Lesson for GT: report exact kernel quantities; trajectories are illustrations** |
| 8C–8F | Local gate geometry, two-gate algebra, K3 conjunctions, interaction→topology | Additive log-weight grammar; K3 carries the gate-by-gate term K2 pairs cannot (CL-F02); incidence motifs conjugate under hidden-bit permutation (CL-F04) |
| 8G | Formal integration | CL-T18 autonomous factorisation, CL-T19 shape-given-edge invariance, CL-T20 lumpability, CL-M01 compilation test, open CL-Q04 (breaking incidence silence) and CL-Q05 (transition-enabling dissolution) |

### 2.2 GT G0 and G1

| Axis | Covered |
| --- | --- |
| Grammar cell | O=2 pair DSL, H=L=G=S=0, W4 factors |
| Sizes and modes | N ∈ {5, 6}; HELD (triangle {0,1,2}, source dissolution prohibited) and FREE |
| Rule families | NULL, DENS (K1), ADJ (K2 form), CLOSE (K3 form), HOLD (K3 dissolve, soft), LOCK (K3 dissolve, hard), each at weak and strong grades where graded |
| Compositions | None. Every G0/G1 cell is one template family, plus the scaffold in HELD |
| Signs | Formation favoured, and supported dissolution suppressed or prohibited. No formation suppression, no dissolution favour, no hard prohibition of formation |
| Observables | Class structure; jump and continuous stationary laws; attachment fraction, also conditioned on free-edge count; distance distribution; radial drift; escape and capture; triangles given edge count; absorption; shell activity, near/far ratio ρ, inward share |
| Kinetic observables | Stationary rates only (G1). No relaxation spectrum, no autocorrelation, no probability current, no event-order statistics, no trajectory sampling |

## 3. A reanalysis that needs no new computation

This is a mathematical inference, layer 2. It was made while writing this audit, from the G0 template definitions; no new cell was run. It explains G0 observation O5 and extends it.

**Claim.** Every label-covariant template on the O=2 pair grammar whose condition reads only the two relations joining the toggled pair (a,b) to one witness c is a reversible chain, and its continuous-time stationary law is a triple-local Gibbs law. This holds for form rules, dissolve rules, mixtures of them and any finite composition, in HELD and FREE modes.

**Argument.**
1. For the toggle of relation ab, call the product of all form-rule factors f and the product of dissolve-rule factors d. Per-witness instantiation makes the rate ratio r_ab(x) = f/d a product over c of φ(x_ac, x_bc).
2. Label covariance requires φ(u,v) = φ(v,u), so φ depends only on s = u + v ∈ {0, 1, 2}.
3. Take a potential ψ on vertex triples that depends only on the number k of present relations in the triple. Set ψ(1+s) − ψ(s) = log φ(s). That fixes ψ up to a constant, and H(x) = Σ over triples of ψ(k_triple) satisfies r_ab(x) = exp(H(x+ab) − H(x)) for every pair and state.
4. So Kolmogorov's criterion holds, the chain satisfies detailed balance, and π_ct ∝ exp H.

Because Σ over triples of ψ(k) is a linear combination of edge, wedge and triangle counts, this is exactly G0's O5: π_ct ∝ m^S with S an edge, wedge or triangle count. It generalises to every single-witness K≤3 composition. The HELD scaffold only freezes three coordinates, and that preserves detailed balance on the reachable class. Hard prohibition of a formation restricts the chain to a closed set on which the remaining rates still satisfy the criterion. The general fact, that local Glauber-type dynamics with gradient rate ratios are reversible with exponential-random-graph laws, is standard. The application to this grammar is the new step.

**Consequences for G0/G1, before any new run:**

- **No arrow.** Every G0 and G1 cell is reversible. None can show a stationary probability current, an irreversible-looking event order in stationarity, or oscillatory relaxation; the generator spectrum is real. Lens D (directional tendency) was observable in G0 only as stationary occupancy, never as stationary direction of succession.
- **Kinetic freedom.** G1's finding that CLOSE(m) and HOLD(1/m) share π is a special case: any two compositions with the same r_ab share π_ct. Within this class the stationary law is fixed by the ratio, and everything else is kinetics.
- **Absent literals add nothing new.** An absent literal is 1 − present, so `form(a-b) | absent(a-c)` at factor m is DENS(m^(N−2)) composed with ADJ(1/m). Different syntax, same kernel (CL-T09 Möbius basis).

**Where the class ends.** A template whose condition uses two witnesses in asymmetric roles is not covered. An example is `form(a-b) | present(a-c) & present(c-d)`, with c,d ∉ {a,b} and c ≠ d. Analytically:
- Let P(ab) count, over both endpoints, the 2-paths leaving that endpoint into the rest of the graph.
- Δ_ac P(ab) = #{d : cd present}, while Δ_ab P(ac) = #{d : bd present}.
- These differ whenever deg(c) and deg(b) differ outside {a,b,c}.
- So the elementary square (x, x+ab, x+ab+ac, x+ac) has non-unit cycle affinity, and the chain is **not** reversible.

The template is K3, label-covariant and uses only present literals: it is inside the existing grammar.

This identifies the largest untouched region adjacent to G0. It is the boundary between **gradient (potential) dynamics**, which is all G0 explored, and **non-gradient dynamics**, which the grammar admits but no GT cell has entered.

## 4. Novelty map

| Region | G0/G1 | Reanalysable without computation | E0A candidate |
| --- | --- | --- | --- |
| Single-witness formation favour (ADJ, CLOSE) | covered | π law (§3) | anchor only, for new observables |
| Supported-dissolution suppression (HOLD), hard (LOCK) | covered | π law, LOCK absorption | HOLD anchor; LOCK exhausted |
| Formation **suppression**, the repulsive mirror | not covered | π law predicted (§3) | yes |
| Hard prohibition of **formation** (exclusion without arrest) | not covered | π uniform on a restricted class (§3) | yes |
| Opposing form and dissolve on one motif (cancelling ratio) | not covered | π uniform (§3); kinetics unknown | yes |
| Same-π kinetic triad (approach / retention / symmetric split) | two of three covered | π shared (§3) | yes, as one cell |
| Competing motifs (wedge favour against triangle cost) | not covered | π law (§3); shape unknown | yes |
| **Two-witness, non-gradient templates** | not covered | reversibility broken (§3); nothing else known | yes, the central new region |
| Relaxation spectrum, autocorrelation, centre persistence | not observed | real spectrum for gradient cells (§3) | new observable channel |
| Probability current, entropy production, event-order asymmetry | not observed | zero for every gradient cell (§3) | new observable channel |
| Replayable trajectories | none in GT | — | illustrative atlas |
| N=7 radial structure (G2) | not covered | — | not chosen (§7) |
| History register H>0 | not covered | — | not chosen: 8H is open, and CL-M01 applies |

## 5. Lens register used to select E0A

These lenses are kept plural. None is a target.
- **D**, directional tendency.
- **A**, asymmetric admissibility.
- **A→D**, derived tendency.
- **B**, basin by retention.
- **C**, coordination or competing rules.
- **K**, kinetic freedom.
- **E**, emergent source and proximity.
- **X**, artefact families: density, imposed source, boundary, finite-state saturation, clock normalisation, projection, estimator.

One lens is added from §3:

- **R, stationary arrow from non-gradient constraint.** In a stationary state, a directed succession of relational change (cycle currents, event-order asymmetry, complex relaxation modes) arises only when the local rate ratios are not the gradient of any configuration function. R is a mechanism lens. It does not claim that any physical arrow of time is of this kind.

## 6. E0A selection

All rules are ordinary O=2 DSL text, instantiated over every ordered witness.

| Id | Template(s) | Grade(s) | Why it is informative | What a null would teach |
| --- | --- | --- | --- | --- |
| NULL | none | — | baseline for every new observable | — |
| CLOSE | `form(a-b) \| present(a-c) & present(b-c)` | strong | G1 anchor (approach kinetics), now seen through the new channels | — (a gradient cell) |
| HOLD | `dissolve(a-b) \| present(a-c) & present(b-c)` | strong | G1 anchor (retention kinetics) | — |
| SPLIT | CLOSE + HOLD | weak + weak | the third kinetics at the same π as CLOSE-strong and HOLD-strong. This completes the kinetic triad (lens K) as one cell, not as a programme | if the observables of the three coincide, kinetics is unobservable in them |
| COMPETE | CLOSE favour + `dissolve(a-b) \| present(a-c) & present(b-c)` favour | strong + strong | opposing rules cancel exactly in π (§3), but not in rates. Is there "activity structure without a basin" (C, K, X-CLOCK)? | if near-source activity equals far, kinetics follows occupancy |
| ANTI | `form(a-b) \| present(a-c) & present(b-c)` | strong_suppress | the repulsive mirror of CLOSE. Does a held structure repel, and is attraction sign-symmetric (D, E)? | if attachment equals null, closure is not what makes the source matter |
| EXCL | the same with `prohibit` | — | hard exclusion of formation: admissibility without arrest (A, A→D). Contrast with LOCK's capture | if nothing distinguishes it from ANTI-strong, hard and soft are equivalent here |
| FRUST | `form(a-b) \| present(a-c)` (and b-c) favour + closure-supported dissolve favour | weak + strong | competing motifs: wedges rewarded, triangles cost two wedge-units each (C, E). The grade pair is chosen in advance by motif arithmetic so that neither term dominates trivially on K_N or on star or bipartite graphs. It is not tuned on outcomes | if it behaves like ADJ, the closure cost is inert |
| PATHF+ | `form(a-b) \| present(a-c) & present(c-d)` | weak_favour | **non-gradient** formation favour from second-neighbourhood support (R, D, A→D, E) | if there is no current or event-order asymmetry, non-reversibility is invisible at these scales |
| PATHF− | the same | weak_suppress | non-gradient, opposite sign | as above |
| PATHH+ | `dissolve(a-b) \| present(a-c) & present(c-d)` | weak_suppress | non-gradient **retention**. It has the same local ratios as PATHF+, so does it share π? (In the gradient class, sharing is guaranteed.) (B, K, R) | if π is shared, the ratio still fixes occupancy despite irreversibility |
| PATHH− | the same | weak_favour | non-gradient dissolution promotion | as above |

The cross product is 12 family-grades × {HELD, FREE} × {5, 6} = **48 exact cells**.

PATH families use the weak grade only. A K3 two-witness template has 2(N−2)(N−3) witnesses per pair, so the strong grade would multiply rates by up to 4^24 at N=6. Saturation at strong grades was already a G0 finding (O2), and it removes selectivity. This choice is made from witness arithmetic, before any PATH computation.

### Complementarity

The 12 entries form four contrasts:

1. **Gradient against non-gradient** at comparable grade: CLOSE/HOLD/ANTI against PATH.
2. **Formation against retention at equal local ratio**: CLOSE vs HOLD (gradient) and PATHF+ vs PATHH+ (non-gradient). This asks whether the G1 shared-basin identity survives irreversibility.
3. **Cooperating, opposing and competing compositions**: SPLIT, COMPETE and FRUST.
4. **Soft and hard repulsion**: ANTI and EXCL.

HELD against FREE separates scaffold effects from what the rule does unaided.

## 7. Not chosen for E0A, and why

- **G2 radial study at N=7.** Its observables (drift, attachment by shell) were shown in G0 to be dominated by density and normalisation. In the gradient class the radial profile is a consequence of an already-known potential. Building an N=7 vectorised kernel first would spend effort on the region §3 already explains.
- **Focused G1 kinetic-convention study** (a √m split or heat-bath rule). It stays a candidate. One cell of it (SPLIT) is included, so E0A can show whether kinetic splitting is even visible in the new channels before the question is focused.
- **G3 source dependence.** It is still a basin-depth question inside the gradient class, with predictable π.
- **History register H>0.** 8H is open and owns the history-witness question. GT should not pre-empt it (CL-M01).
- **Strong PATH grades, LOCK, DENS, ADJ.** Saturation, exhausted cells, and controls whose new-channel values are fixed by §3 (zero current, real spectrum).
