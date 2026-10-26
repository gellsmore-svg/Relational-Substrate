# GT Round E1 — results report

*Prompt GT-P004, deliverables 4 and 6. Written to be read without the programme's internal vocabulary. Numbers are exact-kernel values from `reports/round-e1-tables.json` (result commit `730ef32`, payload `f1727f9d3c3f…`). The behaviour atlas `reports/gt-e1-atlas.md` lists every cell and every channel; this report is a reading of it, not a selection from it.*

Layers are marked: **[O]** model observation, **[M]** mathematical mechanism, **[RS]** Relational Substrate interpretation, **[P]** physical comparison, **[T]** theological premise. No [P] claim is made anywhere in this report.

## 1. What was run, and why

**The model.** A few entities (5, 6 or 7). Between every two of them a relation is present or absent. Relations form and dissolve one at a time. A rule makes some changes more or less likely, multiplying a factor once for every qualifying "witness" nearby. In the HELD set-up three entities form a permanently linked source triangle; the others ("probes") may attach to it or not. The stationary law of every cell is computed exactly, in two clocks:
- **per unit time** (continuous clock): where the system spends its time;
- **per event** (jump clock): what the sequence of changes looks like.

**Why E1.** E0 found that rules which look two steps away (path rules) create a lasting direction of flow — a **handover** cycle: probe–probe relation forms, attachment to the source forms, probe–probe relation dissolves, attachment dissolves. One combined rule, **CSPH**, also gave a small advantage to attachment over the no-rule baseline, shrinking from N=5 to N=6. GT-P003 then found that the advantage depends on the clock and on crowding, and that the same nominal rule might get effectively stronger as N grows (more possible witnesses). E1 asks two questions at once:

1. **Tranche I (8 cells).** The same eight E0B rules, same grades (W4 alphabet), at N=7.
2. **Tranche II (24 cells).** The six non-gradient rules made uniformly stronger (W3: every log-factor × 1.585; W16: × 2) at N=5 and N=6. This shows what "a stronger rule at the same size" does, to compare with what "a bigger system" does.

Plus 16 re-derivations of the published N=5, 6 W4 cells with the same code, so every comparison uses one implementation. These are not new observations.

The plan was frozen and pushed (`4ba2839`) before any round cell ran. All 48 items completed in 24 minutes on four workers (longest cell 615 s, peak 603 MB). No cell was unresolved; every cell passed every numerical check (two-start and third-start agreement, per-entry residual in extended precision, the dense GTH referee at N≤6, the rule strings re-evaluated exactly on sampled states). All identities and controls held: NULL uniform and reversible (Z1), the gradient control on its predicted law (Z2), non-gradient rates in every non-gradient cell (Z3), every published N=5, 6 cell reproduced on the declared robust channels (Z4), and both reversible controls without hub-frame circulation (Z6).

## 2. What changed from N=6 to N=7 at fixed grades

### 2.1 CSPH's attachment advantage is gone at N=7 [O]

| CSPH margin over the null | N=5 | N=6 | N=7 |
| --- | --- | --- | --- |
| raw, per unit time | +0.046 | +0.009 | **−0.067** |
| raw, per event | +0.073 | +0.065 | **+0.002** |
| ceiling-normalised, per unit time | +0.325 | +0.035 | −0.200 |
| ceiling-normalised, per event | +0.511 | +0.260 | +0.005 |
| crowding-adjusted (standardised), per unit time | +0.023 | −0.073 | −0.112 |
| crowding-adjusted, per event | +0.038 | −0.034 | −0.095 |

In every form the N=7 value is at or below the null; the per-event raw margin is +0.002, which is the null to within the size of the effects in this round. **The basin-with-arrow coexistence that E0B found in CSPH (GT-F26) does not survive to N=7 in this model.** This is a finding for this family, this size and these definitions; it is not by itself evidence of an intrinsic finite-size effect, of witness amplification, or of a failure of the wider picture (plan, stop-rule reading).

### 2.2 Why the advantage disappeared: a sparse-only preference, less time sparse [O, M]

The advantage is an average over how many free relations are present (k). Resolved by k (frozen channel: the a/k profile):

