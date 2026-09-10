"""Calculator and research entry points."""

import argparse
import json
from pathlib import Path
import secrets
import sys
import re

from .calculator import calculate
from .engine import Config, Engine, ResourceLimit
from .experiments import run
from .provenance import ROOT, timestamp
from .radix import decode_decimal, encode_decimal, resolve

OPS = {"add": "+", "sub": "-", "mul": "*", "div": "/"}


def configuration(args):
    return Config(locality=args.locality, strength=args.strength,
                  fault_rate=args.noise, max_steps=args.max_steps,
                  max_relations=args.max_relations)


def common(parser):
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strength", type=float, default=1.0)
    parser.add_argument("--noise", type=float, default=0.0)
    parser.add_argument("--locality", choices=["local", "global"], default="global")
    parser.add_argument("--max-steps", type=int, default=100000)
    parser.add_argument("--max-relations", type=int, default=20000)


def display(calculation, verbose=False, json_output=False, include_trace=False):
    engine = calculation.engine
    result = calculation.observed()
    packet = {**result, "converged": True, "convergence_means": "structural normal form",
              "confidence": None, "seed": engine.seed, "iterations": engine.steps,
              "trajectory": engine.trajectory, "events": dict(engine.counts)}
    if include_trace:
        packet["trace"] = engine.events
    if json_output or include_trace:
        print(json.dumps(packet, indent=2))
    else:
        rendered = str(result["value"])
        if result["remainder"]:
            rendered += f' remainder {result["remainder"]}'
        print(rendered)
        if verbose:
            print(f"Converged: yes (structural normal form)\nIterations: {engine.steps}")
            print(f"Seed: {engine.seed}\nTrajectory ID: {engine.trajectory}")
            print(f"Constraint profile: {engine.config}")
            print("Confidence: not estimated for a single run")
            print("Transitions:", json.dumps(dict(engine.counts), sort_keys=True))


def research_command(argv):
    command = argv[0]
    parser = argparse.ArgumentParser(prog=f"rs-calc {command}")
    if command == "sweep":
        parser.add_argument("axis", choices=["constraint"])
    if command == "carry":
        parser.add_argument("a", type=int)
        parser.add_argument("b", type=int)
    else:
        parser.add_argument("operation", choices=OPS)
        parser.add_argument("a", type=int)
        parser.add_argument("b", type=int)
    common(parser)
    parser.add_argument("--runs", type=int, default=100)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--perturbation", choices=["neutral", "erase", "flip"], default="neutral")
    args = parser.parse_args(argv[1:])
    seed = args.seed if args.seed is not None else secrets.randbits(48)
    config = configuration(args)
    if command == "carry":
        engine = Engine(seed, config, trace=args.verbose)
        state = encode_decimal(args.a, engine)
        state.extend(encode_decimal(args.b, engine))
        result = decode_decimal(resolve(state, engine))
        print(json.dumps({"value": result, "seed": seed, "iterations": engine.steps,
                          "trajectory": engine.trajectory, "events": dict(engine.counts),
                          "trace": engine.events}, indent=2) if args.json or args.verbose else result)
        return
    expression = f"({args.a}) {OPS[args.operation]} ({args.b})"
    if command == "trace":
        display(calculate(expression, seed, config, trace=True), include_trace=True)
        return
    if args.runs < 1:
        raise ValueError("--runs must be positive")
    programme = json.loads((ROOT / "configs/programme.json").read_text())
    programme.update(base_seed=seed, replications=1, runs_per_cell=args.runs)
    cell = {"experiment": "CLI", "label": command, "kind": "arithmetic", "runs": args.runs,
            "op": args.operation, "a": args.a, "b": args.b,
            "strength": args.strength, "fault_rate": args.noise, "locality": args.locality,
            "max_steps": args.max_steps, "max_relations": args.max_relations}
    if command == "perturb":
        cell["intervention"] = {"at": 2, "mode": args.perturbation, "pairs": 6}
    cells = [cell]
    if command == "sweep":
        cells = [{**cell, "label": f"strength-{strength}", "strength": strength,
                  "fault_rate": args.noise or 0.15} for strength in programme["strengths"]]
    programme["cells"] = cells
    output = args.output or ROOT / "research/runs" / ("local-" + timestamp().replace(":", "-"))
    summaries = run(programme, output, args.workers)
    for key, summary in summaries.items():
        print(f'{key}: {summary["correct"]}/{summary["runs"]} correct; 95% CI {summary["wilson95"]}')


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if argv and argv[0] in {"experiment", "sweep", "perturb", "trace", "carry"}:
            research_command(argv)
            return 0
        parser = argparse.ArgumentParser(prog="rs-calc", description="Stochastic relational integer calculator")
        parser.add_argument("expression", nargs="?")
        common(parser)
        value_options = {"--seed", "--strength", "--noise", "--max-steps", "--max-relations"}
        for index, token in enumerate(argv):
            if token == "--":
                break
            if re.match(r"^-\s*(?:\d|\()", token) and (index == 0 or argv[index - 1] not in value_options):
                argv = argv[:index] + argv[index + 1:] + ["--", token]
                break
        args = parser.parse_args(argv)
        config = configuration(args)
        seed = args.seed if args.seed is not None else secrets.randbits(48)
        if args.expression is not None:
            display(calculate(args.expression, seed, config), args.verbose, args.json)
            return 0
        answer = None
        while True:
            try:
                expression = input("rs-calc> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return 0
            if expression in {"quit", "exit", ":q"}:
                return 0
            if not expression:
                continue
            try:
                calculation = calculate(expression, seed, config, answer=answer)
                display(calculation, args.verbose, args.json)
                answer = calculation.value
            except (ValueError, SyntaxError, ZeroDivisionError, ResourceLimit) as exc:
                print(f"Error: {exc}", file=sys.stderr)
            seed += 1
    except (ValueError, SyntaxError, ZeroDivisionError, ResourceLimit) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
