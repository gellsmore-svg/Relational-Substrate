# GT-P008 coverage and integrity audit

*Prompt GT-P008, deliverable 1. Written 2026-10-15, before any GT-P008 derived quantity was computed from published data. Layers: [O] observation, [M] mathematics, [RS] interpretation; [P] none; [T] none.*

## 1. Baseline (verified, not assumed)

| Item | Value | How verified |
| --- | --- | --- |
| Branch | `research/gravity-time-admissibility` | `git branch --show-current` |
| Remote head at start | `11f62df0c56a866e46c212fbb86f4dc5623fb2e6` (GT-P007 close) | equals local `HEAD`; worktree clean |
| PR #6 | open, draft, head `11f62df` | `gh pr view 6` |
| CI at start | success (push and pull_request runs on `11f62df`) | `gh run list` |
| `main` | `05b15b0` (PR #7, OTR); unchanged | `git log origin/main` |
| OTR | sha256 `2d902395…88dd`, identical on branch and `main` | `sha256sum` |
| E4A tables | payload `f050380ac32e`, plan hash `61e3bef2…`, 36 complete | payload re-hashed from canonical JSON: matches |
| E4B tables | payload `169e71c33b38`, plan hash `82fce6f3…`, 12 complete | payload re-hashed: matches |
| Published plans/reports | no change between `11f62df` and the GT-P008 prompt commit `fe7701a` | `git diff --stat` empty |

**The baseline has not moved.** The facts in the prompt's §1 (36 + 12 cells, frozen `f5b3b50` / `9a1c539`, results `06e5f36` / `64e183f`, reflection `8127d24`, 748 tests) all agree with the repository.

## 2. What was read

- **Method and governance:** `research-methods/open-thetical-research.md`, `gravity-time/charter.md`, `docs/roadmap.md`, `coherence/current-map.md` and JSONL, the `through-gt-e4.md` snapshot, `plans/journey.jsonl`, `hypotheses.md` and `.jsonl`, `constraint-lab/docs/scientific-plan-discipline.md` (including the 8G compilation gate), and `constraint-lab/formal/open-problems.md` (read only).
- **Evidence:** the E3 report, synthesis, formal note (T7, T8) and transfer note; the E4 scaffold, coverage, formal-floors and transfer notes; both E4 plans and tables; the E4A reflection; the E4 report and synthesis; the GT-P007 execution record.
- **Code:**
  - `gte0a.component_expressions` (templates);
  - `kernel.build_kernel` (a toggle's weight is the product of the factors of every satisfied rule instance);
  - `weights.alphabet_factors` (W4: weak = 2^±1, strong = 2^±2);
  - `gte0b.FAMILIES` (the E4 families);
  - `gte0a.stationary` (jump law, then the continuous law ∝ jump/R);
  - `gte4a.witness_census`, `e4_channels` (the orbit, activity, witness and chord fields);
  - `gt0.Scaffold`.

### Exact rate semantics, from the code

- **Path witness.** For slot e = (a,b), a path witness is an *ordered* triple (end, c, d) with end ∈ {a,b}, c, d ∉ {a,b}, c ≠ d, and (end,c) and (c,d) both present. Each satisfying instance multiplies the toggle once. So a slot has 2(N−2)(N−3) templates.
- **Closure witness.** A vertex c ∉ {a,b} with (a,c) and (b,c) present.
- **Rates, with w_e = path witnesses and t_e = closure witnesses of e in the current state:**

| Family (E4) | Formation rate F_e | Dissolution rate D_e | σ |
| --- | --- | --- | --- |
| NULL | 1 | 1 | 0 |
| PATHF weak_suppress | 2^(−w_e) | 1 | +ln 2 |
| PATHH weak_favour | 1 | 2^(w_e) | +ln 2 |
| CSPH | 4^(t_e) | 2^(w_e) | +ln 2 |
| PCOMP | 2^(w_e) | 2^(w_e) | 0 |
| CLOSEW | 2^(t_e) | 1 | 0 |

- **Held relations** have dissolution rate 0 (a `prohibit` rule). They start present, so they stay present.
- **The two clocks.**
  - *Continuous clock:* law π.
  - *Per-event clock:* the stationary jump-chain law ν(x) = π(x) q(x) / E_π[q], where q(x) is the total rate.

## 3. Evidence inventory and boundaries

| Claim | Source | Kind | Status after this audit | Limitation |
| --- | --- | --- | --- | --- |
| Floor formula, any held graph | `e4-formal-witness-floors.md` F1 | theorem | proof re-checked (§4) | holds for slots (p,s) with p a probe only |
| Only K2 is floor-free among connected references | F2 | theorem | re-checked | — |
| Per-slot constant factors leave every cycle affinity unchanged | F4 (generalises E3 T8) | theorem | re-checked | says nothing about stationary occupancy, jump law or event-order magnitudes |
| Chord adds state-dependent witnesses | F3 | theorem (count) + observation (occupancy) | count re-checked | chord occupancy is not derived |
| Event-order magnitudes move without any affinity change | F5 | explanation, not a theorem | — | no size prediction |
| What each contrast identifies | F6 | methodological table | **overstated (qualification Q-1 below)** | — |
| P3 middle out-attracts the ends; star centre out-attracts the leaves | GT-F60; tables | exact finite-model observation | values re-extracted: P3 0.288–0.365 against 0.141–0.224; star 0.363–0.373 against 0.085–0.093 | adaptive E4B; N ≤ 6; W4 only |
| P4 orbit differences with equal floors (PATHH, CSPH) | GT-F60, synthesis | observation | re-extracted: 0.128/0.159, 0.092/0.151; PATHF 0.146/0.155 | **negative control for a floor-only account** |
| Chord presence collapses the middle | GT-F64 | observation, **conditional** | — | conditioning is observational (Q-2) |
| Native raw gathering (K2, star) | GT-F61 | observation | — | mostly composition (GT-F62) |
| Standardised margins near zero, except CSPH under K2 | GT-F62 | observation | — | 18–31% of the NULL weight on low-mass strata at N=6 |
| Total floor does not predict the overall margin | GT-F63 | observation | — | two references only |
| Handover orientation across five references | GT-F65 | observation | — | magnitude unexplained |
| E3B gathering after neutralisation | GT-F57, E3 §7.6 | instrument-conditional observation | qualified by GT-F62 | not a grammar rule |

### Qualifications recorded here (append-only; earlier documents are not edited)

- **Q-1. F6 overstates what a within-cell orbit contrast identifies.**
  - `e4-formal-witness-floors.md` F6 says that the P3 and star orbit contrasts identify "the effect of the floor on where attachment goes". The E4 report likewise says that differences in size or crowding "cannot explain them".
  - The second statement is correct for global size, density, probe count and null geometry. But orbits also differ in topology, in held degree (which affects closure witnesses) and in state-dependent witnesses.
  - P4 shows orbit differences with **no** floor difference. So a within-cell contrast is a *matched observation*, not an intervention on the floor.
  - GT-P008 replaces "identifies the floor's effect" with "bounds the floor's share once the other channels are accounted for" (derivation note).
- **Q-2. GT-F64 ("the chord switches the middle off") is a conditional association.**
  - The conditioned occupancies (0.411 without the chord, 0.138 with it, PATHF P3 N=5) compare two strata of one stationary law.
  - They do not show that toggling the chord alone causes the difference: the strata also differ in the rest of the state.
- **Q-3. F4 is sometimes paraphrased as "the floor is orientation-neutral".** That is correct for cycle affinities only. The derivation note restates it precisely, as GT-P008 §3 A1 requires.

## 4. Residual confounds and live explanations

| Live account (GT-P008 §2) | Supported by | Contradicted or not distinguished by |
| --- | --- | --- |
| P1 permanent floor | Within-cell P3 and star contrasts; signs agree with the local factor | P4 residue; PCOMP (the floor is present but there is no CT sorting) |
| P2 state-dependent witnesses | The P3 chord strata; "other" witness means differ by orbit | Conditioning is not intervention |
| P3 topology / orbits | P4 residue; CSPH closure reads held degree | Not separable from P2 in the published data |
| P4 kinetics / clock | PATHF and PATHH share every local ratio yet differ in occupancy (GT-F17, P4 residue) | — |
| P5 composition | Raw against standardised margins | Overlap limits at N=6 |
| P6 imposed reference | Every source/probe asymmetry is defined relative to H | No FREE comparison of source-like motifs |
| P7 other | — | — |

## 5. Exposure and permitted analyses

- **All E4A and E4B data are fully exposed.** They were read during GT-P007 and in the E4A reflection, so every GT-P008 analysis of them is **post hoc and explanatory**. None is a preregistered test or independent confirmation.
- **No unopened cells are used.**
- **Permitted (GT-P008 §0):**
  - reading published tables;
  - pure algebra;
  - post hoc derived quantities from published tables;
  - proof-verification fixtures on synthetic factors or logically necessary small constructions;
  - unit and CI tests.
- **Not done:** any E5 cell; any new N=7 or FREE N=7 computation; any grade sweep; any rerun of an E4 cell presented as confirmation.

## 6. Definitions of the secondary quantities (fixed 2026-10-15, before computation)

All quantities are per cell and per source orbit O. Every slot in O is equivalent under the held graph's automorphisms, so slot-level and per-slot orbit quantities coincide. "occ" is `attachment_occupancy_per_slot`; "act" is `attachment_activity_per_slot` (the published fields).

- **D1. Extraction checks.**
  - NULL orbit occupancy is 0.5 in both clocks.
  - PCOMP continuous-time orbit occupancy is 0.5.
  - CLOSEW orbit occupancy in both clocks is recomputed **independently** from the exact Gibbs law π ∝ 2^(#triangles) over free configurations (held relations present). The jump law is ν ∝ π·q.
  - Selected GT-F60 values are re-extracted.
  - A mismatch above 1e-9 (law-level) is reported, not adjusted.
- **D2. Balance check (continuous clock).**
  - The stationary formation flux J_O equals the dissolution flux, so J_O = act/2.
  - Implied checks: PATHF act = 2·occ (D = 1); PATHH act = 2·(1 − occ) (F = 1).
  - Clock consistency: jump act = continuous act / `mean_rate_ct`.
- **D3. Exact conditional rate means (continuous clock).**
  - F̄_O = E_π[F_e | x_e = 0] = J_O / (1 − occ).
  - D̄_O = E_π[D_e | x_e = 1] = J_O / occ.
  - So occ/(1 − occ) = F̄_O / D̄_O (derivation note, theorem S1).
- **D4. Floor share of an orbit contrast.**
  - For two orbits L (lower floor) and H (higher floor) in one cell: Δ = log odds_L − log odds_H.
  - The floor term is Δf·ln 2, where Δf = floor_H − floor_L, for PATHF (through F), PATHH and CSPH (through D). It is 0 for NULL and CLOSEW (no path factor) and for PCOMP, where the floor enters F and D equally and cancels.
  - The residue is Δ minus the floor term.
  - The floor share is (floor term)/Δ, reported only when |Δ| > 0.05. It is undefined, and reported as such, when Δ is near zero or of the opposite sign.
- **D5. Mean sojourns (continuous clock).** Present sojourn τ+ = occ/J_O; absent sojourn τ− = (1 − occ)/J_O. These are exact stationary renewal means, not exponential holding times.
- **D6. First-order (weak-coupling) coefficients (pure algebra, no data).**
  - κ_O = d(log odds)/dε at ε = 0, where every factor is written as e^(g·ε) with g its grade (weak ±1, strong ±2). The published cells have ε = ln 2.
  - Under the NULL product law (held relations present, free relations independent with probability ½):
    - PATHF and PATHH: κ = −E_0[w_e];
    - CSPH: κ = 2E_0[t_e] − E_0[w_e];
    - PCOMP and NULL: κ = 0;
    - CLOSEW: κ = E_0[t_e].
  - The **first-order prediction** for an orbit contrast is ln 2·(κ_L − κ_H). It is compared with Δ in sign and size. The comparison is post hoc. A theorem guarantees only the derivative at ε = 0, not the value at ε = ln 2.
- **D7. Chord strata (P3 only).**
  - Published conditional orbit occupancies are converted to log odds within each stratum, with no causal reading.
  - The star and P4 tables condition on only one of their chords, so their strata are reported as partial.
- **D8. Composition (collation only).** The published raw, normalised and standardised margins and overlap diagnostics are collated in one table. No new standardisation is computed.

Uncertainty: these are exact finite-chain values with numerical error ≤ 1e-12 in the stationary residual. There is no sampling error.

## 7. Addendum after computation (2026-10-15; sections 1–6 above unchanged)

- **D1–D8 were computed as defined.** No definition was changed after the data were read. The extraction checks all passed (largest deviation 2e-14).
- One check was added after the definitions were fixed: published NULL witness means against the S4 closed form (largest deviation 3e-15). It is an extraction check, not a scientific quantity.
- **Q-4. Chord occupancy depends on the family.** The GT-P007 phrasings "the chord is rarely present" (E4 report) and "under σ > 0 path rules the held path suppresses the chord" (GT-F64) are correct for PATHF and PATHH (0.23–0.29). Under CSPH the P3 chord is at 0.45–0.53, close to NULL's 0.5, because closure rewards it. Recorded here; the earlier documents are not edited.
