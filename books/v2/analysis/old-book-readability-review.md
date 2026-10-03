# Readability review: *Coherent Biblical Ontology*, first edition (master draft v3)

Skill: `human-book-readability` v1. Metrics: `books/v2/reviews/edition1-metrics.md` (script run against `books/v2/analysis/terms-edition1.json`).

**Reader profile:** an intelligent adult with no specialist physics, philosophy or theology, willing to think. This is the target reader of the second edition (brief §21).

## 1. Measured indicators (summary)

- **Length.** 43,700 words: 17 chapters of 1,000–4,600 words and four appendices (6,800 words). The appendices are 15% of the book, and Appendix D is development tooling addressed to authors and AI systems, not readers.
- **Sentences.** Mean length 13–19 words in the chapters, which is moderate. Long sentences (over 40 words) concentrate in Chapter 5 (11) and Appendix B (11).
- **Surface ease.** Flesch Reading Ease runs 17–41 across the chapters. That is "difficult", as expected for this genre. *Indicator only.* The genuine difficulty lies elsewhere (below).
- **Local cohesion is weak throughout.** Mean adjacent-paragraph lexical overlap is 0.05–0.16, and there are many paragraph starts sharing no content word with the previous paragraph and lacking a connective. Examples: Chapter 4 has 39, Chapter 14 has 33, Chapter 15 has 24 and Chapter 17 has 18. Much of this comes from the list-and-assert style: bulleted claims followed by fresh assertions.
- **Bullet dependence.** Bullet lines make up 42% of non-blank lines in Chapter 14 and 49% in Chapter 10, with every chapter ending in a bulleted "What This Chapter Establishes".
- **Em-dash density** is 7–13 per 1,000 words in several chapters (Chapters 4, 5, 7, 9 and 10). That is high.
- **Meta-commentary.** "This chapter must…", "What this chapter establishes" and "That leaves the next question" appear in every chapter.
- **Terminology.**
  - T0 is introduced in Chapter 2 and then unused for long stretches (maximum reactivation gap about 20,000 words).
  - The T1A–T1D2 sub-stack is used 41 times, mostly in Chapter 4 and the appendices, yet it does almost no argumentative work later.
  - *Stochastic*, *probability* and *carrier* never occur.
  - *Transmission* occurs 13 times, chiefly in the perception passage of Chapter 5.
- **Order violations.**
  - `T2` is named before the T1 stack is listed (minor).
  - `corruption` is named in the preface about 6,600 words before `alignment`, the concept that defines it. The preface is the intended advance organiser, so this is tolerable if it is signposted, and it is not.

## 2. Human Context Load: highest-risk passages

| Passage | N | P | I | A | D | R | T | X | S | F | Risk |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | --- |
| Ch 4 "The Ontological Stack" + "Transformation Tier" | 15+ (T0, T1A–T1D2, T2, five operations, dialects, three admissibilities, alignment, strain) | 4 | 4 | 5 | 4 | short | about 7/100w | 3 | 2 | 1 | **critical** |
| Ch 5 closure knots, slip, phase, time and relativity | 8 | 6 | 4 | 5 | 5 | 1 chapter | 3/100w | 3 (why a closure knot persists; why tension slows clocks) | 3 (rope-slide analogy, bounded) | 1 | **critical** |
| Ch 2 "Relational Primacy" | 5 | 2 | 3 | 5 | 2 | short | 4.8/100w | 2 (why relation entails continuity) | 1 | 1 | high |
| Ch 4 "Why Continuity Matters Beyond Physics" | 2 | 3 | 3 | 4 | 3 | short | low | 1 | 3 | 3 | moderate (well executed) |
| Ch 8 levels of coherence (7 levels) | 7 | 2 | 3 | 4 | 2 | - | 4.1/100w | 1 | 1 | 2 | high |
| Ch 15 restored alignment | 3 | 4 | 3 | 3 | 4 | 2 chapters (alignment defined in Ch 4) | moderate | 1 | 5 (soldier, marriage, Hebrews 12) | 4 | low (a model of good scaffolding) |

**Diagnosis:** the book front-loads its most abstract apparatus (Chapter 4) before the reader has a reason to need it, and much of that apparatus is never used again. The best-scaffolded passages are the theological ones (Chapters 14–15). The weakest are the physical ontology chapters, which are also the chapters the research has most changed.

