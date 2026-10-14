"""Gravity-time programme, open-thetical Round E0B (prompt GT-P002, OTR 1.0).

Chosen after E0A (gravity-time/reports/gt-e0a-reflection.md section 6). E0A
found stationary arrows only in non-gradient cells that repel probes from the
held source, or at saturation. E0B composes an attractive gradient closure
term with the two unsaturated non-gradient components, at both closure grades
(two equal-ratio pairs), adds a control in which non-gradient rules give a
gradient ratio (PCOMP), a weak closure anchor, and replication of NULL and the
two E0A arrow cells.

One new channel on every cell: event order and projected current in an
emergent hub frame. A toggle of slot e between x and x^e is hub-incident when
e touches a maximum-degree vertex of the edge-present state x | e. The class
is a function of the unordered transition, so a reversible chain gives every
pattern the probability of its reverse in this frame too.

The E0A pipeline (rs_constraint_lab.gte0a.analyse_item) is reused unchanged.
"""

from __future__ import annotations

import itertools
import time

import numpy as np

from rs_constraint_lab import gt0, gte0a
from rs_constraint_lab.state import edges

ROUND_ID = "round-e0b"
EXPERIMENT_ID = "gt-round-e0b-open-thetical"
ANALYSIS_VERSION = "gt-e0b/v1"
MODES = gte0a.MODES
SIZES = gte0a.SIZES

FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {
    "NULL": {"none": []},
    "PATHF": {"weak_suppress": [("path_form", "weak_suppress")]},
    "PATHH": {"weak_favour": [("path_dissolve", "weak_favour")]},
    "CLOSEW": {"weak_favour": [("close_form", "weak_favour")]},
    "PCOMP": {"weak_favour+weak_favour": [("path_form", "weak_favour"), ("path_dissolve", "weak_favour")]},
    "CWPF": {"weak_favour+weak_suppress": [("close_form", "weak_favour"), ("path_form", "weak_suppress")]},
    "CWPH": {"weak_favour+weak_favour": [("close_form", "weak_favour"), ("path_dissolve", "weak_favour")]},
    "CSPF": {"strong_favour+weak_suppress": [("close_form", "strong_favour"), ("path_form", "weak_suppress")]},
    "CSPH": {"strong_favour+weak_favour": [("close_form", "strong_favour"), ("path_dissolve", "weak_favour")]},
}
EQUAL_RATIO_PAIRS = (
    ("CWPF-weak_favour+weak_suppress", "CWPH-weak_favour+weak_favour"),
    ("CSPF-strong_favour+weak_suppress", "CSPH-strong_favour+weak_favour"),
    ("PATHF-weak_suppress", "PATHH-weak_favour"),
)
REPLICATED = ("NULL-none", "PATHF-weak_suppress", "PATHH-weak_favour")
GRADIENT_PARTS = {"CWPF": "CLOSEW-weak_favour", "CWPH": "CLOSEW-weak_favour"}
REPLICATION_TOLERANCE = 1e-12
IDENTITY_TOLERANCE = 1e-9
NON_REVERSIBLE_FLOOR = 1e-6
FRAME_REVERSIBLE_TOLERANCE = 1e-9


def items() -> list[dict]:
    out = []
    for n in SIZES:
        for mode in MODES:
            for family, grades in FAMILIES.items():
                for grade in grades:
                    out.append({"family": family, "grade": grade, "item_id": f"{mode}-N{n}-{family}-{grade}", "mode": mode, "n": n})
    return out


def hub_classes(chain: gte0a.Chain, n: int) -> np.ndarray:
    """Class 1 (hub-incident) or 0 for every (state, slot), from the edge-present state."""
    arrays = gte0a.structure_arrays(chain, n)
    degree = arrays["degree"]
    hubs = degree == degree.max(axis=1, keepdims=True)
    edge_list = edges(n)
    present = np.where(((chain.states[:, None] >> np.arange(chain.n_slots)) & 1) == 1, np.arange(len(chain.states))[:, None], chain.T)
    out = np.zeros((len(chain.states), chain.n_slots), dtype=np.int64)
    for e, (a, b) in enumerate(edge_list):
        j = present[:, e]
        ok = j >= 0
        out[ok, e] = (hubs[j[ok], a] | hubs[j[ok], b]).astype(np.int64)
    return out


