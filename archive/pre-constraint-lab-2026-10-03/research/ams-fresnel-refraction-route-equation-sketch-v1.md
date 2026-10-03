# AMS Fresnel Refraction Route Equation Sketch v1

## Purpose

This file sketches a mathematical bridge between conventional optical boundary physics and AMS route variables.

It follows:

```text
ams-fused-silica-optical-route-map-v1.md
```

The target is to translate:

- refractive index
- Snell refraction
- Fresnel reflection
- Fresnel transmission
- incidence angle
- polarisation
- surface defect burden

into AMS variables:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`
- `I_comp`

This is a sketch, not a final optical theory.

## Source Basis

Initial source anchors:

- HyperPhysics, "Fresnel's Equations." https://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/freseq.html
- HyperPhysics, "External Reflection: Fresnel's Equations." https://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/reflex.html
- Physics LibreTexts, "Reflection and Transmission at Boundaries and the Fresnel Equations." https://phys.libretexts.org/Bookshelves/Optics/Physical_Optics_%28Tatum%29/02%3A_Reflection_and_Transmission_at_Boundaries_and_the_Fresnel_Equations
- PhysLab, "Reflection, Transmission and Fresnel Coefficients." https://physlab.org/experiment/reflection-transmission-and-fresnel-coefficients/
- Wolfram ScienceWorld, "Fresnel Equations." https://scienceworld.wolfram.com/physics/FresnelEquations.html

## Established Physics Baseline

At an interface between two transparent dielectric media:

```text
medium 1 refractive index: n1
medium 2 refractive index: n2
incident angle: theta_i
transmitted angle: theta_t
```

Snell's law:

```text
n1 sin(theta_i) = n2 sin(theta_t)
```

Fresnel amplitude reflection coefficients:

```text
r_s = (n1 cos(theta_i) - n2 cos(theta_t))
      / (n1 cos(theta_i) + n2 cos(theta_t))

r_p = (n2 cos(theta_i) - n1 cos(theta_t))
      / (n2 cos(theta_i) + n1 cos(theta_t))
```

Fresnel amplitude transmission coefficients:

```text
t_s = (2 n1 cos(theta_i))
      / (n1 cos(theta_i) + n2 cos(theta_t))

t_p = (2 n1 cos(theta_i))
      / (n2 cos(theta_i) + n1 cos(theta_t))
```

Reflectance:

```text
R_s = |r_s|^2
R_p = |r_p|^2
```

Transmittance requires the flux correction:

```text
T_s = (n2 cos(theta_t) / n1 cos(theta_i)) |t_s|^2
T_p = (n2 cos(theta_t) / n1 cos(theta_i)) |t_p|^2
```

For non-absorbing media:

```text
R + T = 1
```

at a clean ideal interface.

## AMS Interpretation Layer

AMS does not replace the Fresnel equations.

AMS interprets what the equations mean in route language.

Conventional statement:

```text
part of the electromagnetic wave reflects
part transmits
the transmitted part refracts according to index contrast
```

AMS statement:

```text
the boundary divides the incident route into:

reflected return route
transmitted reseated route

according to boundary compatibility, phase-delay contrast, angle, polarisation, and defect burden.
```

## Variable Translation

### Refractive Index

Conventional:

```text
n = c / v_phase
```

AMS:

```text
n measures coherent route delay in the medium.
```

Route interpretation:

```text
higher n
=> stronger polarisation-coupled delay
=> more route reseating per unit optical path
```

Use:

```text
n1, n2
=> delay contrast across interface
```

### Incidence Angle

Conventional:

```text
theta_i controls path geometry and boundary field matching.
```

AMS:

```text
theta_i controls route-entry stress at the terminal layer.
```

Route interpretation:

```text
normal incidence
=> lowest directional reseating stress

oblique incidence
=> stronger lateral handoff demand

near critical / grazing conditions
=> high exit or admission stress
```

### Polarisation

Conventional:

```text
s and p polarisations have different Fresnel coefficients.
```

AMS:

```text
polarisation selects a different boundary-coupling geometry.
```

Route interpretation:

```text
s-polarisation
=> transverse electric route couples one way to the interface

