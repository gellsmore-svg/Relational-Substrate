# E1 pre-freeze review

*For the human researcher. Written to be read without the programme's internal vocabulary. Prompt GT-P003, deliverable 6.*

**Status: the E1 plan is not frozen, and no E1 experiment has been run.** This note asks you to decide whether to authorise freezing it, and in what form.

## What the model is

A small number of entities (5, 6 or 7). Between every two of them a relation is either present or absent. Over time, relations form and dissolve one at a time. A rule makes some changes more or less likely depending on which other relations are present nearby. For example, "forming a relation is twice as likely for each third entity already connected to both ends". The computer works out, exactly, where such a system spends its time in the long run and in which order changes tend to happen.

Two set-ups are used.
- **HELD:** three entities are permanently linked (a fixed "source"), and we ask whether the others drift toward it.
- **FREE:** nothing is fixed, and we ask whether any centre emerges by itself.

## What the last experiments (E0) found

- Simple rules of the "one witness" kind always settle into a balanced state with no preferred direction in time.
- Rules that look two steps away (paths) can create a lasting direction of flow: a repeated **handover** sequence. An outer entity attaches to the source, then the relation that supported it dissolves. Its direction was the same in every such rule tested.
- How fast things happen, not just which states are favoured, decided where the system spent its time.
- Only one rule (CSPH) gave both a direction of flow and a tendency for outer entities to attach to the source. Even there the effect was small. It shrank from 5 to 6 entities, and outer entities were still detached about half the time.
- No centre emerged by itself at 6 entities or fewer.

## What is still ambiguous

The headline question is whether CSPH's small attachment advantage survives at 7 entities. While preparing for that, this review found three things that make one number a poor guide.

1. **It depends on the clock.** Measured per event, the advantage barely shrank (+0.073 → +0.065). Measured per unit of time, it nearly vanished (+0.046 → +0.009). E0 quoted the second.
2. **It depends on how crowded the system is.** CSPH keeps the system very sparse, with only one to three free relations most of the time. In that sparse regime the few relations present tend to be attachments. At ordinary crowding the same rule mildly favours relations between outer entities. Adjusted to ordinary crowding, the advantage at 6 entities is already slightly negative.
3. **The same rule gets effectively stronger as the system grows.** A rule's effect is multiplied once for every qualifying "witness" (a nearby relation that satisfies its condition). With more entities there are more possible witnesses. The maximum for the path rules goes from 12 to 24 to 40. So "the same rule at 7 entities" is not obviously the same strength as at 6.

The third point has a reassuring side. Measured in the actual long-run behaviour, the rules with a direction of flow mostly steer away from witness-rich states. The witnesses they actually use grew by only about 10% from 5 to 6 entities, not the 60% the raw counts suggest. This load can be measured directly at 7 entities, so it need not be guessed.

## What "scaling the observables" accomplished

The engine that lists possible changes was already fast enough for 7 entities (262,144 HELD states; 2,097,152 FREE states). The measurements were not. This work rewrote every measurement E0 used so that it works at that size, and kept the definitions identical.

All 84 published E0 results were recomputed and compared. Everything agreed, apart from three kinds of tiny-number problem in the *old* results:
- The old method mishandled extremely improbable states, with probabilities down to 10⁻³⁸. Two of its outputs were therefore wrong. A count of "one-way transitions" (120 to 2,136 in five cases) was an artefact; the true value is zero. Some averages at crowding levels the system practically never visits were also wrong.
- In two cases the old method stopped too early on states of probability around 10⁻³⁰, so the averages it reported at those crowding levels were meaningless.
- Two old rules for picking peaks and listing currents depended on rounding.

None of these values was used in any published conclusion.

An independent, more accurate check confirmed the new values in each case.

Some measurements were added:
- the attachment advantage adjusted for crowding;
- how many outer entities are detached at once;
- how often several entities tie as the best-connected;
- how strongly each rule is actually engaged (the witness load);
- how long things stay correlated, which is now available at the larger sizes.

One measurement, the full list of the system's natural relaxation rates, is not computed at 7 entities. It needs dense matrix algebra. E0 had already dropped it at its largest size, and the correlation times carry the information the next experiment needs.

## What experiment is proposed (option B)

1. **The same eight rules as E0B, unchanged, at 7 entities, in the HELD set-up.** These are the six two-step rules and combinations plus two controls: no rule at all, and a simple balanced rule. This is the "same model, bigger system" question.
2. **The same six rules at 5 and 6 entities, made uniformly stronger** using the two stronger weight scales the framework already defines (×1.6 and ×2 in log terms). This shows what "a stronger rule at the same size" does to each measurement. A change from 6 to 7 entities can then be compared against what mere strengthening would have produced.
   - There is a built-in check: doubling the strength at 5 entities matches the witness growth from 5 to 6 exactly, and both of those results are already known. If strengthening fails to mimic that known step, we learn that the comparison is weak before relying on it at 7.
3. **Every measurement in both clocks**, with the attachment advantage reported raw, crowding-adjusted and as a share of its ceiling. The ceiling changes with size (0.857 → 0.75 → 0.667).

Estimated cost:
- Roughly 15 to 50 minutes of computation for the 7-entity HELD cells.
- Under half an hour for the strengthened cells.
- Under 0.5 GB of memory per cell.

These figures come from measured runs on cases whose answers are known in advance, plus extrapolation from 5 and 6 entities.

**The FREE set-up** (nothing fixed) is optional and much more expensive: about 25 minutes was measured for the simplest case, and 30 to 80 minutes is expected for each real rule, with 3.2 GB of memory. Four FREE cells would take several hours. It is the only way to ask whether a centre emerges by itself at 7 entities, so it is offered as a separate second stage that you can include or defer.

## How the likely outcomes would be read

- **Handover persists, attachment advantage gone in every form.** Direction of flow and attraction separate further as the system grows.
- **Advantage survives only in the per-event clock.** The rule biases which changes happen next, but not where the system spends its time.
- **Advantage positive when raw but negative after crowding adjustment.** It remains a sparse-regime effect, as at 6 entities.
- **The 6 → 7 change looks like what strengthening does at 6, and the measured witness load grew.** Growing effective strength is a live explanation, and the "finite-size" label would be premature.
- **The 6 → 7 change runs opposite to what strengthening does.** Strength growth is unlikely to be the cause.
- **The handover reverses or disappears.** A new regime appears at 7 entities.
- **None of these.** Recorded as found.

None of these outcomes would, on its own, support or refute the wider relational-substrate picture. A shrinking or vanished effect is a finding about this model at this size.

## What stays unanswerable

- Whether "intrinsic" size dependence remains after the measurable effects are taken out. With three sizes and one family, that leftover has no unique interpretation.
- The changing balance between the closure and path parts of a combined rule. Uniform strengthening scales both together.
- The shrinking share of fixed source entities (3 of 5, then 3 of 6, then 3 of 7). This is built into the HELD set-up. A bigger fixed source would be a different experiment.

## What decision is requested

1. **Authorise freezing E1 as option B** (HELD at 7 entities plus the strengthened controls at 5 and 6), choose another option in `docs/e1-design-alternatives.md`, or ask for changes.
2. **Decide on the FREE tranche** (option D), which is the only way to ask about centres emerging without a scaffold.
3. **Confirm the proposed roadmap clarification of the stop rule** (`docs/roadmap.md`, last section). A shrinking or vanished advantage would be recorded as a finding for this model at this size. It would not automatically be called "finite-size", and grades would not be retuned afterwards.
4. **Optionally, name which form of the margin the frozen plan should quote first.** Otherwise all four forms are reported side by side and none is primary.
