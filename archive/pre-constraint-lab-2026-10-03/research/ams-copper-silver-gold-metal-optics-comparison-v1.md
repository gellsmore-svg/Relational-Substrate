# AMS Copper Silver Gold Metal Optics Comparison v1

## Purpose

This file moves metallic reflection modelling from a generic complex-index sketch into element-specific optical route behaviour.

It compares:

- silver
- aluminium
- copper
- gold
- iron

The goal is to explain why metals all share a strong return-route pattern while still differing in colour, tarnish sensitivity, oxidation behaviour, UV/visible/IR usefulness, and specular quality.

## Source Basis

Initial source anchors:

- Engineering LibreTexts, "Metallic Reflection." https://eng.libretexts.org/Workbench/Materials_Science_for_Electrical_Engineering/06%3A_Thermal_Optical/6.01%3A_Optical_Properties/6.1.02%3A_Metallic_Reflection
- MDPI Nanomaterials, "Impact of the Interband Transitions in Gold and Silver on the Dynamics of Propagating and Localized Surface Plasmons." https://www.mdpi.com/2079-4991/10/7/1411
- MDPI, "Optical Properties of AgAu Alloy Clusters." https://www.mdpi.com/2674-063X/3/1/3
- Pleiger Laseroptics, "Metal Mirrors." https://www.pleiger-laseroptics.com/pleiger/metal-mirrors.html
- Esco Optics, "Optical Reflective Coatings." https://escooptics.com/pages/metallic-reflectors
- Scientific Reports, "Realistic Silver Optical Constants for Plasmonics." https://www.nature.com/articles/srep30605
- Springer, "Combinatorial exploration of color in gold-based alloys." https://link.springer.com/article/10.1007/s13404-015-0167-z
- OSTI, "Role of reflectance in the photoacoustic spectra of copper, silver, and gold." https://www.osti.gov/biblio/7055759

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Metals have high reflectance across broad spectral regions because of their conduction-electron response.
Silver has very high visible-to-infrared reflectance but tarnishes easily.
Gold is useful especially in the infrared and does not tarnish as readily as silver.
Gold appears yellow because blue/violet light is absorbed more strongly, leaving reflected light deficient in blue.
Silver appears silvery because its visible reflectance is relatively flat; its interband transitions lie mainly in the ultraviolet.
Copper appears reddish/orange because its visible reflectance is spectrally uneven, with stronger absorption in shorter wavelengths.
Aluminium has strong UV and visible usefulness but oxidizes rapidly, usually requiring protective coatings.
Metal optical constants depend on surface condition, film quality, roughness, oxidation, tarnish, thickness, and wavelength.
For silver optical constants, pristine measurement is difficult because tarnishing on air exposure affects results.
Photoacoustic signals in Cu, Ag, and Au can be interpreted as reflectance-loss spectra, proportional to 1 - R.
```

## AMS Core Claim

All polished metals share a common route grammar:

```text
incident optical route
=> conduction-electron surface response
=> coherent return route
=> shallow absorption loss
```

But each metal has a different spectral route filter.

AMS formula:

```text
metal optical character
= return-route strength
+ spectral absorption channels
+ surface condition
+ oxide/tarnish overlayer
+ interband transition structure
+ roughness
```

This means:

```text
metal reflectance is not one generic property.
It is a surface-conditioned, wavelength-dependent route outcome.
```

## Comparison Table

| Metal | Main optical character | AMS route reading | Main loss/filter | Surface issue | Score |
|---|---|---|---|---|---:|
| silver | highest visible/IR mirror metal | strongest broad `R1_return` | UV/interband onset, tarnish loss | tarnishes easily | 8.5 |
| aluminium | strong UV-visible reflector | high `R1_return`, UV-capable | oxide/filter layer | oxidizes rapidly | 8 |
| gold | yellow, strong IR reflector | high red/IR return, blue route absorbed | blue/violet interband absorption | stable, soft | 8.5 |
| copper | red/orange reflector | red-biased return | blue/green absorption | oxidizes/tarnishes | 8 |
| iron | darker, oxidation-sensitive | weaker/rougher return | high absorption, oxide layer | rust/oxide dominates | 7 |

## Silver

### Conventional Optical Character

Silver is one of the strongest broadband visible and near-infrared reflectors.

Its visible reflectance is relatively flat, so it appears silvery rather than coloured.

Its major practical weakness is tarnish and surface degradation.

### AMS Route Reading

```text
metal: silver
primary_route: R1_return
secondary_route: shallow R5 absorption
primary_obstruction: O2 against deep entry
dominance: D1_return
route_grade: G_A when clean and polished
```

Silver has the cleanest visible metal return route.

AMS interpretation:

```text
high free-electron return capacity
low visible spectral filtering
=> strong neutral mirror route
```

Tarnish changes the terminal layer:

```text
clean Ag
=> high Q_surface, low D_oxide

