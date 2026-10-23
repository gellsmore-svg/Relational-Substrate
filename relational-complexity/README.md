# Recursive relational complexity

Independent Open-Thetical Research programme inside the Relational Substrate repository.

The question is whether relational structures can be composed recursively, and whether a finite interface can preserve their consequential behaviour. The charter is [`charter.md`](charter.md). The session hand-off is [`PROGRESS.md`](PROGRESS.md).

This directory does not modify the Constraint Laboratory or the Gravity–Temporality programme.

## Layout

| Path | Role |
| --- | --- |
| `charter.md` | OTR 1.0 charter |
| `docs/` | Reuse map, questions, methods, architecture, feasibility, definitions |
| `coherence/` | RRC ledger |
| `plans/` | Frozen rounds, written before execution |
| `src/rrc/` | Exact engine and resumable runner (from Stage B) |
| `tests/` | Identity, fixture and recovery tests |
| `generated/` | Disposable item output. Not committed |
| `reports/` | Atlases and findings written from completed items |
| `provenance/` | Source commits |

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
