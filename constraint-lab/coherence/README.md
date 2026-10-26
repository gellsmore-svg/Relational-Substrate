# Coherence ledger

`findings.jsonl` and `relations.jsonl` are the canonical record. `current-map.md` and `current-map.mmd` are generated views. Do not edit the views by hand.

Regenerate them from the constraint laboratory:

```text
python -c "from rs_constraint_lab.coherence import write_views; write_views()"
```

A snapshot under `snapshots/` is an immutable generated view written at the close of a substantive generation. Its hash is recorded in that generation's provenance. The snapshot is not a second ledger.

## Dimensions that stay separate

Each finding keeps magnitude, a robustness vector, temporal character, structural role, and one epistemic layer. The robustness coordinates are not summed. No finding or relation carries an overall score.

Magnitude is not importance. Robustness is not importance. Persistence is not importance. A small or fragile phenomenon may later be structurally essential. A large robust phenomenon may be a generic consequence of a simpler mechanism. `functional_significance` stays unknown until a later within-model comparison demonstrates a role.

## How a later generation changes the map

A published finding statement is not rewritten to match later knowledge. Add a new finding and a directed relation (`refines`, `qualifies`, `supersedes_interpretation`, `bounds`, `explains`, and the other controlled types). Change the older status only when that status change is itself part of the record. Do not delete a superseded finding.

Open questions are findings with epistemic layer `OPEN_QUESTION`.

Generation 8G adds `formalises` (a scoped formal representation of a historical finding) and `proves_local_identity_for` (a linked proof of its declared local model identity, not a promotion of every historical observation to theorem). New nodes carry `formal_refs` into the separate canonical theorem catalogue. Historical statements/layers remain unchanged. The formal validator checks reciprocal catalogue links.

Before a future generation, load this ledger and name the nodes that motivate the next question. Most new results should connect first to nearby structural findings. A global-coherence interpretation is a separate layer.
