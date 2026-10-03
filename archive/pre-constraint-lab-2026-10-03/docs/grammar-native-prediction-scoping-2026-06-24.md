# Scoping: where could the RS grammar give a no-established-competitor prediction?

Date: 2026-06-24

This note answers a strategic question raised after the wollastonite-1A RI consistency
pass and the anisotropy-test analysis: across the whole programme, is there an
observable the RS topology grammar predicts that **no established theory already
covers**, so that a pass would be decisive (not a consistency check)? It asserts no
evidence and changes no confidence. It is a synthesis of what the model actually is.

## 1. The diagnosis: why no novel evidence has appeared

Every domain the programme has tested -- mineral refractive index, molecular geometry,
surface-roughness PSD, peroxide torsion -- shares two properties that make decisive
evidence impossible:

1. The observable is a **static physical property** that a **mature reductionist
   theory already predicts** (Shannon-Fischer polarizability for RI; quantum chemistry
   for geometry/torsion; scalar diffraction / bond-polarizability for scatter). RS can
   at best reproduce these -> a consistency check, never novel evidence. The
   wollastonite-1A pass made this concrete.
2. In these benches the grammar is **calibrated to known data, not used to derive a
   prediction**. The README is explicit: the molecule anchors "calibrate the bench;
   they are not claims derived from the Relational Substrate grammar."

So the programme has been testing a grammar of **relational coherence over a history**
against **static snapshots that established physics already nails**. That mismatch,
not data access alone, is the root cause.

## 2. What the grammar actually, distinctively claims

From `src/model.js` (`calculateOutcome` + `simulateSequence`), the grammar's native,
non-borrowed content is:

> whether a stable identity **survives a sequence of encounters**, where accumulated
> **memory/continuity from the history** modulates survival of the current step
> ("path memory boosts continuity"; "history helps preservation").

This is a **path-dependent (historical) persistence** claim. Static reductionist
theories have no history term and make no such prediction. This is the only place the
grammar speaks where established static theory is silent by construction.

## 3. The grammar's sharp, falsifiable fingerprint: a directional ORDER effect

The decisive consequence of memory carry is **non-commutativity**: the same set of
perturbations applied in a different **order** yields different survival. And the model
fixes the **direction**: history that builds continuity/memory makes identity "more
forgiving," so a **gentle-then-harsh** sequence should survive better than
**harsh-then-gentle** (preconditioning / coaxing).

This is the grammar's unique empirical signature because:

- **static** theories predict no order effect (no history);
- the simplest **established cumulative** baselines (e.g. linear damage / Miner's rule,
  most dose-additivity models) are **order-independent by construction** -- they
  predict the null;
- the grammar predicts a **specific, directional, non-generic** deviation from that
  null (gentle-first protects).

A test of "does order matter, in the predicted direction?" is therefore (a) native to
the grammar, (b) silent for static theory, and (c) a clean contrast against the
standard order-independent baseline.

## 4. Candidate domains (assessed for: grammar-native, weak/absent competitor, data)

| Domain | Order effect real? | Established competitor | Data | Verdict |
|---|---|---|---|---|
| Static physical props (RI, geometry, roughness) | n/a (static) | strong (mature) | varies | reject -- where the programme has been |
| **Metal fatigue under variable-amplitude loading** | yes -- the "coaxing effect" (under-stressing first raises endurance) is documented and **Miner's rule misses it** | order-INDEPENDENT baseline (Miner) is standard and acknowledged inadequate; sophisticated models exist but no consensus | fatigue databases exist | **strongest** -- real order effect, weak standard baseline, data |
| Biological preconditioning / hormesis (stress priming) | yes -- mild-stress-first protects | no clean quantitative predictor | exists but noisy | strong on novelty, hard on attribution |
| Catalyst deactivation / poisoning sequences | yes | kinetic models, partial | exists | medium |
| Reaction-network / autocatalytic closure | grammar-native (closure) but static-ish | RAF theory competes | computational | medium; competitor exists |

## 5. The two preconditions for ANY decisive test

- **P1 (the binding one): sharpen the grammar into a derived, falsifiable, non-generic
  prediction.** Specifically: a quantitative, directional **order/sequence effect** on
  survival that follows from the memory-carry rule and is distinguishable from "any
  sensible robustness heuristic." Without P1, every domain gives either consistency
  (strong-theory domains) or unattributable success (weak-theory domains).
- **P2: a domain where that prediction has no established competitor (or an
  acknowledged-inadequate one) plus accessible data.** Section 4 ranks these; the
  order-independent-baseline domains (fatigue coaxing, biological preconditioning) are
  the openings.

## 6. Honest recommendation and the deeper question

1. **Do P1 before any further domain search.** Derive, from the existing
   `simulateSequence` memory rule, a concrete prediction of the form: "for survival
   under a sequence of N perturbations of fixed total severity, gentle-first ordering
   survives longer than harsh-first by an amount that scales with [a named grammar
   quantity]." This is internal work, needs no external data, and is the grammar's one
   genuinely distinctive falsifiable claim.
