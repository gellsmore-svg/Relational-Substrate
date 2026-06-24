# AMS Calcium Carbonate Polymorph Route Map v1

## Purpose

This file maps the main calcium carbonate polymorphs into AMS route, obstruction, dominance, and vorton-closure language.

Calcium carbonate is a clean geometry test because the same bulk chemistry can enter multiple closure states:

```text
CaCO3
=> calcite
=> aragonite
=> vaterite
=> amorphous calcium carbonate
```

This makes CaCO3 useful for testing whether AMS can distinguish closure geometry, route history, and stability without changing elemental composition.

## Source Basis

Initial source anchors:

- "Bio-mineralisation, characterization, and stability of calcium carbonate containing organic matter." https://pmc.ncbi.nlm.nih.gov/articles/PMC8697732/
- "Review on Chemistry of Water-Containing Calcium Carbonates and Their Transformations into Amorphous and Crystalline Carbonate Modifications." https://www.mdpi.com/2304-6740/13/10/321
- "Phase-specific bioactivity and altered Ostwald ripening pathways of calcium carbonate polymorphs in simulated body fluid." https://pmc.ncbi.nlm.nih.gov/articles/PMC9064690/
- "Transformation of amorphous calcium carbonate into aragonite." https://doi.org/10.1016/j.jcrysgro.2012.01.025
- "Unlocking the mysterious polytypic features within vaterite CaCO3." https://www.nature.com/articles/s41467-023-43625-0
- "Inorganic ions regulate amorphous-to-crystal shape preservation in biomineralization." https://pmc.ncbi.nlm.nih.gov/articles/PMC7035494/
- "Spinning up the polymorphs of calcium carbonate." https://www.nature.com/articles/srep03616
- "Biomimetic Mineralization of CaCO3 on a Phospholipid Monolayer: From an Amorphous Calcium Carbonate Precursor to Calcite via Vaterite." https://doi.org/10.1021/la903641k

## Source-Supported Polymorph Summary

The source literature supports the following working map:

```text
calcite
=> thermodynamically stable crystalline endpoint under ambient conditions

aragonite
=> ordered crystalline polymorph favoured in some environmental and biological settings

vaterite
=> least stable main crystalline polymorph, often transient or kinetically selected

amorphous calcium carbonate
=> metastable precursor, storage, or transition phase, often central in biomineralization
```

Important caution:

```text
Transformation pathways are condition-dependent.
ACC does not always pass through every possible stage.
Biological and chemical templates can stabilise phases that would otherwise be transient.
```

## AMS Core Claim

Calcium carbonate polymorphism shows that identity at the chemical formula level is insufficient.

AMS reading:

```text
CaCO3 chemistry
!= single closure state

same composition
=> different route histories
=> different topological closures
=> different stability and biological function
```

The AMS object of interest is therefore not only:

```text
what atoms are present
```

but:

```text
what closure geometry has been admitted and retained.
```

## Polymorph Route Table

| Phase | Stability role | AMS route | Obstruction | Dominance | Route grade | Vorton closure type |
|---|---|---|---|---|---|---|
| calcite | stable endpoint | `R1` | `O1` | `D1` | `G_A` | stable compact closure |
| aragonite | alternative ordered closure | `R1/R3` | `O1/O2` | `D1/D4` | `G_A/G_B` | directed anisotropic closure |
| vaterite | metastable crystalline state | `R3/R5` | `O2/O3` | `D4/D2` | `G_C` | unstable/polytypic closure |
| ACC | amorphous precursor/storage | `R2/R5/R6` | `O3/O5/O6` | `D2/D4` | `G_C/G_D` before crystallisation | pre-closure reservoir |

## Calcite

### Conventional Role

Calcite is the most thermodynamically stable common calcium carbonate polymorph under ambient conditions.

It is widespread geologically and commonly appears as the endpoint of transformation pathways.

### AMS Route Reading

```text
phase: calcite
primary_route: R1
primary_obstruction: O1
dominance: D1
route_grade: G_A
```

