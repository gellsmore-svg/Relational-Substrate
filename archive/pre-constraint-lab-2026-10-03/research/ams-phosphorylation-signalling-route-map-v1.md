# AMS Phosphorylation Signalling Route Map v1

## Purpose

This file maps phosphorylation as phosphate's reversible regulatory switch role.

It follows:

```text
ams-phosphorus-material-family-entry-v1.md
ams-atp-phosphate-energy-relay-route-map-v1.md
ams-phospholipid-membrane-boundary-route-map-v1.md
```

The core question:

```text
How does adding or removing a phosphate group change what a protein can do?
```

## Source Basis

Initial source anchors:

- PMC, "Structural Insights into Protein Regulation by Phosphorylation and Substrate Recognition of Protein Kinases/Phosphatases." https://pmc.ncbi.nlm.nih.gov/articles/PMC8467178/
- MDPI Life, same article page. https://www.mdpi.com/2075-1729/11/9/957
- PMC, "Protein phosphorylation and its role in archaeal signal transduction." https://pmc.ncbi.nlm.nih.gov/articles/PMC5007285/
- PMC, "Reversible control of kinase signaling through chemical-induced dephosphorylation." https://pmc.ncbi.nlm.nih.gov/articles/PMC11366001/
- NCBI Bookshelf, "Second Messenger Targets: Protein Kinases and Phosphatases." https://www.ncbi.nlm.nih.gov/books/NBK11002/
- NCBI Bookshelf, "Protein Phosphorylation is of Fundamental Importance in Biological Regulation." https://www.ncbi.nlm.nih.gov/books/NBK28063/

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Protein phosphorylation is a major post-translational modification.
Protein kinases attach phosphate groups to amino acid side chains, commonly serine, threonine, or tyrosine.
Protein phosphatases remove phosphate groups from phosphorylated proteins.
Phosphorylation and dephosphorylation are reversible.
Kinases and phosphatases together regulate cellular signalling and physiology.
Phosphorylation can activate or deactivate proteins.
Phosphorylation changes protein structure, stability, dynamics, protein-protein interactions, protein-nucleic acid interactions, localisation, and activity.
Phosphate groups can form hydrogen bonds and salt bridges with nearby residues.
Many phosphorylation sites occur in disordered or dynamic protein regions.
Phosphorylation can induce disorder-to-order or order-to-disorder transitions.
Human cells contain hundreds of kinases and many phosphatases, coordinated into signalling systems.
Kinase/phosphatase dysregulation contributes to disease, including cancer, neurodegeneration, and metabolic disorders.
```

## AMS Core Claim

Phosphorylation is reversible route permission.

AMS reading:

```text
phosphate added
=> charge, shape, binding, or localisation changes
=> route permissions change

phosphate removed
=> route state resets or changes again
```

Phosphate functions as a switch token:

```text
not because phosphate is magic
but because adding a charged tetrahedral group changes the local relational geometry of the protein.
```

## Phosphorus Role

Phosphorus role:

```text
P5: regulatory switch token
```

Route profile:

```text
primary_route: R3/R4
secondary_route: R1 once switched state stabilises
primary_obstruction: O2/O4
dominance: D4
route_grade: G_A/G_B under proper regulation
```

Interpretation:

Phosphorylation is not merely decoration. It changes what routes a protein can admit, block, bind, expose, hide, or transmit.

## Basic Switch Cycle

Conventional:

```text
kinase adds phosphate
phosphatase removes phosphate
```

AMS:

```text
kinase writes route state
phosphatase clears or rewrites route state
```

Cycle:

```text
protein
=> kinase + ATP
=> phosphoprotein
=> altered route permissions
=> phosphatase
=> dephosphoprotein
=> reset or alternative state
```

Route notation:

```text
unphosphorylated state: State A
phosphorylated state: State B
dephosphorylated state: State A or State C depending context
```

This is reversible but not always trivial:

```text
the same site can participate in larger network memory,
timing,
feedback,
or multisite logic.
```

## Kinase as Route Writer

Kinases transfer phosphate, usually from ATP, to target residues.

AMS role:

```text
kinase = route-state writer
```

Inputs:

```text
ATP
target protein
recognition motif / docking relation
Mg2+ or catalytic cofactors
activation loop state
cellular signal context
```

Route profile:

```text
substrate recognition: R4
catalytic transfer: R1/R3
gate specificity: O2/O4
dominance: D4
```

Interpretation:

Kinases do not simply add phosphate anywhere. They select substrates and sites through recognition geometry, activation state, localisation, and signalling context.

AMS formula:

```text
kinase specificity
= gate geometry
+ substrate recognition
+ active-state permission
+ cellular localisation
```

## Phosphatase as Route Eraser / Reset Gate

Phosphatases remove phosphate.

AMS role:

```text
phosphatase = route-state remover / reset gate
```

Route profile:

```text
substrate recognition: R4
dephosphorylation: R3/R1 reset
obstruction: O2 if shielded/inaccessible
dominance: D4
```

Interpretation:

Phosphatases are not merely passive off-switches. They also provide specificity, timing, localisation, and network balancing.

AMS formula:

```text
phosphorylation level
= kinase writing pressure
- phosphatase removal pressure
within a local signalling field
```

## Structural Effects of Phosphorylation

Phosphorylation can alter:

```text
charge
hydrogen bonding
salt bridges
folding
disorder/order transitions
binding surfaces
protein-protein interactions
protein-nucleic acid interactions
localisation signals
degradation signals
enzymatic activity
```

AMS route map:

| Structural effect | AMS route meaning |
|---|---|
| charge change | new electrostatic route surface |
| salt bridge formation | new local closure |
| salt bridge disruption | route obstruction or release |
| disorder-to-order transition | route stabilisation |
| order-to-disorder transition | route loosening |
| binding site exposure | route admission |
| binding site masking | route obstruction |
| localisation change | route relocation |
| degradation signal | route to destruction/adaptation |

## Activation and Deactivation

Phosphorylation may activate or deactivate a protein.

AMS distinction:

```text
activation
=> route opened, stabilised, or aligned

