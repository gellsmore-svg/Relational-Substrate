# AMS Iron Toxicity Ferroptosis Threshold Map v1

## Purpose

This note maps iron's `I6` role:

```text
I6: redox-depth failure threshold
```

The previous iron files showed that iron is useful when embedded in heme, staged in catalytic chambers, or governed by storage and transport systems.

This file maps what happens when governance fails.

The central claim is:

> Iron toxicity is not an accidental side effect. It is the negative face of iron's core strength: uncontained redox depth becomes route-destroying oxidation.

## Source Anchors

The source base supports these facts:

- Ferroptosis is an iron-dependent regulated cell-death process driven by lipid peroxidation.
- Ferroptosis is biochemically associated with cystine deficiency, glutathione depletion, GPX4 inactivation, iron loading, and lipid hydroperoxide accumulation.
- The system Xc-GSH-GPX4 axis is a major mammalian ferroptosis-prevention system.
- GPX4 uses glutathione to reduce lipid hydroperoxides to less damaging lipid alcohols.
- Labile ferrous iron contributes to ferroptosis through Fenton chemistry.
- In the Fenton reaction, Fe2+ reacts with hydrogen peroxide to generate hydroxyl radical and Fe3+.
- Lipid peroxidation especially targets polyunsaturated fatty acid-containing phospholipids in membranes.
- Ferritinophagy can release iron from ferritin and expand the labile iron pool.
- Excess heme or non-heme iron can contribute to ferroptotic vulnerability.
- Iron overload after intracerebral haemorrhage can produce ROS and lipid peroxidation, contributing to secondary injury.

Sources consulted:

- "The critical role and molecular mechanisms of ferroptosis in antioxidant systems" (`PMC9011221`)
- "Lipid Peroxidation and Iron Metabolism: Two Corner Stones..." (`PMC9820499`)
- "Iron Metabolism in Ferroptosis" (`PMC7575751`)
- "Bioinorganic Modulators of Ferroptosis" (`PMC9967694`)
- "Ferroptosis: Regulated Cell Death" (`PMC7968485`)
- "Iron toxicity, lipid peroxidation and ferroptosis after intracerebral haemorrhage" (`PMC6613877`)
- "Iron metabolism and ferroptosis in human health and disease" (`PMC12374342`)
- "Mitochondrial Iron Handling and Lipid Peroxidation as Drivers of Ferroptosis" (`PMC12984849`)

## AMS Role Assignment

Iron role:

```text
I6: redox-depth failure threshold
```

Associated roles:

- `I5`: storage and transport governance;
- `I1`: heme oxygen/gas route centre;
- `I2`: heme catalytic route centre;
- `I3`: Fe-S redox-depth node.

Sulfur coupling:

```text
sulfur thiol systems buffer iron-driven oxidative pressure until they are depleted or bypassed.
```

The iron-sulfur relationship therefore has two sides:

```text
Fe-S cluster side: sulfur closes iron redox depth into useful nodes.
Ferroptosis side: sulfur redox buffers protect membranes from iron-driven route collapse.
```

## Core Failure Formula

AMS formula:

```text
labile Fe2+
+ peroxide / ROS
+ PUFA membrane substrate
+ weak GSH/GPX4 repair
= lipid peroxidation route collapse
```

Compact:

```text
unbounded iron depth + failed sulfur repair = ferroptotic membrane failure
```

## Mechanism 1: Labile Iron Pool Expansion

The labile iron pool is the accessible intracellular iron fraction. It sits between uptake, storage, utilisation, and export.

AMS route:

```text
iron uptake / ferritin release / heme breakdown / Fe-S damage
-> labile iron pool expansion
-> increased redox side chemistry
```

Classification:

```text
R3/R6/O2/O6/D4/G_C
```

Why:

The iron may still be inside the cell, but it is no longer safely allocated. It becomes available for competing oxidative routes.

AMS variables:

```text
B_in    = iron released or imported into labile pool
Q_coh   = governance coherence: ferritin, export, chaperones, antioxidant state
J_bound = iron retained in safe forms
J_trans = iron delivered to valid metabolic uses
B_out   = productive heme/Fe-S/enzyme incorporation
I_comp  = Fenton chemistry and lipid peroxidation side routes
D       = D4 shifting toward D2/R6
```

Failure threshold:

```text
I_comp > governance capacity
```

At that point, labile iron stops being an allocation pool and becomes a route-collapse catalyst.

## Mechanism 2: Fenton Radical Route

The Fenton reaction is the core chemical failure route:

```text
Fe2+ + H2O2 -> Fe3+ + OH- + *OH
```

AMS route:

```text
labile Fe2+
-> peroxide encounter
-> hydroxyl radical generation
-> indiscriminate oxidative attack
```

Classification:

```text
R6/O6/D4/G_C/G_D
```

Why:

This is not a governed catalytic route. It is redox depth escaping into destructive side chemistry.

