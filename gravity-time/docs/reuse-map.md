# Reuse map

## 1. Technical base

Remote state was verified on 2026-10-13.

| Branch | Head | State | Used as base? |
| --- | --- | --- | --- |
| `main` | `84ae9a4` | CBO v2.4 books and repository CI; no Constraint Laboratory code beyond Generation 7-era | no; read for the CBO baseline |
| `research/constraint-lab-v0.8e-conjunctive-gates` | `19d243a` | closed and reviewed | no; superseded by 8F/8G |
| `research/constraint-lab-v0.8f-interaction-topology` | `ec319f2` | closed, CI success | no; contained in 8G |
| `research/constraint-lab-v0.8g-formal-integration` | `22e252e` | **closed, reviewed, CI success; formal catalogue CL-T01–T25, Q01–Q05** | **yes** |
| `research/constraint-lab-v0.8h-history-as-state` | `e9f8f3b` | **in progress**: H0 plan frozen, no result | no; not yet stable |
| `research/stochastic-calculator` | `aa06213` | historical, SC-001–SC-027R | read only |

8H is the most recently named branch, but it is mid-generation, so it is not a stable base. Its own charter starts from the reviewed 8G head, which is the base here. The H mechanism 8H is testing is not needed for G0.

## 2. Findings reused as constraints on this programme

| Source | Content | How it constrains GT |
| --- | --- | --- |
| CL-T01, CL-T03 | Rule factors multiply event weights, and logits add. A single weighted slot has `m/(m+5)`-type normalisation | The algebra of every GT rule |
| CL-T12 | Every positive current-state event-weight table is constructible with unbounded factors | Representability of a basin is guaranteed. GT asks which *minimal, label-covariant, relation-reading* rules give one |
| CL-T13 | Rule cardinality cannot create an absent monomial | Adding more K2 rules cannot imitate a K3 closure template |
| CL-T17 | Single-toggle pair epochs have period two | Stationary computations use a lazy chain or a linear solve, not raw power iteration |
| CL-T18, CL-T19 | An autonomous single-action law factorises, and shape given edge count is orbit-counting | **Predicts the density control produces no relational attraction.** Basin evidence must break factorisation |
| CL-Q04 | Which incidence-aware, pair-coupled rules break factorisation? | G0's closure and adjacency templates are such rules. G0 answers part of CL-Q04 |
| CL-Q05 | Transition-enabling dissolution | Relevant to escape from a basin (G3) |
| CL-N01, F8C-GATE-REFRESH, F018 | Apparent memory and forgetting depend on the clock; current efficacy is not memory | Temporal observables must name their clock |
| F8C-EDGE-DRIFT, F8C-DRIFT-DIRECTION, F010-OCCUPANCY-AXIS, F8D-DRIFT-MAGNITUDE-SCOPE | Local drift gives the sign of an occupancy shift and not its size; stationary mass is not inferred from drift | Radial drift and stationary basin are separate observables |
| F004-PASSAGE-AFTER-OCCUPANCY | Most of a stationary delta can be occupancy | Basin claims separate occupancy from passage |
| F8B (F013) | Plug-in information overstates finite-sample information | GT uses exact kernels, no sampling |
| Stochastic calculator SC-026/027 | "Well-like" occupancy came from birth-death bias and reflecting capacity bounds | **Null control:** boundaries and caps mimic attractors. GT uses no caps, and declares the held source as a boundary |
| H3S, technical volume ch. 45 | Four predeclared cadence laws failed a prospective test; temporal boundary of a correction rule | Negative history for "universal cadence". It is not reused as a mechanism |
| First edition, technical volume ch. 6 and 28 | Clock slowing by substrate tension; gravitational regimes as tension gradients | Candidate interpretation T-TENSION only, demoted in CBO v2 |
| CBO v2.4 App E | Spatiality open; time as the ordering of actualisation; T0 open | Governing commitments |

## 3. Code reused

| Module | Use |
| --- | --- |
| `constraints.parse_expression(order=2)`, `Constraint`, `Choreography` | Every GT rule is parsed from ordinary DSL text. No new grammar |
| `kernel.build_kernel` | Exact full-event kernel. An N=6 kernel with 120 rule instances builds in about 5 s |
| `exact` (SCCs, recurrent components, rational stationary, absorption) | Recurrent-class structure, exact rational checks at N=5 |
| `explore08.plan_hash`, `require_frozen_plan`, `remote_contains`, `attention_vector` | Frozen-plan contract and attention vectors |
| `explore08a.verify_journey_chronology` | Plan-then-result chronology test |
| `durable` | Atomic JSON, canonical hashing |
| `coherence` | GT keeps its own ledger in the same schema (`ledger_dir(root)`) |
| `state.edges`, `component_count` | Relational distance and components |

New code: a GT module that builds the template rule sets, solves stationary laws with a numpy linear solve or lazy iteration, computes the GT observables, and runs the bounded item executor. It adds no kernel and no grammar.
