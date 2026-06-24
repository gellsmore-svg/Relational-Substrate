# AMS Formalised Case Library v1

## Purpose

This document applies the compact notation from:

- `ams-interface-formalisation-sketch-v1.md`

to the strongest benchmark cases in the programme.

The aim is to create the first small library of standardised interface-case expressions so the framework can be reused without re-deriving the same descriptive structure each time.

This is not yet a full corpus. It is a formalised benchmark set.

## Notation Reminder

Core structure:

```text
<pairing>
= Zones{...}
= Dom{...}
= Route{...}
= Obst{...}
= Grade{...}
= Flow{...}
```

Core symbols:

- Zones:
  - `Z_A` route-dominant zone
  - `Z_B` pocket-dominant zone
  - `Z_C` diffusing fringe
- Dominance:
  - `D1` route-dominant
  - `D2` pocket-dominant
  - `D3` diffusion-dominant
  - `D4` mixed competitive
- Routes:
  - `R1` narrow viable route
  - `R2` distributed weak routes
  - `R3` blocked apparent route
  - `R4` inward-biased route
  - `R5` loop-dominated pseudo-route
  - `R6` fragmenting route field
- Obstruction:
  - `O1` funnelling
  - `O2` late-gate
  - `O3` pocketing
  - `O4` biasing
  - `O5` diffusing
  - `O6` fragmenting
- Grades:
  - `G_A`
  - `G_B`
  - `G_C`
  - `G_D`

## Case 1: Air -> Glass

```text
air->glass
= Zones{Z_A, (Z_C weak)}
= Dom{D1}
= Route{R1, R2}
= Obst{O1, (O5 weak)}
= Grade{G_A, G_B}
= Flow{Z_A->completion, weak Z_A->Z_C under degraded entry}
```

### Reading

This remains the strongest broad entry anchor.

- route reality is strong
- permissive continuation is real
- weak diffusion only appears under degraded entry conditions

### Current Status

- anchor case

## Case 2: Glass -> Air

```text
glass->air
= Zones{Z_A, Z_B, Z_C}
= Dom{D4->D2}
= Route{R2, R3, R5}
= Obst{O2, O3, O5}
= Grade{G_B, G_C, G_D}
= Flow{Z_A->Z_B, Z_B->Z_B, Z_B->Z_C, D4->Z_B}
```

### Reading

This remains the strongest release-side frontier.

- real route logic is present
- pseudo-route pocketing is often the strongest local winner
- diffuse fringe emerges when pocket coherence weakens

### Current Status

- frontier case

## Case 3: Air -> Polished Metal

```text
air->polished_metal
= Zones{Z_A(return-biased boundary field)}
= Dom{D1(return-biased)}
= Route{R4}
= Obst{O4}
= Grade{G_A inward / G_D outward}
= Flow{return dominance}
```

### Reading

This is the cleanest reflection anchor.

- route reality is strong inwardly
- outward completion-side route reality is weak
- biasing obstruction dominates

### Current Status

- anchor case

## Case 4: Air -> Oxidised Metal

```text
air->oxidised_metal
= Zones{(Z_A weak), Z_C}
= Dom{D3}
= Route{R3, R6}
= Obst{O2, O6, (O4 weak)}
= Grade{G_C/G_D}
= Flow{Z_A->Z_C, D4->Z_C in mixed degraded cases}
```

### Reading

This is the strongest degradation contrast case.

- some route logic survives temporarily
- fragmentation and diffuse degradation dominate overall

### Current Status

- anchor degradation case

## Case 5: Glass -> Crystal

```text
glass->crystal
= Zones{Z_A, Z_B, (Z_C weak)}
= Dom{D1 or D4}
= Route{R1, R3, R5}
= Obst{O1, O2, O3}
= Grade{G_B/G_A, G_C, G_D}
= Flow{Z_A->completion, Z_A->Z_B, D4->Z_A, D4->Z_B}
```

### Reading

This remains the strongest compatibility frontier.

- narrow viable handoff can be real
- late blockage is common
- pseudo-compatibility local zones can coexist with real admissible routes

### Current Status

- frontier case

