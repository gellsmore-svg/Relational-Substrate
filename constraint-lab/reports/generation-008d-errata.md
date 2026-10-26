# Generation 008D errata

This file corrects the scope of several sentences in the Generation 8D report. It does not replace that report. The historical report, its tables and the historical coherence statements stay in place. No 8D number changes, and no recomputation is required.

## 1. The no-gate-product result is a property of the K=2 subgrammar

Generation 8D showed, correctly, that two primitive one-condition rules on one action cannot create an independent gate×gate coefficient in logit space. For two distinct gate literals:

```text
L(G1, G2) = c + λ1 l1(G1) + λ2 l2(G2)
L11 − L10 − L01 + L00 = 0
```

This holds on all 272 same-action two-gate systems of the D0 census.

Several sentences of the report broaden that result beyond what it establishes:

- the inference in §V that XOR of two gates, and any independent tuning of the both-active state, "need a grammar in which one constraint can modulate another";
- the interpretation in §W that two higher-order constraints "cannot express a relation between the two conditions themselves";
- candidate G in §X, which calls meta-constraints, `L > 0`, "the smallest grammar in which one constraint modulates another, and so the first place a gate-by-gate logit coefficient or a two-gate XOR could appear";
- the closing sentence of §Y, which describes an edge "from the gate-product bound to the meta-constraint question".

**Correction.** The zero gate×gate logit coefficient is a property of the Generation 8D subgrammar: two primitive K=2 rules, each with one triad literal. It is not a bound on the full ordinary constraint language. In the order-3 independent hypergraph, `Constraint.k() = 1 + len(conditions) + len(counts)`, and the parser accepts several conditions joined by `&`. A K=3 rule with two conjunctive triad literals, such as `dissolve(0-1) | present(0-1-2) & present(0-1-3) => strong_favour`, is already executable in the existing DSL. It may introduce a genuine second-order gate interaction without `L > 0`. Generation 8E examines it.

## 2. The opening compression overstates "genuinely two-gate"

The report's opening paragraph ends: "Everything else is genuinely two-gate at the local law."

**Correction.** Beyond the exact eliminations, the syntax partitions into zero-, one- and two-effective-gate laws. The census gives 16 weighted canonical systems at effective gate dimension 0, 960 at dimension 1 and 2,608 at dimension 2. So 2,608 of the 3,584 weighted canonical systems need two distinct triad bits locally. The 960 dimension-one systems, the R1T and R2S classes, are not two-gate at the local law. Of the 2,608 dimension-two systems, 256 never activate both rules in one state.

## Coherence record

- `F8E-K2-SCOPE-CORRECTION` records the narrower scope. It is linked by `qualifies` to `F8D-NO-GATE-PRODUCT`, `F8D-ADDITIVE-FEATURE-GRAMMAR` and `F8D-RS-COMPOSITIONAL-BOUND`. Those nodes are marked `qualified`, and their statements are unchanged.
- The relation `R-8D-GATE-PRODUCT-RAISES-META` keeps its historical rationale. A new relation from the correction node qualifies `Q-META-CONSTRAINT`, which stays `unresolved`: meta-constraints are no longer the necessary next route to a gate×gate term.
- The opening-compression correction in §2 concerns report prose only. `F8D-GATE-DIMENSION` states the counts correctly and is not qualified.
- The new open question `Q-K3-CONJUNCTION` asks what new local expressivity appears when one ordinary constraint reads two higher-order relations conjunctively. It is raised by the correction node.
