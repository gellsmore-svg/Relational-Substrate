# AMS Exit Geometry Study v1

## Purpose

This document focuses on the weakest remaining region in the current optical interface programme:

- exit geometry

The current model has become materially stronger on:

- entry
- reflection
- boundary degradation
- cross-transmissive compatibility

But exit-side cases remain less mature, especially:

- `glass -> air`
- `crystal -> air`

The main reason appears to be that the programme has so far treated release too often as if it were simply admission in reverse. The current working claim is that this is wrong.

## Core Claim

Exit is not just reversed entry.

The reason is that exit begins with a disturbance already organised inside a real whole. The problem is therefore not:

- whether the whole can admit a disturbance into its own pathways

but:

- whether a previously coherent internal propagation can be converted into a viable outward event without losing too much of its organisation at the final interface layer

That means exit places more pressure on:

- `B_out`
- `J_bound`
- `J_trans`
- the geometry of final release

and slightly less pressure on:

- first-contact admission quality

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

Supporting bulk variables:

- `R`
- `S`
- `J_dist`

## Why Exit Is Harder Than Entry

The current programme suggests three reasons.

## 1. Exit Begins with Internal Organisation Already in Place

In entry cases, the question is:

- can the receiving whole take up the incoming event?

In exit cases, the question is:

- can the source whole release an event that has already been shaped by its internal organisation?

That means the final boundary must not merely allow passage. It must preserve enough of the internal event structure for release to remain coherent.

## 2. The Final Interface Layer Can Distort More Than the Bulk

A whole may propagate well internally while still releasing badly.

That is because:

- bulk propagation and final release are not the same task

The last interface layer may:

- overconcentrate the event
- scatter the event
- trap the event
- reflect part of the event back inward

even when the bulk whole remains strongly transmissive.

## 3. Release Requires a Conversion, Not Just a Continuation

Inside a whole, propagation is still coupled to the whole’s own admissibility structure.

At exit, the event must become:

- no longer merely internal propagation
- but an outwardly viable event that can survive beyond the source whole

So exit depends on a conversion geometry rather than simple continuity alone.

## Four Candidate Exit Geometries

## Geometry E1: Clean Release Face

### Description

The final boundary allows a previously coherent internal event to detach cleanly into the adjacent medium.

### Expected Variable Pattern

- `B_out`: high
- `J_bound`: medium/high
- `J_trans`: medium
- `Q_coh`: high
- `D`: low

### Likely Outcome

- successful handoff

### Interpretation

This is the most ideal release case.

The internal event approaches the boundary in an already coherent way, and the boundary neither traps nor scrambles it. Release remains structured enough to survive the transition.

### Best Use

- polished, well-formed transmissive exits
- strong crystal release candidates

## Geometry E2: Surface Diffusion at Release

### Description

The internal event approaches the boundary coherently, but the final release zone spreads or loosens that organisation too much.

### Expected Variable Pattern

- `B_out`: medium
- `J_bound`: medium
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium/high

### Likely Outcome

- partial handoff
- diffuse release
- elevated scattering

### Interpretation

The whole still releases something outward, but the final event is no longer sharply preserved.

This geometry is especially plausible for:

- glass exits with imperfect surface quality
- defect-heavy release zones

## Geometry E3: Boundary Retention at Exit

### Description

The internal event reaches the boundary but remains locally retained, repeatedly reseated, or shallowly redirected instead of leaving cleanly.

### Expected Variable Pattern

- `B_out`: low/medium
- `J_bound`: medium/high
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium/high

### Likely Outcome

- trapping
- weak partial handoff
- localised oscillatory retention

### Interpretation

This is the exit analogue of the trapping cases already emerging in compatibility modelling.

The event is not incoherent enough to scatter immediately, but not releasable enough to leave.

### Best Use

- rough surfaces
- layered exits
- interfaces with poor terminal continuity

## Geometry E4: Boundary Return at Exit

### Description

The internal event reaches the boundary and is redirected back into the source whole rather than released outward.

### Expected Variable Pattern

- `B_out`: low/medium
- `J_bound`: high
- `J_trans`: low
- `Q_coh`: medium/high
- `D`: low/medium

### Likely Outcome

