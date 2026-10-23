# Proposal: federate RRC later

**Status:** proposal only. This branch does not edit `infra/shared-research-coherence-v1`.

**Read from:** commit `999ce6652609d14e0b8f782bf48a195a432c0365`, blob `b67997b358091a98dede5fb1a010468668aacadc` of `research-synthesis/docs/architecture.md`.

## What the architecture already requires

Adding a programme is a pin, an adapter and a review. The steps in that document are:

1. Add a source to `sources/pin-spec.json` with its own namespace, branch, commit at a closed round, artifacts, adapter and lineage.
2. Reuse `coherence_ledger_v1` if the ledger uses the shared schema. Declare extra fields. Do not rely on an undeclared field.
3. Run `synth pin`, `synth check` and the tests. Open a review.

Namespaces `C`, `X`, `XQ`, `M` and `P` are shared and must not be used as the programme namespace. `RRC` is free of that collision on the evidence of the architecture text. A future pin still has to confirm the live registry.

## What RRC asks a later federation round to do

- Namespace: `RRC`.
- Branch: `research/recursive-relational-complexity`.
- Commit: a closed-round commit, not this opening commit and not an open plan.
- Artifacts: `relational-complexity/coherence/findings.jsonl`, `relational-complexity/coherence/relations.jsonl`, and the validator that matches `constraint-lab/src/rs_constraint_lab/coherence.py` at `6cae75c2`.
- Adapter: `coherence_ledger_v1`, with no extra required fields at opening. If RRC later adds a field, it must be declared in the pin rather than discovered as drift.
- Lineage: RRC descends from the Constraint Laboratory grammar at the base commit `e2b5dc4c` and reads GT feasibility at `38e92015`. An evidential edge between RRC and CL, or RRC and GT, is not an independence claim. The inherited GT ledger that happens to sit in this branch is not the GT source. GT stays pinned to its own branch, as the architecture already requires for CL.

## What this proposal does not do

- It does not add RRC rows to the shared ledger.
- It does not treat a cross-programme analogy as evidence.
- It does not assert that any RRC observation answers a shared question `XQ::`.
- It does not modify books or ontology.

No recommendation is ready before RRC-001 is closed. The federation intake waits for that close, and for a human review on the synthesis branch.
