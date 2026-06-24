# AMS Aluminium Charge-Compensation Regime Map v1

## Purpose

This file maps aluminium charge-compensation regimes into AMS route, obstruction, dominance, and material-property language.

It focuses on three coupled ratios:

```text
Al/Na
Al/Ca
Al/Mg
```

and the more general relation:

```text
Al2O3 / modifier oxide
```

The aim is to make explicit when aluminium behaves as:

- `A1`: charge-compensated tetrahedral network former
- `A2`: compensation gate node
- `A3`: modifier-competition node
- `A4`: higher-coordination topology complication
- `A5`: ion-exchange regulator

## Source Basis

Initial source anchors:

- "Structure and mechanical properties of compressed sodium aluminosilicate glasses: Role of non-bridging oxygens." https://doi.org/10.1016/j.jnoncrysol.2016.03.011
- "Bridging and Nonbridging Oxygen Atoms in Alkali Aluminosilicate Glasses." https://experts.arizona.edu/en/publications/bridging-and-nonbridging-oxygen-atoms-in-alkali-aluminosilicate-g/
- "Fragility and configurational heat capacity of calcium aluminosilicate glass-forming liquids." https://www.sciencedirect.com/science/article/abs/pii/S0022309317300479
- "Temperature effects on non-bridging oxygen and aluminum coordination number in calcium aluminosilicate glasses and melts." https://doi.org/10.1016/j.gca.2007.11.018
- "Water in Alkali Aluminosilicate Glasses." https://www.frontiersin.org/articles/10.3389/fmats.2020.00085/supplementary-material/10.3389/fmats.2020.00085.s001
- "Laser-induced structural modification in calcium aluminosilicate glasses using molecular dynamic simulations." https://pmc.ncbi.nlm.nih.gov/articles/PMC8096823/
- "Ionic Conductivity in Sodium-Alkaline Earth-Aluminosilicate Glasses." https://doi.org/10.1111/jace.14101
- "Structure of alkali (alumino)silicate glasses. I. Tl+ luminescence and the nonbridging oxygen issue." https://experts.arizona.edu/en/publications/structure-of-alkali-aluminosilicate-glasses-i-tlsupsup-luminescen

## Source-Supported Regime Facts

The source literature supports these working facts:

```text
Al3+ can enter tetrahedral AlO4- units when charge-compensated.
At ideal compensation, aluminosilicate networks can be highly polymerized.
When modifier cations exceed aluminium charge-compensation demand, excess modifiers create non-bridging oxygens.
When modifier cations are insufficient, Al may appear in higher coordination states such as Al[V] or Al[VI], or be accommodated by oxygen triclusters.
NBO/T decreases as Al2O3/Na2O increases in sodium aluminosilicates.
Glass transition temperature and network connectivity increase as NBO/T decreases.
Calcium aluminosilicates complicate the ideal model because some Al[V] and NBO can appear even near nominal charge balance.
Temperature, pressure, quench history, and deformation can shift Al coordination.
Na transport in aluminosilicates is affected by Al coordination, NBOs, free volume, dielectric constant, and charge-compensation structures.
```

## AMS Core Claim

Aluminium is a charge-conditioned topology switch.

The same aluminium content can produce different route outcomes depending on available compensating cations.

AMS formula:

```text
Al role
= aluminium coordination
+ charge compensation
+ modifier surplus/deficit
+ network former context
+ thermal/mechanical history
```

This means aluminium cannot be scored or modelled by content alone.

## General Regime Map

### Regime A: Modifier Excess

Condition:

```text
modifier cations > AlO4 charge-compensation demand
```

Examples:

```text
Al/Na < 1
Al2O3 / Na2O < 1
CaO / Al2O3 > 1
MgO / Al2O3 > 1
```

Conventional structure:

```text
Al can be charge-compensated as Al[IV]
excess modifier creates non-bridging oxygens
network depolymerization increases
```

AMS role:

```text
A1 + excess M2/M3 modifier
```

Route profile:

```text
primary_route: R1/R2
secondary_route: R3 locally
primary_obstruction: O1/O5
secondary_obstruction: O2
dominance: D1/D3/D4 depending excess level
route_grade: G_B
```

Interpretation:

Aluminium is mostly successful as a network participant, but excess modifier opens weak routes.

AMS reading:

```text
Al joins the network.
Extra modifier opens the network.
```

### Regime B: Ideal or Near-Ideal Compensation

Condition:

```text
modifier cations approximately match AlO4 charge-compensation demand
```

Examples:

```text
Al/Na ~= 1
Al2O3 / Na2O ~= 1
CaO / Al2O3 ~= 1
MgO / Al2O3 ~= 1
```

Conventional structure:

```text
Al is mainly tetrahedral and charge-compensated
network is highly polymerized
NBOs are minimized but may not vanish completely in real systems
```

AMS role:

```text
A1 + A2
```

Route profile:

```text
primary_route: R1
secondary_route: R3 at local defects
primary_obstruction: O1
secondary_obstruction: O2
dominance: D1
route_grade: G_A/G_B
```

