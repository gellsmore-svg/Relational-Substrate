# Generation 008D — two-gate composition atlas

Generation 8D is Mode B. It reads the exact local transition law of every two-rule system whose rules are both one-gate `T->P` rules. It runs no new stochastic trajectory, no parameter fit, and no new control. Pass and fail in this note are reserved for tests, chronology, numerical tolerances, and CI.

The numerical record is `constraint-lab/reports/generation-008d-round-d0-tables.json`. Schema `rs-constraint-lab.composition-tables/v1`. File sha256 `dba485576e3ed30d2c7d885490c7f186dcdb6a5d55489e4abf2f0b79d2af5fb2`. Payload sha256 `f33ff7eb8549df7679a85c5756f778904b7a8ea5ffeae368e420827bbea9a553`. The column tables sit under `constraint-lab/reports/tables/generation-008d-*`, and each table's canonical sha256 is recorded in `detail_sha256` inside the summary file. The result commit is `093e460e9992e3ddc4fd24cdb43d6d5397de4e29`. Mutual information is in nats. A fraction identity is stated only where the arithmetic is exact.

The compression this round supports is short. Each primitive rule is one feature: the conjunction of its action's admissibility literal and its gate literal, carrying one log weight. Two rules add their features in the log weight of the slot they name. Six-slot normalisation turns that sum into a probability law, and it couples slots only through the shared denominator. On one action slot the log multiplier is an affine function of the gate literals, with no gate-by-gate coefficient. Exact collapses occur where the affine function loses a variable: complementary gates with equal weights, and opposite directions on one gate with equal weights. Exact syntactic twins occur where two different literal choices give the same affine function. Everything else is genuinely two-gate at the local law, and the balanced information does not see placement, direction, or literal polarity at all.

## A. External Review 008C

Review 008C is `constraint-lab/provenance/reviews/008C-chatgpt-review-v0.8c.md`. It reads branch `research/constraint-lab-v0.8c-mechanism` at `41ec34e72191f93647f28838f16296fa2c2880a3`. The review inspected branch chronology, the C0 frozen plan, the mechanism report, the mechanism tables, the local-law implementation, the topology atlas, the gate-memory analysis, the projection analysis, the drift analysis, the coherence ledger, the coherence generator, the coherence tests, and the final-head CI.

The branch is 12 commits ahead of v0.8B. Final head `41ec34e72191f93647f28838f16296fa2c2880a3`. The frozen C0 plan is `3e783387cd2c8050559c29bac059beae03555ab7`, plan hash `febde3989a8b2f2461440e708897fe78c1fdac436375c0c628b393309932c897`. The C0 tables commit is `f962000d7c6c750565843426d46bcd3fdbb43026`. The report commit is `479469f7b56277849f75080f5f8478e875d95ec7`. The prompt close-out is `41ec34e72191f93647f28838f16296fa2c2880a3`. Final-head Actions run `38356522671` succeeded. The report-head suite reported 207 passed. C0 used 60 deterministic mechanism items, no new stochastic trajectories, no parameter fit, and no new control. The largest item wall was about 1.413 seconds. The 120-second watchdog was not approached.

The review preserves the 8C compression. A triad gate reweights one pair slot. The six-slot law changes by normalisation. Graph topology maps slot identity into edge-count and shape consequences. Stochastic triad refresh erases the initial gate value, while the current gate continues to modify the current transition law. Long-run occupancy reflects persistent rule bias rather than persistent initial-context memory.

For one conditional pair rule with multiplier `m`, the inactive law is `1/6` on each slot, the active law is `m/(m+5)` on the action and `1/(m+5)` elsewhere, and the balanced current-context information is `(1/2) JS(q_0, q_m)`: 0.009748566529643857 nats at `m = 1/4` and 0.023368444772049440 nats at `m = 4`, with enumeration gaps near `1e-15`. R01, R02, and R04 are locally equivalent under that quantity. R05's extra local information is a shared denominator. On the canonical path, dissolving the middle edge gives the 2-edge matching, dissolving an end edge gives the 2-edge path, forming a short chord gives triangle plus pendant, and forming the long chord gives the 4-cycle. R01 and R06 reweight the middle edge. `I(initial gate ; current pair mask)` falls below `1e-10` by pair epoch 64, while `I(current triad ; next pair slot | full pair mask)` stays at the closed-form scale. One-gate balanced edge drift is `+5/168` for strong-suppress dissolve, `−5/168` for strong-suppress form, and `−5/72` for strong-favour dissolve. The stationary average expected edge drift is numerical zero.

## B. 8C errata and coherence corrections

`constraint-lab/reports/generation-008c-errata.md` corrects one sentence of the 8C report. The total-variation ratio `(5/18)/(5/42) = 7/3` and the one-gate drift-magnitude ratio `(5/72)/(5/168) = 7/3` are exact. The balanced-information ratio is `0.023368444772049440 / 0.009748566529643857 = 2.397115996591876`, which is not `7/3`. Jensen–Shannon divergence is nonlinear in the slot probabilities. The historical report is not edited.

