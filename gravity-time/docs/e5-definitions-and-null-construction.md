# E5 definitions and null construction (GT-P009)

*Deliverable 2 of GT-P009. Written before freezing, and before any E5A observable of an N=5 or N=6 cell was computed.*
- *The implementation is `constraint-lab/src/rs_constraint_lab/gtpersist.py` (observables) and `gte5a.py` (round).*
- *Proof fixtures are in `constraint-lab/tests/test_gtpersist.py` and `test_gte5a.py`; they use synthetic chains and N ≤ 4.*
- *The audit and its decisions D-1 to D-11 are in `docs/e5-coverage-and-definition-audit.md`.*

Labels:
- **[T]** a theorem with proof, inside the finite model;
- **[D]** a definition;
- **[L]** a stated limitation.

Nothing here is a physical claim. A motif is not a body, an edge toggle is not movement, and a lifetime is not physical time.

## 1. Setting

- **States.** States x ∈ {0,1}^M, with M = C(N,2) pair slots. The model is FREE (no held slot), N = 5 or 6, and uses the GT order-2 single-pair-toggle grammar with W4 factors.
- **Rates.** The generator rate of toggling slot e in state x is W(x,e) > 0. Every rate is positive in all six family-grades, because W4 factors are powers of 2 and no prohibit grade is used. q(x) = Σ_e W(x,e).
- **Ergodicity [T].** Positive rates on the hypercube make the chain irreducible. There is a unique CT stationary law π. Label covariance (W(σx, σe) = W(x,e) for every vertex permutation σ) makes π exchangeable.
- **Clocks [D].**
  - **CT:** time in model units, stationary law π.
  - **Jump time (JT):** the embedded chain P(x, x⊕e) = W(x,e)/q(x), with stationary law ν(x) = π(x) q(x) / E_π[q].
  - Both are model conventions.

## 2. Predicates [D]

A predicate P defines a set A = {x : P(x)}.

**Intact (fixed-instance, non-induced).** The named relations must be present. All others are free.

| Name | Instance (D-1) | Required slots |
| --- | --- | --- |
| I_TRI(a,b,c) | (0,1,2) | ab, bc, ac |
| I_STAR(c; a,b,d) | (0; 1,2,3) | ca, cb, cd (leaf–leaf free) |
| I_2PATH(a,b,c) | (1,0,2) | ab, bc (here 01, 02; the chord 12 free) |

**Flexible (anchored organisation).** The anchor is an observation index, not a dynamical privilege.

| Name | Instance | Condition | Eligible turnover toggle (D-5) |
| --- | --- | --- | --- |
| F_TRI(ab) | {0,1} | ab present and ∃ c ∉ {a,b} with ac, bc present | slot ac or bc (c ∉ {a,b}) whose other leg is present, so that the completer set C(x) = {c : x_ac x_bc = 1} changes, with x ∈ A and x⊕e ∈ A |
| F_STAR(c) | 0 | deg(c) ≥ 3 | a slot incident on c, with x, x⊕e ∈ A |
| F_2PATH(c) | 0 | deg(c) ≥ 2 | a slot incident on c, with x, x⊕e ∈ A |

**Limitations of the predicates [L].**
- F_STAR ⊂ F_2PATH: these are nested, not competing species.
- An anchored centre that persists is still a *labelled* vertex. It is not an unlabelled structure that moves.
- The predicates are deliberately broad. F_2PATH(0) is true in most states of a dense law.

**Covariance [T].**
- For every predicate and permutation σ: x ∈ A(instance) ⇔ σx ∈ A(σ·instance), and the eligible-toggle set maps the same way.
- With an exchangeable π and covariant W, every episode quantity of the instance therefore equals that of σ·instance.
- E5A recomputes every predicate on the image under v ↦ N−1−v and requires agreement within 10^−9 relative.
- Test: `test_relabelled_instances_agree`.

## 3. Episodes and stationary flux

**[D]** An episode of A begins at a transition Aᶜ → A and ends at the next transition A → Aᶜ. Every mean below is over **entrance-sampled** episodes: the Palm distribution of the stationary point process of entries. It is not over a state drawn from π restricted to A, which would length-bias the episodes.

