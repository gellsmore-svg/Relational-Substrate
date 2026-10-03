# AMS Na/Mg Series Prediction vs Observation Table v1

## Purpose

This table separates three layers for the Na/Mg aluminosilicate series:

- directly observed or reported source behavior
- AMS interpretation of that behavior
- untested AMS predictions

This prevents the model from treating inferred route behavior as if it had already been directly measured.

## Source Series

Primary source:

- Pannefieu, Le Losq, Florian, and Moretti, "Effect of the Na/Mg mixing on the structure and properties of aluminosilicate melts," Journal of Non-Crystalline Solids, 2024. DOI page: https://doi.org/10.1016/j.jnoncrysol.2024.123056

Series:

```text
50 mol% SiO2
12.5 mol% Al2O3
37.5 mol% total Na2O + MgO

X_Na2O = 0.00, 0.25, 0.50, 0.75, 1.00
```

## Evidence Classification

```text
Observed:
reported directly in the source or plainly derived from the stated composition.

AMS interpreted:
not directly reported as AMS language, but mapped from observed source behavior into route, obstruction, dominance, and subregion categories.

Untested prediction:
not directly measured in the source; proposed as a future test.
```

## High-Level Evidence Table

| Property / feature | Source status | Source behavior | AMS interpretation | Evidence strength |
|---|---|---|---|---|
| composition path | observed | controlled Na/Mg substitution at fixed SiO2 and Al2O3 | valid series for route-transition mapping | strong |
| density | observed | decreases from Mg endmember to Na endmember | composition and packing field shift | moderate |
| molar volume | observed | varies across Na/Mg substitution | relational packing changes across series | moderate |
| viscosity | observed | changes substantially and non-linearly as Na replaces Mg | route availability and route completion are not linear | strong |
| configurational entropy | observed | deviates from ideal mixing | internal ordering / non-random route grammar | strong |
| Raman data | observed | structural changes across series | network subregion balance changes | moderate-strong |
| `27Al` MAS NMR | observed | Al coordination shifts toward Al[IV] as Na increases | charge-compensation / network role-sharing shifts | strong |
| `23Na` MAS NMR | observed | Na environment changes across series | Na route role changes with Mg competition | strong |
| Na/Mg role-sharing | observed / source interpretation | cations have preferential modifier and charge-compensator roles | `M4` mixed-competition nodes | strong |
| ion mobility | untested in source | not directly measured in this source | predicted to follow `M2` connectivity | pending |
| chemical durability | untested in source | not directly measured in this source | predicted to follow connected weak paths | pending |
| optical/interface behavior | untested in source | not directly measured in this source | predicted to depend on surface-exposed subregions | weak-pending |

## Composition-Level Table

| `X_Na2O` | Observed source basis | AMS interpretation | Untested prediction | Score pressure |
|---:|---|---|---|---|
| 0.00 | Mg endmember composition; high Mg, no Na | `M3` dominant, `R1/R3`, `O1/O2`, `D1` | lower ion mobility, stronger gate-controlled durability | baseline |
| 0.25 | Mg-dominant mixed composition | local `M2` appears inside strong `M3` interruption field | early non-linear mobility pockets; local weak paths cut by gates | upward if non-linearity appears early |
| 0.50 | balanced Na/Mg composition; strongest mixed point | high `M4`, `R2 -> R3`, `O5 -> O2`, `D4` | maximum non-linear mixed competition; uneven durability | strongest upward pressure |
| 0.75 | Na-dominant mixed composition | `M2` near-connected, `M3` still interrupts | transition toward `D3`; mobility threshold likely | upward if threshold behavior is observed |
| 1.00 | Na endmember composition; high Na, no Mg | `M2` dominant, `R2`, `O5`, `D3` | connected sodium mobility field; broader weak-path durability | baseline |

## Observed Behavior to AMS Mapping

### Non-Linear Viscosity

Observed:

```text
Viscosity changes substantially and non-linearly as Na substitutes Mg.
```

AMS interpretation:

```text
Na-supported route loosening does not simply add to Mg-supported constraint.
Instead, routes open, terminate, redirect, or compete depending on local role-sharing.
```

Mapping:

```text
viscosity non-linearity
=> route/connectivity non-linearity
=> M2/M3/M4 competition
=> D4 strongest near mixed compositions
```

Evidence strength:

```text
strong
```

Reason:

The source directly reports non-linear rheological behavior and structural role changes.

### Configurational Entropy Deviation