In the ledger, `F8D-CORRECT-GRADE-ASYMMETRY` separates probability displacement and drift geometry from information geometry and is linked to `F8C-GRADE-ASYMMETRY` by the new controlled relation `corrects`. `F8D-DRIFT-MAGNITUDE-SCOPE` states that the large magnitude belongs to `F010-OCCUPANCY-AXIS` and that the drift-direction inference explains its sign without inheriting that magnitude. It is linked to `F8C-DRIFT-DIRECTION` by `qualifies`. Both older nodes are now `qualified`. Their statements are unchanged.

D0 adds a further example of the same distinction. Across the one-gate grade surface, strong suppression `m = 1/4` and weak favour `m = 2` have the same drift magnitude, `5/168`, because `|m−1|/(m+5)` is `1/7` at both. Their balanced informations are 0.009748566529643857 and 0.005108359895797386 nats. Equal drift does not mean equal information.

Prompt 008C v2 authored metadata, recorded beside the agent input and not assigned to it: 57,204 bytes, sha256 `aa82700852ee510cae309488df52df10875f2413bb03a13360ceebb3bb9d2568`. The stored agent input is 57,205 bytes, sha256 `dbccad0a983eab3f6f2fa738275fb62c8af9f2beffda005b08b85feb7fc034d9`. These are distinct byte strings. Prompt 008D is stored verbatim at `constraint-lab/provenance/prompts/008D-v0.8d-agent-input.md`, 35,550 bytes, sha256 `73a830bab3f5ca7a99f50bc46b90119370f64a4540c6549f9ba537f4c2e73ee1`.

## C. Question

When two higher-order relational gates coexist in the same memoryless relational system, what exact algebra of composition appears?

More specifically: which two-gate systems collapse to a simpler law, which remain genuinely two-gate at the local transition law, how their weights combine in log-weight space and in probability space, and what two gates can express that one gate cannot. Topology is not given a new trajectory census here. The 8C distinction is kept: a local-law equivalence does not imply equal source trajectories.

The words synergy, antagonism, and cooperation are not used for any measured quantity. Normalisation interaction is the name for the probability-space coupling that the shared denominator produces.

## D. Frozen D0 plan

The frozen analysis plan is commit `ac037f32df81271e04381c79efebf6f5b3d0b607`, plan hash `10a3114bcf7a1a914e9eff19e08f77a9fbcf71852bc4a22f14f04d723912ce07`, file `constraint-lab/exploration/generation-008d/round-d0-plan.json`, file sha256 `e1a0ac884e8c1d8dc16f86bca59dc90cc8170641eaa6293faf459a1048b3d460`. It was committed and pushed before any D0 law was stored. Journey step 1, commit `d3bf0f79b65f3d85e9a95e681b875c0f45b3a966`, has `result_commit` null. Actions run `38375394924` succeeded on that pre-execution commit. Journey step 2 names the tables commit `093e460e9992e3ddc4fd24cdb43d6d5397de4e29`, which descends from the frozen plan.

The frozen census: 96 labelled rules, 4560 unordered labelled pairs, 236 structural S4 orbits, 3584 weighted canonical systems. Canonicalisation used all 24 vertex permutations and unordered rule order. Neither global bit complement nor weight reciprocity was used for reduction. The work count was 237 items (236 orbit items and one one-gate surface item), 3,670,016 exact state evaluations, the same number of kernel-agreement evaluations, 86,016 S4 law images, a wall-time estimate of 1200 seconds, and a disk estimate of 80 MB. Tolerances frozen before execution: fractions exact, canonicalisation exact, probability gap, CMI equality, kernel equality, logit additivity, and reducibility at `1e-12`.

All 237 items completed in one in-process pass, one worker. The largest item wall was 5.58 seconds. The 120-second watchdog was not approached. No supervisor was needed. `generation008d verify` returned complete. Assembly validation reported ok with an empty problem list.

One commit sits between the freeze and the tables. Commit `cbfdae8a5ffb4118abcacc33a8285894f76435bf` corrected two checks in `validate_orbit_result`. Form and dissolve on the same slot with the same literal are two rules, not a repeated rule. Two different actions on opposite literals of one gate can never both be active, so their shared-denominator check has no realised state and must not be required. The correction changed the validator, not the estimands, not the analysis functions, and not any stored item. Every item file was written before that commit, and the tables were assembled after it. Re-assembling the 237 stored items with the published code reproduces the summary file byte for byte. Re-executing ORB-0000, ORB-0028, ORB-0117, ORB-0235, and the surface item reproduces the stored items exactly, wall time excluded.

## E. Two-gate structural universe

A primitive rule is one pair action (6 slots × form or dissolve) conditioned on one triad literal (4 triads × present or absent). That gives 96 labelled rules. The grammar's `structurally_simple` predicate rejects a repeated structural rule. The kernel would multiply a forced duplicate: `strong_favour` and `weak_suppress` on the same rule give the kernel weight `2/1`, the product `4 × 1/2`. That case is outside the atlas, so family A of the prompt, same action, same gate, same polarity, is not executable as two rules. Opposite directions on one slot are distinct rules and are inside the atlas.

The `C(96, 2) = 4560` unordered pairs fall into five composition families.

| Family | Labelled pairs | Count rule |
| --- | --- | --- |
| complementary_gate (same slot, same direction, same triad, opposite literal) | 48 | 6 slots × 2 directions × 4 triads |
| same_action_different_gates (same slot, same direction, two triads) | 288 | 12 actions × 6 triad pairs × 4 literal choices |
| same_slot_opposite_directions (one slot, form and dissolve) | 384 | 6 slots × 8 literals × 8 literals |
| different_actions_same_gate | 960 | 60 action pairs on distinct slots × 4 triads × 4 literal choices |
| different_actions_different_gates | 2880 | 60 action pairs × 12 ordered triad pairs × 4 literal choices |

