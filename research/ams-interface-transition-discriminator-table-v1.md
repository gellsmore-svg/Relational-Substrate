# AMS Interface Transition Discriminator Table v1

## Purpose

This document turns the entry/exit sweep into a harder interface test.

The aim is to distinguish five different interface outcomes:

- successful handoff
- partial handoff
- dominant reflection
- dominant scattering
- dominant trapping

The question is no longer only which variables matter. It is:

- which variable combinations separate these outcomes clearly enough to guide further modelling

This document uses the current interface variable set:

- `B_in`
- `B_out`
- `J_surf`
- `Q_coh`
- `D`

and the provisional derived term:

- `I_comp`

## Outcome Definitions

### Successful Handoff

Propagation passes across the interface and remains functionally coherent in the receiving whole. Local loss may exist, but it does not dominate the event.

### Partial Handoff

Propagation is divided across outcomes. Some coherent transmission occurs, but significant loss, redirection, or degradation occurs at the same interface.

### Dominant Reflection

The interface returns most of the disturbance rather than handing it off. Boundary response overwhelms admission.

### Dominant Scattering

The disturbance is dispersed across many local directions or micro-events. No strong coherent handoff or coherent return dominates.

### Dominant Trapping

The disturbance is retained, redirected, or repeatedly reseated near the interface or within the source whole rather than cleanly handed off or strongly reflected.

## Reading Rule

Low/medium/high here mean relative dominance in shaping the interface outcome, not settled quantitative values.

`I_comp` is treated as a derived summary term, not a primitive variable.

## Discriminator Table

| Outcome | `B_in` | `B_out` | `J_surf` | `Q_coh` | `D` | `I_comp` | Current interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Successful handoff | high | high | med/high | high | low/med | high | boundary release and admission are both viable and interface mediation is coherent |
| Partial handoff | med | med | high | med | med | med | some viable handoff exists, but boundary mismatch or burden prevents dominance |
| Dominant reflection | low/med | med/high | high | med/high or high `Q_coll` analogue | low/med | low | interface resists admission and returns the disturbance coherently or semi-coherently |
| Dominant scattering | low/med | low/med | low/med | low/med | high | low | interface cannot preserve a strong coherent pathway in either direction |
| Dominant trapping | low/med | low | med/high | med | med/high | low/med | disturbance is neither handed off nor cleanly returned, but locally retained or repeatedly reseated |

## Outcome-by-Outcome Analysis

## 1. Successful Handoff

### Best Current Profile

- `B_in`: high
- `B_out`: high
- `J_surf`: medium/high
- `Q_coh`: high
- `D`: low/medium
- `I_comp`: high

### Interpretation

This is the cleanest interface event.

It requires:

- the source whole to release propagation well
- the receiving whole to admit it well
- the interface layer to mediate rather than scramble
- enough coherence continuity that the handoff remains one event rather than a collapse into several competing ones

### Main Discriminator

Successful handoff is the only outcome in which both `B_in` and `B_out` must be strong at the same time.

### Modelling Implication

`I_comp` appears strongest here because it captures the joint viability of the two-sided event better than any single primitive variable.

## 2. Partial Handoff

### Best Current Profile

- `B_in`: medium
- `B_out`: medium
- `J_surf`: high
- `Q_coh`: medium
- `D`: medium
- `I_comp`: medium

### Interpretation

This is likely the most common non-ideal interface outcome.

The key feature is not outright failure, but competition:

- some release works
- some admission works
- some boundary degradation remains
- some coherence is preserved, but not enough to dominate

### Main Discriminator

High `J_surf` with only medium `B_in` and `B_out` suggests that the interface is working hard but not well enough.

### Modelling Implication

This is the best case for treating `I_comp` as a graded rather than binary descriptor.

## 3. Dominant Reflection

### Best Current Profile

- `B_in`: low/medium
- `B_out`: medium/high
- `J_surf`: high
- `Q_coh`: medium/high
- `D`: low/medium
- `I_comp`: low

### Interpretation

Reflection occurs when the interface is capable of coherent response, but not of viable admission.

This is why reflection is not just “failed transmission.” It is an active interface event:

- the boundary is responsive
- the source side may release strongly
- but the receiving side does not admit the event into a stable onward pathway

