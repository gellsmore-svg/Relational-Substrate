# AMS Heme Redox Catalytic Route Map v1

## Purpose

This note maps iron's `I2` role:

```text
I2: heme redox/catalytic route centre
```

The previous heme file mapped `I1`: oxygen and gas routing in hemoglobin and myoglobin.

This file maps heme where it does chemical work:

- cytochromes;
- mitochondrial electron transport;
- cytochrome P450 monooxygenases;
- peroxidases;
- catalases;
- peroxygenases;
- detoxification;
- steroid and xenobiotic metabolism;
- failure into ROS leakage, heme release, or pathological catalytic switching.

The central claim is:

> Heme enzymes turn iron redox depth into governed catalytic route chambers.

## Source Anchors

The source base supports these facts:

- Heme enzymes are widely used across the biosphere.
- Cytochromes transfer electrons through heme iron centres.
- Cytochrome c is a mobile electron carrier in the mitochondrial electron transport chain.
- Cytochrome c oxidase transfers electrons to oxygen to form water.
- Cytochrome P450 enzymes form a large heme enzyme superfamily.
- P450s oxidise fatty acids, steroids, xenobiotics, drugs, and endogenous compounds.
- P450 catalysis commonly uses NAD(P)H and O2 to oxidise substrates.
- P450 catalytic cycles involve heme iron redox state changes, oxygen binding, electron delivery, protonation, and highly reactive Fe-oxo intermediates.
- Compound I, often represented as an Fe(IV)-oxo porphyrin radical / formal FeO3+ entity, is central to many P450/peroxidase oxidations.
- Peroxidases and catalases use heme chemistry to process peroxide and oxidise substrates or dismutate peroxide.
- Heme enzyme specificity depends strongly on protein structure, substrate access, active-site geometry, and redox partner coupling.
- Pathological changes can shift a heme electron-transfer protein into peroxidase-like damaging behaviour.

Sources consulted:

- "Heme Enzyme Structure and Function" (`PMC3981943`)
- "Mechanisms of Cytochrome P450-Catalyzed Oxidations" (`PMC6519473`)
- "Hydrocarbon Hydroxylation by Cytochrome P450 Enzymes" (`PMC2820140`)
- "Structure and function of the cytochrome P450 peroxygenase enzymes" (`PMC5818669`)
- "Electrochemical transformations catalyzed by cytochrome P450s and peroxidases" (`PubMed 37458261`)
- "Expanding P450 catalytic reaction space through evolution and engineering" (`PMC4008644`)
- "Mitochondrial electron transport chain, ROS generation and uncoupling" (`PMC6559295`)
- "Electron flow into cytochrome c coupled with reactive oxygen species..." (`PMC4593697`)

## AMS Role Assignment

Iron role:

```text
I2: heme redox/catalytic route centre
```

Associated roles:

- `I1`: heme oxygen/gas route centre;
- `I5`: storage and transport governance;
- `I6`: toxicity and ferroptosis threshold.

Core distinction:

```text
I1 = heme binds and routes gases
I2 = heme transfers electrons and activates substrates
```

Both roles use the same iron depth but different route outcomes.

## Elemental Division of Labour

| Component | AMS contribution | Route function |
|---|---|---|
| Heme iron | redox-depth centre | accepts/donates electrons, binds O2/peroxide, forms reactive intermediates |
| Porphyrin ring | electronic delocalisation field | stabilises high-energy redox states |
| Axial ligand | redox tuning | shifts potential and catalytic behaviour |
| Protein active site | route chamber | admits substrate, excludes wrong chemistry, tunes orientation |
| Redox partner | electron supply route | delivers electrons at the right stage |
| Proton route | activation support | enables O-O cleavage / intermediate formation |
| Product exit path | release route | prevents product trapping or side damage |

AMS formula:

```text
iron redox depth + porphyrin delocalisation + protein chamber + staged electron/proton supply = heme catalytic route
```

## Mechanism 1: Cytochrome Electron Transfer

Cytochromes use heme iron to move electron state through a chain.

Generic route:

```text
electron donor
-> heme iron redox change
-> protein-tuned transfer path
-> electron acceptor
```

Classification:

```text
R1/O1/D1/G_A
```

Why:

The route is narrow, real, and ordered. The heme site changes redox state without becoming an uncontrolled reactive pocket.

AMS variables:

```text
B_in    = electron arrival from donor
Q_coh   = heme/protein redox geometry coherence
J_bound = temporary electron-state retention on heme
J_trans = successful transfer to acceptor
B_out   = downstream electron route
I_comp  = ROS leakage, wrong acceptor, structural damage
D       = D1
```

