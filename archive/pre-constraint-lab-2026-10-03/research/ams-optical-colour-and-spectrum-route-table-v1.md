# AMS Optical Colour and Spectrum Route Table v1

## Purpose

This file extends the single-wavelength optical benchmark into a spectral route table.

It maps:

- silver's neutral visible mirror route
- gold's yellow return route
- copper's red/orange return route
- aluminium's UV-visible reflector route
- iron's oxidation-sensitive lower-reflectance route
- fused silica's UV-visible-IR transmission windows

The goal is to make colour and transparency route-specific rather than generic.

## Source Basis

Initial source anchors:

- MDPI Nanomaterials, "Impact of the Interband Transitions in Gold and Silver on the Dynamics of Propagating and Localized Surface Plasmons." https://www.mdpi.com/2079-4991/10/7/1411
- Engineering LibreTexts, "Metallic Reflection." https://eng.libretexts.org/Workbench/Materials_Science_for_Electrical_Engineering/06%3A_Thermal_Optical/6.01%3A_Optical_Properties/6.1.02%3A_Metallic_Reflection
- Abridged Optics, "Reflective Optics & Mirrors." https://www.abridgedoptics.com/comprehensive/optics/mirrors
- Edmund Optics, "UV vs. IR Grade Fused Silica." https://www.edmundoptics.com/knowledge-center/application-notes/optics/uv-vs-ir-grade-fused-silica/
- RP Photonics, "Fused Silica." https://www.rp-photonics.com/fused_silica.html
- Alkor Technologies, "Fused Silica windows and lenses." https://alkor.net/FusedSilica_windows_and_lenses.html
- RefractiveIndex.INFO database. https://refractiveindex.info/

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Silver has a comparatively flat visible reflectance spectrum and therefore appears silvery.
Gold absorbs blue/violet light more strongly and appears yellow because reflected light is deficient in blue.
Copper absorbs shorter visible wavelengths more strongly and appears red/orange.
Aluminium has broad UV-visible usefulness but oxidizes rapidly and is commonly protected by coatings.
Silver has very high visible/near-IR reflectance but tarnishes and has weaker UV performance.
Gold is especially useful in infrared mirror applications and has strong chemical stability.
Fused silica transmits broadly across UV, visible, and near-IR depending grade.
OH impurities produce absorption bands around 1.4 um, 2.2 um, and 2.7-2.8 um.
IR-grade fused silica reduces OH-related absorption but tends to have weaker deep-UV performance.
UV-grade fused silica favours UV transmission but can show OH absorption in near-IR.
```

## AMS Core Claim

Colour is spectral route filtering.

Transparency is spectral route admission.

Reflection is spectral route return.

AMS formula:

```text
observed optical appearance
= route distribution across wavelength
= R(lambda) + T(lambda) + A(lambda) + S(lambda)
```

where:

```text
R(lambda) = returned route
T(lambda) = transmitted route
A(lambda) = absorbed route
S(lambda) = scattered route
```

Colour occurs when:

```text
R(lambda)
or
T(lambda)
is uneven across visible wavelengths.
```

## Visible Spectrum Route Bands

Working visible bands:

```text
violet/blue: 400-500 nm
green: 500-570 nm
yellow/orange: 570-620 nm
red: 620-700 nm
```

These are approximate route-analysis bins, not strict colourimetry.

## Metal Spectral Route Table

| Metal | Blue/violet route | Green route | Yellow/orange route | Red route | Visible appearance | AMS class |
|---|---|---|---|---|---|---|
| Ag | high return | high return | high return | high return | silvery / neutral | flat `R1_return` |
| Al | high return, UV-capable | high return | high return | high return | silvery, slightly grey | coated broad `R1_return` |
| Au | absorbed more strongly | moderate return | high return | high return | yellow | blue `R5`, yellow/red `R1_return` |
| Cu | absorbed more strongly | reduced/moderate return | high return | high return | red/orange | short-wave `R5`, red/orange `R1_return` |
| Fe | moderate-low return | moderate-low return | moderate-low return | moderate-low return | grey/dull, oxide-sensitive | mixed `R1/R5/R6` |

## Silver: Neutral Mirror Route

AMS route profile:

```text
blue: R1_return high
green: R1_return high
yellow/orange: R1_return high
red: R1_return high
```

Appearance:

```text
silvery / white-metal
```

Interpretation:

Silver returns visible routes with comparatively little spectral filtering.

AMS description:

```text
flat visible return
=> neutral colour
=> strongest ordinary clean mirror route
```

Failure / degradation:

```text
tarnish
=> terminal-layer filter
=> R3/R5/D4
=> reduced specular return
```

## Aluminium: UV-Visible Broad Return with Oxide Gate

AMS route profile:

```text
UV: high return when surface/coating supports it
blue: R1_return high
green: R1_return high
yellow/orange: R1_return high
red: R1_return high
```

Appearance:

```text
silvery / grey
```

Interpretation:

Aluminium is a broad reflector, especially valuable into the UV, but it rapidly forms oxide. The oxide may be protective, but it becomes part of the optical route.

AMS description:

```text
Al metal return
+ Al2O3 terminal gate
=> coating-dependent broad return
```

Failure / degradation:

```text
uncontrolled oxide
=> altered J_bound / J_trans
=> lower or shifted route return
```

## Gold: Yellow Route Filter

AMS route profile:

```text
blue/violet: R5 absorption elevated
green: moderate return
yellow/orange: R1_return high
red: R1_return high
IR: R1_return high
```

Appearance:

```text
yellow
```

Interpretation:

Gold is not yellow because it emits yellow light. It is yellow because white-light return is spectrally filtered.

AMS description:

```text
blue route capture
+ red/yellow return
=> yellow appearance
```

Mechanism anchor:

```text
interband transitions absorb blue/violet routes more strongly.
```

Stability:

```text
low tarnish
=> terminal-layer route remains stable
```

## Copper: Red/Orange Route Filter

AMS route profile:

```text
blue/violet: R5 absorption elevated
green: reduced/moderate return
yellow/orange: R1_return high
red: R1_return high
IR: strong return
```

Appearance:

```text
red/orange
```

Interpretation:

Copper is a stronger spectral filter than a neutral mirror. It returns red/orange routes more effectively than shorter visible routes.

AMS description:

```text
short-wavelength route capture
+ red/orange return
=> copper colour
```

Surface condition:

```text
oxide/patina
=> new terminal-layer colour route
=> appearance changes strongly
```

## Iron: Oxide-Sensitive Dull Return

AMS route profile:

```text
blue/violet: mixed return/absorption
green: mixed return/absorption
yellow/orange: mixed return/absorption
red: mixed return/absorption
```

Appearance:

```text
grey, darker, duller unless highly polished
rust/oxide colours when oxidised
```

Interpretation:

Iron is not a primary optical mirror material in ordinary conditions because oxide, roughness, and absorption reduce coherent specular return.

AMS description:

```text
polished Fe
=> R1_return possible

