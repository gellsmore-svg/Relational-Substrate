# AMS First Specific Na/Mg Silicate Case v1

## Case Selection

This first specific case uses the balanced composition from a 2024 Na/Mg aluminosilicate glass and melt study.

The selected composition is:

```text
50 mol% SiO2
12.5 mol% Al2O3
18.75 mol% Na2O
18.75 mol% MgO

X_Na2O = Na2O / (Na2O + MgO) = 0.50
```

This is not a pure binary Na2O-MgO-SiO2 glass because it includes Al2O3. It is still the strongest available first case because it directly tests Na/Mg mixing in a silicate network and includes structural and rheological evidence relevant to the AMS model.

## Source-Backed Inputs

Primary source:

- Pannefieu, Le Losq, Florian, and Moretti, "Effect of the Na/Mg mixing on the structure and properties of aluminosilicate melts," Journal of Non-Crystalline Solids, 2024. DOI page: https://doi.org/10.1016/j.jnoncrysol.2024.123056

Relevant reported source facts:

- The studied system has `37.5 mol% Na2O + MgO`, `12.5 mol% Al2O3`, and `50 mol% SiO2`.
- The study varies `X_Na2O = Na2O / (Na2O + MgO)` across `0.00`, `0.25`, `0.50`, `0.75`, and `1.00`.
- The paper reports non-linear variations in density, molar volume, viscosity, and configurational entropy as Na substitutes Mg.
- Raman, `27Al` MAS NMR, and `23Na` MAS NMR data indicate structural changes rather than ideal random averaging.
- The authors report preferential role-sharing between Na and Mg as network modifier and charge compensator.

Supporting source:

- Lu et al., "Mechanical properties of mixed modified oxide glasses," Journal of Non-Crystalline Solids: X, 2022. Source page: https://www.sciencedirect.com/science/article/pii/S2590159122000450

Relevant support:

- Mixed modified oxide glass behavior depends on the local structural role and environment of modifier cations.
- Mixed modifier effects commonly affect properties through structure, not only through bulk composition.

## Template Entry

```text
case_id: na-mg-aluminosilicate-xna050-2024-pannefieu
composition_name: balanced sodium-magnesium aluminosilicate glass
composition_formula_or_mol_percent: 50 SiO2 - 12.5 Al2O3 - 18.75 Na2O - 18.75 MgO mol%

network_formers: SiO2 high, Al2O3 moderate as network former / charge-balanced former
network_modifiers: Na2O moderate-high, MgO moderate-high
intermediates: Al2O3 depends on charge compensation context
processing_context: melt-derived glass / melt viscosity series
thermal_history: synthesized glass; viscosity measured across high-temperature melt range

known_structure_data: Raman, 27Al MAS NMR, 23Na MAS NMR
known_property_data: density, molar volume, viscosity, configurational entropy
source_references: Pannefieu et al. 2024; Lu et al. 2022 review support
```

## AMS Subregion Estimate

```text
M1_silica_backbone: high / 7
M2_sodium_diffusing_regions: moderate-high / 6
M3_magnesium_selective_regions: moderate-high / 6
M4_mixed_modifier_competition_nodes: high / 8
```

### Rationale

`M1` remains high because the composition is still 50 mol% SiO2 with Al-bearing network structure.

`M2` is moderate-high because Na is present at the same molar oxide level as Mg and is expected to support more mobile, modifier-like route loosening.

`M3` is moderate-high because Mg is equally present and can impose stronger local field constraint, selective coordination behavior, and charge-related gate effects.

`M4` is high because the source reports non-linear property behavior and non-ideal structural role-sharing. That directly matches the AMS concept of mixed-modifier competition nodes.

## Connectivity Estimate

```text
M1_connectivity: connected
M2_connectivity: near-percolating
M3_interruption_strength: high
M4_junction_density: high
```

### Rationale

The balanced `X_Na2O = 0.50` composition is the most natural point for mixed competition.

AMS interpretation:

```text
Na-rich route loosening is strong enough to seek connectivity.
Mg-rich selective constraint is strong enough to interrupt it.
Na/Mg role-sharing creates high M4 junction density.
```

The source's non-linear viscosity and entropy behavior is more consistent with a competitive connectivity field than with a simple averaged modifier field.

## Connectivity Regime Selection

```text
primary_regime: Regime 5 frequent M4 junctions
secondary_regime: Regime 3 interrupted M2 pathways
```

### Why Regime 5

The source reports structural role-sharing and non-linear property response. In AMS terms, that is the signature of `M4` junction control.

```text
M4 high
=> local route handoff instability
=> mixed modifier behavior becomes non-linear
=> D4 dominance
```

### Why Regime 3

