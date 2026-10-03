# AMS Optical Route Master Summary v1

## Purpose

This summary consolidates the optical route work into one readable model.

It brings together:

- fused silica transmission
- Fresnel/refraction route equations
- metallic reflection
- metal-specific optical comparison
- interface variables
- vorton interpretation
- evidence status
- remaining modelling gaps

This document is the current bridge between the optical mechanism work and the broader AMS substrate theory.

## Source Artifacts Consolidated

```text
ams-fused-silica-optical-route-map-v1.md
ams-fresnel-refraction-route-equation-sketch-v1.md
ams-metallic-reflection-route-equation-sketch-v1.md
ams-copper-silver-gold-metal-optics-comparison-v1.md
```

Related prior interface artifacts:

```text
ams-interface-formalisation-sketch-v1.md
ams-formalised-case-library-v1.md
ams-expanded-library-scoreboard-v1.md
ams-entry-exit-interface-cases-v1.md
ams-exit-geometry-study-v1.md
ams-release-failure-discriminator-table-v1.md
ams-terminal-layer-depth-and-loop-geometry-v1.md
```

## The Central Optical Contrast

```text
glass admits and delays.
metal rejects and returns.
```

Expanded:

```text
fused silica
=> coherent dielectric through-route
=> refraction, transmission, low absorption in compatible windows

metal
=> conductive surface return-route
=> high reflection, shallow penetration, skin-depth absorption
```

This is now the simplest AMS answer to the paired optical questions:

```text
How does light travel through glass?
How does light reflect off metal?
```

## Established Physics Layer

The following pieces are established optics and are not AMS speculation:

```text
Snell's law
Fresnel reflection and transmission coefficients
complex refractive index N = n + i k for metals and absorbing media
skin depth relation to extinction coefficient
wavelength-dependent refractive index
absorption bands from impurities or vibrational modes
plasma-frequency behaviour of metals
interband transitions contributing to metal colour
surface roughness increasing diffuse scattering
oxide/tarnish changing metal reflectance
```

AMS uses these as constraints.

It does not replace them.

## AMS Interpretation Layer

AMS translates the established optical physics into route language:

```text
reflection
=> route-return fraction

transmission
=> route-continuation fraction

refraction
=> coherent route delay and boundary reseating

absorption
=> route capture into R5/O3 loss

scattering
=> route fragmentation into R6/O6 loss

surface roughness
=> terminal-layer route disorder

oxide/tarnish
=> overlayer gate or filter before the primary material response

defect state
=> local route trap or leakage path
```

## Interface Variables

Current interface variable set:

```text
B_in
= admission capacity

B_out
= release capacity

J_bound
= immediate boundary coupling

J_trans
= through-layer transition continuity

Q_coh
= coherence preservation

D
= defect burden

I_comp
= total interface compatibility
```

First-order compatibility sketch:

```text
I_comp = B_in * B_out * J_bound * J_trans * Q_coh * (1 - D)
```

For clean Fresnel-type dielectric interfaces:

```text
T_AMS ~= T_Fresnel * J_trans * Q_coh * (1 - D)
```

For real interfaces:

```text
R + T + A + S = 1
```

where:

```text
R = returned route
T = transmitted route
A = absorbed route
S = scattered route
```

AMS route mapping:

```text
R => R1_return or R3 block-return
T => R1/R2 continuation
A => R5/O3 capture
S => R6/O6 fragmentation
```

## Fused Silica Route Model

Fused silica:

```text
SiO2 amorphous network
high purity possible
low metallic impurity burden possible
broad UV-visible-near IR transmission depending grade
OH and Si-O vibrational absorption bands
surface reflection from refractive-index contrast
```

AMS route profile:

```text
primary_route: R1 through-route
secondary_route: R2 polarisation/refractive delay
loss_routes: R5 absorption, R6 scattering
obstruction: O1 ordered delay, O3 absorption, O6 scatter
dominance: D1 when clean and wavelength-compatible
grade: G_A in good optical window
```

Core AMS description:

```text
fused silica transmits light
because its Si-O closure field supports coherent optical handoff
without converting most of the route into absorption or scattering.
```

Normal-incidence example:

```text
air n ~= 1.00
fused silica n ~= 1.46

R ~= ((1.00 - 1.46) / (1.00 + 1.46))^2
R ~= 0.035
```

Interpretation:

```text
about 3.5 percent reflected per clean uncoated surface
```

AMS reading:

```text
even a clean glass surface has route-return because delay contrast is real.
```

## Glass Loss Routes

### OH Absorption

Conventional:

```text
OH groups create near-infrared absorption bands.
```

AMS:

```text
OH group
=> wavelength-specific R5/O3 absorption loop
```

### Metallic Impurities

Conventional:

```text
metallic ions increase UV/visible absorption and can reduce optical quality.
```

AMS:

```text
metal impurity
=> defect-state capture route
=> R5/O3
```

### Oxygen-Deficiency Defects

Conventional:

```text
oxygen-deficiency centers can increase UV absorption, luminescence, and laser damage sensitivity.
```

AMS:

```text
oxygen-deficiency center
=> route trap
=> R5/O3
=> possible damage amplification
```

### Rough Surface

Conventional:

```text
roughness increases diffuse scattering.
```

AMS:

```text
rough terminal layer
=> R6/O6 fragmentation
```

## Metal Route Model

Metals:

```text
complex refractive index N = n + i k
large extinction coefficient in visible/IR for many metals
conduction-electron surface response
high reflectance below plasma frequency
shallow penetration depth
surface-dependent specular quality
```

Normal-incidence complex reflectance:

```text
R = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)
```

Skin depth:

```text
delta = lambda / (4 pi k)
```

AMS route profile:

```text
primary_route: R1_return
secondary_route: shallow R5 absorption
blocked_route: deep R1/R2 transmission
obstruction: O2 against deep entry
dominance: D1_return for polished metal
grade: G_A when smooth, clean, and spectrally favourable
```

Core AMS description:

```text
metal reflects light
because the incident optical route drives a collective electron response
that creates a strong return route while admitting only shallow lossy penetration.
```

Example:

```text
n = 0.14
k = 4.0

R ~= 0.968
```

Interpretation:

```text
about 96.8 percent reflected at clean normal incidence
```

AMS contrast:

```text
air -> fused silica
=> about 3.5 percent return per clean surface

air -> high-k polished metal
=> about 97 percent return
```

## Metal-Specific Route Filters

### Silver

```text
route: broad neutral R1_return
loss: tarnish / UV interband onset
AMS role: strongest clean visible mirror case
score: 8.5
```

### Aluminium

```text
route: strong UV-visible R1_return
loss: oxide/coating gate
AMS role: UV-capable coated reflector
score: 8
```

### Gold

```text
route: red/IR R1_return
loss: blue/violet R5 absorption
AMS role: yellow spectral route filter
score: 8.5
```

### Copper

```text
route: red/orange biased R1_return
loss: shorter-wavelength R5 absorption, oxide/patina
AMS role: red/orange spectral route filter
score: 8
```

### Iron

```text
route: R1_return when polished
loss: oxide/rust R5/R6 dominance
AMS role: oxidation-sensitive contrast case
score: 7
```

## Vorton Interpretation

### Fused Silica

```text
Si-O network vortons
=> stable local closure
=> repeated polarisation handoff
=> coherent phase delay
=> transmitted optical route
```

Loss:

```text
OH / impurity / oxygen-defect vortons
=> route capture or scattering loops
=> absorption, luminescence, damage, or loss
```

### Metal

```text
conduction-electron surface response
=> collective return vorton field
=> coherent reflection
```

Loss:

```text
electron damping
=> shallow R5 absorption
=> heat

surface roughness
=> R6 fragmented return
=> diffuse scatter

oxide/tarnish
=> overlayer gate/filter
=> colour shift, absorption, reduced specular reflection
```

## Current Score Summary

| Optical artifact | Score | Confidence |
|---|---:|---|
| fused silica optical route map | 9 | high |
| Fresnel/refraction route equation sketch | 8 | moderate |
| metallic reflection route equation sketch | 8 | moderate |
| copper/silver/gold/aluminium/iron comparison | 8 | moderate-high |
| optical route master model | 8.5 | moderate-high |

Master model score:

```text
AMS optical route model: 8.5/10
confidence: moderate-high
```

Reason:

The model now explains both glass transmission and metal reflection with the same route vocabulary while preserving established optical equations.

## What Is Strong

```text
1. Glass/metal contrast is clear.
2. Fused silica is strongly mapped.
3. Fresnel reflection/transmission has an AMS compatibility overlay.
4. Metals are separated into return, shallow absorption, and diffuse scatter routes.
5. Metal colour is mapped as spectral route filtering.
6. Surface condition is treated as terminal-layer route structure, not cosmetic detail.
```

## What Remains Weak

```text
1. AMS variables are not empirically calibrated.
2. Fresnel equations are not yet derived from AMS primitives.
3. Polarisation-specific route geometry is underdeveloped.
4. Complex-index metal behaviour lacks numerical tables.
5. Thin-film interference and protective coatings are not modelled.
6. Plasmonic behaviour is not modelled.
7. Rayleigh scattering and density fluctuations need geometry.
8. Nonlinear optics and laser damage need separate treatment.
```

## Experimental / Modelling Programme

Next modelling targets should be:

```text
1. Build a numeric table for air -> fused silica at common wavelengths and angles.
2. Build a numeric table for air -> Ag/Au/Cu/Al/Fe at 400, 550, 700, and 1000 nm.
3. Add roughness and oxide/tarnish penalty factors.
4. Model coated aluminium and protected silver as multilayer routes.
5. Map Brewster angle and total internal reflection into route geometry.
6. Compare predicted route classes with real reflectance/transmission data.
```

## Recommended Next Artifact

The next useful artifact should be:

```text
ams-optical-numeric-benchmark-table-v1.md
```

Purpose:

Create a small benchmark table with actual values:

- air -> fused silica reflectance at normal incidence
- air -> fused silica at 30, 45, 60 degrees for s/p polarisations
- air -> silver/gold/copper/aluminium normal-incidence reflectance using representative `n,k`
- approximate skin depth for each metal
- route class assigned to each case

This will move the optical model from qualitative mechanism into testable numeric comparisons.
