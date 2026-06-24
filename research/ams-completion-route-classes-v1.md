# AMS Completion Route Classes v1

## Purpose

This document develops the next layer implied by:

- `ams-l-escape-study-v1.md`

The main question is:

- what kinds of completion routes does a stalled interface event actually have available?

That question matters because the current programme now uses `L_escape` as a meaningful geometric descriptor, but still lacks a strong classification of the route types that make escape viable, weak, misleading, inward-biased, or effectively pseudo-routelike.

So the purpose of this document is to classify the main route types available to stalled events and show how they differ.

## Core Claim

Not all apparent routes are real completion routes.

Some routes are:

- narrow but viable
- broad but weak
- geometrically open but functionally blocked
- biased toward inward resolution
- loop-dominated and only pseudo-escapes

That means route-class matters as much as route-count.

## Context

The main stalled-event family still under analysis is:

- `L3` elongated stall

and the main resolution paths remain:

- successful handoff
- trapped release
- ordered return
- broken multi-loop fragmentation

Route classes are therefore being defined to explain why one of those resolutions becomes dominant.

## Route Classes

## Class R1: Narrow Viable Route

### Description

A small number of highly constrained but genuinely completable routes remain available to the stalled event.

### Main Characteristics

- low route count
- high local continuity
- adequate coherence preservation
- strong dominance if taken

### Typical Relation to Variables

- `J_trans`: high or rising
- `Q_coh`: medium/high or high
- `D`: low/medium
- `L_escape`: high

### Likely Resolution

- successful handoff

### Interpretation

This is the most important route class for completion.

It shows that a stalled event does not need many options. It needs:

- at least one route that remains genuinely viable

This is one of the strongest reasons not to equate escape with openness.

## Class R2: Distributed Weak Routes

### Description

Many possible continuations appear locally available, but none is strong enough to dominate cleanly.

### Main Characteristics

- moderate or high route count
- weak continuity per route
- local competition among continuations
- no clear dominant channel

### Typical Relation to Variables

- `J_trans`: medium
- `Q_coh`: medium
- `D`: medium
- `L_escape`: medium

### Likely Resolutions

- diffuse release
- trapped release
- unstable partial completion

### Interpretation

This is the classic intermediate regime.

The event is not shut down, but its available routes are too weakly structured to force completion.

## Class R3: Blocked Apparent Route

### Description

A route appears geometrically open, but functionally it cannot support completion.

### Main Characteristics

- apparent path present
- continuity breaks late or repeatedly
- route looks open but fails under actual progression

### Typical Relation to Variables

- `J_trans`: low/medium
- `Q_coh`: medium or falling
- `D`: medium/high
- `L_escape`: low/medium despite apparent openness

### Likely Resolutions

- trapped release
- partial handoff failure
- funnel stall

### Interpretation

This is one of the most important route classes in the whole programme.

It explains why some stalled events seem close to completion but never actually finish.

## Class R4: Inward-Biased Route

### Description

The available path structure is more favourable to organised return or inward redirection than to completion.

### Main Characteristics

- strong directional asymmetry
- route continuity preserved, but inwardly
- outward completion options weak or inferior

### Typical Relation to Variables

- `J_bound`: high
- `J_trans`: low/medium
- `Q_coh`: high
- `D`: low/medium
- `L_escape`: low outwardly

### Likely Resolution

- ordered return

### Interpretation

This is important because it shows that low completion escape does not necessarily imply disorder.

Some stalls remain highly organised, but along the wrong directional outcome for outward completion.

## Class R5: Loop-Dominated Pseudo-Route

### Description

The stalled event has local motion and repeated reseating, but those paths do not truly progress toward completion.

### Main Characteristics

- strong local cycling
- little or no net advance toward exit or handoff
- persistent local activity mistaken for route availability

### Typical Relation to Variables

- `J_bound`: medium/high
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium
- `L_escape`: low/medium but overestimated if judged naively

### Likely Resolution

- trapped release
- shallow retention
- elongated stall without completion

### Interpretation

This class is essential because it distinguishes:

- active local behaviour

from:

- true completion viability

Without this class, trapped release would be too easily misread as almost-completed release.

## Class R6: Fragmenting Route Field

### Description

No single route remains strong enough to dominate. The available continuations break into multiple weak, partially disconnected local options.

### Main Characteristics

- route coherence deteriorates
- route competition intensifies
- no stable elongated path persists

### Typical Relation to Variables