2. **Then test the order effect** where the standard baseline is order-independent and
   known to fail -- fatigue coaxing is the prime candidate (real effect, weak baseline,
   data), biological preconditioning the cross-domain second.
3. **Confront the lens-vs-predictor question.** If the grammar cannot be sharpened to a
   derived, non-generic order-effect prediction (P1), then it is best understood as a
   **conceptual lens** -- valuable for organising and explaining coherence phenomena --
   rather than a predictive theory with decisive empirical tests. That is not failure;
   many useful frameworks are lenses. But it changes the success criterion, and the
   programme should choose deliberately: pursue the order-effect prediction (the only
   route to decisive evidence) or reframe the grammar's contribution as explanatory.

## P1 done (same day): the order effect is real in the model — with a crucial endpoint refinement

`analysis/grammar-order-effect-derivation.mjs` (`npm run grammar:order-effect`) drove
`simulateSequence` with reversed regime schedules (gentle = recovering, harsh =
stressed) at matched multisets across 192 configs. Result:

- **Final-state endpoint (residual identity): RECENCY**, not preconditioning. Ending on
  a gentle encounter wins in 100% of configs (mean delta -0.009). Recency is not a
  distinctive no-competitor claim.
- **Whole-history endpoint (minimum identity / did it ever break): PRECONDITIONING
  holds.** Gentle-first holds a higher minimum in 95.8% of configs, with 11 whole-history
  survival flips (gentle-first survives the whole run, harsh-first breaks) and **zero in
  reverse**.

So the grammar's distinctive prediction is real in the model, but **only on a
whole-history survival endpoint**. This sharpens P2 decisively: a real-world test must
measure **time/cycles-to-first-failure** under gentle-first vs harsh-first blocks
(fatigue: cycles-to-first-crack; biology: survival under stress-then-stressor) -- NOT a
final-state endpoint like residual strength, which the model says is recency-dominated
and would show the *opposite* sign. (Derived from a toy rule model: this shows the claim
is internally real and which endpoint reveals it, not that it is physically true.)

## Resolution (2026-06-25): the lens-vs-predictor question is answered — LENS (for magnitude)

The full P2 test ran and the magnitude test settled it (`npm run grammar:order-effect-magnitude`):

- **Direction: corroborated on real data, both sides.** On the Ti-6Al-4V ELI fatigue
  data (validated S-N), gentle-first gives Miner sum D>1 (3/3) and harsh-first D<1
  (3/4); matched pair D(L-H)=1.72 > 1 > D(H-L)=0.82. The grammar beats the
  order-independent Miner null in its pre-registered direction. This is the first
  real-data corroboration of a distinctive RS-grammar prediction.
- **Magnitude: NOT predicted parameter-free.** Survival under repeated load in the
  model is BINARY (lives 0 or the full horizon; no intermediate), so the grammar has
  no intrinsic cycles-to-failure magnitude. Its order effect is a near-threshold sign
  flip (~6% of marginal configs; ~0.007 min-identity shift). The fatigue magnitude
  (D-ratio ~2.1, coaxing up to ~2.5x life) would be supplied entirely by the free
  amplitude->regime / block->steps mapping. With a calibration that supplies the whole
  effect size, the grammar is indistinguishable from a fitted nonlinear-damage model.

So the grammar is a **directional / conceptual lens** for the order effect, not a
quantitative predictor: it earns genuine directional corroboration but does not beat
established nonlinear cumulative-damage models on magnitude. The unification thesis
stands as coherent and directionally suggestive; confidence stays capped. This is the
honest ceiling of the order-effect arc.

**Graded-survival re-test (2026-06-25), the fair check.** To rule out that the lens
verdict was merely an artifact of the model's BINARY survival, a graded survival
dynamic was added as a readout (per-step damage = 1 - coherenceMetric, capacity-
normalized; `src/model.js` unchanged; no tunable fit parameters) and the magnitude test
re-run (`npm run grammar:graded-survival-magnitude`). Result: with the graded dynamic
the grammar DOES produce a coaxing magnitude in the right direction (coaxing-vs-linear
~1.02-1.07, robust across the capacity normalization), but it is ~30-50x too small
versus the fatigue effect (real coaxing ~100-200% above linear; grammar ~2-7%). The
shortfall is fundamental: the model's memory coefficients (~10%) are far weaker than a
fatigue-scale effect, and closing the gap requires amplifying them (a calibration, not
a derivation). So the lens verdict is NOT a binary-survival artifact; it holds with a
graded dynamic. The grammar is a directional/conceptual lens for this effect, full
stop.

## One-line summary

The grammar's only no-established-competitor prediction is its **directional order
effect on identity survival** (gentle-first protects), because static theories have no
history and the standard cumulative baselines are order-independent; the programme's
next decisive step is to **derive that order effect from the model** (P1) and test it
where order-independent baselines are known to fail (fatigue coaxing, biological
preconditioning) -- or else accept the grammar as a conceptual lens.
