# E5C definitions: durable renewal over anchor-local events (GT-P011)

*Written before freezing, and before any E5C quantity of an N=5 or N=6 scientific cell was computed.*
- *Implementation: `constraint-lab/src/rs_constraint_lab/gtdurable.py` (observer) and `gte5c.py` (round).*
- *Proof fixtures: `constraint-lab/tests/test_gtdurable.py` (N ≤ 4 kernels; synthetic neighbourhood rules at N = 5, 6 that are not GT families). Runner plumbing: `tests/test_gte5c.py`.*
- *E5A (T1–T8) and E5B (T9–T11) definitions are reused unchanged.*

Labels: **[T]** theorem; **[D]** definition; **[L]** limitation. An anchor, entry set and renewal are analyst observers. **No rule reads them** (8G gate not engaged). Nothing here is a body, a movement or a physical time.

## 1. Setting

The 12 E5A/E5B laws, FREE N ∈ {5, 6}, positive rates, jump chain P = W/q. Predicates (E5B, primary anchors; relabelled anchors are the image under v ↦ N−1−v):
- **F_2PATH(0):** deg(0) ≥ 2; participants are the neighbours of 0; threshold k = 2; candidates K = N−1.
- **F_TRI({0,1}):** 01 present and ≥ 1 completer; participants are the completers; threshold k = 1; candidates K = N−2.

F_STAR is excluded: complete renewal is impossible at N ≤ 6 (T10), and a durability notion for partial renewal is not defined in this round.

## 2. Episodes, entry sets and first renewal

**[D]** A Palm entrance-sampled episode starts at the transition Aᶜ → A, with entry weights μ_in (Σ μ_in = J_A). S0 is the participant set of the entry state. R(S0) = {x ∈ A : participants(x) ∩ S0 = ∅}, and B(S0) = A ∖ R(S0).

**Canonical frames [T, from E5B §5].** Let σ fix the anchor and map S0 to the canonical set (the first s candidates). Covariance gives the same law for every functional of the observed episode. Mapping every size-s entry state into the frame produces a single row vector μ_s, and **every E5C quantity is linear in μ_s**.

**T12 (first-renewal law) [T].** The unnormalised law of the state at which R is first entered, before exit, is

  φ = μ_s|_B (I − P_BB)⁻¹ P_{B→R}.

*Proof.* Entry states lie in B, since S0 participates at entry. (I − P_BB)⁻¹ sums the expected visits to each B-state before leaving B. ρ(P_BB) < 1 because the finite irreducible chain leaves B almost surely. P_{B→R} is the one-step flow into R. Paths leaving B into Aᶜ or anywhere else are not counted. ∎

- R0_s = Σφ / Σμ_s, and the pooled R0 = Σ_s Σφ_s / J_A. This **replicates E5B's renewal probability**, a frozen check.
- φ is a *first-hitting* law. The diagnostic L1(φ/Σφ, π|_R/π(R)) is reported; it is nonzero on the synthetic fixture, and the independent route confirms that the result follows φ, not π|_R (`test_first_hit_law_differs_from_stationary_restriction`).

## 3. What can change between anchor-local events

LOCAL is the set of slots incident on an anchor vertex (E5B T9).

**T13 (remote closure) [T].** From any x ∈ R(S0), a toggle of a non-local slot leads to a state in R(S0).
- *Proof.* For F_2PATH, participation and deg(0) depend only on slots at 0. For F_TRI, participation of v is x_0v·x_1v, and the anchor edge is 01. Both are local. A non-local toggle changes none of these, so A-membership and participation are unchanged. ∎
- **Frozen check:** count remote transitions from R that leave R; the count must be exactly 0.

**[L]** T13 says remote events cannot *end* durability. It does **not** let them be discarded: they change the state and therefore the rates of later local events.

**Local-event kernel [T].** Split P on R into P_rem (remote toggles; by T13 they map R → R) and P_loc (local toggles, landing anywhere). Every state has q_loc > 0, because rates are positive and LOCAL is nonempty. So every row sum of P_rem is at most 1 − min(q_loc/q) < 1, and

  K = Σ_{j≥0} P_rem^j P_loc = (I − P_rem)⁻¹ P_loc

is the exact law of the state just after the next local event, summed over any number of intervening remote jumps.

## 4. Durable renewal

**[D]** D_h holds when, from first renewal, each of the next h local events leaves the chain in R(S0). By T13 no exit or return happens between local events, so this is the full requirement.
- U_h = Σ_s Σ_y φ_s(y) (K_RR^h 1)(y) / J_A, with U_0 = R0;
- C_h = U_h / R0;
- per class: U_h,s, C_h,s, and the entry weight Σμ_s / J_A.

