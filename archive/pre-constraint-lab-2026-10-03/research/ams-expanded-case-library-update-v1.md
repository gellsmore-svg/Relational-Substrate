# AMS Expanded Case Library Update v1

## Purpose

This document updates the formalised case library after completing the first planned expansion cycle.

The expansion plan identified four additions:

- `glass -> air [diffuse-dominant]`
- `glass -> crystal [late-gate dominated]`
- `crystal -> air [ordered-return dominated]`
- `air -> rough glass`

Those cases now exist as separate studies. This document integrates them into the case-library structure and reassesses the cluster map after expansion.

## Source Additions

The four additions are:

- `glass-to-air-diffuse-dominant-subcase-v1.md`
- `glass-to-crystal-late-gate-dominated-subcase-v1.md`
- `crystal-to-air-ordered-return-dominated-subcase-v1.md`
- `air-to-rough-glass-subcase-v1.md`

## Updated Formalised Case Library

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

Status:

- anchor case

## Case 2: Air -> Rough Glass

```text
air->rough_glass
= Zones{Z_A weak, Z_C, (Z_B secondary)}
= Dom{weak D1 or D3, sometimes D4}
= Route{R1 weak, R2, (R3 weak)}
= Obst{O5, (O1 weak), (O2 weak)}
= Grade{G_B, G_C}
= Flow{Z_A->completion weakly, Z_A->Z_C, D4->Z_C in mixed roughness}
```

Status:

- bridge case

Structural role:

- receiving-side glass degradation
- `B_in` pressure
- bridge between clean entry and degraded glass-frontier cases

## Case 3: Glass -> Air

```text
glass->air
= Zones{Z_A, Z_B, Z_C}
= Dom{D4->D2}
= Route{R2, R3, R5}
= Obst{O2, O3, O5}
= Grade{G_B, G_C, G_D}
= Flow{Z_A->Z_B, Z_B->Z_B, Z_B->Z_C, D4->Z_B}
```

Status:

- frontier case

## Case 4: Glass -> Air [Pocket-Dominant]

```text
glass->air[pocket-dominant]
= Zones{Z_B, Z_C}
= Dom{D2}
= Route{R5, (R2 secondary)}
= Obst{O3, O5}
= Grade{G_D, (G_C fringe)}
= Flow{Z_B->Z_B, Z_B->Z_C}
```

Status:

- specialised frontier subcase

## Case 5: Glass -> Air [Diffuse-Dominant]

```text
glass->air[diffuse-dominant]
= Zones{Z_C, (Z_A weak), (Z_B weak)}
= Dom{D3}
= Route{R2, (R3 weak)}
= Obst{O5, (O2 weak)}
= Grade{G_C, (G_B/G_C edge)}
= Flow{Z_A->Z_C weakly, D4->Z_C in mixed degraded variants, Z_C persistence}
```

Status:

- specialised frontier/degradation bridge subcase

Structural role:

- clean `D3 / O5 / R2` glass-release benchmark
- separates diffuse release from pocket-dominant release

## Case 6: Air -> Polished Metal

```text
air->polished_metal
= Zones{Z_A(return-biased boundary field)}
= Dom{D1(return-biased)}
= Route{R4}
= Obst{O4}
= Grade{G_A inward / G_D outward}
= Flow{return dominance}
```

Status:

- anchor case

## Case 7: Air -> Oxidised Metal

```text
air->oxidised_metal
= Zones{(Z_A weak), Z_C}
= Dom{D3}
= Route{R3, R6}
= Obst{O2, O6, (O4 weak)}
= Grade{G_C/G_D}
= Flow{Z_A->Z_C, D4->Z_C in mixed degraded cases}
```

Status:

- anchor degradation case

## Case 8: Glass -> Crystal

```text
glass->crystal
= Zones{Z_A, Z_B, (Z_C weak)}
= Dom{D1 or D4}
= Route{R1, R3, R5}
= Obst{O1, O2, O3}
= Grade{G_B/G_A, G_C, G_D}
= Flow{Z_A->completion, Z_A->Z_B, D4->Z_A, D4->Z_B}
```

Status:

- frontier case

## Case 9: Glass -> Crystal [Selective Success]

```text
glass->crystal[selective_success]
= Zones{Z_A}
= Dom{D1}
= Route{R1}
= Obst{O1}
= Grade{G_A/G_B}
= Flow{Z_A->completion}
```

Status:

- specialised success subcase

## Case 10: Glass -> Crystal [Late-Gate Dominated]

```text
glass->crystal[late-gate-dominated]
= Zones{Z_A, (Z_B weak), (Z_C weak)}
= Dom{D1->blocked or weak D4}
= Route{R3, (R1 weak)}
= Obst{O2, (O1 weak)}
= Grade{G_C, (G_B/G_C edge)}
= Flow{Z_A->late failure, weak D4->Z_A, minimal Z_A->Z_B}
```

Status:

- specialised frontier subcase

Structural role:

- clean compatibility-side `O2 -> R3` benchmark
- isolates blocked real route logic

