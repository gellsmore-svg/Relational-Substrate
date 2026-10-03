# AMS Glass Modifier Composition Gradient v1

## Purpose

This document extends:

- `ams-glass-modifier-case-study-v1.md`

by modelling glass modifiers across composition gradients rather than treating modified glass as one undifferentiated case.

The focus is:

- pure silica
- low sodium modification
- high sodium modification
- magnesium-rich silicate
- mixed sodium/magnesium modifier systems

The goal is to track how route classes, obstruction character, and dominance modes shift as modifier role and concentration change.

## Core Claim

Glass modification should be treated as a gradient of network transformation, not a binary state.

In AMS terms, different modifiers alter:

- route viability
- route distribution
- obstruction character
- release fragility
- entry permissiveness
- local constraint

in different ways.

Sodium and magnesium are not interchangeable modifiers.

## Baseline Variables and Classes

Relevant route classes:

- `R1` narrow viable route
- `R2` distributed weak routes
- `R3` blocked apparent route
- `R5` loop-dominated pseudo-route

Relevant obstruction classes:

- `O1` funnelling
- `O2` late-gate
- `O3` pocketing
- `O5` diffusing

Relevant dominance modes:

- `D1` route-dominant
- `D3` diffusion-dominant
- `D4` mixed competitive

## Gradient Case 1: Pure Silica Glass

## Formal Profile

```text
pure_silica_glass
= Zones{Z_A, Z_C}
= Dom{D1/D3 depending surface}
= Route{R1, R2}
= Obst{O1, O5}
= Grade{G_A/G_B/G_C}
= Flow{Z_A->completion, Z_A->Z_C under rough/degraded conditions}
```

## AMS Reading

Pure silica glass retains strong network identity despite non-periodic order.

The key balance is:

- real distributed network continuity
- enough route viability for transmission
- enough disorder to make release and surface conditions important

## Dominant Tendencies

- `R1`: medium/high
- `R2`: medium/high
- `O1`: medium
- `O5`: medium under degraded surfaces
- `D1`: possible in cleaner transmissive paths
- `D3`: possible in rough/diffuse surfaces

## Current Confidence

- `8`

## Gradient Case 2: Low Sodium Modification

## Formal Profile

```text
low_sodium_silicate_glass
= Zones{Z_A med, Z_C, (Z_B local weak)}
= Dom{D1/D3, local D4}
= Route{R1 weakened, R2 stronger, (R3 weak)}
= Obst{O5 stronger, (O1 weak), (O2 weak)}
= Grade{G_B/G_C}
= Flow{Z_A->completion weakly, Z_A->Z_C, local D4->Z_C}
```

## AMS Reading

Low sodium modification weakens the purity of the silica network without fully changing the glass into a diffuse-dominant case.

Expected shifts:

- `R1` weakens but remains meaningful
- `R2` strengthens
- `O5` strengthens
- route dominance becomes more conditional

## Entry Behaviour

Entry may become slightly more permissive but less cleanly route-dominant.

Expected:

- weaker `B_in` selectivity
- stronger distributed continuation

## Release Behaviour

Release becomes more sensitive to terminal-layer diffusion.

Expected:

- increased `Z_A -> Z_C`
- stronger `D3` tendency in rougher conditions

## Current Confidence

- `7`

## Gradient Case 3: High Sodium Modification

## Formal Profile

```text
high_sodium_silicate_glass
= Zones{Z_C, Z_A weak, (Z_B local)}
= Dom{D3 or D4}
= Route{R2, R3, (R5 local)}
= Obst{O5, O2, (O3 local)}
= Grade{G_C, (G_D local)}
= Flow{Z_A->Z_C, D4->Z_C, local Z_A->Z_B}
```

## AMS Reading

High sodium modification pushes the network further toward distributed weakening and local incompatibility.

Expected shifts:

- `R1` becomes weak
- `R2` dominates
- `R3` appears where modified routes look viable but fail
- `O5` becomes central
- `O2` appears more often
- local `O3/R5` becomes more plausible

## Entry Behaviour

Entry may remain broadly permissive but less coherent.

Expected:

- more broad admission
- less stable route reality
- more apparent routes

## Release Behaviour

Release becomes substantially more fragile.

Expected:

- stronger diffuse-dominant release
- more trapped/pocketed local failures where modifiers cluster

## Current Confidence

- `6.5/10`

Reason:

- plausible gradient extension, but needs composition-specific comparison.

## Gradient Case 4: Magnesium-Rich Silicate

## Formal Profile

```text
magnesium_rich_silicate
= Zones{Z_A, (Z_B local), (Z_C)}
= Dom{D1 or D4}
= Route{R1, R3, (R2)}
= Obst{O1, O2, (O5)}
= Grade{G_B/G_C}
= Flow{Z_A->completion in structured regions, Z_A->late failure in strained regions}
```

## AMS Reading

Magnesium-rich silicate is not simply “less modified” than sodium silicate. It has a different modifier character.

Expected shifts:

- stronger local constraint
- stronger route selectivity
- less broad diffusion than sodium-rich systems
- more late-gate failure where structured routes strain

## Entry Behaviour

Entry is likely more selective.

Expected:

- stronger `O1`
- more `R1`
- possible `R3` in local strained paths

## Release Behaviour

Release may fail by route blockage rather than diffuse broadening.

Expected:

- more `O2`
- less central `O5`

## Current Confidence

- `7`

## Gradient Case 5: Mixed Sodium/Magnesium Modifier System

## Formal Profile

```text
mixed_na_mg_silicate
= Zones{Z_A, Z_B, Z_C}
= Dom{D4}
= Route{R1, R2, R3, (R5 local)}
= Obst{O1, O2, O5, (O3 local)}
= Grade{G_B/G_C, (G_D local)}
= Flow{Z_A->completion, Z_A->late failure, Z_A->Z_C, local Z_A->Z_B}
```

## AMS Reading

Mixed sodium/magnesium systems are likely the richest modifier cases.

Why:

- sodium contributes distributed weakening and diffusion
- magnesium contributes local constraint and selectivity
- their mixture can create heterogeneous subregions

This makes mixed systems likely to produce:

- route-dominant local regions
- diffusing regions
- late-gate failures
- local pseudo-route pockets

## Entry Behaviour

Entry may be locally variable:

- permissive in sodium-rich regions
- selective in magnesium-rich regions
- mixed competitive where modifier distribution is heterogeneous

## Release Behaviour

Release may be highly surface- and composition-sensitive.

Expected:

- `D4`
- local `D1`
- local `D3`
- possible `D2` if modifier distribution creates pocketing zones

## Current Confidence

- `6.5/10`

Reason:

- structurally plausible but requires specific composition/material comparisons.

## Gradient Summary Table

| Composition case | Dominant route shift | Dominant obstruction shift | Dominance mode | Current confidence |
|---|---|---|---|---:|
| pure silica glass | `R1 + R2` | `O1 + O5` | `D1/D3` | 8 |
| low sodium silicate | weakened `R1`, stronger `R2` | stronger `O5` | `D1/D3`, local `D4` | 7 |
| high sodium silicate | `R2`, `R3`, local `R5` | `O5`, `O2`, local `O3` | `D3/D4` | 6.5 |
| magnesium-rich silicate | `R1`, `R3`, less `R2` | `O1`, `O2`, less `O5` | `D1/D4` | 7 |
| mixed Na/Mg silicate | `R1 + R2 + R3`, local `R5` | `O1 + O2 + O5`, local `O3` | `D4` | 6.5 |

## Strongest Findings

## 1. Modifier Concentration Should Shift Route Reality

As sodium modification rises:

- route reality becomes more distributed and weaker
- `R2` and `O5` grow in importance
- clean `R1` dominance weakens

## 2. Magnesium Does Not Follow the Sodium Pattern

Magnesium-rich cases lean toward:

- selective route preservation
- late-gate failure
- stronger local constraint

rather than pure diffusion.

## 3. Mixed Modifier Systems Are Likely D4-Rich

This is the strongest new result.

Mixed Na/Mg systems are likely to produce local heterogeneity:

- route-dominant subregions
- diffusing subregions
- late-gate subregions
- possibly pocketing subregions

That makes them strong candidates for applying the full mixed-interface diagnostic framework.

## 4. Composition Gradients Strengthen the Interface Framework

The framework is now useful not only for external interfaces, but for internal material variation.

That is a major expansion of scope.

## Score Judgment

No score changes yet.

Current recommended holds:

- pure silica glass: `8`
- low sodium silicate: `7`
- high sodium silicate: `6.5`
- magnesium-rich silicate: `7`
- mixed Na/Mg silicate: `6.5`

Reason:

- the gradient model is structurally useful but needs conventional material comparison before recalibration.

## Current Weak Points

## 1. Conventional Material Properties Not Yet Tabulated

The gradient needs comparison against:

- optical behaviour
- durability
- viscosity
- melting behaviour
- ionic mobility
- surface roughness

## 2. Sodium/Magnesium Composition Ranges Are Not Yet Anchored

The model currently uses qualitative low/high categories.

That is acceptable for this stage, but later work should anchor them better.

## 3. Internal Interface vs External Interface Needs More Distinction

Mixed modifier systems suggest internal subregion interfaces, not only surface interfaces.

That should become a later modelling track.

## Confidence

- confidence that composition gradients matter: `9/10`
- confidence that sodium and magnesium diverge in the right direction: `8/10`
- confidence that mixed Na/Mg systems are likely D4-rich: `7/10`
- confidence that scores should hold pending material comparison: `9/10`

## Recommendation

Keep scores unchanged.

Proceed to conventional material comparison before any recalibration.

## Next Move

The best next artifact is:

- `ams-glass-modifier-material-property-table-v1.md`

That should compare the gradient model against conventional property categories:

- optical transmission
- durability
- viscosity / melting behaviour
- ionic mobility
- surface/interface behaviour

and identify where the AMS gradient model fits well or needs revision.*** End Patch
