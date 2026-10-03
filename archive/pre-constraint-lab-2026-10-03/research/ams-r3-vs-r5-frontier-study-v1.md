# AMS R3 vs R5 Frontier Study v1

## Purpose

This document isolates the sharpest unresolved route-class distinction in the current programme:

- `R3` blocked apparent route
- `R5` loop-dominated pseudo-route

From:

- `ams-route-class-benchmark-table-v1.md`

the main result was that `R3` and `R5` are now the key frontier classes across the most important unresolved cases, especially:

- `glass -> air`
- `glass -> crystal`

The reason this matters is that both classes describe events that:

- look active
- look non-final
- and can easily be confused with one another

But they are not the same thing.

This study aims to clarify:

- what actually separates them
- why the difference matters
- how each behaves across release and compatibility failures

## Core Claim

`R3` and `R5` are not two ways of saying “almost but not quite.”

They differ in kind.

Current best distinction:

- `R3` is a route that appears genuinely available but fails under progression
- `R5` is a local activity pattern that mimics route availability without ever sustaining true completion logic

So:

- `R3` fails a real route
- `R5` imitates a route

That is the most important distinction in the document.

## Working Definitions

## `R3` Blocked Apparent Route

An apparently open or promising route exists, and the event begins to use it, but the route is functionally blocked before completion can occur.

This means:

- the route is not fictional
- the route is not merely local activity
- the route fails under real continuation

## `R5` Loop-Dominated Pseudo-Route

The event exhibits active local motion and repeated reseating that can be mistaken for route progression, but the pattern does not preserve a genuinely viable completion path.

This means:

- the local event is real
- the activity is real
- but the route-like appearance is misleading

## Why the Distinction Matters

If the programme blurs `R3` and `R5`, then it loses one of its strongest new discriminators:

- whether the event failed a route
- or never had a true route to begin with

That distinction matters for:

- completion modelling
- trapped release
- compatibility stall
- how `L_escape` is interpreted

Because:

- `R3` implies some completion logic was genuinely present
- `R5` implies the event’s apparent progress was mostly local cycling all along

## Active Variable Set

Primitive variables:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Derived term:

- `I_comp`

Geometric descriptors:

- `L_depth`
- `L_span`
- `L_loop`
- `L_escape`

## Best Current Signatures

## `R3` Best Current Signature

- `J_trans`: low/medium
- `Q_coh`: medium or falling
- `D`: medium/high
- `L_escape`: low/medium
- `L_loop`: route-like elongation still visible

### Interpretation

The route remains recognisable enough that the event can seem genuinely close to completion.

The failure comes from:

- late obstruction
- repeated continuity break
- inability of the route to carry the event through actual completion

## `R5` Best Current Signature

- `J_bound`: medium/high
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium
- `L_escape`: low/medium but often overestimated
- `L_loop`: local cycling dominates

### Interpretation

The event is active and bounded, but its route-like appearance is mostly produced by repeated local reseating rather than by a true completion pathway.

## Main Structural Difference

Current best formulation:

- `R3` is progression-first, blockage-second
- `R5` is looping-first, progression-second

That is the cleanest distinction in the whole document.

## Geometric Contrast

## `R3` Geometry

### Path Shape

- elongated
- directed enough to look plausibly completeable
- interrupted before completion

### Spatial Logic

The event advances along something that behaves enough like a route to be misleadingly promising.

The route may fail because of:

- narrowing that never quite finishes
- late obstruction
- repeated late-stage break
- incompatible final continuation

### Typical Loop Behaviour

- looping may occur
- but it is secondary to failed route progression

## `R5` Geometry

### Path Shape

- locally active
- cycling
- often pocketed or shallowly elongated
- not strongly completion-directed

### Spatial Logic

The event recycles locally in a way that can resemble progress, but the geometry is mostly self-reseating rather than truly transitional.

### Typical Loop Behaviour

- looping is primary
- apparent progress is derivative or illusory

## Temporal Contrast

This distinction is not only spatial. It is also temporal.

## `R3`

Temporal feel:

- “it was going somewhere, then failed”

## `R5`

Temporal feel:

- “it keeps doing something, but not really getting there”

This temporal difference is one of the clearest intuitive tests of the distinction.

## Relation to `L_escape`

## `R3`

`L_escape` is genuinely present, but weak or unstable.

The event still has some real completion-side viability, which is why blocked apparent routes are so misleading.

## `R5`

`L_escape` is often overread.

The event looks active enough that one might think a route remains, but the actual route viability is much lower than the local activity suggests.

### Main Consequence

This is one of the strongest reasons to keep `L_escape` as:

- route viability

