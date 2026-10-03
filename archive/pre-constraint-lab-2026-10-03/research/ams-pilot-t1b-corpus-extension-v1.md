# AMS Pilot T1B Corpus Extension v1

## Purpose

This document extends the pilot T1B corpus by completing the remaining elements from the original pilot set:

- N
- Na
- Mg
- Si
- P
- S

It should be read alongside:

- `ams-pilot-t1b-corpus-v1.md`
- `ams-element-material-coverage-plan-v1.md`
- `ams-non-persistent-vorton-topology-atlas-v1.md`
- `ams-interface-formalisation-sketch-v1.md`

The aim is not exhaustive chemical coverage. The aim is disciplined representative modelling across bonding, persistence, material, biological, and interface-relevant cases.

## Scoring Rule

Scores remain conservative.

- `5-6`: coherent first-pass mapping, undercompared
- `7`: strong alignment with existing anchors or multiple known behaviours
- `8`: strong cross-corpus fit
- `9`: reserved for unusually coherent cases already pressure-tested across several layers

No new `9` scores are assigned in this extension.

## Element 1: Nitrogen

## Conventional Role Summary

Nitrogen is central to:

- atmospheric stability
- strong triple bonding
- amines and amides
- proteins and nucleic acids
- reactive oxides
- redox-active biological and atmospheric chemistry

Its main value for AMS modelling is contrast:

- extremely stable `N2`
- flexible biological nitrogen forms
- reactive nitrogen oxides

## Representative T1B Formations

## `N2`

### Conventional Structure

Diatomic nitrogen with a strong triple bond and high stability under ordinary conditions.

### AMS Vorton Relation Grammar

- closure type: paired high-lock closure
- coupling type: strong axial coupling
- lock-up tendency: very high
- slip tolerance: very low
- strain distribution: tightly localised between paired centres
- return-path character: short, strong, highly constrained

### Non-Persistent Topology Interactions

Likely resists:

- diffuse topologies
- threshold-fragile perturbation

Likely fails mainly under:

- high-energy overconstraint
- bond-breaking excitation

### Confidence

- score: `7`

Reason:

- strong fit with high-stability closure logic, but not yet pressure-tested across enough nitrogen families for `8`.

## `NH3`

### Conventional Structure

Ammonia, polar molecule with trigonal pyramidal geometry and a lone-pair character.

### AMS Vorton Relation Grammar

- closure type: central nitrogen with asymmetric peripheral coupling
- coupling type: moderate directional coupling to hydrogen closures
- lock-up tendency: medium
- slip tolerance: medium
- strain distribution: asymmetric around central closure
- return-path character: stable but orientation-sensitive

### Non-Persistent Topology Interactions

Likely interacts strongly with:

- boundary-sensitive topologies
- local polarity-compatible perturbations

### Confidence

- score: `6`

Reason:

- coherent first-pass mapping, but lone-pair directionality needs deeper modelling.

## `NO`

### Conventional Structure

Nitric oxide, small reactive radical molecule with biological signalling relevance.

### AMS Vorton Relation Grammar

- closure type: asymmetric partially unbalanced pair closure
- coupling type: polarised N-O coupling
- lock-up tendency: medium/low
- slip tolerance: medium
- strain distribution: uneven and reactive
- return-path character: incomplete or tension-biased

### Non-Persistent Topology Interactions

Likely receptive to:

- metastable-only topologies
- threshold-fragile interactions

### Confidence

- score: `5`

Reason:

- useful radical/reactivity case, but currently under-modelled.

## `NO2`

### Conventional Structure

Reactive bent nitrogen oxide with strong atmospheric and oxidative chemistry relevance.

### AMS Vorton Relation Grammar

- closure type: bent asymmetric multi-centre closure
- coupling type: uneven triadic coupling
- lock-up tendency: medium
- slip tolerance: medium/high
- strain distribution: distributed but imbalanced
- return-path character: strained and reactivity-prone

### Confidence

- score: `5`

Reason:

- coherent as an unstable/asymmetric case, but needs comparison against broader oxide chemistry.

## `NO3-`

### Conventional Structure

Nitrate ion with delocalised bonding and trigonal planar symmetry.

### AMS Vorton Relation Grammar

- closure type: symmetric multi-centre distributed closure
- coupling type: delocalised triadic coupling around nitrogen
- lock-up tendency: medium/high
- slip tolerance: medium
- strain distribution: distributed across equivalent oxygen relations
- return-path character: multi-route and stabilised by symmetry

### Confidence

