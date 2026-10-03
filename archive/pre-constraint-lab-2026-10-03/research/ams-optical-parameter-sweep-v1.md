# AMS Optical Parameter Sweep v1

## Purpose

This document is the first structured parameter sweep for the AMS optical modelling programme.

The earlier work established:

- model families
- optical benchmarks
- experiment logs
- first geometry cases
- a shared variable sketch

The next step is to vary the key optical variables in a disciplined way and see:

- which variables actually discriminate the benchmark cases
- which variables appear secondary
- which variables are still too vague to be useful

This is not full mathematics. It is a structured low / medium / high sweep.

## Variables In Scope

This first sweep focuses on the variables that now look most important for optical behaviour:

- `R` = return-path strength
- `S` = slip tolerance
- `B` = boundary sensitivity
- `D` = defect sensitivity
- `J` = coupling strength
- `Q` = resonance compatibility

Other variables such as `T`, `C`, `K`, and `M` are not ignored, but they are not the first discriminators for the current optical cases.

## Sweep Logic

Each variable is treated at three levels:

- `Low`
- `Medium`
- `High`

The aim is not to assign exact numbers yet. The aim is to track directional behaviour.

## Case Set

The sweep is run against six geometry cases:

- `G1` Regular Nested Transmissive Order
- `G2` Distributed Permissive Transmissive Order
- `G3` Collective Reflective Boundary Order
- `G4` Defect-Disrupted Pathway Order
- `G5` Boundary Entry Transition Order
- `G6` Surface-Degraded Reflective Order

## Variable Sweep 1: Return-Path Strength (`R`)

### Low `R`

Expected effects:

- weak coherent propagation
- poor reseating
- tendency toward diffusion, collapse, or incoherent transition

Most affected cases:

- `G1`
- `G2`
- `G4`

Interpretive note:

Low `R` appears hostile to transmission in both crystal and glass cases.

### Medium `R`

Expected effects:

- partial propagation support
- greater sensitivity to defect and boundary conditions
- transmissive behaviour possible but more fragile

Most affected cases:

- `G2`
- `G4`
- `G5`

Interpretive note:

Medium `R` may be enough for glass-like transmission if pathway permissibility remains adequate.

### High `R`

Expected effects:

- strong propagation continuity
- robust reseating
- greater resistance to minor local disruption

Most affected cases:

- `G1`
- `G2`

Interpretive note:

High `R` currently looks like a necessary condition for strong transmission, but not a sufficient one by itself.

## Variable Sweep 2: Slip Tolerance (`S`)

### Low `S`

Expected effects:

- brittle pathway behaviour
- strong sensitivity to mismatch
- higher risk of disruption at local irregularities

Most affected cases:

- `G2`
- `G4`
- `G5`

Interpretive note:

Low `S` appears much less compatible with disordered transmissive media than with ordered crystalline propagation.

### Medium `S`

Expected effects:

- useful balance between order and adaptability
- stronger transmission through mildly irregular regions

Most affected cases:

- `G1`
- `G2`
- `G5`

Interpretive note:

Medium `S` may be the best current guess for crystal-like transmission with manageable irregularity.

### High `S`

Expected effects:

- more flexible local reseating
- better tolerance of disorder
- possible reduction in sharp collective boundary response if too high

Most affected cases:

- `G2`
- `G4`

Interpretive note:

High `S` currently looks helpful for glass-like transmission, but potentially less helpful for strong metal-like reflection.

## Variable Sweep 3: Boundary Sensitivity (`B`)

### Low `B`

Expected effects:

- weak interface significance
- behaviour dominated by bulk rather than surface transition

Most affected cases:

- `G1`
- `G2`

Interpretive note:

Low `B` is likely incompatible with strong reflection models.

### Medium `B`

Expected effects:

- meaningful interface shaping
- transmissive entry and exit effects without boundary domination

Most affected cases:

- `G2`
- `G5`

Interpretive note:

Medium `B` currently looks plausible for transmissive media where boundary matters but does not fully dominate.

### High `B`

Expected effects:

- strong interface-controlled behaviour
- surface coherence becomes decisive

Most affected cases:

- `G3`
- `G5`
- `G6`

Interpretive note:

High `B` currently looks necessary for metal reflection and reflective degradation cases.

## Variable Sweep 4: Defect Sensitivity (`D`)

### Low `D`

Expected effects:

- defects remain local
- transmission or reflection quality remains comparatively robust

Most affected cases:

- `G1`
- `G3`

Interpretive note:

Low `D` fits idealised or very high-quality media better than real defect-rich materials.

### Medium `D`

Expected effects:

- noticeable but not catastrophic effect of defects
- local degradation of optical quality

