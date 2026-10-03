# External review 004 — ChatGPT review of v0.4

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.4` at `777ef71d123e8f85e6d1372225b5028744fc5ffe`.

The review is external to the v0.4 implementation. It is not a line-by-line audit of every generated kernel or bulk artifact. Shard directories and individual kernel files under `generated/` were not re-derived one by one in that review.

## What was inspected

- The v0.4 commit history.
- The Generation 3c report and specification.
- The Generation 4 report and specification.
- The Generation 4 row table.
- The provenance README, ledger, Prompt 003 and Prompt 004 representations, and Execution 004.
- The memory-clock implementation.
- The pair-event-epoch implementation.
- The N=4 graph-isomorphism implementation.
- The reconfiguration implementation.
- The v0.4 tests.
- The CI state.

## Conclusions recorded from that review

### Execution state

The v0.4 branch is eight commits beyond v0.3.

Generation 3c completed:

```text
7,385 canonical sets
11 shards
2 workers
0 failed
0 quarantined
```

Generation 4 completed:

```text
160 canonical weighted singletons
32 structural singleton orbits
19 shards
2 workers
0 failed
0 quarantined
```

The final v0.4 head itself has successful GitHub Actions run `37143016886`. That run is not the preceding run `37142958088`. The preceding run is the one recorded on the v0.4 ledger `ci` line, on head `0c33263df89d80bb9885ff381c2a85f3edb82ad7`. Execution 004 is not rewritten to insert `37143016886`.

### Memory-clock separation

Generation 3c found:

```text
FULL_EVENT_CLOCK_MEMORY positive: 5,250 / 7,385
PAIR_EVENT_EPOCH_MEMORY positive: 2,886 / 7,385
```

Therefore 2,364 systems have full-event memory that disappears when triad-only events are skipped.

Pure classes:

```text
P->P:  0 / 1,890 epoch-positive
P->T:  0 /   380 epoch-positive
T->P: 370 /  380 epoch-positive
T->T:  0 /    35 epoch-positive
```

Generation 4 sharpens this on singletons:

```text
P->P: 0 / 50 epoch-positive
P->T: 0 / 40 epoch-positive
T->P: 40 / 40 epoch-positive
T->T: 0 / 30 epoch-positive
```

This supports the distinction:

```text
hidden event-timing / persistence information
!=
hidden lower-order transition-law information
```

within the searched grammar.

### N=4 state space

Generation 4 correctly uses:

```text
N = 4
O = 3
6 pair relations
4 independent triadic relations
10 binary slots
1,024 labelled states
90 full hypergraph S4 orbits
11 pairwise graph-isomorphism classes
```

The two-edge path and the two-edge matching are distinct pairwise graph classes with the same edge count.

### N=4 singleton grammar

Generation 4 counted:

```text
380 structural normal forms
1,900 labelled weighted constraints
32 structural singleton orbits
160 canonical weighted singletons
```

All 160 were analysed.

Exactly the 40 `T->P` weighted singletons have hidden-triad-dependent pair-jump laws and pair-event-epoch memory.

### Reconfiguration result

The predeclared one-pair-event same-edge-count non-isomorphic flux measure is identically zero.

This is structural:

> A pair event toggles one pair bit, so pairwise edge count changes by one. Two different graph classes with the same edge count cannot be connected by one pair event.

The review does not reinterpret this zero as a failed implementation.

The separately predeclared horizon-16 path-to-matching and matching-to-path passages do move.

Every `P->P` singleton and every `T->P` singleton changes those focused passages relative to the unconstrained baseline.

Every `T->P` singleton also makes the passage depend on the hidden triadic configuration.

Reference maximum `T->P` effects reported in v0.4 include approximately:

```text
path -> matching baseline-relative delta:
-0.006258155390793857

matching -> path baseline-relative delta:
-0.025032621563174984
```

with corresponding triadic spreads approximately:

```text
0.008995800253034203
0.035983201012137256
```

Ordinary `P->P` singleton rules move the same passage more strongly.

Therefore Generation 4 does not show that a higher-order condition is necessary or the strongest singleton cause of this reconfiguration.

It shows that the hidden higher-order configuration can condition the passage.

### Triad-count projection

Exposing only the number of active triads restored Markovity in 0 / 160 Generation 4 singleton systems.

Aggregate triad occupation was not a sufficient visible state for these kernels.

### Numerical discipline

Generation 4 stationary analysis is float64, not exact rational arithmetic.

The largest primary stationary residual is approximately `2.56e-15`.

The report correctly distinguishes exact structural claims from numerical stationary claims.

### Four improvements required before expanding the science

1. Complete the missing horizon-16 reconfiguration sensitivity analysis.
2. Distinguish changes caused by different source-state occupancy from changes caused by the constrained future dynamics.
3. Replace the finite-horizon passage as the primary mechanistic quantity with an eventual hit-before-return committor where feasible.
4. Build the targeted `T->P + P->P` pair search by enumerating labelled rules and canonicalising the complete two-rule set under `S4`, rather than multiplying singleton orbit counts.

### Authored prompt metadata

The review independently verified the following authored Markdown artifacts. They identify files created by ChatGPT for Graham. They are recorded here as externally verified metadata. They were not present in the working environment when this artifact was filed, and they are not assigned to the stored agent-input files.

Prompt 003 authored Markdown:

```text
bytes: 27,580
sha256: 5acdf96aa311273fa02207e64c08b5509d144cc4f1921c9f101cd02570f77ede
authored_prompt_status: externally_verified_pending_import
```

Prompt 004 authored Markdown:

```text
bytes: 32,018
sha256: ae1979b484da8d30614776445e46f8b674e0d1a991688884685ba327296f398a
authored_prompt_status: externally_verified_pending_import
```

The stored Prompt 003 execution-time capture remains 25,995 bytes, sha256 `9ac0de2c5d4cdd33749fec03a232f2d35fe5f6dbead9b0f572cafce4e23cbccb`. The stored Prompt 004 agent input remains 32,011 bytes, sha256 `f261527e522cc780f0937097b7de7706f7953f8bf69c59837442bbb7e1cf76ef`. Those local hashes are not the authored hashes above.

## Verification available when this artifact was filed

`git log e04e0d4..777ef71` lists eight commits.

`gh run view 37143016886` reported conclusion success, event push, branch `research/constraint-lab-v0.4`, head `777ef71d123e8f85e6d1372225b5028744fc5ffe`, title "provenance: record the v0.4 Actions run", URL https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/37143016886.

`gh run view 37142958088` reported conclusion success on head `0c33263df89d80bb9885ff381c2a85f3edb82ad7`, URL https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/37142958088.

A repository search at filing found no file of 27,580 bytes and no file of 32,018 bytes. The authored hashes are therefore pending import. This check agrees with the review's CI conclusion and with the separation of the two run ids. It is not itself the external review. The scientific counts in the sections above are the review's recorded conclusions. They are not re-derived in this file.

## Status

This review assesses the v0.4 execution. It is linked to prompt 004 and to execution 004. It is not a review of Generation 4a, Generation 5, or v0.5. Review 005 is not written here.
