# E5B definitions, controls and feasibility (GT-P010)

*Deliverable 2 of GT-P010. Written before freezing, and before any E5B observable of an N=5 or N=6 scientific cell was computed.*
- *Implementation: `constraint-lab/src/rs_constraint_lab/gtrenew.py` (observables, NK) and `gte5b.py` (round).*
- *Proof fixtures: `constraint-lab/tests/test_gtrenew.py` (synthetic chains, N ≤ 4 kernels, and a synthetic N = 5 rule that is not one of the twelve laws).*
- *Audit: `docs/gt-p010-hub-and-e5b-audit.md`. E5A definitions T1–T8 (`docs/e5-definitions-and-null-construction.md`) are reused unchanged.*

Labels: **[T]** theorem with proof inside the finite model; **[D]** definition; **[L]** limitation. Nothing here is a physical claim. An anchor is an analyst's index; a renewal is continuity of an operational property, not a body, a mobile reference or identity of the anchor.

## 1. Setting (unchanged from E5A)

FREE, N ∈ {5, 6}, M = C(N,2) slots, the GT order-2 single-toggle grammar with W4 factors, the twelve laws of E5A (NULL; PATHF weak_suppress; PATHH weak_favour; CSPH strong_favour+weak_favour; CLOSEW weak_favour; PCOMP weak_favour+weak_favour). All rates are positive, the chain is irreducible on {0,1}^M, π is the CT stationary law and ν = πq/E_π[q] the jump-chain law. Episodes are E5A's stationary **entrance-sampled (Palm)** episodes of a predicate set A: start at Aᶜ → A, end at the next A → Aᶜ.

Predicates (E5A, primary anchors; relabelled anchors are the image under v ↦ N−1−v):

| Predicate | Anchor | Holds when | Participants of x |
| --- | --- | --- | --- |
| F_TRI({0,1}) | edge 01 | 01 present and some c ∉ {0,1} has 0c and 1c present | C(x) = {c : x_0c x_1c = 1} |
| F_STAR(0) | vertex 0 | deg(0) ≥ 3 | neighbours of 0 |
| F_2PATH(0) | vertex 0 | deg(0) ≥ 2 | neighbours of 0 |

The threshold (participants needed) is 1, 3 and 2 respectively. For F_TRI the anchor edge is a fixed part of the predicate and is never "replaced".

## 2. Clocks

E5A's L_CT = π(A)/J_A and L_JT = E_π[q 1_A]/J_A are retained exactly.

**Anchor-local event count [D].** LOCAL is the set of slots incident on an anchor vertex: the N−1 slots at c for F_STAR and F_2PATH, and the 2N−3 slots at 0 or 1 for F_TRI. It is fixed by the predicate, never chosen from data. With q_loc(x) = Σ_{e∈LOCAL} W(x,e),

  L_local(A) = Σ_{x∈A} π(x) q_loc(x) / J_A.

**T9 [T].**
1. L_local is the mean number of anchor-local events per entrance episode, counting the exit event when it is local and not the entry event. *Proof:* as T2, restricted to local transitions out of A-states; the entry transition leaves an Aᶜ state and is not counted. ∎
2. 0 < L_local ≤ L_JT, with equality iff every event from A is local.
3. **Every exit from a flexible predicate is local.** F_STAR/F_2PATH depend only on deg(c), which only slots at c change. F_TRI fails only when 01 is removed or the last completer loses a leg 0c or 1c; all are incident on 0 or 1. So exit_local_share = 1 (a frozen check).
4. Under NULL, q_loc ≡ |LOCAL|, so L_local = |LOCAL| · L_CT: (N−1)L_CT for the vertex predicates and (2N−3)L_CT for F_TRI (analytic control; test `test_null_local_count_is_local_slots_times_ct_lifetime`).
5. Multiplying every rate by c > 0 leaves L_local, L_JT and every hitting probability below unchanged (T3; test `test_event_count_statistics_are_scale_free`).

**[L]** L_local is a count in the same jump trajectory. It is not a duration, not an independent Markov time axis, and it does not remove kinetic heterogeneity *at* the anchor: a fast-flickering neighbourhood inflates it. Reported beside it: L_CT, L_JT, the local share of events in A, the mean local hazard Σ_A π q_loc / π(A), entries per unit time, prevalence in both clocks, and the local hazard conditional on the edge count k.

