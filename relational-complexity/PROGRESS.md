# RRC progress journal

A new session should read this file first, then `charter.md` and `docs/reuse-map.md`. Do not reconstruct the programme from conversation history.

## Identity

- Programme: Recursive Relational Complexity and Structural Composition (RRC)
- Namespace: `RRC::`
- Branch: `research/recursive-relational-complexity`
- Worktree used to open the branch: `/home/cello/domains/RS-rrc`
- Base commit: `e2b5dc4cb65bafc423047f78468a63c9d6ceb218` (`research/gravity-time-admissibility`, GT-P012 provenance close)
- Method: OTR 1.0, `research-methods/open-thetical-research.md`, sha256 `2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd`

The base is the GT branch tip because that tree already contains the Constraint Laboratory engine, the OTR text, the scientific-plan discipline, and the GT feasibility record. Branching here does not make GT results part of RRC. RRC must not edit `constraint-lab/`, `gravity-time/`, `books/`, or `research-methods/`.

## Source pins

See `provenance/base-commits.md`. The shared synthesis architecture is not on this branch. It is read from `infra/shared-research-coherence-v1` at `999ce6652609d14e0b8f782bf48a195a432c0365`. RRC does not modify that branch. The intake proposal is `docs/synthesis-proposal.md`.

## Stage status

| Stage | State | Commit |
| --- | --- | --- |
| A. Charter, audit, registers, feasibility estimate, journal | in progress at the opening of this file | not yet committed |
| B. Minimal engine and recovery tests | not started | |
| C. Formal definitions for RRC-001 | not started | |
| D. Freeze RRC-001 | not started | no scientific cells have been run |
| E. Execute RRC-001 | not started | |
| F. Interpret and challenge | not started | |
| G. Coherence reflection and RRC-002 decision | not started | |

## Hard rules already in force

- No item may be an indivisible computation expected to exceed five minutes. Target one to three minutes. Watchdog 120 seconds.
- `plan`, `run`, `status`, `resume`, `verify`, `report` are the execution commands, once Stage B exists.
- Do not describe sampling as exhaustive.
- Do not treat six as a privileged size unless a later result says so.
- Do not rewrite frozen plans after execution.
- Do not promote a mathematical result into an ontological claim.
- Bulk output belongs in `relational-complexity/generated/`, which is gitignored. Commit manifests, summaries and provenance.

## Next action

Finish Stage A by committing and pushing this opening record. Then build the smallest exact engine (Stage B) and validate it on identities and synthetic kernels, not on the unopened RRC-001 cells.
