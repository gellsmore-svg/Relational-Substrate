# RS re-anchoring — Decision Log

A chronological, ADR-lite record of the decisions taken in the 2026-07
re-anchoring of the RS modelling programme. Each entry: **context → decision →
rationale → consequences → status**, with a pointer to where it is worked. This
log is the single source of truth for *what was decided and why*; the scaffold's
[containment ledger](coherence-topology-scaffold-2026-07-11.md#6-containment-ledger-living)
is the single source of truth for *what has been contained/correlated*.

---

### D1 — The original experiment drifted from the stated objective · 2026-07-11
- **Context.** The original outcome disappointed; suspicion of a slice-based
  (one-attribute-at-a-time) method.
- **Decision.** Confirmed **objective drift**: the programme began as physics
  unification (EM/Coulomb/optics/molecular benchmarks — see git history + the
  `research/` corpus) and drifted into a stress-history / order-effect
  ("coaxing") resilience programme.
- **Rationale.** The validation doc's own words: on physical observables "the
  grammar is *calibrated*, not used to derive a prediction… consistency at best,
  never novel evidence." The AI then optimised for *a novel null-beating effect*
  instead of the stated *unifying model of the physics*.
- **Consequences.** The stress-history/resilience work is **out of scope**;
  archived, not deleted.
- **Status.** Accepted. Recorded in `vorton-topological-substrate-proposal…` §0.

### D2 — Objective re-locked: the vorton ontology · 2026-07-11
- **Decision.** North star: **a single relational substrate in which the vorton
  (primary topology) is the sole structural primitive**; light/electricity/
  magnetism are downstream Operations A/B/C; E&M complementary. **Success =
  structural reproduction of known physics, not novelty.**
- **Rationale.** This is the stated objective and the books' ontology (RS Ch.13,
  17–19; CBO Ch.5, 8). Serves as the anti-drift anchor.
- **Status.** Accepted. Proposal §1.