- score: `7`

Reason:

- strong fit with distributed closure stabilisation and symmetry logic.

## Amide / Peptide Linkage Relevance

### Conventional Structure

Nitrogen participates in amide bonds central to proteins and peptide backbones.

### AMS Vorton Relation Grammar

- closure type: constrained partial-delocalisation linkage
- coupling type: directional biological backbone coupling
- lock-up tendency: medium/high
- slip tolerance: low/medium
- strain distribution: distributed over local peptide relation
- return-path character: constrained but functionally repeatable

### T1C Escalation

Strong escalation toward:

- proteins
- biological macromolecular assemblies
- chaperone-mediated folding

### Confidence

- score: `7`

Reason:

- strong biological continuity fit, anchored by existing organism-linked corpus.

## Nitrogen Summary

Most useful nitrogen cases:

- `N2`: high-lock stability benchmark
- `NO/NO2`: reactive asymmetry cases
- nitrate and amide: distributed-stabilisation and biological-linkage cases

Overall element confidence:

- `6.5/10`

## Element 2: Sodium

## Conventional Role Summary

Sodium is central to:

- ionic bonding
- salts
- aqueous ions
- glass modifiers
- biological ion gradients

Its AMS value is less about complex local closure and more about:

- separable ionic relation
- pathway modification
- field/boundary relevance

## Representative T1B Formations

## `NaCl`

### Conventional Structure

Ionic sodium chloride with crystal lattice formation.

### AMS Vorton Relation Grammar

- closure type: charge-separated paired relation in lattice context
- coupling type: ionic lattice coupling
- lock-up tendency: high in solid lattice
- slip tolerance: low in crystal, high when dissolved
- strain distribution: extended through lattice relation
- return-path character: lattice-mediated rather than pair-only

### T1C Escalation

- ionic crystals
- dissolution
- conductivity in solution

### Confidence

- score: `7`

Reason:

- strong fit with extended lattice coupling and phase-dependent slip behaviour.

## `Na+` in Aqueous Solution

### Conventional Structure

Hydrated sodium ion with coordination by water molecules.

### AMS Vorton Relation Grammar

- closure type: central ion with dynamic hydration shell
- coupling type: weak/medium transient coordination
- lock-up tendency: low/medium
- slip tolerance: high
- strain distribution: distributed through hydration network
- return-path character: dynamic and exchangeable

### Interface/Route Relevance

Can be read as:

```text
Na+_aq
= Zones{dynamic coordination shell}
= Route{R2}
= Obst{weak O5}
= Grade{G_B/G_C}
```

### Confidence

- score: `6`

Reason:

- coherent dynamic-shell model, but needs future aqueous/ion-gradient comparison.

## `NaOH`

### Conventional Structure

Strong base; ionic compound with hydroxide relation.

### AMS Vorton Relation Grammar

- closure type: separable ionic closure with reactive hydroxide component
- coupling type: high-polarity ionic coupling
- lock-up tendency: medium/high in solid, low/highly mobile in solution
- slip tolerance: phase-dependent
- strain distribution: concentrated in ionic separation and hydroxide reactivity

### Confidence

- score: `5`

Reason:

- chemically important but currently less structurally distinctive inside AMS than `NaCl` or sodium glass roles.

## Sodium Silicates

### Conventional Structure

Sodium modifies silicate networks and is important in glass chemistry.

### AMS Vorton Relation Grammar

- closure type: network-modifier relation
- coupling type: disrupts/adjusts silicate network coupling
- lock-up tendency: medium
- slip tolerance: increases relative to pure network
- strain distribution: changes network continuity and local pathway availability
- return-path character: modified and less purely nested than silica

### Interface Formalisation

```text
sodium_silicate_glass
= Zones{Z_A weak/med, Z_C}
= Route{R2, (R3)}
= Obst{O5, (O2)}
= Grade{G_B/G_C}
```

### Confidence

- score: `7`

Reason:

- strong fit with glass modifier logic and the new interface framework.

## Sodium in Biological Ion Gradients

### Conventional Structure

Sodium ions participate in membrane potentials and transport gradients.

### AMS Vorton Relation Grammar

- closure type: gradient-defined dynamic relation
- coupling type: membrane-mediated ionic coupling
- lock-up tendency: low locally, high functionally at system level
- slip tolerance: high under channel-permitted conditions
- strain distribution: boundary-separated gradient tension

### T1C Escalation

- membranes
- ion channels
- organismal regulation

### Confidence

- score: `7`

Reason:

- strong fit with existing membrane/ion-channel organism-linked corpora, though T1B alone cannot carry full functional meaning.

## Sodium Summary

Most useful sodium cases:

- `NaCl`: ionic lattice anchor
- sodium silicates: glass/network modifier
- biological sodium gradients: boundary-function bridge

Overall element confidence:

- `6.5/10`

## Element 3: Magnesium

## Conventional Role Summary

Magnesium is central to:

- oxides and minerals
- carbonate and silicate structures
- biological coordination
- chlorophyll
- enzyme and ATP-associated chemistry

Its AMS value lies in:

- divalent coordination
- structural mineral contexts
- biological role-bearing coordination

## Representative T1B Formations

## `MgO`

### Conventional Structure

Ionic magnesium oxide with strong lattice structure.

### AMS Vorton Relation Grammar

- closure type: strong divalent ionic lattice relation
- coupling type: high lattice coupling
- lock-up tendency: high
- slip tolerance: low in solid
- strain distribution: extended and lattice-stabilised
- return-path character: strong repetitive lattice return

### Confidence

- score: `7`

Reason:

- strong lattice-stability case, but less cross-layer pressure-tested than silica.

## `MgCl2`

### Conventional Structure

Magnesium chloride, ionic compound with hydration and solution behaviour relevance.

### AMS Vorton Relation Grammar

- closure type: divalent centre with two chloride relations
- coupling type: ionic, hydration-sensitive
- lock-up tendency: medium/high in solid, lower in solution
- slip tolerance: phase-dependent
- strain distribution: charge-distributed around divalent centre

### Confidence

- score: `6`

Reason:

- useful divalent ionic comparison, but currently moderate distinctiveness.

## `MgCO3`

### Conventional Structure

Magnesium carbonate, mineral-forming carbonate compound.

### AMS Vorton Relation Grammar

- closure type: divalent cation coupled to stable carbonate closure
- coupling type: ionic-mineral coupling
- lock-up tendency: high in mineral context
- slip tolerance: low/medium depending on crystal setting
- strain distribution: carbonate-distributed plus magnesium lattice coupling

### Confidence

- score: `6`

Reason:

- coherent mineral-forming case, needs broader carbonate comparison.

## Magnesium Silicates

### Conventional Structure

Magnesium silicates are important mineral/network materials.

### AMS Vorton Relation Grammar

- closure type: divalent modifier/structural participant in silicate networks
- coupling type: mineral-network coupling
- lock-up tendency: medium/high
- slip tolerance: low/medium
- strain distribution: network-mediated with magnesium-stabilised local constraints
- return-path character: structured but less purely silica-like

### Interface Relevance

Relevant to:

- ceramics
- minerals
- rough interfaces
- crystal/glass comparisons

### Confidence

- score: `7`

Reason:

- strong network/material relevance, but still needs specific mineral case studies.

## `Mg2+` in Biological Coordination

### Conventional Structure

Magnesium ions coordinate with biological molecules and are important in ATP-related chemistry.

### AMS Vorton Relation Grammar

- closure type: central coordination relation
- coupling type: biological functional coupling
- lock-up tendency: medium locally, high in functional context
- slip tolerance: regulated and context-dependent
- strain distribution: coordination-stabilised around functional site

### T1C Escalation

- ATP-associated processes
- enzyme active sites
- biological macromolecular assemblies

### Confidence

- score: `7`

Reason:

- strong fit with function-bearing biological corpus, but depends heavily on higher-order context.

## Chlorophyll Central Magnesium

### Conventional Structure

Magnesium sits at the centre of chlorophyll’s porphyrin-like structure.

### AMS Vorton Relation Grammar

- closure type: central coordination lock within extended organic ring
- coupling type: functional light-interaction coordination
- lock-up tendency: high within the molecular complex
- slip tolerance: low locally, functional response mediated by whole complex
- strain distribution: ring-distributed with central stabilisation

### T1C Escalation

- photosynthetic complexes
- pigment-light interaction

### Confidence

- score: `7`

Reason:

- very important functional case, but deserves its own later optical/biological study before higher score.

## Magnesium Summary

Most useful magnesium cases:

- `MgO`: lattice stability
- magnesium silicates: mineral/network bridge
- biological `Mg2+`: functional coordination
- chlorophyll Mg: light-biological bridge

Overall element confidence:

- `6.8/10`

## Element 4: Silicon

## Conventional Role Summary

Silicon is central to:

- silica
- silicates
- glass
- semiconductors
- ceramics
- organosilicon materials

