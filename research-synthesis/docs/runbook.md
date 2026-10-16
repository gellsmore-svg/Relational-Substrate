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
4. **Adopt.** Under AD-0006, use `synth apply-pin --source GT --commit <sha> --standing-decision AD-0006` for a clean descending milestone proposal. Any warning still needs `--reviewed-by "<name>"`. No line-by-line review, scientific review, interpretation acceptance or publication consent is implied by standing adoption.
5. **Regenerate and check.** `synth generate`, then `synth check`. Run `generate` twice: the output must be byte-identical.
6. **Snapshot.** `synth snapshot --name <milestone> --title "<title>"`. Snapshots are immutable and hash-locked.
7. **Close the round trip.** `synth round-close --id RT-000N --date <d> --report <path> --reported-at <sha>`, regenerate, commit. `round-trips.md` now displays every open recommendation with scope and qualification.
8. **PR.** Reuse an open valid synthesis PR. If it has merged, continue from current main with explicit carry-forward provenance. Under AD-0006, a clean adopted milestone can merge once CI is green; a still-gated source update remains draft.
9. **Next instruction.** At the author's next instruction, run `synth ratify --round-trip RT-000N --decision-id AD-000M --date <d> --instruction "<verbatim>" [--object <id>]`. Ratification accepts synthesis interpretations at their displayed categories only. It is not scientific review of a CL/GT generation and not publication consent.

## Successive-Branch Milestones And Pending Approval

For a CL generation on a new branch, prepare metadata JSON (branch, revision, closed milestones, review state and artifacts), then use `propose-pin --source CL --commit <close> --metadata <file>`. `apply-pin` applies this exact hashed metadata together with the commit; it refuses an abandoned/parallel tracked branch. AD-0006 still excludes every warning-bearing proposal, including a status-only rewrite.

While approval is pending, `preview-pins --proposal <pending proposal> --staged-candidates <file> --staged-questions <file> --out research-synthesis/proposals/previews/<name>` validates in a discarded copy. Repeat --proposal only for other pending pins; never replay an already adopted GT milestone. Output is hypothetical, not an adopted source or updated main. See the 8P/P012 report and [synchronisation](synchronisation.md).

## Historical (private) inputs

- Keep the archives outside the repository. Verify with `synth hist-inventory --archive <zip> ... --out <outside dir>`.
- Re-hash cited members with `synth hist-verify --archive-dir <dir>` or `RS_HIST_ARCHIVE_DIR=<dir> synth check`. Without the archives these checks report `requires_private_input`, never a pass.
- Nothing historical is published without an explicit `publication_consent` decision ([`historical-intake.md`](historical-intake.md)).

## Stop conditions

`check` fails and work stops when: a pinned artifact or materialised copy no longer matches its digest; an upstream schema changes; an implicit acceptance has no logged ratification; a historical record lacks consent or a matching digest; or a file outside the synthesis layer (other than the root README link) changes. Report the failure; do not weaken a check to pass.

## Using the hub from a research branch

See [`branch-integration.md`](branch-integration.md).