deactivation
=> route blocked, destabilised, or redirected
```

This matters because:

```text
phosphorylation does not always mean "on."
It means "state changed."
```

Route classes:

```text
P-on activation:
R3 -> R1

P-on inhibition:
R1 -> R3

P-on relocation:
R4 shift

P-on degradation:
R5/R6 disposal route
```

## Multisite Phosphorylation

Many proteins have multiple phosphorylation sites.

AMS:

```text
multiple phosphosites create route logic.
```

Possibilities:

```text
single-site switch
AND gate
OR gate
threshold
timer
priming site
docking site
feedback loop
graded response
all-or-none transition
```

Route interpretation:

```text
each phosphate changes local route geometry.
multiple phosphates create combined route state.
```

This makes phosphorylation suitable for signalling cascades.

## Signalling Cascade

Conventional:

```text
one kinase activates another kinase, which activates downstream targets.
```

AMS:

```text
route-state change propagates through a cascade of switch tokens.
```

Generic cascade:

```text
signal
=> receptor state change
=> kinase A phosphorylation
=> kinase B phosphorylation
=> transcription factor phosphorylation
=> gene expression change
```

Route profile:

```text
signal admission: R3/R4
cascade propagation: R4
amplification: D4 network expansion
output closure: R1 in final response
```

Interpretation:

Phosphorylation cascades turn local events into organised cellular response.

## Reversibility and Timing

Phosphorylation is powerful because it is reversible.

AMS:

```text
reversibility allows runtime control.
```

Time modes:

```text
rapid transient phosphorylation
=> pulse route

sustained phosphorylation
=> maintained state

oscillatory phosphorylation
=> timing route

spatially local phosphorylation
=> compartmental route
```

Phosphatases are essential because without removal, the route state would remain locked or drift.

AMS reading:

```text
signalling needs both writing and erasing.
```

## Misregulation and Disease

Kinase/phosphatase dysregulation can produce disease.

AMS role:

```text
phosphorylation error
=> wrong route permission
```

Examples:

```text
excess kinase activity
=> route permanently open

loss of phosphatase activity
=> route not reset

wrong localisation
=> route written in wrong field

mutation at phosphorylation site
=> route cannot be written or erased

mutation near docking motif
=> specificity fails
```

Route profile:

```text
pathological activation: R1 in wrong context
pathological inhibition: R3 in needed context
network disorder: D4/D2
```

AMS conclusion:

```text
phosphate can create real regulation
or real misregulation.
```

## Relation to ATP

ATP role:

```text
P3: energy relay packet
```

Phosphorylation role:

```text
P5: regulatory switch token
```

Relation:

```text
ATP supplies the transferable phosphate.
Kinase writes it onto a substrate.
The substrate's route permissions change.
```

AMS formula:

```text
P3 transfer packet
=> P5 switch state
```

## Relation to Membranes

Many signalling cascades begin at membranes.

AMS relation:

```text
P4 membrane boundary
receives/organises signal context.

P5 phosphorylation
propagates route-state changes inward.
```

This gives a T1C chain:

```text
boundary reception
=> kinase activation
=> phosphorylation cascade
=> cellular response
```

## Vorton Interpretation

Candidate phosphorylation vorton model:

```text
unphosphorylated protein
=> base conformational route field

phosphate addition
=> new charged closure point
=> altered local loop / salt bridge / binding surface
=> changed route permission

phosphate removal
=> closure point removed
=> route state resets
```

Multisite:

```text
several phosphate closure points
=> composite route logic field
```

Cascade:

```text
route-state vorton propagates through protein network
```

## Score Assessment

Phosphorylation signalling route map:

```text
score: 9/10
confidence: high
```

Reason:

This is a strong phosphorus subcase because:

- phosphorylation is widespread and biologically central
- kinase/phosphatase reversibility maps cleanly to write/reset route logic
- structural consequences of phosphorylation are well supported
- signalling cascades map naturally to propagated route-state changes
- disease misregulation maps cleanly to wrong route permission

Limitations:

- no specific pathway, such as MAPK or insulin signalling, is mapped yet
- multisite phosphorylation logic needs concrete examples
- quantitative phosphoproteomics is not integrated
- phosphatase holoenzyme targeting needs deeper treatment
- spatial compartmentalisation of signalling needs a dedicated model

## Phosphorus Family Score Reassessment

Current phosphorus family score:

```text
9/10
```

Mapped subcases:

```text
DNA/RNA phosphate backbone: 9
ATP energy relay: 9
phospholipid membrane boundary: 9
phosphorylation signalling: 9
```

Updated decision:

```text
phosphorus material family: 9.5/10
confidence: high
```

Reason:

Phosphorus now has four high-confidence mapped subcases covering:

- information
- energy
- boundary
- regulation

This breadth and centrality justify moving the phosphorus family from 9 to 9.5.

Do not move to 10 because phosphate pathology, mineral diversity, ATP synthase, and concrete signalling pathways still need detailed mapping.

## Next Artifact

The next useful artifact should be:

```text
ams-phosphorus-family-score-recalibration-v1.md
```

Purpose:

Lock the phosphorus family score move:

```text
9 -> 9.5
```

and record the evidence stack and remaining limits.
