# GT-E5B reflection: mechanisms, negatives, method and next options

*GT-P010, 15 October 2026. Frozen plan `fc3ec7d`; results `fcb17ae`; consulted hub `38c2501`. Labels: [O] observed in the frozen tables; [T] theorem; [I] inference by the agent after seeing results; [L] limitation. Nothing here is physical.*

## 1. The accounts, family by family

The comparator is NK unless stated. "Both sizes" means the same sign at N=5 and N=6.

| Family | Pattern | Verdict | Accounts it supports |
| --- | --- | --- | --- |
| PCOMP | F_STAR, F_2PATH | [O] below NK in all three clocks, both sizes; far above ND | **H2, between-layer**: E5A's effect was layer traffic. Within-layer heterogeneity (the largest of any law, CV ≤ 0.59) does not add persistence |
| PCOMP | F_TRI | [O] slightly above NK (×1.04–×1.15); renewal at or below NK | H2 mostly; small residual (H6) |
| PATHF | F_STAR, F_2PATH | [O] above NK (= ND) in all clocks, both sizes; more departures and renewal than NK | **H1 (weak form)**: a labelled centre persists slightly longer *with* more partner replacement. Not identity, not a mobile reference |
| PATHF | F_TRI | [O] below NK on lifetime and renewal, both sizes | negative for H1 on triangles |
| PATHH | F_TRI, F_STAR | [O] above NK in all clocks, both sizes; F_STAR flickers less | H1 (weak) for these patterns; flicker (H4) does not explain them |
| PATHH | F_2PATH | [O] below NK, both sizes | negative |
| CSPH | F_TRI | [O] well above NK (L ×1.45–×1.67; renewal ×2.2–×2.6), with about double the flicker | mixed: closure-favoured within-layer structure (prevalence ×2 vs NK) plus **H4**. Renewal at \|S0\|=1 equals a departure (see §2) |
| CSPH | F_STAR | [O] longer in CT and JT, shorter in anchor events, fewer departures | **H5**: activity elsewhere inflates the global clocks |
| CSPH | F_2PATH | [O] CT longer, JT mixed by size, renewal below NK | H6 |
| CLOSEW | all | [O] ×1.02–×1.07 at N=5; F_2PATH reverses at N=6 (×0.92); renewal ≈ NK | **H3 + H2-between**: high prevalence and crowding traffic explain most of E5A's effect |
| NULL | all | [T] analytic control holds; NK = ND = NULL | — |

**H7 (surprises).**
1. [O] NK is not uniformly stricter than ND. CT persistence above the comparator rises from 18/30 (ND) to 21/30 (NK), and 28 of 90 lifetime classifications change, in both directions. PATHH's and CSPH's triangle and star rows move from below ND to above NK.
2. [O] For PATHF, NK and ND coincide. E5A's PATHF comparison was already traffic-matched.
3. [O] PCOMP, the law with the strongest within-layer rate unevenness, ends *below* NK. Within-layer unevenness can shorten, not only lengthen, entrance episodes.

## 2. Negative and qualifying results

- [T] **F_STAR complete renewal is structurally impossible** at N=5 and 6 for all laws (24 law-anchor sets per comparator). This is non-identifiability, not a dynamical negative.
- [T, I] **F_TRI renewal is weak when the entry set has one completer:** it is then the same event as that completer's departure. This covers 92–99% of entries under PATHF, PATHH and CSPH, where a single leg toggle can satisfy it. Large F_TRI renewal ratios there (CSPH ×2.2–×2.6) are not durable-reconstruction evidence. CLOSEW and PCOMP at N=6 have most entries with 3–4 completers, where renewal is a strong event; there, renewal ≈ NK.
- [O] Genuine negatives:
  - PATHF F_TRI below every comparator on renewal;
  - PCOMP F_STAR and F_2PATH and PATHH F_2PATH below NK;
  - CLOSEW F_2PATH below NK at N=6;
  - no unresolved channel and no failed frozen check.
- [O] E5A qualification, recorded append-only in the audit: intact motifs outlive ND in **2/30** rows (not 1/30), with 6/30 exact PATHF ties.