**Fluxes [D].**
- Exit flux: J_A⁺ = Σ_{x∈A} Σ_{e: x⊕e∉A} π(x) W(x,e).
- Entry flux: J_A⁻ = Σ_{x∉A} Σ_{e: x⊕e∈A} π(x) W(x,e).

**T1 (boundary balance) [T].** J_A⁺ = J_A⁻ =: J_A.
- *Proof.* Sum the global balance π(y) q(y) = Σ_x π(x) W(x→y) over y ∈ A. Flows inside A appear on both sides and cancel. What remains is exactly the outflow from A equal to the inflow into A. ∎
- E5A computes both sides independently and requires agreement within 10^−9. This is a numerical check on π, not a new observable.

**T2 (mean lifetimes) [T].** For an ergodic chain with 0 < π(A) < 1 and J_A > 0:
- L_CT(A) = π(A) / J_A;
- L_JT(A) = E_π[q 1_A] / J_A = ν(A) / (J_A / E_π[q]).
- *Proof.*
  - By the ergodic theorem, over [0, T] the time spent in A is π(A)T + o(T), and the number of entries is J_A T + o(T). The entries are counted by the stationary transition rate across the boundary.
  - Since episodes alternate with off-episodes, the mean episode duration is the ratio.
  - In the jump chain, the fraction of steps taken from A is ν(A), and the number of entries per step is J_A / E_π[q] (the jump chain makes E_π[q] steps per unit CT time).
  - L_JT therefore counts the steps taken from A states per episode, including the exit step (D-3). ∎
- Consequences:
  - internal steps per episode = L_JT − 1 (an identity, checked);
  - the off-episode means are (1 − π(A))/J_A and (E_π[q] − E_π[q 1_A])/J_A;
  - the entry-to-entry recurrence is 1/J_A (CT) and E_π[q]/J_A (JT);
  - exit-to-next-entry is the off-episode mean.

  These are **algebraically dependent** summaries of (π(A), E_π[q 1_A], J_A). They are not independent confirmations.

**T3 (rescaling) [T].** If every rate is multiplied by c > 0, then:
- π and ν are unchanged, and J_A scales by c;
- L_CT scales by 1/c, while L_JT, Ω and ρ_JT are unchanged;
- ρ_CT is unchanged, because both of its lifetimes scale by 1/c.

Test: `test_uniform_rate_rescaling`.

**Zero cases [D].**
- π(A) = 0 is classified as "absent", and A equal to the whole space as "whole_space".
- J_A = 0 with 0 < π(A) < 1 is "closed_or_absorbing".
- None of these produces a lifetime. All E5A chains have positive rates, so all are expected to be "ergodic_episodes", and that is checked.
- Tests: `test_closed_set_and_whole_space_classification`, `test_small_n_degeneracies`.

**Entrance versus occupation [T].**
- Let h_CT(x) be the expected time to leave A starting from x ∈ A, and h_JT(x) the expected number of steps from A states. They solve the killed systems (I − P_AA) h = 1/q and (I − P_AA) h = 1.
  - Then the entrance mean, Σ μ_in(y) h(y) with μ_in(y) ∝ Σ_{x∉A} π(x) W(x,y), equals L (an independent first-passage route to T2).
  - The occupation-sampled residual life is R_CT = Σ_{x∈A} π(x) h_CT(x)/π(A). By memorylessness, the residual time at a uniformly chosen instant in x equals h_CT(x).
- By Palm inversion for stationary point processes:
  - R_CT = E⁰[L²] / (2 E⁰[L]) ≥ L_CT / 2;
  - in jump counts, R_JT = E⁰[L(L+1)] / (2 E⁰[L]) ≥ (L_JT + 1)/2.
- **R is not L.** R can be much larger when episode lengths are heavy-tailed. E5A reports R only as a secondary channel and never in place of L.
- Tests: `test_entry_equals_exit_flux_and_first_passage`, and `test_two_state_episode_lifetimes` (exact two-state CTMC: L_CT = 1/b, L_JT = 1).

## 4. Turnover and relative longevity

**T4 (intact motifs cannot turn over) [T].**
- If a required slot of an intact predicate is toggled while x ∈ A, it was present, so the toggle removes it and x⊕e ∉ A.
- Hence no transition inside A changes a required slot, and the required-edge internal flux is identically 0.
- Every exit from A is a required-edge dissolution. Toggles of non-required slots inside A do happen, but they are not constituent turnover.
- **An intact motif never persists through replacement of its own relations.** E5A requires the required-edge internal flux to be exactly 0 and the required-edge exit share to be 1.
- Test: `test_intact_required_edges_never_turn_over`.

