# Final readability review: second edition, v2.1

This review supersedes the v2.0 review, which is preserved in git history at `11495e0`. Its verdict, "no material defect requiring structural change", is withdrawn. The independent review that prompted v2.1 identified load-bearing conceptual defects that the v2.0 readability pass did not detect: T-C-R over-fitted to the calculator protocol, identity reduced to an invariant, and a straw opponent in Chapter 9. A readability pass measures whether a reader can follow the text, not whether what they are following is correct. That limit is now written into how this review is used.

Metrics: `books/v2/reviews/v2.0-final-metrics-rerun.md` (v2.0, recomputed with v2.1 terms) and `books/v2/reviews/v2.1-metrics.md`.

## Indicator comparison, v2.0 → v2.1

| Chapter | Words | Mean sentence | Zero-overlap starts | Note |
| --- | --- | --- | --- | --- |
| 2 | 2,412 → 2,816 | 15.3 → 15.5 | 3 → 4 | coherence tests added as a short list |
| 4 | 2,237 → 2,390 | 14.9 → 14.9 | 6 → 5 | cancellation correction and Generation 2 |
| 6 | 2,203 → 2,999 | 16.8 → 15.7 | 4 → 7 | identity and provenance; the memory evidence list adds paragraph breaks |
| 7 | 3,165 → 3,398 | 15.2 → 15.0 | 10 → 10 | receiver-types list |
| 8 | 2,751 → 3,210 | 17.1 → 16.7 | 3 → 5 | coin rooms, coordination, hidden structure |
| 9 | 3,373 → 2,902 | 16.1 → 15.7 | 4 → 9 | shorter but more listed (alternatives, steps, non-reductions) |

Whole manuscript: about 44,200 words, against 40,900 in v2.0.

- **Em-dashes:** still 0.
- **"Not … but":** stable except in Chapter 9 (4), where the content is a set of distinctions.
- **Prerequisite-order flags:** unchanged in kind. All are advance-organiser mentions or same-section signposts. No new concept appears before its prerequisites. The chapter map passes the topological check.

## Human Context Load

See the v2.1 section of `human-context-load-map.md`. Chapter 8 is now the highest-load chapter, followed by Chapters 6, 7 and 9. Each high-load abstraction is preceded by a concrete case:

- **Coins and keys** introduce equivalence.
- **The lighthouse** introduces non-depleting transmission.
- **Five receiver types** introduce receiver semantics.
- **Two rooms of coin-tossers** introduce the joint process.

## Rubric vector (v2.1)

| Dimension | Score | Reason | Strongest weakness |
| --- | ---: | --- | --- |
| concept-order | 90 | topological order verified | organiser mentions only |
| human-context-load | 74 | richer concepts in Chs 6–8 | Ch 8 now holds the most simultaneous ideas |
| inferential-explicitness | 84 | identity and T-C-R definitions derived from cases; Ch 9 steps rewritten | "recoverable" relies on the reader holding "depends on" |
| local-cohesion | 79 | | list sections in Chs 6 and 9 |
| section-progression | 82 | | Ch 8's research-caveat sections slow it |
| terminology-control | 86 | registers updated; T2 retired; "distinction" standardised | ordinary "difference" coexists with technical "distinction" |
| scaffolding | 86 | five figures; identity figure added | — |
| repetition-control | 82 | analogy guard reduced to high-stakes points | — |
| narrative-flow | 79 | still argued, not specified | caveat density in Chs 6–8 |
| voice | 82 | | some list dependence returned in Ch 9 |
| reader-orientation | 87 | exploratory-research status marked consistently | — |

## Red-team note on this review

The v2.0 review scored conceptual dimensions it could not assess. That was a ceremonial-scoring failure. This review scores only readability. Conceptual correctness is assessed separately in `final-vector-review.md` and in `v2.1-reader-simulation-and-red-team.md`.

## v2.2 update

Chapter 8 went from 3,210 to 3,767 words. Mean sentence length fell from 16.7 to 16.5, adjacent-paragraph overlap held at 0.13, and the three "not … but" constructions are genuine distinctions.

The new orientation paragraph lowers inferential burden: the reader is told in advance that coins, rings, fluids and hidden structure answer four different questions. The simulated first-time reader answered all five Chapter 8 test questions correctly (`v2.2-review-record.md`). Chapter 8 remains the highest-load chapter, and the extra words are mostly the aggregation/coordination distinction the review asked for. Chapters 6 and 7 grew by about 110 and 50 words for their caveats. Metrics: `../reviews/v2.2-metrics.md`.