Calcite represents stable compact closure.

AMS interpretation:

```text
route admitted
closure completed
strain distributed into stable lattice
future transformation pressure reduced
```

Calcite is therefore a baseline for:

```text
stable mineral identity
low route ambiguity
low closure competition
```

### Vorton Geometry

Candidate vorton geometry:

```text
compact repeating closure
short return paths
low residual route ambiguity
low metastable leakage
```

AMS description:

```text
calcite vorton field
= high-retention carbonate closure
= strongly completed R1 route
= minimal R5 pseudo-route activity
```

### Failure / Transition Cases

Calcite can still dissolve, fracture, or be transformed under boundary conditions.

AMS mapping:

```text
acid dissolution
=> boundary-driven route reopening
=> O5/O6 imposed externally

biological inhibition of calcite
=> R1 route blocked or deferred
=> alternative aragonite/vaterite/ACC route admitted
```

## Aragonite

### Conventional Role

Aragonite is an ordered crystalline polymorph often found in marine biominerals, shells, corals, and biologically regulated carbonate structures.

It is less stable than calcite under ordinary ambient conditions but can be favoured by environmental chemistry, magnesium influence, pressure, temperature, or biological templates.

### AMS Route Reading

```text
phase: aragonite
primary_route: R1
secondary_route: R3
primary_obstruction: O1
secondary_obstruction: O2
dominance: D1/D4
route_grade: G_A/G_B
```

Aragonite is not failed calcite. It is an alternative ordered closure.

AMS interpretation:

```text
route admitted under directional/template influence
closure completed in a different geometry
stability depends more strongly on environment and scaffold
```

### Vorton Geometry

Candidate vorton geometry:

```text
anisotropic closure
longer or directionally biased return paths
strong scaffold/interface compatibility
```

AMS description:

```text
aragonite vorton field
= ordered but directed closure
= stable enough under admitted conditions
= more environment-sensitive than calcite
```

### Biological Relevance

Aragonite is important because many organisms select it deliberately.

AMS reading:

```text
biological template
=> route steering
=> aragonite admitted instead of calcite
=> T1C process directs T1B closure
```

This makes aragonite a strong T1B/T1C bridge case.

## Vaterite

### Conventional Role

Vaterite is the least stable of the main crystalline calcium carbonate polymorphs and is often transient, kinetically selected, structurally complex, or biologically/chemically stabilised.

Recent literature emphasises that vaterite has complex polytypic features rather than a simple stable lattice identity.

### AMS Route Reading

```text
phase: vaterite
primary_route: R3
secondary_route: R5
primary_obstruction: O2
secondary_obstruction: O3
dominance: D4/D2
route_grade: G_C
```

Vaterite represents incomplete or unstable crystalline closure relative to calcite/aragonite.

AMS interpretation:

```text
route partially crystallised
closure achieved but not fully stable
residual route ambiguity remains
transition pressure persists
```

### Vorton Geometry

Candidate vorton geometry:

```text
polytypic or competing closure packets
local loop mismatch
incomplete route lock-in
high surface/solubility sensitivity
```

AMS description:

```text
vaterite vorton field
= metastable closure
= R3 route with R5 pseudo-route pressure
= high transformation readiness
```

### Biological / Functional Relevance

Vaterite can be stabilised or selected by organic matter, microbes, additives, or constrained formation environments.

AMS reading:

```text
external template or organic matrix
=> holds metastable closure in place
=> D4/D2 state persists beyond ordinary expectation
```

This is important because it shows that biological order can preserve a metastable mineral state for functional reasons.

## Amorphous Calcium Carbonate

### Conventional Role

Amorphous calcium carbonate is a major precursor, storage, or transition phase in many biomineralization contexts.

It may be hydrated or less hydrated, stabilised by organic matter, transformed into crystalline phases, or used as a temporary mineral reservoir.

### AMS Route Reading

```text
phase: amorphous calcium carbonate
primary_route: R2/R5
secondary_route: R6
primary_obstruction: O3/O5
secondary_obstruction: O6
dominance: D2/D4
route_grade: G_C/G_D before crystallisation
```

