# AMS Interface Variable Refinement v1

## Purpose

This document applies the first explicit interface-variable refinement demanded by the current modelling programme.

The trigger for this refinement was:

- `ams-transition-layer-geometry-study-v1.md`

The main finding there was that `J_surf` had become overloaded. It was being used to cover:

- immediate boundary-face coupling
- through-interface transition-layer mediation
- local reseating capacity within the transition region

That is too much for one variable if the interface is now being treated as a real finite layer rather than a zero-thickness boundary.

## Refinement

Replace:

- `J_surf`

with:

- `J_bound`
- `J_trans`

## Working Definitions

### `J_bound`

Meaning:

- immediate coupling behaviour at the first boundary-contact zone

This covers:

- how strongly the interface responds at initial contact
- whether the first interaction is structured or weak
- whether a coherent boundary event forms at all

### `J_trans`

Meaning:

- coupling continuity within the transition layer after first contact

This covers:

- whether reseating can continue through the interface region
- whether narrowing or ordering can proceed
- whether the handoff process has enough mediated continuity to complete

## Variables Now in Use

Primitive variables:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Derived term:

- `I_comp`

Supporting bulk variables:

- `R`
- `S`
- `J_dist`

## Why This Refinement Matters

Without the split, the model could say:

- “surface mediation is high”

but could not distinguish between:

- strong first contact but poor through-layer continuity
- modest first contact but strong mediated continuation
- strong initial response followed by trapping or collapse

That weakness mattered most in:

- `glass -> crystal`
- trapping scenarios
- oxidised or degraded interfaces
- partial handoff cases

## Translation Table

| Old variable use | New likely reading |
|---|---|
| high `J_surf` in clean reflection case | high `J_bound`, low/medium `J_trans` |
| high `J_surf` in successful cross-handoff | medium/high `J_bound`, high `J_trans` |
| high `J_surf` in trapping case | medium/high `J_bound`, medium `J_trans` or stalled `J_trans` |
| weak `J_surf` in degraded scattering case | low/medium `J_bound`, low `J_trans` |

## Rerun of Key Pairings

## 1. Air -> Glass

### Previous Picture

- successful handoff
- medium `J_surf`

### Refined Picture

- `B_in`: high
- `B_out`: low
- `J_bound`: medium
- `J_trans`: medium/high
- `Q_coh`: medium/high
- `D`: medium/high
- `I_comp`: high

### What Improves

This split makes glass entry clearer.

The first contact does not need unusually strong boundary-face coupling. What matters more is that the receiving whole can continue reseating the incoming disturbance into distributed admissible pathways.

So:

- `J_bound` is only moderate
- `J_trans` does more of the real work

### Result

The glass-entry model becomes cleaner.

## 2. Air -> Polished Metal

### Previous Picture

- dominant reflection
- high `J_surf`

### Refined Picture

- `B_in`: low/medium
- `B_out`: medium/high
- `J_bound`: high
- `J_trans`: low/medium
- `Q_coh`: high
- `D`: low/medium
- `I_comp`: low

### What Improves

This is one of the clearest wins from the split.

Polished metal reflection does not appear to require strong through-layer mediation into a new transmissive grammar. It requires:

- strong boundary-face response
- coherent structured return
- weak admission into onward transmissive handoff

So:

- `J_bound` is high
- `J_trans` does not need to be high

### Result

Reflection becomes more sharply distinct from successful handoff.

## 3. Air -> Oxidised Metal

### Previous Picture

- degraded reflection or scattering
- medium `J_surf`

### Refined Picture

- `B_in`: low/medium
- `B_out`: medium
- `J_bound`: medium
- `J_trans`: low
- `Q_coh`: low/medium
- `D`: high
- `I_comp`: low

### What Improves

The split clarifies how oxide degradation works.

The interface may still respond at first contact, but the transition region no longer carries a strong, coherent continuation. So:

- the first event survives partially
- the deeper continuity of that event degrades

### Result

