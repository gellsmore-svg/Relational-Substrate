# Formal note: support geometry, one-way release and recovery

*Prompt GT-P006, deliverable 3.*
- *Sections 1–6 were written before the E3A freeze. They are pure derivations, checked on proof fixtures (synthetic factor tables and HELD N=4; `constraint-lab/tests/test_gte3a.py`). No round cell's law, recovery value or scan value was used.*
- *Section 7 is added after the rounds and is marked as such.*

## 1. Setting

- **Grammar.** The GT ordinary pair DSL (order 2), label-covariant templates (`gte0a.component_expressions`), single-relation toggles. Each component multiplies a toggle's weight by its factor once per satisfied witness. `prohibit` is the factor 0.
- **Hard path-formation prohibition (HPF).** This is `path_form prohibit`: forming (a,b) is forbidden whenever a *path witness* exists, that is, an end ∈ {a,b} and distinct c, d ∉ {a,b} with (end,c) and (c,d) present. HPF is combined with any number of soft components (closure, adjacency, path) with positive factors.
- **States and support.** A state is a set of present relations. The support graph has a directed edge x → x⊕e when the weight W(x,e) > 0. FREE starts at the empty graph; HELD starts at the source triangle, whose dissolution is prohibited.

## 2. Support theorems for HPF (FREE)

**T1 (dissolution always admissible).** HPF restricts only formation. Soft factors are positive. So W(x,e) > 0 for every present e.

**T2 (one-way exactly when witnessed).** Let e be present in x and y = x − e. The release x → y is one-way (W(y,e) = 0) exactly when e has a path witness in x.

*Proof.* Path witness conditions for e read only (end,c) and (c,d) with c, d ∉ e's endpoints, so they never read e itself. Hence e's witness count is the same in x and y. W(y,e) = 0 exactly when that count is positive (HPF), and soft factors never make a weight zero. ∎

**T3 (no absorption; recovery always possible).**
- From any reachable state, dissolving every present relation (allowed by T1) reaches the empty graph, which is the FREE start. So every reachable state communicates with the start, and the reachable class is a single communicating (recurrent) class.
- Every one-way release therefore lies *inside* a communicating class. A released relation can always be re-formed by some admissible path. Under HPF a one-way **edge** is never a lost **state**.

**T4 (shortest recovery).** After the release x → y of a witnessed e, the shortest admissible path from y to any state containing e has length 1 + h(y,e). Here h(y,e) is the minimum number of present relations whose removal leaves e unwitnessed.

*Proof.*
- *Formations never help.* Witness counts are monotone in the present set, so a formation never reduces e's witness count.
- *Upper bound.* Removing h relations (allowed by T1), then forming e, achieves 1 + h.
- *Lower bound.* Any path ending with the formation of e must, at that moment, be at a state where e is unwitnessed. Its present set differs from y by at least h removals among y's relations. Formations along the way only add witnesses, which then also need removal.

So h(y,e) is a minimum hitting set over e's witness 2-paths: each 2-path is hit by removing either (end,c) or (c,d). ∎

**Corollary T4a.** At y, gate distance = 1 for an unwitnessed release (two-way) and ≥ 2 for a witnessed (one-way) release. Without a hard component every gate distance is 1.

**T5 (the reachable set is downward closed).** If x is reachable, every subgraph of x is reachable, by dissolutions. The HPF reachable set is therefore an independence system: an abstract simplicial complex over relations, determined by its maximal graphs. A graph is reachable exactly when its relations admit an order in which each is unwitnessed when added.
- **Proof fixtures** (structural, independent of soft factors): 54 of 64 graphs at FREE N=4 and 341 of 1,024 at FREE N=5.
- A full combinatorial characterisation of the maximal graphs is **open**.

**T6 (HELD, from E2 formal note 5.4).** The held triangle gives every attachment slot a path witness, so HPF forbids every attachment. HELD then reduces to the probe-only subgraph.

