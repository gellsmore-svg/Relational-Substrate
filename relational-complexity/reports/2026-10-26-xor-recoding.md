# When recoding simplifies support but does not preserve prediction

## Completed increment

This analytic increment answers a bounded-family question prompted by Atlas-018:
which XOR update directions can become single-coordinate moves, and when may
the resulting inactive coordinates be discarded? The full proof and precise
assumptions are in `docs/xor-mask-recoding.md`. This is not a new frozen atlas
round, and its software fixtures are not counted as scientific cells.

The starting live branch was `b4fda19a1f964e09e3080c816a49f8fba1629955`.
The selection was committed and pushed as
`7061e7e8e8a5a2a4140c91024b8a60aef86b2aed` before the checks.
The governing prompt is `prompts/2026-10-26-next-otr-cycle/RESEARCH-PROMPT.md`.
Selection reasons and deferred alternatives are in
`docs/2026-10-26-xor-selection.md`.

## Findings and their limits

**Directions, not event names.** After aggregating equal directions for a
kernel-level comparison, distinct XOR masks become distinct coordinate axes
under one invertible binary-linear recoding exactly when they are linearly
independent. An independent set extends to a basis. A dependence cannot map to
distinct independent axes. This is a support statement, not independence of
the resulting coordinate processes or preservation of original event meanings.

**Predictive closure needs a second condition.** Once independent directions
are recoded, dropping the inactive coordinates is exact precisely when each
fixed observed-state block either entirely halts or has nonzero weight vectors
on one positive ray. Common scaling can disappear under row normalisation;
relative rate changes can remain consequential despite unchanged support.
A mixture of a halted and an enabled row is nonexact even though the naive
cross-product equations all vanish against the zero vector.

**Some supports resist more than linear recoding.** The three-mask circuit
`{1,2,3}` supplies a triangle. The four-mask circuit `{1,2,4,7}` is bipartite
but supplies four common neighbors for two distinct states. Hypercubes have
no triangles and at most two such common neighbors. These are two particular
obstructions to injectively encoding the same transitions as single-bit steps,
even with more target bits. They do not exclude changed clocks, latent-state
models, other observables or every alternative encoding of every event law.

**A control against overinterpreting Atlas-018.** The old directions `{1,6,8}`
are independent with rank three. Adding direction `2` gives four independent
directions, not an unavoidable new primitive. A new recoding can make all four
coordinate moves even when the old disagreement coordinate is no longer
invariant. Failure of EQ-033's particular map is not failure of all maps.

These are applications of binary linear algebra, finite support invariants and
the block-row definition of strong lumpability. The references and direct proofs
in the methods note identify established precedents rather than presenting them
as new general laws. No physical or ontological conclusion follows.

## Independent software evidence

The analysis identifier is `xor-mask-analysis-0.1.0`. The checker is
`provenance/xor-mask-analysis-check.py`; the exact saved output is
`provenance/2026-10-26-xor-verification.json`.

| Validation domain | Actual check |
| --- | --- |
| All distinct nonzero-mask subsets of size at most width, widths 1–4 | 2,014 sets; pivot rank and the independent subset-XOR oracle agree |
| Constructed recodings on independent sets | 1,447 constructions checked as bijections; 78,622 directed-edge checks |
| Dependent subsets in that bounded domain | 567 rejected as coordinate-axis bases |
| Two-direction, one-hidden-bit weight vectors with entries in `{0,1,2}` | All 81 vector pairs; exact block rows agree with the algebraic criterion |
| Closure outcomes in that software domain | 15 exact, 66 nonexact; not a frequency claim about the research model space |
| Canonical support fixtures | Triangle witness and four-common-neighbor witness; independent cube controls do not have either obstruction |

Separate controls include raw vectors `(1,2)` and `(2,4)`, which normalise to
one law; `(1,1)` and `(1,2)`, which share support but lose closure; switching
enabled directions; a halt mismatch; and the all-halt null. Their numerical
values are validation choices, not next-round probability targets.

In the 81-pair check, each pair is reused at every observed active state and
differs only with the hidden bit. This exhausts those local vector pairs, not
every eight-state weight function. The proof supplies the general dependence
on the observed state; the finite enumeration does not establish it by sampling.

Sixteen new test cases and the full 193-test RRC suite passed. The checker does not call RRC workers or modify
the main engine. Its fixture enumeration is small, deterministic and bounded;
the general proofs are not extrapolated from the finite counts.

The saved verification JSON has SHA-256
`001ffc3d975628e9c8e3a0ad055098863dafbe7d23bb336dc2a3f07cc4acfb78`.

Reproduce from `relational-complexity/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 provenance/xor-mask-analysis-check.py
PYTHONDONTWRITEBYTECODE=1 /home/cello/domains/Relational-Substrate/constraint-lab/.venv/bin/python -m pytest tests/test_xor_mask_analysis.py -q
```

The second command uses the existing local environment without changing it.
CI can use the project's documented editable installation instead.

## Integration and stopping point

The committed scientific atlas count stays 218; the 15 historical failures are
still excluded. There are zero new scientific worker invocations, zero adopted
cells and no new experimental plan hash. Atlas-001–020 plans, preflights and
completed result bytes, including the locally deferred Atlas-019/020 outputs,
remain unchanged. The older engine and both historical event-kernel methods
retain their interpretations.

The increment explains three separate questions: whether directions admit
coordinate-axis recoding; whether an observation is predictively closed; and
whether a support has an invariant obstruction beyond linear maps. It does not
classify all nonlinear recodings or all relational compositions. The broad
atlas questions remain open. New scoped analytic registers make these results
navigable without promoting software cases to experimental observations.

A later inquiry could study nonlinear embeddings beyond the two circuit
obstructions, or dynamics where the omitted coordinate itself changes. Another
could compare labelled-event preservation with kernel conjugacy. None is imposed
as the next round. Restart with this report, the methods proof and the selection
record, then choose again for information value.
