# AMS Nitrogen Signalling and Small-Molecule Regulation Route Map v1

## Purpose

This note maps nitrogen's `N6` role:

```text
N6: signalling and small-molecule regulation carrier
```

The previous nitrogen map established:

```text
nitrogen state controls nitrogen meaning.
```

This file maps the signalling side of that state grammar, centred on nitric oxide, nitrate, nitrite, S-nitrosylation, heme sensing, hypoxia-linked reduction, and the boundary between useful regulation and nitrosative stress.

The central claim is:

> Nitrogen can carry biological regulation through small, mobile, state-sensitive molecules. Nitric oxide and related nitrogen oxide species are useful because they are reactive, diffusible, metal-sensitive, thiol-sensitive, and oxygen-context-sensitive; they become destructive when concentration, timing, target, or scavenging escapes governance.

## Source Anchors

The source base supports these facts:

- Nitric oxide is a reactive free-radical diatomic molecule that regulates many physiological processes.
- Nitric oxide synthases produce NO through oxidation of L-arginine to L-citrulline in animals.
- Soluble guanylyl/guanylate cyclase is a primary receptor for NO and contains a heme domain that responds to NO binding by increasing cGMP production.
- NO-sGC-cGMP signalling is central to blood pressure regulation and other physiological processes.
- Nitrate, nitrite, and NO form an interconnected chemical biology.
- Nitrate can be reduced to nitrite, and nitrite can be reduced to NO, especially under hypoxic or pathological oxygen-limited conditions.
- Nitrite can act as an endogenous reservoir for NO-related signalling.
- Nitrogen oxide species interact with biological targets including thiols, metals, heme proteins, dioxygen, and superoxide.
- S-nitrosylation modifies cysteine thiols and can regulate protein interactions and signalling.
- S-nitrosylation is spatially regulated and can interact with other post-translational modifications.
- NO and derived reactive nitrogen species can be beneficial or harmful depending on concentration, spatiotemporal distribution, target, oxygen state, and reactive oxygen species.

Sources consulted:

- "Structure and Activation of Soluble Guanylyl Cyclase, the Nitric Oxide Sensor" (`PMC5240008`)
- "Biological nitric oxide signalling: chemistry and terminology" (`PMC3724101`)
- "Nitrite and nitrate chemical biology and signalling" (`PubMed 30152056`)
- "Nitrite as regulator of hypoxic signaling in mammalian physiology" (`PMC2725214`)
- "S-Nitrosylation signaling regulates cellular protein interactions" (`PMC4035225`)
- "Regulation by S-Nitrosylation of Protein Post-translational Modification" (`PMC3281651`)
- "S-Nitrosylation: An Emerging Paradigm of Redox Signaling" (`PMC6769533`)
- "Protein S-nitrosylation: role for nitric oxide signaling in neuronal death" (`PMC3251724`)
- "Nitric Oxide and Peroxynitrite in Health and Disease" (`PMC2248324`)

## AMS Role Assignment

Nitrogen role:

```text
N6: signalling and small-molecule regulation carrier
```

Associated roles:

- `N5`: oxidation-state and redox diversity carrier;
- `N2`: protein side-chain recognition and active-site nitrogen;
- sulfur `S5`: thiol redox buffering and cysteine targets;
- iron `I1/I2/I3`: heme, Fe-S, and redox-depth targets;
- oxygen: ROS/RNS coupling and hypoxia context;
- phosphorus: cGMP and downstream phosphorylation-regulatory routes;
- carbon: L-arginine substrate, protein targets, metabolic context.

Core distinction:

```text
N5 = nitrogen can occupy many states.
N6 = selected nitrogen states can signal.
```

This file therefore focuses on regulation, not the whole redox ladder.

## AMS Signalling Principle

The signalling principle:

```text
nitrogen signalling depends on governed reactivity.
```

NO is not useful because it is inert. It is useful because it is small, mobile, reactive, and target-sensitive. But the same properties make it dangerous.

AMS interpretation:

```text
signal = routed reactivity.
stress = escaped reactivity.
```

