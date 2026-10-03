# AMS Na/Mg Aluminosilicate Series Map v1

## Purpose

This file maps the full five-point Na/Mg aluminosilicate composition series from the 2024 Pannefieu et al. study into AMS route, obstruction, dominance, connectivity, and expected property curves.

The series holds the base network constant:

```text
50 mol% SiO2
12.5 mol% Al2O3
37.5 mol% total Na2O + MgO
```

and varies:

```text
X_Na2O = Na2O / (Na2O + MgO)
```

across:

```text
0.00, 0.25, 0.50, 0.75, 1.00
```

This makes the series useful because it isolates a controlled Na/Mg substitution path within the same broad aluminosilicate network.

## Source Basis

Primary source:

- Pannefieu, Le Losq, Florian, and Moretti, "Effect of the Na/Mg mixing on the structure and properties of aluminosilicate melts," Journal of Non-Crystalline Solids, 2024. DOI page: https://doi.org/10.1016/j.jnoncrysol.2024.123056

Source-relevant facts:

- The paper reports non-linear variations in density, molar volume, viscosity, and configurational entropy as Na substitutes Mg.
- Raman, `27Al` MAS NMR, and `23Na` MAS NMR indicate structural changes across the series.
- Na and Mg are reported as having preferential role-sharing between network modifier and charge-compensating functions.
- Density decreases from the Mg endmember to the Na endmember.
- Viscosity changes substantially as Na replaces Mg.

AMS use of the source:

The source does not observe vortons. AMS uses the reported structural and property non-linearity as a coherence test for the route, obstruction, subregion, and connectivity model.

## Composition Points

| `X_Na2O` | SiO2 | Al2O3 | Na2O | MgO | AMS short name |
|---:|---:|---:|---:|---:|---|
| 0.00 | 50 | 12.5 | 0.000 | 37.500 | Mg endmember |
| 0.25 | 50 | 12.5 | 9.375 | 28.125 | Mg-dominant mixed |
| 0.50 | 50 | 12.5 | 18.750 | 18.750 | balanced mixed |
| 0.75 | 50 | 12.5 | 28.125 | 9.375 | Na-dominant mixed |
| 1.00 | 50 | 12.5 | 37.500 | 0.000 | Na endmember |

## Subregion Trajectory

| `X_Na2O` | `M1` silica/aluminosilicate backbone | `M2` sodium-diffusing | `M3` magnesium-selective | `M4` mixed-competition | Dominant pressure |
|---:|---:|---:|---:|---:|---|
| 0.00 | high | absent | dominant | absent | constraint / gate |
| 0.25 | high | low-moderate | high | moderate | interruption |
| 0.50 | high | moderate-high | moderate-high | high | mixed competition |
| 0.75 | high-moderate | high | low-moderate | moderate-high | near-percolation |
| 1.00 | moderate | dominant | absent | absent | diffusion / modifier route |

## Connectivity Trajectory

| `X_Na2O` | `M1` connectivity | `M2` connectivity | `M3` interruption | `M4` junction density | Primary regime |
|---:|---|---|---|---|---|
| 0.00 | connected | absent | dominant | absent | Regime 4 |
| 0.25 | connected | isolated / clustered | high | moderate | Regime 4 + 3 |
| 0.50 | connected | near-percolating | high | high | Regime 5 + 3 |
| 0.75 | partial-connected | near-connected / connected | moderate | moderate-high | Regime 3 + 2 |
| 1.00 | weakened but present | connected / dominant | absent | absent | Regime 2 |

## Route and Obstruction Curve

| `X_Na2O` | Primary route | Secondary routes | Primary obstruction | Secondary obstructions | Dominance | Grade |
|---:|---|---|---|---|---|---|
| 0.00 | `R1/R3` | none | `O1/O2` | none | `D1` | `G_A/G_B` |
| 0.25 | `R1/R3` | local `R2` | `O2` | local `O5` | `D1/D4` | `G_B` |
| 0.50 | `R2 -> R3` | `R1`, local `R5` | `O5 -> O2` | `O1`, local `O3` | `D4` | `G_B/G_C` |
| 0.75 | `R2` | `R3`, local `R5` | `O5` | `O2`, local `O3` | `D3/D4` | `G_B/G_C` |
| 1.00 | `R2` | possible `R6` at high disorder | `O5` | possible `O6` | `D3` | `G_B/G_C` |

