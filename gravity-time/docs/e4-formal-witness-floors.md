# Formal note: witness floors of held references (GT-P007)

*GT-P007 §6.*
- *Derived after E4A, except where a result was already stated in the scaffold note.*
- *Each result is a theorem with stated assumptions, or is marked as an observation or as open.*

## Setting

- **Grammar.** The GT ordinary pair DSL with label-covariant path, closure and adjacency templates, and positive factors.
- **Held reference.** A held graph H: its relations are present and their dissolution is prohibited (`gt0.Scaffold`).
- **Source and attachments.** The source S is the set of vertices incident on H. An attachment slot is (p, s) with s ∈ S and p ∉ S.

## F1. The permanent floor of any held graph (theorem)

*Statement.* The number of path witnesses of an attachment slot (p, s) whose two edges are both held, called the **floor** at s, is state-independent and equals

  floor(s) = Σ over held neighbours c of s of (deg_H(c) − 1).

*Proof.*
- A path witness is (end, c, d) with end ∈ {p, s}, distinct c, d ∉ {p, s}, and (end,c) and (c,d) present.
- Both edges held requires end = s, because p has no held edge. It also requires (s,c) ∈ H and (c,d) ∈ H with d ≠ s. Here d ≠ p automatically, since p has no held edge.
- So for each held neighbour c of s there are deg_H(c) − 1 choices of d. Held edges are always present, so the count is state-independent. ∎

| Reference | Floors at its source vertices |
| --- | --- |
| K2 | 0, 0 |
| P3 | 1 (ends), 0 (middle) |
| K3 | 2, 2, 2 |
| Star K1,3 | 0 (centre), 2, 2, 2 (leaves) |
| P4 | 1, 1, 1, 1 |

The census matched these at every reachable state in all 48 E4 cells.

## F2. Only K2 has a zero floor everywhere (theorem)

*Statement.* Among connected held graphs, the floor is zero at every source vertex exactly for K2.

*Proof.* A zero floor at every s needs deg_H(c) = 1 for every vertex c that is a held neighbour of some s, that is, for every vertex of H. A connected graph in which every vertex has degree 1 is a single edge. ∎

*Consequence.* A connected source with more than two vertices cannot remove the floor; it can only redistribute it. Floor heterogeneity within one reference, such as P3 or the star, is the natural covariant instrument.

## F3. Free source chords add state-dependent witnesses (theorem plus census)

- A non-held pair inside the source (a chord) adds witnesses whenever it is present. In P3, the chord (0,2) lifts the middle from 0 to 2 internal witnesses and each end from 1 to 2.
- Under σ > 0 path rules the chord is itself witnessed by the held path. Its formation (or retention) is suppressed: occupancy 0.23–0.29 under the path families, against 0.50 under NULL (E4A, observed).
- **Open:** a closed form for the stationary chord occupancy.

## F4. Per-slot constant factors are orientation-neutral (theorem; generalises E3 T8)

*Statement.* Multiply each slot's formation rate by a constant c_e > 0, and its dissolution rate by a constant d_e > 0, where the constants may differ across slots but not across states. Every cycle affinity is then unchanged.

*Proof.* In any closed cycle each slot is formed as often as it is dissolved. The forward product contains c_e once per forward formation of e and d_e once per forward dissolution of e. The reverse traversal swaps formations and dissolutions, so it contains the same factors. ∎

- **Consequence.** The floor of F1 enters every path component as a per-slot constant m^floor(s) on that slot's formation (or dissolution). It is therefore orientation-neutral at every source orbit, in every scaffold.
- **Not covered.** F4 does not say that the stationary law, or any event-order statistic, is unchanged:
  - occupancy changes;
  - the jump-chain law changes even when the continuous law does not (the PCOMP lesson, E3B C2).

## F5. Why aggregate event-order statistics move although affinities do not

Event-order indices are stationary-weighted sums over squares (E2 formal note). A per-slot factor (F4), or a change of scaffold, reweights which states are occupied, and therefore which squares carry weight. So the handover index can halve while every local affinity formula holds. This is observed: K2/P3 against K3 (E4A), and S4/P4 (E4B). **No theorem predicts the size of the shift.**

## F6. What K2, P3, K3, S4 and P4 can and cannot identify

| Contrast | Holds fixed | Varies | Identifies |
| --- | --- | --- | --- |
| P3 middle against P3 ends (same cell) | State, density, source size, probes | Floor 0 against 1 | The effect of the floor on where attachment goes |
| S4 centre against S4 leaves | Same | Floor 0 against 2 | Same, with a larger floor difference |
| P4 ends against inner | Same | No floor difference | Residual (state-dependent) orbit effects |
| S4 against P4 | k = 4, K = 3, N, r0 | Floor distribution (total 6 against 4) | Whether the total floor or a floor-free site matters for the overall margin |
| K2 against K3 | Probe count (K2 at N=5 against K3 at N=6) or N | k, K, r0, floor | Not separable from a single contrast |
| P3 against K3 | k = 3, N | K, chord, floor | Partly: confounded by the chord and by r0 |

- **Not identifiable from these shapes:** a separate "source size" effect at fixed floor distribution; intrinsic N dependence; anything about N = 7.
