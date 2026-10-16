# Branch integration contract

How the CL and GT research branches use the hub, and how the hub uses them.

## Authority

- **CL and GT are authoritative** for their own plans, frozen protocols, validators, ledgers and results. The hub never edits, rebases, cherry-picks into or writes to their branches.
- **The hub is context, not authority.** A programme may read it when planning a round. Nothing in the hub can change a programme's validator outcome, freeze, or result; a hub connection is never evidence inside a programme ledger.
- **The hub reads programmes only at pinned, closed commits.** Mid-round heads are never pinned.

## Reading the hub from a research branch (read only)

Research branches do not contain `research-synthesis/` and must not merge it wholesale. Read a **pinned** hub commit instead:

```
git fetch origin main                        # or the synthesis branch before it is merged
HUB=<hub commit sha>                         # record this in the round's plan
git show $HUB:research-synthesis/generated/index.md
git show $HUB:research-synthesis/generated/questions.md
# or a throwaway read-only checkout outside the branch:
git worktree add --detach ../rs-hub-$HUB $HUB
```

Record in the round's plan (before freezing): the hub commit consulted and which hub records informed the question. That keeps the influence auditable and stops a later hub change from silently re-motivating a frozen round.

The original hub PR is merged. Use current main, or the explicitly selected active hub PR commit, at a recorded immutable SHA. Do not keep following the historical infrastructure branch.

## Proposing back to the hub (after a round closes)

1. The programme closes its round on its own branch, as usual.
2. Findings or questions for the hub are written as **seed files** (`candidate-relations.jsonl`, `metaphors.jsonl`) outside the programme's ledger, or simply listed in the round's close report.
3. A hub cycle ([`runbook.md`](runbook.md), steps 1–9) pins the closed commit, stages the seeds with `synth intake-seeds`, reviews them as proposals, and closes a round trip.
4. Only the hub PR touches `research-synthesis/`. The programme branch is never modified by the hub.

## Staleness

`synth audit` / `synth check` report a programme head that moved past its pin as `behind_branch_head` (or `diverged_from_branch`). That is a notification, not an action: the pin moves only through the reviewed cycle. A rewritten upstream row (a finding changed in place) marks every hub connection citing it for re-review.

The audit also discovers descendant candidate continuations under the programme's branch namespace. This catches CL generations opening a new branch while the old branch still equals its pin. Unknown heads are not certified closed or reviewed. The authoritative source branch moves only with a hash-anchored metadata proposal under the adoption rules: AD-0006 for clean descending milestones, named-human review for any warning. See [synchronisation](synchronisation.md).