This principle is necessary for N6. Without it, nitric oxide becomes either romanticised as a signalling miracle or flattened into toxicity. The correct model is route-governed reactivity.

## Elemental Division of Labour

| Signalling system | Nitrogen contribution | Other element contributions |
|---|---|---|
| NO | mobile radical signalling state | oxygen/redox context, metal and thiol targets |
| NOS route | NO generation from arginine | carbon skeleton, oxygen, cofactors, protein enzyme |
| sGC route | NO sensing by heme | iron heme target, GTP/cGMP phosphorus route |
| nitrate-nitrite-NO route | reducible NO reservoir | oral microbiome, heme proteins, molybdenum cofactors, hypoxia |
| S-nitrosylation | NO-group transfer to cysteine thiols | sulfur target, protein structure |
| immune NO | high-output reactive nitrogen route | ROS coupling, microbial targets |
| nitrosative stress | escaped RNS chemistry | oxygen radicals, metals, lipids, DNA, proteins |

Nitrogen signalling is therefore inseparable from iron, sulfur, oxygen, carbon, and phosphorus route fields.

## Route Map 1: NOS-Derived Nitric Oxide

Nitric oxide synthases generate NO from L-arginine.

AMS route:

```text
L-arginine + oxygen + cofactors -> NO + L-citrulline
```

This route converts protein/amino-acid nitrogen chemistry into small-molecule signalling chemistry. Arginine, already identified in N2 as a nitrogen-rich side chain, becomes the substrate for a mobile nitrogen oxide signal.

Vorton interpretation:

```text
NOS vorton = enzyme-gated nitrogen signal generator
NO vorton = mobile radical signalling node
```

Route profile:

```text
route class: R1/R4
obstruction class: O1/O4
dominance: D1/D4
grade: G_A
```

AMS implication:

```text
nitrogen signalling begins as enzyme-governed state conversion.
```

NO is not just released chaos. It is generated through a defined route.

## Route Map 2: NO-sGC-cGMP Heme Signalling

Soluble guanylyl cyclase is a major NO receptor.

AMS route:

```text
NO -> ferrous heme in sGC -> conformational activation -> GTP to cGMP -> downstream signalling
```

This is one of the clearest examples of nitrogen signalling through iron. NO binds a heme target, and the protein converts that event into cyclic nucleotide signalling.

Vorton interpretation:

```text
NO-heme vorton = metal-bound signal capture
sGC vorton = heme-to-cyclase transduction route
cGMP vorton = phosphorus-bearing second messenger route
```

Route profile:

```text
route class: R1/R4
obstruction class: O1/O4
dominance: D1/D4
grade: G_A
```

Cross-element formula:

```text
nitrogen signal + iron heme sensor + phosphorus second messenger = vascular/regulatory route
```

AMS implication:

```text
NO signalling is not merely diffusion; it is target-selective capture and transduction.
```

## Route Map 3: Nitrate-Nitrite-NO Reservoir Route

Nitrate and nitrite can act as reservoirs feeding NO-related chemistry.

AMS route:

```text
NO3- -> NO2- -> NO
```

This route is especially important under hypoxia, where nitrite reduction to NO becomes more significant. Nitrite can therefore carry latent NO potential.

Vorton interpretation:

```text
nitrate reservoir vorton = oxidised stored nitrogen signal precursor
nitrite reservoir vorton = reducible NO-ready intermediate
hypoxic NO vorton = oxygen-context-triggered signal release
```

Route profile:

```text
route class: R4
obstruction class: O4/O2
dominance: D4
grade: G_A/G_B
```

AMS implication:

```text
nitrogen signalling can be stored in one oxidation state and released through reduction in another context.
```

This is state-switching as regulation.

## Route Map 4: S-Nitrosylation as Covalent Regulatory Route

S-nitrosylation modifies cysteine thiols by adding an NO-related group.

AMS route:

```text
NO/nitrosating equivalent + cysteine thiol -> S-nitrosothiol -> altered protein interaction/function
```

This route is not the same as NO simply diffusing to heme. It is covalent, local, target-selective, reversible, and integrated with other post-translational modifications.