At balanced Na/Mg content, sodium-supported weak routes are likely strong enough to form near-connected pathways, but magnesium-supported selective constraint prevents simple sodium-dominant diffusion.

```text
M2 near-connected
+ M3 high interruption
=> R2 -> R3
=> O5 -> O2
=> D4
```

## Route and Obstruction Mapping

```text
primary_route: R2 -> R3
secondary_routes: R1, local R5
primary_obstruction: O5 -> O2
secondary_obstructions: O1, local O3
dominance_class: D4
route_grade: G_B/G_C
```

### Interpretation

The balanced mixed composition is not best read as sodium behavior diluted by magnesium or magnesium behavior diluted by sodium.

It is better read as a competitive route field:

```text
distributed weak route begins
selective gate interrupts
handoff node redirects or traps
whole field remains mixed competitive
```

This is exactly the situation where AMS should outperform a flat average-composition model.

## Property Predictions

### Ion Mobility

Prediction:

```text
moderate-high, non-linear, threshold-sensitive
```

AMS reasoning:

`M2` creates mobility pressure, but `M3` and `M4` prevent clean through-going sodium-dominant percolation.

Expected pattern:

```text
more mobile than Mg-rich endmember
less cleanly mobile than Na-rich endmember
non-linear near balanced composition
```

### Chemical Durability

Prediction:

```text
uneven, path-sensitive, not reducible to sodium content alone
```

AMS reasoning:

Durability weakness should follow connected or near-connected `M2` pathways, but those pathways are repeatedly interrupted by `M3` constraint and `M4` junction competition.

Expected pattern:

```text
local vulnerability along Na-rich weak paths
interrupted degradation where Mg/Al constraint dominates
mixed durability response
```

### Viscosity / Softening

Prediction:

```text
strong non-linear response
```

AMS reasoning:

The source directly reports non-linear viscosity behavior as Na substitutes Mg. AMS maps this to mixed route handoff:

```text
M2 lowers route resistance
M3 gates route completion
M4 increases competitive reseating
=> viscosity is not a linear weighted sum
```

This is the strongest property anchor for this case.

### Optical / Surface Behavior

Prediction:

```text
cautious; likely secondary unless subregion contrast reaches optical or surface-relevant scale
```

AMS reasoning:

The source case is strongest for melt/glass structure and rheology, not optical interface behavior. Optical claims should remain secondary until surface, refractive, scattering, or interface measurements are introduced.

### Interface Release

Prediction:

```text
mixed release, local late-gate and pocketing risk
```

AMS reasoning:

If an interface intersects a high-`M4` region, route handoff may be unstable. If it intersects connected `M1`, release should be cleaner. If it intersects near-connected `M2`, release should be more diffuse.

Expected local alternatives:

```text
M1 surface => R1/O1
M2 surface => R2/O5
M3 surface => R3/O2
M4 surface => local R5/O3
```

## Composition Score

```text
composition_score: 7.5
score_confidence: moderate
score_pressure_on_family: upward
```

### Reason

This composition gives the AMS mixed-modifier model a real test case with direct evidence of non-linear property behavior and non-ideal structural role-sharing.

It strengthens the family-level score because:

- the composition sits at the strongest mixed-competition point, `X_Na2O = 0.50`
- the reported behavior is non-linear rather than averaged
- structural data support role-sharing rather than random mixing
- viscosity, entropy, Raman, and NMR evidence all point toward internal organisation

The score is not higher than 7.5 because:

- the case is aluminosilicate, not a pure Na/Mg silicate
- the AMS subregion proportions are inferred, not directly imaged
- ion mobility and durability are inferred from mixed-modifier logic, not fully measured in this specific case
- interface release is not directly tested

## Family Score Implication

Previous family score:

```text
mixed Na/Mg silicate: 7/10
```

Updated pressure:

```text
7/10 retained, upward pressure strengthened
```

Do not move the family score to 7.5 yet.

Reason:

This is a strong first composition case, but it is one balanced aluminosilicate series. The family score should move only after additional compositions show the same AMS route logic across different Na/Mg ratios or in a less aluminous system.

## Next Required Evidence

The next cases should test the balanced case against asymmetric compositions from the same series.

Recommended sequence:

```text
X_Na2O = 0.25
X_Na2O = 0.75
X_Na2O = 0.00
X_Na2O = 1.00
```

Purpose:

```text
X = 0.25 tests Mg-dominant interruption.
X = 0.75 tests Na-dominant near-percolation.
X = 0.00 and X = 1.00 define endmember route baselines.
```

The next artifact should be:

```text
ams-na-mg-aluminosilicate-series-map-v1.md
```

That file should map all five `X_Na2O` compositions into route, obstruction, dominance, connectivity, and expected property curves.
