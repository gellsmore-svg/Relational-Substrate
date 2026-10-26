"""N=7 cost fixtures for the E1 observables, on theorem-fixed cells only.

Fixtures:

* NULL (HELD and FREE): the stationary law is uniform by theorem, so every
  occupancy channel is fixed by counting, and the chain is reversible.
* CLOSE strong_favour (HELD and FREE): a gradient family whose stationary law
  is the closed-form triple-local Gibbs law (coverage audit, section 3). It is
  not a proposed E1 cell. Its ``predicted_law_l1_gap`` checks the N=7
  iterative solver against an analytic answer.

Only costs and solver checks are written: timings, iterations, residuals,
cross-check distances, the Gibbs-law gap, the reachable size and the
symmetry check. No observable value is written. Run one fixture per process
so that peak memory can be measured:

    /usr/bin/time -v python -m rs_constraint_lab.gtobs_fixtures HELD NULL none --out f.json
"""

from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from pathlib import Path

from rs_constraint_lab import gtkernel, gtobs

FIXTURES = {("NULL", "none"), ("CLOSE", "strong_favour")}


def run(mode: str, family: str, grade: str, n: int = 7) -> dict:
    if (family, grade) not in FIXTURES:
        raise SystemExit(f"{family} {grade} is not a declared theorem-fixed fixture")
    families = gtkernel.all_e0_components()
    started = time.perf_counter()
    chain, kernel_timing = gtkernel.reachable_chain(n, mode, families[family][grade])
    built = time.perf_counter() - started
    result, _ = gtobs.analyse(chain, family=family, grade=grade, n=n, mode=mode, families=families, with_trajectories=False)
    stationary = result.get("stationary", {})
    return {
        "autocorrelation_diagnostics": result.get("autocorrelation_diagnostics"),
        "build_and_reach_seconds": built,
        "family": family,
        "gibbs_projection_converged": (result.get("gibbs_projection") or {}).get("converged"),
        "grade": grade,
        "kernel_timing": kernel_timing,
        "mode": mode,
        "n": n,
        "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
        "predicted_law_l1_gap": result.get("predicted_law_l1_gap"),
        "reachable_states": result["reachable_states"],
        "regime": result["regime"],
        "stationary": {k: stationary.get(k) for k in ("iterations", "cross_check_iterations", "cross_check_l1", "cross_check_max_relative", "residual", "last_max_relative_change", "decay_ratio", "remaining_l1_estimate", "resolved", "seconds")},
        "symmetry_max_abs_difference": result.get("symmetry_max_abs_difference"),
        "timings": result.get("timings"),
        "total_seconds": time.perf_counter() - started,
        "observables_version": gtobs.OBSERVABLES_VERSION,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode")
    parser.add_argument("family")
    parser.add_argument("grade")
    parser.add_argument("--n", type=int, default=7)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    row = run(args.mode, args.family, args.grade, args.n)
    Path(args.out).write_text(json.dumps(row, indent=1, sort_keys=True, default=float) + "\n")
    print(json.dumps({k: row[k] for k in ("mode", "family", "reachable_states", "total_seconds", "peak_rss_mb", "predicted_law_l1_gap")}, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
