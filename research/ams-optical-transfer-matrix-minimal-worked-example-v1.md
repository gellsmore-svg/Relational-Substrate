# AMS Optical Transfer-Matrix Minimal Worked Example v1

## Purpose

This file gives the first minimal numeric multilayer worked example for the AMS optical route model.

It compares:

- uncoated air to glass
- ideal single-layer quarter-wave antireflection coating on glass
- MgF2 single-layer quarter-wave coating on glass
- bare aluminium
- MgF2-overcoated aluminium at the same design wavelength

The purpose is not to design a real optical coating.

The purpose is to show how route-return cancellation and protective-overlayer effects can be made calculable.

## Model Scope

This is a normal-incidence, one-layer transfer-matrix example.

Assumptions:

```text
wavelength: 550 nm
normal incidence
non-magnetic materials
ideal smooth interfaces
no roughness scattering
no graded interlayers
no temperature effects
no manufacturing defects
```

These are intentionally simplified conditions.

## Source Basis

Relevant prior artifacts:

```text
ams-fresnel-refraction-route-equation-sketch-v1.md
ams-metallic-reflection-route-equation-sketch-v1.md
ams-optical-multilayer-oxide-coating-route-model-v1.md
```

External source anchors:

- Physics LibreTexts, "Reflection and Transmission at Boundaries and the Fresnel Equations." https://phys.libretexts.org/Bookshelves/Optics/Physical_Optics_%28Tatum%29/02%3A_Reflection_and_Transmission_at_Boundaries_and_the_Fresnel_Equations
- Laser Focus World, "Thin-film Coatings: Understanding key design principles of antireflection coatings." https://www.laserfocusworld.com/optics/article/16547029/thin-film-coatings-understanding-key-design-principles-of-antireflection-coatings
- NASA Science, "Coated Mirrors Achieve Record-setting Far Ultraviolet Reflectance Levels." https://science.nasa.gov/science-research/science-enabling-technology/technology-highlights/coated-mirrors-achieve-record-setting-far-ultraviolet-reflectance-levels/
- NASA NTRS, "Advanced Al Mirrors Protected with LiF Overcoat to Realize Stable Mirror Coatings for Astronomical Telescopes." https://ntrs.nasa.gov/citations/20230006299

## Transfer-Matrix Setup

For a single layer:

```text
medium 0 -> coating layer 1 -> substrate 2
```

At normal incidence:

```text
n0 = incident index
n1 = coating index
n2 = substrate index
d1 = coating thickness
lambda = vacuum wavelength
```

Phase thickness:

```text
delta = 2 pi n1 d1 / lambda
```

Quarter-wave condition:

```text
n1 d1 = lambda / 4
d1 = lambda / (4 n1)
```

For a single-layer antireflection design:

```text
n1_ideal = sqrt(n0 * n2)
```

At the design wavelength, the two main reflected routes cancel when the index and thickness are ideal.

AMS translation:

```text
top-boundary return route
+ delayed bottom-boundary return route
=> destructive route recombination
=> reduced total return
=> increased through-route
```

## Case 1: Uncoated Air to Glass

Assumptions:

```text
n0 = 1.000
n2 = 1.520
```

Normal-incidence reflectance:

```text
R = ((n0 - n2) / (n0 + n2))^2
R = ((1.000 - 1.520) / (1.000 + 1.520))^2
R = 0.0426
```

Result:

```text
R ~= 4.26 percent
T ~= 95.74 percent
```

AMS route reading:

```text
single clean boundary
=> real route-return from index mismatch
=> most route admitted into glass
```

Route class:

```text
R_return: low-moderate
T_route: high
class: clean dielectric admission
```

## Case 2: Ideal Quarter-Wave AR Layer on Glass

Assumptions:

```text
n0 = 1.000
n2 = 1.520
n1 = sqrt(1.000 * 1.520)
n1 = 1.233
lambda = 550 nm
d1 = lambda / (4 n1)
d1 = 111.5 nm
```

Transfer-matrix result:

```text
R ~= 0.00000000000000000000000000000000017
```

Practically:

```text
R ~= 0 percent at design wavelength
```

AMS route reading:

```text
engineered terminal layer
=> top return and bottom return cancel
=> route-return suppressed
=> through-route maximized
```

Route class:

```text
R_return: cancelled
T_route: maximized
class: ideal route-return cancellation
```

Important note:

```text
This is an ideal mathematical case.
Real coating materials, finite bandwidth, angle, polarisation, absorption, roughness, and manufacturing tolerances prevent perfect cancellation.
```

## Case 3: MgF2 Quarter-Wave Layer on Glass

Assumptions:

```text
n0 = 1.000
n1 = 1.380
n2 = 1.520
lambda = 550 nm
d1 = lambda / (4 n1)
d1 = 99.6 nm
```

Transfer-matrix result:

```text
R ~= 0.0126
```

Result:

```text
R ~= 1.26 percent
T ~= 98.74 percent
```

AMS route reading:

```text
MgF2 coating partially cancels return route,
but its index is not the ideal sqrt(1.52) value.
```

Route class:

```text
R_return: reduced
T_route: improved
class: practical single-layer AR
```

Comparison:

```text
uncoated glass: R ~= 4.26 percent
MgF2-coated glass: R ~= 1.26 percent
ideal AR-coated glass: R ~= 0 percent
```

AMS interpretation:

```text
coating success is route recombination quality.
```

## Case 4: Bare Aluminium at 550 nm

Representative optical constants:

```text
N_Al = n + i k
n = 1.44
k = 7.38
```

Normal-incidence reflectance:

```text
R = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)
R ~= 0.905
```

Result:

```text
R ~= 90.5 percent
```

AMS route reading:

```text
metallic surface creates strong return route.
deep route is blocked by high extinction.
```

Route class:

```text
R1_return
O2 deep-entry block
D1_return
```

## Case 5: MgF2 Quarter-Wave Layer on Aluminium at 550 nm

Assumptions:

```text
n0 = 1.000
n1 = 1.380
N_Al = 1.44 + 7.38i
lambda = 550 nm
d1 = 99.6 nm
```

Transfer-matrix result:

```text
R ~= 0.833
```

Result:

```text
R ~= 83.3 percent
```

AMS route reading:

```text
the MgF2 layer protects or gates the metal route,
but at this visible design condition it reduces reflectance compared with bare Al in the simplified model.
```

This is important:

```text
protective coating
!= automatically higher reflectance at every wavelength.
```

A protective overcoat may be chosen to:

- prevent oxidation
- improve lifetime
- preserve UV/FUV performance
- allow cleaning
- tune reflectance in a selected band

even if a simple one-layer visible calculation shows reduced reflectance.

Route class:

```text
R1_return through coating gate
R3 phase/overlayer gate
D4 coating-metal competition
```

## Summary Table

| Case | Stack | Reflectance at 550 nm | AMS route result |
|---|---|---:|---|
| uncoated glass | air -> glass | 4.26% | clean dielectric admission with small return |
| ideal AR glass | air -> ideal QW layer -> glass | ~0% | ideal route-return cancellation |
| MgF2 AR glass | air -> MgF2 -> glass | 1.26% | practical partial return cancellation |
| bare aluminium | air -> Al | 90.5% | strong metal return route |
| MgF2 on aluminium | air -> MgF2 -> Al | 83.3% | protected/gated metal return, not automatically higher |

## AMS Findings

### Finding 1: AR Coating Is Route Cancellation

The ideal AR case demonstrates:

```text
thin film can reduce reflectance not by absorbing it
but by causing return routes to cancel.
```

AMS route statement:

```text
R_top + R_bottom -> 0
```

### Finding 2: Real Coating Index Matters

MgF2 on glass reduces reflectance:

```text
4.26 percent -> 1.26 percent
```

but does not eliminate it because:

```text
n_MgF2 = 1.38
ideal n = 1.233
```

AMS route statement:

```text
non-ideal gate index
=> incomplete route cancellation
```

### Finding 3: Protective Coating Is Not Always Reflectance Boosting

MgF2 on aluminium at 550 nm in this toy model:

```text
90.5 percent -> 83.3 percent
```

AMS route statement:

```text
overlayer gate can preserve material chemically
while reducing optical return at a given wavelength.
```

This supports the distinction between:

```text
protective route gate
and
enhancing route gate
```

### Finding 4: Stack Behaviour Cannot Be Reduced to the Final Material

Bare aluminium and MgF2-coated aluminium are different optical route systems.

AMS:

```text
air -> Al
!=
air -> MgF2 -> Al
```

The terminal layer is part of the optical object.

## Route Class Updates

### Single Clean Dielectric Interface

```text
class: D-1
route: R1/R2 admission
return: low Fresnel return
```

### Ideal AR Stack

```text
class: D-AR-ideal
route: R1 transmission
return: cancelled by phase recombination
```

### Practical AR Stack

```text
class: D-AR-practical
route: R1 transmission improved
return: partially cancelled
```

### Bare Metal

```text
class: M-return
route: R1_return
entry: shallow R5 absorption only
```

### Protected Metal

```text
class: M-coated
route: R1_return through overlayer gate
secondary: R3 phase gate, R5 absorption if coating lossy
```

## Score Assessment

Optical transfer-matrix minimal worked example:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

This strengthens the optical model by:

- making coating-route cancellation numeric
- distinguishing ideal vs practical AR
- showing coating index and thickness matter
- showing protected metal is not automatically higher reflectance
- tying stack behaviour to AMS route classes

Limitations:

- normal incidence only
- one wavelength only
- one coating layer only
- no absorption in dielectric coating
- no roughness
- no oxide growth kinetics
- no real protected-silver or enhanced-aluminium design

## Effect on Optical Master Model

Previous optical master score:

```text
8.5/10
```

Updated pressure:

```text
strong upward pressure toward 9
but retain 8.5/10
```

Reason:

The model now has real calculations for both dielectric AR and coated metal behaviour. It should move to 9 only after at least one multi-wavelength or angle-dependent transfer-matrix case is added.

## Next Artifact

The next useful artifact should be:

```text
ams-optical-angle-and-polarisation-benchmark-v1.md
```

Purpose:

Extend the numeric work to:

- Brewster angle
- total internal reflection
- `s` vs `p` reflection curves
- glass-to-air exit failure
- route-return cancellation by polarisation
- comparison with the prior `glass -> air` exit geometry work