| CSPH, per unit time | attachment per free relation at k = 1, 2, 3, 4, 5 | null | time spent at k ≤ 2 |
| --- | --- | --- | --- |
| N=5 | 0.855, 0.924, 0.922, 0.870, 0.850 | 0.857 | 0.86 |
| N=6 | 0.771, 0.792, 0.746, 0.701, 0.667 | 0.750 | 0.68 |
| N=7 | 0.718, 0.701, 0.625, 0.533, 0.472 | 0.667 | 0.42 |

At N=7 the preference for attachment is still there when only one or two relations are free (excess +0.03 to +0.05 over the null, against +0.02 to +0.04 at N=6). At three to five free relations the rule prefers probe–probe relations, more strongly than at N=6 (k=4: −0.13 against −0.05). And the system spends less of its time in the sparse regime: with more probes there are more ways to have several free relations. The same pattern holds per event (excess at k ≤ 3; time at k ≤ 2 falls 0.62 → 0.43 → 0.24).

A **post hoc** decomposition (computed after the results; not a frozen comparison; `reports/e1-margin-composition-posthoc.json`) writes the margin as the occupancy-weighted average of the per-density excess and splits its change into an occupancy part and a preference part. For CSPH from N=6 to N=7: per unit time −0.075 = −0.025 (occupancy) − 0.050 (preference); per event −0.063 = −0.027 − 0.036. **About a third of the loss is the move to higher density; two thirds is a stronger anti-attachment preference at moderate density.** The local preference at very low density survives but no longer dominates.

### 2.3 The handover persists, unchanged in orientation [O]

All four steps of the handover cycle run in the E0 direction **in all 30 non-gradient cells** (six families × every size and alphabet), and in none of the reversible controls. The handover index (forward-minus-reverse probability over the four steps, per event pair) at N = 5, 6, 7:

| | CSPH | CSPF | CWPH | CWPF | PATHF | PATHH |
| --- | --- | --- | --- | --- | --- | --- |
| index | 0.036, 0.043, 0.042 | 0.070, 0.062, 0.040 | 0.049, 0.052, 0.047 | 0.087, 0.071, 0.047 | 0.095, 0.076, 0.050 | 0.055, 0.056, 0.049 |
| irreversible flux | 0.090, 0.136, 0.157 | 0.126, 0.162, 0.147 | 0.098, 0.136, 0.150 | 0.134, 0.161, 0.154 | 0.132, 0.158, 0.153 | 0.088, 0.124, 0.140 |

For rules that act on dissolution (…H) the handover's per-event weight is roughly constant with N; for rules that act on formation (…F) it shrinks. Total irreversible flux is roughly constant from N=6 to N=7 (0.14–0.16 in all six). **The arrow does not weaken with size in total; the attachment advantage does. Arrow and basin separate further at N=7.** [O]

### 2.4 Other changes with N [O]

- **Detachment stays high.** In every non-gradient cell a probe is detached about 55–58% of the time at N=7 (NULL: 1.8%; gradient control: 0.004%). At N=7, three or four of the four probes are often detached at once (CSPH: 49% of the time per unit time). The repulsive character of every arrow-carrying rule (GT-F18) persists.
- **The equal-ratio gap keeps growing, more slowly.** Pairs with the same local ratios but acting on formation versus dissolution differ in stationary law by L1 0.18–0.22 (N=5), 0.32–0.49 (N=6), 0.37–0.62 (N=7). Growth slows from ×1.8–2.3 to ×1.15–1.25.
- **Near/far activity contrast weakens in the arrow cells.** The ratio of probe activity near the source to activity farther out (ρ) falls toward 1 in formation-acting rules (CSPF 1.18 → 1.09, PATHF 1.11 → 1.03 per unit time). In the gradient control it falls below 1 and keeps falling (CLOSEW 1.03 → 0.89 → 0.61): near-source slowing grows with N there, consistent with G1's kinetic account.
- **Attachments last longer, measured in events.** The correlation time of "probe attached" grows with N in every non-gradient family (e.g. CSPH 4.6 → 5.9 → 7.0 mean events; CWPH 2.4 → 3.5 → 4.6; PATHF 1.7 → 3.1 → 4.8).
- **Hubs.** The share of time a probe alone is the best-connected entity rises with N in every family (N=7: 0.03–0.10), tracking the NULL rate (0.016 → 0.055 → 0.108) but staying below it. This is the changing geometry of the HELD set-up (more probes, smaller source share 3/N), not an emergent centre.
- **The gradient control (CLOSEW) fills up.** Free-relation density 0.81 → 0.90 → 0.96. Its raw margin falls to about zero (+0.0008) because it is near the ceiling, while its crowding-adjusted margin grows (+0.022 → +0.034 → +0.042). The only rule in the round with a crowding-adjusted attachment preference that grows with N is the reversible gradient control, not any arrow-carrying rule.

