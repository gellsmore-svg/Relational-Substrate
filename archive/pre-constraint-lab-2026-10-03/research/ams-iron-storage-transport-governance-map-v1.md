# AMS Iron Storage Transport Governance Map v1

## Purpose

This note maps iron's `I5` role:

```text
I5: redox-depth containment and allocation system
```

The previous iron files mapped heme oxygen/gas routing and heme redox catalysis. Both showed the same rule:

```text
iron is powerful only when governed.
```

This file maps the governance layer itself: how organisms store, transport, recycle, release, restrict, and allocate iron without letting its redox depth become toxicity.

The central claim is:

> Iron storage and transport are not secondary housekeeping. They are the route-governance system that makes iron biology possible.

## Source Anchors

The source base supports these facts:

- Iron is essential for oxygen transport, cellular respiration, DNA synthesis, heme, Fe-S clusters, and many enzymes.
- Iron redox cycling makes it useful but toxic when uncontrolled.
- Vertebrate plasma iron is kept in a relatively narrow range despite variable intake, bleeding, recycling, and tissue demand.
- Most daily iron flow comes from macrophage recycling of senescent erythrocytes, not new absorption.
- Transferrin carries ferric iron in plasma and delivers it to tissues, especially erythroid precursors.
- Ferritin stores iron safely in cells and protects against oxidative damage while preserving bioavailable iron.
- Ferroportin is the major cellular iron exporter, present on enterocytes, macrophages, and hepatocytes.
- Hepcidin is the systemic iron-regulatory hormone.
- Hepcidin binds ferroportin, inducing internalisation/degradation and reducing iron export into plasma.
- High hepcidin restricts plasma iron; low hepcidin permits more iron release and absorption.
- Hepcidin is regulated by iron stores, plasma iron, erythropoietic demand, and inflammation.
- Hepcidin excess causes iron-restrictive states; hepcidin deficiency or resistance causes iron overload.

Sources consulted:

- "Hepcidin and Iron Homeostasis" (`PMC4048856`)
- "The Hepcidin-Ferroportin System as a Therapeutic Target..." (`PMC4034574`)
- "Hepcidin-Ferroportin Interaction Controls Systemic Iron Homeostasis" (`IJMS`, 2021)
- "Recent Advances in Research on Iron Metabolism, Ferritin, and Hepcidin" (`PMC12841351`)
- "Liver iron sensing and body iron homeostasis" (`PMC6318427`)
- "Regulation of the Iron Homeostatic Hormone Hepcidin" (`PMC5227985`)
- "Physiological and pathophysiological mechanisms of hepcidin regulation" (`PMC8164969`)
- Iron family entry: `ams-iron-material-family-entry-v1.md`

## AMS Role Assignment

Iron role:

```text
I5: redox-depth containment and allocation system
```

Associated roles:

- `I1`: heme oxygen/gas route centre;
- `I2`: heme redox/catalytic route centre;
- `I3`: Fe-S redox-depth node;
- `I6`: toxicity and ferroptosis threshold.

Core point:

```text
I5 enables I1-I4 and prevents I6.
```

Iron cannot be treated as merely present or absent. The system must govern:

- chemical state;
- binding carrier;
- compartment;
- release permission;
- storage reserve;
- recycling route;
- absorption rate;
- inflammation/host-defence restriction;
- erythropoietic demand.

## Elemental Division of Labour

| Component | AMS contribution | Route function |
|---|---|---|
| Transferrin | plasma route carrier | carries Fe3+ safely through blood |
| Transferrin receptor | cellular entry gate | imports transferrin-bound iron |
| Endosome/DMT1 route | release and cytosolic entry | converts delivered iron into usable intracellular pool |
| Ferritin | storage vorton | stores iron safely and reversibly |
| Ferroportin | export gate | releases cellular iron to plasma |
| Hepcidin | systemic gatekeeper | closes ferroportin-mediated export |
| Macrophage recycling | recovery route | returns erythrocyte iron to circulation |
| Enterocyte absorption | environmental input route | admits dietary iron into body route system |
| Hepatocyte storage/sensing | reserve and regulator | stores iron and produces hepcidin |

AMS formula:

```text
iron redox depth + carrier binding + storage shell + export gate + hormone control = governed iron route system
```

## Mechanism 1: Transferrin Plasma Routing

Transferrin binds ferric iron and transports it through plasma.

AMS route:

```text
iron export/release
-> transferrin binding
-> circulation
-> transferrin receptor engagement
-> endocytosis
-> endosomal release
-> cytosolic allocation
```

Classification:

```text
R1/O1/D1/G_A
```

Why:

Transferrin converts dangerous free plasma iron into a narrow, controlled delivery route.

AMS variables:

```text
B_in    = iron entering plasma
Q_coh   = transferrin binding capacity and receptor route coherence
J_bound = iron safely bound to transferrin
J_trans = delivery into target cells
B_out   = intracellular usable iron route
I_comp  = non-transferrin-bound iron, inflammatory restriction, overload
D       = D1
```

Failure:

```text
transferrin saturation -> non-transferrin-bound iron -> parenchymal uptake/toxicity
```

Classification:

```text
R6/O6/D4/G_C
```

## Mechanism 2: Ferritin Storage Vorton

Ferritin stores iron in a protein shell, keeping it available while limiting redox damage.

AMS route:

```text
labile intracellular iron
-> ferritin loading
-> mineral/protein storage core
-> controlled mobilisation under demand
```

Classification:

```text
R1/R4/O1/O4/D1/D4/G_A
```

Why:

Ferritin is not passive storage. It is redox-depth containment.

Vorton interpretation:

```text
protein shell + mineral iron core + controlled release route = ferritin storage vorton
```

Failure:

```text
too little ferritin -> labile iron toxicity
too much inaccessible storage -> functional deficiency
storage breakdown -> oxidative release
```

Classifications:

```text
labile toxicity: R6/O6/D4/G_C
functional deficiency: R3/O2/D4/G_C
storage breakdown: R6/O6/D4/G_C
```

## Mechanism 3: Hepcidin-Ferroportin Systemic Gate

Ferroportin exports iron from enterocytes, macrophages, and hepatocytes into plasma. Hepcidin binds ferroportin and causes its internalisation/degradation, reducing iron export.

AMS route:

```text
iron abundance/inflammation signal
-> hepcidin production
-> ferroportin closure/degradation
-> reduced plasma iron entry
```

Low-hepcidin route:

```text
iron deficiency / erythropoietic demand
-> hepcidin suppression
-> ferroportin remains active
-> increased iron entry into plasma
```

Classification:

```text
R4/O4/D4/G_A
```

Why:

This is a systemic conditional gate. It does not transport iron itself; it controls route permission.

AMS variables:

```text
B_in    = body iron signal / inflammation / erythroid demand
Q_coh   = hepatic sensing and ferroportin responsiveness
J_bound = iron retained in enterocytes/macrophages/hepatocytes when gate closed
J_trans = iron export into plasma when gate open
B_out   = transferrin-bound plasma iron availability
I_comp  = hepcidin resistance, excess inflammation, ineffective erythropoiesis
D       = D4
```

## Mechanism 4: Macrophage Recycling Route

Most daily plasma iron flow comes from macrophage recycling of old red blood cells.

AMS route:

```text
senescent erythrocyte uptake
-> heme degradation
-> iron recovery
-> macrophage storage or ferroportin export
-> transferrin loading
-> marrow erythropoiesis
```

Classification:

```text
R1/R4/O1/O4/D1/D4/G_A
```

Why:

This is the dominant high-volume iron route in the adult body. Dietary absorption compensates losses; recycling carries the main flow.

AMS interpretation:

```text
iron biology is circular before it is absorptive.
```

Failure:

```text
macrophage retention under high hepcidin -> iron-restricted erythropoiesis
```

Classification:

```text
R3/O2/D4/G_C
```

## Mechanism 5: Enterocyte Absorption Route

Dietary iron enters through intestinal absorption and must be exported through ferroportin to join the plasma route.

AMS route:

```text
dietary iron uptake
-> enterocyte handling
-> ferroportin export
-> transferrin binding
-> systemic allocation
```

Classification:

```text
R4/O4/D4/G_A
```

Why:

Absorption is conditional and system-regulated. The body lacks a strong active iron excretion route, so entry control matters.

Failure:

```text
excess absorption under low hepcidin -> overload
excess hepcidin -> blocked absorption -> deficiency
```

Classifications:

```text
overload: R6/O6/D4/G_C
restriction: R3/O2/D4/G_C
```

## Route-State Table

| Iron governance situation | Route | Obstruction | Dominance | Grade | Meaning |
|---|---:|---:|---:|---:|---|
| Transferrin-bound plasma iron | `R1` | `O1` | `D1` | `G_A` | safe narrow plasma route |
| Ferritin storage | `R1/R4` | `O1/O4` | `D1/D4` | `G_A` | contained reserve |
| Hepcidin-ferroportin gating | `R4` | `O4` | `D4` | `G_A` | systemic permission control |
| Macrophage recycling | `R1/R4` | `O1/O4` | `D1/D4` | `G_A` | high-volume recovery route |
| Enterocyte absorption | `R4` | `O4` | `D4` | `G_A` | regulated environmental input |
| Non-transferrin-bound iron | `R6` | `O6` | `D4` | `G_C` | overload leakage route |
| Hepcidin excess | `R3` | `O2` | `D4` | `G_C` | iron present but route-locked away |
| Hepcidin deficiency/resistance | `R6` | `O6` | `D4` | `G_C` | export gate remains too open |
| Functional iron deficiency | `R3` | `O2` | `D4` | `G_C` | stores exist but delivery fails |