Most affected cases:

- `G2`
- `G4`
- `G6`

Interpretive note:

Medium `D` may be the most realistic default assumption for many real materials.

### High `D`

Expected effects:

- strong scattering or degraded reflection quality
- defect-driven redirection or loss of coherence

Most affected cases:

- `G4`
- `G6`

Interpretive note:

High `D` currently appears central to scattering models and degraded metallic surfaces.

## Variable Sweep 5: Coupling Strength (`J`)

### Low `J`

Expected effects:

- weak collective behaviour
- higher difficulty sustaining whole-level response

Most affected cases:

- `G3`
- `G6`

Interpretive note:

Low `J` is likely incompatible with strong collective metal reflection.

### Medium `J`

Expected effects:

- moderate whole coherence
- useful for some transmissive and weakly collective cases

Most affected cases:

- `G2`
- `G5`

Interpretive note:

Medium `J` may work for distributed transmissive wholes where propagation is collective enough to persist but not strongly surface-locked.

### High `J`

Expected effects:

- strong collective response
- stronger whole-level coherence
- more robust nested or surface-coherent behaviour

Most affected cases:

- `G1`
- `G3`
- `G6`

Interpretive note:

High `J` currently looks central for crystal transmission and metal reflection, but with different whole-level expressions.

## Variable Sweep 6: Resonance Compatibility (`Q`)

### Low `Q`

Expected effects:

- weak dynamic coherence
- lower tendency toward coordinated response

Most affected cases:

- `G3`
- `G2`

Interpretive note:

Low `Q` may still permit transmission, but probably weakens collective surface reflection.

### Medium `Q`

Expected effects:

- useful dynamic support without strong collective amplification

Most affected cases:

- `G1`
- `G2`
- `G5`

Interpretive note:

Medium `Q` may fit many transmissive cases better than reflective ones.

### High `Q`

Expected effects:

- stronger collective dynamic response
- more coherent surface-level reaction to incoming disturbance
- greater risk of instability if not supported by other variables

Most affected cases:

- `G3`
- `G6`

Interpretive note:

High `Q` currently looks especially important in reflection cases rather than bulk transmission cases.

## Cross-Variable Provisional Profiles

### Crystal Transmission

Most plausible current profile:

- high `R`
- medium `S`
- medium `B`
- low bulk `D`
- high `J`
- medium `Q`

Interpretive summary:

- strong nested whole-order with regular pathways and robust propagation support

### Glass Transmission

Most plausible current profile:

- medium to high `R`
- medium to high `S`
- medium `B`
- medium to high `D`
- medium `J`
- medium `Q`

Interpretive summary:

- disordered but still permissive whole, with defect sensitivity playing a much larger role than in the crystal case

### Metal Reflection

Most plausible current profile:

- medium `R`
- low to medium `S`
- very high `B`
- medium to high `D`
- high `J`
- high `Q`

Interpretive summary:

- collective, highly boundary-sensitive whole response rather than pathway-dominated transmission

### Defect-Sensitive Scattering

Most plausible current profile:

- medium `R`
- medium `S`
- medium `B`
- very high `D`
- medium `J`
- low to medium `Q`

Interpretive summary:

- propagation still exists, but defect-driven local disruption redirects or degrades it

## Main Discriminators Emerging

The first sweep suggests that the most discriminating optical variables are:

1. `B`
2. `D`
3. `J`
4. `R`

Secondary but still important:

5. `S`
6. `Q`

This is useful because it gives the next modelling round a more focused target.

## Variables Still Too Vague

The current sweep also shows where the model remains under-specified:

- exact geometric meaning of `R` at whole scale
- how `Q` differs from `J` in some boundary cases
- how `S` should be defined at surfaces versus in bulk
- how `B` should be decomposed into:
  - entry sensitivity
  - exit sensitivity
  - reflective response sensitivity

These should be the next refinement targets.

## Immediate Conclusions

### 1. Reflection and transmission already separate cleanly

Transmission currently depends more on:

- `R`
- `S`
- admissible bulk pathway continuity

Reflection currently depends more on:

- `B`
- `J`
- `Q`
- surface coherence

This is one of the strongest early results in the optical programme.

### 2. Defect sensitivity is central across the whole optical field

`D` now looks less like a modifier and more like a central cross-cutting variable for real materials.

### 3. The current model is good enough to guide remodelling

The sweep does not settle the optics. But it is now structured enough to tell us where the weak points are.

That is real progress.

## Recommended Next Move

The next correct artifact should be:

- `ams-boundary-response-subvariables-v1.md`

That document should refine:

- `B`
- `J`
- `Q`

especially for metal reflection, transmissive entry/exit, and degraded boundary behaviour.
