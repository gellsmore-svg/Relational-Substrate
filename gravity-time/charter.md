# Gravity, Temporality and Emergent Spatiality — research charter

**Programme id:** GT. **Branch:** `research/gravity-time-admissibility`. **Base:** `22e252e560cc711d337b6ae506b0fb76728247d6`, the closed and reviewed Generation 8G head of the Constraint Laboratory (formal integration). The base choice is justified in [`docs/reuse-map.md`](docs/reuse-map.md) §1.

**Instruction:** [`provenance/prompts/GT-P001-agent-input.md`](provenance/prompts/GT-P001-agent-input.md). That file is an agent transcription of the session input, not a byte capture.

## 1. Question

Can a minimal architecture of relational constraints, acting through constrained stochastic actualisation, produce both of the following?

1. Behaviour resembling gravitational attraction: a stable relational basin toward which relational distance tends.
2. Systematic differences in the relative progression of recurrent processes, analogous to gravitational clock-rate differences.

Can both arise from one constraint architecture, without imposing the equations or mechanisms that describe them? And does the same architecture help explain spatial ordering, distance, direction and temporal succession?

The programme is not asked to prove the Relational Substrate. It asks what follows from its proposals, where they are coherent, where they need refinement, and whether their explanatory reach extends this far. A model that cannot produce gravitational behaviour is a result.

## 2. Commitments inherited from the CBO v2.4 baseline

These are taken from `books/v2/analysis/research-baseline.md` and Appendix E on `main` at `84ae9a4`. They are not revised here.

- Relational primacy is the governing proposal.
- T0 names whatever conditions actualisation. Its deeper ontology is open.
- T1 is actualised, history-bearing relational order.
- Constrained stochastic actualisation is a working hypothesis.
- Admissibility (forbidding) and tendency (favouring) are distinct.
- T-C-R is the candidate grammar of consequential relation.
- Substrate spatiality is unresolved: intrinsic, emergent and proto-spatial families are all live.
- Time as the ordering of actualisation is a working ontological interpretation, not a temporal theory.
- A fundamental limit or constraint on primitive event succession is an open candidate.
- **Design is an upstream premise of the programme, not an outcome.** No model result is offered as evidence for or against it.

Historical mechanisms are not canonised. Substrate tension, closure knots and a universal cadence are preserved only as candidate interpretations in the register ([`hypotheses.md`](hypotheses.md)).

## 3. Model class and declared scaffolding

The programme starts inside the existing grammar: the O=2 pair-relation model of the Constraint Laboratory, on N labelled entities with C(N,2) binary relations, single-toggle dynamics and the ordinary rule DSL. A rule's weight multiplies the weight of one toggle, and `prohibit` is the zero. Before any new primitive or expressivity axis is added, the register asks whether the existing grammar can represent the behaviour (CL-T12 already guarantees current-state weight universality with unbounded factors). The scientific question is therefore **which minimal, label-covariant, relation-reading rules** produce a basin, not whether some rule set can be written to produce one.

Anything imposed is declared as scaffolding. It is never presented as emergent.

| Scaffold | Where it is used | What it is not |
| --- | --- | --- |
| **Held source**: a designated set of entities whose mutual relations are prohibited from dissolving | Basin rounds | Not mass and not a gravitating body. It is a fixed relational structure against which a tendency can be measured |
| **Relational distance**: shortest-path length in the current pair graph | Observable only | Not a primitive metric. It is a derived function of the current relations, and no rule reads it |
| **Global event count** (jump-chain clock) | Step-indexed quantities | Not a universal clock. A second convention, continuous time with per-slot rates, is always reported beside it |
| **Labelled entities** and a finite N | Everywhere | Not physical particles. N is a resource bound |

Rules are **label-covariant templates**. A template is instantiated identically over every ordered witness, so no rule names a direction, a source or a place. A template instantiated per witness multiplies once per satisfying witness. That is declared semantics, and it is distinct from duplicating syntax.

## 4. Candidates

All of the following are candidates. None is privileged for resembling familiar physics.

- **D**, directional tendency: weights make some trajectories preferentially realised.
- **A**, asymmetric pathway availability: the admissible future pathways change, and a tendency may appear without any directional instruction.
- **A→D**, emergent tendency from admissibility: hard or soft restriction of pathways produces a statistical directional bias.
- **U**, unified gravitational-temporal constraint: the configuration that produces a basin also changes the accessibility, coordination or frequency of recurrent actualisations.
- **Additional candidates and artefacts** are listed in the register: coordination-mediated tendency; clock-convention dependence; density and boundary artefacts.

## 5. Governance

The laboratory's standards apply in full:

- predeclared and frozen plans, committed and pushed before execution;
- exact small-system analysis where possible;
- deterministic replay, so no seed is needed for exact work;
- symmetry and parameter robustness;
- negative controls;
- null and failed results recorded;
- observation, inference and interpretation kept apart;
- frozen comparison targets.

The programme keeps its own records under `gravity-time/`: plans and journey, reports and tables, provenance, and a coherence ledger in the laboratory's schema. It reads the laboratory's ledgers and the formal catalogue without changing them. Proposals that would change the ontology are written as explicit proposals for later review ([`docs/ontology-proposals.md`](docs/ontology-proposals.md)). The CBO books are not edited.

Pass and fail are reserved for software, CI, validation and execution contracts. No system is ranked by a scalar.
