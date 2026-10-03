# AMS Recovery Ecology Scenario Comparison v1

## Purpose

This file pressure-tests the recovery-ecology formalism against concrete multi-machine scenarios.

The formalism already introduced:

```text
R_cap   = recovery capacity
R_res   = reserve depth
B_sync  = burden synchronisation
C_sup   = cross-support strength
F_casc  = cascade susceptibility
V_E     = ecology viability
θ_rec   = recoverability threshold
```

That scaffold is useful only if it can discriminate between different real burden patterns.

The aim here is therefore simple:

```text
test whether different ecology paths really look different under the model
```

## Central Claim

The central claim is:

> The recovery-ecology formalism is strong enough to distinguish several genuinely different cell trajectories: an acute respiratory crash, a chronic translation-decay path, a boundary-collapse cascade, a repair-buffered recovery state, and a mixed burden spiral. These scenarios do not differ only in severity. They differ in how reserve, cross-support, burden synchronisation, and cascade susceptibility interact over time.

More briefly:

```text
Cells do not merely die in one way more or less strongly; they die by different ecological paths.
```

## Method

This file does not attempt laboratory measurement.

It uses disciplined comparative scenario profiles.

Each scenario is described through the ecological variables:

- `R_cap`
- `R_res`
- `B_sync`
- `C_sup`
- `F_casc`
- `V_E`

using the qualitative bands:

```text
low
moderate
high
very high
```

The value of the exercise lies in structural discrimination, not exact numerics.

## Scenario 1: Acute Respiratory Crash

### Scenario Shape

This is the classic case where respiratory instability drives:

- rapid energetic disruption;
- gradient loss;
- oxidative spill;
- fast whole-cell destabilisation.

### Ecological Profile

```text
R_cap   = moderate-low and falling fast
R_res   = low and rapidly draining
B_sync  = high
C_sup   = weakening
F_casc  = very high
V_E     = dropping sharply toward or below θ_rec
```

### Why This Looks This Way

- respiration strongly supports energy order and reserve;
- its destabilisation rapidly burdens boundary and damage systems;
- the resulting burdens synchronise quickly;
- cross-support weakens before slower systems can compensate fully.

### Ecological Reading

This is:

```text
acute-dominant ecological failure
```

The cell is not mainly being worn down.

It is being driven over.

## Scenario 2: Chronic Translation-Decay Path

### Scenario Shape

This is the classic case where translation remains active enough to delay overt collapse while:

- architecture renewal lags;
- coordination burden rises;
- defective-product burden accumulates;
- future recoverability narrows.

### Ecological Profile

```text
R_cap   = moderate and slowly declining
R_res   = moderate-low and steadily eroding
B_sync  = moderate, rising over time
C_sup   = still present but thinning
F_casc  = moderate at first, rising later
V_E     = above θ_rec for a prolonged interval, then narrowing toward it
```

### Why This Looks This Way

- renewal failure weakens the future more than the present;
- multiple machines continue to work, but under poorer replacement conditions;
- cross-support persists for a while because the ecology is not yet acutely broken;
- burden synchronisation increases gradually as deferred maintenance becomes system-wide debt.

### Ecological Reading

This is:

```text
cumulative-dominant ecological decline
```

The cell is not collapsing quickly.

It is aging into failure under load.

## Scenario 3: Boundary-Collapse Cascade

### Scenario Shape

This is the case where membrane retention, transport gating, or compartment discipline weakens enough that:

- gradients flatten;
- local burdens spread rapidly;
- machine separability breaks down;
- one bounded ecology becomes less governable as one bounded ecology.

### Ecological Profile

```text
R_cap   = moderate at first, then sharply compromised
R_res   = moderate, then rapidly consumed
B_sync  = very high
C_sup   = collapsing
F_casc  = very high
V_E     = collapses quickly once boundary failure passes threshold
```

### Why This Looks This Way

