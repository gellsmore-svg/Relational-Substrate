# Crystal-to-Air Ordered-Return-Dominated Subcase v1

## Purpose

This document adds the third planned case under:

- `ams-case-library-expansion-plan-v1.md`

The specific goal is to isolate a clean:

- `crystal -> air [ordered return dominated]`

subcase.

The broader `crystal -> air` benchmark already carries:

- viable ordered release
- failed ordered release
- return-side structure

That is useful, but it means the return-side logic is still partly mixed with the release-side logic. This subcase separates it out.

## Core Character

This is the crystal-to-air subcase in which:

- a strongly ordered internal event reaches the boundary
- route organisation remains strong
- outward completion does not dominate
- the event resolves into structured inward return rather than pocketing, diffusion, or fragmentation

So the main governing layer is:

- `O4`

and the main route logic is:

- `R4`

rather than:

- `R1`
- `R3`
- or mixed release-side competition

## Main Current Reading

Best current structural profile:

- route reality remains strong
- directional asymmetry dominates
- the boundary preserves organised return-side viability better than outward completion viability
- pseudo-route pocketing is weak

This is the cleanest current case for:

- ordered return
- directional route asymmetry
- high-quality non-completion

## Active Formal Profile

### Zones

- `Z_A` strong, but return-biased
- `Z_B` weak
- `Z_C` weak

### Dominance

- `D1(return-biased)`

### Route Classes

- `R4`
- weak `R1` as unrealised release-side neighbour

### Obstruction Classes

- `O4`
- weak `O2` as a secondary comparison edge

### Route-Reality Grades

- inward: `G_A`
- outward: `G_D` or weak `G_C` edge

## Formalised Case Expression

```text
crystal->air[ordered-return-dominated]
= Zones{Z_A(return-biased), (Z_B weak), (Z_C weak)}
= Dom{D1(return-biased)}
= Route{R4, (R1 weak outward)}
= Obst{O4, (O2 weak)}
= Grade{G_A inward / G_D outward, (G_C weak outward edge)}
= Flow{return dominance, weak unrealised release-side alternative}
```

## Why This Is Not the Viable Ordered Release Subcase

This must be stated clearly.

It is **not** the viable ordered release case because:

- outward completion does not dominate
- the narrow release route does not win
- the boundary preserves directional return better than release completion

So this is not:

- `R1`
- `O1`

at the centre.

It is:

- `R4`
- `O4`

at the centre.

## Why This Is Not a Pocketing or Diffuse Case

It is also **not**:

- `R5`
- `R2`
- `O3`
- `O5`

because:

- local pseudo-progressive looping does not dominate
- broad degraded continuation does not dominate
- route organisation remains strong and directional

That is one of the main reasons this subcase is important. It shows that not all non-completion is weak or degraded.

## Route Logic

## Dominant Route Class: `R4`

This is the central route logic.

Why:

- a coherent route survives
- but it is directionally biased inward rather than outward
- the event resolves by organised return rather than by route collapse

This is the cleanest return-side route benchmark outside the polished-metal case.

## Secondary Route Class: weak `R1`

This is present only as the neighbouring unrealised alternative:

- a narrow release route is nearby in possibility space
- but does not win

This is useful because it sharpens the distinction between:

- outward completion route reality
- inward return route reality

## Obstruction Logic

## Dominant Obstruction Class: `O4`

This is the core obstruction logic.

Why:

- the route field is not simply blocked
- it is biased
- the bias favours inwardly organised continuation over outward completion

This is exactly the current meaning of biasing obstruction.

## Secondary Obstruction Class: weak `O2`

This appears only as a neighbour condition:

- the event may look close to outward completion for part of its progression
- but the main structural logic is not late route failure
- it is directional bias

So `O2` is secondary here, not dominant.

## Event-Flow Reading

Most likely flows:

- `Z_A -> R4`
- weak unrealised `Z_A -> completion`

### Interpretation

This subcase is what happens when:

- the interface preserves route organisation strongly
- but route leverage is asymmetrically weighted toward return

This makes it the cleanest ordered-return case in the current library.

## Route-Reality Reading

Best current grades:

- inward route reality: `G_A`
- outward route reality: `G_D` or weak `G_C`

### Why This Matters

This is one of the clearest demonstrations in the whole programme that:

- route reality must be direction-sensitive

The event does not lack route structure.
It lacks outwardly viable route structure.

That is a major stabilising result.

## Comparison to Existing Cases

## Compared with the Broader `crystal -> air` Benchmark

Broader `crystal -> air`:

- mixes viable ordered release with return-side structure

This subcase:

- isolates the return-dominant side

That makes the comparison family sharper internally.

## Compared with `air -> polished metal`

This is the most important comparison.

Both cases share:

- strong directional asymmetry
- `R4`
- `O4`

But they differ in surrounding structure:

- polished metal is the cleaner reflection-side anchor
- crystal return preserves a stronger neighbouring relation to ordered release

This makes crystal return the stronger bridge case between:

- route-dominant release
- and return-dominant non-completion

## Compared with `glass -> air [pocket-dominant]`

This is a strong contrast.

Glass pocket-dominant:

- `R5`
- `O3`
- `D2`

Crystal ordered-return dominated:

- `R4`
- `O4`
- `D1(return-biased)`

That is one of the clearest current illustrations that:

- not all non-completion is pocketing or degradation

## Structural Value to the Library

This subcase fills a real gap.

It gives the library:

- a cleaner `R4` comparison case
- a cleaner `O4` case outside polished metal
- a better return-side counterpart to the stronger glass frontier cases

Without it, the library is slightly too weak on the return-side comparison cluster.

This addition corrects that.

## Clustering Role

This case belongs:

- primarily in the return-side comparison cluster

It strengthens the family resemblance between:

- polished reflection
- ordered return

while still preserving their differences.

## Confidence

- confidence that this is a distinct useful subcase: `9/10`
- confidence that `O4 / R4` is the right core profile: `9/10`
- confidence that this fills a real library gap: `8/10`

## Recommendation

Add this case to the formalised case library as a standard return-side comparison subcase.

It should now sit alongside:

- `crystal -> air`
- `air -> polished metal`

as a stronger return-side bridge case.

## Next Move

The best next artifact is:

- `air-to-rough-glass-subcase-v1.md`

That should be the fourth planned library expansion case and should bridge:

- clean glass entry
- degraded glass release

by isolating a receiving-side glass roughness benchmark.*** End Patch
