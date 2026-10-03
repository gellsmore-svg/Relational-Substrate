# AMS Sulfur Redox Buffering and Thiol State Map v1

## Purpose

This note maps sulfur's `S5` and `S8` roles:

- `S5`: redox buffer and state stabiliser;
- `S8`: toxicity/signalling boundary species.

The previous sulfur notes established:

- disulfides as protein topology locks;
- iron-sulfur clusters as protein-bound mineral electron route nodes.

This note completes the core sulfur biological triangle:

```text
disulfide locks
Fe-S electron nodes
thiol redox buffering and signalling
```

The central claim is:

> Sulfur gives biology a reversible state-control chemistry: cysteine and related thiols can absorb, signal, repair, relay, or fail under oxidising pressure.

## Source Anchors

The source base is strong:

- Cellular redox homeostasis depends heavily on glutathione, thioredoxin, NADPH-regenerating systems, and related enzymes.
- Glutathione is a major thiol-containing redox buffer, antioxidant, and enzyme cofactor.
- Thioredoxin and glutathione systems support cytoprotective reactions and enzymes controlling reactive oxygen species.
- Cysteine thiols can be oxidised into disulfides, sulfenic acid, sulfinic acid, sulfonic acid, S-nitrosothiols, persulfides, and other modifications.
- Sulfenic acid formation can be reversible and can regulate protein function, signalling, and immune activation.
- Sulfinic acid can be reversible in specific peroxiredoxin systems through sulfiredoxin-mediated repair, though many sulfinic/sulfonic states represent deeper damage.
- Sulfonic acid oxidation is usually an irreversible overoxidation marker.
- Hydrogen sulfide signalling is strongly associated with protein persulfidation, converting cysteine thiols into persulfides.
- Persulfidation can regulate protein activity, structure, localisation, stress response, and protection from irreversible oxidation.
- Cysteine redox states interact with reactive oxygen, nitrogen, and sulfur species, so the system is not a linear ladder only; it is a competing state network.

Sources consulted:

- "Cellular Redox Homeostasis" (`PMC8469889`)
- Glutathione redox homeostasis review (`PubMed 26007177`)
- Gupta and Carroll, cysteine sulfenic acid targeting (`PMC4830130`)
- B-cell activation and reversible cysteine sulfenic acid (`PMC3659792`)
- Nature Reviews Chemistry, "Thiol oxidation: A slippery slope"
- Discovering mechanisms of signalling-mediated cysteine oxidation (`PubMed 18282483`)
- Peroxiredoxin sulfonic acid / hyperoxidation study (`PMC2662001`)
- Sulfiredoxin reversal of peroxiredoxin sulfinic acid (`PubMed 12714748`)
- H2S signalling through persulfidation (`Chemical Reviews`, 2018)
- Plant and mammalian persulfidation reviews (`PMC6157319`, `PMC9037506`, `PMC5853657`, `PMC8614790`)

## AMS Role Assignment

Sulfur roles:

```text
S5 = redox buffer/state stabiliser
S8 = toxicity/signalling boundary species
```

Associated roles:

- `S1`: reactive thiol gate;
- `S3`: disulfide fold lock;
- `S4`: Fe-S electron route node.

Sulfur's distinct contribution is not simply that it reacts. Many elements react. Sulfur is valuable because its biological reactions occupy a controlled middle zone between stability and danger.

It can:

- remain reduced as a thiol;
- form reversible disulfides;
- form regulatory sulfenic acid;
- undergo deeper sulfinic or sulfonic oxidation;
- become glutathionylated;
- become nitrosylated;
- become persulfidated;
- participate in redox relay through thioredoxin, glutaredoxin, peroxiredoxin, glutathione, and related systems.

AMS interpretation:

```text
sulfur supplies reversible chemical state space for biological route correction
```

## State Ladder and Route Classes

The sulfur redox field is best treated as a state map rather than a simple one-way ladder.

### Reduced Thiol

Form:

```text
R-SH / R-S-
```

AMS role:

- available gate;
- redox-sensitive residue;
- ligand site;
- switchable catalytic or structural node.

Classification:

- Route class: `R1`
- Obstruction class: `O1`
- Dominance: `D1`
- Grade: `G_A`

The reduced thiol is a prepared route. It is not merely inert. It is a poised gate.

### Sulfenic Acid

Form:

```text
R-SOH
```

AMS role:

- early oxidation state;
- signalling intermediate;
- reversible regulatory state;
- branching point toward repair, disulfide, glutathionylation, persulfidation, or overoxidation.

Classification:

- Route class: `R4`
- Obstruction class: `O4`
- Dominance: `D4`
- Grade: `G_B/G_A` when governed

Sulfenic acid is a controlled inward-bias state. It is not damage by default. It is often the first usable oxidation mark.

### Disulfide

Form:

```text
R-S-S-R
```

AMS role:

- topology lock;
- reversible protection;
- redox relay product;
- folding or signalling state.

Classification:

- Correct structural disulfide: `R1/O1/D1/G_A`
- Reversible regulatory disulfide: `R4/O4/D4/G_A`
- Mispaired disulfide: `R3/R5/O2/O3/D4/D2/G_C/G_D`

### Glutathionylation

Form:

```text
Protein-S-S-G
```

AMS role:

- reversible cysteine protection;
- redox marking;
- temporary route shielding;
- relay through glutathione/glutaredoxin systems.

Classification:

- Route class: `R4`
- Obstruction class: `O4`
- Dominance: `D4`
- Grade: `G_A/G_B`

The protein cysteine is not destroyed; it is parked in a recoverable protected state.

### Sulfinic Acid

Form:

```text
R-SO2H
```

AMS role:

- deeper oxidation;
- damage or specialised reversible modification depending on context;
- peroxiredoxin hyperoxidation state in repairable cases.

Classification:

- Repairable specialist case: `R4/O4/D4/G_B`
- General overoxidation case: `R3/O2/D4/G_C`

The AMS rule is context-sensitive:

```text
sulfinic acid is not automatically terminal, but it is beyond ordinary thiol switching
```

### Sulfonic Acid

Form:

```text
R-SO3H
```

AMS role:

- terminal overoxidation in most protein contexts;
- marker of route exhaustion;
- persistent damage state.

Classification:

- Route class: `R6`
- Obstruction class: `O6`
- Dominance: `D4/D2`
- Grade: `G_C/G_D`

Sulfonic acid marks failed recoverability unless the protein has an unusual repurposed state.

### Persulfide

Form:

```text
R-S-SH
```

AMS role:

- H2S/sulfane-sulfur signalling state;
- protection against irreversible cysteine oxidation;
- increased nucleophilic route state;
- redox relay and state modulation.

Classification:

- Route class: `R4`
- Obstruction class: `O4`
- Dominance: `D4`
- Grade: `G_A/G_B`

Persulfidation is not merely sulfur overload. It can be a governed state change that changes protein activity, localisation, structure, or stress response.

### S-Nitrosothiol

Form:

```text
R-SNO
```

AMS role:

- nitric oxide-linked signalling state;
- reversible cysteine modification;
- crosstalk with sulfenylation, persulfidation, and disulfide chemistry.

Classification:

- Route class: `R4`
- Obstruction class: `O4`
- Dominance: `D4`
- Grade: `G_B`

This sits at the sulfur-nitrogen signalling boundary.

## Route-State Table