**T14 (post-renewal feasibility) [T].** For a vertex predicate with threshold k, K candidates and entry size s:
- a renewed state has d participants, all outside S0, with k ≤ d ≤ K − s;
- a local event either adds a participant (an outsider, staying in R, or an original, which is a return) or removes one (d − 1 < k means exit).

Staying in R is therefore possible iff K − s > k. For F_2PATH, s = 2 and k = 2:
- **N = 5 (K = 4):** K − s = 2 = k, so every local event from R leaves R, and **C_h = 0 for all h ≥ 1 structurally**;
- **N = 6 (K = 5):** survival is possible.

The implementation detects this generally, by counting local transitions R → R, and labels the class `STRUCTURALLY_ZERO_FOR_H_GE_1` rather than reporting a measured zero. It was found on the synthetic N = 5 rule; it is law-independent combinatorics. For F_TRI, a local toggle of a leg of a non-completing vertex can stay in R, so survival is feasible for every renewable class at N = 5 and N = 6.

**T15 (causes after renewal) [T].** From φ the chain leaves R almost surely (R is transient). The first transition out of R goes either to A ∖ R (an original returns while the property holds) or to Aᶜ (exit). These are exclusive and exhaustive:

  P(return before exit) + P(exit before return) = 1,

computed from φ (I − P_RR)⁻¹ P_{R→·}. "Immediate original return" and "immediate exit" are the same split applied to the next local event, using K. They differ from E5B's `reversal_next_event`, which asks whether the next event toggles the same slot back.

**Monotonicity [T].** D_{h+1} ⊂ D_h, so U and C are non-increasing in h (frozen check). U_h,s = R0_s · C_h,s holds by construction (frozen check).

## 5. Entry composition

- Every quantity is reported per entry-set size, with its entry weight.
- For F_TRI, size 1 (where renewal equals a single departure, E5B GT-F87) is reported **separately** from the pooled size ≥ 2 classes.
- Classes infeasible by T10 are `STRUCTURALLY_IMPOSSIBLE`.

A pooled change can come from a change in composition rather than within-class survival, so pooled and within-class values are always shown together.

## 6. Comparators

N0, ND (E5A T6) and NK (E5B T11) are unchanged. NK matches the CT edge-count profile, every adjacent-layer flux, E[q|k], the mean rate and the jump-clock density. It does **not** match within-layer arrangement, anchor-local activity, shape correlations or multi-time structure. Any effect beyond NK may be account D4, local kinetics, which is still a property of the finite process and not of a self-maintaining object. No comparator is tuned in this round.

## 7. Clock

The clock is the anchor-local event count within the same jump trajectory: remote jumps are integrated (§3), not dropped. Uniform rescaling of all rates leaves every E5C quantity unchanged; a non-uniform change of remote rates alters C_h through K (`test_uniform_rescaling_invariant_and_remote_change_matters`). No continuous-time post-renewal channel is computed; this omission is declared, not a negative result.

## 8. Verification on fixtures (before freezing)

| Check | Fixture | Result |
| --- | --- | --- |
| Independent route: propagating (x, phase, local count) through the plain jump chain from every original entry state, with no canonical frame, resolvent or kernel | N = 4 NULL, PCOMP, CLOSEW (F_TRI); synthetic N = 5 rule (F_2PATH, F_TRI) | U_h agree within 1e-8 (N = 4) and 1e-7 (N = 5) |
| Monte Carlo trajectories | N = 4 NULL F_TRI, 60,000 episodes | U_0, U_1, U_2 agree within 0.004 |
| R0 replicates E5B renewal | the same fixtures | within 1e-10 |
| T13, T15, monotonicity, U = R0·C, relabelling, structural labels | synthetic N = 5 rule; N = 4 | hold exactly or within 1e-9 |
| T14 labels | synthetic rules at N = 5 (zero) and N = 6 (computed) | as predicted |

**Cost** (synthetic N = 6 rule only): about 21 s per law for both predicates and both anchors; peak 346 MB; at most 34 solver iterations.

## 9. Live accounts

| Account | Readouts |
| --- | --- |
| D1 durable reconstruction | U_h and C_h above N0, ND and NK at h = 2, 4, within entry classes, at both sizes |
| D2 flicker-assisted renewal | high immediate original return; C_1 low; return before exit high |
| D3 layer traffic | NK reproduces target U_h and C_h |
| D4 local kinetics | target differs from NK; local share at first renewal differs |
| D5 composition | pooled differences that vanish within classes; F_TRI size-1 dominance |
| D6 clock dependence | sign changes between the E5B lifetime clocks and local-event durability |
| D7 null or structural | STRUCTURALLY_IMPOSSIBLE or STRUCTURALLY_ZERO_FOR_H_GE_1 cells; ties; unresolved channels |

No readout is a success criterion, and no scalar score is formed.
