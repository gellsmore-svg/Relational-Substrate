# Candidate transfer note for the Constraint Laboratory (CL-Q04, CL-Q05)

*Prompt GT-P006, deliverable 9.*
- *These are suggestions only. No Constraint Laboratory record, branch or file was edited or cherry-picked.*
- *The two programmes share the OTR method but keep independent baselines and frozen-plan chronologies.*
- *GT results are in the O=2 pair grammar. They are **not** established for the laboratory's O=3 grammar.*

## Grammar differences to keep in view

| | GT (this evidence) | Constraint Laboratory |
| --- | --- | --- |
| Order | O=2: binary pair relations, single-toggle dynamics | O=3 (pair and triad incidence) in later generations |
| Templates | Label-covariant closure, adjacency and path; factor per witness; `prohibit` = 0 | Fixed incidence-informed templates; history and meta axes considered separately (8G gate) |
| Scaffold | HELD source triangle, or FREE | No held source in the CL passage contrasts |
| Clocks | Jump chain and continuous time with per-toggle rates | Pair-event epochs (F004) and its own clocks |

## Suggested items

### T-1. Support geometry of hard formation bans (for CL-Q05)

- **Claim (theorems).** Under a hard formation ban that reads path witnesses, combined with positive-factor soft rules:
  - dissolution is always admissible;
  - a release is one-way exactly when the released relation is witnessed;
  - the reachable class is one communicating class, so no released relation is permanently lost;
  - the shortest recovery is 1 + the minimum number of dissolutions that break every witness;
  - the reachable set is downward closed.
- **Provenance.** `gravity-time/docs/e3-formal-support-and-recovery.md` §2 (T1–T5). Checked in E3A (plan `ab5f341`, results `595f4a7`; identity S1 in 8 cells, with rule-string references).
- **Assumptions.** Witness conditions never read the released relation. Soft factors are positive. The start is the empty graph.
- **To reproduce or challenge in the laboratory.** State the analogous condition for an O=3 template (do triad witnesses read the released pair?). Check irreducibility of the reachable class; compute gate distances by reverse BFS.

### T-2. Four senses of "dissolution enables" and their separation (for CL-Q05)

- **Claim (observations).** Precedence, opportunity (normalisation), rate and strict support enabling separate cleanly under matched removal.
  - Soft rules never strictly enable.
  - Opportunity dominates in 59% of soft groups.
  - Strict enabling needs a hard rule and is neither necessary nor sufficient for direction.
  - An enabled event beats restoration of its support about half the time.
- **Provenance.**
  - GT-P005: `gravity-time/reports/gt-e2-dissolution-analysis.md`; E2A `32ac7f6`, E2B `ecb3e73`.
  - E3A adds recovery kinetics: witnessed releases stay absent longer; gate-limited against rate-limited persistence. Atlas `gravity-time/reports/gt-e3a-atlas.md` §7.
- **To reproduce.** Apply the matched-removal decomposition (rate log ratio, normalisation part, passage within H, race committor) to F004's passage contrasts. The laboratory's `passage.py` eventual committor is the natural analogue of the race committor.

### T-3. Local versus aggregate orientation (for CL-Q04)

- **Claim.**
  - In the O=2 grammar, two-witness path templates are the minimal coupled actions with non-gradient rates. Their square affinity is exactly σ·(deg r − deg q); closure and adjacency templates cancel. This is a theorem (`gravity-time/docs/e2-formal-mechanism.md` §2).
  - The aggregate orientation follows σ in 36/36 cells and on 128 grid points (E3A scan). It is **not proved**, and 6–36% of square-level circulation runs counter to local affinity.
  - Under hard formation bans, one-way steps can run against the aggregate that two-way circulation carries.
- **To reproduce.** In an O=3 grammar, derive the analogous cross-count asymmetry for triad-reading actions before testing aggregate orientation.

### T-4. An imposed reference participates (methodological, for both programmes)

- **Claim (theorems T7, T8, and an E3B observation).**
  - A held structure's internal relations act as witnesses for others. For the GT triangle this is an exact, orientation-neutral occupancy bias on every attachment.
  - Divided out (a counterfactual instrument), the GT direction-carrying families gather.
- **Provenance.** `gravity-time/docs/e3-formal-support-and-recovery.md` §7.4–7.6; E3B plan `1bc7c18`, results `1fbaf5a`.
- **Relevance to the laboratory.** Wherever a laboratory contrast holds or conditions on a source class, check whether that class's internal relations satisfy the witness conditions of the rules under test.

## Integration suggestion

If the laboratory adopts any item, it should enter the laboratory's own theorem catalogue or coherence ledger with GT provenance (file, commit, finding ID), under the laboratory's governance. GT findings: GT-F45, GT-F49 to F51, GT-F54 to F59.