Observed:

```text
Configurational entropy deviates from ideal mixing.
```

AMS interpretation:

```text
The system is not behaving as a random averaged field.
It has internal ordering and role differentiation.
```

Mapping:

```text
non-ideal entropy
=> non-random local organisation
=> M4 mixed-competition nodes
=> D4 rather than simple averaged disorder
```

Evidence strength:

```text
strong
```

Reason:

This is one of the cleanest bridges from conventional thermodynamic language to AMS connectivity language.

### Raman and NMR Structural Evidence

Observed:

```text
Raman, 27Al MAS NMR, and 23Na MAS NMR indicate structural changes across Na/Mg substitution.
```

AMS interpretation:

```text
Subregion balance changes as cation roles shift.
```

Mapping:

```text
Al coordination shift
=> charge-compensation field changes
=> M1/M3 relation changes

Na environment shift
=> sodium route role changes
=> M2/M4 relation changes
```

Evidence strength:

```text
moderate-strong
```

Reason:

The structural evidence supports role-sharing and non-random organisation, but does not directly identify AMS route classes.

### Density and Molar Volume

Observed:

```text
Density decreases from Mg endmember to Na endmember; molar volume varies across the series.
```

AMS interpretation:

```text
The packing and relational closure field changes as Mg is replaced by Na.
```

Mapping:

```text
density/molar volume change
=> material-scale packing shift
=> supports but does not prove route reclassification
```

Evidence strength:

```text
moderate
```

Reason:

Density and molar volume are useful constraints, but less diagnostic than viscosity, entropy, and NMR.

## Untested Prediction Table

| Prediction | AMS basis | Required measurement | Expected confirmation pattern | Current strength |
|---|---|---|---|---|
| ion mobility rises non-linearly with `M2` connectivity | `M2` route percolation | electrical conductivity, tracer diffusion, ion transport | threshold or non-linear mobility across `X_Na2O` | pending |
| durability weakness follows connected weak paths | `M2` and `O5` | leaching, dissolution, corrosion tests | Na-rich / weak-path compositions degrade disproportionately | pending |
| `X=0.50` shows strongest mixed competition | high `M4` | combined viscosity, NMR, entropy, mobility comparison | maximum deviation from linear model near balanced composition | partially supported |
| `X=0.75` approaches `D3` transition | near-connected `M2` | conductivity/diffusion vs composition | mobility increases faster than linear expectation | pending |
| surface release depends on exposed subregion | M1/M2/M3/M4 interface exposure | surface spectroscopy, scattering, polishing, reflectance/transmission tests | different release behavior by local surface chemistry | weak-pending |

## Score Pressure by Property Class

| Property class | Evidence status | AMS fit | Score pressure |
|---|---|---:|---|
| viscosity / softening | observed | 8 | upward |
| configurational entropy | observed | 8 | upward |
| NMR structural role-sharing | observed | 8 | upward |
| Raman structural shift | observed | 7 | upward |
| density / molar volume | observed | 6.5 | mild upward |
| ion mobility | untested | 7 predicted | pending |
| chemical durability | untested | 7 predicted | pending |
| optical/interface release | untested | 5.5 predicted | neutral / pending |

## Updated Series Judgment

Current series score:

```text
Na/Mg aluminosilicate series: 7.5/10
confidence: moderate
```

This score is justified by:

- controlled composition path
- observed non-linear viscosity
- observed non-ideal configurational entropy
- structural evidence from Raman and NMR
- source-level interpretation of Na/Mg role-sharing

The score should not move above 7.5 until:

- ion mobility is tested across the same or closely comparable series
- durability is tested across the same or closely comparable series
- at least one composition has enough structural detail to estimate subregion connectivity more concretely

## Family-Level Judgment

Current broader family score:

```text
mixed Na/Mg silicate family: 7/10
confidence: moderate
```

Pressure:

```text
upward, but not enough for 7.5 yet
```

Reason:

The aluminosilicate series is strong, but it contains Al2O3. The broader family requires either:

- a lower-Al or Al-free Na/Mg silicate case
- direct ion mobility evidence
- direct durability evidence
- interface or optical behavior evidence

## Next Artifact

The next useful artifact should be:

```text
ams-na-mg-series-mobility-durability-prediction-grid-v1.md
```

That file should formalise the expected mobility and durability curves across `X_Na2O = 0.00` to `1.00` and define what evidence would confirm, weaken, or falsify the AMS connectivity reading.
