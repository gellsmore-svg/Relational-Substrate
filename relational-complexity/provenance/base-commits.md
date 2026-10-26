# Source commits

RRC was opened on `research/recursive-relational-complexity` from base

`e2b5dc4cb65bafc423047f78468a63c9d6ceb218`

which is `origin/research/gravity-time-admissibility` at the GT-P012 provenance close. Blobs below are the bytes in that tree unless a different branch is named.

| Document | Commit | Blob | Role for RRC |
| --- | --- | --- | --- |
| `research-methods/open-thetical-research.md` | `4efcd022fd8c7debe961fce961b3d6ff9e227321` | `669754b54e4374d7f8c9a606b1faf4811b7b8569` | OTR 1.0. sha256 `2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd` |
| `research-methods/README.md` | same introduction commit; canonical home note is on `main` | in the base tree | Sharing rule: a file on one branch is not on another. RRC inherits OTR because the base tree already contains it |
| `constraint-lab/docs/research-charter.md` | `aad25e0260cbb55115ddd8561451d61d14e14a08` | `158dd972df87ba6a493fc0d44e2980b891cc54f0` | Laboratory charter. Read, not revised |
| `constraint-lab/docs/scientific-plan-discipline.md` | `1b9d93d536b179150842dfd4eb9a616cc9291539` | `2e6a8d35e1d9939c8d4406ae2f938413ba5b7c85` | Freeze-before-execution and the permanent compilation gate |
| `constraint-lab/formal/expressivity-boundaries.md` | `9fe848a9ce3b05ac03c593941f6ac29dcade2968` | `7dfa431027f5c737a302db8f254849fe3575a159` | CL-T12 and the K/J/state test |
| `constraint-lab/docs/execution-resilience.md` | `37134fc4366adbda284960d536b9ebde7838a8db` | `393724da6e2f75a6173bb80d7b6d5bda1174c7b7` | Short items, atomic shards, interruption tests |
| `gravity-time/docs/feasibility.md` | `38e92015231939bd993ec0b36f4a2ffea5595189` | `d75151d242870a28b2a5d4794bf38ce1572dda5e` | Measured kernel costs at N=4..8 |
| `gravity-time/docs/reuse-map.md` | in the base tree | | Precedent for a reuse map. RRC writes its own |
| `constraint-lab/src/rs_constraint_lab/kernel.py` | `b100754accd3be0b21d2f55f5e72b5925b13e318` | | Reference single-toggle kernel. RRC cross-checks the unconstrained case against it. RRC does not patch it |
| `constraint-lab/src/rs_constraint_lab/coherence.py` | `6cae75c2eb3baa85969e8f221c4cc12530cdd178` | | Ledger schema RRC copies in its own directory |
| `research-synthesis/docs/architecture.md` | branch `infra/shared-research-coherence-v1`, commit `999ce6652609d14e0b8f782bf48a195a432c0365` | `b67997b358091a98dede5fb1a010468668aacadc` | Federation rules. Not present on this branch. Cited read-only |

`main` also carries OTR, introduced there by cherry-pick as `3840a7c` and noted canonical in `cf9f491`. RRC's copy is the base-tree blob, which matches the published sha256.

No Constraint Laboratory generation branch was checked out. Their ledgers were not modified. The GT ledger on this branch is inherited history and is not an RRC source. Cross-programme citations name the GT or CL commit above, not the inherited copy as if it were independent.