This pairing now distinguishes:

- degraded boundary-face response
- more severely degraded through-layer continuity

better than before.

## 4. Glass -> Crystal

### Previous Picture

- strongest `I_comp` case
- high `J_surf`

### Refined Picture

- `B_out`: medium/high
- `B_in`: medium
- `J_bound`: medium/high
- `J_trans`: high
- `Q_coh`: medium/high
- `D`: medium
- `I_comp`: medium/high

### What Improves

This is the most important rerun in the document.

The split shows why `glass -> crystal` is hard:

- first contact can be workable
- but the real burden lies in maintaining mediated continuity while narrowing distributed permissive propagation into patterned admissibility

That means:

- `J_bound` matters
- but `J_trans` matters more

### Result

The pairing becomes sharper, and `I_comp` is less overloaded because the model now has a way to say:

- “the interface event forms”
- but
- “the transition through the layer fails or succeeds to a different degree”

## 5. Trapping Cases

### Previous Picture

Trapping was distinguishable, but still blurred.

### Refined Picture

Two main trapping signatures now appear more clearly:

#### T1: Shallow Retention

- `J_bound`: medium/high
- `J_trans`: low
- `B_in`: low/medium
- `B_out`: low
- `Q_coh`: low/medium
- `D`: medium/high

Interpretation:

- the disturbance forms a local interface event
- but it does not continue through the layer

#### T2: Funnel Stall

- `J_bound`: medium/high
- `J_trans`: medium
- `B_in`: low/medium
- `B_out`: low/medium
- `Q_coh`: medium
- `D`: medium

Interpretation:

- the disturbance enters the transition layer
- narrowing begins
- final handoff fails
- local reseating persists

### Result

Trapping is now materially clearer than before.

## Cross-Rerun Findings

## 1. The Split Is Worth Keeping

This is the main conclusion.

The refinement is not cosmetic. It produces genuinely sharper distinctions:

- reflection now leans on high `J_bound` without needing high `J_trans`
- successful cross-transmissive handoff leans strongly on `J_trans`
- degraded interfaces now show asymmetric weakening
- trapping becomes more legible

## 2. `I_comp` Carries Less Hidden Load

Before the split, `I_comp` was partly compensating for the fact that `J_surf` mixed several jobs together.

After the split:

- `I_comp` still looks useful
- but less as a hidden catch-all
- more as a higher-order compatibility descriptor

That is an improvement.

## 3. Reflection and Cross-Transmissive Handoff Separate Better

Current best distinction:

- reflection:
  - high `J_bound`
  - low/medium `J_trans`
- cross-transmissive handoff:
  - medium/high `J_bound`
  - high `J_trans`

This is one of the strongest results yet in the optical interface programme.

## 4. Oxidation and Surface Degradation Become Easier to Model

The split helps distinguish:

- damaged first-contact response
- damaged through-layer continuity

That should make later oxide-film and rough-surface modelling cleaner.

## Revised Role of `I_comp`

Current best reading:

- `I_comp` is the degree of viable joint handoff across the interface, after primitive variables have already specified:
  - admission
  - release
  - boundary-face response
  - through-layer continuity
  - coherence
  - defect burden

So `I_comp` now looks more defensible precisely because it depends on a better primitive base.

## Confidence

- confidence that `J_surf` needed splitting: `9/10`
- confidence that `J_bound` / `J_trans` is a real improvement: `9/10`
- confidence that `glass -> crystal` is now sharper: `8/10`
- confidence that trapping is now more distinguishable: `8/10`
- confidence that `I_comp` is now less overloaded: `8/10`

## Recommendation

Keep the refinement.

The active interface variable set should now be:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`
- derived `I_comp`

## Next Move

The best next artifact is:

- `ams-refined-interface-pairings-v2.md`

That should rewrite the main real pairings using the refined variable set and then identify:

- which pairings sharpen the most
- whether exit-side cases improve materially
- whether another split is actually needed or whether the model can now stabilise for a while
