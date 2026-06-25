# Relational Substrate — validation status (the lens framing)

Canonical statement of what the Relational Substrate (RS) modelling programme has and
has not established empirically. Adopted 2026-06-25. This supersedes any reading of the
programme as a validated quantitative theory; it does not change any confidence number.

## The one-line standing

**The RS grammar is a coherent, directional / conceptual LENS — not a quantitative
predictor.** It organises coherence phenomena and predicts the *direction* of effects
across domains; it does not, on current evidence, beat established domain theories on
*magnitude*. One distinctive, pre-registered RS prediction has been corroborated on real
data (direction only). Confidence stays capped; the unification thesis is **coherent and
directionally corroborated, not quantitatively validated.**

## How the programme reached this (the evidence)

1. **Diagnosis of why novel evidence never appeared** (`docs/information-limitation-assessment-2026-06-24.md`).
   The programme repeatedly tested a grammar of *relational coherence over a history*
   against *static* physical observables (refractive index, molecular geometry, surface
   roughness, peroxide torsion) that mature reductionist theory already predicts. On
   those benches the grammar is *calibrated*, not used to derive a prediction. Result:
   consistency at best, never novel evidence — and most tracks are also blocked by a
   field-wide data-access wall (identity-locked held-out data is rarely published in
   numerically extractable form).

2. **Refractive index, tested to completion.** A full source-locked predictor was built
   and a fresh held-out mineral (wollastonite-1A) scored cleanly (|n_struct − n_meas| ≈
   0.003, beating a structure-blind control). But the predictor *is* the established
   Shannon–Fischer 2016 method, so the pass is **consistency with established crystal
   chemistry, not independent evidence** for the topology grammar. RI is effectively a
   *closed* domain for novel RS evidence (even its only SF2016-independent opening,
   optical anisotropy, competes with the established bond-polarizability model). See the
   `ri-*` artifacts and `ri-anisotropy-topology-test-design.mjs`.

3. **The grammar's one distinctive claim** (`docs/grammar-native-prediction-scoping-2026-06-24.md`).
   Its non-borrowed content (from `src/model.js` `simulateSequence` + memory carry) is
   *path-dependent identity persistence*: a directional **order effect** — gentle-first
   ("coaxing") protects whole-history survival — which static theories and the
   order-*independent* cumulative baselines (Miner's rule) cannot predict.

4. **The order effect, derived and then tested on real data.**
   - P1 (`grammar-order-effect-derivation.mjs`): the model produces the effect, but only
     on a *whole-history* endpoint (a final-state endpoint is recency-dominated and flips
     the sign).
   - P2 (`grammar-order-effect-fatigue-*.mjs`): on open CC0 Ti-6Al-4V ELI fatigue data
     with independently-validated S-N, gentle-first gives Miner sum D>1 (3/3) and
     harsh-first D<1 (3/4); matched pair D(L-H)=1.72 > 1 > D(H-L)=0.82. **The grammar's
     pre-registered direction beats the order-independent Miner null, both-sided.** This
     is the first real-data corroboration of a distinctive RS prediction.
   - Magnitude (`grammar-order-effect-magnitude-test.mjs` and
     `grammar-graded-survival-magnitude-test.mjs`): the grammar predicts the *direction*
     parameter-free but not the *magnitude*. With binary survival it has no magnitude at
     all; given a graded survival dynamic (no fitted parameters) it produces coaxing
     ~30–50× too small versus the real effect. Matching the magnitude needs amplifying
     the model's memory coefficients — a calibration, not a derivation. So established
     nonlinear cumulative-damage models still win on magnitude.
   - Cross-domain reach (`grammar-order-effect-crossdomain-scoping.mjs`): the *same*
     pre-registered directional law is corroborated in a **second, unconnected domain** —
     cardiac ischemic preconditioning, where open-access meta-analytic data (785
     comparisons) shows mild-first preconditioning reduces infarct size by ~24.6%, with
     the order-specificity (preconditioning > postconditioning) matching too. Materials
     fatigue and cardiac ischemia have no connecting established theory, so this is the
     unification thesis's one no-established-competitor space: the grammar predicts the
     same directional order effect in both. It is **directional reach, not decisive** — a
     skeptic can note that any memory/adaptive system shows preconditioning — but it is
     the strongest honest support the unification-as-lens framing can have, and it does
     not change the magnitude verdict or raise confidence. The domains are recorded side
     by side in a single auditable cross-domain directional ledger
     (generator `grammar-two-domain-directional-ledger.mjs`; rendered table:
     [`docs/cross-domain-directional-ledger.md`](cross-domain-directional-ledger.md)):
     one pre-registered law, confirmed in
     **10/10 entries across four domains** with no connecting established theory,
     different underlying mechanisms, and even different endpoint *types* — materials
     fatigue (4/4; microstructural; cycles-to-failure), cardiac ischemia (3/3; cellular
     signalling; infarct size, −24.6%), wildfire ecology (2/2; landscape fuel depletion;
     prescribed fire reduces subsequent severity 62–72%), and behavioral resilience (1/1;
     psychological coping; stress-inoculation reduces anxiety / enhances performance under
     a later stressor across 37 studies, 1837 participants) — the order-independent null
     rejected in all four, with a recurring requirement that the gentle/mild step come
     first. The mechanistic/endpoint disanalogy is the point: one shared *direction*, not
     one shared mechanism.

## What "lens" means as the success criterion

A lens is a framework that **organises and directionally predicts** phenomena across
domains, earning its keep by clarity and reach rather than by beating established
quantitative models. Under this criterion the RS programme's contribution is:

- a single, transferable grammar (route, closure, phase, charge, continuity + memory)
  that gives a consistent *qualitative/directional* account across molecular, material,
  optical, and interface orderings;
- one genuine, pre-registered, cross-domain **directional** empirical corroboration (the
  fatigue order effect) on record;
- a rigorously honest map of where it does *not* add quantitative value (RI = established
  chemistry; magnitude of the order effect = established damage models).

It is **not**: a validated quantitative predictor, a replacement for domain theories, or
grounds to raise the confidence metrics. Those remain capped.

## What would change the verdict

A domain where the RS grammar makes a **graded** (not threshold) prediction that (a) no
established theory already covers and (b) has accessible identity-locked data. The arc so
far suggests this is hard: mature theory and the data wall recur, and the model's
intrinsic effects are small. Until such a case is found and passes, the lens framing is
the honest standing.

## Pointers

- Confidence (held): inferential convergence 5.6, cross-domain 5.2, unification thesis
  4.8 (cap 6.25). Audit with `npm run reports` then `npm run evidence:ledger`.
- Full chronological state and next moves: `.restart.md`.
- The conceptual framework itself (the books in `books/`) is unaffected by this status;
  this note concerns the empirical/modelling *validation* layer only.
