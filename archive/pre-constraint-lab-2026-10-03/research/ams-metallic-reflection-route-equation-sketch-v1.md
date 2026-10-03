# AMS Metallic Reflection Route Equation Sketch v1

## Purpose

This file sketches a mathematical and mechanistic AMS account of metallic reflection.

It follows:

```text
ams-fresnel-refraction-route-equation-sketch-v1.md
```

and completes the direct optical pair:

```text
light through glass
light off metal
```

The core contrast is:

```text
fused silica
=> dielectric through-route with coherent delay

metal
=> conductive surface response with strong return route and shallow absorption
```

## Source Basis

Initial source anchors:

- Engineering LibreTexts, "Metallic Reflection." https://eng.libretexts.org/Workbench/Materials_Science_for_Electrical_Engineering/06%3A_Thermal_Optical/6.01%3A_Optical_Properties/6.1.02%3A_Metallic_Reflection
- Engineering LibreTexts, "Metallic Reflection: Reflectance and conductivity." https://eng.libretexts.org/Workbench/Materials_Science_for_Electrical_Engineering/06%3A_Thermal_Optical/6.01%3A_Optical_Properties/6.1.02%3A_Metallic_Reflection
- ScienceDirect Topics, "Plasma Frequency." https://www.sciencedirect.com/topics/physics-and-astronomy/plasma-frequency
- ScienceDirect, "Optical Properties of Thin Metal Films." https://doi.org/10.1016/S0079-6638(08)70477-3
- Naval Postgraduate School course note, "Free Electron Refraction." https://www.oc.nps.edu/NWDC_EM_Course/course_materials/free_electron_refraction.html

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Metals are highly reflective because conduction electrons respond strongly to incident electromagnetic fields.
Metal optical behaviour is described using a complex refractive index N = n + i k.
The extinction coefficient k describes attenuation inside the metal.
High conductivity is associated with high reflectance, especially at lower frequencies / longer wavelengths.
The Drude model relates free-electron response to metal optical behaviour.
Below the plasma frequency, metals are highly reflective and opaque.
Above the plasma frequency, some metals become more transmissive in the ultraviolet because electrons cannot screen the field as effectively.
Light entering a metal penetrates only a shallow skin depth before being attenuated.
Absorption occurs through electron excitation, lattice vibrations, and damping losses.
Thin metal films require care because their optical constants and reflection depend on thickness, surface, and film quality.
```

## Established Physics Baseline

For a metal, refractive index is complex:

```text
N = n + i k
```

where:

```text
n = real refractive index contribution
k = extinction coefficient / attenuation contribution
```

At normal incidence from air into a material with complex index `N`, reflectance is:

```text
R = |(N - 1) / (N + 1)|^2
```

Expanding for:

```text
N = n + i k
```

gives:

```text
R = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)
```

When `k` is large:

```text
R -> high
```

Skin depth is approximately:

```text
delta = lambda / (4 pi k)
```

for optical wavelength `lambda` in vacuum.

This means:

```text
large k
=> shallow penetration
=> strong attenuation
```

## AMS Core Claim

Metal reflects light because the incident optical route is not admitted as a deep coherent dielectric through-route.

Instead:

```text
incident optical field
=> drives collective surface/conduction-electron response
=> induced response creates strong return route
=> small fraction enters as shallow lossy route
```

AMS reading:

```text
metallic reflection
= high B_return
+ low B_deep
+ high shallow absorption capacity
+ strong conductive surface reseating
```

This is different from fused silica:

```text
fused silica:
route enters and continues with phase delay

metal:
route is mostly returned by collective electron response
```

## Route Variables for Metals

Add metal-specific interface variables:

```text
B_return
= boundary return capacity

B_deep
= deep propagation admission capacity

K_ext
= extinction / attenuation strength

S_e
= surface electron response strength

L_skin
= skin-depth route length

