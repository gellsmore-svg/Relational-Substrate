# GT-E2 Open-Thetical coherence synthesis

*Prompt GT-P005, deliverable 9. It covers the E2A round (plan `1974678`, result `32ac7f6`), the E2A reflection (`b90c3ac`), the E2B round (plan `9448f95`, result `ecb3e73`) and the formal note.*

*Layers: [O] model observation, [M] mathematical mechanism, [RS] ontological interpretation. [P] physical comparison: **none**. [T] theological premise: not engaged.*

## 1. What the inquiry changed

**Before GT-P005**, the handover was E1's most robust behaviour (30 of 30 cells), but nothing explained it, and it was half-read as "dissolution enabling the next step".

**After GT-P005:**

| Level | Finding | Kind |
| --- | --- | --- |
| Local rates | Path rules make the cross-influence of two adjacent relations asymmetric through the degrees of their far endpoints. Closure and adjacency are symmetric | [M] exact |
| Cycle affinity | A = σ·(deg r − deg q) on every adjacent square; 0 on disjoint squares; 0 for σ = 0 | [M] theorem (formal note section 2); verified on 64 cells |
| Orientation | The handover is "keep the relation to the richer partner, release the poorer". It takes the E0 direction exactly when σ > 0; every E0/E1 family had σ = +log 2 | [M] local, [O] aggregate |
| Reversal | σ < 0 reverses it. Where density is held down the reversal is plainly visible: comparable to forward handovers with adjacency suppression (−0.112 against forward 0.015–0.19 at HELD N=5), weaker with hard closure exclusion (−0.015 to −0.042). It is negligible at saturation | [O] |
| Stationary current | Follows σ in aggregate (36 of 36 cells with σ ≠ 0, no one-way transitions and nonzero flux), but 6–36% of square-level circulation runs counter to local affinity, and large through-flow crosses zero-affinity squares | [O] |
| Enabling | In soft rules, the release step is an opportunity effect: the next event's own rate is unchanged or lower. Strict enabling needs a hard component and then appears with no direction, with soft direction, or with one-way release | [O] |
| A new mode | Hard path-form exclusion gives one-way release (relations, once let go, cannot return while supported), with its own orientation, which overrides σ | [O]; mechanism open (GT-Q11) |

So the handover now has a **proven local explanation** within a stated grammar, an **empirically robust aggregate orientation** within the tested domain, and **no support** as a causal enabling mechanism in soft rules.

## 2. Findings that did not align with the expected handover

- **Reversed handovers.** These come in two sizes: negligible in saturated σ < 0 cells, and full-size where density is held down by adjacency suppression or closure exclusion.
- **One-way release.** The largest FREE irreversibility in either round (flux 0.26) has σ = 0 and orients against σ when σ < 0.
- **Enabling without direction.** The hard closure and adjacency exclusions are reversible yet strictly enabling (up to 87% of matched cases).
- **Path terms switched off by a hard adjacency exclusion.** Five rules collapse to one law.
- **The held source as a witness.** Under two hard rules, HELD collapses to a two-state chain.
- **Counter-circulation and through-flow.** These live on zero-affinity squares.
- **Precedence that misses enabling.** After an executed dissolution, the enabled formations are less likely than average as the next event.

## 3. Succession, gathering, persistence, release

- **Succession** is clearer. The model now has three distinct generators of ordered succession:
  1. soft non-gradient circulation, oriented by σ;
  2. one-way release under hard formation exclusion;
  3. none: reversible chains, even with strict enabling.

  Each is a different relation between rates, admissibility and order.
- **Gathering** was not studied directly. E2A's HELD attachment fractions are all below the null except the reversible controls, consistent with GT-F36 and GT-F18.
  - The reversed handover in ADPF did not produce gathering either: attachment 0.627 against the null 0.857.
  - Orientation of succession and attachment remain decoupled (GT-F43).
- **Persistence** is less clear than before. The race channel shows that enabled configurations persist only about as long as the support takes to return (wins about 0.5). One-way release gives a stronger kind of persistence: an *absence* that cannot be undone while supported.
- **Release.** [RS] The distinction GT-P005 asked for is now concrete. Release can be:
  - a kinetic occasion (soft);
  - an admissibility change (hard);
  - an irreversible step (one-way).

  Only the last makes release itself a directed event.

## 4. Interpretation, kept separate [RS]

- **Tendency and admissibility generate order differently.**
  - Tendency (soft weights) orders succession only through cycle affinity. The orientation is a degree comparison: relations to better-connected partners persist.
  - Admissibility (hard rules) can order succession without any cycle affinity, by making some releases unrecoverable.
  - These are two different ontological readings of "direction", and the grammar keeps them apart.
