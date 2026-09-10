"""Independent measuring instruments. Never imported by the mechanism."""

from collections import Counter
import math
import statistics


def wilson(correct: int, total: int) -> list[float]:
    if not total:
        return [0.0, 1.0]
    z = 1.959963984540054
    p = correct / total
    d = 1 + z * z / total
    c = (p + z * z / (2 * total)) / d
    h = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def entropy(values) -> float:
    counts = Counter(values)
    n = counts.total()
    return -sum((v / n) * math.log2(v / n) for v in counts.values()) if n else 0.0


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    if not n:
        raise ValueError("Cannot summarize an empty batch")
    correct = sum(r["correct"] for r in rows)
    iterations = sorted(r["iterations"] for r in rows)
    outcomes = [str(r["result"]) for r in rows]
    paths = [r["trajectory"] for r in rows]
    return {"runs": n, "correct": correct, "accuracy": correct / n,
            "wilson95": wilson(correct, n),
            "nonconvergence": sum(not r["converged"] for r in rows) / n,
            "mean_iterations": statistics.mean(iterations),
            "median_iterations": statistics.median(iterations),
            "p95_iterations": iterations[math.ceil(0.95 * n) - 1],
            "outcome_entropy_bits": entropy(outcomes),
            "outcomes": dict(Counter(outcomes)), "unique_trajectories": len(set(paths)),
            "trajectory_entropy_proxy_bits": entropy(paths),
            "unique_final_structures": len({r["final_structure"] for r in rows})}
