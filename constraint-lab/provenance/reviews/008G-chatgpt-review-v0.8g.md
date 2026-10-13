# External Review 008G: Generation 8G formal integration

Authoring source: external review supplied in Prompt 008H, recorded by the implementing agent.
Target branch: `research/constraint-lab-v0.8g-formal-integration`.
Reviewed head: `22e252e560cc711d337b6ae506b0fb76728247d6`.

This record does not retrospectively claim that the implementing agent performed
the externally supplied review. Historical formal statements and provenance remain unchanged.

## Inspection scope

The review inspected branch chronology; final-head CI; theorem catalogue; formal
grammar; current-state expressivity theorem; K/interaction-order scope correction;
stationary factorisation theorem; shape-given-edge corollary; counterexample
boundary; equivalence hierarchy; symmetry/quotient formalisation; H/L compilation
test; coherence snapshot; and provenance close-out.

## Chronology and CI

The reviewed branch was **11 commits ahead of Generation 8F**.

- Formal coherence snapshot commit:
  `6cae75c2eb3baa85969e8f221c4cc12530cdd178`.
- Closing provenance commit / final head:
  `22e252e560cc711d337b6ae506b0fb76728247d6`.
- Snapshot-head Actions run: `38438048094`, successful.
- Final-head Actions run: `38439269919`, successful on the exact closing head.
- Both `constraint-lab` and `books` jobs succeeded.
- Snapshot-head suite: **301 passed**.

The formal catalogue had 45 entries: 25 ALGEBRAIC_THEOREM,
4 FINITE_EXHAUSTIVE_RESULT, 6 NUMERICAL_KERNEL_RESULT, 2 MODEL_INFERENCE,
3 METHODOLOGICAL_PRINCIPLE and 5 OPEN_QUESTION.
No G0 scientific computation or new stochastic experiment was opened.

## Current-state expressivity boundary

For the unbounded positive-factor O2/O3 literal parser/backend, every strictly
positive current-state event-weight table on the existing finite single-bit-toggle
support is constructible with finite expression complexity and rule cardinality:

```text
K <= D
J <= D * 2^D
```

Assumptions: fixed current state; positive weights; existing single-toggle support;
arbitrary positive factors; unbounded backend rule budget.
The theorem does not provide arbitrary support, multibit events, self-loop
universality, history dependence, finite-W4 completeness or bounded-runner
completeness.

This explains why the next controlled boundary is history rather than additional
current-state K/J expansion.

## History versus compilation

One fixed H=0 law on unchanged complete material state x supplies one future row.
If one common controller assigns different futures to reachable histories ending
at identical x, no such fixed-state kernel reproduces both conditional rows.

This is representation-relative non-compilability, not absolute non-Markovianity.
Finite history can be made Markov by augmenting represented state. The ordinary
material projection and the augmented process must be distinguished.

## Stationary factorisation and scope

The autonomous single-action theorem assumes its distinguished pair rate depends
only on its own bit and hidden bits, with other pair/hidden flips symmetric unit.
Stationary pair occupancy factorises into that action bit times uniform other
pairs. The shape-given-edge corollary is not intrinsically N=4-specific.

An action rate reading another visible pair bit lies outside the theorem and has
a symbolic counterexample. Generation 8H does not challenge the theorem merely
by increasing N.

## Authored Prompt 008G metadata

Externally verified authored representation:

```text
bytes: 45624
sha256: e2b9ba3c4bef322b060b48d7629d29b439d1f2636b5e6e35db6e4e7c158a5a62
```

Unchanged stored agent transcription:

```text
path: constraint-lab/provenance/prompts/008G-v0.8g-agent-input.md
bytes: 45632
sha256: 81703b51e2d869da5fda862d9528c854846cdf8b037f54aac6ad400a7f1e704e
```

These are distinct representations. The authored artifact is not imported or
byte-compared here; relationship remains unknown. Its hash is not assigned to
the stored transcription. Metadata is appended in provenance rather than rewriting
the historical 008G execution or prompt.
