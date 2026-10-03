# AMS Aluminosilicate Ion-Exchange Strengthening Route Map v1

## Purpose

This file maps chemical strengthening of sodium aluminosilicate glass into AMS route language.

The key process is:

```text
K+ from molten salt replaces Na+ near the glass surface
larger K+ creates crowding / volume mismatch
surface compressive stress forms
surface hardness and damage resistance improve
```

The AMS question is:

```text
How can the glass allow enough ion exchange for strengthening while retaining enough network closure to hold compressive stress?
```

This is aluminium's `A5` role:

```text
A5 = ion-exchange regulator
```

## Source Basis

Initial source anchors:

- "Effect of Al2O3 content on the mechanical and interdiffusional properties of ion-exchanged Na-aluminosilicate glasses." https://doi.org/10.1016/j.jnoncrysol.2016.12.019
- "Effect of Al2O3 and MgO contents on the structure and mechanical properties of sodium aluminosilicate glasses with chemical strengthening treatment." https://doi.org/10.1016/j.ceramint.2025.07.350
- "Chemical Strengthening of Sodium Aluminosilicate Glasses Containing P2O5 and B2O3." https://doi.org/10.1016/j.jnoncrysol.2020.120600
- "Effects of Thermal and Pressure Histories on the Chemical Strengthening of Sodium Aluminosilicate Glass." https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2016.00014/full
- "Pressure-Induced Changes in Interdiffusivity and Compressive Stress in Chemically Strengthened Glass." https://doi.org/10.1021/am5019868
- "Structure, mechanical properties, and diffusion kinetics of chemical strengthening ultra-thin aluminosilicate glass by two-step method." https://www.sciencedirect.com/science/article/pii/S0272884225015913

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Chemical strengthening replaces smaller Na+ with larger K+ near the glass surface.
The K-for-Na exchange creates surface compressive stress because of size/volume mismatch.
Surface compressive stress improves mechanical resistance by suppressing crack growth.
In one sodium aluminosilicate series, increasing Al2O3 content increases surface compressive stress, surface hardness, and K+/Na+ exchange ratio while decreasing interdiffusion distance.
Higher Al2O3 content increases network connectivity and Tg.
Al2O3 and MgO can reduce non-bridging oxygen and improve network connectivity.
Ion-exchange behavior depends on composition, treatment temperature, time, density, thermal history, and pressure history.
Higher treatment temperature increases mutual diffusivity and depth of layer.
Compression or densification can decrease Na-K interdiffusivity and increase compressive stress.
Different network formers such as P2O5 and B2O3 can shift compressive stress and depth of layer in opposite directions.
```

## AMS Core Claim

Chemical strengthening works only if two route systems coexist:

```text
1. exchange route
=> K+ must enter and Na+ must leave near the surface

2. stress-retention route
=> the glass network must hold the resulting compressive mismatch
```

If the exchange route is too closed:

```text
not enough K+ enters
=> weak strengthening
```

If the network is too open:

```text
stress relaxes or diffuses too deeply
=> weak surface compression
```

The strong glass lies between:

```text
controlled R2 exchange
inside
strong R1 surface-retention matrix
```

## AMS Process Map

### Stage 1: Pristine Aluminosilicate Network

AMS profile:

```text
Al role: A1/A2
Na role: charge compensator + residual modifier
route: R1 with controlled R2 availability
obstruction: O1/O2
dominance: D1/D4
```

The network must contain exchangeable alkali ions, but not be so depolymerized that it cannot retain stress.

### Stage 2: Salt-Bath Boundary Forcing

Conventional process:

```text
KNO3 molten salt bath
K+ enters surface
Na+ exits surface
```

AMS profile:

```text
boundary condition: forced ion-exchange gradient
route: R2
obstruction: O5
dominance: local D3 at surface
```

This is an externally imposed exchange route.

The surface becomes a controlled diffusion interface.

### Stage 3: K-for-Na Replacement

Conventional process:

```text
larger K+ replaces smaller Na+
local volume/crowding mismatch develops
```

AMS profile:

```text
route: R2 admitted through A5 gate
obstruction: O2 if network gates exchange
dominance: D4
```

This is not free diffusion through a liquid-like field. It is gated substitution through an amorphous network.

### Stage 4: Surface Compressive Stress Retention

Conventional process:

```text
volume mismatch produces compressive surface layer
```

AMS profile:

```text
route: R1 stress-retention
obstruction: O1 against crack opening
dominance: D1
grade: G_A/G_B
```

The strengthened surface requires retained mismatch.

AMS formula:

```text
K-for-Na exchange
+ strong Al-supported network
=> retained compressive stress
=> crack growth obstruction
```

### Stage 5: Crack Suppression

AMS profile:

```text
external crack route: attempted R6 fracture propagation
surface compression: O1/O2 blocks opening route
dominance: D1 against fracture initiation
```

The surface compression does not remove defects. It changes whether cracks can open and propagate.

## Aluminium Role: `A5` Ion-Exchange Regulator

Aluminium's `A5` role is:

```text
allow exchange
limit over-diffusion
retain compressive stress
strengthen surface route closure
```

Mechanism:

```text
AlO4- charge-compensated network
=> stronger R1 matrix
=> lower uncontrolled interdiffusion
=> higher stress retention
```

But this is not a simple rule that more aluminium always means deeper exchange.

The observed pattern can vary:

```text
more Al2O3
=> higher network connectivity and Tg
=> higher compressive stress / hardness
=> often reduced interdiffusion distance in one series

Al2O3 plus MgO and higher treatment temperature
=> can improve ion-exchange efficiency and deeper strengthened layer in another context
```

AMS interpretation:

```text
Al controls route quality, not merely route quantity.
```

## Route Tension: Depth vs Stress

Ion-exchange strengthening has a built-in route tension.

```text
deep exchange
=> larger strengthened depth
=> requires open enough R2 pathway

