# Does the shape of the fixed reference decide where links form?

*A plain-English report for the human researcher on prompt GT-P007 (rounds E4A and E4B, 14 October 2026). It assumes no knowledge of the code. Detailed documents are listed at the end.*

## Why this round

The last round found something awkward. The fixed reference used in every earlier experiment, a triangle of three permanently linked entities, quietly pushed outer entities away. Its own internal links count as "supporting paths" for every possible link to it, and the rules that produce a direction of flow treat supported links as harder to form or easier to break.

Dividing that effect out with a measuring device made those rules gather. But the device was not a rule the model allows, so it proved nothing on its own. You asked for a fair test: change the **shape** of the fixed reference, keep the **rules** exactly as they are, and see what happens.

## What I changed in the code

- **Any set of permanent links can now serve as the fixed reference.** Before, the triangle was hard-wired.
- **The rules still cannot tell which entities are "the source".** They read only which links are present.
- **Checks.** I confirmed that:
  - the computed rates match an independent implementation of the rules exactly, for every shape;
  - renaming the entities changes nothing except the names;
  - the triangle still reproduces every published number exactly.

## What I ran

**Round E4A** (36 cases, frozen before running). Three reference shapes, at 5 and 6 entities, under six rule sets:
- **a single link** (two entities);
- **an open path of three entities**, whose closing link is free to form and dissolve;
- **the original triangle**: these 12 cases repeat published results as a check, and all matched.

**Round E4B** (12 cases, chosen after reading E4A, frozen before running). Two four-entity shapes at 6 entities:
- **a star** (one centre linked to three others);
- **a path of four.**

All 48 cases completed, and every built-in check passed.

## What I found

**1. The reference's shape sorts where links form. This is the clearest result.**
- Within a single reference, the parts that are themselves less supported attract more links.
- In the open path, the middle entity (no permanent supporting paths) attracts about **twice** as many links as the two ends (one supporting path each).
- In the star, the centre (none) attracts about **four times** as many as the tips (two each).
- In the four-path, where every part has the same support, the difference largely disappears. One rule shows it fully; under the other two the middle still attracts a little more.
- These comparisons are made **inside the same system at the same moment**, so differences in size or crowding cannot explain them.

**2. A free link in the reference can switch a site off.** In the open path, when the closing link forms, the middle suddenly has supporting paths, and links to it drop sharply (from 41% to 14% occupancy in one rule). Under these rules the closing link itself is rarely present, because the permanent path it would close counts against it.

**3. Without permanent support at all (the single link), the direction-carrying rules do gather.**
- Under the single-link reference, every such rule gives more links to the reference than the no-rule baseline, in both ways of keeping time and at both sizes: from about 1 to 12 points above.
- This is the first time it happens with the rules unchanged.

**4. But most of that gathering comes from the system being sparse.**
- These rules keep the whole graph thin, and when few links exist, those few tend to involve the reference.
- After adjusting for how crowded the system is, most of the advantage disappears. Only one combined rule keeps a small advantage at both sizes, and it shrinks as the system grows.

**5. Total support is not what decides the overall effect.**
- The star has *more* permanent support in total than the four-path. Yet it gathers (for the simple rules) while the four-path does not.
- Having one completely unsupported site seems to matter more than the total.
- The open path is an exception: it has an unsupported middle but still sits slightly below baseline overall.

**6. The direction of flow survived every shape.** The handover kept its direction under all five references. Its strength varied, being about half as large without the triangle.

## What has **not** been shown

- **This is not attraction in any physical sense.** "Gathering" here means a fixed structure is linked more often than chance in a small random model, mostly because the model stays sparse.
- **Nothing moves.** There is still no notion of displacement, distance as a physical quantity, or acceleration.
- **The fixed reference is imposed.** It is a boundary condition, not something that formed by itself.
- **Seven or more entities were not tested** (not authorised).

## Did anything go wrong?

- **No frozen check failed in either round.**
- **One labelling fix.** The single-probe channels used a fixed entity number, which is a source entity in the four-entity shapes. Before E4B ran, I made them pick a probe whenever the usual one is part of the reference. I confirmed this changed nothing in earlier results.
- **The crowding adjustment is partly hypothetical** at 6 entities, because the systems rarely visit some of the densities it compares against. This is flagged in the tables.

## What I recommend next (not done)

1. **Derive the sorting effect mathematically** (recommended). It is robust and close enough to the rules that a proof, or at least tight bounds, should be possible.
2. **Pause to review what a "reference" should be**: imposed (as now), emergent, or none at all. Five shapes have shown that any imposed reference shapes the results through its own structure.
3. **Separate sparseness from preference** more cleanly, using the data already collected (an analysis, not a new round).
4. Test the single-link reference at **seven entities** (needs authorisation).

## Decisions I need from you

1. Should the next step be the derivation (option 1), the architecture review (option 2), or both?
2. Should the cross-programme note (`docs/e4-cross-programme-transfer.md`) go to the Constraint Laboratory?
3. Should the new ontology proposals (OP-16 and OP-17) be adopted? They are "support can make a site less available" and "gathering must survive density adjustment".
4. Should PR #6 stay a draft?

## Where to look

| What | File |
| --- | --- |
| This report | `gravity-time/reports/gt-e4-report.md` |
| How the reference is now configured, and its checks | `gravity-time/docs/e4-configurable-scaffold.md` |
| The mathematics of supporting paths | `gravity-time/docs/e4-formal-witness-floors.md` |
| Every case | `gravity-time/reports/gt-e4a-atlas.md`, `gt-e4b-atlas.md` |
| Reasoning between rounds | `gravity-time/reports/gt-e4a-reflection.md` |
| Synthesis and next steps | `gravity-time/reports/gt-e4-synthesis.md` |
| What was done, when, with which checks | `gravity-time/provenance/execution-GT-P007.md` |