The counts sum to 4560.

## F. Canonical S4 orbit atlas

| Family | Orbits | Labelled pairs | Incidence patterns | Weighted systems |
| --- | --- | --- | --- | --- |
| complementary_gate | 4 | 48 | 2 | 64 |
| same_action_different_gates | 20 | 288 | 3 | 272 |
| same_slot_opposite_directions | 24 | 384 | 4 | 384 |
| different_actions_same_gate | 52 | 960 | 4 | 784 |
| different_actions_different_gates | 136 | 2880 | 14 | 2080 |
| total | 236 | 4560 | | 3584 |

Orbit sizes are 24 (148 orbits), 12 (80 orbits), and 6 (8 orbits). They sum to 4560. An orbit carries 16 weighted systems when its two rules cannot be exchanged by a vertex permutation, and 10 when they can, because an exchange identifies the assignments `(w1, w2)` and `(w2, w1)`. 204 orbits carry 16 and 32 carry 10.

The structural orbit table records the action relation (same pair, adjacent pairs, disjoint pairs), direction relation, gate relation, polarity relation (same, opposite on one triad, mixed across two triads), and the full 2×2 incidence matrix. Entry `(i, j)` says whether rule `i`'s action pair is a face of rule `j`'s condition triad.

## G. Local softmax grammar

For a two-rule system the pair-event law is

```text
q(e | x) ∝ exp( λ1 φ1(x, e) + λ2 φ2(x, e) ),    λi = ln mi
```

where `φi(x, e) = 1` exactly when rule `i` names slot `e`, its action is admissible at `x` (the edge is absent for a formation, present for a dissolution), and its gate literal is true at `x`. Each primitive feature is therefore a two-literal conjunction: one admissibility literal on the slot's own bit, one gate literal on a triad bit.

The implementation agrees with this form on every system. For all 3584 weighted systems, the implementation kernel weights equal the product formula on all 1024 states as exact fractions, gap 0. The log-weight residual `log w(x, e) − (λ1 φ1 + λ2 φ2)` has maximum absolute value `2.22e-16` over every state and pair slot of every system, the float64 rounding of `ln` on exact fractions. The primitive two-rule composition is exactly additive in log weight.

That is feature composition. It is a statement about the DSL's algebra. It does not say that probabilities, informations, drifts, or trajectory observables add.

## H. Minimal sufficient coordinates

The candidate coordinates are the distinct raw bits among the two action slots and the two gate triads. Every subset was searched on all 1024 states.

| Family | Minimal coordinate count | Systems |
| --- | --- | --- |
| complementary_gate, equal weights | 1 (the action slot) | 16 |
| complementary_gate, unequal weights | 2 (action slot, gate) | 48 |
| same_slot_opposite_directions, same literal, equal weights | 1 (the gate) | 16 |
| same_slot_opposite_directions, other same-triad systems | 2 (slot, gate) | 112 |
| same_slot_opposite_directions, different triads | 3 | 256 |
| same_action_different_gates | 3 (slot, two gates) | 272 |
| different_actions_same_gate | 3 (two slots, gate) | 784 |
| different_actions_different_gates | 4 | 2080 |

In each system exactly one minimal set was found. Each was checked to have no smaller determining subset.

Two collapses appear here. A complementary pair with equal weights loses its gate, and its law reads only the action slot. A form rule and a dissolve rule on the same slot and the same literal with equal weights lose the slot's own bit, and the law reads only the gate. The second is the direction analogue of the first. Admissibility is a literal on the slot's bit, and equal weights on its two values remove it.

## I. Effective gate dimension

`effective_gate_dimension` is the smallest number of triad bits that, with the full pair mask, determines the six-slot law.

| Dimension | Systems | Reducibility classes |
| --- | --- | --- |
| 0 | 16 | R1U |
| 1 | 960 | R1T 48, R2S 912 |
| 2 | 2608 | R2G |

Dimension 2 contains two different kinds of system. In 2352 systems both rules are active together in some state. In 256 systems, every same-slot opposite-direction system with two different triads, they never are. Admissibility of form and of dissolve are complementary values of one bit. The pair mask chooses which gate is read, and each mask reads at most one triad bit. Across masks, two triad bits are needed. This split is read from the published truth tables. It is not a frozen estimand.

The simplest dimension-2 example the census names, `ORB-0028-W00`, is of the switched kind:

```text
dissolve(0-1) | absent(0-1-2) => strong_favour
form(0-1)     | absent(0-1-3) => strong_favour
```

Its truth table has two distinct rows. Edge `0-1` present with `0-1-2` absent, or edge `0-1` absent with `0-1-3` absent, gives `4/9` on slot `0-1` and `1/9` elsewhere. Every other state is uniform. Neither gate can be removed: each ablation has maximum probability gap `5/18`. No single one-gate rule reproduces it. Its balanced information is 0.046736889544097 nats, exactly twice the one-gate value, and the information each gate carries given the other equals its marginal.

