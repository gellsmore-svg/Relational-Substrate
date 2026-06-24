# AMS Case Library Expansion Plan v1

## Purpose

This document formalises the next-case priorities for expanding the AMS formalised interface-case library.

The need for this plan follows from:

- `ams-case-similarity-and-clustering-note-v1.md`

The current case library is already meaningful, but it should not be expanded arbitrarily. New cases should be added only where they strengthen:

- the main frontier cluster
- the main anchor contrasts
- the main degradation contrasts

This plan identifies:

- which additions are highest priority
- why each is needed
- what structural gap each fills
- and what order they should be developed in

## Current Case-Library State

### Main benchmark cases already formalised

- `air -> glass`
- `glass -> air`
- `air -> polished metal`
- `air -> oxidised metal`
- `glass -> crystal`
- `crystal -> air`

### Focused subcases already formalised

- `glass -> air [pocket-dominant]`
- `glass -> crystal [selective_success]`
- `glass -> crystal [mixed_frontier]`

## Current Structural Picture

### Strongest frontier cluster

- glass frontier cluster

Main cases:

- `glass -> air`
- `glass -> crystal`
- `glass -> crystal [mixed_frontier]`

### Strongest broad anchors

- `air -> glass`
- `crystal -> air`

### Strongest return-side anchor

- `air -> polished metal`

### Strongest degradation contrast

- `air -> oxidised metal`

## Expansion Principle

New cases should be added only if they do one of the following:

1. sharpen an unresolved internal distinction inside the glass frontier cluster
2. isolate a route/obstruction/dominance mode currently mixed with others
3. strengthen a comparison cluster that is underrepresented
4. bridge two neighbouring clusters without collapsing them

If a proposed case does not do one of these, it should not be added yet.

## Priority Order

## Priority 1: Expand the Glass Frontier Cluster Internally

This is the highest priority because the glass frontier cluster is now the programme’s centre of gravity.

### Case 1

- `glass -> air [diffuse-dominant]`

### Why it is needed

The current library already has:

- the broader `glass -> air`
- the `glass -> air [pocket-dominant]` subcase

What it lacks is a clean:

- `D3`
- `O5`
- `R2`

glass release benchmark.

### Structural gap filled

- separates diffuse release from pocket-dominant release inside the same benchmark family
- strengthens the degradation side of the glass release cluster
- makes the `D2` versus `D3` distinction more operational

### Why priority is high

Because the current library over-represents pocket and mixed glass release compared with explicitly diffuse glass release.

## Priority 2: Sharpen the Glass->Crystal Frontier Internally

### Case 2

- `glass -> crystal [late-gate dominated]`

### Why it is needed

The current library already has:

- `glass -> crystal [selective_success]`
- `glass -> crystal [mixed_frontier]`

What it lacks is a cleaner subcase focused primarily on:

- `O2`
- `R3`

without strong `R5` competition.

### Structural gap filled

- isolates blocked real compatibility route logic
- clarifies the `O2 -> R3` side of the compatibility frontier
- strengthens comparison with the mixed-frontier glass->crystal case

### Why priority is high

Because `glass -> crystal` is the strongest compatibility frontier and the library should separate its main subfamilies more cleanly.

## Priority 3: Strengthen the Return-Side Comparison Cluster

### Case 3

- `crystal -> air [ordered return dominated]`

### Why it is needed

The current `crystal -> air` case is useful, but it still mixes:

- viable ordered release
- failed ordered release
- return-side structure

The library would benefit from a clearer subcase centred on:

- `R4`
- `O4`
- route reality that remains strong but inwardly biased

### Structural gap filled

- strengthens Cluster C3
- gives a better comparison partner for `air -> polished metal`
- clarifies return-side organisation outside the polished-metal benchmark

### Why priority is medium-high

Because return-side structure is important, but the glass frontier still remains the main library priority.

## Priority 4: Entry-Side Degradation Bridge

### Case 4

- `air -> rough glass`

### Why it is needed

The current library has:

- clean entry (`air -> glass`)
- complex exit (`glass -> air`)

but it does not yet have a clean case that shows:

- degraded entry into a glass-like whole

### Structural gap filled

- bridges the entry anchor and the glass release frontier
- shows how glass-like degradation appears on the receiving side rather than only on exit
- clarifies whether roughened glass entry behaves more like:
  - weakened `O1`
  - or early `O5`

### Why priority is medium

Because it is structurally useful, but less central than deepening the internal glass frontier subcases first.

## Lower-Priority Candidate Cases

These are worth keeping in reserve, but should not come first.

### Candidate 5

- `air -> crystal [selective-failure subcase]`

Why lower priority:

- route-dominant anchors are already reasonably well represented

### Candidate 6

- `air -> partially oxidised metal`

Why lower priority:

- degradation contrast is already represented at the strong end
- the frontier gains are currently greater inside the glass family

### Candidate 7

- `glass -> metal`

Why lower priority:

- already conceptually represented as a mixed transmission/reflection case
- not the sharpest current structural gap

## Recommended Expansion Order

The best next-case order is:

1. `glass -> air [diffuse-dominant]`
2. `glass -> crystal [late-gate dominated]`
3. `crystal -> air [ordered return dominated]`
4. `air -> rough glass`

### Why this order works

- the first two deepen the main frontier cluster directly
- the third strengthens the underdeveloped return-side comparison cluster
- the fourth builds an entry-side bridge without distracting from the core frontier

## What Each Addition Should Clarify

## `glass -> air [diffuse-dominant]`

Should clarify:

- `D2` vs `D3`
- `O3` vs `O5`
- `R5` vs `R2`

## `glass -> crystal [late-gate dominated]`

Should clarify:

- `O2 -> R3`
- blocked real compatibility route logic
- route reality grade `G_C` in a cleaner cross-whole form

## `crystal -> air [ordered return dominated]`

Should clarify:

- `O4 -> R4`
- how ordered return differs from pocket-driven pseudo-progression
- directional route-reality asymmetry

## `air -> rough glass`

Should clarify:

- entry-side degradation of a glass-like whole
- whether receiving-side roughness behaves more like selective narrowing failure or broad diffusion weakening

## Expansion Stop Rule

This is important.

Do not expand the library further than these four additions until:

- the new cases have been formalised
- clustered
- and checked against the existing framework

Otherwise the library will start growing faster than its internal discrimination power.

## Confidence

- confidence that the expansion priorities are correctly ordered: `8/10`
- confidence that the first two additions should both be inside the glass frontier cluster: `9/10`
- confidence that `crystal -> air [ordered return dominated]` is the right third step: `8/10`
- confidence that `air -> rough glass` is the right bridge case after that: `7/10`

## Recommendation

Do not expand the library widely.

Expand it strategically in the order above.

## Next Move

The best next artifact is:

- `glass-to-air-diffuse-dominant-subcase-v1.md`

That should be the first actual addition under this expansion plan and should formalise the clean `D3 / O5 / R2` glass-release subcase so the internal structure of the glass frontier cluster becomes sharper.*** End Patch
