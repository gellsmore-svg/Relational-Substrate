# AMS Mixed Modifier Subregion Model v1

## Purpose

This document models mixed sodium/magnesium silicate as an internally heterogeneous material field.

It follows:

- `ams-glass-modifier-material-property-table-v1.md`

The key prediction from the modifier-property comparison was that mixed Na/Mg systems are likely to be:

- `D4`-rich
- locally heterogeneous
- shaped by interacting sodium-rich, magnesium-rich, and silica-rich subregions

This document tests whether the mixed-interface framework can handle internal material heterogeneity, not only external optical interfaces.

## Core Claim

Mixed Na/Mg silicate should not be modelled as one averaged modifier condition.

The stronger AMS reading is:

- mixed modifier systems contain internal subregions with different route and obstruction logic

The major candidate subregions are:

- sodium-rich diffusing zones
- magnesium-rich selective / late-gate zones
- silica-rich route-preserving zones

These internal zones may interact like a material-internal analogue of the mixed interface framework.

## Active Modelling Layer

Primitive variables:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

For internal material modelling, `B_in` and `B_out` are less central than:

- `J_trans`
- `Q_coh`
- `D`
- route class
- obstruction class
- subregion dominance

Geometric descriptors:

- `L_depth`
- `L_span`
- `L_loop`
- `L_escape`

## Internal Subregion Types

## Subregion M1: Silica-Rich Route-Preserving Zone

### Dominant Logic

- route preservation
- network continuity
- relatively strong `R1/R2`

### Formal Profile

```text
M1_silica_rich
= Zones{Z_A}
= Dom{D1}
= Route{R1, R2}
= Obst{O1, (O5 weak)}
= Grade{G_A/G_B}
= Flow{Z_A->completion}
```

### Interpretation

This subregion preserves the strongest relation to pure silica glass.

It is not necessarily crystalline or perfectly ordered, but it remains the most route-reliable part of the mixed material.

## Subregion M2: Sodium-Rich Diffusing Zone

### Dominant Logic

- distributed weakening
- increased route broadening
- more diffusing obstruction

### Formal Profile

```text
M2_sodium_rich
= Zones{Z_C, (Z_A weak), (Z_B local)}
= Dom{D3 or D4}
= Route{R2, (R3), (R5 local)}
= Obst{O5, (O2), (O3 local)}
= Grade{G_C, (G_D local)}
= Flow{Z_A->Z_C, D4->Z_C, local Z_A->Z_B}
```

### Interpretation

This subregion is not simply “bad.” It may remain transmissive or dynamically permissive, but its route reality is weaker and more distributed.

It is the strongest internal analogue of diffuse-dominant glass behaviour.

## Subregion M3: Magnesium-Rich Selective / Late-Gate Zone

### Dominant Logic

- stronger local constraint
- selective route preservation
- late-gate failure under strain

### Formal Profile

```text
M3_magnesium_rich
= Zones{Z_A, (Z_B weak)}
= Dom{D1 or D4}
= Route{R1, R3}
= Obst{O1, O2}
= Grade{G_B/G_C}
= Flow{Z_A->completion, Z_A->late failure}
```

### Interpretation

This subregion differs sharply from sodium-rich zones.

It tends to preserve route structure more strongly, but it may fail later and more selectively.

## Subregion M4: Mixed-Modifier Competition Zone

### Dominant Logic

- local competition between sodium-style diffusion and magnesium-style constraint

### Formal Profile

```text
M4_mixed_modifier_competition
= Zones{Z_A, Z_B, Z_C}
= Dom{D4}
= Route{R1, R2, R3, (R5)}
= Obst{O1, O2, O5, (O3)}
= Grade{G_B/G_C, (G_D local)}
= Flow{Z_A->completion, Z_A->late failure, Z_A->Z_C, local Z_A->Z_B}
```

### Interpretation

This is the richest internal subregion and likely the most important one for mixed Na/Mg systems.

It is where the material behaves least like an averaged composition and most like an internally mixed field.

## Internal-Interface Interpretation

The major new step here is to treat boundaries between material subregions as internal interfaces.

The relevant transitions are not:

- air -> glass

but:

- silica-rich zone -> sodium-rich zone
- sodium-rich zone -> magnesium-rich zone
- magnesium-rich zone -> silica-rich zone

These internal transitions can reuse the same logic developed for external interfaces, but with different emphasis.

## Internal Transition 1: Silica-Rich -> Sodium-Rich

### Expected Transition

```text
M1->M2
= Flow{Z_A->Z_C, R1->R2, O1->O5}
```

### Interpretation

This transition weakens route dominance and shifts toward distributed continuation.

Likely effects:

- reduced route reality
- increased diffusion
- more local route broadening

## Internal Transition 2: Sodium-Rich -> Magnesium-Rich

### Expected Transition

```text
M2->M3
= Flow{Z_C->Z_A, R2->R1/R3, O5->O1/O2}
```