D_oxide
= oxide/tarnish/contamination layer defect or dielectric-overlayer burden
```

Relations:

```text
K_ext ~ k

L_skin ~ delta

S_e increases with free-electron response and conductivity

B_return increases with S_e and K_ext

B_deep decreases with K_ext
```

## AMS Metallic Reflection Formula Sketch

For a clean polished metal:

```text
R_AMS = R_complex_Fresnel * Q_surface * (1 - D_rough - D_oxide)
        + R_diffuse
```

where:

```text
R_complex_Fresnel
= reflectance from complex index N = n + i k

Q_surface
= coherent surface return quality

D_rough
= roughness scatter penalty

D_oxide
= oxide/tarnish/contamination route penalty

R_diffuse
= scattered return fraction
```

Transmission into deep bulk:

```text
T_deep_AMS ~= T_boundary * exp(-d / delta)
```

where:

```text
d = metal thickness
delta = skin depth
```

For thick metals:

```text
d >> delta
=> T_deep_AMS -> 0
```

Absorption:

```text
A_AMS = 1 - R_AMS - T_deep_AMS - S_external
```

Route interpretation:

```text
R = returned route
T_deep = admitted propagating route
A = shallow lossy route
S_external = diffuse scattered route
```

## Route Classes

### Polished Metal Surface

Route profile:

```text
primary_route: return route
AMS route class: R1_return / R3_admission_block
primary_obstruction: O2 against deep entry
dominance: D1_return
route_grade: G_A for polished coherent reflection
```

Interpretation:

The metal surface provides a highly coherent return route when smooth and clean.

AMS description:

```text
surface electron response
creates ordered return
while skin-depth loss remains shallow
```

### Rough Metal Surface

Route profile:

```text
primary_route: fragmented return
route class: R6
obstruction: O6
dominance: D3/D4 depending roughness
route_grade: G_C
```

Interpretation:

Roughness does not remove metallic electron response. It destroys the geometric coherence of the returned route.

Expected behaviour:

```text
less mirror reflection
more diffuse scatter
still low deep transmission
```

### Oxidised / Tarnished Metal

Route profile:

```text
primary_route: dielectric-overlayer filtering plus metal return
route class: R1/R3/R5
obstruction: O2/O3
dominance: D4
route_grade: G_B/G_C
```

Interpretation:

An oxide layer inserts a dielectric or semiconducting terminal layer between air and metal.

AMS formula:

```text
air -> oxide/tarnish layer -> metal
=> delayed, absorbed, scattered, or colour-shifted return route
```

This explains why polished metal, oxidised metal, and coloured tarnished metal need separate interface cases.

## Plasma Frequency Interpretation

Conventional:

```text
below plasma frequency
=> conduction electrons screen the field
=> high reflectance

above plasma frequency
=> electrons cannot follow effectively
=> reflectance decreases and transmission may increase
```

AMS:

```text
below plasma frequency
=> S_e high
=> B_return high
=> B_deep low

above plasma frequency
=> S_e weaker
=> B_return falls
=> B_deep may rise
```

Route transition:

```text
metal-like return route
=> dielectric-like admission route
```

This matters because metal reflectivity is frequency-dependent, not an absolute surface property.

## Conductivity Link

Conventional:

```text
high conductivity correlates with high infrared reflectance.
```

The Hagen-Rubens relation connects reflectance with conductivity in an applicable low-frequency regime:

```text
R = 1 - 4 sqrt(nu pi epsilon_0 / sigma)
```

where:

```text
nu = frequency
epsilon_0 = vacuum permittivity
sigma = conductivity
```

AMS interpretation:

```text
higher conductivity
=> stronger collective electron route response
=> stronger coherent return capacity
```

Route form:

```text
sigma high
=> S_e high
=> B_return high
=> R high
```

## Glass vs Metal Route Contrast

| Feature | Fused silica | Metal |
|---|---|---|
| optical index | mostly real in transparency window | complex `n + i k` |
| primary response | polarisation delay | conduction-electron screening/return |
| route type | deep through-route | surface return route |
| loss type | wavelength-specific absorption/scattering | shallow skin-depth absorption |
| surface effect | reflection plus transmission | reflection plus shallow attenuation |
| AMS dominant route | `R1` through-route | `R1_return` / `R3_admission_block` |
| defect sensitivity | bulk impurities and OH bands matter | roughness/oxide/tarnish strongly affect return quality |

AMS summary:

```text
glass admits and delays.
metal rejects and returns.
```

## Worked Normal-Incidence Example: Silver-Like High-k Metal

Use a generic optical metal condition:

```text
n = 0.14
k = 4.0
```

Normal-incidence reflectance:

```text
R = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)

