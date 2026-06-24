# AMS Route Variable Mathematical Framework v1

## Purpose

This note formalises the core AMS route variables introduced throughout the research corpus.

The previous closure-formalism file defined:

- substrate region;
- local state field;
- constraint flow;
- vorton conditions;
- closure and coherence;
- route admissibility;
- threshold transitions.

That file answered:

```text
what are the objects?
```

This file answers:

```text
what do the main AMS variables mean,
how should they be related,
and how do they constrain route behaviour?
```

## Central Claim

The central claim is:

> The AMS route variables can be treated as a semi-formal state vector describing whether a closure-pattern remains bounded, coherent, transmissible, and competitively dominant enough to count as a viable route-bearing identity. The variables are not arbitrary descriptive tags; they are coupled measures of retention, exposure, junction quality, transition quality, dominance, and route competition.

## Variable Set

The current core variable set is:

```text
B_in
B_out
Q_coh
J_bound
J_trans
D
I_comp
```

For some analyses, two auxiliary variables are also useful:

```text
L_diff
X_frag
```

where:

- `L_diff` = diffusive loss tendency;
- `X_frag` = fragmentation tendency.

## State Vector

The simplest formal bundling is:

```text
Z(V,t) = [B_in, B_out, Q_coh, J_bound, J_trans, D, I_comp, L_diff, X_frag]
```

for a vorton or coupled system `V` at time `t`.

This is the route-state vector.

The point is not that every variable is fundamental in the same way. The point is that the system state can be discussed through a fixed vector rather than drifting prose.

## Variable Definitions

## 1. Inward Boundedness `B_in`

### Meaning

`B_in` measures how strongly a pattern retains organised constraint within its own closure region.

It answers:

```text
how strongly does the pattern hold itself together against dispersal?
```

### Formal Role

High `B_in` raises:

- persistence;
- local retention;
- return-path viability.

Low `B_in` raises:

- leakage;
- route weakening;
- failure of local identity.

### First-pass range

Normalise:

```text
0 <= B_in <= 1
```

Interpretation:

```text
0   = no effective inward retention
1   = maximal inward retention for the chosen normalisation
```

### Important risk

Very high `B_in` with very low spread is not automatically good.

That is why `B_in` must be read with `D_spread` or equivalent distribution terms rather than alone.

## 2. Outward Boundary Pressure `B_out`

### Meaning

`B_out` measures the effective external pressure acting across the closure boundary.

It answers:

```text
how strongly is the pattern being pressed, perturbed, loaded, or drained by its environment?
```

### Sources of `B_out`

Depending on context, `B_out` may include:

- neighbouring route demand;
- field gradients;
- solvent or thermal pressure;
- charge imbalance;
- external coupling demands;
- environmental perturbation.

### First-pass range

Normalise:

```text
0 <= B_out <= 1
```

### Relation to persistence

Persistence requires not:

```text
B_in high in isolation
```

but:

```text
B_in sufficient relative to B_out
```

This leads to the first basic ratio:

```text
R_bound = B_in / (B_out + ε)
```

where `ε > 0` prevents division singularity.

Interpretation:

```text
R_bound >> 1  -> strong retention relative to environmental load
R_bound ~ 1   -> marginal retention
R_bound << 1  -> likely failure or diffusive loss
```

## 3. Coherence `Q_coh`

### Meaning

`Q_coh` measures the internal compatibility of local state transitions.

It answers:

```text
can the pattern reseat lawfully without tearing itself apart?
```

### First-pass range

Normalise:

```text
0 <= Q_coh <= 1
```

Interpretation:

```text
0   = incoherent, internally conflicting
1   = maximally coherent for chosen normalisation
```

### Role

High `Q_coh` supports:

- stable identity;
- smooth reseating;
- productive route completion;
- genuine higher-order wholeness.

Low `Q_coh` supports:

- hidden internal competition;
- false persistence;
- fragmentation under load.

### Important distinction

```text
B_in asks whether the pattern is held
Q_coh asks whether what is held behaves as one thing
```

## 4. Boundary Junction Quality `J_bound`

### Meaning

`J_bound` measures the quality of stable boundary interfaces.

It answers:

```text
how well can the pattern couple to neighbouring structure without losing identity at the interface?
```

Examples:

- hydration shell interface;
- membrane boundary interface;
- crystal or oxide boundary;
- protein docking boundary;
- machine surface coupling.

### First-pass range

Normalise:

```text
0 <= J_bound <= 1
```

Interpretation:

```text
0   = poorly formed or destructive boundary junction
1   = highly stable and selective boundary coupling
```

### Role

High `J_bound` supports:

- stable exchange;
- selective interface;
- coherent coupling between wholes.

Low `J_bound` supports:

- spill;
- rupture;
- false docking;
- leakage across the interface.

## 5. Transition Junction Quality `J_trans`

### Meaning

`J_trans` measures the quality of internal or interfacial transitions through which route progress occurs.

It answers:

```text
how well can constraint or process move from one state to another without stalling, pocketing, or fragmenting?
```

Examples:

- electron-transfer relay;
- proton-transfer path;
- peptide-bond elongation step;
- codon-to-amino-acid matching transition;
- ATP capture transition.

### First-pass range

Normalise:

```text
0 <= J_trans <= 1
```

Interpretation:

```text
0   = transition effectively blocked or destructive
1   = highly permissive and coherent transition
```

### Important distinction

```text
J_bound = quality of interface stability
J_trans = quality of route passage through a state change
```

Some systems may have strong boundary stability but weak transition permissibility, or the reverse.

## 6. Dominance `D`

### Meaning

`D` measures which behavioural regime currently dominates the route field.

Earlier work used categorical dominance labels:

- `D1` route-dominant;
- `D2` pocket-dominant;
- `D3` diffusion-dominant;
- `D4` mixed competitive.

### Semi-formal representation

Rather than a single scalar only, treat dominance as a regime selector:

```text
D ∈ {D1, D2, D3, D4}
```

optionally backed by regime scores:

```text
d = [d_route, d_pocket, d_diff, d_mix]
```

with:

```text
Σ d_i = 1
```

and `D` assigned by whichever `d_i` is greatest.

### Meaning of regimes

```text
D1 -> productive route behaviour dominates
D2 -> local trapping/pocketing dominates
D3 -> diffusion and loss dominate
D4 -> no clean dominance; competing partial behaviours
```

This mixed discrete-continuous form is better than a raw scalar because the regime labels are already doing real analytical work.

## 7. Competitive Interaction `I_comp`

### Meaning

`I_comp` measures the degree to which multiple possible routes, pockets, sinks, or closures compete inside the same system.

It answers:

```text
how much unresolved competition exists among candidate behaviours?
```

### First-pass range

Normalise:

```text
0 <= I_comp <= 1
```

Interpretation:

```text
0   = one behaviour overwhelmingly dominant, little competition
1   = strong unresolved competition among candidate behaviours
```

### Role

High `I_comp` often correlates with:

- mixed dominance;
- metastability;
- delayed threshold failure;
- context sensitivity.

Low `I_comp` often correlates with:

- cleaner route classification;
- stronger predictability;
- more stable functional identity.

## Auxiliary Variables

## 8. Diffusive Loss `L_diff`

### Meaning

`L_diff` measures tendency toward non-productive spread and loss.

Range:

```text
0 <= L_diff <= 1
```

Role:

High `L_diff` lowers admissibility and weakens closure.

## 9. Fragmentation Tendency `X_frag`

### Meaning

`X_frag` measures tendency toward breakup, internal incompatibility, or route-destroying discontinuity.

Range:

```text
0 <= X_frag <= 1
```

Role:

High `X_frag` is more severe than high `L_diff`.

Diffusion means:

```text
order is thinning
```

Fragmentation means:

```text
order is tearing
```

## Core Relations

The variables now need coupled relations.

## Relation 1: Effective Retention

Define:

```text
E_ret = B_in * Q_coh
```

Interpretation:

```text
retention without coherence is weak identity
coherence without retention is unstable identity
```

So effective retention depends on both.

## Relation 2: Effective Exposure Stress

Define:

```text
E_stress = B_out + L_diff + X_frag
```

Interpretation:

External load, diffuse loss, and fragmentation all contribute to route stress.

## Relation 3: Interface Capacity

Define:

```text
E_int = α * J_bound + β * J_trans
```

with:

```text
α, β > 0
```

Interpretation:

Some systems fail because their boundaries are poor.
Others fail because their transitions are poor.
`E_int` captures both.

## Relation 4: Route Viability

A first-pass route viability score can now be written:

```text
V_route = E_ret + E_int - E_stress - γ * I_comp
```

where:

```text
γ > 0
```

Interpretation:

Route viability rises with:

- retention;
- coherence;
- good interfaces and transitions.

It falls with:

- external load;
- diffusive loss;
- fragmentation;
- unresolved competition.

### Threshold reading

```text
V_route >> 0   -> strong viable route
V_route > 0    -> weak but real route
V_route ~ 0    -> threshold / unstable case
V_route < 0    -> pseudo-route or failure route
```

## Relation 5: Dominance Assignment

Use:

```text
D1 if V_route high and pocket/diffusion penalties low
D2 if local retention exists but J_trans poor and pocket terms dominate
D3 if L_diff dominates
D4 if no regime strongly dominates because I_comp is high
```

This gives a more explicit basis for the categorical dominance labels.

## Route-Class Conditions

The earlier route classes can now be expressed in terms of the variable set.

### R1: Narrow Viable Route

Requires:

```text
high B_in
high Q_coh
high J_trans
moderate/high J_bound
low I_comp
low L_diff
low X_frag
D = D1
```

### R2: Distributed Weak Routes

Requires:

```text
moderate B_in
moderate Q_coh
moderate J_trans
non-negligible I_comp
non-negligible L_diff
D often mixed between D1 and D4
```

### R3: Blocked Apparent Route

Requires:

```text
reasonable local retention
but poor J_trans or high late obstruction
V_route near or below 0 after transition penalties
```

### R4: Inward-Biased Route

Requires:

```text
high B_in relative to through-transition quality
moderate/high Q_coh
route deepens internal closure more than external completion
```

### R5: Loop-Dominated Pseudo-Route

Requires:

```text
circulation-like retention
moderate closure
weak net transition completion
often moderate/high I_comp
```

### R6: Fragmenting Route Field

Requires:

```text
high X_frag
falling Q_coh
often high B_out and/or L_diff
D = D3 or unstable D4
```

## State-Space Interpretation

The route variables define a state space.

Each system occupies a point or moving region in:

```text
Z-space
```

Transitions can then be described as trajectories:

```text
Z(t1) -> Z(t2) -> ...
```

Examples:

### Stable Route

```text
high B_in
high Q_coh
high J_trans
low I_comp
low X_frag
```

### Metastable Route

```text
moderate B_in
moderate Q_coh
high I_comp
moderate L_diff
low/moderate X_frag
```

### Collapse Trajectory

```text
B_in down
Q_coh down
J_trans down
L_diff up
X_frag up
```

This gives the programme a more explicit way to talk about:

- weakening;
- tipping;
- pseudo-stability;
- sudden failure.

## Coupled-System Variables

For higher-order wholes, define system-level effective variables:

```text
B_in(W)
Q_coh(W)
J_bound(W)
J_trans(W)
I_comp(W)
...
```

These are not simple averages.

They should be treated as weighted functions of:

- component states;
- coupling strengths;
- bottleneck transitions;
- weakest-link or strongest-link behaviours depending on system type.

### First-pass coupled closure

For a coupled system `W`:

```text
C(W) = Φ(component closure, coupling quality, whole coherence)
```

where:

```text
Φ` must exceed whole-level threshold for W to count as a real higher-order whole
```

This is the variable-level counterpart to the coupled-wholeness criterion from the previous file.

## Failure Signatures

The variable system gives specific failure signatures.

### Diffusive Failure

```text
B_in modest
Q_coh modest
L_diff rising
X_frag low/moderate
```

Interpretation:

The system thins out before it tears apart.

### Pocket Failure

```text
B_in local high
J_trans low
I_comp moderate/high
D -> D2
```

Interpretation:

Constraint gets trapped without productive route completion.

### Fragmentation Failure

```text
Q_coh collapses
X_frag rises sharply
J_trans falls
D -> D3 or unstable D4
```

Interpretation:

The system no longer behaves as one thing.

### Counterfeit Stability

```text
B_in moderate/high
Q_coh low/moderate
I_comp high
apparent persistence without clean route completion
```

Interpretation:

This is one of the most important variable signatures for corruption-style false persistence.

## What This Enables

This variable framework now makes several things possible.

### 1. More disciplined scoring

Family and route-model scores can now be tethered more explicitly to:

- closure quality;
- coherence quality;
- transition quality;
- competition burden;
- failure sensitivity.

### 2. More disciplined comparison

Two candidate models can be compared by asking:

```text
which gives better Z-state coherence?
which predicts cleaner dominance?
which better explains observed transition patterns?
```

### 3. More disciplined edge-case analysis

Borderline living states, metastable materials, and machine-failure states can all be discussed through variable movement rather than prose alone.

## What Still Remains Open

This is still not a fully closed mathematical theory.

Open issues:

- exact formulas for `B_in`, `Q_coh`, etc. in specific physical systems;
- rigorous mapping to measurable observables;
- topology-specific versions of the variable set;
- exact weighting constants and non-linear forms;
- state-space bifurcation analysis;
- coupled-system aggregation rules.

These remain for later files.

## Compact Variable Grammar

The best current compression is:

```text
AMS route behaviour is governed by retention, exposure, coherence, interface quality, transition quality, dominance regime, and unresolved competition, with diffusion and fragmentation as the main loss channels.
```

Expanded:

```text
The route-state of a vorton or coupled system can be represented by a bounded state vector whose components measure whether the pattern holds together strongly enough, interfaces cleanly enough, transits lawfully enough, and dominates competitively enough to preserve identity rather than thinning, trapping, or fragmenting.
```

## Score Recalibration

### Constraint Gain

This file materially tightens the model by turning the variable language into an explicit state-vector framework.

Score:

```text
8.5/10
```

### Formal Sufficiency

It remains semi-formal and depends on later system-specific definitions.

Score:

```text
7.5/10
```

### Programme Value

As a bridge between qualitative grammar and later mathematical modelling, it is high value.

Score:

```text
9.0/10
```

## Provisional Conclusion

The AMS programme now has a first-pass mathematical framework for its route variables.

AMS summary:

```text
Route viability depends on the coupled state of inward retention, outward load, coherence, boundary quality, transition quality, dominance regime, and competitive interference, with diffusion and fragmentation acting as the main routes of loss.
```

Score:

```text
route variable mathematical framework: 8.5/10 as scaffold
```

## Recommended Next Workstream

The best next artifact is:

```text
ams-topology-transition-criteria-v1.md
```

Reason:

The objects and variables are now defined. The next dependency is to formalise when a system:

- stays in the same identity class;
- lawfully reconfigures;
- slips into metastability;
- fragments into another route regime.