## 3. Entry sets and three kinds of change

**Entrance weights [D].** μ_in(y) = Σ_{x∉A, x⊕e=y} π(x) W(x,e) for y ∈ A; Σ μ_in = J_A (T1).

**Entry participants [D].** S0(y) is the participant set of the entrance state y, immediately after entry. For F_STAR an entry always crosses deg 2 → 3, so |S0| = 3. For F_2PATH an entry crosses deg 1 → 2, so |S0| = 2. For F_TRI, |S0| ∈ {1, …, N−2}: an entry by forming 01 inherits every existing completer; an entry by a new completer has |S0| = 1.

Within an episode, all quantities are evaluated **only in A-states**: a participant lost in the exit transition is not a departure, and renewal must be reached while the predicate holds.

1. **Gross turnover Ω [D]** (E5A, reproduced as a check): eligible participant-changing internal toggles per episode, rapid returns included.
2. **Distinct departures [D].** For s ∈ S0(y), d_s(y) = P_y(an A-state with s not participating is reached before exit). The reported quantities are E[Σ_{s∈S0} d_s] per episode and its fraction of Σ μ_in |S0|. A departed participant may return; this detects change, not replacement.
3. **Complete renewal [D].** P_full_renewal = Σ_y μ_in(y) r(y) / J_A, where r(y) = P_y(reach x ∈ A with participants(x) ∩ S0(y) = ∅ before exit). The qualifying participants then all come from outside S0. This is stronger than "every original left at some time", and it is not unlabelled identity or replacement of the anchor.
4. **Flicker [D], reported separately.** For eligible internal transitions x → y = x⊕e (both in A):
   - reversal_next_event = Σ π(x)W(x,e) · W(y,e)/q(y) / Σ π(x)W(x,e): the probability that the next event of the full process toggles e back;
   - reversal_next_local_event: the same with q_loc(y), the next anchor-local event;
   - reversals per episode = Σ π(x)W(x,e) W(y,e)/q(y) / J_A.

   No "net Ω" is formed by subtraction. Under NULL the two probabilities are exactly 1/M and 1/|LOCAL| (test `test_flicker_null_closed_form_n4`).

**Decision on the optional durable-renewal filter.** Not attempted in E5B. A filter that tracks survival after renewal needs a second observer set (the renewed participants) and roughly doubles the solve count. It is recorded as a deliberate omission, not as a negative result.

## 4. Structural feasibility

**T10 [T].** Let K = N − |anchor vertices| be the number of candidates and k the threshold. Complete renewal from an entry set of size s is possible iff K − s ≥ k. The largest number of entry participants simultaneously absent while the predicate holds is max(0, min(s, s + (K − s) − k)).

*Proof.* A renewed state needs k current participants, all outside S0, from K − s candidates. Conversely, if K − s ≥ k, the state in which exactly k outside candidates participate (and the anchor edge is present for F_TRI) is in A and is reachable by single toggles inside A. Positive rates make every such path have positive probability, provided toggles can be ordered to stay inside A: first add the outside participants, then remove the originals. The partial bound counts the minimum number of originals that must remain. ∎

| Predicate | N | K | s | Complete renewal | Max originals absent |
| --- | --- | --- | --- | --- | --- |
| F_STAR | 5 | 4 | 3 | **STRUCTURALLY_IMPOSSIBLE** | 1 of 3 |
| F_STAR | 6 | 5 | 3 | **STRUCTURALLY_IMPOSSIBLE** | 2 of 3 |
| F_2PATH | 5 | 4 | 2 | feasible | 2 |
| F_2PATH | 6 | 5 | 2 | feasible | 2 |
| F_TRI | 5 | 3 | 1–2 feasible; 3 impossible | entry-class dependent | |
| F_TRI | 6 | 4 | 1–3 feasible; 4 impossible | entry-class dependent | |

For every cell the report gives the fraction of entry episodes in feasible classes, renewal conditional on feasibility, and unconditional renewal. Where feasibility is zero, the status is `STRUCTURALLY_IMPOSSIBLE` with no estimate. **That is not evidence that the rules fail to maintain a star.** For F_STAR the informative channel is **maximal partial renewal**: P(reach an A-state with N−4 originals simultaneously absent, before exit).

## 5. Computation