### Main Discriminator

The key separation from successful handoff is:

- high `B_out`
- low/medium `B_in`

with interface coherence still intact enough to return a structured response rather than randomise it.

### Modelling Implication

This outcome supports the existing reflection-side cluster from the optical programme:

- strong boundary response
- strong surface mediation
- preserved coherence on the return side

## 4. Dominant Scattering

### Best Current Profile

- `B_in`: low/medium
- `B_out`: low/medium
- `J_surf`: low/medium
- `Q_coh`: low/medium
- `D`: high
- `I_comp`: low

### Interpretation

Scattering is the clearest incoherence-heavy outcome.

No interface function dominates:

- admission is weak
- release is weak
- interface coupling is weak or noisy
- coherence continuity is poor
- defect burden is high

### Main Discriminator

High `D` with weak `Q_coh` separates scattering from both reflection and trapping.

### Modelling Implication

This strengthens the earlier suspicion that `D` may need a later split between:

- defect burden
- defect tolerance

because some wholes survive high background defect sensitivity while others collapse into scattering rapidly.

## 5. Dominant Trapping

### Best Current Profile

- `B_in`: low/medium
- `B_out`: low
- `J_surf`: medium/high
- `Q_coh`: medium
- `D`: medium/high
- `I_comp`: low/medium

### Interpretation

Trapping is the most subtle outcome in the current table.

It differs from reflection because the disturbance is not cleanly returned.
It differs from scattering because the event still retains enough local organisation to remain bounded or repeatedly re-seated near the interface.

This suggests:

- non-trivial surface mediation
- insufficient release
- insufficient onward admission
- enough local structure to prevent immediate randomisation

### Main Discriminator

The strongest signal is:

- low `B_out`
- non-low `J_surf`

That means the interface is still active, but not effectively handoff-capable.

### Modelling Implication

Trapping may become especially important for:

- surface roughness cases
- layered media
- oxidised or contaminated transmissive boundaries
- internally mismatched nested wholes

## Strongest Current Discriminators

## 1. `B_in` vs `B_out`

The most useful current distinction is still:

- admission capability
- release capability

This is now much harder to collapse into a single boundary variable.

## 2. `J_surf`

`J_surf` separates:

- mere failure
- active but non-ideal mediation

It is especially important in:

- partial handoff
- reflection
- trapping

## 3. `Q_coh`

`Q_coh` separates:

- structured return or transfer
- incoherent dispersion

It is one of the clearest dividers between:

- reflection
- scattering

## 4. `D`

`D` is the strongest driver toward scattering, but not every high-`D` case scatters. Where local structure remains strong enough, `D` may contribute instead to trapping or degraded partial handoff.

## 5. `I_comp`

`I_comp` is proving useful as a summary discriminator for:

- successful handoff
- partial handoff

It is less useful as a direct predictor of reflection or scattering, where the primitive variables already tell most of the story.

## Current Weak Points

## 1. Trapping Is Still Underdefined

The current model can describe trapping better than before, but it still lacks a strong geometry for:

- repeated local reseating
- shallow boundary retention
- oscillatory near-interface persistence

## 2. Reflection Still Borrows from the Earlier Optical Programme

That is not wrong, but it means the interface framework is still partly dependent on earlier reflection-side assumptions rather than fully re-deriving them here.

## 3. `I_comp` Needs Testing Against Real Interface Families

The derived term is useful, but still abstract. It needs to be tested against concrete interface pairings such as:

- air to glass
- glass to air
- crystal to air
- glass to crystal
- oxide film to metal

## Confidence

- discriminator usefulness confidence: `8/10`
- confidence that the five outcomes are genuinely distinct in the current model: `7/10`
- confidence that `I_comp` is worth keeping as a derived term: `8/10`
- confidence that trapping is modelled sharply enough yet: `5/10`

## Next Move

The best next artifact is:

- `ams-real-interface-pairings-v1.md`

That should map the discriminator logic onto concrete pairings such as:

- air -> glass
- glass -> air
- air -> crystal
- crystal -> air
- air -> polished metal
- air -> oxidised metal
- glass -> metal

That is the right bridge from current abstract interface logic into more recognisable material cases.
