# Generation 008E — conjunctive gate grammar

Generation 8E is Mode B. It reads the exact local law of every single K=3 rule with one pair action and two distinct triad literals. It runs no stochastic trajectory, no stationary census, no parameter fit and no new control. Pass and fail in this note are reserved for tests, chronology, numerical tolerances and CI.

The numerical record is `constraint-lab/reports/generation-008e-round-e0-tables.json`. Schema `rs-constraint-lab.conjunction-tables/v1`. File sha256 `499addff9a7a47fc10a29d13b8b384e02dfc0df3c9a7d67fa285bda6246c4c33`. Payload sha256 `231b4a1b6413d4f332272e161802265cbf115f224d11c2da1d3d6838ecb65b46`. The column tables are `constraint-lab/reports/tables/generation-008e-*`, and each table's canonical sha256 is in `detail_sha256`. The result commit is `2daf1ce3f54f8bacbc331b6bc575b44ed3f20c27`. Information is in nats.

The compression this round supports is short. Within this DSL, one ordinary rule's literals are conjoined, so a rule that reads r triad literals contributes one log weight times the product of their truth values. Over two gate bits, a single K=3 rule therefore carries a gate×gate term that no number of one-literal K=2 rules can produce. Rule cardinality adds such terms; expression complexity raises their order. With continuous weights, the four features `1, G1, G2, G1G2` (one K=1, two K=2 and one K=3 rule) span every four-corner action-logit table, and so do the four K=3 corner rules. The finite W4 alphabet reaches different, overlapping parts of that space through the two bases.

## A. External Review 008D

Review 008D is `constraint-lab/provenance/reviews/008D-chatgpt-review-v0.8d.md`. It reads `research/constraint-lab-v0.8d-two-gate-composition` at `50e3f4dfeac19d8e075964c51560d4d3f08b85c8`, 14 commits ahead of 8C.

- **Frozen D0 plan:** `ac037f32df81271e04381c79efebf6f5b3d0b607`, plan hash `10a3114bcf7a1a914e9eff19e08f77a9fbcf71852bc4a22f14f04d723912ce07`.
- **Pre-result head:** `d3bf0f7`, with Actions run `38375394924`.
- **Tables:** `093e460`. **Report:** `7dc3883`. **Snapshot:** `36cb89c`.
- **Close-out:** `50e3f4d`, with Actions run `38392825068` successful. 227 tests passed at the snapshot head.

The review records repository-state continuity across the Grok-to-Opus continuation at `093e460` as established, and second-session prompt byte identity as not established. It treats the post-freeze validator correction `cbfdae8` as a change to validation only, with the frozen plan intact. It preserves:

- the D0 composition result: additive log-weight features, a weight gap of 0, and a residual of 2.22e-16;
- the exact collapses: complementary-gate elimination, direction elimination, and reciprocal literal-flip twins;
- the effective-dimension split 16 / 960 / 2608, with 256 switched systems;
- the conclusion that information does not rank dimension.

It asks for a scope correction to the no-gate-product result.

The authored Prompt 008D metadata (35,541 bytes, sha256 `de835332…7844`) is recorded beside the stored agent input (35,550 bytes, sha256 `73a830ba…e1`) and is not assigned to it. Prompt 008E is stored at `constraint-lab/provenance/prompts/008E-v0.8e-agent-input.md`, 44,734 bytes, sha256 `ce1efd0a…f6a2`. It is the implementing agent's transcription of the session input, not a byte capture, so its byte identity with the authored prompt is not established.

## B. 8D scope erratum

`constraint-lab/reports/generation-008d-errata.md` records two corrections. The 8D report is not edited.

1. The zero gate×gate coefficient is a property of the 8D subgrammar, two K=2 rules each with one triad literal. It is not a bound on the ordinary language. The 8D statements that relating two conditions needs a meta-constraint, and that `L > 0` would be the first place a gate×gate coefficient could appear, are withdrawn.
2. The opening compression "everything else is genuinely two-gate" is narrowed. 2,608 of the 3,584 weighted systems need two triad bits locally, 960 need one, and 16 need none.