## Mechanism 2: Mitochondrial Terminal Reduction

In respiratory chains, cytochrome systems help route electrons toward oxygen reduction. Cytochrome c oxidase transfers electrons from cytochrome c to oxygen to form water.

AMS route:

```text
reduced cytochrome c
-> cytochrome c oxidase route
-> controlled electron/proton delivery
-> O2 reduction
-> H2O
```

Classification:

```text
R1/R4/O1/O4/D1/D4/G_A
```

Why:

Oxygen reduction is chemically dangerous if uncontrolled. Heme/copper/protein architecture turns it into a governed terminal route rather than diffuse ROS production.

Failure:

```text
electron leakage -> superoxide/ROS -> oxidative damage
```

Classification:

```text
R6/O6/D4/G_C
```

## Mechanism 3: P450 Monooxygenase Chamber

P450 enzymes use heme iron to activate oxygen and insert one oxygen atom into a substrate while reducing the other to water.

Simplified route:

```text
substrate binding
-> water displacement / redox potential shift
-> electron input
-> O2 binding
-> second electron/proton steps
-> reactive Fe-oxo intermediate
-> substrate oxidation
-> product release
```

Classification:

```text
R4/O4/D4/G_A
```

Why:

This is an inward-biased catalytic chamber. The route intentionally holds a dangerous intermediate long enough to perform selective oxidation.

AMS variables:

```text
B_in    = substrate and electron/O2 availability
Q_coh   = active-site geometry, redox partner coupling, proton routing
J_bound = activated oxygen / Fe-oxo intermediate retention
J_trans = oxygen atom transfer or substrate oxidation
B_out   = product release and enzyme reset
I_comp  = uncoupling, peroxide shunt, ROS leakage, wrong substrate
D       = D4
```

AMS reading:

```text
P450 is not a wire. It is a redox-depth reaction chamber.
```

## Mechanism 4: Peroxidase and Catalase Routes

Peroxidases and catalases use heme to handle peroxide chemistry.

Peroxidase route:

```text
peroxide arrival
-> heme high-valent intermediate
-> substrate oxidation
-> enzyme reset
```

Catalase route:

```text
peroxide arrival
-> heme intermediate
-> second peroxide engagement
-> water + oxygen release
```

Classification:

```text
R4/O4/D4/G_A
```

Why:

Peroxide is dangerous. Heme enzymes place it into a route chamber where its oxidising force can be used or neutralised.

Failure:

```text
peroxide overload / active-site damage / wrong substrate -> oxidative side route
```

Classification:

```text
R6/O6/D4/G_C
```

## Mechanism 5: Pathological Catalytic Switching

Some heme proteins can switch function under stress. Cytochrome c normally acts as an electron-transfer protein, but oxidative modification and altered ligand coordination can allow peroxidase-like activity against cardiolipin in pathological contexts.

AMS route:

```text
normal electron carrier
-> oxidative/structural perturbation
-> heme pocket altered
-> peroxidase-like route opens
-> membrane lipid damage
```

Classification:

```text
R3/R4/O2/O4/D4/G_C
```

Why:

The heme centre remains active, but its route identity changes. This is not simple loss of function. It is route repurposing into damaging chemistry.

AMS principle:

```text
same heme depth + altered governance = different route identity
```

## Route-State Table

| Heme catalytic situation | Route | Obstruction | Dominance | Grade | Meaning |
|---|---:|---:|---:|---:|---|
| Cytochrome electron relay | `R1` | `O1` | `D1` | `G_A` | narrow real electron route |
| Terminal O2 reduction | `R1/R4` | `O1/O4` | `D1/D4` | `G_A` | governed reduction to water |
| P450 monooxygenase | `R4` | `O4` | `D4` | `G_A` | inward-biased catalytic chamber |
| Peroxidase route | `R4` | `O4` | `D4` | `G_A` | peroxide oxidation route |
| Catalase route | `R4` | `O4` | `D4` | `G_A` | peroxide neutralisation route |
| P450 uncoupling | `R6` | `O6` | `D4` | `G_C` | electron/O2 route leaks into ROS |
| Cytochrome c pathological switching | `R3/R4` | `O2/O4` | `D4` | `G_C` | route repurposed into damaging peroxidase |
| Free heme catalytic damage | `R6` | `O6` | `D4` | `G_C/G_D` | redox centre escapes governance |

## Vorton Interpretation

Heme catalytic systems produce redox-chamber vortons.

