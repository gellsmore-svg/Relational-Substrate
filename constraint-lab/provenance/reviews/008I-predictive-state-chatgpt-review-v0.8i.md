# External Review 008I predictive-state

External review supplied by the user in Prompt 008K, recorded before substantive
synthesis. This document records that supplied review; it is not a claim that
the implementing agent performed the external review independently.

Target branch: research/constraint-lab-v0.8i-predictive-state
Reviewed head: 6c8f052c2d3361516e08c5a3def10a15474096cc
Chronology: 11 commits ahead of Generation 8H.

## Inspected scope

Branch chronology; I0 freeze; freeze exception; prior related exposure;
generic exact partition refinement; 384->28->12->2 non-neutral ladder;
64->11->7->2 neutral ladder; S4 marked-pair quotient; graph-class 28-state
minimal refinement; edge-count 12-state refinement; parity all-order erasure;
two-snapshot synchronization; Markov-order results; stationary one-step
invisibility; temporal conditional information; quotient commutation;
theorem catalogue; coherence close-out; final-head CI.

## Freeze and commits

- Frozen I0 plan: 872dd1344c60325d8d545d13c38c13c85d8483d1
- Canonical plan hash: 328be1bf7dbac354d5bc4d0510c76555bbe638e8485d8089f63bea0898d9825c
- Plan-file SHA256: 805a4e568341ab2947ea36d7c28cba5449e0d6fd2a6572f3664aebefc9b511f7
- Exact results: 2c8e21415dfa0281746de9c106e080253fb59a07
- Formal proofs: 44fd0ffcb7c3321e1b99a3b35933f1235e539079
- Catalogue integration: c3e718d450d6ac1acfd235876743faa5f0305cc8
- Snapshot: e7b89f9d95b1ef06ea2088e38decb2d1bdc28b29
- Closing head: 6c8f052c2d3361516e08c5a3def10a15474096cc

Final-head Actions run 38587523159 succeeded on the exact closing head.
Both constraint-lab and books jobs succeeded. Local full suite: 368 passed.

## Permanent provenance qualifications

Qualification A: not blind. Previously exposed results came from alternate
role-grammar 8I head 6615c9f03a1fa30558f8cf519a125e610d393f31 and coarse-process
8J head 64a4fe67e585e5be03f6afb2a0613e147c509b63. Exposure included 28 roles,
the twelve-state count/role quotient, class-pair reconstruction, related coarse
temporal information and order results. The new principal targets were generic
exact refinement, minimality certificates, membership equivalence and quotient
commutation, not independent discovery of the known related results.

Qualification B: pre-freeze test_v08h.py re-ran published non-neutral
labelled-mask temporal/Markov-order checks, violating a literal reading of the
008I prohibition. New graph/count refinement, 28/12 minimality certificates,
coarse CMI and quotient-commutation targets stayed unopened until pushed freeze.

External review verdict: **Procedural deviation, not scientific invalidation.
No rerun required.** The exception must not be deleted or retrospectively repaired.

## Reviewed scientific scope

Non-neutral minimal strong refinements: mask 384, class 28, count 12, parity 2.
Neutral refinements: 64,11,7,2. The model-specific compression path is exact pair
identity -> structural marked-pair role -> last formation/dissolution -> none.
This is observation-relative predictive compression, not an ontology hierarchy.

The eleven N4 graph classes have pair-role counts 1,3,4,2,2,2,4,4,2,3,1.
Generic refinement and independent S4/Aut(G) partitions agree. Two class
observations synchronize the non-neutral 28-state refinement.

The count refinement has (0,0),(k,0),(k,1) for k=1..5,(6,1), twelve states.
Here r is remembered-pair presence, equivalently last formation (1) or
dissolution (0). Down probability is [k+(m-1)r]/(m+5); up probability is
[6-k+(m-1)(1-r)]/(m+5). Two counts synchronize it. Class and count stationary
order is two non-neutrally, one at neutral.

Parity is pathwise R_t=R_0 xor (t mod 2), independent of multiplier/history
given initial parity at ALL temporal orders. It is not merely a zero-CMI result.

Stationary CMI (nats), m=1/4 then m=4:
- mask: 0.06751737542833735558..., 0.21066571905623144862...
- class: 0.02788083444593021907..., 0.10741301177849012749...
- count: 0.01055645618624704153..., 0.05170056159049064334...
- parity: exact zero at both.
No general monotonic conditional-information theorem follows from that ladder.

All adjacent arrows are deterministic strong lumpings. Direct/composed kernels
and stationary pushforwards agree. This is a positive exact valid-quotient
example after 8A's visible-only quotient warning.

Reviewed entries: CL-T52..CL-T59, CL-F08, CL-N08. Namespace must be audited
against divergent branches before assigning new IDs.

## Coherence recommendation

Reviewed totals: 140 findings, 205 relations. Q-H-MINIMAL-STATE and
Q-H-COARSE-GRAINING retain status unresolved despite scoped partial-answer
relations. Review recommends additive recorded transitions to qualified if
consistent with ledger conventions. Do not close the general questions or alter
their statements/creation metadata/historical snapshots.

## Authored Prompt 008I metadata

Externally verified authored predictive-state prompt: 54,103 bytes, SHA256
78728586acc1c47a0b0f3af9b418c0b6e66b06a081e39cc5ce17bde1dc4af43a.
Stored agent transcription: 54,159 bytes, SHA256
99cce12712ab204a60c6c67a8bbe7c75492a2a43562289e0cdf3d1029a2e70fc.
These are distinct representations. Historical transcription remains unchanged;
the authored artifact itself is not supplied for byte comparison.
