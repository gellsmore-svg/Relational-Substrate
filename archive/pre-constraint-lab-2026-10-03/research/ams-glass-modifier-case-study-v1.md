# AMS Glass Modifier Case Study v1

## Purpose

This document studies glass modifiers as the first targeted case study after completing the pilot element set and Round 7 recalibration.

The immediate focus is:

- sodium silicates
- magnesium silicates
- pure silica glass comparison

The reason is that sodium and magnesium silicates were both placed on the watchlist in:

- `ams-score-recalibration-log-v7.md`

They matter because they connect:

- element coverage
- glass networks
- interface modelling
- route classes
- obstruction character
- roughness and diffusion behaviour
- transmission and release

## Core Question

How do network modifiers alter the AMS glass model?

More specifically:

- do they mainly weaken route dominance?
- do they increase distributed weak routes?
- do they create more diffusing obstruction?
- do they increase pocketing or blocked apparent routes?
- do they alter entry and release differently?

## Baseline: Pure Silica Glass

## Conventional Role

Pure silica glass is a non-periodic but strongly connected network based on silicon-oxygen structures.

## AMS Baseline Reading

Pure silica glass currently reads as:

- distributed network closure
- non-periodic but real higher-order whole
- medium/high return-path support
- medium/high slip tolerance relative to crystal
- transmission by distributed permissive admissibility

## Formal Baseline Expression

```text
silica_glass
= Zones{Z_A,Z_C}
= Dom{D1/D3 depending surface}
= Route{R1,R2}
= Obst{O1,O5}
= Grade{G_A/G_B/G_C depending interface condition}
= Flow{Z_A->completion, Z_A->Z_C under rough/degraded conditions}
```

## Current Baseline Confidence

- score: `8`

Rationale:

- strongly supported by glass/interface modelling, but treated below the broader `SiO2` cross-level `9`.

## Sodium Silicate Modifier Case

## Conventional Role

Sodium modifies silicate networks. In broad terms, sodium can disrupt or alter the pure silica network and change properties such as melting behaviour, durability, ionic mobility, and glass structure.

## AMS Reading

Sodium behaves as a network modifier rather than as a primary network former.

AMS interpretation:

- sodium weakens or redistributes network continuity
- increases local pathway variability
- raises the importance of distributed weak routes
- may increase diffusing obstruction in interface conditions

## Vorton Relation Grammar

- closure type: modified silicate network closure
- coupling type: network-disruptive / network-adjusting ionic relation
- lock-up tendency: medium
- slip tolerance: increased relative to pure silica network
- strain distribution: less uniformly network-distributed than pure silica
- return-path character: more locally variable and modifier-sensitive

## Formalised Case Expression

```text
sodium_silicate_glass
= Zones{Z_A weak/med, Z_C, (Z_B local)}
= Dom{D3 or D4 depending modifier distribution}
= Route{R2, R3, (R5 local)}
= Obst{O5, O2, (O3 local)}
= Grade{G_B/G_C, (G_D local)}
= Flow{Z_A->Z_C, D4->Z_C, local Z_A->Z_B under pocketing defects}
```

## Interpretation

Compared with pure silica glass:

- `R1` weakens
- `R2` strengthens
- `O5` strengthens
- `D3` becomes more likely
- local `O2/R3` and `O3/R5` become more plausible where modifier distribution creates local incompatibilities

## Interface Consequences

### Entry

Sodium-modified glass likely makes entry more permissive in some respects but less cleanly route-dominant.

Expected shift:

- from strong `Z_A`
- toward `Z_A weak/med + Z_C`

### Transmission

Bulk transmission may remain viable, but route reality becomes more distributed and less strongly network-coherent.

Expected route shift:

- more `R2`
- less clean `R1`

### Release

Release likely becomes more sensitive to terminal-layer diffusion and local modifier distribution.

Expected release shift:

- more `O5`
- more `D3`
- possible local `O3/R5`

## Confidence

- current score: `7`
- post-study judgment: remains `7`, with upward pressure

Rationale:

- the case now fits the interface framework better than before, but needs specific composition and property comparisons before moving to `8`.

## Magnesium Silicate Modifier / Structural Case

## Conventional Role

Magnesium silicates are important mineral and material structures. Magnesium can participate in silicate mineral networks and contributes divalent coordination and structural constraint.

## AMS Reading

Magnesium behaves differently from sodium.

Where sodium often reads as a looser network modifier, magnesium reads more as:

- divalent constraint former
- structural stabiliser
- mineral-network participant

AMS interpretation:

- magnesium may strengthen local constraint relative to sodium
- preserve more structured mineral-network regions
- create more selective route pathways
- reduce simple diffusion compared with sodium-rich modification

## Vorton Relation Grammar

- closure type: divalent silicate-network participation
- coupling type: structural/mineral network coupling
- lock-up tendency: medium/high
- slip tolerance: lower than sodium-modified networks
- strain distribution: more constrained and mineral-structured
- return-path character: stronger local route preservation

## Formalised Case Expression

```text
magnesium_silicate
= Zones{Z_A, (Z_C), (Z_B local)}
= Dom{D1 or D4 depending structure}
= Route{R1, R3, (R2)}
= Obst{O1, O2, (O5)}
= Grade{G_B/G_C}
= Flow{Z_A->completion in structured regions, Z_A->late failure in strained regions}
```

## Interpretation

Compared with sodium silicates:

- `R1` is stronger
- `O1` is stronger
- `O5` is weaker
- `R2` is less dominant
- `O2/R3` may appear where structured routes fail under strain

## Interface Consequences

### Entry

Entry may be more selective than sodium-modified glass because local constraints are stronger.

Expected shift:

- more `O1`
- stronger `R1`
- less broad `R2`

### Transmission

Transmission may be more structured in mineral-like regions but less permissively distributed.

Expected route shift:

- `R1/R3`
- rather than `R2` dominance

### Release

Release may fail more by late blocking or selective mismatch than by broad diffusion.

Expected obstruction shift:

- more `O2`
- less `O5`

## Confidence

- current score: `7`
- post-study judgment: remains `7`, with upward pressure

Rationale:

- stronger distinction from sodium now exists, but specific magnesium silicate material studies are needed before `8`.

## Comparison Table

| Case | Network role | Dominant route shift | Dominant obstruction shift | Dominance tendency | Current score |
|---|---|---|---|---|---:|
| pure silica glass | network former | `R1 + R2` | `O1 + O5` | `D1/D3` | 8 |
| sodium silicate glass | loose modifier | stronger `R2`, local `R3/R5` | stronger `O5`, local `O2/O3` | `D3/D4` | 7 |
| magnesium silicate | structural/divalent participant | stronger `R1/R3` | stronger `O1/O2` | `D1/D4` | 7 |

## Strongest Findings

## 1. Sodium and Magnesium Should Not Be Treated as Generic Modifiers

This is the main result.

They modify network behaviour differently.

Sodium tends toward:

- distributed weakening
- diffusion
- route broadening

Magnesium tends toward:

- local constraint
- selective route preservation
- late-gate failure under strain

## 2. The Interface Framework Is Useful for Modifier Chemistry

The notation now helps say what changes:

- route class
- obstruction class
- dominance mode
- release/entry behaviour

That is a real gain over loose “network modified” language.

## 3. Scores Should Not Move Yet

Both sodium and magnesium silicates are stronger after this study, but not enough to raise scores.

They need:

- more specific composition studies
- direct material comparisons
- perhaps optical/interface examples

## 4. Glass Modifier Cases Are Now a Strong Candidate for Phase 2 Depth

This may be more valuable than immediately adding many new elements.

The modifier logic could become one of the strongest bridges between:

- element chemistry
- material behaviour
- interface modelling

## Recalibration Note

No score change yet.

Current status:

- sodium silicates: `7`, upward pressure
- magnesium silicates: `7`, upward pressure
- pure silica glass: `8`, stable
- `SiO2`: `9`, stable

## Current Weak Points

## 1. Composition Sensitivity

The current model does not yet distinguish:

- low sodium content
- high sodium content
- mixed sodium/magnesium modifier systems

## 2. Property-Specific Behaviour

Transmission, durability, viscosity, melting behaviour, and surface roughness may not all shift in the same way.

## 3. Lack of Direct Empirical Table

The study is structurally useful but still needs a later conventional-material comparison table.

## Confidence

- confidence that sodium and magnesium modifiers differ meaningfully in AMS terms: `8/10`
- confidence that sodium tends toward `O5/R2/D3`: `7/10`
- confidence that magnesium tends toward `O1/O2/R1/R3`: `7/10`
- confidence that scores should hold at `7` for now: `9/10`

## Recommendation

Do not raise scores yet.

Instead, treat glass modifiers as a priority depth track.

## Next Move

The best next artifact is:

- `ams-glass-modifier-composition-gradient-v1.md`

That should examine:

- pure silica
- low sodium modification
- high sodium modification
- magnesium-rich silicate
- mixed modifier systems

and ask how route/obstruction/dominance profiles shift along composition gradients.*** End Patch