### D3 — Substrate anchor corrected: topological-soliton theory, GA demoted · 2026-07-11
- **Context.** Geometric Algebra was first proposed (E&M as one bivector `F`).
- **Decision.** Anchor the **structural** language on **topological-soliton /
  knot-field theory** (Kelvin vortex atom → Skyrme → Hopfion); **demote GA** to
  the *downstream* tier (expressing a vorton's circulation as E/M/light).
- **Rationale (user correction).** In RS *only the vorton is structural*; E/M/
  light are downstream. GA-as-`E+IB` promotes a field description to structural
  rank — it **inverts the hierarchy**. GA is a *local* language; the vorton is a
  *global/topological* fact.
- **Status.** Accepted. Proposal §2.

### D4 — Prior `src/model.js` core retired as the spine · 2026-07-11
- **Decision.** Retire the linear-response affine core (coherence = affine blend
  of sliders; history as ±3–12% nudges).
- **Rationale.** It is a per-case *fitter*, structurally incapable of magnitude or
  topology — the wrong mathematics for topological primitives.
- **Status.** Accepted. Salvage: objective, pre-registration discipline,
  knot-class vocabulary, admissibility walkthroughs.

### D5 — Phase reframed: conceptual, coherence-based, not numeric · 2026-07-11
- **Decision.** This phase produces a **scaffold + guidelines + thought
  experiments**, not code. Method: **strip buried assumptions** from working math,
  keep robust *background-free* patterns, **correlate** patterns across models.
  **Progress = containment, not fit.**
- **Rationale (user framing).** The substrate is non-material (no send/transmit/
  receive), describable only via **coherence**; more information → more coherence
  → more containment → higher likelihood of success.
- **Status.** Accepted. `coherence-topology-scaffold…` §0–§4.

### D6 — Darkness = the substrate at rest (a thing), not an absence · 2026-07-11
- **Decision.** The default topological state is **darkness = the substrate in its
  definite unperturbed rest configuration** (bounded metaphor: a taut trampoline
  skin) — a *thing* that *enables* light (and potentially E&M) to form
  topologically. Not empty; "unrevealed" = at rest / no closure.
- **Rationale (user correction).** Retired the misleading "zero linking"; linking
  only enters at first closure (T2).
- **Status.** Accepted. Scaffold §0, principle 2, T0.

### D7 — T0 carries a rest orientation (director) · 2026-07-11
- **Decision.** The rest state carries a **uniform rest orientation** (a director/
  grain), not a featureless medium.
- **Rationale & consequences.** This **derives** the field type (orientation → a
  sphere of directions = the Faddeev–Niemi/Hopfion field — no longer imported),
  fixes the identity invariants, and **unlocks `Lk = Tw + Wr`**. Correlates with
  the AMS **magnetic constraint geometry** at rest (Axiom M1).
- **Status.** Accepted. Scaffold T0 worked entry.

### D8 — T0 = nematic axis (RP²), 3D bulk · 2026-07-12
- **Context.** Fork: vector (S²) vs nematic (RP²) director.
- **Decision.** **Nematic** (unoriented axis, head ≡ tail), **3D bulk**.
- **Rationale.** By ordered-media defect topology (Mermin, RMP 51 (1979) 591),
  RP² gives a **layered identity** from one grain: **π₁=Z₂ → spin** (half-integer
  disclination = SU(2) double cover), **π₂=Z → charge**, **π₃=Z → the vorton
  (Hopf knot)**. Spin-½ arises *structurally*; an axis is gentler on
  background-independence; the stack aims at atoms. 3D is required for the full π₃
  Hopf identity.
- **Consequence / open debt.** The **sign** of charge (π₂) is gauged by the spin
  disclination (π₁): only **|N|** is invariant (Volovik–Mineev) — spin and
  charge-sign are locked. *(Corrects an earlier loose "mod 2" wording; resolved in
  the shared-budget entry.)*
- **Status.** Accepted. Scaffold T0/T2 entries.

### D9 — Electromagnetism is emergent (B1), not an external field · 2026-07-12
- **Context.** How does the vorton's structure become EM (Maxwell + electric
  charge)? Branches: B1 emergent U(1); B2 external gauged U(1); B3 Hopf/θ term.
- **Decision.** **B1** — EM is the emergent expression of the substrate: the
  director's winding bivector `F = n·(dn∧dn)` = `E + I·B` (GA). **B2 rejected**
  (a second fundamental field violates the one-substrate north star, D2). **B3**
  (the θ/Hopf–Wess–Zumino term) **folds into B1** as part of its effective action.
- **Rationale.** One-substrate forbids external gauging; CP¹ / Mermin–Ho give an
  emergent U(1) with the skyrmion density as flux and spin-½ spinons (matching our
  vorton).
- **Status.** Accepted; crux worked (below).

---

## Standing results (not decisions, but fixed by the above)

- **Correlated core:** identity = conserved self-linkage; **`Lk = Tw + Wr`** splits
  identity into **twist → magnetism (Op C)** and **writhe → electricity (Op B)**;
  two coupled circulations → E&M complementary; **stability = information-driven
  containment**; light = revealing without linking.
- **First pre-registered could-fail test:** charge quantisation as an integer
  Hopf/linking invariant of the vorton; magnetic polarity = sign of the twist.
  Precedent: Skyrme model gives integer baryon number.
- **Shared spin/charge budget — resolved (2026-07-12).** Spin (π₁) **gauges charge
  sign** (only |N| invariant — Volovik–Mineev); the disclination, the vorton's
  framing/twist parity, and the 2π→4π director rotation are **one Z₂**; and by
  **Finkelstein–Rubinstein** (2π rotation = exchange = that Z₂) the vorton is a
  **spin-½ fermion** — so fermionic matter is structurally available, not inserted.
  Corrects D8's "mod 2."
