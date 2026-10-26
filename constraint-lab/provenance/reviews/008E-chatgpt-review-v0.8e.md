# External Review 008E: ChatGPT review of v0.8E

This records the external review supplied with Prompt 008F, targeting
`research/constraint-lab-v0.8e-conjunctive-gates` at
`19d243a83105d0082866b38190ec269d78294e94`. The implementing agent is recording
that review, rather than claiming to have performed its external inspection.
Historical reports, tables, plans, journey records and snapshots remain evidence.

## Inspection scope

The review inspected branch chronology; the frozen E0 plan; pre-freeze
smoke/unit-test exposure; K3 parser semantics; labelled enumeration; the S4
structural atlas; exact local laws; second discrete derivatives; balanced
information and drift; the exact Generation 8D comparison; the Boolean/Moebius
basis; the corner basis; XOR/XNOR constructions; the general-r targeted check;
coherence-map updates; and final-head CI.

## Chronology and CI

Generation 8E is 12 commits ahead of Generation 8D.

| Record | Commit or hash |
| --- | --- |
| Reviewed final head / close-out | `19d243a83105d0082866b38190ec269d78294e94` |
| Frozen E0 plan | `5303388815a3695ac6bf4eb4176c0102b9ca460c` |
| Plan hash | `ec515306c2d3fa669f15ce31a86cdaac78f5fcab0d01ea7ad82533fde71c9be6` |
| Question before execution | `b2811bd2fda8eecc20a0885f51f356fa5b8a812b` |
| Tables / results | `2daf1ce3f54f8bacbc331b6bc575b44ed3f20c27` |
| Report | `11abbd2cb99a641f191f2f43648a5f5b93c0d02e` |
| Snapshot | `fa46cb5a5bd2618076e96d4d7a090287062abb24` |

[Actions run 38412783401](https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38412783401)
succeeded on the exact reviewed final head. Both `books` and `constraint-lab`
jobs succeeded. Snapshot-head constraint-lab CI reported 245 passed; this count
is attributed to the snapshot-head run, not silently reassigned to another run.

## Operational result

E0 used 288 labelled K3 conjunction rules, 20 S4 structural orbits, 80 W4
weighted canonical systems, 27 deterministic execution items, 81,920 full-state
evaluations, 81,920 kernel-agreement evaluations, 1,920 S4 law images, and 160
Generation 8D comparison fingerprints. Execution used one worker, no stochastic
trajectories, no stationary census, no parameter fit and no new controls. The
largest item wall was approximately 3.44 seconds. Verify was complete and
assembly validation was ok.

## Local interaction and non-representability

For every non-neutral single K3 two-triad conjunction, on an admissible action,
`L(U1,U2) = ln(m) U1 U2`, so `Delta12 L = L11-L10-L01+L00 = ln(m)`.
All 80 weighted systems have literal Delta12 `ln(m)`, effective gate dimension 2,
minimal coordinate count 3, gate interaction order 2, two distinct local law
rows, and 128 active full states out of 1024. The local-law/kernel gap is zero.

Symbolically, `c U1 U2 = c0 + a U1 + b U2` holds on all four corners only when
`c = 0`. The additive span has rank 3; adding `U1U2` gives rank 4. Independently,
the finite census found zero labelled matches and zero S4 matches between the
80 non-neutral K3 laws and all 3,584 Generation 8D weighted two-K2 systems.

## Balanced information and drift

`I_K3(m) = (1/2) JS_(1/4,3/4)(q_m,q_0)` in nats:

| m | Balanced information |
| --- | --- |
| 1/4 | 0.006761384413735860 |
| 1/2 | 0.002333270369315632 |
| 2 | 0.003961514536995558 |
| 4 | 0.018447186631125990 |

The analytic/enumerated gap is at most approximately `1.5e-15`.
Balanced rule-induced edge drift is `5(1-m)/[48(m+5)]` for dissolution and
`5(m-1)/[48(m+5)]` for formation. The K3 law has higher interaction order than
the corresponding one-gate K2 law while carrying less balanced information and
half its balanced drift. Magnitude does not rank structural interaction order.

## Boolean and corner bases

In raw coordinates `L = c+aG1+bG2+dG1G2`, with `c=L00`, `a=L10-L00`,
`b=L01-L00`, and `d=L11-L10-L01+L00=Delta12 L`. Continuous positive ordinary
rule multipliers for `1,G1,G2,G1G2` span every real four-corner action-logit
table. The four K3 corner indicators form an equivalent basis. Finite W4
coverage remains a separate question from algebraic completeness.

Two ordinary K3 corner rules realise XOR gate selection and XNOR gate selection,
with kernel gap zero over all 1024 states in the targeted constructions.
`L>0` is not required for the first simultaneous gate-by-gate interaction or
two-gate XOR. Meta-constraints remain a future question about constraints acting
on constraints.

## Required qualifications

The general-r claim requires non-neutrality, distinct gate variables and joint
satisfiability. A contradictory `present(T) & absent(T)` rule never matches and
has zero local law. The additive erratum is
`constraint-lab/reports/generation-008e-errata.md`; the historical report remains
unchanged. The coherence finding `F8E-GENERAL-K-INTERACTION` remains visible with
qualified status and is linked from `F8F-GENERAL-K-SCOPE`.

E0 transparently declared pre-freeze exposure of K3-00 as a smoke test, K3-00
and K3-03 in unit tests, and algebra items in unit tests. The external prompt had
already declared the questions, formulas, counts, candidates and constructions;
the review does not treat that exposure as changing the conclusion. It requests
a permanent stronger scientific-execution gate, recorded separately as a
methodological refinement.

## Prompt 008E representation

Externally verified authored metadata: 44,720 bytes, sha256
`33d535be12b1120f959ad4b04201afc9ad93759675e0dfa0470800b35cbcf01d`.
Stored agent transcription: 44,734 bytes, sha256
`ce1efd0a5463496bd26dd0d171d7111ec1414ccc27a6481bd0ea48ea4194f6a2`.
Its execution record calls it an agent transcription of session input, not a
byte capture, with one transcription slip corrected before storage. The authored
artifact is not imported or byte-compared. Relationship is `unknown`; the known
different sizes exclude byte identity of these two representations. The authored
hash is not assigned to the transcription.
