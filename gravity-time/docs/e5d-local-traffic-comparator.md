# E5D definitions: the anchor-local traffic comparator NL (GT-P012)

*Written before freezing, and before any NL value or new E5D readout of an N=5 or N=6 scientific cell was computed.*
- *Implementation: `constraint-lab/src/rs_constraint_lab/gtlocalcontrol.py` (NL) and `gte5d.py` (round).*
- *Fixtures: `tests/test_gtlocalcontrol.py` and `tests/test_gte5d.py`.*
- *E5C definitions (T12–T15) and every earlier comparator are reused unchanged.*

Labels: **[T]** theorem; **[D]** definition; **[L]** limitation. NL is a **comparison process** parameterised from a target's stationary generator. It is not a relational constraint family, not an ontology, and its macro currents are not a physical arrow of time.

## 1. Partition (fixed before any durability is examined)

**[D]** FREE graph x ∈ {0,1}^M with positive single-toggle rates W(x,e) and CT stationary law π. For an analyst anchor:
- **F_TRI({0,1}):** LOCAL = slots incident on 0 or 1 (|LOCAL| = L = 2N−3); REMOTE = the rest (R = M − L). Slot 01 gets no special treatment.
- **F_2PATH(0):** LOCAL = the N−1 slots at vertex 0; REMOTE = the rest.

Let ℓ(x) and r(x) be the present counts in each pool, and z(x) = (ℓ, r). The projection never reads motif membership, completers, the entry set S0, durability or which family showed an effect. The relabelled anchor uses its own transformed partition.

## 2. Construction

**[D]**
- p_z = Σ_{z(x)=z} π(x).
- For each neighbouring cell, the **ordered** stationary flux J_{z→z'} = Σ_{z(x)=z} π(x) Σ_{e: z(x⊕e)=z'} W(x,e): a sum of positive terms, never a difference.
- NL's per-slot rates at a graph in cell (ℓ, r):

| Slot | Rate |
| --- | --- |
| absent LOCAL | J_{(ℓ,r)→(ℓ+1,r)} / [p_(ℓ,r) (L−ℓ)] |
| present LOCAL | J_{(ℓ,r)→(ℓ−1,r)} / [p_(ℓ,r) ℓ] |
| absent REMOTE | J_{(ℓ,r)→(ℓ,r+1)} / [p_(ℓ,r) (R−r)] |
| present REMOTE | J_{(ℓ,r)→(ℓ,r−1)} / [p_(ℓ,r) r] |

- A move with no eligible slot does not exist (its count is zero), so there is no division by zero.
- Directed fluxes are used as they are. **Nothing is symmetrised.**
- **Degenerate pools [D]:** if REMOTE is empty (R = 0), NL reduces to the count-dependent lift on LOCAL alone; likewise if LOCAL is empty. Neither case arises at N = 5, 6, where both pools are nonempty.

## 3. Theorems

**T16 (stationarity without detailed balance) [T].** π_NL(x) = p_{z(x)} / [C(L,ℓ) C(R,r)] is stationary for NL.

*Proof.* Every toggle changes ℓ or r by one, so no transition stays inside a cell.
- **Outflow.** At x in cell z, the outflow is π_NL(x) Σ_moves (number of eligible slots) × rate = Σ_{z'} J_{z→z'} / [C(L,ℓ)C(R,r)].
- **Inflow.** Consider the inflow from cell z − e_L (a local formation into x).
  - The present local slots of x are ℓ in number. Each gives a predecessor y with π_NL(y) = p_{z−e_L} / [C(L,ℓ−1)C(R,r)] and rate J_{z−e_L→z} / [p_{z−e_L}(L−ℓ+1)].
  - Summing gives J_{z−e_L→z} · ℓ / [(L−ℓ+1) C(L,ℓ−1) C(R,r)] = J_{z−e_L→z} / [C(L,ℓ)C(R,r)], using C(L,ℓ−1)(L−ℓ+1) = C(L,ℓ)·ℓ.
  - The other three directions are identical.
- **Balance.** Inflow = Σ_{z'} J_{z'→z} / [C(L,ℓ)C(R,r)]. Balance at x is therefore equivalent to **macro-flux conservation**, Σ_{z'} J_{z→z'} = Σ_{z'} J_{z'→z}. The target satisfies this: sum its global balance over the fibre; there are no intra-fibre transitions. ∎

**Frozen check:** the target's macro conservation holds within 10⁻⁹, and NL's global balance within 10⁻¹⁰.

**T17 (what NL matches) [T].**
- NL's cell masses are p_z: sum π_NL over the C(L,ℓ)C(R,r) graphs of the cell.
- Its ordered flux from z to z + e_L is p_z (L−ℓ) · J_{z→z+e_L} / [p_z (L−ℓ)] = J_{z→z+e_L}, and likewise for every direction. **Every ordered macro flux matches.**
- Consequently NL also matches:
  - the edge-count profile (k = ℓ + r);
  - every adjacent edge-count flux (sums of macro fluxes), so NL matches everything NK matches;
  - the mean CT activity;
  - the event-weighted macro profile;
  - the total local and remote stationary event traffic.