- **π₂–π₃ selection rule — worked (2026-07-12).** The Hopf number is the
  **helicity/self-linking of the charge flux** (`H = ∫A∧F`), so π₃ is a quadratic
  functional of π₂: `H = Σ nᵢmᵢ + Σ 2nᵢnⱼℓᵢⱼ` (self + mutual linking; `H=nm` for
  one tube). Vorton **species live on a discrete lattice** indexed by (charge
  content, linking); spin = framing parity (cross-checked by Wilczek–Zee `θ=π →
  fermion`). **Frontier reached:** net electric charge vs Hopf number are distinct;
  charge assignment needs a **U(1) coupling / Hopf–Wess–Zumino term whose
  coefficient topology does not fix** — the next decision, which re-engages the
  downstream (GA / U(1)_EM) tier of D3.
- **Emergent-EM crux — worked (2026-07-12, D9).** The director gives one emergent
  bivector `F = n·(dn∧dn) = E + I·B` (GA): **B = held twist = skyrmion density**
  (Op C, dissipationless); **E = moving writhe = skyrmion current** (Op B). So
  **T3 and Mermin–Ho are the static/dynamic projections of one `F`** — reconciled.
  **Correction:** π₂ is the emergent **magnetic** flux, *not* electric charge.
  **Upgrade:** `dF=0` (a pullback) gives the homogeneous Maxwell equations for
  free, so **no magnetic monopole and induction (Faraday) are now derived**, not
  suggestive. **Next could-fail test:** the *sourced* equations (Gauss/Ampère) and
  **electric-charge quantisation** come from the θ/Hopf–WZ term and must fall out
  **without calibrating** stiffnesses.
- **Electric-charge test — PASSED (2026-07-12).** Quantisation is derived by two
  coupling-independent routes: **Dirac** (`e·g = 2πn`, forced by the *existence* of
  the emergent π₂ magnetic sector) and **Witten** (`Q = e(n + θm/2π)`, θ fixed to
  the fermion point θ=π → dyon spectrum `Q = e(n + m/2)`). **No stiffness
  calibration.** One θ=π yields spin-½, statistics, *and* the charge shift together.
  **Honest limit:** the absolute unit `e` (α) is the emergent coupling — *not*
  topological; fitting it is forbidden. Conditional (instantiation-level): the
  microscopic generation of θ=π must still be shown. This effectively **closes the
  EM tier** at the structural level.
- **T6 binding — worked (2026-07-12).** Structural reach to atoms: composite
  magnetic & electric charges add and stay quantised (neutral atom = ΣQ=0);
  composite identity carries mutual linking (`H = ΣHᵢ + 2ΣQᵢQⱼℓᵢⱼ` — a topological
  bond); and the derived Fermi statistics force **Pauli exclusion → shell structure
  → the periodic organisation of matter** (chemistry's structure derived, not
  fitted). A binding channel exists structurally (director elasticity + emergent
  EM). **Honest boundary (the old-cycle trap):** binding sign/strength, the mass
  hierarchy (cores vs shells), and energetic stability are magnitudes/dynamics —
  **parked, not fitted.** The **north star is now reached at the structural /
  combinatorial level** across light, E&M, constituents, and atoms; magnitudes
  uniformly out of scope.

## Open decisions (not yet taken)

- **Assembly layer (next frontier).** With the EM tier closed at the structural
  level, the far half of the north star: **binding vortons → atoms/molecules**
  (scaffold T6, secondary topology) and **light–vorton admissibility** (T7).
- **Magnitudes / α (parked).** The absolute couplings (e/α, and any mass ratios)
  are out of scope this phase and not derivable from topology alone; revisit only
  with a rule that forbids per-case calibration.
- Whether the *absolute* rest axis is unobservable (only textures revealed →
  effective isotropy; protects background-independence).
- The quantitative (magnitude) map — deliberately deferred; out of scope this phase.
- When to instantiate numerically (a Hopfion computing the T2 linking invariant
  parameter-free) — only after the ledger is tight enough.