## Case 6: Crystal -> Air

```text
crystal->air
= Zones{Z_A, (Z_B weak), (Z_C weak)}
= Dom{D1}
= Route{R1, R4, (R3 secondary)}
= Obst{O1, O2, O4}
= Grade{G_A, G_B/G_C}
= Flow{Z_A->completion, Z_A->R4 in ordered return cases}
```

### Reading

This is the strongest ordered-release comparison case.

- route reality is preserved better than in glass-side failures
- ordered return remains a serious competing logic
- pseudo-route pocketing is weaker here than in glass frontier cases

### Current Status

- anchor comparison case

## Case 7: Glass -> Air, Pocket-Dominant Subcase

```text
glass->air[pocket-dominant]
= Zones{Z_B, Z_C}
= Dom{D2}
= Route{R5, (R2 secondary)}
= Obst{O3, O5}
= Grade{G_D, (G_C fringe)}
= Flow{Z_B->Z_B, Z_B->Z_C}
```

### Reading

This is a useful specialised subcase because it isolates:

- pocket capture
- pseudo-route persistence
- bleed into diffuse release

without the stronger route-zone competition of the broader benchmark.

### Current Status

- specialised frontier subcase

## Case 8: Glass -> Crystal, Selective Success Subcase

```text
glass->crystal[selective_success]
= Zones{Z_A}
= Dom{D1}
= Route{R1}
= Obst{O1}
= Grade{G_A/G_B}
= Flow{Z_A->completion}
```

### Reading

This is the clean selective-compatibility success case.

- one narrow viable route survives
- pocketing and diffusion remain weak enough not to capture the event

### Current Status

- specialised success subcase

## Case 9: Glass -> Crystal, Mixed Frontier Subcase

```text
glass->crystal[mixed_frontier]
= Zones{Z_A, Z_B}
= Dom{D4}
= Route{R3, R5, (R1 weak)}
= Obst{O2, O3, (O1 weak)}
= Grade{G_C, G_D, (G_B weak)}
= Flow{Z_A->Z_B, D4->Z_A, D4->Z_B}
```

### Reading

This is the clearest frontier-only subcase for the whole programme.

- blocked route logic
- pseudo-route logic
- unstable competition between real and apparent completion

### Current Status

- specialised frontier subcase

## Cross-Case Observations

## 1. The Notation Reuses Cleanly

This is the main result.

The benchmark cases can now be represented compactly without losing the main distinctions:

- zones
- dominance mode
- route classes
- obstruction classes
- route-reality grades
- main flow tendencies

## 2. Anchor and Frontier Cases Separate More Cleanly

Current anchors:

- `air->glass`
- `air->polished_metal`
- `air->oxidised_metal`
- `crystal->air`

Current frontiers:

- `glass->air`
- `glass->crystal`

This is now visible very quickly from the library expressions themselves.

## 3. Glass Cases Remain the Richest

This is reinforced again.

Glass-side cases support:

- `R2`
- `R3`
- `R5`

and:

- `O2`
- `O3`
- `O5`

with:

- `D4`
- `D2`

appearing repeatedly.

That makes them the densest cases in the library.

## 4. Reflection and Ordered Return Are Now Compact

The polished-metal and crystal-release cases are especially useful here because the formalisation compresses their directional asymmetry cleanly.

## Current Weak Point

The notation is now usable, but it is still primarily:

- case-summary notation

It is not yet:

- comparison-optimised notation

for rapid side-by-side similarity judgments or clustering.

That is the next obvious refinement if the library grows.

## Confidence

- confidence that the notation works across the benchmark cases: `9/10`
- confidence that the case library is already useful as a reusable reference: `8/10`
- confidence that no additional notation growth is needed before more applications: `8/10`

## Recommendation

Keep the notation stable.

Use this case-library format for future additions rather than inventing new ad hoc summaries.

## Next Move

The best next artifact is:

- `ams-case-similarity-and-clustering-note-v1.md`

That should compare the formalised cases and identify:

- which cases cluster together
- which cases are genuine outliers
- which cases should be added next if the library is expanded beyond the current benchmark set