def event_order_frame(chain: gte0a.Chain, jump: np.ndarray, n: int, classes: np.ndarray, names: tuple[str, str] = ("N", "H")) -> dict:
    """Event-pair time-reversal asymmetry with transition-symmetric slot classes."""
    edge_list = edges(n)
    P = chain.W / chain.rates[:, None]
    probs: dict[tuple, float] = {}
    for e in range(chain.n_slots):
        ie = chain.T[:, e]
        ok_e = (ie >= 0) & (P[:, e] > 0)
        if not ok_e.any():
            continue
        t1 = np.where(((chain.states >> e) & 1) == 0, 0, 1)
        c1 = classes[:, e]
        after = chain.states ^ (1 << e)
        for f in range(chain.n_slots):
            prob = np.zeros(len(chain.states))
            prob[ok_e] = jump[ok_e] * P[ok_e, e] * P[ie[ok_e], f]
            if not (prob > 0).any():
                continue
            rel = "same" if e == f else ("adjacent" if set(edge_list[e]) & set(edge_list[f]) else "disjoint")
            t2 = np.where(((after >> f) & 1) == 0, 0, 1)
            c2 = np.zeros(len(chain.states), dtype=np.int64)
            c2[ok_e] = classes[ie[ok_e], f]
            code = ((t1 * 2 + c1) * 2 + t2) * 2 + c2
            sums = np.bincount(code, weights=prob, minlength=16)
            for k in np.nonzero(sums)[0]:
                a, rest = divmod(int(k), 8)
                ca, rest = divmod(rest, 4)
                b, cb = divmod(rest, 2)
                key = (a, ca, b, cb, rel)
                probs[key] = probs.get(key, 0.0) + float(sums[k])
    seen = set()
    asym = 0.0
    rows = []
    label = lambda t, c: ("F" if t == 0 else "D") + names[c]
    for key in sorted(probs):
        a, ca, b, cb, rel = key
        rev = (1 - b, cb, 1 - a, ca, rel)
        pair = tuple(sorted([key, rev]))
        if pair in seen or key == rev:
            seen.add(pair)
            continue
        seen.add(pair)
        diff = probs.get(key, 0.0) - probs.get(rev, 0.0)
        asym += abs(diff)
        rows.append({"forward": label(a, ca) + label(b, cb) + ":" + rel, "forward_probability": probs.get(key, 0.0), "reverse": label(1 - b, cb) + label(1 - a, ca) + ":" + rel, "reverse_probability": probs.get(rev, 0.0)})
    rows.sort(key=lambda r: (-abs(r["forward_probability"] - r["reverse_probability"]), r["forward"]))
    return {"pattern_asymmetry": asym, "top_asymmetric_patterns": rows[:6]}


def analyse_item(item: dict) -> tuple[dict, dict | None]:
    result, trajectories = gte0a.analyse_item(item, families=FAMILIES, round_id=ROUND_ID)
    if result.get("regime") != "recurrent" or not result.get("stationary", {}).get("resolved"):
        return result, trajectories
    started = time.perf_counter()
    kernel = gte0a.build(item["family"], item["grade"], item["n"], item["mode"], FAMILIES)
    chain = gte0a.chain_from_kernel(kernel, gt0.start_state(item["n"], item["mode"]))
    stat = gte0a.stationary(chain)
    n = item["n"]
    classes = hub_classes(chain, n)
    arrays = gte0a.structure_arrays(chain, n)
    frame = event_order_frame(chain, stat["jump"], n, classes)
    width = n
    bins = arrays["edges"] * width + arrays["degree"].max(axis=1)
    labels = [f"k{k}m{m}" for k in range(int(arrays["edges"].max()) + 1) for m in range(width)]
    current = gte0a.projected_current(chain, stat["ct"], bins, labels)
    current["projection"] = "(edge count, maximum degree)"
    result["hub_frame"] = {"event_order": frame, "projected_current": current}
    result["timings"]["hub_frame"] = time.perf_counter() - started
    return result, trajectories


# --- plan, execution and publication -------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e0b-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e0b"
TABLES_RELPATH = "gravity-time/reports/round-e0b-tables.json"
E0A_TABLES_RELPATH = gte0a.TABLES_RELPATH
WATCHDOG_SECONDS = 900
ROUND_WALL_CAP_SECONDS = 3 * 3600
ONTOLOGY = gte0a.ONTOLOGY


