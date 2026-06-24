# AMS Respiration Failure Propagation Matrix v1

## Purpose

This note maps how failure propagates through the respiration and ATP-synthesis machine.

The previous quantitative comparison established that respiration is:

```text
the higher-pressure, higher-catastrophic-risk core runtime machine
```

The task now is to make that more explicit by asking:

```text
when respiration fails,
how does the failure move through the system?
```

This file is therefore a propagation matrix, not just another summary.

## Central Claim

The central claim is:

> Respiration rarely fails as a single isolated event. It fails as a propagation structure: disturbances in redox depth, oxygen closure, membrane asymmetry, or ATP capture can cascade into one another, producing escalating transitions from reduced efficiency to oxidative fragmentation, energy starvation, membrane disorder, and wider cell-state collapse. The most important feature of respiratory failure is not merely local damage but loss of coupling among depth, closure, field, and capture.

## Core Runtime Chain Recap

The healthy machine was previously compressed as:

```text
Iron carries the depth.
Sulfur keeps parts of that depth narrow.
Oxygen closes the depth and helps carry the proton field.
Phosphorus captures the field as ATP.
Carbon and nitrogen build the machine that makes all of that governable.
```

Failure propagation can now be understood as:

```text
breaks or weakens in any part of this chain
spilling into the others
```

## Formal Variable Recap

The current route-state framework uses:

```text
B_in
B_out
Q_coh
J_bound
J_trans
D
I_comp
L_diff
X_frag
```

Respiration's semi-quantitative signature was:

```text
B_in   = 0.82
B_out  = 0.74
Q_coh  = 0.88
J_bound = 0.84
J_trans = 0.91
I_comp = 0.52
L_diff = 0.18
X_frag = 0.62 under failure pressure
```

This file now traces how perturbations in those variables propagate.

## Failure Matrix

| Primary disturbance | Immediate variable effect | First machine consequence | Secondary propagation | Whole-system danger |
|---|---|---|---|---|
| Iron-depth instability | `Q_coh↓`, `J_trans↓`, `X_frag↑` | unreliable electron relay | oxygen leak / ROS / ATP fall | oxidative and energetic collapse |
| Sulfur-route weakening | `J_trans↓`, `I_comp↑`, `X_frag↑` | Fe-S relay instability, weaker governance | redox misrouting, leak, repair burden | transition to fragmentation |
| Oxygen terminal-closure weakening | `J_trans↓`, `B_out↑`, `X_frag↑` | incomplete reduction, ROS increase | proton pumping weakens, ATP falls | oxidative-field failure |
| Membrane proton leak | `B_in↓`, `J_bound↓`, `L_diff↑` | gradient weakens | ATP synthesis impaired, transport burden rises | boundary and energy failure |
| ATP-capture impairment | `J_trans↓`, effective output collapse | low transferable order | translation/repair slow, recovery weakens | cell-state decline |
| Repair / antioxidant overload | `Q_coh↓`, `X_frag↑`, `I_comp↑` | ROS no longer buffered well | protein, lipid, DNA damage rises | generalised failure escalation |

This table is the main result of the file.

## Propagation Class 1: Iron-Depth Destabilisation

### Trigger

Examples:

- heme dysfunction;
- Fe-S instability;
- non-heme catalytic miscoupling;
- labile iron expansion.

### Variable shift

```text
Q_coh down
J_trans down
X_frag up
```

### Immediate consequence

The machine loses clean staged redox descent.

That means:

- relay becomes less narrow;
- off-path transfers increase;
- oxygen-facing chemistry becomes less well governed.

### Propagation

```text
iron-depth instability
-> oxygen leak or incomplete reduction
-> ROS increase
-> membrane and protein damage
-> ATP production falls further
```

### Interpretation

This is the classical:

```text
depth escapes governance
```

failure mode.

It is one of the most dangerous because the initiating family is itself one of the highest-energy parts of the machine.

## Propagation Class 2: Sulfur-Route Weakening

### Trigger

Examples:

- Fe-S cluster damage;
- thiol-state stress;
- redox repair burden exceeding capacity.

### Variable shift

```text
J_trans down
I_comp up
X_frag up
```

### Immediate consequence

Sulfur can no longer keep parts of iron depth narrow and governable.

This increases:

- branch ambiguity;
- relay failure;
- misactivation risk.

### Propagation

```text
sulfur-route weakening
-> iron relay disorder
-> oxygen closure weakens
-> ROS rises
-> repair burden rises further
```

### Interpretation

This is a recursive danger:

```text
governance failure produces more of the stress that governance was needed to restrain
```

That is why sulfur is so important in keeping respiration from sliding toward `T4`.

## Propagation Class 3: Oxygen-Closure Weakening

### Trigger

Examples:

- impaired terminal oxidase function;
- limited oxygen availability;
- poor catalytic closure at terminal step;
- disrupted oxygen activation logic.

### Variable shift

```text
J_trans down
B_out up
X_frag up
```

### Immediate consequence

Oxygen is no longer being used as:

```text
productive terminal closure
```

but increasingly becomes:

```text
pressure without clean discharge
```

### Propagation

```text
poor oxygen closure
-> incomplete reduction / ROS
-> weaker proton pumping
-> lower ATP
-> weaker repair and translation
-> more system-wide instability
```

### Interpretation

This is the main `O5 -> O6` failure corridor inside the machine.

## Propagation Class 4: Membrane Proton-Field Leak

### Trigger

Examples:

- membrane disruption;
- uncoupling;
- channel/path leak;
- lipid peroxidation weakening boundary integrity.

### Variable shift

```text
B_in down
J_bound down
L_diff up
```

