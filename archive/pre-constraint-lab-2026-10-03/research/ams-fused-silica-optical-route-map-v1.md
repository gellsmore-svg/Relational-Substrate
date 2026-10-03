# AMS Fused Silica Optical Route Map v1

## Purpose

This file maps fused silica optical transmission into AMS route, obstruction, dominance, and vorton language.

It reconnects the element-family programme to the original optical question:

```text
How does light travel through glass from a vorton perspective?
```

Fused silica is the cleanest first case because it is a high-purity `SiO2` glass with strong amorphous network closure, broad optical transparency, low thermal expansion, and well-characterised absorption limits.

## Source Basis

Initial source anchors:

- Edmund Optics, "UV vs. IR Grade Fused Silica." https://www.edmundoptics.com/knowledge-center/application-notes/optics/uv-vs-ir-grade-fused-silica/
- Translume, "Fused Silica Material Properties." https://www.translume.com/component/k2/item/186-fused-silica-material-properties
- RP Photonics, "Fused Silica." https://www.rp-photonics.com/fused_silica.html
- Photonics Spectra, "Fused Silica: A Transparent Look at a Complex Material." https://www.photonics.com/Articles/Fused_Silica_A_Transparent_Look_at_a_Complex/a68477
- Journal of Non-Crystalline Solids, "Effect of hydroxyl impurity on temperature coefficient of refractive index of synthetic silica glasses." https://doi.org/10.1016/j.jnoncrysol.2009.08.011
- Applied Optics, "Optical constants of silica glass from extreme ultraviolet to far infrared at near room temperature." https://doi.org/10.1364/AO.46.008118
- International Journal of Thermal Sciences, "Spectral properties of an UV fused silica within 0.8 to 5 um at elevated temperatures." https://doi.org/10.1016/j.ijthermalsci.2017.09.018

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Fused silica is widely used for lenses, windows, prisms, mirrors, beamsplitters, precision optics, and optical components.
It has broad transparency from deep UV through visible and into near/mid infrared, depending on grade and impurities.
It is chemically pure when made synthetically and can have very low metallic impurity levels.
UV-grade fused silica gives high UV transmission but can contain OH groups that absorb in the near infrared.
IR-grade fused silica has lower OH content and better infrared transmission, but usually poorer deep-UV transmission.
OH groups cause absorption bands near roughly 1.4 um, 2.2 um, and 2.7-2.8 um.
Intrinsic Si-O vibrational absorption appears in the infrared, including strong absorption around the 8.9-9.5 um region.
Metallic impurities and oxygen-deficiency defects can increase UV absorption and radiation/laser damage sensitivity.
Fused silica is amorphous and optically isotropic, unlike crystalline quartz.
Its refractive index depends on wavelength and temperature.
Surface reflection causes Fresnel losses unless corrected by coatings or geometry.
```

## AMS Core Claim

Fused silica transmits light because its amorphous silicon-oxygen network is sufficiently coherent to admit optical through-routes while lacking large periodic or particulate discontinuities that would scatter the route strongly.

AMS reading:

```text
fused silica
= retained amorphous network closure
+ low impurity burden
+ low defect-state absorption
+ smooth enough terminal layers
=> high optical route viability
```

Transmission is not absence of interaction.

It is successful route handoff:

```text
incoming optical disturbance
=> admitted at entry surface
=> propagated through polarizable network
=> released at exit surface
```

## Route Stack

### Stage 1: Air-to-Silica Admission

Conventional language:

```text
light reaches an air-glass boundary
part of it reflects
part of it transmits
transmitted light changes speed and direction according to refractive index and angle
```

AMS route language:

```text
entry boundary tests route compatibility
```

Route profile:

```text
primary_route: R1/R2
secondary_route: R3 if angle/impedance mismatch is high
primary_obstruction: O1
secondary_obstruction: O2
dominance: D1/D4
route_grade: G_A/G_B for polished optical surfaces
```

Interpretation:

Entry is not simply penetration. It is boundary reseating. The incoming optical route must be admitted into the denser silica route field.

AMS formula:

```text
air route
+ silica terminal layer
=> refracted route inside glass
+ reflected route at boundary
```

### Stage 2: Bulk Propagation Through Amorphous SiO2

Conventional language:

```text
light propagates through a transparent dielectric with wavelength-dependent refractive index.
```

AMS route language:

```text
bulk silica provides a coherent optical route field
```

Route profile:

```text
primary_route: R1
secondary_route: R2 for wavelength-dependent polarisation response
primary_obstruction: O1
secondary_obstruction: O5 if absorption/defect fields increase
dominance: D1
route_grade: G_A in clean visible/near-UV/near-IR windows
```

Interpretation:

Fused silica is amorphous, but not route-random. Its local Si-O closure is connected enough to preserve optical coherence across the bulk.

AMS formula:

```text
local Si-O closure
+ amorphous isotropy
+ low defect density
=> coherent through-route
```

### Stage 3: Refractive Delay and Bending

Conventional language:

```text
light travels more slowly in glass than in air
the refractive index controls phase velocity and bending at an interface
```

AMS route language:

```text
glass imposes route delay by polarisation-coupled reseating
```

Route profile:

```text
route: R1 with controlled R2 response
obstruction: O1 as ordered delay
dominance: D1
grade: G_A
```

Interpretation:

Refraction is not treated as a hard collision with particles. It is a coherent change in route timing caused by the polarizable network.

AMS description:

```text
the optical event repeatedly hands off through the silica closure field
each handoff imposes phase delay
phase-delay gradient at boundary becomes bending
```

Vorton reading:

```text
Si-O network vortons
do not trap the optical route
but impose coherent delay on it
```

### Stage 4: Bulk Loss Channels

Conventional loss channels:

```text
OH absorption
metallic impurity absorption
oxygen-deficiency defects
point defects / color centers
Si-O vibrational absorption in IR
bubbles, inclusions, density inhomogeneity
Rayleigh scattering from frozen density fluctuations
surface damage
```

AMS route language:

```text
loss occurs when the optical route is diverted into absorption, scattering, or defect-state trapping.
```

Route profile:

```text
absorption: R5/O3
scattering: R6/O6
impurity route capture: R3/R5, O2/O3
defect-state trapping: R5/O3
dominance: local D2/D4
```

Interpretation:

Loss is route failure or route diversion.

```text
good fused silica
=> high R1 continuity, low R5/R6 leakage

