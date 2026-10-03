# AMS Case Similarity and Clustering Note v1

## Purpose

This document compares the current formalised benchmark cases from:

- `ams-formalised-case-library-v1.md`

The aim is to identify:

- which cases cluster together
- which cases are genuine outliers
- which cases should be added next if the library expands

This is not yet a quantitative cluster analysis. It is a structured comparative note based on the now-stable case notation.

## Comparison Basis

Cases are compared across:

- zone composition
- dominance mode
- route classes
- obstruction classes
- route-reality grades
- flow structure

These are enough to identify meaningful family resemblance without pretending the library is already mathematically embedded.

## Current Case Set

Main benchmark cases:

- `air -> glass`
- `glass -> air`
- `air -> polished metal`
- `air -> oxidised metal`
- `glass -> crystal`
- `crystal -> air`

Focused subcases:

- `glass -> air [pocket-dominant]`
- `glass -> crystal [selective_success]`
- `glass -> crystal [mixed_frontier]`

## First-Pass Clusters

## Cluster C1: Broad Route-Dominant Anchors

Cases:

- `air -> glass`
- `crystal -> air`
- `glass -> crystal [selective_success]`

### Shared Features

- strong or reasonably strong `Z_A`
- `D1` dominance
- `R1` present centrally
- `O1` important
- route-reality at `G_A` or `G_B`
- completion-led flow remains plausible and often dominant

### Interpretation

These cases form the cleanest route-dominant cluster in the library.

They differ in detail:

- `air -> glass` is permissive-entry weighted
- `crystal -> air` is ordered-release weighted
- `glass -> crystal [selective_success]` is selective compatibility weighted

But the structural resemblance is real and useful.

### Current Role

- anchor cluster

## Cluster C2: Glass Frontier Mixed Cases

Cases:

- `glass -> air`
- `glass -> crystal`
- `glass -> crystal [mixed_frontier]`

### Shared Features

- `Z_A` and `Z_B` coexist strongly
- often weak `Z_C` or real fringe pressure
- `D4` common
- `R3` and `R5` both active
- `O2` and `O3` both active
- route-reality spans `G_B`, `G_C`, and `G_D`
- transition flows such as:
  - `Z_A -> Z_B`
  - `D4 -> Z_A`
  - `D4 -> Z_B`

### Interpretation

This is the main frontier cluster in the whole programme.

These cases are similar because they are not merely difficult. They are difficult in the same way:

- real route logic exists
- pseudo-route logic also exists
- one interface can sustain mixed local competition

### Current Role

- frontier cluster

## Cluster C3: Boundary Return / Reflection Cases

Cases:

- `air -> polished metal`
- `crystal -> air` partially

### Shared Features

- strong directional asymmetry
- `R4` significant
- `O4` significant
- route reality strong in one direction and weak in another
- cleaner dominance than in the glass frontier cluster

### Interpretation

This is not as large or as rich a cluster as the glass frontier cases, but it is a coherent one.

The core shared logic is:

- organised route structure survives
- but is biased away from outward completion

### Current Role

- return-side anchor cluster

## Cluster C4: Degraded / Fragmenting Cases

Cases:

- `air -> oxidised metal`
- `glass -> air [pocket-dominant]` partially at the edge

### Shared Features

- stronger `Z_C`
- weaker stable `Z_A`
- `O6` or strong drift toward `O6`
- route-reality at `G_C / G_D`
- broad weakening of route dominance

### Interpretation

This is the degradation-edge cluster.

It is less unified than the route-dominant anchors or the glass frontier cluster, but it is still useful because it captures:

- collapse of route coherence
- fringe and fragmentation pressure

### Current Role

- degradation contrast cluster

## Strongest Pairwise Similarities

## 1. `glass -> air` and `glass -> crystal`

This is the strongest pairwise similarity in the whole library.

Why:

- both are mixed-zone frontier cases
- both rely on `R3` / `R5`
- both rely on `O2` / `O3`
- both often sit in `D4`

These should now be treated as the main paired frontier cases of the programme.

## 2. `air -> glass` and `glass -> crystal [selective_success]`

