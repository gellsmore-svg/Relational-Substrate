# AMS Refined Interface Pairings v2

## Purpose

This document rewrites the main real interface pairings using the refined interface variable set established in:

- `ams-interface-variable-refinement-v1.md`

The main change is:

- `J_surf` is replaced by `J_bound` and `J_trans`

The aim is to test whether the real pairings now become:

- sharper
- more stable
- less dependent on hidden catch-all language

This is also the point where the programme needs to decide whether:

- the interface model is stable enough for a while

or whether:

- another variable split is already required

## Active Interface Variable Set

Primitive variables:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Derived term:

- `I_comp`

Supporting context variables:

- `R`
- `S`
- `J_dist`
- `B_ref`
- `B_coh`

## Pairing 1: Air -> Glass

### Refined Profile

- `B_in`: high
- `B_out`: low
- `J_bound`: medium
- `J_trans`: medium/high
- `Q_coh`: medium/high
- `D`: medium/high
- `I_comp`: high

### Outcome

- successful handoff
- minor competing reflection possible

### What Is Sharper Now

The pairing is cleaner because it no longer needs to say “surface mediation” in a vague way.

The model can now say:

- first contact is not the dominant problem
- through-layer continuity into distributed permissive pathways is the dominant enabling feature

That is a real gain.

### Stability Judgment

Stable anchor case.

## Pairing 2: Glass -> Air

### Refined Profile

- `B_in`: low
- `B_out`: medium/high
- `J_bound`: medium
- `J_trans`: medium
- `Q_coh`: medium
- `D`: medium/high
- `I_comp`: medium/high

### Outcome

- successful handoff or partial handoff

### What Is Sharper Now

The split helps somewhat, but not dramatically.

The pairing is still weaker than the entry-side cases because:

- release geometry remains less mature than admission geometry
- `J_trans` is useful, but the model still lacks a strong picture of the final release path

### Stability Judgment

Improved, but not yet fully stable.

## Pairing 3: Air -> Crystal

### Refined Profile

- `B_in`: medium/high
- `B_out`: low
- `J_bound`: medium
- `J_trans`: high
- `Q_coh`: high
- `D`: low
- `I_comp`: medium/high

### Outcome

- selective successful handoff

### What Is Sharper Now

The pairing now makes better sense as an ordered-entry case.

The model can distinguish:

- the initial boundary event
- the deeper transition into patterned admissibility

That means high `Q_coh` is still important, but it no longer has to do all the work by itself.

### Stability Judgment

Strong and reasonably stable.

## Pairing 4: Crystal -> Air

### Refined Profile

- `B_in`: low
- `B_out`: high
- `J_bound`: medium/high
- `J_trans`: medium
- `Q_coh`: high
- `D`: low
- `I_comp`: medium/high

### Outcome

- successful handoff or partial handoff

### What Is Sharper Now

Some improvement is visible.

The split helps distinguish:

- strong release potential from the crystal side
- the more fragile question of whether that release can remain coherent through the interface layer

But this case still depends on underdeveloped release geometry.

### Stability Judgment

Better than before, but still not anchor-grade.

## Pairing 5: Air -> Polished Metal

### Refined Profile

- `B_in`: low/medium
- `B_out`: medium/high
- `J_bound`: high
- `J_trans`: low/medium
- `Q_coh`: high
- `D`: low/medium
- `I_comp`: low

### Outcome

- dominant reflection

### What Is Sharper Now

This is one of the clearest victories of the refinement.

The pairing now shows a very clean reflection signature:

- strong boundary-face event
- weak onward transition continuity
- preserved coherence sufficient for structured return

### Stability Judgment

Very strong anchor case.

## Pairing 6: Air -> Oxidised Metal

### Refined Profile

- `B_in`: low/medium
- `B_out`: medium
- `J_bound`: medium
- `J_trans`: low
- `Q_coh`: low/medium
- `D`: high
- `I_comp`: low

### Outcome

- degraded reflection
- dominant scattering
- or partial handoff depending on oxide state

### What Is Sharper Now

This pairing benefits strongly from the split.

It now becomes clearer that oxidation can degrade:

- the initial boundary-face response somewhat
- the through-layer continuity more severely

That separation was harder to state before.

### Stability Judgment

Strong anchor case for surface-layer degradation.

## Pairing 7: Glass -> Metal

### Refined Profile

- `B_in`: low/medium
- `B_out`: medium/high
- `J_bound`: high
- `J_trans`: low/medium
- `Q_coh`: medium/high
- `D`: low/medium for polished surface, higher if degraded
- `I_comp`: low/medium

### Outcome

- dominant reflection
- or partial handoff with strong return

### What Is Sharper Now

This mixed case becomes clearer because the receiving whole can now be described more sharply:

- it does not merely “respond strongly”
- it responds strongly at the boundary face without supporting strong through-interface continuity into a transmissive grammar

### Stability Judgment

Improved and useful, but still partly derivative of the stronger anchor cases.

## Pairing 8: Glass -> Crystal

### Refined Profile

- `B_in`: medium
- `B_out`: medium/high
- `J_bound`: medium/high
- `J_trans`: high
- `Q_coh`: medium/high
- `D`: medium
- `I_comp`: medium/high

### Outcome

- selective successful handoff
- or partial handoff
- or trapping if transition-layer mediation stalls

### What Is Sharper Now

This is the single biggest beneficiary of the refinement.

The pairing now has a clear internal logic:

- the interface event can form
- the real burden lies in sustaining mediated continuity through the transition layer
- narrowing into crystal-style admissibility is the decisive step

That means the model can now distinguish:

- workable first contact
- incomplete through-layer mediation
- final admission failure

without forcing all of that into one variable.

### Stability Judgment

Sharpened strongly, but still a frontier case rather than a settled anchor.

## Which Pairings Sharpened Most

## Strongest Sharpening

### 1. Air -> Polished Metal

Why:

- the reflection signature is now much cleaner
- `J_bound` and `J_trans` separate the boundary event from onward handoff failure

### 2. Glass -> Crystal

Why:

- the compatibility problem is now more explicit
- `I_comp` is less overloaded
- trapping becomes more intelligible

### 3. Air -> Oxidised Metal

Why:

- surface-layer degradation can now be described asymmetrically
- the model no longer needs to blur all oxide effects into one weakened surface variable

## Moderate Sharpening

### 4. Air -> Glass

Sharper, but it was already a strong case.

### 5. Air -> Crystal

Sharper in a useful way, but less dramatically than the high-pressure pairings.

## Weakest Sharpening

### 6. Glass -> Air
### 7. Crystal -> Air

These improved, but less than the others.

The reason appears consistent:

- exit-side geometry still lags entry-side geometry

## Has the Model Stabilised?

Current answer:

- mostly yes, for the present stage

The current variable set now appears good enough to support another round of modelling without immediate further splitting.

That means the active interface variable set can remain:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`
- derived `I_comp`

## Is Another Split Already Needed?

Current answer:

- not yet

The main candidate for future refinement would be:

- splitting `D`

into something like:

- defect burden
- defect tolerance

But that does not yet look mandatory at the interface level.

The current split has bought enough clarity to proceed further before adding more variables.

## Strongest Current Interface Anchors

- air -> glass
- air -> polished metal
- air -> oxidised metal

These now form a reasonably stable anchor triangle:

- clean handoff
- clean reflection
- degraded boundary response

## Strongest Current Frontier

- glass -> crystal

This remains the best place to test:

- transition-layer geometry
- `I_comp`
- trapping
- compatibility between transmissive grammars

## Confidence

- confidence that the refined interface set is stable enough for now: `8/10`
- confidence that no immediate further split is required: `7/10`
- confidence that exit-side cases still lag entry-side cases: `8/10`
- confidence that `glass -> crystal` remains the best frontier case: `9/10`

## Recommendation

Do not split more variables yet.

Use the refined set for the next modelling phase.

## Next Move

The strongest next artifact is:

- `ams-exit-geometry-study-v1.md`

Reason:

- the model has stabilised enough on entry and compatibility
- exit-side cases are now the clearest remaining weak region
- the current refined variables are good enough to pressure release geometry without further immediate refinement