- partial inward return
- degraded release
- reflection-like internal redirection

### Interpretation

This case matters because it shows that poor exit does not always mean outward scattering.

Sometimes the boundary preserves too much structured response for scattering, but not enough release capacity for outward handoff.

### Best Use

- strongly bounded exits
- polished but non-releasing surfaces
- cases where internal propagation remains organised right up to the edge

## Exit Geometry by Whole Type

## Glass -> Air

### Best Current Reading

The glass whole can carry propagation internally through distributed permissive order, but the final surface layer can degrade release quality more than the bulk degrades transmission quality.

### Most Plausible Exit Geometries

- E1 in clean cases
- E2 in ordinary imperfect cases
- E3 where surface disorder rises

### Best Current Variable Profile

- `B_out`: medium/high
- `J_bound`: medium
- `J_trans`: medium
- `Q_coh`: medium
- `D`: medium/high

### Current Judgment

Glass exit is viable, but fragile.

The weak point is not internal propagation; it is final release coherence.

## Crystal -> Air

### Best Current Reading

The crystal whole can carry more patterned internal propagation, but that pattern must be relaxed or converted at the final boundary if release is to succeed.

### Most Plausible Exit Geometries

- E1 in strong cases
- E4 when ordered boundary response returns the event inward
- E3 when release begins but stalls

### Best Current Variable Profile

- `B_out`: high
- `J_bound`: medium/high
- `J_trans`: medium
- `Q_coh`: high
- `D`: low

### Current Judgment

Crystal exit has stronger release potential than glass exit, but also more pressure on orderly conversion at the boundary.

So it may be:

- cleaner when successful
- more selective in how success is achieved

## What Exit Geometry Suggests About `B_out`

Current best reading:

- `B_out` is not merely the mirror of `B_in`

It appears to mean:

- the degree to which a source whole can release an already-organised internal event into a viable outward transition without dominant retention, return, or scattering

That definition is stronger than the earlier shorthand and better matches the current modelling.

## What Exit Geometry Suggests About `J_bound` and `J_trans`

The split continues to hold.

### `J_bound`

At exit, this appears to control:

- how strongly the final boundary responds to the incoming internal event
- whether the boundary forms a structured release event, a retention event, or a return event

### `J_trans`

At exit, this appears to control:

- whether the event can continue through the final release region without stalling or diffusing

That means the split is still useful, and perhaps even more important for exit than for entry.

## Cross-Geometry Findings

## 1. Exit Depends More on Terminal Layer Quality Than Entry Does

This is the clearest result in the document.

A whole may:

- admit well
- propagate well
- but release poorly

The terminal layer is therefore not a minor detail.

## 2. Glass Exit and Crystal Exit Fail Differently

Current distinction:

- glass exit tends to fail by surface diffusion or release fragility
- crystal exit tends to fail by over-ordered boundary return or stalled release conversion

This is a good sign for the model, because it means the whole types are not failing in generic ways.

## 3. Trapping and Return Are Both Real Exit Modes

That matters because poor release is not one thing.

It may produce:

- scattering
- trapping
- return

depending on how much organisation remains in the boundary event.

## 4. Exit Geometry Now Looks Modelable Without Another Variable Split

At present, the refined variable set seems good enough.

The main need is not new primitives, but:

- more concrete exit pairings
- better geometric comparison

## Confidence

- confidence that exit is not just reversed entry: `9/10`
- confidence that `B_out` is now better defined: `8/10`
- confidence that the `J_bound` / `J_trans` split remains useful on exit: `9/10`
- confidence that glass and crystal exits now fail in distinguishable ways: `8/10`
- confidence that another split is needed immediately: `3/10`

## Recommendation

Do not split more variables yet.

Use the current refined set to deepen release modelling directly.

## Next Move

The best next artifact is:

- `ams-exit-pairings-scoreboard-v1.md`

That should rank:

- glass -> air
- crystal -> air
- glass -> crystal exit-side variants where relevant
- metal-surface release edge cases if needed

by:

- explanatory strength
- geometry maturity
- usefulness for next-step release modelling

That will show whether the next deepening target should be:

- crystal release
- glass release
- or retained/returned exit modes.
