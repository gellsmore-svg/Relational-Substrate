# When an attachment switches: representation and necessary predictive state

## Completed inquiry

The selected question asks what changes when a link switches two actors between
separate and joint updates, rather than changing a value on the previous fixed
shared interface. It also asks what an observer retaining the actor configuration
must remember about that link.

The answer has three parts: an exact fixed-protocol reduction; a proved coarsest
current-state refinement; and a separate same-clock single-bit support limit.
These distinguish behavioural representation, predictive information and event
support without claiming a new computational primitive or ontology.

Starting local/main SHA was `47e9cbeb71034b6f2791a2c6fb7ec24538f365a3`.
After fetching the new handoff, live research HEAD was
`b1aacb73f68a1e59789eeb1d9e7883f3c3ee81c6`.
All six registered worktrees were checked; no unpublished new inquiry was found.
The old generated files and deferred outputs retained their audit hashes.
Selection `a44aba107a231c0e2240a54d93cdb96da2751784` was pushed before its
new validation domain ran. The independent OTR rationale and alternatives are
`../docs/2026-10-26-switching-link-selection.md`.

Changing attachment was selected over another shared-port quotient theorem,
another rejected-attempt clock contrast and deferred finite-atlas recovery:
it directly separates changing participation from fixed-protocol representation,
with exact types, a useful reducible outcome and bounded independent checks.
No candidate family is cancelled or prescribed next.

Definitions, general proofs and interpretation boundaries are
`../docs/switching-attachment.md`.

## Model and actual mathematical findings

Actors have finite nonempty states and nonnegative integer **off-diagonal**
raw matrices A and B. All `(s,t,m)` states are allowed; binary m is an independent
input coordinate. With m=0, one actor updates at a time. With m=1, both update
with product weight. A switch holds the actor states and changes m, with
nonnegative weights gamma_0/gamma_1. Four labels identify left/right/joint/switch.
Only the final global-event row normalises; a zero row halts without adding
an event. Weights are dimensionless and the coupling rule is an instrument.

**Exact reduction.** The changing attachment compiles to two expanded actor
catalogues and a two-state controller, all sharing the same fixed four labels.
Unit passive loops and controller guards reproduce every original raw labelled
entry on the same full state set. No new state beyond the already declared link,
extra clock step or implicit-halt-as-event substitution is introduced. Keeping
these raw matrices also preserves later same-H composition, including private
competing contexts. Literal graph/participation interpretation and individual
event identities are not asserted identical.

**Necessary predictive state.** Call `(s,t)` active when either actor has a
positive outgoing row there. The two modes have different actor-observed rows
at every active configuration: local updates change exactly one actor while
joint updates change both and switches change neither. At an inactive
configuration only switches or halt occur and both observed rows hold.

The unique coarsest strongly lumpable deterministic refinement of the actor
view therefore splits the two modes at every active configuration and merges
them at every inactive one. Its state count is
`|S||T| + number of active configurations`. Necessity follows by aggregating
any putatively equal refined rows back to the differing actor-view rows;
sufficiency follows because the only nonsingleton blocks are actor-inactive.
This is proved for arbitrary finite actors in the declared grammar, including
zero switch weights. It is not a minimum over all observations or histories,
a special-initial-mode claim, or a guarantee for every later context.

**Single-bit boundary.** Positive binary toggle actors and positive switch
weights give the directed five-cycle `000 -> 100 -> 110 -> 111 -> 001 -> 000`,
where the coordinates are `(left actor,right actor,mode)`. Every edge is
positive by the event rule. Hamming parity forbids an injective encoding of
this support into one-bit moves in any dimension at the same event clock.
Each frozen mode separately has a one-bit encoding. Thus the fixed finite
protocol reduction remains exact while a single-toggle-support reduction
under those permitted mappings is impossible. Changed clocks, intermediate
states, coarse/distributional encodings and other event primitives are outside
this obstruction.

## Controls and independent challenge

For unit binary weights, forgetting the mode at actor state 00 gives rows
`[1/3,1/3,1/3,0]` and `[1/2,0,0,1/2]`. No exact actor-only quotient is filled
in for this failure. All actor configurations are active, so the coarsest
actor-preserving refinement has eight states. If only the actors' 0-to-1 moves
are enabled, actor state 11 is inactive and the coarsest refinement has seven.
If both actors are wholly inactive, four actor states suffice even while m
switches. These are constructed controls, not preferred complexity thresholds.

The state-only quotient need not retain protocol information: inactive actors
with switch weights 1 and 2 can be distinguished by a later synchronizing
partner with private competition. This is an application of the earlier
calibration result, included to protect the new minimality claim's scope.

Analysis-only `switching-link-analysis-0.1.0` compares direct guarded matrices
with independent n-ary matching of compiled event catalogues. Exact Fraction
block sums enumerate all permitted actor-view refinements and find every
minimal exact one without assuming the proposed formula. Tests add hand rows,
the previous binary sparse product, a further private context and a separate
support-colouring algorithm.

| Predeclared software domain | Verified count |
| --- | --- |
| Four binary actor weights and two switch weights over {0,1,2} | 729 networks |
| Direct versus compiled raw labelled matrices | 729 comparisons |
| All 16 actor-view refinements per binary network | 11664 checks |
| Exact refinements among that menu | 1224 |
| Networks with an exact unrefined actor view | Nine |
| Additional controls | Three-state actor, 64 refinements of its six actor blocks, invalid actor loops/weights, active/partial/inactive cases, zero/frozen switches, five-cycle and fixed-mode encodings |

The saved coarsest-state histogram is a property of this software menu, not a
scientific frequency, threshold or agenda. The general statements follow from
proofs. There are no new frozen scientific cells.

All **268 local RRC tests pass**, including 21 added tests; the baseline had 247.
Saved deterministic evidence:
`../provenance/2026-10-26-switching-link-verification.json`, SHA-256
`ae9ed1657d04a6df9b306b8e817508cbe9eaef9d68017825aa9748edc4febfcc`.
Reproduce from `relational-complexity/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 provenance/switching-link-analysis-check.py
PYTHONDONTWRITEBYTECODE=1 /home/cello/domains/Relational-Substrate/constraint-lab/.venv/bin/python -m pytest -q
```

The checker uses no production RRC calculations. Existing engine, event-kernel
and analysis identifiers retain their meanings. Guarded synchronization,
passive participation, strong lumpability and bipartite support are established
mathematics; the specific link policy, exact reduction and refinement formula
are the scoped RRC construction. Official PRISM precedents and their different
scheduling/rate semantics are identified in the methods note.

The post-register ledger/frozen-plan checks also pass (23 tests). The evidence
reproduces byte-for-byte; all six registers, the journal and crosswalk retain
their starting bytes as prefixes. IDs, endpoints and evidence/commit references
validate. Frozen/old-method/other-programme tracked paths are unchanged, all
new files belong to cello, and the three protected directory hashes match the
selection audit.

## Publication, preservation and restart

There are zero selected scientific worker invocations and zero newly adopted
atlas cells. The adopted count remains 218, excluding 15 historical failures.
All broad questions remain open. Frozen records, old methods, other programmes,
generated files and deferred/unadopted Atlas-019/020 bytes are preserved.

Selection, publication, handoff and observed CI/merge provenance are recorded
in PROGRESS.md and the integration PR. Under AGENTS.md, merge only after all
applicable checks pass and synchronize the continuing research branch.

Restart with this report, its proof and the selection. Possible later work may
vary ownership, relation graphs, observation/history classes or coupling clocks;
none is mandated. The selected mathematical increment is complete, rather than
a method awaiting an unperformed scientific experiment.
