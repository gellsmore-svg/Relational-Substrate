# Execution record — GT-P005 (handover, directed succession and transition-enabling dissolution)

- **Prompt.** `provenance/prompts/GT-P005-agent-input.md`, an agent transcription: 26,486 bytes, sha256 `ca324d371294b1e04482d38db9faeea97b30ad23ab182ce6bbb204d5ad0f742e`. It has not been compared with the authored external file, and no byte identity is claimed.
- **Agent:** Claude Opus 5.5.
- **Branch:** `research/gravity-time-admissibility`. Draft PR #6, not merged.
- **Starting commit:** `3686a78` (GT-P004 close). It was verified as the remote head, with a clean worktree, PR #6 an open draft and CI green on both events. The OTR text is byte-identical to `main` (sha256 `2d902395…`).
- **Method:** OTR 1.0.

## Mandate kept

- **Rounds.** E2A, plus one E2B chosen because of E2A. No E2C, no N=7, no FREE N=7.
- **Grammar.** No new primitive and no grammar change. `prohibit` and `adj_form` are existing grammar.
- **Records.** G0, G1, E0 and E1 plans, tables and reports are unchanged. CBO and `main` are unchanged, and the Constraint Laboratory's branches were not edited. The cross-programme items are suggestions only (synthesis, section 6).

## Chronology

| Commit | Content |
| --- | --- |
| `3300f80` | Prompt stored; ledger row |
| `5c6fa40` | Coverage audit, formal note sections 1–4, the `gte2a` runner, and backward-compatible arguments in `gte1` and `gtobs`. Suite: 591 passed |
| `1974678` | **E2A frozen plan.** Hash `94a53734c94f6b763b0a61e9a395f64569291ccfa885198384feb36e9d18e933`; file sha256 `6f636ecb…`; pushed |
| `9622c9e` | Journey step 11 (E2A opened); pushed before execution |
| — | E2A executed 15:20:09–15:22:25 UTC. The runner verified plan ancestry, remote presence and contract |
| `32ac7f6` | **E2A results.** Tables payload `e4147f1e181b`, file sha256 `25384052…`; atlas and its generator |
| `b90c3ac` | **E2A reflection and E2A → E2B selection,** committed before any E2B code |
| `a6ed458` | `gte2b` and tests; `gte2a.analyse_item` gains `families`/`round_id`/`extra` arguments with unchanged defaults. Suite: 606 passed |
| `9448f95` | **E2B frozen plan.** Hash `72d266bcfa7f4bcaeb6b840e9cfa5194dde10680e67d5e4ca2b78d6d7b18577b`; file sha256 `061474c5…`; pushed |
| `379ec0f` | Journey steps 12 (E2A closed) and 13 (E2B opened); pushed before execution |
| — | E2B executed 15:31:33–15:31:38 UTC |
| `ecb3e73` | **E2B results.** Tables payload `56390e58ea57`, file sha256 `7f5cd60a…`; atlas |
| (this commit) | Formal note section 5; dissolution analysis; mechanism atlas; synthesis; plain-English report; ledger GT-F45–F53, GT-Q11–Q13 and GT-R69–R85; register (status after E2; H-EN, X-OPP); OP-10–OP-12; README; roadmap; execution record; journey step 14 |

## Pre-freeze work and exposure

- **Algebra.** The square-affinity identity was derived and checked on synthetic factor tables (0.13, 0.41, 2.7, 6.3 and 0) at N=4 and 5. This is a proof-verification fixture under the 8G gate.
- **Smoke run.** It used synthetic N=4 cells for all 21 E2A families in both modes, and its outputs were read. It showed one-way irreversibility in FREE N=4 path-form prohibit and an arrested HELD N=4 cell. This is declared in the E2A plan.
- **Timing.** One run on the published HELD N=6 CLOSEW cell (not a round cell): 48 s and 312 MB.
- **Published-cell exposure.** 18 E2A cells have published standard channels (the plan lists them); their new channels were never computed before. The other 28 E2A cells and all 18 E2B cells were unopened.
- **E2B.** Planned after reading all E2A results, as the OTR method intends. The E2B plan says so, and does not present E2B as independent confirmation.

