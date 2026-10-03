"""Command line for the constraint laboratory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rs_constraint_lab.accounting import template_accounting
from rs_constraint_lab.constraints import Choreography, parse_expression
from rs_constraint_lab.generation import run_experiment
from rs_constraint_lab.grammar import build_grammar, is_canonical_ids
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.semantics import get_semantics, semantics_names
from rs_constraint_lab.spec import load_spec, spec_hash
from rs_constraint_lab.state import canonical_states, edge_count, n_states
from rs_constraint_lab.trajectory import replay_matches, sample_trajectory
from rs_constraint_lab.version import ENGINE_VERSION
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rs-lab")
    parser.add_argument("--version", action="version", version=ENGINE_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    inspect = sub.add_parser("inspect-space", help="print the coordinate, counts, and unsearched regions")
    inspect.add_argument("spec")

    enumerate = sub.add_parser("enumerate", help="enumerate states or constraints for one N")
    enumerate.add_argument("kind", choices=["states", "constraints"])
    enumerate.add_argument("spec")
    enumerate.add_argument("--n", type=int, required=True)

    exact = sub.add_parser("exact", help="run the exact finite-state generation")
    _add_run_args(exact)
    run = sub.add_parser("run", help="run a generation, including selected replays")
    _add_run_args(run)

    replay = sub.add_parser("replay", help="regenerate a stored trajectory and compare it")
    replay.add_argument("run_file")

    compare = sub.add_parser("compare", help="print records that share ids")
    compare.add_argument("summary")
    compare.add_argument("ids", nargs="+")

    report = sub.add_parser("report", help="print headline counts from a summary")
    report.add_argument("summary")
    analyse = sub.add_parser("analyze", help="alias of report")
    analyse.add_argument("summary")

    catalogue = sub.add_parser("catalogue", help="locate the family catalogue for a summary")
    catalogue.add_argument("action", choices=["build"])
    catalogue.add_argument("summary")

    args = parser.parse_args(argv)
    if args.command == "inspect-space":
        return _inspect(Path(args.spec))
    if args.command == "enumerate":
        return _enumerate(Path(args.spec), args.kind, args.n)
    if args.command in {"exact", "run"}:
        spec = load_spec(args.spec)
        _require_graph(spec)
        summary = run_experiment(spec, Path(args.out), Path(args.publish) if args.publish else None)
        print(json.dumps({
            "experiment_id": summary["experiment_id"],
            "spec_hash": summary["spec_hash"],
            "runtime_seconds": round(summary["runtime_seconds"], 3),
            "cells": [
                {
                    "N": cell["coordinate"]["N"],
                    "K_max": cell["coordinate"]["K_max"],
                    "families": cell["families"],
                    "canonical": {key: value["canonical"] for key, value in cell["cardinalities"].items()},
                }
                for cell in summary["cells"]
            ],
        }, indent=2))
        return 0
    if args.command == "replay":
        return _replay(Path(args.run_file))
    if args.command == "compare":
        return _compare(Path(args.summary), args.ids)
    if args.command in {"report", "analyze"}:
        return _report(Path(args.summary))
    if args.command == "catalogue":
        return _catalogue(Path(args.summary))
    return 2


def _add_run_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("spec")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--publish", type=Path, help="copy summaries, tables, and selected exemplars here")


def _require_graph(spec: dict) -> None:
    semantics = get_semantics(spec["semantics"])
    if semantics.name != "graph":
        semantics.relation_slots(spec["cells"][0]["N"])


def _inspect(path: Path) -> int:
    spec = load_spec(path)
    print(f"experiment {spec['experiment_id']}  schema {spec['schema']}")
    print(f"spec_hash {spec_hash(spec)}")
    print(f"engine {ENGINE_VERSION}")
    print(f"semantics axis: {', '.join(semantics_names())}")
    print(f"active semantics: {spec['semantics']}")
    if spec["semantics"] != "graph":
        print("this generation executes graph only; the named semantics will be refused")
    for cell in spec["cells"]:
        n = cell["N"]
        accounting = template_accounting(n, cell["K_max"], len(spec.get("weights", ENUMERATED_WEIGHTS)))
        print(
            f"E(N={n}, K<={cell['K_max']}, O={spec.get('O', 2)}, G={spec.get('G', 0)}, "
            f"S={spec.get('S', 0)}, H={spec.get('H', 0)}, L={spec.get('L', 0)}, "
            f"semantics={spec['semantics']}, W={spec['alphabet']})"
        )
        print(
            f"  labelled states {accounting['labelled_states']}; "
            f"relation slots {accounting['relation_slots']}; "
            f"raw templates {accounting['raw_structural_templates']}; "
            f"syntax-invalid {accounting['removed_syntax_invalid']}; "
            f"redundant {accounting['removed_redundant_normalisation']}; "
            f"outside K {accounting['outside_k_bound']}; "
            f"normal forms {accounting['structural_normal_forms']}; "
            f"labelled constraints {accounting['labelled_constraints']}"
        )
        print(f"  cardinalities requested: {cell['cardinalities']}")
    for note in spec.get("unsearched", []):
        print(f"unsearched: {note}")
    return 0


def _enumerate(path: Path, kind: str, n: int) -> int:
    spec = load_spec(path)
    cell = next((item for item in spec["cells"] if item["N"] == n), None)
    if cell is None:
        print(f"N={n} is not a cell of {spec['experiment_id']}", file=sys.stderr)
        return 1
    if kind == "states":
        states = canonical_states(n)
        print(f"N={n} labelled {n_states(n)} canonical {len(states)} slots {edge_count(n)}")
        print("canonical states:", " ".join(str(state) for state in states[:32]))
        return 0
    grammar = build_grammar(n, cell["K_max"], spec["weights"])
    canonical = sum(1 for i in range(len(grammar.labelled)) if is_canonical_ids((i,), grammar.image))
    print(
        f"N={n} K<={cell['K_max']} labelled constraints {len(grammar.labelled)} "
        f"canonical singles {canonical}"
    )
    shown = 0
    for i, constraint in enumerate(grammar.labelled):
        if is_canonical_ids((i,), grammar.image):
            print(grammar.expression(i))
            shown += 1
            if shown >= 20:
                break
    return 0


def _replay(path: Path) -> int:
    stored = json.loads(path.read_text(encoding="utf-8"))
    n = stored["n"]
    constraints = tuple(parse_expression(text, n) for text in stored["expressions"])
    factors = alphabet_factors(stored["alphabet"])
    kernel = build_kernel(n, Choreography(stored.get("H", 0), stored.get("L", 0), constraints), factors)
    from rs_constraint_lab.state import edges

    regenerated = sample_trajectory(
        kernel,
        constraints,
        factors,
        edges(n),
        stored["initial_state"],
        stored["seed"],
        stored["horizon"],
        stored["spec_hash"],
        stored["constraint_set_id"],
    )
    if not replay_matches(stored, regenerated):
        print(f"replay diverged for {stored['run_id']}", file=sys.stderr)
        return 1
    print(f"replay matched {stored['run_id']} events={len(stored['events'])} final={stored['final_state']}")
    return 0


def _load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _report(path: Path) -> int:
    summary = _load_summary(path)
    print(f"{summary['experiment_id']} engine {summary['engine_version']} spec {summary['spec_hash']}")
    print(f"python {summary['python']} numpy {summary['numpy']} commit {summary['git_commit']}")
    print(f"runtime_seconds {summary['runtime_seconds']:.3f}")
    for cell in summary["cells"]:
        coord = cell["coordinate"]
        print(
            f"N={coord['N']} K<={coord['K_max']} families {cell['families']} "
            f"structural {cell['structural_families']} screened {cell['screened_families']} "
            f"baseline-equivalent {cell['baseline_equivalent_families']}"
        )
        for cardinality, counts in cell["cardinalities"].items():
            print(
                f"  cardinality {cardinality}: combinations {counts['labelled_combinations']} "
                f"canonical {counts['canonical']} symmetry-removed {counts['removed_by_symmetry']}"
            )
    return 0


def _compare(path: Path, ids: list[str]) -> int:
    summary = _load_summary(path)
    found = False
    for cell in summary["cells"]:
        for reference in cell.get("references") or []:
            single = reference.get("single") or {}
            if single.get("set_id") in ids or single.get("family_id") in ids or single.get("modal_family") in ids:
                print(json.dumps(reference, indent=2, sort_keys=True))
                found = True
    root = path.parent
    for jsonl in root.glob("families-*.jsonl"):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row["motif_id"] in ids:
                print(json.dumps({key: row[key] for key in ("motif_id", "tags", "count", "expressions", "observed")}, indent=2))
                found = True
    catalogue = path.parents[1] / "catalogue" if len(path.parents) > 1 else None
    if catalogue and catalogue.exists():
        for jsonl in catalogue.glob(f"{summary['experiment_id']}-families-*.jsonl"):
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                if row["motif_id"] in ids:
                    print(json.dumps({key: row[key] for key in ("motif_id", "tags", "count", "expressions", "observed")}, indent=2))
                    found = True
    if not found:
        print("no matching id in the summary references or family catalogue", file=sys.stderr)
        return 1
    return 0


def _catalogue(path: Path) -> int:
    summary = _load_summary(path)
    print(f"catalogue source {path}")
    print(f"experiment {summary['experiment_id']}")
    for cell in summary["cells"]:
        print(
            f"N={cell['coordinate']['N']} families {cell['families']} "
            f"structural {cell['structural_families']} screened {cell['screened_families']}"
        )
    return 0
