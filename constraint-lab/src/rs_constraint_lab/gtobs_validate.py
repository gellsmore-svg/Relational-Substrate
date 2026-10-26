"""Reproduction of published E0A/E0B cells by ``gtobs`` (opt-in engineering validation).

Every committed result in ``round-e0a-tables.json`` and ``round-e0b-tables.json``
is recomputed from a ``gtkernel`` chain by ``gtobs.analyse`` with the iterative
stationary solver (the method E1 would use at N=7) and compared channel by
channel. Spectrum and timings are not compared (not reproduced / not
deterministic). Run:

    python -m rs_constraint_lab.gtobs_validate [--n 5] [--out report.json]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

from rs_constraint_lab import gte0a, gte0b, gtkernel, gtobs

SKIP_KEYS = {"timings", "spectrum", "spectrum_note", "e1_additions", "observables_version", "autocorrelation_diagnostics", "stationary", "dense_limit_note"}
ABS_TOLERANCE = 1e-10
REL_TOLERANCE = 1e-8


TOP_LISTS = {"top_asymmetric_patterns": ("forward", "reverse"), "top_net_currents": ("from", "to")}


def _magnitude(row: dict) -> float:
    if "net_fraction" in row:
        return float(row["net_fraction"])
    return abs(float(row["forward_probability"]) - float(row["reverse_probability"]))


def _close(a: float, b: float, abs_tol: float, rel_tol: float) -> bool:
    return abs(a - b) <= abs_tol or abs(a - b) <= rel_tol * max(abs(a), abs(b))


TOP_LIST_NOISE_FLOOR = 1e-12


def compare_top_list(ref: list, new: list, path: str, identity: tuple[str, str], abs_tol: float, rel_tol: float) -> list[dict]:
    """Ranked lists compared by entry identity.

    Entries of equal magnitude (cycle currents are equal by Kirchhoff's law;
    reverse-pair differences can tie) have no defined order, so order is not
    compared. An entry present in only one list is accepted when its
    magnitude ties the smallest magnitude shown (a tie at the cut).
    """
    ref = [r for r in ref if _magnitude(r) >= TOP_LIST_NOISE_FLOOR]
    new = [r for r in new if _magnitude(r) >= TOP_LIST_NOISE_FLOOR]
    if len(ref) != len(new):
        return [{"path": path, "kind": "length", "ref": len(ref), "new": len(new)}]
    key = lambda r: (r[identity[0]], r[identity[1]])
    a = {key(r): r for r in ref}
    b = {key(r): r for r in new}
    out = []
    for k in sorted(set(a) & set(b)):
        out.extend(compare(a[k], b[k], f"{path}<{k[0]}>", abs_tol=abs_tol, rel_tol=rel_tol))
    cut_ref = min((_magnitude(r) for r in ref), default=0.0)
    cut_new = min((_magnitude(r) for r in new), default=0.0)
    for k in sorted(set(a) - set(b)):
        if _magnitude(a[k]) < TOP_LIST_NOISE_FLOOR:
            continue
        if not _close(_magnitude(a[k]), cut_new, abs_tol, rel_tol):
            out.append({"path": f"{path}<{k[0]}>", "kind": "top_list_member", "ref": a[k], "new": None})
    for k in sorted(set(b) - set(a)):
        if _magnitude(b[k]) < TOP_LIST_NOISE_FLOOR:
            continue
        if not _close(_magnitude(b[k]), cut_ref, abs_tol, rel_tol):
            out.append({"path": f"{path}<{k[0]}>", "kind": "top_list_member", "ref": None, "new": b[k]})
    return out


def plateau_modes(distribution: dict, rel_tol: float = 1e-9) -> set[int]:
    """Local maxima of a distribution allowing equal neighbours (tie-aware)."""
    keys = sorted(distribution, key=int)
    values = [distribution[k] for k in keys]
    out = set()
    for j, v in enumerate(values):
        if v <= 1e-12:
            continue
        left = j == 0 or v >= values[j - 1] * (1 - rel_tol)
        right = j == len(keys) - 1 or v >= values[j + 1] * (1 - rel_tol)
        if left and right:
            out.add(int(keys[j]))
    return out


def compare(ref, new, path: str = "", *, abs_tol: float = ABS_TOLERANCE, rel_tol: float = REL_TOLERANCE) -> list[dict]:
    """Differences between two JSON-like values; floats within tolerance are equal."""
    out: list[dict] = []
    name = path.rsplit("/", 1)[-1]
    if name in TOP_LISTS and isinstance(ref, list) and isinstance(new, list):
        return compare_top_list(ref, new, path, TOP_LISTS[name], abs_tol, rel_tol)
    if isinstance(ref, dict) and isinstance(new, dict):
        for key in sorted(set(ref) | set(new)):
            if key in SKIP_KEYS and path == "":
                continue
            if key not in ref or key not in new:
                out.append({"path": f"{path}/{key}", "kind": "missing", "ref": key in ref, "new": key in new})
                continue
            if key == "edge_count_modes" and ref[key] != new[key]:
                plateau = plateau_modes(ref.get("edge_count_distribution", {}))
                if set(ref[key]) <= plateau and set(new[key]) <= plateau:
                    out.append({"path": f"{path}/{key}", "kind": "tie_sensitive", "ref": ref[key], "new": new[key]})
                    continue
            out.extend(compare(ref[key], new[key], f"{path}/{key}", abs_tol=abs_tol, rel_tol=rel_tol))
        return out
    if isinstance(ref, list) and isinstance(new, list):
        if len(ref) != len(new):
            return [{"path": path, "kind": "length", "ref": len(ref), "new": len(new)}]
        for i, (a, b) in enumerate(zip(ref, new)):
            out.extend(compare(a, b, f"{path}[{i}]", abs_tol=abs_tol, rel_tol=rel_tol))
        return out
    if isinstance(ref, bool) or isinstance(new, bool) or isinstance(ref, str) or ref is None or new is None:
        return [] if ref == new else [{"path": path, "kind": "value", "ref": ref, "new": new}]
    if isinstance(ref, (int, float)) and isinstance(new, (int, float)):
        if isinstance(ref, float) and math.isinf(ref):
            return [] if ref == new else [{"path": path, "kind": "value", "ref": ref, "new": new}]
        diff = abs(float(ref) - float(new))
        if diff <= abs_tol or diff <= rel_tol * max(abs(float(ref)), abs(float(new))):
            return []
        return [{"path": path, "kind": "number", "ref": ref, "new": new, "abs": diff}]
    return [] if ref == new else [{"path": path, "kind": "value", "ref": ref, "new": new}]


def gth_stationary(chain) -> dict:
    """Jump-chain stationary law by GTH elimination (dense, subtraction-free).

    Grassmann-Taksar-Heyman state reduction keeps high relative accuracy on
    every entry, including states of probability ~1e-12. Used only as an
    independent referee where E0 and gtobs disagree (dense; N <= 6 HELD).
    """
    import numpy as np

    size = len(chain.states)
    A = np.zeros((size, size))
    valid = chain.T >= 0
    rows = np.broadcast_to(np.arange(size)[:, None], chain.T.shape)[valid]
    np.add.at(A, (rows, chain.T[valid]), (chain.W / chain.rates[:, None])[valid])
    for k in range(size - 1, 0, -1):
        s = A[k, :k].sum()
        A[:k, :k] += np.outer(A[:k, k] / s, A[k, :k])
        A[:k, k] /= s
    pi = np.zeros(size)
    pi[0] = 1.0
    for k in range(1, size):
        pi[k] = pi[:k] @ A[:k, k]
    pi /= pi.sum()
    ct = pi / chain.rates
    ct /= ct.sum()
    return {"ct": ct, "jump": pi, "mean_rate_ct": float(ct @ chain.rates), "method": "gth_dense_referee", "resolved": True}


def strict_stationary(chain, start: int) -> dict:
    """Referee for classes above the dense limit: lazy iteration to 1e-15 relative change, from two starts.

    Returns the uniform-start law and the largest relative difference between
    the uniform-start and point-mass-start limits.
    """
    import numpy as np

    R = chain.rates
    P = chain.W / R[:, None]
    pred, p_in = gtobs._incoming(chain, P)
    a, _, _, _ = gtobs._lazy_power(pred, p_in, np.full(len(R), 1.0 / len(R)), 1e-15, 5_000_000, relative_tolerance=1e-15)
    point = np.zeros(len(R))
    point[start] = 1.0
    b, _, _, _ = gtobs._lazy_power(pred, p_in, point, 1e-15, 5_000_000, relative_tolerance=1e-15)
    a = a / a.sum()
    ct = a / R
    ct /= ct.sum()
    return {"ct": ct, "jump": a, "mean_rate_ct": float(ct @ R), "method": "strict_two_start_referee", "resolved": True, "two_start_max_relative": float((np.abs(a - b / b.sum()) / a).max())}


NEW_CAPABILITY_KEYS = ("/autocorrelation", "/localisation_persistence_index")


def reproduce(item_id: str, ref: dict, families: dict, round_id: str, *, referee: bool = True) -> dict:
    started = time.perf_counter()
    chain, _ = gtkernel.reachable_chain(ref["n"], ref["mode"], families[ref["family"]][ref["grade"]])
    kwargs = dict(family=ref["family"], grade=ref["grade"], n=ref["n"], mode=ref["mode"], families=families, item_id=item_id, round_id=round_id, with_trajectories=False, hub_frame="hub_frame" in ref)
    new, _ = gtobs.analyse(chain, **kwargs)
    diffs = compare(ref, new)
    for d in diffs:
        if d["kind"] == "value" and d["ref"] is None and d["path"] in NEW_CAPABILITY_KEYS and ref["reachable_states"] > gtobs.DENSE_LIMIT:
            d["kind"] = "new_capability"
    adjudication = None
    real = [d for d in diffs if d["kind"] not in ("tie_sensitive", "new_capability")]
    if referee and real and new.get("regime") == "recurrent":
        if len(chain.states) <= gtobs.DENSE_LIMIT:
            law = gth_stationary(chain)
        else:
            law = strict_stationary(chain, gtobs.start_index(chain, ref["n"], ref["mode"]))
        judged, _ = gtobs.analyse(chain, stationary_override=law, **kwargs)
        new_vs_referee = [d for d in compare(judged, new) if d["path"] in {x["path"] for x in real}]
        ref_vs_referee = [d for d in compare(judged, ref) if d["path"] in {x["path"] for x in real}]
        adjudication = {
            "e0_differs_from_referee": len(ref_vs_referee),
            "gtobs_differs_from_referee": len(new_vs_referee),
            "referee": law["method"],
            "referee_two_start_max_relative": law.get("two_start_max_relative"),
            "verdict": ("e0_dense_solve_error" if ref.get("stationary", {}).get("method") == "dense_solve" else "e0_unconverged_iteration") if not new_vs_referee and ref_vs_referee else ("gtobs_error" if new_vs_referee and not ref_vs_referee else "unresolved"),
        }
    return {
        "adjudication": adjudication,
        "item_id": item_id,
        "differences": diffs,
        "ref_method": (ref.get("stationary") or {}).get("method"),
        "new_stationary": new.get("stationary"),
        "autocorrelation_diagnostics": new.get("autocorrelation_diagnostics"),
        "gibbs_converged_ref": (ref.get("gibbs_projection") or {}).get("converged"),
        "seconds": time.perf_counter() - started,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--n", type=int, action="append")
    parser.add_argument("--only", action="append")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    root = Path(args.root)
    jobs = []
    for rel, families, round_id in (("gravity-time/reports/round-e0a-tables.json", gte0a.FAMILIES, gte0a.ROUND_ID), ("gravity-time/reports/round-e0b-tables.json", gte0b.FAMILIES, gte0b.ROUND_ID)):
        tables = json.loads((root / rel).read_text())
        for item_id, ref in sorted(tables["results"].items()):
            if args.n and ref["n"] not in args.n:
                continue
            if args.only and not any(s in item_id for s in args.only):
                continue
            jobs.append((round_id, item_id, ref, families))
    rows = []
    for round_id, item_id, ref, families in jobs:
        row = reproduce(item_id, ref, families, round_id)
        row["round_id"] = round_id
        rows.append(row)
        real = [d for d in row["differences"] if d["kind"] not in ("tie_sensitive", "new_capability")]
        status = "OK" if not real else f"{len(real)} differences"
        if any(d["kind"] == "new_capability" for d in row["differences"]):
            status += " (+autocorrelation, omitted by E0 above the dense limit)"
        if row["adjudication"]:
            status += f" [{row['adjudication']['verdict']}]"
        if any(d["kind"] == "tie_sensitive" for d in row["differences"]):
            status += " (tie-sensitive E0 value)"
        print(f"{round_id} {item_id} {status} {row['seconds']:.1f} s", flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1, sort_keys=True, default=str))
    e0_wrong = ("e0_dense_solve_error", "e0_unconverged_iteration")
    bad = sum(1 for r in rows if any(d["kind"] not in ("tie_sensitive", "new_capability") for d in r["differences"]) and not (r["adjudication"] and r["adjudication"]["verdict"] in e0_wrong))
    for verdict in e0_wrong:
        judged = sum(1 for r in rows if r["adjudication"] and r["adjudication"]["verdict"] == verdict)
        print(f"{judged} cells differ only where the referee shows E0 wrong ({verdict})")
    ties = sum(1 for r in rows if any(d["kind"] == "tie_sensitive" for d in r["differences"]))
    print(f"{len(rows)} cells; {bad} with differences; {ties} with tie-sensitive E0 values")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