The first jointly activated dimension-2 law with the fewest rows is on one slot with two gates and equal weights, for example `ORB-0001-W00`:

```text
dissolve(0-1) | absent(0-1-2) => strong_favour
dissolve(0-1) | absent(0-1-3) => strong_favour
```

with three rows: uniform, `4/9` on the action when one literal is true, and `16/21` on the action when both are true.

## J. Complementary-gate elimination

`A | G => m` together with `A | NOT G => m` reduces exactly to `A => m`. All 16 equal-weight complementary systems (4 orbits × 4 grades) are class R1U. Each one's full ten-slot weight table, pair slots and triad slots, equals the unconditional comparator's on all 1024 states as exact fractions. The full-event transition kernel is therefore identical, not only the pair-slot law. Two rows remain: uniform where the action is inadmissible, `m/(m+5)` where it is admissible.

The gate is eliminated together with its placement. The face orbit (`0-1` inside `0-1-2`) and the non-face orbit (`0-1` against `0-2-3`) give the same labelled law at every grade, in both directions. These are eight of the 24 labelled-law coincidences across orbits.

With unequal weights the gate partitions the action. Exactly one of the two literals is true, so the action carries `m_present` or `m_absent`. All 48 such systems are class R1T, with three rows: uniform, `m_present/(m_present+5)`, and `m_absent/(m_absent+5)`. The DSL has no single primitive rule with a two-level gate, so R1T is a local-law equivalence to a two-level gate law without a one-rule syntactic representation. The kernel check is the algebraic table identity, gap 0.

This is the higher-order analogue of the Generation 7B diagonal collapse, `F009-TWO-LEVEL-COLLAPSE`, where a two-parameter pair-face representation used its two slots as one unconditional weight. Here the two literal values of one triad bit, given the same weight, become no condition at all.

## K. Same-action different-gate composition

Two rules on the same action and two different triads give the action four levels,

```text
G1 G2   action multiplier
0  0    1
1  0    m1
0  1    m2
1  1    m1*m2
```

where `Gi` is literal truth, not the raw triad bit. On all 272 systems in the family the both-active row was checked against `m1*m2/(m1*m2+5)` on the action and `1/(m1*m2+5)` elsewhere, gap 0, and the logit interaction

```text
Δ12 L = L11 − L10 − L01 + L00
```

is 0 on every system. Two primitive one-gate rules do not create a gate-by-gate logit coefficient.

The levels coincide in two ways. When `m1 = m2`, the two single-active rows are the same law. When `m1*m2 = 1`, the both-active row returns to the uniform law. Each gives three distinct rows: 80 systems with equal weights, 64 with reciprocal weights. The remaining 128 systems have four rows.

Reciprocal weights also produce syntactic twins. On one slot the log multiplier is

```text
L = c + β1 G1 + β2 G2        (Gi now the raw triad bits)
```

A present literal with log weight `λ` contributes `β = λ`. An absent literal contributes `β = −λ` and adds `λ` to `c`. Flipping both literals and inverting both weights keeps `(β1, β2)` and changes `c` by `−(λ1 + λ2)`, so the law is unchanged exactly when `m1*m2 = 1`. For example

```text
dissolve(0-1) | absent(0-1-2)  => strong_favour
dissolve(0-1) | absent(0-2-3)  => strong_suppress
```

and

```text
dissolve(0-1) | present(0-1-2) => strong_suppress
dissolve(0-1) | present(0-2-3) => strong_favour
```

have the identical labelled weight table: both are `L = ln 4 · (G_023 − G_012)`. Sixteen labelled-law coincidences across orbits are of this kind. Eight more coincide only after a vertex permutation. Together with the eight complementary coincidences in section J, these are all of the cross-orbit coincidences in the census: 24 labelled, 32 under S4. The local law determines `(c, β1, β2)`. It does not determine which literals were written.

## L. Different-action same-gate composition

Two actions on different slots read one triad.

With the same literal, the gate is a jointly gated multi-slot bias. When the literal is true and both actions are admissible,

```text
q(a) = m1 / (m1 + m2 + 4)
q(b) = m2 / (m1 + m2 + 4)
q(other) = 1 / (m1 + m2 + 4)
```

For `ORB-0005-W00`, two `strong_favour` dissolutions of `0-1` and `0-2` on `absent(0-1-2)`, that row is `1/3, 1/3, 1/12, 1/12, 1/12, 1/12`. With one action admissible the other slot keeps weight 1, so the row is the one-gate law on that slot. All 400 same-literal systems have four rows: uniform, slot `a` alone, slot `b` alone, and both. Equal weights do not merge the two single-slot rows, because they reweight different slots. Effective gate dimension is 1 throughout. Class R2S.

With opposite literals the gate is a partition across slots. Exactly one of the two rules can be active. The triad bit selects which slot is reweighted. The two rules are never active together, so no state realises the shared denominator. All 384 such systems have three rows: uniform, `q_{m1}` on slot `a`, `q_{m2}` on slot `b`. Dimension 1, class R2S.

## M. Different-action different-gate composition

Two actions on different slots read two different triads. Where both actions are admissible there are four activation combinations, and the logit vector is

```text
z = λ1 G1 e_a + λ2 G2 e_b
```

