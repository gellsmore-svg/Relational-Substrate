# AMS O2/O3 and R3/R5 Crosswalk v1

## Purpose

This document directly maps the current obstruction-side frontier pair:

- `O2` late-gate obstruction
- `O3` pocketing obstruction

against the current route-side frontier pair:

- `R3` blocked apparent route
- `R5` loop-dominated pseudo-route

The purpose is to test whether the two frontier distinctions now align cleanly enough to function as one cross-layer modelling framework rather than two parallel vocabularies.

This is the strongest remaining integration test in the current programme.

## Core Claim

The present working claim is:

- `O2` tends to generate `R3`
- `O3` tends to generate `R5`

But “tends to” is not the same as “always produces.”

So the right question is:

- where is the alignment clean?
- where is it mixed?
- where does one layer still fail to map neatly onto the other?

## Working Definitions

### `O2`

Route-preserving, then route-blocking obstruction.

### `O3`

Pocket-forming, then route-imitating obstruction.

### `R3`

Failed real route.

### `R5`

Pseudo-route dominated by local looping.

## Crosswalk Logic

The crosswalk is evaluated along four axes:

1. route reality
2. loop dominance
3. stage of failure
4. true versus apparent `L_escape`

## Crosswalk Matrix

| Benchmark condition | Dominant obstruction reading | Dominant route reading | Alignment quality | Main reason |
|---|---|---|---:|---|
| glass -> air late blocked release | `O2` | `R3` | 9/10 | real release route persists long enough to fail late |
| glass -> air pocketed pseudo-release | `O3` | `R5` | 9/10 | local retention pocket dominates while true release route never stabilises |
| glass -> crystal late compatibility failure | `O2` | `R3` | 9/10 | admissible handoff path is genuinely formed, then blocked |
| glass -> crystal pseudo-compatibility activity | `O3` | `R5` | 9/10 | narrowing-like activity is mostly local and route-imitating |
| crystal -> air failed ordered release | `O2` | `R3` | 8/10 | ordered route remains real longer than in glass and fails late |
| crystal -> air local pocketing edge case | weak `O3` | weak `R5` | 5/10 | possible, but not a dominant failure family |
| glass -> air mixed trapped-release zone | `O2` + `O3` | `R3` + `R5` | 7/10 | late blockage and pocketed pseudo-progress can coexist in one terminal layer |
| glass -> crystal mixed compatibility zone | `O2` + `O3` | `R3` + `R5` | 7/10 | real narrowing and pseudo-narrowing can overlap in one transition region |

## Clean Alignments

## 1. `O2 -> R3`

This is now the cleanest obstruction-to-route mapping in the programme.

### Why It Aligns

`O2` preserves route reality for long enough that:

- forward continuity is genuinely present
- directional commitment remains real
- `L_escape` is weak but not fictional

Then the route fails near completion.

That is exactly the logic of `R3`.

### Strongest Benchmarks

- glass -> air late blocked release
- glass -> crystal late compatibility failure
- crystal -> air failed ordered release

### Current Judgment

This mapping should now be treated as stable.

## 2. `O3 -> R5`

This is the second cleanest mapping.

### Why It Aligns

`O3` reshapes the active region into a local pocket or bounded local zone in which:

- activity is preserved
- coherence is local
- apparent progression is driven by looping
- route reality is overestimated

That is exactly the logic of `R5`.

### Strongest Benchmarks

- glass -> air pocketed pseudo-release
- glass -> crystal pseudo-compatibility activity

### Current Judgment

This mapping should also now be treated as stable, especially in glass-side frontier cases.

## Mixed Zones

The crosswalk is not perfectly one-to-one everywhere.

That matters.

## 1. Glass -> Air Mixed Trapped-Release Zone

### Why It Is Mixed

A glass terminal layer can plausibly contain both:

- a route that is genuinely trying to complete but failing late (`O2 -> R3`)
- a nearby pocket of local reseating that imitates completion without truly supporting it (`O3 -> R5`)

This means the same benchmark case can contain both mappings at once, but in different local subregions.

### Judgment

This is not a failure of the crosswalk. It is a sign that the programme is reaching a realistic level of local complexity.