| State | Primary meaning | Route | Obstruction | Dominance | Grade |
|---|---|---:|---:|---:|---:|
| `R-SH/R-S-` | poised thiol gate | `R1` | `O1` | `D1` | `G_A` |
| `R-SOH` | reversible oxidation/signal branch | `R4` | `O4` | `D4` | `G_A/G_B` |
| `R-S-S-R` | lock or relay | `R1/R4` | `O1/O4` | `D1/D4` | `G_A` |
| mispaired `R-S-S-R` | false lock | `R3/R5` | `O2/O3` | `D4/D2` | `G_C/G_D` |
| `Protein-S-S-G` | protected parked cysteine | `R4` | `O4` | `D4` | `G_A/G_B` |
| repairable `R-SO2H` | specialist reversible hyperoxidation | `R4` | `O4` | `D4` | `G_B` |
| damaging `R-SO2H` | overoxidation | `R3` | `O2` | `D4` | `G_C` |
| `R-SO3H` | terminal overoxidation | `R6` | `O6` | `D4/D2` | `G_C/G_D` |
| `R-S-SH` | persulfide signal/protection | `R4` | `O4` | `D4` | `G_A/G_B` |
| `R-SNO` | NO-linked signal | `R4` | `O4` | `D4` | `G_B` |

## Glutathione System

Glutathione is the major small-molecule thiol buffer.

Core route:

```text
oxidant pressure
-> GSH engagement
-> peroxide or cysteine-state correction
-> GSSG formation / protein glutathionylation
-> reductive recovery through NADPH-supported systems
```

AMS variables:

```text
B_in    = incoming oxidative pressure
Q_coh   = redox-pool coherence
J_bound = oxidant load temporarily held by sulfur state changes
J_trans = successful transfer into repair/reduction pathways
B_out   = restored thiol route availability
I_comp  = competing oxidative damage routes
D       = D4 under active buffering, D1 after restored balance
```

Classification:

- Healthy buffer: `R4/O4/D4/G_A`
- Restored steady state: `R1/O1/D1/G_A`
- Buffer exhaustion: `R6/O6/D4/G_C`

GSH is not merely an antioxidant sponge. It is a route-management reservoir.

It converts uncontrolled oxidative pressure into governable sulfur-state traffic.

## Thioredoxin System

Thioredoxin operates as a protein disulfide/reductive relay system.

Core route:

```text
oxidised protein target
-> thioredoxin active-site cysteines
-> target reduction
-> oxidised thioredoxin
-> thioredoxin reductase / NADPH restoration
```

Classification:

- Route class: `R1/R4`
- Obstruction class: `O1/O4`
- Dominance: `D1/D4`
- Grade: `G_A`

AMS interpretation:

Thioredoxin is a mobile route editor. It restores cysteine route availability by moving redox burden through a prepared enzymatic loop.

## Peroxiredoxin and Sulfiredoxin

Peroxiredoxins use reactive cysteine residues to reduce peroxides.

Core route:

```text
peroxide encounter
-> peroxiredoxin cysteine oxidation
-> disulfide or hyperoxidised state
-> reductive reset by thioredoxin or specialised repair
```

The important AMS point is that peroxiredoxin intentionally places sulfur at the damage boundary.

It takes the hit so the wider system does not.

Classification:

- Normal peroxide reduction: `R4/O4/D4/G_A`
- Repairable hyperoxidation: `R4/O4/D4/G_B`
- Irreversible overoxidation: `R6/O6/D4/G_C/G_D`

Sulfiredoxin-mediated repair of some sulfinic peroxiredoxin states shows that biology can govern even deeper sulfur oxidation when the route is specialised.

## Persulfidation and H2S Signalling

Hydrogen sulfide was long treated mainly as toxic. Current literature supports a signalling role in plants and animals, with persulfidation as a major mechanism.

Core route:

```text
H2S / sulfane sulfur availability
-> cysteine persulfidation
-> altered protein activity, localisation, structure, or protection
-> depersulfidation / downstream redox handling
```

AMS classification:

- Route class: `R4`
- Obstruction class: `O4`
- Dominance: `D4`
- Grade: `G_A/G_B`

Persulfidation is a sulfur-added state that can make a cysteine more reactive and can protect it from irreversible oxidation. It is a controlled increase in route potential.

Failure route:

```text
excess sulfide / uncontrolled persulfide chemistry
-> off-target route capture
-> enzyme disruption or toxicity
```

Failure classification:

- `R6/O6/D4/G_C`