R = ((0.14 - 1)^2 + 4.0^2) / ((0.14 + 1)^2 + 4.0^2)

R = (0.7396 + 16) / (1.2996 + 16)

R = 16.7396 / 17.2996

R ~= 0.968
```

So:

```text
about 96.8 percent reflected at a clean normal-incidence surface
```

AMS reading:

```text
large k
=> high extinction
=> deep route is unavailable
=> coherent return dominates
```

This contrasts with fused silica:

```text
air -> fused silica
=> about 3.5 percent reflected per clean surface

air -> high-k polished metal
=> about 97 percent reflected at clean normal incidence
```

## Vorton Interpretation

In fused silica:

```text
Si-O network vortons
=> coherent delay and through-route
```

In metal:

```text
conduction-electron surface response
=> collective return vorton field
=> shallow absorption loops
```

Candidate metal vorton model:

```text
incident optical route
drives surface electron displacement
surface electron field reseats against incident field
return route forms coherently
penetrating fraction decays over skin depth
```

Loss route:

```text
electron damping
=> shallow R5 absorption
=> heat
```

Roughness route:

```text
surface geometry disorder
=> R6 fragmented return
=> diffuse scatter
```

Oxide route:

```text
oxide overlayer
=> dielectric gate before metal
=> R3/R5/O2/O3
=> colour, absorption, reduced specular reflection
```

## Integration with Existing Interface Library

Existing strong anchors:

```text
air -> polished metal
air -> oxidised metal
```

Updated interpretation:

```text
air -> polished metal
=> high S_e, high B_return, low D_rough, low D_oxide
=> coherent high reflectance

air -> oxidised metal
=> oxide overlayer changes J_bound and J_trans
=> D_oxide increases
=> return route becomes filtered, absorbed, colour-shifted, or diffuse
```

Route classification:

```text
polished metal:
R1_return / O2_deep-entry block / D1_return / G_A

oxidised metal:
R1/R3/R5 / O2/O3 / D4 / G_B-G_C
```

## Score Assessment

Metallic reflection route equation sketch:

```text
score: 8/10
confidence: moderate
```

Reason:

This is a useful first metal optical model because:

- it preserves complex-index Fresnel physics
- it distinguishes return, shallow absorption, and deep transmission routes
- it maps conductivity and plasma frequency into surface-return capacity
- it explains polished vs rough vs oxidised metal differences
- it contrasts cleanly with fused silica transmission

Limitations:

- no specific metal family has been fully mapped yet
- Drude parameters are not imported numerically
- interband transitions are not modelled
- surface plasmon behaviour is not mapped
- oxide-layer interference and colour require a multilayer route model

## Next Artifact

The next useful artifact should be:

```text
ams-copper-silver-gold-metal-optics-comparison-v1.md
```

Purpose:

Compare real metals with different colours and optical constants:

- silver: high broadband visible reflectance
- aluminium: high reflectance with UV relevance
- copper: red/orange colour from spectral absorption
- gold: yellow colour from blue absorption / interband transitions
- iron: lower, oxidation-sensitive reflectance

This will move the metal reflection model from generic complex-index sketch to element-specific optical route behaviour.
