# AMS Heme Oxygen and Gas Route Map v1

## Purpose

This note maps iron's `I1` role:

```text
I1: heme oxygen/gas route centre
```

The iron family entry defined iron as the redox-depth carrier:

```text
Iron carries redox depth that must be embedded, stored, transported, or mineralised to remain useful.
```

Heme oxygen and gas handling is the first detailed iron submodel because it shows the core rule clearly:

> Iron becomes biologically useful when its deep redox/gas-binding capacity is embedded inside a tuned ligand field and protein route.

## Source Anchors

The source base supports these facts:

- Heme is an iron-containing tetrapyrrole central to oxygen transport, gas sensing, oxidative metabolism, mitochondrial respiration, and detoxification.
- Hemoglobin is a tetramer with four heme sites; each heme can bind one oxygen molecule.
- Oxygen binds to the Fe(II) ion of heme.
- Hemoglobin cooperativity lets oxygen affinity shift during oxygenation, making oxygen loading and unloading responsive to physiological oxygen-pressure differences.
- Protein environment and heme-pocket structure tune ligand binding and release.
- Myoglobin stores oxygen in muscle using a heme pocket with different route logic from hemoglobin.
- Carbon monoxide competes with oxygen at the heme iron site and can cause hypoxia by blocking oxygen transport.
- Nitric oxide binds heme proteins and can act as a signal or inhibitor depending on context.
- Free heme is cytotoxic, hydrophobic, can generate reactive oxygen species, and requires tight homeostatic control.

Sources consulted:

- "Molecular Mechanisms of Iron and Heme Metabolism" (`PMC9398995`)
- "An Origin of Cooperative Oxygen Binding of Human Adult Hemoglobin" (`PMC4526547`)
- "The oxygen-binding intermediates of human hemoglobin" (`PMC1233676`)
- "Reverse Engineering the Cooperative Machinery of Human Hemoglobin" (`PMC3842276`)
- "Effective intermediate-spin iron in O2-transporting heme proteins" (`PMC5559043`)
- "Analysis of Fluctuation in the Heme-Binding Pocket and Heme Distortion in Hemoglobin and Myoglobin" (`MDPI Life`, 2022)
- "Binding of Carbon Monoxide to Hemoglobin in an Oxygen Environment" (`PMC11137813`)
- "Nitric oxide inhibition of respiration involves both competitive heme and noncompetitive copper binding to cytochrome c oxidase" (`PMC1334642`)

## AMS Role Assignment

Iron role:

```text
I1: heme oxygen/gas route centre
```

Associated roles:

- `I2`: heme redox/catalytic centre;
- `I5`: storage and transport governance;
- `I6`: toxicity and ferroptosis threshold.

Sulfur comparison:

```text
Fe-S = iron redox depth closed by sulfur
heme = iron redox/gas depth embedded by porphyrin and protein pocket
```

Heme is not merely iron plus a ring. It is iron placed inside an organic field that allows gas-route selectivity.

## Elemental Division of Labour

| Component | AMS contribution | Route function |
|---|---|---|
| Fe(II) centre | gas/redox binding depth | binds O2, CO, NO, other ligands depending on context |
| Porphyrin ring | planar ligand field | embeds and tunes iron geometry |
| Axial protein ligand | vertical coordination | anchors iron into protein state |
| Distal pocket | ligand discrimination field | modulates access, escape, angle, polarity, and competition |
| Globin fold | route container | protects heme and governs gas traffic |
| Hemoglobin tetramer | allosteric route network | couples four heme sites into cooperative loading/release |

AMS formula:

```text
Fe2+ gas-binding depth + porphyrin embedding + protein-pocket tuning = heme gas route centre
```

## Mechanism 1: Basic Heme Oxygen Route

Minimal route:

```text
O2 arrival
-> distal pocket access
-> Fe(II)-O2 binding
-> protein-state response
-> governed release when external conditions shift
```

Classification:

```text
R1/R4/O1/O4/D1/D4/G_A
```

Why:

The route is strongly real but conditional. Oxygen is not simply captured permanently. It is bound in a protein-governed state so it can be loaded, carried, stored, or released.

AMS variables:

```text
B_in    = oxygen availability and pocket access
Q_coh   = heme-pocket geometry and Fe coordination coherence
J_bound = oxygen retained on heme iron
J_trans = successful oxygen delivery/release
B_out   = released oxygen to tissue or downstream respiratory route
I_comp  = CO, NO, oxidation, pocket distortion, free heme leakage
D       = D1/D4
```

## Mechanism 2: Hemoglobin Cooperative Route Network

