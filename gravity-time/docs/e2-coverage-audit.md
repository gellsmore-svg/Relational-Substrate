# GT-P005 coverage-and-selection audit (before E2A)

*Prompt GT-P005, deliverable 1. Written before any E2A plan was frozen and before any E2A round cell was computed. It records:*
- *what the existing data already settle;*
- *what is genuinely unobserved;*
- *which machinery is reused;*
- *which alternative mechanisms stay live.*

## 1. Verified baseline

- **Branch and PR.** The branch `research/gravity-time-admissibility` was at `3686a78` (GT-P004 close), with a clean worktree and CI green on both events. PR #6 is an open draft.
- **OTR.** The OTR 1.0 text on the branch is byte-identical to `main` (sha256 `2d902395…`).
- **E1 as reported** (`reports/gt-e1-report.md`, `provenance/execution-GT-P004.md`):
  - 8 HELD N=7 W4 cells, 24 W3/W16 cells at N=5 and 6, and 16 re-derivations;
  - the plan was frozen at `4ba2839` before any result;
  - the handover orientation was forward in 30 of 30 non-gradient cells;
  - CSPH's attachment advantage is not robust at N=7.

  All of these are model results.

## 2. Definitions read from code (not from prose)

| Concept | Where | Exact meaning |
| --- | --- | --- |
| PATH component | `gte0a.component_expressions` | For slot (a,b): one rule instance per ordered witness (end ∈ {a,b}, c, d), with c, d ∉ {a,b} and c ≠ d. The condition is `present(end-c) & present(c-d)`. Each satisfied instance multiplies the formation (`path_form`) or dissolution (`path_dissolve`) weight by the grade factor. The maximum is 2(N−2)(N−3) witnesses |
| Closure / adjacency | same | Closure: c with (a,c) and (b,c) present. Adjacency: c with (a,c) or (b,c) present, one instance each |
| Rates | `gtkernel.weights` | The product of factors over components; the HELD scaffold sets source dissolution to 0 |
| Event order | `gtobs.event_order` | Consecutive event pairs on the stationary jump chain. Key: (type, slot class, type, slot class, relation same/adjacent/disjoint). The time reverse is (flip t2, c2, flip t1, c1) |
| Handover index | `gte1.handover_statistics` | Forward minus reverse probability over the four steps FPFA, FADP, DPDA, DAFP |
| Hub frame | `gte0b.event_order_frame` | A slot is "hub" if it touches a maximum-degree vertex of the edge-present state |
| Flux | `gte0a.reversibility` | Irreversible flux = Σ|F − F_rev| / Σ(F + F_rev), with F = π_ct·W |
| Square affinity | `gte0a.reversibility` | Over all elementary squares, the **magnitude** \|log forward − log reverse\| only; the sign is not kept, and squares are not separated by role |

## 3. What existing data already settle

