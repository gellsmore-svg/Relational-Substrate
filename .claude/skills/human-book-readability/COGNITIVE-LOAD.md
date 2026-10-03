# Human Context Load (HCL)

"Human context window" is an editorial metaphor. Human readers do not have token windows. They have a small working memory (about 4 novel chunks; Cowan 2001), long-term schemas that let many elements act as one chunk, and a situation model that decays and must be reactivated. HCL estimates how much a passage asks the reader to hold *at once*, given what the book has already built.

## The vector

Score each dimension for a section or passage. Use counts where countable and 1–5 bands otherwise.

| Code | Dimension | How to estimate | Research basis |
| --- | --- | --- | --- |
| N | novel concepts | concepts first introduced in this passage | CLT intrinsic load |
| P | active prerequisites | earlier concepts the passage requires the reader to recall *now* | situation model |
| I | interaction density | how many of N+P must be combined simultaneously: 1 = separable, 5 = all mutually dependent | element interactivity (Sweller 2010) |
| A | abstraction | 1 = concrete and perceptual; 5 = relations among abstract relations | concreteness effects |
| D | dependency depth | longest prerequisite chain behind the passage's main concept (from the concept graph) | schema construction |
| R | recall distance | words or chapters since the most distant active prerequisite was last substantively used | spacing (Cepeda 2006) |
| T | terminology burden | technical terms per 100 words, plus terms used before definition | extraneous load |
| X | implicit inferential steps | count of steps the reader must supply | Britton & Gülgöz 1991 |
| S | scaffolding support | 1 = none; 5 = example, bounded analogy and diagram near the abstraction | worked-example and advance-organiser effects |
| F | familiarity to the declared reader | 1 = alien; 5 = everyday | McNamara et al. 1996 |

## Risk rules (explicit, not a weighted sum)

- **Critical:**
  - I ≥ 4 and N + P ≥ 6 and S ≤ 2; or
  - any term used before definition in a load-bearing passage; or
  - X ≥ 3 on a load-bearing claim.
- **High:**
  - I ≥ 4 and N + P ≥ 5; or
  - A ≥ 4 and S ≤ 2; or
  - R spans more than one chapter for a load-bearing prerequisite with no reminder; or
  - X = 2.
- **Moderate:**
  - N ≥ 3 with I ≥ 3; or
  - T > 6 per 100 words; or
  - F ≤ 2 with S ≤ 3.
- **Low:** otherwise.

Raise one level if the concept is load-bearing for the whole book (high graph centrality). Lower one level for an explicitly expert reader profile, since expertise reverses scaffolding needs (Kalyuga et al. 2003).

## Interventions by failing dimension

| Failing | Typical fix |
| --- | --- |
| N high | Split concept acquisition across sections. Introduce sub-concepts first. |
| I high | Build an intermediate chunk (name the combination) before combining it further. |
| A high | Add a concrete instance immediately adjacent to the abstraction. |
| R high | Add a one-clause reminder. Do not re-explain. |
| T high | Replace a term with ordinary English where equally precise, or define it earlier. |
| X high | Write the missing step. This is the most valuable single fix. |
| S low | Add an example, a bounded analogy (with what maps and what does not), or a diagram. |
| F low | Anchor in ordinary experience first, then generalise. |

## Caution

Cognitive load theory's measurement instruments are contested. HCL is a structured editorial judgement for prioritising revision. It is not a measurement of a reader's mind.
