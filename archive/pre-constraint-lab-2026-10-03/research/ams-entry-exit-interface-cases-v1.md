# AMS Entry/Exit Interface Cases v1

## Purpose

This document sharpens the least-developed part of the current optical modelling programme:

- transmissive boundary entry
- transmissive boundary exit

The goal is to stop treating `B_in` and `B_out` as vague interface labels and instead pressure them with explicit geometric cases. The central question is not only whether propagation inside a whole can remain coherent, but how propagation first enters or leaves that whole without collapsing into immediate reflection, destructive scattering, or localised dissipation.

This is especially important because the current programme already separates bulk transmission and bulk reflection reasonably well:

- transmission is mainly driven by `R`, `S`, and `J_dist`
- reflection is mainly driven by `B_ref`, `B_coh`, `J_surf`, and `Q_coll`

What remains underconstrained is the transition from one regime into another.

## Working Assumption

Entry and exit are not merely boundary events in the geometric sense. They are transition events between two differently organised wholes. That means the key problem is not only surface contact, but interface compatibility.

The current working assumption is:

- `B_in` measures the degree to which an incoming transmissive disturbance can be admitted into the receiving whole without being dominantly reflected or destructively scrambled
- `B_out` measures the degree to which an internally propagated disturbance can leave the transmitting whole coherently rather than being trapped, scattered, or incoherently re-radiated

So `B_in` and `B_out` are not simply mirror images. A whole may be relatively permissive for one direction and comparatively poor for the other, depending on the relation between its bulk pathways, surface geometry, and local defect burden.

## Main Variables in Scope

The following variables appear most relevant for entry and exit cases:

- `B_in`
- `B_out`
- `R`
- `S`
- `J_dist`
- `J_surf`
- `Q_coh`
- `D`

Secondary variables:

- `B_ref`
- `B_coh`
- `Q_dest`

## Case 1: Entry into Regular Nested Transmissive Order

### Target

Incoming propagation entering a crystal-like whole with strong internal order.

### Whole Type

Regular nested transmissive order.

### Interface Geometry

The outer boundary is comparatively smooth, while the receiving whole has strongly patterned internal admissibility rather than merely permissive disorder.

### Expected Behaviour

Entry is possible when the incoming disturbance can couple into the receiving order without immediate destructive mismatch. This suggests:

- moderate/high `B_in`
- high `R`
- high `J_dist`
- high `Q_coh`
- comparatively low `D`

The receiving whole is not permissive simply because it is ordered. In fact, excessive order may make entry more selective. The likely picture is:

- lower general permissiveness
- higher coherence for admitted propagation

So crystals may be harder to enter well but better at carrying admitted propagation coherently.

### Main Risk

If the incoming disturbance cannot match the admissible internal patterning, entry may fail locally and be redirected toward reflection or boundary scattering.

### Unresolved Question

How much of entry selectivity is carried by `Q_coh` and how much by the geometry hidden inside `B_in` itself?

## Case 2: Entry into Distributed Permissive Transmissive Order

### Target

Incoming propagation entering a glass-like whole.

### Whole Type

Distributed permissive transmissive order.

### Interface Geometry

The receiving whole is disordered at fine scale but still forms a real higher-order whole with many admissible bulk pathways.

### Expected Behaviour

Glass-like entry currently appears to require:

- medium/high `B_in`
- medium/high `R`
- high `S`
- medium `J_dist`
- medium/high `Q_coh`
- medium/high `D`

The intuition is different from the crystal case. Entry is likely less pattern-selective but more dependent on the receiving whole being able to reseat local disturbance into many neighbouring pathways without catastrophic loss.

This suggests:

- better permissive entry than a highly ordered crystal in some cases
- weaker long-range coherence than a crystal once inside

### Main Risk

High disorder may support admission but also increase local pathway redirection, raising sensitivity to impurity, stress, and micro-defect burden.

### Unresolved Question

What minimum level of `J_dist` is needed for distributed permissiveness to remain transmissive rather than merely diffusive?

## Case 3: Exit from Regular Nested Transmissive Order

### Target

Propagation leaving a crystal-like whole into an adjacent medium.

### Whole Type

Regular nested transmissive order to less ordered or external medium.

### Interface Geometry

Strong internal coherence approaches a boundary where the receiving outside no longer shares the same ordered pathway structure.

### Expected Behaviour

Coherent exit likely requires:

- medium/high `B_out`
- high `R`
- high `Q_coh`
- sufficiently flexible `S` near the boundary
- moderate `J_surf`

The crystal case suggests that exit is not only the reverse of entry. A strongly ordered internal whole may carry propagation very well but still lose coherence at the boundary if its final reseating options are too constrained.

So a crystal may:

- propagate well internally
- exit cleanly only when boundary conditions preserve enough coherence

### Main Risk

Over-ordered local exit geometry may force partial trapping, surface redirection, or structured reflection.

### Unresolved Question

What boundary relaxation mechanism allows a strongly ordered internal pathway to hand off coherently into a less ordered outside medium?

## Case 4: Exit from Distributed Permissive Transmissive Order

### Target

Propagation leaving a glass-like whole.