## 3. What one-way support does to standard quantities

- **Entropy production.** With a one-way transition, the logarithmic Schnakenberg entropy production diverges. `gte0a.reversibility` sums only over two-sided pairs, so the finite values it reports for HPF cells are the two-sided part only. E3A reports the one-way flux share beside it.
- **Detailed balance and intact squares.** Zero affinity on every intact square (E2 formal note §3) does **not** imply detailed balance when the support is asymmetric. HPF has zero intact-square affinity and nonzero irreversible flux (FREE N=5: 0.23).
- **One-way edges are not absorption.** Absorption happens under hard *dissolution* prohibition (`path_dissolve prohibit` absorbs in the complete graph; E2).

## 4. Four regimes, kept distinct

| Regime | Support | Stationary law | Strict enabling | Direction | Example |
| --- | --- | --- | --- | --- | --- |
| Reversible with strictly enabling release | Symmetric on the reachable class | Restricted Gibbs, detailed balance | Yes | None | EXCL; hard adjacency exclusion |
| Non-reversible, positive rates | Symmetric (all toggles admissible) | Non-equilibrium; circulation with square affinity σ·Δdeg | No | Yes, sign of σ (empirically aggregate; locally proved) | Soft path rules |
| One-way edges inside one communicating class | Asymmetric; irreducible | Non-equilibrium; infinite log entropy production | Yes | Yes (observed; mechanism open) | HPF |
| Absorbing / arrested | Asymmetric; not irreducible | Point mass on the absorbing state (or arrested) | — | None at stationarity | path_dissolve prohibit; HELD N=4 HPF |

## 5. Orientation of one-way release: what can and cannot be said before E3A

- **Local edge level.** Every one-way edge is a dissolution of a witnessed relation (T2), and its reverse has rate 0. So in any statistic that compares a pattern with its time reverse, a pattern containing a one-way step has a reverse of probability 0, and contributes its full probability.
- **Stationary current.** On a one-way edge the net current equals the forward flux, which is positive whenever the source state has positive mass.
- **Aggregate partner index.** The partner index (keep the relation to the better-connected partner) sums signed pattern probabilities.
  - **No sign law is derived.** T2 says which relations are released one-way (the witnessed ones), but whether witnessed relations are typically those to the poorer-connected partner depends on the stationary weights.
  - *Sketch, not a proof.* A witness at endpoint p of e = (p,q) needs a neighbour c ≠ q of p that has another neighbour. That favours p having more connected neighbours, but the partner frame compares the far endpoints of two relations sharing a vertex, not the two endpoints of one relation. **Open: GT-Q11.**
- **Hypothesis to test, not assumed.** HPF is the extreme of path-formation suppression (soft factor → 0). E3A compares the existing rungs 1/2, 1/4, 1/9, 1/16 and 0. Soft rungs have σ = −log m_f > 0 and positive support; the hard zero has asymmetric support. No continuity is claimed: positive and zero support are qualitatively different.

## 6. GT-Q12 (aggregate orientation follows σ): status before E3A

- **Obstacle.** The local identity fixes the affinity of every square. The aggregate partner index weights squares by stationary probabilities, which depend on all rates jointly. E2 found 6–36% of square circulation running counter to local affinity, so no square-by-square argument can give the aggregate sign.
- **Smallest class.**
  - At N=3 there is no path witness (a slot's other vertex has no second neighbour outside the slot), so every rule is gradient.
  - **N=4 FREE is the smallest class with path affinity.** There, the chain has 64 states and two rate parameters (m_f, m_d). A symbolic proof would need the sign of a rational function of (m_f, m_d) over the positive quadrant.
- **E3A step.** A bounded counterexample search on a frozen 9×9 grid at N=4 and N=5 FREE. A grid without counterexamples is evidence within the grid only.

## 7. Results after E3A (and E3B, if run)

*(Added after the rounds.)*