Each gate moves its own coordinate of the slot-logit vector. The logits add, coordinate by coordinate, with no cross term. The probabilities do not: when both are active, slot `a`'s probability is `m1/(m1+m2+4)`, which depends on `m2`. That dependence is the normalisation interaction. It is a property of the denominator, not of a gate-by-gate coefficient.

For `ORB-0007-W00`, `dissolve(0-1) | absent(0-1-2) => strong_favour` with `dissolve(0-2) | absent(0-1-3) => strong_favour`, the truth table on masks with both edges present is uniform, `4/9` on `0-1`, `4/9` on `0-2`, and `1/3, 1/3, 1/12, 1/12, 1/12, 1/12` when both literals are true. All 2080 systems in the family are jointly activated, have four distinct rows, need four coordinates, and are class R2G. The shared-denominator formula was checked on all 2080, gap 0. If the actions coincide, `z = (λ1 + λ2) e_a`, which is section K.

### Same slot, opposite directions

The opposite-direction family is the one place where two rules on one slot cannot coexist. Form is admissible only where the edge is absent and dissolve only where it is present, so the two rules are never active together.

On one triad with the same literal and equal weights the slot's own bit drops out (section H). The law is a gated toggle: slot `e` carries `m` whenever the literal is true, whatever the edge state. On one triad with opposite literals and equal weights, for example `ORB-0027-W00`,

```text
dissolve(0-1) | absent(0-1-2)  => strong_favour
form(0-1)     | present(0-1-2) => strong_favour
```

the action is active exactly when `edge(0-1) XOR triad(0-1-2)` is 1. Two rows, two coordinates. Two primitive literals realise an XOR between a slot's own bit and a gate bit, because each primitive feature already contains a literal on the slot's own bit. With unequal weights these become two-level forms, 3 rows. With two different triads they are the switched dimension-2 systems of section I.

## N. Log-space additivity

On every one of the 3584 weighted systems, every state, and every pair slot, the combined log weight equals the sum of the two rules' log-weight features. The maximum residual is `2.22e-16`, against the frozen tolerance `1e-12`. 3584 log-weight-additivity identities and 3584 kernel-agreement identities are recorded in the identities table, all verified.

## O. Probability-space normalisation interaction

The two closed forms are:

```text
different action slots, both active:
q(a) = m1 / (m1 + m2 + 4),   q(b) = m2 / (m1 + m2 + 4),   q(other) = 1 / (m1 + m2 + 4)

same action slot, both active:
q(a) = m1*m2 / (m1*m2 + 5),  q(other) = 1 / (m1*m2 + 5)
```

They hold for all positive `m1` and `m2`. The implementation check is at the W4 points, on every both-active state of every system where both rules can be active: 2480 different-action systems and 272 same-action systems, all with exact-fraction gap 0. The 384 opposite-literal same-gate systems and the 384 opposite-direction systems have no both-active state. The validator confirms that no state activates both rules there. The surface item also evaluates the two forms at `(1/4, 4)`, `(1/2, 2)`, `(3, 5)`, `(1/3, 7)`, and `(4, 4)`. That item checks the normalisation arithmetic, not the kernel.

## P. Truth-table expressivity

On one action with two distinct gate literals, the log multiplier over the four literal states is

```text
L(G1, G2) = c + λ1 l1(G1) + λ2 l2(G2)
```

with `li` the chosen literal of `Gi`. Every such table satisfies `Δ12 L = 0`, so `L11 = L10 + L01 − L00`. That gives the exact answers to the three questions.

There is no independently tunable conjunction term. The both-active level is fixed by the other three.

XOR between two gates cannot be isolated. An XOR table needs `L00 = L11 ≠ L10 = L01`, so `Δ12 L = −2(L10 − L00) ≠ 0`. A literal flip replaces `li` by `1 − li`, which changes `c` and the sign of `λi` and leaves `Δ12 L = 0`. No choice of literals or weights reaches XOR.

The both-active state cannot be moved while the other three are fixed. The nearest available shape is `L11 = L00`, reached only with `λ2 = −λ1`, which forces `L10 = −L01`. The reciprocal systems of section K realise that shape.

The bound is about two gate literals. Between a slot's own bit and one gate bit, XOR is realised by two rules, `ORB-0027-W00` in section M, because admissibility and the gate literal are already conjoined inside each primitive feature. The surface item records the bound as a statement. The evidence is the derivation above and the 272 measured `Δ12 L = 0` identities.

## Q. Reducibility classes

| Class | Meaning | Systems |
| --- | --- | --- |
| R0 | baseline, no effective rule | 0 |
| R1U | one unconditional pair rule | 16 |
| R1G | one one-gate conditional pair rule | 0 |
| R1T | one action with a two-level complementary gate law | 48 |
| R2S | two rules, one effective triad bit | 912 |
| R2G | two distinct triad bits at the local law | 2608 |

The comparator grammar is the 433 one-rule laws: the empty law, 48 unconditional rules (6 slots × 2 directions × 4 grades), and 384 one-gate rules (6 × 2 × 4 triads × 2 literals × 4 grades). Every R1U system reproduces its comparator's full weight table on all 1024 states. No R2G system matches any comparator.