### Whole Type

Distributed permissive transmissive order to outside medium.

### Interface Geometry

The whole carries distributed bulk propagation, but the final surface region may not preserve the same permissive pathway distribution.

### Expected Behaviour

Clean exit likely depends on:

- medium/high `B_out`
- medium/high `R`
- high `S`
- moderate `J_surf`
- medium `Q_coh`
- controlled `D`

This case likely differs from crystal exit in a crucial way:

- the problem is less rigid mismatch of ordered pattern
- more local disorder concentration at the last interface layer

So exit may be comparatively permissive in principle, but degrade rapidly when surface irregularity rises.

### Main Risk

Bulk permissiveness may not automatically produce clean surface release. If the terminal layer is defect-rich, the disturbance may be scattered or partially dissipated before coherent exit.

### Unresolved Question

How much of poor glass exit is caused by bulk disorder and how much by interface-layer defect concentration?

## Case 5: Mismatched Interface Between Two Transmissive Wholes

### Target

Propagation moving from one transmissive whole into another with different pathway organisation.

### Whole Type

Transmissive whole to transmissive whole, but with mismatched admissibility geometry.

### Interface Geometry

The two wholes are each capable of transmission, but not necessarily by the same local pathway logic.

### Expected Behaviour

This is probably the best diagnostic case for separating `B_in` and `B_out`, because both sides matter simultaneously.

Expected dominant variables:

- `B_out`
- `B_in`
- `Q_coh`
- `J_surf`
- `D`

The key issue is not whether either side can propagate, but whether the interface can mediate a viable reseating from one admissibility structure into another.

Possible outcomes:

- coherent handoff
- partial reflection plus partial transmission
- boundary scattering
- localised dissipation

### Main Risk

The current model may still be too coarse here because it treats whole types more clearly than cross-whole reseating rules.

### Unresolved Question

Do we need an explicit interface compatibility variable rather than overloading `B_in` and `B_out`?

## Case 6: Entry Under Surface Disorder or Impurity

### Target

Incoming propagation meeting a nominally transmissive whole whose surface layer is damaged, contaminated, oxidised, or defect-heavy.

### Whole Type

Transmissive bulk whole with degraded boundary layer.

### Interface Geometry

The outer layer no longer faithfully represents the admissible bulk geometry behind it.

### Expected Behaviour

Dominant variables:

- low/medium `B_in`
- elevated `D`
- degraded `J_surf`
- weakened `Q_coh`
- sometimes elevated `B_ref`

This case matters because it tests whether boundary degradation can block admission even when the underlying whole remains transmissive.

The likely answer is yes:

- transmissive bulk identity is not enough
- the boundary must still provide viable admission geometry

### Main Risk

Current modelling may conflate defect sensitivity with reflection tendency too quickly. Some degraded surfaces may produce diffuse scattering rather than strong reflection.

### Unresolved Question

What pattern of surface damage pushes the interface from weak admission into dominant scattering rather than reflection?

## Cross-Case Provisional Findings

### 1. Entry and Exit Are Not Symmetric

The current cases suggest that:

- entry depends more strongly on admission compatibility
- exit depends more strongly on release coherence

So `B_in` and `B_out` should remain distinct.

### 2. Bulk Transmission Does Not Guarantee Good Entry or Exit

A whole may:

- carry propagation well once internal
- admit it poorly
- release it poorly

This is especially likely where surface geometry and bulk geometry diverge.

### 3. Crystals and Glasses May Both Transmit for Different Reasons

Current working distinction:

- crystals transmit through structured nested admissibility
- glass transmits through distributed permissive admissibility

That suggests different entry and exit pathologies even where both are transmissive in bulk.

### 4. Surface Layers Need Their Own Treatment

The current programme still risks treating surfaces as thin versions of bulk wholes. The cases suggest that this is not enough. Surface layers appear to have their own causal role, especially in:

- admission
- release
- boundary coherence
- defect concentration

## Provisional Modelling Implications

The following additions are now plausible:

### Interface Compatibility Candidate

Introduce a possible derived variable:

- `I_comp`

Meaning:

- the degree to which two adjacent wholes or layers can hand off propagation without dominant incoherence

This may later be decomposed, but it is useful as a placeholder if `B_in` and `B_out` alone remain overloaded.

### Surface-Layer Distinction Candidate

Introduce an explicit distinction between:

- bulk whole
- surface layer
- interface event

This would help separate:

- transmissive identity of the whole
- local entrance behaviour
- local exit behaviour

## Confidence

This document is still exploratory rather than settled.

- structural confidence: `7/10`
- variable separation confidence: `6/10`
- explanatory usefulness confidence: `8/10`

The usefulness score is slightly higher than the variable-separation score because the cases already expose where the current model is weak, even before those weak areas are fully solved.

## Next Move

The most useful next artifact is:

- `ams-entry-exit-parameter-sweep-v1.md`

That should vary:

- `B_in`
- `B_out`
- `J_surf`
- `Q_coh`
- `D`

across the six interface cases and test whether:

- `I_comp` is genuinely needed
- or the existing variable set can still carry the transition logic without another layer.
