# E1 scale and witness-strength confound audit

Prompt GT-P003, deliverable 3. This is design analysis, not a scientific round. **No N=7 scientific cell was opened.** Every number below comes from one of three places:

- the template definitions (law-free counting over the candidate space);
- the NULL family, whose stationary law is uniform by theorem;
- already-published N=5 and N=6 E0 cells, recomputed by the validated `gtobs` path.

Channels computed post hoc on published cells are labelled **post hoc**. They are design observations, not frozen-plan results.

Data:
- `reports/e1-scale-census.json` (law-free and NULL; `python -m rs_constraint_lab.gtscale`).
- `reports/e1-engaged-witness-n5-n6.json` (executed-event witness census of published design cells; post hoc).
- `reports/e1-margin-decomposition-n5-n6.json` (attachment margins and detachment counts of published HELD cells; post hoc).

## 1. What the representation fixes

The model has one present/absent bit per unordered pair. So there are N(N−1)/2 slots and 2^[N(N−1)/2] FREE configurations. HELD fixes the three source relations, which leaves 2^[N(N−1)/2 − 3] candidates.

| N | Slots | FREE configurations | HELD candidates | Probes (HELD) | Source share of entities |
| --- | --- | --- | --- | --- | --- |
| 5 | 10 | 1,024 | 128 | 2 | 0.60 |
| 6 | 15 | 32,768 | 4,096 | 3 | 0.50 |
| 7 | 21 | 2,097,152 | 262,144 | 4 | 0.43 |

These counts are consequences of the chosen representation, and section 7 says what does and does not follow from them.

## 2. Witness counts: definitions, bounds and null means

A label-covariant template multiplies its factor m once per satisfying witness. A component's contribution to a toggle's log-weight is therefore w·log m, where w is the witness count.

| Component | Witnesses of pair ab | Maximum w | N=5 / 6 / 7 |
| --- | --- | --- | --- |
| closure | #{c : x_ac ∧ x_bc} | N−2 | 3 / 4 / 5 |
| adjacency | #{c : x_ac} + #{c : x_bc} | 2(N−2) | 6 / 8 / 10 |
| path | Σ_end #{(c,d) : x_end,c ∧ x_c,d} | 2(N−2)(N−3) | 12 / 24 / 40 |

Mean w over every acting (state, slot) of the candidate space is the NULL law's mean. In FREE each bit is an independent fair coin, so the means are (N−2)/4 for closure, N−2 for adjacency and (N−2)(N−3)/2 for path. The census reproduces these exactly.

| Component | FREE mean, N=5 / 6 / 7 | Ratio N6→N7 | HELD mean, N=5 / 6 / 7 | Ratio N6→N7 |
| --- | --- | --- | --- | --- |
| closure | 0.75 / 1.00 / 1.25 | 1.25 | 1.18 / 1.38 / 1.58 | 1.15 |
| adjacency | 3.0 / 4.0 / 5.0 | 1.25 | 3.86 / 4.75 / 5.67 | 1.19 |
| path | 3.0 / 6.0 / 10.0 | 1.67 | 5.57 / 9.00 / 13.33 | 1.48 |

**Consequence.** At a fixed W4 grade, the typical path log-weight available to a toggle grows by about 1.5–1.7× from N=6 to N=7. The closure log-weight grows by only about 1.15–1.25×. A composite such as CSPH (closure strong_favour + path weak_favour) therefore changes its *internal balance* as N grows, as well as its overall strength. A fixed grade is not a fixed aggregate influence.

## 3. What the dynamics actually engage (post hoc, published cells)

The null means above are what the representation offers. What matters for a cell is how many witnesses its executed events actually carry under its own stationary law. The new `witness_census_jump` channel measures this, per executed event of each component (`gtobs.witness_census`).

| HELD cell | Component | Engaged mean w, N5 → N6 | Ratio | Null mean ratio |
| --- | --- | --- | --- | --- |
| CSPH | closure form (strong_favour) | 0.99 → 0.84 | 0.85 | 1.17 |
| CSPH | path dissolve (weak_favour) | 3.75 → 4.10 | 1.09 | 1.62 |
| CSPF | path form (weak_suppress) | 2.60 → 2.19 | 0.84 | 1.62 |
| CWPH | path dissolve (weak_favour) | 3.13 → 3.44 | 1.10 | 1.62 |
| PATHF weak_suppress | path form | 1.96 → 1.73 | 0.88 | 1.62 |
| PATHH weak_favour | path dissolve | 2.76 → 3.03 | 1.10 | 1.62 |
| CLOSEW (gradient) | closure form (weak_favour) | 2.36 → 3.46 | 1.47 | 1.17 |

FREE cells show the same pattern. Their path-term ratios are 1.20–1.39, against a FREE null ratio of 2.0 from N5 to N6. CLOSEW's is 1.67, and CSPH's closure term falls (0.80 → 0.74).

