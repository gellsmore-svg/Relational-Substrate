# AMS Aluminium Family Score Recalibration v1

## Purpose

This recalibration records the aluminium material-family score move from:

```text
8/10
```

to:

```text
8.5/10
```

It follows the first aluminium workstream:

- `ams-aluminium-material-family-entry-v1.md`
- `ams-aluminium-charge-compensation-regime-map-v1.md`
- `ams-sodium-aluminosilicate-composition-series-map-v1.md`
- `ams-aluminosilicate-ion-exchange-strengthening-route-map-v1.md`

## Previous Score

```text
aluminium material family: 8/10
confidence: moderate-high
pressure: upward
```

Original rationale:

Aluminium was already strong because it acts as a conditional network former, charge-coupled gate, topology stiffener, modifier competitor, ion-exchange regulator, and durability enhancer in aluminosilicate systems.

The score was held at 8 until specific subcases were mapped.

## Supporting Subfamilies

### 1. Aluminium Charge-Compensation Regime Map

File:

```text
ams-aluminium-charge-compensation-regime-map-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main AMS result:

```text
Aluminium is a charge-conditioned topology switch.
```

Regime summary:

```text
modifier excess
=> Al joins the network, excess modifier opens weak routes
=> R1/R2, O1/O5, D1/D3/D4

ideal compensation
=> AlO4- is charge-supported
=> R1/O1/D1

modifier deficit / Al excess
=> higher-coordination Al, triclusters, topology complications
=> R3/R4, O2/O4, D4

thermal / pressure / deformation shift
=> dynamic Al coordination change
=> route reconfiguration and stress accommodation
```

Why it matters:

This subcase shows that aluminium content alone is insufficient. Aluminium's role depends on charge compensation, modifier availability, coordination state, and history.

### 2. Sodium Aluminosilicate Composition Series

File:

```text
ams-sodium-aluminosilicate-composition-series-map-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main AMS result:

```text
increasing Al2O3 shifts sodium from weak-route modifier to charge-compensation participant.
```

Route progression:

```text
low Al
=> R2/O5/D3
=> sodium-opened weak routes

moderate Al
=> R2/R1/D4
=> mixed modifier/compensation field

near ideal compensation
=> R1/O1/D1
=> aluminium-supported backbone
```

Why it matters:

This gives aluminium a concrete composition-driven route transition tied to observed trends:

- NBO/T decrease
- Tg increase
- network connectivity increase
- stiffness/hardness increase
- densification behavior change
- ion-exchange behavior change

### 3. Aluminosilicate Ion-Exchange Strengthening

File:

```text
ams-aluminosilicate-ion-exchange-strengthening-route-map-v1.md
```

Score:

```text
8.5/10
confidence: moderate-high
```

Main AMS result:

```text
chemical strengthening requires controlled R2 exchange inside strong R1 stress-retention matrix.
```

Aluminium role:

```text
A5 = ion-exchange regulator
```

Route tension:

```text
too open
=> exchange deep but stress retention weak

too closed
=> stress retention possible but exchange shallow

balanced
=> useful K-for-Na substitution and retained surface compression
```

Why it matters:

This subcase connects aluminium topology directly to industrial surface strengthening, compressive stress, hardness, diffusion depth, and crack suppression.

## Recalibration Decision

Updated score:

```text
aluminium material family: 8.5/10
confidence: moderate-high
```

Reason:

Aluminium now has three strong mapped subcases:

```text
charge-compensation topology
composition-driven route transition
ion-exchange strengthening
```

These cover:

- network topology
- charge compensation
- NBO suppression
- modifier role switching
- ion mobility control
- mechanical strengthening
- surface compressive stress
- glass durability and stiffness

That breadth justifies the move from 8 to 8.5.

## Why Not 9

Do not move aluminium above 8.5 yet.

Reasons:

```text
1. Natural aluminosilicate minerals and clays are not yet mapped.
2. Aluminium biological incompatibility and toxicity boundaries are not yet mapped.
3. Calcium aluminosilicate Ca/Al regime cases are not yet mapped in detail.
4. Peraluminous Al-excess composition series need deeper treatment.
5. Surface hydration, weathering, and degradation after ion exchange remain unmapped.
6. Quantitative NBO/T and coordination tables have not yet been imported.
```

The family is strong, but still glass-heavy.

## Score Log Entry

```text
aluminium family recalibration v1:

previous_score: 8/10
updated_score: 8.5/10
confidence: moderate-high
pressure: upward but capped below 9

supporting_subfamilies:
- aluminium charge-compensation regimes: 8.5
- sodium aluminosilicate composition series: 8.5
- aluminosilicate ion-exchange strengthening: 8.5

reason:
aluminium acts as a charge-conditioned topology switch and ion-exchange regulator across aluminosilicate material systems.
```

## Comparative Position

Current relevant family scores:

```text
mixed Na/Mg silicate family: 7/10
Na/Mg aluminosilicate series: 7.5/10
calcium material family: 8.5/10
aluminium material family: 8.5/10
calcium carbonate polymorph family: 8.5/10
hydroxyapatite-collagen nested closure: 9/10
```

Interpretation:

Calcium and aluminium now sit as high-confidence bridge families:

```text
calcium
=> bridge-forming constraint carrier across mineral, glass, and biological composites

aluminium
=> charge-conditioned topology switch across glass, transport, and strengthening systems
```

## Next Workstream Options

### Option A: Silicon Family Consolidation

Artifact:

```text
ams-silicon-material-family-entry-v1.md
```

Purpose:

Consolidate silicon as the main network-forming backbone across silica, silicates, glass, semiconductors, biological silica, and interface optics.

Value:

Very high. Silicon is foundational for T1B material structure and optical/interface work.

### Option B: Aluminium Natural Mineral / Clay Map

Artifact:

```text
ams-aluminium-clay-and-aluminosilicate-mineral-map-v1.md
```

Purpose:

Extend aluminium beyond glass into clays, feldspars, zeolites, and natural aluminosilicate structures.

Value:

Would broaden aluminium family beyond industrial glass.

### Option C: Calcium Signalling and Membrane-Adjacent Roles

Artifact:

```text
ams-calcium-signalling-membrane-gate-map-v1.md
```

Purpose:

Extend calcium from material closure into biological regulation.

Value:

Could push calcium toward 9.

## Recommended Next Artifact

Recommended next:

```text
ams-silicon-material-family-entry-v1.md
```

Reason:

Silicon is now the natural consolidation point. The previous workstreams repeatedly depend on silicon as:

- silicate backbone
- glass network former
- route-closure reference
- optical transmission medium
- silica/calcium/sodium/aluminium comparison baseline
- possible biological silica case
- semiconductor/interface bridge

Silicon should become the reference family against which calcium, aluminium, sodium, and magnesium modifier roles are compared.
