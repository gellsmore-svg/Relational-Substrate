# E1 feasibility: HELD versus FREE at N=7

Prompt GT-P003, deliverable 4. Measured costs come from theorem-fixed fixtures only (`gtobs_fixtures.py`). Costs for scientific cells are **extrapolations**, labelled as such. Machine: 16 cores, about 8.7 GB available RAM, numpy 2.5.3. The pipeline is single-threaded.

## 1. Measured (fixtures)

Full `gtobs.analyse` pipeline: every published channel, the additions, the two-start stationary check, autocorrelation and the hub frame. No trajectories.

| Fixture | States | Stationary iterations (uniform start / point start) | Autocorrelation terms | Wall | Peak RSS | Solver check |
| --- | --- | --- | --- | --- | --- | --- |
| HELD N7 NULL | 262,144 | 1 / 577 | 467 | 136 s | 450 MB | two starts agree to 1.0e-13 relative |
| HELD N7 CLOSE strong_favour (gradient) | 262,144 | 537 / 575 | 320 | 136 s | 452 MB | L1 gap to the analytic Gibbs law 2.7e-16 |
| FREE N7 NULL | 2,097,152 | 1 / 673 | 542 | 1,512 s (25 min) | 3.2 GB | two starts agree to 1.3e-13 relative; symmetry check 0 |

Stage times, FREE N7 NULL:
- autocorrelation: 855 s;
- point-start stationary run: 330 s (0.49 s per iteration);
- class table, 5,040 permutations: 178 s;
- reversibility: 62 s;
- hub frame: 56 s;
- event order: 17 s.

Stage times, HELD N7:
- autocorrelation: 62–90 s;
- stationary: 31–59 s (0.05 s per iteration);
- every other stage: under 6 s.

The autocorrelation loop was later made allocation-free, which brought HELD N7 NULL from 90 s to 73 s. The table keeps the earlier, conservative figures.

## 2. How the fixtures relate to scientific cells

NULL starts at its exact stationary law, so its uniform-start run takes one iteration. That is not representative. Its point-start run, and the CLOSE gradient cell, are representative. The prompt warns that NULL is not representative of non-gradient composite chains, so the extrapolation uses the new solver's iteration counts on the published non-gradient cells at N = 5 and 6 (`provenance/e1-observables-validation.log`).

| HELD cell | Iterations N5 → N6 | Growth | FREE cell | Iterations N5 → N6 | Growth |
| --- | --- | --- | --- | --- | --- |
| CSPH | 191 → 395 | 2.07 | CSPH | 230 → 477 | 2.07 |
| CSPF | 171 → 335 | 1.96 | CSPF | 194 → 244 | 1.26 |
| CWPH | 152 → 349 | 2.30 | CWPH | 207 → 405 | 1.96 |
| CWPF | 131 → 253 | 1.93 | CWPF | 156 → 205 | 1.31 |
| PATHF weak_suppress | 116 → 210 | 1.81 | PATHF weak_suppress | 141 → 188 | 1.33 |
| PATHH weak_favour | 144 → 313 | 2.17 | PATHH weak_favour | 198 → 336 | 1.70 |
| CLOSEW | 268 → 435 | 1.62 | CLOSEW | 487 → 676 | 1.39 |
| NULL (point start) | 218 → 382 → 577 at N7 | 1.75, 1.51 | NULL (point start) | 316 → 479 → 673 at N7 | 1.52, 1.40 |

NULL's growth slows from N6 to N7, but the composites' growth from N5 to N6 was larger. The extrapolation therefore takes a growth factor of 1.5–2.5 from N6 to N7, and a further 3× safety margin for the round cap.

| Extrapolated (not measured) | Iterations per start | Stationary (two starts) | Autocorrelation | Other stages | Per cell | Memory |
| --- | --- | --- | --- | --- | --- | --- |
| HELD N7 design cell | 300–1,100 | 30–110 s | 60–200 s | under 15 s | **2–6 min** | about 0.45 GB |
| FREE N7 design cell | 500–1,700 | 8–28 min | 15–45 min | about 5 min | **30–80 min** | about 3.2 GB |

COMPETE (1,408 iterations at HELD N6) is the slowest published family. It is not proposed for E1. At the same growth it would take about 3,500 iterations per start: about 6 minutes in HELD, or about 1 hour of stationary solving alone in FREE.

**Convergence strategy.**
- Lazy power iteration until the L1 change < 1e-15 and the maximum relative change < 1e-13.
- A second run from a point mass must agree within 1e-10 L1.
- Residual ≤ 1e-12.
- Autocorrelation series to a relative term of 1e-13.
- Cap of 2,000,000 iterations. A cell that hits the cap, or whose starts disagree, is recorded as unresolved, not estimated.
- Saturated cells resolve fine: the relative criterion was designed on them, and reaches 1e-15 relative accuracy on states of probability 1e-12.

**Durability.** The E0 runners write each cell atomically with a `status.json`, and resume by skipping finished cells. An E1 runner would reuse that pattern (`gte0b.run`). A FREE cell of up to about 80 minutes is the unit of loss on interruption.

## 3. What each mode can answer

| Question | HELD N7 | FREE N7 |
| --- | --- | --- |
| Does CSPH's source selectivity survive (GT-Q07)? | Yes, directly | No: FREE has no source |
| Does the handover keep its orientation? | Yes, source-relative | Hub-relative only (GT-F28) |
| Radial structure, shells 1–4 (G2) | Yes | No source shells |
| Is the arrow legible relative to an emergent hub? | Hub frame is computed, but the source dominates hubs (null: hub includes a source vertex 89%) | Yes; the question E0B opened |
| Does a centre emerge without a scaffold? | No: a scaffold is imposed | Yes: hub ties, hub persistence (autocorrelation of the hub indicator), class occupancy |
| Equal-ratio occupancy gap | Yes | Yes |

**Neither mode is evidence for the other.** The disappearance of an imposed-source effect in HELD says nothing about unscaffolded organisation. A FREE hub is not a source.

## 4. Recommendation on FREE

FREE N7 is practical but not cheap. Four cells (NULL, CSPH, PATHH weak_favour, CLOSEW) are extrapolated at 2–5 hours of sequential computation with a 3.2 GB peak. Running two at once would fit in memory, but not with much margin.

- **If the FREE tranche is included**, run it after the HELD tranche, under its own wall cap (proposed 6 h). The HELD results are then complete even if FREE is interrupted.
- **If FREE is deferred**, these questions stay open: whether a centre emerges without a scaffold at N=7; whether the hub-frame arrow persists or grows (GT-F28); and how hub ties and hub persistence change with size. They could be asked later as a FREE-only round with the same machinery. They could also be asked at N=6, where autocorrelation and hub persistence are now available, so a cheap first look at hub persistence needs no N=7 computation.
