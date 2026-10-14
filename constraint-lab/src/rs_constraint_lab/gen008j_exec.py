"""Frozen, durable analysis-only Generation 8J coarse-process execution."""

from __future__ import annotations

import argparse
import gzip
import json
import signal
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.coarse_process import (
    CLOCK, FLOOR, LENGTHS, ORIENTATION, analyse, complement_class_map,
    edge_map, published_models,
)
from rs_constraint_lab.durable import (
    atomic_write_bytes, atomic_write_json, canonical_json, read_json,
    sha256_bytes, sha256_file,
)
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.history import HistoryError, PRECISION

BASE = "6615c9f03a1fa30558f8cf519a125e610d393f31"
VERSION = "generation-008j-coarse-process/v1"
DIRECTORY = "constraint-lab/exploration/generation-008j"
PLAN = DIRECTORY + "/round-j0-plan.json"
MANIFEST = "constraint-lab/reports/generation-008j-round-j0-tables.json"
OUTPUT = "constraint-lab/reports/items/generation-008j"
CALIBRATION = DIRECTORY + "/calibration.json"
TABLES = "constraint-lab/reports/tables/generation-008j-"
CROSSCHECK_FEATURES = ("SAME_ANY", "FORM_ANY", "SAME_FORM", "ADJ_FORM", "DISJ_FORM")
INPUTS = tuple("constraint-lab/reports/tables/generation-008i-" + name + ".json" for name in (
    "kernels", "stationary-distributions", "controller-catalog", "neutral",
)) + (
    "constraint-lab/reports/generation-008i-round-i0-tables.json",
    "constraint-lab/exploration/generation-008i/structural-orbits.json",
    "research-methods/open-thetical-research.md",
    "constraint-lab/methodology/open-thetical-application.md",
    DIRECTORY + "/charter.md", DIRECTORY + "/open-thetical-possibilities.md",
)
SOURCES = tuple("constraint-lab/src/rs_constraint_lab/" + name for name in (
    "coarse_process.py", "gen008j_exec.py", "gen008i_exec.py", "history.py",
    "history_roles.py", "role_atlas.py", "graphs.py", "state.py", "durable.py",
    "explore08.py", "exact.py", "memory_clocks.py", "coherence.py",
))


def repository_root():
    return Path(__file__).resolve().parents[3]


def digest(value):
    return sha256_bytes(canonical_json(value).encode())


def serial_words(document):
    return json.loads(canonical_json(document))


def item_name(controller):
    return controller.replace("I0-", "J0-", 1)


def load_word_file(root, envelope):
    path = root / envelope["word_path"]
    if sha256_file(path) != envelope["word_sha256"]:
        raise HistoryError("compressed word digest mismatch")
    data = gzip.decompress(path.read_bytes())
    if sha256_bytes(data) != envelope["uncompressed_word_sha256"]:
        raise HistoryError("uncompressed word digest mismatch")
    return json.loads(data)


def validate_result(result):
    if result["clock"] != CLOCK or result["precision_decimal_digits"] != PRECISION:
        raise HistoryError("clock/precision drift")
    if len(result["word_atlas"]) != 12 or len(result["process_information"]) != 6:
        raise HistoryError("incomplete frozen word lengths")
    for row in result["word_atlas"]:
        if row["word_length"] <= 2 and not row["exact_equal"]:
            raise HistoryError("mandatory matched controls failed")
        if row["reachable_words_H"] != row["reachable_words_Kpi"]:
            raise HistoryError("positive common toggle support unexpectedly changed")
    for row in result["process_information"]:
        if Decimal(row["chain_gap"]) > FLOOR:
            raise HistoryError("information-chain defect")
    for key, value in result["validation"].items():
        if key.endswith("_gap") and Fraction(value):
            raise HistoryError(f"exact validation defect: {key}")


