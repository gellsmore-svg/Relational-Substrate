# Reuse map

RRC reuses mechanisms only where the existing grammar already represents them. Each row says what is reused, what is left alone, and what RRC computes for itself.

## Reused as read-only references

| Existing work | Where it lives | How RRC uses it |
| --- | --- | --- |
| Single-toggle pairwise kernel | `constraint-lab/src/rs_constraint_lab/kernel.py` | The unconstrained kernel is an oracle in tests. Scientific items use RRC's own weight builder so a change in item code cannot rewrite the laboratory |
| Edge numbering | `state.edges`: pairs `i < j` in lexicographic order, bit `e` present or absent | Same numbering, so the oracle comparison is bit-exact |
| Halt completion | Empty admissible set becomes a self-loop, marked and not counted as a relational event | Same convention, under the name `halt_self_loop` |
| Exact SCC structure | `exact.py` Kosaraju on the support graph | RRC implements its own iterative SCC and checks the unconstrained N≤4 case against the laboratory function in tests |
| Strong lumpability is not in the laboratory | — | New. It is classical Markov theory applied to this kernel, not a new transition primitive |
| Symmetry canonicalisation at N=4 | `graphs.py` | Not required for interface partitions, which are label-fixed experimental instruments. Not imported |
| History channels H and meta-state L | Represented, not executed, in `Choreography` | Not used in RRC-001. Hidden *current* state is not history. The expressivity note already separates them |
| Higher-order slots | `higher_order.py`, independent triadic relations | Not opened in RRC-001. A wedge count on pair edges is still an O=2 current-state weight. See `compilation-gate.md` |
| Shard supervisor, receipts, 120-second budget | `execution-resilience.md`, `supervisor.py`, `workstore.py` | Pattern only. RRC writes its own store under `relational-complexity/generated/` so laboratory generation directories are never touched |
| Coherence schema | `coherence.py` at `6cae75c2` | Copied as a validator over RRC's own ledger. The laboratory ledger is not loaded and not rewritten |
| GT feasibility table | `gravity-time/docs/feasibility.md` at `38e92015` | Cost prior: N=6 free mode is 32,768 states and was built in about 5 seconds for a heavy template; N=7 was estimated at 10–20 minutes in the fraction builder; N≥8 is infeasible for exhaustive kernels. RRC remeasures its own builder before freeze |
| Frozen-plan discipline | `scientific-plan-discipline.md` | Adopted in full, including the distinction between identity fixtures and unopened cells |
| OTR 1.0 | `research-methods/open-thetical-research.md` | Governing method |

## Not reused

| Piece | Reason |
| --- | --- |
| GT round modules (`gte5d.py` and the rest) | They answer basin, clock and anchor questions. Importing them would couple RRC's results to GT's scaffolds |
| Held-source templates, relational-distance observables, jump versus continuous clocks | Declared GT instruments. RRC introduces an interface partition and, for propagation only, a path-index scaffold, each labelled as an instrument |
| Generation censuses, W4 alphabets, canonical-simple enumeration | A different question. RRC fixes a handful of rules and varies the reduction |
| Shared synthesis ledger | Different branch. Proposal only |
| Books and ontology proposals | Out of scope |

## Architectural decision

RRC-001 studies **reductions of the existing O=2 single-toggle chain**, not a new generator.

The engine therefore owns:

- integer weights for a declared current-state rule;
- exact rational signatures of a declared partition;
- the strong-lumpability defect;
- a small menu of interface augmentations;
- the lumpable closure of a partition when the state count is inside the frozen budget;
- stationary occupation and toggle rates for propagation items, with an independent solver on the sizes where a dense check fits.

It does not own a new relation order, a history bit, a geometric embedding, or a large-network approximation.

If a later round needs history or an independent hyperedge, the compilation gate is applied again and the failure witness is written down before any code claims a new axis.