- `J_trans`: low
- `Q_coh`: low/medium
- `D`: medium/high or high
- `L_escape`: low

### Likely Resolution

- broken multi-loop fragmentation
- scattering

### Interpretation

This is the route-level equivalent of `L4`.

It marks the point where the event ceases to retain one usable transition logic.

## Route-Class Table

| Route class | Route count | Route quality | Dominant direction | Typical `L_escape` | Typical resolution |
|---|---|---|---|---:|---|
| R1 narrow viable route | low | high | outward / onward | high | successful handoff |
| R2 distributed weak routes | medium/high | weak/moderate | contested | medium | diffuse release / trapping |
| R3 blocked apparent route | apparent low/medium | misleading | nominally outward, functionally blocked | low/medium | trapping / partial failure |
| R4 inward-biased route | low/medium | high inwardly | inward | low outwardly | ordered return |
| R5 loop-dominated pseudo-route | low/medium | locally active but non-completing | local cycling | low/medium | trapped release |
| R6 fragmenting route field | medium/high | low | none dominant | low | fragmentation / scattering |

## Strongest Pairwise Distinctions

## R1 vs R2

Main difference:

- route dominance

R1:

- one viable route is enough

R2:

- many weak routes compete and completion does not dominate

## R2 vs R5

Main difference:

- weak distributed continuation versus local cycling without real progression

R2:

- still retains genuine, if weak, outward possibilities

R5:

- looks active but mostly recycles locally

## R3 vs R5

Main difference:

- blocked apparent route versus pseudo-route

R3:

- a route appears real but fails under progression

R5:

- the event mostly never had a true completion route in the first place, only local cycling that mimics one

## R4 vs R1

Main difference:

- same possibility of strong route quality
- opposite directional bias

This is one of the clearest reasons why `L_escape` should remain interpreted as:

- completion-side viability

rather than generic route quality.

## R6 vs All Others

Main difference:

- loss of dominant route logic

R6 is the breakdown regime where the route field stops behaving like one stalled event with a latent resolution and starts behaving like fragmented partial events.

## Best Current Mapping to Main Cases

## Glass Release

Strongest route classes:

- `R2` distributed weak routes
- `R3` blocked apparent route
- `R5` loop-dominated pseudo-route

This fits the idea that glass can preserve activity and partial continuation without guaranteeing completion.

## Crystal Release

Strongest route classes:

- `R1` narrow viable route
- `R4` inward-biased route
- some `R3`

This fits the more selective and more ordered character of crystal release.

## Glass->Crystal Compatibility Stall

Strongest route classes:

- `R1` narrow viable route
- `R3` blocked apparent route
- `R5` loop-dominated pseudo-route

This is one of the clearest mixed cases because the event may seem close to completion while still lacking a true admissible handoff route.

## Programme-Level Gains

## 1. `L_escape` Is Now Much Less Vague

This is the main result.

The programme can now say not only that escape is high or low, but:

- what kind of route structure remains

## 2. Trapped Release Is Much Better Understood

The strongest trapped-release route classes now appear to be:

- `R3`
- `R5`

That is a significant clarification.

## 3. Ordered Return Is Now Cleaner

Return is now best understood not only as strong boundary response, but as:

- survival of an inward-biased high-quality route

That is stronger than the earlier looser description.

## 4. Completion Is No Longer Confused with Openness

That is one of the deepest conceptual gains in the entire recent sequence.

The relevant question is not:

- how many ways forward seem open?

but:

- whether any route remains truly viable enough to dominate resolution

## Current Weak Point

The current route classes are strong conceptually, but they still need one harder test:

- can they discriminate the main benchmark cases cleanly when put side by side?

That is the obvious next step.

## Confidence

- confidence that route class matters as much as route count: `9/10`
- confidence that `R1-R6` is a useful first route taxonomy: `8/10`
- confidence that `R3` and `R5` are especially important for trapped release: `8/10`
- confidence that `R4` clarifies ordered return materially: `8/10`

## Recommendation

Keep `L_escape` as a geometric descriptor for now.

Do not formalise new route primitives yet.

Instead, pressure the route classes against the main benchmark cases directly.

## Next Move

The best next artifact is:

- `ams-route-class-benchmark-table-v1.md`

That should compare the main benchmark cases side by side:

- air -> glass
- glass -> air
- air -> polished metal
- air -> oxidised metal
- glass -> crystal
- crystal -> air

and mark which route classes dominate in each.*** End Patch
