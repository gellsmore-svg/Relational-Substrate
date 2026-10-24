# RRC atlas registers

Machine-readable records for the continuation described in `docs/atlas-charter.md`. A later session should read `PROGRESS.md`, then this file, then the JSONL registers. Do not reconstruct the agenda from conversation.

| File | Contents |
| --- | --- |
| `ideas.jsonl` | Possibilities, including ones with no experiment |
| `coverage.jsonl` | Regions and their status |
| `equivalences.jsonl` | Distinct specs with the same mathematical object. Composer identities may be recorded before a round. Cell comparisons follow a verified batch. Rows from EQ-008 onward name `equivalence_type`. Earlier rows do not: `composer` is an identity of the opening composer, and `cell` is weight-table equality in the declared order |
| `patterns.jsonl` | Cross-cell relations. A row here is not an order to investigate |
| `questions.jsonl` | Open questions. No row has to be closed by the next round |

Experiment output lives in `results/<round-id>/`, one directory per frozen round. RRC-001’s `results/rrc-001/` is historical and is not an atlas batch.

Status words for coverage: `open`, `frozen`, `exhaustive`, `partial`, `sampled`, `analytical`, `infeasible`.

Status words for ideas: `open`, `selected`, `partial`, `explored`. `selected` means a frozen plan names the idea. `explored` means a verified batch has reported it. Neither word means the idea was confirmed.

Equivalence status `method` is an identity of the comparison, checked by a unit test. It is not a scientific cell. EQ-008, EQ-014, EQ-017, and EQ-020 use that status. EQ-014 has type `line_graph_total_domination`: deadlock states of one incident-prohibit template, not equality of whole weight tables across grammars. EQ-017 is weight-table identity of `incident_count` `ge 1` with incident present, and of `eq 0` with incident absent. EQ-018 and EQ-019 are atlas-006 cell rows. EQ-020 has type `effective_cardinality`: the uniform `ge 2` multiply, scoped in `docs/incident-count-cardinality.md`. EQ-021 has type `strong_lumpability`: the present-edge-count label on an empty list and a constant positive baseline. It does not cover the degree sequence or the present line graph.

Composition formulations are in `docs/composition-taxonomy.md`. That note is not a round. `COV-COMPOSITION` and `COV-COMPOSITION-LIBRARY` stay `open`.
