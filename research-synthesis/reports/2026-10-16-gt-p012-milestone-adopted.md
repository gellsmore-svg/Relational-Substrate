# GT milestone adopted through GT-P012 (standing decision AD-0006)

*Dated 2026-10-16. Applied by an AI research assistant (Claude Opus 5.5) on hub branch `hub/gt-p010-p011-milestone`.*

**Status: HUB ADOPTED THROUGH GT-P012.** The hub's GT pin moved from `79fa6b0119449bd56359acf4436015df27855f43` (GT-P009) to `e2b5dc4cb65bafc423047f78468a63c9d6ceb218` (GT-P012 close).

## Basis

- The author instructed on 2026-10-16: *"skip the central approval steps and integrate automatically"*. It is logged as **AD-0006** (`standing_pin_adoption`) in `proposals/author-decisions.jsonl`.
- The pin was adopted with `synth apply-pin --standing-decision AD-0006`. The proposal `proposals/pin-updates/GT-e2b5dc4cb65b.json` now records `status: adopted`, `adoption_basis: AD-0006` and `human_reviewed: false`.
- **No line-by-line review of the pin took place, and nobody's name was entered as reviewer.**
- The standing path is refused for a proposal that does not descend from the current pin or has any warning. This proposal descends, with no warnings: 0 rows removed and 0 rewritten.

## What changed

| Item | Value |
| --- | --- |
| Pin delta | +25 findings and questions (10 GT-P010, 8 GT-P011, 7 GT-P012); +36 relations (13, 11, 12); 0 removed; 0 rewritten |
| GT entry | `proposals/pin-updates/GT-e2b5dc4cb65b-pin-spec-entry.json` applied as proposed: 10 → 19 artifacts (E5B–E5D snapshots, transfer notes and reports); `unreviewed_generations` GT-P009 to GT-P012 |
| Manifest | rebuilt; only the GT receipt changed (it names AD-0006); other sources byte-unchanged |
| Index | GT `e2b5dc4cb65b`, 129 nodes |
| Candidates | P::GT-C1 to P::GT-C4 appended to `proposals/candidate-relations.jsonl` unchanged (agent_drafted, proposed, candidate) |
| Checks | validate: valid; generate twice: byte-identical; check: ok, 0 errors; hub tests: 100 OK |

## Warnings kept

- **X::0001 to X::0009** were reviewed against GT `79fa6b0` and are flagged for re-review at `e2b5dc4`. No cited GT row was rewritten, so their endpoints are byte-unchanged. AD-0006 covers pin adoption only, not re-review, so the flags stay.
- OTR source: `behind_branch_head`; outside this milestone.

## What this is not

- **Not scientific review.** GT-P009 to GT-P012 remain closed but scientifically unreviewed (draft PR #6, unmerged).
- **Not acceptance.** No candidate connection is accepted, and no `X::` record, metaphor or decision category is created or upgraded.
- **Not publication consent.** HIST stays pending intake and private.
- **CL is unchanged** at `e650d71` (008N). CL 8O (`99565d1`) and 8P would be separate milestones.

## Round trip

RT-0004 closes this round. It lists no recommendations, because nothing is agent-reviewed and open.
