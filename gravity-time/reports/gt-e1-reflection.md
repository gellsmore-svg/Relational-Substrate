# GT Round E1 — Open-Thetical coherence reflection

*Prompt GT-P004, deliverable 7. Reflection after the frozen E1 round (plan `4ba2839`, result `730ef32`). Numbers are from `reports/round-e1-tables.json` and `reports/gt-e1-report.md`. Items marked post hoc come from `reports/e1-margin-composition-posthoc.json`, computed after the results. Layers: [O] model observation, [M] mathematical mechanism, [RS] interpretation, [P] physical comparison (none made), [T] theological premise (none used).*

## 1. What was directly observed

1. **CSPH's attachment advantage is gone at N=7 in every form** [O]. Raw −0.067 per unit time, +0.002 per event; crowding-adjusted −0.112 / −0.095. GT-Q07 is answered for this family and these grades: basin-with-arrow coexistence does not survive to N=7.
2. **The handover is the most robust behaviour in the programme so far** [O]. Its orientation is the same in all 30 non-gradient cells: three sizes, three strength scales, six rule families. Its total irreversible flux is steady from N=6 to N=7 (0.14–0.16).
3. **The arrow-carrying rules barely get stronger with size** [O]. Their engaged log-weight changes by ×0.87–1.08 from N=6 to N=7, against a nominal maximum ×1.67.
4. **Strengthening is a different operation from growing** [O, post hoc M]. Strengthening crowds the system into sparse states and acts on the per-density preference. Growing spreads occupancy to denser states and acts on both parts. In the dissolution-acting families the occupancy parts have opposite signs under the two operations.
5. **Detachment is size-stable and strength-sensitive** [O]. A probe is detached 52–55% of the time at N=6 W4 and 55–58% at N=7, but 84–89% at N=6 W16.
6. **The equal-ratio gap keeps growing, more slowly** [O]: L1 0.18–0.22, then 0.32–0.49, then 0.37–0.62.

## 2. What was unexpected

- **Strengthening splits CSPH's clocks** [O]. Per event its margin *rises* with strength (+0.065 → +0.092 at N=6), while per unit time it collapses (+0.009 → −0.297). A stronger rule makes attachment more likely *as the next event* but shorter-lived *in time*. That is a concrete instance of X-CLOCK at its sharpest.
- **The reversible gradient control is the only rule whose crowding-adjusted attachment preference grows with N** (+0.022 → +0.034 → +0.042) [O]. Its raw margin goes to zero only because it fills the graph (density 0.96 at N=7). The rule designed as a control shows the clearest density-independent "gathering" in the round; none of the arrow-carrying rules does.
- **Near-source slowing grows with N in the gradient control and fades in the arrow rules** [O]. The near/far activity ratio of CLOSEW falls 1.03 → 0.89 → 0.61 per unit time. In the formation-acting arrow rules it falls toward 1 (CSPF 1.32 → 1.18 → 1.09).
- **Attachments last longer in events as N grows, and shorter as strength grows** [O]. For CSPH, the correlation time of "probe attached" is 4.6 → 5.9 → 7.0 events with size, and 5.9 → 5.5 at N=6 with strength. For CWPH it is 3.5 → 1.5 with strength.
- **Most N=6 → N=7 changes go the way strengthening goes, but by less than either bracket member** [O]. 55 of 102 channel readings are in the same direction but smaller; 22 are opposite. The bracket gets the direction right and the size wrong.

## 3. How the distinctions moved

The programme's main distinction is between **occupancy** (where the system spends time), **kinetics** (how fast things change, and where), and **succession** (the order of events).

- **Sharpened: succession versus occupancy.** At N≤6 the handover and CSPH's attachment advantage appeared together in one rule. At N=7 the handover is undiminished and the attachment advantage is gone. So the two are produced by the same rules but are not coupled [O].
- **Sharpened: per-event versus per-time preference.** The clock dependence first seen in GT-F34 is now systematic. Strengthening moves the two clocks in opposite directions in CSPH, and every margin must be quoted with its clock [O].
- **Sharpened: preference per density versus occupied density.** The margin is an average of a per-density preference over the occupied density profile [M]. Size and strength load these two factors differently (post hoc). "Attraction" in this grammar is therefore at least two things, and only the per-density part is a property of the rule alone.
- **Blurred: "selective" versus "repulsive" rules.** At N=7 every non-gradient rule has a negative crowding-adjusted margin (−0.095 to −0.136, both clocks) and similar detachment (0.55–0.58). The CSPH/CWPH-versus-PATH distinction that carried E0B's basin question has narrowed. What still separates the families is kinetics (handover weight, flux, persistence), not occupancy.

## 4. Robust and fragile

