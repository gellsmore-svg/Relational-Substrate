"""Scale and witness-strength census for the E1 design (no scientific cell is opened).

Two kinds of quantity, both fixed before any E1 cell runs:

* Representational facts: slot and configuration counts, and the
  distribution of each component's witness count over every (state, slot)
  of the candidate space. These depend only on the template definitions
  and N.
* NULL baselines: the NULL family's stationary law is uniform on the
  candidate space (theorem; checked numerically to 2.5e-19 at HELD N7 in
  docs/e1-kernel.md), so its occupancy channels are fixed by counting.

    python -m rs_constraint_lab.gtscale --out scale.json [--n 5 --n 6 --n 7]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gtkernel, gtobs
from rs_constraint_lab.gte0a import SOURCE, Chain
from rs_constraint_lab.state import edges
from rs_constraint_lab.weights import alphabet_factors

KINDS = ("close_form", "close_dissolve", "adj_form", "path_form", "path_dissolve")
ALPHABETS = ("W4", "W3", "W16")


def max_witnesses(kind: str, n: int) -> int:
    """Largest witness count of one pair, from the template definitions."""
    if kind.startswith("close"):
        return n - 2
    if kind == "adj_form":
        return 2 * (n - 2)
    return 2 * (n - 2) * (n - 3)


def witness_distribution(n: int, mode: str, kind: str) -> dict:
    """Witness counts over every (state, slot) of the candidate space where the component acts."""
    states = gtkernel.candidate_states(n, mode)
    counts = gtkernel.witness_counts(states, n, kind)
    present = ((states[:, None] >> np.arange(counts.shape[1])) & 1).astype(bool)
    acts = ~present if kind.endswith("_form") else present
    if mode == "HELD":
        acts[:, [i for i, (a, b) in enumerate(edges(n)) if a in SOURCE and b in SOURCE]] = False
    values = counts[acts]
    dist = np.bincount(values, minlength=max_witnesses(kind, n) + 1)
    total = int(dist.sum())
    mean = float((np.arange(len(dist)) * dist).sum() / total)
    return {
        "acting_opportunities": total,
        "distribution": {str(w): int(c) for w, c in enumerate(dist) if c},
        "max_possible": max_witnesses(kind, n),
        "max_observed": int(values.max()),
        "mean": mean,
        "share_zero": float(dist[0] / total),
    }


def log_weight_scale(mean: float, max_w: int) -> dict:
    """Mean and maximum log-weight |w log m| for each grade and alphabet."""
    out = {}
    for alphabet in ALPHABETS:
        factors = alphabet_factors(alphabet)
        for grade in ("weak_favour", "strong_favour"):
            lm = math.log(float(factors[grade]))
            out[f"{alphabet}:{grade}"] = {"log_factor": lm, "max_log_weight": max_w * lm, "mean_log_weight_uniform": mean * lm}
    return out


def null_baselines(n: int, mode: str) -> dict:
    """Occupancy channels of the NULL cell, from the uniform law on the candidate space."""
    states = gtkernel.candidate_states(n, mode)
    size = len(states)
    law = np.full(size, 1.0 / size)
    slots = len(edges(n))
    chain = Chain(slots, states, np.ones((size, slots)), np.zeros((size, slots), dtype=np.int64))
    arrays = gtobs.structure_arrays(chain, n)
    out: dict = {"hub_structure": gtobs.hub_structure(arrays["degree"], law, n, mode), "expected_edges": float(law @ arrays["edges"])}
    if mode == "HELD":
        D = gtobs.source_distances(states, n)
        probes = [p for p in range(n) if p not in SOURCE]
        shells = {}
        for p in probes:
            for d in np.unique(D[:, p]):
                key = "inf" if d < 0 else str(int(d))
                shells[key] = shells.get(key, 0.0) + float((D[:, p] == d).mean()) / len(probes)
        detached = (D[:, probes] < 0).sum(axis=1)
        edge_list = edges(n)
        attach = sum(1 for a, b in edge_list if (a in SOURCE) != (b in SOURCE))
        free = sum(1 for a, b in edge_list if not (a in SOURCE and b in SOURCE))
        out.update({
            "attachment_slots": attach,
            "free_slots": free,
            "null_attachment_fraction": attach / free,
            "probe_distance_distribution": dict(sorted(shells.items())),
            "detached_probe_count_distribution": {str(int(c)): float((detached == c).mean()) for c in np.unique(detached)},
            "max_finite_distance": int(D[:, probes].max()),
            "source_share_of_entities": len(SOURCE) / n,
        })
    return out


def census(n: int, mode: str) -> dict:
    slots = len(edges(n))
    started = time.perf_counter()
    out = {
        "candidate_states": 1 << (slots - (3 if mode == "HELD" else 0)),
        "configurations_2_pow_slots": 1 << slots,
        "mode": mode,
        "n": n,
        "slots": slots,
        "components": {},
    }
    for kind in KINDS:
        dist = witness_distribution(n, mode, kind)
        dist["log_weight"] = log_weight_scale(dist["mean"], dist["max_possible"])
        out["components"][kind] = dist
    out["null_baselines"] = null_baselines(n, mode)
    out["seconds"] = time.perf_counter() - started
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, action="append")
    parser.add_argument("--mode", action="append")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    rows = []
    for n in args.n or (5, 6, 7):
        for mode in args.mode or ("HELD", "FREE"):
            row = census(n, mode)
            rows.append(row)
            print(f"N{n} {mode}: {row['candidate_states']} states, {row['seconds']:.1f} s", flush=True)
    Path(args.out).write_text(json.dumps({"census": rows, "version": "gt-scale-census/v1"}, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
