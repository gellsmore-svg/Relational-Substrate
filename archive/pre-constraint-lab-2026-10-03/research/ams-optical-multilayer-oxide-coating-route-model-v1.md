# AMS Optical Multilayer Oxide Coating Route Model v1

## Purpose

This file models the missing bridge between ideal optical surfaces and real optical components.

It covers:

- dielectric antireflection coatings on glass
- protected aluminium mirrors
- protected silver mirrors
- tarnished silver
- oxidised aluminium
- oxidised copper
- rusted iron
- thin-film interference as route recombination

The core issue:

```text
real optical surfaces are rarely single clean interfaces.
They are terminal-layer stacks.
```

## Source Basis

Initial source anchors:

- NASA Science, "Coated Mirrors Achieve Record-setting Far Ultraviolet Reflectance Levels." https://science.nasa.gov/science-research/science-enabling-technology/technology-highlights/coated-mirrors-achieve-record-setting-far-ultraviolet-reflectance-levels/
- NASA NTRS, "Advanced Al Mirrors Protected with LiF Overcoat to Realize Stable Mirror Coatings for Astronomical Telescopes." https://ntrs.nasa.gov/citations/20230006299
- NASA Technology Transfer, "Advanced AlF3-Passivated Aluminum Mirrors." https://technology.nasa.gov/patent/GSC-TOPS-363
- Laser Focus World, "Thin-film Coatings: Understanding key design principles of antireflection coatings." https://www.laserfocusworld.com/optics/article/16547029/thin-film-coatings-understanding-key-design-principles-of-antireflection-coatings
- Abridged Optics, "Reflective Optics & Mirrors." https://www.abridgedoptics.com/comprehensive/optics/mirrors
- Springer, "Anti-reflective and optical transparent coatings fabricated by a computer-controlled system." https://link.springer.com/article/10.1007/s11082-026-08675-w
- Quarter-wave AR calculator reference page. https://www.firgelliauto.com/blogs/calculators/anti-reflection-coating-quarter-wave-calculator

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Thin optical coatings work by creating multiple reflected/transmitted waves that interfere constructively or destructively.
Quarter-wave antireflection coatings reduce reflection when optical thickness is lambda/4 at the design wavelength.
The ideal single-layer antireflection coating index is approximately sqrt(n_air * n_substrate).
Multilayer coatings broaden or tune the spectral response beyond a single wavelength.
Bare aluminium has intrinsically high reflectance across broad UV/visible/IR ranges but oxidizes rapidly.
Protective fluoride overcoats such as MgF2 or LiF are used to protect aluminium and improve or preserve UV/FUV reflectance.
Protective overcoats can themselves absorb or limit reflectance in some wavelength ranges.
Silver has very high visible/near-IR reflectance but tarnishes; protective dielectric coatings slow degradation.
Protected metal coatings trade some ideal bare-metal performance for environmental stability and cleanability.
Oxides, tarnish, rust, and roughness change surface reflectance by adding absorbing, scattering, or phase-shifting terminal layers.
```

## AMS Core Claim

A coating is a route-engineered terminal layer.

AMS reading:

```text
coating
= deliberately inserted route gate
that controls how incident optical routes split,
recombine,
cancel,
transmit,
or return.
```

Oxide and tarnish are uncontrolled terminal layers:

```text
oxide/tarnish/rust
= accidental route gate
that filters, absorbs, scatters, or phase-shifts the primary optical route.
```

## Terminal-Layer Stack Model

Single clean interface:

```text
medium 0 -> medium 1
```

Coated interface:

```text
medium 0 -> coating layer -> substrate
```

Multilayer mirror:

```text
air -> protective dielectric stack -> metal -> substrate
```

Oxidised metal:

```text
air -> oxide/tarnish/rust layer -> metal
```

AMS stack variables:

```text
Layer_i:
  n_i(lambda)
  k_i(lambda)
  d_i
  roughness_i
  coherence_i
  absorption_i
  scattering_i
```

Whole-stack route:

```text
R_stack(lambda)
T_stack(lambda)
A_stack(lambda)
S_stack(lambda)
```

with:

```text
R + T + A + S = 1
```

## Thin-Film Route Recombination

Conventional thin-film effect:

```text
reflections occur at multiple interfaces
the reflected waves recombine
phase determines constructive or destructive interference
```

AMS translation:

```text
route splits at each terminal boundary
partial return routes acquire phase delay
return routes recombine
recombination either strengthens or cancels the returned route
```

Route notation:

```text
R_top
= route returned from first surface