def prepare_plan() -> dict:
    from rs_constraint_lab.explore08 import plan_hash

    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "gravity-time/reports/gt-e0a-reflection.md section 6 (E0A result commit c31ef92aaf6e5299b9cb15bd7b5c10e768d65f43); live explanations (a) arrow and basin exclusive, (b) grade artefact, (c) projection, (d) kinetics sets basin depth",
        "clocks": "as E0A (rs_constraint_lab.gte0a plan): jump, continuous with event weights as rates, event order on the stationary jump chain",
        "comparisons": {
            "equal_ratio_pairs": [list(p) for p in EQUAL_RATIO_PAIRS],
            "composite_against_gradient_part": GRADIENT_PARTS,
            "notes": "class-level L1 between stationary laws; attachment fraction, detachment, rho, irreversible flux, pattern asymmetries in the source and hub frames, projected currents side by side",
        },
        "e0a_reference": {"plan_commit": "2e5c97e3fdb1f5b2ed18ae652ab6af9f391efdf7", "result_commit": "c31ef92aaf6e5299b9cb15bd7b5c10e768d65f43", "tables": E0A_TABLES_RELPATH},
        "experiment_id": EXPERIMENT_ID,
        "families": {
            family: {
                grade: {
                    "components": [{"grade": g, "K": gte0a.COMPONENT_K[k], "kind": k, "template_example": gte0a.component_expressions(k, 5, g)[0]} for k, g in components],
                    "gradient": gte0a.is_gradient(family, FAMILIES),
                    "predicted_potential": gte0a.predicted_potential(family, grade, FAMILIES),
                }
                for grade, components in grades.items()
            }
            for family, grades in FAMILIES.items()
        },
        "frozen_expectations": {
            "Y1_pcomp_reversible_uniform": f"PCOMP has form and dissolve factors equal on every pair and state (both read only other relations), so rates are symmetric: irreversible flux <= {gte0a.REVERSIBLE_FLUX_TOLERANCE}, real spectrum, and pi_ct uniform on the reachable class (L1 to uniform <= {IDENTITY_TOLERANCE}) in every mode and N",
            "Y2_replication": f"NULL, PATHF weak_suppress and PATHH weak_favour reproduce their E0A class tables (class-level L1 <= {REPLICATION_TOLERANCE}) and E0A irreversible flux fractions within {REPLICATION_TOLERANCE}",
            "Y3_closew_gradient": f"CLOSEW follows the predicted triple-Gibbs law (L1 <= {IDENTITY_TOLERANCE}) and is reversible",
            "Y4_composite_rates_non_gradient": f"every CWPF, CWPH, CSPF, CSPH cell has maximum square affinity > {NON_REVERSIBLE_FLOOR}. Stationary irreversibility (flux) is not predicted: E0A showed rates and flux can separate under saturation",
            "Y5_hub_frame_reversible_null": f"every reversible cell (NULL, CLOSEW, PCOMP) has hub-frame pattern asymmetry <= {FRAME_REVERSIBLE_TOLERANCE} and zero hub-frame projected current within {FRAME_REVERSIBLE_TOLERANCE} (the frame is transition-symmetric)",
        },
        "history": False,
        "initial_conditions": "as E0A",
        "items": items(),
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "observables": {
            "e0a_pipeline": "every E0A observable, unchanged (rs_constraint_lab.gte0a.analyse_item)",
            "hub_frame": "event-pair pattern asymmetry with slot class hub-incident (touches a maximum-degree vertex of the edge-present state) or not; projected net current on (edge count, maximum degree); top patterns and currents",
            "trajectories": "as E0A, seeds sha256('round-e0b:<item_id>:<k>')[:16]",
        },
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "Does any composite raise the attachment fraction above null while carrying irreversible stationary flux (basin and arrow together)?",
            "If so, does the source-relative circulation keep the E0A orientation or reverse?",
            "Do the equal-ratio composite pairs (formation-acting against dissolution-acting non-gradient term) give different basin depths?",
            "Is the FREE-mode arrow legible in the emergent hub frame, and how does hub-frame asymmetry compare with the source frame in HELD?",
            "Does the composite saturate at the strong closure grade?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "note": "E0A tables were read in full (they motivate E0B). Before freezing, the hub-frame channel was exercised only on the synthetic cycle fixture and N=4 fixtures of NULL and CLOSE; one E0A item (HELD-N5-PATHF-weak_suppress) was recomputed after a backward-compatible families parameter was added to gte0a, to confirm the E0A pipeline is unchanged (largest difference 2.8e-10 in a conditional attachment on a 1e-9 mass; otherwise <= 1e-15; tied top-k entries may reorder). No composite, PCOMP or CLOSEW cell at N=5 or N=6 was computed.",
        },
        "programme": "GT",
        "prompt_id": "GT-P002",
        "question": "Can an attractive gradient constraint and a non-gradient constraint together produce a basin with a stationary arrow; does kinetics set basin depth under irreversibility; is direction legible without the held scaffold?",
        "round_id": ROUND_ID,
        "sampling": "exact census of 36 declared cells",
        "schema": "rs-gt.e0b-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte0b", "numpy": np.__version__, "python": __import__("platform").python_version(), "reproducibility_note": "multi-threaded BLAS makes results reproducible to about 1e-15, not bitwise"},
        "stochastic_trajectories": "illustrative_only",
        "stop_conditions": {
            "item": f"an item past the {WATCHDOG_SECONDS}-second watchdog stops the round",
            "round": f"all items written, or the {ROUND_WALL_CAP_SECONDS}-second wall cap",
            "unresolved": "as E0A: unresolved stationary laws are recorded without stationary observables; no post-freeze retuning",
        },
        "tolerances": {"frame_reversible": FRAME_REVERSIBLE_TOLERANCE, "identity": IDENTITY_TOLERANCE, "non_reversible_floor": NON_REVERSIBLE_FLOOR, "replication": REPLICATION_TOLERANCE, "e0a": "as E0A plan"},
        "work_count": {"disk_budget_bytes": 50_000_000, "items": len(items()), "largest_state_space": 32768, "memory_budget_bytes": 4_000_000_000, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "wall_time_estimate_seconds": 600, "watchdog_seconds": WATCHDOG_SECONDS, "workers": 1},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo, commit, *, require_remote=True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("history") is not False or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E0B plan contract drifted")
    return plan