tarnished Ag
=> D_oxide increases
=> R1_return becomes filtered/scattered/absorbed
```

### Vorton Interpretation

```text
silver surface electron field
=> broad coherent return vorton field
```

Tarnish:

```text
silver sulfide / surface contamination
=> oxide/sulfide overlayer
=> R3/R5 filter before metal return
```

### AMS Score

```text
silver optical route case: 8.5/10
confidence: moderate-high
```

Reason:

Silver is the strongest clean visible mirror case, but its surface instability prevents a higher score without protective-layer modelling.

## Aluminium

### Conventional Optical Character

Aluminium is widely used for optical coatings and has strong UV-visible reflectance.

It oxidizes rapidly and usually requires a protective overcoat.

### AMS Route Reading

```text
metal: aluminium
primary_route: R1_return
secondary_route: R3 through oxide/filter layer
primary_obstruction: O2
secondary_obstruction: O3 if oxide absorbs/scatters
dominance: D1/D4
route_grade: G_A/G_B depending coating
```

AMS interpretation:

```text
Al metal has strong return capacity.
Al oxide rapidly inserts a dielectric terminal layer.
```

This makes aluminium a natural multilayer-route case:

```text
air -> oxide/protective coating -> aluminium
```

### Vorton Interpretation

```text
aluminium electron return field
+ oxide overlayer gate
=> coated return route
```

The oxide layer is not merely damage. It can be protective and functionally useful if controlled.

### AMS Score

```text
aluminium optical route case: 8/10
confidence: moderate-high
```

Reason:

Strong UV-visible relevance and practical coating importance, but oxide/coating layers need explicit multilayer modelling.

## Gold

### Conventional Optical Character

Gold is highly reflective in red and infrared regions and appears yellow because blue/violet light is absorbed more strongly.

Sources connect this to interband transitions shifted into visible blue due to gold's electronic structure and relativistic effects.

Gold is chemically stable and tarnishes much less readily than silver.

### AMS Route Reading

```text
metal: gold
primary_route: R1_return for red/IR
secondary_route: R5 absorption for blue/violet
primary_obstruction: O2 against deep entry
secondary_obstruction: O3 spectral capture
dominance: D1_return with spectral D2 loss
route_grade: G_A/G_B
```

AMS interpretation:

```text
gold does not simply return all visible routes equally.
It selectively captures blue/violet routes and returns red/yellow-biased routes.
```

This creates colour:

```text
white light in
blue route partly absorbed
red/green routes returned
=> yellow appearance
```

### Vorton Interpretation

```text
gold surface field
=> strong return route
plus interband absorption loop in blue-visible region
```

The colour is a route-filter effect, not a pigment coating.

### AMS Score

```text
gold optical route case: 8.5/10
confidence: moderate-high
```

Reason:

Gold is a strong case because colour, infrared reflectance, chemical stability, and interband absorption map clearly to route filtering.

## Copper

### Conventional Optical Character

Copper appears reddish/orange because its reflectance is spectrally uneven. Shorter visible wavelengths are absorbed more strongly than red/orange wavelengths.

Copper oxidizes and tarnishes, changing its surface colour and reflectance.

### AMS Route Reading

```text
metal: copper
primary_route: R1_return for red/orange
secondary_route: R5 absorption for shorter visible wavelengths
primary_obstruction: O2
secondary_obstruction: O3 spectral absorption
dominance: D1_return with spectral D2 loss
route_grade: G_B/G_A when clean, lower when oxidised
```

AMS interpretation:

```text
copper returns red/orange routes more strongly than blue/green routes.
```

Oxidation:

```text
Cu oxide / patina
=> new terminal-layer filter
=> colour and reflectance shift
```

### Vorton Interpretation

```text
copper electron return field
+ visible interband/filter loss
+ oxide-layer route modification
=> red/orange metallic appearance
```

### AMS Score

```text
copper optical route case: 8/10
confidence: moderate
```

Reason:

Copper is a strong colour-filter metal case, but oxidation/patina complexity needs separate modelling.

## Iron

### Conventional Optical Character

Iron is less optically mirror-like than silver, gold, copper, or aluminium in ordinary surfaces and is strongly affected by oxidation.

Rust and oxide layers dominate practical appearance and reduce coherent metallic reflection.

### AMS Route Reading

```text
metal: iron
primary_route: R1_return when polished
secondary_route: R5 absorption and R6 diffuse scatter
primary_obstruction: O2
secondary_obstruction: O3/O6
dominance: D4 under real surface conditions
route_grade: G_B clean, G_C oxidised
```

AMS interpretation:

```text
clean polished Fe can return routes,
but real iron often becomes an oxide-layer optical case.
```

Oxidation:

```text
Fe oxide / rust
=> high D_oxide
=> high D_scat
=> lower Q_surface
=> diffuse/dull appearance
```

### Vorton Interpretation

```text
iron metal return field
is easily masked by oxide-route fragmentation
```

### AMS Score

```text
iron optical route case: 7/10
confidence: moderate
```

Reason:

Iron is useful mainly as the oxidation-sensitive contrast case. It needs a dedicated iron/oxide route map before higher confidence.

## Spectral Route Classes

### Neutral Mirror Route

Best example:

```text
silver
```

AMS:

```text
broad visible R1_return
low spectral filtering
```

### UV-Capable Reflector Route

Best example:

```text
aluminium
```

AMS:

```text
strong return field
oxide/coating gate critical
```

### Yellow Return Route

Best example:

```text
gold
```

AMS:

```text
blue/violet R5 absorption
red/green R1_return
```

### Red/Orange Return Route

Best example:

```text
copper
```

AMS:

```text
short-wavelength absorption
red/orange return dominance
```

### Oxide-Dominated Return Route

Best example:

```text
iron
```

AMS:

```text
metal return masked by oxide roughness/absorption
```

## Polished vs Oxidised/Tarnished Route Table

| Metal | Polished route | Oxidised/tarnished route | Main change |
|---|---|---|---|
| Ag | `R1_return/G_A` | `R3/R5/D4` | tarnish filters and lowers reflectance |
| Al | `R1_return/G_A` | oxide-gated `R1/R3` | protective oxide/coating controls route |
| Au | stable `R1_return` | minor overlayer issues | chemically stable route retained |
| Cu | red-biased `R1_return` | oxide/patina `R3/R5/R6` | colour and diffuse response change |
| Fe | `R1_return/G_B` if polished | rust/oxide `R5/R6/G_C` | coherent return collapses into dull surface |

## Relation to Complex-Index Model

All these cases fit the generic model:

```text
N = n + i k
```

But element-specific behaviour depends on:

```text
k(lambda)
n(lambda)
interband transitions
plasma frequency
surface oxidation
tarnish
roughness
film quality
protective coating
```

AMS translation:

```text
N(lambda)
=> wavelength-specific route return and absorption profile

