# Provenance and source dependence

Generated view. Programme ledgers are authoritative in their own branches; the shared layer reads them at the pins below. **Local tree** says whether the path exists in this branch's checked-out tree; programme files do not, and are read from git objects or from the non-authoritative materialised copies under `sources/materialised/`.

| Source | Programme | Role | Status | Branch | Pinned commit | Round boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `CL` (CL::) | Constraint Laboratory | research_programme | **INCLUDED** | `research/constraint-lab-v0.8n-h2-controlled-passage` | `e650d71bda72` | Prompt 008N closed at e650d71 ('provenance: close Prompt 008N ...'); immutable snapshot through-generation-008n.md published in cc9678b |
| `GT` (GT::) | Gravity, Temporality and Emergent Spatiality | research_programme | **INCLUDED** | `research/gravity-time-admissibility` | `79fa6b011944` | GT-P009 (E5A) closed at 79fa6b0 ('GT-P009: provenance close ...'); snapshot through-gt-e5a.md |
| `CL-8G` (CL::) | Constraint Laboratory (8G, common ancestor) | lineage_anchor | **LINEAGE_ONLY** | `research/constraint-lab-v0.8g-formal-integration` | `22e252e560cc` | 8G closed; common ancestor of CL 8N and GT |
| `SC` (SC::) | Stochastic Relational Calculator | test_apparatus | **CATALOGUED_ONLY** | `research/stochastic-calculator` | `aa06213ce42e` | draft PR #2; last commit 2026-09-10; no structured ledger |
| `OTR` (OTR::) | Open-Thetical Research method (shared) | shared_method | **CATALOGUED_ONLY** | `main` | `05b15b0d903d` | OTR 1.0 on main (PR #7) |
| `EXT-SYNTH-20261015` (EXT::) | External cross-research synthesis (2026-10-15) | external_interpretation | **EXTERNAL_STORED** | `—` | `—` | Supplied with the author pack (background/2026-10-15-cross-research-synthesis.md) and stored verbatim. Exploratory evidence synthesis by its own statement; its cosine scores are lexical retrieval measures, not evidence. A dated interpretation, not independent experiment evidence. Its historical claims are secondary pointers into private archives (HIST, pending). |
| `HIST` (HIST::) | Historical archives (505-507, Work 11, 46-48) | historical_archive | **PENDING_INTAKE** | `—` | `—` | Private archives; not in the repository or the local workspace (searched 2026-10-15 by name). Expected archive names, sha256 and primary paths come from the author's seed manifest (proposals/seeds/2026-10-15-author-pack/source-manifest.json) and are unverified until the original bytes are available. Intake follows 05_HISTORICAL_INTAKE.md. Only pending pointers may reference this namespace. |

## Reviewed pins, schemas and round review state

`commit` is the **reviewed source commit**. Moving branch heads are reported by `synth audit` and `synth check` (staleness) and are never substituted for a pin.

| Source | Reviewed source commit | Source schema (validator blob) | Closed but unreviewed rounds | Note |
| --- | --- | --- | --- | --- |
| `CL` | `e650d71bda72` | `1fc80911d99f` | 008N | 008N closed at the pin; the branch records External Review 008M (8075827) but no review of 008N. Findings created in 008N are shown as closed-but-unreviewed; links resting on them cannot be accepted. |
| `GT` | `79fa6b011944` | `1fc80911d99f` | GT-P009 | GT-P009 (E5A) closed at the pin; awaiting the author's review in draft PR #6. Findings created in GT-P009 are closed-but-unreviewed. |
| `CL-8G` | `22e252e560cc` | `1fc80911d99f` | — |  |
| `SC` | `aa06213ce42e` | `—` | — |  |
| `OTR` | `05b15b0d903d` | `—` | — |  |
| `EXT-SYNTH-20261015` | `—` | `—` | — |  |
| `HIST` | `—` | `—` | — |  |

## Artifacts at the pins

| Source | Path | Kind | sha256 | Materialised copy | Local tree |
| --- | --- | --- | --- | --- | --- |
| `CL` | `constraint-lab/coherence/findings.jsonl` | findings | `aa4060043716…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/coherence/relations.jsonl` | relations | `bcf35359425d…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/src/rs_constraint_lab/coherence.py` | validator | `a99d65438d3d…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/theorem-catalog.jsonl` | theorem_catalog | `09f6137c5c24…` | yes | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/formal/open-problems.md` | document | `da5c6d5b5f60…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/coherence/snapshots/through-generation-008n.md` | snapshot | `ffcd7dfd69f7…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/generation-008n-h2-controlled-passage.md` | document | `5100facd35f7…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/reports/generation-008k-predictive-state-synthesis.md` | document | `d0e469a80d33…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `CL` | `constraint-lab/docs/scientific-plan-discipline.md` | document | `4101d64f8b4d…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/findings.jsonl` | findings | `cd79b3a9792c…` | yes | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/relations.jsonl` | relations | `386e38b86375…` | yes | ABSENT (not tracked on this branch) |
| `GT` | `constraint-lab/src/rs_constraint_lab/coherence.py` | validator | `a99d65438d3d…` | yes | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/coherence/snapshots/through-gt-e5a.md` | snapshot | `977127fa272d…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/reference-architecture-review.md` | document | `bc7b74aa53ff…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/e3-cross-programme-transfer.md` | document | `e20264f7ff6c…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/e4-cross-programme-transfer.md` | document | `4fecf0984f7f…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-p008-cross-programme-transfer.md` | document | `0564d68b2360…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/docs/gt-e5a-cross-programme-transfer.md` | document | `c755646adbae…` | no (pointer only) | ABSENT (not tracked on this branch) |
| `GT` | `gravity-time/reports/gt-e5a-report.md` | document | `fcb002551216…` | no (pointer only) | ABSENT (not tracked on this branch) |
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

- `CL` **descends_from** `CL-8G`: 8N descends from 8G (22e252e) through 8H-8M
- `GT` **descends_from** `CL-8G`: GT branch was created from CL 8G (22e252e); shares the constraint-lab DSL, kernel builder and coherence validator
- `GT` **carries_inherited_copy_of** `CL-8G`: constraint-lab/coherence/{findings,relations}.jsonl on the GT branch are byte-identical to 8G and are NOT read as CL evidence

## Adapter reports

| Source | Counts | Problems |
| --- | --- | --- |
| `CL` | coherence_ledger_v1: 216, theorem_catalog_v1: 108 | 0 |
| `CL-8G` | — | 0 |
| `EXT-SYNTH-20261015` | — | 0 |
| `GT` | coherence_ledger_v1: 104 | 0 |
| `HIST` | — | 0 |
| `OTR` | document_v1: 1 | 0 |
| `SC` | document_v1: 4 | 0 |