R0 is empty because every rule carries a non-neutral weight and no two distinct rules cancel on every state. R1G is empty. A one-gate law reweights one region, the 256 states where one admissibility literal and one gate literal are both true, by one multiplier. Every two-rule system either reweights two such regions with non-neutral weights, or covers both halves of one admissible region, which is R1U or R1T. R1T is a local-law equivalence without one-rule syntax. The DSL cannot write a two-level gate in one primitive rule. R2S collects the same-gate different-action systems (784) and the same-triad opposite-direction systems (128).

These are local-law classes. They say nothing about global irreducibility.

## R. Balanced information atlas

`I(full current triad ; next pair slot | full pair mask)` under the balanced weighting was computed on every system and reproduced from truth-table weighting on the gate bits alone. The maximum gap between the two is `2.4e-15`.

| Dimension | Minimum | Maximum |
| --- | --- | --- |
| 0 | numerical zero (`−1.5e-15` to `−6.7e-16`) | |
| 1 | 0.001845529907568047 (`ORB-0000-W07`) | 0.059365300578680294 (`ORB-0101-W01`) |
| 2 | 0.005059081105794422 (`ORB-0141-W09`) | 0.04781829997118239 (`ORB-0103-W00`) |

The largest information in the census belongs to a dimension-1 system, the complementary two-level law `dissolve(0-1) | absent(0-2-3) => strong_favour` with `dissolve(0-1) | present(0-2-3) => strong_suppress`. Its gate switches the action between `4/9` and `1/21`, the two strong laws, rather than between one strong law and uniform. More effective gate dimension does not mean more information.

Representative rows:

| System | Composition | Dim | Rows | Full CMI | I(G1) | I(G2) | I(G1 given G2) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ORB-0001-W00 | same action, two gates, 4 and 4 | 2 | 3 | 0.047818 | 0.022688 | 0.022688 | 0.025131 |
| ORB-0001-W01 | same action, two gates, 4 and 1/4 | 2 | 3 | 0.032099 | 0.015540 | 0.015540 | 0.016559 |
| ORB-0007-W00 | two actions, two gates, 4 and 4 | 2 | 4 | 0.044220 | 0.022064 | 0.022064 | 0.022155 |
| ORB-0007-W05 | two actions, two gates, 1/4 and 1/4 | 2 | 4 | 0.020159 | 0.010078 | 0.010078 | 0.010081 |
| ORB-0007-W01 | two actions, two gates, 4 and 1/4 | 2 | 4 | 0.032676 | 0.023721 | 0.008940 | 0.023735 |
| ORB-0028-W00 | switched, 4 and 4 | 2 | 2 | 0.046737 | 0.023368 | 0.023368 | 0.023368 |
| ORB-0005-W00 | two actions, one gate, same literal | 1 | 4 | 0.037527 | | | |
| ORB-0006-W00 | two actions, one gate, opposite literals | 1 | 3 | 0.050139 | | | |
| ORB-0026-W00 | gated toggle | 1 | 2 | 0.046737 | | | |
| ORB-0027-W00 | slot-gate XOR | 1 | 2 | 0.046737 | | | |
| ORB-0101-W01 | complementary two-level, 4 and 1/4 | 1 | 3 | 0.059365 | | | |

The gated toggle, the slot-gate XOR, and the switched dimension-2 system carry the same information, `JS(q_0, q_4) = 0.046736889544` nats, while needing one, two, and three coordinates. Information magnitude does not see the coordinate structure.

Four readings of the published table follow. None is a frozen estimand.

First, the balanced information is blind to placement, direction, and literal polarity. Grouping the 3584 systems by family, same or different triad, whether two literals on one triad are opposite, and the weight multiset gives 80 groups, and every group has a single information value at `1e-11`. The census has 3552 S4 local-law classes and 57 distinct information values. The balanced weighting is uniform on the 1024 states, and complementing any one bit or permuting vertices maps it to itself, so the information is invariant under all of those maps while the local-law class is invariant only under vertex permutations. The 8C equivalence of R01, R02, and R04 is the one-rule case of this invariance.

Second, the chain rule holds exactly. On all 2608 two-gate systems `I(G1, G2) = I(G1) + I(G2 | G1) = I(G2) + I(G1 | G2)` to `2.4e-15`, and the joint value equals the full-triad value. The two gate bits are independent given the pair mask under the balanced weighting, so `I(G1 | G2) − I(G1) = I(G1 ; G2 | slot, mask) ≥ 0`. A gate never carries less information once the other gate is known. Equality holds on exactly the 256 switched systems, where the slot never couples the two gates. This difference is a property of the balanced weighting. It is not used as a universal score.

Third, the opposite-direction family is exactly additive in information. On all 384 systems the full value equals the sum of the two single-rule values, because the two rules act on disjoint halves of the pair masks.

Fourth, adding a rule can lower information. In 64 systems the two-rule value is below the larger single-rule value: the 16 complementary eliminations, which carry none, 16 complementary two-level laws whose two unequal grades lie on the same side of 1 (for example `1/4` and `1/2`), and 32 same-action two-gate systems of the same kind, two unequal grades on the same side of 1. More gates do not imply more information.

## S. Gate ablations

Each system was compared with rule 1 only, rule 2 only, and neither: 14,336 ablation rows. No ablation leaves the law unchanged. The smallest maximum probability gap of any ablation is `5/66 = 0.0758`, the weak-suppress displacement `1/6 − 1/11`. No rule is redundant in any system. Every rule is active on a proper subset of the states.

