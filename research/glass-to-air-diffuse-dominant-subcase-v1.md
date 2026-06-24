# Glass-to-Air Diffuse-Dominant Subcase v1

## Purpose

This document adds the first new case under:

- `ams-case-library-expansion-plan-v1.md`

The specific goal is to isolate a clean:

- `glass -> air [diffuse-dominant]`

subcase.

The broader `glass -> air` benchmark already carries:

- blocked route behaviour
- pocket-dominant pseudo-release
- diffuse release

That richness is useful, but it also means the internal structure of the glass frontier cluster is still under-separated.

This subcase is meant to fix that by giving the diffuse side of glass release a cleaner formal identity.

## Core Character

This is the glass-release subcase in which:

- the event still resolves outward to some degree
- route dominance is weakened broadly rather than pocket-captured locally
- bounded local pseudo-route structure is not the main winner
- the dominant failure is broadening and weakening of continuation

So the main governing layer is:

- `D3`

rather than:

- `D2`
- or `D4 -> D2`

## Main Current Reading

Best current structural profile:

- route logic present only weakly
- no dominant bounded pocket takes over
- terminal-layer weakening broadens the event
- outward continuation survives, but degraded

This is the cleanest current glass-side case for:

- diffuse release
- `O5`
- `R2`

## Active Formal Profile

### Zones

- `Z_C` strong
- `Z_A` weak
- `Z_B` weak or non-dominant

### Dominance

- `D3`

### Route Classes

- `R2`
- weak `R3` possible at the edge

### Obstruction Classes

- `O5`
- weak `O2` possible in more structured degraded variants

### Route-Reality Grades

- `G_C`
- sometimes `G_B/C` edge if a weak real route still survives

## Formalised Case Expression

```text
glass->air[diffuse-dominant]
= Zones{Z_C, (Z_A weak), (Z_B weak)}
= Dom{D3}
= Route{R2, (R3 weak)}
= Obst{O5, (O2 weak)}
= Grade{G_C, (G_B/G_C edge)}
= Flow{Z_A->Z_C weakly, D4->Z_C in mixed degraded variants, Z_C persistence}
```

## Why This Is Not the Pocket-Dominant Subcase

This must be stated clearly.

It is **not** the pocket-dominant glass release case because:

- local bounded reseating does not dominate the whole-interface outcome
- pseudo-progressive looping is not the main event
- `R5` is not the central route class
- `O3` is not the central obstruction class

Instead:

- broad weakening of route dominance
- weak distributed continuation
- and degraded outward spreading

are doing the main work.

## Route Logic

## Dominant Route Class: `R2`

This is the central route logic in the subcase.

Why:

- some outward continuation remains
- route count may still be moderate
- no one route dominates strongly
- no bounded pseudo-route pocket dominates strongly either

This is exactly the shape of:

- weak distributed continuation

## Secondary Route Class: weak `R3`

This appears only at the edge of the subcase, where:

- one route may still look somewhat real
- but broad degradation is already overtaking it

This does not make `R3` dominant. It only marks the diffuse-dominant case as potentially adjacent to blocked-route conditions.

## Obstruction Logic

## Dominant Obstruction Class: `O5`

This is the core obstruction logic.

Why:

- the obstruction does not mainly create bounded pockets
- it does not mainly preserve one late-failing route
- it weakens route dominance broadly and allows the event to spread

This is exactly what diffusing obstruction means in the current framework.

## Secondary Obstruction Class: weak `O2`

This may appear at the edge where:

- one route remains partly viable for a time
- but broad weakening still dominates the whole-interface result

Again, this is secondary only.

## Event-Flow Reading

Most likely flows:

- `A -> C`
- `D4 -> C`
- `C -> C` persistence

### Interpretation

This subcase is what happens when:

- route-led activity weakens
- pocket capture does not take over decisively
- diffuse broadening becomes the dominant result

That is why it matters. It gives the programme a cleaner outcome class than the broader glass release benchmark alone.

## Route-Reality Reading

Best current grade:

- `G_C`

Why:

- forward continuity is weak
- directional commitment is weakened
- completion remains more apparent than robust
- looping does not dominate enough for `G_D`
- but route reality is too weak to count as strong `G_B`

This is one of the clearest current cases for:

- apparent but unreliable route structure

without strong pseudo-route pocketing.

## Comparison to Existing Glass Release Cases

## Compared with the Main `glass -> air` Benchmark

The main benchmark is richer and more mixed:

- `Z_A`
- `Z_B`
- `Z_C`

with:

- `D4 -> D2`

often dominant.

This new subcase strips that down and says:

- what if diffusion wins cleanly?

That is the point of the new case.

## Compared with `glass -> air [pocket-dominant]`

This is the most important comparison.

Pocket-dominant:

- `D2`
- `R5`
- `O3`

Diffuse-dominant:

- `D3`
- `R2`
- `O5`

Pocket-dominant:

- bounded local reseating wins

Diffuse-dominant:

- broad degraded continuation wins

This comparison is exactly why the new case is needed.

## Structural Value to the Library

This subcase fills a real gap.

It gives the library:

- a cleaner `D3` glass benchmark
- a cleaner `O5` glass benchmark
- a cleaner `R2` glass benchmark

Without it, the glass cluster is slightly too weighted toward:

- mixed competitive
- pocket-dominant
- pseudo-route logic

This addition corrects that imbalance.

## Clustering Role

This case belongs primarily in:

- the glass frontier cluster

but it also strengthens:

- the degradation-contrast cluster

because it sits between:

- the rich mixed glass frontiers
- and the more fully degraded / fragmenting cases like oxidised metal

That bridge role is one of its main values.

## Confidence

- confidence that this is a distinct useful subcase: `9/10`
- confidence that `D3 / O5 / R2` is the right core profile: `8/10`
- confidence that this fills a real library gap: `9/10`

## Recommendation

Add this case to the formalised case library as a standard glass frontier subcase.

It should now sit alongside:

- `glass -> air`
- `glass -> air [pocket-dominant]`

as the cleaner diffusion-side counterpart.

## Next Move

The best next artifact is:

- `glass-to-crystal-late-gate-dominated-subcase-v1.md`

That should be the second planned library expansion case and should isolate the clean:

- `O2`
- `R3`

side of the `glass -> crystal` frontier.*** End Patch
