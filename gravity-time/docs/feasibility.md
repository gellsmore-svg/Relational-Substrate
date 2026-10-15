# Computational feasibility

Every G0 quantity is exact: a full-event kernel and a linear-algebra stationary or absorption solve. No sampling, so no seed. The costs below were measured on this implementation before the G0 plan was written.

| N | Pair slots | Free-mode states | Held-triangle reachable class | Rule instances (largest G0 template) | Kernel build | Stationary solve |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 6 | 64 | 8 | 24 | <0.01 s | dense, exact rational |
| 5 | 10 | 1,024 | 128 | 60 | 0.04 s (30 instances) | dense float, exact rational check on held class |
| 6 | 15 | 32,768 | 4,096 | 120 | **5.0 s** measured (120 K2 instances) | dense float on held class (4,096); sparse lazy iteration on free mode (32,768) |
| 7 | 21 | 2,097,152 | 262,144 | 210 | est. 10–20 min in the Fraction builder | sparse only |
| 8 | 28 | 268,435,456 | 33,554,432 | 336 | infeasible in this builder | — |

**Decision.**
- G0 runs at N=5 and N=6: 40 items, each well inside the 120-second watchdog.
- N=7 is deferred to G2. It needs a vectorised template kernel, validated against `build_kernel` on N≤6, and a sparse stationary solver. Opening it needs a measured cost and a stated information value: more distance shells for S-DIST.
- N≥8 is out of scope for exhaustive exact analysis.

**Expected information value of G0.** Three things:
1. whether any minimal label-covariant template produces relational attraction that survives the density, boundary, combinatorial and clock controls;
2. whether hard and soft admissibility differ in kind, as capture versus stationary concentration;
3. whether a K3 conjunction is needed.

Each outcome, including a null for every template, constrains H-D, H-A, H-AD, H-C and H-K3.
