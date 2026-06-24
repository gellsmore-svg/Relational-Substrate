# AMS Optical Parameter Sweep v2

## Purpose

This document reruns the main optical parameter sweep using the refined boundary, coupling, and resonance subvariables.

Round 1 of the sweep showed that the coarse variables:

- `B`
- `J`
- `Q`

were carrying too much at once.

This second sweep asks whether the new subvariables actually sharpen the optical modelling:

- or whether the same uncertainty remains under new names

## Subvariables In Scope

The main refined variables are:

- `B_in` = boundary entry sensitivity
- `B_out` = boundary exit sensitivity
- `B_ref` = reflective boundary sensitivity
- `B_coh` = boundary coherence dependence
- `J_loc` = local coupling strength
- `J_dist` = distributed whole coupling
- `J_surf` = surface-layer coupling
- `Q_coh` = coherent resonance compatibility
- `Q_coll` = collective response readiness
- `Q_dest` = destabilising resonance susceptibility

The older variables still matter:

- `R`
- `S`
- `D`

## Sweep Rule

Each benchmark is rerun with:

- dominant subvariables
- weakly constrained subvariables
- a judgment about whether the refinement improved explanatory discrimination

## Sweep Case 1: Glass Transmission

### Current candidate profile

- `R`: medium to high
- `S`: medium to high
- `D`: high
- `B_in`: medium
- `B_out`: medium
- `B_ref`: low
- `B_coh`: low to medium
- `J_loc`: medium
- `J_dist`: medium
- `J_surf`: low
- `Q_coh`: medium
- `Q_coll`: low
- `Q_dest`: low to medium

### What the refinement clarifies

The subvariable split improves this case in three ways:

1. it distinguishes transmissive entry and exit from reflectivity
2. it shows that glass likely depends on distributed whole coupling more than surface-layer coupling
3. it clarifies that the key resonance variable here is likely `Q_coh`, not `Q_coll`

### Current dominant variables

- `R`
- `S`
- `D`
- `J_dist`
- `Q_coh`

### Weakly constrained variables

- exact relation between `B_in` and `B_out`
- exact role of low versus medium `B_coh`

### Round 2 judgment

Improved.

The case now looks cleaner:

- glass transmission is not a weak reflection case
- it is a bulk-distributed pathway case with meaningful but secondary boundary entry/exit shaping

## Sweep Case 2: Crystal Transmission

### Current candidate profile

- `R`: high
- `S`: medium
- `D`: low in bulk / high at defects
- `B_in`: medium
- `B_out`: medium
- `B_ref`: low
- `B_coh`: medium
- `J_loc`: high
- `J_dist`: high
- `J_surf`: low to medium
- `Q_coh`: medium
- `Q_coll`: low
- `Q_dest`: low

### What the refinement clarifies

The subvariable split improves this case by distinguishing:

- strong distributed whole coupling
- from low surface-reflective sensitivity

This helps make crystal transmission look less like “high order in general” and more like:

- strong nested bulk coherence with relatively low reflective bias

### Current dominant variables

- `R`
- `J_loc`
- `J_dist`
- structured `S`

### Weakly constrained variables

- whether `B_coh` is materially more important than currently assumed
- whether some crystal families require higher `Q_coh`

### Round 2 judgment

Improved.

The crystal case now looks more explicitly bulk-ordered and less boundary-driven than the reflective metal case.

## Sweep Case 3: Metal Reflection

### Current candidate profile

- `R`: medium
- `S`: low to medium
- `D`: medium to high
- `B_in`: high
- `B_out`: not primary
- `B_ref`: very high
- `B_coh`: very high
- `J_loc`: medium
- `J_dist`: high
- `J_surf`: high to very high
- `Q_coh`: medium
- `Q_coll`: high
- `Q_dest`: medium

### What the refinement clarifies

This is the biggest gain of the entire subvariable split.

The case is now much more explicit:

- reflection is not just “high boundary sensitivity”
- it appears to require:
  - high reflective boundary bias
  - high surface coherence dependence
  - strong surface-layer coupling
  - strong collective response readiness

### Current dominant variables

- `B_ref`
- `B_coh`
- `J_surf`
- `Q_coll`

### Weakly constrained variables

- whether `R` is merely supportive or more structurally important
- exact role of `Q_dest` in imperfect reflective media

### Round 2 judgment

Strongly improved.

This is the clearest case where the subvariables genuinely increased explanatory discrimination.

## Sweep Case 4: Defect-Sensitive Scattering

### Current candidate profile

- `R`: medium
- `S`: medium
- `D`: very high
- `B_in`: low to medium
- `B_out`: low to medium
- `B_ref`: low
- `B_coh`: low to medium
- `J_loc`: medium
- `J_dist`: medium
- `J_surf`: low
- `Q_coh`: low to medium
- `Q_coll`: low
- `Q_dest`: medium