impure or damaged fused silica
=> local R5/R6 leakage increases
```

### Stage 5: Silica-to-Air Release

Conventional language:

```text
light exits glass into air, with refraction and partial reflection.
```

AMS route language:

```text
exit boundary releases the silica route back into the air route field.
```

Route profile:

```text
primary_route: R1/R2
secondary_route: R3 at high mismatch or angle
primary_obstruction: O1/O2
dominance: D1/D4
grade: G_A/G_B for polished optical surfaces
```

Interpretation:

Exit is another reseating operation. A smooth, clean, polished terminal layer allows ordered release. A rough, contaminated, or defect-rich layer introduces diffuse release.

AMS formula:

```text
silica internal route
+ terminal-layer geometry
=> transmitted release
+ reflected return
+ possible diffuse scatter
```

## Why Fused Silica Is Transparent

AMS transparent condition:

```text
R1 through-route remains stronger than R5 absorption and R6 scattering routes.
```

For fused silica in a good optical window:

```text
network coherence: high
impurity burden: low
defect density: low
large-scale scatterers: low
terminal-layer polish: high
wavelength compatibility: high
```

Therefore:

```text
I_comp high
Q_coh high
D low
B_in high
B_out high
```

using the interface variables:

```text
B_in: admission capacity
B_out: release capacity
J_bound: immediate boundary coupling
J_trans: through-layer transition continuity
Q_coh: coherence preservation
D: defect burden
```

## UV-Grade vs IR-Grade Fused Silica

### UV-Grade

Source-supported behaviour:

```text
high UV transmission
often higher OH content
OH absorption bands in near infrared
low metallic impurities for deep-UV performance
```

AMS route profile:

```text
UV route: strong R1
near-IR OH bands: local R5/O3 absorption
defect burden: low for metallic UV absorbers
```

Interpretation:

UV-grade fused silica is optimised to keep UV routes open, even if OH-related infrared routes are compromised.

### IR-Grade

Source-supported behaviour:

```text
low OH content
better infrared transmission
usually weaker deep-UV transmission than UV-grade
```

AMS route profile:

```text
IR route: stronger R1 than high-OH silica
UV route: more vulnerable to metallic/defect absorption
```

Interpretation:

IR-grade fused silica is optimised to suppress OH absorption routes, even if deep UV admission is weaker.

## Wavelength Route Table

| Spectral region | Conventional behaviour | AMS route reading | Main obstruction |
|---|---|---|---|
| deep UV below useful window | absorption rises | route captured by electronic/defect states | `O3/R5` |
| UV-grade transmission window | high transmission if impurities low | strong `R1` through-route | low `D` required |
| visible | very high transmission | strongest `R1/G_A` route | surface reflection mostly |
| near IR | generally good, OH bands matter | `R1` interrupted by OH `R5` bands | `O3` |
| mid IR beyond silica window | vibrational absorption rises | route couples into Si-O vibration | `R5/O3` |
| rough/damaged surface case | scattering/reflection increases | terminal-layer release fragments | `R6/O6` |

## Interface Variable Mapping

### Clean Polished Fused Silica Surface

```text
B_in: high
B_out: high
J_bound: high
J_trans: high
Q_coh: high
D: low
I_comp: high
```

Expected behaviour:

```text
ordered refraction
low diffuse scatter
predictable Fresnel reflection
high transmission
```

### OH-Rich Bulk

```text
B_in: high
B_out: high
J_bound: high
J_trans: moderate in OH absorption bands
Q_coh: wavelength-dependent
D: moderate at OH bands
I_comp: high outside absorption bands, lower inside them
```

Expected behaviour:

```text
good visible/UV transmission
near-IR absorption dips
```

### Metallic Impurity / Defect-Rich Bulk

```text
B_in: moderate-high
B_out: moderate-high
J_bound: variable
J_trans: reduced
Q_coh: reduced
D: high
I_comp: reduced
```

Expected behaviour:

```text
UV absorption
color centers
laser damage sensitivity
luminescence or solarization risk
```

### Rough or Damaged Surface

```text
B_in: lower
B_out: lower
J_bound: low-moderate
J_trans: bulk may remain high
Q_coh: surface-limited
D: high at terminal layer
I_comp: surface-limited
```

Expected behaviour:

```text
diffuse scatter
reduced transmission
uncontrolled reflection
```

## Vorton Interpretation

Fused silica is not transparent because nothing happens inside it.

It is transparent because the Si-O closure field supports coherent optical handoff without converting most of the route into absorption or scattering.

Candidate vorton model:

```text
Si-O network vorton field
=> local stable closure
=> repeated polarisation handoff
=> coherent delay
=> transmitted optical route
```

Loss model:

```text
OH group
=> vibrational capture loop
=> wavelength-specific R5 absorption

