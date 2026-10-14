# Research methods (shared)

This directory holds methodological references meant to be shared by more than one research programme in this repository. A method file here is not a result, a theory or an ontology change. Each programme keeps its own plans, results, registers and provenance.

| File | Version | sha256 | Status |
| --- | --- | --- | --- |
| [`open-thetical-research.md`](open-thetical-research.md) | OTR 1.0, 14 October 2026 | `2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd` (10,048 bytes) | Agent transcription of the author's supplied definition, pasted with prompt GT-P002. Not rewritten. Byte identity with the authored file is not established, so the status is `agent_transcription_pending_byte_comparison` |

## Provenance

The OTR text was supplied by the author as a separate document alongside prompt GT-P002 (`gravity-time/provenance/prompts/GT-P002-agent-input.md`). It was transcribed as given. The only alteration is file encoding (UTF-8, LF line endings, one trailing newline). If the author's original file is later imported, compare its sha256 with the value above. If the bytes differ, publish the authored file as a new version and record the difference here. Do not overwrite silently.

## How OTR is applied in GT

The GT programme adopts OTR 1.0 from prompt GT-P002 onward. In GT terms:

- **Direction.** The gravitational-basin question chooses where to look: persistent relational structures, conditional formation and dissolution, held and free arrangements, recurrence, direction and relational distance. It does not choose results.
- **Rounds.** Each exploratory round (GT-E0A, GT-E0B, …) has its own frozen plan, committed and pushed before its scientific cells run. A later round is chosen only after the earlier result has been recorded and interpreted. The reason is recorded in a decision note and in `gravity-time/plans/journey.jsonl`.
- **Records.** Results go into GT's own ledger (`gravity-time/coherence/`), in the Constraint Laboratory's ledger schema. They are not merged into the laboratory's register.
- **Layers.** Each written result keeps five layers apart: formal-system observation; mathematical mechanism or inference; RS / global-coherence interpretation; physical comparison; theological premise. Design is an upstream premise and is not tested.

## Sharing one version across branches

A file on one branch does not appear on another. This file was first committed on `research/gravity-time-admissibility`. That commit touches only `research-methods/` and GT provenance, so the methodology can be carried across in one of two ways. Neither has been done; both await the author's direction.

1. **Recommended: land on `main`.** Open a small PR that adds only `research-methods/` to `main`. Each research branch then picks it up by a merge from `main` or by a cherry-pick of that one commit. Every programme cites the version and sha256 in the table above.
2. **Cherry-pick between research branches.** Cherry-pick the commit that adds `research-methods/` onto the Constraint Laboratory branch in use (8H or its successor). Record the resulting commit and the file sha256 in that branch's provenance. This must not happen while a laboratory generation is mid-execution without the author's explicit direction, because it would change that branch's history during a frozen round.

Either way, a programme references the method as `research-methods/open-thetical-research.md`, OTR 1.0, with the sha256 above. A changed definition is a new version with a new row, never an in-place edit.
