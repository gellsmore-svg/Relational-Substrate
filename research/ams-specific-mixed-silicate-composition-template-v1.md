# AMS Specific Mixed Silicate Composition Template v1

## Purpose

This template defines how to map a named mixed silicate composition into the AMS mixed-modifier model.

It is designed for Na/Mg silicate cases first, but the structure can later be extended to other mixed modifier systems.

The goal is to move from family-level claims such as:

```text
mixed Na/Mg silicate: 7/10
```

to composition-specific entries with explicit route, obstruction, dominance, property, and score-pressure judgments.

## Required Inputs

Each composition case should begin with the following inputs.

```text
case_id:
composition_name:
composition_formula_or_mol_percent:
network_formers:
network_modifiers:
intermediates:
processing_context:
thermal_history:
known_structure_data:
known_property_data:
source_references:
```

## Composition Categories

### Network Formers

Network formers are species that build the primary glass-forming relational backbone.

For the current silicate model:

```text
SiO2 => primary former
```

Possible extensions:

```text
B2O3
P2O5
Al2O3 in charge-balanced contexts
```

AMS default mapping:

```text
network former dominance
=> M1 pressure
=> R1/O1/D1 pressure
```

### Network Modifiers

Network modifiers disrupt, depolymerise, or reconfigure the network.

For the current Na/Mg silicate model:

```text
Na2O => M2 pressure
MgO => M3 pressure
```

AMS default mapping:

```text
Na-rich modification
=> distributed weak routes
=> R2/O5/D3 pressure

Mg-rich modification
=> selective local constraint
=> R1/R3 and O1/O2 pressure
```

### Mixed Modifier Competition

Mixed modifier competition occurs where two modifier behaviors interfere rather than average.

AMS default mapping:

```text
Na/Mg competition
=> M4 pressure
=> D4
=> local R5/O3 possibility
```

## Subregion Estimate

Each case should estimate the relative presence of `M1`, `M2`, `M3`, and `M4`.

Use a qualitative or numeric scale.

Qualitative:

```text
absent / low / moderate / high / dominant
```

Numeric:

```text
0-10 relative intensity
```

Template:

```text
M1_silica_backbone:
M2_sodium_diffusing_regions:
M3_magnesium_selective_regions:
M4_mixed_modifier_competition_nodes:
```

Example format:

```text
M1_silica_backbone: high / 8
M2_sodium_diffusing_regions: moderate / 5
M3_magnesium_selective_regions: moderate / 5
M4_mixed_modifier_competition_nodes: high / 7
```

## Connectivity Estimate

The subregions must then be classified by connectivity.

### `M1` Connectivity

```text
M1_connectivity:
isolated / partial / connected / dominant
```

Interpretation:

```text
connected M1
=> retained backbone
=> D1/D4 pressure
```

### `M2` Connectivity

```text
M2_connectivity:
isolated / clustered / near-percolating / connected / dominant
```

Interpretation:

```text
isolated M2
=> local D3 pockets only

near-percolating M2
=> D4 pressure

connected M2
=> D3 pressure
```

### `M3` Interruption

```text
M3_interruption_strength:
low / moderate / high / dominant
```

Interpretation:

```text
high M3 interruption
=> R2 routes often terminate as R3
=> O5 becomes O2
=> D4 pressure
```

### `M4` Junction Density

```text
M4_junction_density:
low / moderate / high / dominant
```

Interpretation:

```text
high M4 density
=> non-linear mixed modifier behavior
=> local R5/O3
=> D4 pressure
```

## Connectivity Regime Selection

Select one primary regime and one optional secondary regime.

```text
primary_regime:
secondary_regime:
```

Allowed regimes:

```text
Regime 1: isolated M2 islands
Regime 2: connected M2 pathways
Regime 3: interrupted M2 pathways
Regime 4: connected M1/M3 backbone
Regime 5: frequent M4 junctions
Regime 6: fragmented high-disorder field
```

Guidance:

```text
M2 isolated + M1 connected
=> Regime 1 or 4

M2 connected
=> Regime 2

M2 near-connected but cut by M3
=> Regime 3

M1/M3 connected and dominant
=> Regime 4

M4 high
=> Regime 5

M1 broken + M2 abundant + disorder high
=> Regime 6
```

## Route and Obstruction Mapping

Each composition should map into route and obstruction classes.

Template:

```text
primary_route:
secondary_routes:
primary_obstruction:
secondary_obstructions:
dominance_class:
route_grade:
```

Allowed route classes:

```text
R1 narrow viable route
R2 distributed weak routes
R3 blocked apparent route
R4 inward-biased route
R5 loop-dominated pseudo-route
R6 fragmenting route field
```

Allowed obstruction classes:

```text
O1 funnelling
O2 late-gate
O3 pocketing
O4 biasing
O5 diffusing
O6 fragmenting
```

Allowed dominance classes:

```text
D1 route-dominant
D2 pocket-dominant
D3 diffusion-dominant
D4 mixed competitive
```

Allowed route grades:

```text
G_A strongly real route
G_B weak but real route
G_C apparent but unreliable route
G_D pseudo-route
```

## Property Prediction Fields

Each composition case should predict directional behavior for key property classes.

Template:

```text
ion_mobility_prediction:
chemical_durability_prediction:
viscosity_softening_prediction:
optical_surface_prediction:
interface_release_prediction:
```

Use directional language:

```text
low / moderate / high
increased / reduced / non-linear / uneven / threshold-sensitive
```

## Score Fields

Each composition receives both a local score and pressure on the family score.

Template:

```text
composition_score:
score_confidence:
score_pressure_on_family:
reason:
```

Score confidence:

```text
low / moderate / high
```

Score pressure:

```text
downward / neutral / upward
```

Interpretation:

```text
composition_score < 6
=> weak case; may reduce family confidence if repeated

composition_score 6-7
=> useful case; supports family-level 7 if repeated

composition_score 8+
=> strong case; requires detailed structural/property match
```

## Full Case Template

```text
case_id:
composition_name:
composition_formula_or_mol_percent:

network_formers:
network_modifiers:
intermediates:
processing_context:
thermal_history:

known_structure_data:
known_property_data:
source_references:

M1_silica_backbone:
M2_sodium_diffusing_regions:
M3_magnesium_selective_regions:
M4_mixed_modifier_competition_nodes:

M1_connectivity:
M2_connectivity:
M3_interruption_strength:
M4_junction_density:

primary_regime:
secondary_regime:

primary_route:
secondary_routes:
primary_obstruction:
secondary_obstructions:
dominance_class:
route_grade:

ion_mobility_prediction:
chemical_durability_prediction:
viscosity_softening_prediction:
optical_surface_prediction:
interface_release_prediction:

composition_score:
score_confidence:
score_pressure_on_family:
reason:
next_required_evidence:
```

## Worked Example: Generic Balanced Na/Mg Silicate

This is a placeholder example, not a final scored real composition.

```text
case_id: mixed-na-mg-silicate-generic-balanced
composition_name: generic balanced sodium-magnesium silicate
composition_formula_or_mol_percent: unspecified Na2O-MgO-SiO2 glass

network_formers: SiO2 high
network_modifiers: Na2O moderate, MgO moderate
intermediates: none specified
processing_context: unspecified melt-derived glass
thermal_history: unspecified

known_structure_data: not composition-specific
known_property_data: family-level mixed modifier behavior only
source_references: mixed modifier literature used in prior corpus notes

M1_silica_backbone: high / 8
M2_sodium_diffusing_regions: moderate / 5
M3_magnesium_selective_regions: moderate / 5
M4_mixed_modifier_competition_nodes: high / 7

M1_connectivity: connected
M2_connectivity: near-percolating
M3_interruption_strength: moderate-high
M4_junction_density: high

primary_regime: Regime 5 frequent M4 junctions
secondary_regime: Regime 3 interrupted M2 pathways

primary_route: R2 -> R3
secondary_routes: R1, local R5
primary_obstruction: O5 -> O2
secondary_obstructions: O1, local O3
dominance_class: D4
route_grade: G_B/G_C

ion_mobility_prediction: moderate and non-linear; threshold-sensitive
chemical_durability_prediction: uneven; weaker along sodium-rich near-connected paths
viscosity_softening_prediction: non-linear due to mixed modifier competition
optical_surface_prediction: cautious; depends on subregion scale and surface exposure
interface_release_prediction: mixed route release with local pocketing risk

composition_score: 7
score_confidence: moderate-low
score_pressure_on_family: neutral-to-upward
reason: matches current family-level mixed Na/Mg silicate score but lacks composition-specific structural evidence.
next_required_evidence: named composition with mobility, durability, viscosity, and structural data.
```

## Next Artifact

The next useful artifact should be:

```text
ams-first-specific-na-mg-silicate-case-v1.md
```

That artifact should select one real Na/Mg silicate composition from the literature and fill this template with actual composition and property data.