In the ledger, `F8E-K2-SCOPE-CORRECTION` qualifies `F8D-NO-GATE-PRODUCT`, `F8D-ADDITIVE-FEATURE-GRAMMAR`, `F8D-RS-COMPOSITIONAL-BOUND` and `Q-META-CONSTRAINT`, and raises `Q-K3-CONJUNCTION`. The first three are now `qualified`, with statements unchanged. `Q-META-CONSTRAINT` stays `unresolved`.

## C. Why K before L

The ordinary `Constraint` grammar already lets one rule read several conditions conjunctively. Before the ontology is changed, by meta-constraints (`L > 0`) or by history (`H > 0`), it is worth knowing what the existing grammar can say. The axes stay apart:

- **relation order O** says which relations exist;
- **expression complexity K** says how many conditions one rule reads jointly;
- **rule cardinality** says how many rules are present;
- **H** says whether prior states are read;
- **L** says whether a rule can act on a rule.

Generation 8D held K at 2 and raised cardinality to 2. Generation 8E holds cardinality at 1 and raises K to 3.

## D. Frozen E0 plan

- **Plan commit:** `5303388815a3695ac6bf4eb4176c0102b9ca460c`, plan hash `ec515306c2d3fa669f15ce31a86cdaac78f5fcab0d01ea7ad82533fde71c9be6`. File `constraint-lab/exploration/generation-008e/round-e0-plan.json`, sha256 `f07b6153…7990`. Committed and pushed before execution.
- **Journey:** step 1 (`b2811bd`) has `result_commit` null. Step 2 names `2daf1ce`, which descends from the plan.
- **Frozen census:** 288 labelled rules, 20 structural orbits, 80 W4 weighted systems, 27 items (20 orbit items and 7 algebra items).
- **Work count:** 81,920 full-state evaluations, the same number of kernel-agreement evaluations, 1,920 S4 law images, and 160 comparison fingerprints against 8D.
- **Tolerances:** exact for canonicalisation and rational laws; `1e-12` for probability, CMI, the interaction coefficient, 8D law equality and basis reconstruction.

Before the freeze, orbit K3-00 was analysed as a smoke test of the implementation, and the unit tests analysed K3-00 and K3-03 and ran the algebra items. The plan records that those values were seen.

**Execution:**
- All 27 items ran, none skipped.
- The largest item wall was 3.44 seconds, against the 120-second watchdog.
- One worker, no supervisor.
- `verify` returned complete, and assembly validation was ok with no problems.

## E. K3 labelled rule universe

A primary rule has a pair action (6 slots × form or dissolve), two distinct triad slots (C(4,2) = 6 pairs) and an independent literal on each (4 choices). The enumeration produces 6 × 2 × 6 × 4 = 288 rules. Each was checked against the required shape rather than accepted from the expected count:

- two conditions;
- no count predicate;
- a pair action;
- both conditions on triad slots;
- distinct triads;
- conditions in canonical order;
- `k() = 3`.

The order-3 parser semantics were read directly. `dissolve(0-1) | present(0-1-3) & present(0-1-2) => strong_favour` parses to two sorted conditions with no counts and `k() = 3`. The parser rejects a repeated literal, a condition on the action slot, and a count predicate. One behaviour is worth recording: it accepts the two opposite literals of one triad (`present(0-1-2) & absent(0-1-2)`). That rule never matches any of the 1,024 states, and the census requires distinct triads.

## F. S4 structural atlas

The 288 rules fall into 20 S4 orbits, 10 for each action direction. At N=4, two distinct triads share exactly one pair, so the action has one of three incidences:

| Incidence | Action is the shared pair | Same literals (pp, aa) | Mixed literals | Orbit sizes |
| --- | --- | --- | --- | --- |
| face of both triads | yes | 2 orbits per direction | 1 orbit per direction | 6, 6, 12 |
| face of exactly one triad | no | 2 orbits per direction | 2 orbits per direction (face present / face absent) | 24 each |
| face of neither triad | no (it is the complementary pair) | 2 orbits per direction | 1 orbit per direction | 6, 6, 12 |

When the action is a face of exactly one triad, a mixed-literal rule has two inequivalent forms, because the face triad's literal can be present or absent. With both and with neither, the two triads are exchanged by a vertex permutation that fixes the action. Canonicalisation, not the descriptors, decided the count. The descriptors turned out to classify the orbits exactly.

Each orbit at each W4 grade is one weighted system, giving 80 in total.

## G. One-rule conjunctive local law

On every one of the 80 systems the kernel weights equal the product formula on all 1,024 states, with gap 0. In literal coordinates, with U the truth of the written literal:

```text
U1 U2   action multiplier
0  0    1
0  1    1
1  0    1
1  1    m
```

and the action log multiplier is `L(U1, U2) = ln(m) U1 U2`. There are exactly two six-slot law rows: uniform, and `m/(m+5)` on the action with `1/(m+5)` elsewhere. The active row occupies 128 of the 1,024 states, half for admissibility times a quarter for both literals true. That count was measured, not assumed.

## H. First non-zero gate×gate coefficient

In literal coordinates, `Δ12 L = L11 − L10 − L01 + L00 = ln(m)`, with gap 0 on all 80 systems. Every W4 grade is non-neutral, so `Δ12 L ≠ 0` throughout. Side by side with 8D:

```text
two K=2 one-literal rules on one action:  Δ12 L = 0      (272 of 272 systems, Generation 8D)
one K=3 two-literal rule:                 Δ12 L = ln(m)  (80 of 80 systems, Generation 8E)
```

The gate interaction order, defined as the highest non-zero discrete-derivative order of the action log multiplier over the gate variables, is 2 on every system.

## I. Literal versus raw-bit interaction sign

Write `U_i = G_i` for a present literal and `U_i = 1 − G_i` for an absent one, so `U_i = (1 − s_i)/2 + s_i G_i` with `s_i = +1` or `−1`. Then

```text
ln(m) U1 U2 = ln(m) [ (1 − s1)/2 + s1 G1 ] [ (1 − s2)/2 + s2 G2 ]
```

and the coefficient of `G1 G2` is `ln(m) s1 s2`. So the raw second difference is `+ln(m)` when the two literals have the same polarity, both present or both absent, and `−ln(m)` when they are mixed. All 80 systems match, with gap 0. The magnitude is fixed by the rule's weight. The sign is fixed by the coordinate system, because flipping a literal is a reflection of one gate axis, which reverses the sign of a mixed second difference and leaves its size alone. The interaction belongs to the rule. Its sign belongs to how the gates are written.

## J. Minimal coordinates and effective gate dimension

Every subset of the three candidate raw bits (the action pair bit and the two triad bits) was searched on all 1,024 states. All 80 systems need all three, so the minimal coordinate count is 3, with one minimal set. Effective gate dimension, as defined in 8D, is 2 on all 80. No structural placement collapses a coordinate.

Two effective gates and only two law rows coexist here. The second gate does not add a law row. It narrows where the single non-uniform row applies.

## K. Analytic balanced information

Under balanced full-state weighting, the action is admissible on half the pair masks. On an admissible mask the conjunction is true on a quarter of triad states, giving `q_m`, and false on three quarters, giving the uniform law `q_0`. So

```text
I_K3(m) = (1/2) [ H( (1/4) q_m + (3/4) q_0 ) − (1/4) H(q_m) − (3/4) H(q_0) ]
        = (1/2) JS_(1/4, 3/4)(q_m, q_0)
```