**Within-episode turnover [D].** Ω(A) = (Σ π(x) W(x,e) over x ∈ A, x⊕e ∈ A, (x,e) eligible) / J_A. This is the mean number of eligible toggles per entrance episode.
- The count is common to both clocks: the jump chain makes the same transitions. The clocks differ only in how they weight episode duration.
- 0 ≤ Ω ≤ L_JT − 1. E5A also reports the eligible share Ω/(L_JT − 1).
- **[L] Ω counts toggles, not replacements** (D-4). A completer that leaves and returns counts twice. Whether an episode ever replaces *all* the participants it started with is an identity-tracking question, and it is **not defined in E5A**.

**T5 (small-N degeneracy) [T].**
- F_TRI at N = 3 has a single possible completer, so Ω ≡ 0.
- F_STAR at N = 4: degree 3 is the maximum, so every removal at the centre leaves A. Ω ≡ 0.
- At N = 5 and 6, F_TRI has 3 and 4 possible completers, and F_STAR has headroom of 1 and 2 above the threshold, so Ω can be positive.
- Test: `test_small_n_degeneracies`.

**Edge present-lifetime [D].** A_e = {x_e = 1} for slot (0,1), with (N−2, N−1) as the relabelled check. L(edge) is given by T2, and ρ_clock(A) = L_clock(A) / L_clock(edge) in the same law.

**[L] ρ is not a test of self-maintenance.** Under plain NULL at N = 6, F_2PATH(0) has ρ = 13/10 > 1 (table in §6). A flexible predicate with many interchangeable witnesses outlives a single edge with no organisation at all. So ρ is always read beside prevalence, Ω and both comparators, never against a universal threshold.

## 5. Comparators

### N0: ordinary NULL

N0 is the NULL item at the same N: all rates 1, with the same predicates and formulas. Its values are theorem-fixed (§6), so N0 also tests the machinery.

**[L]** N0 differs from a target in density and in overall activity. Its mean rate is M, while a target's is E_π[q]. So L_CT/L_CT,N0 mixes the two. ρ removes the overall clock scale (T3), but not density.

### ND: density-matched exchangeable Markov process

**Construction [D].** ND is fixed before any target data are seen, and is applied identically to every target:
1. p_k = Σ_{|x|=k} π_target(x), for k = 0..M (the CT edge-count profile).
2. φ_k = p_k / C(M,k): the comparator weight of each labelled k-edge graph.
3. Birth rate b_k = min(1, φ_{k+1}/φ_k) for x → x+e with |x| = k. Death rate d_{k+1} = min(1, φ_k/φ_{k+1}) for the reverse.
4. All rates are multiplied by c = E_{π_target}[q] / E_{π_ND,unscaled}[q].

The ratios are formed in logarithms (`gtpersist.nd_rates`).

**T6 (ND properties) [T].**
1. *Detailed balance:* φ_k b_k = min(φ_k, φ_{k+1}) = φ_{k+1} d_{k+1}. ND is reversible with π_ND(x) ∝ φ_{|x|}.
2. *Density match:* Σ_{|x|=k} π_ND(x) = C(M,k) φ_k = p_k exactly. ND is uniform conditional on k.
3. *Covariance:* ND's rates read only |x| and whether e is present, so ND is invariant under every relabelling.
4. *Calibration:* scaling by c leaves π_ND and the ND jump chain unchanged (T3) and makes E_{π_ND}[q] equal the target's mean CT event rate.
5. *NULL fixed point:* the NULL target has p_k = C(M,k)/2^M, so φ_k is constant, every rate is 1 and c = 1. ND = NULL.
6. *PCOMP:* PCOMP's CT law is uniform at any strength (GT-P008 S2b). Its profile is therefore binomial and every unscaled ND rate is 1. So ND(PCOMP) is NULL kinetics scaled by c = E_PCOMP[q]/M, which gives:
   - ND CT lifetimes = N0 lifetimes / c;
   - ND JT lifetimes, Ω and ρ equal N0's.

   E5A checks this as a frozen identity.

