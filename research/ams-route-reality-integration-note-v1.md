# AMS Route Reality Integration Note v1

## Purpose

This document consolidates the current state of the AMS interface and route-reality programme after the recent modelling sequence.

It is meant to provide one usable summary of:

- the refined interface variables
- the main loop families
- the route classes
- the route-reality criteria and grades
- the strongest current anchors
- the strongest current frontiers

It also states where the programme is now strongest and what the next high-value frontier would be if the modelling continues.

## Current Interface Variable Set

The active refined interface set is now:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Derived term:

- `I_comp`

This is the correct set to keep using for now.

The main refinement gain was:

- replacing `J_surf`

with:

- `J_bound`
- `J_trans`

That split materially improved the programme by separating:

- immediate boundary-face coupling
- through-layer transition continuity

This sharpened:

- reflection
- release
- trapping
- cross-transmissive compatibility

No further primitive split looks necessary yet.

## Current Geometric Descriptors

The active non-primitive geometric descriptors are now:

- `L_depth`
- `L_span`
- `L_loop`
- `L_escape`

These should remain descriptors for now, not primitives.

They are already doing real work, especially:

- `L_loop`
- `L_escape`

but formalising them too early would likely create false precision.

## Main Loop Families

The current loop-family set is:

- `L1` face loop
- `L2` shallow pocket loop
- `L3` elongated stall loop
- `L4` broken multi-loop field

### Current Roles

`L1`
- mainly release-side
- shallow boundary-face retention

`L2`
- strongest in glass release
- bounded local retention near the interface

`L3`
- the strongest recurring stall family in the whole programme
- appears across:
  - glass release
  - crystal release
  - glass-to-crystal compatibility stall

`L4`
- best treated as the breakdown edge toward fragmentation and scattering
- not the main stable family

### Most Important Loop Result

`L3` is the first genuinely reusable interface-stall geometry in the programme.

That is one of the biggest gains in the whole recent sequence.

## Main Route Classes

The current route taxonomy is:

- `R1` narrow viable route
- `R2` distributed weak routes
- `R3` blocked apparent route
- `R4` inward-biased route
- `R5` loop-dominated pseudo-route
- `R6` fragmenting route field

### Current Roles

`R1`
- strongest class for genuine completion

`R2`
- especially relevant in glass entry and glass release
- real but weak distributed continuation

`R3`
- failed real route
- route exists in a real sense but fails under progression

`R4`
- strongest reflection-side route class
- especially clear in polished metal

`R5`
- pseudo-route driven by local looping
- active but not genuinely completion-directed

`R6`
- breakdown edge where route coherence fragments

### Most Important Route Result

The sharpest unresolved route distinction was:

- `R3` versus `R5`

That distinction now appears stable.

Best current formulation:

- `R3` = progression-first, blockage-second
- `R5` = looping-first, progression-second

That is one of the most important discriminator gains in the entire programme.

## Route-Reality Criteria

The current route-reality test has five minimum criteria:

1. forward continuity
2. directional commitment
3. completion viability under progression
4. dominance over local looping
5. completion remains a live outcome

These are now the right working criteria for deciding whether a route is genuinely real.

### Route-Reality Grades

- `A` strongly real route
- `B` weak but real route
- `C` apparent but unreliable route
- `D` pseudo-route

These grades have already been pressure-tested across the benchmark cases and are holding up well.

## Benchmark Results Now Stabilised

The strongest current benchmark associations are:

### `air -> glass`

- strongest broad entry anchor
- dominant route form:
  - viable handoff
- route-reality grade:
  - `A`

### `glass -> air`

- strongest broad release anchor
- dominant frontier route forms:
  - `R2`
  - `R3`
  - `R5`
- route-reality range:
  - `B`
  - `C`
  - `D`

### `air -> polished metal`

- strongest reflection anchor
- dominant route form:
  - `R4`
- route-reality:
  - strong inwardly
  - weak outwardly

### `air -> oxidised metal`

- strongest degraded surface / boundary-layer benchmark
- dominant route classes:
  - `R3`
  - `R6`

### `glass -> crystal`

- strongest compatibility frontier
- dominant route classes:
  - `R1`
  - `R3`
  - `R5`
- strongest direct pressure case for:
  - `I_comp`
  - `L3`
  - route reality under cross-whole transition

### `crystal -> air`

- strongest ordered-release benchmark
- dominant route classes:
  - `R1`
  - `R4`
- route-reality tends to remain stronger even in failure than in glass

## Where the Programme Is Strongest

At this stage, the programme is strongest in five areas.

## 1. Reflection from Polished Metal

This is now one of the cleanest cases in the whole system.

It is best captured by:

- strong `R4` inward-biased route
- high `J_bound`
- low/medium `J_trans`
- preserved coherence for return-side organisation