| Grade | m | Enumerated | Analytic | Review prediction | Gap to prediction | K2 one-gate value | K3 / K2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| strong_suppress | 1/4 | 0.006761384413736 | 0.006761384413735860 | 0.006761384413735834 | 2.6e-17 | 0.009748566529643857 | 0.694 |
| weak_suppress | 1/2 | 0.002333270369316 | 0.002333270369315632 | 0.002333270369315642 | 1.0e-17 | 0.003238674092597321 | 0.720 |
| weak_favour | 2 | 0.003961514536996 | 0.003961514536995558 | 0.003961514536995468 | 9.0e-17 | 0.005108359895797386 | 0.775 |
| strong_favour | 4 | 0.018447186631126 | 0.018447186631125990 | 0.018447186631125900 | 9.0e-17 | 0.023368444772049440 | 0.789 |

The enumerated and analytic values agree to at most `1.5e-15` on every system. The review's external predictions are confirmed. At every multiplier the K3 conjunction carries less balanced information than a one-gate K2 rule, because it is active on half as many states. Higher interaction order with smaller information magnitude is another instance of magnitude not tracking structure.

## L. Analytic edge-count drift

The rule-induced balanced drift was enumerated exactly over all 1,024 states and matches

```text
dissolution:  5(1 − m) / [48(m + 5)]
formation:    5(m − 1) / [48(m + 5)]
```

on every system as exact fractions. The dissolution values are `+5/336` at m = 1/4, `+5/528` at 1/2, `−5/336` at 2, and `−5/144` at 4.

The K3 drift is exactly half the K2 one-gate drift at every grade, while the information ratio is 0.69 to 0.79. That is the distinction recorded in the 8C erratum, between linear probability displacement and nonlinear information, appearing again. Stationary occupancy is not inferred from drift.

## M. K2 additive versus K3 conjunctive non-representability

**Symbolic.** Over the four literal corners, ordered (0,0), (1,0), (0,1), (1,1):

- the one-literal additive features `1, U1, U2` have rank 3 by exact rational elimination;
- adding `U1 U2` raises the rank to 4;
- without the constant, `U1, U2` have rank 2, and adding `U1 U2` raises it to 3.

So `c U1 U2 = c0 + a U1 + b U2` on all four corners forces `c = 0`, for every real `c, a, b, c0`. Directly: corner (1,0) gives `a = 0` and corner (0,1) gives `b = 0`, using (0,0) to fix `c0 = 0`. Corner (1,1) then gives `c = 0`. Every additive feature has `Δ12 = 0`, and the conjunction has `Δ12 = 1`.

**Scope.** The statement covers any number of same-action one-literal features with arbitrary real coefficients, with or without an unconditional term. It is not a statement that K3 "cannot be represented by lower K" in every sense. It concerns one-literal same-action features. Any comparison grammar that admits a product term reproduces the conjunction trivially.

## N. Exact comparison against Generation 8D laws

The committed 8D weighted-system table was loaded and its canonical hash checked (`e5acbf8b…8e07`). For every one of the 80 K3 systems, the labelled full-event weight-table hash and the S4 minimum hash were looked up among all 3,584 8D systems:

- labelled matches: 0;
- S4 matches: 0;
- matches against the 433 empty, unconditional and one-gate one-rule laws: 0.

The 80 K3 systems are 80 distinct labelled laws and 80 distinct S4 classes. The finite search agrees with the symbolic argument, and the symbolic argument is the proof.

## O. Expression-complexity ladder

On one action over two gate bits, the ordinary grammar supplies:

```text
K=1   unconditional rule            feature 1
K=2   one triad literal             features G1, G2  (or 1 − G1, 1 − G2)
K=3   two triad literals            feature G1 G2, or any one corner
```

A targeted check (not a census) on one placement extends this to r = 1, 2, 3, 4 literals, K = 2 to 5. For every literal pattern, the top Möbius coefficient of the action log multiplier over the r raw gate bits is `ln(4) Π s_i` for `strong_favour`. The general statement follows from the DSL's matching rule, which conjoins its literals. For r literals the feature is `admissible × Π U_i`, its order-r coefficient in raw bits is `ln(m) Π s_i ≠ 0`, and every lower coefficient is fixed by the same product. So within this DSL a rule that reads r triad literals has gate interaction order exactly r. A blind K=4 census is unnecessary for the local question.