This is a strong route-dominant similarity.

Why:

- both preserve viable completion
- both lean on `R1`
- both lean on selective route preservation rather than heavy pocket competition

## 3. `air -> polished metal` and `crystal -> air`

This is a useful directional-structure similarity.

Why:

- both preserve strong route organisation
- both involve meaningful return or directional bias logic
- neither behaves like the glass frontier family

## Strongest Outliers

## 1. `air -> polished metal`

This is the cleanest outlier in the library.

Why:

- it is the purest reflection-side anchor
- it is strongly directional
- it is much cleaner and less mixed than the glass frontier cases

It belongs in Cluster C3, but still behaves as a strong outlier relative to the overall library because its logic is so clean.

## 2. `air -> oxidised metal`

This is the strongest degradation outlier.

Why:

- it drifts more quickly toward fragmentation and diffuse degradation
- it does not preserve the same mixed route/pocket richness as the glass frontier cases

It is useful precisely because it prevents the library from becoming too glass-centric in its intuitions.

## What the Clustering Now Shows

## 1. The Library Already Has a Real Centre of Gravity

That centre is:

- the glass frontier cluster

This is not accidental. It reflects the repeated result that glass-like interfaces are the richest place to study:

- route reality
- pseudo-route activity
- mixed dominance
- local subregion competition

## 2. The Library Also Has Stable Anchors

The route-dominant cluster and return-side cluster give the programme:

- cleaner cases
- contrast cases
- stabilising benchmarks

That is important because the framework should not be built only from frontier complexity.

## 3. Degradation Cases Form Their Own Family

This matters because it prevents the model from mistaking:

- mixed frontier richness

for:

- simple degradation collapse

The oxidised-metal case is especially important here.

## What Cases Should Be Added Next?

If the case library expands, the next additions should not be random.

They should fill the current structural gaps.

## Priority Additions

### 1. `glass -> air [diffuse-dominant]`

Why:

- the library already has the pocket-dominant subcase
- it needs the clearer diffusion-dominant partner

This would strengthen Cluster C4 and separate `D2` from `D3` more sharply inside glass release.

### 2. `glass -> crystal [late-gate dominated]`

Why:

- the library already has:
  - selective success
  - mixed frontier

It would benefit from a cleaner blocked-route subcase centred on:

- `O2`
- `R3`

This would sharpen the frontier cluster internally.

### 3. `crystal -> air [ordered return dominated]`

Why:

- the current crystal case still mixes viable release and return-side structure
- a cleaner return-dominant subcase would strengthen Cluster C3

### 4. `air -> rough glass`

Why:

- this would sit between:
  - `air -> glass`
  - `glass -> air`
  - degraded glass release

It would help separate entry-side degradation from exit-side fragility.

## Lower-Priority Additions

### 5. `air -> crystal [selective-failure subcase]`

Useful, but lower priority because route-dominant anchors are already reasonably well represented.

### 6. `air -> partially oxidised metal`

Useful for degradation gradients, but slightly secondary until the main glass subcases are expanded.

## Most Important Clustering Judgment

The single strongest clustering judgment is this:

- the programme’s main frontier is not “interfaces in general”
- it is the glass-family mixed-interface frontier

That is where:

- `D4`
- `R3`
- `R5`
- `O2`
- `O3`

cluster most densely.

That should continue to guide priorities.

## Confidence

- confidence that the current case clustering is already meaningful: `9/10`
- confidence that the glass frontier cluster is the true centre of gravity: `9/10`
- confidence that `air -> polished metal` and `air -> oxidised metal` are useful outliers: `8/10`
- confidence that the next additions proposed above would strengthen the library well: `8/10`

## Recommendation

Keep the library focused.

Do not expand indiscriminately.

If new cases are added, add them to strengthen:

- the glass frontier cluster
- the return-side comparison cluster
- the degradation contrast cluster

in that order.

## Next Move

The best next artifact is:

- `ams-case-library-expansion-plan-v1.md`

That should formalise:

- which case additions are highest priority
- why they are needed
- what structural gap each one fills
- and what order they should be developed in.*** End Patch