## 3. Rubric vector

| Dimension | Score | Reason | Strongest weakness | Revision action (for v2) |
| --- | ---: | --- | --- | --- |
| concept-order | 55 | Scripture → substrate → stack → matter is defensible | Stack and transformation tier arrive as one load spike; T1 sub-levels unused afterwards | Introduce concepts on demand; drop unused sub-levels |
| human-context-load | 45 | Theology chapters are well paced | Two critical passages on load-bearing physics | Decompose relation → possibility → actualisation → identity → T-C-R across chapters |
| inferential-explicitness | 55 | Continuity argument (Ch 4) is spelled out well | Key steps asserted: why relation entails continuity; why closure knots persist; why tension slows clocks | State or remove each step |
| local-cohesion | 50 | Prose passages flow | List-and-assert rhythm breaks entity continuity | Write in paragraphs; connect claims with causal connectives |
| section-progression | 60 | "That leaves the next question" gives momentum | Formulaic; many micro-sections (17 chapters, about 160 headings) | Fewer, longer sections that each answer a felt question |
| chapter-readability | 60 | Chapters have clear purposes | Each chapter opens with a preview and closes with a bulleted summary | One orienting sentence; no restating summaries |
| terminology-control | 55 | Most terms defined | T0 changes sense in the July research; "admissibility" means two things (transformation-tier layers; T0 grammar); "alignment" carries both structural and moral weight | Terminology register; one sense per term |
| semantic-density | 60 | Dense where needed | Containment notes and foreclosure lists add volume, not understanding | Move polemic to an appendix |
| scaffolding | 65 | Bounded metaphors (rope-slide, pressure, compass needles) state their limits | Physics analogies scaffold mechanisms the evidence does not support | Keep the discipline; change what is scaffolded |
| repetition-control | 50 | Some productive deepening (continuity across chapters) | Containment and foreclosure points repeated in Chs 1–5, 10, 14–16 and Appendix A | One treatment |
| narrative-flow | 55 | Strong in Chs 14–16 | Physics and method chapters read as specification | Write as argument |
| voice | 55 | Serious, Scripture-dense, confident | Em-dash saturation; "not X but Y"; triplets; "This chapter must…" | Voice pass |
| reader-orientation | 65 | Clear arc from creation to restoration | The reader cannot tell which claims are Scripture, inference or RS hypothesis | Epistemic status visible in prose |

## 4. Red-team pass

These are the questions a sceptical reader would ask and the book cannot answer.

1. **Circularity.** Chapter 6 says mathematics "had begun to describe, accurately, the behaviour of an unseen substrate reality". That presupposes the substrate in order to explain the history of physics that is meant to motivate it.
2. **Overclaim.** Time dilation is presented as explained by "substrate tension" ("exactly as measured"), but no quantity is derived. A physicist would read this as a relabelling of general relativity offered as an explanation.
3. **Category slippage.** "Beauty, order, truth, and the good are … four perspectives on the same structural property." This risks reducing moral and aesthetic realities to a physical-structural property, the very collapse the book elsewhere forbids. The technical volume itself says that alignment "is not a theological synonym for beauty or goodness" (Ch 42), so the two books contradict each other.
4. **Theological overreach.** Miracles as operations under "wider permissions … not violations of the grammar" place Christ's acts inside creaturely substrate admissibility. That is a contested inference stated as the framework's position.
5. **Polemic displacing ontology.** Chapter 11 and Appendix A spend more words excluding positions than Chapters 2–3 spend constructing the substrate.
6. **Missing research.** The book contains none of the September–October work: stochastic actualisation, identity as invariant across stochastic paths, T-C-R, and admissibility versus tendency.

## 5. Conclusion for the rewrite

The first edition's theological chapters are its strongest material and should be substantially retained, with lighter structure. Its physical ontology must be rebuilt from the research baseline and decomposed into a sequence of graspable acquisitions. Its method material (coherence, description and ontology) should be strengthened and de-polemicised. Its apparatus (unused stack levels, the operations typology, foreclosure lists, the thought-work appendix) should be removed from the reader's path.