## P. Boolean / Möbius logit basis

For any four-corner action-logit table in raw bits:

```text
c = L00
a = L10 − L00
b = L01 − L00
d = L11 − L10 − L01 + L00
L(G1, G2) = c + a G1 + b G2 + d G1 G2
```

This is the unique representation. It was verified, with exact rational reconstruction gap 0, on five tables: the conjunction, XOR, XNOR, an additive table and a generic one. The interaction coefficient `d` is exactly the second discrete difference. In these coordinates, the 8D K2-only grammar is the subspace `d = 0`, and one K3 rule supplies `d ≠ 0`.

All four basis features are executable ordinary rules: `A => m`, `A | present(T1) => m`, `A | present(T2) => m` and `A | present(T1) & present(T2) => m`. With continuous positive multipliers, `ln m` is any real number, so these four rules represent every four-corner table.

## Q. Corner-literal basis

A K3 rule selects one raw gate corner. As raw polynomials, in the order (1, G1, G2, G1G2):

```text
[G1=0, G2=0] = 1 − G1 − G2 + G1G2    (1, −1, −1,  1)
[G1=1, G2=0] =      G1      − G1G2   (0,  1,  0, −1)
[G1=0, G2=1] =           G2 − G1G2   (0,  0,  1, −1)
[G1=1, G2=1] =                G1G2   (0,  0,  0,  1)
```

The matrix has determinant 1, so the corner indicators are a second basis of the same four-dimensional space. In it, a table's coefficients are simply its four corner values, and the change of basis to Möbius coefficients is the formula in §P.

**Grammar basis versus finite alphabet.** With at most one W4 rule per basis element (no rule, or one of four grades), each basis reaches 625 distinct four-corner tables:

- In log2 units, the corner basis reaches every table whose corners lie in {0, ±1, ±2}.
- The polynomial basis reaches corners up to ±8 in log2.
- The two sets share 279 tables, and each reaches 346 that the other does not.

Algebraic completeness holds for both bases. Finite-alphabet coverage differs between them, and neither contains the other.

## R. XOR and XNOR constructions

These are targeted constructions on one placement, the action `0-1` with gates `0-1-2` and `0-1-3`, at every W4 grade and in both directions. They are not a K3-pair census.

- `A | G1 & NOT G2 => m` with `A | NOT G1 & G2 => m` gives multiplier 1 at (0,0) and (1,1), and `m` at (0,1) and (1,0): an exact XOR-gated action. In raw Möbius coefficients this is `a = b = ln m`, `d = −2 ln m`.
- `A | G1 & G2 => m` with `A | NOT G1 & NOT G2 => m` gives `m` at the equal corners and 1 at the mixed ones: XNOR. Here `c = ln m`, `a = b = −ln m`, `d = 2 ln m`.

Both match on all 1,024 states with kernel gap 0, and no other gate state receives the multiplier. Generation 8D found that two K2 rules cannot isolate XOR. Two K3 rules do.

Four mutually exclusive K3 corner rules assign four independent multipliers. With `strong_suppress`, `weak_suppress`, `weak_favour` and `strong_favour` on corners 00, 01, 10 and 11, the measured gate table is 1/4, 1/2, 2, 4, exact, because exactly one corner rule matches any gate state. With continuous weights, any four positive multipliers are reachable this way. Under W4 each corner is limited to {1, 1/4, 1/2, 2, 4}.

The Boolean structure is in the gate-selection feature: which gate states apply a multiplier to one action slot. The six-slot event law is still a normalised weight, and the transition function as a whole is not Boolean.

## S. Rule cardinality versus expression complexity

