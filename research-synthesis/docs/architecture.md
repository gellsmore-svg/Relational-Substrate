# Architecture

## 1. Federation model

```
programme branches (authoritative)          shared layer (this directory)
  CL  constraint-lab/coherence/*.jsonl   --pin-->  sources/manifest.json --adapter--> source nodes CL::*
  GT  gravity-time/coherence/*.jsonl     --pin-->        (sha256, git blob)              source nodes GT::*
  CL  constraint-lab/formal/theorem-catalog.jsonl  -->                                   formal claims CL::CL-T*
  SC  stochastic-calculator/*.md (catalogued)      -->                                   document nodes SC::<path>
                                                         ledger/*.jsonl  ----------------> concepts C::, connections X::,
                                                                                           questions XQ::, metaphors M::
                                                         generated/ (projection; never authoritative)
```

- **Pins.**
  - `sources/pin-spec.json` names a branch and a full commit for each source, plus the artifacts to read.
  - `synth pin` verifies that every path exists at that commit. It records sha256, size and git blob id. It writes byte-identical copies of the ledgers and validators that adapters need to `sources/materialised/`.
  - The copies are a convenience for offline checking and are **not authoritative**. `check` compares each copy with the git object at the pin whenever git can reach it.
- **Adapters.** Adapters validate real upstream records under their own pinned rules.

  | Adapter | What it does |
  | --- | --- |
  | `coherence_ledger_v1` | Reads the vocabulary (layers, statuses, relation types, robustness keys) from the **pinned** `coherence.py` with `ast`, never executing it, and validates the upstream rows under that vocabulary |
  | `theorem_catalog_v1` | Reads the CL theorem catalogue |
  | `document_v1` | Registers document pointers only |

  - Each source declares its optional fields: CL has `formal_refs`, GT has `dependence`. An undeclared field is reported, so silent schema drift is caught.
  - If GT's and CL's validators diverge, each is still validated under its own pinned rules.
- **Namespaces.**
  - A reference is `NS::local` (the namespace's default revision) or `NS@REV::local` (an explicit revision).
  - Programme namespaces cannot use the shared namespaces (`C`, `X`, `XQ`, `M`, `P`).
  - Two default revisions in one namespace are a collision.
  - A lineage-only revision (for example `CL@008g`) is not ingested, so references to it fail.
- **Lineage.**
  - Each source lists the sources it descends from or carries copies of.
  - GT and CL 8N both descend from CL 8G, so `lineage_shared(CL, GT)` is true. An evidential connection between them cannot claim independence without a written note.
  - The GT branch's inherited copy of the 8G CL ledger is **not read**: CL is read only from its own pin.

## 2. Node and edge families

| Family | Kinds | Where |
| --- | --- | --- |
| Source nodes | `source_finding`, `source_question`, `formal_claim`, `source_document` | Adapters (read only) |
| Shared nodes | `concept`, `shared_question`, `metaphor` | `ledger/` |
| Scientific edges | `source_relation`, `source_catalogue_link` (upstream), `cross_programme_connection` (shared) | `graph.json` → `scientific_edges` |
| Metaphor edges | `metaphor_link` (seven types) | `graph.json` → `metaphor_edges` |
| Provenance edges | `lineage`, `membership` | `graph.json` → `provenance_edges` |

- **The two vocabularies are disjoint.**
  - Connection types: `exact_theorem_correspondence`, `tested_structural_analogy`, `common_definition`, `shared_implementation_assumption`, `epistemic_compatibility`, `explicit_contrast`, `qualifies`, `supersedes_interpretation`, `untested_hypothesis`, `instance_of_theme`.
  - Metaphor link types: `covers_concept`, `illustrates_relation`, `bridges_metaphors`, `complements`, `conflicts_with`, `fails_for`, `requires_qualification`.
- **The disjointness is asserted** in code, in the validator and in tests.

## 3. Views

`synth generate` produces deterministic files: no timestamps, sorted output, the same bytes from the same inputs.
- a front page;
- thematic projections:
  - provenance;
  - links;
  - contradictions and nulls;
  - questions;
  - candidate bridges;
  - metaphor coverage, overlap and gaps;
  - chronology;
- one page per theme;
- `graph.json`, so richer viewers can be added later.

Statuses appear in text (for example "AGENT-REVIEWED (awaiting human acceptance)", "MISSING"), not only in colour. Mermaid charts are kept small and per-topic. A test bounds their edge counts.

## 4. Adding a programme

1. Add a source to `sources/pin-spec.json`, with its own namespace, branch, commit at a closed round, artifacts, adapter and lineage.
2. If its ledger uses the shared coherence schema, reuse `coherence_ledger_v1` with the declared extra fields. Otherwise, write an adapter that validates its records under its own rules.
3. Run `synth pin`, `synth check`, and the tests, then open a PR for review.

## 5. Discovery

`synth update-candidates` ranks cross-programme pairs by a deterministic TF-IDF cosine over statements (`rssynth/discover.py`). Every candidate is a ranking aid only.
- **Controls:**
  - a cap of 3 candidates per node;
  - a cap of 2 per near-duplicate cluster;
  - a flag on possible inherited wording;
  - a calibration list showing where reviewed connections rank.

  On 2026-10-15, three of nine reviewed connections had zero similarity, and the top-ranked candidate was a boilerplate false positive, rejected as P::0008.
- **Embeddings.** No embedding model is used. If one is added, its name and version must be pinned, and CI must not need network access.
