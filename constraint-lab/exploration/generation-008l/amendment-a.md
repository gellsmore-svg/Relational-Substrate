# H2-0 amendment A: type-sensitive validation caches

This is an engineering correction, not a changed scientific law, palette,
controller, estimand, tolerance or compiler class.

After original H2-0 result commit 3e71f06, the combined post-freeze/plumbing
suite found that functools.lru_cache with untyped keys can equate True and 1.
After a valid slot-1 call, an invalid boolean slot could hit the cache without
running the strict integer validator. No original scientific state used booleans:
all 2304 state coordinates are constructed from integer range/divmod.
The original valid-state results and frozen sources at the original commit
remain preserved, not retrospectively changed.

Correction: typed=True on the two SECOND-RECENT probability caches.
No row or update on any legal int/None history changes. Analysis VERSION v2
and a separately named amended plan/output tree prevent overwrite of v1.
The old plan, receipt, twelve items, tables and manifest remain immutable.

Original freeze: 6f00fcdb07fc0e8323f8b6360fdc59960be7dcb4.
Original plan hash: b7670bbdac76fb29da687d60c6c5c7c74bf32277d8458442b0bcad947575f7de.
This amendment is not blind: all original twelve scientific items are known.
The original zero pre-freeze H2 target exposure is NOT asserted for this later
amendment. Before replaying v2 non-neutral items, commit and push
round-h2-0-amendment-a.json, sealing corrected source/input hashes.
Its planning ledger hash explicitly reuses the original frozen planning context,
not pending uncommitted post-result ledger updates.

Execute the same twelve cells into a NEW amendment-A item directory and new
tables/manifest. Compare every scientific result_sha256 against the v1 item;
all twelve must match EXACTLY. Timings, analysis version and freeze metadata
may differ, but scientific result payloads must not. Retain any mismatch,
stop interpretation and diagnose. Do not overwrite or recompute away v1.
Separately replay the original verifier in the original result-commit worktree.
A cache-domain regression is added to ensure the invalid call is tested AFTER
the equal-valued valid call.

No new model-system census, parameter search, weak grade or stochastic execution
is introduced. All valid-state H2 claims keep their original frozen scope.