| System | Rule cardinality | Max per-rule K | Effective gate dimension | Gate interaction order | Distinct law rows |
| --- | --- | --- | --- | --- | --- |
| two K2 rules, one action, two gates (8D, e.g. ORB-0001-W00) | 2 | 2 | 2 | 1 | 3–4 |
| one K3 conjunction (8E, any system) | 1 | 3 | 2 | 2 | 2 |
| two K3 rules, XOR or XNOR (8E construction) | 2 | 3 | 2 | 2 | 2 |
| four K3 corner rules (8E construction, W4 grades 1/4, 1/2, 2, 4) | 4 | 3 | 2 | 1 | 5 |

The vector is not summed. Cardinality and K move independently. The last row is worth noticing. The measured four-corner assignment has log2 corner values −2, −1, +1, +2 at 00, 01, 10, 11. That is `−2 + 3 G1 + G2` with `d = 0`, so four K3 rules wrote a law with no gate×gate term at all. Syntactic K bounds the interaction order. It does not fix it, and the coefficients decide. Two K2 rules raise cardinality without raising the interaction order. One K3 rule raises the order at cardinality 1. The two-gate XOR needs both.

## T. What balanced information can and cannot see

Grouping the 80 systems by grade, literal-polarity relation and incidence class gives 24 groups, and each group has one information value. Further, only 4 distinct values occur in the census, one per grade. Action direction, literal polarity, incidence and placement are all invisible to balanced information, exactly as for one gate in 8C and for two gates in 8D. The balanced measure is uniform on the 1,024 states, and complementing a bit or permuting vertices preserves it.

The local law is not placement-blind: the 80 systems are 80 distinct S4 classes. A labelled source graph will also respond differently according to where the action sits (Generation 8C). No trajectory atlas is run here.

## U. Observations

- 288 labelled K3 rules; 20 S4 orbits; 80 weighted systems. All 27 items ran, validation was ok, and the kernel gap is 0.
- On all 80 systems: 3 minimal coordinates, effective gate dimension 2, gate interaction order 2, 2 law rows, and 128 active states.
- Literal `Δ12 L = ln m`. Raw `Δ12 L = +ln m` for same-polarity literals and `−ln m` for mixed, with gap 0.
- Balanced information equals `(1/2) JS_(1/4,3/4)(q_m, q_0)` to at most 1.5e-15. It matches the review predictions to at most 9e-17, and takes one value per grade.
- Balanced drift equals `±5(1 − m)/[48(m + 5)]` exactly. It is half the K2 drift, while the information is 0.69 to 0.79 of the K2 value.
- No K3 law matches any 8D law or one-rule law, labelled or S4. The 80 laws are pairwise distinct.
- The additive one-literal span has rank 3 over four corners, and adding the conjunction makes it rank 4.
- The corner and Möbius bases are related by a determinant-1 matrix. Under W4 each reaches 625 tables, and they share 279.
- Two K3 rules realise exact XOR and XNOR, and four realise any W4 corner assignment. The measured four-corner assignment happens to be additive (`d = 0`).
- The top Möbius coefficient of an r-literal rule is `ln(4) Π s_i` for r = 1 to 4.

## V. Inferences

Within this DSL, expression complexity and rule cardinality are different operations on the event logit. A rule contributes one log weight times the product of its literal truths, so a rule reading r literals adds a term of interaction order r. Adding rules sums such terms. K therefore supplies gate×gate interaction that increasing the cardinality of K2 rules cannot.

The ordinary grammar is already hierarchically complete over two gates when weights are continuous: `K ≤ 3` rules, through either basis, express every four-corner action-logit table, including XOR and the independent tuning of the both-active state that 8D could not reach. What 8D found was the boundary of a subgrammar.

Meta-constraints are therefore not needed for a gate×gate term, or for two-gate XOR. If they add expressivity, it must be something no fixed set of higher-K ordinary rules reproduces: for example, one relation changing another rule's coefficient, existence, polarity or structure. That question stays open.

