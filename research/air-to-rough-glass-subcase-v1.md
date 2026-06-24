# Air-to-Rough-Glass Subcase v1

## Purpose

This document adds the fourth planned case under:

- `ams-case-library-expansion-plan-v1.md`

The specific goal is to isolate:

- `air -> rough glass`

as a receiving-side glass roughness benchmark.

The current library already contains:

- clean `air -> glass`
- mixed `glass -> air`
- diffuse-dominant `glass -> air`
- pocket-dominant `glass -> air`

What it lacks is a clean case showing how glass-like degradation behaves on the entry side rather than the release side.

This subcase fills that gap.

## Core Character

This is the glass-entry subcase in which:

- the receiving whole remains glass-like and transmissive in bulk
- the entry surface is rough, disordered, or locally degraded
- admission remains possible
- but clean handoff into distributed permissive order is weakened

So the main issue is:

- degraded receiving-side admission

not:

- terminal release failure

## Main Current Reading

Best current structural profile:

- the glass bulk still supports distributed permissive transmission
- the rough entry layer weakens or scatters incoming admission
- some routes remain viable
- some broaden or fail early
- pocketing is possible but not necessarily dominant

This case sits between:

- clean `air -> glass`

and:

- degraded glass release cases

but it is not identical to either.

## Active Formal Profile

### Zones

- `Z_A` present but weakened
- `Z_C` present
- `Z_B` possible but secondary

### Dominance

- weak `D1`
- or `D3`
- sometimes `D4` under mixed roughness

### Route Classes

- `R1` weakened
- `R2`
- weak `R3` in more blocked local entry paths

### Obstruction Classes

- `O5`
- weak `O1`
- weak `O2` in local blocked-entry paths

### Route-Reality Grades

- `G_B`
- `G_C`

## Formalised Case Expression

```text
air->rough_glass
= Zones{Z_A weak, Z_C, (Z_B secondary)}
= Dom{weak D1 or D3, sometimes D4}
= Route{R1 weak, R2, (R3 weak)}
= Obst{O5, (O1 weak), (O2 weak)}
= Grade{G_B, G_C}
= Flow{Z_A->completion weakly, Z_A->Z_C, D4->Z_C in mixed roughness}
```

## Why This Is Not Clean `Air -> Glass`

Clean `air -> glass`:

- strong `Z_A`
- `D1`
- `R1 + R2`
- `O1` weak/selective
- `G_A / G_B`

Rough glass entry:

- weakened `Z_A`
- stronger `Z_C`
- weakened `R1`
- stronger `O5`
- more `G_C`

Main difference:

- entry is still possible, but admission quality is degraded before bulk propagation begins

## Why This Is Not `Glass -> Air`

This is important.

Rough glass entry is not the same as rough or fragile glass release.

`glass -> air` asks:

- can an already-propagating internal event leave cleanly?

`air -> rough glass` asks:

- can the receiving whole admit an incoming event despite degraded surface conditions?

So:

- `B_in` is under pressure here
- `B_out` is not the main variable

That makes this a distinct bridge case.

## Route Logic

## Route Class: weakened `R1`

Some narrow viable handoff routes remain.

This is why the case does not collapse into pure degradation.

But those routes are weaker than in clean `air -> glass`.

## Route Class: `R2`

Distributed weak routes become more important because the rough surface broadens or loosens entry behaviour.

This is one of the main reasons the case is useful.

## Route Class: weak `R3`

In local roughness pockets, an entry path may appear available but fail under actual admission.

This is secondary, but relevant.

## Obstruction Logic

## Dominant Obstruction Class: `O5`

Roughness mainly behaves here as:

- diffusing obstruction

Why:

- it broadens entry behaviour
- weakens route dominance
- does not necessarily create stable pocket capture

## Secondary Obstruction Class: weak `O1`

Some local selective routes may still remain. This is why `R1` is weakened but not absent.

## Secondary Obstruction Class: weak `O2`

Some local entry paths may fail late enough to behave like weak blocked apparent routes.

This is not the core logic.

## Event-Flow Reading

Most likely flows:

- `Z_A -> completion weakly`
- `Z_A -> Z_C`
- `D4 -> Z_C`

### Interpretation

This subcase is what happens when:

- receiving-side glass admission is degraded
- but not destroyed
- and diffusion pressure competes with weak route completion

## Route-Reality Reading

Best current grades:

- `G_B`
- `G_C`

Why:

- some routes remain weak but real
- others are apparent or unreliable
- pseudo-route dominance is not usually the main feature

This makes the case different from:

- pocket-dominant glass release

and closer to:

- diffuse-dominant entry-side degradation

## Comparison to Existing Cases

## Compared with Clean `Air -> Glass`

Clean entry:

- `D1`
- strong `R1`
- weak/selective `O1`

Rough entry:

- weak `D1` or `D3`
- weakened `R1`
- stronger `R2`
- dominant `O5`

## Compared with `Glass -> Air [Diffuse-Dominant]`

Both share:

- `O5`
- `R2`
- `D3`

But they differ by direction:

- rough entry stresses `B_in`
- diffuse release stresses `B_out`

This is the main reason this bridge case matters.

## Compared with `Air -> Oxidised Metal`

Both involve degraded interfaces, but:

- rough glass still retains stronger transmissive bulk logic
- oxidised metal trends more toward fragmentation and degraded reflection

So rough glass is a weaker and more transmissive degradation case.

## Structural Value to the Library

This subcase fills a real gap.

It gives the library:

- a receiving-side degradation case for glass
- a bridge between clean entry and degraded release
- a better way to compare `B_in` pressure against `B_out` pressure

Without it, the library is slightly too exit-heavy in its treatment of glass roughness and degradation.

## Clustering Role

This case belongs between:

- the broad route-dominant anchor cluster
- the glass frontier cluster
- the degradation contrast cluster

It is a bridge case, not a pure anchor or pure frontier.

That is its main value.

## Confidence

- confidence that this is a distinct useful bridge case: `8/10`
- confidence that `O5 / R2 / weak R1` is the right core profile: `8/10`
- confidence that this fills a real library gap: `8/10`

## Recommendation

Add this case to the formalised case library as a standard receiving-side glass degradation subcase.

It should be used when comparing:

- clean admission
- degraded admission
- fragile release

inside the glass family.

## Next Move

The best next artifact is:

- `ams-expanded-case-library-update-v1.md`

That should update the formalised case library with the four planned additions:

- `glass -> air [diffuse-dominant]`
- `glass -> crystal [late-gate dominated]`
- `crystal -> air [ordered-return dominated]`
- `air -> rough glass`

and then reassess the cluster structure after expansion.*** End Patch
