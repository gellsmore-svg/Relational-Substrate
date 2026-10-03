# AMS Real Interface Pairings v1

## Purpose

This document applies the current interface-transition model to concrete material pairings.

The aim is to test whether the abstract variables and outcomes developed in:

- `ams-entry-exit-interface-cases-v1.md`
- `ams-entry-exit-parameter-sweep-v1.md`
- `ams-interface-transition-discriminator-table-v1.md`

still hold when attached to recognisable optical cases.

This is the first bridge from abstract interface logic into material-specific modelling.

## Variables in Use

Primitive variables:

- `B_in`
- `B_out`
- `J_surf`
- `Q_coh`
- `D`

Derived term:

- `I_comp`

Supporting optical context:

- `B_ref`
- `B_coh`
- `J_dist`
- `R`
- `S`

## Pairing 1: Air -> Glass

### Expected Dominant Outcome

Successful handoff, often with some minor competing reflection.

### Best Current Profile

- `B_in`: high
- `B_out`: low
- `J_surf`: medium
- `Q_coh`: medium/high
- `D`: medium/high
- `I_comp`: high

### Interpretation

This is the clearest real case supporting the current glass-transmission model.

The receiving whole is disordered at fine scale but still supports distributed permissive transmissive order. That means:

- the surface can admit propagation reasonably well
- the bulk can reseat propagation into many admissible onward pathways
- coherence is preserved enough for transmission, even though the underlying order is not crystal-like

Minor reflection is expected because:

- admission is not perfect
- the interface still has a surface event

But the dominant story remains handoff into a real transmissive whole.

### Main Pressure Point

This case is one of the strongest arguments for keeping `D` from being treated as purely destructive, because the glass whole can remain transmissive even with comparatively high defect sensitivity.

## Pairing 2: Glass -> Air

### Expected Dominant Outcome

Successful handoff or partial handoff, depending heavily on the final surface layer.

### Best Current Profile

- `B_in`: low
- `B_out`: medium/high
- `J_surf`: medium
- `Q_coh`: medium
- `D`: medium/high
- `I_comp`: medium/high

### Interpretation

This is the clearest real case for testing `B_out`.

The glass whole has already carried propagation internally. The question is whether the surface can release that propagation coherently into the outside medium.

The current model suggests:

- clean exit is possible
- but exit quality is more fragile than bulk transmission quality

That fragility comes from the last interface layer, where distributed permissiveness no longer guarantees clean release.

### Main Pressure Point

This case puts direct pressure on the distinction between:

- transmissive bulk identity
- surface-release quality

## Pairing 3: Air -> Crystal

### Expected Dominant Outcome

Selective successful handoff, with entry quality strongly dependent on coherence compatibility.

### Best Current Profile

- `B_in`: medium/high
- `B_out`: low
- `J_surf`: medium
- `Q_coh`: high
- `D`: low
- `I_comp`: medium/high

### Interpretation

This is the clearest real case for crystal-style ordered entry.

The crystal whole is not simply “more transmissive” than glass in a general sense. It is more pattern-dependent.

So the current model suggests:

- entry is more selective
- admitted propagation can remain more strongly ordered once inside

This case therefore supports the idea that crystals and glasses both transmit, but do so through different organisational logics.

### Main Pressure Point

This case is one of the strongest tests of whether `Q_coh` is properly defined, because coherence compatibility seems more important here than in glass entry.

## Pairing 4: Crystal -> Air

### Expected Dominant Outcome

Successful handoff or partial handoff, depending on whether ordered propagation can be released without destructive mismatch.

### Best Current Profile

- `B_in`: low
- `B_out`: high
- `J_surf`: medium/high
- `Q_coh`: high
- `D`: low
- `I_comp`: medium/high

### Interpretation

This case differs from glass -> air because the internal propagation is more strongly patterned.

The current model suggests:

- release can be very coherent
- but only if the boundary can relax that internal order into an admissible outgoing event

So this is a stronger `B_out` and `Q_coh` case than glass exit.

### Main Pressure Point

This pairing puts direct pressure on whether the model has enough geometry for boundary relaxation. Right now that part is still underdeveloped.

## Pairing 5: Air -> Polished Metal

### Expected Dominant Outcome

Dominant reflection.

### Best Current Profile

- `B_in`: low/medium
- `B_out`: medium/high
- `J_surf`: high
- `Q_coh`: high
- `D`: low/medium
- `I_comp`: low

### Interpretation

This is the clearest real pairing for the reflection side of the model.

The current optical programme already suggests that polished metal behaves as:

- highly boundary-sensitive
- strongly surface-coupled
- capable of collective response

So the dominant outcome is not poor structure, but highly structured non-admission.

That is important. Reflection here is not merely failure. It is an active surface event:

- release/return remains strong
- admission is weak
- boundary coherence remains high enough to preserve structured reflection

