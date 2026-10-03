# AMS Optical Master Score Recalibration v1

## Purpose

This recalibration records the optical route model score move from:

```text
8.5/10
```

to:

```text
9/10
```

It consolidates the completed optical workstream:

- `ams-fused-silica-optical-route-map-v1.md`
- `ams-fresnel-refraction-route-equation-sketch-v1.md`
- `ams-metallic-reflection-route-equation-sketch-v1.md`
- `ams-copper-silver-gold-metal-optics-comparison-v1.md`
- `ams-optical-route-master-summary-v1.md`
- `ams-optical-numeric-benchmark-table-v1.md`
- `ams-optical-colour-and-spectrum-route-table-v1.md`
- `ams-optical-multilayer-oxide-coating-route-model-v1.md`
- `ams-optical-transfer-matrix-minimal-worked-example-v1.md`
- `ams-optical-angle-and-polarisation-benchmark-v1.md`

## Previous Score

```text
AMS optical route model: 8.5/10
confidence: moderate-high
pressure: upward
```

Previous rationale:

The model already explained:

- fused silica transmission
- metal reflection
- Fresnel route splitting
- complex-index metal behaviour
- metal colour as spectral filtering
- coatings as route gates

It was held at 8.5 because numerical and angular benchmarks were incomplete.

## New Upgrade Basis

The upgrade to 9 is justified by three additions:

```text
1. numeric reflectance and skin-depth benchmarks
2. minimal transfer-matrix coating examples
3. angle/polarisation Fresnel benchmarks including Brewster and total internal reflection
```

These additions move the optical model from qualitative mechanism to partially calculable structure.

## Evidence Stack

### 1. Fused Silica Transmission

File:

```text
ams-fused-silica-optical-route-map-v1.md
```

Score:

```text
9/10
confidence: high
```

Main result:

```text
fused silica transmits light because its Si-O closure field supports coherent optical handoff without converting most of the route into absorption or scattering.
```

Route:

```text
primary_route: R1 through-route
secondary_route: R2 polarisation/refractive delay
loss_routes: R5 absorption, R6 scattering
dominance: D1 in clean optical windows
```

### 2. Fresnel / Refraction Route Equations

File:

```text
ams-fresnel-refraction-route-equation-sketch-v1.md
```

Score:

```text
8/10
confidence: moderate
```

Main result:

```text
Snell/Fresnel physics can be preserved while interpreting reflection as route return and transmission as route continuation.
```

Key sketch:

```text
T_AMS ~= T_Fresnel * J_trans * Q_coh * (1 - D)
```

### 3. Metallic Reflection

File:

```text
ams-metallic-reflection-route-equation-sketch-v1.md
```

Score:

```text
8/10
confidence: moderate
```

Main result:

```text
metal reflects light because the incident optical route drives a collective electron response that creates a strong return route while admitting only shallow lossy penetration.
```

Key equation:

```text
R = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)
```

### 4. Metal-Specific Colour and Return Routes

File:

```text
ams-copper-silver-gold-metal-optics-comparison-v1.md
```

Score:

```text
8/10
confidence: moderate-high
```

Main result:

```text
metal colour is spectral route filtering.
```

Examples:

```text
silver
=> broad neutral R1_return

gold
=> blue/violet R5 absorption plus yellow/red return

copper
=> short-wavelength absorption plus red/orange return

aluminium
=> broad UV-visible return with oxide/coating gate

iron
=> oxidation-sensitive mixed return/loss
```

### 5. Numeric Optical Benchmarks

File:

```text
ams-optical-numeric-benchmark-table-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main numeric results:

```text
air -> fused silica normal incidence:
R ~= 3.48 percent

Ag at 550 nm:
R ~= 96.7 percent
skin depth ~= 11.0 nm

Al at 550 nm:
R ~= 90.5 percent
skin depth ~= 5.9 nm

Au at 550 nm:
R ~= 76.4 percent
skin depth ~= 18.2 nm

Cu at 550 nm:
R ~= 65.9 percent
skin depth ~= 18.0 nm

Fe at 550 nm:
R ~= 55.3 percent
skin depth ~= 13.3 nm
```

Main result:

```text
glass/metal contrast is now numerically anchored.
```

### 6. Spectral Route Table

File:

```text
ams-optical-colour-and-spectrum-route-table-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main result:

```text
R(lambda) + T(lambda) + A(lambda) + S(lambda) = 1
```

Colour and transparency now depend on wavelength-specific route distribution.

### 7. Multilayer / Oxide / Coating Model

File:

```text
ams-optical-multilayer-oxide-coating-route-model-v1.md
```