## Execution and validation

| | E2A | E2B |
| --- | --- | --- |
| Items | 46 complete | 18 complete |
| Wall | 136 s (4 workers); cells 0.13–124 s; sum 521 s | 5 s; cells 0.10–1.9 s |
| Peak memory per cell | ≤ 314 MB | ≤ 43 MB |
| Identities | I1 46/46, I2 46/46, I3 10/10, I4 6/6, I5 20/20 | I1 18/18, I2 18/18, I5 9/9, I6 2/2 |
| Numerical acceptance (Z5) | 44/44 recurrent cells | 18/18 |
| Structure only | 2 cells (hard path-dissolve prohibition, absorbing) | 0 |

**Per-cell checks:**
- stationary two-start agreement and residual;
- the GTH dense referee (every class has at most 4,096 states);
- the long-double per-entry residual, with no zero-mass state;
- symmetry;
- the kernel sample (rule strings with exact fractions);
- the affinity reference (120 seeded squares from the rule strings);
- the partner-frame loop reference;
- the passage path-enumeration reference;
- in E2B, race-committor convergence (at most 384 iterations against a 20,000 cap).

**Tests.** 606 passed at the E2B code commit, plus the atlas tests. The final suite count is recorded in the provenance ledger row.

## Deviations and notes, in order

1. **Arrested label.** During the pre-freeze smoke test, a single-state class with no admissible event was labelled "stationary unresolved". It was relabelled "arrested" before freezing.
2. **A buggy unused helper.** A helper with wrong path multiplicity (`hit_reference`) was written, found while reviewing, and deleted before any test or freeze. The exact recursive reference `hit_reference_exact` was used.
3. **Formal note corollary 1.** It was tightened before the freeze: square generation of the cycle space holds when the class is a subcube. A hard-restricted class needs a separate argument.
4. **E2A reflection wording.** The E2A reflection (`b90c3ac`, committed before E2B) says ADPF's reversed handover is "as strong as any forward handover". That overstates: forward HELD indices range 0.015–0.19, and ADPF's −0.112 lies within that range. The reflection is left as written. Later documents and ledger GT-F47 say "comparable to forward handovers".
5. **Numbers corrected before publication** in the post-result documents, after re-checking against the tables:
   - enabling shares (EXCL FREE 0.27, EXPF 0.98);
   - cell counts per orientation class (16 σ > 0 soft cells; 10 saturated; 7 hard-gradient; 8 degenerate);
   - the soft passage maximum (0.12; 0.011 for the release step);
   - the domain of the aggregate claim (36 cells without one-way transitions);
   - the saturated reversal scale.
6. **Square circulation is a projection.** It sums oriented edge currents, which belong to several cycles. It is reported as such, not as a cycle decomposition.
7. **One HELD cell below the reporting floor.** HELD PATHF strong_favour has partner index −7e-13, below the declared 1e-12 floor, and is recorded as zero.

## Results (summary)

See `reports/gt-e2-report.md` and `reports/gt-e2-synthesis.md`.
- The local orientation is an identity (GT-F45).
- The aggregate follows σ in 36 of 36 cells without one-way transitions (GT-F46).
- σ < 0 reverses the handover (GT-F47).
- Square-level counter-circulation (GT-F48).
- The soft release step is an opportunity effect (GT-F49).
- Strict enabling is neither necessary nor sufficient for direction (GT-F50).
- One-way release overrides σ (GT-F51).
- Hard adjacency silences path terms (GT-F52).
- The held source acts as a witness (GT-F53).

Recommended next, not run: the one-way release mechanism (GT-Q11), with the aggregate-orientation theorem (GT-Q12).