def calibrate(root):
    if (root / PLAN).exists():
        raise HistoryError("calibration must precede J0 freeze")
    model = published_models(root)["I0-NEUTRAL"]
    start = time.monotonic()
    result, words = analyse(model, independent=True)
    wall = time.monotonic() - start
    validate_result(result)
    raw = canonical_json(words).encode()
    counts = {label: result["diagnostics"][label]["work"]["reachable_words"] for label in ("H", "Kpi")}
    record = {
        "clock": CLOCK, "fixture": "published neutral only", "actual_A_C_target_word_analyses": 0,
        "B_used_for_prefreeze_words": False, "wall_seconds": wall,
        "neutral_word_file_bytes": len(raw), "neutral_word_gzip_bytes": len(gzip.compress(raw, mtime=0)),
        "reachable_graphclass_words": counts,
        "reachable_edge_words": {str(row["word_length"]): row["reachable_words_H"] for row in result["word_atlas"] if row["projection"] == "edge_count"},
        "forward_work": {label: result["diagnostics"][label]["work"]["forward_updates"] for label in ("H", "Kpi")},
        "independent_hidden_path_visits": {label: result["diagnostics"][label]["independent_hidden_path_visits"] for label in ("H", "Kpi")},
        "bound_justification": "All published systems have identical positive toggle support and positive stationary laws; neutral reachable-word counts are exact support counts for every item.",
    }
    atomic_write_json(root / CALIBRATION, record)
    return record


def write_plan(root):
    calibration = read_json(root / CALIBRATION)
    models = published_models(root)
    if len(models) != 23:
        raise HistoryError("8I palette drift")
    items = [{"item_id": item_name(key), "controller_id": key,
              "independent_hidden_path_crosscheck": key == "I0-NEUTRAL" or model.get("feature") in CROSSCHECK_FEATURES}
             for key, model in sorted(models.items())]
    plan = {
        "round_id": "J0", "analysis_version": VERSION, "parent_commit": BASE,
        "mode": "B / OpenThetical analysis-only", "clock": CLOCK, "orientation": ORIENTATION,
        "word_lengths": LENGTHS, "projections": ["graph_class", "edge_count"],
        "models": ["true stationary H role quotient", "published stationary Kpi graph-class quotient"],
        "items": items, "cross_model_items": ["J0-COMPLEMENT-VALIDATION"],
        "method_source": {"path": "research-methods/open-thetical-research.md",
                          "sha256": "2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd",
                          "resolved_ref": "05b15b0d903d46070b99ac84f9cab1bd898046ba"},
        "ontology": {"N": 4, "O": 3, "G": 0, "S": 0, "L": 0, "H_pair": 1, "hypergraph": "independent"},
        "new_controllers": 0, "new_grades": 0, "new_stationary_solves": 0, "stochastic_scientific_trajectories": 0,
        "arithmetic": {"probabilities": "exact fractions", "information_decimal_digits": PRECISION, "log": "natural", "unit": "nats"},
        "estimands": [
            "sparse exact H/Kpi class and edge words L1..6, support counts, equal-prior word JS",
            "direct conditional shape-sequence model information and independent chain gap",
            "H role->class and role->edge strong lumpability; Kpi S4/material->class/class->edge",
            "stationary triple CMI for each model/projection, exact conditional-independence flag",
            "finite-depth conditional-row residuals for candidate orders 1..4 using L3..6; no all-past claim from zero",
            "first positive word-information length at frozen 1e-25 floor, exact equality separately",
            "complete rational triples with differences and individual JS contributions",
            "posterior role endpoint-support min/max only; role MI/entropy not opened",
        ],
        "controls": [
            "exact word normalisation and stationary initialisation",
            "L1/L2 H=Kpi all systems; B/neutral all frozen lengths with passive-register all-length proof",
            "Kpi exact S4 covariance and all-member 11-class quotient check in every item",
            "class-to-edge words equal separately computed direct edge DP",
            "independent recursive hidden-path summation for neutral and ten feature/grade items, all L1..6",
            "complement word probability equality H and Kpi across all retained partners and lengths",
            "content hashes, deterministic word sorting, gzip mtime=0, independent reassembly",
        ],
        "tolerances": {"rational_identities": "exact", "quotient_and_covariance": "exact",
                       "information_chain": "1e-25", "process_information_floor_nats": "1e-25",
                       "complement_probabilities": "exact", "independent_words": "exact"},
        "pre_freeze_exposure": {
            "actual_A_C_target_word_analyses": 0, "neutral_calibration": True, "synthetic_fixtures": True,
            "B_word_calibration": False, "known_8I_inputs": "all published stationary/kernel observations",
            "symbolic_proofs": "user-predeclared matching, covariance, passive-register paths, chain rule, invariant-window label silence",
        },
        "work_counts": {
            "model_items": 23, "cross_model_items": 1, "total_items": 24,
            "model_projection_length_rows": 23 * 2 * 6, "process_decomposition_rows": 23 * 6,
            "Kpi_covariance_transition_comparisons": 23 * 24 * 64 * 6,
            "finite_depth_checks": 23 * 2 * 2 * 4,
            "independent_items": sum(item["independent_hidden_path_crosscheck"] for item in items),
            "per_item_reachable_class_words": calibration["reachable_graphclass_words"],
            "per_item_reachable_edge_words": calibration["reachable_edge_words"],
            "per_item_forward_updates": calibration["forward_work"],
            "support_counts_are_exact_bounds": True,
        },
        "runtime_disk": {"neutral_calibration_seconds": calibration["wall_seconds"],
                         "estimated_total_seconds": max(60, calibration["wall_seconds"] * 23 * 30),
                         "hard_per_item_seconds": 120, "disk_budget_bytes": 512_000_000,
                         "workers": 1, "safe_resume": "reuse only hash-valid complete item and word envelopes",
                         "on_overrun": "stop, preserve completed items, freeze amendment before changing scope/budget"},
        "source_sha256": {path: sha256_file(root / path) for path in SOURCES},
        "input_sha256": {path: sha256_file(root / path) for path in INPUTS},
        "calibration_sha256": sha256_file(root / CALIBRATION),
    }
    plan["plan_hash"] = plan_hash(plan)
    if (root / PLAN).exists():
        raise HistoryError("refusing to replace existing plan")
    atomic_write_json(root / PLAN, plan)
    return plan


