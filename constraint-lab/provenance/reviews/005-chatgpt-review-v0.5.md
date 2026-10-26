# External review 005 — ChatGPT review of v0.5

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.5` at `003a7c64a35ce8e781e7208117e09702ce63a715`.

The review is external to the v0.5 implementation. It is not a line-by-line audit of every generated shard or kernel. Shard directories and individual kernel files under `generated/` were not re-derived one by one in that review.

## What was inspected

- The v0.5 commit history.
- The Generation 4a report and specification.
- The Generation 5 report and specification.
- The Generation 5 row table.
- Provenance Review 004 and Execution 005.
- `passage.py`.
- `v05.py`.
- The v0.5 tests.
- Whole-pair canonicalisation.
- Controlled-source construction.
- The eventual committor.
- The interaction residual.
- State-resolved interaction.
- The final CI state.

## Conclusions recorded from that review

### Execution state

Generation 4a completed:

```text
160 canonical weighted singletons
10 shards
2 workers
0 failed
0 quarantined
```

Generation 5 completed:

```text
50,688 weighted labelled pairs
576 canonical structural pairs
2,304 canonical weighted pairs
6 shards
2 workers
0 failed
0 quarantined
```

The `8 × 10 × 2 × 2 = 320` singleton-orbit grid was not used as the canonical pair count. Complete two-rule systems were canonicalised under `S4`, preserving relative alignment.

The final v0.5 head itself has successful GitHub Actions run `37151937623` on `003a7c64a35ce8e781e7208117e09702ce63a715`. Jobs `constraint-lab` and `books` both completed. This run is distinct from the preceding close-out run `37151793037` on `777191bdb1406f6ee97ebcceae91881ef088019c`. The ledger `ci` line records `37151793037` and says that line is not a run id for the commit that adds it. This review is the record of the final-head run. Do not chase final-head CI by adding commits whose only purpose is to record the run of the commit that records the previous run.

### Generation 4a

Generation 4a completed the missing horizon-16 sensitivity work and introduced the controlled-source eventual committor. Generation 4 itself was not rewritten.

The qualitative Generation 4 pattern survived all predeclared horizon-16 probes:

```text
P->P:  50 / 50 move the focused passage,  0 / 50 hidden-triad-conditioned
T->P:  40 / 40 move the focused passage, 40 / 40 hidden-triad-conditioned
P->T:   0 / 40 move it above the floor
T->T:   0 / 30 move it above the floor
```

The controlled eventual committor remains nonzero for all 40 `T->P` singletons, and the hidden triadic configuration alters that committor for all 40.

Source occupancy was a substantial part of the old stationary effect. For the 40 `T->P` rows, the median of `|occupancy contribution| / |stationary eventual delta|` is approximately `0.75` in both directions. Generation 4 mixed a change in which hidden states are occupied when the source class is seen with a change in the future transition law. The controlled future-dynamics effect survives. `P->P` remains the stronger singleton mechanism on the focused path/matching passage.

### Generation 5 canonicalisation

Generation 5 enumerated:

```text
96 labelled T->P structural rules
132 labelled P->P structural rules
192 weighted T->P rules
264 weighted P->P rules
50,688 weighted labelled pairs
0 invalid structurally-simple pairs
576 canonical structural pairs
2,304 canonical weighted pairs
```

Orbit accounting closes: `384 × 12 + 1,920 × 24 = 50,688`. Complete-set canonicalisation was necessary. Multiplying singleton orbit counts would have reported 320 and missed relative alignment.

The report's 1,280 relative-alignment classes are distinct full alignment signatures, including component orbit identities and weight assignments. They are not 1,280 pure geometric edge/triad relationship categories. Those two counts must stay separate.

### Primary interaction result

For the controlled eventual committor, the interaction residual is outside `1e-8` on 2,304 / 2,304 systems in each direction. The median absolute residual is approximately `0.00397` on path to matching and `0.00437` on matching to path.

The strongest prohibit/prohibit motif has controlled path-to-matching values approximately:

```text
Q0   = 0.18823529411764703
QT   = 0.18808717457278007
QP   = 0.18765207631874303
QTP  = 0.2538772345202259
```

The external review recomputed the residual from those published committors:

```text
I = QTP - QT - QP + Q0 = 0.06637327774634985
```

The super-singleton gap on that row is `G = 0.0650587226036749`. The reverse direction has interaction residual approximately `-0.0805972080418577`.

The motif is an unconditional dissolve-prohibit on one edge plus a triad-conditioned dissolve-prohibit on the disjoint edge. Four condition-polarity and alignment representatives share the aggregate extremum within the effect floor.

### Higher-order selectivity

`Delta_S = S_TP - S_T` is the change in the spread of the controlled eventual committor across the 16 hidden triadic configurations. `Delta_S > 0` on 1,948 / 2,304 path-to-matching rows and 1,576 / 2,304 matching-to-path rows. The strongest prohibit motif has positive `Delta_S`, and that sign survives `rho3 = 1/2` and `rho3 = 2` on the selected extrema. On many systems, adding a `P->P` rule changes how strongly the hidden triadic configuration matters, as well as the aggregate passage.

### State-resolved interaction

On the validated strongest prohibit/prohibit representative, every stored path-to-matching source-state interaction residual is positive, and every stored matching-to-path source-state interaction residual is negative. The aggregate extreme does not hide equal and opposite state-level effects inside the source class.

Direct and iterative committor calculations agreed within approximately `2.9e-12` on the selected extrema. Relabelled `S4` images reproduced the interaction residual to approximately `2.3e-16` or better.

### Epistemic limits

A nonzero residual `I = Q_TP - Q_T - Q_P + Q_0` does not by itself establish a uniquely higher-order interaction. A committor is a nonlinear function of the transition kernel. Two purely pairwise constraints can also produce `I != 0` through ordinary composition, transition normalisation, and multi-step path structure. The fact that all 2,304 targeted systems have nonzero `I` makes a matched lower-order control necessary.

The conclusion supported by v0.5 is that constraint composition is strongly non-additive in the lower-order reconfiguration observable, and that a higher-order-conditioned component can make that non-additivity depend strongly on hidden higher-order relational state. v0.5 does not establish that higher-order conditioning creates a uniquely new kind of non-additivity.

The strongest motif uses `prohibit`, which sets a transition weight to zero. That is qualitatively different from a finite grade. v0.5 does not separate a hard-deletion phenomenon from a graded constraint-composition phenomenon.

Those two distinctions are the subject of the following round. They are not answered by this review.