## 3. Methodological lessons

1. **Matching the right projection changes conclusions more than changing the clock.** 28/90 classifications moved from ND to NK; only 3/30 rows disagree across clocks.
2. **A comparator should match layer traffic, not just a mean rate**, whenever rates depend strongly on crowding. ND's single scale made PCOMP look ×25 persistent.
3. **Replacement observables need a feasibility theorem first.** Without T10, F_STAR would have reported "zero renewal" as if it were a finding.
4. **Renewal and departure coincide for single-participant entry sets.** Any future replacement test should report results by entry-set size and treat size-1 renewal as departure.
5. **Exact hitting problems were cheap.** Twelve items took about 3 minutes, so simulation was never needed.

## 4. Lens B (mathematical capability)

The grammar can produce labelled anchored properties that persist slightly beyond a layer-traffic-matched control while their partners turn over completely (PATHF centres; PATHH triangle and star). It can also produce large apparent persistence that a declared projection fully explains (PCOMP, CLOSEW). Every quantity used here is a generator/stopping-set functional with an explicit observer; no rule reads it.

## 5. Lens A (foundational bridge)

- **Clearer.** Continuity of an *operational property* through complete partner replacement is possible in FREE laws, and it can be separated from crowding traffic for some families. That is a prerequisite one would want before speaking of a self-maintaining reference.
- **Still absent.**
  - an unlabelled or mobile reference: the anchor is fixed by the analyst, and N ≤ 6 rules out permanent labelled centres;
  - interaction between two such organisations;
  - displacement;
  - any gravity-like reading.
- **Possibly unnecessary.** None identified.
- **Bridge-map change.** The "persistence through turnover" gap moves from *undefined* (E5A) to *defined and partially observed, comparator-qualified*. The identity gap stays open.

## 6. Cross-programme notes (for the handoff; no hub writes)

- **XQ::01.** NK is a stationary-conditional projection lift, the GT analogue of CL's Kpi on the projection K. It is not CL's matched-source construction: there is no hidden history, the clock is CT, the projection is edge count, and the lift is uniform within a layer.
- **XQ::04.** Renewal is a trajectory observable defined without a history axis (8G gate not engaged). It distinguishes renewal from flicker only for entry sets larger than one.
- **XQ::07.** Both programmes now use hitting and stopping-set functionals of a generator (CL: first return, MFPT, committors; GT: exit-before-renewal and departure). That is a shared kind of quantity, not a shared theorem.

## 7. What changed in the GT picture

- GT-F76 (flexible outlives ND, qualified) is now further qualified by NK: much of it is traffic.
- GT-F77 (PATHF centres) is strengthened in scope: it survives the stricter comparator and the local count, with more replacement.
- GT-F78/X-KINHET (rate heterogeneity suffices) is refined: the sufficient heterogeneity is between layers.
- GT-F80 (CLOSEW closure recovery) is weakened: mostly prevalence and traffic.

## 8. Next options (not executed)

| Option | What it would decide | Cost | Risk |
| --- | --- | --- | --- |
| **A. Durable renewal on the rows above NK** (PATHF F_STAR/F_2PATH, PATHH F_TRI/F_STAR, CSPH F_TRI): after renewal, P(survive k further local events with no original partner returning), reported by entry-set size | whether the surviving effects are reconstruction or flicker-assisted renewal | one extra observer set; minutes | small; same laws (exposed) |
| B. A within-layer arrangement control (match the joint law of k and the anchor's local degree) | whether PATHF/PATHH effects are anchor-neighbourhood kinetics (the account NK leaves open) | a new comparator with its own proofs | moderate: risk of over-fitting the comparator to the effect |
| C. No further round: consolidate E5A+E5B and hand off to the hub | — | none | leaves Q22's durability question open |

**Recommendation: A.** It is the smallest test of the main remaining ambiguity: are the surviving effects durable replacement, or renewal that flicker can satisfy? It needs no new comparator. C is a reasonable alternative if the author prefers to consolidate first. Neither is run under GT-P010.
