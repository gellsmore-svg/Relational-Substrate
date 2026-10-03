# Research chronology for the second edition

Compiled 2026-10-03 from the repository state, all branches, and the author's local workspace. Dates are commit or document dates. Where a claim in the brief could not be located in any record, that is stated rather than filled in.

## Sources inspected

| Source | Location | Date range |
| --- | --- | --- |
| Main branch history (135 commits) | `origin/main` | 2026-05-03 → 2026-08-07 |
| First-edition CBO | `books/coherent-biblical-ontology-bachelors.md` (master draft v3) | 2026-08-06/07 |
| Technical volume | `books/relational-substrate.md` (master draft v1, revised) | 2026-05-25 → 2026-08-06 |
| Pre-June AMS research notes (299 files, migrated) | `research/` | 2025-12 → 2026-06 |
| Modelling and validation docs | `docs/` | 2026-05 → 2026-07-13 |
| Stochastic calculator (SC-001 → SC-027R) | branch `research/stochastic-calculator`, draft PR #2 | 2026-09-10 |
| Constraint Laboratory, Generations 000–001 | branch `research/constraint-lab-v0.1` | 2026-10-03 |
| Constraint Laboratory v0.2 (in progress, uncommitted) | local working tree only | 2026-10-03 |
| Multipath Reasoning origins | `gellsmore-svg/recursive-reasoning-skills/docs/origins.md` | 2026-08 |
| ChatGPT export (AMS origins) | `~/chatgpt-history` | 2025-12 → 2026-02 |

## Phase 0 — AMS origins (December 2025 → April 2026)

The framework begins as the *Aetheric Magnetic Substrate* (AMS). Its picture is a continuous medium whose magnetic constraint geometry and torsion carry form, and whose stable knots ("vortons") are matter. Light, electricity and magnetism are assigned to propagation, reconfiguration and alignment respectively. Books are drafted in several tiers.

**What survived:** continuity, the priority of configuration over assembly, matter as stable form, the Creator/creature boundary, darkness as created condition rather than non-being.

**What was later weakened:** the "aetheric" and "magnetic" descriptors as foundational terms.

## Phase 1 — Rename to RS, sandbox and benchmarks (May 2026)

`1e7f31f` (2026-05-07) renames the project *Relational Substrate*. The rename is substantive: relation is now the foundational claim (F0), and continuity is derived from it. The technical volume adds the transformation tier: five operations, agent dialects, three-layer admissibility, alignment.

A JavaScript sandbox (`src/model.js`) scores "coherence" over molecular, optical and material cases against conventional comparators.

**What was later rejected:** the sandbox as evidence. It was a linear-response affine fitter calibrated per case — "consistency, not derivation" in the project's own words (D4, 2026-07-11).

## Phase 2 — Discipline and the lens verdict (June 2026)

Predeclaration gates, a descriptor registry, an evidence ledger and source-locking are built. Refractive-index and roughness tracks run into source-access walls. The order-effect ("gentle-first protects survival") prediction is corroborated on open Ti-6Al-4V fatigue data against the Miner null (`5f7cda6`, 2026-06-25). It is later extended to three further domains, 10/10 directionally.

**Verdict adopted 2026-06-25:** the RS grammar is a *directional lens*, not a quantitative predictor. Magnitudes come out 30–50× too small without calibration.

**Relevance to CBO:** path dependence is real and history-carrying (a form of persistence-as-memory), but the magnitude claim failed.

## Phase 3 — Re-anchor on topology (July 2026)

