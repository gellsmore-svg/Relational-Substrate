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

## 7. Results after E3A and E3B (written after the rounds)

**7.1 Support theorems in every executed hard cell [M, O].** T1–T4 were checked in all 8 FREE cells with hard path-formation prohibition (E3A identity S1):
- the class is irreducible;
- a release is one-way exactly when the relation is witnessed;
- one-way releases have gate distance ≥ 2 (observed ≈ 2.00–2.02 on average);
- two-way releases have gate distance 1.

Gate distances and one-way classifications were recomputed from the rule strings with exact fractions on 25 seeded releases per cell, with no mismatch.

**7.2 Q11, the orientation of one-way release: a reading, not a theorem [O].**
- Along the existing formation factors 1/2, 1/4, 1/9, 1/16 and 0, the partner index, flux and absence durations of the hard zero lie at the end of the soft ladder: FREE N=5 partner index 0.072, 0.104, 0.112, 0.111, 0.108. The hard mode differs qualitatively only in support.
- Reading: the hard ban acts as path-formation suppression with σ → +∞ on witnessed formations. With that convention, every E2B/E3A orientation agrees with σ. Opposing dissolution down to soft σ = −log 16 lowers the index to +0.007 but does not reverse it.
- **No sign law is proved.** The one-way part of the index can be negative while the two-way part is positive (W16).

**7.3 Q12 [O].** No counterexample on the frozen grids:
- FREE N=4: 72 judged points;
- FREE N=5: 56 judged points (16 below the 1e-12 floor at saturation).

The obstacle in section 6 stands, and **no proof is offered**.

**7.4 T7, the source-witness floor (derived after E3A; verified in E3B) [M].**

*Statement.* In HELD with source S = {s, s′, s″} held present, every attachment slot (p,s), with p ∉ S, has exactly two path witnesses whose three entities all lie in S: (end = s, c = s′, d = s″) and (s, s″, s′). They are present in every state. Probe–probe and source slots have none.

*Proof.* A path witness of (p,s) needs end ∈ {p,s}, and c, d ∉ {p,s} with c ≠ d. For all three entities to lie in S, end = s, and {c,d} = S∖{s} in either order. Both edges, (s,c) and (c,d), are source edges, which are held present. A probe–probe slot has no endpoint in S. A source slot (s,s′) would need c, d ∈ S∖{s,s′}, a single vertex, so no witness exists. ∎

E3B verified T7 on every reachable state of all 18 cells.

**7.5 T8, the floor is orientation-neutral (derived after E3A; verified in E3B) [M].**

*Statement.* Multiplying every formation (or every dissolution) rate of one slot class by a constant c > 0 changes no cycle affinity.

*Proof.* In a closed cycle every slot is formed exactly as often as it is dissolved. The forward product of a cycle contains c once per formation of a class-slot. The reverse traversal turns every formation into a dissolution and vice versa, so it contains c once per *dissolution* in the forward direction. That is the same number. ∎

*Consequence.* Each path component with factor m multiplies every attachment's formation (path_form) or dissolution (path_dissolve) rate by m² (from T7). This is an occupancy bias that leaves every affinity unchanged:
- **against** attachment when the component's σ-contribution is positive;
- **toward** attachment when it is negative.

E3B verified T8 numerically: the largest change of any square affinity is ≤ 1e-12 in all 18 cells.

**7.6 E3B outcome [O].** The neutralised instrument kernel is the original with the floor divided out of attachment rates. **It is not a grammar rule**: it reads scaffold membership and is not label-covariant. With it, every σ > 0 path family gathers above the null at HELD N=5 and 6 in the raw margin, both clocks:

| Cell | N=5, continuous margin | N=6, continuous margin |
| --- | --- | --- |
| PATHF weak_suppress | −0.107 → +0.071 | −0.206 → +0.073 |
| PATHH weak_favour | −0.044 → +0.091 | −0.112 → +0.128 |
| CWPH | −0.007 → +0.107 | −0.067 → +0.153 |
| CSPH | +0.046 → +0.123 | +0.009 → +0.177 |

- The handover index stays positive (smaller), and flux changes little.
- σ < 0 families stay saturated.

**8G compilation note.** Removing the floor *within* label-covariant rules is not possible: a covariant path term acts on all witnesses alike. Removing it with a scaffold-indexed rule is possible, but that rule is not covariant. The covariant alternative is a **different scaffold**: a held structure without internal two-paths, such as a held single edge. That is a scaffold change, not a new primitive.

**7.7 Frozen checks that failed as specified (recorded, not re-run) [methodological].**
- **K** (kernel unchanged off attachment slots) failed in all 18 cells, because the check divided by zero-weight source-slot entries. A post hoc direct comparison shows the kernels identical off attachment slots (largest difference 0).
- **C2** (PCOMP unchanged) failed, because the expectation was wrong. For PCOMP the floor scales attachment formation and dissolution equally, so the continuous-time law is unchanged (uniform). But attachments' total rates change, so jump-clock channels move: raw jump margin +0.009 → +0.022 (N=5).
