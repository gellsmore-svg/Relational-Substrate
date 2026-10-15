# GT-P012 handoff to the shared synthesis hub

*Not the hub update itself. The hub milestone on branch `hub/gt-p010-p011-milestone` (draft PR #9) is extended to cover GT-P010, GT-P011 and GT-P012; see the PR #6 description and `provenance/execution-GT-P012.md`. Nothing here is accepted; candidates are `proposed`.*

| Item | Value |
| --- | --- |
| GT-P012 close | the provenance-close commit after this file (in `provenance/ledger.jsonl`) |
| E5D freeze / results | `c74d896325ead635e010ab809b36d78ca7746247` (plan_hash `6a83dbb788ace935a83ed1c1769a1b4cdd1a6dd3a0dad7b2b94acff1bef21fe7`) / `6749346` (payload `228b7bb9d3131fabe6e292a4519152c701536af2b5e73ebfcd740d97605e8def`) |
| Snapshot | `coherence/snapshots/through-gt-e5d.md` |
| New records | GT-F98 to GT-F103, GT-Q26, GT-R167 to GT-R178 |
| Qualification edges | GT-F101 qualifies GT-F84 and GT-F94 (the PATHF effect is traffic); GT-F100 supports GT-F93; GT-F102 supports GT-F95; GT-F103 supports GT-F92; GT-F98 refines GT-F88 |
| Review status | GT-P010, GT-P011 and GT-P012 are closed and scientifically unreviewed |

## Shared questions

| Question | GT-P012 report |
| --- | --- |
| XQ::01 | A finer projection (local/remote) explains PATHF but not PATHH or PCOMP class durability: comparator adequacy is family-specific and projection-relative. |
| XQ::03 | Anchor-local counts are unchanged (T13). NL's circulation is a projection property. |
| XQ::04 | The one durable residual (PATHH triangle) is not flicker and not traffic; identity remains analyst-anchored. |
| XQ::07 | NL is a stationary-flux lift on a two-component projection. CL's Kpi is a stationary-conditional kernel on (P, h1). Both are coarse comparators defined from stationary flows; no common theorem is shown. |

## Candidate (proposed)

**C-4.** `GT::GT-F98-NL-LOCAL-REMOTE-TRAFFIC-COMPARATOR` ↔ `CL::F8N-H1-MATCHED-PASSAGE-BOUNDARY`, type `requires_scope_alignment`.
- **The claim.** Both are coarse comparators defined from stationary flows on a projection: NL preserves directed (possibly circulating) macro fluxes; Kpi matches the full adjacent joint on (P, h1).
- **Eight dimensions:**

  | Dimension | GT | CL |
  | --- | --- | --- |
  | State | graph | (P, h1, h2) |
  | Clock | CT | epochs |
  | Projection | (ℓ, r) | (P, h1) |
  | Transition law, support, horizon | differ | differ |
  | Intervention | none | none |
  | Conditioning | stationary | stationary |

- **Lineage:** 8G.
- **Falsifier:** a CL projection where the directed-flux lift and Kpi disagree on a matched quantity.
- **Category:** `candidate`.