Vorton interpretation:

```text
S-nitrosylation vorton = nitrogen-sulfur covalent regulatory switch
transnitrosylation vorton = NO-group transfer route between proteins
```

Route profile:

```text
route class: R4/R1
obstruction class: O4/O1
dominance: D4
grade: G_A
```

AMS implication:

```text
nitrogen signal can become a temporary sulfur switch.
```

This directly links nitrogen to the sulfur family:

```text
sulfur carries controllable reactivity.
nitrogen supplies regulatory nitrosyl state.
```

## Route Map 5: Compartmentalised NO Signalling

NO is often described as freely diffusible, but biological signalling is also spatially constrained by source localisation, rapid consumption, target proximity, membranes, organelles, and scavenging chemistry.

AMS route:

```text
local NO source -> nearby target field -> rapid consumption/scavenging -> bounded signal zone
```

Vorton interpretation:

```text
NO microdomain vorton = bounded reactive signalling locality
```

Route profile:

```text
route class: R4/R2
obstruction class: O4/O5
dominance: D4
grade: G_A/G_B
```

AMS implication:

```text
small-molecule signalling is not automatically global; reactivity can create locality.
```

This helps explain how a diffusible molecule can still carry specific biological information.

## Route Map 6: Immune and Cytotoxic NO

NO can participate in immune defence and cytotoxic chemistry, especially at higher or sustained concentrations and in combination with reactive oxygen species.

AMS route:

```text
high-output NO + ROS / metals / microbial targets -> antimicrobial or tissue-damaging chemistry
```

Vorton interpretation:

```text
immune NO vorton = high-output reactive nitrogen defence field
```

Route profile:

```text
route class: R4/R6
obstruction class: O4/O6
dominance: D4
grade: G_B/G_A
```

AMS implication:

```text
the same nitrogen species can be signal, weapon, or damage source depending on output and target.
```

This is governed danger, not contradiction.

## Route Map 7: Signalling-to-Stress Threshold

Nitrogen signalling becomes nitrosative/nitrative stress when concentration, duration, location, or target selection fails.

AMS route:

```text
NO/RNS + excess ROS / wrong target / sustained exposure -> protein, lipid, DNA, metal-centre damage
```

Vorton interpretation:

```text
nitrosative stress vorton = escaped nitrogen-signalling field
```

Route profile:

```text
route class: R6
obstruction class: O6
dominance: D4
grade: G_C/G_D
```

AMS principle:

```text
signalling is not defined by molecule alone; it is defined by governed route conditions.
```

NO can support physiology at one route density and contribute to disease at another.

## Failure and Distortion Modes

### Failure Mode 1: NO Scavenging or sGC Oxidation

If NO is scavenged or the heme target is oxidised/damaged, NO-sGC signalling fails.

```text
route class: R3/R6
obstruction class: O2/O6
dominance: D4
grade: G_C
```

### Failure Mode 2: Excess NO Output

Sustained high NO can shift from signalling to stress.

```text
route class: R6
obstruction class: O6
dominance: D4
grade: G_C/G_D
```

### Failure Mode 3: Wrong S-Nitrosylation Target

Nitrosylation of the wrong cysteine or wrong protein can distort signalling.

```text
route class: R3/R6
obstruction class: O3/O6
dominance: D4
grade: G_C
```

### Failure Mode 4: Failed Denitrosylation or Signal Reset

If S-nitrosylation is not reversed or cleared, a temporary signal becomes persistent distortion.

```text
route class: R6
obstruction class: O6
dominance: D4
grade: G_C
```

### Failure Mode 5: Hypoxic Overproduction

Nitrate/nitrite reduction can help in oxygen limitation, but excessive NO under hypoxia/anoxia can become cytotoxic.

```text
route class: R4/R6
obstruction class: O4/O6
dominance: D4
grade: G_B/G_C
```

## Cross-Element Implications

### Nitrogen and Iron

NO commonly signals by binding iron-heme systems such as soluble guanylyl cyclase.

```text
nitrogen signal is read by iron depth.
```

### Nitrogen and Sulfur