### Immediate consequence

The machine may still move electrons, but:

```text
field asymmetry no longer holds well
```

### Propagation

```text
proton leak
-> weaker ATP synthesis
-> energy shortage
-> reduced repair and translation support
-> boundary maintenance weakens further
```

### Interpretation

This is the classic:

```text
redox still running, capture failing
```

state.

It proves that electron transport alone is not the whole machine. Capture matters.

## Propagation Class 5: ATP-Capture Impairment

### Trigger

Examples:

- ATP synthase dysfunction;
- phosphate or coupling disruption;
- collapse in usable transfer packet generation.

### Variable shift

```text
J_trans down at capture step
effective output down
```

### Immediate consequence

Transferable biological order falls even if some upstream redox function remains.

### Propagation

```text
ATP capture impairment
-> translation slowdown
-> repair slowdown
-> transport and signalling pressure
-> architecture not renewed adequately
```

### Interpretation

This failure class is especially important because it shows:

```text
machine activity can continue
while useful runtime order still falls below viability threshold
```

That is a critical distinction for the wider ontology.

## Propagation Class 6: Antioxidant / Repair Overload

### Trigger

Examples:

- sustained ROS increase;
- sulfur-buffer exhaustion;
- cumulative oxidative damage.

### Variable shift

```text
Q_coh down
X_frag up
I_comp up
```

### Immediate consequence

The machine can no longer maintain clean local conditions for:

- redox centres;
- membranes;
- proteins;
- route specificity.

### Propagation

```text
repair overload
-> higher ROS persistence
-> more membrane and protein damage
-> poorer machine coherence
-> more leak and less capture
```

### Interpretation

This is the positive-feedback collapse path.

Once it dominates, the machine moves quickly from:

```text
T2 metastable drift
to
T3 threshold crossing
to
T4 fragmentation
```

## Propagation Network

The matrix can be condensed into a network.

```text
iron-depth disorder
-> sulfur governance strain
-> oxygen-closure weakness
-> ROS increase
-> membrane leak
-> ATP capture decline
-> weaker translation/repair
-> more iron/sulfur/oxygen instability
```

This is the main respiratory collapse loop.

It shows why respiratory failure is especially dangerous:

```text
it is self-amplifying once several links weaken at once
```

## Transition-Class Reading

The propagation matrix can now be tied to transition classes.

### T0 Healthy Persistence

Profile:

```text
all major links strongly coupled
V_route strongly positive
```

### T1 Lawful Reconfiguration

Profile:

```text
load changes or transient perturbations absorbed
without loss of machine identity
```

### T2 Metastable Drift

Profile:

```text
ATP still adequate
ROS elevated but buffered
proton field weaker but recoverable
repair burden rising
```

### T3 Threshold Crossing

Profile:

```text
oxygen closure degrades
membrane leak rises
ATP capture falls below robust margin
repair starts to lose ground
```

### T4 Fragmentation

Profile:

```text
ROS and leak dominate
capture collapses
repair cannot recover coupling
whole machine no longer behaves as one route-bearing system
```

This transition reading makes the collapse story much more precise.

## Family-Weighted Interpretation

The propagation matrix also clarifies family roles under failure.

### Iron

```text
initiates high-cost failure if depth escapes
```

### Sulfur

```text
slows or accelerates transition depending on governance integrity
```

### Oxygen

```text
shifts from productive closure to fragmentation pressure
```

### Phosphorus

```text
records failure downstream as falling transferable order
```

### Carbon

```text
absorbs downstream architecture and membrane damage
```

### Nitrogen

```text
suffers later via weakened translation and repair fidelity
```

This sequence is useful because it locates not just what fails, but where failure is first expressed and where it later appears.

## Quantitative Compression

The best current compression is:

```text
Respiration fails catastrophically when depth, closure, field, and capture stop remaining coupled, because disruption in any one of those domains tends to propagate into the others rather than stay local.
```

Expanded:

```text
The respiration machine is highly efficient but failure-sensitive: iron-depth disorder, sulfur-governance weakening, oxygen-closure failure, membrane proton leak, ATP-capture impairment, and antioxidant overload each shift the same route-state vector toward lower coherence, lower transition quality, higher competition, and higher fragmentation, producing escalating whole-system collapse.
```

## What This Still Does Not Do

This file is a propagation scaffold, not a finished dynamic simulation.

It does not yet provide:

- exact temporal equations for collapse progression;
- weighting constants for each branch of propagation;
- measured thresholds for specific biological systems;
- probabilistic transition modelling.

Those remain later tasks.

## Score Recalibration

### Calibration Gain

This file substantially improves the machine-level failure side of the programme.

Score:

```text
8.5/10
```

### Formal Sufficiency

It remains matrix-structured rather than fully dynamical.

Score:

```text
7.5/10
```

### Programme Value

As a calibration bridge between the formal scaffold and the cell-failure ontology, it is very high value.

Score:

```text
9.0/10
```

## Provisional Conclusion

The respiration machine can now be analysed as a failure-propagation structure rather than a single black-box failure state.

AMS summary:

```text
Respiratory collapse propagates because iron depth, sulfur governance, oxygen closure, proton-field asymmetry, and ATP capture are tightly coupled; when one weakens, the others are driven toward lower coherence and higher fragmentation until whole-machine viability is lost.
```

Score:

```text
respiration failure propagation matrix: 8.5/10 as calibration step
```

## Recommended Next Workstream

The best next artifact is:

```text
ams-ribosome-route-dependency-matrix-v1.md
```

Reason:

The energy-side machine now has a propagation matrix. The next balanced move is to do the same for the information-side machine so the comparison becomes symmetrical.
