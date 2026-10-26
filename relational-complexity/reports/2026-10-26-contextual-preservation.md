# What every allowed partner can distinguish

## Completed analytical answer

For the declared fixed-H product, an observation stays exact with **every
finite allowed partner** exactly when it preserves each shared label's raw
outgoing block weights and the aggregate private outgoing block weights.
Private label allocation can be discarded for this state-only observer;
the private weight itself, including internal-block events, cannot generally
be discarded. This sharpens the earlier sufficient condition without changing
its semantics or claiming a necessary condition for one arbitrary fixed partner.

Starting live HEAD: `c9337285ec4553e3dab21530fa3b397507017d9b`.
The new prompt is `prompts/2026-10-26-context-and-interface-otr/RESEARCH-PROMPT.md`.
The selection was committed and pushed before its new checks as
`37a84ae8250dff0c3400391b8044ff0a72d1c28f`.
See `docs/2026-10-26-context-selection.md` for the qualitative OTR comparison.
Contextual distinguishability was selected over evolving membership,
state-interface identification, alternate synchronization policies and deferred
recovery because it resolves a precise quantifier gap using an already typed
operation. None of those alternative families is cancelled or prescribed next.

Full definitions and proofs are `docs/contextual-preservation.md`.

## Quantifiers and construction

The component and every partner have finite nonempty states, finite labels,
the same fixed finite handshake alphabet H and nonnegative integer weights.
Partners may offer private events of unit weight. Shared weights multiply;
private events interleave; only the final global-event row is normalised.
Implicit halt completion adds no event. The observation is pi on the component
and the identity on the partner, with no event labels observed, for every
microstate and initial distribution. This is a statement about strong
lumpability at the declared clock, not a stationary or physical-time result.

For each observed target block C, the signature retains the raw sum for every
shared h and the sum over all private labels together. The exact theorem is:

```text
block-constant signature
  iff exact product observation for every finite allowed partner
  iff exact product observation for the finite separating probe family.
```

The family has one two-state private-only probe and one three-state probe for
each h. The latter branches from partner state 0 to state 1 on h and to state 2
on a unit-weight private event. The private branch probability is `1/D`; dividing
each observed branch probability by it recovers raw block weights. This proves
necessity without enumerating arbitrary partners. The finite block-row formula
proves sufficiency for any allowed partner, including zero rows and evolving
omitted state. The `1+|H|` family is an upper bound, not a minimality result.
This separates exact probability laws; it is not an exact inference algorithm
from finitely many sampled trajectories.

Merging private labels into one private channel commutes with the weighted
product. The signature is the standard weighted-bisimulation block condition
after that relabelling. The RRC-specific work is the explicit context class,
observation and separating construction; no new universal process-algebra
theorem or equivalence with a general probabilistic testing theory is claimed.

## Informative limits

| Contrast | Exact consequence |
| --- | --- |
| Private p/q allocation changes with hidden state; total private flow does not | Full raw labelwise equality fails, yet the theorem gives preservation in every declared context |
| Promote p/q to shared labels by changing H | Selective handshakes can distinguish the same hidden states |
| Observe emitted labels | p versus q is already visible; the state-only result does not apply |
| Remove competing private events from a selected shared-only partner | Hidden shared weights 1 and 2 can still give the same joint flip; necessity is not exported to this restricted context class |
| Private internal self-loop weight 1 versus halt, with constant component observation | The private probe's move has probability `1/2` versus `1`; internal events cannot simply be erased |

These statements retain the declared clock, label and observation boundaries.
No new membership state, autonomous entity, causal intervention, original
interface identification or physical timescale is inferred.

## Independent verification

Analysis-only method `context-probe-analysis-0.1.0` scans events for raw block
signatures independently of dense per-label matrix composition and exact
Fraction block aggregation. It reconstructs each signature from the resulting
probe probabilities. Tests also compare nine context kernels with the previous
sparse-event implementation and verify private relabelling at raw matrix level.
Hand-derived fractions and boundary controls challenge the classification.

| Predeclared software domain | Verified count |
| --- | --- |
| Zero, one or two unit entries among six channel/update positions | 22 row templates |
| Ordered hidden-state template pairs | 484 |
| Hidden hold, flip and reset updates | 1452 systems |
| All three calibrated probes per system | 4356 probe laws |
| Probability-based signature reconstructions, four states per system | 5808 |
| Signature-constant / nonconstant cases | 66 / 1386 |

The 66/1386 split describes this software menu, not the frequency of contextual
mechanisms. Proofs establish the quantified result. Other controls cover empty
H, identity and constant observations, halt, duplicate/zero/non-unit events,
namespace collisions and invalid inputs. Nonexact quotient rows stay absent;
explicit differing rows are retained as witnesses.

Saved deterministic evidence: `provenance/2026-10-26-context-verification.json`.
SHA-256: `31a3a9713ba32dd7c8a9445de9605bc36b5d414d6a41855a71e678ffc92d9663`.
All **223 local tests pass**, including 19 added context-analysis tests; the
starting suite had 204. The existing local virtual environment was reused
without modification. Reproduce from `relational-complexity/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 provenance/context-probe-analysis-check.py
PYTHONDONTWRITEBYTECODE=1 /home/cello/domains/Relational-Substrate/constraint-lab/.venv/bin/python -m pytest -q
```

The checker imports neither the RRC engine nor the previous checker. Its size
and event caps are implementation costs, not theorem bounds. Existing
`label-sync-analysis-0.1.0`, engine `rrc-0.4.0` and both event-kernel versions
retain their original meanings.

The ledger-schema and frozen Atlas-018 checks also pass (23 tests). All six
living registers, the journal and crosswalk preserve their starting bytes as a
prefix; IDs are unique, relationship endpoints and evidence paths resolve.
Commit references resolve to real commits. Frozen tracked paths and both
deferred directory content hashes are unchanged; all new files belong to cello.

## Integration and restart

The question is answered for the stated class, not for all composition policies,
observers or evolving interfaces. All broad atlas questions remain open.
There are zero scientific worker invocations and zero new adopted atlas cells.
The count remains 218, excluding 15 historical failures. Atlas-019/020 remain
deferred with their original untracked bytes and frozen decisions preserved.

Restart with this report, its proof and the selection. Potential later questions
are a genuinely restricted partner class, evolving H, state-interface
identification or different weight/clock policies; none is scheduled. The
selected analytical inquiry is complete, rather than a method awaiting an
unperformed experiment. Commit references and observed CI status are recorded
in the final PROGRESS.md checkpoint.
