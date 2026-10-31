# Readability review: the three tiered editions (October 2026)

Method: the `human-book-readability` skill, with metrics from `.claude/skills/human-book-readability/scripts/book_metrics.py` run against each assembled tier using `analysis/terms-edition2.json`. Metrics are evidence, not verdicts. Reader profiles and budgets are in [`../README.md`](../README.md). Source of truth: revision 2.7 (`books/v2/manuscript/`, Appendix E).

## Outcome against budget

Prose words exclude Markdown markup. Read-time is at 200 words a minute.

| Tier | Budget | Main path | Read-time | On demand | Within ±10% |
| --- | --- | --- | --- | --- | --- |
| Beginner | 9,000 | 9,798 | 49 min | none | yes (+8.9%) |
| Intermediate | 16,000 | 17,598 | 88 min | none | yes (+10.0%, at the ceiling) |
| A-level | 22,000 | 22,829 | 114 min | status table, 782 | yes (+3.8%) |

All three first drafts overran (Beginner by 20%, Intermediate by 18%). They were compressed by cutting recaps to three bullets, removing restated illustrations, and dropping one section the Intermediate reader does not need (created runtime order, kept at A-level). No integrity item was cut.

## Integrity set

All sixteen items in the README's integrity table were checked by phrase search in each assembled tier, and confirmed by reading where the search was inconclusive. All are present in all three tiers. The items most at risk of being softened in a short edition were kept explicitly:

- **I6**, matter's non-material foundation as premise versus hypothesis;
- **I7**, openness concerning created determination, not divine knowledge (the c5fda91 clarification);
- **I11**, the fossil-record conflict named and left open.

## Metric summary

Measured on the assembled drafts before the review fixes below; the fixes shortened sentences and did not add terms.

| Indicator | Beginner | Intermediate | A-level |
| --- | --- | --- | --- |
| Mean sentence length (range across chapters) | 10.5 to 17.0 | 11.3 to 17.3 | 16.1 to 21.9 |
| Sentences over 40 words (whole book) | 3 | 3 | 33 (many are list or caption artefacts; see below) |
| Flesch* (range) | 75 to 85 | 55 to 68 | 20 to 48 |
| Em dashes | 0 | 0 | 0 |
| not…but constructions | 4 | 14 | 24 |

*Surface indicator only.

Prerequisite-order "violations" reported by the script are artefacts of matching the full edition's term list against tiers with different vocabularies. The Beginner tier uses "relationships" where the list expects "relation". "Carry" first appears as an ordinary verb, and "restoration" first appears as a forward pointer. The A-level preface previews T-C-R before Chapter 7 defines it. None is a concept used before it is explained.

## Human Context Load (HCL)

Load is judged against each reader's profile. High (H) means more than about four interacting novel concepts with no prior chunk to hold them.

| Passage | Beginner | Intermediate | A-level |
| --- | --- | --- | --- |
| Ch 1 Scripture and the world | L | L | M |
| Ch 2 How we know | M (machine, coherence, elasticity) | M to H (six layers, coherence scopes, elasticity, comparison) | **H** (adds accessibility respects, true and inferential logic, proof, coherence factor) |
| Ch 3 Relation before things | M (two pictures, interoperability, premise vs hypothesis) | M to H (A/B/C) | H (A/B/C with routes, grounding regress) |
| Ch 4 What can be | L | M | M to H (T0, T1, explicit and implicit constraints, opportunity) |
| Ch 5 Chance | L | M | M |
| Ch 6 Identity, materiality, time | M | M to H | H (densest physical chapter) |
| Ch 7 T-C-R | L | M | M to H (organiser and coherer, cause, enabling) |
| Ch 8 Organised identity | L (merged into Ch 7) | M | M to H |
| Ch 9 Regularity and mathematics | L (merged into Ch 5) | M | M to H |
| Ch 10 onwards (theological arc) | L to M | L to M | M |

Mitigations: the A-level Chapter 2 now opens with a roadmap of its six tools, and its tests of coherence are a list, not one 65-word sentence. A-level Chapters 3 and 6 rely on subsection headings and closing summaries. Splitting them further would break the source's chapter correspondence.

## Concept order and cohesion