D1 (2026-07-11) declares the stress-history programme objective drift. D2–D9 re-lock the objective on a single substrate with a topological soliton as the sole structural primitive, with light and electromagnetism downstream. A conceptual ladder (named T0–T7, which is *not* the books' T0/T1 stack) derives spin-½, quantised charge, emergent homogeneous Maxwell structure and shell structure from a nematic director field. Five parameter-free computational anchors pass: integer Hopf number, the selection rule, the emergent magnetic sector, the Jackiw–Rebbi zero mode and the parity check.

**Honest ceiling:** internal containment is high; empirical correctness is low and capped. No number has been reproduced. The fermion and charge results hold only in a non-generic θ = π class (WP-A lowered confidence). The substrate choice is motivated, not proven.

## Phase 4 — Book consolidation (6–7 August 2026)

`2f53601` renames "vorton" to "closure knot" in both books and replaces the technical volume's research part with the RS-H3S numerical record. H3S is a finite carrier-field calculation: a local patch supported through t = 1, a temporal boundary, and four cadence laws rejected. The H3S raw records are not in this repository. `06cb0dc` adds the CBO coherence chapters (8 and 11) and builds the first EPUBs.

**State of the first edition:**

- The physics chapters still teach closure knots, the closed five-operation set, light as "torsional disturbance" and time as tension-governed reseating, as *declared ontology*.
- There is no stochastic content.
- There is no T-C-R.
- Roughly fifty "foreclosed" positions are spread across the chapters and Appendix A.

## Phase 5 — The stochastic calculator (September 2026)

Branch `research/stochastic-calculator`, draft PR #2 (2026-09-10). A programme of 87,800 trials on arithmetic produced by stochastic rewriting of signed relational populations, verified by an independent oracle.

Established *within the model*:

- **Exact outputs under diverse stochastic paths.** 40,000/40,000 additions were correct. Fixing the entire initial microstate gave 4,000/4,000 correct along 4,000 distinct paths (SC-005, SC-019).
- **Identity as an equivalence class.** Charge-preserving perturbations never changed the number (4,000/4,000). Erasure of an unpaired relation was never repaired (0/1,800). Conservation is not reconstruction (SC-001, SC-008).
- **Designed covariance stabilises an aggregate.** Components with variance 77.2 and covariance −77.2 gave zero net variance (SC-017). *Relations between fluctuations* do the stabilising work.
- **Reliability rises with enforcement.** This is explained without fitting by a conventional survival law, `((1-d)/(1+d))^7`. There is no phase transition or "deepening well" (SC-006, SC-022).
- **Locality costs time, not correctness.** Local cancellation on a ring of regions stays exact while mean events rise from 30 to 356 as regions go from 2 to 32 (SC-013).
- **T-C-R as re-instantiation.** In decimal carry, ten relations are consumed (transmit), a gate certificate is replaced (carry), and a fresh relation is instantiated in the next column (receive). 2,000/2,000 trials were correct. The certificate's information persists while no entity travels. Replay exclusion is load-bearing under duplication faults: 0.8275 and 0.48 accuracy unprotected, 1.0 protected (SC-012, SC-014).
- **Conservation, readable capture and durable readout are separate stabilities** (SC-023, SC-024).
- **Recurrent readability without permanent cleanup.** Pure readout occupied about 95% of the time with around 230 departures and returns, while charge was never lost (SC-027, SC-027R).

Explicitly *not* established: any unique RS mechanism, any physical implication, any necessity of higher-order relations (H5 inconclusive), or full decentralisation (H9 inconclusive). The researchers' own conclusion is that *"the RS contribution at this stage is a concrete experimental vocabulary and test bench, not independent confirmation."*

## Phase 6 — The Constraint Laboratory (3 October 2026)

Branch `research/constraint-lab-v0.1`. The pre-October modelling programme is archived (tag `pre-constraint-lab-2026-10-03`, "archival does not repudiate"). The laboratory restarts *beneath* geometry and particles. It treats a constraint as "a transformation of relational possibility" that "modifies the measure over otherwise possible transitions", and it exhausts small grammars before going deeper. Its charter states the working premises openly: reality is designed; the material runtime is not exhaustive; "the ultimate receiver in the deepest T–C–R sense may be non-material"; the lab cannot access that realm.

Generation 001 is an exhaustive census of memoryless pairwise grammars at N = 2–5 with exact Markov analysis. It found:

- Hard prohibitions alone change *which* transitions exist. They change support, period and halting. Soft weights change only *how likely* transitions are. The report's interpretation is a distinction between **admissibility and tendency**.
- Constraints can cancel: reciprocal grades are baseline-equivalent. "More constraints, more effect" is false.
- Occupation statistics and transition measures come apart. A rule can leave every edge-count summary unchanged while altering entropy rate and reversibility.
- The hoped-for motif "constructive dissolution" did *not* appear at this level. That is recorded as a tension, not retuned.

The v0.2 working tree (uncommitted, in progress at the time of writing) is not cited as evidence.

## Phase 6b — Constraint Laboratory v0.2 (3 October 2026, afternoon)

Branch `research/constraint-lab-v0.2` (head `0170189`). The engine now runs as resumable shards, and two generations are recorded.

- **Generation 1b** removes stacked-weight artifacts from the Generation 1 census. Generation 1's own files are untouched. 1b also shows large exact-kernel variation hidden inside coarse family labels.
- **Generation 2** adds an occupation-count literal. It found 654 new exact kernels, 189 new families and 30 new supports, all from hard count-gated prohibitions. Constructive dissolution was again not found.

These post-date the first v2 draft and are integrated in v2.1.

## Threads named in the brief but not found in any record

The following are named in the brief (§2.3–2.8). They were searched for across every branch, the GitHub organisation, the local workspace, the vector index and the ChatGPT export, and no records were found:

- the "502-series" (recursive relational admissibility, carrier substitution, two-scale closure);
- a "relational stochastic ring" experiment as such;
- separate memory/persistence experiments;
- Navier–Stokes work (Relational Persistence, Layer Validity, Effective Determinism);
- spectral / positive-Grassmannian / amplituhedron work beyond one literature summary (RS-705) in the curated reading corpus.

Partial counterparts do exist:

- **Locality on a ring.** The calculator's local mode is a ring of regions (SC-013).
- **Fluctuation closure.** Designed covariance (SC-017).
- **Population and convergence ideas.** These are recorded only as the *origin story* of Multipath Reasoning, an engineering method that "ships empty of results".
- **Path-dependent memory.** The June order-effect corroboration.
- **Admissibility.** Constraint-lab Generation 001.

**v2.1 update:** the author has since supplied the conclusions of these threads from conversational research. They now inform the ontology, with their provenance recorded in `conversational-research-import-v1.md`, and they are still not cited as repository experiments. The v2 first draft used these themes only to the extent the located evidence supported. Unlocated programmes are treated as *possibly existing elsewhere and unverified*, and are named as such in `research-baseline.md`.
