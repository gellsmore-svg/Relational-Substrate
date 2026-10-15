"""P0 exact passage: calibration, frozen gate, supervised items and reassembly."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

from flint import fmpq as Q

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.gen008m_exec import items as old_items, read, write
from rs_constraint_lab.gen008m_symmetry import MASKS as OPPOSITE_MASKS
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_passage import (
    VERSION, analyse, compare, layers, reconstruct, require, solve_boundary,
)
from rs_constraint_lab.h2_roles import canonical, fingerprint, ln

BASE = "9b2f857687be2ca6867d698fa9eda51db2f788a5"
DIRECTORY = "constraint-lab/exploration/generation-008n"
PLAN = DIRECTORY + "/round-p0-plan.json"
OUTPUT = "constraint-lab/reports/items/generation-008n-p0"
TABLE = "constraint-lab/reports/tables/generation-008n-"
SOURCES = tuple("constraint-lab/src/rs_constraint_lab/" + name for name in (
    "h2_passage.py", "gen008n_exec.py", "h2_roles.py", "gen008m_exec.py", "gen008m_symmetry.py",
    "durable.py", "explore08.py", "graphs.py", "state.py", "history.py", "exact.py")) + ("constraint-lab/pyproject.toml",)
INPUTS = tuple(DIRECTORY + "/" + name for name in (
    "charter.md", "open-thetical-possibilities.md", "predeclared-controls.md", "namespace-audit.json")) + (
    "constraint-lab/provenance/prompts/008N-v0.8n-agent-input.md", "constraint-lab/tests/test_v08n_plumbing.py",
    "constraint-lab/reports/tables/generation-008m-h2-role-atlas.json",
    "constraint-lab/reports/tables/generation-008m-augmented-s4-orbits.json",
    "constraint-lab/reports/tables/generation-008m-m1-opposite-pair.json",
    "constraint-lab/exploration/generation-008m/round-m0-plan.json",
    "constraint-lab/exploration/generation-008m/round-m1-plan.json")


def root():
    return Path(__file__).resolve().parents[3]


def items():
    return [{**row, "source_item_id": row["item_id"], "item_id": row["item_id"].replace("M0-", "P0-")}
            for row in old_items()]


def source_item(item):
    return {key: item[key] for key in ("role", "family", "m")} | {"item_id": item["source_item_id"]}


def source_path(item):
    return "constraint-lab/reports/items/generation-008m-m0/" + item["source_item_id"] + ".json"


def namespace_audit(repository):
    refs = subprocess.check_output(["git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes/origin"],
                                   cwd=repository, text=True).splitlines()
    seen, records, meanings = set(), [], {}
    for ref in refs:
        commit = subprocess.check_output(["git", "rev-parse", ref], cwd=repository, text=True).strip()
        if commit in seen:
            continue
        seen.add(commit)
        path = "constraint-lab/formal/theorem-catalog.jsonl"
        p = subprocess.run(["git", "show", commit + ":" + path], cwd=repository, capture_output=True)
        if p.returncode:
            records.append({"ref": ref, "head": commit, "catalogue": "absent"})
            continue
        entries = [json.loads(line) for line in p.stdout.splitlines()]
        records.append({"ref": ref, "head": commit, "catalogue_sha256": sha256(p.stdout).hexdigest(),
                        "IDs": [r["theorem_id"] for r in entries]})
        for row in entries:
            meanings.setdefault(row["theorem_id"], {}).setdefault(row["statement"], []).append(ref)
    collisions = {key: value for key, value in meanings.items() if len(value) > 1}
    maximum = {prefix: max([int(k[4:]) for k in meanings if k.startswith("CL-" + prefix)] or [0])
               for prefix in "TFNIMQ"}
    value = {"all_accessible_distinct_heads": records, "statement_collisions": collisions,
             "max_used_ids": maximum, "reserved_for_8N": {"T": "85-90", "F": "11", "N": "11"},
             "policy": "No divergent import or historical renumbering. IDs reserved only after accessible-ref audit."}
    write(repository / DIRECTORY / "namespace-audit.json", value)
    print("NAMESPACE", maximum, "collisions", len(collisions), flush=True)


def calibrate(repository):
    require(not (repository / PLAN).exists(), "calibration only before freeze")
    t = time.monotonic()
    value = analyse(repository, old_items()[0], independent=True)
    seconds = time.monotonic() - t
    # Large-denominator dense synthetic equations exercise exact solve costs,
    # without opening a non-neutral ROLE passage cell.
    n = 120
    rows = tuple({j: Q(((i * 17 + j * 31) % 97) + 1, 1) for j in range(n)} for i in range(n))
    rows = tuple({j: v / sum(row.values()) for j, v in row.items()} for row in rows)
    t = time.monotonic()
    solve_boundary(rows, {0: (Q(0),)}, reward=1, independent=True)
    synthetic_seconds = time.monotonic() - t
    write(repository / DIRECTORY / "calibration.json", {
        "new_non_neutral_8N_passage_outputs": 0, "neutral_complete_seconds": seconds,
        "neutral_complete_bytes": len(canonical(value).encode()), "synthetic_dense_120_seconds": synthetic_seconds,
        "historical_regressions": "test_v08m_plumbing.py; published roles only, no new passage output",
        "workers": 1, "numeric_threads": 1, "watchdog_seconds": 900,
        "estimated_total_seconds": 73 * max(10, 20 * seconds, 5 * synthetic_seconds),
        "disk_budget_bytes": 1_000_000_000,
        "reason": "small neutral run plus dense rational synthetic; conservative timeout; preserve and amend on overrun"})
    print("CALIBRATION", seconds, synthetic_seconds, flush=True)


def make_plan(repository):
    require(not (repository / PLAN).exists(), "never replace frozen plan")
    for item in items():
        # This prerequisite revalidates existing kernels/source identities only.
        reconstruct(repository, source_item(item))
    value = {
        "experiment_id": "generation-008n-h2-controlled-passage", "round_id": "P0", "prompt_id": "008N",
        "parent_commit": BASE, "analysis_version": VERSION, "ontology": {"N": 4, "O": 3, "G": 0, "S": 0, "L": 0, "H_pair": 2},
        "clock": "pair-event epoch", "support": "six positive single pair toggles; triads exactly summed out as in 8M",
        "items": items(), "source_hashes": {p: sha256_file(repository / p) for p in SOURCES},
        "input_hashes": {p: sha256_file(repository / p) for p in INPUTS},
        "immutable_8M_item_hashes": {source_path(item): sha256_file(repository / source_path(item)) for item in items()},
        "kernels": "immutable 8M H2 reconstruction and Kpi event rows; no new controller/stationary solve",
        "source_law": "pi2 conditioned C=c; pi1 conditioned C=c; exact labelled and (P,h1) pushforward before passage",
        "layers": layers(), "MFPT_tasks": [(s, t) for names in layers().values() for s in names for t in names if s != t],
        "committor_tasks": [{"source": s, "ordered_targets": [t for t in layers()[3] if t != s]} for s in layers()[3]],
        "return": {"tau": "inf{t>=1:K_t=k}", "kernel": "T_AB (I-T_BB)^-1 T_BA; class aggregate under stationary source",
                   "interpretation": "one return only; class return sequence not assumed Markov",
                   "lengths": [2, 4, 6, 8, 10, 12], "tail": "exact R minus explicit lengths",
                   "routes": ["UP first step k+1", "DOWN first step k-1"],
                   "metrics": ["exact delta/equality", "row JS", "first exact distinguishing slice or tail", "route cancellation"]},
        "hitting": "exact absorbing mean times for all sibling tasks; three K3 ordered competing-target committors",
        "method": "FLINT 0.8.0 fmpq_mat dixon; independently fflu EVERY solve; S4 H2=120 / Kpi=28 verified from full rows",
        "full_validation": "lift every harmonic/reward solution and verify every 2304/384 sparse boundary/equation; exact normalization and nonnegative tail",
        "controls": ["source/target occupancy", "stationary adjacent and first step", "F2 equality", "odd length zero",
                     "nu R = nu", "Kac 1/pi(class)", "neutral all passage null", "all FORM/DISSOLVE complement partners",
                     "R05/R06 opposite-pair transport for all families/grades; target order accounted for"],
        "precision": 160, "logs": "natural/nats", "tolerances": {"all_rational": "exact", "classification": "exact rational zero",
                                                                     "independent_JS_routes": "1e-25"},
        "resources": read(repository / DIRECTORY / "calibration.json"),
        "execution": {"workers": 1, "numeric_threads": 1, "heartbeat_seconds": 5, "watchdog_seconds": 900,
                      "atomic": "fsync/parse/replace via durable API", "resume": "skip only matching item/freeze/source/payload hashes",
                      "retry": "none automatic", "quarantine": "failure receipt, stop and preserve completed items",
                      "split": "only deterministic system x layer, engineering amendment before changed execution; no estimand changes",
                      "merge": "restartable tables from valid items; independently recheck all lifted equations and conjugacy"},
        "pre_freeze_exposure": {"new_non_neutral_8N_passage_outputs": 0,
                                "known": "all 8M kernels/stationary laws and L4+ words; not blind to these",
                                "allowed": "immutable prerequisites, neutral, synthetic, historical regressions, symbolic controls"},
        "outputs": ["return-kernels", "return-lengths", "mfpt", "committor", "summary", "validation"],
    }
    value["plan_hash"] = plan_hash(value)
    write(repository / PLAN, value)
    print("PLAN", value["plan_hash"], sha256_file(repository / PLAN), flush=True)


def gate(repository, freeze):
    plan = require_frozen_plan(repository, freeze, PLAN, repository / PLAN)
    require(remote_contains(repository, freeze), "P0 must be pushed before target execution")
    for path, digest in (plan["source_hashes"] | plan["input_hashes"] | plan["immutable_8M_item_hashes"]).items():
        require(sha256_file(repository / path) == digest, "frozen source/input drift: " + path)
    require(plan["analysis_version"] == VERSION, "P0 analysis version")
    return plan


def valid(path, item, plan, freeze):
    if not path.exists():
        return False
    value = read(path)
    require(value["item"] == item and value["plan_hash"] == plan["plan_hash"] and
            value["frozen_analysis_plan_commit"] == freeze and value["result_hash"] == fingerprint(value["result"]),
            "invalid existing item; never overwrite " + str(path))
    return True


def worker(repository, freeze, identity):
    plan = gate(repository, freeze)
    item = next(i for i in plan["items"] if i["item_id"] == identity)
    path = repository / OUTPUT / (identity + ".json")
    if valid(path, item, plan, freeze):
        print("RESUME", identity, flush=True)
        return
    start = time.monotonic()
    print("PASSAGE", identity, flush=True)
    result = analyse(repository, source_item(item), independent=True)
    payload = {"item": item, "frozen_analysis_plan_commit": freeze, "plan_hash": plan["plan_hash"],
               "source_8M_sha256": plan["immutable_8M_item_hashes"][source_path(item)],
               "result": result, "result_hash": fingerprint(result), "wall_seconds": time.monotonic() - start,
               "status": "VERIFIED"}
    used = sum(p.stat().st_size for p in (repository / OUTPUT).glob("*.json"))
    require(used + len(canonical(payload).encode()) < plan["resources"]["disk_budget_bytes"], "P0 disk budget")
    write(path, payload)
    ln.cache_clear()
    print("DONE", identity, round(payload["wall_seconds"], 3), payload["result_hash"], flush=True)


def run(repository, freeze, only=None):
    plan = gate(repository, freeze)
    for item in plan["items"]:
        identity = item["item_id"]
        if only and identity != only:
            continue
        if valid(repository / OUTPUT / (identity + ".json"), item, plan, freeze):
            print("RESUME", identity, flush=True)
            continue
        start = time.monotonic()
        process = subprocess.Popen([sys.executable, "-m", "rs_constraint_lab.gen008n_exec", "worker", "--freeze", freeze, "--item", identity], cwd=repository)
        while process.poll() is None:
            elapsed = time.monotonic() - start
            write(repository / DIRECTORY / "status.json", {"state": "running", "item": identity, "elapsed_seconds": elapsed,
                                                          "freeze": freeze, "workers": 1})
            if elapsed > plan["execution"]["watchdog_seconds"]:
                process.kill()
                process.wait()
                break
            time.sleep(5)
        if process.returncode:
            write(repository / DIRECTORY / "quarantine" / (identity + ".json"), {
                "item": item, "returncode": process.returncode, "state": "quarantined", "elapsed_seconds": time.monotonic() - start})
            raise RuntimeError("quarantined item; completed items preserved: " + identity)
    write(repository / DIRECTORY / "status.json", {"state": "complete", "freeze": freeze, "items": len(plan["items"])})


def verify_certificates(repository, item, result):
    a, b, controls = reconstruct(repository, source_item(item))
    require(fingerprint(controls) == fingerprint(result["controls"]), "source reconstruction differs")
    for name, chain in (("H2", a), ("Kpi", b)):
        for k, layer in result["layers"].items():
            stored = layer[name]
            names = layers()[int(k)]
            boundary = {s: tuple(Q(c == t) for t in names) for s, c in enumerate(chain.classes) if chain.counts[s] == int(k)}
            values = tuple(tuple(Q(x) for x in row) for row in stored["certificate"]["quotient_values"])
            require(fingerprint(chain.certify(values, boundary)) == fingerprint(stored["certificate"]), "return certificate differs")
        h = result["hitting"][name]
        for target, cert in h["MFPT_certificates"].items():
            values = tuple(tuple(Q(x) for x in row) for row in cert["quotient_values"])
            boundary = {s: (Q(0),) for s, c in enumerate(chain.classes) if c == target}
            require(fingerprint(chain.certify(values, boundary, reward=1)) == fingerprint(cert), "MFPT certificate differs")
        for source, record in h["committors"].items():
            cert = record["certificate"]
            values = tuple(tuple(Q(x) for x in row) for row in cert["quotient_values"])
            boundary = {s: (Q(c == record["target_a"]),) for s, c in enumerate(chain.classes)
                        if c in (record["target_a"], record["target_b"])}
            require(fingerprint(chain.certify(values, boundary)) == fingerprint(cert), "committor certificate differs")


def transport(left, right, mask_map, swap_direction):
    table = pair_classes()
    cmap = {table.name_of[p]: table.name_of[mask_map[p]] for p in table.representatives}
    for model in ("H2", "Kpi"):
        for k, layer in left["layers"].items():
            names = layer[model]["classes"]
            target_k = next(p.bit_count() for p in table.representatives if table.name_of[p] == cmap[names[0]])
            other = right["layers"][str(target_k)][model]
            for source in names:
                for field in ("R", "UP", "DOWN", "tail"):
                    mapped_field = ({"UP": "DOWN", "DOWN": "UP"}.get(field, field) if swap_direction else field)
                    for j, target in enumerate(names):
                        require(Q(layer[model][field][source][j]) == Q(other[mapped_field][cmap[source]][other["classes"].index(cmap[target])]),
                                "passage conjugacy: " + field)
                for n in ("2", "4", "6", "8", "10", "12"):
                    for j, target in enumerate(names):
                        require(Q(layer[model]["lengths"][n][source][j]) ==
                                Q(other["lengths"][n][cmap[source]][other["classes"].index(cmap[target])]), "length conjugacy")
        h, g = left["hitting"][model], right["hitting"][model]
        for target, row in h["MFPT"].items():
            for source, value in row.items():
                require(Q(value) == Q(g["MFPT"][cmap[target]][cmap[source]]), "MFPT conjugacy")
        for source, row in h["committors"].items():
            other = g["committors"][cmap[source]]
            q = Q(other["probability"])
            if other["target_a"] != cmap[row["target_a"]]:
                q = 1 - q
            require(Q(row["probability"]) == q, "committor conjugacy/order")
    return True


def verify_merge(repository, freeze):
    plan = gate(repository, freeze)
    values, summaries, returns, lengths, mfpts, committors = {}, [], [], [], [], []
    for item in plan["items"]:
        path = repository / OUTPUT / (item["item_id"] + ".json")
        require(valid(path, item, plan, freeze), "missing P0 item")
        value = read(path)
        r = value["result"]
        verify_certificates(repository, item, r)
        values[item["item_id"]] = value
        meta = {"system_id": item["item_id"], "role": item["role"], "family": item["family"], "m": item["m"]}
        for k, layer in r["layers"].items():
            for source, row in layer["comparison"].items():
                summaries.append({**meta, "k": int(k), "source": source, **row,
                                  "category_8M": r["controls"]["category_8M"], "KU_equal_8M": r["controls"]["KU_equal_8M"],
                                  "result_hash": value["result_hash"]})
            returns.append({**meta, "k": int(k), **{model: {key: layer[model][key] for key in ("classes", "R", "UP", "DOWN", "nu")}
                                                   for model in ("H2", "Kpi")}, "comparison": layer["comparison"]})
            lengths.append({**meta, "k": int(k), **{model: {key: layer[model][key] for key in ("classes", "lengths", "tail", "odd_zero_hashes")}
                                                   for model in ("H2", "Kpi")}})
        h = r["hitting"]
        for target, row in h["MFPT_differences"].items():
            for source, delta in row.items():
                mfpts.append({**meta, "source": source, "target": target, "difference": delta,
                              "H2": h["H2"]["MFPT"][target][source], "Kpi": h["Kpi"]["MFPT"][target][source],
                              "ratio": h["MFPT_ratios"][target][source]})
        for source, delta in h["committor_differences"].items():
            committors.append({**meta, "source": source, "difference": delta,
                              "target_a": h["H2"]["committors"][source]["target_a"],
                              "target_b": h["H2"]["committors"][source]["target_b"],
                              "H2": h["H2"]["committors"][source]["probability"], "Kpi": h["Kpi"]["committors"][source]["probability"]})
    controls = []
    for role in range(12):
        for grade in ("m025", "m4"):
            a, b = (values[f"P0-{f}-R{role:02d}-{grade}"]["result"] for f in ("FORM", "DISSOLVE"))
            transport(a, b, tuple(p ^ 63 for p in range(64)), True)
            controls.append({"map": "complement", "role": role, "grade": grade, "exact": True})
    for family in ("ANY", "FORM", "DISSOLVE"):
        for grade in ("m025", "m4"):
            a, b = (values[f"P0-{family}-R{role:02d}-{grade}"]["result"] for role in (5, 6))
            transport(a, b, OPPOSITE_MASKS, False)
            controls.append({"map": "opposite_pair", "family": family, "grade": grade, "exact": True})
    data = {"summary": summaries, "return-kernels": returns, "return-lengths": lengths, "mfpt": mfpts, "committor": committors}
    for suffix, rows in data.items():
        write(repository / (TABLE + suffix + ".json"), rows)
    validation = {"status": "VERIFIED", "items": len(values), "plan_hash": plan["plan_hash"], "freeze": freeze,
                  "full_sparse_certificates_reverified": True, "second_exact_route": "fflu EVERY worker solve",
                  "conjugacies": controls, "source_matches": len(values), "F2_matches": len(values) * 3,
                  "Kac_checks": len(values) * 7 * 2,
                  "row_activity": dict(Counter(("active" if r["routing_active"] else "silent") for r in summaries)),
                  "result_hashes": {key: value["result_hash"] for key, value in values.items()},
                  "table_hashes": {suffix: sha256_file(repository / (TABLE + suffix + ".json")) for suffix in data}}
    write(repository / (TABLE + "validation.json"), validation)
    print("VERIFIED", len(values), validation["row_activity"], flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("audit", "calibrate", "plan", "run", "worker", "verify"))
    p.add_argument("--freeze")
    p.add_argument("--item")
    args = p.parse_args()
    repository = root()
    if args.action == "audit": namespace_audit(repository)
    elif args.action == "calibrate": calibrate(repository)
    elif args.action == "plan": make_plan(repository)
    elif args.action == "worker": worker(repository, args.freeze, args.item)
    elif args.action == "run": run(repository, args.freeze, args.item)
    else: verify_merge(repository, args.freeze)


if __name__ == "__main__":
    main()
