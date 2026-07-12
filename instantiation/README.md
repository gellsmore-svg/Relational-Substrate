# Instantiation phase

The conceptual phase (ladder T0–T7, see [`../docs/`](../docs/)) was deliberately
non-numeric. This directory begins the **instantiation phase**: explicit
computations that put the conceptual claims under **parameter-free, could-fail**
numerical test — still forbidding per-case calibration (the D1/D4 discipline).

## Test 1 — the vorton's identity is an integer Hopf number · **PASSED**

`hopf_invariant.py` builds the elementary Hopfion director field *explicitly*
(R³ →[inverse stereographic]→ S³ →[Hopf map]→ S²) and computes its Hopf number by
the Whitehead integral (`F` = pullback flux, `∇×A = F` solved spectrally,
`H = ∫A·F`).

**Claim under test:** the vorton's topological identity (π₃) is the *integer* 1
and — being topological — **independent of the configuration's physical size** (no
tuned parameter).

**Result** (grid 128³, box L=16):

```
H = 0.9998   → integer 1
scale-independent to < 0.001 across sizes 0.8–1.25
```

**PASS.** The identity is real, computes to the integer, and is parameter-free.
The residual 2×10⁻⁴ is pure discretisation; a small-box run gives ~0.987 *falling*
with size — a finite-box boundary artifact, **not** a topological effect (which is
itself a nice confirmation: the deviation behaves like a boundary error, not like
a real dependence).

### What this does and does not establish

- **Does:** the vorton's *topological identity* is a genuine, computable integer
  invariant, parameter-free — the first computational anchor beneath the
  conceptual chain.
- **Does not:** validate the physics chain (fermion / charge / EM / atoms) — those
  remain conceptual/pending. This is one narrow, clean rung. Empirical-correctness
  confidence stays capped (see
  [`../docs/conceptual-phase-completion-2026-07-12.md`](../docs/conceptual-phase-completion-2026-07-12.md) §4).

## Test 2 — the π₂–π₃ selection rule `H = p·q` · **PASSED**

`selection_rule.py` builds the **type-(p,q) Hopfion** (`w = Z₁ᵖ / Z₂q`, director by
inverse stereographic projection) — two winding numbers playing the roles of
skyrmion charge and internal twist — and computes its Hopf number with the same
verified routine. Claim: `H = p·q`.

**Result** (grid 128³, box L=16):

```
(p,q)   p·q   H
(1,1)    1    0.9998
(2,1)    2    2.0000
(1,2)    2    1.9995
(2,2)    4    3.9995
(3,1)    3    3.0000
(2,3)    6    5.9906
```

**PASS** — `H = p·q` holds parameter-free across the family. The `(2,3)` case
(5.99) shows the expected mild discretisation error at higher charge, still
rounding to 6. This confirms the **species-lattice arithmetic** — the quadratic
combination rule underpinning the particle inventory — is real and computable, not
merely asserted.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python hopf_invariant.py
```

## Next instantiation tests

1. **The emergent magnetic sector** — confirm a hedgehog carries emergent flux
   (the skyrmion density integrates to its charge).
2. *(Hardest, instantiation-level conditional)* whether **θ=π is generated**, not
   inserted — the assumption behind the charge-quantisation and fermion results.