*Proof.* Items 1–3 follow directly from the definitions. For item 4, multiplying a generator by a constant leaves the solution of π Q = 0 and Q's jump chain unchanged. Item 5 follows from item 2 and the definition of c. Item 6: S2b, with items 2 and 5. ∎

Tests:
- `test_nd_null_fixed_point`;
- `test_nd_nonuniform_profile`: a strongly non-uniform synthetic p_k, checked by the solver;
- `test_nd_rare_interior_bin_is_flagged_and_analytic`;
- `test_nd_zero_bin_is_unresolved`;
- `test_nd_jump_density_differs_from_target_jump_density`.

**Numerical policy [D].**
- π_ND is used in its analytic form φ_{|x|}, verified by detailed balance (≤ 10^−12) and global balance (≤ 10^−10). An iterative solve (at most 20,000 lazy iterations) is a cross-check only, recorded resolved or unresolved.
- A rare bin, p_k < 10^−12, is flagged with its mass.
- The smallest unscaled rate is reported:
  - an interior rare bin makes ND nearly reducible, with mixing times around 10^12 (found in the proof fixture), and ND lifetimes would then reflect that bottleneck;
  - a zero bin makes ND unresolved for that item, and nothing is smoothed.

**Static versus dynamical [T].**
- ND's motif prevalence π_ND(A) equals the **static density-standardised prevalence**: uniform graphs at each k, weighted by p_k. That is a reweighting of a distribution, and it determines no lifetime.
- ND's lifetimes, Ω and lags come from its declared **rates**. Only those are dynamical comparisons.
- Reweighting the NULL histogram would not define a process, so it is not used.

**Limitations to state with every result [L].**
- ND matches the CT density marginal and the CT mean event rate only. It does **not** match:
  - the full state law;
  - the local rates;
  - temporal correlations;
  - the JT density marginal.
- CT comparisons against ND are density- and activity-matched under one comparator. JT comparisons are kinetic diagnostics. E5A reports the JT edge-count profiles of target and ND and their L1 gap.
- ND is one reasonable dynamics at a matched profile. An effect relative to ND is a fact about that comparison, not about comparator-independent metastability. This underdetermination stays open (to be recorded as a GT question).

## 6. NULL expectations (theorem-fixed)

**T7 [T].** Under NULL every slot is an independent unit-rate bit:
- π is uniform and q ≡ M;
- the centre degree is Binomial(N−1, ½);
- the F_TRI completers are independent with probability ¼ each, over s = N−2 candidates.

Counting boundary toggles gives the values below (`gtpersist.null_closed_forms`; the test re-derives them independently).
- **Fluxes:**
  - I_TRI and I_STAR: J = 3/8 (three required slots, each dissolving at rate 1);
  - I_2PATH: J = 1/2;
  - F_TRI: J = π(A) + s·¼·(¾)^(s−1) (anchor loss, plus loss of either leg of a unique completer);
  - F_STAR: J = 3·P(d=3);
  - F_2PATH: J = 2·P(d=2).
- **Eligible flux:**
  - F_TRI: (s/2)(1 − (¾)^(s−1));
  - F_STAR: Σ_{d≥3} P(d)[(N−1−d) + d·1(d≥4)];
  - F_2PATH: Σ_{d≥2} P(d)[(N−1−d) + d·1(d≥3)].
- **Edge:** L_CT = 1, L_JT = M. Hence ρ_CT = L_CT(A).
- **Lagged hub:**
  - each slot relaxes as E[x_e(t)] = ½ + (x_e(0) − ½)e^(−2t), so the normalised gap is e^(−2t) and the retention is ½ + ½e^(−2t);
  - in JT the factor is (1 − 2/M)^Δ.

| N | Predicate | π(A) | J_A | L_CT | L_JT | Ω |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | I_TRI, I_STAR | 1/8 | 3/8 | 1/3 | 10/3 | 0 |
| 5 | I_2PATH | 1/4 | 1/2 | 1/2 | 5 | 0 |
| 5 | F_TRI | 37/128 | 91/128 | 37/91 | 370/91 | 12/13 |
| 5 | F_STAR | 5/16 | 3/4 | 5/12 | 25/6 | 2/3 |
| 5 | F_2PATH | 11/16 | 3/4 | 11/12 | 55/6 | 8/3 |
| 6 | I_TRI, I_STAR | 1/8 | 3/8 | 1/3 | 5 | 0 |
| 6 | I_2PATH | 1/4 | 1/2 | 1/2 | 15/2 | 0 |
| 6 | F_TRI | 175/512 | 391/512 | 175/391 | 2625/391 | 592/391 |
| 6 | F_STAR | 1/2 | 15/16 | 8/15 | 8 | 5/3 |
| 6 | F_2PATH | 13/16 | 5/8 | 13/10 | 39/2 | 11/2 |