## 2. Air -> Glass Entry

This remains the strongest broad handoff benchmark.

It anchors:

- high `B_in`
- viable distributed permissive continuation
- genuine route reality without rigid over-ordering

## 3. Glass Release as a Frontier Anchor

This is one of the most valuable results in the programme.

Glass release now clearly separates:

- clean release
- diffuse release
- trapped release

and serves as the best release-side test bed.

## 4. Glass -> Crystal Compatibility

This remains the strongest frontier case for:

- `I_comp`
- `L3`
- `R3`
- `R5`

It is the clearest test of whether one transmissive grammar can transition into another.

## 5. The Route-Reality Framework

The route-reality criteria and grades are now operational enough to use repeatedly rather than reinventing the logic for each case.

That is a major stabilising gain.

## Where the Programme Is Still Weakest

The weakest remaining areas are no longer basic ontology or basic interface vocabulary. They are more specific.

## 1. Formal Treatment of `L_escape`

`L_escape` is now doing real explanatory work.

Current best reading:

- route viability, not mere openness

That is good, but it still needs a more systematic route-level comparison if the programme deepens further.

## 2. Obstruction Character

The programme now clearly suggests that obstruction is not only about amount.

What matters is also:

- distribution
- structure
- whether it blocks one route
- whether it fragments the whole route field

This is under-modelled.

## 3. Ordered Return as a Full Family

Ordered return is now clear enough to identify, but it has not yet had a dedicated family study comparable to the work done on:

- trapped release
- `L3`
- route reality

## 4. Cross-Case Route Dynamics Over Time

The programme now has good static and quasi-static route categories, but less explicit treatment of:

- how one route class becomes another over time

especially:

- `R3 -> R5`
- `L3 -> R1`
- `L3 -> R4`
- `L3 -> L4`

## Most Important Strategic Judgments

## 1. The Programme Has Cross-Case Reuse Now

This is the biggest structural result.

The interface programme is no longer inventing a different local story for every case.

It now has reusable:

- variables
- loop families
- route classes
- route-reality grades

That is real progress.

## 2. `L3` Is the Main Recurring Stall Family

This should remain a central organising idea for the next stage if the work continues.

## 3. `R3` and `R5` Are the Main Frontier Route Classes

They now represent the sharpest unresolved distinction between:

- failed real progression
- and pseudo-progressive local activity

## 4. Glass Remains the Best Frontier Material

This is repeatedly confirmed from multiple angles.

Glass is especially valuable because it can support:

- real handoff
- weak distributed continuation
- blocked apparent routes
- pseudo-routes
- trapped release

without immediately collapsing into simpler ordered-return logic.

## 5. No New Primitive Split Is Needed Yet

This should be stated clearly.

The recent gains came from:

- better geometry
- better comparison
- better route discrimination

not from multiplying primitives.

That is a good sign.

## Current Best Frontier If Modelling Continues

If the modelling continues, the next high-value frontier is:

- route viability under obstruction character

More specifically:

- how different obstruction distributions preserve, distort, stall, redirect, or fragment route reality

This frontier sits at the intersection of:

- `L_escape`
- `R3`
- `R5`
- `L3`
- boundary-layer degradation

It is the clearest place where the current model has enough structure to push deeper without simply repeating itself.

## Recommended Next Artifacts

If the programme continues, the strongest next candidates are:

### 1. `ams-obstruction-character-study-v1.md`

Why:

- best next frontier
- would deepen route viability without needing more primitives

### 2. `ams-ordered-return-family-study-v1.md`

Why:

- strongest major family still underdeveloped compared with trapping and stall work

### 3. `ams-route-class-transition-map-v1.md`

Why:

- would clarify how route classes mutate under changing conditions rather than only classifying them statically

## Confidence

- confidence that the programme now has a stable reusable interface framework: `9/10`
- confidence that `L3` is the strongest recurring stall family: `9/10`
- confidence that `R3` and `R5` are the key frontier route classes: `9/10`
- confidence that no new primitive split is needed yet: `8/10`
- confidence that obstruction character is the best next frontier: `8/10`

## Bottom Line

The programme is now in a better state than it was at the start of this sequence.

It now has:

- a stable refined interface variable set
- a recurring stall geometry
- a workable loop taxonomy
- a workable route taxonomy
- explicit route-reality criteria and grades
- stable anchor cases
- stable frontier cases

The strongest current anchor triangle is:

- `air -> glass`
- `air -> polished metal`
- `air -> oxidised metal`

The strongest current frontier pair is:

- `glass -> air`
- `glass -> crystal`

And the strongest current recurring deep structure is:

- `L3`

That is enough structure to keep going usefully if you want to push the technical programme further.*** End Patch
