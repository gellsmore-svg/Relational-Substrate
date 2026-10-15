# Runbook

The shared synthesis hub is the canonical place for **cross-programme** coherence: links, contrasts, nulls, questions and metaphors across the Constraint Laboratory (CL) and Gravity/Time (GT). Each programme stays authoritative for its own plans, validators and results on its own branch.

Everything below is standard-library Python 3. No network, no third-party packages, no experiment is run.

## Daily use (read only)

| Want | Do |
| --- | --- |
| The map | Open [`generated/index.md`](../generated/index.md) |
| One theme | `generated/themes/<concept>.md` (Markdown and Mermaid) |
| Everything, machine-readable | `generated/graph.json` |
| What the author's next instruction will ratify | [`generated/round-trips.md`](../generated/round-trips.md) |
| Historical intake state | [`generated/historical-coverage.md`](../generated/historical-coverage.md) |
| Health check | `python3 research-synthesis/synth check` |

## The milestone cycle (after a programme round closes)

Nothing runs on a timer. A cycle starts only when a CL or GT round is **closed** (its close commit pushed).

1. **Check provenance.** `synth audit` shows each pin, the branch head and whether the head moved past the pin (`behind_branch_head`, or `diverged_from_branch`).
2. **Propose the pin.** `synth propose-pin --source GT --commit <close sha>` writes a pin proposal listing added, removed and rewritten upstream rows.
3. **Review.** Read the new findings. Draft relations or questions as **proposals** (never in the ledger). Seed files from a programme go through `synth intake-seeds <dir>`.
4. **Adopt.** `synth apply-pin --source GT --commit <sha> --standing-decision AD-0006` (the author's standing instruction of 2026-10-16). Refused for a non-descending proposal or one with warnings; those need `--reviewed-by "<name>"`. Pins never move on a timer: adoption still happens only at a milestone, after a round closes.
5. **Regenerate and check.** `synth generate`, then `synth check`. Run `generate` twice: the output must be byte-identical.
6. **Snapshot.** `synth snapshot --name <milestone> --title "<title>"`. Snapshots are immutable and hash-locked.
7. **Close the round trip.** `synth round-close --id RT-000N --date <d> --report <path> --reported-at <sha>`, regenerate, commit. `round-trips.md` now displays every open recommendation with scope and qualification.
8. **PR.** Open or update the synthesis PR, and merge it once CI is green (AD-0006).
9. **Next instruction.** At the author's next instruction, run `synth ratify --round-trip RT-000N --decision-id AD-000M --date <d> --instruction "<verbatim>" [--object <id>]`. Ratification accepts synthesis interpretations at their displayed categories only. It is not scientific review of a CL/GT generation and not publication consent.

## Historical (private) inputs

- Keep the archives outside the repository. Verify with `synth hist-inventory --archive <zip> ... --out <outside dir>`.
- Re-hash cited members with `synth hist-verify --archive-dir <dir>` or `RS_HIST_ARCHIVE_DIR=<dir> synth check`. Without the archives these checks report `requires_private_input`, never a pass.
- Nothing historical is published without an explicit `publication_consent` decision ([`historical-intake.md`](historical-intake.md)).

## Stop conditions

`check` fails and work stops when: a pinned artifact or materialised copy no longer matches its digest; an upstream schema changes; an implicit acceptance has no logged ratification; a historical record lacks consent or a matching digest; or a file outside the synthesis layer (other than the root README link) changes. Report the failure; do not weaken a check to pass.

## Using the hub from a research branch

See [`branch-integration.md`](branch-integration.md).
