# Configurable held scaffold: semantics, witness census and validation (GT-P007)

*Deliverable 2. Written before the E4A freeze. Code: `constraint-lab/src/rs_constraint_lab/gt0.py` (`Scaffold`, `SCAFFOLDS`, `use_scaffold`, `source`, `held_pairs`, `held_slot_indices`, `free_slot_indices`, `attach_slot_indices`, `slot_classes`). Tests: `constraint-lab/tests/test_scaffold.py`, `test_gte4a.py`.*

## 1. Semantics

- **What a scaffold is.** A **scaffold** is a declared boundary condition: a set of pair relations held present, whose dissolution is prohibited (`dissolve(a-b) => prohibit`). This is exactly the mechanism used for the triangle since G0. It is **not** a grammar primitive.
- **Source set.** It is derived as the vertices incident on held edges, and is used **only by measurements**: attachment classification, distance to source, source frames, hub statistics.
- **Rules never read the scaffold.** Rates depend on it only through the held relations being present and non-dissolvable:
  - `gtkernel.weights` zeroes the dissolution of held slots;
  - `gt0.scaffold_expressions` lists exactly the held pairs;
  - the start state contains exactly the held pairs.
- **Non-held pairs are free, including ones whose endpoints are both source vertices.** The P3 closing chord (0,2) is such a pair. It is an ordinary free relation, class **C** in slot and event-order classes.
- **Measurement classes** (`gt0.slot_classes`):

  | Class | Meaning | When it occurs |
  | --- | --- | --- |
  | A | source–probe (attachment) | every scaffold |
  | S | held | every scaffold |
  | C | both ends in the source, not held | the P3 chord; never under K3, so legacy classes are unchanged |
  | P | probe–probe | every scaffold |

- **Free slots** = all non-held slots. The attachment fraction is attachments over present free relations, and the null baseline is r0 = k(N−k)/M with M = C(N,2) − K. For P3 this counts the chord as a free slot.
- **Symmetry group.** The automorphisms of the held graph: permutations preserving the held edge set, combined with any permutation of the probes.
  - K3: S3 × S(N−3);
  - P3: the endpoint swap × S(N−3);
  - K2: the swap × S(N−2).
- **Default.** The active scaffold defaults to **K3 on {0,1,2}**. `gt0.SOURCE` keeps its legacy value. Modules that are inherently triangle-specific and already published (`gtscale`, `gte3b`) are unchanged.
- **Identity in results.** Scaffold names appear in item IDs (`HELD-K2-N5-…`), and every result records its scaffold's held edges and source.

## 2. Scaffolds used

| Name | Held edges | Source | Probes (N=5) |
| --- | --- | --- | --- |
| K2 | (0,1) | {0,1} | 2, 3, 4 |
| P3 | (0,1), (1,2) | {0,1,2}; middle 1, endpoints 0 and 2 | 3, 4 |
| K3 | (0,1), (0,2), (1,2) | {0,1,2} | 3, 4 |

## 3. Witness census (analytic, from the template's ordered witnesses)

A path witness of slot (a,b) is (end ∈ {a,b}, c, d) with c, d ∉ {a,b}, c ≠ d, and (end,c) and (c,d) present. For an attachment slot (p,s), with p a probe and s a source vertex, the witnesses lying wholly inside the source need end = s and c, d ∈ source.

| Scaffold | Held-only (permanent) floor at each source vertex | With the free chord present |
| --- | --- | --- |
| K2 | 0, 0 | — |
| P3 | endpoints 1, middle 0 | 2 at every source vertex (the chord adds s–2–1 / s–0–1 at the endpoints, and 1–0–2 and 1–2–0 at the middle) |
| K3 | 2, 2, 2 | — |

**Proof sketch.**
- **K3:** for s, the ordered pairs (c,d) are (s′,s″) and (s″,s′), both made of held edges.
- **P3:**
  - at endpoint 0, (c,d) = (1,2) uses (0,1) and (1,2), both held; (2,1) needs (0,2), which is free;
  - at middle 1, both orders need (0,2), which is free.
- **K2:** a single other source vertex leaves no d.

Probe–probe slots have no wholly-internal witness.

`gte4a.witness_census` splits every (state, slot) witness count into:
- **held floor** (both edges held);
- **chord-internal** (all three vertices in the source, at least one edge free);
- **other** (a probe or another free edge involved).

Tests check:
- that the three parts sum to `gtkernel.witness_counts`;
- that the held floor equals the analytic floor at every state, for N=4, 5, 6;
- that P3 with the chord present has 2 internal witnesses at every source vertex.

**The floor is an explanation and a cross-check. It is never subtracted from a native kernel.**

## 4. Null geometry

| N | Scaffold | Held K | Free M | Attachment slots k(N−k) | Probe–probe slots | Non-held source-internal slots | r0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | K2 | 1 | 9 | 6 | 3 | 0 | 6/9 |
| 5 | P3 | 2 | 8 | 6 | 1 | 1 | 6/8 |
| 5 | K3 | 3 | 7 | 6 | 1 | 0 | 6/7 |
| 6 | K2 | 1 | 14 | 8 | 6 | 0 | 8/14 |
| 6 | P3 | 2 | 13 | 9 | 3 | 1 | 9/13 |
| 6 | K3 | 3 | 12 | 9 | 3 | 0 | 9/12 |

- These values are verified against the estimator: under NULL, `gtobs.held_observables` returns attachment fraction = r0 in both clocks, to 1e-12.
- Baselines are not interchangeable between scaffolds.
- K2 against K3 changes the number of source vertices. P3 against K3 keeps three source vertices but changes the held-edge count and adds a dynamic chord.

## 5. Validation before freezing

| Check | Result |
| --- | --- |
| Rule strings: exhaustive kernel equality with the independent DSL implementation (`build_kernel` on `rules_for` with scaffold prohibitions) | K2, P3, K3 × N=4, 5 × NULL, PATHF ws, PATHH wf, CSPH, PCOMP, CLOSEW: states, targets and weights identical |
| Relabelling covariance | The P3 kernel with middle 1 equals, after the vertex permutation (1 2), the kernel of P3 with middle 2, for all six families |
| Held edges never dissolve; free slots always toggle | NULL N=5, all three scaffolds: held weights 0, free weights > 0, reachable class = 2^M states |
| Automorphism group sizes | K3 12/36, P3 4/12, K2 12/48 at N=5/6; the class-table symmetry check passes under P3 and K2 |
| Reference implementation versus arrays under P3 | `gt0.held_observables` (kernel-based) equals `gtobs.held_observables` |
| Legacy default reproduces published triangle cells | All numerical values identical (tolerance 0) for E1 HELD-N5-W4-CSPH, E2A HELD-N5-PATHH-weak_favour, E3A HELD-N5-W4-PF-strong_suppress and E3B HELD-N5-CSPH. The only differences are the bookkeeping keys `item_id` (added at publication) and `e2a/alphabet` (added after E2A) |
| Full suite | 638 passed before the E4A module; the dedicated tests are listed above |

## 6. What was not changed

- **Unchanged:** the DSL grammar; every template; the alphabets; the published tables, plans and reports.
- **Not added:** no rule reads source labels, and no compensating or witness-correcting rule exists.
- **Not copied:** the E3B instrument (`gte3b.neutralised`) is not reused for E4A.