| Question | Existing evidence | Status |
| --- | --- | --- |
| Gradient rules are reversible | GT-F12 (theorem plus 32+ cells), E1 Z2 | Settled in this grammar |
| PATH rules have non-gradient rates | E0A X3/X4 and E1 Z3: max square affinity > 1e-6 in every PATH cell | Settled, but **unsigned** |
| Handover orientation when the PATH sign gives σ > 0 | E0B, E1: 30/30 cells, all with path_form suppress or path_dissolve favour | Observed (contingent on these grades) |
| Handover when σ < 0 | E0A published HELD N=5 PATHF weak_favour and PATHH weak_suppress: saturated (10.00 of 10 relations), flux 1e-6 and 3e-5; largest handover-step difference DPDA −2e-6 (reversed sign) | **Hint only:** magnitudes at the GT-F35 rare-mass scale; recompute required |
| Non-gradient rules with gradient ratio | E0B PCOMP (path_form wf + path_dissolve wf): reversible and uniform | Settled for that pair |
| FREE arrow legible only in the hub frame | GT-F16, GT-F28 | Observed |
| Strict support change by dissolution | Never measured. E0A EXCL (close_form prohibit) has restricted support but was not analysed for enabling | **Unobserved** |
| Passage / committor after dissolution | Never measured in GT (the laboratory's F004 is a different grammar and observable) | **Unobserved** |
| Signed local cycle structure, by role | Never measured | **Unobserved** |
| Stationary circulation against local affinity | Never measured | **Unobserved** |
| One-way transition structure under hard path rules | Never measured. GT-F35 shows E0's published one-sided counts at HELD N=6 were numerical artefacts | **Unobserved** |

## 4. Pre-freeze algebra (formal note, `docs/e2-formal-mechanism.md`)

The rule definitions above give an exact local identity, verified before freezing on synthetic factor tables only.

- For slots e = (p,q) and f = (p,r) sharing p, the square "form e, form f, dissolve e, dissolve f" from a base state x (where e and f are absent) has log affinity σ·(deg_x(r) − deg_x(q)).
- σ = Σ log m over the path-dissolve components − Σ log m over the path-form components.
- Squares on disjoint slots have affinity 0. Closure and adjacency components cancel.

This turns three of the prompt's live possibilities into precise, separately testable statements:
- **Orientation from signs and incidence.** Locally this is now an identity. Locally the handover is "keep the relation to the better-connected partner, release the one to the poorer". In HELD the source vertices carry two extra neighbours, which explains the observed orientation for σ > 0.
- **Contingent on grading.** Yes, through the sign of σ. Every E1 cell had σ > 0, so the 30/30 invariance is a consequence of the families chosen, not a fact about all path rules.
- **Local affinity against aggregated statistics.** The identity is local. Whether stationary currents and event-order indices follow it, cancel or reverse is **not** implied, and is the open empirical question.

The identity also brings out a **new mechanism**. With a hard path prohibition, no intact square carries affinity (intact squares need deg(r) = deg(q) = 0 for that component). Any irreversibility must then come from one-way transitions. A synthetic N=4 FREE smoke test (not a round cell) shows this: flux 0.12 with no affinity on any intact square. This exposure is declared in the plan.

## 5. Genuinely new contrasts, and the chosen boundary

| Axis | Covered before | New in E2A |
| --- | --- | --- |
| Sign of σ, single path component | weak grades at N=5 and 6 (E0A) | Every W4 grade, including strong and prohibit, recomputed with new channels (S1) |
| Form + dissolve pairs | PCOMP only | All four weak pairs: σ = +2 log 2, 0, 0, −2 log 2 (S2) |
| Reversible and hard references | NULL, CLOSEW, EXCL standard channels | Matched-dissolution and one-way channels (S3) |
| Strict support with circulation | none | Hard closure exclusion plus each unsaturated path component (S4) |
| σ < 0 away from saturation | none: σ < 0 saturates | Strong adjacency suppression opposed to path_form weak_favour, with a σ > 0 comparator (S5) |
| Reversed local squares | none | HELD N=6, where a probe can out-connect a source vertex (S6) |
| HELD versus FREE | E0 standard channels | Every N=5 stratum in both modes, with a source-free partner frame |

- **Size.** N=5 is the smallest size with two probes beside the held triangle. HELD N=5 cannot contain a reversed attachment/probe square (identity I5), so N=6 is added only for the four HELD cells where reversal becomes possible.
- **Excluded.**
  - N=7, and FREE N=6;
  - other closure and adjacency grades, three-component mixes, interpolated grades;
  - composites with closure favour (E0B and E1 covered them; the closure part cancels in the affinity).

## 6. Machinery reused without alteration

- `gtkernel` (kernel, W4 alphabet).
- `gtobs.analyse`, with two optional, backward-compatible arguments: a `start` override and an explicit stationary law.
- `gtobs.event_pattern_probabilities`.
- `gte1`: the handover index; the one-process-per-cell runner (now with a module argument); the long-double residual; the kernel sample check (now with family and mode arguments); the law difference.
- `gtobs_validate.gth_stationary`.
- The frozen-plan guards of `explore08`.

E1's 48 items and E0's 84 are cited, not recomputed. Published N=5 and 6 cells that reappear in E2A are recomputed only because their new channels need the law. Their standard channels are declared exposed.

## 7. Alternative mechanisms kept live

1. The orientation is a local identity, and aggregated statistics follow it everywhere.
2. Aggregated statistics follow σ only away from saturation. Near saturation the currents vanish, and their sign is numerically fragile.
3. Circulation is induced on squares with no affinity (neighbouring cycles), so local affinity under-describes the current.
4. Some stationary circulation runs **against** the local affinity of its square, through cancellation across roles or orbits.
5. Dissolution only re-weights rates (soft) in every soft cell. Strict enabling needs a hard component.
6. Strict enabling can coexist with reversibility (EXCL), so enabling and directed succession are separable.
7. Hard path rules create a one-way mode of succession that is not a soft cycle.
8. The observed precedence after a dissolution differs from the intervention effect (a selection effect).
9. Something not listed.

## 8. Laboratory context (read, not edited)

- **CL-Q04** (`constraint-lab/formal/open-problems.md`; theorem catalogue CL-T18/T25). Single-action factorisation does not cover multi-witness, pair-coupled actions. Path rules are exactly such actions.
- **CL-Q05.** "When does controlled dissolution enable a distinct configuration rather than merely remove one?" The next test asked for is matched occupancy/support passage controls (CL-N02, F004-PASSAGE-AFTER-OCCUPANCY).
- **Plan discipline and the 8G gate** (`constraint-lab/docs/scientific-plan-discipline.md`). Algebraic derivations and proof fixtures need no freeze. A bounded scientific search does.
- **E2A adds no axis.** It uses only ordinary pair-DSL templates. `prohibit` and `adj_form` are existing grammar.
