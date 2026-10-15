# Cadence and change control

**Milestone-triggered, human-reviewed.** Nothing here runs on a timer to reinterpret science.

## When a GT or CL round closes

1. **Check the round boundary.** Confirm that the programme's round is closed: its close or provenance commit is pushed and its snapshot is published. Branches mid-round are not pinned (in-flight protection).
2. **Propose a pin.** `python3 research-synthesis/synth propose-pin --source GT --commit <sha>` writes `proposals/pin-updates/<source>-<sha>.json`, with:
   - added, removed and **rewritten** upstream rows;
   - whether the new commit descends from the current pin;
   - warnings.

   A rewritten row means an upstream finding changed in place. Every shared connection citing it needs re-review.
3. **Review.** Read the new findings. Draft any new connection or question as a proposal, never directly in the ledger, and write review records.
4. **Adopt.** Under the author's standing instruction (AD-0006, 2026-10-16: "skip the central approval steps and integrate automatically"), run `synth apply-pin --source GT --commit <sha> --standing-decision AD-0006`. This updates `pin-spec.json`, rebuilds `manifest.json` and the materialised copies, and marks the proposal adopted with `adoption_basis: AD-0006` and `human_reviewed: false`.
   - It is refused when the proposal does not descend from the current pin or carries any warning (rows removed or rewritten in place). Those cases need a named human: `--reviewed-by "<name>"`.
   - Nobody's name is entered as reviewer. Adoption is not scientific review: the generations stay in `unreviewed_generations`.
5. **Regenerate, check, snapshot, open a PR.**
   - `synth generate`, then `synth check`.
   - `synth snapshot --name <milestone> --title "<title>"`. A snapshot is immutable and carries a lock with source pins, digests and a content hash.
   - Open a PR. Under AD-0006 the milestone PR is merged once CI is green; the author reviews after the fact.

## The round trip: implicit human acceptance

The author's rule (AD-0002, 2026-10-15): **human acceptance is implicit in the round trip.**

1. **Close the round.** At the end of each round, after the report and the PR update, run `synth round-close --id RT-000N --date <d> --report <path> --reported-at <sha>`. This writes the immutable `proposals/round-trips/RT-000N.json`, listing every record that is currently agent-reviewed: the agent's open recommendations, each with its decision category.
2. **The author's next instruction ratifies it.** When the author sends the next instruction without objecting, run `synth ratify --round-trip RT-000N --decision-id AD-000M --date <d> --instruction "<verbatim>" [--object <id> ...]`. This does three things:
   - logs a human decision in `proposals/author-decisions.jsonl`;
   - appends a human entry to each listed record's decision history;
   - writes `proposals/reviews/AD-000M.md`.
3. **What ratification does and does not do.**
   - Listed items become `human_accepted` at their reported decision category. Ratification **never upgrades** a category. The unreviewed-round cap, the pending-source rule and the HIST-intake rule still apply, so a connection resting on CL 008N or GT-P009 stays `qualified`.
   - An item the author objects to returns to `under_review`.
   - Only agent-reviewed records are listed. Seeds, external claims and unreviewed proposals are never accepted this way.
   - `check` validates every implicit acceptance against its logged ratification, and lists round trips still open.

The author can still decide explicitly at any time (`synth review ... --human`, or a logged decision such as AD-0001).

## Stop conditions

`check` fails, and work stops until the mismatch is reported and understood, when:
- a materialised copy or a pinned artifact no longer matches its recorded digest or git blob;
- an upstream validator no longer exposes the expected vocabulary (incompatible schema);
- upstream rows carry fields their source does not declare.

## Metaphor review

Drafts live in `proposals/metaphor-drafts.jsonl`. A metaphor moves to `ledger/metaphors.jsonl` only after a review against its mapping, its "does not mean" list and its misleading readings. The author's acceptance (explicit, or implicit through the round trip) makes it `human_accepted`. It stays non-evidentiary.

## Optional reminder

A monthly stale-link audit (`synth check`, reading the staleness section) may be run by a person as a reminder. It reports branches that moved past their pins. It never changes pins or records.

## Seeds and external material

- **Seed files.** The author's seed files are staged with `synth intake-seeds <dir>`. They become `proposed` proposals with `origin: author_seed`, never ledger entries.
- **External syntheses.** These are registered as `EXT::` sources and their claims as proposals.
- **Historical archives.** These stay `pending_intake` until the archives themselves pass the custody gate in [`historical-intake.md`](historical-intake.md). Private archives are never committed.
