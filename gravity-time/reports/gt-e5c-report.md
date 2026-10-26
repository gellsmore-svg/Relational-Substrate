# Does renewal last? Post-renewal survival over anchor-local changes (GT-E5C)

*A plain-English report for the human researcher on prompt GT-P011, 15 October 2026.*
- *One frozen round, executed once:*
  - frozen plan `469ee28`, plan_hash `bab7a59d…6e47`;
  - results `5080199`, payload `582e845ba338…`;
  - consulted hub commit `38c2501` (read only).
- *Numbers are exact finite-model computations, not simulations. Tables: `round-e5c-tables.json`; per-row view: `gt-e5c-atlas.md`; definitions and proofs (T12–T15): `docs/e5c-durable-renewal-definitions.md`.*
- *Nothing here is a body, a movement, a physical time or gravity. The anchor (a vertex or link) and its original partners are tracked by the analyst; no rule reads them.*

## The question

E5B found that a pattern held by an anchor sometimes reaches a moment when **none** of the partners it started with takes part ("complete renewal"). It also warned that such renewal might be fleeting: for triangles that start with one completing vertex, a single flicker can produce it.

E5C asks what happens **after the first renewal**. Over the next 1, 2, 4 and 8 changes at the anchor, does the pattern stay true with none of the original partners back? And how does that compare with the three stand-ins (N0, ND, NK)?

Two numbers are kept apart:
- **U_h:** the chance, per episode, of renewing *and then* surviving h anchor changes;
- **C_h:** the chance of surviving h anchor changes *given* that renewal happened.

U can rise just because renewal is reached more often. C can rise just because hard episodes never renew. Neither replaces the other.

## What did we learn?

**1. Renewal rarely lasts.**
- Across every law, conditional survival falls steeply: C_1 is about 0.2–0.5 and C_4 about 0.004–0.14.
- A renewed pattern usually ends within a few anchor changes, either by an original partner coming back or by the pattern dissolving.
- There is no sign of a renewed organisation that maintains itself indefinitely.

**2. CSPH's strong triangle renewal is mostly flicker.**
- CSPH's triangle reaches renewal 2.2–2.6 times as often as NK, and its unconditional durability U_h is ×1.9–×3.0.
- But **once renewed, it survives no better** (C_1 ×0.84–×0.86; C_4 ×1.14–×1.15).
- An original completer comes back before the pattern ends 2.5–3 times as often as under NK (0.31 against 0.13 at N=5; 0.25 against 0.09 at N=6). The very next anchor change brings one back 2.7–3.2 times as often.
- So CSPH renews a lot because its completers flicker in and out. This is account **D2**, flicker-assisted renewal, as E5B suspected.

**3. PATHH's triangle is the one clear case of better survival after renewal.**
- At both sizes, and in both the one-completer and two-completer entry classes, PATHH's renewed triangle outlasts NK's, and the gap widens with more anchor changes: C_4 is 0.055 against 0.026 at N=5 and 0.077 against 0.048 at N=6.
- Original completers come back no more often than under NK (6–7%). Most episodes end by the triangle dissolving, not by a return.
- This is durable renewal relative to the traffic-matched stand-in (**D1, weak form**). It may still come from how PATHH places activity near the anchor, which NK does not match (**D4**).

**4. PATHF's small E5B advantage is short-lived.**
- PATHF "≥2 links" at N=6 reaches renewal more often than NK (×1.32) and survives the first anchor change better (C_1 0.20 against 0.16).
- By four changes survival equals NK's (C_4 0.010 against 0.010), and originals return slightly more often.
- PATHF's triangle is below NK throughout, and increasingly so with more changes (C_4 about half of NK's).

**5. The control families behave like controls, with one surprise.**
- CLOSEW is at or below NK everywhere (C_h ×0.87–×1.01).
- PCOMP is close to NK overall.
- **The surprise:** its triangle episodes that start with two or more completers survive four changes better than NK at both sizes: ×2.2 at N=5 (0.024 against 0.011) and ×1.5 at N=6 (0.033 against 0.022). The absolute values are small. This is a within-crowding-level kinetic effect that E5B's lifetimes did not show.

**6. "≥2 links" cannot survive renewal at all at five vertices.**
- At N=5, a renewed "≥2 links" pattern has exactly two partners, both newcomers. The next anchor change either brings back an original partner or drops a partner and ends the pattern.
- So survival past renewal is **mathematically impossible** (theorem T14), and those cells are labelled as such, not reported as measured zeros. At N=6 it is possible, and it was measured.

**7. Sampling the moment of renewal matters.**
- The state at which renewal first happens is very different from a "typical" renewed state drawn from the long-run picture (L1 distance 0.3–1.7).
- Measuring survival from typical states would have given different answers. All E5C numbers use the actual first-renewal state.

## Answers to the prompt's comparisons

| Comparison | Answer |
| --- | --- |
| Do E5B's positive renewal rows persist to h = 2, 4 under NK? | Unconditionally yes for CSPH and PATHH triangles and PATHF "≥2 links" (N=6). **Conditionally only PATHH's triangle** clearly exceeds NK at h = 2 and 4 at both sizes |
| PATHF F_2PATH in both U_h and C_h at both sizes? | N=5: structurally zero after renewal. N=6: U_h ×1.31–×1.67; C_h ×1.27 at h=1, about ×1 at h = 2–4 |
| CSPH and PATHH triangles after isolating size-1 entries? | Size-1 entries dominate (92–99%). Within size 1: CSPH C_h below NK at h = 1–2 with high return; PATHH above NK. Size ≥ 2 classes agree in direction (PATHH above, CSPH C_1 below) |
| PCOMP and CLOSEW? | CLOSEW at or below NK. PCOMP near NK, except its size-≥2 triangle classes at h = 4 (×2.2 at N=5, ×1.5 at N=6) |
| What NK does not control | Within-layer and anchor-local rate arrangement, shape correlations, multi-time structure. The PATHH and PCOMP-size-≥2 effects may come from these |

## What this does not show

- No self-maintaining organisation: all renewed patterns decay within a few anchor changes.
- No identity of a moving or unlabelled structure: the anchor is fixed by the analyst, and N ≤ 6.
- Nothing about interaction between structures, displacement, acceleration or gravity.
- No independent confirmation: E5C is an adaptive follow-up on laws whose E5A/E5B values were exposed.
- Ratios at h = 4–8 rest on small absolute probabilities (often below 0.01). Treat them as structure, not magnitude.

## Files

`plans/round-e5c-plan.json`, `reports/round-e5c-tables.json`, `reports/gt-e5c-atlas.md`, `reports/gt-e5c-reflection.md`, `docs/e5c-durable-renewal-definitions.md`, `docs/gt-p011-starting-audit.md`, `docs/gt-e5c-cross-programme-transfer.md`, `docs/gt-p011-shared-synthesis-handoff.md`, `provenance/execution-GT-P011.md`.
