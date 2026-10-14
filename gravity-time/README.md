# Gravity, Temporality and Emergent Spatiality (GT)

An independently governed research programme built on the Constraint Laboratory (base: Generation 8G, `22e252e`).

| Record | Path |
| --- | --- |
| Charter | [`charter.md`](charter.md) |
| Hypothesis register | [`hypotheses.md`](hypotheses.md), canonical [`hypotheses.jsonl`](hypotheses.jsonl) |
| Reuse map and base choice | [`docs/reuse-map.md`](docs/reuse-map.md) |
| Dependency graph | [`docs/dependency-graph.mmd`](docs/dependency-graph.mmd) |
| Roadmap and discrimination tests | [`docs/roadmap.md`](docs/roadmap.md) |
| Feasibility | [`docs/feasibility.md`](docs/feasibility.md) |
| Plans and journey | [`plans/`](plans/) |
| Report, G0 and G1 | [`reports/gt-g0-g1-report.md`](reports/gt-g0-g1-report.md) |
| Method (from GT-P002) | [`../research-methods/open-thetical-research.md`](../research-methods/open-thetical-research.md), OTR 1.0 |
| E0 coverage and selection audit | [`docs/e0-coverage-and-selection.md`](docs/e0-coverage-and-selection.md) |
| E0A reflection and E0A→E0B decision | [`reports/gt-e0a-reflection.md`](reports/gt-e0a-reflection.md) |
| Report, E0A and E0B (with completion answers) | [`reports/gt-e0-report.md`](reports/gt-e0-report.md) |
| Behavioural atlas, E0 | [`reports/gt-e0-atlas.md`](reports/gt-e0-atlas.md), trajectories [`reports/gt-e0-atlas-trajectories.json`](reports/gt-e0-atlas-trajectories.json) |
| E1 machinery: vectorised kernel | [`docs/e1-kernel.md`](docs/e1-kernel.md) |
| E1 observables: scalable implementation and validation matrix | [`docs/e1-observables.md`](docs/e1-observables.md) |
| E1 scale and witness-strength confound audit | [`docs/e1-scale-confound-audit.md`](docs/e1-scale-confound-audit.md), census [`reports/e1-scale-census.json`](reports/e1-scale-census.json) |
| E1 feasibility, HELD versus FREE | [`docs/e1-held-free-feasibility.md`](docs/e1-held-free-feasibility.md) |
| E1 design alternatives (review draft, not frozen) | [`docs/e1-design-alternatives.md`](docs/e1-design-alternatives.md) |
| E1 pre-freeze review (plain English) | [`reports/gt-e1-prefreeze-review.md`](reports/gt-e1-prefreeze-review.md) |
| **E1 round (GT-P004): frozen plan** | [`plans/round-e1-plan.json`](plans/round-e1-plan.json) (commit `4ba2839`) |
| E1 results report (plain English) | [`reports/gt-e1-report.md`](reports/gt-e1-report.md) |
| E1 behaviour atlas (every cell and channel) | [`reports/gt-e1-atlas.md`](reports/gt-e1-atlas.md), tables [`reports/round-e1-tables.json`](reports/round-e1-tables.json) |
| E1 coherence reflection and next-step recommendation | [`reports/gt-e1-reflection.md`](reports/gt-e1-reflection.md) |
| E1 post hoc margin decomposition (labelled post hoc) | [`reports/e1-margin-composition-posthoc.json`](reports/e1-margin-composition-posthoc.json) |
| E1 execution record | [`provenance/execution-GT-P004.md`](provenance/execution-GT-P004.md) |
| **GT-P005 (E2A, E2B): plain-English report** | [`reports/gt-e2-report.md`](reports/gt-e2-report.md) |
| E2 coverage-and-selection audit | [`docs/e2-coverage-audit.md`](docs/e2-coverage-audit.md) |
| E2 formal mechanism note (square-affinity identity) | [`docs/e2-formal-mechanism.md`](docs/e2-formal-mechanism.md) |
| E2A frozen plan, tables, atlas, reflection | [`plans/round-e2a-plan.json`](plans/round-e2a-plan.json), [`reports/round-e2a-tables.json`](reports/round-e2a-tables.json), [`reports/gt-e2a-atlas.md`](reports/gt-e2a-atlas.md), [`reports/gt-e2a-reflection.md`](reports/gt-e2a-reflection.md) |
| E2B frozen plan, tables, atlas | [`plans/round-e2b-plan.json`](plans/round-e2b-plan.json), [`reports/round-e2b-tables.json`](reports/round-e2b-tables.json), [`reports/gt-e2b-atlas.md`](reports/gt-e2b-atlas.md) |
| E2 mechanism atlas, dissolution analysis, synthesis | [`reports/gt-e2-mechanism-atlas.md`](reports/gt-e2-mechanism-atlas.md), [`reports/gt-e2-dissolution-analysis.md`](reports/gt-e2-dissolution-analysis.md), [`reports/gt-e2-synthesis.md`](reports/gt-e2-synthesis.md) |
| GT-P005 execution record | [`provenance/execution-GT-P005.md`](provenance/execution-GT-P005.md) |
| Coherence ledger and snapshot | [`coherence/`](coherence/) |
| Ontology proposals for later review | [`docs/ontology-proposals.md`](docs/ontology-proposals.md) |
| Provenance | [`provenance/`](provenance/) |

Code: `constraint-lab/src/rs_constraint_lab/gt0.py`, `gt0_exec.py`, `gt1.py`, `gte0a.py`, `gte0b.py`, `gte0_atlas.py`, `gtkernel.py`, `gtobs.py`, `gtobs_validate.py`, `gtobs_fixtures.py`, `gtscale.py`. Commands: `python -m rs_constraint_lab gt0|gt1|gte0a|gte0b ...`. Tests: `constraint-lab/tests/test_gt0.py`, `test_gte0a.py`, `test_gte0b.py`, `test_gtkernel.py`, `test_gtobs.py`. Generated items go to `gravity-time/generated/`, which is gitignored.