Score:

```text
8/10
confidence: moderate
```

Main result:

```text
coatings are engineered terminal-layer route gates.
oxide/tarnish/rust are uncontrolled terminal-layer gates.
```

### 8. Minimal Transfer-Matrix Worked Example

File:

```text
ams-optical-transfer-matrix-minimal-worked-example-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main numeric results:

```text
uncoated air -> glass:
R ~= 4.26 percent

ideal quarter-wave AR on glass:
R ~= 0 percent at design wavelength

MgF2 quarter-wave on glass:
R ~= 1.26 percent

bare Al at 550 nm:
R ~= 90.5 percent

MgF2 quarter-wave on Al at 550 nm:
R ~= 83.3 percent
```

Main result:

```text
coatings can now be treated as calculable route-recombination systems.
```

### 9. Angle and Polarisation Benchmark

File:

```text
ams-optical-angle-and-polarisation-benchmark-v1.md
```

Score:

```text
9/10
confidence: high
```

Main numeric results:

```text
air -> glass Brewster angle:
56.66 deg

glass -> air Brewster angle:
33.34 deg

glass -> air critical angle:
41.14 deg
```

Main AMS result:

```text
Brewster angle
=> p-route return cancellation

total internal reflection
=> ordered release failure
```

## Recalibration Decision

Updated score:

```text
AMS optical route model: 9/10
confidence: moderate-high
```

Reason:

The optical route model now has:

- conceptual coherence
- preserved standard physics
- fused silica transmission mechanism
- metal reflection mechanism
- spectral colour filtering
- normal-incidence numerical benchmarks
- metal skin-depth estimates
- multilayer coating interpretation
- transfer-matrix worked example
- angle/polarisation benchmarks
- Brewster and total-internal-reflection route interpretation

This is enough to move from 8.5 to 9.

## Central Model Statement

The current optical model can be summarised as:

```text
Glass admits and delays.
Metal rejects and returns.
Coatings recombine routes.
Defects capture or fragment routes.
Colour is spectral route filtering.
```

Expanded:

```text
fused silica
=> high T(lambda), low A(lambda), low S(lambda)
=> coherent dielectric through-route

metal
=> high R(lambda), shallow A(lambda), near-zero deep T(lambda)
=> conductive surface return-route

coating
=> controlled route phase and recombination

oxide/tarnish/rust
=> uncontrolled overlayer route filter
```

## Why Not 9.5

Do not move above 9 yet.

Remaining gaps:

```text
1. Full spectral numerical curves for fused silica and metals.
2. Multi-wavelength transfer-matrix coating examples.
3. Angle-dependent coated-surface examples.
4. Roughness and Rayleigh scattering calibration.
5. Oxide/tarnish optical constants and thickness cases.
6. Surface plasmon / nanostructure route modelling.
7. Nonlinear optics and laser damage.
8. Direct vorton geometry diagrams and mathematical topology.
9. Experimental comparison against measured spectra in a structured score table.
```

## Score Log Entry

```text
optical master recalibration v1:

previous_score: 8.5/10
updated_score: 9/10
confidence: moderate-high
pressure: upward but capped below 9.5

reason:
the model now explains and numerically benchmarks glass transmission, metal reflection, colour filtering, coatings, Brewster cancellation, and total internal reflection while preserving established optical equations.
```

## Next Workstream Options

### Option A: Full Spectral Numeric Curves

Artifact:

```text
ams-optical-full-spectrum-numeric-route-curves-v1.md
```

Value:

Would build numerical `R(lambda)`, `T(lambda)`, `A(lambda)` curves for fused silica and metals.

### Option B: Surface Roughness and Scattering

Artifact:

```text
ams-optical-roughness-scattering-route-model-v1.md
```

Value:

Would model polish, frosted glass, matte metal, Rayleigh scatter, and diffuse reflection.

### Option C: Return to Element Families

Artifact:

```text
ams-phosphorus-material-family-entry-v1.md
```

Value:

Would continue the element/material programme into phosphate, ATP, DNA/RNA backbone, membranes, hydroxyapatite, and biological energy structures.

## Recommended Next Artifact

Recommended next:

```text
ams-phosphorus-material-family-entry-v1.md
```

Reason:

The optical route model is now strong enough to pause. Phosphorus is the next highest-value element family because it connects:

- phosphate minerals
- hydroxyapatite
- DNA/RNA backbone
- ATP/energy transfer
- membranes/phospholipids
- biological signalling and regulation
- T1B-to-T1C transition

It will also deepen the already-started calcium/hydroxyapatite and biological-function workstreams.