The same sulfur chemistry can signal or poison. The difference is governed route placement.

## Boundary Between Signalling and Damage

Sulfur redox states form a boundary system.

Governed signalling:

```text
specific cysteine + controlled oxidant/sulfur signal + repair route present
```

Damage:

```text
non-specific oxidation + repair route absent/exhausted + competing chemistry high
```

AMS discriminator:

| Variable | Signalling | Damage |
|---|---|---|
| `B_in` | bounded | excessive or diffuse |
| `Q_coh` | maintained | falling |
| `J_bound` | controlled temporary retention | trapped or leaky |
| `J_trans` | routed to reset/output | irregular |
| `B_out` | restored or redirected function | weak or corrupted |
| `I_comp` | low/moderate | high |
| `D` | `D4` returning to `D1` | `D4` collapsing into `D2/R6` |

This is the main insight:

> Sulfur redox biology is not a simple good/bad chemistry. It is a threshold-governed route field.

## Vorton Interpretation

Sulfur redox buffering creates transient state vortons.

These are not stable identity carriers like a whole protein fold, nor compact mineral nodes like Fe-S clusters. They are temporary closures of chemical constraint that hold danger long enough for correction, signalling, or transfer.

Examples:

- GSH/GSSG cycle: pool-level buffering vorton;
- thioredoxin active-site cycle: mobile reductive relay vorton;
- peroxiredoxin oxidation/reset: sacrificial peroxide-capture vorton;
- protein sulfenylation: signalling branch vorton;
- persulfidation: sulfur-added protective/signalling vorton;
- sulfonic acid overoxidation: collapsed terminal residue of failed route control.

General form:

```text
incoming oxidative/sulfur/nitrogen pressure
-> cysteine-state capture
-> temporary closure
-> repair, signal, relay, or collapse
```

Viability conditions:

1. The sulfur state must be reachable under physiological pressure.
2. The state must be bounded to specific residues, pools, enzymes, or compartments.
3. A return route or output route must exist.
4. Competing irreversible chemistry must remain below threshold.
5. The system must distinguish useful temporary oxidation from uncontrolled overoxidation.

## Interaction With Previous Sulfur Roles

### With Disulfides

Disulfides are one outcome of sulfur redox buffering.

The redox system decides whether disulfide formation is:

- a correct fold lock;
- a temporary regulatory state;
- a protective parked state;
- a mispaired false lock.

Thus `S5` governs `S3`.

### With Fe-S Clusters

Fe-S clusters depend on redox buffering because oxidative or nitrosative stress can damage clusters.

The redox system:

- preserves cluster ligands;
- buffers oxidant pressure;
- supports repair and replacement;
- prevents released iron/sulfur chemistry from becoming uncontrolled.

Thus `S5` protects `S4`.

### With H2S and Persulfides

Persulfidation links `S5` and `S8`.

At governed levels:

```text
S8 becomes signalling
```

At excessive or misplaced levels:

```text
S8 becomes toxicity
```

## Biological Stress-Test Cases

### Immune Cell Activation

B-cell receptor signalling produces reactive oxygen intermediates. Reversible cysteine sulfenic acid formation participates in activation and proliferation.

AMS reading:

```text
controlled ROI -> sulfenylation -> signalling route -> proliferation programme
```

Classification:

- `R4/O4/D4/G_A`

If sulfenic signalling is blocked or overrun, the route fails.

### Oxidative Stress

High peroxide pressure pushes sulfur states from reversible signalling into overoxidation.

AMS reading:

```text
oxidant excess -> sulfenic overload -> sulfinic/sulfonic accumulation -> route collapse
```

Classification:

- Early governed: `R4/O4/D4/G_B`
- Late failed: `R6/O6/D4/G_C/G_D`

### Peroxiredoxin Sacrifice and Repair

Peroxiredoxin captures peroxide pressure at an active cysteine.

AMS reading:

```text
peroxide -> Prx cysteine state change -> reset by Trx/sulfiredoxin or terminal overoxidation
```

Classification:

- `R4/O4/D4/G_A` when reset works;
- `R6/O6/D4/G_C` when terminal.

### Persulfidation Under Stress

Persulfidation can protect proteins from irreversible oxidation and alter protein function.

AMS reading:

```text
sulfane sulfur -> cysteine persulfide -> protective/signalling route -> restored or modified function
```

Classification:

- `R4/O4/D4/G_A/G_B`

## Element-Level Comparison

### Sulfur Versus Phosphorus

Phosphorus carries transferable order through phosphate groups. Sulfur carries reversible redox state.

```text
Phosphorus = transferable charged order
Sulfur = reversible redox-state control
```

Phosphorylation often writes a relatively stable regulatory token. Sulfur redox often holds a more chemically dangerous, faster, and more context-sensitive state.

### Sulfur Versus Calcium

Calcium bridges and signals through ionic gradients and binding events. Sulfur changes covalent/redox state.

```text
Calcium = relational bridge and gradient carrier
Sulfur = covalent/redox switch and buffer
```

### Sulfur Versus Iron

Iron gives deep redox capacity. Sulfur makes redox capacity biologically governable.

```text
Iron = redox depth
Sulfur = redox closure, buffering, and route control
```

Fe-S clusters show this most clearly.

## Testable Expectations

If the AMS sulfur-redox model is coherent, the following should hold:

1. Reversible cysteine oxidation should often correlate with signalling, regulation, or protection rather than simple damage.
2. Loss of glutathione or thioredoxin capacity should shift cysteine states from governed `R4` toward failed `R6`.
3. Sulfenic acid should appear as an early branch point in many redox-sensitive proteins.
4. Sulfinic acid should separate into repairable specialist cases and damaging general cases.
5. Sulfonic acid should mostly behave as a terminal or persistent overoxidation marker.
6. Persulfidation should sometimes protect cysteines from irreversible oxidation.
7. The same sulfur species should be beneficial or toxic depending on boundedness, repair route availability, and context.
8. Redox-buffer exhaustion should increase misfolding, Fe-S damage, enzyme failure, and signalling distortion.

These expectations match the literature strongly.

## Score

Sulfur redox buffering and thiol-state model:

```text
9.5/10
```

Confidence class:

```text
High
```

Reasons:

- glutathione and thioredoxin redox systems are core cellular biology;
- cysteine oxidation-state chemistry is well established;
- the route model cleanly separates signalling, buffering, protection, repair, and damage;
- reversible/irreversible thresholds map naturally into AMS route classes;
- persulfidation gives sulfur a distinct signalling/protection mode beyond classical antioxidant language;
- this artifact integrates disulfides and Fe-S clusters rather than standing apart from them.

Remaining uncertainty:

The exact specificity of persulfidation targets and the full interplay among sulfenylation, nitrosylation, glutathionylation, and persulfidation remain active research areas. This does not weaken the core sulfur model, but it prevents overclaiming precise route predictions for every protein.

## Sulfur Family Score Recalibration

Previous sulfur family score:

```text
9/10 provisional
```

Updated sulfur family score:

```text
9/10 locked
```

Rationale:

The sulfur family now has three independently strong biological mechanisms:

1. Disulfide bonds lock protein topology.
2. Fe-S clusters route electron state through protein-bound mineral geometry.
3. Thiol redox systems buffer, signal, repair, and fail through governed sulfur-state transitions.

This gives sulfur a coherent high-confidence identity:

```text
Sulfur carries controllable chemical reactivity.
```

It is not as geometrically simple as calcium, not as network-stable as silicon, and not as declaratively transferable as phosphorus. Its strength is controlled danger: it sits at the boundary between useful reactivity and destructive chemistry.

## Next Artifact

Recommended next file:

```text
ams-sulfur-family-score-recalibration-v1.md
```

Purpose:

Consolidate sulfur's material-family role across disulfides, Fe-S clusters, redox buffering, sulfates/extracellular matrix, sulfur minerals, and toxicity/signalling boundary species.