def require_execution(root, commit):
    plan = require_frozen_plan(root, commit, PLAN, root / PLAN)
    if not remote_contains(root, commit):
        raise FrozenPlanError("J0 plan must be pushed before target execution")
    if plan["analysis_version"] != VERSION or tuple(plan["word_lengths"]) != LENGTHS:
        raise FrozenPlanError("analysis semantics drift")
    for field in ("source_sha256", "input_sha256"):
        for path, value in plan[field].items():
            if sha256_file(root / path) != value:
                raise FrozenPlanError(f"J0 frozen artifact drift: {path}")
    if sha256_file(root / CALIBRATION) != plan["calibration_sha256"]:
        raise FrozenPlanError("calibration drift")
    return plan


def load_envelope(root, item, plan, commit):
    path = root / OUTPUT / (item["item_id"] + ".json")
    value = read_json(path)
    if value["item"] != item or value["plan_hash"] != plan["plan_hash"] or value["frozen_analysis_plan_commit"] != commit:
        raise HistoryError("item freeze mismatch")
    if value["analysis_version"] != VERSION or digest(value["result"]) != value["result_sha256"]:
        raise HistoryError("item content digest mismatch")
    validate_result(value["result"])
    load_word_file(root, value)
    return value


def complement_validation(root, envelopes):
    values = {}
    for value in envelopes:
        words = load_word_file(root, value)
        values[value["result"]["controller_id"]] = (value["result"], words)
    checks = []
    class_map = complement_class_map()
    for key, (result, words) in sorted(values.items()):
        feature = result["feature"]
        partner_feature = feature.replace("FORM", "TEMP").replace("DISSOLVE", "FORM").replace("TEMP", "DISSOLVE") if feature else None
        partner = key if key == "I0-NEUTRAL" or result["family"] == "A" else key.replace(feature, partner_feature)
        target = values[partner][1]
        rows_checked = 0
        for left, right in zip(words["words"], target["words"]):
            mapping = class_map if left["projection"] == "graph_class" else {i: 6-i for i in range(7)}
            transformed = {tuple(mapping[y] for y in row["word"]): (row["P_H"], row["P_Kpi"]) for row in left["rows"]}
            expected = {tuple(row["word"]): (row["P_H"], row["P_Kpi"]) for row in right["rows"]}
            if transformed != expected:
                raise HistoryError(f"complement word identity failed: {key}")
            rows_checked += len(expected)
        checks.append({"controller_id": key, "partner": partner, "clock": CLOCK,
                       "exact_probability_gap": "0/1", "word_rows_checked": rows_checked})
    return checks