Hemoglobin is not four independent heme sites in a bag. Its tetrameric structure couples oxygen binding at one site to affinity changes at other sites.

AMS route:

```text
lung O2 pressure
-> first heme oxygen binding
-> subunit/tertiary/quaternary shift
-> increased affinity at remaining sites
-> oxygen-loaded transport state
-> tissue pressure/context shift
-> cooperative release
```

Classification:

```text
R1/R4/O1/O4/D1/D4/G_A
```

Why:

Hemoglobin turns local heme binding into a higher-order allosteric route field. The route is not merely molecular; it is a T1C cooperative transport system.

AMS interpretation:

```text
each heme is a local gas route;
the tetramer is a route-coupled delivery network.
```

The route advantage:

```text
small oxygen-pressure differences become large functional loading/release differences
```

This makes hemoglobin a high-confidence case of higher-order wholeness. The whole carries route behaviour that the isolated heme site does not fully express.

## Mechanism 3: Myoglobin Storage Route

Myoglobin uses heme to hold oxygen in muscle.

AMS route:

```text
oxygen arrival
-> myoglobin heme pocket binding
-> local oxygen reserve
-> release under muscle demand
```

Classification:

```text
R1/O1/D1/G_A
```

Why:

Myoglobin is less of a cooperative transport network and more of a local storage/release route. It stabilises oxygen availability near active tissue.

Contrast:

```text
hemoglobin = cooperative transport route
myoglobin = local storage route
```

## Mechanism 4: Gas Competition and Misrouting

Heme's strength creates vulnerability. Other gases can occupy the route.

### Carbon Monoxide

Carbon monoxide competes with oxygen for the heme iron site.

AMS route:

```text
CO arrival
-> high-affinity heme binding
-> oxygen route blocked
-> tissue hypoxia
```

Classification:

```text
R3/R5/O2/O3/D4/D2/G_C/G_D
```

Why:

The heme route is present but captured by the wrong ligand. It becomes an apparent route that no longer performs its intended oxygen-delivery function.

CO is not merely an external poison. In AMS terms, it is route capture by a competitive ligand.

### Nitric Oxide

Nitric oxide can bind heme systems and function as signal, regulator, or inhibitor depending on context.

AMS route:

```text
NO arrival
-> heme interaction
-> signalling or respiratory inhibition
```

Classification:

```text
governed signal: R4/O4/D4/G_B/G_A
inhibitory capture: R3/O2/D4/G_C
```

Why:

NO sits at the gas-signalling boundary. Context decides whether the route is regulated communication or route interference.

## Mechanism 5: Free-Heme Failure

Heme must be embedded, transported, degraded, or sequestered. Free heme is dangerous.

Failure route:

```text
heme release
-> hydrophobic membrane insertion / nonspecific protein binding
-> peroxidase-like reactivity / ROS
-> oxidative stress and tissue damage
```

Classification:

```text
R6/O6/D4/G_C/G_D
```

Why:

The embedded route centre has escaped its governing field. Iron's redox depth becomes destructive once the heme route is no longer bounded.

This confirms the iron family rule:

```text
iron must be embedded, stored, transported, or mineralised to remain useful.
```

## Route-State Table

| Heme gas situation | Route | Obstruction | Dominance | Grade | Meaning |
|---|---:|---:|---:|---:|---|
| Normal heme O2 binding | `R1/R4` | `O1/O4` | `D1/D4` | `G_A` | governed oxygen capture/release |
| Hemoglobin cooperativity | `R1/R4` | `O1/O4` | `D1/D4` | `G_A` | coupled multi-site transport route |
| Myoglobin storage | `R1` | `O1` | `D1` | `G_A` | local oxygen reserve |
| CO capture | `R3/R5` | `O2/O3` | `D4/D2` | `G_C/G_D` | wrong ligand blocks oxygen route |
| NO signal | `R4` | `O4` | `D4` | `G_B/G_A` | governed gas-signalling route |
| NO inhibition | `R3` | `O2` | `D4` | `G_C` | gas route interference |
| Oxidised/damaged heme pocket | `R3/R6` | `O2/O6` | `D4` | `G_C` | route geometry degraded |
| Free heme toxicity | `R6` | `O6` | `D4` | `G_C/G_D` | route centre escaped containment |

## Vorton Interpretation

Heme oxygen transport creates gas-route vortons.

### Local Heme Vorton

```text
Fe2+ centre + porphyrin ring + axial ligand + distal pocket + O2 ligand
```

Function:

```text
temporary gas-binding closure
```

It must be stable enough to carry oxygen but not so stable that oxygen cannot be released.

