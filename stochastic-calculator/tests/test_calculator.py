import ast
from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import tempfile
import unittest

from rs_calc.calculator import calculate
from rs_calc.cli import main
from rs_calc.engine import Config, Engine, ResourceLimit, structural
from rs_calc.experiments import trial
from rs_calc.experiments import run
from rs_calc.metrics import summarize, wilson
from rs_calc.numbers import decode, encode
from rs_calc.operations import add, multiply
from rs_calc.provenance import ROOT
from rs_calc.radix import decode_decimal, encode_decimal, resolve
from rs_calc.verification import audit_sources, expected_binary


class MechanismTests(unittest.TestCase):
    def test_exhaustive_signed_grid(self):
        for seed in [1, 719]:
            for a in range(-9, 10):
                for b in range(-9, 10):
                    for op, symbol in [("add", "+"), ("sub", "-"), ("mul", "*"), ("div", "/")]:
                        if op == "div" and b == 0:
                            continue
                        with self.subTest(a=a, b=b, op=op, seed=seed):
                            self.assertEqual(calculate(f"({a}){symbol}({b})", seed).observed(),
                                             expected_binary(op, a, b))

    def test_conservation_and_validity(self):
        for locality in ["local", "global"]:
            for seed in range(30):
                engine = Engine(seed, Config(locality=locality))
                state = engine.perturb(encode(7, engine), "neutral", 10)
                with self.assertRaises(ValueError):
                    decode(state)
                result = engine.normalize(state)
                self.assertEqual(decode(result), 7)
                self.assertEqual(len({e.uid for e in result}), len(result))
                self.assertTrue(all(0 <= e.source < 8 and 0 <= e.target < 8 for e in result))

    def test_reproducibility_and_diversity(self):
        x = calculate("17+28", 123, trace=True)
        y = calculate("17+28", 123, trace=True)
        self.assertEqual(x.engine.events, y.engine.events)
        self.assertEqual(x.engine.trajectory, y.engine.trajectory)
        self.assertEqual(x.value, y.value)
        results = [calculate("17+28", seed) for seed in range(30)]
        self.assertEqual(len({r.engine.trajectory for r in results}), 30)
        self.assertEqual({r.observed()["value"] for r in results}, {45})

    def test_identity_loss_is_not_repaired(self):
        for seed in range(20):
            e = Engine(seed)
            self.assertEqual(decode(e.normalize(e.perturb(encode(7, e), "erase"))), 6)

    def test_chains(self):
        examples = {"(7+5)*3/4": 9, "2+3*4": 14, "-(3-7)*2": 8,
                    "100-37-48": 15, "(13//3)+1": 5, "(-13)%3": -1,
                    "(-13)//3": -4, "0*99": 0, "123+456": 579}
        for expression, expected in examples.items():
            self.assertEqual(calculate(expression).observed()["value"], expected)
        x = calculate("17+28")
        self.assertEqual(calculate("ans*2", answer=x.value).observed()["value"], 90)
        with self.assertRaises(ValueError):
            calculate("13/3+1")

    def test_invalid_and_limits(self):
        for expression in ["1.5+2", "True+1", "foo(3)", "2**3", "[1]", "ans"]:
            with self.assertRaises(ValueError):
                calculate(expression)
        with self.assertRaises(ZeroDivisionError):
            calculate("1/0")
        with self.assertRaises(ResourceLimit):
            calculate("100", config=Config(max_relations=20))
        with self.assertRaises(ResourceLimit):
            calculate("12*12", config=Config(max_relations=100))
        with self.assertRaises(ResourceLimit):
            calculate("9+9", config=Config(max_steps=1))
        with self.assertRaises(ValueError):
            Config(strength=float("nan"))

    def test_no_hidden_oracle(self):
        self.assertEqual(audit_sources(ROOT), [])
        # Observer failure must not prevent relational operation construction.
        from unittest.mock import patch
        with patch("rs_calc.numbers.decode", side_effect=AssertionError("observer used")):
            e = Engine(42)
            result = add(encode(17, e), encode(28, e), e)
            self.assertEqual(len(result), 45)

    def test_product_comparator(self):
        for seed in range(20):
            for model in ["product", "repeated"]:
                e = Engine(seed)
                self.assertEqual(decode(multiply(encode(-7, e), encode(6, e), e, model)), -42)


