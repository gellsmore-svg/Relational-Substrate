# OTR selection and recovery — 26 October 2026

## Authority and live audit

The instruction executed is `prompts/2026-10-26-otr-handoff/RESEARCH-PROMPT.md`,
introduced at `333b1948e645c2b5943f7fed936cf4680b636ee9`. The live remote branch
was `b8e5ac48a2ef26e3d8cb2727a5798d5980b49435`. The existing RRC worktree was
at `8923de6565937a99a185f817526816ba50690def` and was fast-forwarded to the
remote without resetting or replacing local research files.

The tracked atlas through Atlas-017 contains 215 complete result records and
15 failed Atlas-007 records. Those failures remain excluded. The local worktree
also contains untracked output for Atlas-018 (three items), Atlas-019 (three)
and Atlas-020 (four). All ten output records predate this session. They are
not newly executed work and are not automatically adopted as scientific results.
The earlier shallow directory listing showed only manifests; the deeper audit
found the nested item files before any scientific run was attempted.

The three original plans and preflights are unchanged. Local remote-tracking
reflog evidence records the push of freeze `8923de6` at
`2026-10-26 00:53:06 +0000`. The Atlas-018 item-file modification times are
`2026-10-26 00:53:26–27 +0000`. This supports the ordering of the earlier
execution after the pushed freeze, but filesystem times are not an independent
trusted execution timestamp. The original invocation transcript is unavailable.

The 171 existing RRC tests passed. Execution uses the existing Python 3.12.3
environment at `/home/cello/domains/Relational-Substrate/constraint-lab/.venv`,
with NumPy 2.5.3 and pytest 9.1.1. That environment is read, not modified.
Repository commands and any new files use Linux user `cello`.

## Selected question

Recover and independently verify the unchanged Atlas-018 comparison: when does
the inclusion `(e0, e1, e2) -> (e0, e1, e1, e2)` support an exact dynamical
correspondence between an identified interface and two copies?

The alternatives are the identified three-bit law, a four-bit free-copy law,
and the four-bit coupled-copy law. The inclusion's state bijection is not enough:
its image must be invariant, and the restricted transition law must match.
Failure, agreement and reducibility are all useful outcomes. No probability,
hierarchy, degree of complexity or physical interpretation is a target.

| Selection consideration | Assessment |
| --- | --- |
| Consequence | Separates a state encoding from an invariant dynamical interface, and a restricted correspondence from a full-system equivalence. |
| Readiness | Three immutable finite items, a committed disposable worker preflight, bounded rational matrices and existing local receipts are available. |
| Leverage | Connects ATLAS-Q10, the compilation gate, interface composition and the distinction between independent state and a derived description. |
| Cognitive/computation cost | At most 16 states per item; direct independent enumeration can check every stored row without another scientific run. |
| Research relevance | Establishes what an interface comparison preserves before introducing more elaborate interacting or recursive systems. |

This is a selection for recovery and interpretation, not an assertion that every
previously prepared round must run. The existing Atlas-018 plan hash is
`2468bf59c1fce72fb909482dc94e1abeae30e627f0bd71e4536ed8b10b7a27e0`.
Its freeze is already pushed. No new plan or method identifier is needed because
no experimental item, clock, state or engine interpretation is changed.

## Verification and stopping contract

Before adoption, check manifest, item/spec/plan hashes, receipt bytes, complete
status, strict event semantics, integer aggregation and every exact probability
against a separate standard-library implementation. Check the inclusion and its
invariance/conjugacy independently, including the negative case. The existing
verification command is an additional check, not a replacement for independent
calculation. Do not call a worker to replace valid existing results.

The interpretation will also check alternative encodings and the full-state
versus invariant-image distinction. Any analytic consequence is labelled as
post-execution analysis, not another frozen cell or an externally new theorem.
Add adversarial software fixtures for the independent checker. Preserve failures
and stop adoption if the stored evidence does not meet the checks.

Stop at one verified, interpreted and pushed recovery increment. Atlas-019 and
Atlas-020 remain deferred with uncommitted local outputs: neither is rerun,
adopted, deleted or silently retired. Further temporal and elementary inquiries
remain alternatives for a later information-value decision. All atlas questions
and broad coverage regions remain open unless separately justified.