### Hemoglobin Allosteric Vorton

```text
four heme vortons + tetrameric protein coupling + oxygen-pressure field
```

Function:

```text
cooperative transport closure
```

This is a higher-order route vorton. The individual heme sites are real, but the tetramer produces a new delivery logic.

### Myoglobin Storage Vorton

```text
single heme pocket + muscle oxygen demand field
```

Function:

```text
local retention and release
```

### CO-Captured Vorton

```text
heme pocket + CO ligand + blocked O2 route
```

Function:

```text
false closure
```

The site is occupied, but the biological route is corrupted.

## T1B-to-T1C Implication

Heme oxygen transport is a clean T1B-to-T1C case.

T1B components:

```text
iron coordination chemistry
porphyrin ligand field
gas-binding equilibrium
```

T1C integration:

```text
globin fold
tetrameric allostery
blood transport
tissue oxygen delivery
metabolic demand response
```

AMS implication:

```text
material redox/gas chemistry becomes physiological route behaviour through protein-governed embedding.
```

This is not a metaphor. The protein system gives the iron centre a new functional identity by controlling access, affinity, competition, and release.

## Cross-Element Comparison

### Iron and Sulfur

Fe-S:

```text
iron redox depth + sulfur closure
```

Heme:

```text
iron redox/gas depth + porphyrin/protein embedding
```

The iron role is shared: depth. The governing structure differs.

### Iron and Phosphorus

Phosphorus carries transferable biological order. Heme iron carries gas-binding and redox depth.

```text
phosphate writes transferable state;
heme iron carries oxygen route state.
```

### Iron and Calcium

Calcium bridges and stabilises. Heme iron binds and releases gas through redox-sensitive coordination.

```text
calcium = relational constraint
heme iron = reversible gas-route depth
```

## Failure Grammar

The heme gas route fails in several distinct ways:

| Failure | Route profile | Meaning |
|---|---|---|
| CO poisoning | `R3/R5/O2/O3/D4/D2/G_C/G_D` | wrong ligand captures oxygen route |
| Methemoglobin/oxidation | `R3/O2/D4/G_C` | iron state no longer supports proper O2 route |
| Free heme toxicity | `R6/O6/D4/G_C/G_D` | embedded redox centre escapes governance |
| Protein-pocket deformation | `R3/O2/D4/G_C` | heme present but route geometry altered |
| Hemoglobin allostery defect | `R3/O2/D4/G_C` | local sites remain but cooperative route weakens |
| NO over-inhibition | `R3/O2/D4/G_C` | signalling gas becomes route interference |

## Testable Expectations

If the AMS `I1` model is coherent, the following should hold:

1. Heme oxygen function should depend on protein-pocket geometry, not iron alone.
2. Hemoglobin should show higher-order route behaviour beyond isolated heme binding.
3. Myoglobin should behave more like local storage than cooperative transport.
4. CO should act as route capture rather than generic toxicity.
5. NO should split into governed signalling and inhibitory route interference depending on concentration and context.
6. Free heme should be damaging because the redox/gas centre has left its governing field.
7. Heme trafficking, sequestration, and degradation should be necessary consequences of heme's power.

These expectations align strongly with the source literature.

## Score

Heme oxygen and gas route model:

```text
9.5/10
```

Confidence class:

```text
High
```

Reasons:

- heme oxygen transport is one of the clearest examples of iron embedded into governed biological route function;
- hemoglobin cooperativity gives a strong higher-order whole case;
- myoglobin supplies a contrasting storage route;
- CO and NO provide clean route-capture and route-boundary tests;
- free-heme toxicity reinforces the iron-family containment rule.

Remaining uncertainty:

Detailed quantitative oxygen-affinity modelling, Bohr effect, 2,3-BPG regulation, fetal/adult hemoglobin contrasts, and pathological hemoglobin variants need separate deeper treatment. They are refinements, not blockers.

## Effect on Iron Family Score

Previous iron family score:

```text
9/10 provisional
```

Updated pressure:

```text
upward pressure within 9/10 band
```

Revised iron family score:

```text
9/10 provisional
```

Reason:

The `I1` model is very strong, but iron should not be locked until at least heme catalysis, Fe-S from iron side, storage/transport, ferroptosis, and magnetite biomineralization are mapped.

## Next Artifact

Recommended next file:

```text
ams-heme-redox-catalytic-route-map-v1.md
```

Purpose:

Map heme iron in cytochromes, mitochondrial electron transport, peroxidases, catalases, P450 enzymes, oxidative metabolism, detoxification, and heme-catalysis failure modes as iron's `I2` role.

