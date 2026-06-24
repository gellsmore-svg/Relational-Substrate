# AMS Na/Mg Series Mobility and Durability Prediction Grid v1

## Purpose

This file defines the AMS predictions for ion mobility and chemical durability across the five-point Na/Mg aluminosilicate series.

It separates:

- expected curve shape
- AMS route cause
- confirming evidence
- weakening evidence
- falsifying evidence

This is important because the main source series directly supports viscosity, entropy, and structural role-sharing, but does not directly measure ion mobility or durability across all compositions.

## Series

```text
50 mol% SiO2
12.5 mol% Al2O3
37.5 mol% total Na2O + MgO

X_Na2O = Na2O / (Na2O + MgO)

X = 0.00, 0.25, 0.50, 0.75, 1.00
```

## AMS Connectivity Premise

The prediction depends on this route sequence:

```text
X=0.00
=> M3 dominant
=> R1/R3, O1/O2, D1

X=0.25
=> M2 appears but remains mostly interrupted
=> local R2 cut by R3, O5 cut by O2, D1/D4

X=0.50
=> M4 strongest
=> route handoff competition, R2 -> R3, O5 -> O2, D4

X=0.75
=> M2 near-connected or connected
=> R2 dominant with residual R3/O2, D3/D4

X=1.00
=> M2 dominant
=> R2, O5, D3
```

The core prediction is not a smooth line. The core prediction is a connectivity curve with thresholds.

## Mobility Prediction

### Expected Shape

AMS predicts that ion mobility should increase as Na replaces Mg, but not as a simple linear function.

Expected qualitative curve:

```text
X=0.00: low
X=0.25: low-moderate with local mobility pockets
X=0.50: moderate but strongly non-linear / mixed
X=0.75: high or sharply rising
X=1.00: high
```

Expected curve type:

```text
threshold-sensitive rise between X=0.50 and X=0.75
or strong deviation from linear interpolation near X=0.50
```

### AMS Cause

```text
Ion mobility follows M2 connectivity.
```

Detailed cause:

```text
M2 isolated
=> local sodium mobility only

M2 near-percolating
=> mobility pressure but interrupted routes

M2 connected
=> material-scale mobility path
```

Route mapping:

```text
R2 = distributed weak route
O5 = diffusing obstruction
D3 = diffusion-dominant field
```

Mobility should increase most strongly when the system shifts from:

```text
interrupted R2 -> connected R2
```

## Mobility Prediction Table

| `X_Na2O` | AMS mobility class | Route cause | Expected observation | Score pressure if observed |
|---:|---|---|---|---|
| 0.00 | low | `M3`, `R1/R3`, `O1/O2` | low conductivity / diffusion | baseline |
| 0.25 | low-moderate | isolated `M2` pockets | small increase, local effects only | mild upward |
| 0.50 | moderate / non-linear | high `M4`, interrupted `M2` | deviation from linear trend | upward |
| 0.75 | high / threshold | near-connected `M2` | sharp rise or strong curvature | strong upward |
| 1.00 | high | connected `M2`, `R2/O5/D3` | high Na mobility | baseline |

## Mobility Confirmation Conditions

Mobility evidence confirms the AMS reading if one or more of the following are observed:

```text
1. Conductivity or diffusion rises non-linearly rather than linearly with X_Na2O.
2. The strongest change occurs between X=0.50 and X=0.75.
3. X=0.50 shows anomalous behavior relative to both endmember interpolation and simple modifier averaging.
4. Na-rich mobility appears locally before it becomes whole-material mobility.
5. Structural evidence shows Na-rich pathways or Na environments becoming more connected with increasing X.
```

## Mobility Weakening Conditions

Mobility evidence weakens the AMS reading if:

```text
1. Conductivity or diffusion follows a near-perfect linear interpolation between endmembers.
2. X=0.50 shows no anomaly or non-linear behavior.
3. Mobility tracks only total sodium content with no structural dependence.
4. NMR or other structural data show no meaningful change in Na environment across the series.
```

## Mobility Falsification Conditions

Mobility evidence would seriously challenge this AMS submodel if:

```text
1. Mobility is highest at X=0.00 and lowest at X=1.00 without a separate mechanism.
2. Mixed compositions show no detectable mobility difference from linear averaging despite strong structural non-ideality.
3. A directly mapped Na connectivity measurement contradicts the inferred M2 connectivity sequence.
4. X=0.75 remains mobility-suppressed while X=0.50 and X=1.00 are high, with no structural gate explanation.
```

## Durability Prediction

### Expected Shape