**Hitting problems [D].** Each quantity in §3 is h(x) = P_x(hit T before leaving A) for a target T ⊂ A on the **jump chain**. These probabilities are the same in CT and in jumps, so they need no clock. With B = A ∖ T, solve (I − P_BB) h_B = P_{B,T} 1.

**Canonical frames [T].** Let σ fix the anchor vertices. Covariance (W(σx,σe) = W(x,e)) and σ(participants(x)) = participants(σx) give r_{S0}(y) = r_{σS0}(σy), and the same for departures. So one canonical entry set per size (the first s candidates) suffices. Each entry state is mapped to it by a σ fixing the anchor; for departures σ sends the tracked member to the first canonical slot. The observer (S0, the target sets) is an analyst's bookkeeping: **no rule reads it, and no history register enters the dynamics** (8G gate not engaged).

**Solver policy [D].**
- BiCGSTAB (`gtpersist.bicgstab`): relative residual 10⁻¹², cap 20,000 iterations, 600 s per solve.
- A dense direct solve as an independent route whenever |B| ≤ 4,096, with the maximum difference reported.
- h must lie in [0, 1]; violations are reported.
- A solve not reaching 10× tolerance is `UNRESOLVED`. The channel keeps that status with its diagnostics, and nothing is substituted under the same name.

**Verification on fixtures.**
- An independent augmented-observer route propagates (x, S0) directly, with no canonical map and no BiCGSTAB. It agrees within 10⁻⁹ (N=4: NULL, PCOMP, CLOSEW) and 10⁻⁸ (synthetic N=5 rule, all three predicates).
- A Monte Carlo trajectory check (40,000 episodes, N=4 NULL) agrees with L_local (2%) and renewal (0.006 absolute).
- Dense versus iterative differences on fixtures are at most about 10⁻¹⁶.

**Cost.** Measured on fixtures and published NULL N=6 (timing only): about 9 s per law per anchor set. Each item computes target, ND and NK, each with primary and relabelled anchors.

## 6. The NK comparator

**Construction [D].** Fixed before E5B data are applied:
1. p_k = Σ_{|x|=k} π(x), the target CT edge-count profile.
2. The target's upward layer flux J[k,k+1] = Σ_{|x|=k} π(x) Σ_{e∉x} W(x,e), a sum of positive terms.
3. b_k = J[k,k+1] / ((M−k) p_k) for every absent slot, and d_{k+1} = J[k,k+1] / ((k+1) p_{k+1}) for every present slot.

No subtraction of nearly equal terms is used. Any zero bin or zero flux makes NK `UNRESOLVED` for that item; bins with p_k < 10⁻¹² are flagged with their mass; nothing is smoothed.

**T11 (NK properties) [T].**
1. *Covariance:* rates read only |x| and whether e is present.
2. *Reversibility and law:* with π_NK(x) = p_|x| / C(M,|x|), π_NK(x) b_k = J[k,k+1] / (C(M,k)(M−k)) and π_NK(x+e) d_{k+1} = J[k,k+1] / (C(M,k+1)(k+1)). These are equal because C(M,k)(M−k) = C(M,k+1)(k+1). So detailed balance holds, π_NK is stationary, and its edge-count profile is exactly p_k.
3. *Layer traffic:* NK's upward flux from layer k is p_k (M−k) b_k = J[k,k+1], and its downward flux from k+1 is p_{k+1}(k+1) d_{k+1} = J[k,k+1]. The target's downward flux equals its upward flux by stationarity (layer balance across the cut between k and k+1). So **every adjacent-layer stationary flux matches**.
4. *Rates by layer:* every toggle changes k by ±1, so Σ_{|x|=k} π q = J[k,k+1] + J[k−1,k] in both processes. Hence E[q | k] matches, and so do the mean CT rate and the **jump-clock density profile** ν_k = p_k E[q|k] / E_π[q]. ND matches neither of the last two in general.
5. *NULL fixed point:* NULL has p_k binomial and J[k,k+1] = p_k (M−k), so b = d = 1 and NK = NULL.

*Proof.* Items 1–5 are the computations shown. ∎ Tests: `test_nk_null_fixed_point`, `test_nk_propositions_on_heterogeneous_uniform_law` (the analytic law agrees with an independent solve; p, fluxes, E[q|k], mean rate and jump density agree within 10⁻¹⁰), `test_nk_zero_bin_is_unresolved`.

