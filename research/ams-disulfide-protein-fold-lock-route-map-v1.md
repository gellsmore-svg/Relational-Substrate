# AMS Disulfide Protein Fold Lock Route Map v1

## Purpose

This file maps disulfide bonds as sulfur's protein topology-lock role.

It follows:

```text
ams-sulfur-material-family-entry-v1.md
```

The core question:

```text
How do disulfide bonds stabilise protein form, and how do mispaired disulfides create folding failure?
```

## Source Basis

Initial source anchors:

- PubMed, "Protein disulfide isomerase: the structure of oxidative folding." https://pubmed.ncbi.nlm.nih.gov/16815710/
- MDPI Molecules, "PDI-Regulated Disulfide Bond Formation in Protein Folding and Biomolecular Assembly." https://www.mdpi.com/1420-3049/26/1/171
- PMC, "Disulfide bonds in ER protein folding and homeostasis." https://pmc.ncbi.nlm.nih.gov/articles/PMC3078216/
- PMC, "Disulfide Mispairing During Proinsulin Folding in the Endoplasmic Reticulum." https://pmc.ncbi.nlm.nih.gov/articles/PMC4806660/
- PubMed, "Oxidative protein folding: from thiol-disulfide exchange reactions to the redox poise of the endoplasmic reticulum." https://pubmed.ncbi.nlm.nih.gov/25091901/
- ScienceDirect, "Protein disulfide isomerase." https://doi.org/10.1016/j.bbapap.2004.02.017
- PMC, "Structural determinants of oxidative folding in proteins." https://pmc.ncbi.nlm.nih.gov/articles/PMC30135/
- PMC, "Critical roles of protein disulfide isomerases in balancing proteostasis in the nervous system." https://pmc.ncbi.nlm.nih.gov/articles/PMC9253707/

## Source-Supported Working Facts

The source literature supports these working facts:

```text
Disulfide bonds form covalent links between cysteine residues.
Disulfide bonds can stabilise protein folds and extracellular proteins.
Disulfide bond formation is part of oxidative protein folding.
In eukaryotes, many disulfide bonds form or are rearranged in the endoplasmic reticulum.
Protein disulfide isomerases catalyse disulfide formation, isomerisation, and reduction.
Disulfide bonds can form intra-molecularly or inter-molecularly.
Correct disulfide pairing supports native protein folding.
Mispaired disulfides can cause protein misfolding, ER stress, aggregation, or disease.
Disulfide formation and reshuffling depend on protein conformation and redox environment.
The ER redox environment must allow both oxidation and reduction/isomerisation so incorrect disulfides can be corrected.
Disulfide bonds can reduce entropy of the unfolded state and make unfolding less likely.
```

## AMS Core Claim

Disulfide bonds are protein topology locks.

AMS reading:

```text
two cysteine thiols
=> oxidation
=> covalent sulfur-sulfur bridge
=> distant protein regions are locked into a shared route constraint
```

This is not merely local chemistry.

It is topological constraint:

```text
the fold space changes because two locations in the chain become covalently tied.
```

## Sulfur Role

Sulfur role:

```text
S3: disulfide fold lock
```

Route profile:

```text
primary_route: R1
secondary_route: R3 during reshuffling/reduction
primary_obstruction: O1
secondary_obstruction: O2
dominance: D1/D4
route_grade: G_A when correctly paired
route_grade: G_C when mispaired
```

Interpretation:

A correct disulfide stabilises the intended fold. A wrong disulfide stabilises the wrong route.

## Disulfide Formation Route

Starting state:

```text
protein with cysteine thiols
Cys-SH ... Cys-SH
```

Oxidised state:

```text
Cys-S-S-Cys
```

AMS route sequence:

```text
free cysteine thiols
=> oxidative gate
=> disulfide bridge
=> fold route constrained
=> native state stabilised if pairing is correct
```

Route class:

```text
R3 open/flexible cysteine route
=> R1 locked fold route
```

## Correct Pairing

Correct pairing occurs when the disulfide connects cysteines that belong together in the native fold.

AMS reading:

```text
correct disulfide
=> route lock supports intended higher-order protein closure
```

Effects:

```text
reduced unfolded-state entropy
faster or more reliable native folding in some cases
greater extracellular stability
resistance to unfolding
domain or subunit stabilisation
```

Route profile:

```text
route: R1
obstruction: O1 against unfolding
dominance: D1
grade: G_A
```

## Mispaired Disulfides

Mispaired disulfides connect the wrong cysteine residues.

AMS reading:

```text
wrong bridge
=> wrong route locked
=> folding landscape distorted
```

Effects:

```text
misfolding
aggregation
ER retention
ER stress
loss of function
disease in specific cases
```

Route profile:

```text
route: R3/R5
obstruction: O2/O3
dominance: D4/D2
grade: G_C/G_D
```

Important point:

```text
mispaired disulfides are not absence of closure.
They are wrong closure.
```

This is a recurring AMS distinction:

```text
real closure can be disordered if it occurs in the wrong higher-order relation.
```

## Disulfide Isomerisation

Protein disulfide isomerases can rearrange incorrect disulfides.

AMS role:

```text
PDI = fold-lock editor
```

Route sequence:

```text
mispaired disulfide
=> PDI engagement
=> reduction / exchange / reshuffling
=> new pairing attempt
=> native fold lock or further correction
```

Route profile:

```text
wrong R1 lock
=> R3 unlocked intermediate
=> corrected R1 lock
```

Interpretation:

Disulfide folding requires not only locking but editable locking.

AMS reading:

```text
the ER needs both oxidising power and corrective reducing/isomerising capacity.
```

## Redox Poise

Disulfide folding depends on redox environment.

Too reducing:

```text
disulfides fail to form or remain unstable
```

Too oxidising:

```text
wrong disulfides may lock too quickly
```

Balanced redox:

```text
formation + correction + maturation
```

AMS profile:

```text
redox field
=> route-lock permission field
```

This connects disulfide folding to sulfur's broader redox role:

```text
S3 fold lock depends on S5 redox-field stabilisation.
```

## Intra- vs Inter-Molecular Disulfides

### Intramolecular

```text
one protein chain
cysteine A linked to cysteine B
```

AMS:

```text
internal topology lock
```

Route:

```text
R1 fold stabilisation
```

### Intermolecular

```text
two protein chains
cysteine on chain A linked to cysteine on chain B
```

AMS:

```text
assembly lock
```

Route:

```text
R1/R4 complex stabilisation
```

Failure:

```text
wrong intermolecular crosslink
=> aggregation / D2/D4
```

## Extracellular and Secretory Context

Disulfides are especially important in secreted and extracellular proteins.

Reason:

```text
extracellular environments can be harsher
proteins may need greater stability
chaperone control is reduced after secretion
```

AMS:

```text
disulfide lock preserves fold after the protein leaves the intracellular folding field.
```

Route:

```text
fold exported
=> disulfide locks maintain external function
```

## Folding Landscape Interpretation

Protein folding without disulfide:

```text
many conformational routes
noncovalent interactions guide closure
```

Protein folding with correct disulfide:

```text
allowed conformational space is constrained
native basin becomes favoured
```

Protein folding with wrong disulfide:

```text
wrong basin becomes trapped
native route obstructed
```

AMS:

```text
disulfides reshape the route landscape.
```

## Proinsulin Example

Source-supported case:

```text
proinsulin requires correct disulfide pairing for proper folding and insulin bioactivity.
mutations that perturb native disulfide pairing can cause misfolding and disease.
```

AMS reading:

```text
wrong cysteine route
=> wrong fold lock
=> ER stress / failed secretion / functional loss
```

Route profile:

```text
correct insulin disulfides:
R1/D1/G_A

mispaired proinsulin:
R5/D2/G_D
```

This is a high-value concrete example for later expansion.

## Vorton Interpretation

Candidate disulfide vorton model:

```text
cysteine thiol
=> reactive local sulfur gate

disulfide bridge
=> covalent return loop between two protein positions

native disulfide
=> topology-preserving fold vorton

mispaired disulfide
=> topology-corrupting fold vorton
```

AMS reading:

```text
the disulfide is a local sulfur bond
with global fold consequences.
```

## Failure Modes

### Failure 1: No Disulfide Formation

AMS profile:

```text
route: R3 remains open
obstruction: weak O1
dominance: D4
```

Effect:

```text
protein may remain unstable or fail to mature.
```

### Failure 2: Mispaired Disulfide

AMS profile:

```text
route: R5
obstruction: O3
dominance: D2/D4
```

Effect:

```text
wrong fold stabilised.
```

### Failure 3: Over-Oxidation

AMS profile:

```text
route: R3/R5
obstruction: O2/O3
dominance: D4
```

Effect:

```text
thiol chemistry damaged or redirected.
```

### Failure 4: Failed Isomerisation

AMS profile:

```text
wrong R1 lock persists
correction route blocked
```

Effect:

```text
misfolded species accumulates.
```

### Failure 5: Aggregating Intermolecular Crosslinks

AMS profile:

```text
route: R5/R6
obstruction: O3/O6
dominance: D2/D3
```

Effect:

```text
protein assemblies become pathological.
```

## Score Assessment

Disulfide protein fold-lock route map:

```text
score: 9/10
confidence: high
```

Reason:

This is a strong sulfur subcase because:

- disulfide bonds are concrete covalent protein topology locks
- correct and incorrect closures are clearly distinguishable
- PDI-mediated isomerisation maps to fold-lock editing
- ER redox poise maps to route-lock permission
- extracellular stability and disease failure modes are well supported
- proinsulin provides a strong concrete stress-test case

Limitations:

- no specific protein family beyond proinsulin is fully mapped
- disulfide-rich toxins/peptides need separate modelling
- quantitative folding kinetics are not integrated
- ER quality-control pathways need a deeper map
- glutathione/PDI redox coupling needs separate treatment

## Sulfur Family Score Pressure

Current sulfur family score:

```text
8.5/10
```

Disulfide fold-lock subcase:

```text
9/10
```

Updated pressure:

```text
upward toward 9
but retain sulfur family at 8.5/10
```

Reason:

Disulfides are strong, but sulfur needs Fe-S clusters and redox buffering mapped before the whole family should move.

## Next Artifact

The next useful artifact should be:

```text
ams-iron-sulfur-cluster-electron-route-map-v1.md
```

Purpose:

Map sulfur as metal-sulfur electron route node:

- [2Fe-2S], [3Fe-4S], [4Fe-4S]
- cysteine ligation
- electron transfer
- respiration/photosynthesis
- catalysis and sensing
- oxygen sensitivity
- mineral-to-protein bridge