not:

- sheer amount of local motion

## Benchmarks

## 1. Glass -> Air

### `R3` Role

Strong when:

- release begins
- the terminal path looks plausible
- but the path breaks under actual continuation

### `R5` Role

Strong when:

- the terminal region becomes locally active
- repeated reseating near the boundary imitates release
- but no true release route dominates

### Judgment

This is the best release-side benchmark for separating `R3` and `R5`.

## 2. Glass -> Crystal

### `R3` Role

Strong when:

- the compatibility path seems real
- narrowing toward crystal-style admissibility begins
- final handoff never actually completes

### `R5` Role

Strong when:

- the transition zone becomes locally active
- pseudo-progressive looping mimics compatibility
- but no genuine admissible route dominates

### Judgment

This is the best compatibility-side benchmark for separating `R3` and `R5`.

## 3. Crystal -> Air

### `R3` Role

Plausible where ordered release begins but fails late.

### `R5` Role

Weaker than in glass cases, because crystal failures more often seem to shift toward:

- narrow viable route
- or inward-biased route

rather than sustained pseudo-looping.

### Judgment

Useful secondary benchmark, but not the strongest place to stabilise the distinction.

## Best Discriminators Between `R3` and `R5`

## 1. Does the Event Ever Possess a Genuinely Completion-Directed Route?

If yes, even weakly:

- likely `R3`

If no, and activity remains mostly local:

- likely `R5`

## 2. Is Looping Primary or Secondary?

If looping is secondary to failed progression:

- `R3`

If looping is the main event:

- `R5`

## 3. Does the Stall Fail Early or Late?

If the route fails after real progression:

- `R3`

If apparent progress never becomes more than local cycling:

- `R5`

## 4. Is `L_escape` Real or Overestimated?

If route viability is genuinely present but weak:

- `R3`

If route viability only seems present because local activity is intense:

- `R5`

## Relationship to Other Route Classes

## `R3` vs `R1`

`R3` is a failed real route.

`R1` is a successful narrow viable route.

So `R3` sits adjacent to completion.

## `R5` vs `R2`

`R5` is not weak distributed continuation.

It is local pseudo-progression.

So `R5` sits closer to trapping than to diffuse release.

## `R5` vs `R6`

`R5` still preserves one dominant local activity pattern.

`R6` is what happens when even that local pattern breaks apart.

So `R5` is a pre-fragmentation regime, not a fragmentation regime.

## Strongest Current Judgments

## 1. `R3` Is About Failed Completion

This is its defining role.

It should be used when:

- the event genuinely advances along a route
- but the route does not complete

## 2. `R5` Is About Misleading Local Activity

This is its defining role.

It should be used when:

- the event is active and bounded
- but the apparent route is mostly pseudo-progressive

## 3. Glass Cases Are the Best Test Bed

Both:

- `glass -> air`
- `glass -> crystal`

remain the strongest current places to pressure this distinction.

That is because glass can preserve:

- real activity
- partial route appearance
- and genuine failure

without immediately collapsing into simpler ordered-return behaviour.

## Programme-Level Importance

## 1. The Route Taxonomy Now Has a Clear Frontier Distinction

This is the main result.

The programme now has a genuinely hard discriminator between:

- true but failed route progression
- and pseudo-progressive local looping

## 2. `L_escape` Has Been Clarified Further

The study sharpens one key point:

- local activity should not be mistaken for route viability

That is crucial for the whole next stage of modelling.

## 3. The Model Can Now Diagnose “False Near-Completion”

That is a real gain.

Some events only look close to completion because their local cycling is intense. `R5` gives the programme a way to say that clearly.

## Current Weak Point

The main remaining weakness is not the distinction itself.

It is that the programme still needs a direct way to compare:

- true late-stage route blockage
- pseudo-progressive looping

under the same benchmark conditions.

That means the next best step is a direct case matrix rather than more abstract definition work.

## Confidence

- confidence that `R3` and `R5` are genuinely distinct route classes: `9/10`
- confidence that the key distinction is failed route versus pseudo-route: `9/10`
- confidence that glass cases are the best current test bed: `8/10`
- confidence that no new route class is needed yet: `8/10`

## Recommendation

Keep both classes.

Do not merge them.

Do not add new frontier classes yet.

The next gains should come from harder side-by-side case testing.

## Next Move

The best next artifact is:

- `ams-r3-r5-case-matrix-v1.md`

That should compare `R3` and `R5` directly across:

- glass -> air
- glass -> crystal
- crystal -> air

and force a side-by-side judgment of:

- route reality
- loop dominance
- stage of failure
- true vs apparent `L_escape`
