# Recursive relational complexity

Independent Open-Thetical Research programme inside the Relational Substrate repository.

The question is whether relational structures can be composed recursively, and whether a finite interface can preserve their consequential behaviour. The charter is [`charter.md`](charter.md). The session hand-off is [`PROGRESS.md`](PROGRESS.md).

RRC-001 is closed. The plain-language account is [`reports/rrc-001-findings.md`](reports/rrc-001-findings.md). The mathematical reading is [`reports/rrc-001-interpretation.md`](reports/rrc-001-interpretation.md). The continuation is the atlas in [`docs/atlas-charter.md`](docs/atlas-charter.md). [`docs/rrc-002-proposal.md`](docs/rrc-002-proposal.md) is an unfrozen note and is not the atlas queue.

This directory does not modify the Constraint Laboratory or the Gravity–Temporality programme.

## Layout

| Path | Role |
| --- | --- |
| `charter.md` | OTR 1.0 charter |
| `atlas/` | Idea library, coverage, equivalences, patterns, open questions |
| `docs/` | Reuse map, questions, methods, architecture, feasibility, definitions, atlas charter |
| `coherence/` | RRC ledger |
| `plans/` | Frozen rounds, written before execution |
| `src/rrc/` | Exact engine and resumable runner (from Stage B) |
| `tests/` | Identity, fixture and recovery tests |
| `generated/` | Disposable timing output. Not committed |
| `results/` | Per-item results, receipts, and the round manifest |
| `reports/` | Atlases and findings written from completed items |
| `provenance/` | Source commits and the execution record |

## Commands

Once the engine is present, from this directory, with NumPy available:

```bash
python -m rrc plan --round rrc-001
python -m rrc run --round rrc-001 --max-items 4
python -m rrc status --round rrc-001
python -m rrc resume --round rrc-001
python -m rrc verify --round rrc-001
python -m rrc report --round rrc-001
```

`plan` does not run scientific cells. `run` and `resume` execute only a frozen plan, skip valid completed items, and stop at the declared budget.