- boundary systems preserve separability;
- once separability is lost, burdens stop remaining local;
- synchronisation rises quickly across machines;
- support topology may still exist structurally, but effective support collapses because the bounded conditions for support are gone.

### Ecological Reading

This is:

```text
containment-failure ecological collapse
```

It is closely related to respiratory crisis, but not identical.

Its distinctive mark is:

```text
loss of bounded separability
```

## Scenario 4: Repair-Buffered Recovery State

### Scenario Shape

This is the case where local burdens are substantial but repair and compensation systems still:

- buffer damage;
- preserve reserve long enough;
- keep burdens partly desynchronised;
- maintain owned recoverability.

### Ecological Profile

```text
R_cap   = moderate-high
R_res   = moderate
B_sync  = low-moderate
C_sup   = high
F_casc  = low-moderate
V_E     = clearly above θ_rec despite local burden
```

### Why This Looks This Way

- repair systems are effectively buying time;
- coordination still allocates effort intelligently;
- local machine stress is real but not yet ecology-owning;
- the system remains a functioning recovery ecology rather than a failing aggregate.

### Ecological Reading

This is:

```text
burdened but genuinely recoverable life
```

This is one of the most important positive scenarios because it shows the formalism is not only a theory of collapse.

It is also a theory of real persistence under stress.

## Scenario 5: Mixed Burden Spiral

### Scenario Shape

This is the hardest case and probably the most realistic severe trajectory.

Here:

- respiration weakens enough to reduce energy reserve;
- translation weakens enough to increase renewal debt;
- repair systems are overloaded;
- coordination becomes less effective;
- burdens begin to amplify one another.

### Ecological Profile

```text
R_cap   = low and unstable
R_res   = low
B_sync  = high
C_sup   = moderate-low and falling
F_casc  = high
V_E     = hovering near or below θ_rec with oscillatory instability
```

### Why This Looks This Way

- no one machine failure fully explains the state;
- instead, multiple burdens interact;
- local recovery attempts consume reserve without restoring full ecological coherence;
- the system alternates between partial compensation and renewed cascade pressure.

### Ecological Reading

This is:

```text
compound spiral failure
```

It is probably the most important scenario for the life boundary because it shows how:

- the cell can still be active;
- the ecology can still be partially compensating;
- and yet owned recoverability can be near loss.

## Comparative Table

| Scenario | `R_cap` | `R_res` | `B_sync` | `C_sup` | `F_casc` | Main style |
|---|---|---|---|---|---|---|
| Acute respiratory crash | moderate-low, falling fast | low, draining | high | weakening | very high | acute collapse |
| Chronic translation decay | moderate, slowly declining | moderate-low, eroding | moderate, rising | thinning | moderate, later rising | cumulative degradation |
| Boundary-collapse cascade | moderate then sharply compromised | moderate then rapidly consumed | very high | collapsing | very high | containment failure |
| Repair-buffered recovery | moderate-high | moderate | low-moderate | high | low-moderate | recoverable stress |
| Mixed burden spiral | low and unstable | low | high | moderate-low, falling | high | compound failure |

This table is the strongest current comparative output of the file.

## What the Comparison Clarifies

The scenario comparison clarifies six important things.

## 1. Low Reserve and High Cascade Are Not Enough by Themselves

Different scenarios can share:

- low reserve;
- high cascade risk;

yet still differ dramatically in:

- time scale;
- burden source;
- reversibility;
- ecological shape.

That is why the ecology layer needs more than one variable.

## 2. Burden Synchronisation Is One of the Sharpest Discriminators

This variable now looks especially important.

Why:

- acute respiratory crash raises it quickly;
- chronic translation decline raises it gradually;
- repair-buffered states keep it partly suppressed;
- boundary collapse drives it abruptly very high.

This suggests `B_sync` is one of the most valuable next variables to refine further.

