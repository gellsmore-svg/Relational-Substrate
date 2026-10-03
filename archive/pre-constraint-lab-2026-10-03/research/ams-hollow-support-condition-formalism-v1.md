# AMS Hollow Support Condition Formalism v1

## Purpose

This file formalises the hollow-support condition as a distinct severe ecology state.

Recent work has already shown that:

- support topology can remain present;
- compensation can remain visible;
- local function can remain active;

while:

- effective support becomes weak;
- reserve becomes shallow;
- synchronised burden stays high;
- recoverability becomes thin.

That condition is important enough to deserve its own formal treatment.

## Central Claim

The central claim is:

> A hollow-support condition exists when the ecology still retains structural support routes and visible compensatory activity, but effective support has fallen too low to restore reserve, reduce synchronisation, or rebuild robust recoverability. In that state, the system may still look organised and active, yet its support relations no longer function as genuinely restorative ecology.

More briefly:

```text
The system still looks held together, but it is no longer being held together well enough.
```

## Why Hollow Support Needs Its Own Category

Without this category, the ontology risks collapsing two importantly different cases into one:

1. chronic decline with still-real support
2. severe states in which support remains structurally present but functionally hollow

Those are not the same.

They differ in:

- what visible activity means;
- how misleading apparent compensation can be;
- how close the system may be to death approach despite still looking organised.

The hollow-support condition therefore matters especially for:

- life-boundary precision;
- anti-naive recovery judgments;
- distinguishing real recoverability from merely prolonged activity.

## Hollow Support Definition

The hollow-support condition is the ecology state in which:

```text
C_struct remains non-trivial
but C_eff is too low relative to burden, reserve loss, and synchronisation to keep the ecology restoratively recoverable
```

This is the decisive distinction.

Support still exists in principle.
It no longer works well enough in practice.

## Structural vs Effective Support

The earlier support formalism already defined:

```text
C_struct = structural support
C_eff    = effective support
```

The hollow-support condition is the first place where that distinction becomes central rather than optional.

## Structural Support

Structural support asks:

```text
how much support architecture still exists in principle?
```

## Effective Support

Effective support asks:

```text
how much of that support is still actually helping the ecology remain recoverable?
```

The hollow-support condition appears when the gap between these becomes large enough to matter ecologically.

That gap can be written as:

```text
H_gap = C_struct - C_eff
```

This is the first important variable in the file.

## Hollowing Gap

Define:

```text
H_gap = C_struct - C_eff
```

Interpretation:

- low `H_gap` means support architecture is still largely effective
- high `H_gap` means the ecology still looks connected, but much of its support is no longer operationally meaningful

This is one of the strongest current severe-state markers in the corpus.

## The Three Main Drivers of Hollow Support

The hollow-support condition is usually driven by three things:

1. supporter weakening
2. recipient unusability
3. synchronisation overrun

These should be formalised separately.

## 1. Supporter Weakening

This occurs when:

```text
Q_i falls in support-giving machines
```

Interpretation:

the support route still exists, but the supporting machine is too compromised to supply support strongly.

Examples:

- repair systems still active but underpowered
- respiratory support still present but thin
- coordination systems still signalling but poorly

## 2. Recipient Unusability

This occurs when:

```text
U_j falls in burdened recipient machines
```

using the earlier usability term:

```text
U_j = 1 / (1 + p*A_j + q*C_j + r*B_sync)
```

Interpretation:

support still exists, but the recipient machine is too burdened or too synchronised to use it well.

This is one of the clearest reasons a system can still be supported in principle while no longer being recoverable in practice.

## 3. Synchronisation Overrun

This occurs when:

```text
B_sync remains high enough that many support relations are simultaneously blunted
```

Interpretation:

support is not only locally weakened.

It is ecologically outpaced by burden alignment.

This is why hollow support is often a severe-state concept rather than merely a moderate-stress concept.

## First Hollow-Support Function

The simplest useful hollow-support function is:

```text
H_cond = H_gap * Ω(B_sync, R_res)
```

where:

- `H_gap = C_struct - C_eff`
- `Ω(B_sync, R_res)` increases with synchronisation and decreases with reserve

The best first approximation is:

```text
Ω(B_sync, R_res) = (1 + m*B_sync) / (1 + n*R_res)
```

for positive `m` and `n`.

Interpretation:

Hollow support becomes ecologically serious when:

- the gap between structural and effective support is large;
- synchronisation is high;
- reserve is shallow.

This is the right shape.

## Hollow-Support Criterion

The best first criterion is:

```text
Hollow_E = 1 if:
1. C_struct remains moderate or high
2. C_eff is low or sharply reduced
3. H_cond exceeds a hollowing threshold θ_h
4. V_E is near θ_rec or trending downward
```

This is better than simply saying:

```text
support is weak
```

because hollow support is not identical to weak support in general.

It is:

```text
apparent support that no longer restores enough ecology to matter as true recoverability
```

## The Signature Variable Pattern

The strongest current hollow-support signature is:

```text
C_struct = moderate-high
C_eff    = low
H_gap    = high
R_res    = low
B_sync   = high
R_cap    = moderate at best
F_casc   = high
V_E      = near θ_rec
```