metal impurity
=> defect-state capture / electronic loss
=> UV R5 absorption

oxygen-deficiency center
=> defect loop
=> UV absorption / luminescence / laser damage sensitivity

rough terminal layer
=> broken release loops
=> R6 scatter
```

## Relation to Earlier Interface Work

This file strengthens the previous interface categories:

```text
air -> glass
=> entry admission

glass -> air
=> exit release

glass -> crystal
=> route mismatch / late-gate risk

rough glass
=> terminal-layer fragmentation

OH / impurity bands
=> bulk loss channels
```

It also clarifies why fused silica is a stronger optical benchmark than soda-lime glass:

```text
fewer modifiers
lower impurity burden when synthetic
more uniform Si-O backbone
lower route competition
```

## Score Assessment

Fused silica optical route map:

```text
score: 9/10
confidence: high
```

Reason:

This is a very strong AMS case because:

- fused silica is a clean SiO2 backbone system
- optical transmission, refraction, absorption, and surface reflection map naturally to route variables
- UV/IR grade differences map to specific defect/impurity routes
- OH absorption is a concrete wavelength-specific route-capture case
- surface polish and defect burden map directly to interface variables
- it directly answers the original glass-light mechanism question

Limitations:

- refractive index mathematics is not yet formalised inside AMS notation
- Fresnel reflection has not yet been translated into a route equation
- Rayleigh scattering and density fluctuation geometry need a separate note
- nonlinear optics and laser damage need deeper modelling

## Silicon Family Score Pressure

Current silicon family score:

```text
9/10
```

Fused silica optical subcase:

```text
9/10
```

Updated pressure:

```text
retain 9/10
confidence strengthened
```

Reason:

The fused silica optical case confirms silicon's role as reference backbone and optical route medium, but the whole family should not move above 9 until semiconductor/interface and biological silica subcases are mapped in comparable detail.

## Next Artifact

The next useful artifact should be:

```text
ams-fresnel-refraction-route-equation-sketch-v1.md
```

Purpose:

Translate the conventional optical boundary laws into AMS variables:

- refractive index
- phase delay
- incidence angle
- reflection coefficient
- transmission coefficient
- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

This would begin the mathematical side of the vorton/interface optical model.