p-polarisation
=> electric field has interface-plane relation that can reach Brewster cancellation
```

### Reflectance

Conventional:

```text
R = reflected power fraction
```

AMS:

```text
R = route-return fraction
```

Interpretation:

```text
high R
=> incident route poorly admitted into medium 2
or
boundary conditions favour return route
```

### Transmittance

Conventional:

```text
T = transmitted power fraction
```

AMS:

```text
T = route-admission and through-boundary continuation fraction
```

Interpretation:

```text
high T
=> boundary route compatibility high
and
bulk through-route remains available
```

## Interface Variables

AMS interface variable definitions:

```text
B_in
= admission capacity from medium 1 into terminal layer / medium 2

B_out
= release capacity from terminal layer / medium 1 into medium 2

J_bound
= immediate boundary coupling quality

J_trans
= through-layer transition continuity

Q_coh
= coherence preservation through the boundary and near-surface layer

D
= defect burden / scattering / absorption / roughness penalty

I_comp
= total interface compatibility
```

## First-Order AMS Interface Compatibility

Proposed first-order compatibility sketch:

```text
I_comp = B_in * B_out * J_bound * J_trans * Q_coh * (1 - D)
```

where each variable is normalised:

```text
0 <= variable <= 1
```

This is not a replacement for Fresnel transmission. It is a diagnostic layer over physical transmission.

Interpretation:

```text
I_comp near 1
=> clean, coherent, high-quality interface

I_comp near 0
=> defective, absorbing, rough, or route-incompatible interface
```

## Linking Fresnel to AMS Variables

For a clean ideal dielectric interface:

```text
D ~= 0
Q_coh ~= 1
J_bound determined mostly by n1, n2, theta_i, polarisation
J_trans high if medium 2 is transparent at wavelength
```

Therefore:

```text
T_Fresnel
approximately expresses the ideal boundary route-admission fraction.
```

AMS transmission estimate:

```text
T_AMS = T_Fresnel * I_comp_nonideal
```

where:

```text
I_comp_nonideal = J_trans * Q_coh * (1 - D)
```

for cases where Fresnel already handles the clean boundary split.

Alternative full diagnostic form:

```text
T_AMS_diag = T_Fresnel * B_in * B_out * J_trans * Q_coh * (1 - D)
```

Use the full diagnostic form when surface admission/release defects are not already captured by the refractive-index boundary model.

## Reflection Estimate

For a clean non-absorbing interface:

```text
R_Fresnel + T_Fresnel = 1
```

For a real interface:

```text
R + T + A + S = 1
```

where:

```text
A = absorption route
S = scattering route
```

AMS mapping:

```text
R
=> route-return fraction

T
=> route-continuation fraction

A
=> R5/O3 absorption capture

S
=> R6/O6 scattering fragmentation
```

Proposed real-interface sketch:

```text
T_real = T_Fresnel * Q_coh * (1 - D_abs - D_scat)

R_real = R_Fresnel * J_bound + R_diffuse

A_real = D_abs * C_abs

S_real = D_scat * C_scat
```

This needs later refinement.

The important AMS move is:

```text
loss is not simply missing transmission.
loss splits into return, absorption, and scattering route classes.
```

## Normal Incidence Simplification

At normal incidence:

```text
theta_i = theta_t = 0
```

For non-magnetic dielectric media, reflectance simplifies to:

```text
R = ((n1 - n2) / (n1 + n2))^2
```

Transmission:

```text
T = 1 - R
```

for ideal non-absorbing media.

AMS interpretation:

```text
normal incidence reflection
=> pure delay-contrast return fraction
```

Example:

```text
air n1 ~= 1.00
fused silica n2 ~= 1.46 at visible wavelengths
```

Approximate normal-incidence reflection per clean surface:

```text
R ~= ((1.00 - 1.46) / (1.00 + 1.46))^2
R ~= 0.035
```

So:

```text
about 3.5 percent reflected per uncoated clean surface
```

AMS reading:

```text
even a clean high-quality surface returns some route because delay contrast is real.
```

## Brewster Angle Interpretation

Conventional:

```text
for p-polarised light, reflection can vanish at Brewster angle
tan(theta_B) = n2 / n1
```

for light entering from medium 1 into medium 2.

AMS interpretation:

```text
p-polarised boundary geometry reaches a route-cancellation condition for the return route.
```

At Brewster angle:

```text
R_p ~= 0
T_p high
```

AMS reading:

```text
boundary coupling geometry suppresses the reflected return route.
```

This is a useful discriminator because it shows that reflection is not merely "surface resistance." It is geometry and polarisation dependent.

## Total Internal Reflection Interpretation

Conventional:

```text
when n1 > n2 and theta_i exceeds critical angle,
no propagating transmitted ray exists in medium 2.
```

AMS interpretation:

```text
exit route cannot be admitted into medium 2 as a propagating route.
```

Route profile:

```text
B_out -> 0 for propagating transmission
R return route -> high
near-boundary evanescent field remains as non-propagating route pressure
```

This maps cleanly to prior exit-geometry work:

```text
glass -> air
at high angle
=> release failure
=> ordered return
```

## Defect and Roughness Corrections

A clean Fresnel interface assumes a smooth, ideal boundary.

AMS requires additional penalties for real materials:

```text
D_abs
= absorption defect burden

