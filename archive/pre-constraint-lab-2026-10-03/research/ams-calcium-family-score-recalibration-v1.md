# AMS Calcium Family Score Recalibration v1

## Purpose

This recalibration records the calcium material-family score move from:

```text
8/10
```

to:

```text
8.5/10
```

It follows the first calcium workstream:

- `ams-calcium-material-family-entry-v1.md`
- `ams-calcium-carbonate-polymorph-route-map-v1.md`
- `ams-hydroxyapatite-collagen-nested-closure-map-v1.md`
- `ams-calcium-silicate-soda-lime-route-map-v1.md`

## Previous Score

```text
calcium material family: 8/10
confidence: moderate-high
pressure: upward
```

Original rationale:

Calcium was already strong because it connects silicate glasses, carbonate polymorphs, phosphate minerals, hydroxyapatite, biomineral composites, and biological mineralization.

At the previous stage, the score was held at 8 because the subfamilies had not yet been mapped in enough detail.

## New Supporting Subfamilies

### 1. Calcium Carbonate Polymorph Family

File:

```text
ams-calcium-carbonate-polymorph-route-map-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main AMS result:

```text
same chemistry
=> multiple closure geometries
=> polymorph-specific route states
```

Route map:

```text
calcite
=> R1/O1/D1/G_A
=> stable compact closure

aragonite
=> R1/R3, O1/O2, D1/D4
=> directed anisotropic closure

vaterite
=> R3/R5, O2/O3, D4/D2
=> metastable/polytypic closure

ACC
=> R2/R5/R6, O3/O5/O6, D2/D4
=> pre-closure reservoir
```

Why it matters:

Calcium carbonate gives AMS a strong geometry test because formula identity is not enough. The same chemical composition can enter different retained closure states depending on route history, environment, and biological templating.

### 2. Hydroxyapatite-Collagen Nested Closure

File:

```text
ams-hydroxyapatite-collagen-nested-closure-map-v1.md
```

Score:

```text
9/10
confidence: high
```

Main AMS result:

```text
T1B mineral closure
inside
T1C biological scaffold and regulation
```

Nested closure levels:

```text
1. Ca/P ion availability
2. matrix vesicle nucleation gate
3. hydroxyapatite crystal growth
4. collagen scaffold admission
5. mineralized collagen composite
6. tissue-level bone matrix
```

Why it matters:

Hydroxyapatite/collagen is one of the strongest AMS cases because it demonstrates mineral order being generated, admitted, oriented, propagated, and regulated by living biological process.

This directly supports the T1B/T1C boundary architecture.

### 3. Calcium Silicate / Soda-Lime Route Map

File:

```text
ams-calcium-silicate-soda-lime-route-map-v1.md
```

Score:

```text
8/10
confidence: moderate-high
```

Main AMS result:

```text
Na opens.
Mg gates.
Ca bridges.
Si closes.
```

Soda-lime profile:

```text
M1 silica backbone
+ M2 sodium weak-route opener
+ M3_Ca bridge-stabilising modifier
=> workable and durable amorphous retained form
```

Route map:

```text
primary_route: R1/R2
secondary_route: R3 at local gates
primary_obstruction: O1
secondary_obstruction: O2/O5
dominance: D1/D4
route_grade: G_A/G_B
```

Why it matters:

This subfamily shows calcium's non-biological T1B role as a bridge-stabilising modifier in one of the most common human-used glass systems.

It also reconnects calcium to the existing glass/interface research track.

## Recalibration Decision

Updated score:

```text
calcium material family: 8.5/10
confidence: moderate-high
```

Reason:

The calcium family now has three independently strong mapped subfamilies:

```text
carbonate polymorph closure geometry
hydroxyapatite-collagen biological nested closure
silicate/soda-lime glass modifier-stabiliser behavior
```

These cover:

- mineral polymorphism
- biomineralization
- biological tissue formation
- composite mechanics
- non-biological glass stabilisation
- route regulation across T1B and T1C

That breadth justifies the move from 8 to 8.5.

## Why Not 9

Do not move the whole calcium family above 8.5 yet.

Reasons:

```text
1. Calcium signalling has not been mapped.
2. Calcium membrane-adjacent roles have not been mapped.
3. Calcium surface/interface optics are not yet deeply modelled.
4. Calcium silicate composition curves need more detail.
5. Hydroxyapatite pathology and defective mineralization need separate treatment.
6. Carbonate organic-template controls need more specific biological cases.
```

The family is broad and strong, but not yet fully saturated.

## Score Log Entry

```text
calcium family recalibration v1:

previous_score: 8/10
updated_score: 8.5/10
confidence: moderate-high
pressure: upward but capped below 9

supporting_subfamilies:
- calcium carbonate polymorphs: 8.5
- hydroxyapatite-collagen nested closure: 9
- calcium silicate / soda-lime glass: 8

reason:
calcium repeatedly acts as bridge-forming constraint carrier across mineral, glass, biomineral, and tissue-level domains.
```

## Comparative Position

Current relevant family scores:

```text
mixed Na/Mg silicate family: 7/10
Na/Mg aluminosilicate series: 7.5/10
calcium carbonate polymorph family: 8.5/10
hydroxyapatite-collagen nested closure: 9/10
calcium silicate / soda-lime subcase: 8/10
calcium material family: 8.5/10
```

Interpretation:

Calcium is currently stronger than mixed Na/Mg as a whole-family AMS case because it has broader cross-domain reach and stronger T1B-to-T1C evidence.

## Next Workstream Options

### Option A: Calcium Signalling and Membrane-Adjacent Roles

Artifact:

```text
ams-calcium-signalling-membrane-gate-map-v1.md
```

Purpose:

Extend calcium from material closure into biological regulation.

Value:

Could push calcium toward 9 if handled well.

### Option B: Aluminium Material Family Entry

Artifact:

```text
ams-aluminium-material-family-entry-v1.md
```

Purpose:

Map aluminium's role in aluminosilicates, charge compensation, glass strengthening, clay/mineral structures, and biological toxicity boundaries.

Value:

Strong next element because Al appears repeatedly in glass, Na/Mg transport, and network connectivity.

### Option C: Calcium Silicate Composition Curve

Artifact:

```text
ams-calcium-silicate-composition-gradient-v1.md
```

Purpose:

Map increasing CaO in silicate/aluminosilicate systems to NBO/T, durability, viscosity, crystallisation, and route classes.

Value:

Strengthens the glass/interface side before moving to another element.

## Recommended Next Artifact

Recommended next:

```text
ams-aluminium-material-family-entry-v1.md
```

Reason:

Aluminium is now the most natural continuation because it appears as a recurring gate/backbone factor in:

- Na/Mg aluminosilicate transport
- calcium aluminosilicate glasses
- soda-lime and cover-glass strengthening
- charge-compensation structures
- bridging oxygen / non-bridging oxygen balance

It will also clarify several existing calcium and Na/Mg claims.