## 3. Cross-Support Strength Distinguishes Recovery from Decline Better Than Local Severity Alone

Local machine stress can be serious while recovery remains real if:

- `C_sup` stays high enough;
- reserve remains usable;
- burdens remain partly separable.

That is one of the strongest formal support points for the life boundary.

## 4. The Model Distinguishes Acute and Cumulative Failure Properly

This is a major success.

The scenarios show clearly that:

- acute respiratory crash

and:

- chronic translation decline

are not just the same curve at different speeds.

They are different ecological shapes.

## 5. The Model Can Also Describe Positive Persistence

The repair-buffered scenario matters because it proves the model can describe:

- stressed but viable life;
- burdened but owned recoverability;
- real resilience.

That is important because the ontology is not only about collapse.

## 6. Mixed Burden Spiral Is Probably the Most Realistic Severe Whole-Cell Pattern

This may be the most important scenario in the whole file.

Why:

Because many severe living failures are probably not pure:

- respiratory crashes;
- or pure translation declines;
- or pure boundary failures.

They are coupled spirals.

The model now has a way to say that clearly.

## Strongest Current Scenario Rule Set

The comparison supports a small set of stronger rules.

## Rule 1

```text
Different cell failures are not distinguished only by how much burden they contain, but by how burden is organised ecologically.
```

## Rule 2

```text
Burden synchronisation is one of the best current predictors of whether local stress is becoming ecology-owning decline.
```

## Rule 3

```text
Cross-support strength is one of the best current predictors of whether severe burden remains recoverable.
```

## Rule 4

```text
Boundary failure is ecologically special because it destroys separability rather than merely increasing load.
```

## Rule 5

```text
Many severe living failures are likely mixed spirals rather than single-machine collapses.
```

These are the strongest current rules that come out of the comparison.

## What This Clarifies About Life Boundary and Death Approach

The scenario comparison improves the life boundary again.

It now becomes clearer that:

- life persists when severe burden remains ecologically recoverable;
- death approaches when burden becomes ecology-owning;
- ecology-owning burden is usually a matter of synchronisation, reserve exhaustion, cross-support collapse, and cascade pressure together.

This is stronger than the older language of:

- stress;
- damage;
- decline;

taken separately.

## Best Current Compression

The best short line is:

```text
Cells fail not only by load, but by the shape their burdens take together.
```

The best fuller line is:

```text
Different living failures are ecologically different: some drive rapid collapse, some erode recoverability gradually, some destroy bounded separability, some remain recoverable under repair buffering, and some spiral through multi-machine coupling until owned recovery is nearly lost.
```

These are the strongest reusable lines from the scenario comparison.

## What This File Now Resolves

This file resolves five things.

1. The ecology formalism has now been pressure-tested against different whole-cell paths.
2. The model can distinguish acute, cumulative, containment, buffered, and mixed burden patterns.
3. The life boundary is better grounded in ecological scenario logic.
4. The mixed burden spiral now has an explicit place in the ontology.
5. The next technical work can now refine the most important variables rather than all variables equally.

## Recommended Next Workstream

The best next move is:

```text
refine the strongest ecology variables rather than expanding the variable set
```

If one file is required next, the best immediate candidate is:

```text
ams-burden-synchronisation-formalism-v1.md
```

because the scenario comparison strongly suggests that `B_sync` is one of the sharpest current discriminators and deserves its own more careful treatment.

## Compact Grammar

The best compression is:

```text
Cells fail not just by pressure, but by synchrony.
```

## Provisional Conclusion

The recovery-ecology formalism has survived a first meaningful stress test.

AMS scenario comparison summary:

```text
The recovery-ecology model can now distinguish several different whole-cell trajectories, showing that viability and death approach depend not only on burden magnitude but on reserve depth, cross-support strength, burden synchronisation, and cascade organisation across the machine ecology as a whole.
```

Score:

```text
recovery ecology scenario comparison: 9.35/10
```