surface condition
=> terminal-layer route quality

interband transitions
=> spectral R5 capture loops

oxide/tarnish
=> overlayer gate before metal response
```

## Score Assessment

Metal optics comparison set:

```text
score: 8/10
confidence: moderate-high
```

Reason:

This comparison strengthens the metal reflection model by showing that:

- metallic reflection is a shared route grammar
- metal colour is spectral route filtering
- silver, gold, copper, aluminium, and iron differ by interband transitions and surface layers
- oxidation and tarnish are terminal-layer route changes, not cosmetic details
- the generic complex-index model can be tied to element-specific AMS route classes

Limitations:

- numerical optical constants are not yet tabulated
- aluminium and silver protective coatings need multilayer modelling
- copper and iron oxide cases need dedicated maps
- plasmonic behaviour is not yet modelled
- thin-film interference is not yet included

## Score Pressure on Metal Reflection Model

Previous generic metal reflection sketch:

```text
8/10
confidence: moderate
```

Updated pressure:

```text
retain 8/10
confidence strengthened to moderate-high
```

Reason:

The comparison improves qualitative specificity but does not yet import quantitative optical constants or multilayer equations.

## Next Artifact

The next useful artifact should be:

```text
ams-optical-route-master-summary-v1.md
```

Purpose:

Consolidate the optical work into one readable model:

- fused silica transmission
- Fresnel/refraction route sketch
- metallic reflection
- metal comparison
- interface variables
- what is proven physics
- what is AMS interpretation
- what remains experimental/speculative

This should become the bridge document for feeding the optical mechanism back into the larger substrate theory.