## Case 11: Glass -> Crystal [Mixed Frontier]

```text
glass->crystal[mixed_frontier]
= Zones{Z_A, Z_B}
= Dom{D4}
= Route{R3, R5, (R1 weak)}
= Obst{O2, O3, (O1 weak)}
= Grade{G_C, G_D, (G_B weak)}
= Flow{Z_A->Z_B, D4->Z_A, D4->Z_B}
```

Status:

- specialised frontier subcase

## Case 12: Crystal -> Air

```text
crystal->air
= Zones{Z_A, (Z_B weak), (Z_C weak)}
= Dom{D1}
= Route{R1, R4, (R3 secondary)}
= Obst{O1, O2, O4}
= Grade{G_A, G_B/G_C}
= Flow{Z_A->completion, Z_A->R4 in ordered return cases}
```

Status:

- anchor comparison case

## Case 13: Crystal -> Air [Ordered-Return Dominated]

```text
crystal->air[ordered-return-dominated]
= Zones{Z_A(return-biased), (Z_B weak), (Z_C weak)}
= Dom{D1(return-biased)}
= Route{R4, (R1 weak outward)}
= Obst{O4, (O2 weak)}
= Grade{G_A inward / G_D outward, (G_C weak outward edge)}
= Flow{return dominance, weak unrealised release-side alternative}
```

Status:

- specialised return-side comparison subcase

Structural role:

- clean `O4 -> R4` bridge outside polished metal
- strengthens return-side comparison cluster

## Updated Cluster Structure

## Cluster C1: Route-Dominant Anchors

Cases:

- `air -> glass`
- `glass -> crystal [selective_success]`
- `crystal -> air`

New status:

- stable

Change after expansion:

- `air -> rough glass` now sits near this cluster as a degraded bridge, but does not belong fully inside it.

## Cluster C2: Glass Frontier Cluster

Cases:

- `glass -> air`
- `glass -> air [pocket-dominant]`
- `glass -> air [diffuse-dominant]`
- `glass -> crystal`
- `glass -> crystal [late-gate dominated]`
- `glass -> crystal [mixed_frontier]`

New status:

- much stronger

Change after expansion:

- this cluster is now internally differentiated into:
  - release mixed
  - release pocket-dominant
  - release diffuse-dominant
  - compatibility selective
  - compatibility late-gate
  - compatibility mixed

This is the biggest gain from the expansion.

## Cluster C3: Return-Side Comparison Cluster

Cases:

- `air -> polished metal`
- `crystal -> air [ordered-return dominated]`
- `crystal -> air` partially

New status:

- stronger

Change after expansion:

- the cluster now has a clean second anchor outside polished metal
- directional route reality is now better represented

## Cluster C4: Degradation / Diffusion Cluster

Cases:

- `air -> oxidised metal`
- `glass -> air [diffuse-dominant]`
- `air -> rough glass`

New status:

- stronger and more nuanced

Change after expansion:

- now includes:
  - receiving-side glass degradation
  - release-side glass diffusion
  - metal-surface fragmentation/degradation

That makes the degradation family less one-dimensional.

## Updated Strategic Findings

## 1. The Expansion Was Worth Doing

The four additions all filled real structural gaps.

None appears redundant.

## 2. The Glass Frontier Cluster Is Now Much Better Resolved

This is the strongest result.

The programme no longer has only a general sense that glass is rich. It now has internal subfamilies:

- mixed release
- pocket release
- diffuse release
- selective compatibility
- late-gate compatibility
- mixed compatibility

## 3. Return-Side Logic Is Now Better Anchored

The ordered-return crystal subcase prevents polished metal from being the only clean `O4 / R4` benchmark.

That strengthens the whole framework.

## 4. Degradation Is Now Less Metal-Centric

Before expansion, oxidised metal carried too much of the degradation role.

Now:

- rough glass
- diffuse glass release

also carry degradation/diffusion logic.

That is healthier for the library.

## 5. The Library Should Pause Expansion Briefly

The expansion plan originally advised not expanding beyond these four additions until the new structure was reassessed.

That has now happened.

The next step should not be random expansion. It should be either:

- a revised cluster map
- a scoring pass over the expanded library
- or a move back toward element/material coverage using the stronger notation.

## Current Confidence

- confidence that the expanded library is structurally stronger than before: `9/10`
- confidence that the four additions were non-redundant: `9/10`
- confidence that the glass frontier cluster is now the strongest resolved cluster: `9/10`
- confidence that further expansion should pause for reassessment: `8/10`

## Recommendation

Pause broad case addition.

The best next work is one of:

1. `ams-expanded-library-scoreboard-v1.md`
2. `ams-expanded-cluster-map-v2.md`
3. `ams-element-material-coverage-plan-v1.md`

## Best Next Move

The best next artifact is:

- `ams-expanded-library-scoreboard-v1.md`

That should score the expanded cases by:

- anchor strength
- frontier value
- cluster contribution
- geometry maturity
- notation clarity

before the programme resumes broadening into more elements or material classes.*** End Patch
