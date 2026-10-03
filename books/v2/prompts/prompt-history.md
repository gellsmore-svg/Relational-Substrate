# Prompt and process history

## 2026-10-03: initiating instruction

The full instruction is in [`rewrite-master-prompt.md`](rewrite-master-prompt.md), copied verbatim from the session. It asked for:

- a fundamental rewrite of CBO from the current research state;
- a reusable readability skill;
- a concept graph and human-context-load analysis;
- vector-scored architecture selection;
- an epistemic register;
- covers;
- a validated EPUB 2;
- full provenance.

No further instructions were given during the work. It was carried out in one autonomous session, in these stages, each committed separately on branch `book/coherent-biblical-ontology-v2`:

1. **Research baseline.** All branches, the GitHub organisation, the local workspace and the archived ChatGPT export were searched.
   - The stochastic calculator (branch `research/stochastic-calculator`, PR #2) and the constraint laboratory (branch `research/constraint-lab-v0.1`) were found to carry the September–October work.
   - Several programmes named in the brief (the 502-series, a relational stochastic ring, Navier–Stokes, spectral/Grassmannian work) were not found in any record. They were treated as unverified (`research-baseline.md`, D-3 and D-5).
   - The in-progress, uncommitted constraint-lab v0.2 working tree was left untouched and is not cited.
2. **Readability skill.** Literature citations were verified by web search before use. The skill was applied to the first edition first.
3. **Concept graph and architecture.** Five candidates were scored, and the selected one was revised once (D → D′) and red-teamed.
4. **Drafting.** Chapter by chapter, with factual corrections made during drafting:
   - molecule count in a tyre;
   - the subject of Einstein's 1905 paper;
   - the origin of nucleon mass;
   - the constraint-laboratory occupation statement;
   - the SC-024 reliability figure;
   - the status of the false-attractor observations.
5. **Review.** Metrics, voice pass, acceptance tests (added attractor and mathematical-determinism definitions; powers-ontology concession; quantum-interpretation flag), final vector review.
6. **Build.** Covers (seeded SVG), EPUB 2 build integrated into `scripts/build-epubs.sh`, epubcheck validation.

The brief's formulations that the research revised are recorded with reasons in `../analysis/research-baseline.md` §3.