| Behaviour | Across clocks | Across definitions | Across strength | Across size | Reading |
| --- | --- | --- | --- | --- | --- |
| Handover orientation | order is clock-free | 4/4 steps forward, adjacent and all | all 30 cells | all 30 cells | **robust** |
| Irreversible flux present | — | flux and square affinity | yes (falls at N=6 W16 in formation-acting rules) | yes | **robust** |
| Probe detachment high in arrow rules | both | per probe and counts | grows strongly | stable | **robust in sign** |
| Equal-ratio gap (dissolution-acting more selective) | — | class L1 | grows | grows | **robust** |
| CSPH attachment advantage | clock-dependent | sign depends on form | per event up, per time down | lost at N=7 | **fragile** |
| Near-source slowing | sign depends on clock and family (GT-F30) | — | — | grows (gradient), fades (arrow) | **family-dependent** |
| Probe-only hub share | — | — | suppressed | tracks NULL geometry | **geometric, not emergent** |

## 5. What the strength bracket can and cannot illuminate

- **It can** show that the N=6 → N=7 changes are *not* what strengthening does. Strengthening produces large preference changes, opposite occupancy shifts and a clock split. Growth produces small, mixed changes. Combined with the engaged-load ratio of about 1, **witness amplification is at most a minor contributor to the N=6 → N=7 changes in the arrow-carrying rules**.
- **It cannot** reproduce the published N=5 → N=6 step in size: the calibration verdict is "direction only" in five families and "poor" in CSPH. So it cannot measure how much of any step is amplification. It can only say that amplification would look different.
- **Still not identifiable:** intrinsic size dependence beyond the measured effects; the closure/path rebalancing inside composites (CSPH closure load ×0.87, path load ×1.05); the falling source share (3/N) and null ceiling. All three move with N together in HELD.

## 6. What next — recommendation (not executed)

Candidates were compared factor by factor, as OTR section 6 asks, with no combined score.

| Candidate | Information value | Mechanism novelty | Contrast with prior results | Artefact discrimination | Interpretability | Cost | Cross-programme coherence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **A. Handover mechanism round** (derive the sign of the elementary-square affinity for path rules; ablate slot classes; test whether orientation is a theorem of the grammar) | High: converts the most robust observation into a mechanism, or finds where it breaks | High: no derivation exists (GT-F33 notes the gap) | Directly builds on 30/30 invariance | Separates "grammar theorem" from "grade coincidence" | High: N≤6 exact, partly analytic | Low (minutes) | High: CL-Q05 (transition-enabling dissolution) |
| B. FREE N=7 emergent-hub tranche (option D) | Low–moderate: E1 found no mechanism that predicts a centre; arrow rules are repulsive and sparse; probe-only hubs track geometry below the null | Low | Extends E-CENTRE "not observed" | Moderate | High | High (30–80 min and 3.2 GB per cell) | Moderate |
| C. Source-size control (held K4 at N=7 versus triangle) | Moderate: separates source share and null ceiling from N | Low | Addresses a declared confound | High for that confound | High | Moderate (HELD N=7 cells) | Low |
| D. Component-specific scaling (closure and path engaged loads held separately) | Moderate | Moderate | Addresses the composite-balance confound | Moderate | Moderate | Needs new size-normalised families (a grammar change; ontology proposal) | Low |
| E. Density-composition study (can any rule keep occupancy sparse as N grows?) | Moderate | Low | Follows the post hoc decomposition | Low | Moderate | Low | Low; **risk:** it drifts toward searching for an attractive rule |

**Recommendation: A, a narrower kinetic/handover mechanism investigation.**
- Its reason is information value, not resemblance to gravity. The handover is now the programme's most robust phenomenon, and it is unexplained.
- A derivation would say whether the orientation is a theorem of the path templates or a coincidence of the grades tried. Either answer changes how the succession/occupancy distinction is used.
- It is cheap, exact and interpretable. Its natural follow-up, the FREE-frame handover, can be tested at N=6, where autocorrelation and hub persistence are now available.

**FREE N=7 has become less informative after E1, not more.**
- No E1 observation suggests a mechanism that would make a centre emerge.
- The only density-independent gathering seen was in the reversible gradient control, which is already known not to produce a hub (GT-F22).
- It should stay a separate future decision, revisited if a rule with size-stable gathering or hub persistence appears at N≤6.

Source-size control (C) is the best way to address HELD's built-in confound, if that becomes the priority.

## 7. Additions to the open-question register

- **GT-Q08 — handover orientation as a theorem.** Is the handover's orientation fixed by the path templates for every grade sign and strength, and why? (30/30 invariance; no derivation.)
- **GT-Q09 — clock split under strengthening.** Why does strengthening raise CSPH's per-event attachment preference while lowering its per-time preference? Is it general for dissolution-acting composites with a strong closure part?
- **GT-Q10 — gradient gathering with size.** Does the gradient control's growing crowding-adjusted preference continue beyond N=7? Is it the source triangle's closure witnesses, or the density reweighting?
- **GT-Q07** (coexistence scaling) is partially answered for CSPH at W4: coexistence does not survive to N=7. It stays open for other rules and for FREE.

## 8. Interpretive notes (kept separate)

- **[RS]** The round supports keeping *succession* (an ordered actualisation, robust here) and *gathering* (a time-weighted relation to a reference, fragile here) as distinct notions in the relational picture. The same local rules can carry the first without the second. This is a structural lesson about the grammar, not evidence about the world.
- **[P]** None. A shrinking or vanished advantage in a seven-entity toy chain says nothing about gravity, and a robust event order says nothing about physical time.
- **[T]** Not engaged.
