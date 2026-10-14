"""Gravity-time programme, Round E2B (prompt GT-P005, OTR 1.0): the hard/soft interface.

Chosen after E2A (gravity-time/reports/gt-e2a-reflection.md section 5). E2A
found strict enabling by dissolution only with hard components, related to
direction in three ways: none (EXCL, reversible), soft circulation following
sigma (EXPH, EXPF), and a one-way mode with sigma = 0 (path_form prohibit,
FREE). E2B crosses the three hard formation exclusions with soft path terms
of both sigma signs, at N=5 in HELD and FREE.

Every E2A channel is kept (gte2a.analyse_item). Added per cell:

* one-way flux: the share of stationary flux pi_ct W carried by transitions
  whose reverse has rate 0, split by action (formation or dissolution) and,
  in HELD, by slot class;
* race committor: for every non-source slot g and other slot f, from the
  matched state x- (g removed from x ~ pi_jump restricted to g present), the
  probability that f toggles before g toggles back; reported separately over
  instances where removing g strictly enables f and over all instances.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte0a, gte2a, gtobs

ROUND_ID = "round-e2b"
EXPERIMENT_ID = "gt-round-e2b-hard-soft-interface"
ANALYSIS_VERSION = "gt-e2b/v1"
PROMPT_ID = "GT-P005"

SOFT = {"none": [], "PDwf": [("path_dissolve", "weak_favour")], "PDws": [("path_dissolve", "weak_suppress")], "PFws": [("path_form", "weak_suppress")], "PFwf": [("path_form", "weak_favour")]}
HARD = {"HPF": ("path_form", "prohibit"), "HCF": ("close_form", "prohibit"), "HAF": ("adj_form", "prohibit")}
CELLS = [("HPF", "PDwf"), ("HPF", "PDws"), ("HCF", "PDws"), ("HCF", "PFwf"), ("HAF", "none"), ("HAF", "PDwf"), ("HAF", "PDws"), ("HAF", "PFws"), ("HAF", "PFwf")]
CITED_FROM_E2A = {
    ("HPF", "none"): "PATHF-prohibit",
    ("HCF", "none"): "EXCL-prohibit",
    ("HCF", "PDwf"): "EXPH-prohibit+weak_favour",
    ("HCF", "PFws"): "EXPF-prohibit+weak_suppress",
    ("NOHARD", "PDwf"): "PATHH-weak_favour",
    ("NOHARD", "PDws"): "PATHH-weak_suppress",
    ("NOHARD", "PFws"): "PATHF-weak_suppress",
    ("NOHARD", "PFwf"): "PATHF-weak_favour",
}
OMITTED = {("HPF", "PFws"): "path_form soft terms can never act under path_form prohibit (a witness forbids formation outright)", ("HPF", "PFwf"): "as above"}


def family_name(hard: str, soft: str) -> str:
    return f"{hard}-{soft}"


def grade_name(hard: str, soft: str) -> str:
    h = HARD[hard][1]
    return h if soft == "none" else f"{h}+{SOFT[soft][0][1]}"


FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {family_name(h, s): {grade_name(h, s): [HARD[h]] + SOFT[s]} for h, s in CELLS}


def items() -> list[dict]:
    out = []
    for h, s in CELLS:
        for mode in ("HELD", "FREE"):
            fam, grade = family_name(h, s), grade_name(h, s)
            out.append({"family": fam, "grade": grade, "hard": h, "item_id": f"{mode}-N5-{fam}-{grade}", "mode": mode, "n": 5, "soft": s})
    return out


# --- added channels ----------------------------------------------------------------------------


def one_way_flux(chain, n: int, mode: str, ct: np.ndarray) -> dict:
    valid = chain.T >= 0
    F = ct[:, None] * chain.W
    total = float(F.sum())
    bits = gte2a._bits(chain)
    classes = gte2a.slot_classes(n, mode)
    out = {"formation": 0.0, "dissolution": 0.0, "by_class": {}}
    for e in range(chain.n_slots):
        m = valid[:, e] & (chain.W[:, e] > 0)
        rev = np.zeros(len(chain.states), dtype=bool)
        rev[m] = chain.W[chain.T[m, e], e] <= 0
        if not rev.any():
            continue
        form = rev & (bits[:, e] == 0)
        diss = rev & (bits[:, e] == 1)
        out["formation"] += float(F[form, e].sum())
        out["dissolution"] += float(F[diss, e].sum())
        key = classes[e]
        out["by_class"][key] = out["by_class"].get(key, 0.0) + float(F[rev, e].sum())
    norm = total if total > 0 else 1.0
    return {"by_class_share": {k: v / norm for k, v in sorted(out["by_class"].items())}, "dissolution_share": out["dissolution"] / norm, "formation_share": out["formation"] / norm, "share_of_total_flux": (out["formation"] + out["dissolution"]) / norm}


RACE_TOLERANCE = 1e-14
RACE_CAP = 20000


def race_values(chain, f: int, g: int) -> tuple[np.ndarray, int]:
    """h(y) = probability that slot f toggles before slot g, from y (jump chain), by iteration."""
    P = chain.W / chain.rates[:, None]
    valid = chain.T >= 0
    target = np.where(valid, chain.T, 0)
    Pv = np.where(valid, P, 0.0)
    h = np.zeros(len(chain.states))
    others = [e for e in range(chain.n_slots) if e not in (f, g)]
    it = 0
    for it in range(1, RACE_CAP + 1):
        new = Pv[:, f].copy()
        for e in others:
            new += Pv[:, e] * h[target[:, e]]
        delta = float(np.abs(new - h).max())
        h = new
        if delta < RACE_TOLERANCE:
            break
    return h, it


def race_committor(chain, n: int, mode: str, jump: np.ndarray) -> dict:
    bits = gte2a._bits(chain)
    classes = gte2a.slot_classes(n, mode)
    groups: dict[str, dict] = {}
    worst_iter = 0
    capped = 0
    for g in range(chain.n_slots):
        if classes[g] == "S":
            continue
        X = np.nonzero((bits[:, g] == 1) & (chain.T[:, g] >= 0))[0]
        if not len(X):
            continue
        Xm = chain.T[X, g]
        w = jump[X]
        if w.sum() <= 0:
            continue
        w = w / w.sum()
        for f in range(chain.n_slots):
            if f == g or classes[f] == "S":
                continue
            h, it = race_values(chain, f, g)
            worst_iter = max(worst_iter, it)
            capped += int(it >= RACE_CAP)
            enabled = (chain.W[X, f] == 0) & (chain.W[Xm, f] > 0)
            act = np.where(bits[X, f] == 0, "F", "D")
            for a in ("F", "D"):
                sel = act == a
                if not sel.any():
                    continue
                G = groups.setdefault(f"{gte2a.relation_class(n, mode, g, f)}:{a}", {"all_mass": 0.0, "all_value": 0.0, "enabled_mass": 0.0, "enabled_value": 0.0, "matched_x_value": 0.0})
                ws = w[sel]
                G["all_mass"] += float(ws.sum())
                G["all_value"] += float((ws * h[Xm[sel]]).sum())
                G["matched_x_value"] += float((ws * h[X[sel]]).sum())
                en = enabled[sel]
                if en.any():
                    G["enabled_mass"] += float(ws[en].sum())
                    G["enabled_value"] += float((ws[en] * h[Xm[sel][en]]).sum())
    out = {}
    for k, G in sorted(groups.items()):
        out[k] = {
            "race_from_x_minus_all": G["all_value"] / G["all_mass"] if G["all_mass"] > 0 else None,
            "race_from_x_minus_enabled": G["enabled_value"] / G["enabled_mass"] if G["enabled_mass"] > 0 else None,
            "race_from_x_with_g": G["matched_x_value"] / G["all_mass"] if G["all_mass"] > 0 else None,
            "enabled_weight_share": G["enabled_mass"] / G["all_mass"] if G["all_mass"] > 0 else 0.0,
        }
    return {"groups": out, "max_iterations": worst_iter, "capped_pairs": capped}


def extra(block, chain, n, mode, stat):
    if stat is None:
        return
    block["one_way_flux"] = one_way_flux(chain, n, mode, stat["ct"])
    block["race"] = race_committor(chain, n, mode, stat["jump"])


def analyse_item(item: dict, *, with_trajectories: bool = True, checks: bool = True, on_main=None):
    result, traj = gte2a.analyse_item(item, with_trajectories=with_trajectories, checks=checks, on_main=on_main, families=FAMILIES, round_id=ROUND_ID, extra=extra)
    result["e2b"] = {"analysis_version": ANALYSIS_VERSION, "hard": item["hard"], "soft": item["soft"]}
    return result, traj


def check_problems(result: dict) -> list[str]:
    problems = gte2a.check_problems(result)
    race = (result.get("e2a") or {}).get("race")
    if race and race["capped_pairs"]:
        problems.append("race committor iteration cap")
    return problems


def assemble(results: dict[str, dict]) -> dict:
    base = gte2a.assemble(results)
    for key, r in results.items():
        if r.get("regime") == "recurrent" and (r.get("stationary") or {}).get("resolved"):
            base["frozen_expectations"][f"Z5-{key}"] = {"holds": not check_problems(r), "problems": check_problems(r)}
        if r["e2b"]["soft"] == "none" and r.get("regime") == "recurrent" and (r.get("stationary") or {}).get("resolved"):
            flux = r["reversibility"]["irreversible_flux_fraction"]
            ow = r["e2a"]["one_way"]["one_way_transitions"]
            base["frozen_expectations"][f"I6-{key}"] = {"holds": flux <= 1e-9 and ow == 0, "irreversible_flux_fraction": flux, "one_way_transitions": ow}
        row = base["cell_rows"].get(key)
        if row is not None and "e2a" in r and "one_way_flux" in r["e2a"]:
            row["one_way_flux_share"] = r["e2a"]["one_way_flux"]["share_of_total_flux"]
            row["hard"] = r["e2b"]["hard"]
            row["soft"] = r["e2b"]["soft"]
    return base


# --- plan and execution ---------------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e2b-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e2b"
TABLES_RELPATH = "gravity-time/reports/round-e2b-tables.json"
WATCHDOG_SECONDS = {5: 900}
ROUND_WALL_CAP_SECONDS = 3600
WORKERS = 4
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [5], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = (
    "gravity-time/reports/gt-e2a-reflection.md",
    "gravity-time/reports/round-e2a-tables.json",
    "gravity-time/plans/round-e2a-plan.json",
    "gravity-time/docs/e2-formal-mechanism.md",
    "gravity-time/docs/e2-coverage-audit.md",
    "gravity-time/provenance/prompts/GT-P005-agent-input.md",
)


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    document = {
        "adaptive_choice_note": "E2B was chosen because of E2A results (gt-e2a-reflection.md section 5); it is not independent confirmation of E2A and E2A is not changed",
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "gravity-time/reports/gt-e2a-reflection.md section 5 (commit b90c3ac): strict enabling occurs only with hard components and relates to direction in three ways; the one-way mode is unexplained",
        "cited_comparators_from_e2a": {f"{h}+{s}": f"E2A cells HELD/FREE-N5-{v} (tables round-e2a-tables.json, result commit 32ac7f6)" for (h, s), v in CITED_FROM_E2A.items()},
        "clocks": "as E2A",
        "comparisons": {
            "D1_sigma_with_hard": "for each irreversible cell, sign of the soft sigma against the sign of the partner index (and HELD handover index), beside the same soft term without a hard component (E2A)",
            "D2_one_way_mode": "one-way flux share and its split by action and class; partner index of cells with sigma = 0 and one-way transitions",
            "D3_enabling_and_direction": "strict enabling shares (matched dissolution) against irreversible flux, per cell",
            "D4_race": "race committor from x- over strictly enabled instances against all instances and against the matched x with g present",
            "D5_scaffold": "HELD versus FREE for each hard component (the source triangle as a witness)",
            "no_aggregate_score": "no ranking",
        },
        "controls_and_identities": {
            "I1_I2": "as E2A: the square identity on intact squares, zero on disjoint squares",
            "I6_hard_gradient_alone": "adj_form prohibit alone (HAF-none), HELD and FREE: a gradient restriction; flux <= 1e-9 and no one-way transitions (forward and reverse rates vanish together within the class)",
            "Z5_numerical": "as E2A, plus the race committor converging (max change < 1e-14) before 20,000 iterations",
            "separation_note": "no expectation on the sign or size of any index, flux, enabling share or race probability",
        },
        "deliberate_omissions": {**{f"{h}+{s}": why for (h, s), why in OMITTED.items()}, "n6_free_strong_grades_hard_dissolution": "held out for a possible future confirmatory test (gt-e2a-reflection.md section 5)", "n7": "not run"},
        "estimands": "every E2A channel plus one-way flux and the race committor, for each cell; D1-D5",
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in comps], "sigma_soft": gte2a.sigma(comps)} for g, comps in grades.items()} for f, grades in FAMILIES.items()},
        "history": False,
        "initial_conditions": "as E2A",
        "items": cells,
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "numerical_policy": "as E2A (gte2a numerical checks with round_id round-e2b), race committor by value iteration to max change < 1e-14, cap 20,000",
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "Is the one-way mode (hard path-form exclusion) oriented in the partner frame regardless of an added soft sigma of either sign, or does the soft sigma decide?",
            "Does sigma predict the partner-index sign when a hard closure or adjacency exclusion is present?",
            "What share of flux do one-way transitions carry, and is it formation or dissolution that cannot be reversed?",
            "Do strictly enabled events win the race against restoration more often than other events, and more than from the matched state with the support present?",
            "Does strict enabling ever come without any irreversibility apart from the hard-gradient controls?",
            "How does the held source act as a witness under each hard component?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {"e2a": "all E2A results were read in full (they motivate E2B); the cited comparators are E2A cells", "e2b_cells": "no E2B cell (hard component crossed with a soft term, or adj_form prohibit) was computed before freezing; plumbing tests use synthetic N=4 cells", "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES}},
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "Where admissibility rather than rate structures succession: when does strict enabling by dissolution come with direction, is the one-way mode oriented by its own rule, and does sigma still predict orientation under a hard component?",
        "round_id": ROUND_ID,
        "sampling": f"exact census of {len(cells)} declared cells at N=5, HELD and FREE",
        "schema": "rs-gt.e2b-plan/v1",
        "selection_rule": "the three existing hard formation exclusions (path_form, close_form, adj_form prohibit) crossed with no soft term and the four weak path terms (path_dissolve weak_favour/weak_suppress, path_form weak_suppress/weak_favour); combinations run in E2A are cited, path_form soft terms are omitted under path_form prohibit",
        "software": {"analysis_module": "rs_constraint_lab.gte2b", "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "illustrative_only",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s; then stop", "unresolved": "recorded; no retuning", "amendment": "cell or estimand changes stop the round"},
        "tolerances": {"identity": 1e-9, "formula": 1e-12, "references": 1e-12, "race": RACE_TOLERANCE},
        "work_count": {"items": len(cells), "largest_state_space": 1024, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {"5": 900}, "workers": WORKERS, "estimate_note": "E2A N=5 cells took seconds; the race committor adds up to 90 value iterations of <= 1,024 states per cell: estimated under 2 minutes per cell"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E2B plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()

    def payload(result, status):
        return {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}

    def on_main(result, trajectories):
        atomic_write_json(root / "items" / f"{item['item_id']}.partial.json", payload(result, "complete_checks_interrupted"))

    result, _ = analyse_item(item, on_main=on_main)
    final = payload(result, "complete")
    atomic_write_json(root / "items" / f"{item['item_id']}.json", final)
    partial = root / "items" / f"{item['item_id']}.partial.json"
    if partial.exists():
        partial.unlink()
    return final


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    from rs_constraint_lab import gte1

    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module="rs_constraint_lab.gte2b", **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results and results[k].get("regime") == "recurrent" else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e2b-tables/v1", "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


ATLAS_RELPATH = "gravity-time/reports/gt-e2b-atlas.md"


def render_atlas(repo: Path, tables: Path | None = None, plan_path: Path | None = None) -> str:
    """The E2A atlas sections for E2B cells, plus one-way flux and race committor tables."""
    import json

    from rs_constraint_lab import gte2a_atlas

    text = gte2a_atlas.build(repo, tables or repo / TABLES_RELPATH, plan_path or repo / PLAN_RELPATH, title="GT-E2B hard/soft interface atlas", tables_rel=TABLES_RELPATH, generator="rs_constraint_lab.gte2b render_atlas")
    t = json.loads((tables or repo / TABLES_RELPATH).read_text())
    L = ["## 7. One-way flux (D2)", "", "Share of stationary flux on transitions whose reverse has rate 0, by action and slot class.", ""]
    L += ["| Cell | share | formation | dissolution | by class |", "| --- | --- | --- | --- | --- |"]
    for k, r in t["results"].items():
        ow = (r.get("e2a") or {}).get("one_way_flux")
        if ow:
            L.append(f"| {k} | {ow['share_of_total_flux']:.4f} | {ow['formation_share']:.4f} | {ow['dissolution_share']:.4f} | {ow['by_class_share']} |")
    L += ["", "## 8. Race committor (D4)", "", "From the matched state x- (support g removed), probability that f toggles before g is restored: over strictly enabled instances, over all instances, and from x with g present.", ""]
    L += ["| Cell | Group | enabled weight | race x- enabled | race x- all | race x (g present) |", "| --- | --- | --- | --- | --- | --- |"]
    fmt = lambda v: "—" if v is None else f"{v:.3f}"
    for k, r in t["results"].items():
        race = (r.get("e2a") or {}).get("race")
        if not race:
            continue
        for gk, g in race["groups"].items():
            L.append(f"| {k} | {gk} | {g['enabled_weight_share']:.3f} | {fmt(g['race_from_x_minus_enabled'])} | {fmt(g['race_from_x_minus_all'])} | {fmt(g['race_from_x_with_g'])} |")
    return text + "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte2b")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    sub.add_parser("atlas")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import read_json

    if args.command == "atlas":
        repo = Path(__file__).resolve().parents[3]
        text = render_atlas(repo)
        (repo / ATLAS_RELPATH).write_text(text)
        print(f"wrote {ATLAS_RELPATH} ({len(text)} bytes)")
        return 0
    root = Path(args.root)
    plan = read_json(root / "plan.json")
    (item,) = [it for it in plan["items"] if it["item_id"] == args.item_id]
    if item not in items() and not plan.get("synthetic_fixture"):
        raise SystemExit("item is not in the E2B manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
