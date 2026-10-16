# Provenance and source dependence

Generated view. Programme ledgers are authoritative in their own branches; the shared layer reads them at the pins below. **Local tree** says whether the path exists in this branch's checked-out tree; programme files do not, and are read from git objects or from the non-authoritative materialised copies under `sources/materialised/`.

| Source | Programme | Role | Status | Branch | Pinned commit | Round boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `CL` (CL::) | Constraint Laboratory | research_programme | **INCLUDED** | `research/constraint-lab-v0.8p-stopping-sufficiency` | `08d7017be856` | 8P closed at 08d7017be85616df7bc5b2934e8076bdcc73a319; annotated tag constraint-lab-008p-close dereferenced; separate closed 8O milestone retained |
| `GT` (GT::) | Gravity, Temporality and Emergent Spatiality | research_programme | **INCLUDED** | `research/gravity-time-admissibility` | `e2b5dc4cb65b` | GT-P012 (E5D) closed at e2b5dc4 ('GT-P012: provenance close ...'); snapshot through-gt-e5d.md |
| `CL-8G` (CL::) | Constraint Laboratory (8G, common ancestor) | lineage_anchor | **LINEAGE_ONLY** | `research/constraint-lab-v0.8g-formal-integration` | `22e252e560cc` | 8G closed; common ancestor of CL 8N and GT |
| `SC` (SC::) | Stochastic Relational Calculator | test_apparatus | **CATALOGUED_ONLY** | `research/stochastic-calculator` | `aa06213ce42e` | draft PR #2; last commit 2026-09-10; no structured ledger |
| `OTR` (OTR::) | Open-Thetical Research method (shared) | shared_method | **CATALOGUED_ONLY** | `main` | `05b15b0d903d` | OTR 1.0 on main (PR #7) |
| `EXT-SYNTH-20261015` (EXT::) | External cross-research synthesis (2026-10-15) | external_interpretation | **EXTERNAL_STORED** | `—` | `—` | Supplied with the author pack (background/2026-10-15-cross-research-synthesis.md) and stored verbatim. Exploratory evidence synthesis by its own statement; its cosine scores are lexical retrieval measures, not evidence. A dated interpretation, not independent experiment evidence. Its historical claims are secondary pointers into private archives (HIST, pending). |
| `HIST` (HIST::) | Historical archives (505-507, Work 11, 46-48) | historical_archive | **PENDING_INTAKE** | `—` | `—` | Private archives; not in the repository or the local workspace (searched 2026-10-15 by name). Expected archive names, sha256 and primary paths come from the author's seed manifest (proposals/seeds/2026-10-15-author-pack/source-manifest.json) and are unverified until the original bytes are available. Intake follows 05_HISTORICAL_INTAKE.md. Only pending pointers may reference this namespace. |

## Reviewed pins, schemas and round review state

`commit` is the **reviewed source commit**. Moving branch heads are reported by `synth audit` and `synth check` (staleness) and are never substituted for a pin.

| Source | Reviewed source commit | Source schema (validator blob) | Closed but unreviewed rounds | Note |
| --- | --- | --- | --- | --- |
| `CL` | `08d7017be856` | `1fc80911d99f` | 008O, 008P | 8N externally reviewed in 8O (008N-chatgpt-review-v0.8n.md). 8O and 8P closed, exact-head CI successful, external scientific review pending. Pin adoption is administrative intake, not scientific review or interpretation acceptance. |
| `GT` | `e2b5dc4cb65b` | `1fc80911d99f` | GT-P009, GT-P010, GT-P011, GT-P012 | GT-P009 to GT-P012 closed at the pin; awaiting the author's scientific review in draft PR #6. Findings created in GT-P009 to GT-P012 are closed-but-unreviewed. |
| `CL-8G` | `22e252e560cc` | `1fc80911d99f` | — |  |
| `SC` | `aa06213ce42e` | `—` | — |  |
| `OTR` | `05b15b0d903d` | `—` | — |  |
| `EXT-SYNTH-20261015` | `—` | `—` | — |  |
| `HIST` | `—` | `—` | — |  |

## Artifacts at the pins

| Source | Path | Kind | sha256 | Materialised copy | Local tree |
| --- | --- | --- | --- | --- | --- |
| `CL` | `constraint-lab/coherence/findings.jsonl` | findings | `2fa6d863c8d8…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/coherence/relations.jsonl` | relations | `b60ef7fc7171…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/src/rs_constraint_lab/coherence.py` | validator | `a99d65438d3d…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/theorem-catalog.jsonl` | theorem_catalog | `4e29fa9d18dc…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/open-problems.md` | document | `139c31942a8c…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/coherence/snapshots/through-generation-008n.md` | snapshot | `ffcd7dfd69f7…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/generation-008n-h2-controlled-passage.md` | document | `5100facd35f7…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/generation-008k-predictive-state-synthesis.md` | document | `d0e469a80d33…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/docs/scientific-plan-discipline.md` | document | `4101d64f8b4d…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/coherence/snapshots/through-generation-008o.md` | snapshot | `638b5a73afbd…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/coherence/snapshots/through-generation-008p.md` | snapshot | `efa90d19e585…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/generation-008o-route-null-factorization.md` | document | `d8482cc050c5…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/generation-008p-stopping-sufficiency.md` | document | `979b306a157e…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/markovization-stopping-factorization.md` | document | `ec1c11aab315…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/task-relative-stopping-sufficiency.md` | document | `4844cfcac71e…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/route-null-weight-identities.md` | document | `53dd5cee8a1d…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/insertionwise-timing-cancellation.md` | document | `5b671b58c3b5…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/stopping-sufficiency-counterexamples.md` | document | `aa0c772af77f…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/provenance/synthesis-handoffs/008O/README.md` | document | `e3cbf1b7b569…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/provenance/synthesis-handoffs/008P/README.md` | document | `dfda26fe82c0…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/provenance/reviews/008N-chatgpt-review-v0.8n.md` | document | `3ea790f772f0…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/provenance/status-changes/008O.json` | document | `e87cb935ec38…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/exploration/generation-008o/close-out.md` | document | `e5b5475bc1a1…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/exploration/generation-008p/close-out.json` | document | `da9c140b7903…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/tables/generation-008o-factor-validation.json` | document | `a25d4ef977b5…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/tables/generation-008p-proof-checks.json` | document | `393c2a3c2fa1…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/findings.jsonl` | findings | `7061af382cdd…` | yes | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/relations.jsonl` | relations | `2559cbd1721b…` | yes | ABSENT (not tracked on this branch) |
| `GT` | `constraint-lab/src/rs_constraint_lab/coherence.py` | validator | `a99d65438d3d…` | yes | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/snapshots/through-gt-e5a.md` | snapshot | `977127fa272d…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/reference-architecture-review.md` | document | `bc7b74aa53ff…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/e3-cross-programme-transfer.md` | document | `e20264f7ff6c…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/e4-cross-programme-transfer.md` | document | `4fecf0984f7f…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-p008-cross-programme-transfer.md` | document | `0564d68b2360…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-e5a-cross-programme-transfer.md` | document | `c755646adbae…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/reports/gt-e5a-report.md` | document | `fcb002551216…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/snapshots/through-gt-e5b.md` | snapshot | `5e96d6ee1395…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/snapshots/through-gt-e5c.md` | snapshot | `fc84a95ddb7b…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/snapshots/through-gt-e5d.md` | snapshot | `68b7a0b02b76…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-e5b-cross-programme-transfer.md` | document | `96a6325c8b95…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-e5c-cross-programme-transfer.md` | document | `8059cffd43ae…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-e5d-cross-programme-transfer.md` | document | `f0731e3b3274…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/reports/gt-e5b-report.md` | document | `af51fcf6ab31…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/reports/gt-e5c-report.md` | document | `1680b104bf8f…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/reports/gt-e5d-report.md` | document | `3bb7a9a94aec…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL-8G` | `constraint-lab/src/rs_constraint_lab/coherence.py` | validator | `a99d65438d3d…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL-8G` | `constraint-lab/coherence/findings.jsonl` | findings | `ac9fef6f3a7f…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `SC` | `stochastic-calculator/RS_FINDINGS.md` | document | `a603f8895767…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `SC` | `stochastic-calculator/DISCOVERIES.md` | document | `5344a6e20d88…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `SC` | `stochastic-calculator/HYPOTHESES.md` | document | `b48f44b74020…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `SC` | `stochastic-calculator/research/VALIDATION.md` | document | `f5eeaa0e891b…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `OTR` | `research-methods/open-thetical-research.md` | document | `2d9023955ddf…` | no (pointer only) | present |
| `EXT-SYNTH-20261015` | `research-synthesis/reports/external-2026-10-15-cross-research-synthesis.md` | document | `1c817747b15e…` | no (pointer only) | present |

## Lineage

Shared lineage means agreement on inherited code, kernels or validators is not independent evidence.

- `CL` **descends_from** `CL-8G`: 8P descends from CL 8G through canonical predictive 8I, 8K, 8L, 8M, 8N and 8O; alternate 8I/8J unmerged
- `GT` **descends_from** `CL-8G`: GT branch was created from CL 8G (22e252e); shares the constraint-lab DSL, kernel builder and coherence validator
- `GT` **carries_inherited_copy_of** `CL-8G`: constraint-lab/coherence/{findings,relations}.jsonl on the GT branch are byte-identical to 8G and are NOT read as CL evidence

## Adapter reports

| Source | Counts | Problems |
| --- | --- | --- |
| `CL` | coherence_ledger_v1: 235, theorem_catalog_v1: 118 | 0 |
| `CL-8G` | — | 0 |
| `EXT-SYNTH-20261015` | — | 0 |
| `GT` | coherence_ledger_v1: 129 | 0 |
| `HIST` | — | 0 |
| `OTR` | document_v1: 1 | 0 |
| `SC` | document_v1: 4 | 0 |