def publish(root, envelopes, plan, commit):
    complement = complement_validation(root, envelopes)
    tables = {"word-atlas": [], "process-information": [], "lumpability": [], "triples": [], "validation": []}
    for envelope in envelopes:
        result = envelope["result"]
        common = {"controller_id": result["controller_id"], "clock": CLOCK}
        tables["word-atlas"].extend(dict(row, **common) for row in result["word_atlas"])
        tables["process-information"].extend(dict(row, **common) for row in result["process_information"])
        tables["lumpability"].append(dict(common, diagnostics=result["diagnostics"], first_visible_word_length=result["first_visible_word_length"]))
        tables["triples"].append(dict(common, orientation=ORIENTATION, projections=result["triples"]))
        tables["validation"].append(dict(common, **result["validation"]))
    hashes = {}
    for name, data in tables.items():
        path = TABLES + name + ".json"
        atomic_write_json(root / path, {"clock": CLOCK, "orientation": ORIENTATION, "rows": data})
        hashes[path] = sha256_file(root / path)
    path = TABLES + "complement.json"
    atomic_write_json(root / path, {"clock": CLOCK, "checks": complement})
    hashes[path] = sha256_file(root / path)
    files = {}
    for envelope in envelopes:
        path = OUTPUT + "/" + envelope["item"]["item_id"] + ".json"
        files[path] = sha256_file(root / path)
        files[envelope["word_path"]] = envelope["word_sha256"]
    summary = {
        "round_id": "J0", "status": "COMPLETE", "analysis_version": VERSION,
        "clock": CLOCK, "orientation": ORIENTATION, "word_lengths": LENGTHS,
        "frozen_analysis_plan_commit": commit, "plan_hash": plan["plan_hash"],
        "plan_file_sha256": sha256_file(root / PLAN), "item_sha256": files, "table_sha256": hashes,
        "model_items": len(envelopes), "cross_model_items": 1, "new_stationary_solves": 0,
        "stochastic_scientific_trajectories": 0, "information_decimal_digits": PRECISION,
        "timings": {e["item"]["item_id"]: e["wall_seconds"] for e in envelopes},
    }
    atomic_write_json(root / MANIFEST, summary)
    return summary


