# Historical role grammar

## Pre-freeze definitions and generic reduction

This section records semantics, symbolic covariance and structural enumeration
before I0 freeze. Actual non-neutral I0 stationary, projection, feedback,
fingerprint and temporal calculations remain unopened at drafting. Post-freeze
proofs and verification links will be appended separately.

The ordinary material state still has six pair/four independent triad bits.
At pair epochs, augmented state is (p,h), p in 0..63 and h in 0..5. A pair
event e sends (p,h) to (p xor 2^e,e). Triad events preserve p and h.
No S, L, geometry, deeper H or new relation channel is introduced.

rho(e,h) is SAME, ADJACENT or DISJOINT by equality/intersection of the two
unordered vertex pairs. Counts per h are (1,4,1), mechanically enumerated.
Direction is FORM on an absent candidate bit and DISSOLVE on a present one.
The eleven declared single-feature predicates use only rho, direction or their
conjunction. Weights are m^phi, phi Boolean, m>0. At the initial sentinel,
history-relation predicates are inactive and current-only predicates still apply.

## Exact pair-event closure

Let W(p,h) be the sum of the six positive pair weights. At fixed p,h each
triad-only event leaves W unchanged, regardless of triad mask. Its total
full-event probability is 4/(W+4)<1. The next-pair slot probability is

```text
sum_{k>=0} [4/(W+4)]^k w_e/(W+4) = w_e/W.
```

Absorption occurs almost surely. The pair event updates only p,h as above, so
the exact next-pair process closes on 384 recurrent augmented states. This does
not assume a triad prior. Direct raw-triad block solves are separately frozen
as post-freeze checks. No dense full 7168-state kernel is required.

## Symbolic S4 covariance

A vertex permutation preserves equality and vertex intersection of pairs, and
preserves whether the relabelled candidate is present in the relabelled mask.
Therefore it preserves every feature value. It permutes the weight vector and
its sum, hence the normalised row and deterministic register/toggle update.
Thus simultaneous vertex relabelling is a kernel automorphism for every m>0.
By CL-T20 its orbits form a valid strongly lumpable quotient. I0 additionally
checks aggregate rows for every one of the 384 states for every primary cell.

## Structural orbit enumeration

Enumerating all 24 vertex permutations partitions 384 states into 28 orbits,
with total size 384. Keeping a remembered edge fixed leaves endpoint swaps and
the swap of the other two vertices. The four adjacent edge bits form a 2x2
binary matrix modulo row/column swaps. Its seven patterns have counts
1,1,3,1,1 at occupancy 0,1,2,3,4. The independent remembered and disjoint bits
give 2*2*7=28 orbits, an independent structural derivation.

The diagnostic tuple (R,A_h,D_h,C_h) has 24 distinct values. Four pairs of
orbits collide when A_h=2,C_h=0: two adjacent bits at one endpoint and two
diagonal bits are different configurations. R and D_h independently give four
such collisions. They remain distinct orbits. The exact enumeration is in
exploration/generation-008i/structural-orbits.json; it is a declared pre-freeze
structural observation, not an I0 non-neutral dynamical result.

## Reading the future atlas

Stationary solves use exact rational 28-orbit balance and exact full lift checks.
Conditional shape information must allow unequal model priors inside each
edge-count block. KU uniformly averages h at each p; Kpi uses stationary h|p.
They are distinct. Reversibility of augmented, quotient and stationary projected
kernels is kept separate. Fingerprints distinguish exact full law, quotient law,
stationary joint, stationary material and one-step projected statistics.

Any post-freeze structural effect is a behavioural observation, not a stronger
capability theorem than CL-T28. Current-only structural effects are not H
discoveries. Finite augmentation still restores first-order Markov form.