In the 16 complementary eliminations both gates are masked by equal weights: the triad bit disappears from the law. Each rule is still necessary, because each covers the half of the admissible states where its own literal is true. A masked gate is not a redundant rule.

This is within-model functional analysis. It does not infer design purpose.

## T. Structural orbit versus local-law equivalence

The 3584 weighted systems have 3560 distinct labelled weight tables and 3552 S4 local-law classes. The coincidences are the eight complementary eliminations whose face and non-face orbits share a law, and the reciprocal same-action twins of section K. No other two orbits share a law.

A local-law class here is a class of full ten-slot weight tables. Two systems in one class have S4-conjugate full-event kernels. Their global dynamics, including stationary distributions and graph-class projections, agree up to relabelling. That follows from D0 without a further computation.

Three equivalences are now in the record, from finest to coarsest: equal labelled kernel, S4-conjugate kernel, and equal balanced information. The census separates them sharply. 3552 kernel classes collapse to 57 information values. The 8C caveat holds at the coarse level. Systems with equal balanced information, such as R01, R02, and R04, can still differ from a labelled source, because an action can be admissible on one source and not on another. At the S4-conjugate level the only difference is a relabelling of the source.

## U. Observations

96 labelled one-gate rules, 4560 unordered pairs, 236 S4 orbits, 3584 weighted canonical systems. All 237 items completed. Validation ok. Kernel gap 0. Log-weight residual at most `2.22e-16`.

Effective gate dimension: 16 at 0, 960 at 1, 2608 at 2. Of the 2608, 256 never activate both rules in one state. Reducibility: R0 0, R1U 16, R1G 0, R1T 48, R2S 912, R2G 2608.

The 16 equal-weight complementary systems equal their unconditional comparators on all 1024 states. The 16 equal-weight same-literal opposite-direction systems read only the gate. The 16 equal-weight opposite-literal opposite-direction systems read `slot XOR gate`.

`Δ12 L = 0` on all 272 same-action two-gate systems. Both-active normalisation matches `m1*m2/(m1*m2+5)` and `m/(m1+m2+4)` on every realised state, gap 0. Three rows appear on one slot exactly when `m1 = m2` or `m1*m2 = 1`.

24 labelled-law and 32 S4-law coincidences across orbits, all complementary eliminations or reciprocal same-action twins.

Balanced information ranges: dimension 1 from 0.001846 to 0.059365, dimension 2 from 0.005059 to 0.047818 nats. 57 distinct values. Information is constant on 80 placement-, direction-, and polarity-blind groups. The chain rule holds to `2.4e-15`. Conditional gate information is never below marginal, equal on 256 systems. The opposite-direction family is exactly additive. 64 systems have two-rule information below the larger single rule.

No rule is redundant. Smallest ablation gap `5/66`.

One-gate weak-grade surface, enumerated and analytic: balanced information 0.003238674092597 nats at `m = 1/2` and 0.005108359895797 nats at `m = 2`. Balanced dissolve drift `5(1−m)/(24(m+5))`: `5/264` at `1/2`, `−5/168` at `2`. The unconditional drift is twice the conditional drift at the checked grade.

## V. Inferences

The current DSL composes constraints as additive features in event-logit space. Each primitive feature is the conjunction of an admissibility literal and one gate literal. A system's local law is the softmax of the sum of its active features. Within this grammar, that sentence is exact.

Two primitive one-gate rules cannot create a gate-by-gate logit coefficient. The most two gates can do on one slot is an affine function of two literals. XOR of two gates, and any independent tuning of the both-active state, need a grammar in which one constraint can modulate another.

What cardinality two adds over one gate is: two-bit dependence through additive levels (`1, m1, m2, m1*m2`); multi-slot bias under one gate with a shared denominator; gate partitions, where one bit selects which slot or which multiplier is active; switched reading, where the pair mask selects which gate is read; and slot-gate XOR. Each is built from the same two operations, log-weight addition and normalisation.

Higher-order syntax can be dynamically redundant. When complementary conditions assign the same weight, the condition vanishes from the full kernel. When opposite directions on one literal assign the same weight, the slot's own state vanishes. When reciprocal weights sit on flipped literals, two different texts are one kernel. The law determines the affine logit, not the literals that wrote it.

Probability-space coupling is a denominator fact. Different-action gates add their logits independently, and each slot's probability depends on the other's weight only through `m1 + m2 + 4`. That is a normalisation interaction, not a new interaction term in the rule algebra.

Information is a coarse reading of the grammar. It is blind to everything a vertex permutation or a bit complement changes, which includes exactly the placement that 8C showed topology converts into shape. It does not rank effective dimension, reducibility, or structural role. The largest value in the census is one-dimensional, and some three-coordinate laws carry exactly the information of a one-coordinate law.

The local equivalences in D0 are kernel conjugacies. They need no global round to transfer to global dynamics. The global questions that remain are of a different kind: how occupancy and topology weight the distinct, non-equivalent laws.

## W. RS / global-coherence interpretation

Inside this model, a small multiplicative constraint grammar composes additively in event-logit space. Visible dynamics come from normalisation, from occupancy, and from how topology places the reweighted slots. Two higher-order constraints can express a genuinely two-dimensional relational dependence that no single constraint expresses. They cannot express a relation between the two conditions themselves. That is the exact sense in which the cardinality-two grammar is compositional and also bounded.

