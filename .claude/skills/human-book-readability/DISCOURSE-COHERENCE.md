# Discourse coherence checks

Cohesion is the visible ties in a text. Coherence is the reader's connected understanding. Check both.

## Local (sentence to paragraph)

- **Entity continuity.** Adjacent sentences and paragraphs should share a salient entity, or announce the shift (Barzilay & Lapata 2008; centering theory). The script reports adjacent-paragraph content-word overlap; overlap of zero with no opening connective is a flag.
- **Reference.** A paragraph-initial "this", "it", "that" or "such" must have one obvious antecedent. After a heading, a figure or a long quotation, restate the noun.
- **Connectives.** Causal and logical relations should be marked when they carry the argument ("because", "therefore", "but", "so", "which means"). Missing causal connectives on load-bearing steps are a deep-cohesion failure.
- **Dependency length.** Long sentences are acceptable when the dependency chain is short. Flag sentences that hold a subject unresolved across many intervening clauses.

## Section and chapter

- **Question–answer progression.** Each section should answer something the reader now wants answered. Flag sections whose purpose is not inferable from their opening paragraph.
- **Signposting economy.** One orienting sentence beats a preview list. Flag repeated "this chapter will…", chapter-end summaries that repeat the chapter, and thesis restatements within a few pages.
- **Topological order.** Every concept's first substantive use comes after its prerequisites. Compare the text's first-use order with the concept graph.
- **Transitions between chapters.** The opening of each chapter should connect to the last concept the reader holds, not restate the whole book.

## Whole book

- **Terminology register.** One sense per technical term. Track first definition, each later use, and any drift. Equivocation is a coherence failure, not a style issue.
- **Epistemic register.** The certainty of a claim's wording must match its support. Watch for modal drift ("may" becoming "is") between chapters.
- **Category integrity.** An analogy must not later be used as identity.
- **Reactivation.** Load-bearing concepts that return after long absence get a one-clause reminder. Concepts re-explained at length nearby are redundant.

## Calibrating cohesion to the reader

Low-knowledge readers need explicit cohesion. High-knowledge readers can be over-served by it (McNamara et al. 1996). For an intelligent non-specialist, make every load-bearing inference explicit, and leave secondary connections to the reader.
