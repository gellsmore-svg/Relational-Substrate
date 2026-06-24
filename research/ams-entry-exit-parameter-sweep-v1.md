# AMS Entry/Exit Parameter Sweep v1

## Purpose

This document performs the first structured parameter sweep across the entry/exit interface cases defined in:

- `ams-entry-exit-interface-cases-v1.md`

The immediate goals are:

- test whether `B_in` and `B_out` remain meaningfully distinct
- pressure `J_surf`, `Q_coh`, and `D` as interface variables rather than only bulk variables
- assess whether a provisional interface compatibility term, `I_comp`, is genuinely needed

This is not a numerical model. It is a structured low/medium/high sweep designed to expose whether the current variable set can discriminate interface behaviours without collapsing into verbal restatement.

## Variables in Scope

Primary sweep variables:

- `B_in`
- `B_out`
- `J_surf`
- `Q_coh`
- `D`

Supporting context variables:

- `R`
- `S`
- `J_dist`
- `B_ref`

## Reading Rule

Low/medium/high does not mean “small physical amount” in any settled mathematical sense. It means:

- low: not playing a dominant positive role in the case
- medium: materially present, but not the clearest driver
- high: a main discriminator or enabling condition

For `D`, high means strong defect burden or strong defect sensitivity.

## Sweep Table

| Case | `B_in` | `B_out` | `J_surf` | `Q_coh` | `D` | Provisional outcome |
|---|---:|---:|---:|---:|---:|---|
| Entry into regular nested transmissive order | high | low/med | med | high | low | selective admission, strong coherence if admitted |
| Entry into distributed permissive transmissive order | med/high | low/med | med | med/high | med/high | broader admission, weaker patterned guidance |
| Exit from regular nested transmissive order | low/med | high | med/high | high | low | coherent release if boundary relaxation is adequate |
| Exit from distributed permissive transmissive order | low/med | med/high | med | med | med/high | possible release, but surface disorder can scramble final handoff |
| Mismatched transmissive interface | med | med | high | med/high | med | mixed outcome: partial handoff, partial loss, strong context dependence |
| Entry under surface disorder or impurity | low/med | low | low/med | low/med | high | degraded admission, elevated scattering or incoherent loss |

## Case Analysis

## 1. Entry into Regular Nested Transmissive Order

### Sweep Reading

Best current profile:

- `B_in`: high
- `B_out`: low/medium
- `J_surf`: medium
- `Q_coh`: high
- `D`: low

### Interpretation

This remains a selective-admission case. High `B_in` does not mean easy entry in a casual sense. It means that when the incoming disturbance matches the receiving order closely enough, the boundary can admit it in a way that preserves coherence.

So this is:

- not permissive in a broad sense
- but strongly coherence-favouring when admission succeeds

### Main Discriminator

`Q_coh` is doing unusually heavy work here. Entry into ordered transmissive wholes appears to depend strongly on coherence compatibility, not only on surface access.

### Pressure on `I_comp`

This case supports an interface-compatibility idea, because `B_in` alone does not explain why some incoming disturbances are admitted coherently while others are turned away.

## 2. Entry into Distributed Permissive Transmissive Order

### Sweep Reading

Best current profile:

- `B_in`: medium/high
- `B_out`: low/medium
- `J_surf`: medium
- `Q_coh`: medium/high
- `D`: medium/high

### Interpretation

This case differs from crystal-like entry. The receiving whole appears less pattern-selective and more dependent on local reseating across many neighbouring admissible pathways.

That implies:

- better broad admission than a highly ordered whole
- less structured coherence once inside

### Main Discriminator

High or medium/high `D` is not automatically destructive here. In glass-like wholes, defect sensitivity appears entangled with the very distributed permissiveness that makes transmission possible.

### Pressure on `I_comp`

This case weakens the argument for treating compatibility as purely coherence-pattern matching. Admission here may be more about pathway accommodation than precise structural matching.

## 3. Exit from Regular Nested Transmissive Order

### Sweep Reading

Best current profile:

- `B_in`: low/medium
- `B_out`: high
- `J_surf`: medium/high
- `Q_coh`: high
- `D`: low

### Interpretation

This is the clearest exit-driven case. The whole can carry propagation well, but the boundary must convert that propagation into a releasable form without destroying coherence.

That suggests a specific relation:

- high `Q_coh` is still needed
- but `J_surf` becomes more important than it was in bulk transmission

### Main Discriminator

`B_out` is now clearly doing different work from `B_in`. Entry asks whether the whole can admit a disturbance. Exit asks whether the boundary can release a previously coherent disturbance into another regime.

### Pressure on `I_comp`

This case again argues that transition variables are not reducible to a single bulk property. Some additional interface-level term still looks useful.

## 4. Exit from Distributed Permissive Transmissive Order

### Sweep Reading