Its AMS value is extremely high because it directly connects:

- network formation
- optical transmission
- glass/crystal contrast
- interface modelling
- semiconductor behaviour

## Representative T1B Formations

## `SiO2`

### Conventional Structure

Silicon dioxide in quartz, glass, and network forms.

### AMS Vorton Relation Grammar

- closure type: network-forming tetrahedral closure
- coupling type: extended nested network coupling
- lock-up tendency: high in quartz, medium/high in glass
- slip tolerance: low in crystal, distributed in glass
- strain distribution: network-distributed
- return-path character: extended, nested, and strongly cross-level

### Existing Corpus Relation

`SiO2` is already one of the strongest current AMS cases.

Current score in prior corpus:

- `9`

### Confidence

- score: `9`

Reason:

- already pressure-tested across T1B, T1C, boundary, glass/crystal, and interface modelling.

## Silicates

### Conventional Structure

Silicate units form diverse minerals and networks with modifiers.

### AMS Vorton Relation Grammar

- closure type: modular network closure
- coupling type: variable network coupling with modifier-sensitive constraints
- lock-up tendency: medium/high
- slip tolerance: variable
- strain distribution: network and modifier distributed
- return-path character: extended but composition-dependent

### Confidence

- score: `8`

Reason:

- strongly supported by silica/network work, but broad class needs subdivision.

## Silicon Crystal

### Conventional Structure

Crystalline silicon forms covalent lattice structures and is central to semiconductor behaviour.

### AMS Vorton Relation Grammar

- closure type: ordered covalent lattice closure
- coupling type: high regular lattice coupling
- lock-up tendency: high
- slip tolerance: low in ideal lattice, defect-sensitive in functional contexts
- strain distribution: ordered and lattice-wide
- return-path character: regular nested admissibility

### Interface Formalisation

Potentially relevant to:

```text
air->silicon_crystal
= Zones{Z_A}
= Dom{D1 selective}
= Route{R1, (R3)}
= Obst{O1, (O2)}
= Grade{G_A/G_B}
```

### Confidence

- score: `8`

Reason:

- strong lattice/semiconductor relevance, but specific semiconductor modelling still needs its own pass.

## Silicon Dioxide Glass Network

### Conventional Structure

Amorphous silica-based glass network.

### AMS Vorton Relation Grammar

- closure type: distributed network closure
- coupling type: non-periodic but real higher-order coupling
- lock-up tendency: medium/high
- slip tolerance: medium/high compared with crystal
- strain distribution: distributed and non-repeating
- return-path character: permissive network return

### Interface Formalisation

```text
silica_glass
= Zones{Z_A,Z_C}
= Dom{D1/D3 depending surface}
= Route{R1,R2}
= Obst{O1,O5}
= Grade{G_A/G_B/G_C}
```

### Confidence

- score: `8`

Reason:

- strongly supported by glass-transmission and release modelling.

## Organosilicon / Silicones

### Conventional Structure

Silicon-oxygen backbones with organic side groups, flexible polymer-like materials.

### AMS Vorton Relation Grammar

- closure type: flexible network/polymer hybrid closure
- coupling type: backbone-stabilised with side-group modulation
- lock-up tendency: medium
- slip tolerance: high
- strain distribution: backbone and side-chain mediated
- return-path character: flexible and deformation-tolerant

### Confidence

- score: `6`

Reason:

- coherent extension, but undercompared relative to silica cases.

## Silicon Summary

Most useful silicon cases:

- `SiO2`: top structural cross-level anchor
- silicate networks: modifier-sensitive network family
- silicon crystal: semiconductor and ordered-lattice bridge
- silica glass: optical/interface frontier anchor

Overall element confidence:

- `8.2/10`

## Element 5: Phosphorus

## Conventional Role Summary

Phosphorus is central to:

- phosphate chemistry
- DNA/RNA backbones
- ATP
- phospholipids
- minerals
- biological energy and membrane structures

Its AMS value is especially high for:

- biological function
- role-bearing chemical persistence
- boundary and membrane formation

## Representative T1B Formations

## Phosphate `PO4^3-`

### Conventional Structure

Tetrahedral phosphate ion with strong biological and mineral relevance.

### AMS Vorton Relation Grammar

- closure type: tetrahedral distributed closure
- coupling type: high multi-centre oxygen coupling
- lock-up tendency: high
- slip tolerance: low/medium in fixed contexts, higher in biological transfer contexts
- strain distribution: distributed across oxygen relations
- return-path character: stable multi-route closure