R_bottom
= route returned after entering coating and reflecting from second boundary

Delta_phi
= phase difference between return routes
```

Then:

```text
R_total depends on R_top + R_bottom + phase relation.
```

AMS description:

```text
thin-film interference
= route recombination with controlled phase.
```

## Quarter-Wave Antireflection Coating

Conventional design:

```text
optical thickness = lambda_0 / 4
d = lambda_0 / (4 n_coating)
```

Ideal coating index:

```text
n_coating = sqrt(n_air * n_substrate)
```

At design wavelength:

```text
reflections from top and bottom coating boundaries cancel
```

AMS route interpretation:

```text
AR coating creates a deliberate second return route
that cancels the first return route.
```

Route effect:

```text
uncoated glass:
R_return nonzero

quarter-wave AR:
R_top + R_bottom -> cancellation
=> T_route increases
```

AMS classification:

```text
route: R1 transmission enhanced
return route: suppressed by phase cancellation
obstruction: O1 controlled phase gate
dominance: D1
grade: G_A at design wavelength
```

Limitation:

```text
single-layer AR works best near one wavelength and angle.
Broadband AR requires multiple layers.
```

## Protected Aluminium Mirror

Clean aluminium:

```text
air -> Al
```

Real protected aluminium:

```text
air -> MgF2 / LiF / AlF3 or other protective layer -> Al
```

Source-supported role:

```text
Al has high intrinsic reflectance.
Al must be protected from oxygen exposure to avoid Al2O3 formation.
Fluoride layers can protect and preserve or improve UV/FUV reflectance.
Overcoats can introduce residual absorption.
```

AMS route interpretation:

```text
protective coating
=> controlled overlayer gate
=> preserves metal return route
=> reduces uncontrolled oxide route
```

Route profile:

```text
primary_route: R1_return from Al
coating_route: R1/R3 gate
loss_route: R5 if overcoat absorbs
obstruction: O1/O2
dominance: D1/D4
grade: G_A/G_B depending wavelength and coating
```

Uncontrolled oxide:

```text
air -> Al2O3 -> Al
```

AMS:

```text
oxide layer changes phase, absorption, and boundary compatibility.
```

Protected aluminium is therefore:

```text
not bare metal
but engineered terminal-layer return.
```

## Protected Silver Mirror

Clean silver:

```text
air -> Ag
=> very high visible/near-IR R1_return
```

Problem:

```text
silver tarnishes, especially with sulfur exposure.
```

Protected silver:

```text
air -> dielectric overcoat -> Ag
```

AMS route interpretation:

```text
protective dielectric
=> preserves Ag return field
=> adds controlled phase/filter layer
=> slows uncontrolled tarnish route
```

Route profile:

```text
primary_route: R1_return
coating_route: controlled R3 phase gate
loss_route: R5 if coating absorbs or tarnish penetrates
dominance: D1/D4
grade: G_A when coating is well matched
```

Tarnished silver:

```text
air -> Ag2S / contamination -> Ag
```

AMS:

```text
tarnish is an uncontrolled absorbing/filtering overlayer.
```

Route result:

```text
R1_return decreases
R5 absorption increases
R6 scatter may increase
```

## Oxidised Copper

Clean copper:

```text
red/orange-biased metal return
```

Oxidised copper:

```text
air -> copper oxide / patina -> Cu
```

AMS route interpretation:

```text
oxide/patina layer becomes dominant colour/filter route.
```

Route profile:

```text
primary_route: R3/R5 overlayer filter
secondary_route: R1_return from Cu
scattering_route: R6 if rough or granular
dominance: D4
grade: G_B/G_C
```

Interpretation:

The copper surface is no longer simply a copper optical case. It is a copper-plus-oxide stack.

## Rusted Iron

Clean polished iron:

```text
air -> Fe
=> moderate R1_return
```

Rusted iron:

```text
air -> hydrated iron oxide / rough rust layer -> Fe
```

AMS route interpretation:

```text
rust creates a thick, rough, absorbing, scattering terminal field.
```

Route profile:

```text
primary_route: R5/R6
secondary_route: weak R1_return from underlying metal
obstruction: O3/O6
dominance: D3/D4
grade: G_C/G_D
```

Interpretation:

The metal return route is masked by an oxide-fragmentation field.

## Dielectric Antireflection on Glass

Uncoated fused silica:

```text
air -> SiO2
R ~= 3.5 percent per clean surface at normal visible incidence
```

AR-coated fused silica:

```text
air -> AR layer -> SiO2
```

AMS route interpretation:

```text
AR layer intentionally creates a second route-return component
whose phase cancels the first route-return component.
```

Route profile:

```text
primary_route: T/R1 through-route
suppressed_route: R_return
obstruction: O1 controlled cancellation
dominance: D1
grade: G_A at design wavelength
```

Broadband AR:

```text
multiple layers
=> multiple route-return components
=> wider cancellation band
```

## Multilayer Route Classes

### MLC1: Protective Return-Preserving Layer

Examples:

```text
protected silver
protected aluminium
```

AMS:

```text
overlayer preserves metal route by blocking chemical degradation.
```

Risk:

```text
overlayer absorption or phase mismatch
```

### MLC2: Antireflection Cancellation Layer

Examples:

```text
MgF2 on glass
single-layer AR
multilayer broadband AR
```

AMS:

```text
engineered route-return cancellation.
```

Risk:

```text
narrowband performance, angle sensitivity, polarisation effects
```

### MLC3: Uncontrolled Oxide/Tarnish Filter

Examples:

```text
tarnished silver
oxidised copper
rusted iron
uncontrolled Al2O3
```

AMS:

```text
accidental overlayer creates absorption/scattering/filter route.
```

Risk:

```text
lower specular reflectance, colour shift, roughness, incoherence
```

### MLC4: Enhanced Reflector Stack

Examples:

```text
dielectric-enhanced metal mirrors
high-reflector multilayers
UV/FUV protected Al systems
```

AMS:

```text
multiple controlled return routes recombine constructively.
```

Risk:

```text
coating absorption, layer instability, bandwidth limits
```

## Route Equation Sketch

For a stack with layers:

```text
0 -> 1 -> 2 -> ... -> N
```

Each layer has:

```text
n_i(lambda)
k_i(lambda)
d_i
theta_i
```

Phase delay in layer `i`:

```text
phi_i = (2 pi / lambda) * n_i * d_i * cos(theta_i)
```

Round-trip phase contribution:

```text
Delta_i = 2 phi_i
```

AMS route recombination:

```text
R_stack(lambda)
= coherent sum of partial return routes
modified by absorption, scattering, and roughness penalties.
```

Diagnostic AMS form:

```text
R_stack_AMS
= R_interference(lambda)
  * Q_stack
  * (1 - D_abs - D_scat - D_rough)
