# AMS Sodium Aluminosilicate Composition Series Map v1

## Purpose

This file maps a concrete sodium aluminosilicate composition series into AMS route, obstruction, dominance, and property language.

The chosen experimental series is:

```text
(75 - x) SiO2 - x Al2O3 - 25 Na2O
x = 0, 5, 10, 15, 20, 25 mol%
```

This series is useful because `Na2O` is held constant while `Al2O3` increases. That lets the route map track how sodium shifts from weak-route modifier behavior toward aluminium charge-compensation behavior.

## Source Basis

Initial source anchors:

- "Structure and mechanical properties of compressed sodium aluminosilicate glasses: Role of non-bridging oxygens." https://doi.org/10.1016/j.jnoncrysol.2016.03.011
- Penn State metadata page for the same study: https://pure.psu.edu/en/publications/structure-and-mechanical-properties-of-compressed-sodium-aluminos
- "Structure and properties of sodium aluminosilicate glasses from molecular dynamics simulations." https://doi.org/10.1063/1.4816378
- PubMed page for the same MD study: https://pubmed.ncbi.nlm.nih.gov/23901993/
- "Effect of Al2O3 content on the mechanical and interdiffusional properties of ion-exchanged Na-aluminosilicate glasses." https://doi.org/10.1016/j.jnoncrysol.2016.12.019
- "Crack-resistant Al2O3-SiO2 glasses." https://www.nature.com/articles/srep23620

## Source-Supported Working Facts

The source literature supports these working facts:

```text
The experimental sodium aluminosilicate series uses (75-x)SiO2 - xAl2O3 - 25Na2O with x = 0,5,10,15,20,25.
In this series, Al2O3/Na2O <= 1.
Increasing Al2O3/Na2O decreases NBO/T.
Decreasing NBO/T increases network connectivity.
Tg increases with increasing Al2O3/Na2O.
Higher NBO content corresponds to depolymerized network, higher atomic packing density, lower hardness, and higher crack resistance in the compressed-glass study.
High-NBO glasses densify more under hot compression and show stronger pressure-induced property changes.
27Al NMR shows some five-fold Al in as-made high-NBO glasses, with additional formation under compression.
MD simulations over Al/Na = 0.6 to 1.5 find mostly four-fold Al in peralkaline compositions and small amounts of five-fold Al plus oxygen triclusters in peraluminous compositions.
Increasing Al/Na increases calculated bulk, shear, and Young's moduli in the MD study.
Ion-exchanged sodium aluminosilicate studies report higher Al2O3 content giving higher Tg, higher network connectivity, higher surface compressive stress and hardness, and lower interdiffusion distance.
```

## AMS Core Claim

In sodium aluminosilicate glass, increasing aluminium does not simply add a strengthening ingredient.

It changes sodium's job.

AMS reading:

```text
low Al
=> Na mostly opens the silicate network
=> R2/O5 weak-route pressure

increasing Al
=> Na increasingly compensates AlO4-
=> R1/O1 network support

near ideal compensation
=> strong Al[IV]-supported network
=> R1/D1

Al beyond compensation
=> topology complications
=> A4/D4 pressure
```

The series selected here reaches the ideal compensation boundary but does not cross it, because `Al2O3/Na2O <= 1`.

## Composition Table

| Case | SiO2 | Al2O3 | Na2O | Al2O3/Na2O | AMS regime |
|---:|---:|---:|---:|---:|---|
| NAS-00 | 75 | 0 | 25 | 0.00 | sodium silicate / modifier excess |
| NAS-05 | 70 | 5 | 25 | 0.20 | low-Al modifier excess |
| NAS-10 | 65 | 10 | 25 | 0.40 | moderate-Al modifier excess |
| NAS-15 | 60 | 15 | 25 | 0.60 | high-Al modifier excess |
| NAS-20 | 55 | 20 | 25 | 0.80 | near-compensation approach |
| NAS-25 | 50 | 25 | 25 | 1.00 | nominal ideal compensation |

## Route Progression

