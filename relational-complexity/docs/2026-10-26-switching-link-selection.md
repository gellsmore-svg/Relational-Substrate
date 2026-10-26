# OTR selection: switching attachment and fixed-protocol representation

26 October 2026. Starting local HEAD was
`47e9cbeb71034b6f2791a2c6fb7ec24538f365a3`; live research HEAD after fetching
the new prompt is `b1aacb73f68a1e59789eeb1d9e7883f3c3ee81c6`.
Remote main remains at 47e9cbe. All six registered worktrees were checked; none
contains unpublished new research. The only local artifacts are the original
two generated files and deferred Atlas-019/020 outputs. Their directory hashes
still match `../provenance/2026-10-26-adaptive-local-audit.md`:

- generated: `50f1a9578bb54f53590d1bb336766b457e8f16c4ed328851ad8a50a25f8b87b5`.
- Atlas-019: `c462b52c7e343247e32e45754305060629585264d976959ac97df2a03a26461d`.
- Atlas-020: `9d97f9d29fc7adcb76e75a0fe8e03c8174c89c2dc5e60297a35e551936397b25`.

The baseline is 247 passing RRC tests and successful live-HEAD workflow
40396219066. Existing methods, frozen science and other programmes are unchanged.
The atlas remains 218 adopted cells, excluding 15 historical failures.

## Chosen inquiry and assumptions

How much of a changing attachment relation is a new representation requirement,
and how much can an ordinary fixed synchronization protocol express exactly?
Which current-state information must remain when the original actor
configuration is the required observation?

Use two finite nonempty actors with nonnegative integer **off-diagonal** raw
transition matrices A and B, and an independently declared binary link state m.
All `(s,t,m)` combinations are valid. With the link off, one actor updates at a
time; with the link on, two actor moves synchronize with product weight. Link
switches hold both actors and have weights gamma_0/gamma_1. Four distinct output
channels are left, right, joint and switch. Weights are dimensionless. Normalize
only the final global event row; zero rows halt without adding an event.

The link specifies whether the constituents update separately or together;
its change is not merely a new value on the prior fixed shared port. Its
independent state is specified in the input, not inferred from a grouping.
Investigate compilation to fixed all-shared labels with a two-state controller
and explicit unit-weight passive participation, preserving raw labelled weights
and one-event clock. No physical rate or universal composition policy is assumed.

Investigate exact strong lumpability and the coarsest deterministic refinement
of the actor-only observation pi(s,t,m)=(s,t), uniformly over all initial states.
Minimality, if proved, is **only** under this partition-refinement order; it is
not a statement about every recoding, selected initial distribution or history.
Compare fixed link modes and a genuinely switching binary example for same-clock
single-bit support encodings. A finite-state reduction does not automatically
preserve the single-toggle primitive support of rrc-0.4.0.

## Alternatives and qualitative vectors

| Vector | Judgement |
| --- | --- |
| Consequence | Separates changing relationship structure from a fixed-label guarded encoding, and state augmentation from preservation of one-bit event support. |
| Readiness | Local versus joint updates have explicit disjoint observed supports; a controller protocol and exhaustive refinement oracle can be defined exactly. |
| Leverage | Answers where independently declared attachment information enters, what a later protocol can retain, and which state distinctions prediction needs. |
| Cognitive/compute cost | Short algebraic proofs, small exact matrices and bounded software domains; no scientific worker or new atlas round needed. |
| Personal research significance | Examines a relationship that actually connects/disconnects update participation, rather than repeating the previous changing-value interface. |

Alternatives considered: boundary-preserving weighted quotients for shared-port
gluing (valuable but closer to the previous context/boundary track); an additional
rejected-attempt clock comparison (already partly covered); and independent
Atlas-019/020 recovery (different finite observations, not this representation
gap). None is cancelled or mandatory next work. No numeric aggregate, preferred
hierarchy, desired ratio or scientific-cell quota is used.

## Predeclared independent checks and stop

This is analytical-only, `switching-link-analysis-0.1.0`. Give direct proofs of
the compilation and any minimal-refinement claim; finite enumeration checks
implementations rather than extending their quantifiers. Keep the old engine,
event-kernel and analysis identifiers unchanged.

For two-state actors, enumerate their four off-diagonal entries over {0,1,2}
and both switch weights over {0,1,2}: 729 networks. Compare direct guarded global
matrices with independent matching of the compiled three-factor protocol.
For each eight-state network, enumerate all 16 deterministic refinements of the
four-block actor observation (11664 checks), independently test exact block rows
and determine every minimal exact refinement. Compare to the proposed active-
versus-inactive actor-block split; do not assume its minimality from examples.

Include a three-state cycle actor with a two-state actor, non-unit weights,
fully active and wholly inactive cases, a partially inactive case, zero switch
weights and frozen modes, forbidden actor self-loops/invalid inputs, exact
raw-label and old sparse-composition compatibility, and a positive binary
switching support. Check any claimed odd cycle directly and with a separate
bipartiteness algorithm; fixed-mode encodings are controls. No extra hidden step
or reinterpreted halt may be used to claim same-clock equivalence.

Publish this selection before running the new domain. Stop when one scoped
mathematical answer is proved, independently checked, recorded and published;
then automatically merge after all actual integration checks pass. Broad
questions stay open, scientific workers/new adopted cells are zero, and the
protected generated/deferred bytes remain unchanged.