Best current profile:

- `B_in`: low/medium
- `B_out`: medium/high
- `J_surf`: medium
- `Q_coh`: medium
- `D`: medium/high

### Interpretation

This is a weaker release case than crystal exit. The whole may transmit internally, but the lack of strongly patterned boundary release geometry makes clean exit fragile.

This suggests:

- bulk permissiveness does not guarantee clean emission
- surface condition may dominate late-stage outcome

### Main Discriminator

`D` remains unusually important here. It may not merely degrade the interface; it may actively shape whether the final event is:

- clean exit
- diffuse scattering
- partial trapping

### Pressure on `I_comp`

This case supports a compatibility term, but in a weaker form than crystal entry/exit. The main issue may be interface quality rather than structural mismatch alone.

## 5. Mismatched Transmissive Interface

### Sweep Reading

Best current profile:

- `B_in`: medium
- `B_out`: medium
- `J_surf`: high
- `Q_coh`: medium/high
- `D`: medium

### Interpretation

This is the hardest diagnostic case because no single variable dominates cleanly. The interface must:

- release from one regime
- admit into another
- preserve enough coherence to avoid collapse into pure loss

The result is typically mixed.

### Main Discriminator

`J_surf` appears stronger here than in any simpler entry-only or exit-only case. That suggests the interface layer itself may do more active mediation than the current model has fully described.

### Pressure on `I_comp`

This is the strongest case for `I_comp`. The current variables describe important parts of the event, but they do not yet fully capture whether two transmissive orders can actually hand off propagation to one another.

## 6. Entry under Surface Disorder or Impurity

### Sweep Reading

Best current profile:

- `B_in`: low/medium
- `B_out`: low
- `J_surf`: low/medium
- `Q_coh`: low/medium
- `D`: high

### Interpretation

This is the clearest degradation case. A nominally transmissive bulk whole may admit poorly if the boundary layer no longer represents the bulk whole faithfully.

This is an important result because it separates:

- transmissive identity of the whole
- transmissive quality of the boundary

### Main Discriminator

High `D` is dominant here. It lowers admission quality and often prevents the interface from forming a viable handoff event in the first place.

### Pressure on `I_comp`

This case does not by itself require `I_comp`. A sufficiently strong defect burden can already explain poor admission without adding another variable.

## Cross-Case Findings

## 1. `B_in` and `B_out` Survive the Sweep

The sweep supports keeping them separate.

They are not redundant because:

- `B_in` governs admission into a whole
- `B_out` governs release from a whole

Some cases are high in one and only medium in the other.

## 2. `J_surf` Is More Important Than Previously Treated

The interface layer is not passive. `J_surf` appears especially important in:

- mismatched transmissive interfaces
- crystal exit
- degraded surface cases

This suggests that boundary mediation is partly a coupling problem, not only a coherence problem.

## 3. `Q_coh` Matters Most Where Order Is Strong

Ordered wholes rely more on coherence compatibility.

Disordered permissive wholes rely more on:

- pathway accommodation
- slip
- defect-tolerant reseating

This supports the broader distinction already emerging between crystal-like and glass-like transmission.

## 4. `D` Does Two Different Jobs

`D` is not one thing.

It appears to function as:

- destructive burden in degraded interface cases
- tolerated structural background in some distributed transmissive wholes

This suggests `D` may later need its own sub-split, perhaps between:

- defect burden
- defect tolerance

## 5. `I_comp` Is Probably Needed

The sweep does not prove that `I_comp` must become a formal variable, but it does make a good case that something like it is needed.

Reason:

The current variables explain:

- admission quality
- release quality
- surface coupling
- coherence compatibility
- defect burden

But they still do not fully describe the joint relation between two adjacent transmissive orders.

So the present working judgment is:

- `I_comp` is justified as a provisional derived term
- not yet justified as a primitive variable

## Provisional Derived Term

### `I_comp`

Working meaning:

- the degree to which two adjacent whole-structures can support a viable handoff of propagation across their interface without dominant incoherence, loss, or reflection

Current likely dependence:

- `B_out`
- `B_in`
- `J_surf`
- `Q_coh`
- secondarily `D`

This is likely not an independent primitive. It is more plausibly a higher-order descriptor derived from the joint behaviour of the other variables.

## Confidence

- sweep usefulness confidence: `8/10`
- confidence that `B_in` and `B_out` are genuinely distinct: `8/10`
- confidence that `I_comp` is a useful derived term: `7/10`
- confidence that the current variable set is fully sufficient without further splitting: `5/10`

## Next Move

The next most useful artifact is:

- `ams-interface-transition-discriminator-table-v1.md`

That should force a direct contrast between:

- successful handoff
- partial handoff
- dominant reflection
- dominant scattering
- dominant trapping

using the current interface variables and provisional `I_comp`.