Interpretation:

This is the strongest aluminium backbone regime.

AMS reading:

```text
charge demand matched
=> AlO4 closure admitted
=> modifier no longer primarily weak-route opener
=> network connectivity strengthened
```

Important caveat:

```text
nominal balance does not guarantee perfect structure.
NBOs, Al[V], and triclusters may still appear due to composition, temperature, pressure, or history.
```

### Regime C: Modifier Deficit / Aluminium Excess

Condition:

```text
modifier cations < AlO4 charge-compensation demand
```

Examples:

```text
Al/Na > 1
Al2O3 / Na2O > 1
CaO / Al2O3 < 1
MgO / Al2O3 < 1
```

Conventional structure:

```text
not all Al can be simply charge-compensated as Al[IV]
higher-coordination Al[V]/Al[VI] may appear
oxygen triclusters may appear
topological accommodation becomes more complex
```

AMS role:

```text
A2 + A4
```

Route profile:

```text
primary_route: R3/R4
secondary_route: R1 locally
primary_obstruction: O2/O4
secondary_obstruction: O1
dominance: D4
route_grade: G_B/G_C
```

Interpretation:

Aluminium remains structurally important, but the system must solve excess charge/topology demand through local reconfiguration.

AMS reading:

```text
Al wants to join the network.
Compensation is insufficient.
The network develops strained gates, higher coordination, or tricluster solutions.
```

### Regime D: Thermal / Pressure / Deformation Shift

Condition:

```text
temperature, fictive temperature, pressure, shear, or compression alters coordination and NBO distribution
```

Conventional structure:

```text
Al[V] can increase with fictive temperature or deformation
NBO concentration may change depending composition
high pressure can generate higher-coordinated Al
dynamic coordination changes can contribute to deformation and flow
```

AMS role:

```text
A4 dynamic topology shift
```

Route profile:

```text
primary_route: R4/R3
secondary_route: R2 during flow
primary_obstruction: O4/O2
secondary_obstruction: O5
dominance: D4
route_grade: G_C locally, G_B systemically if stress is dissipated
```

Interpretation:

Aluminium can become a stress-adaptive topology element.

AMS reading:

```text
coordination change
=> route reconfiguration
=> stress accommodation or flow
```

This matters because higher-coordination aluminium is not merely a defect. It can be part of how the glass rearranges under thermal or mechanical stress.

## Al/Na Regimes

### `Al/Na < 1`: Sodium Excess

Source-supported pattern:

```text
Al can be charge-compensated.
Excess Na acts as network modifier.
NBOs appear.
```

AMS map:

```text
Al role: A1
Na role: charge compensator + M2 modifier
route: R1/R2
obstruction: O1/O5
dominance: D1/D3/D4 depending excess sodium
```

Material expectation:

```text
increased workability / ion mobility
reduced network rigidity relative to ideal compensation
durability depends on weak-route connectivity
```

### `Al/Na ~= 1`: Charge Balance

Source-supported pattern:

```text
Al is mostly tetrahedral.
Na is mostly charge compensating.
Network is more polymerized.
NBOs minimized.
```

AMS map:

```text
Al role: A1/A2
Na role: compensator
route: R1
obstruction: O1
dominance: D1
```

Material expectation:

```text
higher Tg
higher stiffness/connectivity
lower free modifier mobility
better chemical durability
```

### `Al/Na > 1`: Aluminium Excess

Source-supported pattern:

```text
not all Al can be charge-compensated by Na.
Al[V]/Al[VI] or oxygen triclusters may appear.
```

AMS map:

```text
Al role: A2/A4
Na role: insufficient compensator
route: R3/R4
obstruction: O2/O4
dominance: D4
```

Material expectation:

```text
topology becomes composition-sensitive
stiffness may remain high
local rearrangement paths become important
transport depends on gate structure
```

## Al/Ca Regimes

### `Ca/Al > 1`: Calcium Excess

Conventional pattern:

```text
Ca can charge-compensate Al.
Excess Ca can act as modifier and create NBOs.
```

AMS map:

```text
Al role: A1
Ca role: compensator + M3_Ca bridge modifier
route: R1/R2
obstruction: O1/O2
dominance: D1/D4
```

Material expectation:

```text
calcium bridge-stabilisation
but possible depolymerization if Ca excess is high
reactivity may increase where Ca forms NBO-related sites
```

### `Ca/Al ~= 1`: Calcium-Aluminium Charge Balance

Conventional pattern:

```text
ideal model predicts Al[IV] charge compensation and minimal NBO.
real CAS glasses may still contain some Al[V] and NBO.
```

AMS map:

```text
Al role: A1/A2
Ca role: bridge compensator
route: R1 with local R3
obstruction: O1 with local O2
dominance: D1/D4
```

Material expectation:

```text
strong calcium-aluminosilicate backbone
but local topology complications remain possible
```

### `Ca/Al < 1`: Calcium Deficit / Aluminium Excess

Conventional pattern:

```text
Al charge demand exceeds Ca compensation.
higher-coordination Al and triclusters become more likely.
```

AMS map:

```text
Al role: A4 pressure
Ca role: insufficient bridge compensator
route: R3/R4
obstruction: O2/O4
dominance: D4
```

Material expectation:

```text
high topology sensitivity
possible increased polymerization with strained accommodation
reactivity and durability depend on local charge solutions
```

## Al/Mg Regimes

### `Mg/Al > 1`: Magnesium Excess

Conventional pattern:

```text
Mg can act as charge compensator and/or modifier depending composition.
Mg has stronger field strength than Ca.
```

AMS map:

```text
Al role: A1/A2
Mg role: M3_Mg selective gate + possible modifier
route: R1/R3
obstruction: O1/O2
dominance: D1/D4
```

Material expectation:

```text
stronger local gating than Ca
more selective constraint
transport may be sharply affected
```

### `Mg/Al ~= 1`: Magnesium-Aluminium Charge Balance

Conventional pattern:

```text
Mg charge compensation can support Al[IV], but Mg's higher field strength creates stronger local structural effects than Ca.
```

AMS map:

```text
Al role: A1/A2
Mg role: selective compensation gate
route: R1/R3
obstruction: O1/O2
dominance: D1/D4
```

Material expectation:

```text
strong but more locally constrained network
high relevance for Na/Mg aluminosilicate transport
```

### `Mg/Al < 1`: Magnesium Deficit / Aluminium Excess

Conventional pattern:

```text
Al compensation demand exceeds Mg supply.
higher-coordination Al or tricluster accommodation becomes more likely.
```

AMS map:

```text
Al role: A4
Mg role: insufficient selective gate
route: R3/R4
obstruction: O2/O4
dominance: D4
```

Material expectation:

```text
topology-sensitive stiffness and deformation behavior
possible dynamic Al coordination shifts under stress
```

## Modifier Role Switch Table

| Modifier cation | Role when compensating AlO4 | Role when excess | AMS switch |
|---|---|---|---|
| Na+ | charge support for network | weak-route opener / NBO creator | `R1` support -> `R2/O5` |
| Ca2+ | bridge compensator | bridge-stabilising modifier / possible NBO creator | `R1` support -> `R1/R2` |
| Mg2+ | selective compensator | high-field modifier / gate | `R1` support -> `R1/R3` |

This table is central.

AMS implication:

```text
the same cation cannot be assigned one fixed route role.
its role depends on whether aluminium has already claimed it for compensation.
```

## Property Predictions

### Durability

Expected AMS relation:

```text
ideal compensation / high polymerization
=> higher durability

modifier excess / connected NBO routes
=> lower durability

Al excess / topology complication
=> durability depends on local accommodation
```

### Stiffness and Hardness

Expected AMS relation:

```text
R1-dominant Al[IV] network
=> higher stiffness / hardness

R2/NBO-rich network
=> lower hardness, more densification potential

A4 higher-coordination regions
=> stress-sensitive deformation response
```

### Ion Mobility

Expected AMS relation:

```text
modifier as charge compensator
=> reduced free modifier mobility

modifier as NBO-associated mobile species
=> increased mobility

Al gate structures
=> mobility controlled by charge-compensation geometry
```

### Reactivity

Expected AMS relation:

```text
NBO-rich modifier-excess regions
=> higher reactivity

highly polymerized Al[IV] network
=> lower reactivity

Al/Ca imbalance
=> reactivity depends on whether Ca remains available for NBO-associated sites
```

## Score Assessment

Aluminium charge-compensation regime map:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

This is a strong AMS subcase because the regime map directly captures:

- why content alone is insufficient
- why modifier role changes with compensation demand
- why NBO formation changes route grammar
- why Al coordination shifts matter
- why transport, durability, stiffness, and reactivity are coupled

Limitations:

- needs composition-specific Al/Na and Al/Ca examples
- needs quantitative NBO/T and Al coordination tables
- needs direct mapping to chemical-strengthening data
- thermal/pressure history needs deeper modelling

## Aluminium Family Score Pressure

Previous aluminium family score:

```text
8/10
```

Charge-compensation regime subcase:

```text
8.5/10
```

Updated pressure:

```text
upward, but retain aluminium family at 8/10 for now
```

Reason:

The compensation map is strong, but the family still needs:

- a sodium aluminosilicate composition series map
- a calcium aluminosilicate composition series map
- chemical strengthening / ion exchange route map
- natural aluminosilicate mineral or clay case

## Next Artifact

The next useful artifact should be:

```text
ams-sodium-aluminosilicate-composition-series-map-v1.md
```

Purpose:

Use a concrete `SiO2-Al2O3-Na2O` series to map:

- increasing Al2O3/Na2O
- NBO/T decrease
- Tg increase
- density / hardness / crack resistance changes
- Al[IV]/Al[V] shifts
- route transitions from `R2/O5` toward `R1/O1`, then `A4/D4` if Al exceeds compensation