### Confidence

- score: `8`

Reason:

- strong distributed closure and biological/mineral cross-context relevance.

## ATP Phosphate Linkages

### Conventional Structure

Phosphate linkages in ATP participate in energy transfer processes.

### AMS Vorton Relation Grammar

- closure type: high-strain transferable linkage
- coupling type: functional biological coupling
- lock-up tendency: medium/high
- slip tolerance: regulated
- strain distribution: linkage-specific and context-sensitive
- return-path character: metastable-functional rather than merely stable

### T1C Escalation

- energy metabolism
- enzyme coupling
- biological macromolecular assemblies

### Confidence

- score: `7`

Reason:

- strong functional relevance, but needs dedicated biological-energy modelling.

## Phospholipids

### Conventional Structure

Phosphorus-containing amphiphilic molecules central to membranes.

### AMS Vorton Relation Grammar

- closure type: amphiphilic boundary-forming closure
- coupling type: head-tail polarity and membrane assembly coupling
- lock-up tendency: medium locally, high at membrane level
- slip tolerance: high laterally within membrane
- strain distribution: boundary-distributed
- return-path character: layer-mediated and function-bearing

### Interface/T1C Relevance

Strong connection to:

- membranes
- boundary-defined wholes
- organismal regulation

### Confidence

- score: `8`

Reason:

- strongly supported by existing membrane and teleology/function corpora.

## Phosphoric Acid

### Conventional Structure

Acidic phosphate compound with multiple dissociation states.

### AMS Vorton Relation Grammar

- closure type: proton-sensitive phosphate closure
- coupling type: pH/state-dependent coupling
- lock-up tendency: medium
- slip tolerance: medium/high under proton exchange
- strain distribution: state-dependent
- return-path character: chemically switchable

### Confidence

- score: `6`

Reason:

- useful state-change case, but needs deeper acid/base comparison.

## Phosphate Minerals

### Conventional Structure

Phosphate ions form stable mineral structures with cations such as calcium.

### AMS Vorton Relation Grammar

- closure type: phosphate-cation lattice closure
- coupling type: mineral lattice coupling
- lock-up tendency: high
- slip tolerance: low
- strain distribution: extended lattice-stabilised
- return-path character: mineral-context stable

### Confidence

- score: `7`

Reason:

- strong mineral stability case, but cation-specific variants needed.

## Phosphorus Summary

Most useful phosphorus cases:

- phosphate ion: distributed stable closure
- ATP phosphate linkages: functional transfer
- phospholipids: membrane boundary formation
- phosphate minerals: structural stability

Overall element confidence:

- `7.2/10`

## Element 6: Sulfur

## Conventional Role Summary

Sulfur is central to:

- ring structures
- sulfides
- sulfates
- redox chemistry
- volcanic/atmospheric compounds
- disulfide bonds in proteins

Its AMS value lies in:

- bonding diversity
- redox transitions
- ring closure
- protein structural locking
- mineral and surface relevance

## Representative T1B Formations

## `S8`

### Conventional Structure

Elemental sulfur commonly forms cyclic `S8` rings.

### AMS Vorton Relation Grammar

- closure type: ring-loop molecular closure
- coupling type: repeated sulfur-sulfur coupling
- lock-up tendency: medium/high
- slip tolerance: medium
- strain distribution: loop-distributed
- return-path character: literal molecular ring return

### Confidence

- score: `8`

Reason:

- unusually strong fit to closure/loop logic; useful vorton-knotting analogue.

## `H2S`

### Conventional Structure

Hydrogen sulfide, bent molecule with reactive/toxic behaviour.

### AMS Vorton Relation Grammar

- closure type: bent central sulfur with weak hydrogen coupling
- coupling type: polar/asymmetric coupling
- lock-up tendency: low/medium
- slip tolerance: medium
- strain distribution: local asymmetric
- return-path character: weakly constrained

### Confidence

- score: `5`

Reason:

- coherent but not yet strongly discriminating.

## `SO2`

### Conventional Structure

Sulfur dioxide, bent molecule with atmospheric and reactive relevance.

### AMS Vorton Relation Grammar

- closure type: asymmetric triadic closure
- coupling type: polarised S-O coupling
- lock-up tendency: medium
- slip tolerance: medium
- strain distribution: bent and reactive
- return-path character: strained distributed closure

### Confidence

- score: `6`

Reason:

- useful reactive oxide comparison, needs broader sulfur-oxide family pressure.

## `SO3`

### Conventional Structure

