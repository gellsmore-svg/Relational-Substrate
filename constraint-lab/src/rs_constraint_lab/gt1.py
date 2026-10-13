"""Gravity-time programme, Round G1: relative local recurrence rates.

G1 asks whether a constraint that produces a G0 basin also changes how often a
probe's own relations actualise, by relational distance from the held source,
and whether the answer depends on the clock convention. All quantities are
exact kernel results on the HELD reachable class. No trajectory is sampled.

Local activity of probe p at state x:
  jump clock        a_j(x) = probability that the next event toggles a relation incident to p
  continuous clock  a_c(x) = total rate of the relations incident to p (event weights as rates)
Shell activity A(k) is the stationary mean of a(x) given d(p, source) = k.
The near/far ratio rho = A(1) / A(2) uses two local processes counted on one history.
Inward share: among probe-distance-changing moves from shell k, the fraction
that reduce distance. It is a ratio of rates, so it is independent of overall
rate scale, but inward moves are formations and outward moves dissolutions, so
any formation preference raises it. It is reported without a prediction.
"""

from __future__ import annotations

import math

import numpy as np

from rs_constraint_lab import gt0
from rs_constraint_lab.state import edges

ROUND_ID = "round-g1"
EXPERIMENT_ID = "gt-round-g1-recurrence-rates"
ANALYSIS_VERSION = "gt-g1/v1"
FAMILIES = {
    "NULL": (None,),
    "DENS": ("weak_favour", "strong_favour"),
    "ADJ": ("weak_favour", "strong_favour"),
    "CLOSE": ("weak_favour", "strong_favour"),
    "HOLD": ("weak_suppress", "strong_suppress"),
}
SIZES = (5, 6)
MASS_FLOOR = 1e-12
IDENTITY_TOLERANCE = 1e-12
PAIRED = {"weak_favour": "weak_suppress", "strong_favour": "strong_suppress"}


def items() -> list[dict]:
    out = []
    for n in SIZES:
        for family, grades in FAMILIES.items():
            for grade in grades:
                out.append({"family": family, "grade": grade, "item_id": f"HELD-N{n}-{family}-{grade or 'none'}", "mode": "HELD", "n": n})
    return out


def analyse_item(item: dict) -> dict:
    family, n, grade = item["family"], item["n"], item["grade"]
    kernel = gt0.build(family, n, grade, "HELD")
    start = gt0.start_state(n, "HELD")
    states = gt0.reachable(kernel, start)
    structure = gt0.class_structure(kernel, states)
    if len(structure["recurrent_classes"]) != 1 or len(structure["recurrent_classes"][0]) != len(states):
        raise gt0.BasinError(f"{item['item_id']} is not one recurrent class")
    pi, residual = gt0.stationary_dense(kernel, states)
    rates = gt0.total_rates(kernel, states)
    ct = gt0.continuous_time(pi, rates)
    edge_list = edges(n)
    probes = [p for p in range(n) if p not in gt0.SOURCE]
    incident = {p: [i for i, (a, b) in enumerate(edge_list) if p in (a, b)] for p in probes}
    out = {"family": family, "grade": grade, "n": n, "reachable_states": len(states), "stationary_residual": residual}
    cache: dict[tuple[int, int], float] = {}

    def d_of(s: int, p: int) -> float:
        key = (s, p)
        if key not in cache:
            cache[key] = gt0.distance_to_source(s, n, edge_list, p)
        return cache[key]

    for clock, law in (("jump", pi), ("continuous", ct)):
        act_num: dict[str, float] = {}
        mass: dict[str, float] = {}
        inward: dict[str, float] = {}
        moving: dict[str, float] = {}
        for i, s in enumerate(states):
            w = float(law[i])
            total = float(sum(kernel.weights[s]))
            for p in probes:
                shell = "inf" if math.isinf(d_of(s, p)) else str(int(d_of(s, p)))
                if clock == "jump":
                    activity = sum(float(kernel.weights[s][slot]) for slot in incident[p]) / total
                else:
                    activity = sum(float(kernel.weights[s][slot]) for slot in incident[p])
                act_num[shell] = act_num.get(shell, 0.0) + w * activity
                mass[shell] = mass.get(shell, 0.0) + w
                d = d_of(s, p)
                if math.isinf(d):
                    continue
                rate_in = rate_any = 0.0
                for t, prob in kernel.successors[s]:
                    dt = d_of(t, p)
                    if dt != d:
                        rate = float(prob) * (total if clock == "continuous" else 1.0)
                        rate_any += rate
                        if dt < d:
                            rate_in += rate
                if rate_any > 0:
                    inward[shell] = inward.get(shell, 0.0) + w * rate_in / rate_any
                    moving[shell] = moving.get(shell, 0.0) + w
        activity = {k: act_num[k] / mass[k] for k in sorted(mass) if mass[k] > MASS_FLOOR}
        share = {k: inward[k] / moving[k] for k in sorted(moving) if moving[k] > MASS_FLOOR}
        rho = activity["1"] / activity["2"] if "1" in activity and "2" in activity and activity["2"] > 0 else None
        out[clock] = {"inward_share_by_shell": share, "near_far_ratio": rho, "shell_activity": activity, "shell_mass": {k: mass[k] for k in sorted(mass)}}
    return out