D_scat
= scattering/roughness burden

D_phase
= phase coherence disruption
```

Expanded:

```text
D_total = clamp(D_abs + D_scat + D_phase - overlap_terms, 0, 1)
```

Then:

```text
Q_coh_eff = Q_coh * (1 - D_phase)

T_eff = T_Fresnel * J_trans * Q_coh_eff * (1 - D_abs - D_scat)
```

This is still schematic.

It is useful because it separates:

```text
index mismatch reflection
from
material loss
from
surface scattering
```

## Fused Silica Case

For polished fused silica in visible light:

```text
n1 air ~= 1.00
n2 fused silica ~= 1.46
D_abs low
D_scat low
Q_coh high
J_trans high
```

Expected:

```text
Fresnel reflection per surface around 3.5 percent at normal incidence
bulk transmission high
loss dominated by surface reflection unless antireflection coated
```

AMS variable assignment:

```text
B_in: high
B_out: high
J_bound: high
J_trans: high
Q_coh: high
D: low
I_comp: high
```

For OH-rich fused silica at an OH absorption band:

```text
D_abs increases
J_trans decreases
Q_coh remains high outside the absorption route
```

AMS:

```text
same boundary
different wavelength route viability
```

For rough fused silica:

```text
D_scat increases
B_in/B_out decrease
R_diffuse and S increase
```

AMS:

```text
terminal-layer route breaks before bulk route fails.
```

## Metals Contrast

For metals, the refractive index is complex:

```text
N = n + i k
```

where:

```text
k = extinction coefficient
```

Conventional:

```text
large k often produces high reflectance and shallow penetration.
```

AMS:

```text
metal surface strongly rejects coherent dielectric admission
and converts attempted entry into return route plus shallow absorption route.
```

Route profile:

```text
air -> polished metal
=> high R return route
=> low transmitted through-route
=> shallow loss channel
```

This connects directly to the original second optical question:

```text
How does light reflect off metal from a vorton perspective?
```

That should be handled in a separate metallic-reflection equation sketch.

## Score Assessment

Fresnel/refraction AMS equation sketch:

```text
score: 8/10
confidence: moderate
```

Reason:

This is a useful first mathematical bridge because:

- it preserves established Snell/Fresnel physics
- it maps reflection/transmission into route-return and route-continuation fractions
- it introduces nonideal AMS penalties for absorption, scattering, roughness, and phase disruption
- it connects directly to fused silica and prior interface work

Limitations:

- variables are not yet empirically calibrated
- defect penalties are schematic
- polarisation-specific AMS geometry is not developed
- complex refractive index for metals is only introduced, not modelled
- vorton-level microgeometry remains interpretive rather than quantitative

## Next Artifact

The next useful artifact should be:

```text
ams-metallic-reflection-route-equation-sketch-v1.md
```

Purpose:

Use complex refractive index and surface electron response to map:

- high metal reflectance
- shallow penetration depth
- absorption loss
- polished vs oxidised surface difference
- why metals reflect differently from glass
- `air -> polished metal`
- `air -> oxidised metal`

This completes the direct pair:

```text
light through glass
light off metal
```