### Main Pressure Point

This case still depends partly on the earlier reflection-side model. It is strong, but not yet fully re-derived from the interface side alone.

## Pairing 6: Air -> Oxidised Metal

### Expected Dominant Outcome

Partial handoff, dominant scattering, or degraded reflection, depending on oxide thickness and surface continuity.

### Best Current Profile

- `B_in`: low/medium
- `B_out`: medium
- `J_surf`: medium
- `Q_coh`: low/medium
- `D`: high
- `I_comp`: low

### Interpretation

This is the clearest real case showing that bulk metallic identity does not guarantee polished-metal-style reflection.

The oxide layer acts as:

- altered boundary geometry
- elevated defect burden
- degraded surface coherence

So the current model predicts:

- lower `B_coh`
- lower effective `Q_coh`
- weaker `J_surf`
- more scattering or degraded reflection

### Main Pressure Point

This case strongly supports the distinction between:

- bulk whole identity
- actual boundary-layer behaviour

## Pairing 7: Glass -> Metal

### Expected Dominant Outcome

Dominant reflection or partial handoff with strong return, depending on surface quality.

### Best Current Profile

- `B_in`: low/medium
- `B_out`: medium/high
- `J_surf`: high
- `Q_coh`: medium/high
- `D`: low/medium for polished metal, higher if degraded
- `I_comp`: low/medium

### Interpretation

This is a useful mixed case because the source whole is transmissive and the receiving whole is strongly reflective at the interface.

The current model suggests:

- the glass can carry propagation to the interface
- the metal boundary mediates a strong non-admitting response
- return dominates over onward handoff

This makes the pairing useful for separating:

- bulk transmission quality in the source whole
- interface behaviour at the receiving whole

### Main Pressure Point

This case may help later in distinguishing whether metal reflection is mostly a receiving-boundary event or a joint interface event.

## Pairing 8: Glass -> Crystal

### Expected Dominant Outcome

Partial handoff or selective successful handoff.

### Best Current Profile

- `B_in`: medium
- `B_out`: medium/high
- `J_surf`: high
- `Q_coh`: medium/high
- `D`: medium
- `I_comp`: medium

### Interpretation

This is a strong test of `I_comp`.

Both wholes are transmissive, but they transmit through different organisational logics:

- glass through distributed permissive order
- crystal through structured nested order

So the handoff problem is not between transmission and reflection, but between two distinct transmissive grammars.

### Main Pressure Point

This pairing is one of the strongest cases for keeping `I_comp`, because neither side is simply “bad at transmission,” yet the interface may still be difficult.

## Cross-Pairing Findings

## 1. Air -> Glass Is the Strongest Handoff Benchmark

At the current stage, this is the cleanest real case supporting:

- high `B_in`
- viable `I_comp`
- distributed transmissive order

## 2. Air -> Polished Metal Is the Strongest Reflection Benchmark

This remains the cleanest real case for:

- weak admission
- strong structured return
- high `J_surf`
- high boundary coherence

## 3. Glass -> Crystal Is the Strongest Compatibility Benchmark

This is currently the best real case for testing whether `I_comp` adds genuine value rather than just summarising already obvious variables.

## 4. Oxidised Metal Is the Strongest Boundary-Layer Degradation Benchmark

This is one of the best real pairings for testing:

- defect burden
- degraded surface coherence
- loss of polished-metal-style reflection without loss of all metallic identity

## 5. Exit Cases Remain Less Secure Than Entry Cases

The current pairings reinforce an earlier result:

- `B_in` is currently easier to model than `B_out`

That does not mean `B_out` is weak as a concept. It means release geometry still needs more work.

## Current Strongest and Weakest Pairings

### Strongest Current Pairings

- air -> glass
- air -> polished metal
- air -> crystal
- air -> oxidised metal

These are strongest because the material contrast is sharper and the expected outcome classes separate more cleanly.

### Weakest Current Pairings

- glass -> air
- crystal -> air
- glass -> crystal

These are weakest because:

- release geometry is less developed than entry geometry
- cross-transmissive compatibility is still only partially captured

## Provisional Confidence

- usefulness of real-pairing bridge: `9/10`
- confidence in air -> glass model: `8/10`
- confidence in air -> polished metal model: `8/10`
- confidence in oxidised metal degradation model: `8/10`
- confidence in exit-side cases: `6/10`
- confidence in glass -> crystal compatibility model: `7/10`

## Next Move

The best next artifact is:

- `ams-interface-pairing-scoreboard-v1.md`

That should rank the current pairings by:

- explanatory strength
- variable clarity
- geometry maturity
- immediate usefulness for further modelling

That will help decide whether to go deeper first into:

- exit geometry
- oxide / surface-layer modelling
- transmissive-to-transmissive compatibility

instead of trying to advance all three fronts at once.