S-nitrosylation places nitrogen signalling onto cysteine sulfur.

```text
nitrogen writes temporary regulatory state onto sulfur.
```

### Nitrogen and Oxygen

Oxygen context controls NO production, consumption, nitrite reduction, ROS coupling, and stress transition.

```text
oxygen determines whether nitrogen signal is released, consumed, or converted into damage.
```

### Nitrogen and Phosphorus

sGC converts GTP into cGMP, making phosphorus-bearing nucleotide chemistry the downstream messenger route.

```text
nitrogen signal activates phosphorus messenger.
```

### Nitrogen and Carbon

NO generation begins from L-arginine, and NO/RNS targets carbon-based proteins, lipids, and nucleic acids.

```text
carbon architecture supplies both substrate and target field for nitrogen signalling.
```

## T1B-to-T1C Implication

At T1B, NO is a small reactive molecule. At T1C, it becomes regulated vascular tone, neurotransmission, immune response, hypoxic adaptation, protein post-translational modification, and stress boundary chemistry.

AMS statement:

```text
T1C life recruits nitrogen's small reactive states as bounded regulatory signals.
```

This strengthens the family identity:

```text
nitrogen carries recognition and state-sensitive regulation.
```

## Confidence Assessment

### Evidence Strength

The evidence base is very strong:

- NO is an established biological signalling molecule;
- NOS-derived NO and sGC/cGMP signalling are well characterised;
- nitrate-nitrite-NO routes are established as complementary NO pathways;
- S-nitrosylation is a major redox-based post-translational modification;
- NO/RNS stress and peroxynitrite-related chemistry are well documented;
- concentration, timing, localisation, and target context are known to affect outcomes.

### AMS Model Strength

The AMS mapping is strong because:

- NO signalling maps directly to governed reactivity;
- sGC shows precise target capture;
- S-nitrosylation links nitrogen and sulfur route grammars;
- nitrate/nitrite routes show state-stored signal potential;
- stress transition maps cleanly to route escape.

### Remaining Uncertainty

The uncertainty lies in scope:

- NO biology is enormous and tissue-specific;
- S-nitrosylation target catalogues are large and context-dependent;
- nitrate/nitrite pathways differ between mammals, plants, microbes, and ecosystems;
- quantitative thresholds require concentration, time, location, oxygen, and target-specific modelling.

## Score

Nitrogen signalling and small-molecule regulation carrier:

```text
Score: 9.5/10
```

Reason:

Nitrogen's role in NO/nitrite/nitrate signalling is direct, mechanism-facing, and biologically broad. The same chemistry also explains the stress boundary, making this a strong route-governance case.

## Effect on Nitrogen Family Score

Previous nitrogen family score:

```text
9.5/10 provisional
```

After this file:

```text
9.5/10 provisional retained
```

Reason:

`N6` confirms that nitrogen carries not only recognition and availability but also state-sensitive regulation.

## Updated Nitrogen Identity

Short form:

```text
Nitrogen carries biological availability and recognition.
```

Expanded form:

```text
Nitrogen carries biological availability, molecular recognition, fold patterning, genetic readability, and chemically switchable regulation through fixation gates, amino addressability, amide restraint, protein-side-chain function, nucleobase identity, redox-state ladders, nitric-oxide signalling, and ecological circulation.
```

Master sentence:

> Nitrogen is the availability-and-recognition element: abundant in the atmosphere but biologically inaccessible without fixation, it enters living order through nitrogenase-gated availability, amino addressability, amide restraint, peptide fold patterning, side-chain recognition, nucleobase readability, redox-state switching, nitric-oxide signalling, and ecological circulation.

## Next Artifact

The next nitrogen artifact should map:

```text
ams-nitrogen-energetic-instability-boundary-route-map-v1.md
```

Target role:

```text
N7: energetic compounds and instability boundary carrier
```

Focus:

- azides;
- nitrates and nitro compounds;
- ammonium nitrate;
- explosive decomposition;
- N2 formation as stable product;
- energetic instability versus atmospheric stability;
- biological versus technological danger;
- route difference between governed nitrogen state and rapid collapse.

