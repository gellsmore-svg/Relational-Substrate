# GT-E5D reflection: what the local/remote traffic match explains, and what it does not

*GT-P012, 15 October 2026. Frozen plan `c74d896`; results `6749346`; hub `38c2501`. Labels: [T] theorem; [O] observation; [I] post hoc interpretation; [C] conjecture; [N] null. Nothing here is physical.*

## 1. Theorems (held in every cell)

- [T] **T16–T19.** π_NL is stationary from macro-flux conservation alone; NL matches every ordered (ℓ,r) flux; it is unique among pool-exchangeable lifts; it is reversible iff no macro current exists.
- [T] **NL ⊇ NK.** Every adjacent edge-count flux is a sum of macro fluxes, so NL matches everything NK matches.

## 2. Observations

- [O] **Projected circulation.**
  - PATHF, PATHH and CSPH carry net (ℓ,r) currents of 0.43–0.98 relative, so NL is non-reversible for them.
  - CLOSEW and PCOMP carry none (≤ 4×10⁻¹³), so NL is reversible for them.
- [O] **PATHH F_TRI.**
  - C_h exceeds NL at both sizes, growing with h: C_4 ×1.99 / ×1.44, C_8 ×3.7 / ×2.0.
  - The excess holds in size 1 and size 2; original return before exit is at or below NL's level (about 6–10%).
- [O] **PCOMP F_TRI, size ≥ 2.** C_4 ×2.2 (N5, s=2) and ×2.35 (N6, s=3) against NL. Pooled values are near control.
- [O] **PATHF F_2PATH N6.** The R0 and C_1 excess over NK (×1.32, ×1.27) vanishes against NL (×1.00, ×1.01).
- [O] **CSPH F_TRI.**
  - NL removes part of the renewal excess: R0 goes from ×2.24 / ×2.62 against NK to ×1.97 / ×2.12 against NL.
  - C_1 stays below NL; returns before exit are 2.1–2.4× NL's.
- [N] **PATHF F_TRI** is below every comparator. **CLOSEW** and **PCOMP pooled** are near control.

## 3. The accounts

| Account | Status after E5D |
| --- | --- |
| D1 residual beyond NL | supported for PATHH triangle (both sizes and classes) and PCOMP size ≥ 2, *relative to this projection only* |
| D2 local/remote traffic | supported for PATHF "≥2 links": E5B/E5C's PATHF centre effect is traffic |
| D3 within-cell configuration | [I] the most economical reading of the PATHH and PCOMP residuals: completer arrangement and within-cell rates (PCOMP within-cell CV up to 0.67), which NL cannot see |
| D4 flicker or composition | CSPH remains flicker-assisted; PATHH and PCOMP are not flicker (returns at NL's level) |
| D5 null or reversal | CSPH "≥2 links" sign change across h; CLOSEW control; PATHF triangle negative |
| D6 projection circulation | present for PATH and CSPH, absent for PCOMP. NL preserves it. Circulation is not what makes PATHH durable: NL, with the same circulation, does not reproduce it |

[I] D1 and D3 cannot be separated by E5D. Telling "organisation" from "within-cell arrangement" would need a finer projection, whose design risks fitting the effect.

## 4. What became clearer, what weakened

- **Clearer:** PATHF's long-standing small centre advantage is a traffic-placement effect. PATHH's triangle durability is the one residual in GT that survives density, layer traffic, local/remote traffic and flicker controls.
- **Weakened:** any reading of PATHF centres as organisation.
- **Open:** what in PATHH's triangle arrangement (or rate placement within a cell) sustains survival; and whether PCOMP's class residual has the same source.

## 5. Lens A and Lens B

- **Lens B:** the grammar can produce post-renewal durability that no projection matched so far (k, then (ℓ,r)) reproduces, for a non-reversible family. That is a mathematical fact about these generators.
- **Lens A:** a candidate prerequisite is sharper: *configuration-dependent survival beyond traffic*. Still absent:
  - an unlabelled reference;
  - interaction;
  - displacement and acceleration;
  - any physical comparison.

  Renewal remains transient.

## 6. Next bounded question (not executed)

**Completer-resolved projection for PATHH (and PCOMP size ≥ 2).** Add the number of current completers to the projection, z = (ℓ, r, c). Ask whether the residual collapses.
- **Cost:** a new lift with its own stationarity proof (the completer count is not a pool count, so T16 does not transfer directly), plus minutes of compute.
- **Risk:** the projection now reads part of the predicate, so a collapse would be partly definitional. That must be argued before freezing.
- **Alternative:** a principled pause, consolidating E5A–E5D while the hub adopts the GT pins.