| Case | Al role | Na role | Route | Obstruction | Dominance | Grade |
|---:|---|---|---|---|---|---|
| NAS-00 | absent | modifier | `R2` | `O5` | `D3` | `G_B/G_C` |
| NAS-05 | limited `A1` | mostly modifier, some compensator | `R2` with local `R1` | `O5/O1` | `D3/D4` | `G_B` |
| NAS-10 | `A1/A2` increasing | modifier + compensator | `R2/R1` | `O5/O1` | `D4` | `G_B` |
| NAS-15 | strong `A1/A2` | compensator + modifier | `R1/R2` | `O1/O5` | `D1/D4` | `G_B/G_A` |
| NAS-20 | near-compensated `A1/A2` | mostly compensator | `R1` with local `R2` | `O1` with local `O5` | `D1` | `G_A/G_B` |
| NAS-25 | nominal compensated `A1` | compensator | `R1` | `O1` | `D1` | `G_A` |

## Point-by-Point Map

### NAS-00: Sodium Silicate Baseline

Composition:

```text
75 SiO2 - 0 Al2O3 - 25 Na2O
```

AMS profile:

```text
Al role: absent
Na role: M2 weak-route modifier
route: R2
obstruction: O5
dominance: D3
```

Interpretation:

This is the sodium-opened silicate baseline. Sodium creates non-bridging oxygen and lowers network closure strength.

Expected properties:

```text
high NBO/T
lower Tg relative to Al-bearing compositions
greater mobility/reactivity risk
lower hardness
higher densification response under compression
```

Score:

```text
composition_score: 7
confidence: moderate-high
```

### NAS-05: Low-Al Modifier-Excess Regime

Composition:

```text
70 SiO2 - 5 Al2O3 - 25 Na2O
```

AMS profile:

```text
Al role: limited A1
Na role: mostly modifier, some compensator
route: R2 with local R1
obstruction: O5/O1
dominance: D3/D4
```

Interpretation:

Aluminium begins to claim sodium for charge compensation, but sodium remains mostly available for modifier/NBO behavior.

Expected properties:

```text
NBO/T begins to decrease
Tg begins to rise
network connectivity increases locally
weak-route behavior still significant
```

Score:

```text
composition_score: 7.25
confidence: moderate-high
```

### NAS-10: Moderate-Al Modifier-Excess Regime

Composition:

```text
65 SiO2 - 10 Al2O3 - 25 Na2O
```

AMS profile:

```text
Al role: A1/A2 increasing
Na role: modifier + compensator
route: R2/R1
obstruction: O5/O1
dominance: D4
```

Interpretation:

The glass is now mixed between sodium-opened and aluminium-compensated network behavior.

Expected properties:

```text
NBO/T lower
Tg higher
hardness/stiffness increasing
mobility routes increasingly gated
```

Score:

```text
composition_score: 7.5
confidence: moderate-high
```

### NAS-15: High-Al Modifier-Excess Regime

Composition:

```text
60 SiO2 - 15 Al2O3 - 25 Na2O
```

AMS profile:

```text
Al role: strong A1/A2
Na role: compensator + modifier
route: R1/R2
obstruction: O1/O5
dominance: D1/D4
```

Interpretation:

Aluminium has become a major network participant. Sodium is split between charge-compensation and residual modifier roles.

Expected properties:

```text
network connectivity substantially increased
Tg increased
weak-route mobility reduced
mechanical rigidity increased
```

Score:

```text
composition_score: 7.75
confidence: moderate-high
```

### NAS-20: Near-Compensation Approach

Composition:

```text
55 SiO2 - 20 Al2O3 - 25 Na2O
```

AMS profile:

```text
Al role: near-compensated A1/A2
Na role: mostly compensator
route: R1 with local R2
obstruction: O1 with local O5
dominance: D1
```

Interpretation:

Most sodium is now structurally recruited into aluminium charge compensation. Weak-route sodium behavior is strongly reduced.

Expected properties:

```text
low NBO/T
high Tg
higher stiffness/hardness
reduced interdiffusion distance in ion-exchange contexts
stronger retained network
```

Score:

```text
composition_score: 8
confidence: moderate-high
```

### NAS-25: Nominal Ideal Compensation

Composition:

```text
50 SiO2 - 25 Al2O3 - 25 Na2O
```

AMS profile:

```text
Al role: A1 charge-compensated tetrahedral network former
Na role: compensator
route: R1
obstruction: O1
dominance: D1
```

Interpretation:

This is the ideal compensation boundary for the experimental series. Aluminium is maximally recruited into the network under the available sodium budget.

Expected properties:

```text
minimum NBO/T within this series
highest Tg within this series
strongest network connectivity within this series
highest route coherence within this series
```

Important caveat:

The ideal stoichiometric picture is not perfect. Source studies report five-fold aluminium in some sodium aluminosilicate glasses and additional formation under compression, so local `A4` topology complication remains possible.

Score:

```text
composition_score: 8.25
confidence: moderate-high
```

## Property Curve Predictions

### NBO/T

Observed/source-supported direction:

```text
NBO/T decreases as Al2O3/Na2O increases.
```

AMS route interpretation:

```text
Na shifts from M2 modifier role
to A1/A2 compensation role.
```

Route curve:

```text
R2/O5/D3
=> R2/R1/D4
=> R1/O1/D1
```

### Glass Transition Temperature

Observed/source-supported direction:

```text
Tg increases as Al2O3/Na2O increases.
```

AMS interpretation:

```text
greater route closure coherence
=> higher thermal resistance to rearrangement
```

### Hardness and Stiffness

Source-supported direction:

```text
network connectivity and mechanical moduli increase with Al/Na ratio.
high-NBO compositions show lower hardness.
```

AMS interpretation:

```text
R1 dominance increases
=> stiffness/hardness increase

R2/NBO dominance increases
=> easier deformation/densification
```

### Crack Resistance

Source-supported nuance:

```text
high-NBO glasses can show higher crack resistance despite lower hardness.
```

AMS interpretation:

```text
R2-compliant routes can dissipate local stress
while R1-dominant routes increase stiffness but may not maximize crack resistance alone.
```

This is important:

```text
stronger closure is not always better for every function.
```

### Ion Exchange

Source-supported direction from ion-exchanged aluminosilicate studies:

```text
higher Al2O3 content
=> higher surface compressive stress and hardness
=> lower interdiffusion distance
```

AMS interpretation:

```text
stronger Al-supported R1 network
=> exchange route becomes shallower but mechanically more effective
```

Route mapping:

```text
A5 ion-exchange regulator
=> controlled R2 surface exchange inside stronger R1 matrix
```

## Extension Beyond the Series: Peraluminous Regime

The selected experimental series stops at:

```text
Al2O3/Na2O = 1.00
```

But MD studies also cover:

```text
Al/Na > 1
```

AMS extension:

```text
Al excess
=> A4 higher-coordination topology complication
=> oxygen triclusters
=> R3/R4
=> O2/O4
=> D4
```

Expected property behavior:

```text
moduli may continue to increase
topology becomes more complex
transport depends strongly on local gate structure
stress response may involve coordination change
```

This extension should be treated separately from the six-point peralkaline-to-balanced series.

## Series Score

Sodium aluminosilicate composition series:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

The series strongly supports AMS because it provides a clear composition-driven route transition:

```text
Na modifier weak routes
=> Al charge-compensated backbone
=> stronger network closure
```

It also ties route change to observed property directions:

- NBO/T decrease
- Tg increase
- network connectivity increase
- stiffness/hardness increase
- densification behavior change
- ion-exchange behavior change

Limitations:

- exact numeric NBO/T values are not yet imported into the AMS table
- peraluminous extension needs a dedicated map
- surface/interface optics are not yet modelled
- crack resistance requires a separate compliance-vs-hardness treatment

## Aluminium Family Score Pressure

Previous aluminium family score:

```text
8/10
```

Subcases now:

```text
aluminium charge-compensation regime map: 8.5/10
sodium aluminosilicate composition series: 8.5/10
```

Updated pressure:

```text
strong upward pressure toward 8.5
```

Do not move the whole aluminium family yet unless one more independent subcase is mapped, preferably:

```text
chemical strengthening / ion exchange
or
calcium aluminosilicate Ca/Al regime map
```

## Next Artifact

The next useful artifact should be:

```text
ams-aluminosilicate-ion-exchange-strengthening-route-map-v1.md
```

Purpose:

Map aluminium's role in chemical strengthening:

- K+/Na+ exchange
- surface compressive stress
- interdiffusion depth
- Al2O3 content
- network connectivity
- hardness and crack resistance
- `A5` ion-exchange regulator behavior
