# External Review 008L: completed history-depth-two line

Supplied external re-review, recorded first for Prompt 008M.
Target: `research/constraint-lab-v0.8l-history-depth-two`.
Reviewed head: `147d3156e396f92e3a4a12252468e5fc9dced8cd`.

## Verdict and scope

**Generation 8L passes scientific, mathematical, engineering, provenance,
coherence, and final-head CI review. No scientific rerun is required.**

The supplied re-review inspected the fully completed line, including work
incomplete during an earlier review: 14 additive commits ahead of reviewed 8K,
0 behind; original freeze; typed-cache validation amendment; independent
original-verifier replay; common-start same-X/same-h1 witness; strict H1
compiler; pair-event closure; generic iterative predictive refinement;
stationarity, irreducibility and period; local pure shape; temporal nulls and
lag-two signal; exact mask order three; formal catalogue; coherence and CI.

Actions run `38630877441` succeeded on the exact reviewed head, both
`constraint-lab` and `books`. Full local suite: 425 passed, 30 tests above 8K.

## Original freeze

Commit: `6f00fcdb07fc0e8323f8b6360fdc59960be7dcb4`.
Canonical hash: `b7670bbdac76fb29da687d60c6c5c7c74bf32277d8458442b0bcad947575f7de`.
File SHA256: `4c97e0f0bc87723aa754eae78c57b49972f39559bf24b0f692ce3eefca7dd015`.
Committed and pushed before new non-neutral N4 H2 targets: actual exposure 0.
Symbolic design and capability expectations were known, not blind discovery.

## Validation-only amendment A

An untyped cache could confuse invalid boolean True with valid integer slot 1
after a cached valid call. Scientific inputs used only legal int/None values.
Typed cache keys corrected input validation, not the legal transition law.
Amended freeze: `a889f6a62db7cba51a82d216c4991d118b42bf69`.
Canonical hash: `df27a5078059fbea70836727023b03fa10cde7ccf8e09b8791c8bf1a5193b8d2`.
File SHA256: `417f1adfb126b178ac0a7e736a799637690c67d28488fcbbf0c4bfbf7d9c6311`.
All twelve original results were known: validation-only, explicitly not blind.
All 12 scientific payload hashes and all four summary-table hashes match
exactly. The original verifier separately passes at
`3e71f0687e6097de87efdcab455e1b28c8b2a765`. Original artifacts remain immutable.

## Preserved scientific boundary

History is the two most recent pair slots, updated (h1,h2)->(e,h1); triad
events preserve it. A=(01,12,23), B=(12,01,23) from the empty ten-bit state
end at pair mask 41, zero triads, same h1=23, distinct h2. SECOND-RECENT
future rows differ iff m!=1. Strict state (X,h1), arbitrary positive K/J,
unchanged support/clock/observation and one programme cannot compile both
rows. Hidden state, recoding, expanded history alphabet, time phase and
per-history programmes are excluded. Unrestricted augmentation is possible.

The 2304-state pair chain has generic non-neutral refinement 64->384->2304,
neutral 64, uniform stationary law 1/2304 for every m>0, irreducibility and
period two. Material occupancy and stationary one-step rows are neutral.
Adjacent event dependence and ordinary mask order-two CMI are exactly zero;
lag-two dependence is nonzero iff m!=1; masks have order three non-neutrally.
One/two/three-time material laws match H0; four-time words first distinguish.
The local same-(X,h1) witness has equal edge-count but different shape laws.
Persistent history-marginalised structure remains the new question.

## Formal and coherence close-out

Preserve CL-T68..CL-T76, CL-F09, CL-N09, CL-M06; catalogue total 90.
Coherence: 177 findings, 265 relations. Q-H2-LAST-PAIR-COMPILER is qualified,
not closed; Q-H2-STRUCTURAL-UTILITY is the live new target.
Snapshot: `constraint-lab/coherence/snapshots/through-generation-008l.md`.
Snapshot SHA256: `9d26cdc87112f2a84768d67e327416867c3745fff382355095b39114b5b483a5`.
Ledger SHA256: `6352743e74c276692c07eab7f6860125f6bd630cc4e6930dff107f9e52712955`.

## Provenance distinction

008L transcription: 49,422 bytes, SHA256
`5808e05877dfa8587737e10dba0c41b85ce4745e7388635c57ade8389071b340`.
Independent authored metadata unavailable. No authored identity is invented.
This records the supplied review testimony, not a newly impersonated review.