**Reading.** The non-gradient composites largely regulate themselves away from high-witness states. Their path terms dissolve or suppress the configurations that would carry many witnesses. Their engaged path load grows by about 10% from N5 to N6, against 62% for the null. The engaged closure load in CSPH and CSPF actually falls. The gradient densifier CLOSEW behaves in the opposite way: it walks into dense states, and its engaged load grows faster than the null's.

So witness amplification is not a fixed multiplier attached to N. It depends on the dynamics, and it is measurable. E1 can record the engaged load at N=7 as an ordinary channel, and an interpretation can then condition on it, without assuming it. This is the main reason the confound is partly identifiable (section 6).

## 4. Other size-dependent baselines (NULL, theorem-fixed)

| HELD NULL quantity | N=5 | N=6 | N=7 |
| --- | --- | --- | --- |
| Attachment slots / free slots, r0 | 6/7 = 0.857 | 9/12 = 0.750 | 12/18 = 0.667 |
| Room for selectivity, 1 − r0 | 0.143 | 0.250 | 0.333 |
| Expected free edges | 3.5 | 6.0 | 9.0 |
| P(probe at distance 1) | 0.875 | 0.875 | 0.875 |
| P(probe at distance 2) | 0.055 | 0.085 | 0.103 |
| P(probe at distance 3) | — | 0.0034 | 0.0045 |
| P(probe at distance 4) | — | — | 0.00016 |
| P(probe detached) | 0.070 | 0.036 | 0.018 |
| P(all probes detached) | 0.016 | 0.002 | 0.00024 |
| P(a probe is among the max-degree vertices) | 0.23 | 0.34 | 0.42 |
| P(the hub set is probes only) | 0.016 | 0.055 | 0.108 |

| FREE NULL quantity | N=5 | N=6 | N=7 |
| --- | --- | --- | --- |
| P(unique max-degree vertex) | 0.513 | 0.530 | 0.545 |
| P(2 tied hubs) | 0.264 | 0.263 | 0.255 |
| P(≥3 tied hubs) | 0.224 | 0.208 | 0.199 |

Implications for E1:

- **The attachment null r0 falls** from 0.857 to 0.667. A raw margin at N=7 is measured against a lower bar, with more room above it. Comparing raw margins across N mixes a changing ceiling with a changing effect. The normalised margin (af − r0)/(1 − r0) should be reported alongside the raw one; at N=5 and N=6 it is 0.32 and 0.036 for CSPH (continuous clock).
- **Shells 3 and 4 are rare under the null.** At N=7, shell 4 holds 1.6e-4 of the null probe mass. Its activity is computed exactly (no sampling noise), but it describes rare, long probe chains. It should not be read as a typical outer region.
- **Hub ties are common.** In FREE about 45% of null states have tied hubs at every N. A hub frame that admits ties (as E0B's does) is needed; a "unique hub" analysis would discard half the ensemble.
- **The source becomes a smaller share of entities** (0.6 → 0.43), and the probability that the hub set is probes only grows (0.016 → 0.108) even under the null. A probe-only hub at N=7 is therefore not by itself evidence of emergent centralisation.

## 5. The CSPH margin depends on clock and density (post hoc, published cells)

GT-F26 and the E0 report quote the CSPH margin as +0.047 (N5) and +0.009 (N6). That is the continuous-clock value, attachment_fraction − r0. Recomputing on the published laws gives:

| HELD CSPH | Continuous margin | Continuous, null-density standardised | Jump margin | Jump, null-density standardised |
| --- | --- | --- | --- | --- |
| N=5 | +0.046 | +0.023 | +0.073 | +0.038 |
| N=6 | +0.009 | **−0.073** | +0.065 | **−0.034** |

- **Clock.** Under the jump clock (per event) the margin hardly shrinks, from +0.073 to +0.065. Its fragility is a property of the per-unit-time convention, which weights long-lived states. Both conventions were published; the report quoted one.
- **Density.** The published profile of attachment fraction by free-edge count k (HELD N6, continuous) is 0.771, 0.792, 0.746, 0.701, 0.667 and 0.650 for k = 1 to 6, against r0 = 0.75. CSPH spends about 93% of its time at k ≤ 3, where the ratio exceeds r0. At typical null densities the same rule mildly favours probe–probe relations. The standardised margin reweights E[a | k] to the null's binomial density profile, and that profile sits where a/k < r0.
- Every comparison cell with a path term (CSPF, CWPH, CWPF, PATHF, PATHH) is negative under both standardisations at N=6.
- **What the standardised margin is.** It is a counterfactual comparison: the rule's conditional preference E[a | k], read at the null's densities. Some of those densities a cell rarely visits. At N=6, k = 9–11 carry about 7% of the binomial weight but can have stationary mass as low as 1e-35. `gtobs` computes those conditionals to about 1e-13 relative, which E0's dense solve did not (validation note, section 3). They still describe configurations the cell does not occupy. The standardised margin therefore complements the raw margin and does not replace it. CLOSEW is mildly positive (+0.03), and NULL is 0 to 1e-12, as the identity requires.

This qualifies GT-F26 without contradicting it. The selective attachment is real at the densities CSPH occupies, but it is a sparse-regime preference, not a density-independent bias toward the source. The qualification comes from a post hoc channel and is recorded as such (coherence ledger, GT-F34). It does not rewrite the published finding.

## 6. Identifiability at N=7

What the native fixed-grade sequence N = 5, 6, 7 (W4) can and cannot separate:

| Possible cause of a change between N=6 and N=7 | Separable at N=7? | How |
| --- | --- | --- |
| Lower attachment ceiling (r0 falls) | Yes | Report raw, normalised and standardised margins together |
| Density shift (the cell visits different k) | Yes | Full a/k profile by k, density-standardised margin, edge-count distribution |
| Clock convention | Yes | Every rate channel in both clocks, as E0 did |
| Witness amplification, overall | Partly | Engaged-witness census at N=7 against N=6, and the base-sensitivity bracket below |
| Witness amplification, component balance (closure vs path) | Only partly | Per-component engaged load. No in-grammar model holds one component's load fixed while N changes |
| Source-share and probe-count changes | No, not from N alone | Intrinsic to HELD with a fixed three-vertex source. A larger held source would be a different instrument (G3) |
| Shell-size and topology changes | Descriptively only | Shell masses against the null shell masses |
| "Intrinsic" size dependence of the organisation | No | The residual after the above. With three sizes and one family it has no unique interpretation |

**A base-sensitivity bracket (within the existing grammar).** The laboratory already defines the sensitivity alphabets W3 (base 3) and W16 (base 4): `weights.py`, `docs/experiment-roadmap.md`, Generation 7. They keep every grade and ordering, and scale every log-factor by log 3 / log 2 = 1.585 or by 2. At a fixed N they change rule strength and nothing else: not the combinatorics, the source share or the shells. Running the same families at N = 5 and 6 under W3 and W16 measures each observable's response to uniform strength scaling at fixed size.

- If an observable's N6→N7 change lies within the span produced by W4→W3→W16 at N6, in the same direction, *and* the N=7 engaged log-weight ratio falls in the 1.0–2.0 range those alphabets bracket, witness amplification remains a candidate explanation.
- If the N=7 change runs opposite to the strength response, or exceeds it while the engaged load barely grows, amplification is unlikely to be the main cause.
- The bracket can be **calibrated on the published N5→N6 step** first. N5 under W16 doubles every log-factor, which exactly matches the path-witness maximum from N5 to N6 (12 × 2 = 24). Comparing N5-W16 with the published N6-W4 tests whether the bracket explains a step whose two ends are already known.

Limits of the bracket:
- It scales closure and path together, so it cannot reproduce the changed closure/path balance of a composite.
- It is a bracket, not a decomposition.
- Exact matching of aggregate log-weight would need non-dyadic bases such as 2^(3/5). The named alphabets exclude these (`formal/expressivity-boundaries.md`), so that would be a grammar change, requiring an ontology proposal, and is not proposed here.
- The single-component families (PATHF weak_suppress, PATHH weak_favour, CLOSEW) are the cleanest bracket cases, because one component carries all the strength.

## 7. What the binary representation does and does not imply

- The count 2^[N(N−1)/2] arises only because this finite model gives each unordered pair one present/absent bit.
- Directed relations, multivalued states, relation types, or triadic (O=3) relations would give different counts and different witness structures.
- The combinatorics are the practical limit on exact exploration: N=8 FREE would have 2^28 ≈ 2.7×10⁸ states.
- No physical or ontological claim about a binary reality follows from this representational choice.

## 8. Predeclared reading rules proposed for E1

These are proposals for the frozen plan, chosen before any N=7 cell is seen:

1. **A sign change of one margin is an observation about that fixed-grade, finite-N model**, in the stated clock and standardisation. It is not on its own evidence of intrinsic size dependence, of witness amplification, or of failure of the wider RS ontology.
2. **Report every margin in four forms**: raw and null-density standardised, each in both clocks. Also report the normalised margin (af − r0)/(1 − r0) and the full a/k profile. No single form is primary for interpretation; the plan may name one form for its frozen expectation, chosen now.
3. **No grade, alphabet or threshold is chosen after seeing N=7.** Any follow-up sensitivity cell is designed and frozen in a later round.
4. **Fragile and negative outcomes are findings.** A vanished margin, a persisting handover with no selectivity, or no effect at all are recorded as computed.
