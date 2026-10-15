# Release, recovery, and a reference that takes part

*A plain-English report for the human researcher on prompt GT-P006 (rounds E3A and E3B, 14 October 2026). It assumes no knowledge of the code. Detailed documents are listed at the end.*

## Where we started

In the model, entities are linked or unlinked, and links form and dissolve one at a time under local rules. The earlier rounds found two ways for such a system to run in a preferred direction:
- a gentle bias in which changes happen (a "soft" rule);
- a strict ban that stops some changes outright (a "hard" rule).

One hard rule produced **one-way release**: a link that dissolves cannot simply re-form while a two-step path leads to it. It seemed to have a direction of its own, overriding the soft rules.

You asked for two things:
- a map of what might lie between this kind of model and anything like gravity, time or motion;
- a closer look at release and recovery, keeping clear what is shown and what is not.

## What I did

1. **A map of the gap** (`docs/foundational-bridge-map.md`, written before any experiment).
   - It lists what the model can already do, what gravity-like or motion-like phenomena would need, and the links between the two.
   - Each link is labelled as proved, observed, conjectured, blocked or undefined.
   - It includes a glossary that separates words often run together: event order, clock, drift, distance, displacement, acceleration, attraction.
2. **Some mathematics** (`docs/e3-formal-support-and-recovery.md`). With the hard rule in place:
   - links can always dissolve;
   - a dissolution is one-way exactly when a two-step path leads to that link;
   - **nothing is ever lost for good**, because every arrangement can return to the empty one;
   - the shortest way back for a released link is one step more than the number of supporting links that must first dissolve.
3. **Round E3A** (27 cases plus two mathematical scans, frozen before running). It compared:
   - the hard rule with soft rules of increasing strength, using strengths the framework already has (formation slowed to 1/2, 1/4, 1/9 and 1/16, then forbidden);
   - the hard rule against opposing rules;
   - several controls, with and without a fixed source.

   It measured how released links come back: how far, how fast, and by which route.
4. **Round E3B** (18 cases, chosen *because of* what E3A showed, frozen before running). It tested whether the fixed source itself was biasing the results.

All 45 cases (27 + 18) and both scans completed. In E3A, two cases with very extreme rule strengths failed a numerical check and are flagged. A later check suggests the checking method, not the computation, was at fault (details below).

## What I found

**1. One-way release is not a separate kind of direction.**
- As formation is slowed more and more (1/2, 1/4, 1/9, 1/16), the direction, the amount of flow, and how long a released link stays away all settle at the values the hard rule gives.
- The hard ban behaves like the extreme end of an ordinary slowing rule. What is genuinely different is only the route back: a released link must wait for a supporting link to dissolve first, and can never come back directly.
- This also explains the earlier "exception": counted as an infinitely strong slowing rule, the hard ban agrees with the usual direction rule.
- The strongest opposing rule available weakened the direction a great deal (from +0.070 to +0.007) but never reversed it.

**2. Absences can persist, in two different ways.**
- A link dissolved while supported stays away longer than one dissolved unsupported.
- Under the hard rule it is **blocked** until a supporting link goes. Under soft rules it is **slow** to return, and can come back directly.
- In nearly full systems, the rare gaps that do open can last thousands of times longer than usual.

**3. The fixed source is not neutral. It quietly pushes outer entities away.**
- The fixed source is a triangle of three permanently linked entities.
- Every possible link from an outer entity to the source has exactly two supporting paths that run *inside the triangle itself*, and they are always there.
- So every rule that reads such paths applies a fixed extra factor to every attachment. For the rules that produce the handover, that factor works against attachment.
- I proved this factor cannot change any direction of flow. It only changes where the system spends its time.

**4. Removing that bias, the direction-carrying rules gather.**
- In E3B I recomputed each case with the triangle's built-in factor divided out.
- **Every rule with the usual handover direction moved from being pushed away from the source to being drawn toward it**, at both sizes tested (5 and 6 entities). Outer entities were detached about half as often. The handover kept its direction.
- One rule went from about 21 points *below* the no-rule baseline to 7 points *above* it.
- Every earlier round concluded that rules producing a direction do not gather. It now looks as if this was largely an effect of the source's shape.
- **Caveat:** the "divided-out" version is a measuring device, not a rule the model allows. A fair test needs a fixed source with no internal paths (point 6).

**5. The mathematical scan found no exception.** Over 162 combinations of rule strengths, the overall direction matched the usual rule in all 128 where it could be judged. That is evidence, not a proof.

## What has **not** been shown

- **Nothing about gravity.** No physical gravity, acceleration or time is involved.
- **"Drawn toward the source"** is a statement about how often outer entities are linked to a fixed structure in a small random model. It is not physical attraction.
- **No drift or acceleration was demonstrated.** Neither is yet defined for this model. Defining them needs an identity for "the thing that moves" and a way to measure separation that does not assume the answer.
- **The gathering result** uses a measuring device, not a rule of the model, and has not been tried at seven entities.

## What I recommend next (not done)

1. **A fixed source without internal paths** (recommended). For example, two permanently linked entities instead of three, under the same fair rules. If the direction-carrying rules gather there, the result stands without any device. This needs a small change in how the fixed source is set up, and I'd want your authorisation for it.
2. Check whether gathering-with-direction survives at **seven entities** (not authorised here).
3. Attempt a **proof of the overall-direction rule** for the smallest case.
4. Define **displacement** before any talk of motion or acceleration.

## Decisions I need from you

1. May the next prompt make the fixed source configurable (a held single edge, or other shapes), so option 1 can run?
2. Should the cross-programme notes (`docs/e3-cross-programme-transfer.md`) be passed to the Constraint Laboratory?
3. Should OP-13 to OP-15 in `docs/ontology-proposals.md` be adopted as ontology proposals? They are: "a reference takes part", "two kinds of persistence of absence", and "a hard ban as the limit of a soft one".
4. PR #6 stays a draft. Is that still right?

## Two checks I got wrong, and one flagged case

- **E3B kernel check.** In E3B, the check meant to show "nothing changed except attachments" was written badly: it divided by zero at the fixed source's own links. A direct comparison shows the identity holds exactly.
- **E3B expectation.** One E3B expectation was wrong. I said one balanced rule would be completely unchanged. Its time-weighted picture was unchanged, but its per-event picture shifted slightly.
- **E3A flagged cases.** Two extreme E3A cases failed a numerical check. The solutions themselves are accurate (residuals near 10⁻¹⁵). The checking method had not converged in one case, and its threshold was too strict in the other.

All of these are recorded as failed checks, with explanations. None of the frozen plans were changed.

## Where to look

| What | File |
| --- | --- |
| This report | `gravity-time/reports/gt-e3-report.md` |
| The gap map (baseline plus revision) | `gravity-time/docs/foundational-bridge-map.md` |
| The mathematics | `gravity-time/docs/e3-formal-support-and-recovery.md` |
| Every case | `gravity-time/reports/gt-e3a-atlas.md`, `gt-e3b-atlas.md` |
| Reasoning between rounds | `gravity-time/reports/gt-e3a-reflection.md` |
| Synthesis and next steps | `gravity-time/reports/gt-e3-synthesis.md` |
| Notes for the other programme | `gravity-time/docs/e3-cross-programme-transfer.md` |
| What was done, with which checks | `gravity-time/provenance/execution-GT-P006.md` |
