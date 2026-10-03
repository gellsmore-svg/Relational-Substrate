---
name: human-book-readability
description: Review a long-form non-fiction book, outline or chapter for human comprehensibility, meaning conceptual load, inferential gaps, cohesion, concept ordering, terminology stability, repetition and flow, not just reading-ease formulas. Use when asked to assess or improve the readability of a book, manuscript, chapter or outline, to estimate "human context load", to check that concepts arrive after their prerequisites, or to run a readability pass on serious technical, philosophical or theological prose.
---

# Human book readability

Readability for serious books is mostly **conceptual**: can a declared reader build the intended mental model with the working memory they have? Surface formulas (Flesch, Dale–Chall) are low-level indicators and must never be reported as comprehension scores. Research basis: [REFERENCE.md](REFERENCE.md).

## Inputs to establish first

1. **Reader profile.** Prior knowledge, domain familiarity, motivation. Cohesion and scaffolding effects reverse with expertise, so never review without one.
2. **Concept inventory or graph,** if one exists. If not, extract the 20–60 load-bearing terms first.
3. **Unit of review:** outline, chapter, or whole book.

## Workflow (summary)

Full procedure: [BOOK-REVIEW-WORKFLOW.md](BOOK-REVIEW-WORKFLOW.md).

1. Run `scripts/book_metrics.py` for the surface, cohesion-proxy, terminology, reactivation and style indicators. Treat its output as *evidence*, not verdict.
2. Estimate the **Human Context Load (HCL)** vector for each major section ([COGNITIVE-LOAD.md](COGNITIVE-LOAD.md)).
3. Check **concept order** against the graph: every concept introduced after its prerequisites; the distance from prerequisite to use; reactivation where needed.
4. Check **cohesion and coherence**: entity continuity, missing connectives, unstated inferences, ambiguous references ([DISCOURSE-COHERENCE.md](DISCOURSE-COHERENCE.md)).
5. Run **adversarial reader passes** from the declared profiles. Record exactly where each would lose the thread.
6. Score with the **rubric vector** ([RUBRIC.md](RUBRIC.md)). Every score carries a reason, its strongest weakness, evidence and a revision action.
7. Prioritise revisions by *risk × centrality*: a high-HCL passage on a load-bearing concept comes first.

## Non-negotiables

- Report a **vector**, never one overall number.
- **Inferential gaps** outrank sentence length. The best fix is usually an added "because" step, not a shorter sentence.
- More than about **4 interacting novel concepts** in one passage with no prior chunk to hold them is high risk.
- Do not fragment prose to lower load. Decompose *concepts* across a sequence, and keep *paragraphs* continuous.
- Distinguish **reinforcement** (a brief reminder after distance), **deepening** (a return at a new level) and **redundancy** (repetition without gain).
- Every analogy states what maps and what does not.
- If every dimension scores well, run a red-team pass before accepting the result.

## Outputs

A review file containing:

- the reader profile;
- metric summary;
- HCL table;
- concept-order findings;
- cohesion findings;
- adversarial findings;
- the rubric vector with reasons;
- a ranked revision list.

Keep it actionable. Cite line or section anchors.