class RadixTests(unittest.TestCase):
    def test_carry_borrow_sign_grid(self):
        values = [-100, -48, -9, -1, 0, 1, 9, 37, 48, 100, 999]
        for seed in [0, 101]:
            for a in values:
                for b in values:
                    e = Engine(seed)
                    state = encode_decimal(a, e)
                    state.extend(encode_decimal(b, e))
                    self.assertEqual(int(decode_decimal(resolve(state, e))), a + b)

    def test_gate_ablation(self):
        for coordinated, expected in [(True, "85"), (False, "95")]:
            e = Engine(31, Config(fault_rate=1.0), trace=True)
            state = encode_decimal(37, e)
            state.extend(encode_decimal(48, e))
            self.assertEqual(decode_decimal(resolve(state, e, coordinated)), expected)
            self.assertEqual(e.counts["transmit"], 1)
            self.assertEqual(e.counts["carry"], 1)
            self.assertEqual(e.counts["receive"], 1)


class HarnessTests(unittest.TestCase):
    def test_seeded_trial(self):
        cell = {"experiment": "test", "label": "addition", "kind": "arithmetic", "a": 3, "b": 4, "op": "add"}
        a, b = trial((cell, {}, 42, 0)), trial((cell, {}, 42, 0))
        for key in ["result", "initial", "final", "iterations", "trajectory"]:
            self.assertEqual(a[key], b[key])
        summary = summarize([a, b])
        self.assertEqual(summary["accuracy"], 1)
        self.assertLess(summary["wilson95"][0], 1)
        self.assertEqual(wilson(0, 0), [0, 1])

    def test_censoring_and_intervention(self):
        cell = {"experiment": "test", "label": "censor", "kind": "arithmetic", "a": 17, "b": 28, "op": "add"}
        row = trial((cell, {"max_steps": 1}, 0, 0))
        self.assertFalse(row["converged"])
        self.assertFalse(row["correct"])
        self.assertIsNone(row["result"])
        self.assertIn("population", row["diagnostics"]["last_active_state"])
        cell["intervention"] = {"at": 10, "mode": "neutral", "pairs": 6}
        row = trial((cell, {}, 0, 0))
        self.assertTrue(row["diagnostics"]["intervention_applied"])
        self.assertTrue(row["correct"])

    def test_noise_destroyed_divisor_is_logged(self):
        cell = {"experiment": "test", "label": "divisor-loss", "kind": "arithmetic",
                "a": 4, "b": 1, "op": "div"}
        row = trial((cell, {"fault_rate": 1.0, "strength": 0.0}, 7, 0))
        self.assertFalse(row["converged"])
        self.assertIsNotNone(row["error"])

    def test_logging_replay_and_parallel_semantics(self):
        import gzip
        from rs_calc.replay import replay
        config = {"base_seed": 72, "replications": 1, "runs_per_cell": 2, "engine": {},
                  "cells": [{"experiment": "test", "label": "addition", "kind": "arithmetic",
                             "runs": 2, "a": 3, "b": 4, "op": "add"}]}
        with tempfile.TemporaryDirectory() as tmp:
            single, parallel = Path(tmp) / "single", Path(tmp) / "parallel"
            with redirect_stdout(io.StringIO()):
                run(config, single, workers=1)
                run(config, parallel, workers=2)
            self.assertTrue((single / "source.tar.gz").exists())
            self.assertTrue(replay(single, 72)["matches"])
            def paths(directory):
                with gzip.open(directory / "trials.jsonl.gz", "rt") as stream:
                    return [json.loads(line)["trajectory"] for line in stream]
            self.assertEqual(paths(single), paths(parallel))
            with self.assertRaises(FileExistsError):
                run(config, single)

    def test_cli(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["13/3", "--seed", "7", "--json"]), 0)
        output = json.loads(stream.getvalue())
        self.assertEqual((output["value"], output["remainder"]), (4, 1))
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["-13/3", "--seed", "7", "--json"]), 0)
        self.assertEqual(json.loads(stream.getvalue())["value"], -4)
        with redirect_stderr(io.StringIO()):
            self.assertEqual(main(["1/0"]), 2)


if __name__ == "__main__":
    unittest.main()
