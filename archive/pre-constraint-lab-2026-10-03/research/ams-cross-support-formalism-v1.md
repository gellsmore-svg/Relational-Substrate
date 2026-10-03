# AMS Cross-Support Formalism v1

## Purpose

This file formalises cross-support as a distinct ecology-level variable.

The recent recovery-ecology work introduced:

```text
C_sup = cross-support strength
```

and the later formalism and scenario work showed that this variable is central to whether:

- burdens remain locally containable;
- reserve can be used intelligently;
- synchronisation is damped;
- cascade pressure is resisted;
- recoverability remains owned by the ecology.

This file therefore develops `C_sup` more carefully.

## Central Claim

The central claim is:

> Cross-support is one of the strongest current indicators of real ecological recoverability because a living system does not remain viable merely by having many machines present, but by having machines that still support, buffer, and restore one another strongly enough that local burdens do not become globally owning decline.

More briefly:

```text
Life survives when machines still help each other enough.
```

## Why Cross-Support Matters More Than Local Machine Quality Alone

A cell can contain:

- one very strong machine;
- one still-functional repair system;
- one remaining reserve pool;

and yet still approach death.

Why:

because isolated strength is not enough if:

- burdens are already synchronising;
- support routes have thinned;
- recovery cannot be distributed across the ecology;
- one machine's health no longer materially helps another.

That means local excellence is not the same as ecological viability.

Ecological viability depends on:

```text
effective mutual support
```

not just the existence of machine parts.

## The Ecological Meaning of Cross-Support

Cross-support means:

```text
the degree to which one machine's present coherence, output, or reserve materially improves another machine's ability to remain coherent, recoverable, or burden-buffering
```

This includes:

- direct energetic support;
- renewal support;
- burden buffering;
- regulatory coordination;
- preservation of bounded separability.

Cross-support is therefore not merely:

```text
machines are connected
```

It is:

```text
machine relations remain positively effective for shared recoverability
```

## First Formal Definition

Let the machine ecology be:

```text
E = {M_1, M_2, ..., M_n}
```

with the support matrix:

```text
K_sup = [s_ij]
```

where:

- `s_ij >= 0`
- `s_ij` measures how strongly machine `M_i` supports machine `M_j`

Then cross-support strength should be treated as:

```text
C_sup = sup(K_sup, Q_i, R_res, B_sync)
```

This matters because support depends not only on coupling topology, but also on:

- whether the supporting machine is coherent enough to support;
- whether enough reserve exists to make support usable;
- whether synchronised burden is already overwhelming support routes.

## Structural Support vs Effective Support

This distinction is necessary.

Let:

```text
C_struct = structural support
C_eff    = effective support
```

## 1. Structural Support

Define:

```text
C_struct = Σ s_ij
```

Interpretation:

This is the raw topology of supportive links.

It answers:

```text
how much support architecture exists in principle?
```

But this is not enough.

A cell can retain structural support routes while still losing actual ecological support.

## 2. Effective Support

Define:

```text
C_eff = Σ (s_ij * Q_i * U_j)
```

where:

- `Q_i` = coherence of supporting machine `M_i`
- `U_j` = usability of support by recipient machine `M_j`

Interpretation:

Support only counts strongly when:

- the supporter is coherent enough to provide it;
- the receiver is still capable of using it;
- the ecology is not so synchronised that the support arrives too late or too weakly.

This is the most important distinction in the file.

## Recipient Usability Function

The ecology needs a first usability term.

Define:

```text
U_j = 1 / (1 + p*A_j + q*C_j + r*B_sync)
```

where:

- `A_j` = acute burden on recipient machine
- `C_j` = cumulative burden on recipient machine
- `B_sync` = ecology-wide burden synchronisation
- `p,q,r > 0`

Interpretation:

Support becomes harder to use when:

- acute destabilisation is high;
- cumulative burden is high;
- synchronisation is high.

This is the right direction.

Support can exist structurally while becoming ecologically unusable.

## Reserve Modulation of Cross-Support

Reserve matters because support often requires spare capacity.

Define reserve-modulated effective support:

```text
C_sup* = C_eff * Φ(R_res)
```

with:

```text
Φ(R_res) = 1 + k*R_res
```

for `k > 0`.

Interpretation:

- deeper reserve increases the ecology's ability to convert support topology into real support;
- shallow reserve makes the same support topology less effective.

This is important because support is often reserve-dependent rather than free.

## Cross-Support Classes

The ecology formalism is clearer if support is divided into classes.

The strongest current classes are:

## 1. Energy Support

Meaning:

```text
machine A supports machine B by supplying or preserving ordered-energy headroom
```

Examples:

- respiration supporting repair;
- respiration supporting translation;
- boundary systems preserving energetic asymmetry.

## 2. Renewal Support

Meaning:

```text
machine A supports machine B by preserving or restoring the architecture B depends on
```

Examples:

- translation supporting respiratory component renewal;
- renewal systems supporting repair machinery turnover.

## 3. Buffering Support

Meaning:

```text
machine A supports machine B by absorbing or reducing the burden that would otherwise destabilise B
```

Examples:

- antioxidant and repair systems buffering respiratory damage;
- clearance systems buffering translation burden.

## 4. Coordination Support

Meaning:

```text
machine A supports machine B by improving timing, allocation, or regulatory fit
```

Examples:

- regulatory systems rerouting effort toward repair;
- state-switching logic delaying unnecessary load.

## 5. Separability Support

Meaning:

```text
machine A supports machine B by helping keep burdens partitioned rather than synchronised
```

Examples:

- boundary systems containing local insult;
- coordination systems reducing cross-machine entanglement.