The finite alphabet is a separate constraint. Basis completeness is algebraic. What W4 can actually execute depends on the basis used, and the two bases cover different tables.

## W. RS / global-coherence interpretation

Inside this model, a small constraint grammar has an ordinary compositional hierarchy. Increasing expression complexity introduces progressively higher-order relational features in the event logit, and rule cardinality composes the features available at each level additively. Visible dynamics still come from normalisation, occupancy and topology.

For the broader account, this keeps three ideas apart that are easily run together: that a higher-order relation exists (O), that one constraint reads several relations jointly (K), and that several constraints coexist (cardinality). A higher-order effect in a description is not, by itself, evidence for any one of them.

None of this shows that nature uses Boolean polynomials, that physical law is a softmax, that higher K is more fundamental, or that a Designer is established. It is a statement about this DSL.

## X. E1 decision and candidate directions

E1 is not opened. E0 settles the local question, and the r-literal monomial law makes an exhaustive K=4 census unnecessary. Candidates are recorded with non-summed attention vectors (CN contextual novelty, RD routing diversity, RC recurrence, EC explanatory compression, CG coherence relevance, CB computational boundedness):

| Candidate | CN | RD | RC | EC | CG | CB |
| --- | --- | --- | --- | --- | --- | --- |
| A. path/star/triangle response of a K3 conjunction against a matched two-K2 additive comparator | 3 | 4 | 2 | 3 | 3 | 4 |
| B. stationary current-context information of one conjunction | 2 | 2 | 2 | 3 | 3 | 5 |
| C. exact forgetting curve of an initial two-bit conjunction state | 3 | 2 | 3 | 3 | 3 | 4 |
| D. XOR-gated action on the canonical sources | 3 | 4 | 2 | 3 | 3 | 4 |
| E. K=4 census (now reduced to the proved monomial law) | 1 | 1 | 1 | 1 | 2 | 4 |
| F. H>0, after the K ladder | 5 | 3 | 4 | 3 | 5 | 2 |
| G. L>0, asked for expressivity beyond fixed higher-K ordinary rule sets | 5 | 3 | 2 | 4 | 5 | 2 |

## Y. Coherence-map update

The ledger is `constraint-lab/coherence/findings.jsonl` and `constraint-lab/coherence/relations.jsonl`. The snapshot is `constraint-lab/coherence/snapshots/through-generation-008e.md`. Its sha256 and the canonical ledger sha256 are recorded in Execution 008E.

The scope correction recorded earlier in this generation is `F8E-K2-SCOPE-CORRECTION`, with `Q-K3-CONJUNCTION`.

New E0 findings:
- `F8E-K3-CONJUNCTION-INTERACTION`
- `F8E-RAW-SIGN`
- `F8E-K2-K3-NONREPRESENTABILITY`
- `F8E-NO-8D-MATCH`
- `F8E-K3-INFORMATION-SURFACE`
- `F8E-K3-DRIFT-SURFACE`
- `F8E-BOOLEAN-LOGIT-BASIS`
- `F8E-CORNER-BASIS`
- `F8E-W4-COVERAGE`
- `F8E-XOR-XNOR-FROM-K3`
- `F8E-GENERAL-K-INTERACTION`
- `F8E-PARSER-SAME-TRIAD`
- the inferences `F8E-CARDINALITY-VS-K` and `F8E-ORDINARY-K-SUPPLIES-INTERACTION`
- the interpretation `F8E-RS-COMPOSITIONAL-HIERARCHY`

`Q-K3-CONJUNCTION` is `qualified` and partially answered. `Q-META-CONSTRAINT` stays `unresolved`, now sharpened by `F8E-ORDINARY-K-SUPPLIES-INTERACTION` to expressivity beyond ordinary higher-K conjunctions. `Q-H-POSITIVE`, `Q-SCALE-N` and `Q-THREE-EDGE-LAYER` stay unresolved.