## 3. Size versus strength

### 3.1 How much stronger do the rules actually act at N=7? [O]

A path rule can see up to 12, 24 and 40 witnesses at N = 5, 6, 7. But the witnesses a rule *actually uses* at the events that happen grew very little. The ratio of mean engaged log-weight N=7 / N=6, per component:

| | closure part | path part |
| --- | --- | --- |
| CSPH | 0.87 | 1.05 |
| CSPF | 0.99 | 0.87 |
| CWPH | 0.87 | 1.06 |
| CWPF | 1.05 | 0.92 |
| PATHF | — | 0.94 |
| PATHH | — | 1.08 |
| CLOSEW (gradient) | 1.35 | — |

Every non-gradient component is between 0.87 and 1.08, far below the strengthening bracket (1.585 for W3, 2 for W16). The arrow-carrying rules steer the system into states with few witnesses, so their effective strength barely changes with size. **Witness amplification, as actually engaged, is small from N=6 to N=7.** (The gradient control does amplify, 1.35, because it fills the graph.)

### 3.2 Does "stronger at N=5" reproduce the known step N=5 → N=6? [O]

The frozen calibration compares, channel by channel (17 declared channels), the step N=5 W4 → N=5 W16 (log-strength doubled, matching the witness maximum 12 → 24) with the published step N=5 → N=6 at W4.

| Family | verdict (frozen rule) | channels with the same direction | of which comparable in size |
| --- | --- | --- | --- |
| PATHF (clean case) | direction only | 12 of 17 | 3 |
| PATHH (clean case) | direction only | 14 of 16 | 5 |
| CWPF | direction only | 13 of 17 | 4 |
| CWPH | direction only | 15 of 17 | 6 |
| CSPF | direction only | 15 of 17 | 6 |
| CSPH | **poor proxy** | 10 of 17 | 0 |

Strengthening moves most channels in the same direction as growing the system, but by a different amount, and in no family does it reproduce the step in size. For CSPH it is a poor proxy: it gets 7 channels in the wrong direction, including the per-event margin, irreversible flux and the handover index. Under the frozen reading rule, CSPH's N=7 comparison below is reported but not used as evidence for or against amplification.

### 3.3 Is the N=6 → N=7 step what strengthening does at N=6? [O]

Per channel, the N=6 → N=7 step is compared with the W3 and W16 responses at N=6. Pooled over the six families (102 channel readings): 16 in the direction and size range of strengthening, 55 in the direction but outside the range, 22 opposite, 8 with a non-monotone strength response, 1 negligible. Almost all "outside the range" readings are **smaller** than strengthening would produce, which is what the engaged-load ratio of about 1 predicts.

Channels that run **opposite** to strengthening in most families:
- **probe-only hub share** (all six families): N raises it, strengthening lowers it — a geometric effect of adding probes;
- **near/far activity ratio** (five families);
- in CSPH, the **per-event margin and irreversible flux**: strengthening raises both, size lowers the margin and raises the flux less;
- the **handover index** in CWPH and PATHH: strengthening raises it, size leaves it flat or slightly lower.

Detachment is the clearest contrast: strengthening at N=6 drives probe detachment from 0.52–0.55 to 0.84–0.89; going to N=7 changes it only to 0.55–0.58.

### 3.4 Size and strength act on the margin differently [O, M]

The same post hoc decomposition (labelled as such) applied to the strengthening step separates the two operations:

| Margin change, per unit time | total | occupancy part | preference part |
| --- | --- | --- | --- |
| CSPH, size N=6 → 7 | −0.075 | −0.025 | −0.050 |
| CSPH, strength N=6 W4 → W16 | −0.306 | +0.007 | −0.312 |
| CWPH, size | −0.065 | −0.031 | −0.035 |
| CWPH, strength | −0.318 | +0.018 | −0.336 |
| PATHH, size | −0.055 | −0.032 | −0.023 |
| PATHH, strength | −0.268 | +0.029 | −0.296 |

