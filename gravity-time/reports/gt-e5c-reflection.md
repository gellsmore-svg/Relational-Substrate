# GT-E5C reflection: durability, flicker, and what NK leaves open

*GT-P011, 15 October 2026. Frozen plan `469ee28`; results `5080199`; hub consulted `38c2501`. Labels: [O] observed; [T] theorem; [I] inference after results; [L] limitation. Nothing here is physical.*

## 1. The accounts, family by family (comparator NK unless stated)

| Family | Pattern | Verdict | Accounts |
| --- | --- | --- | --- |
| CSPH | F_TRI | [O] R0 ×2.2–2.6 and U_h ×1.9–3.0, but C_1 ×0.84–0.86; original return before exit about 2.5–3× NK; immediate original return about 2.7–3.2× | **D2** flicker-assisted renewal (E5B's caution confirmed) |
| PATHH | F_TRI | [O] C_h above NK at both sizes, growing with h (C_4 ×2.1, ×1.6), in both entry classes; return at NK's level; exits dominate | **D1 (weak)**, or **D4** (local kinetics NK does not match) |
| PATHF | F_2PATH, N=6 | [O] U_h ×1.3–1.7 (from R0), C_1 ×1.27, C_2–C_4 ≈ 1; more returns | short-lived; **D3/D5** beyond one step |
| PATHF | F_TRI | [O] below NK in R0, U_h and C_h, worsening with h | negative |
| PATHH | F_2PATH, N=6 | [O] U_h ×0.75–0.87; C_h about 1 | near-control |
| CSPH | F_2PATH, N=6 | [O] C_1, C_2 ×0.93; C_4 ×1.45 (small absolute values) | **D6**-like sign change across horizon; small numbers |
| CLOSEW | both | [O] at or below NK (C ×0.87–1.01) | **D3** |
| PCOMP | F_2PATH, N=6 | [O] ≈ NK at h ≤ 2, C_4 ×1.36 (absolute 0.004) | near-control |
| PCOMP | F_TRI, size ≥ 2 | [O] C_4 ×2.2 (N=5), ×1.5 (N=6); pooled C close to NK | **D4/D5**: a within-layer effect visible only within classes |
| all | F_2PATH, N=5 | [T] post-renewal survival structurally zero (T14) | **D7** structural |

## 2. Negative and qualifying results

- [T] F_2PATH at N=5 cannot survive any anchor-local event after renewal (T14). The renewal R0 there is real; durability is undefined.
- [O] No law shows sustained post-renewal survival: C_8 is small everywhere. Durability is a matter of a few anchor events.
- [O] CSPH's E5B renewal advantage does not translate into survival.
- [O] PATHF's E5B centre advantage fades after one anchor event.
- [O] The first-renewal law differs strongly from the stationary law restricted to the renewed states (L1 0.3–1.7). A stationary-sampled durability would have been biased.
- [L] At h ≥ 4 the absolute probabilities are mostly below 0.02, so ratios there are fragile as magnitudes.

## 3. Methodological lessons

1. **Separate "reaching renewal" from "surviving it".** The unconditional U_h for CSPH looked like strong durability; C_h and the return/exit split showed it is renewal frequency plus flicker.
2. **First-hit conditioning is essential.** It changes the starting distribution substantially.
3. **Structural feasibility applies after renewal too (T14),** not only to renewal itself (T10).
4. **Within-class durability can reveal kinetic structure** (PCOMP size ≥ 2) that pooled lifetimes and pooled durability hide.

## 4. Lens B (mathematical capability)

The grammar produces post-renewal survival that exceeds a layer-traffic-matched control for one family (PATHH triangles). It produces renewal that is mostly flicker for another (CSPH). In every law, survival decays within a few anchor events. Each quantity is an exact hitting or resolvent functional with a read-only observer.

## 5. Lens A (foundational bridge)

- **Clearer:** a self-maintaining replacement-based organisation is *not* produced by these laws at N ≤ 6. Renewed configurations are transient. One family shows modest durable renewal relative to NK, and its source (local kinetics or organisation) is unresolved.
- **Still undefined:** an unlabelled or mobile reference, interaction between organisations, relative displacement, acceleration, any gravity-like reading.
- **Bridge-map change:** "identity through change" moves from *defined, partially observed* to *defined, durability measured: transient, with one qualified durable case*.

## 6. Cross-programme notes (handoff only; no CL edits)

- **XQ::04.** Durability is a trajectory observable with no history axis. With the return/exit split it **does** separate reconstruction from flicker (CSPH against PATHH).
- **XQ::07.** E5C quantities are resolvent and stopping-set functionals: first hitting, then powers of a local-event kernel. CL 8O derived a Markovization-stopping defect factorization on its side (pinned only after a hub review). Both now use resolvent and stopping language. No common theorem is shown here.
- **XQ::01.** NK leaves within-layer and anchor-local arrangement unmatched; the PATHH and PCOMP-size-≥2 effects sit exactly there.
- **XQ::03.** Anchor-local counts integrate remote events through K. They are not a time change hiding events.

## 7. Next options (not executed)

| Option | Decides | Cost | Risk |
| --- | --- | --- | --- |
| A. An anchor-local kinetic comparator (match the joint law of k and the anchor's local degree or local rate) applied to PATHH triangles and PCOMP size ≥ 2 | whether the remaining durable effects are local kinetics (D4) or organisation (D1) | a new comparator with proofs; minutes to run | moderate: a comparator can be fitted to an effect; must be frozen from first principles |
| B. An unlabelled-identity feasibility design: define a persistence notion that tracks a pattern without a fixed anchor, and prove what N ≤ 6 permits | whether any notion of mobile identity is even definable here | definitions first; possibly no experiment | may conclude "not definable at N ≤ 6" (still informative) |
| C. Principled pause: consolidate E5A–E5C and wait for hub review and a CL comparison | — | none | leaves D1 against D4 open |

**Recommendation: A**, if the author wants the PATHH question settled; otherwise **C**. B is valuable but conceptually earlier, and should come after the hub's comparison on XQ::04/XQ::07. None is chosen for looking gravity-like, and none is run.
