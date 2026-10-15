# Does anything persist through replacement? Local counts, a stricter control and entry-set tracking (GT-E5B)

*A plain-English report for the human researcher on prompt GT-P010, 15 October 2026.*
- *One frozen round, executed once:*
  - frozen plan `fc3ec7d`, plan_hash `c35bc3bb…d944`;
  - results `fcb17ae`, payload `0d307350d1ac…`;
  - consulted hub commit `38c2501` (read only).
- *Numbers are exact computations on finite models, not simulations. Tables: `round-e5b-tables.json`; per-row view: `gt-e5b-atlas.md`; definitions and proofs: `docs/e5b-definitions-controls-and-feasibility.md`.*
- *Nothing here is a body, a movement, a physical time or gravity. A "pattern" is a set of links tracked through an anchor the analyst chose; an "event count" is a count, not a duration.*

## The question

E5A found that flexible patterns often outlast ND, a stand-in with matched crowding and overall activity. It also found that PCOMP, whose long-run picture is identical to the no-rule system, could look 25 times more persistent than ND. So "outlasts the stand-in" could come from uneven activity rather than organisation.

E5B asked, on the same 12 laws and the three flexible patterns ("this link closes a triangle", "this vertex has ≥3 links", "this vertex has ≥2 links"):
1. Does the pattern still look persistent against a **stricter stand-in (NK)**? NK matches not only crowding but the full traffic between every pair of adjacent link counts.
2. Does it look persistent when we count only **events at its own anchor**?
3. Do its partners actually get **replaced**: does every partner it started with leave while the pattern holds?
4. How much of the partner turnover is **flicker**, a link undone at once?

## What did we learn?

**1. Most of PCOMP's "persistence" was traffic between crowding levels, not anything within them.**
- Against ND, PCOMP's "≥2 links" lasted ×25.2 (N=6) in model time. Against NK it lasts ×0.90, *shorter*.
- "≥3 links" goes from ×4.4 (ND) to ×0.82 (NK); both vertex patterns are below NK at both sizes in all three clocks.
- PCOMP has the most uneven activity *within* each crowding level of any law (coefficient of variation up to 0.59). Yet once traffic *between* levels is matched, that unevenness does not make it more persistent; it makes it slightly less so.
- So E5A's "rate heterogeneity" was heterogeneity across crowding levels. PCOMP is slow when sparse and very fast when dense, and ND, with one overall speed, could not match that.

**2. PATHF's small centre advantage survives every control.**
- For PATHF the two stand-ins are identical: PATHF only slows link formation, so ND already matched its traffic. E5A's "cleanest comparison" was in fact already the stricter one.
- "≥3 links" against NK:
  - lasts ×1.075 (N=5) and ×1.10 (N=6) in model time;
  - lasts ×1.18 and ×1.25 counted in anchor events;
  - loses more of its starting partners (×2.2 and ×1.8);
  - reaches its maximum possible partial replacement more often (×2.1 and ×3.7).
- "≥2 links": ×1.07 and ×1.04 in model time, ×1.15 and ×1.11 in anchor events; complete replacement ×1.66 and ×1.32.
- The triangle pattern stays *below* the stand-in, with fewer replacements (×0.53, ×0.41).
- The effect is small but consistent across sizes and clocks, and it comes with **more** partner change, not less.

**3. CLOSEW's strong E5A result was mostly crowding.**
- Against ND, CLOSEW's patterns lasted ×1.1–×2.8 longer. Against NK this shrinks to ×1.02–×1.07, and at N=6 "≥2 links" is *shorter* than NK (×0.92 in every clock).
- These patterns are present 70–91% of the time under CLOSEW at N=5 and 88–99% at N=6. That is exactly the prevalence confound the prompt flagged, and NK, which matches crowding traffic, absorbs most of it.

**4. Two other families show effects that survive NK, with caveats.**
- **PATHH:**
  - its triangle and "≥3 links" patterns exceed NK at both sizes, in all three clocks;
  - "≥3 links" also flickers **less** than NK (×0.74, ×0.71);
  - "≥2 links" is below NK.
- **CSPH:**
  - its triangle pattern exceeds NK strongly, ×1.67 and ×1.45 in model time;
  - complete replacement runs ×2.2 and ×2.6;
  - but flicker is also about double NK's, and see point 6 on what "replacement" means for triangles.
  - "≥3 links" is longer than NK in model time but **shorter** in anchor events, with fewer partner changes. The clock decides that classification.

**5. Complete replacement happens, and the stricter control mostly explains how often.**
- "≥2 links" can always replace both starting partners while it holds. The probability that it does so before the episode ends:
  - ranges from 0.021 (PATHH, N=5) to 0.755 (PCOMP, N=6);
  - is 0.077 and 0.194 under the no-rule system.
- Against NK, CLOSEW and PCOMP replace about as often as their stand-in (×0.83–×1.03). Their high replacement is traffic.
- Only PATHF's "≥2 links" (×1.66, ×1.32) replaces more than NK at both sizes among the vertex patterns.

**6. What counted, and did not count, as replacement.**
- **Counted:** a moment, inside the episode, when the pattern still holds and *none* of the partners it started with takes part. All current partners are then newcomers. The anchor itself never changes.
- **Not counted:** a partner lost in the very event that ends the episode; the anchor being replaced; any unlabelled pattern moving around.
- **Weak case: triangles.** Most triangle episodes start with one completing vertex (92–99% in the PATH and CSPH laws). Then "complete replacement" is the same event as that one vertex losing a link while another vertex completes the triangle. A single flicker can do it. CSPH's strong triangle replacement is therefore **not** evidence of durable reconstruction.
- **Not attempted:** we did not run the optional test that the replacement survives without an original partner returning.