Contrast with heme catalysis:

```text
heme enzyme = protein-governed oxidation chamber
Fenton route = ungoverned oxidation leak
```

The same iron capacity is involved, but the route governance is absent.

## Mechanism 3: Lipid Peroxidation Chain

Ferroptosis depends heavily on peroxidation of membrane phospholipids, especially those containing polyunsaturated fatty acyl chains.

AMS route:

```text
hydroxyl radical / iron-dependent oxidant pressure
-> PUFA phospholipid attack
-> lipid radical propagation
-> lipid hydroperoxide accumulation
-> membrane route failure
```

Classification:

```text
R6/O6/D4/G_D
```

Why:

The membrane is a boundary route. Lipid peroxidation destroys the integrity of that route. Once propagation exceeds repair, the failure is structural and terminal.

AMS interpretation:

```text
ferroptosis is membrane-boundary collapse driven by iron-catalysed oxidative route propagation.
```

## Mechanism 4: GSH-GPX4 Sulfur Repair Route

The main protective axis is:

```text
system Xc- -> cystine uptake -> cysteine -> glutathione -> GPX4 -> lipid hydroperoxide reduction
```

AMS route:

```text
lipid hydroperoxide
-> GPX4 engagement
-> GSH reducing input
-> lipid alcohol
-> membrane route preserved
```

Classification:

```text
R4/O4/D4/G_A
```

Why:

This is governed repair at the iron-sulfur boundary. Sulfur-containing glutathione supplies reducing capacity that prevents iron-driven lipid damage from crossing into collapse.

Failure:

```text
cystine deficiency / GSH depletion / GPX4 inhibition
-> lipid hydroperoxide accumulation
-> ferroptotic route collapse
```

Classification:

```text
R6/O6/D4/G_D
```

AMS principle:

```text
iron creates the danger; sulfur buffering delays or prevents the collapse.
```

## Mechanism 5: Ferritinophagy and Storage Breakdown

Ferritin normally contains iron. Ferritinophagy releases ferritin iron through selective autophagy and can expand the labile iron pool.

AMS route:

```text
ferritin storage
-> NCOA4-mediated ferritinophagy
-> Fe2+ release
-> labile pool expansion
-> increased ferroptotic susceptibility
```

Classification:

```text
R3/R6/O2/O6/D4/G_C
```

Why:

Storage breakdown can be useful when iron is needed. It becomes dangerous when release exceeds allocation and repair capacity.

Governed ferritin mobilisation:

```text
R4/O4/D4/G_B/G_A
```

Ungoverned release:

```text
R6/O6/D4/G_C
```

## Mechanism 6: Heme Toxicity and Hemorrhage

Heme carries iron in a powerful embedded form. When blood breaks down outside normal compartments, heme and iron release can drive oxidative injury.

AMS route:

```text
hemoglobin/heme release
-> heme degradation / iron liberation
-> local iron overload
-> ROS and lipid peroxidation
-> tissue injury
```

Classification:

```text
R6/O6/D4/G_C/G_D
```

Why:

The heme route centre has escaped its intended physiological containment. The embedded redox centre becomes a local toxicity source.

Intracerebral haemorrhage is a strong stress-test case:

```text
blood in brain tissue -> iron overload -> ROS/lipid peroxidation -> secondary injury / ferroptotic contribution
```

## Route-State Table

| Iron toxicity situation | Route | Obstruction | Dominance | Grade | Meaning |
|---|---:|---:|---:|---:|---|
| Healthy labile iron pool | `R4` | `O4` | `D4` | `G_A/G_B` | usable allocation pool |
| Labile iron expansion | `R3/R6` | `O2/O6` | `D4` | `G_C` | governance weakening |
| Fenton radical route | `R6` | `O6` | `D4` | `G_C/G_D` | ungoverned oxidative side route |
| Lipid peroxidation propagation | `R6` | `O6` | `D4` | `G_D` | membrane route collapse |
| GSH-GPX4 repair active | `R4` | `O4` | `D4` | `G_A` | lipid peroxide repair route |
| GSH-GPX4 failure | `R6` | `O6` | `D4` | `G_D` | ferroptotic threshold crossed |
| Governed ferritin mobilisation | `R4` | `O4` | `D4` | `G_B/G_A` | controlled storage release |
| Excess ferritinophagy | `R3/R6` | `O2/O6` | `D4` | `G_C` | storage turns into iron leak |
| Heme release toxicity | `R6` | `O6` | `D4` | `G_C/G_D` | embedded iron centre loses containment |

## Vorton Interpretation

Iron toxicity creates failure vortons.

### Labile Iron Collapse Vorton

```text
Fe2+ pool + peroxide + weak containment
```

Function:

```text
radical-generating side loop
```

### Fenton Vorton

```text
Fe2+/Fe3+ cycling + H2O2 + hydroxyl radical production
```

