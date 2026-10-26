# Catalogue

The catalogue is the growing record of constraint families. It stores measurements. Inferences and RS interpretations are written in the generation report, not in these files.

## What is committed

- `motifs/` — a deterministic selection, at most 48 families per cell. Each file records the canonical expressions, the coordinate (`N`, `A`, `O`, `G`, `S`, `H`, `K`, `L`, semantics, alphabet, cardinality), the observed sentence, the exemplar trajectory signature, the shift and closing ranges, the symmetry class, the number of grammars in the family, and the evaluation vector. The notes object keeps `inferred` and `speculative` empty of scientific claims.
- Family indexes `generation-*-families-n*-k*.jsonl`, when the file is at most 2 MB. Each line is one modal-and-support family: tags, count, expressions of the exemplar, ranges, and the exemplar’s heavy scalars.
- Larger indexes stay in `generated/` and are reproduced by rerunning the specification. The summary’s `family_histogram` still describes the whole cell, including families that were not copied into git.

## Tags

`baseline-equivalent`, `structural`, `measure`, `screened`. See [../docs/observables.md](../docs/observables.md). A screened family crossed a predeclared flag. The flag is coarse. Read the histogram before treating the tag as a rare-event mark.

## Selection order

Within a cell, motifs are chosen in this order, skipping duplicates, until 48 are kept:

1. Every baseline-equivalent family.
2. Up to 12 structural families, smallest cardinality first, then largest dissolution shift.
3. Up to 8 families with the largest absolute closing bias.
4. Up to 8 families with the largest absolute rise-then-release excess on the exemplar.
5. Up to 4 measure-only families with the largest dissolution shift.

The exemplar of a family is its first-seen member: smallest cardinality, then earliest canonical combination.

## Boring records

Baseline-equivalent families and measure-only families are eligible on purpose. A grammar census that drops them cannot show which rules did nothing.