def assemble(results: dict[str, dict]) -> dict:
    """Frozen predictions P1-P3, evaluated against the stored results."""
    checks = {}
    for n in SIZES:
        null = results[f"HELD-N{n}-NULL-none"]
        for favour, suppress in PAIRED.items():
            close = results[f"HELD-N{n}-CLOSE-{favour}"]
            hold = results[f"HELD-N{n}-HOLD-{suppress}"]
            gap = max(abs(close["continuous"]["shell_mass"].get(k, 0.0) - hold["continuous"]["shell_mass"].get(k, 0.0)) for k in set(close["continuous"]["shell_mass"]) | set(hold["continuous"]["shell_mass"]))
            checks[f"P1-N{n}-{favour}"] = {"gap": gap, "holds": gap <= IDENTITY_TOLERANCE}
            r_null = null["continuous"]["near_far_ratio"]
            r_close = close["continuous"]["near_far_ratio"]
            r_hold = hold["continuous"]["near_far_ratio"]
            holds = r_null is not None and r_close is not None and r_hold is not None and r_close > r_null and r_hold < r_null
            checks[f"P2-N{n}-{favour}"] = {"close_ratio": r_close, "hold_ratio": r_hold, "holds": holds, "null_ratio": r_null}
            jump_gap = max(abs(close["jump"]["shell_mass"].get(k, 0.0) - hold["jump"]["shell_mass"].get(k, 0.0)) for k in set(close["jump"]["shell_mass"]) | set(hold["jump"]["shell_mass"]))
            checks[f"P3-N{n}-{favour}"] = {"gap": jump_gap, "holds": jump_gap > 1e-9}
    return checks


# --- plan and execution ------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-g1-plan.json"
WATCHDOG_SECONDS = 120


