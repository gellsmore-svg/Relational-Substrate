# Research synthesis: a federated map across research programmes

This directory builds **one navigable map across the repository's research programmes without merging or rewriting their records**. It also holds a separate, clearly non-evidentiary layer of metaphors for readers.

**Start here:** [`generated/index.md`](generated/index.md), the front page, with links to every view.

## What it is, and what it is not

**It is:**
- **Federated, not merged.** Each programme keeps its own ledger, validator and governance on its own branch. This layer reads those ledgers at **pinned commits**, refers to their findings by namespaced reference, and never edits them.
  - `CL::` is the Constraint Laboratory.
  - `GT::` is Gravity, Temporality and Emergent Spatiality.
  - `SC::` is the stochastic calculator (catalogued only).
  - `OTR::` is the shared method.
  - `EXT::` and `HIST::` are missing or pending sources.
- **Disciplined about cross-programme claims.** A connection between programmes has:
  - a type from a fixed vocabulary;
  - a formal comparison on eight dimensions (state, transition law, support, clock, projection, intervention, horizon, conditioning);
  - an independence statement, needed because GT and CL share 8G code lineage;
  - controls, alternatives and falsifiers;
  - a written review record.
- **Honest about disagreement.** Contrasts, qualifications, rejected proposals and the programmes' own negative findings have their own view.

**It is not:**
- scientific validation;
- a physical claim;
- a scalar score of anything;
- a replacement for either programme's ledger.

Retrieval similarity is used only to suggest pairs for human review.

## Layout

| Path | Contents | Authority |
| --- | --- | --- |
| `sources/pin-spec.json` | Human-edited declaration of source revisions | Edited by people, under review |
| `sources/manifest.json` | Generated pins: commit, sha256 and git blob of every artifact, lineage, ingestion receipt | Generated from the spec |
| `sources/materialised/` | Byte-identical copies of pinned ledgers and validators, so checks work without the branches | **Not authoritative**; checked against git |
| `ledger/concepts.jsonl` | Shared concepts and themes with plain-language definitions and anchors | Shared layer |
| `ledger/connections.jsonl` | Cross-programme connections, each with an explicit review status | Shared layer |
| `ledger/questions.jsonl` | Shared open questions and candidate discriminating tests | Shared layer |
| `ledger/metaphors.jsonl`, `ledger/metaphor-links.jsonl` | Reviewed metaphors and typed coverage links (**never evidence**) | Shared layer |
| `proposals/` | Candidate relations (including rejected ones, with rationale), draft metaphors, review records, retrieval diagnostics, pin-update proposals; `proposals/seeds/<label>/` holds author seed files verbatim with a receipt and an intake report | Staging |
| `generated/` | Deterministic views (Markdown, Mermaid, JSON) | Regenerated; never hand-edited |
| `snapshots/` | Immutable milestone views with lock files | Immutable |
| `reports/` | Dated syntheses with epistemic status | Dated |
| `audits/` | Starting audit and later audits | Dated |
| `rssynth/`, `synth`, `tests/` | Standard-library Python tool and acceptance tests | Code |

## Commands

Run from the repository root:

```
python3 research-synthesis/synth audit              # pins, branch heads, artifact verification
python3 research-synthesis/synth validate           # manifest, source ledgers (pinned vocabularies), shared records
python3 research-synthesis/synth generate           # rebuild generated/ (deterministic)
python3 research-synthesis/synth check              # everything CI checks (add --no-git for copies only)
python3 research-synthesis/synth update-candidates  # retrieval diagnostics -> proposals/ (never the ledger)
python3 research-synthesis/synth review --id P::0003 --decision undetermined --reviewer "<name>" --rationale "..." [--human]
python3 research-synthesis/synth propose-pin --source GT --commit <sha>   # milestone pin proposal (diff + warnings)
python3 research-synthesis/synth apply-pin --source GT --commit <sha> --reviewed-by "<human name>"
python3 research-synthesis/synth snapshot --name <milestone> --title "<title>"
python3 research-synthesis/synth intake-seeds <dir>  # stage author seed files as unapproved proposals
python3 -m unittest discover -s research-synthesis/tests
```

There are no third-party dependencies, no network access, and no research suite is run.

## Governance

- **Who decides.** The author accepts connections and metaphors (`human_accepted`). Agent review (`agent_reviewed`) is labelled as such and awaits that acceptance.
- **When things change.** Updates are milestone-triggered: a pin moves only after a completed, reviewed round. See [`docs/cadence.md`](docs/cadence.md).
- **What must never be edited.**
  - Programme findings: they are qualified or superseded with directed edges instead.
  - Past snapshots and frozen research records.
  - Books.
- **If upstream changes under a pin.** If a source's bytes change under its pin, or its schema becomes incompatible, `check` fails. Stop, and report the mismatch.

More detail:
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/epistemic-policy.md`](docs/epistemic-policy.md)
- [`docs/acceptance.md`](docs/acceptance.md)
- [`docs/cadence.md`](docs/cadence.md)
- [`audits/2026-10-15-starting-audit.md`](audits/2026-10-15-starting-audit.md)