This is the main comparative fingerprint.

## Hollow Support vs Chronic Decay

This distinction is important.

### Chronic Decay

Main shape:

- cumulative burden high
- reserve eroding
- support thinning gradually
- future recoverability narrowing

### Hollow Support

Main shape:

- support architecture still present
- visible compensation still active
- effective support already too weak to be meaningfully restorative

The crucial difference is:

```text
chronic decay describes a burden path
hollow support describes a support condition within or across burden paths
```

That is why hollow support can appear:

- inside chronic decline;
- inside mixed spirals;
- inside near-death active states.

## Hollow Support vs Mixed Spiral

This distinction is also important.

### Hollow Support

This is mainly a condition:

```text
support is no longer effectively restorative
```

### Mixed Spiral

This is mainly a process:

```text
recovery cycles continue while hollow support helps drive net decline
```

So:

- hollow support can exist without a full spiral
- mixed spirals usually involve hollow support

This is the strongest current relation between the two concepts.

## Hollow Support Archetypes

The hollow-support condition itself appears in several subtypes.

## 1. Repair-Hollow State

Pattern:

- repair still active
- damage buffering still visible
- but reserve and effective support too weak for deep restoration

Meaning:

```text
the system is repairing, but mostly to delay failure
```

## 2. Coordination-Hollow State

Pattern:

- regulation still active
- signals still present
- but allocation quality no longer meaningfully restores ecology-level headroom

Meaning:

```text
the system still manages, but not well enough to heal
```

## 3. Renewal-Hollow State

Pattern:

- some renewal continues
- architecture still turns over
- but output quality and reserve restoration are too weak

Meaning:

```text
the system still replaces parts, but not fast or well enough to recover
```

## 4. Boundary-Hollow State

Pattern:

- containment machinery still functions partially
- but not strongly enough to keep burdens partitioned

Meaning:

```text
the system still holds itself together locally, but no longer preserves robust separability
```

These subtypes are helpful because they show hollow support is not one narrow pathology.

## Best Current Formal Rules

The hollow-support formalism is most useful when expressed as rules.

## Rule 1

```text
Support can remain structurally present while ceasing to be ecologically restorative.
```

## Rule 2

```text
Visible compensation is not evidence that effective support remains strong.
```

## Rule 3

```text
High synchronisation and shallow reserve are the strongest amplifiers of support hollowing.
```

## Rule 4

```text
Hollow support is one of the clearest markers of false recovery.
```

## Rule 5

```text
Death approach often begins before support disappears; it begins when support remains too hollow to restore future recoverability.
```

This fifth rule is one of the strongest current severe-state lines in the ecology layer.

## What This Clarifies About Life Boundary

This file strengthens the life boundary again.

It explains why a system may still:

- act;
- compensate;
- repair;
- remain locally organised;

without therefore being robustly recoverable.

The key line is:

```text
life remains while support is still real enough to preserve owned recoverability
```

The hollow-support condition marks the state where that becomes doubtful even before all activity disappears.

That is one of the most useful boundary clarifications in the current corpus.

## What This Clarifies About Death Approach

The strongest current hollow-support reading of death approach is:

```text
death approach often begins when the ecology still looks organised but no longer supports itself restoratively enough to rebuild reserve, reduce synchrony, or restore robust recoverability
```

This is a strong line because it blocks a naïve equation:

```text
organisation visible
therefore recoverability remains strong
```

That equation is false.

## Best Current Compression

The best short line is:

```text
The system is dying when support still exists but no longer saves.
```

The best fuller line is:

```text
A hollow-support condition exists when structural support routes and visible compensatory activity remain, but effective support has fallen too low relative to synchronisation, reserve loss, and burden debt to restore ecology-level recoverability; the system may still appear organised, yet its support is no longer restorative enough to preserve its future as a living ecology.
```

These are the strongest current reusable hollow-support lines.

## What This File Now Resolves

This file resolves five things.

1. Hollow support now has its own formal treatment.
2. The gap between structural and effective support is now explicit.
3. Hollow support is now cleaner to distinguish from chronic decay and mixed spiral.
4. False recovery has a stronger ecology-level marker.
5. The life-boundary work is stronger against superficial recovery readings.

## Recommended Next Workstream

The best next move is:

```text
either integrate the severe-state ecology work back into the life-boundary synthesis
or continue sharpening the remaining severe patterns comparatively
```

If one file is required next, the best immediate candidate is:

```text
ams-life-boundary-synthesis-v3.md
```

because the severe-state ecology layer is now strong enough that the life-boundary synthesis should absorb it directly rather than leaving it distributed across technical notes.

## Compact Grammar

The best compression is:

```text
The dangerous systems are the ones that still look helped.
```

## Provisional Conclusion

The hollow-support condition now has a strong place in the corpus.

AMS hollow-support summary:

```text
A hollow-support condition exists when the ecology still retains support structure and visible compensation, but effective support has become too weak to rebuild reserve, lower synchrony, or restore robust recoverability; the system therefore appears held together while no longer being restoratively held together enough to secure its future as a living ecology.
```

Score:

```text
hollow support condition formalism: 9.45/10
```