**[L] What NK does not match:**
- the within-layer arrangement of rates (NK has none: q depends on k only);
- anchor-local activity given the configuration;
- shape correlations;
- multi-time structure.

It is a control for the declared projection onto k, not a universal "fair kinetics" counterfactual. It uses target generator data to define a projection: an adaptive, declared comparison, not a blind one.

**Expected PCOMP behaviour [L, stated before execution].** PCOMP's law is uniform, so p_k is binomial, but its within-layer rates are heterogeneous. NK(PCOMP) therefore differs from N0 and from ND(PCOMP) in its layer rates. If PCOMP still exceeds NK, the excess is attributable to within-layer heterogeneity, which NK does not match. If it does not, ND's failure was a layer-traffic effect.

**Diagnostics, not constraints.** For target and comparators: the within-layer weighted standard deviation and range of q (two-pass, no cancellation), and the anchor-local hazard given A and k.

## 7. Comparators, together

| Comparator | Matches | Does not match |
| --- | --- | --- |
| N0 (NULL, same N) | nothing about the target | density, activity |
| ND (E5A T6, unchanged) | CT density profile, CT mean rate | JT density, layer traffic, within-layer rates |
| NK (new) | CT density profile, every adjacent-layer flux, E[q|k], CT mean rate, JT density | within-layer rates, local activity, correlations |

No CL matched-source control is implemented (audit §4): the CL construction projects out a hidden history coordinate at event epochs, and GT has none. A look-alike under CL's name would misstate the scope.

The optional anchor-local sensitivity analysis is not attempted, to keep the round bounded.

## 8. Live accounts and what discriminates them

| Account | Readouts that bear on it |
| --- | --- |
| H1 genuine replacement-supported organisation | renewal above all three comparators in feasible classes; departures above comparators without flicker inflation; L_local above comparators |
| H2 kinetic heterogeneity | target above ND but not above NK; within-layer q dispersion large; PCOMP pattern |
| H3 prevalence / density composition | high π(A) and JT prevalence; long L with low renewal; NK and ND reproduce the effect |
| H4 flicker | high reversal probability; Ω large but departures and renewal small |
| H5 remote-event clock | L_JT above comparators while L_local is not; low local share |
| H6 null or mixed | effects change sign across comparator, clock, family or N |
| H7 surprising structure | anything not anticipated, reported as found |

No readout is a success criterion, and no scalar score is formed.

**Prospective interpretation.**
- *Lens B:* each result is a property of the grammar under the stated observer and comparator.
- *Lens A:* renewal in a labelled predicate would show that an operational property can survive turnover of all its initial partners. It would not show an emergent reference, interaction, displacement or gravity.

A zero renewal for F_STAR at N ≤ 6 is structural non-identifiability, not dynamical falsification.

## 9. Frozen checks (to be written into the plan)

- **Replication of published E5A target laws and E5A episode values** (L_CT, L_JT, Ω, π(A)) within max(10⁻¹⁰, 10⁻⁸·|value|). This is a replication, not evidence.
- **N0:** E5A closed forms (10⁻⁹), and L_local = |LOCAL|·L_CT (10⁻⁹).
- **ND:** E5A construction unchanged; ND law and rates as in E5A (10⁻¹²).
- **PCOMP:** CT law uniform (10⁻⁹ relative per state).
- **NK:**
  - detailed balance ≤ 10⁻¹² and global balance ≤ 10⁻¹⁰;
  - p_k, adjacent fluxes, E[q|k], mean rate and JT density equal the target's (relative ≤ 10⁻⁹, absolute 10⁻¹² for the JT profile);
  - every rate positive;
  - rare bins flagged.
- **Every law:**
  - entry flux = J_A (10⁻⁹);
  - Σ entrance weights = J_A;
  - L_local ≤ L_JT;
  - exit_local_share = 1 (10⁻¹²);
  - relabelled anchors agree (10⁻⁹ relative on L_local, departures, renewal, flicker);
  - h ∈ [0,1] (violation ≤ 10⁻¹⁰);
  - dense versus iterative ≤ 10⁻⁹ where dense is run;
  - all solves resolved, or recorded `UNRESOLVED`.
- **F_STAR:** renewal status `STRUCTURALLY_IMPOSSIBLE` at both sizes.
- **Comparator status:** E5A's two numerically qualified CT hub-lag channels are not part of E5B and are not reclassified.
