# Does an effective component description survive interaction?

## Completed analytic increment

A standalone Markov description can be exact yet insufficient when that system
is composed with another. The missing information can be event labels, raw
weight calibration or both. This increment defines one precise reapplicable
composition operation, proves a sufficient preservation rule, and supplies exact
positive and negative cases. It is not another XOR recoding variation.

The starting live HEAD was `2bda78f45d3032a2d3f923863390bba4f2eb3d89`.
The selection is `docs/2026-10-26-sync-selection.md`, committed and pushed as
`df0ccb6c34d07153567299eb3e3d3b2f88205383` before its checks. The governing
prompt is the relational-composition-and-dynamics handoff. Full definitions,
proofs and literature boundaries are `docs/labelled-sync-composition.md`.

## Operation and result

Inputs are finite weighted labelled systems with the same declared handshake
alphabet. Shared-label events pair and multiply their weights; private events
update one factor. The output retains weighted labels on Cartesian states so
it can participate in another composition. Only the final one-global-event row
is normalised. An empty row halts without manufacturing a synchronising event.

This weighted operation is associative, after Cartesian reassociation, at fixed
handshake alphabet. Its identity is a one-state component offering one unit-
weight self-loop for every handshake label. The all-halt one-state system has
the same standalone kernel but is not the same composition identity. A partner
can distinguish them through whether a handshake can occur.

**Loss of closure.** A four-state component `(z,d)` flips z with weight one,
using label a when d=0 and b when d=1. Dropping d gives an exact deterministic
flip. Composing with an a-only partner gives, at the same retained `(z,partner)`
state, either a deterministic joint move or halt. Exact standalone prediction
does not imply exact prediction after this interaction. The aggregate raw
standalone weights are unchanged, so this case isolates label information.

**Preservation rule.** Equality within each source block of every label's raw
weight into every target block is sufficient. Those block weights factor or
add through shared/private composition, so quotient and composition commute
before normalisation and also after it, including all-halt rows. Hidden state
may evolve, reset or remain fixed. The proof does not require it to be inactive.

**Limits of necessity and calibration.** The stronger rule is not necessary for
one fixed partner. Hidden a-flip weights 1 and 2 still give an exact joint flip
with a shared-only partner. Giving that partner a private unit-weight self-loop
changes joint probabilities to `1/2` and `2/3`, revealing the omitted raw scale.
This conclusion is scoped to the declared product-weight/global-clock policy;
it is not a claim that every reasonable composition has the same calibration.

The data distinguish labelwise weighted equivalence, aggregate kernel equality,
standalone strong lumpability and contextual preservation. Microscopic event
identities, original carrier semantics, autonomous entities and physical ontology
are not proved equivalent by these constructions.

## Independent checks

Method `label-sync-analysis-0.1.0` is an analysis-only version. The script
`provenance/label-sync-analysis-check.py` imports no RRC engine calculation.
It compares event-pair enumeration with per-label matrix formulas and verifies
exact quotient rows against hand-derived witnesses.

| Predeclared software domain | Actual validation |
| --- | --- |
| Empty two-state component plus each single shared/private unit transition | Nine basis components |
| All ordered pairs from that menu | 81 event/matrix oracle comparisons |
| All ordered triples, fixed handshake alphabet | 729 associativity checks |
| Both identity sides for each menu component | Nine unit controls |
| Hidden-coordinate hold/flip/reset lifts against all basis partners | 243 quotient/composition comparisons |
| Additional typed controls | Three-state cycle, duplicate events, non-unit weights, and both factors reduced with evolving hidden state |
| Boundary cases | Halt versus declared no-op, hidden labels, private clocks, constant/identity observations, invalid signatures and all-halt rows |

The domains validate a proof implementation; they are not a census of stochastic
systems, experiments, or atlas cells. The matrix proofs establish generality.
The positive weighted condition is deliberately distinguished from merely
passing a particular context. Nonexact projected rows stay absent, with an
explicit block-row witness.

Saved exact evidence: `provenance/2026-10-26-sync-verification.json`.
SHA-256: `0c659cd02373bac68beac198e3f56670731f8d3d406c99675d2d38eabffb49bb`.
All **204 local tests pass**, including 11 synchronization-analysis tests;
the baseline had 193. The JSON is deterministic and reproducible byte-for-byte.
Reproduce from `relational-complexity/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 provenance/label-sync-analysis-check.py
PYTHONDONTWRITEBYTECODE=1 /home/cello/domains/Relational-Substrate/constraint-lab/.venv/bin/python -m pytest tests/test_label_sync_analysis.py -q
```

The local environment is reused without modification. The prototype's resource
caps are not formal impossibility statements about larger finite models.

The ledger-schema and frozen Atlas-018 checks also pass (23 tests). All six
living JSONL registers retain their starting bytes as a prefix, with unique
IDs and existing evidence paths. A tracked-path audit found no modification to
engine code, frozen plans, preflights, results or other research programmes.
Content hashes of both deferred result directories match the starting audit.

## Interpretation and restart

The meaningful advance is a typed operation that produces further dynamics and
admits reapplication, together with a precise distinction between sufficient
standalone and compositional descriptions. Retaining labels and the relevant
weight calibration can matter even when aggregate component dynamics coincide.
A labelled quotient self-loop can remain consequential to a partner; it should
not automatically be erased as irrelevant stuttering.

This applies familiar weighted transition-system and bisimulation ideas to a
specified RRC inquiry. It is not a new universal process-algebra theorem. It does
not identify shared interface states or implement changing relational membership;
those are different constructions requiring their own validity contracts.

There are zero new scientific workers or adopted cells. The atlas count remains
218, with 15 historical failures excluded. Atlas-019/020 remain deferred and
their local outputs unchanged. All broad questions remain open. A later inquiry
could compare synchronization policies, state-interface identification, or
weaker contextual quotient conditions. None is imposed as the next experiment.
Restart with this report, its methods proof and the selection record.