**T18 (restricted uniqueness) [T].** Consider single-toggle generators that are exchangeable within each pool (rates depend only on the cell, the pool and the slot's state) and whose stationary law has cell masses p_z. Such a generator's stationary law is invariant under pool-preserving permutations, which act transitively on each cell, so it is uniform within cells. Matching every ordered macro flux then forces each per-slot rate to equal NL's. **No uniqueness is claimed over generators outside this class.**

**T19 (reversibility) [T].** NL satisfies detailed balance iff every macro edge carries zero net current, J_{z→z'} = J_{z'→z}.
- *Proof.* For x in z and y = x⊕e in z', π_NL(x)W_NL(x,e) = J_{z→z'} / [C(L,ℓ)C(R,r) × (number of eligible slots)].
- Matching the count factors, as in T16, gives π_NL(x)W(x,e) / π_NL(y)W(y,e) = J_{z→z'} / J_{z'→z}. ∎
- A non-reversible target can have projected circulation on the (ℓ,r) grid. NL preserves it; a reversible lift could not.

## 4. Limitations

**[L]** NL does **not** match:
- the arrangement within a cell (which local slots are present, and hence the completer structure);
- completer counts and local motif hazards;
- correlations and multi-time structure;
- the first-hit law;
- persistence.

The target's (ℓ,r) projection need not be Markov. NL matches stationary one-step projected traffic only.
- **A residual beyond NL** means the effect is *not explained by this projection*. It is not proof of an organisational mechanism.
- **A collapse against NL** means the projection reproduces the effect. It does not identify a unique kinetic cause.

## 5. Verification on fixtures (before freezing)

| Check | Fixture | Result |
| --- | --- | --- |
| NULL fixed point (NL = NULL) | N = 4, both partitions | rates all 1 within 1e-10 |
| Non-reversible projection | synthetic N = 4 circulating chain, both partitions | projected net current > 1e-3; π_NL stationary (balance < 1e-10); every ordered flux matched (< 1e-10); NL not reversible; the same net currents reproduced; independent stationary solve L1 < 1e-8 |
| Count-dependent target | synthetic N = 4 | NL = NK = target |
| Relabelled anchor | N = 4 PCOMP | NL durability agrees within 1e-9 |
| Zero cell | synthetic | UNRESOLVED (not smoothed) |
| Blindness | static | `nl_chain(n, local, mf)` takes no predicate, entry set or durability; the module never reads them |

**Cost** (synthetic N = 6 rule): NL for four anchor sets about 25 s, peak 357 MB.

## 6. E5D matrix and readouts

- **Matrix:** F_TRI({0,1}) on all 12 laws; F_2PATH(0) on the six N=6 laws. N=5 F_2PATH is excluded: it is structurally zero after renewal (T14). That makes **18 analyses**.
- **Comparators:** target, N0, ND, NK, NL, each with its own entrance law and first-renewal law (E5C T12). NL is built per anchor.
- **Readouts:** the E5C objects unchanged (R0; U_h and C_h at h = 0, 1, 2, 4, 8; return and exit; immediate return; entry-size classes; F_TRI size ≥ 2 pooled).
- **Diagnostics:** target macro conservation; net currents on the (ℓ,r) grid; rare and zero cells; within-cell local-rate SD and CV; NL reversibility.

## 7. Live accounts (no predicted sign)

| Account | Readout |
| --- | --- |
| D1 residual beyond NL | C_h above NL at both sizes and in meaningful entry classes, with low original return |
| D2 local/remote traffic | an excess over NK that collapses against NL |
| D3 within-cell configuration | a residual remaining after NL; large within-cell local-rate CV |
| D4 flicker or composition | pooled differences that vanish within classes; high return |
| D5 null or reversal | equal, mixed, h-dependent or N-dependent results |
| D6 projection circulation | nonzero target macro currents, so NL non-reversible; compare against NK (reversible) |

## 8. Frozen checks (written into the plan)

- **Replication:** target, ND and NK U_h equal the published E5C values within max(10⁻¹⁰, 10⁻⁸·|value|).
- **NL identities (T16, T17):** global balance ≤ 10⁻¹⁰; p_z and ordered fluxes within 10⁻⁹ relative; all rates positive; analytic law against the iterative solve L1 ≤ 10⁻⁸ when that solve resolves.
- **Target macro conservation:** ≤ 10⁻⁹.
- **E5C durability checks for all laws:** monotone U_h; T13; leave-R causes sum to 1; dense against iterative; relabelling.
- **NULL:** all comparators equal.
