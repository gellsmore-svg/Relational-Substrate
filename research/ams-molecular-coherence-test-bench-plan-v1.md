# AMS Molecular Coherence Test Bench Plan

## Purpose

This note defines how to extend the current vorton/topology sandbox toward basic molecule modelling without smuggling material entities into the wrong ontological layer.

The aim is not to prove an invisible substrate. The aim is to build a mathematical coherence bench that can ask whether AMS-style variables prefer known stable material arrangements over incoherent alternatives.

The controlling sequence remains:

```text
continuous substrate
-> local organised disturbance
-> torsion / tension / alignment expression
-> candidate closure-pattern
-> stable primary topology / vorton
-> coupled vorton regimes
-> secondary material regimes
-> perceived matter
```

Atoms and molecules therefore enter the test bench as secondary material regimes, not as hidden substrate components and not as immediate vorton species.

## Why This Is Not Too Soon

It is too soon to claim that AMS derives chemistry from first principles.

It is not too soon to use known chemistry as a constraint set for coherence testing. Classical chemistry already tells us which simple molecular geometries are stable, strained, polar, delocalised, weakly coupled, or impossible. AMS can use that knowledge as calibration data while asking a different question:

```text
Can a topology-and-constraint scoring model distinguish coherent material regimes from nearby incoherent ones?
```

If it cannot, the model is too weak. If it can, the result is still not proof, but it gives the ontology a disciplined modelling programme.

## Binding Terminology

The old word `binding` should be treated as a provisional shorthand only.

For modelling, replace it with more precise terms:

- `coupling`: two regimes preserve a shared relation.
- `constraint compatibility`: their allowed transformations do not destroy each other.
- `route continuity`: a disturbance can traverse or redistribute coherently through the regime.
- `storage asymmetry`: local order can hold stress, charge separation, or delay.
- `closure coherence`: a ring, loop, or distributed route preserves identity rather than collapsing into noise.

## Use Of Classical Chemistry

Classical chemistry should be used as observed constraint data.

It should not be treated as AMS ontology.

Useful translations are:

| Classical feature | AMS test-bench proxy |
|---|---|
| Valence / electron configuration | Coupling capacity and admissible route count |
| Bond order | Coupling strength and route continuity |
| Bond length | Preferred rest distance for coupled regimes |
| Bond angle / VSEPR geometry | Preferred angular topology |
| Hybridisation | Local geometry family and route distribution |
| Electronegativity difference | Boundary asymmetry and storage tendency |
| Formal / partial charge | Route pressure and storage imbalance |
| Resonance / aromaticity | Distributed route coherence |
| Steric hindrance | Boundary pressure and route obstruction |
| Hydrogen bonding | Weak inter-regime coupling |
| Ionic character | High boundary asymmetry with strong long-range ordering |

The test bench should infer relative coupling strength from existing chemistry, then test whether candidate geometries satisfy those constraints coherently.

## Minimal Data Schema

A molecule candidate should be represented as a graph plus geometry:

```text
MoleculeCandidate
  atoms[]
  bonds[]
  angles[]
  torsions[]
  rings[]
  global_properties
```

Each atom should minimally include:

```text
Atom
  id
  element
  valence_capacity
  preferred_valence
  electronegativity
  radius
  formal_charge
  preferred_geometry
```

Each bond should minimally include:

```text
Bond
  atom_a
  atom_b
  order
  preferred_length
  flexibility
  polarity
  rotation_barrier
```

Each geometry candidate should include:

```text
Geometry
  coordinates
  bond_lengths
  bond_angles
  torsions
  ring_closures
```

## Coherence Score

The first score should be deliberately simple and inspectable.

Suggested components:

| Symbol | Meaning |
|---|---|
| `V_sat` | Valence satisfaction |
| `G_fit` | Preferred geometry fit |
| `A_strain` | Angle strain penalty |
| `B_strain` | Bond-length strain penalty |
| `P_balance` | Polarity and storage balance |
| `R_route` | Route continuity / conjugation |
| `C_ring` | Ring closure coherence |
| `S_steric` | Steric obstruction penalty |
| `Q_mol` | Overall molecular coherence |

Initial sketch:

```text
Q_mol =
  0.18 V_sat
+ 0.16 G_fit
+ 0.14 (1 - A_strain)
+ 0.12 (1 - B_strain)
+ 0.12 P_balance
+ 0.14 R_route
+ 0.08 C_ring
+ 0.06 (1 - S_steric)
```

The weights are starting assumptions, not doctrine. The first job of the bench is to expose where the weights fail.

## First Molecule Set

Begin with molecules where classical expectations are simple and well-known:

- `H2`: one simple coupling relation.
- `O2`: stronger coupled route with known complications.
- `N2`: high bond order and strong route continuity.
- `H2O`: bent geometry and polarity.
- `CO2`: linear geometry with polar bonds but balanced whole.
- `CH4`: tetrahedral geometry and saturated coupling.
- `NH3`: trigonal pyramidal geometry and polarity.
- `NaCl`: ionic ordering rather than covalent geometry.
- `benzene`: ring closure and distributed route coherence.

Do not begin with proteins, cells, membranes, or biological machinery. Those belong later, after the test bench can handle simple molecular constraint graphs.

## Iteration Method

For each molecule:

1. Encode the classical reference graph and approximate geometry.
2. Generate perturbed candidates by changing bond length, angle, torsion, polarity balance, or ring closure.
3. Score each candidate using `Q_mol`.
4. Check whether the known stable geometry ranks above strained or incoherent alternatives.
5. Inspect failures and decide whether the AMS variable set is missing something or merely weighted badly.

The output should be a ranked table, not a claim of discovery.

## Software Direction

The current topology sandbox should remain the visual and conceptual rule bench.

The molecule work can be added in phases:

1. `analysis/molecule-coherence.mjs`: hand-entered molecule data and scoring.
2. Browser tab: molecule graph visualisation and coherence readout.
3. Perturbation sweeps: ranked stable, fragile, and incoherent candidates.
4. Optional cheminformatics integration:
   - RDKit for molecule parsing, conformers, descriptors, and known geometries.
   - Open Babel as an alternative conversion and geometry tool.
   - 3Dmol.js or Three.js molecule rendering for browser display.

External chemistry libraries should help generate and compare candidate geometries. They should not define AMS ontology.

## Guardrails

- No cells, beads, lattice pellets, hidden solids, or material parts may be placed between `T0` and vorton formation.
- A molecule is not a vorton. It is a secondary material regime arising from coupled primary topologies.
- Classical chemistry calibrates the score; it does not prove the substrate.
- A successful score means the model is coherent enough to continue, not that AMS has derived chemistry.
- Every new variable must be traceable back to route, boundary, storage, scattering, closure, coupling, or topology.

## Immediate Next Step

Build a tiny `molecule-coherence` script with `H2`, `H2O`, `CO2`, `CH4`, and `benzene`.

The script should compare one known-good geometry with several perturbed alternatives for each molecule and write a markdown summary. The pass/fail question is simple:

```text
Does the current coherence score rank the known-good candidate above obvious bad candidates?
```

If the answer is no, the model should be corrected before visual complexity is added.
