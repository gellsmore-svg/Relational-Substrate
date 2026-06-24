# AMS Reflection vs Transmission Discriminator Table v1

## Purpose

This document puts the current optical cases side by side in one explicit comparison table.

The goal is simple:

- test whether the current difference between transmission and reflection is genuinely discriminating
- or whether the programme is still partly relying on persuasive wording rather than sharp contrast

The cases compared here are:

- glass transmission
- crystal transmission
- metal reflection
- degraded metal reflection

## Comparison Table

| Feature | Glass Transmission | Crystal Transmission | Metal Reflection | Degraded Metal Reflection |
|---|---|---|---|---|
| Whole type | disordered but real transmissive whole | ordered nested transmissive whole | reflective boundary whole with collective surface response | reflective whole with degraded surface coherence |
| Dominant family set | `G + D + F` | `C + G + F` | `H + E + F` | `H + E + F` |
| Bulk vs boundary emphasis | bulk-distributed | bulk-ordered | surface-dominant | bulk persists, surface degrades |
| `R` return-path strength | medium to high | high | medium | medium |
| `S` slip tolerance | medium to high | medium | low to medium | low to medium |
| `D` defect sensitivity | high | low in bulk, high at defects | medium to high | high |
| `B_in` boundary entry sensitivity | medium | medium | high | medium to high |
| `B_out` boundary exit sensitivity | medium | medium | not primary | not primary |
| `B_ref` reflective boundary sensitivity | low | low | very high | high but degraded |
| `B_coh` boundary coherence dependence | low to medium | medium | very high | reduced from very high |
| `J_loc` local coupling | medium | high | medium | medium |
| `J_dist` distributed whole coupling | medium | high | high | high in bulk |
| `J_surf` surface-layer coupling | low | low to medium | high to very high | reduced |
| `Q_coh` coherent resonance compatibility | medium | medium | medium | low to medium |
| `Q_coll` collective response readiness | low | low | high | reduced |
| `Q_dest` destabilising resonance susceptibility | low to medium | low | medium | medium to high |
| Role of defects | clarity degradation and scattering | local disruption of otherwise regular propagation | reduced reflection quality, roughness effects | central to degradation of reflectivity |
| Best current AMS description | distributed admissible pathways through a disordered whole | regular nested admissible pathways through an ordered whole | collective reflective response at a coherent boundary layer | partial loss of reflective surface coherence while bulk identity remains |

## First Discriminator Results

### 1. Reflection and transmission are no longer just different words

The current table shows a real split:

- transmission cases are dominated by:
  - `R`
  - `S`
  - `J_dist`
- reflection cases are dominated by:
  - `B_ref`
  - `B_coh`
  - `J_surf`
  - `Q_coll`

That is a substantial gain over the earlier programme state.

### 2. Glass and crystal are now distinguishable without changing ontology

The contrast is currently:

- glass: disordered but permissive bulk pathways, higher defect significance
- crystal: ordered nested pathways, lower bulk defect burden, stronger regular whole-order

That is important because it keeps both inside one propagation grammar while still differentiating them.

### 3. Degraded metal reflection is now one of the best diagnostic cases

This case is especially useful because it preserves:

- bulk metallic identity

while degrading:

- `B_coh`
- `J_surf`
- `Q_coll`

That makes it a strong pressure test for whether the reflection model is really surface-coherence-driven.

### 4. The weakest column is still transmissive boundary entry / exit

The table helps expose the least sharp part of the current programme:

- `B_in`
- `B_out`

These are still present mostly as placeholders rather than genuinely well-constrained discriminators.

## Strongest Current Discriminators

The strongest currently useful discriminators are:

1. `B_ref`
2. `B_coh`
3. `J_surf`
4. `Q_coll`
5. `R`
6. `J_dist`

Interpretive summary:

- reflection is now best distinguished by the first four
- transmission is now best distinguished by the last two, together with `S`

## Current Weak Discriminators

The weakest or least settled are:

- `B_in`
- `B_out`
- exact role of `Q_coh` in transmissive media
- exact role of `R` in reflection

These are now the best targets for further refinement.

## Current Best Hypotheses After Direct Comparison

### Glass Transmission

Best current hypothesis:

- a disordered but still coherent whole supports transmission when distributed admissible pathways remain sufficiently continuous, with defects mainly degrading rather than abolishing that continuity

### Crystal Transmission

Best current hypothesis:

- a more regular nested whole supports transmission through stronger ordered pathway continuity and higher distributed coupling

### Metal Reflection

Best current hypothesis:

- a highly coupled whole produces reflection when the boundary layer remains coherent enough to sustain strong collective surface response

### Degraded Metal Reflection

Best current hypothesis:

- reduced reflection quality emerges when surface coherence, surface-layer coupling, and collective response readiness are degraded even while the bulk metallic whole persists

## What This Table Proves And Does Not Prove

### What it now supports

- the optical programme is becoming genuinely discriminating
- reflection and transmission are now being separated by different dominant variables
- degraded reflection is being treated as a real structural case, not just “more disorder”

### What it does not yet support

- final mathematics
- a complete theory of entry and exit effects
- a settled account of the exact role of resonance in all optical cases

## Recommended Next Move

The next correct artifact should be:

- `ams-entry-exit-interface-cases-v1.md`

That should focus directly on the weakest current area:

- transmissive boundary entry and exit

and try to sharpen:

- `B_in`
- `B_out`
- their relation to `R`, `S`, and `Q_coh`
