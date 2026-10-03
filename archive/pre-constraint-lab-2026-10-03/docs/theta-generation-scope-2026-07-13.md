# Scoping: is θ=π *generated*, not inserted?

**Date:** 2026-07-13 · **Status:** scope / plan only (no implementation). The last
instantiation-level conditional behind the conceptual chain.

## 1. What rests on this, and the precise claim

Two conceptual-phase results leaned on **θ=π**:

- the vorton is a **spin-½ fermion** (Finkelstein–Rubinstein / Wilczek–Zee: θ=π is
  the fermion point);
- **electric-charge quantisation** via the Witten effect `Q = e(n + θm/2π)`, whose
  dyon spectrum `Q = e(n + m/2)` uses θ=π.

**The conditional:** is θ=π *forced by the substrate*, or a free input we chose to
match the fermion requirement? If forced → those results are genuinely derived; if
it must be inserted → they are assumptions. This scoping asks what it would take to
settle that, honestly including the ways it can fail.

## 2. The mechanism (established)

A topological θ-term acquires a *definite, quantised* coefficient by **integrating
out a gapped fermionic sector coupled to the order parameter**. The rigorous
template is **Abanov–Wiegmann** (*Nucl. Phys. B* 570 (2000) 685,
[hep-th/9911025](https://arxiv.org/abs/hep-th/9911025)): integrating out `N` Dirac
fermions gapped by the sigma-model field yields **Θ = Nπ**. So:

> **θ=π ⟺ an *odd* number of Dirac fermions in the microscopic sector.**

This is the same physics as a topological-insulator surface (a single Dirac cone →
θ=π magnetoelectric response) and, in a monopole background, the **Jackiw–Rebbi**
zero mode → induced charge **±½** (*Phys. Rev. D* 13 (1976) 3398) — i.e. the θ=π
Witten half-charge. The coefficient is a **spectral-asymmetry index** of the Dirac
operator: quantised, not tunable. That is exactly the property we need — *if* the
right fermion exists.

## 3. The pivotal fork (and the one-substrate tension)

Two honest sub-questions decide everything:

**(a) Is θ=π already the same Z₂ we have, or independent?** The vorton's fermionic
character came from `π₁(RP²)=Z₂` (FR / Volovik–Mineev). θ=π is *also* a Z₂ (mod 2π)
statement. If these are the **same** topological fact, θ=π is near-automatic given
the nematic grain (and tests 1–3 + FR essentially settle it). If **independent**,
θ=π needs its own microscopic origin (a Dirac sector). Distinguishing these is the
first task — and the answer is not obvious.

**(b) Does the substrate *provide* the fermion, or must one be *added*?** Abanov–
Wiegmann needs a Dirac fermion to integrate out. Two routes:

- **Intrinsic (one-substrate-respecting, the target).** The fermion is the
  substrate's **own emergent excitation** — e.g. the **CP¹ spinon** (`n = z†σz`,
  with `z` a fractionalised excitation of the director). If the substrate's spinon
  sector is a *single Dirac* fermion, integrating it out gives θ=π with **no new
  fundamental field**. This connects to real physics (deconfined criticality,
  θ-terms in quantum antiferromagnets).
- **Added (ontology cost).** Postulating a separate fundamental fermion generates θ
  but introduces a **second fundamental field**, straining "one substrate" (D2).
  Acceptable only as a fallback, and it would *downgrade* the north-star claim.

**The crux:** does the nematic RP²/3D substrate yield an *odd, intrinsic* Dirac
sector? Plausible, not guaranteed.

## 4. Work packages

**WP-A — analytic (the real derivation).** Carry out the Abanov–Wiegmann gradient
expansion for a Dirac fermion gapped by the RP²/3D director; show the induced term
is Θ=Nπ and **identify N from the substrate's own content** (ideally the CP¹
spinon). Deliverable: θ=Nπ with N fixed intrinsically. *Pen-and-paper + symbolic
(sympy); research-scale; genuine uncertainty.*

**WP-B — numeric could-fail check (buildable now, extends test 3).** Put a lattice
Dirac operator in the **hedgehog background already constructed in
`instantiation/emergent_magnetic.py`**, diagonalise, and check for the **Jackiw–
Rebbi zero mode → induced charge ½**. A clean, falsifiable test that a *single*
Dirac fermion in the emergent-monopole background realises the θ=π half-charge.
Deliverable: induced charge ≈ ½ (PASS) or not (FAIL). *~150–250 lines; one session;
builds directly on test 3.*

Recommended order: **WP-B first** (concrete, could-fail, reuses test 3), then WP-A
to establish whether N is *forced* intrinsically.

## 5. Pre-registered criteria + anti-drift guard

- **PASS.** An intrinsic (substrate-emergent) **odd** Dirac sector is identified,
  and WP-B yields induced charge ½ → **θ=π is generated, not inserted**; the fermion
  and charge-quantisation results become fully derived.
- **PARTIAL.** θ=Nπ is generated but the parity `N` is an *input* not forced by the
  substrate → θ=π is a **motivated choice, not forced**; the dependent results are
  honestly downgraded from "derived" to "derived given one input."
- **FAIL / STALL.** No consistent intrinsic fermion sector, or the induced term is
  θ=0/2π (boson) → the fermion + charge results **lose their structural footing**,
  putting them in tension with the FR-derived fermion and forcing a rethink.

**Anti-drift guard (critical).** `N` must be **fixed by the substrate's field
content**, never tuned to land on π. If we ever find ourselves choosing N=1
*because we need θ=π*, that is calibration — forbidden (D1/D4). The entire value of
this step is that N is *forced*.

## 6. Honest risk assessment

Unlike tests 1–3 — pure topology, guaranteed to pass if the math is right — **this
step can genuinely fail to resolve.** Three realistic outcomes: (i) θ=π forced
intrinsically (a real capstone); (ii) θ=π requires an added or input ingredient
(partial, with an ontology or honesty cost); (iii) ambiguous — the substrate's
fermion content isn't cleanly defined without further modelling choices (a stall).
All three are acceptable *outcomes*; only pretending (i) when we have (ii)/(iii)
would be drift.

This is also where the program stops being "compute an invariant of a given field"
and becomes "posit dynamics and integrate out matter" — a materially larger,
more open-ended kind of step, with correspondingly wider error bars.

## 7. What I'd need to proceed

- **For WP-B:** nothing new — extend `emergent_magnetic.py` with a lattice Dirac
  operator in the hedgehog background (numpy/scipy sparse eigensolver).
- **For WP-A:** a decision on the microscopic ansatz for the substrate's fermionic
  excitation (CP¹ spinon is the recommended, one-substrate-respecting candidate),
  then the induced-term calculation.

Recommendation: if pursued, do **WP-B** as the next concrete increment (it is
could-fail and reuses existing code), and treat **WP-A** as a separate,
research-scale undertaking with explicitly wider uncertainty.

**Sources:** [Abanov–Wiegmann, θ-terms in NLSMs (arXiv hep-th/9911025)](https://arxiv.org/abs/hep-th/9911025) ·
Jackiw–Rebbi, *Phys. Rev. D* 13 (1976) 3398 (fermion fractionalisation / zero mode
in a monopole background).