- **Strength acts almost entirely through the per-density preference**, and its occupancy part has the opposite sign: strengthening crowds the system into low density (CSPH time at k ≤ 2: 0.68 → 0.83), which by itself would *raise* the margin. In CSPH it also **splits the clocks**: per event the preference survives (attachment per free relation at k = 1–3: 0.87, 0.91, 0.85 against the null 0.75) and the per-event margin rises (+0.065 → +0.092), while per unit time it collapses (0.58, 0.65, 0.22) and the margin falls (+0.009 → −0.297). In CWPH and PATHH strengthening lowers the preference in both clocks.
- **Size acts through both parts**, and its occupancy part is negative in all three dissolution-acting families and both clocks (−0.024 to −0.032): growing the system moves occupancy toward higher density, the opposite of what strengthening does.
- In the formation-acting families (CSPF, CWPF, PATHF) the occupancy part is small for both operations (|·| ≤ 0.02) and both act through the preference.

So "the rule got stronger" and "the system got bigger" are distinguishable in this grammar: they move occupancy in opposite directions, and strengthening changes the preference several times more than one step of size. [M: the margin is exactly Σ_k q(k)·x(k), an average of the per-density excess x over the attachment-weighted density profile q; the split depends on the order of the two terms, and the reported split uses the smaller system's preference and the larger system's profile.]

### 3.5 What remains confounded

- **Intrinsic size dependence.** With three sizes, what remains after the measured effects (engaged load, density composition, ceiling) has no unique interpretation.
- **Composite balance.** Uniform strengthening scales closure and path parts together. In CSPH the engaged closure load fell (0.87) while the path load rose (1.05) from N=6 to N=7; the bracket cannot reproduce that rebalancing.
- **Source share.** The fixed source triangle is 60%, 50%, 43% of the entities at N = 5, 6, 7, and the null ceiling falls with it. Neither is separable from N in HELD.
- **Counterfactual standardisation.** The crowding-adjusted margin reweights to the NULL density profile, which at N=7 puts most weight on k = 7–11, where CSPH's own mass is 3e-4 to 1e-15 (some flagged rare). It is reported beside the raw margin and never alone. Every rare conditional (mass < 1e-12) is flagged in the tables and not interpreted.
- **Spectrum.** The relaxation spectrum is unavailable in every E1 cell (not computed by the scalable observables); it is not zero.

## 4. Model result versus physical implication

Everything above is **[O]** or **[M]**: properties of a declared stochastic grammar on 5–7 entities. Nothing here is a statement about gravity, time dilation or any physical system **[P]**. In particular:
- the disappearance of CSPH's attachment advantage is not evidence against relational accounts of gravity, and its persistence would not have been evidence for them;
- the handover is an order of events in a toy chain, not a physical arrow of time;
- the near-source slowing in the gradient control is a kinetic property of that rule (G1), not a clock-rate effect.

The **[RS]** reading, kept separate: the round sharpens a distinction the RS framework can use — between *succession* (a stationary order of actualisation, here robust to size and strength) and *gathering* (a time-weighted preference for relation to a reference, here fragile, density-dependent and clock-dependent). In this grammar the two are produced by the same rules but are not coupled; the RS layer should not treat one as evidence of the other. No theological premise **[T]** is tested or used.

## 5. What was not run

- FREE N=7 (option D) was not authorised; whether a centre emerges without a fixed source at N=7 remains open.
- No grade, alphabet or size was added after freezing; no cell was re-run.
- Trajectories (four per cell, 400 events) were generated and are replayable from their seeds, but add no independent insight beyond the exact laws; the atlas does not reproduce them.

## 6. Where to look

- Every cell and channel: `reports/gt-e1-atlas.md`.
- Raw tables, comparisons, flags: `reports/round-e1-tables.json`.
- Frozen plan: `plans/round-e1-plan.json` (commit `4ba2839`, hash `c6328d51…`).
- Reflection and next-step recommendation: `reports/gt-e1-reflection.md`.
- Execution record: `provenance/execution-GT-P004.md`.