def execute(root, commit):
    plan = require_execution(root, commit)
    models = published_models(root)
    envelopes = []
    output = root / OUTPUT
    output.mkdir(parents=True, exist_ok=True)

    def timeout(signum, frame):
        raise TimeoutError("120-second J0 item watchdog: preserve prior valid items; amendment required")

    prior = signal.signal(signal.SIGALRM, timeout)
    try:
        for position, item in enumerate(plan["items"]):
            path = output / (item["item_id"] + ".json")
            if path.exists():
                envelopes.append(load_envelope(root, item, plan, commit))
                print("RESUMED", item["item_id"], flush=True)
                continue
            atomic_write_json(root / DIRECTORY / "status.json", {"status": "RUNNING", "active_item": item["item_id"], "completed": position, "total": 23})
            started = time.monotonic()
            signal.alarm(plan["runtime_disk"]["hard_per_item_seconds"])
            result, words = analyse(models[item["controller_id"]], independent=item["independent_hidden_path_crosscheck"])
            validate_result(result)
            signal.alarm(0)
            word_path = OUTPUT + "/" + item["item_id"] + "-words.json.gz"
            raw = canonical_json(words).encode()
            atomic_write_bytes(root / word_path, gzip.compress(raw, mtime=0))
            envelope = {
                "item": item, "analysis_version": VERSION, "plan_hash": plan["plan_hash"],
                "frozen_analysis_plan_commit": commit, "result": result, "result_sha256": digest(result),
                "word_path": word_path, "word_sha256": sha256_file(root / word_path),
                "uncompressed_word_sha256": sha256_bytes(raw), "wall_seconds": time.monotonic() - started,
            }
            atomic_write_json(path, envelope)
            if sum(p.stat().st_size for p in output.iterdir() if p.is_file()) > plan["runtime_disk"]["disk_budget_bytes"]:
                raise HistoryError("frozen disk budget exceeded: stop and amend")
            envelopes.append(serial_words(envelope))
            print("COMPLETE", item["item_id"], f"{envelope['wall_seconds']:.3f}s", flush=True)
        result = publish(root, envelopes, plan, commit)
        atomic_write_json(root / DIRECTORY / "status.json", {"status": "COMPLETE", "completed": 23, "cross_model_items": 1})
        return result
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, prior)


def verify(root, commit):
    plan = require_execution(root, commit)
    summary = read_json(root / MANIFEST)
    if summary["status"] != "COMPLETE" or summary["plan_hash"] != plan["plan_hash"] or summary["model_items"] != 23:
        raise HistoryError("incomplete frozen publication")
    for path, value in {**summary["item_sha256"], **summary["table_sha256"]}.items():
        if sha256_file(root / path) != value:
            raise HistoryError(f"published digest mismatch: {path}")
    envelopes = []
    for item in plan["items"]:
        envelope = load_envelope(root, item, plan, commit)
        words = load_word_file(root, envelope)
        for block in words["words"]:
            rows = block["rows"]
            if rows != sorted(rows, key=lambda row: row["word"]):
                raise HistoryError("word canonicalisation drift")
            for model in ("P_H", "P_Kpi"):
                if sum(Fraction(row[model]) for row in rows) != 1:
                    raise HistoryError("independent published word normalisation failed")
            equal = all(row["P_H"] == row["P_Kpi"] for row in rows)
            if block["word_length"] <= 2 and not equal:
                raise HistoryError("independent matched control failed")
            if ("-FORM_ANY-" in item["item_id"] or "-DISSOLVE_ANY-" in item["item_id"] or item["item_id"] == "J0-NEUTRAL") and not equal:
                raise HistoryError("independent passive-register path control failed")
        envelopes.append(envelope)
    expected = complement_validation(root, envelopes)
    actual = read_json(root / (TABLES + "complement.json"))["checks"]
    if expected != actual:
        raise HistoryError("independent complement reassembly differs")
    return {"status": "VERIFIED", "model_items": 23, "cross_model_items": 1, "plan_hash": plan["plan_hash"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("calibrate", "plan", "execute", "verify"))
    parser.add_argument("--frozen-plan-commit")
    args = parser.parse_args()
    root = repository_root()
    if args.command == "calibrate":
        result = calibrate(root)
    elif args.command == "plan":
        result = write_plan(root)
    elif args.command == "execute":
        result = execute(root, args.frozen_plan_commit)
    else:
        result = verify(root, args.frozen_plan_commit)
    print(json.dumps(result, default=str, sort_keys=True))


if __name__ == "__main__":
    main()
