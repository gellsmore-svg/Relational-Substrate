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
  Corrects D8's "mod 2." **Next thread:** π₂–π₃ selection rule (Hopf number ↔
  spin-parity, |charge|) → a *spectrum of vorton species* (particle inventory).

## Open decisions (not yet taken)

- Whether the *absolute* rest axis is unobservable (only textures revealed →
  effective isotropy; protects background-independence).
- The quantitative (magnitude) map — deliberately deferred; out of scope this phase.
- When to instantiate numerically (a Hopfion computing the T2 linking invariant
  parameter-free) — only after the ledger is tight enough.
