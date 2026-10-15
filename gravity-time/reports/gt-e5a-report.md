# Does anything last on its own? FREE persistence at five and six entities (GT-E5A)

*A plain-English report for the human researcher on prompt GT-P009, 15 October 2026.*
- *One frozen round, executed once:*
  - frozen plan commit `1dc43c6`, plan_hash `31202d70…97a8`;
  - results commit `59eb682`, tables payload `6e978571d83e…`.
- *File references are at the end. Numbers are exact computations on finite models, not simulations.*
- *Nothing here is a body, a movement or a physical time. A "pattern" is a set of links; "time" is the model's clock.*

## The question

**Background.** Every earlier round held a reference in place by decree: a triangle, or another fixed shape that could never dissolve. GT-P008 showed that, in a finite system where every link can change, nothing can stay "the centre" forever. So a reference the system makes for itself could at best be *long-lived*.

**This round's question.** With nothing held fixed, do the existing rules keep any recognisable pattern going longer than a fair comparison would? And can a pattern survive while some of its own links change?

**Patterns tested.** We looked at two kinds:
- **Intact patterns:** a specific triangle, star or two-step path, where every named link must be present.
- **Flexible patterns,** each tracked through a marked vertex or link:
  - "this link still closes some triangle";
  - "this vertex still has at least three links";
  - "this vertex still has at least two links".

  The partners may change while the pattern holds.

**Measurements.** For each pattern we measured three things:
- how long an episode lasts, counted both in model time and in number of events;
- how often it appears;
- how many of its participating links change while it lasts.

**Comparators.** Two:
- **N0:** the no-rule system;
- **ND:** a declared stand-in process with the same distribution of link counts and the same overall activity as the rule set under test.

**Hub control.** Separately, we picked the busiest vertex at one moment and followed it, to see how quickly its advantage fades.

## What did we actually learn?

**1. Intact patterns do not outlast the fair comparison in model time.**
- Across 30 intact cases (5 rule sets × 2 sizes × 3 patterns), a specific triangle, star or two-step path lived longer than the matched stand-in in model time only once: the star under PATHH. That was by 0.4% at five entities and 9% at six.
- The mathematics explains why. An intact pattern cannot survive the loss of any of its own links, so it lasts exactly as long as its weakest link holds.
- Under the two rule sets that only change how links *form* (PATHF, CLOSEW), every link breaks at the plain rate. A triangle therefore lasts exactly one third of a time unit, whatever the rules do. Its survival reflects how fast links break, not any organisation.

**2. Flexible patterns often outlast the stand-in, but the round's own control shows how that can happen with no organisation at all.**
- In 18 of 30 flexible cases the pattern lasted longer than the stand-in in both clocks, and in 28 of 30 more of its links changed during an episode.
- The largest effects were under PCOMP. At six entities, "this vertex has at least two links" lasted 25 times longer than in the stand-in, with 199 link changes per episode against 5.5.
- **But PCOMP's long-run picture is exactly the same as the no-rule system's.** Every arrangement of links is equally likely. Its stand-in has:
  - the same long-run picture;
  - the same average link lifetime (this is forced: see point 6);
  - the same overall activity.

  What differs is *where* the activity happens. PCOMP's links flicker very fast in crowded neighbourhoods and change slowly elsewhere.
- So "lasts longer than the matched stand-in" can be produced purely by uneven activity, with no preference for any structure. **This is the main unexpected finding.** The stand-in we agreed in advance controls crowding and average activity, but not how activity is spread out. Lifetime contrasts against it can confuse organisation with unevenness.

**3. The cleanest comparison shows a small effect for "centres" and none for triangles.**
- PATHF only slows formation, so every link breaks at the plain rate. Its stand-in then matches it in crowding (in both clocks), in overall activity and in how links break. Only the formation rule differs.
- Against that stand-in:
  - **"this vertex has at least three links"** lasted 7.5% longer at five entities and 10% longer at six (model time), and 1–5% longer counted by events, with about twice as many partner changes per episode;
  - **"at least two links"** lasted 4–7% longer;
  - **triangle patterns did not last longer:** the flexible triangle was 1% shorter in model time and 7% shorter by events, with fewer partner changes. Intact triangles were exactly equal in model time.
- These are small but consistent across both clocks and both sizes.

**4. Under the reversible closure rule (CLOSEW), flexible patterns last two to three times longer than the stand-in.**
- At six entities, "at least two links" lasted 2.8 times longer and "at least three links" 2.2 times longer, in both clocks, while changing more partners.
- CLOSEW's links break at the plain rate, so the pattern does not last because its links are slow. It lasts because broken links are replaced quickly: closure favours re-forming links that close triangles nearby.
- Two cautions:
  - these patterns are true 96–99% of the time, so their episodes are rare, long stretches;
  - CLOSEW's formation rates are uneven too, so point 2's warning applies to it in part.
- This is the strongest candidate signal of a pattern maintained through turnover. It is a closure effect.

**5. The busiest vertex keeps its advantage longer under the path rules, but it always fades.**
- A vertex picked for having the most links starts above average by selection. That is not stability.
- Under PATHF, PATHH and CSPH, the advantage fades more slowly than in the stand-in, in both clocks and at both sizes. Under CSPH at six entities, 24–27% of it remained after 16 events' worth of activity, against 6–9% in the stand-in.
- Under CLOSEW and PCOMP it faded *faster* than in the stand-in when counted by events.
- In every case the advantage heads to zero. This is a memory of a past selection, not a lasting centre. It is also related to correlation times that earlier rounds had already published (E0A/E0B), so it is not wholly new.

