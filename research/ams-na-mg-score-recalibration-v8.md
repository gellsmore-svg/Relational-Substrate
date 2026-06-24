# AMS Na/Mg Score Recalibration v8

## Purpose

This recalibration records the score impact of the Na/Mg mixed-modifier modelling sequence.

It follows these artifacts:

- `ams-glass-modifier-case-study-v1.md`
- `ams-glass-modifier-composition-gradient-v1.md`
- `ams-glass-modifier-material-property-table-v1.md`
- `ams-mixed-modifier-subregion-model-v1.md`
- `ams-mixed-modifier-property-comparison-v1.md`
- `ams-mixed-modifier-percolation-and-connectivity-v1.md`
- `ams-mixed-modifier-connectivity-scorecard-v1.md`
- `ams-specific-mixed-silicate-composition-template-v1.md`
- `ams-first-specific-na-mg-silicate-case-v1.md`
- `ams-na-mg-aluminosilicate-series-map-v1.md`
- `ams-na-mg-series-prediction-vs-observation-table-v1.md`
- `ams-na-mg-series-mobility-durability-prediction-grid-v1.md`
- `ams-na-mg-series-source-hunt-mobility-durability-v1.md`
- `ams-na-mg-transport-anchor-integration-v1.md`

## Current Scores Before v8

```text
mixed Na/Mg silicate family: 7/10
Na/Mg aluminosilicate series: 7.5/10
mixed Na/Mg balanced composition case: 7.5/10
```

## Recalibration Inputs

### Strong Inputs

```text
Na/Mg mixed modifier behavior has a controlled composition series.
Na/Mg substitution produces non-linear viscosity and configurational entropy behavior.
Raman and NMR evidence support structural role changes.
Na and Mg show preferential role-sharing rather than simple ideal averaging.
Connectivity modelling now distinguishes isolated, interrupted, connected, and competitive regimes.
Transport anchor evidence supports Na mobility being gated by alkaline-earth / aluminosilicate structure.
```

### Moderate Inputs

```text
The balanced X_Na2O = 0.50 case maps cleanly onto M4 mixed-competition behavior.
The X_Na2O = 0.75 case is a plausible D4 -> D3 transition point.
Al charge-compensation structures provide a concrete basis for M1/M3 gate modelling.
Activation energy can be mapped into route-grade language.
```

### Weak or Pending Inputs

```text
No exact five-point Na/Mg conductivity curve has been located.
No exact five-point Na/Mg durability curve has been located.
Interface release, optical behavior, and surface route exposure remain untested.
Pure or low-Al Na/Mg silicate evidence is still thinner than aluminosilicate evidence.
```

## Evidence Status Update

| Evidence class | Previous status | v8 status | Score effect |
|---|---|---|---|
| structural role-sharing | strong | strong | supports 7.5 series |
| viscosity non-linearity | strong | strong | supports 7.5 series |
| configurational entropy non-ideality | strong | strong | supports 7.5 series |
| Na/Mg subregion model | moderate | moderate-strong | supports 7 family |
| connectivity/percolation model | moderate | moderate-strong | supports 7 family |
| mobility | pending | partially supported with adjacent direct evidence | upward pressure |
| durability | pending | analogue-supported only | no upgrade |
| interface release | pending | pending | no upgrade |
| pure Na/Mg silicate family breadth | moderate-low | moderate-low | limits family score |

## Score Decisions

### Mixed Na/Mg Silicate Family

Previous:

```text
7/10
```

v8 decision:

```text
retain 7/10
```

Confidence:

```text
moderate, strengthened
```

Reason:

The family-level model is now much stronger than when it first moved from 6.5 to 7. It has subregions, connectivity regimes, a comparative scorecard, a composition template, and a transport-anchor integration.

The score does not move higher because the strongest direct series is aluminosilicate, not a broad pure Na/Mg silicate family, and because durability/interface claims remain under-tested.

Score pressure:

```text
upward
```

Upgrade condition:

```text
7 -> 7.5
if either:
1. direct Na/Mg conductivity or diffusion data across a comparable substitution series confirms the predicted M2 connectivity curve
or
2. direct Na/Mg durability data confirms weak-path / gate-controlled degradation behavior
or
3. a low-Al or Al-free Na/Mg silicate series shows the same non-linear route pattern.
```

### Na/Mg Aluminosilicate Series

Previous:

```text
7.5/10
```

v8 decision:

```text
retain 7.5/10
```

Confidence:

```text
moderate, strengthened
```

Reason:

The series remains the strongest Na/Mg controlled case. It has direct support for non-linear viscosity, non-ideal configurational entropy, structural role-sharing, and composition-controlled substitution.

Mobility is now partially supported by adjacent direct evidence from sodium-alkaline-earth-aluminosilicate conductivity work. That strengthens confidence but does not justify a numerical upgrade because the exact five-point conductivity curve remains missing.

Score pressure:

```text
upward
```

Upgrade condition:

```text
7.5 -> 8
if direct conductivity, diffusion, or durability data are found for the same or closely matched X_Na2O series.
```

### Balanced `X_Na2O = 0.50` Case

Previous:

```text
7.5/10
```

v8 decision:

```text
retain 7.5/10
```

Confidence:

```text
moderate
```

Reason:

The balanced case remains the strongest mixed-competition point. It maps cleanly to:

```text
primary_regime: Regime 5 frequent M4 junctions
secondary_regime: Regime 3 interrupted M2 pathways
route: R2 -> R3
obstruction: O5 -> O2
dominance: D4
```

It does not move higher because mobility and durability for this exact composition remain inferred.

## Route Model Recalibration

The transport-anchor integration changes the mobility model from:

```text
Ion mobility follows M2 connectivity.
```

to:

```text
Ion mobility follows M2 connectivity as admitted or gated by M1/M3 charge-compensation structures.
```

This is a meaningful refinement.

It prevents the model from becoming sodium-content reductionism.

Updated formula:

```text
Na mobility
= M2 route potential
x M1 network admission
x M3 gate condition
x M4 mixed-junction interference
```

## Score Log Entry

```text
v8 recalibration:

mixed Na/Mg silicate family
score: 7/10
confidence: moderate, strengthened
pressure: upward
reason: subregion, connectivity, composition-template, and transport-anchor modelling now coherent; exact conductivity/durability series still missing.

Na/Mg aluminosilicate series
score: 7.5/10
confidence: moderate, strengthened
pressure: upward
reason: direct non-linear viscosity, entropy, Raman/NMR role-sharing; mobility partially supported by adjacent conductivity evidence.

balanced Na/Mg aluminosilicate X_Na2O=0.50
score: 7.5/10
confidence: moderate
pressure: upward if direct transport/durability data are found.
```

## No-Upgrade Rationale

No score moves upward numerically in v8.

Reason:

```text
The work improved mechanism clarity and evidence integration.
It did not yet add exact direct transport/durability measurements for the same Na/Mg series.
```

This is important for keeping the 1-10 confidence scale meaningful.

## Next Workstream

The Na/Mg mixed-modifier line is now stable enough to pause unless new direct data are found.

Recommended next workstream:

```text
calcium material family entry
```

Why calcium:

- central in silicate glasses and minerals
- strong biological relevance
- interacts with phosphate, carbonate, proteins, membranes, and bone-like structures
- useful bridge from T1B material modelling into T1C biological stress tests
- important interface modifier in soda-lime glass and bioactive glass systems

Next artifact:

```text
ams-calcium-material-family-entry-v1.md
```
