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
| A. Charter, audit, registers, feasibility estimate, journal | committed and pushed | `7260f0477ab4e3d9d25896fc0c5087eb945d6ebe` |
| B. Minimal engine and recovery tests | committed and pushed | `399dba247061b10823f31bfbf5148d9a8099c9a7` |
| C. Formal definitions for RRC-001 | committed and pushed | `2053b8bddc94b3a9b1d5db712f4c91c6518a681b` |
| D. Freeze RRC-001 | in progress in this edit | plan written, cells not run |
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

## Engine state at Stage B

Package `relational-complexity/src/rrc`. Version `rrc-0.1.0`.

- Exact rational strong lumpability, augmentations (`interface`, `edge_count`, `parity`, `interface_wedge_counts`), lumpable closure, recurrent classes.
- Stationary laws use parity-balanced iteration (a positive single-toggle chain has period 2). Cross-check: a second start, and a dense solve when the state count is at most 1,024.
- Commands: `plan`, `run`, `resume`, `status`, `verify`, `report`, `preflight`, `coherence-view`, plus a hidden `worker`.
- `plan` refuses while `plans/rrc-001.json` is absent. That absence is intentional.
- Recovery tests cover death during an item, death after a valid result, a partial write, invalid JSON, a failed item, a timeout, a sibling item surviving, and an incompatible plan.
- Identity fixtures cover the unconstrained kernel, including a bit-exact match to `rs_constraint_lab.kernel.build_kernel` at N=3 and N=4. They do not compute soft-wedge or hard-wedge lumpability.

## Next action

Push this freeze commit. Only after it is on `origin` run:

```text
python -m rrc run --round rrc-001 --max-items 6 --budget-seconds 180
```

Repeat until pending is 0. Do not edit `plans/rrc-001.json`. Then verify, write the atlas, and only then interpret.