This last class is especially important because it links `C_sup` directly to `B_sync`.

## Cross-Support Decomposition

The first useful decomposition is:

```text
C_sup = C_en + C_ren + C_buf + C_coord + C_sep
```

where:

- `C_en` = energy support
- `C_ren` = renewal support
- `C_buf` = buffering support
- `C_coord` = coordination support
- `C_sep` = separability support

This decomposition is not yet fully quantitative, but it prevents cross-support from remaining too generic.

## Support Decay

Cross-support weakens in at least three ways.

## 1. Local Supporter Decay

Pattern:

```text
Q_i falls, so the supporting machine can no longer give as much support
```

## 2. Recipient Unusability

Pattern:

```text
U_j falls, so support still exists but can no longer be productively used
```

## 3. Ecology-Wide Synchronisation Overrun

Pattern:

```text
B_sync rises, making many support relations simultaneously less effective
```

This third mode is one of the main reasons `C_sup` and `B_sync` must be studied together.

## First Relation to Synchronisation

The strongest current relation is:

```text
B_sync high -> C_sup effective decreases
C_sup high -> B_sync effective decreases
```

This gives a reciprocal ecology rule.

More formally:

```text
B_sync* = B_sync / (1 + m*C_sup*)
```

for positive `m`.

Interpretation:

effective support damps the ecological force of synchronisation.

This is a useful first reciprocal coupling.

## First Relation to Recovery Capacity

The strongest current relation is:

```text
R_cap rises with effective cross-support
```

First approximation:

```text
R_cap = h(Q_i, C_sup*, burdens)
```

or more explicitly:

```text
R_cap = (Σ w_i*Q_i + a*C_sup*) / (1 + Σ A_i + Σ C_i)
```

This means:

- support is not a side variable;
- it is a direct contributor to ecology-level recovery.

## First Relation to Reserve

The strongest current relation is:

```text
reserve enables support, and support preserves reserve
```

Why:

- support often costs reserve to use;
- but good support prevents wasteful burden spread that would otherwise consume reserve faster.

This is a mutually reinforcing pair, not a one-way dependency.

## Cross-Support Archetypes

The variable becomes more useful when support archetypes are separated.

## 1. Robust Support Ecology

Pattern:

- high `C_struct`
- high `C_eff`
- high reserve
- low synchronisation

Meaning:

```text
the system still knows how to help itself strongly
```

## 2. Thin but Functional Support Ecology

Pattern:

- moderate support topology
- moderate effective support
- reserve not deep but still usable
- burdens still partly partitioned

Meaning:

```text
the system is burdened but genuinely recoverable
```

## 3. Hollow Support Ecology

Pattern:

- structural support still present
- effective support low
- recipient usability poor
- synchronisation high

Meaning:

```text
the ecology still looks connected, but no longer supports itself well enough
```

This is a very important archetype.

It explains how a system can appear complex and organised while nearing failure.

## 4. Broken Support Ecology

Pattern:

- support routes decayed
- effective support collapsed
- synchronisation high
- cascade pressure dominant

Meaning:

```text
the ecology no longer functions as a support network
```

This is the strongest current ecology-level death-approach state.

## Best Current Formal Rules

The cross-support formalism is most useful when expressed as rules.

## Rule 1

```text
Structural support is not the same as effective support.
```

## Rule 2

```text
Support only counts strongly when the giver is coherent, the receiver is usable, and the ecology is not too synchronised.
```

## Rule 3

```text
Reserve and support mutually reinforce one another.
```

## Rule 4

```text
High synchronisation is dangerous partly because it hollows out effective support even when support topology still exists.
```

## Rule 5

```text
Life persists while effective support remains strong enough to keep burdens ecologically partitionable and recoverable.
```

This last rule is one of the strongest current life-boundary lines.

## What This Clarifies About Life

This file strengthens the life ontology again.

Life is not only:

- machine coherence;
- or recoverability;
- or burden tolerance.

It is also:

```text
the continued effectiveness of mutual machine support inside one bounded ecology
```

That means death approach can now be seen not only as:

- rising burden;
- rising synchronisation;

but also as:

```text
the hollowing out of effective ecological support
```

This is a major gain.

## Best Current Compression

The best short line is:

```text
Life survives while support is still real.
```

The best fuller line is:

```text
A living system remains recoverable while its machines still support one another effectively enough that burdens remain usable, partitionable, and reversible rather than synchronising into cascade beyond ecological recovery.
```

These are the strongest current reusable support lines.

## What This File Now Resolves

This file resolves five things.

1. `C_sup` now has its own formal treatment.
2. Structural support and effective support are now separated.
3. Recipient usability and reserve modulation are now built into support logic.
4. Support is now formally tied to synchronisation and recovery capacity.
5. The ecology layer now has a second major variable sharpened after `B_sync`.

## Recommended Next Workstream

The best next move is:

```text
either integrate support and synchronisation into one coupled ecology model
or formalise reserve depth next
```

If one file is required next, the best immediate candidate is:

```text
ams-reserve-depth-formalism-v1.md
```

because reserve now clearly sits between support, burden, and recoverability as the next crucial ecology variable to sharpen.

## Compact Grammar

The best compression is:

```text
Life fails when support becomes hollow.
```

## Provisional Conclusion

Cross-support now has a useful formal shape in the corpus.

AMS cross-support summary:

```text
Cross-support is one of the strongest current indicators of ecological recoverability because living systems remain viable not merely when support routes exist, but when support remains effective enough to help machines buffer, restore, and partition one another's burdens before synchronisation and cascade make recovery ecologically hollow.
```

Score:

```text
cross-support formalism: 9.4/10
```
