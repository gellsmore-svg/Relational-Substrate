# Books and Manuscripts

This directory contains the book-length manuscripts of the Relational Substrate (RS) framework.

## Included Volumes

- **relational-substrate.md** — *The Relational Substrate: A Hierarchical Ontology of Runtime Physical Reality*
  The technical volume. Detailed ontology, primitives, axioms, the transformation tier, and the numerical research record.

- **coherent-biblical-ontology-second-edition.md** — *Coherent Biblical Ontology*, **Second Edition** (October 2026). *Current edition.*
  A Scripture-first account of a relational creation, rewritten from first principles around the current research: constrained possibility (admissibility and tendency), constrained stochastic actualisation, identity as preserved invariance, Transmit–Carry–Receive, emergent regularity and the place of mathematics, and the argument that a relation-first physical world matters for global coherence, while material, living, personal and spiritual categories remain distinct.
  The chapters are edited in `v2/manuscript/` and assembled into this file with `python3 books/v2/tools/assemble_manuscript.py`.

- **coherent-biblical-ontology-bachelors.md** — *Coherent Biblical Ontology*, first edition (master draft v3, August 2026). *Preserved as the historical baseline.*
  Its theological chapters remain largely sound and much of their substance is carried into the second edition. Its physical chapters present mechanisms (closure knots, a closed five-operation set, torsional light) that later research did not support, and it predates the stochastic and T-C-R work. See `v2/analysis/research-baseline.md` for what changed and why.

## Editions at a glance

| | First edition | Second edition |
| --- | --- | --- |
| Physical ontology | proposed mechanisms stated as ontology | relation, constrained possibility, constrained chance, invariance, T-C-R, regularity, each with its evidential status |
| Method | coherence chapters added late | description versus ontology and levels of claim set out before any physical claim; "not an empirical proof" stated plainly |
| Other worldviews | foreclosure lists throughout | one appendix, "Points of Divergence" |
| Material versus spiritual | stated | defended at every crossing (structural analogy is not ontological identity) |

## The second-edition working record (`v2/`)

The reasoning behind the second edition is kept so the work can be inspected and continued: research chronology and baseline, concept graph (generated, with centrality analysis), human-context-load map, architecture candidates and scores, epistemic register, source ledger, readability reviews, final vector review, the initiating prompt and prompt history, figures and cover sources. Start with [`v2/README.md`](v2/README.md).

## EPUB Editions

Validated EPUB 2 editions are published in [`epub/`](epub/):

- `coherent-biblical-ontology-second-edition.epub` (with front cover, figures and back cover)
- `coherent-biblical-ontology.epub` (first edition)
- `relational-substrate.epub`

Rebuild and validate all three with `npm run books:epub`, or only the second edition with `npm run books:epub:v2`. `pandoc` and `epubcheck` are required. The second-edition build refuses to run if the assembled manuscript is out of date.

Companion volumes exist in draft form elsewhere in the workspace (the general volume *A Coherent World*, and the devotional *How to Hug the Right Tree*) and may be added here in the future.

A free electronic edition is referenced in each manuscript (see the project site, <https://relational-substrate.blogspot.com/>).