AMS predicts that chemical durability should generally weaken as sodium-supported weak paths become more connected, but the curve should be uneven rather than simply proportional to sodium content.

Expected qualitative curve:

```text
X=0.00: relatively stronger / gate-controlled
X=0.25: mostly retained durability with local vulnerable pockets
X=0.50: uneven mixed durability
X=0.75: weaker, pathway-sensitive durability
X=1.00: weakest or broadly weak-path dominated
```

Expected curve type:

```text
non-linear degradation vulnerability
with increased path sensitivity near X=0.50 to X=0.75
```

### AMS Cause

```text
Durability follows connected weak paths, not modifier presence alone.
```

Detailed cause:

```text
isolated M2
=> local vulnerability only

interrupted M2
=> uneven vulnerability

connected M2
=> material-scale degradation pathways
```

Magnesium-rich and aluminosilicate constraint regions can delay or interrupt degradation:

```text
M3 / M1 constraint
=> O2 late gates
=> degradation route termination
```

## Durability Prediction Table

| `X_Na2O` | AMS durability class | Route cause | Expected observation | Score pressure if observed |
|---:|---|---|---|---|
| 0.00 | stronger / gate-controlled | connected `M1/M3` | low leaching / slower dissolution | baseline |
| 0.25 | mostly retained, local weak pockets | isolated `M2` cut by `M3` | small local vulnerability | mild upward |
| 0.50 | uneven / mixed | high `M4`, interrupted paths | non-uniform degradation | upward |
| 0.75 | weaker / path-sensitive | near-connected `M2` | strong increase in leaching or dissolution | strong upward |
| 1.00 | broad weak-path vulnerability | connected `M2` | high leaching / faster dissolution | baseline |

## Durability Confirmation Conditions

Durability evidence confirms the AMS reading if:

```text
1. Durability degradation is non-linear across X_Na2O.
2. X=0.50 shows uneven or anomalous durability rather than midpoint behavior.
3. X=0.75 shows disproportionate vulnerability compared with X=0.50.
4. Leaching/dissolution follows structural weak paths rather than bulk composition alone.
5. Mg-rich regions or Al-related constraint regions are associated with local degradation interruption.
```

## Durability Weakening Conditions

Durability evidence weakens the AMS reading if:

```text
1. Durability is a simple monotonic linear function of Na content.
2. Mixed compositions show no local unevenness or path sensitivity.
3. Structural maps show uniform modifier distribution with no relation to degradation behavior.
4. Mg-rich or constraint-rich regions do not alter degradation progression at all.
```

## Durability Falsification Conditions

Durability evidence would seriously challenge this AMS submodel if:

```text
1. Connected sodium-rich pathways are observed but have no effect on durability.
2. Degradation proceeds uniformly through all subregions despite strong structural heterogeneity.
3. The most sodium-rich endmember is most durable without a separate stabilising mechanism.
4. Mixed compositions are more durable or less durable in ways that contradict their mapped connectivity and cannot be explained by phase separation, crystallisation, hydration, or other conventional structure changes.
```

## Combined Mobility-Durability Pattern

The strongest confirmation would be coupled behavior:

```text
mobility increase
+ durability decrease
both tracking the same inferred M2 connectivity transition
```

Best expected confirmation:

```text
X=0.50
=> mixed / anomalous

X=0.75
=> threshold-like increase in mobility
=> increased degradation vulnerability
```

This would support:

```text
M2 connectivity controls material-scale weak-path behavior.
```

## Score Implications

Current score:

```text
Na/Mg aluminosilicate series: 7.5/10
mixed Na/Mg silicate family: 7/10
```

If mobility evidence confirms the curve:

```text
series: 7.5 -> 8
family: 7 -> 7.25
```

If durability evidence confirms the curve:

```text
series: 7.5 -> 8
family: 7 -> 7.25
```

If both mobility and durability confirm the same connectivity transition:

```text
series: 8.25 possible
family: 7.5 possible
```

If both are linear and structure-independent:

```text
series: 7.5 -> 6.5 or 7
family: 7 -> 6.5
```

## Next Artifact

The next useful artifact should be:

```text
ams-na-mg-series-source-hunt-mobility-durability-v1.md
```

That file should search specifically for:

- electrical conductivity across Na/Mg aluminosilicate or Na/Mg silicate series
- sodium diffusion across Na/Mg mixed modifier series
- leaching or dissolution across Na/Mg aluminosilicate/silicate series
- any structural mapping tying Na/Mg distribution to transport or durability

The purpose is to replace the pending prediction fields with observed evidence where possible.
