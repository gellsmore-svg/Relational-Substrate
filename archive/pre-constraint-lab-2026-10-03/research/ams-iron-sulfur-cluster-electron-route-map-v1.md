# AMS Iron-Sulfur Cluster Electron Route Map v1

## Purpose

This note maps iron-sulfur clusters as sulfur's `S4` role: protein-bound mineral electron route nodes.

The prior sulfur note established disulfide bonds as protein topology locks. This note moves from fold-locking to electron routing. In disulfides, sulfur helps a protein retain a shape. In iron-sulfur clusters, sulfur helps a protein hold a small mineral circuit inside a biological fold so electrons can be received, stored briefly, passed, sensed, or used for catalytic work.

The central claim is direct:

> Iron-sulfur clusters are protein-bound mineral route nodes: iron carries redox change, sulfur supplies bridging closure, and the surrounding protein tunes where the electron may go.

## Source Anchors

The source base is strong and coherent:

- Iron-sulfur clusters are ancient, common, structurally diverse cofactors used in respiration, photosynthesis, nitrogen fixation, DNA repair, regulation, and catalysis.
- Common biological cluster types include `[2Fe-2S]`, `[3Fe-4S]`, and `[4Fe-4S]`.
- `[2Fe-2S]` clusters are rhombic; `[4Fe-4S]` clusters are cubane-like.
- Iron ions in these clusters are commonly ligated by cysteine thiolates, though histidine, arginine, aspartate, tyrosine, water, substrates, and cofactors can also participate in some proteins.
- Fe-S clusters mediate electron transfer by reversible changes in iron redox state.
- Fe-S cluster biogenesis requires regulated assembly systems because free iron and free sulfur are chemically dangerous.
- Major assembly systems include ISC, SUF, and NIF.
- General assembly involves cysteine-derived sulfur, scaffold-bound cluster construction, and transfer into recipient apoproteins.
- SUF systems are especially important under oxidative stress or iron limitation in many bacteria.
- Fe-S clusters are vulnerable to oxidative and nitrosative attack, misassembly, incorrect insertion, and ligand disruption.

Sources consulted:

- Pérard and Ollagnier de Choudens, "Iron-sulfur clusters biogenesis by the SUF machinery" (`PMC6006206`)
- Johnson et al., "Iron-Sulphur Cluster Biosynthesis" (`PMC2827815`)
- Deere et al., "Methanosarcina acetivorans contains a functional ISC system for iron-sulfur cluster biogenesis"
- Maio, "Iron-Sulfur Clusters: Assembly and Biological Roles"
- Mitochondrial Fe-S review (`PMC8577454`)
- Xu and Moller, "Iron-Sulfur Clusters: Biogenesis, Molecular Mechanisms, and Their Functional Significance"

## AMS Role Assignment

Sulfur role:

`S4`: iron-sulfur electron route node.

Associated roles:

- `S1`: reactive thiol gate, because cysteine ligands bind and position the cluster.
- `S5`: redox buffer/state stabiliser, because Fe-S function depends on the surrounding redox field.
- `S7`: mineral-redox bridge, because Fe-S clusters join inorganic mineral geometry to living enzymatic order.
- `S8`: toxicity/signalling boundary species, because damaged Fe-S chemistry can release iron, sulfur species, or stress signals.

Elemental division of labour:

| Component | AMS contribution | Route function |
|---|---|---|
| Iron | Redox-variable centre | Accepts and releases electron state |
| Inorganic sulfide | Internal bridge | Holds cluster closure and Fe-Fe spacing |
| Cysteine sulfur | Protein ligand gate | Anchors mineral closure inside fold geometry |
| Protein fold | Context field | Tunes potential, access, specificity, and protection |
| Assembly machinery | Construction route | Builds transferable cluster without uncontrolled free chemistry |

The cluster is not merely a small mineral stuck inside a protein. It is a coupled T1B/T1C interface. The mineral node supplies dense redox geometry; the protein supplies boundary, gating, insulation, positioning, and route selection.

## Cluster Geometry as Route Topology

### `[2Fe-2S]`

`[2Fe-2S]` is the small rhombic route node.

AMS interpretation:

- two iron centres provide a minimal redox pair;
- two bridging sulfides close the route across the iron pair;
- cysteine or mixed ligands bind the node to a protein scaffold;
- the cluster acts as a compact electron relay rather than a broad catalytic chamber.

Route classification:

- Route class: `R1`
- Obstruction class: `O1`
- Dominance: `D1`
- Grade: `G_A`

Why:

The route is narrow, bounded, and strongly real. The cluster does not let charge diffuse randomly through the protein. It offers a constrained route through a prepared redox node.

Failure deformation:

- ligand weakening or oxidative damage shifts the cluster toward `R3`;
- local mispositioning shifts it toward `O2`;
- protein unfolding exposes it to `O5/O6` diffusion and fragmentation.

### `[4Fe-4S]`

`[4Fe-4S]` is the cubane route node.

AMS interpretation:

- four iron centres and four sulfides produce a denser closed redox geometry;
- the cluster can support stronger catalytic participation, multi-electron-adjacent behaviour, radical chemistry, or substrate activation depending on context;
- the protein decides whether the cluster is a relay, catalytic centre, structural lock, sensor, or radical initiator.

Route classification:

- Route class: `R1/R4`
- Obstruction class: `O1/O4`
- Dominance: `D1/D4`
- Grade: `G_A`

Why:

The route is real and strongly bounded, but it can be inward-biased. In many enzymes, an electron does not merely pass through the node. It is held long enough to be coupled to substrate chemistry. That makes `[4Fe-4S]` more than a wire. It is a redox chamber.

Failure deformation:

- conversion to `[3Fe-4S]` can mark controlled functional state change or damage, depending on protein context;
- oxidative loss of an iron produces route collapse or route reclassification;
- exposed cubanes become vulnerable fragmentation sites.

### `[3Fe-4S]`

`[3Fe-4S]` is the altered or open cluster node.

AMS interpretation:

- it can be a legitimate biological cofactor in some proteins;
- it can also appear as a damaged or transformed state of a larger cluster;
- its meaning depends on whether the protein fold is built for it.

Route classification:

- Native `[3Fe-4S]`: `R1/O1/D1/G_A`
- Damage-derived `[3Fe-4S]`: `R3/O2/D4/G_C`

Why:

The same visible cluster type can have different ontological status. If the protein expects and stabilises the geometry, it is a real route. If it appears after oxidative loss, it is a damaged route remnant.

This is important for AMS method. Topology alone is not enough. Context decides whether a form is a valid closure or a residue of broken closure.

## Electron Transfer Route Model

Minimal electron route:

```text
donor -> protein entry field -> Fe-S cluster -> protein exit field -> acceptor
```

AMS variables:

```text
B_in      = incoming electron-route availability
B_out     = outgoing electron-route availability
J_bound   = cluster-bound redox retention
J_trans   = successful transfer current through the node
Q_coh     = coherence of cluster geometry and ligand field
D         = dominance class
I_comp    = competing route intensity
```

For a high-quality Fe-S relay:

```text
B_in high
Q_coh high
J_bound moderate
J_trans high
B_out high
I_comp low
D = D1
```

For a catalytic Fe-S site:

```text
B_in high
Q_coh high
J_bound high
J_trans gated
B_out conditional
I_comp low-to-moderate
D = D1/D4
```

For a damaged Fe-S cluster:

```text
B_in unstable
Q_coh falling
J_bound leaky or trapped
J_trans irregular
B_out weak
I_comp high
D = D4/D2
```

The key distinction is between relay and chamber.

A relay keeps `J_trans` high and `J_bound` modest. A chamber raises `J_bound` because electron state must be coupled to catalytic geometry before release. Damage lowers `Q_coh`, increases `I_comp`, and makes retention either leaky or trapped.

## Vorton Interpretation

An Fe-S cluster is a small mineral vorton embedded inside protein order.

The vorton is not a free object. It exists as a retained circulation of redox constraint across iron, sulfide, cysteine ligation, and fold geometry.

Viability conditions:

1. It must be bounded enough that electron state does not diffuse into uncontrolled protein chemistry.
2. It must be distributed enough that redox change is not localised into destructive single-site collapse.
3. It must be coupled enough that incoming and outgoing routes are geometrically selected.
4. It must be insulated enough that water, oxygen, nitric oxide, or wrong ligands do not capture the route.
5. It must be integrated enough that the protein can tune redox potential without destroying cluster closure.

