# Book review workflow

Use the same workflow at every scale. The emphasis changes.

## 0. Declare

- **Reader profiles.** Name 1–3. For example: "intelligent adult, no specialist physics, philosophy or theology; willing to think".
- **Concept list.** A JSON list of terms (aliases allowed) for the metrics script; see `scripts/book_metrics.py --help`.
- **Load-bearing concepts.** Those with high centrality in the concept graph.

## 1. Measure

```bash
python3 .claude/skills/human-book-readability/scripts/book_metrics.py BOOK.md \
    --terms terms.json --level 1 --out review-metrics.md
```

The script reports, per section (split at the given heading level):

- words;
- sentences;
- mean and 90th-percentile sentence length;
- long sentences (over 40 words);
- Flesch Reading Ease (a low-level indicator only);
- technical-term density;
- terms used before their first defining section;
- adjacent-paragraph lexical overlap and zero-overlap paragraph starts;
- paragraph-initial pronouns;
- bullet-line share;
- em-dashes per 1,000 words;
- "not X but Y" and meta-commentary counts;
- per-term first use and maximum reactivation gap.

## 2. Outline review (before drafting)

For each planned chapter:

- purpose;
- concepts introduced;
- prerequisites;
- HCL vector;
- risks;
- reader state on entry and on exit.

Check that the outline order is a topological ordering of the concept graph. Look for chapters with more than four new load-bearing concepts.

## 3. Chapter review (after each draft)

1. Run the metrics for the chapter.
2. Estimate HCL for each major section and mark critical and high passages.
3. Check terms against the terminology register, and claims against the epistemic register.
4. Run adversarial passes: for each declared profile, read the hardest section and write down where understanding fails and why.
5. Score the rubric vector.
6. Revise the two or three highest-value weaknesses, then rescore.
7. Stop when no load-bearing dimension is below about 70 and further passes trade one dimension against another.

## 4. Whole-book review

- **Continuity:** first-use order against the graph across the whole book.
- **Terminology:** drift.
- **Reactivation:** gaps on load-bearing concepts.
- **Redundancy:** repeated explanations across chapters.
- **Flow:** chapter openings and closings.
- **Compression:** which passages add volume without adding understanding.

## 5. Record

Save outputs beside the manuscript (for example `analysis/<book>-readability-review.md`) so later reviews can compare vectors.

## Improving this skill

When a review exposes a failure the workflow did not catch, add the check here. Add the research basis to `REFERENCE.md` and to the research log.