high compressive stress
=> strong retained mismatch
=> requires closed enough R1 matrix
```

AMS map:

| Condition | Route result | Strengthening risk |
|---|---|---|
| too open | `R2/O5/D3` | exchange deep but stress relaxes |
| too closed | `R1/O1/D1` | stress can retain but exchange shallow |
| balanced | `R2 inside R1` | strong compressive layer |
| heterogeneous | `R2 -> R3`, `D4` | uneven exchange or local stress concentration |

The best strengthening field is not maximum diffusion. It is controlled substitution with retained stress.

## Aluminium Content Trajectory

Using the sodium aluminosilicate series logic:

```text
low Al2O3
=> more Na as modifier
=> more R2/O5 weak-route diffusion
=> easier interdiffusion but weaker stress retention

moderate Al2O3
=> mixed compensation/modifier field
=> controlled exchange begins to improve

high Al2O3 near compensation
=> stronger Al-supported R1 network
=> higher compressive stress/hardness
=> shallower but more effective exchange layer in some series
```

Route progression:

```text
low Al:
R2/O5/D3

moderate Al:
R2/R1/D4

high Al:
R1 with controlled R2/A5
```

## MgO Co-Role

Some strengthening data include MgO.

AMS reading:

```text
MgO
=> M3_Mg selective gate
=> reduces NBO
=> increases local network connectivity
=> changes ion-exchange pathway
```

Mg can sharpen gate behavior:

```text
Al provides charge-coupled topology.
Mg provides selective local constraint.
Together they can create a denser, stronger, more gated exchange field.
```

This helps explain why Al2O3/MgO combinations can affect hardness, compressive stress, and ion-exchange depth in composition-sensitive ways.

## Treatment History

Ion exchange depends strongly on processing.

AMS variables:

```text
temperature
time
density
thermal history
pressure history
surface side / float history
salt bath composition
```

Route interpretation:

```text
higher temperature
=> increases R2 route admission

higher density / compression
=> reduces R2 diffusivity
=> may increase R1 stress retention

thermal/pressure history
=> changes gate field before exchange
```

This means composition alone is insufficient.

AMS formula:

```text
strengthening outcome
= composition route field
+ boundary forcing
+ thermal history
+ pressure/density history
+ treatment duration
```

## Strengthening Outcome Classes

### Class S1: Open Exchange, Weak Retention

Profile:

```text
low network connectivity
high R2/O5
deep exchange possible
stress retention weaker
```

Likely in:

```text
low-Al, high-NBO glasses
```

AMS score:

```text
strengthening_fit: 6
```

### Class S2: Balanced Exchange and Retention

Profile:

```text
controlled R2
strong R1 matrix
A5 active
high compressive stress
useful surface hardness
```

Likely in:

```text
well-designed sodium aluminosilicate cover glasses
```

AMS score:

```text
strengthening_fit: 8.5
```

### Class S3: Closed Network, Shallow Exchange

Profile:

```text
very strong R1
limited R2 admission
high stress if exchange occurs
small depth of layer
```

Likely in:

```text
over-connected or dense networks
```

AMS score:

```text
strengthening_fit: 7
```

### Class S4: Heterogeneous Gate Field

Profile:

```text
mixed local composition
R2 -> R3
O5 -> O2
D4
uneven exchange or stress gradients
```

Likely in:

```text
compositionally complex or history-sensitive glasses
```

AMS score:

```text
strengthening_fit: 7.5
```

## Property Mapping

| Property | Conventional variable | AMS route meaning |
|---|---|---|
| surface compressive stress | retained K-for-Na crowding | `R1` stress-retention field |
| depth of layer | penetration depth of K | `R2` exchange-route reach |
| interdiffusion coefficient | Na/K mobility | `R2` route openness |
| surface hardness | strengthened surface resistance | `R1` matrix plus compression |
| crack resistance | suppression of crack opening | `O1/O2` against fracture route |
| Tg | network rearrangement resistance | R1 closure strength |
| density / molar volume | packing and available route space | route admission and stress relaxation constraints |

## Score Assessment

Aluminosilicate ion-exchange strengthening route map:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

This is a strong AMS subcase because:

- the mechanism is concrete and industrially important
- route tension between diffusion and stress retention is clear
- aluminium's `A5` role is distinct from simple network forming
- observed Al2O3 effects map cleanly to network connectivity and stress retention
- treatment history maps naturally to route admission and gate changes

Limitations:

- exact composition-specific numeric curves are not yet imported
- two-step and multi-step strengthening need separate route maps
- stress relaxation kinetics are not formalised mathematically
- surface hydration/weathering after exchange needs a separate degradation map

## Aluminium Family Score Reassessment

Current aluminium family score:

```text
8/10
```

Subcase scores:

```text
charge-compensation regime map: 8.5
sodium aluminosilicate composition series: 8.5
ion-exchange strengthening route map: 8.5
```

Updated family decision:

```text
aluminium material family: 8.5/10
confidence: moderate-high
```

Reason:

Aluminium now has three strong mapped subcases:

```text
charge compensation topology
composition-driven route transition
ion-exchange strengthening
```

These cover topology, transport, mechanical strengthening, durability, and surface compression. That is enough to move the whole family from 8 to 8.5.

Do not move above 8.5 yet because natural aluminosilicate minerals, clays, biological incompatibility/toxicity boundaries, and detailed surface degradation remain unmapped.

## Next Artifact

The next useful artifact should be:

```text
ams-aluminium-family-score-recalibration-v1.md
```

That file should lock the aluminium family score move:

```text
8 -> 8.5
```

and record the three supporting subcases plus remaining gaps.
