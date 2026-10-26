# RRC coherence ledger

`findings.jsonl` and `relations.jsonl` are the record. `current-map.md` is a generated view. Do not edit the view by hand.

The schema is the Constraint Laboratory schema at `constraint-lab/src/rs_constraint_lab/coherence.py` commit `6cae75c2`: epistemic layer, magnitude, temporal character, structural roles, a five-coordinate robustness vector, and the controlled relation types. Coordinates are not summed. No row carries an overall score.

Regenerate the view, once the package exists, with:

```text
python -m rrc coherence-view
```

A finding statement is not rewritten when a later round learns more. Add a finding and a relation. This ledger is not the laboratory ledger and not the GT ledger.

Opening rows are questions and one methodological decision. They are not observations. Observations appear only after a frozen round has been executed and verified.