- **"Dissolution enabling a later change" has at least four non-equivalent meanings** in a relational substrate account: precedence, opportunity, rate, and support. They separate cleanly in the model, so an RS statement should name which one it means.
- **Orientation toward the better-connected partner** is a candidate motif for "relations to structure outlast relations to periphery". It is a local kinetic rule, not gathering. GT-F43's decoupling still holds.
- None of this is physics. A Markov-chain cycle arrow is not thermodynamic entropy production, and it is not an arrow of time, gravity, duration or redshift. Nothing here says what would sustain such a rule physically.

## 5. Coherence ledger links

New findings and questions (GT-F45 to F53, GT-Q11 to Q13) are linked in `coherence/` to:
- GT-F37: orientation explained, its domain stated;
- GT-F43 and GT-F44: decoupling unchanged;
- GT-Q08: partially answered;
- GT-Q09: not addressed;
- GT-Q10: retained, not studied;
- GT-F18 and GT-F14: repulsion and saturation.

## 6. Cross-programme suggestions (not entered in the laboratory's records)

The Constraint Laboratory is governed independently. Nothing was edited or cherry-picked into its branches. Suggested items, with evidence paths on this branch:

1. **For CL-Q04** (incidence and coupled actions breaking factorisation).
   - Suggested finding: in the ordinary pair DSL, two-witness path templates are the minimal coupled actions that produce non-gradient rates. Their square affinity is exactly σ·(deg r − deg q), so incidence enters the dynamics through the degree asymmetry of far endpoints. Closure and adjacency templates are incidence-symmetric and cancel.
   - Evidence: `gravity-time/docs/e2-formal-mechanism.md` section 2; `gravity-time/reports/round-e2a-tables.json` (I1, I2).
   - Suggested integration: a theorem-catalogue entry with GT provenance, if the laboratory adopts it.
2. **For CL-Q05** (transition-enabling dissolution).
   - Suggested finding: under matched occupancy/support controls, strict enabling by dissolution occurs only through hard formation exclusions. It can coexist with reversibility, with soft circulation, or with one-way release. Soft-rule "enabling" decomposes into rate and opportunity effects, with opportunity dominant in 59% of groups.
   - Evidence: `gravity-time/reports/gt-e2-dissolution-analysis.md`; the E2A/E2B tables (`matched_dissolution`, `race`).
   - Suggested next laboratory test: the race committor on the laboratory's own F004 passage contrasts.
3. **Suggested question for both programmes.** Is one-way release under hard formation exclusion the general form of irreversible succession without cycle affinity in finite relational grammars? (GT-Q11.)

## 7. The next experiment (recommended, not run)

Factors are compared separately (OTR section 6), with no combined score.

| Candidate | Information value | Novelty | What it discriminates | Cost |
| --- | --- | --- | --- | --- |
| **A. One-way release mechanism** (GT-Q11): derive or refute its orientation; vary which hard formation exclusion creates one-way release; N=4/5 analytic plus a small frozen census | High: the one counterexample to σ, and the only directed succession without cycle affinity | High | Is release orientation set by where two-paths end (degree), by density, or by the exclusion's incidence? | Low |
| B. Aggregate-orientation theorem attempt | Moderate–high: would turn the 36/36 regularity (cells without one-way transitions) into a theorem or produce a counterexample | Moderate (cycle-decomposition mathematics) | Proof versus counterexample among positive-factor rules | Low (mathematical), uncertain outcome |
| C. Clock split (GT-Q09) | Moderate | Moderate | Why strengthening splits CSPH's clocks | Low |
| D. Source-size control (held K4 versus triangle) | Moderate; E2 showed the scaffold acts as a witness under hard rules, so source structure matters more than assumed | Low–moderate | Scaffold as witness against scaffold as reference | Moderate (N=6/7 HELD) |
| E. FREE N=7 hub emergence | Low: nothing in E2 suggests a hub mechanism. The partner frame shows that orientation needs no hub | Low | — | High (not authorised) |

**Recommendation: A, with B as its mathematical companion.**
- E2 found exactly one place where the σ account fails: one-way release. That is also the only form of directed succession the grammar produces without cycle affinity, and the only place where dissolution is itself an irreversible, directed event.
- Understanding it would close GT-Q08's last gap and give CL-Q05 a precise answer. It is cheap and exact.
- **Source-size control (D)** has gained value: the held source turned out to act as a witness, not only as a reference.
- **FREE N=7 (E)** has lost value further.