def run(root, plan) -> list[dict]:
    from rs_constraint_lab.durable import atomic_write_json, read_json

    round_started = time.perf_counter()
    rows = []
    for index, item in enumerate(plan["items"], start=1):
        path = root / "items" / f"{item['item_id']}.json"
        if path.is_file() and read_json(path).get("item_id") == item["item_id"]:
            payload = read_json(path)
        else:
            if time.perf_counter() - round_started > ROUND_WALL_CAP_SECONDS:
                raise RuntimeError("round wall cap reached")
            started = time.perf_counter()
            result, trajectories = analyse_item(item)
            wall = time.perf_counter() - started
            if wall > WATCHDOG_SECONDS:
                raise RuntimeError(f"{item['item_id']} exceeded the watchdog ({wall:.1f}s)")
            payload = {"item": item, "item_id": item["item_id"], "result": result, "wall_seconds": wall}
            atomic_write_json(path, payload)
            if trajectories is not None:
                atomic_write_json(root / "trajectories" / f"{item['item_id']}.json", trajectories)
        rows.append(payload)
        atomic_write_json(root / "status.json", {"completed_items": index, "item_count": len(plan["items"]), "last_item_id": item["item_id"], "updated_unix": time.time()})
    return rows


def _held_row(r: dict) -> dict:
    row = gte0a._kinetic_row(r)
    row["expected_edges"] = r["occupancy_ct"]["expected_edges"]
    row["hub_frame_asymmetry"] = r["hub_frame"]["event_order"]["pattern_asymmetry"]
    row["hub_frame_net_current"] = r["hub_frame"]["projected_current"]["net_flux_fraction"]
    row["projected_net_current"] = r["projected_current"]["net_flux_fraction"]
    row["top_projected_currents"] = r["projected_current"]["top_net_currents"][:4]
    if r["mode"] == "HELD":
        hc = r["held_continuous"]
        row["attachment_fraction_ct"] = hc["attachment_fraction"]
        row["attachment_fraction_jump"] = r["held_jump"]["attachment_fraction"]
        row["null_attachment_fraction"] = hc["null_attachment_fraction"]
        row["detached_probability_ct"] = hc["distance_distribution"].get("inf", 0.0)
    return row