Sulfur trioxide, trigonal planar compound and sulfate precursor.

### AMS Vorton Relation Grammar

- closure type: symmetric triadic sulfur-oxygen closure
- coupling type: stronger distributed oxygen coupling
- lock-up tendency: medium/high
- slip tolerance: low/medium
- strain distribution: symmetric and delocalised
- return-path character: stabilised multi-route closure

### Confidence

- score: `6`

Reason:

- coherent symmetry/stability contrast with `SO2`, but undercompared.

## Sulfate `SO4^2-`

### Conventional Structure

Tetrahedral sulfate ion, stable and widespread in minerals and solution.

### AMS Vorton Relation Grammar

- closure type: tetrahedral distributed closure
- coupling type: high multi-centre oxygen coupling
- lock-up tendency: high
- slip tolerance: medium depending context
- strain distribution: distributed over oxygen relations
- return-path character: stable multi-route closure

### Confidence

- score: `8`

Reason:

- strong analogy with phosphate-style distributed closure and strong mineral/solution relevance.

## Sulfide Minerals

### Conventional Structure

Sulfur forms sulfide minerals with metals, often with surface and optical relevance.

### AMS Vorton Relation Grammar

- closure type: metal-sulfur lattice closure
- coupling type: mineral/metallic lattice hybrid coupling
- lock-up tendency: medium/high
- slip tolerance: low/medium
- strain distribution: lattice and surface-sensitive
- return-path character: mineral-stabilised but defect/surface sensitive

### Interface Relevance

Potentially relevant to:

- surface reflection
- oxidation
- roughness
- mineral optical behaviour

### Confidence

- score: `7`

Reason:

- strong material relevance, but needs specific mineral studies.

## Disulfide Bonds

### Conventional Structure

Sulfur-sulfur bonds link cysteine residues and stabilise protein structure.

### AMS Vorton Relation Grammar

- closure type: biological cross-link closure
- coupling type: structural protein lock
- lock-up tendency: medium/high
- slip tolerance: low unless chemically reduced
- strain distribution: protein-scale structural constraint
- return-path character: cross-link stabilised

### T1C Escalation

- protein folding
- biological macromolecular assemblies
- structural memory

### Confidence

- score: `8`

Reason:

- strong biological structure/function bridge, supported by organism-linked and macromolecular corpora.

## Sulfur Summary

Most useful sulfur cases:

- `S8`: ring-loop closure
- sulfate: distributed tetrahedral closure
- sulfide minerals: surface/material relevance
- disulfide bonds: biological cross-link and structural memory

Overall element confidence:

- `7.0/10`

## Cross-Element Findings

## 1. Silicon Is the Strongest Addition

Silicon joins the programme with the highest confidence because it connects directly to:

- `SiO2`
- glass
- quartz
- interface modelling
- semiconductor/network behaviour

## 2. Phosphorus and Sulfur Are the Strongest Biological/Functional Additions

Phosphorus strengthens:

- membranes
- ATP
- phosphate backbones

Sulfur strengthens:

- protein structure
- redox
- ring closure
- mineral surfaces

## 3. Sodium and Magnesium Strengthen Boundary and Coordination Logic

Sodium helps with:

- ionic gradients
- glass modification
- aqueous coordination

Magnesium helps with:

- divalent coordination
- mineral structure
- chlorophyll and biological function

## 4. Nitrogen Adds Stability/Reactivity Contrast

Nitrogen is useful because it spans:

- stable `N2`
- reactive oxides
- biological amides

## Updated Pilot Set Status

The original pilot element set is now covered at first pass:

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

## Recalibration Pressures

Potential future score pressure:

- `SiO2` remains justified at `9`
- silicates may rise after more material-specific coverage
- phosphate and sulfate may become stronger after direct mineral/membrane comparisons
- `S8` may become important for vorton loop/knotting analogies
- sodium silicates may become important for glass modifier modelling

## Confidence

- confidence that Phase 1 pilot coverage is now structurally complete: `9/10`
- confidence that scores remain appropriately conservative: `8/10`
- confidence that silicon should be treated as the strongest extension element: `9/10`
- confidence that phosphorus/sulfur are the next strongest biological-functional additions: `8/10`

## Recommendation

Create a formal recalibration log for the completed pilot set before moving into Phase 2.

## Next Move

The best next artifact is:

- `ams-score-recalibration-log-v7.md`

That should review the whole now-complete pilot element set and decide whether any scores should shift after adding:

- N
- Na
- Mg
- Si
- P
- S