Thus:

```text
Fe redox variability + sulfide bridge closure + cysteine anchoring + protein tuning = Fe-S vorton route node
```

The cluster retains a circulation of constraint. It accepts redox change, redistributes it through a closed mineral geometry, and releases it only through routes permitted by the protein.

## Why Sulfur Is Essential

Iron alone gives redox capacity but not stable biological routing.

Sulfur supplies:

- bridge geometry between iron centres;
- soft ligand compatibility with transition-metal redox behaviour;
- cysteine anchoring into protein folds;
- reversible vulnerability that allows sensing and damage response;
- a mineral-to-biological coupling layer.

In AMS terms:

> Iron carries change; sulfur closes the route.

Without sulfur, the system has redox reactivity without the same compact biological closure. Without iron, the sulfur framework lacks the same redox depth. Fe-S is a coupled identity, not a mere mixture.

## Functional Modes

### Electron Relay

Examples include ferredoxins, respiratory-chain components, photosynthetic proteins, and many redox enzymes.

AMS route:

```text
donor -> Fe-S relay -> acceptor
```

Classification:

- `R1/O1/D1/G_A`

The cluster is a narrow, real route. It has enough retention to receive electron state and enough release geometry to pass it onward.

### Catalytic Node

Some Fe-S clusters participate directly in substrate chemistry.

AMS route:

```text
donor -> cluster-bound redox state -> substrate-coupled transformation -> product release
```

Classification:

- `R1/R4`
- `O1/O4`
- `D1/D4`
- `G_A`

The route is not simply through the cluster. It turns inward into a reaction pocket. The cluster is then a gated chamber rather than only a relay.

### Radical Initiation

Radical SAM systems use Fe-S chemistry to initiate controlled radical reactions.

AMS route:

```text
Fe-S cluster -> SAM activation -> radical route -> substrate transformation
```

Classification:

- `R4`
- `O4`
- `D4`
- `G_A` when controlled
- `G_C/G_D` when radical escape occurs

The cluster creates a dangerous route but holds it inside an ordered channel. This is high-risk, high-specificity chemistry.

### Structural Stabilisation

Some Fe-S clusters stabilise protein structure or assembly.

AMS route:

```text
cluster ligation -> fold retention -> functional geometry
```

Classification:

- `R1/O1/D1/G_A`

Here the cluster acts partly like a mineral fold-lock, but unlike disulfide it also carries redox-sensitive state.

### Sensing and Regulation

Fe-S clusters can act as oxygen, nitric oxide, iron, redox, or metabolic state sensors.

AMS route:

```text
environmental chemical pressure -> cluster state change -> protein conformational/regulatory response
```

Classification:

- Normal sensing: `R4/O4/D4/G_B`
- Destructive sensing: `R3/O2/D4/G_C`

Sensor clusters are often designed to be conditionally vulnerable. Their partial fragility is not a defect when it is governed. It becomes a defect when damage exceeds the regulatory route.

## Assembly Route: ISC, SUF, NIF

Fe-S clusters are too reactive to be assembled casually.

General route:

```text
cysteine sulfur mobilisation
-> scaffold-bound Fe/S assembly
-> protected cluster maturation
-> transfer to recipient apoprotein
-> final fold-tuned cluster state
```

AMS interpretation:

The cell does not merely gather ingredients. It runs a controlled route-construction sequence.

Biogenesis classification:

- Route class: `R1`
- Obstruction class: `O1/O2`
- Dominance: `D1`
- Grade: `G_A`

The assembly machinery is itself a route-preserving system. It prevents raw iron and sulfur from becoming uncontrolled reactive fields.

### ISC

ISC is a general assembly system, especially important in bacteria and mitochondria.

AMS role:

- primary cluster construction route;
- scaffold-mediated closure;
- transfer-ready cluster preparation.

Classification:

- `R1/O1/D1/G_A`

### SUF

SUF is especially associated with stress conditions in many bacteria, including oxidative stress and iron limitation.

AMS role:

- stress-resistant cluster construction route;
- route preservation when ordinary construction is threatened;
- constrained assembly under low-resource or hostile chemistry.