**6. Two exact facts about the comparators,** found after the results were in and checked on every case:
- The way the stand-in's activity was calibrated forces its average *link* lifetime to equal the rule set's. So the stand-in differs from the rule set only in how its rates are arranged.
- When a rule set only changes formation, a pattern made of fixed links has a lifetime fixed purely by how many links it needs.

**7. How long a typical episode lasts is not the same as how much longer a pattern will last if you look at a random moment.** The second is longer when some episodes are very long. For example, for "at least two links" under CLOSEW at six entities it is 21.4 against 16.8 time units. We report the two separately (all 144 such calculations converged).

## The direct answer

- **Intact patterns:** no evidence of persistence beyond the matched comparison in model time, except one marginal case. Their survival is set by how fast their links break.
- **Flexible patterns:** they often outlast the stand-in, and do so while their partners change. But the round's equal-ratio control proves that the stand-in cannot separate organisation from uneven activity.
- **The two candidate signals:**
  - **CLOSEW:** large (2–3×), closure-driven, but at near-certain occupancy and with uneven rates;
  - **PATHF:** small (4–10%) but against a fully matched stand-in, and only for vertex-centred patterns, not triangles.
- **Hubs:** none lasts. Selection memory fades more slowly under path rules.

**So:** at five and six entities, the existing grammar gives at most weak, comparator-dependent evidence of patterns maintained through turnover. It gives none of a persistent intact pattern or a self-made centre.

## What went wrong, or was qualified

- **Two numerical checks failed, as recorded in the frozen plan.** The model-time hub calculation for PATHH and CSPH at six entities exceeded the agreed 10^−9 tolerance on two internal checks (up to 9.7×10^−9), after 21–25 repeated squarings of a very stiff matrix.
  - The values are kept and marked "numerically qualified".
  - Their likely error is around 10^−8, far smaller than any contrast described here.
  - Every other check (32 of 34) held, including the exact no-rule formulas and the stand-in's construction checks.
- **The comparator was weaker than intended.** The stand-in did what it was declared to do, but that turned out not to be enough (point 2). This is a definition lesson, to be revised *after* the round. Nothing was changed during it.
- **Partner changes are counted as events, not replacements.** A partner that leaves and comes back counts twice, so PCOMP's 199 changes per episode are largely flicker. Whether an episode ever replaces *all* its original partners was not defined in this round.
- **Pre-exposure.** All 12 rule-set laws had been published before (E0B). Their recomputation matched those publications to 10^−10. How often each pattern occurs is a re-expression of those published laws. The new quantities are lifetimes, turnover and the hub follow-up.

## What it means for the bridge

- A held reference cannot simply be swapped for something these rules make. No intact pattern holds itself together beyond chance-level comparisons at these sizes.
- **New capabilities established:**
  - an exact way to measure the lifetime and turnover of any pattern in both clocks;
  - a proof that patterns made of fixed links cannot persist through replacement;
  - a demonstration that **lifetime is not determined by the long-run picture** (PCOMP and the no-rule system share the picture but not the lifetimes).
- **Still undefined:**
  - identity through complete replacement;
  - a comparator that matches how activity is spread;
  - displacement;
  - any interaction between two such patterns.
- The bridge map gains one step (persistence) marked "partially answered, comparator-dependent".

**None of this is gravity, attraction, a body or physical time.**

## What I recommend next (not run; E5B is not authorised)

1. **Principal: repeat the lifetime contrasts with a local clock and a replacement count, on the same 12 laws.**
   - Measure each flexible pattern's lifetime in events that touch its own vertex or link (a local clock), so busy activity elsewhere cannot inflate it.
   - Add a replacement measure: the fraction of episodes in which every original partner has been replaced at least once.
   - This directly tests whether the CLOSEW and PATHF signals survive the unevenness problem. It needs no new rule set and no larger size.
2. **Fallback: the floor-reversal test** from GT-P008 (option B). It is independent of this round.
3. **Alternatively:** stop motif work here and record that the grammar, at these sizes, shows no persistent self-made reference.

## Decisions I need from you

1. Should E5B be authorised, and if so, the local-clock and replacement design (principal), the floor-reversal test (fallback), or neither?
2. Do you accept the reading that ND controls density and average link lifetime but not how activity is spread, and that its contrasts are therefore qualified?
3. Should the cross-programme suggestions (`docs/gt-e5a-cross-programme-transfer.md`) go to the Constraint Laboratory?
4. Should the new ontology proposal OP-19 ("lifetime is not a property of the stationary picture") be considered?

## Where to look

| What | File |
| --- | --- |
| This report | `gravity-time/reports/gt-e5a-report.md` |
| Competing explanations, architecture, futures | `gravity-time/reports/gt-e5a-reflection.md` |
| Every cell, predicate, comparator and check | `gravity-time/reports/gt-e5a-atlas.md` (+ `round-e5a-tables.json`) |
| Definitions and proofs (T1–T8) | `gravity-time/docs/e5-definitions-and-null-construction.md` |
| Starting audit and exposure | `gravity-time/docs/e5-coverage-and-definition-audit.md` |
| Frozen plan | `gravity-time/plans/round-e5a-plan.json` (commit `1dc43c6`) |
| What was done, in what order | `gravity-time/provenance/execution-GT-P009.md` |
| Code | `constraint-lab/src/rs_constraint_lab/gtpersist.py`, `gte5a.py`; tests `test_gtpersist.py`, `test_gte5a.py` |