## Vorton Interpretation

Iron governance creates allocation vortons.

### Transferrin Vorton

```text
Fe3+ + transferrin lobes + receptor route + pH-dependent release
```

Function:

```text
safe plasma delivery
```

### Ferritin Vorton

```text
protein shell + mineral iron core + loading/release gates
```

Function:

```text
safe storage of redox depth
```

### Hepcidin-Ferroportin Vorton

```text
hormone signal + export receptor + internalisation/degradation route
```

Function:

```text
systemic permission switch for iron release
```

### Macrophage Recycling Vorton

```text
erythrocyte uptake + heme breakdown + iron recovery + ferroportin/transferrin export
```

Function:

```text
closed-loop conservation of iron route material
```

## T1B-to-T1C Implication

Iron governance shows that material potency alone is not life.

T1B:

```text
Fe2+/Fe3+ redox chemistry
coordination chemistry
mineral storage potential
```

T1C:

```text
transferrin circulation
ferritin containment
hepcidin-ferroportin systemic control
macrophage recycling
erythropoietic allocation
inflammation-mediated restriction
```

AMS implication:

```text
life does not merely use iron; it builds a whole route economy around iron.
```

## Failure Grammar

Iron governance fails in two opposite directions.

### Restriction Failure

Iron exists but cannot reach the route that needs it.

Examples:

- hepcidin excess;
- inflammation-driven hypoferremia;
- ferroportin loss of function;
- iron trapped in macrophages;
- functional iron deficiency.

Classification:

```text
R3/O2/D4/G_C
```

### Overload Failure

Iron escapes route governance.

Examples:

- hepcidin deficiency;
- hepcidin-resistant ferroportin;
- transferrin saturation;
- non-transferrin-bound iron;
- parenchymal deposition;
- oxidative toxicity.

Classification:

```text
R6/O6/D4/G_C/G_D
```

The AMS rule:

```text
too little route permission causes deficiency;
too much route permission causes toxicity.
```

## Cross-Role Comparison

### I5 and I1/I2

Heme oxygen and catalytic systems require iron delivery and heme governance.

```text
I5 supplies the allocation field;
I1/I2 use the allocated iron in heme routes.
```

### I5 and I6

`I5` prevents `I6`.

```text
storage/transport governance prevents ferroptotic and oxidative failure.
```

### Iron and Sulfur

Sulfur redox buffering protects against iron's failure modes.

```text
iron overload increases oxidative burden;
sulfur thiol systems buffer and repair redox damage until overwhelmed.
```

This means iron and sulfur are coupled not only in Fe-S clusters but also in failure control.

## Testable Expectations

If the AMS `I5` model is coherent, the following should hold:

1. Iron's biological availability should depend more on routing than total iron alone.
2. Transferrin saturation should mark transition from safe route to leakage route.
3. Ferritin should protect against oxidative damage while preserving future availability.
4. Hepcidin excess should produce iron restriction even when total stores are not absent.
5. Hepcidin deficiency or resistance should produce overload by leaving export routes too open.
6. Macrophage recycling should dominate daily iron flow relative to dietary absorption.
7. Inflammation should alter iron distribution as a host-defence route restriction.
8. Iron governance failure should predict both anemia-like deficiency and oxidative overload pathology.

These expectations align strongly with the source literature.

## Score

Iron storage transport governance model:

```text
9.5/10
```

Confidence class:

```text
High
```

Reasons:

- the hepcidin-ferroportin axis is a strong systemic gate model;
- transferrin and ferritin give clear safe-route and storage-route mechanisms;
- macrophage recycling supplies a high-volume route loop;
- the model explains both deficiency and overload as route-permission failures;
- it directly supports the iron-family rule that redox depth requires governance.

Remaining uncertainty:

Intracellular iron trafficking details, labile iron pool dynamics, non-transferrin-bound iron uptake, and some ferroportin mechanistic details remain complex. These affect fine modelling, not the main route-governance claim.

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

`I1`, `I2`, and `I5` are now all `9.5/10`. Iron should still remain provisional until `I6` ferroptosis/toxicity and `I7` biomineralization are mapped, because those define the failure and mineral identity boundaries.

## Next Artifact

Recommended next file:

```text
ams-iron-toxicity-ferroptosis-threshold-map-v1.md
```

Purpose:

Map labile iron, Fenton chemistry, lipid peroxidation, GPX4/GSH protection, ferroptosis, iron overload, heme toxicity, and route-collapse failure as iron's `I6` role.