These values are evaluated from formulas, not from the E5A NULL cells. The frozen identity requires the NULL items to reproduce them within 10^−9.

## 7. Lagged-hub control

**Definition [D].**
- x_0 is drawn from π for CT lags and from ν for JT lags.
- The hub is chosen once, uniformly among maximum-degree vertices: h(x,v) = 1/|argmax| (S_N-covariant).
- The comparison vertex is uniform over all N vertices (D-7).
- At each lag:
  - the expected degrees of the hub and the comparison vertex, and their gap;
  - gap/gap(0);
  - the expected number of the hub's initial neighbours still adjacent, and its ratio to the expected initial hub degree;
  - the same two quantities for the comparison vertex.
- The lags are Δ ∈ {0, 1, 2, 4, 8, 16} jumps. CT uses t = Δ / E_π[q], each law with its own mean rate (ND's equals the target's). This scale translates average activity only.

**T8 [T].** Under a stationary start:
- the comparison vertex's expected degree is constant in the lag (it is a vertex average of a stationary process);
- as the lag → ∞, the gap → 0, by mixing and exchangeability (GT-P008 R1).
- A decaying gap is **selected-frame memory**: the high initial degree comes from selection. No vertex is permanently distinguished.

**Computation [T].**
- **Strong lumpability.** Let G(x) = E_x[X_01(t)]. Every covariant chain is strongly lumpable under the group fixing vertices 0 and 1: the aggregated rate from x into an orbit O equals that from σx, for every σ fixing 0 and 1. G is invariant under that group.
- **CT.** G is computed exactly as exp(tQ̄) f̄ on the lumped chain (240 states at N = 5, 1,992 at N = 6). The exponential is Padé-13 scaling and squaring.
- **Recovering every pair.** E_x[X_vu(t)] = G(σx) for any σ with σ(v) = 0 and σ(u) = 1, because (σx)_{σ(i)σ(j)} = x_ij (the `gtobs.permute_codes` convention).
- **JT.** JT lags propagate P^Δ on the full space.
- **Why not uniformisation [L].** PATHH, CSPH and PCOMP have dissolution factors 2^w with w up to 24 path witnesses at N = 6, so rates reach 2^24 against mean rates of order 10. Uniformisation would need about 10^7 terms.
- **Checks:**
  - lumpability defect;
  - stochastic propagator rows;
  - stationarity of π̄;
  - a non-dyadic semigroup check, P(t) against P(¾t)P(¼t);
  - lumped against full JT propagation;
  - pair-permutation covariance (two choices of σ);
  - a uniformisation cross-check where it is cheap.
- **Tests:**
  - `test_lagged_hub_null_closed_forms`;
  - `test_lumpability_and_expm_checks_on_nonreversible_chains`;
  - `test_stiff_expm_matches_symmetrised_eigendecomposition`: a reversible chain with rates up to 2^12, checked against an exact symmetrised eigen-solution to 10^−9;
  - `test_hub_tie_rule_is_covariant`.

## 8. What these observables can and cannot show [L]

- **Intact motifs.**
  - Can show: survival of a fixed, labelled set of relations, against N0 and ND.
  - Cannot show: identity through replacement (T4).
- **Flexible predicates.**
  - Can show: that an anchored organisation outlives single relations while some of its participants change (Ω > 0).
  - Cannot show: an unlabelled, reconfiguring structure; complete replacement; or movement.
- **Lagged hub.**
  - Can show: how fast selected-frame memory decays relative to the comparators.
  - Cannot show: a permanently distinguished centre (T8).
- **Any contrast against ND** is relative to one comparator. A longer lifetime is a finite-N, model-clock observation. It is not a demonstration of an emergent reference, a body or a physical time scale.
- **The 8G gate is not engaged.** All matching is done by a read-only analyser; no rule reads a motif, an anchor, a selected hub, a label or a history.
