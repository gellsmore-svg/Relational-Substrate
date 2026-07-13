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

## Test 3 — the emergent magnetic sector · **PASSED**

`emergent_magnetic.py` tests the Mermin–Ho identification the whole EM tier rests
on — `b_i = (1/8π) ε_ijk n·(∂_j n × ∂_k n)` is the emergent magnetic field, whose
flux equals the enclosed topological charge — in two halves:

**(a) a hedgehog (singular, degree q) is an emergent monopole** — box flux `∮b·dS`:

```
q=1 → 1.017    q=2 → 2.033    q=3 → 3.047   (expect q)
```

**(b) a smooth Hopfion carries no net monopole** — flux `= -0.00000` (expect 0).

**PASS.** So `π₂ density = emergent magnetic flux` (a hedgehog carries flux equal
to its charge = an emergent monopole), while a *smooth* texture carries none —
computationally confirming the crux's **"no magnetic monopole for smooth vortons;
a monopole requires a singular hedgehog"** (and hence the premise of the Dirac
charge-quantisation argument). The ~2–5% excess in (a) is finite-difference
discretisation at the box faces (rounds to the integer); (b) is exact to five
decimals.

## Test 4 — WP-B: a Dirac fermion in the hedgehog → Jackiw–Rebbi zero mode · **PASSED (mechanism)**

`hedgehog_dirac.py` builds an 8-band Wilson–Dirac fermion with a genuine degree-1
**hedgehog mass** (the same `r̂` field as test 3) and diagonalises it (dense, N=8),
scanning the Wilson parameter `M`. Jackiw–Rebbi: a *single* Dirac cone in a
degree-1 hedgehog binds **exactly one zero mode** → induced charge ½ = the θ=π
Witten half-charge (see [`../docs/theta-generation-scope-2026-07-13.md`](../docs/theta-generation-scope-2026-07-13.md)).

**Result** (grid 8³):

```
M=1.0  → 1 core zero mode, |E|=0.023, gap 0.215   (topological)
M=1.5  → 0 zero modes                             (trivial)
M=2.0  → 0 zero modes                             (trivial)
M=2.5  → 1 core zero mode, |E|=0.027, gap 0.798   (topological, cleanest)
M=3.0  → none clean
```

In the **topological windows** the hedgehog binds **one** mid-gap mode, localized
at the core (≈79% within R/4, peak at the centre); in the trivial windows it binds
none. **PASS** — a single Dirac cone in the hedgehog (emergent-monopole) background
realises the Jackiw–Rebbi ½, i.e. the θ=π mechanism, computed and could-fail.

### What this does and does not establish (honest)

- **Does:** the *mechanism* is real and computable — an odd (single) Dirac cone in
  the hedgehog gives induced charge ½ = θ=π (Abanov–Wiegmann N=1). Trivial regimes
  binding no mode is a correct control.
- **Does not:** settle **WP-A** — whether the *substrate itself* provides exactly
  one such Dirac fermion (the CP¹-spinon parity). Here the single fermion was put
  in **by hand**; θ=π is shown to *follow from* an odd Dirac sector, not yet shown
  to be *forced/intrinsic*. So the θ=π conditional is now **mechanism-verified,
  origin-open** — a partial advance, not full closure (scope §5, "PARTIAL").
- **Finite size:** N=8 shifts the topological windows and leaves the modes
  near-zero (0.02–0.03) rather than exactly zero; larger N would sharpen. The
  qualitative JR signature (one core mode in topological windows, none in trivial)
  is robust.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python hopf_invariant.py
```

## Next instantiation tests

1. **WP-A** — whether θ=π is *forced/intrinsic* (does the substrate's own CP¹ spinon
   supply exactly one Dirac fermion?). WP-B verified the *mechanism*; WP-A is the
   *origin*, and is research-scale (an induced-term / spectral-asymmetry derivation),
   with genuinely wider uncertainty. See the θ-generation scope.
