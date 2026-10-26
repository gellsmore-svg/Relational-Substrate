"""Gravity-time programme, Round E3B (prompt GT-P006, OTR 1.0): the source-witness floor.

Chosen after E3A (gravity-time/reports/gt-e3a-reflection.md section 4).

Post hoc mechanism to be tested (derived after E3A, formal note section 7):
  T7  in HELD every attachment slot (p, s) has exactly two path witnesses lying
      wholly inside the held source triangle, in every state;
  T8  a constant factor on all formations (or all dissolutions) of one slot class
      changes no cycle affinity.
Hence each path component with factor m multiplies every attachment's formation
(path_form) or dissolution (path_dissolve) rate by m^2, an orientation-neutral
occupancy bias: against attachment when sigma > 0, toward it when sigma < 0.

Each cell is computed on its kernel and on a NEUTRALISED INSTRUMENT KERNEL in
which that constant floor is divided out of the attachment rates. The
instrument is not a grammar rule (it treats source-internal witnesses specially
and is not label-covariant); it is a counterfactual comparison only.
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte0a, gte0b, gte1, gte2a, gtkernel, gtobs
from rs_constraint_lab.gte0a import SOURCE, Chain
from rs_constraint_lab.state import edges

ROUND_ID = "round-e3b"
EXPERIMENT_ID = "gt-round-e3b-source-witness-floor"
ANALYSIS_VERSION = "gt-e3b/v1"
PROMPT_ID = "GT-P006"
MODE = "HELD"

FAMILY_GRADES = (("PATHF", "weak_suppress"), ("PATHF", "weak_favour"), ("PATHH", "weak_favour"), ("PATHH", "weak_suppress"), ("CSPH", "strong_favour+weak_favour"), ("CWPH", "weak_favour+weak_favour"), ("PCOMP", "weak_favour+weak_favour"), ("CLOSEW", "weak_favour"), ("NULL", "none"))
FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {}
for _f, _g in FAMILY_GRADES:
    src = gte0b.FAMILIES if _f in gte0b.FAMILIES and _g in gte0b.FAMILIES[_f] else gte0a.FAMILIES
    FAMILIES.setdefault(_f, {})[_g] = list(src[_f][_g])


def items() -> list[dict]:
    out = []
    for n in (5, 6):
        for f, g in FAMILY_GRADES:
            out.append({"family": f, "grade": g, "item_id": f"HELD-N{n}-{f}-{g}", "mode": MODE, "n": n})
    return out


def internal_witnesses(states: np.ndarray, n: int) -> np.ndarray:
    """Number of path witnesses (end, c, d) of every (state, slot) lying wholly inside the source."""
    E = edges(n)
    pos = {pair: i for i, pair in enumerate(E)}
    out = np.zeros((len(states), len(E)), dtype=np.int64)
    for e, (a, b) in enumerate(E):
        for end in (a, b):
            for c in range(n):
                for d in range(n):
                    if len({end, c, d, a if end == b else b}) < 4 or c == d:
                        continue
                    if c in (a, b) or d in (a, b):
                        continue
                    if not ({end, c, d} <= set(SOURCE)):
                        continue
                    i1, i2 = pos[(min(end, c), max(end, c))], pos[(min(c, d), max(c, d))]
                    out[:, e] += ((states >> i1) & 1) * ((states >> i2) & 1)
    return out


def floor_factors(chain: Chain, n: int, components) -> np.ndarray:
    """Multiplicative factor the source-internal witnesses contribute to every (state, slot) rate."""
    iw = internal_witnesses(chain.states, n)
    present = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).astype(bool)
    F = np.ones_like(chain.W)
    for kind, grade in components:
        if not kind.startswith("path"):
            continue
        m = float(gte0a.FACTORS[grade])
        acts = ~present if kind == "path_form" else present
        F = np.where(acts, F * np.power(m, iw.astype(float)), F)
    return F


def neutralised(chain: Chain, n: int, components) -> Chain:
    F = floor_factors(chain, n, components)
    return Chain(chain.n_slots, chain.states, chain.W / F, chain.T)


def profile(chain: Chain, n: int, family: str, grade: str, components, *, label: str, item_id: str) -> dict:
    start = gtobs.start_index(chain, n, MODE)
    stat = gtobs.stationary(chain, start, cross_check=True)
    result, _ = gtobs.analyse(chain, family=family, grade=grade, n=n, mode=MODE, families=FAMILIES, item_id=f"{item_id}:{label}", round_id=ROUND_ID, with_trajectories=False, stationary_override=stat)
    out = {"result": result}
    if not stat.get("resolved"):
        return out
    hc, hj = result["held_continuous"], result["held_jump"]
    add = result["e1_additions"]["held"]
    r0 = hc["null_attachment_fraction"]
    ch = {"null_attachment_fraction": r0}
    for clock, h, a in (("ct", hc, add["continuous"]), ("jump", hj, add["jump"])):
        af = h["attachment_fraction"]
        ch[f"attachment_fraction_{clock}"] = af
        ch[f"margin_raw_{clock}"] = af - r0
        ch[f"margin_normalised_{clock}"] = None if r0 >= 1.0 else (af - r0) / (1 - r0)
        ch[f"margin_standardised_{clock}"] = a["attachment_margin_null_density_standardised"]
        ch[f"detached_fraction_{clock}"] = h["distance_distribution"].get("inf", 0.0)
    ch["irreversible_flux_fraction"] = result["reversibility"]["irreversible_flux_fraction"]
    ch["expected_edges"] = result["occupancy_ct"]["expected_edges"]
    ch["handover_index"] = gte1.handover_statistics(gtobs.event_pattern_probabilities(chain, stat["jump"], n, MODE))["index_adjacent"]
    ch["partner_index"] = gte2a.partner_frame(chain, n, stat["jump"])["index"]
    from rs_constraint_lab import gtobs_validate

    law = gtobs_validate.gth_stationary(chain)
    out["gth"] = {"ct": gte1._law_difference(stat["ct"], law["ct"]), "jump": gte1._law_difference(stat["jump"], law["jump"])}
    out["long_double_residual"] = gte1.long_double_residual(chain, stat["jump"])
    out["channels"] = ch
    out["squares"] = gte2a.square_census(chain, n, MODE, components, stat["ct"])
    return out


def square_affinity_difference(a: Chain, b: Chain) -> float:
    """max |A_a - A_b| over every intact elementary square (both chains share states and targets)."""
    worst = 0.0
    la = np.where(a.W > 0, np.log(np.where(a.W > 0, a.W, 1.0)), np.nan)
    lb = np.where(b.W > 0, np.log(np.where(b.W > 0, b.W, 1.0)), np.nan)
    bits = ((a.states[:, None] >> np.arange(a.n_slots)) & 1)
    for e in range(a.n_slots):
        for f in range(e + 1, a.n_slots):
            base = np.nonzero((bits[:, e] == 0) & (bits[:, f] == 0))[0]
            i1, i3 = a.T[base, e], a.T[base, f]
            ok = (i1 >= 0) & (i3 >= 0)
            base, i1, i3 = base[ok], i1[ok], i3[ok]
            i2 = a.T[i1, f]
            ok = i2 >= 0
            base, i1, i2, i3 = base[ok], i1[ok], i2[ok], i3[ok]
            if not len(base):
                continue
            def aff(L):
                return (L[base, e] + L[i1, f] + L[i2, e] + L[i3, f]) - (L[base, f] + L[i3, e] + L[i2, f] + L[i1, e])
            d = np.abs(aff(la) - aff(lb))
            d = d[np.isfinite(d)]
            if d.size:
                worst = max(worst, float(d.max()))
    return worst


def analyse_item(item: dict, *, with_trajectories: bool = False, checks: bool = True, on_main=None) -> tuple[dict, None]:
    n, family, grade = item["n"], item["family"], item["grade"]
    components = FAMILIES[family][grade]
    t0 = time.perf_counter()
    chain, _ = gtkernel.reachable_chain(n, MODE, components)
    neut = neutralised(chain, n, components)
    iw = internal_witnesses(chain.states, n)
    classes = gte2a.slot_classes(n, MODE)
    attach = np.array([c == "A" for c in classes])
    t7 = bool((iw[:, attach] == 2).all() and (iw[:, ~attach & np.array([c != "S" for c in classes])] == 0).all())
    orig = profile(chain, n, family, grade, components, label="original", item_id=item["item_id"])
    neu = profile(neut, n, family, grade, components, label="neutralised", item_id=item["item_id"])
    expected_floor = {}
    for kind, g in components:
        if kind.startswith("path"):
            expected_floor[kind] = float(gte0a.FACTORS[g]) ** 2
    ratio = chain.W / np.where(neut.W > 0, neut.W, 1.0)
    out = {
        "analysis_version": ANALYSIS_VERSION,
        "expected_floor_factor_by_component": expected_floor,
        "family": family,
        "grade": grade,
        "kernel_ratio_non_attachment_max_deviation": float(np.abs(ratio[:, ~attach] - 1.0).max()),
        "mode": MODE,
        "n": n,
        "neutralised": neu,
        "original": orig,
        "regime": orig["result"].get("regime"),
        "sigma": gte2a.sigma(components),
        "square_affinity_max_change": square_affinity_difference(chain, neut),
        "t7_two_internal_witnesses_on_every_attachment": t7,
        "seconds": time.perf_counter() - t0,
    }
    if checks:
        out["kernel_sample"] = gte1.kernel_sample_check({**item, "alphabet": "W4"}, chain, gtobs.start_index(chain, n, MODE), families=FAMILIES, round_id=ROUND_ID)
    if "channels" in orig and "channels" in neu:
        out["delta"] = {k: neu["channels"][k] - orig["channels"][k] for k in orig["channels"] if isinstance(orig["channels"][k], float) and isinstance(neu["channels"][k], float)}
    return out, None


def check_problems(r: dict) -> list[str]:
    problems = []
    for side in ("original", "neutralised"):
        s = r[side]
        st = s["result"].get("stationary") or {}
        if not st.get("resolved"):
            problems.append(f"{side}: stationary unresolved")
            continue
        if st["residual"] > gtobs.STATIONARY_RESIDUAL_TOLERANCE:
            problems.append(f"{side}: residual")
        for clock in ("ct", "jump"):
            g = s["gth"][clock]
            if g["l1"] > gte1.REFEREE_L1 or (g["max_relative"] or 0) > gte1.REFEREE_MAX_RELATIVE:
                problems.append(f"{side}: gth {clock}")
        if s["long_double_residual"]["zero_mass_states"]:
            problems.append(f"{side}: zero-mass states")
        if (s["long_double_residual"]["max_relative"] or 0) > gte1.RESIDUAL_MAX_RELATIVE:
            problems.append(f"{side}: per-entry residual")
        if (s["result"].get("symmetry_max_abs_difference") or 0) > gte0a.SYMMETRY_TOLERANCE:
            problems.append(f"{side}: symmetry")
    ks = r.get("kernel_sample")
    if ks and (ks["max_relative_weight_difference"] > gte1.KERNEL_RELATIVE_TOLERANCE or ks["zero_pattern_mismatches"] or ks["target_mismatches"]):
        problems.append("kernel sample check")
    return problems


def assemble(results: dict[str, dict]) -> dict:
    checks = {}
    rows = {}
    for key, r in results.items():
        fam = r["family"]
        checks[f"T7-{key}"] = {"holds": r["t7_two_internal_witnesses_on_every_attachment"]}
        checks[f"T8-{key}"] = {"holds": r["square_affinity_max_change"] <= 1e-12, "square_affinity_max_change": r["square_affinity_max_change"], "neutralised_formula_error": (r["neutralised"].get("squares") or {}).get("formula_max_abs_error")}
        checks[f"K-{key}"] = {"holds": r["kernel_ratio_non_attachment_max_deviation"] <= 1e-15, "max_deviation": r["kernel_ratio_non_attachment_max_deviation"]}
        if fam in ("CLOSEW", "NULL") and "delta" in r:
            dmax = max(abs(v) for v in r["delta"].values())
            checks[f"C1-{key}"] = {"holds": dmax <= 1e-12, "max_channel_change": dmax}
        if fam == "PCOMP" and "delta" in r:
            dmax = max(abs(v) for v in r["delta"].values())
            checks[f"C2-{key}"] = {"holds": dmax <= 1e-9, "max_channel_change": dmax}
        probs = check_problems(r)
        checks[f"Z5-{key}"] = {"holds": not probs, "problems": probs}
        if "delta" in r:
            rows[key] = {"family": fam, "grade": r["grade"], "n": r["n"], "sigma": r["sigma"], "original": r["original"]["channels"], "neutralised": r["neutralised"]["channels"], "delta": r["delta"]}
    return {"frozen_expectations": checks, "cell_rows": rows}


PLAN_RELPATH = "gravity-time/plans/round-e3b-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e3b"
TABLES_RELPATH = "gravity-time/reports/round-e3b-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e3b-atlas.md"
WATCHDOG_SECONDS = {5: 900, 6: 900}
ROUND_WALL_CAP_SECONDS = 3600
WORKERS = 4
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [5, 6], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = ("gravity-time/reports/gt-e3a-reflection.md", "gravity-time/reports/round-e3a-tables.json", "gravity-time/plans/round-e3a-plan.json", "gravity-time/docs/e3-formal-support-and-recovery.md", "gravity-time/provenance/prompts/GT-P006-agent-input.md", "gravity-time/reports/round-e0b-tables.json", "gravity-time/reports/round-e2a-tables.json")


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    document = {
        "adaptive_choice_note": "E3B was chosen because of E3A finding 6 and the post hoc derivation T7/T8 (gt-e3a-reflection.md sections 2 and 4, commit 1e5ebc3); it is not independent confirmation and E3A is unchanged",
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "gravity-time/reports/gt-e3a-reflection.md section 4",
        "clocks": "as E3A; attachment margins in both clocks",
        "comparisons": {
            "F1_margin_shift": "for each cell and N, the change (neutralised minus original) of the raw, ceiling-normalised and null-density-standardised attachment margins and the detached fraction, both clocks; whether any sigma>0 family's margin becomes positive once the floor is removed",
            "F2_orientation": "change of handover index, partner index and irreversible flux (T8 fixes the affinities, not the aggregate)",
            "F3_sign_structure": "whether the floor's effect on attachment has the sign opposite to sigma in every path family (from T7/T8: against attachment for sigma>0)",
            "no_aggregate_score": "no ranking",
        },
        "controls_and_identities": {
            "T7": "every attachment slot has exactly two wholly-internal source witnesses in every reachable state; every probe-probe slot has none",
            "T8": "max |A_neutralised - A_original| <= 1e-12 over every intact elementary square; the neutralised kernel also satisfies the square identity",
            "K": "the neutralised kernel equals the original on every non-attachment slot (ratio deviation <= 1e-15)",
            "C1": "CLOSEW and NULL (no path component): every channel unchanged (<= 1e-12)",
            "C2": "PCOMP (floor on formation and dissolution, equal): every channel unchanged (<= 1e-9)",
            "Z5": "per kernel: stationary resolved and residual, GTH referee, long-double residual, symmetry; kernel sample check (rule strings) on the original",
            "separation_note": "T7, T8, K, C1 and C2 are identities; nothing predicts the size or sign of any margin, index or flux change",
        },
        "deliberate_omissions": {"n7_free": "not run", "other_source_structures": "held out (would need a configurable scaffold)", "trajectories": "not generated"},
        "estimands": "original and neutralised channels (margins in three forms and both clocks, detached fractions, flux, expected relations, handover and partner indices) and their differences; T7/T8 checks",
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in comps], "sigma": gte2a.sigma(comps)} for g, comps in grades.items()} for f, grades in FAMILIES.items()},
        "history": False,
        "initial_conditions": "HELD start state (source triangle); reachable class",
        "instrument_note": "the neutralised kernel divides each attachment rate by prod over path components of m^(internal witnesses) (= m^2), on formations for path_form and dissolutions for path_dissolve. It is not a grammar rule and not label-covariant; it is a counterfactual instrument to measure the share of an effect produced by the held triangle's own witnesses",
        "items": cells,
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "How much of each path family's attachment deficit (relative to the size-specific null) does the source-witness floor account for?",
            "Does any sigma>0 family (path_form suppress, path_dissolve favour, CSPH, CWPH) gather once the floor is removed, in any form or clock?",
            "Do the handover index, partner index and flux change, given that the affinities do not?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {"e3a": "all E3A results read (they motivate E3B)", "published": "the original kernels of HELD N=5/6 PATHF and PATHH weak grades, CSPH, CWPH, PCOMP, CLOSEW and NULL are published (E0A/E0B/E1/E2A); their standard channels are known. No neutralised kernel was computed before freezing; plumbing tests use HELD N=4 only", "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES}},
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "Is the repulsion of the sigma>0 path families from the held source produced by the source triangle's own path witnesses (a constant, orientation-neutral floor), and does removing it change gathering?",
        "round_id": ROUND_ID,
        "sampling": f"{len(cells)} cells x 2 kernels",
        "schema": "rs-gt.e3b-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte3b", "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s; then stop", "unresolved": "recorded; no retuning", "amendment": "cell or estimand changes stop the round"},
        "tolerances": {"t8": 1e-12, "kernel_ratio": 1e-15, "c1": 1e-12, "c2": 1e-9, "numerical": "as E1 (gte1)"},
        "work_count": {"items": len(cells), "largest_state_space": 4096, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "workers": WORKERS, "estimate_note": "two HELD N=6 kernels with GTH: about 2 minutes per N=6 cell"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E3B plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()
    result, _ = analyse_item(item)
    final = {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": "complete", "wall_seconds": time.perf_counter() - started}
    atomic_write_json(root / "items" / f"{item['item_id']}.json", final)
    return final


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module="rs_constraint_lab.gte3b", **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e3b-tables/v1", "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def render_atlas(repo: Path, tables: Path | None = None) -> str:
    import json

    t = json.loads((tables or repo / TABLES_RELPATH).read_text())
    fmt = lambda v: "—" if v is None else (f"{v:+.1e}" if v != 0 and abs(v) < 1e-3 else f"{v:+.3f}")
    L = ["# GT-E3B source-witness floor atlas", "", f"Generated by `rs_constraint_lab.gte3b atlas` from `{TABLES_RELPATH}` (payload `{t['payload_sha256'][:12]}…`), frozen plan `{t['frozen_analysis_plan_commit'][:7]}`. Every cell is listed. 'Neutralised' is a counterfactual instrument kernel (source-witness floor divided out of attachment rates), not a grammar rule.", ""]
    groups: dict[str, list] = {}
    for k, c in t["frozen_expectations"].items():
        groups.setdefault(k.split("-")[0], []).append(c["holds"])
    L += ["Identities and acceptance: " + "; ".join(f"**{z}** {sum(v)}/{len(v)}" for z, v in sorted(groups.items())) + ".", "", "## Item records", "", "| Item | Status | Wall s | Problems |", "| --- | --- | --- | --- |"]
    for k, rec in t["item_records"].items():
        L.append(f"| {k} | {rec['status']} | {rec['wall_seconds']:.1f} | {'; '.join(rec['numerical_problems'] or []) or 'none'} |")
    keys = ["margin_raw_ct", "margin_raw_jump", "margin_normalised_ct", "margin_standardised_ct", "margin_standardised_jump", "detached_fraction_ct", "irreversible_flux_fraction", "handover_index", "partner_index", "expected_edges"]
    L += ["", "## Original, neutralised and change", ""]
    for k, row in t["cell_rows"].items():
        L += [f"**{k}** (σ = {row['sigma']:+.3f})", "", "| Channel | original | neutralised | change |", "| --- | --- | --- | --- |"]
        for c in keys:
            L.append(f"| {c} | {fmt(row['original'].get(c))} | {fmt(row['neutralised'].get(c))} | {fmt(row['delta'].get(c))} |")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte3b")
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
        raise SystemExit("item is not in the E3B manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