ordinary/oxidised Fe
=> R5/R6 oxide-dominated route
```

## Fused Silica Spectral Route Table

| Spectral region | UV-grade fused silica | IR-grade fused silica | AMS route reading |
|---|---|---|---|
| deep UV | strong if low metallic defects | weaker than UV grade | `R1` if defects low |
| visible | strong transmission | strong transmission | strongest `T/R1` window |
| near IR around 1.4 um | OH absorption possible | reduced if low-OH | local `R5/O3` if OH present |
| near IR around 2.2 um | OH absorption strong | reduced if low-OH | local `R5/O3` |
| near IR around 2.7-2.8 um | OH absorption strong | reduced if low-OH | local `R5/O3` |
| mid IR beyond silica window | intrinsic vibration absorption rises | limited by Si-O modes | `R5/O3` vibrational capture |

## Fused Silica Route Interpretation

### Visible Region

```text
T(lambda) high
A(lambda) low
S(lambda) low if polished/homogeneous
```

AMS:

```text
strong through-route
=> transparent appearance
```

### UV Region

```text
T(lambda) depends on metallic impurities, oxygen defects, and solarization resistance.
```

AMS:

```text
UV route is defect-sensitive.
```

### Near-IR OH Bands

```text
OH absorbs at specific bands.
```

AMS:

```text
OH introduces wavelength-specific R5/O3 capture loops.
```

### Mid-IR Si-O Vibrational Region

```text
intrinsic Si-O vibration absorption rises.
```

AMS:

```text
optical route couples into network vibration
=> through-route fails
```

## Colour as Route Distribution

For white light:

```text
incident spectrum = many wavelength routes
```

Observed colour depends on:

```text
returned spectrum for reflective objects
transmitted spectrum for transparent objects
emitted spectrum for luminous objects
```

AMS reflective colour:

```text
colour_reflected(lambda)
= R(lambda) * incident(lambda)
```

AMS transparent colour:

```text
colour_transmitted(lambda)
= T(lambda) * incident(lambda)
```

Absorbed route:

```text
A(lambda)
=> missing colour contribution
=> heat / electronic excitation / vibrational excitation
```

## Spectral Route Classes

### Class C1: Flat Return

Example:

```text
silver
```

AMS:

```text
R(lambda) high and flat across visible
=> neutral mirror appearance
```

### Class C2: Blue-Absorbing Return

Example:

```text
gold
```

AMS:

```text
R_blue lower
R_yellow/red higher
=> yellow appearance
```

### Class C3: Short-Wavelength-Absorbing Return

Example:

```text
copper
```

AMS:

```text
short visible routes captured
red/orange routes returned
=> copper colour
```

### Class C4: Oxide-Gated Return

Examples:

```text
aluminium, iron, tarnished silver, oxidised copper
```

AMS:

```text
metal return filtered through terminal overlayer
```

### Class C5: Transparent Window

Example:

```text
fused silica visible range
```

AMS:

```text
T(lambda) high
R(lambda) modest
A(lambda) low
S(lambda) low
```

### Class C6: Absorption-Band Window Failure

Example:

```text
OH bands in fused silica
```

AMS:

```text
localized wavelength-specific R5/O3 capture
```

## Route Model Update

The optical model should now distinguish three spectral functions:

```text
R(lambda)
T(lambda)
A(lambda)
```

plus scattering:

```text
S(lambda)
```

with conservation:

```text
R(lambda) + T(lambda) + A(lambda) + S(lambda) = 1
```

For glass:

```text
T(lambda) dominates in the transparency window.
```

For polished metals:

```text
R(lambda) dominates below relevant plasma/interband limits.
```

For coloured metals:

```text
A(lambda) selectively removes part of visible spectrum.
```

For oxidised/rough surfaces:

```text
S(lambda) and overlayer A(lambda) increase.
```

## Score Assessment

Optical colour and spectrum route table:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

This table strengthens the optical model because:

- colour is now tied to wavelength-dependent route distribution
- gold and copper are explained as spectral absorption/return cases
- silver and aluminium are separated as flat/broad return cases with different surface vulnerabilities
- fused silica transparency is separated into UV, visible, OH-band, and IR routes
- the model now uses `R(lambda)`, `T(lambda)`, `A(lambda)`, and `S(lambda)` rather than single scalar reflectance

Limitations:

- no full spectral numerical curves yet
- no CIE colour calculation
- no coating/thin-film interference model
- no oxide-specific spectral constants
- no plasmonic nanostructure treatment

## Effect on Optical Master Model

Previous optical route master score:

```text
8.5/10
```

Updated pressure:

```text
upward, but retain 8.5/10
```

Reason:

The model is more complete spectrally, but it still lacks full numerical wavelength curves and multilayer/oxide modelling.

## Next Artifact

The next useful artifact should be:

```text
ams-optical-multilayer-oxide-coating-route-model-v1.md
```

Purpose:

Model:

- protected aluminium
- protected silver
- tarnished silver
- oxidised copper
- rusted iron
- dielectric antireflection coating on glass
- thin-film interference as route recombination

This is the missing bridge between ideal surfaces and real optical components.