### What the refinement clarifies

The subvariable split confirms that scattering is not mainly a reflective-boundary case.

It looks more like:

- a pathway-disruption case
- with possible local destabilising response when `Q_dest` rises

### Current dominant variables

- `D`
- `R`
- `S`
- secondarily `Q_dest`

### Weakly constrained variables

- exact threshold between `Q_dest`-driven scattering and more purely defect-driven scattering

### Round 2 judgment

Improved modestly.

The subvariables help by confirming what scattering is *not*, even more than by fully explaining what it is.

## Sweep Case 5: Transparent Boundary Entry

### Current candidate profile

- `R`: medium
- `S`: medium
- `D`: medium
- `B_in`: high
- `B_out`: medium
- `B_ref`: low to medium
- `B_coh`: medium
- `J_loc`: medium
- `J_dist`: medium
- `J_surf`: low to medium
- `Q_coh`: medium
- `Q_coll`: low
- `Q_dest`: low

### What the refinement clarifies

This case was underconstrained in Round 1. The new subvariables do help by isolating:

- entry sensitivity
- from reflective bias

That is useful, but the case is still weak overall.

### Current dominant variables

- `B_in`
- `R`
- `S`

### Weakly constrained variables

- almost everything else
- especially the interaction between `B_in`, `J_loc`, and `Q_coh`

### Round 2 judgment

Still underconstrained, but better framed.

We now know the weakness more precisely:

- entry geometry is the problem, not just “boundary” in general

## Sweep Case 6: Surface-Degraded Reflection

### Current candidate profile

- `R`: medium
- `S`: low to medium
- `D`: high
- `B_in`: medium to high
- `B_out`: not primary
- `B_ref`: high but degraded
- `B_coh`: reduced from high to medium or lower
- `J_loc`: medium
- `J_dist`: high in bulk
- `J_surf`: reduced
- `Q_coh`: low to medium
- `Q_coll`: reduced
- `Q_dest`: medium to high

### What the refinement clarifies

This case improves a lot with subvariables because it can now be described as:

- bulk metallic order still present
- but reflective boundary bias, surface coherence, and collective response readiness partially degraded

That is much more precise than “more disorder.”

### Current dominant variables

- `B_coh`
- `J_surf`
- `Q_coll`
- `D`

### Weakly constrained variables

- exact relation between surface oxidation and reduced `B_ref`
- how much `Q_dest` rises in real degraded surfaces

### Round 2 judgment

Strongly improved.

This is now one of the more useful comparative reflection cases.

## Main Comparative Results

### 1. The subvariable split was worth doing

This is now clear.

The largest gains are in:

- metal reflection
- degraded reflective surfaces
- glass transmission

### 2. Reflection is now much more sharply characterised

The reflection cases are increasingly dominated by:

- `B_ref`
- `B_coh`
- `J_surf`
- `Q_coll`

That is a much more disciplined claim than earlier rounds.

### 3. Transmission remains a bulk-distributed phenomenon in the current model

The transmission cases are still dominated by:

- `R`
- `S`
- `J_dist`
- secondarily `Q_coh`

That supports the current structural distinction between transmission and reflection.

### 4. Defect logic remains central across the whole optical field

This remains one of the strongest stable results of the optical programme.

`D` is not merely a modifier. It is one of the major cross-cutting discriminators.

## Current Optical Hypotheses After Round 2

### Glass transmission

Best current form:

- a disordered but real whole with sufficient return-path strength, slip tolerance, and distributed coupling to support propagation through admissible bulk pathways, while remaining highly defect-sensitive

### Crystal transmission

Best current form:

- a more strongly ordered nested whole with high return-path strength and high bulk-distributed coupling, supporting regularised transmissive propagation

### Metal reflection

Best current form:

- a highly boundary-sensitive, surface-coherent, strongly surface-coupled whole that produces collective reflective response

### Degraded metal reflection

Best current form:

- a reflective whole whose bulk identity persists while boundary coherence, surface coupling, and collective response readiness are degraded

## Remaining Bottlenecks

The current main modelling bottlenecks are:

1. exact geometry of entry sensitivity
2. exact geometric meaning of surface-layer coupling
3. sharper distinction between `Q_coh` and `Q_coll`
4. relation between oxidation and `B_ref`

These are now narrow enough to target directly.

## Recommended Next Move

The next correct artifact should be:

- `ams-reflection-vs-transmission-discriminator-table-v1.md`

That document should force a direct side-by-side contrast between the dominant variables and geometry conditions for:

- glass transmission
- crystal transmission
- metal reflection
- degraded metal reflection

That should expose whether the current discrimination is genuinely sharp or still partly rhetorical.
