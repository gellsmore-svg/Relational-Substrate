"""Atomic, resumable Generation 8F deterministic execution and publication."""

from __future__ import annotations

import csv
import io
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab.durable import (
    atomic_write_bytes, atomic_write_json, atomic_write_text, canonical_json,
    read_json, sha256_bytes, sha256_file,
)
from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan
from rs_constraint_lab.explore08f import (
    ANALYSIS_VERSION, CHECKPOINTS, COMPARATORS, EXPERIMENT_ID, ROUND_ID, SOURCES,
    TOLERANCES, BridgeError, LawSpec, all_laws, analyse_law, build_law_kernel,
    canonical_fingerprint, canonical_law, decomposition, epoch_landing,
    full_transition_matrix, law_fingerprint, law_record, local_table,
    path_event_categories, polarity_conjugacy_check, prepare_f0_plan,
    raw_to_canonical, source_topology_table, stationary_distribution,
)

PLAN_RELPATH = "constraint-lab/exploration/generation-008f/round-f0-plan.json"
SCHEMA = "rs-constraint-lab.bridge-tables/v2"
SOURCE_PATHS = (
    "constraint-lab/src/rs_constraint_lab/explore08f.py",
    "constraint-lab/src/rs_constraint_lab/gen008f_exec.py",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def write_plan(repo: Path | None = None) -> dict:
    root = repo or _repo_root()
    document = prepare_f0_plan()
    document["analysis_source_sha256"] = {path: sha256_file(root / path) for path in SOURCE_PATHS}
    from rs_constraint_lab.explore08 import plan_hash

    document["plan_hash"] = plan_hash(document)
    atomic_write_json(root / PLAN_RELPATH, document)
    # Publish the local and source tables before any global F0 kernel.
    atomic_write_json(root / "constraint-lab/reports/tables/generation-008f-local-matching.json", document["local_matching"])
    atomic_write_json(root / "constraint-lab/reports/tables/generation-008f-source-topology.json", document["source_topology"])
    return document


def require_f0_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan is not on a remote-tracking branch")
    expected = prepare_f0_plan()
    for key, value in expected.items():
        if key != "plan_hash" and plan.get(key) != value:
            raise FrozenPlanError(f"execution refused: plan field {key} drifted")
    for path, digest in plan["analysis_source_sha256"].items():
        if sha256_file(repo / path) != digest:
            raise FrozenPlanError(f"execution refused: analysis source {path} drifted")
    return plan


def law_from_record(record: dict) -> LawSpec:
    return LawSpec(
        record["target_id"], record["model"], record["incidence_motif"],
        record["direction"], record["grade"], record["m"], record["action_pair"],
        tuple(record["condition_triads"]), tuple(record["comparator_parameters"].items()),
        tuple(record["literal_polarities"]),
    )


def cache_key(law: LawSpec) -> str:
    return sha256_bytes(canonical_json({
        "law_fingerprint": canonical_fingerprint(law), "analysis_version": ANALYSIS_VERSION,
        "precision": "80 decimal digits for weights; float64 matrices",
    }).encode())


def worker(spec_path: Path, result_path: Path, matrix_path: Path) -> None:
    spec = read_json(spec_path)
    law = law_from_record(spec["law"])
    result, matrices = analyse_law(law)
    buffer = io.BytesIO()
    np.savez_compressed(buffer, **matrices)
    atomic_write_bytes(matrix_path, buffer.getvalue())
    result["cache_key"] = cache_key(law)
    result["matrix_sha256"] = sha256_file(matrix_path)
    result["plan_hash"] = spec["plan_hash"]
    atomic_write_json(result_path, result)


def _completed_item(result_path: Path, matrix_path: Path, key: str, plan: dict) -> bool:
    if not result_path.exists() or not matrix_path.exists():
        return False
    try:
        result = read_json(result_path)
        return result["cache_key"] == key and result["plan_hash"] == plan["plan_hash"] and result["matrix_sha256"] == sha256_file(matrix_path)
    except (KeyError, ValueError):
        return False


def _run_item(root: Path, law: LawSpec, plan: dict, done: int, total: int) -> tuple[dict, dict]:
    key = cache_key(law)
    directory = root / "items"
    directory.mkdir(parents=True, exist_ok=True)
    result_path, matrix_path = directory / f"{key}.json", directory / f"{key}.npz"
    if not _completed_item(result_path, matrix_path, key, plan):
        spec_path = directory / f"{key}.spec.json"
        atomic_write_json(spec_path, {"law": law_record(law), "plan_hash": plan["plan_hash"]})
        log_path = directory / f"{key}.log"
        started = time.monotonic()
        with log_path.open("wb") as log:
            process = subprocess.Popen(
                [sys.executable, "-m", "rs_constraint_lab.gen008f_exec", "--worker", str(spec_path), str(result_path), str(matrix_path)],
                stdout=log, stderr=subprocess.STDOUT,
            )
            while process.poll() is None:
                elapsed = time.monotonic() - started
                atomic_write_json(root / "status.json", {
                    "stage": "law", "active_item": key, "completed_items": done,
                    "total_items": total, "elapsed_item_seconds": elapsed,
                    "worker_pid": process.pid, "plan_hash": plan["plan_hash"],
                })
                if elapsed > plan["execution"]["watchdog_seconds"]:
                    process.kill()
                    process.wait()
                    raise BridgeError(f"item {key} exceeded 120-second watchdog; retry resumes completed items")
                print(f"F0 heartbeat {done}/{total} {law.model} {law.direction} {law.grade} {elapsed:.1f}s", flush=True)
                try:
                    process.wait(timeout=plan["execution"]["heartbeat_seconds"])
                except subprocess.TimeoutExpired:
                    pass
            if process.returncode:
                raise BridgeError(f"item {key} failed; inspect {log_path}")
        atomic_write_json(directory / f"{key}.timing.json", {"wall_seconds": time.monotonic() - started})
    result = read_json(result_path)
    with np.load(matrix_path, allow_pickle=False) as bundle:
        matrices = {name: bundle[name] for name in bundle.files}
    return result, matrices


def _polarity_prerequisite(laws: list[LawSpec]) -> dict:
    cache = {}
    for law in laws:
        if law.incidence_motif == "BOTH" and law.model == "K3" and law.direction == "form":
            kernel = build_law_kernel(canonical_law(law))
            epoch, _ = epoch_landing(kernel)
            cache[canonical_fingerprint(law)] = {
                "full": full_transition_matrix(kernel), "epoch": epoch,
                "stationary": stationary_distribution(epoch)["pi"],
            }
    return polarity_conjugacy_check(laws, cache)


def execute(root: Path, plan: dict, *, frozen_plan_commit: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    laws = all_laws(plan["drift_roots"])
    print("F0 polarity prerequisite, after freeze", flush=True)
    polarity = _polarity_prerequisite(laws)
    atomic_write_json(root / "polarity-conjugacy.json", polarity)
    representatives = {}
    for law in laws:
        representatives.setdefault(canonical_fingerprint(law), canonical_law(law))
    results, matrices = {}, {}
    for index, (fingerprint, law) in enumerate(representatives.items()):
        result, bundle = _run_item(root, law, plan, index, len(representatives))
        results[fingerprint], matrices[fingerprint] = result, bundle
        print(f"F0 complete {index+1}/{len(representatives)} {law.model} {law.direction} {law.grade}", flush=True)
    payload = assemble(plan, laws, results, matrices, polarity, frozen_plan_commit)
    payload["wall_seconds"] = time.monotonic() - started
    atomic_write_json(root / "round-f0-tables.json", payload)
    verification = verify_payload(root / "round-f0-tables.json")
    if not verification["complete"]:
        raise BridgeError(str(verification["problems"]))
    atomic_write_json(root / "status.json", {"stage": "complete", "completed_items": len(representatives), "total_items": len(representatives), "plan_hash": plan["plan_hash"]})
    return payload


def assemble(plan: dict, laws: list[LawSpec], results: dict, matrices: dict, polarity: dict, commit: str) -> dict:
    local, validation, context, distributions, stationary_distributions = [], [], [], [], []
    equivalence, first, complement = [], [], []
    canonical_kernels = {key: build_law_kernel(canonical_law(law)) for key, law in {canonical_fingerprint(x): x for x in laws}.items()}
    for index, law in enumerate(laws):
        fingerprint = canonical_fingerprint(law)
        result = results[fingerprint]
        raw = build_law_kernel(law)
        canonical = canonical_kernels[fingerprint]
        mapping = raw_to_canonical(law)
        # Check probabilities, not just syntax, for each labelled law.
        exact = all(
            raw.weights[s] == canonical.weights[int(mapping[s])]
            and {int(mapping[t]): p for t, p in raw.successors[s]} == dict(canonical.successors[int(mapping[s])])
            for s in range(1024)
        )
        if not exact:
            raise BridgeError("hidden-bit canonicalisation failed")
        record = law_record(law)
        local.append({**record, **local_table(law)})
        validation.append({"law_id": law_fingerprint(law), "canonical_law_id": fingerprint, "target_id": law.target_id, "model": law.model, **result["numeric_validation"]})
        context.append({"target_id": law.target_id, "model": law.model, **local_table(law), "stationary_pair_event_CMI": result["stationary_pair_event_CMI"], "stationary_post_epoch_conditional_CMI": result["stationary_post_epoch_conditional_CMI"], "context_weighting": result["context_weighting"]})
        equivalence.append({"target_id": law.target_id, "model": law.model, "law_id": law_fingerprint(law), "canonical_law_id": fingerprint, "raw_to_canonical_triad_order": list(law.condition_triads) + [i for i in range(6, 10) if i not in law.condition_triads], "exact_full_kernel_conjugacy_gap": "0", "pair_labels_fixed": True, "uniform_raw_triad_prior_retained": True})
        for row in result["source_distributions"]:
            expanded = {"target_id": law.target_id, "model": law.model, **row}
            distributions.append(expanded)
            if row["checkpoint"] == 1:
                first.append({**expanded, "path_event_categories": path_event_categories(row) if row["source"] == "path" else None})
        stationary_distributions.append({"target_id": law.target_id, "model": law.model, **result["stationary"], "parity_conditioned": result["stationary_by_parity"]})
        print(f"F0 labelled conjugacy {index+1}/48", flush=True)
    checkpoint_rows, stationary_rows, rankings = [], [], []
    d_index = {(r["target_id"], r["model"], r["source"], r["checkpoint"]): r for r in distributions}
    s_index = {(r["target_id"], r["model"]): r for r in stationary_distributions}
    v_index = {(r["target_id"], r["model"]): r for r in validation}
    target_ids = sorted({law.target_id for law in laws})
    for target_id in target_ids:
        for comparator in COMPARATORS:
            for source in SOURCES:
                for checkpoint in CHECKPOINTS:
                    left = d_index[target_id, "K3", source, checkpoint]
                    right = d_index[target_id, comparator, source, checkpoint]
                    checkpoint_rows.append({"target_id": target_id, "comparator": comparator, "source": source, "checkpoint": checkpoint, **decomposition(left["pair_mask"], right["pair_mask"])})
            left, right = s_index[target_id, "K3"], s_index[target_id, comparator]
            k3_residual = v_index[target_id, "K3"]["stationary_residual"]
            comp_residual = v_index[target_id, comparator]["stationary_residual"]
            stationary_rows.append({
                "target_id": target_id, "comparator": comparator,
                "stationary_residual": max(k3_residual, comp_residual),
                "stationary_residual_k3": k3_residual, "stationary_residual_comparator": comp_residual,
                **decomposition(left["pair_mask"], right["pair_mask"]),
                "parity_conditioned_decomposition": {
                    str(parity): decomposition(left["parity_conditioned"][str(parity)]["pair_mask"], right["parity_conditioned"][str(parity)]["pair_mask"])
                    for parity in (0, 1)
                },
            })
        for source in SOURCES:
            for checkpoint in CHECKPOINTS:
                rows = [r for r in checkpoint_rows if r["target_id"] == target_id and r["source"] == source and r["checkpoint"] == checkpoint]
                rankings.append({"target_id": target_id, "source": source, "checkpoint": checkpoint, **{
                    metric: [r["comparator"] for r in sorted(rows, key=lambda x: x[metric])]
                    for metric in ("I_model_pairmask", "I_model_graph_class", "I_model_edgecount", "I_model_shape_given_edgecount", "I_model_label_given_class")
                }})
    # Direction complementation leaves all triad bits unchanged.
    mapping = np.arange(1024) ^ 63
    for law in laws:
        if law.incidence_motif != "BOTH" or law.direction != "form":
            continue
        other = next(x for x in laws if x.incidence_motif == "BOTH" and x.direction == "dissolve" and x.model == law.model and x.grade == law.grade)
        left, right = matrices[canonical_fingerprint(law)], matrices[canonical_fingerprint(other)]
        full_gap = float(np.max(np.abs(left["full"] - right["full"][np.ix_(mapping, mapping)])))
        epoch_gap = float(np.max(np.abs(left["epoch"] - right["epoch"][np.ix_(mapping, mapping)])))
        if max(full_gap, epoch_gap) > TOLERANCES["conjugacy"]:
            raise BridgeError("form/dissolve complement check failed")
        complement.append({"model": law.model, "grade": law.grade, "full_kernel_gap": full_gap, "epoch_kernel_gap": epoch_gap, "state_map": "s xor 63", "same_labelled_source_mapped": False})
    tables = {
        "target_comparator_specs": [law_record(law) for law in laws], "local_matching": local,
        "source_topology": source_topology_table(), "checkpoint_distributions": distributions,
        "checkpoint_bridge": checkpoint_rows, "first_event_topology": first,
        "stationary_bridge": stationary_rows, "stationary_distributions": stationary_distributions,
        "stationary_context": context, "numeric_validation": validation,
        "law_equivalence": equivalence, "comparator_distance_order": rankings,
        "polarity_conjugacy": polarity, "direction_complement": complement,
    }
    payload = {
        "schema": SCHEMA, "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID, "round_id": ROUND_ID,
        "frozen_analysis_plan_commit": commit, "plan_hash": plan["plan_hash"],
        "stochastic_trajectories": False, "tolerances": plan["tolerances"],
        "summary": plan["work_count"], "tables": tables,
    }
    payload["validation"] = {"ok": True, "problems": []}
    return payload


def verify_payload(path: Path) -> dict:
    payload = read_json(path)
    problems = []
    if (payload.get("schema"), payload.get("analysis_version"), payload.get("experiment_id"), payload.get("round_id")) != (SCHEMA, ANALYSIS_VERSION, EXPERIMENT_ID, ROUND_ID):
        problems.append("identity drifted")
    if not payload.get("frozen_analysis_plan_commit") or payload.get("stochastic_trajectories") is not False:
        problems.append("freeze or trajectory declaration missing")
    tables = payload["tables"]
    distributions = tables["checkpoint_distributions"]
    stationary = tables["stationary_distributions"]
    index = {(r["target_id"], r["model"], r["source"], r["checkpoint"]): r for r in distributions}
    s_index = {(r["target_id"], r["model"]): r for r in stationary}
    targets = {r["target_id"] for r in tables["target_comparator_specs"]}
    expected = {(t, c, s, k) for t in targets for c in COMPARATORS for s in SOURCES for k in CHECKPOINTS}
    actual = {(r["target_id"], r["comparator"], r["source"], r["checkpoint"]) for r in tables["checkpoint_bridge"]}
    if len(targets) != 12 or actual != expected or len(tables["checkpoint_bridge"]) != 756 or len(index) != 1008 or len(distributions) != 1008:
        problems.append("checkpoint coverage incomplete or duplicated")
    if len(tables["stationary_bridge"]) != 36 or len(s_index) != 48 or len(stationary) != 48:
        problems.append("stationary coverage incomplete or duplicated")
    for table_name in ("checkpoint_bridge", "stationary_bridge"):
        for row in tables[table_name]:
            if table_name == "checkpoint_bridge":
                key = row["target_id"], row["source"], row["checkpoint"]
                left = index.get((key[0], "K3", key[1], key[2]))
                right = index.get((key[0], row["comparator"], key[1], key[2]))
            else:
                left = s_index.get((row["target_id"], "K3"))
                right = s_index.get((row["target_id"], row["comparator"]))
            if left is None or right is None:
                problems.append("missing projection distributions")
                continue
            calculated = decomposition(left["pair_mask"], right["pair_mask"])
            for field, value in calculated.items():
                if abs(value - row[field]) > TOLERANCES["information_chain_rule"]:
                    problems.append(f"{table_name} {row['target_id']} {field} does not reproduce")
            if max(abs(row["pairmask_chain_gap"]), abs(row["class_chain_gap"])) > TOLERANCES["information_chain_rule"]:
                problems.append("independent chain rule failed")
            if min(row[k] for k in calculated if k.startswith("I_model")) < -TOLERANCES["information_floor"]:
                problems.append("negative information beyond floor")
    local = {(r["target_id"], r["model"]): r for r in tables["local_matching"]}
    for target in targets:
        for model in ("K3", *COMPARATORS):
            row = local.get((target, model))
            if row is None:
                problems.append("local row missing")
                continue
            expected_delta = math_log_fraction(row["m"]) if model == "K3" else 0
            if abs(row["local_delta12"] - expected_delta) > TOLERANCES["logit_second_difference"]:
                problems.append("local interaction order failed")
        if (target, "K3") in local and (target, "DRIFT") in local:
            for field in ("balanced_action_probability", "balanced_edge_drift"):
                if abs(local[target, "K3"][field] - local[target, "DRIFT"][field]) > TOLERANCES["drift_balanced_action_match"]:
                    problems.append("DRIFT match failed")
    for row in tables["numeric_validation"]:
        for field, tolerance in (
            ("row_sum_error", "kernel_row_sum"), ("epoch_row_sum_error", "kernel_row_sum"),
            ("reference_probability_gap", "float_local_probability_gap"),
            ("epoch_kernel_residual", "epoch_solve_residual"),
            ("stationary_residual", "stationary_residual"),
        ):
            if row[field] > TOLERANCES[tolerance]:
                problems.append(f"{row['law_id']} {field} exceeds tolerance")
        if row["communicating_classes"] != 1 or row["stationary_min_entry"] < -TOLERANCES["stationary_nonnegative"]:
            problems.append("invalid stationary interpretation")
    if not tables["polarity_conjugacy"]["holds"]:
        problems.append("polarity prerequisite failed")
    return {"complete": not problems, "missing_count": len(problems), "problems": problems}


def math_log_fraction(value: str) -> float:
    import math
    from fractions import Fraction

    return math.log(float(Fraction(value)))


def _csv(rows: list[dict]) -> str:
    buffer = io.StringIO()
    columns = list(dict.fromkeys(key for row in rows for key in row))
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: canonical_json(value) if isinstance(value, (dict, list)) else value for key, value in row.items()})
    return buffer.getvalue()


def publish_tables(payload: dict, reports: Path) -> dict[str, str]:
    directory = reports / "tables"
    hashes = {}
    for name, rows in payload["tables"].items():
        path = directory / f"generation-008f-{name.replace('_', '-')}.json"
        atomic_write_json(path, rows)
        hashes[name] = sha256_file(path)
        if name in ("checkpoint_bridge", "stationary_bridge", "local_matching", "source_topology", "stationary_context", "numeric_validation", "direction_complement"):
            atomic_write_text(path.with_suffix(".csv"), _csv(rows))
    summary = {key: value for key, value in payload.items() if key != "tables"}
    summary["detail_sha256"] = hashes
    atomic_write_json(reports / "generation-008f-round-f0-tables.json", summary)
    return hashes


if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "--worker":
        raise SystemExit("internal invocation: --worker spec.json result.json matrices.npz")
    worker(*(Path(value) for value in sys.argv[2:]))

