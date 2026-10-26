# Atlas-018 execution recovery and adoption

Recorded 26 October 2026. This record recovers existing local files; it does not
claim a new run, recreate an unavailable invocation transcript, or edit results.

| Fact | Value |
| --- | --- |
| Starting live branch HEAD | `b8e5ac48a2ef26e3d8cb2727a5798d5980b49435` |
| Governing prompt | `prompts/2026-10-26-otr-handoff/RESEARCH-PROMPT.md`, introduced at `333b1948e645c2b5943f7fed936cf4680b636ee9` |
| Recovery selection commit | `a2dfc5d1ee98c26cb249a15fe9e7828830917478` |
| Original freeze | `8923de6565937a99a185f817526816ba50690def` |
| Definitions commit | `81389d9d50eafe53ccd0e6eee339602989f13886` |
| Engine / method | `rrc-0.4.0` / `event-kernel-0.2.0` |
| Grammar / clock | `strict-event-image-v1` / `one_declared_event` |
| Canonical plan hash | `2468bf59c1fce72fb909482dc94e1abeae30e627f0bd71e4536ed8b10b7a27e0` |
| Plan / preflight | `plans/atlas-018.json` / `docs/atlas-018-preflight.md`, unchanged |
| Output | `results/atlas-018/`, existing bytes adopted unchanged |
| Complete / failed / timeout / unresolved / invalid / pending | `3 / 0 / 0 / 0 / 0 / 0` |
| New scientific worker invocations in this session | `0` |
| Independent probability entries checked | `576` |

## Chronology evidence and limits

The original local remote-tracking reflog records freeze `8923de6` as an
`update by push` at `2026-10-26 00:53:06 +0000`. The three result-file modification
times are `00:53:26.903012681`, `00:53:27.068153266` and `00:53:27.235180315`
on the same date, in UTC. The preceding freeze commit time is `00:53:02` UTC.
This supports the required ordering; local filesystem times and reflog are
provenance evidence, not an independently authenticated clock or a transcript.
No original total wall-clock time or invocation options are reconstructed.

The stored item elapsed fields are `0.000145` seconds for identified,
`0.000544` for free and `0.000640` for coupled. They are original worker fields,
not this recovery's measurements or new scientific observables. The immutable
plan declares a 120-second watchdog and a 300-second hard ceiling.

## Independent verification

From `relational-complexity/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 provenance/atlas-018-independent-check.py --out results/atlas-018
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/cello/domains/Relational-Substrate/constraint-lab/.venv/bin/python -m rrc verify --round atlas-018 --out results/atlas-018
```

Both checks pass. The first imports no RRC module and calls no worker. It
reconstructs planned event laws with exact fractions and checks input hashes,
receipt hashes, status, file inventory, semantics, every probability entry and
the declared image correspondence. It also checks the separately labelled
post-execution recoding. The saved output is
`provenance/atlas-018-independent-verification.json`; software negative fixtures
are `tests/test_atlas_018_audit.py`.

| Item | SHA-256 of original result bytes |
| --- | --- |
| `A18-identified` | `f4c2f9ea8e3d337396605b5af995b973a9300c2b9d814137f122f56fc895c653` |
| `A18-free` | `c2afb75fc903cee3d3f9488f24463f6c3c506978665ceb1ecaab06b10893a202` |
| `A18-coupled` | `317e876aa206bf0098e2ade7e8679c2105fb829baeb0d4abcff076ee874b2c03` |

The generated table is `reports/atlas-018.md`; interpretations and the algebraic
proof are `reports/atlas-018-observations.md`. Atlas-019 and Atlas-020 local files
remain deferred/unadopted and untouched. Atlas-001–017, all frozen plans,
preflights, the main engine, other programmes, shared synthesis and books were
not modified. Historical Atlas-007 failures remain failures.