Classification:

- `R1/O2/D1/G_A`

The `O2` marker matters. SUF is not merely another route. It is a late-gate/stress-gate construction system.

### NIF

NIF is tied to nitrogenase-related cluster assembly.

AMS role:

- specialised cluster construction for complex catalytic mineral cofactors;
- high-order mineral route preparation.

Classification:

- `R1/R4`
- `O1/O4`
- `D1/D4`
- `G_A`

## Failure Modes

### Oxidative Damage

Oxygen-derived stress can damage Fe-S clusters, oxidise ligands, release iron, or convert one cluster state into another.

AMS failure route:

```text
oxidative pressure -> ligand/cluster damage -> Q_coh loss -> route leakage or collapse
```

Classification:

- `R3/R6`
- `O2/O6`
- `D4`
- `G_C`

The route does not merely stop. It can become chemically dangerous because released or damaged components create competing routes.

### Nitrosative Attack

Nitric oxide can interact with Fe-S clusters and shift them into regulatory or damaging states.

AMS failure/sensing route:

```text
NO encounter -> cluster alteration -> signalling or collapse
```

Classification:

- Governed sensor case: `R4/O4/D4/G_B`
- Ungoverned damage case: `R3/O2/D4/G_C`

### Misligation

Wrong ligand geometry can preserve apparent binding while corrupting route function.

AMS failure route:

```text
cluster present -> wrong ligand field -> wrong redox potential or geometry -> failed transfer/catalysis
```

Classification:

- `R3`
- `O2`
- `D4`
- `G_C`

This is the Fe-S analogue of a mispaired disulfide. The node exists, but the route is wrong.

### Assembly Failure

Iron shortage, sulfur shortage, scaffold failure, transfer failure, or recipient-fold defects all interrupt cluster formation.

AMS failure route:

```text
incomplete assembly -> unstable intermediate -> no valid recipient closure
```

Classification:

- `R6`
- `O6`
- `D4/D2`
- `G_C/G_D`

Assembly failure is route failure before the route node exists.

## Comparison With Disulfide Topology Locks

| Feature | Disulfide bond | Iron-sulfur cluster |
|---|---|---|
| Main sulfur role | Fold topology lock | Electron route node |
| Core chemistry | S-S covalent bridge | Fe-S mineral cluster |
| Main function | Retain protein form | Transfer, hold, sense, or use electron state |
| Editing system | PDI and redox environment | ISC/SUF/NIF assembly and repair systems |
| Main failure | Mispairing, reduction, aggregation | Oxidation, NO attack, misligation, cluster loss |
| AMS class | `S3` | `S4` |
| Typical valid route | `R1/O1/D1/G_A` | `R1/O1/D1/G_A` or `R1/R4/O1/O4/D1/D4/G_A` |

The difference is important.

Disulfide sulfur locks protein topology. Fe-S sulfur closes mineral redox topology inside protein order.

Disulfide failure corrupts fold identity. Fe-S failure corrupts electron routing, catalysis, sensing, and metabolic continuity.

## Element-Level Comparison

### Against Phosphorus

Phosphorus carries transferable biological order through phosphate backbones, phosphate energy relay, membrane headgroups, and phosphorylation tokens.

Sulfur in Fe-S clusters carries redox-route closure.

Contrast:

```text
Phosphorus: transferable charged order
Sulfur: controllable redox reactivity
Iron-sulfur: mineral redox route embedded in protein order
```

Phosphate is often a declarative or transferable state marker. Fe-S is more like an active route node.

### Against Calcium

Calcium bridges and stabilises larger relational structures.

Fe-S clusters conduct and gate electron state at small scale.

Contrast:

```text
Calcium: bridge-forming constraint carrier
Fe-S: electron-route mineral node
```

Calcium often stabilises whole structures or signalling gradients. Fe-S carries local redox work.

### Against Silicon

Silicon forms stable extended networks and optical/electronic route media.

Fe-S clusters are compact biological mineral route nodes.

Contrast:

```text
Silicon: extended route medium
Fe-S: embedded route node
```

Glass admits and delays light across a network. Fe-S accepts and releases electron state through a compact protein-bound closure.