ACC is not merely "failed crystal." It is a pre-closure or storage field.

AMS interpretation:

```text
material identity present chemically
crystalline closure not yet selected
route options remain open
biological or environmental gate will select later closure
```

### Vorton Geometry

Candidate vorton geometry:

```text
pre-vorton reservoir
distributed local order
no single retained long-range closure
high transformation potential
```

AMS description:

```text
ACC field
= chemically bounded but topologically undercommitted
= route reservoir
= phase-choice substrate
```

### Biological Relevance

ACC is especially important in biomineralization because it allows organisms to separate:

```text
material gathering
from
final crystalline commitment
```

AMS reading:

```text
ACC storage
=> T1C system holds T1B material in pre-closure state
=> later converts it under scaffold/template control
```

This is one of the clearest examples of biological process governing material closure.

## Transformation Route Map

Generic transformation pressure:

```text
ACC
=> vaterite or aragonite intermediate
=> calcite endpoint
```

But actual pathways vary:

```text
ACC -> calcite
ACC -> vaterite -> calcite
ACC -> aragonite
ACC -> monohydrocalcite -> aragonite
ACC stabilised by organic matter
vaterite stabilised by organic matter
aragonite held by biological scaffold
```

AMS route sequence:

```text
pre-closure reservoir
=> metastable closure
=> alternative ordered closure
=> stable endpoint
```

In route notation:

```text
ACC: R2/R5/R6, D2/D4
vaterite: R3/R5, D4/D2
aragonite: R1/R3, D1/D4
calcite: R1, D1
```

## Biological Template Control

Calcium carbonate biomineralization is not merely precipitation in life.

AMS reading:

```text
organic matrix
microbial surface
phospholipid layer
protein / polysaccharide environment
Mg2+ or other ion field

=> changes route admission
=> changes polymorph selection
=> changes closure timing
=> changes retained morphology
```

This supports the broader AMS claim:

```text
T1C biological order can direct T1B material closure.
```

## Route Discriminator Table

| Question | Calcite | Aragonite | Vaterite | ACC |
|---|---|---|---|---|
| Is closure complete? | yes | yes | partially / metastably | no crystalline closure |
| Is route stable without template? | high | moderate | low | low unless stabilised |
| Is biological steering common? | can inhibit/select against | yes | yes | very common |
| Does it preserve route ambiguity? | low | moderate | high | very high |
| Does it function as precursor/storage? | rarely | sometimes endpoint | often intermediate | strongly |
| AMS best class | stable closure | directed closure | metastable closure | pre-closure reservoir |

## Score Assessment

Calcium carbonate polymorph family:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

CaCO3 strongly supports AMS because:

- same chemistry produces multiple closure geometries
- phase stability maps cleanly onto route completion
- ACC and vaterite show pre-closure and metastable closure behavior
- biological systems can steer polymorph selection
- carbonate phases connect material ontology to biomineral T1C function

Limitations:

- vaterite structure remains complex and needs deeper modelling
- ACC hydration states need separate route treatment
- quantitative transformation kinetics are not yet integrated
- organic-matrix controls need a dedicated T1C template map

## Score Pressure on Calcium Family

Previous calcium family score:

```text
8/10
```

Updated pressure:

```text
upward, but retain 8/10 for whole calcium family
```

Reason:

Calcium carbonate polymorphism is very strong, but whole-family calcium scoring also includes silicates, phosphates, signalling, membranes, and biological composites. A single strong subfamily should not move the whole family until hydroxyapatite and calcium silicate entries are also mapped.

## Next Artifact

The next useful artifact should be:

```text
ams-hydroxyapatite-collagen-nested-closure-map-v1.md
```

Reason:

Calcium carbonate establishes polymorph route geometry. Hydroxyapatite/collagen establishes nested T1B-to-T1C closure:

```text
mineral lattice
inside biological scaffold
under living regulation
forming tissue-level function
```
