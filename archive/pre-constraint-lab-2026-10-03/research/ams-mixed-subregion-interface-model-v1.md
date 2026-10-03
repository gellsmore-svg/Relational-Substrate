# AMS Mixed Subregion Interface Model v1

## Purpose

This document models the next high-value frontier in the AMS interface programme:

- mixed local subregions inside one real interface layer

The previous crosswalk work established that the main frontier distinctions now hold cleanly:

- `O2 -> R3`
- `O3 -> R5`

But it also showed something more advanced:

- one interface may contain multiple local subregions at once

That means the next problem is no longer:

- which one global label fits this interface?

It is:

- how different local subregions coexist inside one active interface layer
- how an event moves between them
- how whole-interface outcomes emerge from their interaction

## Core Claim

A real interface should no longer be modelled as one uniform zone.

The current working claim is:

- one interface layer can contain multiple local subregions with different obstruction, route, and loop behaviour

For example:

- a late-gate route zone
- a pocketing pseudo-route zone
- a diffusing fringe

The event may:

- enter through one zone
- partially progress into another
- stall in a third

That means interface behaviour is often:

- locally heterogeneous

rather than globally uniform.

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

## Why This Step Matters

The current taxonomy work has already done most of the hard early labour:

- variables are sharper
- loop families are sharper
- route classes are sharper
- obstruction classes are sharper

So the next realistic question is:

- how do these different local patterns sit together in one actual interface?

Without this step, the model risks staying too clean conceptually and too coarse spatially.

## First-Pass Mixed Interface Template

The current best first-pass template is a three-zone interface:

## Zone A: Late-Gate Route Zone

### Dominant Logic

- `O2`
- `R3`

### Character

- route reality is genuinely present
- progression is real
- failure occurs near the end of the route

### Typical Variable Profile

- `J_trans`: medium
- `Q_coh`: medium/high
- `D`: medium/high
- `L_escape`: weak but real

### Main Outcome Tendency

- blocked apparent route

## Zone B: Pocketing Pseudo-Route Zone

### Dominant Logic

- `O3`
- `R5`

### Character

- local activity is strong
- local coherence is real
- apparent progression is mostly produced by bounded reseating

### Typical Variable Profile

- `J_bound`: medium/high
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium
- `L_escape`: mostly apparent

### Main Outcome Tendency

- pseudo-route
- trapped release
- local compatibility cycling

## Zone C: Diffusing Fringe

### Dominant Logic

- `O5`
- sometimes drift toward `R2`

### Character

- route dominance weakens
- the event broadens rather than cleanly stalls or completes
- outward continuation may still exist, but badly

### Typical Variable Profile

- `J_trans`: low/medium
- `Q_coh`: medium or falling
- `D`: medium/high
- `L_escape`: low/medium

### Main Outcome Tendency

- diffuse release
- weak distributed continuation

## Why These Three Zones Matter

This three-zone model is the smallest mixed-interface picture that can already explain several important results:

### 1. Why one interface can show both `R3` and `R5`

Because different local subregions may produce each.

### 2. Why one event can look near-complete in one place and pseudo-progressive in another

Because route reality may vary locally inside the same interface layer.

### 3. Why whole-interface behaviour can be mixed without the model becoming incoherent

Because mixed outcomes can emerge from structured subregion interaction rather than from conceptual sloppiness.

## Event Movement Across Subregions

The next key question is:

- how does an event move between zones?

The current first-pass answer is:

- by local reseating and route competition

But that needs more explicit shape.

## Path M1: Route Preserved, Then Blocked

### Sequence

- event enters Zone A
- real route progression occurs
- late-gate obstruction blocks completion

### Main Outcome

- `O2 -> R3`

## Path M2: Route Attempt Falls into Pocketing

### Sequence

- event begins with some route-directed behaviour
- continuity weakens locally
- event drops into Zone B
- local pocketing and pseudo-route activity take over

### Main Outcome

- `R3` drift toward `R5`

### Importance

This is one of the strongest reasons to model mixed subregions at all.

## Path M3: Pocketing Bleeds into Diffusing Fringe

### Sequence

- event becomes locally trapped in Zone B
- bounded coherence weakens
- event spreads into Zone C

### Main Outcome

- pseudo-route gives way to diffuse release or degraded continuation

## Path M4: Route Survives the Mixed Field

### Sequence

- event begins in or passes through Zone A
- avoids domination by Zone B
- diffusing fringe does not destabilise the dominant route
- completion still occurs

### Main Outcome

- successful handoff despite a mixed interface

### Importance

This is a major reminder that mixed interfaces do not automatically imply failure.

## Path M5: Mixed Field Breaks into Fragmentation

### Sequence

- route zone weakens
- pocket zone destabilises
- diffusing fringe expands

### Main Outcome

- transition toward `R6`
- broken multi-loop field

## Strongest Current Mixed-Interface Benchmarks

## 1. Glass -> Air

This is the strongest release-side mixed-interface benchmark.

Why:

- blocked release routes can coexist with pocketed pseudo-release and diffuse fringe behaviour

This is the best place to study:

- `O2`
- `O3`
- `O5`

inside one interface layer.

## 2. Glass -> Crystal

This is the strongest compatibility-side mixed-interface benchmark.

Why:

- a real narrowing route may coexist with pseudo-narrowing local pockets and weaker diffusing outskirts

This is the best place to study:

- route reality variation inside one transition zone

## 3. Oxidised Metal Edge Cases

This is a useful secondary benchmark.

Why:

- structured route remnants may coexist with fragmenting degraded regions

But this is slightly less central than the glass cases because it trends more quickly toward collapse regimes.

## What This Changes in the Programme

## 1. Whole-Interface Labels Become Less Absolute

This is the main result.

The programme should no longer assume:

- one interface
- one label

Instead it should increasingly assume:

- one interface
- several local subregions
- one emergent dominant behaviour

## 2. Crosswalk Results Become More Realistic

The earlier crosswalk:

- `O2 -> R3`
- `O3 -> R5`

still holds.

But now it can hold:

- locally

rather than only globally.

That is a major gain.

## 3. Frontier Cases Are Better Explained

The strongest frontier cases:

- `glass -> air`
- `glass -> crystal`

were difficult partly because they seemed to host multiple route behaviours at once.

The mixed-subregion model explains why.

## 4. No New Primitive Variables Are Needed

This remains important to state clearly.

The gains are still coming from:

- local spatial modelling
- not from enlarging the primitive set

## Current Weak Point

The model now has a useful mixed-subregion template, but it still lacks:

- explicit weighting of zone dominance
- explicit transition rules between zones
- clear criteria for when one local zone governs the whole-interface result

Those are the obvious next steps.

## Provisional Confidence

- confidence that real interfaces should be modelled as locally heterogeneous: `9/10`
- confidence that the three-zone template is a useful first model: `8/10`
- confidence that glass cases are the best mixed-interface benchmarks: `9/10`
- confidence that no new primitive split is needed yet: `8/10`

## Recommendation

Keep the current taxonomies and variable set unchanged.

The next gains should come from:

- zone weighting
- dominance logic
- transition rules between local subregions

## Next Move

The best next artifact is:

- `ams-subregion-dominance-and-weighting-v1.md`

That should address:

- how much each local zone has to matter before it changes the whole-interface outcome
- when a mixed interface is mostly `R3`, mostly `R5`, or mostly diffuse
- how local zone weighting interacts with:
  - `L_escape`
  - `Q_coh`
  - `J_trans`