### Interpretation

This transition may reintroduce selective constraint after distributed weakening.

Likely effects:

- route narrowing
- possible late-gate failure
- local compatibility tension

This is a strong candidate for internal `D4` behaviour.

## Internal Transition 3: Magnesium-Rich -> Silica-Rich

### Expected Transition

```text
M3->M1
= Flow{R3->R1 if compatibility succeeds, O2->O1}
```

### Interpretation

This transition may recover stronger route-preserving network continuity if the magnesium-rich constraint aligns with silica-rich network structure.

Likely effects:

- route recovery
- selective completion
- reduced diffusion

## Internal Transition 4: Silica-Rich -> Mixed-Modifier Competition

### Expected Transition

```text
M1->M4
= Flow{D1->D4, R1->R1/R2/R3, O1->O1/O2/O5}
```

### Interpretation

This transition creates the richest internal mixed zone.

It is likely where material properties become most composition-sensitive.

## Whole-Material Profile

Mixed Na/Mg silicate can now be written as:

```text
mixed_na_mg_silicate_internal
= Subregions{M1,M2,M3,M4}
= Dom{D4 material field}
= Route{R1,R2,R3,(R5 local)}
= Obst{O1,O2,O5,(O3 local)}
= Grade{G_B/G_C,(G_D local)}
= Flow{M1->M2, M2->M3, M3->M1, M1->M4}
```

## Expected Property Consequences

## Optical Transmission

Likely:

- locally variable but not necessarily poor

Reason:

- M1 and M3 preserve route structure
- M2 and M4 weaken or complicate it

AMS prediction:

- transmission depends strongly on subregion continuity and whether M2/M4 zones break route coherence broadly.

## Durability

Likely:

- stronger than high-sodium systems
- less uniform than pure silica

Reason:

- magnesium-rich and silica-rich zones preserve constraint
- sodium-rich zones remain vulnerability points

## Viscosity / Processing

Likely:

- lower than pure silica
- not as simply diffusion-dominated as high-sodium systems

AMS prediction:

- viscosity behaviour should reflect competing route weakening and route constraint.

## Ionic Mobility

Likely:

- sodium mobility remains important
- but magnesium-rich and silica-rich zones may constrain pathways

AMS prediction:

- mobility may be strongly path-dependent and heterogeneous.

## Surface / Interface Behaviour

Likely:

- highly local
- composition-sensitive
- potentially `D4`-rich at surface and internal boundaries

AMS prediction:

- roughness, release, and entry behaviour will depend on which subregions dominate the terminal layer.

## Strongest Findings

## 1. Mixed Modifiers Are Best Modelled as Internal Subregion Fields

This is the main result.

Averaging sodium and magnesium into one modifier effect loses too much structure.

## 2. The Interface Framework Transfers to Internal Material Heterogeneity

This is a significant expansion.

The same zone/route/obstruction language can model:

- external optical interfaces
- internal subregion transitions

without adding new primitives.

## 3. Mixed Na/Mg Systems Are Strong D4 Candidates

This is reinforced.

The material is likely:

- mixed competitive internally

rather than simply route-dominant or diffusion-dominant.

## 4. Property Behaviour Should Be Locally Conditional

The model predicts that properties should depend on:

- which subregions dominate the path
- how continuous those subregions are
- whether sodium-rich zones connect into broader pathways
- whether magnesium-rich zones interrupt or stabilise those paths

## Score Judgment

No score movement yet.

Current confidence:

- mixed Na/Mg silicate: `6.5`

Post-study pressure:

- upward pressure, but not enough for `7` yet

Reason:

- internal subregion model is coherent, but not yet checked against direct material data or specific compositions.

## Current Weak Points

## 1. No Specific Composition Examples

The model still lacks:

- actual Na/Mg ratios
- specific glass systems
- property trends by composition

## 2. Internal Subregion Geometry Is Still Schematic

The model says what kinds of zones likely exist, but not:

- their size
- connectivity
- percolation behaviour
- persistence under processing

## 3. Mobility and Durability Need Direct Conventional Comparison

The next step should not be more abstract zone creation.

It should compare the subregion model against conventional mixed-modifier property behaviour.

## Confidence

- confidence that mixed Na/Mg systems should be modelled as internally heterogeneous: `8/10`
- confidence that the interface framework transfers usefully to internal material fields: `8/10`
- confidence that `D4` is the right dominant material-field diagnosis: `8/10`
- confidence that score should remain `6.5` until specific data comparison: `9/10`

## Recommendation

Keep the model.

Do not recalibrate yet.

Proceed to direct comparison against known mixed modifier / modifier-composition effects.

## Next Move

The best next artifact is:

- `ams-mixed-modifier-property-comparison-v1.md`

That should compare this internal subregion model against conventional mixed-modifier effects, especially:

- ion mobility
- durability
- viscosity
- glass transition / softening
- optical and surface behaviour where available.