**7. "≥3 links" can never replace all its partners at five or six vertices.**
- It always starts with exactly three partners, and there are only one (N=5) or two (N=6) other vertices. Complete replacement is **mathematically impossible**: it is labelled STRUCTURALLY_IMPOSSIBLE, not "not observed", and is not a sign that the rules fail to keep a star.
- The informative measure is the most replacement possible: one of three (N=5) or two of three (N=6) partners absent at once.

**8. Flicker is real, and mostly traffic.**
- After a partner change, the next event undoes it with probability 0.06–0.21. The no-rule baseline is 1/M: 0.10 at N=5 and 0.067 at N=6.
- Against NK, CLOSEW and PCOMP flicker about as much as their stand-in (×1.0–×1.1).
- PATHF's centres flicker more (×1.15–×1.49) and its triangle less (×0.85).
- CSPH flickers more on triangles and "≥2 links" (×1.3–×2.0); PATHH and CSPH flicker less on "≥3 links" (×0.69–×0.78).

**9. The three counts of time disagree in a few places, for understandable reasons.**
- Against NK, all three clocks agree in 27 of 30 rows. The three that disagree are all CSPH.
- Model time and the global event count weight episodes by how fast the whole graph moves. The anchor count ignores remote events.
- When CSPH's "≥3 links" is long in model time but short in anchor events, its anchor is relatively quiet while the rest of the graph is busy (account H5).
- **Switching comparator matters more than switching clock:** 28 of 90 lifetime classifications change between ND and NK, in both directions.

## The ten questions

| # | Question | Answer (table rows: `predicate_rows`; atlas sections by row id) |
| --- | --- | --- |
| 1 | PATHF's centre advantage and CLOSEW's result under NK and the local count? | PATHF survives unchanged (NK = ND; anchor-event ratios slightly larger). CLOSEW shrinks to a few percent and reverses for "≥2 links" at N=6. |
| 2 | Does PCOMP still look persistent against NK? | No: below NK for both vertex patterns at both sizes in every clock; triangles ×1.04–×1.15. Within-layer heterogeneity does not produce persistence beyond NK; between-layer traffic produced the E5A effect. |
| 3 | Can a feasible organisation replace all entry partners at once? | Yes, in all feasible classes (F_2PATH: every entry; F_TRI: 55–100% of entries). Probability 0.008–0.755 depending on law; mostly equal to NK; above NK at both sizes for PATHF F_2PATH, PATHH F_TRI and CSPH F_TRI. |
| 4 | Structurally impossible, unresolved, genuine negative? | Impossible: F_STAR complete renewal at N=5,6 (all laws). Unresolved: none. Genuine negatives include PATHF F_TRI (below every comparator on renewal), PCOMP and PATHH F_2PATH below NK, CLOSEW F_2PATH below NK at N=6. |
| 5 | How much turnover was flicker? Durable reconstruction? | Reversal 0.06–0.21 per change; at NK's level for CLOSEW and PCOMP, above it for PATHF centres and CSPH triangles, below it for PATHH/CSPH stars. F_TRI renewal with one entry completer equals a departure and can be met by flicker. Durability was not tested (filter not attempted). |
| 6 | Did clocks and comparators classify differently? | Clocks: 3/30 rows (all CSPH). Comparators: 28/90 lifetime classifications change ND→NK. |
| 7 | What transfers to CL? | Entry-set tracking and renewal are stopping-set (hitting) functionals of a generator; they transfer as definitions. NK is the GT analogue of CL's stationary-conditional projection, on edge count rather than history. The anchor-local count does not transfer as is: CL's clocks are event epochs with hidden triad events. |
| 8 | GT-Q21, GT-Q22, XQ::01, XQ::04, XQ::07? | GT-Q21 partially answered (NK plus local count discriminate E5A signals; within-layer arrangement still unmatched). GT-Q22 partially answered (renewal defined without a history axis; F_STAR non-identifiable at N ≤ 6; flicker can mimic triangle renewal). XQ::07: both programmes use hitting/stopping-set functionals of a generator; no common theorem shown. |
| 9 | What goes to the hub? | `docs/gt-p010-shared-synthesis-handoff.md`: provenance, the question matrix, two candidate connections (proposed only), and the intake commands for a separate, reviewed hub cycle. |
| 10 | Best single next step? | See the reflection §8: a durable-renewal test on the three rows above NK, or no further round. Not executed. |

## What this does not show

- It does not show a body, a moving or unlabelled reference, interaction between structures, displacement or gravity.
- A persistent anchored pattern is a property of a labelled vertex or link that the analyst fixed.
- E5B is a follow-up on laws whose E5A values were already exposed, not an independent confirmation.
- NK is one declared projection (onto link count). Effects that survive it may still reflect within-layer arrangements that no comparator here matches.

## Files

`gravity-time/plans/round-e5b-plan.json`, `reports/round-e5b-tables.json`, `reports/gt-e5b-atlas.md`, `reports/gt-e5b-reflection.md`, `docs/e5b-definitions-controls-and-feasibility.md`, `docs/gt-p010-hub-and-e5b-audit.md`, `docs/gt-e5b-cross-programme-transfer.md`, `docs/gt-p010-shared-synthesis-handoff.md`, `provenance/execution-GT-P010.md`.