## 2. Glass -> Crystal Mixed Compatibility Zone

### Why It Is Mixed

A compatibility layer may contain:

- a genuine narrowing route that almost becomes admissible but fails (`O2 -> R3`)
- local narrowing-like activity that never becomes a true handoff route (`O3 -> R5`)

This is one of the clearest reasons why `glass -> crystal` remains the strongest frontier case in the entire programme.

### Judgment

Again, the mixed case is informative rather than destabilising.

## Weak Alignments

## Crystal -> Air Pocketing Edge Case

### Reading

- weak `O3`
- weak `R5`

### Why It Is Weak

Crystal release tends to preserve route reality or directional return better than glass.

So pocketing pseudo-routes are possible, but not central.

This is useful because it shows the crosswalk is not being forced everywhere indiscriminately.

## Cross-Layer Findings

## 1. The Two Frontier Distinctions Now Reinforce Each Other

This is the main result.

The route-side and obstruction-side frontier pairs are no longer just parallel descriptions. They now map onto each other in a principled way.

Current best summary:

- `O2` is the obstruction-side generator of `R3`
- `O3` is the obstruction-side generator of `R5`

## 2. Glass Is the Main Crosswalk Material

This is reinforced again.

Glass:

- supports late real-route blockage
- supports local pseudo-progressive pocketing
- supports mixed zones where both can coexist

That makes it the best material for testing the crosswalk.

## 3. Crystal Is the Useful Contrast Material

Crystal matters because it shows where the mapping does **not** spread equally.

That strengthens the crosswalk by showing it is selective rather than indiscriminate.

## 4. Mixed Zones Are Real and Productive

The existence of mixed `O2/O3` and `R3/R5` zones is not a problem.

It suggests that the next stage of the programme should allow:

- local subregion modelling

rather than forcing whole interfaces to be classified by one label only.

That is an important maturation step.

## What This Clarifies About `L_escape`

The crosswalk sharpens `L_escape` further.

### In `O2 -> R3`

`L_escape` is:

- weak but real

The route is genuinely completion-directed for part of its life.

### In `O3 -> R5`

`L_escape` is:

- mostly apparent

The event looks active enough to suggest escape, but the local pocket geometry is doing most of the work.

### Main Consequence

This may be the cleanest current explanation for why:

- true escape viability
- and apparent escape viability

must remain distinct.

## Current Strongest Stable Crosswalks

Most stable now:

- `glass -> air` late blocked release: `O2 -> R3`
- `glass -> air` pocketed pseudo-release: `O3 -> R5`
- `glass -> crystal` late compatibility failure: `O2 -> R3`
- `glass -> crystal` pseudo-compatibility activity: `O3 -> R5`

These should now be treated as stable frontier mappings.

## Programme-Level Consequences

## 1. The Interface Programme Now Has a Strong Cross-Layer Match

That is the biggest result in this document.

The programme can now move between:

- obstruction character
- route class

without losing explanatory sharpness.

## 2. The Frontier Has Shifted Again

The hardest remaining problem is no longer:

- whether the categories hold

It is:

- how mixed local subregions are organised inside one active interface layer

That is a more advanced and more interesting problem.

## 3. No New Taxonomy Expansion Is Needed Yet

The current obstruction classes and route classes are enough for another stage of work.

The next gains should come from:

- local subregion modelling
- not from creating more names

## Confidence

- confidence that `O2 -> R3` is now a stable mapping: `9/10`
- confidence that `O3 -> R5` is now a stable mapping: `9/10`
- confidence that mixed zones are real and important: `8/10`
- confidence that glass remains the best crosswalk material: `9/10`
- confidence that no new class expansion is needed yet: `8/10`

## Recommendation

Keep the current obstruction and route taxonomies unchanged.

The next work should deepen:

- local mixed-zone modelling

rather than abstract taxonomy growth.

## Next Move

The best next artifact is:

- `ams-mixed-subregion-interface-model-v1.md`

That should model one interface layer as containing multiple local subregions, for example:

- a late-gate route zone
- a pocketing pseudo-route zone
- a diffusing fringe

and ask how the event moves between them inside one real interface rather than under one global label.*** End Patch
