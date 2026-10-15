# GT-E2 controlled dissolution analysis

*Prompt GT-P005, deliverable 7. From the frozen E2A and E2B tables (`reports/round-e2a-tables.json`, result `32ac7f6`; `reports/round-e2b-tables.json`, result `ecb3e73`). All quantities are exact-kernel values. "Removing g" is an experimental instrument: a stationary state with relation g present is compared with the same state without g. It is not a claim that the model contains interventions.*

## 1. What was compared

For a relation g that is present in a state x, the matched partner x⁻ is x with g removed. Both x and x⁻ are in the recurrent class, and the rule set is the same for both. x is drawn from the stationary per-event law, restricted to states containing g.

For every other relation slot f, and the action available on it (form or dissolve), the analysis records five quantities:

| Mechanism (GT-P005 section 4) | Quantity |
| --- | --- |
| Strict support enabling / disabling | Share of matched pairs where f's rate is 0 at x and positive at x⁻ (enabling), or the reverse (disabling) |
| Rate enabling / suppression | Mean of log W(x⁻, f) / W(x, f), where both are positive |
| Opportunity (denominator) effect | Mean of log P(x⁻, f) / P(x, f) minus the rate log ratio. This is the part of the next-event change due only to the total rate of competing events |
| Indirect pathway effect | Change in the probability that f happens within H = 1, 2, 4, 8 events. E2B adds the race probability that f happens before g is restored |
| Temporal precedence | p(next event is f, given that g was just dissolved) ÷ p(an event is f): the observed sequence, without intervention |

## 2. Soft rules: no strict enabling; most of the effect is opportunity

There are 288 groups across the soft cells: support class × target class × action, over all soft E2A cells. They show:
- **No strict enabling or disabling.** This follows from the definitions: a positive soft factor never makes a positive rate zero.
- **In 170 groups (59%), the opportunity part is larger than the rate part.** Removing g changes which event comes next mainly by changing how fast everything else happens.
- **In 54 groups (19%), the next-event probability moves opposite to f's own rate.** f becomes more likely next although its own rate fell, or the reverse. This is a pure denominator effect.

**The handover's release step** (the probe–probe relation P is removed; the target is the attachment A sharing that probe), in the unsaturated σ > 0 cells at HELD N=5:

| Cell | Rate log ratio | Opportunity part | Next-event log ratio | Δ passage, 1 event | Δ passage, 8 events | Precedence |
| --- | --- | --- | --- | --- | --- | --- |
| PATHH weak_favour | −0.169 | +0.563 | +0.394 | +0.112 | +0.011 | 1.14 |
| PATHH strong_favour | −0.125 | +0.763 | +0.638 | +0.288 | +0.001 | 1.40 |
| PATHF weak_suppress | 0 | +0.288 | +0.288 | +0.118 | +0.003 | 0.85 |
| PATHF strong_suppress | 0 | +0.556 | +0.556 | +0.348 | 0.000 | 0.69 |
| PFD weak_suppress+weak_favour | −0.018 | +0.594 | +0.576 | +0.326 | +0.000 | 1.07 |

In every one of these cells, dissolving P makes the attachment's dissolution more likely *as the next event*. But the attachment's own dissolution rate is unchanged (path-form rules) or **lower** (path-dissolve rules). The increase comes entirely from the opportunity term: P's own fast dissolution is gone from the competition. The effect on whether A dissolves within 8 events is negligible (≤ 0.011). Observed precedence is near 1 and can fall below it.

**Reading.** In soft rules the handover is a **kinetic sequence**, ordered by competition for the next event. It is not transition-enabling dissolution in any stronger sense. This is the negative finding GT-P005 allowed for.

## 3. Hard components: strict enabling, with three different relations to direction

