# GT-E2 mechanism atlas (E2A and E2B)

*Prompt GT-P005, deliverable 6. A map of mechanisms against the cells in which they occur. Every cell, with every channel, is in the generated atlases:*
- *`reports/gt-e2a-atlas.md` (46 cells, frozen plan `1974678`);*
- *`reports/gt-e2b-atlas.md` (18 cells, frozen plan `9448f95`).*

*Replayable exemplar squares (four states, eight rates, affinity, circulation) are listed per cell in section 6 of the E2A and E2B atlases, selected by the frozen rule.*

## 1. Local transition structures

| Structure | Rule | Where it occurs | Where it is absent |
| --- | --- | --- | --- |
| Square with affinity σ·(deg r − deg q) | Two slots sharing a vertex; positive factors | Every intact adjacent square of every cell (64/64 cells; identity I1) | — |
| Square with zero affinity | Disjoint slots; or σ = 0; or a hard path component on the square | Disjoint squares everywhere; all σ = 0 cells; every intact square under hard path-form prohibition | — |
| Reversed attachment/probe square (probe out-connects the source vertex) | Needs deg(q) > deg(s) | HELD N=6: 1,152 of 13,824 nonzero squares, in each of the four N=6 cells | Impossible at HELD N=5 (I5: 29 of 29 cells) |
| One-way transition | Forward admissible, reverse forbidden | Hard path-form prohibition: 510 transitions at FREE N=5 (all are releases); hard path-dissolve prohibition (absorbing) | Every soft cell; hard closure and adjacency exclusions |
| Arrest | No admissible event | Hard path-dissolve prohibition (complete graph absorbs); HELD N=4 hard path-form (synthetic) | — |
| Path terms inert | No two relations share a vertex | Hard adjacency exclusion plus any path term (formal note 5.3) | — |

## 2. Event-order motifs and orientation

Orientation is measured by the partner-frame index (keep the relation to the richer partner, release the poorer) and, in HELD, by the handover index. Both are signed. "+" is the E0/E1 orientation.

| Class of cell | Cells | Sign of orientation | Size | Notes |
| --- | --- | --- | --- | --- |
| Soft, σ > 0, unsaturated | 16 (E2A: 12 at N=5, 4 at HELD N=6) | + in all | 0.015–0.19 | Includes the strong grades and the σ = +2 log 2 pair (largest: HELD 0.190) |
| Soft, σ < 0, unsaturated | 2 (E2A ADPF, HELD and FREE) | − | −0.112 (HELD), −0.031 (FREE) | **The handover reversed, at full size** |
| Soft, σ < 0, saturated | 10 (E2A) | − | 1e-13 to 4e-5 | Real sign; negligible currents (X-SAT). One HELD cell is below the 1e-12 floor |
| Hard closure exclusion + soft σ < 0 | 4 (E2B) | − | −0.007 to −0.042 | The exclusion caps density, so the reversal is visible |
| Hard closure exclusion + soft σ > 0 | 4 (E2A EXPH, EXPF) | + | 0.04–0.10 | |
| Hard path-form exclusion (σ = 0, +, −) | 3 (FREE) | **+ in all three** | 0.070–0.126 | **Counterexample to "σ sets the sign":** the one-way release mode orients + even when σ < 0 |
| σ = 0, positive factors (NULL, CLOSEW, both PFD cancellations) | 8 | 0 | ≤ 1e-15 | Identity (I3) |
| Hard gradient restrictions (EXCL HELD/FREE; hard adjacency ± path, FREE) | 7 | 0 | ≤ 1e-15 | Reversible with strict enabling |
| HELD under hard path-form or adjacency exclusion | 8 | 0 | 0 | Two-state chain; the held source is a witness |

**Frames, FREE N=5.**
- The partner-frame index is 1.3–2.3 times the hub-frame asymmetry and 7–32 times the class-free asymmetry in every irreversible cell.
- The source frame (HELD handover index) and the partner frame agree in sign in every HELD cell. In HELD, the partner frame includes attachment/attachment and probe/probe pairs as well.

## 3. Stationary currents against local affinity

| Quantity | Range over irreversible cells | Reading |
| --- | --- | --- |
| Share of adjacent-square circulation aligned with the square's affinity | 0.62–1.00 | Majority follows local affinity |
| Share running counter to it | 0.00–0.36 | Common; largest at HELD N=6 and in HELD strong cells |
| Share on squares without affinity (adjacent) | 0.00–0.12 | Largest in saturated σ < 0 HELD cells |
| Oriented flow across disjoint (zero-affinity) squares | up to 0.35 of total flux (HELD N=6) | Through-flow from neighbouring cycles |
| Net oriented circulation on attachment/probe squares | Sign of σ in every HELD cell, N=5 and 6 | Aggregate follows σ despite local reversals |

## 4. Matched dissolution: mechanism coverage

| Mechanism | Soft cells | Hard cells |
| --- | --- | --- |
| Strict enabling | 0 of 288 groups | 17 of 54 E2A groups; every E2B hard closure, path-form and FREE adjacency cell |
| Rate facilitation or suppression | Present in every σ ≠ 0 cell | Present |
| Opportunity effect larger than the rate effect | 170 of 288 groups | Common |
| Next-event change opposite to own-rate change | 54 of 288 groups | — |
| Passage within 8 events | up to 0.12 in absolute value in soft cells; ≤ 0.011 for the handover release step | Larger (race 0.49–0.53 against ≤ 0.28) |
| Precedence tracks enabling | — | No (one-way cell: enabled formations 0.72–0.95 times average after an executed dissolution) |

Details: `reports/gt-e2-dissolution-analysis.md`.

## 5. HELD and FREE framing

- **HELD imposes the reference.** The orientation is source-relative because source vertices carry two extra neighbours (formal note, corollary 3). Under hard path-form or adjacency exclusion, the source triangle is itself a witness and blocks every attachment (formal note 5.4).
- **FREE has no reference.** Orientation is still legible, relative to an *induced* one: the better-connected partner. The partner frame is defined in every state from current degrees, without a held structure or a hub label.
- **Neither frame is evidence of an emergent centre.** The partner frame refers to local degree differences, not to a persistent hub.

## 6. Counterexamples and boundaries found

1. **σ does not set the orientation when one-way transitions are present.** Hard path-form plus path_dissolve weak_suppress: σ < 0, partner index +0.070.
2. **Local affinity does not fix local current.** Up to 36% of circulation runs counter to its square's affinity.
3. **Strict enabling is neither necessary nor sufficient for direction** (EXCL, hard adjacency exclusion; soft σ ≠ 0 cells).
4. **One-step precedence is not counterfactual enabling** (one-way cell).
5. **The handover's release step is an opportunity effect in soft rules** (own rate unchanged or lower).
6. **Hard adjacency exclusion removes the incidence on which every path term acts.**
7. **The held source blocks attachment under hard path-form or adjacency exclusion.**
