# RRC integration into main — 26 October 2026

The user's instruction, "merge, and do so automatically going forward", is
recorded in `../AGENTS.md`. It authorizes automatic integration of completed,
validated RRC increments without another confirmation request.

## Inputs and resolution

Default-branch input: `7dd10a81e2e6a8f689a7cefb7088f2d1bca82bfe`.
RRC input: the standing-authorization commit after `954450d`, including the
published contextual-preservation result `6bece5d` and its handoff `24df50c`.
The subsequent adaptive-interface prompt is included as pending research text;
it was not executed as part of this merge.

The research branch diverged before main's later application, book and synthesis
changes. A normal two-parent integration preserves its research commit ancestry
and frozen provenance. Conflicts in README/package and historical directory
moves are resolved by retaining main outside these programme directories:

- `relational-complexity/`: completed research, immutable history and guidance.
- `constraint-lab/`: unchanged dependency snapshot. RRC imports its coherence
  validator and view generator; it was absent from main.
- `gravity-time/`: unchanged snapshot used by laboratory validation and already
  described by the main synthesis. Its files were also absent from main.

Frozen programme artefacts are not rewritten. Main's application sources, package and
lockfile, books, synthesis, scripts, ontology statements and research-method
authorities remain byte-identical. The only changes outside these directories
are additive CI integration and README navigation describing the available
snapshots. The existing application build/report CI job is retained; laboratory,
RRC and book checks are added. Research-branch pushes also run CI.

One laboratory compatibility test is corrected: its claim that the 008G formal
increment preserved books is checked at that increment's published commit
`22e252e560cc711d337b6ae506b0fb76728247d6`, rather than prohibiting every later
book publication on main. Its current checks of immutable laboratory artefacts
and ledger prefixes remain intact. All laboratory production code, data,
formal catalogues and historical evidence, and the full GT snapshot, are
byte-identical to the research branch. Committed-evidence checks are run after
creating the integration commit so HEAD contains the imported provenance.

## Evidence and ongoing operation

RRC's scientific count remains 218 adopted cells, with 15 historical failed
items excluded. Analytic fixtures are not scientific cells. Atlas-019/020 stay
deferred, unadopted and untracked in the original worktree; their content hashes
are preserved. No book or synthesis pin is advanced by copying dependency files,
and merge authority is not scientific peer review or ontology adoption.

Validate the integrated RRC suite, the shared laboratory suite and book checks;
require all pull-request CI jobs to pass before merging. Record actual results,
the full source/integration/merge SHAs and the pull-request link in the PR and
session handoff. Keep the research branch and fast-forward it to merged main
for the next increment, preserving the deferred local output directories.
