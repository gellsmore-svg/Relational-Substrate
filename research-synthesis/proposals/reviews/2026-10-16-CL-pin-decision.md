# CL Pin Warning Review: One Remaining Adoption Decision

Date: 2026-10-16. **PENDING**. No reviewer name or author decision has been entered.

The earlier two-pin checkpoint is superseded: merged PR #9 has already adopted GT-P012
under AD-0006. That standing instruction explicitly excludes proposals with any warning.
It cannot authorise the CL status-only rewrite by itself.

## Prepared Decision

- Source: CL.
- Current authoritative pin: e650d71bda7203c8018d8bd134c5496a03d74a11.
- Proposed closed pin: 08d7017be85616df7bc5b2934e8076bdcc73a319.
- Continuation branch: research/constraint-lab-v0.8p-stopping-sufficiency.
- Metadata digest: d819a2614a22bc5a9dbfe46a651c6907a44fea41b17bd0ba3d89acae90c20340.
- Metadata file: proposals/source-metadata/CL-synchronisation-2026-10-16.json.
- Proposal: proposals/pin-updates/CL-08d7017be856.json.
- Exact-head CI: CL8O 38790237303; CL8P 38802246455, successful.
- Aggregate additions: 19 findings, 33 relations, ten catalogue entries.
- Removals: none. Unexpected schema changes: none.

The sole old-row change is Q-H2-ROUTE-NULL-FACTORIZATION, unresolved -> qualified.
Its statement and creation metadata are unchanged. The original source receipt is
constraint-lab/provenance/status-changes/008O.json at the proposed commit, SHA256
e87cb935ec384a518907e793f0cf8bcc688fc6795cb8e63598ce7654485e0b52.
The before/after hashes are preserved in the segment/aggregate delta audit; the warning
is not suppressed or reclassified as a clean proposal.

A named human can approve **administrative ingestion plus the specified metadata**.
This is not independent scientific review of 8O/8P, acceptance of any cross-programme
interpretation, private publication consent or ratification of the new round trip.

Requested response: **approve CL pin, reviewed by <your name>**.

## Resume After Genuine Approval

From this hub continuation worktree, not a programme branch:

```bash
python3 research-synthesis/synth apply-pin \
  --source CL --commit 08d7017be85616df7bc5b2934e8076bdcc73a319 \
  --reviewed-by "$REVIEWED_BY"
```

REVIEWED_BY must be the actual named reviewer from the approval, not an inferred name.
Record the genuine instruction separately. Then install the staged C1 and CL8P question
extensions, retaining the now-reviewed C2/C3/C4 histories. Review C1 at qualified scope,
regenerate/check twice, run the suite, create a new adopted snapshot and close a new
round trip. Push and verify the exact final head. Do not rewrite the staged snapshot,
the merged GT milestone, existing author decisions or original programme records.

The current continuation already contains actual qualified agent reviews of C2/C3/C4,
source reconciliation, metadata safeguards and a validated hypothetical CL8P preview.
Only CL pin adoption and its reference-dependent additions are gated.

