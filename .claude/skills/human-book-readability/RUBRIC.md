# Readability rubric (vector)

Score 0–100 per dimension. A score is a heuristic judgement. It is valid only with its four companions: **reason, strongest weakness, evidence (with anchors), revision action**. Never average the dimensions into one score.

| Dimension | 90+ means | Below 60 means |
| --- | --- | --- |
| concept-order | every concept follows its prerequisites; distances short or reminded | terms used before definition; prerequisites far away and unreminded |
| human-context-load | no critical HCL passages; high passages scaffolded | critical passages on load-bearing concepts |
| inferential-explicitness | load-bearing steps stated | readers must supply several steps for central claims |
| local-cohesion | entity continuity and connectives carry the argument | frequent unannounced topic jumps and ambiguous references |
| section-progression | each section answers a felt question | sections read as lists of assertions |
| chapter-readability | clear arc and purpose | purpose unclear or fragmented |
| terminology-control | one sense per term, defined once | equivocation or drift |
| semantic-density | dense where it must be, light where it can be | uniformly dense or padded |
| scaffolding | examples, bounded analogies and diagrams placed near abstractions | abstractions unsupported, or analogies unbounded |
| repetition-control | reinforcement and deepening, no redundancy | repeated explanations or theses |
| narrative-flow | reads as an argued book | reads as a specification or a list |
| voice | calm, specific, varied | machine tics: triplets, "not X but Y", em-dash saturation, inflated adjectives |
| reader-orientation | the reader always knows where they are and why | lost between levels |

## Anti-ceremony rule

If more than half the dimensions score 90 or above, run a red-team pass before accepting the scores. Look for:

- circularity;
- a concept used in two senses;
- an unstated premise;
- the hardest passage read as the least-knowledgeable declared reader.

Record what that pass found, including "nothing material".

## Report template

```text
dimension: <name>  score: <0-100>
reason: ...
strongest weakness: ...
evidence: <section/line anchors, script metrics>
revision: ...
```
