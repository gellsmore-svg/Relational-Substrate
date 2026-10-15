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
4. **Adopt.** A named human runs `synth apply-pin --source GT --commit <sha> --reviewed-by "<name>"`. This updates `pin-spec.json`, rebuilds `manifest.json` and the materialised copies, and marks the proposal adopted.
5. **Regenerate, check, snapshot, open a PR.**
   - `synth generate`, then `synth check`.
   - `synth snapshot --name <milestone> --title "<title>"`. A snapshot is immutable and carries a lock with source pins, digests and a content hash.
   - Open a PR for the author's review.

## Stop conditions

`check` fails, and work stops until the mismatch is reported and understood, when:
- a materialised copy or a pinned artifact no longer matches its recorded digest or git blob;
- an upstream validator no longer exposes the expected vocabulary (incompatible schema);
- upstream rows carry fields their source does not declare.

## Metaphor review

Drafts live in `proposals/metaphor-drafts.jsonl`. A metaphor moves to `ledger/metaphors.jsonl` only after a review against its mapping, its "does not mean" list and its misleading readings. The author's acceptance makes it `human_accepted`.

## Optional reminder

A monthly stale-link audit (`synth check`, reading the staleness section) may be run by a person as a reminder. It reports branches that moved past their pins. It never changes pins or records.

## Seeds and external material

- **Seed files.** The author's seed files are staged with `synth intake-seeds <dir>`. They become `proposed` proposals with `origin: author_seed`, never ledger entries.
- **External syntheses.** These are registered as `EXT::` sources and their claims as proposals.
- **Historical archives.** These stay `pending_intake` until a declared intake procedure is supplied. Private archives are never committed.