def prepare_plan() -> dict:
    from rs_constraint_lab.explore08 import plan_hash

    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "clocks": {
            "continuous": "per-slot exponential rates equal to the event weights; activity is a rate per unit time",
            "jump": "lab full-event kernel; activity is a probability per event",
        },
        "experiment_id": EXPERIMENT_ID,
        "families": {family: [g for g in grades if g is not None] for family, grades in FAMILIES.items()},
        "frozen_predictions": {
            "P1_close_hold_same_continuous_basin": "CLOSE(m) and HOLD(1/m) have identical continuous-time shell masses within 1e-12 (derivation: both have rate ratio m^w for an edge with w common neighbours, so pi_ct is proportional to m^triangles)",
            "P2_opposite_near_far_rate_shift": "Under the continuous clock the near/far activity ratio rho = A(1)/A(2) is above NULL's for CLOSE(m) and below NULL's for HOLD(1/m), at N=5 and N=6 and both grades. This is a directional expectation from the rate structure (CLOSE multiplies near-source formation rates; HOLD divides near-source dissolution rates), not a derivation, and may fail.",
            "P3_jump_clock_separates_the_pair": "CLOSE(m) and HOLD(1/m) jump-chain shell masses differ by more than 1e-9 (derivation: pi_jump is proportional to pi_ct times the total rate, which differs between them)",
        },
        "history": False,
        "items": items(),
        "meta_constraints": False,
        "mode": "B",
        "motivation": "G0 found that each template's continuous-time stationary law is m^S/Z with S edges, wedges or triangles, and that CLOSE(m) and HOLD(1/m) share one basin. G1 asks whether a shared basin carries one recurrence-rate signature.",
        "new_primitives": False,
        "observables": [
            "shell masses under both clocks",
            "shell activity A(k) under both clocks",
            "near/far ratio rho = A(1)/A(2) under both clocks",
            "inward share by shell under both clocks (reported without prediction: formation preference raises it)",
        ],
        "ontology": {"G": 0, "H": 0, "L": 0, "O": 2, "S": 0, "grammar": "ordinary pair DSL", "mode": "HELD", "N": list(SIZES)},
        "pre_freeze_exposure": "The G1 observables were run only on an N=4 fixture before this plan was frozen. G0 tables (published) were read; they contain shell masses but not activities, rates or inward shares.",
        "programme": "GT",
        "question": "Does the configuration that produces a G0 basin also change the relative recurrence rate of a probe's own relations by relational distance, and does a shared basin determine one rate signature?",
        "round_id": ROUND_ID,
        "schema": "rs-gt.recurrence-plan/v1",
        "stochastic_trajectories": False,
        "tolerances": {"identity": IDENTITY_TOLERANCE, "mass_floor": MASS_FLOOR},
        "work_count": {"items": len(items()), "largest_state_space": 4096, "watchdog_seconds": WATCHDOG_SECONDS, "workers": 1},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo, commit, *, require_remote=True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("history") is not False or plan.get("new_primitives") is not False:
        raise FrozenPlanError("execution refused: G1 plan contract drifted")
    return plan


def run(root, plan) -> list[dict]:
    import time

    from rs_constraint_lab.durable import atomic_write_json, read_json

    rows = []
    for item in plan["items"]:
        path = root / "items" / f"{item['item_id']}.json"
        if path.is_file() and read_json(path).get("item_id") == item["item_id"]:
            payload = read_json(path)
        else:
            started = time.perf_counter()
            result = analyse_item(item)
            wall = time.perf_counter() - started
            if wall > WATCHDOG_SECONDS:
                raise RuntimeError(f"{item['item_id']} exceeded the watchdog")
            payload = {"item": item, "item_id": item["item_id"], "result": result, "wall_seconds": wall}
            atomic_write_json(path, payload)
        rows.append(payload)
    return rows


def publish(root, plan, out, *, frozen_plan_commit) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    loaded = {item["item_id"]: read_json(root / "items" / f"{item['item_id']}.json") for item in plan["items"]}
    results = {k: v["result"] for k, v in loaded.items()}
    residual = max(r["stationary_residual"] for r in results.values())
    payload = {
        "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "frozen_predictions": assemble(results),
        "plan_hash": plan["plan_hash"],
        "results": results,
        "round_id": ROUND_ID,
        "schema": "rs-gt.recurrence-tables/v1",
        "validation": {"max_stationary_residual": residual, "ok": residual <= gt0.STATIONARY_RESIDUAL_TOLERANCE},
        "wall_seconds_max": max(v["wall_seconds"] for v in loaded.values()),
    }
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]