```

Transmission:

```text
T_stack_AMS
= T_interference(lambda)
  * J_trans_stack
  * Q_stack
  * (1 - D_abs - D_scat)
```

Absorption/scatter:

```text
A_stack + S_stack
= 1 - R_stack - T_stack
```

## Score Assessment

Optical multilayer / oxide / coating route model:

```text
score: 8/10
confidence: moderate
```

Reason:

This is a necessary and useful bridge because:

- it explains coatings as engineered route gates
- it explains tarnish/oxide/rust as uncontrolled terminal layers
- it connects AR coatings to route-return cancellation
- it connects protected metal mirrors to route preservation
- it prepares the model for real optical components

Limitations:

- no transfer-matrix calculation yet
- no numeric coating examples yet
- no oxide optical constants imported
- no roughness/scattering calibration
- no specific protected-silver or protected-aluminium stack simulated

## Effect on Optical Master Model

Current optical route master score:

```text
8.5/10
```

Updated pressure:

```text
retain 8.5/10
confidence strengthened in real-surface applicability
```

Do not move to 9 yet because the multilayer model remains schematic and lacks numeric transfer-matrix cases.

## Next Artifact

The next useful artifact should be:

```text
ams-optical-transfer-matrix-minimal-worked-example-v1.md
```

Purpose:

Create a minimal numeric worked example:

- uncoated air -> glass
- single-layer quarter-wave AR coating on glass
- protected aluminium as air -> MgF2 -> Al
- compare route-return values
- identify phase cancellation and overlayer absorption terms

This will turn the multilayer route model into an actual calculable benchmark.