def assemble(results: dict[str, dict], e0a_results: dict[str, dict]) -> dict:
    checks: dict[str, dict] = {}
    comparisons: dict[str, dict] = {}
    for key, r in results.items():
        if r.get("regime") != "recurrent" or "reversibility" not in r:
            continue
        fam = r["family"]
        flux = r["reversibility"]["irreversible_flux_fraction"]
        imag = r["spectrum"]["max_abs_imag_relative"] if r.get("spectrum") else None
        if fam == "PCOMP":
            uniform = 1.0 / r["reachable_states"]
            l1 = sum(abs(row["ct"] - row["orbit_size"] * uniform) for row in r["class_table"])
            checks[f"Y1-{key}"] = {"holds": flux <= gte0a.REVERSIBLE_FLUX_TOLERANCE and (imag is None or imag <= gte0a.IMAG_RELATIVE_THRESHOLD) and l1 <= IDENTITY_TOLERANCE, "irreversible_flux_fraction": flux, "l1_to_uniform": l1, "max_abs_imag_relative": imag}
        if fam == "CLOSEW":
            gap = r["predicted_law_l1_gap"]
            checks[f"Y3-{key}"] = {"holds": gap is not None and gap <= IDENTITY_TOLERANCE and flux <= gte0a.REVERSIBLE_FLUX_TOLERANCE, "irreversible_flux_fraction": flux, "l1_gap": gap}
        if fam in ("CWPF", "CWPH", "CSPF", "CSPH"):
            aff = r["reversibility"]["max_square_affinity"]
            checks[f"Y4-{key}"] = {"holds": aff > NON_REVERSIBLE_FLOOR, "irreversible_flux_fraction": flux, "max_square_affinity": aff}
        if fam in ("NULL", "CLOSEW", "PCOMP"):
            hub = r["hub_frame"]
            asym, cur = hub["event_order"]["pattern_asymmetry"], hub["projected_current"]["net_flux_fraction"]
            checks[f"Y5-{key}"] = {"holds": asym <= FRAME_REVERSIBLE_TOLERANCE and cur <= FRAME_REVERSIBLE_TOLERANCE, "hub_frame_net_current": cur, "hub_frame_pattern_asymmetry": asym}
        suffix = f"{r['family']}-{r['grade']}"
        if suffix in REPLICATED:
            old = e0a_results.get(key)
            l1 = gte0a._class_l1(r, old) if old else None
            dflux = abs(flux - old["reversibility"]["irreversible_flux_fraction"]) if old else None
            checks[f"Y2-{key}"] = {"class_l1": l1, "flux_difference": dflux, "holds": l1 is not None and l1 <= REPLICATION_TOLERANCE and dflux <= REPLICATION_TOLERANCE}
    for n in SIZES:
        for mode in MODES:
            prefix = f"{mode}-N{n}-"
            for a, b in EQUAL_RATIO_PAIRS:
                ra, rb = results.get(prefix + a), results.get(prefix + b)
                if ra and rb and "class_table" in ra and "class_table" in rb:
                    comparisons[f"equal_ratio-{mode}-N{n}-{a}|{b}"] = {"class_l1": gte0a._class_l1(ra, rb), a: _held_row(ra), b: _held_row(rb)}
            for fam, part in GRADIENT_PARTS.items():
                composite = [k for k in results if k.startswith(prefix + fam + "-")]
                rp = results.get(prefix + part)
                for key in composite:
                    rc = results[key]
                    if rp and "class_table" in rc and "class_table" in rp:
                        comparisons[f"composite_vs_part-{key}"] = {"class_l1": gte0a._class_l1(rc, rp), "composite": _held_row(rc), "gradient_part": _held_row(rp)}
            for key in [k for k in results if k.startswith(prefix)]:
                r = results[key]
                if "class_table" in r:
                    comparisons.setdefault(f"cells-{mode}-N{n}", {})[key] = _held_row(r)
    return {"comparisons": comparisons, "frozen_expectations": checks}


def publish(root, plan, out, *, frozen_plan_commit, e0a_tables) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    loaded = {item["item_id"]: read_json(root / "items" / f"{item['item_id']}.json") for item in plan["items"]}
    results = {k: v["result"] for k, v in loaded.items()}
    e0a = read_json(e0a_tables)["results"]
    problems = []
    for key, r in results.items():
        if r.get("regime") == "recurrent":
            st = r.get("stationary", {})
            if not st.get("resolved"):
                problems.append(f"{key}: stationary unresolved")
            elif st["residual"] > gte0a.STATIONARY_RESIDUAL_TOLERANCE:
                problems.append(f"{key}: residual")
            if "symmetry_max_abs_difference" in r and r["symmetry_max_abs_difference"] > gte0a.SYMMETRY_TOLERANCE:
                problems.append(f"{key}: symmetry")
    assembled = assemble(results, e0a)
    payload = {
        "analysis_version": ANALYSIS_VERSION,
        "comparisons": assembled["comparisons"],
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "frozen_expectations": assembled["frozen_expectations"],
        "plan_hash": plan["plan_hash"],
        "results": results,
        "round_id": ROUND_ID,
        "schema": "rs-gt.e0b-tables/v1",
        "validation": {"ok": not problems, "problems": problems},
        "wall_seconds_max": max(v["wall_seconds"] for v in loaded.values()),
        "wall_seconds_total": sum(v["wall_seconds"] for v in loaded.values()),
    }
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]
