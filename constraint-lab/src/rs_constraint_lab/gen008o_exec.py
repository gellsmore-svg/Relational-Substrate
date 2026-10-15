"""F0: gated, durable derived factor census; no new stochastic process."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import time

from flint import fmpq as Q

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.gen008m_exec import read, write
from rs_constraint_lab.gen008m_symmetry import MASKS, OPPOSITE
from rs_constraint_lab.gen008n_exec import items as passage_items
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_passage import layers, require
from rs_constraint_lab.h2_roles import STATES, fingerprint, canonical
from rs_constraint_lab.stopping_factorization import VERSION, analyse, matrix, setup

BASE = "e650d71bda7203c8018d8bd134c5496a03d74a11"
HUB = "38c2501bbab22ca1eb2288ea76a962ac0170d5e6"
DIRECTORY = "constraint-lab/exploration/generation-008o"
PLAN = DIRECTORY + "/round-f0-plan.json"
OUTPUT = "constraint-lab/reports/items/generation-008o-f0"
TABLE = "constraint-lab/reports/tables/generation-008o-"
SOURCES = tuple("constraint-lab/src/rs_constraint_lab/" + name for name in (
    "stopping_factorization.py", "gen008o_exec.py", "h2_passage.py", "gen008n_exec.py", "h2_roles.py",
    "gen008m_exec.py", "gen008m_symmetry.py", "durable.py", "explore08.py", "graphs.py", "state.py", "history.py", "exact.py"))
INPUTS = tuple(DIRECTORY + "/" + name for name in (
    "charter.md", "open-thetical-possibilities.md", "predeclared-algebra.md", "namespace-audit.json", "calibration.json")) + (
    "constraint-lab/provenance/prompts/008O-v0.8o-agent-input.md",
    "constraint-lab/provenance/synthesis-context/008O.json", "constraint-lab/tests/test_v08o_plumbing.py",
    "constraint-lab/pyproject.toml", "constraint-lab/exploration/generation-008n/round-p0-plan.json",
    "constraint-lab/reports/generation-008n-p0-tables.json",
    "constraint-lab/reports/tables/generation-008m-augmented-s4-orbits.json",
    "constraint-lab/reports/tables/generation-008m-h2-role-atlas.json",
    "constraint-lab/reports/tables/generation-008m-m1-opposite-pair.json")


def root():
    return Path(__file__).resolve().parents[3]


def items():
    return [{**i, "source_passage_id": i["item_id"], "item_id": i["item_id"].replace("P0-", "F0-")}
            for i in passage_items()]


def audit(repository):
    refs = subprocess.check_output(["git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes/origin"], cwd=repository, text=True).splitlines()
    seen, records, meanings = set(), [], defaultdict(dict)
    for ref in refs:
        head = subprocess.check_output(["git", "rev-parse", ref], cwd=repository, text=True).strip()
        if head in seen:
            continue
        seen.add(head)
        p = subprocess.run(["git", "show", head + ":constraint-lab/formal/theorem-catalog.jsonl"], cwd=repository, capture_output=True)
        if p.returncode:
            records.append({"ref": ref, "head": head, "catalogue": "absent"})
            continue
        rows = [__import__("json").loads(line) for line in p.stdout.splitlines()]
        records.append({"ref": ref, "head": head, "sha256": sha256(p.stdout).hexdigest(), "IDs": [r["theorem_id"] for r in rows]})
        for row in rows:
            meanings[row["theorem_id"]].setdefault(row["statement"], []).append(ref)
    maxima = {prefix: max([int(k[4:]) for k in meanings if k.startswith("CL-" + prefix)] or [0]) for prefix in "TFNIMQ"}
    write(repository / DIRECTORY / "namespace-audit.json", {"distinct_heads": records, "statement_collisions": {k: v for k, v in meanings.items() if len(v) > 1},
        "max_used_ids": maxima, "reservation": {"T": "91-95", "F": "12", "M": "07"},
        "policy": "branch-qualified historical IDs preserved; no divergent import; new IDs above every accessible maximum"})
    print("AUDIT", maxima, flush=True)


def calibrate(repository):
    require(not (repository / PLAN).exists(), "calibration before freeze only")
    start = time.monotonic()
    value = analyse(repository, items()[0])
    seconds = time.monotonic() - start
    write(repository / DIRECTORY / "calibration.json", {"neutral_seconds": seconds, "neutral_bytes": len(canonical(value).encode()),
        "new_non_neutral_8O_factor_diagnostics": 0, "workers": 1, "numeric_threads": 1,
        "estimated_seconds": 73 * max(10, 30 * seconds), "disk_budget_bytes": 1_000_000_000,
        "timeout_seconds": 300, "fixtures": "test_v08o_plumbing.py: neutral and synthetic noncommuting rational chains only",
        "historical_regressions": "published 8N source reconstruction and immutable neutral route certificates; no new non-neutral factor outputs"})
    print("CALIBRATION", seconds, flush=True)


def make_plan(repository):
    require(not (repository / PLAN).exists(), "never overwrite a frozen plan")
    reused = []
    for item in items():
        reused.extend(["constraint-lab/reports/items/generation-008m-m0/" + item["source_item_id"] + ".json",
                       "constraint-lab/reports/items/generation-008n-p0/" + item["source_passage_id"] + ".json"])
    reused += [str(p.relative_to(repository)) for p in (repository / "constraint-lab/reports/tables").glob("generation-008n-*.json")]
    value = {"experiment_id": "generation-008o-route-null-factorization", "round_id": "F0", "prompt_id": "008O", "parent_commit": BASE,
        "analysis_version": VERSION, "hub_context_commit": HUB, "hub_records": ["X::0001", "X::0009", "XQ::01", "XQ::07"],
        "hub_authority": "read-only planning context; not CL evidence; no hub mutation or GT test",
        "items": items(), "non_neutral_source_route_count": 1008, "neutral_source_route_count": 14,
        "source_hashes": {p: sha256_file(repository / p) for p in SOURCES}, "input_hashes": {p: sha256_file(repository / p) for p in INPUTS},
        "reused_hashes": {p: sha256_file(repository / p) for p in sorted(set(reused))},
        "orientation": "row distributions; T row stochastic; C:ZxS, L:SxZ; Pi=C L; LC=I; Kpi=L T C",
        "stopping": "A=count k, k=2,3,4; B complement; independent route blocks B_UP=count>k / B_DOWN=count<k; complete side domain",
        "source": "stationary conditional on current material class; a_d=mu1 L_A T_AB^d; route-joint (not route-conditioned) rows",
        "operators": {"Q": "T_BB", "Ares": "(I-Q)^-1", "Mres": "(I-Q Pi_B)^-1", "Rexit": "T_BA G",
            "identity": "Ares-Pi_B Mres=Ares(I-Pi_B)Mres", "U": "a_d Ares(I-Pi_B)", "V": "Mres Rexit", "W": "(I-Pi_B)V", "defect": "Delta=U V=U W"},
        "method": "reuse pinned 8N harmonic certificates; V=Rexit+Q lift(g1), verify Pi V=lift(g1) and (I-QPi)V=Rexit; new left occupation solve only",
        "validation": "Dixon plus independent fflu EVERY new solve; exact equations lifted to all original sparse states; reproduce published route/F4 rows; toy full-matrix resolvent identity",
        "taxonomy": {"ACTIVE": "UV!=0", "N0_UPSTREAM_ANNIHILATION": "U=0", "N1_TARGET_INSENSITIVITY": "U!=0,W=0 on complete route side",
            "N2_BILINEAR_ORTHOGONALITY": "U!=0,W!=0,UV=0", "refinements": ["orbitwise zero", "fibrewise cancellation", "signed bilinear cancellation", "explicit involution pairing if exactly certified"]},
        "ranks": "full rank(I-Pi)=|Z_B|-|S_B|; same for Ares(I-Pi); independently exact invariant-sector projection rank, invariant W column rank, U/source-target map ranks; do not conflate sector/full ranks",
        "contributions": "complete ordered orbit list; U orbit MASS times W invariant VALUE per target; sparse nonzero contribution records with sign/absolute numerator/denominator and exact sum; no importance ranking",
        "symmetries": "all FORM/DISSOLVE complement partners; opposite-pair all families/roles/grades, R05<->R06; transform kernel/reset, route and target alphabets, all factors; test null contribution anti-pairing only under source/route/target-preserving explicit self maps",
        "finite_length": "n=2,4 only new insertion diagnostics; j=n-2; Q^j-Pi(QPi)^j=sum_l Q^l(I-Pi)(QPi)^(j-l); verify a Pi=a, F2 zero; compare F4 with 8N; timing aggregation classified insertionwise or between-insertion cancellation",
        "precision": "exact rational throughout; no new log statistic", "zero_criterion": "exact rational zero", "resources": read(repository / DIRECTORY / "calibration.json"),
        "execution": {"workers": 1, "numeric_threads": 1, "heartbeat_seconds": 1, "watchdog_seconds": 300,
            "resume": "skip valid item/freeze/plan/source/payload hashes only", "retry": "none automatic; quarantine and stop", "split": "engineering amendment before changed execution; never outcome-dependent"},
        "pre_freeze_exposure": {"new_non_neutral_8O_factor_diagnostics": 0, "known": "all 8N route flags and passage results; explanatory/post-hoc as to null locations, not independent discovery",
            "allowed": "neutral/synthetic algebra, combinatorial indexing, immutable hashes, published regressions"},
        "outputs": ["route-null-factorization", "null-mechanism-summary", "timing-factorization", "factor-validation"]}
    value["plan_hash"] = plan_hash(value)
    write(repository / PLAN, value)
    print("PLAN", value["plan_hash"], sha256_file(repository / PLAN), flush=True)


def gate(repository, freeze):
    plan = require_frozen_plan(repository, freeze, PLAN, repository / PLAN)
    require(remote_contains(repository, freeze), "F0 must be pushed before new factor diagnostics")
    for p, digest in (plan["source_hashes"] | plan["input_hashes"] | plan["reused_hashes"]).items():
        require(sha256_file(repository / p) == digest, "frozen source/input drift: " + p)
    require(plan["analysis_version"] == VERSION, "F0 version")
    return plan


def valid(path, item, plan, freeze):
    if not path.exists():
        return False
    value = read(path)
    require(value["item"] == item and value["plan_hash"] == plan["plan_hash"] and value["freeze"] == freeze and
            value["result_hash"] == fingerprint(value["result"]), "invalid existing receipt; never overwrite: " + str(path))
    return True


def worker(repository, freeze, identity):
    plan = gate(repository, freeze)
    item = next(i for i in plan["items"] if i["item_id"] == identity)
    path = repository / OUTPUT / (identity + ".json")
    if valid(path, item, plan, freeze):
        print("RESUME", identity, flush=True)
        return
    start = time.monotonic()
    print("FACTOR", identity, flush=True)
    result = analyse(repository, item)
    value = {"item": item, "freeze": freeze, "plan_hash": plan["plan_hash"], "result": result,
             "result_hash": fingerprint(result), "wall_seconds": time.monotonic() - start, "status": "VERIFIED"}
    used = sum(p.stat().st_size for p in (repository / OUTPUT).glob("*.json"))
    require(used + len(canonical(value).encode()) < plan["resources"]["disk_budget_bytes"], "disk budget")
    write(path, value)
    print("DONE", identity, round(value["wall_seconds"], 3), value["result_hash"], flush=True)


def run(repository, freeze):
    plan = gate(repository, freeze)
    for item in plan["items"]:
        identity = item["item_id"]
        if valid(repository / OUTPUT / (identity + ".json"), item, plan, freeze):
            print("RESUME", identity, flush=True)
            continue
        start = time.monotonic()
        p = subprocess.Popen([sys.executable, "-m", "rs_constraint_lab.gen008o_exec", "worker", "--freeze", freeze, "--item", identity], cwd=repository)
        while p.poll() is None:
            elapsed = time.monotonic() - start
            write(repository / DIRECTORY / "status.json", {"state": "running", "item": identity, "seconds": elapsed, "freeze": freeze})
            if elapsed > plan["execution"]["watchdog_seconds"]:
                p.kill(); p.wait()
                break
            time.sleep(1)
        if p.returncode:
            write(repository / DIRECTORY / "quarantine" / (identity + ".json"), {"item": item, "returncode": p.returncode, "state": "quarantined"})
            raise RuntimeError("item quarantined; completed results preserved: " + identity)
    write(repository / DIRECTORY / "status.json", {"state": "complete", "items": len(plan["items"]), "freeze": freeze})


def transport(repository, li, ri, left, right, opposite=False):
    a, _, _, _, t, _, _, p, _ = setup(repository, li)
    b, _, _, _, t2, _, _, p2, _ = setup(repository, ri)
    def state_map(z):
        mask, i, j = z
        return (MASKS[mask], OPPOSITE[i], OPPOSITE[j]) if opposite else (mask ^ 63, i, j)
    index = {s: i for i, s in enumerate(STATES)}
    omap = [b.lookup[index[state_map(a.states[block[0]])]] for block in a.blocks]
    require(len(set(omap)) == len(omap), "orbit permutation")
    require(all(t[i,j] == t2[omap[i],omap[j]] and p[i,j] == p2[omap[i],omap[j]]
                for i in range(t.nrows()) for j in range(t.ncols())), "kernel/reset factor conjugacy")
    classes = pair_classes()
    cmap = {classes.name_of[mask]: classes.name_of[MASKS[mask] if opposite else mask ^ 63] for mask in classes.representatives}
    for key, side in left["sides"].items():
        k, direction = side["k"], side["route"]
        rk, rd = (k, direction) if opposite else (6-k, "DOWN" if direction == "UP" else "UP")
        other = right["sides"][f"{rk}-{rd}"]
        cols = [other["B_orbit_indices"].index(omap[o]) for o in side["B_orbit_indices"]]
        source_map = [other["classes"].index(cmap[s]) for s in side["classes"]]
        for field in ("entrance", "occupation", "U"):
            require(all(Q(side[field][i][j]) == Q(other[field][source_map[i]][cols[j]]) for i in range(len(source_map)) for j in range(len(cols))), "source factor transport: " + field)
        for field in ("V", "W"):
            require(all(Q(side[field][i][j]) == Q(other[field][cols[i]][source_map[j]]) for i in range(len(cols)) for j in range(len(source_map))), "target factor transport: " + field)
        for field in ("Delta", "F4"):
            require(all(Q(side[field][i][j]) == Q(other[field][source_map[i]][source_map[j]]) for i in range(len(source_map)) for j in range(len(source_map))), "readout transport: " + field)
    return {"left": li["item_id"], "right": ri["item_id"], "map": "opposite_pair" if opposite else "complement", "exact": True}


def symmetry_pairing(result):
    """Only a checked self-involution with opposite contributions earns a label."""
    from rs_constraint_lab.h2_roles import augmented_structure
    blocks, lookup = augmented_structure(2)
    index = {s: i for i, s in enumerate(STATES)}
    omap = [lookup[index[(MASKS[STATES[block[0]][0]], OPPOSITE[STATES[block[0]][1]], OPPOSITE[STATES[block[0]][2]])]] for block in blocks]
    table = pair_classes()
    cmap = {table.name_of[p]: table.name_of[MASKS[p]] for p in table.representatives}
    for row in result["rows"]:
        if row["role"] in (5, 6) or cmap[row["source"]] != row["source"]:
            row["symmetry_pair_test"] = "no source-preserving opposite-pair self symmetry"
            continue
        side = result["sides"][f"{row['k']}-{row['route']}"]
        i, indices = side["classes"].index(row["source"]), side["B_orbit_indices"]
        u, w = matrix(side["U"]), matrix(side["W"])
        pairs = [(j, indices.index(omap[o])) for j, o in enumerate(indices)]
        anti = all(u[i,j]*w[j,t] + u[i,p]*w[p,t] == 0 for j,p in pairs for t in range(w.ncols()))
        nonzero = bool(row["sparse_orbit_contributions"])
        row["symmetry_pair_test"] = {"involution": "opposite_pair", "source_route_preserved": True,
                                    "all_target_contributions_anti_pair": anti, "nonzero_contributions": nonzero}
        if anti and nonzero and row["bilinear_product_zero"]:
            row["symmetry_explanation_id"] = "OPPOSITE_PAIR_SIGN_REVERSING_CONTRIBUTIONS"
            for entry in row["sparse_orbit_contributions"]:
                entry["symmetry_partner"] = f"Z{omap[int(entry['orbit_id'][1:])]:03d}"


def verify_merge(repository, freeze):
    plan = gate(repository, freeze)
    values, rows, timing = {}, [], []
    for item in plan["items"]:
        path = repository / OUTPUT / (item["item_id"] + ".json")
        require(valid(path, item, plan, freeze), "missing item")
        value = read(path)
        values[item["item_id"]] = value
        symmetry_pairing(value["result"])
        rows.extend(value["result"]["rows"])
        timing.extend(value["result"]["timing_rows"])
    byid = {i["item_id"]: i for i in plan["items"]}
    controls = []
    for role in range(12):
        for grade in ("m025", "m4"):
            l, r = (f"F0-{f}-R{role:02d}-{grade}" for f in ("FORM", "DISSOLVE"))
            controls.append(transport(repository, byid[l], byid[r], values[l]["result"], values[r]["result"]))
            same = f"F0-ANY-R{role:02d}-{grade}"
            controls.append(transport(repository, byid[same], byid[same], values[same]["result"], values[same]["result"]))
    for family in ("ANY", "FORM", "DISSOLVE"):
        for grade in ("m025", "m4"):
            for role in range(12):
                partner = 11-role if role in (5,6) else role
                if role == 6:
                    continue
                l, r = f"F0-{family}-R{role:02d}-{grade}", f"F0-{family}-R{partner:02d}-{grade}"
                controls.append(transport(repository, byid[l], byid[r], values[l]["result"], values[r]["result"], True))
    primary = [r for r in rows if r["m"] != "1"]
    require(len(primary) == 1008, "complete route universe")
    for r in rows:
        grade = "m025" if r["m"] == "1/4" else "m4"
        r["complement_partner"] = None if r["m"] == "1" else {"model": r["model_id"].replace("FORM", "DISSOLVE") if r["family"] == "FORM" else r["model_id"].replace("DISSOLVE", "FORM"), "k": 6-r["k"], "route": "DOWN" if r["route"] == "UP" else "UP"}
        r["opposite_pair_partner"] = None if r["m"] == "1" else f"F0-{r['family']}-R{11-r['role'] if r['role'] in (5,6) else r['role']:02d}-{grade}"
    def counts(keys):
        c = Counter(tuple(str(r[k]) for k in keys) for r in primary)
        return [{**dict(zip(keys,key)), "count": n} for key,n in sorted(c.items())]
    summary = {"non_neutral_rows": len(primary), "neutral_rows": len(rows)-len(primary),
        "mechanisms": counts(["mechanism"]), "by_route": counts(["route", "mechanism"]),
        "by_family": counts(["family", "mechanism"]), "by_role_grade": counts(["role", "m", "mechanism"]),
        "by_layer_source": counts(["k", "source", "mechanism"]), "cancellation_subtypes": counts(["mechanism", "cancellation_subtype"])}
    tables = {"route-null-factorization": rows, "null-mechanism-summary": summary, "timing-factorization": timing}
    for suffix, value in tables.items():
        write(repository / (TABLE + suffix + ".json"), value)
    validation = {"status": "VERIFIED", "items": len(values), "freeze": freeze, "plan_hash": plan["plan_hash"],
        "source_route_rows": len(rows), "conjugacies": controls, "all_full_sparse_residuals": True, "independent_solve": "Dixon and fflu every occupation solve",
        "result_hashes": {key: v["result_hash"] for key,v in values.items()}, "table_hashes": {s: sha256_file(repository / (TABLE+s+".json")) for s in tables}}
    write(repository / (TABLE + "factor-validation.json"), validation)
    print("VERIFIED", summary["mechanisms"], flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("audit", "calibrate", "plan", "run", "worker", "verify"))
    p.add_argument("--freeze")
    p.add_argument("--item")
    args = p.parse_args()
    if args.action == "audit": audit(root())
    elif args.action == "calibrate": calibrate(root())
    elif args.action == "plan": make_plan(root())
    elif args.action == "worker": worker(root(), args.freeze, args.item)
    elif args.action == "run": run(root(), args.freeze)
    else: verify_merge(root(), args.freeze)


if __name__ == "__main__":
    main()