### Cytochrome Relay Vorton

```text
heme iron + protein redox path + donor/acceptor alignment
```

Function:

```text
temporary electron-state retention and transfer
```

### P450 Catalytic Vorton

```text
heme iron + O2 + electron/proton delivery + substrate pocket + Fe-oxo intermediate
```

Function:

```text
controlled dangerous oxidation
```

### Peroxidase/Catalase Vorton

```text
heme iron + peroxide + high-valent intermediate + reset route
```

Function:

```text
peroxide capture, transformation, or neutralisation
```

### Pathological Switch Vorton

```text
heme centre + altered ligand geometry + ROS/lipid substrate
```

Function:

```text
damaging route created by governance failure
```

## T1B-to-T1C Implication

Heme redox catalysis shows how material chemistry becomes enzyme function.

T1B:

```text
Fe redox states
porphyrin electronic delocalisation
O2/peroxide chemistry
substrate oxidation potential
```

T1C:

```text
protein chamber
redox partner coupling
proton routing
substrate specificity
product release
cellular detoxification / metabolism / respiration
```

AMS implication:

```text
iron redox depth becomes living chemistry only when staged by protein order.
```

## Cross-Role Comparison

### I1 Versus I2

`I1` heme gas route:

```text
bind, carry, store, release gas
```

`I2` heme catalytic route:

```text
transfer electrons, activate oxygen/peroxide, transform substrate
```

Shared rule:

```text
heme embeds iron depth so it can be governed.
```

### I2 Versus I3

`I2` heme catalysis uses porphyrin/protein chambers.

`I3` Fe-S redox nodes use sulfur bridge closure.

```text
heme = porphyrin-governed iron depth
Fe-S = sulfur-closed iron depth
```

## Failure Grammar

Heme catalytic failure modes:

| Failure | Route profile | Meaning |
|---|---|---|
| Electron leakage | `R6/O6/D4/G_C` | redox route escapes into ROS |
| P450 uncoupling | `R6/O6/D4/G_C` | oxygen activation without productive substrate oxidation |
| Wrong substrate | `R3/O2/D4/G_C` | chamber acts but product route is wrong |
| Peroxide overload | `R6/O6/D4/G_C/G_D` | oxidising pressure exceeds reset route |
| Cytochrome c peroxidase switch | `R3/R4/O2/O4/D4/G_C` | normal relay becomes damaging catalytic route |
| Free heme | `R6/O6/D4/G_C/G_D` | catalytic centre outside containment |

## Testable Expectations

If the AMS `I2` model is coherent, the following should hold:

1. Heme catalysis should depend on active-site geometry, not heme iron alone.
2. Cytochromes should show narrow route behaviour relative to P450 catalytic chambers.
3. P450 substrate binding should alter redox route permission.
4. Uncoupling should produce ROS or peroxide-like side products when electron/O2/substrate/proton timing fails.
5. Peroxidases and catalases should operate near the boundary between detoxification and damaging oxidation.
6. The same heme protein can change route identity if ligand geometry or protein context changes.
7. Free heme should behave as uncontrolled catalytic redox depth.

These expectations align strongly with the source literature.

## Score

Heme redox catalytic route model:

```text
9.5/10
```

Confidence class:

```text
High
```

Reasons:

- heme catalytic biology is broad, mature, and mechanistically rich;
- the AMS distinction between relay, chamber, peroxide route, and failure leakage maps cleanly;
- P450s provide a strong example of governed dangerous chemistry;
- cytochrome c pathological switching confirms that altered governance changes route identity;
- the model reinforces iron as redox depth requiring containment.

Remaining uncertainty:

Detailed electron distribution in some high-valent intermediates, P450 substrate-specific selectivity, and accessory-protein coupling remain complex. These affect fine prediction, not the family-level route model.

## Effect on Iron Family Score

Previous iron family score:

```text
9/10 provisional
```

Updated pressure:

```text
strong upward pressure within 9/10 band
```

Revised iron family score:

```text
9/10 provisional
```

Reason:

`I1` and `I2` are both `9.5/10`, but iron should remain provisional until the storage/transport and ferroptosis maps are complete. Iron's usefulness cannot be separated from its governance burden.

## Next Artifact

Recommended next file:

```text
ams-iron-storage-transport-governance-map-v1.md
```

Purpose:

Map ferritin, transferrin, lactoferrin, ferroportin, hepcidin, cellular labile iron pools, macrophage recycling, intestinal absorption, and route-allocation failures as iron's `I5` role.