## Point-by-Point Interpretation

### `X_Na2O = 0.00`: Mg Endmember

Composition:

```text
50 SiO2 - 12.5 Al2O3 - 0 Na2O - 37.5 MgO
```

AMS profile:

```text
M1 high
M2 absent
M3 dominant
M4 absent
```

Expected behavior:

The field is dominated by connected constraint and selective gate behavior.

Route grammar:

```text
R1/R3
O1/O2
D1
```

Interpretation:

This endmember defines the high-constraint baseline. Motion and rearrangement are not absent, but they are forced through narrower or more selective routes.

Score:

```text
composition_score: 7
confidence: moderate
```

Reason:

It is a useful baseline for magnesium-selective gating, but it is less distinctive than the mixed cases because it does not test `M4` competition.

### `X_Na2O = 0.25`: Mg-Dominant Mixed

Composition:

```text
50 SiO2 - 12.5 Al2O3 - 9.375 Na2O - 28.125 MgO
```

AMS profile:

```text
M1 high
M2 low-moderate
M3 high
M4 moderate
```

Expected behavior:

Sodium-rich weak routes begin to appear, but they are mostly isolated or clustered. Magnesium-rich selective regions remain strong enough to interrupt them.

Route grammar:

```text
local R2 attempting to enter R1/R3 field
O5 locally cut by O2
D1/D4
```

Interpretation:

This point should show early non-linearity if even small sodium addition changes local route availability disproportionately.

Score:

```text
composition_score: 7.25
confidence: moderate
```

Reason:

It tests whether sodium route-loosening appears before sodium-rich regions fully connect. That is a useful AMS discriminator.

### `X_Na2O = 0.50`: Balanced Mixed

Composition:

```text
50 SiO2 - 12.5 Al2O3 - 18.75 Na2O - 18.75 MgO
```

AMS profile:

```text
M1 high
M2 moderate-high
M3 moderate-high
M4 high
```

Expected behavior:

This is the maximum mixed-competition point.

Route grammar:

```text
R2 -> R3
O5 -> O2
local R5/O3
D4
```

Interpretation:

The central case is not a midpoint average. It is a competitive handoff field in which sodium-supported weak routes, magnesium-supported selective gates, and aluminosilicate role-sharing collide.

Score:

```text
composition_score: 7.5
confidence: moderate
```

Reason:

This remains the strongest single point because it best tests `M4` junction density and mixed-competition behavior.

### `X_Na2O = 0.75`: Na-Dominant Mixed

Composition:

```text
50 SiO2 - 12.5 Al2O3 - 28.125 Na2O - 9.375 MgO
```

AMS profile:

```text
M1 high-moderate
M2 high
M3 low-moderate
M4 moderate-high
```

Expected behavior:

Sodium-rich weak routes approach or cross the percolation threshold, but remaining Mg-rich and Al-related gate behavior can still interrupt or redirect motion.

Route grammar:

```text
R2 dominant
R3 secondary
O5 dominant
O2 secondary
D3/D4
```

Interpretation:

This point tests whether the field has shifted from mixed competition toward sodium-diffusion dominance.

Score:

```text
composition_score: 7.25
confidence: moderate
```

Reason:

It is a strong test for the `D4 -> D3` transition. Its value depends on whether property curves show threshold-like behavior rather than smooth averaging.

### `X_Na2O = 1.00`: Na Endmember

Composition:

```text
50 SiO2 - 12.5 Al2O3 - 37.5 Na2O - 0 MgO
```

AMS profile:

```text
M1 moderate
M2 dominant
M3 absent
M4 absent
```

Expected behavior:

The field is dominated by distributed weak routes.

Route grammar:

```text
R2
O5
D3
```

Interpretation:

This endmember defines the sodium-diffusion baseline. It is useful as a contrast case, but it is not the most distinctively mixed-modifier case.

Score:

```text
composition_score: 7
confidence: moderate
```

Reason:

It anchors the Na-rich endpoint but does not test mixed competition.

## Expected Property Curves

### Viscosity

AMS expectation:

```text
viscosity changes non-linearly as X_Na2O increases
```

Route interpretation:

```text
X=0.00: high constraint / narrow routes
X=0.25: first weak routes appear but are gated
X=0.50: maximum handoff competition
X=0.75: weak routes increasingly dominate
X=1.00: sodium-diffusion route field dominates
```

The key AMS claim is not simply that viscosity decreases as sodium replaces magnesium. It is that the curve should carry non-linear signatures because route availability and route completion are different events.

### Configurational Entropy

AMS expectation:

```text
entropy should not follow ideal random mixing
```

Route interpretation:

```text
Na/Mg role-sharing
=> non-random local ordering
=> M4 junction behavior
=> D4 rather than simple averaged disorder
```

This matches the source's report that configurational entropy deviates from an ideal mixing law.

### Density and Molar Volume

AMS expectation:

```text
density decreases from Mg endmember to Na endmember
but mixed points may not follow a purely linear structural interpretation
```

Route interpretation:

Density tracks composition partly, but molar volume and local role-sharing indicate changes in the available relational packing field.

### Ion Mobility

AMS expectation:

```text
X=0.00: low-moderate
X=0.25: local mobility pockets
X=0.50: non-linear threshold sensitivity
X=0.75: near-connected mobility paths
X=1.00: connected sodium mobility field
```

This is inferred rather than directly measured in the source. It should be tested with conductivity or diffusion data before being used as a primary score anchor for this specific series.

### Chemical Durability

AMS expectation:

```text
durability weakness should become more pathway-sensitive as X_Na2O rises
```

Predicted curve:

```text
Mg-rich: stronger constraint, more gate-controlled
balanced: uneven mixed vulnerability
Na-rich: broader weak-path vulnerability
```

This also requires direct durability data before becoming a primary score anchor.

## Series-Level Score

Individual case scores:

| `X_Na2O` | Composition score | Confidence | Main value |
|---:|---:|---|---|
| 0.00 | 7.00 | moderate | Mg gate baseline |
| 0.25 | 7.25 | moderate | early interruption regime |
| 0.50 | 7.50 | moderate | maximum mixed competition |
| 0.75 | 7.25 | moderate | `D4 -> D3` transition |
| 1.00 | 7.00 | moderate | Na diffusion baseline |

Series score:

```text
Na/Mg aluminosilicate series: 7.5/10
confidence: moderate
```

Reason:

The controlled composition path, reported non-linear properties, and structural evidence make this a strong AMS test series.

Family implication:

```text
mixed Na/Mg silicate family remains 7/10
upward pressure strengthened
```

Do not move the broader family to 7.5 yet because this series includes Al2O3 and does not directly test interface release, durability, or ion mobility across all points.

## Model Pressure

This series supports three AMS claims strongly:

```text
1. Mixed modifier behavior is not a linear average.
2. Na/Mg role-sharing maps naturally onto M4 mixed-competition nodes.
3. Viscosity and entropy non-linearity can be interpreted as route/connectivity non-linearity.
```

It leaves three claims under-tested:

```text
1. Whether M2 connectivity predicts measured ion mobility.
2. Whether interrupted M2 paths predict durability behavior.
3. Whether surface/interfacial release follows M1/M2/M3/M4 exposure.
```

## Next Artifact

The next useful artifact should be:

```text
ams-na-mg-series-prediction-vs-observation-table-v1.md
```

That file should separate:

- directly observed source behavior
- AMS-inferred behavior
- untested predictions
- score pressure by property class

This will prevent overloading the series with claims the source does not yet directly support.