| Cell (N=5) | Strict enabling (largest group share) | Irreversible flux | Direction |
| --- | --- | --- | --- |
| Hard closure exclusion alone (EXCL), HELD / FREE | 0.87 / 0.27 (A→A same probe, formation; FREE: adjacent formation) | 1e-15 | **None** (reversible) |
| Hard adjacency exclusion alone, FREE | 0.60 | 8e-16 | **None** (reversible) |
| Hard adjacency exclusion + any path term, FREE | 0.60 | 8e-16 | **None.** The path terms are inert (formal note 5.3) |
| Hard closure exclusion + path term, σ > 0 (EXPH, EXPF), HELD | 0.96, 0.98 | 0.076, 0.126 | Soft circulation following σ (+) |
| Hard closure exclusion + path term, σ < 0, HELD | 0.76, 0.72 | 0.049, 0.016 | Soft circulation following σ (−); visible because the exclusion keeps density low |
| Hard path-form exclusion (± path_dissolve), FREE | 0.47 (disjoint), 0.19 (adjacent) | 0.17–0.26 | **One-way release**; orientation + whatever the soft σ (formal note 5.5) |
| Hard path-form or adjacency exclusion, HELD | 0 (the held source is a witness; formal note 5.4) | 0 | Degenerate two-state chain |

**Strict enabling is neither necessary nor sufficient for directed succession in this grammar.**
- **Not necessary:** every soft cell with σ ≠ 0 circulates without any strict enabling.
- **Not sufficient:** EXCL and the hard adjacency exclusions enable strictly and are reversible.

## 4. Does an enabled event actually follow?

E2B's race probability asks whether, from x⁻, the target f happens before g is restored.

| Cell (FREE N=5 unless noted) | Group | f wins, enabled instances | f wins, all instances from x⁻ | f wins, from x with g present |
| --- | --- | --- | --- | --- |
| Hard path-form + path_dissolve weak_favour | disjoint formation | 0.514 | 0.463 | 0.142 |
| Hard path-form + path_dissolve weak_favour | adjacent formation | 0.495 | 0.465 | 0.232 |
| Hard closure + path_dissolve weak_suppress | adjacent formation | 0.491 | 0.386 | 0.279 |
| Hard closure + path_dissolve weak_suppress, HELD | attachment → attachment, same probe | 0.491 | 0.430 | 0.000 |
| Hard adjacency exclusion alone | adjacent formation | 0.500 | 0.443 | 0.000 |

- **Removing the support opens a window.** An enabled event wins the race against restoration about half the time (0.49–0.53). With the support present, the same event wins 0.00–0.28 of the time.
- **It is not a commitment.** Restoring the support competes about evenly with the enabled event.
- **Observed precedence misses this.** In the one-way cell, the strictly enabled formations are *less* likely than average as the next event after an executed dissolution (precedence 0.72 adjacent, 0.95 disjoint). The counterfactual question (what removal makes possible) and the observational one (what tends to follow) separate.

## 5. Where "transition-enabling dissolution" exists, in this grammar

| Sense | Exists? | Where |
| --- | --- | --- |
| Temporal precedence (A dissolved, then B happened) | Yes, in every irreversible cell | Event-order statistics |
| Rate enabling | Yes, soft and hard | Matched rate log ratios; often outweighed by opportunity |
| Opportunity (denominator) effect | Yes; dominant in 59% of soft groups | Matched jump-ratio decomposition |
| Indirect pathway (passage within H events, race) | Yes. In soft rules it is small for the handover release step (≤ 0.011 at 8 events) and up to 0.12 in other groups. In hard rules it is large (race about 0.5 against ≤ 0.28) | Passage and race channels |
| Strict support enabling | Only with a hard component | EXCL, EXPH, EXPF, hard adjacency and path-form exclusions |
| Strict enabling **with** direction | With a hard component plus soft circulation, or with one-way release | EXPH/EXPF; hard path-form exclusion |
| Irreversible release (a released relation cannot return while supported) | Only under hard path-form exclusion | 100% of one-way flux is release |

For CL-Q05 ("when does controlled dissolution enable a distinct configuration rather than merely remove one?"):
- In this grammar, dissolution enables a distinct configuration *strictly* only through hard formation exclusions. It does so whether or not the dynamics has a direction.
- The soft handover enables only in the opportunity sense.

This is a GT model result. It is offered to the laboratory as a suggested finding, not entered in its records (`reports/gt-e2-synthesis.md`, section 6).