- Every tier introduces each term once, at first need, and keeps it. "Constrained chance" (Beginner) and "constrained stochastic actualisation" (A-level) each name the source's single concept at the tier's register.
- The recurring stone scene gives every chapter an entry point and is closed in the last chapter of each tier.
- Bridges between chapters follow the source's question-to-question hand-offs.
- **Fixed in review:**
  - Beginner Ch 3 introduced "universal interoperability" without reusing it (wasted lifting), so the label was removed.
  - Intermediate Ch 3 cited "underdetermination", undefined at that tier, so it was replaced by the plain claim with a pointer to Ch 2.
  - Intermediate Ch 4's "non-agentic runtime" lost its explanation of "runtime" when the created-order section was cut, so a gloss was added.

## Adversarial reader passes

- **Beginner (a reader of about 12):**
  - Romans 8:20's "vanity" would be read as pride, so a one-line gloss was added.
  - The author is referred to as "the author", never by pronoun.
  - The four kinds of claim set out before Chapter 1 are reused in Chapter 12, which gives the reader a frame to hang the book's confidence on.
  - A risk remains: Chapter 3's distinction between belief from Scripture and idea being tested is the subtlest point in the book for this reader. It is stated plainly and recapped, but it is a single passage.
- **Intermediate (14 to 16):**
  - A reader may lose the A/B/C comparison in Chapter 3. Its conclusion is restated in the recap and again in Chapter 9's list of what would count against the book.
  - Chapter 6 asks the reader to hold five new ideas (equivalence class, individual, provenance, material organisation, succession). Each is in its own subsection and recapped.
- **A-level (16 to 18):**
  - A philosophy student will look for overclaiming. Each RS claim carries an explicit status, the defeaters list in Chapter 9 is complete, and the status table gives a one-page audit.
  - A physics student will press entanglement and clock rates. Both are named as unsolved, not deflected.
  - Over-long sentences in Chapters 6, 9 and 14 were split. The Chapter 14 sentence was split because it carries an integrity item (animal mortality).

## Rubric vector

| Dimension | Beginner | Intermediate | A-level | Reason and strongest weakness |
| --- | --- | --- | --- | --- |
| Fidelity to source | H | H | H | Every claim traces to revision 2.7. The weakness is that compression loses qualifications the full edition keeps; the integrity set was checked against that. |
| Status honesty | H | H | H | Hypotheses are labelled as such at every tier. At Beginner, the statuses are simplified to four kinds. |
| Concept load for reader | H | M | M | The weakness is the Intermediate Ch 2 to 3 and A-level Ch 2, 3 and 6 peaks (HCL table). |
| Cohesion and arc | H | H | H | The stone scene and question hand-offs carry the arc. At Beginner, the merged Ch 5 and Ch 7 each carry two source chapters. |
| Register fit | H | M to H | H | Intermediate sits between a list-heavy school style and continuous prose, and some sections are denser than a 14-year-old's comfort. |
| Scripture density (house style) | M | M to H | H | Beginner quotes fewer passages, by design. KJV format is preserved throughout. |
| Budget | H | M | H | Intermediate is at the 10% ceiling. |

## Red-team pass

Because most dimensions scored high, a red-team pass asked where a hostile but fair reader would object.

1. **"The short editions make the hypothesis sound more settled than the full edition does."** Checked: each tier states the hypothesis status where the idea is introduced and again in its closing chapter, and Beginner and Intermediate each list what could prove it wrong. Not upheld.
2. **"The Beginner edition still teaches a picture (matter as steady pattern) a child will take as fact."** Partly upheld. The chapter says "the book's idea" and the closing chapter lists it under "the book's best idea", but a young reader may retain the picture without the label. This is accepted as the cost of the tier and left to the author's judgment.
3. **"Animal death and the fossil record are mentioned to be dismissed."** Not upheld. Every tier states it as the author's interpretation and names the conflict as open and unresolved, as the author decided (Q11, option 1).
4. **"Intermediate overreaches its reader in Ch 2 and Ch 3."** Partly upheld. It is the main risk for this tier. The remedy, if wanted, is a touchpoint split (a short "toolkit" chapter before Ch 2), which would add length the budget does not have.

## Ranked revisions

| Rank | Item | State |
| --- | --- | --- |
| 1 | A-level Ch 2 load: roadmap and list form | Done |
| 2 | Intermediate undefined terms (underdetermination, runtime) | Done |
| 3 | Beginner wasted label (interoperability); archaic "vanity" | Done |
| 4 | Over-long A-level sentences in Ch 6, 9, 14 | Done |
| 5 | Intermediate Ch 2 and 3 peak load (red-team 4) | Open: author's call on adding a toolkit chapter |
| 6 | Beginner retention of "matter as steady pattern" without its label (red-team 2) | Open: author's call |