## Worked Model: Electron Relay Protein

Suppose a ferredoxin-like protein contains a `[2Fe-2S]` cluster.

Route:

```text
donor redox protein
-> surface encounter
-> protein electrostatic guide
-> [2Fe-2S] cluster
-> exit guide
-> acceptor redox protein
```

AMS variables:

```text
B_in    = high when donor docks correctly
Q_coh   = high when cluster geometry and ligand field are intact
J_bound = moderate
J_trans = high
B_out   = high when acceptor route is aligned
I_comp  = low
D       = D1
```

Classification:

- `R1/O1/D1/G_A`

If oxygen damages the cluster:

```text
B_in    = unstable
Q_coh   = reduced
J_bound = leaky or trapped
J_trans = low/irregular
B_out   = weak
I_comp  = high
D       = D4
```

Classification:

- `R3/R6/O2/O6/D4/G_C`

The model predicts that apparent cluster retention is not enough. Route quality depends on redox potential, ligand geometry, donor/acceptor docking, and protection from competing chemistry.

## Worked Model: Fe-S Catalytic Site

Suppose an enzyme uses a `[4Fe-4S]` cluster to help activate a substrate.

Route:

```text
electron donor
-> [4Fe-4S] cluster
-> substrate-coupled redox geometry
-> product-forming transition
-> release/reset
```

AMS variables:

```text
B_in    = high
Q_coh   = high
J_bound = high
J_trans = conditional
B_out   = product-dependent
I_comp  = low unless radical or oxygen escape occurs
D       = D1/D4
```

Classification:

- `R1/R4/O1/O4/D1/D4/G_A`

This is not a wire. It is an active redox chamber. Route validity requires temporary retention.

## Testable Expectations

If the AMS reading is coherent, the following should hold across Fe-S systems:

1. Better ligand-field integrity should correlate with sharper redox behaviour and more reliable electron transfer.
2. Protein fold changes should tune Fe-S redox potential without changing the basic cluster atoms.
3. Damage that lowers cluster coherence should increase side reactivity, route leakage, or route loss.
4. Stress-resistant assembly systems should preserve Fe-S function under conditions where ordinary assembly routes degrade.
5. Native `[3Fe-4S]` clusters and damage-derived `[3Fe-4S]` clusters should not be treated as equivalent merely because they share a formal atom count.
6. Catalytic Fe-S sites should show higher `J_bound` and more conditional `B_out` than simple electron relays.
7. Radical Fe-S chemistry should require especially strong route containment to avoid uncontrolled side routes.

These expectations match the literature direction strongly enough to raise confidence in the sulfur model.

## Score

Iron-sulfur cluster electron route map:

```text
9.5/10
```

Confidence class:

```text
High
```

Reasons:

- the source literature strongly supports Fe-S clusters as common, ancient, protein-bound redox cofactors;
- the geometry-to-function mapping is direct and not forced;
- AMS route variables distinguish relay, catalytic chamber, sensor, structural node, and failure modes cleanly;
- the sulfur contribution is specific rather than generic;
- the model connects T1B mineral order to T1C biological function with minimal strain.

Remaining gap:

The model still needs a dedicated redox-buffering pass for glutathione, thioredoxin, cysteine/cystine balance, and reactive sulfur species. That is required before sulfur as a family should be locked above `9/10`.

## Effect on Sulfur Family Score

Previous sulfur family score:

```text
8.5/10
```

Updated pressure:

```text
strong upward pressure toward 9/10
```

Provisional family score after disulfides and Fe-S clusters:

```text
9/10 provisional
```

Reason:

Disulfide topology locks and Fe-S electron nodes now give sulfur two strong, independent high-confidence biological roles:

- sulfur locks protein folds;
- sulfur closes mineral redox routes inside proteins.

The score should be held as provisional until the redox-buffering map is complete.

## Next Artifact

Recommended next file:

```text
ams-sulfur-redox-buffering-and-thiol-state-map-v1.md
```

Purpose:

Map glutathione, thioredoxin, cysteine/cystine balance, sulfenic/sulfinic/sulfonic oxidation states, persulfides, hydrogen sulfide signalling, and oxidative stress control as sulfur's `S5` and `S8` roles.