The collapses are part of the picture. Contextual syntax can be dynamically empty, and different syntax can be one dynamics. A coherence account built on this grammar should therefore attach meaning to the law, the affine logit and its placement, and not to the rule text.

Nothing here shows that a physical or biological system uses this DSL, or that relations in nature compose by adding log weights. Nothing here infers a designer. The analogy to a formal language is an analogy: literal gates, action slots, and log-weight tokens combine by addition into a sentence whose meaning is an event distribution. The grammar is the experimenter's.

The ledger keeps the dimensions apart. The two-gate information is small and exact. Effective gate dimension is an exact structural descriptor. Reducibility is a local-law fact, not a global one. The negative results, no gate-by-gate coefficient, no two-gate XOR, no redundant rule, are boundaries of the grammar, and they are recorded as findings.

## X. D1 candidate global follow-ups

D1 is not opened. D0 already yields a closed local grammar, and its equivalences are kernel conjugacies that transfer to global dynamics without computation. The follow-ups below are recorded for a later prompt. The coordinates are contextual novelty, routing diversity, recurrence, explanatory compression, coherence relevance, and computational boundedness, ordinals from 0 to 5, not summed.

A. Stationary persistence of a joint two-gate law: exact stationary distribution and stationary current-context CMI of a jointly activated R2G system, such as `ORB-0103-W00`, against its two single-rule ablations. Attention: CN 3, RD 3, RC 3, EC 4, CG 4, CB 4.

B. Switched versus joint dimension two: `ORB-0028-W00` against a jointly activated R2G system with the same balanced information. Attention: CN 4, RD 2, RC 2, EC 4, CG 3, CB 5.

C. Gated-toggle dynamics: `ORB-0026-W00` reads no edge state on its slot. Its toggle weight is the same in both directions, so the jump chain may have a closed-form stationary law. Attention: CN 4, RD 3, RC 4, EC 4, CG 3, CB 5.

D. Slot-gate XOR topology response: checkpoint-1 class and edge-count information of `ORB-0027-W00` from star, path, and triangle sources. Attention: CN 4, RD 4, RC 2, EC 3, CG 3, CB 4.

E. The census maximum under stationary weighting: does the complementary two-level law `ORB-0101-W01` keep its local information lead once occupancy weights the masks? Attention: CN 2, RD 2, RC 2, EC 3, CG 3, CB 5.

F. Reciprocal twins: a direct global confirmation that the S4-conjugate twins have identical stationary graph-class masses. D0 already implies the answer. Attention: CN 1, RD 1, RC 1, EC 2, CG 2, CB 5.

G. Meta-constraints, `L > 0`: the smallest grammar in which one constraint modulates another, and so the first place a gate-by-gate logit coefficient or a two-gate XOR could appear. Not a D1 item. Attention: CN 5, RD 3, RC 2, EC 4, CG 5, CB 2.

## Y. Coherence-map update

The ledger is `constraint-lab/coherence/findings.jsonl` and `constraint-lab/coherence/relations.jsonl`. The generated views are `current-map.md` and `current-map.mmd`. The snapshot is `constraint-lab/coherence/snapshots/through-generation-008d.md`. Its sha256 and the canonical ledger sha256 are recorded in the Prompt 008D execution record.

Earlier in this generation: `F8D-CORRECT-GRADE-ASYMMETRY` corrects `F8C-GRADE-ASYMMETRY`, and `F8D-DRIFT-MAGNITUDE-SCOPE` qualifies `F8C-DRIFT-DIRECTION`. Both older nodes are `qualified` with their statements unchanged.

New D0 findings: `F8D-LOG-ADDITIVITY`, `F8D-NORMALISATION-INTERACTION`, `F8D-COMPLEMENTARY-ELIMINATION`, `F8D-DIRECTION-ELIMINATION`, `F8D-NO-GATE-PRODUCT`, `F8D-RECIPROCAL-TWINS`, `F8D-GATE-DIMENSION`, `F8D-SWITCHED-DIMENSION`, `F8D-SLOT-GATE-XOR`, `F8D-NO-REDUNDANT-RULE`, `F8D-INFORMATION-BLINDNESS`, `F8D-INFORMATION-NOT-DIMENSION`, `F8D-WEAK-GRADE-SURFACE`, the inferences `F8D-ADDITIVE-FEATURE-GRAMMAR` and `F8D-SYNTAX-CAN-VANISH`, and the interpretation `F8D-RS-COMPOSITIONAL-BOUND`.

`Q-GATE-COMPOSITION` and `Q-WEAK-GRADE` are marked `qualified`, with their statements left as published, and linked by `partially_answered_by` to the findings that answer them. `Q-WEAK-GRADE` keeps the part D0 did not compute: the stationary and global behaviour across the grade surface. `Q-GATE-COMPOSITION` keeps the global side of composition. The new open question `Q-META-CONSTRAINT` asks what a constraint that modulates another constraint can express. `Q-H-POSITIVE`, `Q-SCALE-N`, and `Q-THREE-EDGE-LAYER` stay unresolved.

The main new edges run from complementary elimination to the Generation 7B two-level collapse, from the normalisation interaction to the R05 denominator, from information blindness to the 8C local equivalence, which it generalises, and from the gate-product bound to the meta-constraint question.