Function:

```text
destructive redox circulation
```

### Lipid Peroxidation Vorton

```text
PUFA membrane + radical propagation + hydroperoxide accumulation
```

Function:

```text
boundary collapse loop
```

### Protective Sulfur Vorton

```text
cystine/cysteine + GSH + GPX4 + lipid peroxide substrate
```

Function:

```text
membrane repair and ferroptosis prevention
```

The key AMS contrast:

```text
protective vorton wins -> membrane preserved
failure vorton wins -> ferroptosis
```

## T1B-to-T1C Implication

Iron toxicity is a reverse T1C-to-T1B collapse.

Normally:

```text
T1B iron chemistry -> T1C governed heme/Fe-S/enzyme/storage routes
```

In ferroptosis:

```text
T1C governance fails -> T1B-like redox chemistry escapes -> T1C membrane boundary collapses
```

AMS implication:

```text
life maintains higher-order order by preventing raw material potency from escaping its route context.
```

## Cross-Element Comparison

### Iron and Sulfur

Iron:

```text
redox depth and radical risk
```

Sulfur:

```text
thiol buffering and repair capacity
```

Ferroptosis is one of the sharpest iron-sulfur contrast cases:

```text
iron drives lipid oxidation;
sulfur-containing GSH helps stop it.
```

### Iron and Oxygen

Oxygen is required for respiration but creates oxidant pressure.

Iron activates or misactivates oxygen-derived species.

```text
oxygen supplies oxidising substrate;
iron supplies catalytic redox depth.
```

### Iron and Phosphorus

Phospholipids are the membrane route substrate damaged in ferroptosis.

```text
phosphorus helps define membrane order;
iron-driven lipid peroxidation destroys it.
```

## Failure Grammar

Iron `I6` is the clearest failure grammar in the iron family:

| Failure | Route profile | Meaning |
|---|---|---|
| labile iron expansion | `R3/R6/O2/O6/D4/G_C` | allocation becomes leakage |
| Fenton reaction | `R6/O6/D4/G_C/G_D` | redox depth becomes radical generation |
| lipid peroxidation | `R6/O6/D4/G_D` | membrane boundary route collapses |
| GSH depletion | `R6/O6/D4/G_D` | sulfur repair route fails |
| GPX4 inhibition | `R6/O6/D4/G_D` | lipid peroxide repair is blocked |
| ferritinophagy excess | `R3/R6/O2/O6/D4/G_C` | storage route feeds labile pool |
| heme release | `R6/O6/D4/G_C/G_D` | embedded iron escapes containment |

## Testable Expectations

If the AMS `I6` model is coherent, the following should hold:

1. Ferroptosis should require both iron availability and lipid peroxide vulnerability.
2. Expanding the labile iron pool should increase ferroptotic susceptibility.
3. Ferritin storage should protect against ferroptosis unless mobilisation becomes excessive.
4. GSH or GPX4 loss should shift cells sharply toward lipid-peroxidation collapse.
5. Iron chelation should reduce ferroptotic pressure by reducing redox-depth leakage.
6. Heme release or hemorrhage should create local iron-toxicity stress.
7. Membranes rich in vulnerable PUFA phospholipids should be more exposed to ferroptotic route failure.
8. Sulfur redox buffering should be a major counter-route to iron toxicity.

These expectations align strongly with the source literature.

## Score

Iron toxicity and ferroptosis threshold model:

```text
9.5/10
```

Confidence class:

```text
High
```

Reasons:

- the ferroptosis field directly supports iron-dependent lipid peroxidation as a failure mechanism;
- labile iron, Fenton chemistry, GSH-GPX4 protection, and membrane collapse map cleanly into AMS route grammar;
- the model integrates iron governance and sulfur redox buffering;
- failure modes are concrete and experimentally tractable;
- this confirms iron's family identity from the negative side.

Remaining uncertainty:

The exact contribution of mitochondria, lipoxygenases, autophagy, FSP1-CoQ10, DHODH, BH4, and cell-type-specific regulators varies by context. These refine the model but do not weaken the core iron-failure route.

## Effect on Iron Family Score

Previous iron family score:

```text
9/10 provisional
```

Updated pressure:

```text
very strong upward pressure within 9/10 band
```

Revised iron family score:

```text
9/10 provisional
```

Reason:

`I1`, `I2`, `I5`, and `I6` are now all `9.5/10`. Iron should remain provisional until `I7` magnetic biomineralization and `I8` mineral-redox bridge are mapped, because those define iron's mineral identity and geochemical continuity.

## Next Artifact

Recommended next file:

```text
ams-iron-magnetic-biomineralization-route-map-v1.md
```

Purpose:

Map magnetotactic bacteria, magnetosomes, magnetite, greigite, iron concentration, redox/pH control, nucleation, crystal size/shape, chain organisation, and magnetic orientation as iron's `I7` role.

