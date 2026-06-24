# AMS Element and Material Coverage Plan v1

## Purpose

This document defines how to resume the original larger AMS technical programme:

- element-by-element
- molecule/material by molecule/material

using the interface framework developed in the recent optical modelling sequence.

The goal is to prevent the programme from returning to loose prose after the interface work achieved a stable modelling toolkit.

## Context

The original technical aim was to examine:

- major T1B formations for each element
- non-persistent vorton topologies
- T1C formations and higher-order stress tests

The recent interface work produced reusable tools for:

- boundary entry and exit
- transmission and reflection
- route reality
- obstruction character
- mixed-interface subregions
- compact formalised case notation

The next task is to bring those tools back into broader element/material coverage.

## Current Toolkits Available

## 1. Existing T1B Corpus

Current file:

- `ams-pilot-t1b-corpus-v1.md`

Current pilot coverage:

- H
- C
- O
- Fe

## 2. Existing T1C Corpus

Current file:

- `ams-t1c-stress-test-corpus-v1.md`

Current coverage includes:

- water networks
- quartz
- glass
- metallic iron / grain structures
- magnetite
- polymers
- membranes
- alloys
- catalytic surfaces
- biological macromolecular assemblies

## 3. Interface Modelling Toolkit

Core files:

- `ams-interface-formalisation-sketch-v1.md`
- `ams-formalised-case-library-v1.md`
- `ams-expanded-case-library-update-v1.md`
- `ams-expanded-library-scoreboard-v1.md`

Key modelling layer:

- variables
- zones
- route classes
- obstruction classes
- dominance modes
- route-reality grades
- transition flows

## 4. Score Recalibration System

Current files:

- `ams-score-recalibration-log-v1.md`
- `ams-score-recalibration-log-v2.md`
- `ams-score-recalibration-log-v3.md`
- `ams-score-recalibration-log-v4.md`
- `ams-score-recalibration-log-v5.md`
- `ams-score-recalibration-log-v6.md`

The score system should continue to be used:

- conservatively
- comparatively
- with explicit recalibration logs

## Coverage Principle

Do not try to cover the whole periodic table in one pass.

Instead, proceed in staged element/material clusters that maximise contrast.

The aim is not encyclopaedic completeness first. The aim is:

- broad enough coverage to stress the framework
- deep enough modelling to force refinement

## Proposed Coverage Phases

## Phase 1: Complete the Pilot Element Set

The original pilot set included:

- H
- C
- N
- O
- Na
- Mg
- Si
- P
- S
- Fe

Current T1B coverage is strongest for:

- H
- C
- O
- Fe

So Phase 1 should complete:

- N
- Na
- Mg
- Si
- P
- S

## Phase 2: Add Interface-Relevant Metals

After the pilot set, add metals important for reflection, conduction, surface effects, and oxidation:

- Al
- Cu
- Ag
- Au
- Ti
- Ni
- Cr

Reason:

- these stress the polished/oxidised/surface-response side of the interface framework

## Phase 3: Add Network and Glass-Relevant Elements

Add elements important for glass, ceramic, and network materials:

- B
- Al
- Ca
- K
- Li

Reason:

- these stress the glass frontier, network formation, and modifier effects

## Phase 4: Add Biological and Functional Elements

Add elements central to biological function and catalytic/coordination behaviour:

- Cl
- Ca
- Zn
- Cu
- Mn
- Co
- I

Reason:

- these stress membranes, ions, enzymes, biological macromolecules, and functional specificity

## Phase 5: Broader Periodic Table Expansion

Only after the above phases should the programme consider broader periodic-table coverage.

At that stage, coverage can be grouped by:

- alkali metals
- alkaline earths
- transition metals
- halogens
- noble gases
- lanthanides / actinides if relevant

## Per-Element Record Structure

Each element should receive a structured record with the following sections.

## 1. Conventional Role Summary

Briefly identify:

- basic bonding tendencies
- common oxidation or valence behaviour
- common molecular/material roles
- major known material behaviours

This should remain observed/conventional, not AMS inference.

## 2. Top Representative T1B Formations

List up to 10 representative formations.

Selection should prioritise:

- abundance
- structural diversity
- bonding diversity
- material relevance
- biological or optical relevance where applicable

Each formation should include:

- conventional structure
- persistence conditions
- polarity/symmetry where relevant
- expected vorton relation grammar
- confidence score

## 3. Vorton Relation Grammar

For each formation, describe:

- closure type
- coupling type
- lock-up tendency
- slip tolerance
- strain distribution
- return-path character

Use the existing language from the T1B corpus, but tighten with the interface notation where useful.

## 4. Non-Persistent Topology Interactions

For each element family, note likely interactions with:

- diffuse topologies
- collapse-prone topologies
- overconstrained topologies
- threshold-fragile topologies
- metastable-only topologies

Use:

- `ams-non-persistent-vorton-topology-atlas-v1.md`

as the reference.

## 5. T1C Escalation Targets

For each element, identify material or higher-order cases such as:

- crystals
- glasses
- oxides
- alloys
- polymers
- membranes
- catalytic surfaces
- biological complexes

## 6. Interface/Optical Relevance

Where applicable, use the formal notation from the interface case library:

- zones
- dominance modes
- route classes
- obstruction classes
- route-reality grades
- flows

This is especially important for:

- glass-related elements
- metals
- oxides
- surfaces
- crystals

## 7. Confidence and Recalibration Notes

Each element record should end with:

- confidence scores
- comparison anchors
- reasons for score
- open questions
- likely recalibration triggers

## Immediate Next Corpus File

The best next concrete corpus file is:

- `ams-pilot-t1b-corpus-extension-v1.md`

Scope:

- N
- Na
- Mg
- Si
- P
- S

Why:

- completes the original pilot set
- adds major missing chemistries:
  - nitrogen bonding and atmospherics
  - sodium ionic behaviour
  - magnesium structural/biological roles
  - silicon network/glass relevance
  - phosphorus biological/oxidation roles
  - sulfur redox and bonding diversity

## Priority T1B Formations for Extension

## Nitrogen

Candidate formations:

- `N2`
- `NH3`
- `NO`
- `NO2`
- `N2O`
- `NO3-`
- organic amines
- amides / peptide linkage relevance

## Sodium

Candidate formations:

- `NaCl`
- `NaOH`
- sodium silicates
- sodium carbonates
- sodium ions in aqueous solution
- sodium in biological ion gradients

## Magnesium

Candidate formations:

- `MgO`
- `MgCl2`
- `MgCO3`
- magnesium silicates
- `Mg2+` in aqueous and biological coordination
- chlorophyll central magnesium case

## Silicon

Candidate formations:

- `SiO2`
- silicates
- silicon dioxide glass networks
- silicon crystals
- silicones / organosilicon
- semiconductor silicon

## Phosphorus

Candidate formations:

- phosphate `PO4^3-`
- ATP phosphate linkages
- phospholipids
- phosphoric acid
- phosphorus oxides
- phosphate minerals

## Sulfur

Candidate formations:

- `S8`
- `H2S`
- `SO2`
- `SO3`
- sulfate `SO4^2-`
- sulfide minerals
- disulfide bonds

## How the Interface Framework Should Enter

Not every T1B case needs full interface notation.

Use interface notation when:

- the formation participates in optical behaviour
- the formation participates in surface behaviour
- the formation is part of a material boundary
- the formation contributes to glass/crystal/metal/alloy behaviour
- the formation affects transmission/reflection/scattering/conduction

Examples:

- silicon and silicates: high interface relevance
- sodium in glass: network modifier / roughness / diffusion relevance
- magnesium silicates: ceramic/network relevance
- sulfur in sulfide minerals: surface/optical relevance
- nitrogen gases: lower direct interface notation need, but strong persistence/bonding relevance

## Scoring Policy

Initial confidence scores should remain conservative.

Use:

- `5-6` for coherent but undercompared new mappings
- `7` where the case strongly aligns with established anchors
- `8+` only when a case is strongly supported across multiple existing corpora

No new `9` should be assigned casually.

The current `9` scores should remain special and hard-won.

## Stop Rule for Phase 1

After completing the pilot extension:

1. run a recalibration log
2. compare the new cases against existing high-score anchors
3. identify which new elements most strongly pressure the framework
4. decide whether Phase 2 should begin with metals or network/glass elements

## Confidence

- confidence that this is the right next programme structure: `9/10`
- confidence that completing the original pilot set should happen before broadening: `9/10`
- confidence that the interface notation should now be reused selectively, not everywhere: `8/10`

## Recommendation

Proceed with:

- `ams-pilot-t1b-corpus-extension-v1.md`

covering:

- N
- Na
- Mg
- Si
- P
- S

This is the cleanest way to return to element/material coverage while preserving the modelling gains from the interface sequence.*** End Patch
