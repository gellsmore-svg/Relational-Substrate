from dataclasses import replace
import gzip
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from rs_calc.constraint_lab import encode, observe, run, trial
from rs_calc.proposal_kernel import Bond, Constraints, KINDS, Proposal, proposals, transition


class ConstraintLabTests(unittest.TestCase):
    def test_local_conservation_predicate_exhaustively(self):
        for signs in itertools.product((False, True), repeat=3):
            state = tuple(Bond(sign, 0, 1) for sign in signs)
            for kind, i, j, sign in itertools.product(KINDS, range(3), range(3), (False, True)):
                p = Proposal(kind, i, j, 1, 0, sign, 0.5)
                out, _ = transition(state, p, Constraints(no_growth=False, readiness=False), 20)
                self.assertEqual(observe(state)[0], observe(out)[0])

    def test_monotone_constraints(self):
        state = (Bond(True, 0, 1, True), Bond(False, 1, 0))
        for p in proposals(72, 500, 8):
            out, _ = transition(state, p, Constraints(), 20)
            before = (len(state), sum(not b.ready for b in state))
            after = (len(out), sum(not b.ready for b in out))
            self.assertLessEqual(after, before)
            state = out

    def test_tape_independent_of_constraints_and_state(self):
        left, right = encode([3, 4], 3, 8), ()
        a, b = [], []
        for p in proposals(91, 100, 8):
            a.append(p)
            left, _ = transition(left, p, Constraints(), 128)
        for p in proposals(91, 100, 8):
            b.append(p)
            right, _ = transition(right, p, Constraints(0, False, False), 128)
        self.assertEqual(a, b)
        self.assertNotEqual(left, right)

    def test_each_gate_has_a_distinct_effect(self):
        state = (Bond(True, 0, 1, True), Bond(True, 1, 0, True))
        examples = [("death", Constraints(), "conservation"),
                    ("cancel", Constraints(), "conservation"),
                    ("pair_birth", Constraints(), "growth"),
                    ("unready", Constraints(), "readiness")]
        for kind, c, reason in examples:
            p = Proposal(kind, 0, 1, 0, 1, True, 0.5)
            self.assertEqual(transition(state, p, c, 10)[1], reason)
            off = Constraints(0, False, False)
            self.assertEqual(transition(state, p, off, 10)[1], "accepted")

    def test_capacity_locality_and_empty(self):
        with self.assertRaises(ValueError):
            encode([10**20], 0, 8, capacity=16)
        with self.assertRaises(ValueError):
            encode([], 10**20, 8, capacity=16)
        state = (Bond(True, 0, 1), Bond(False, 1, 0))
        p = Proposal("pair_birth", 0, 1, 0, 1, True, 0.5)
        self.assertEqual(transition(state, p, Constraints(no_growth=False), 2)[1], "capacity")
        p = replace(p, kind="cancel")
        self.assertEqual(transition(state, p, Constraints(local_cancel=True), 2)[1], "locality")
        self.assertEqual(transition((), p, Constraints(), 2)[1], "inapplicable")

    def test_signed_inputs_and_no_readable_escape_under_full_constraints(self):
        config = {"neutral_pairs": 3, "regions": 8, "capacity": 128, "horizon": 2000}
        for inputs in ([0, 0], [3, -7], [3, 4], [17, 28]):
            for seed in range(10):
                row = trial({"experiment": "test", "label": "full", "inputs": inputs,
                             "constraints": {}}, seed, config)
                # Fixed horizons are not convergence guarantees, especially at scale.
                if row["readable"]:
                    self.assertTrue(row["correct"])
                self.assertEqual(row["identity_violating_steps"], 0)
                self.assertEqual(row["escapes"], 0)

    def test_logging_reproduction_and_validation(self):
        config = {"neutral_pairs": 1, "regions": 8, "capacity": 32, "horizon": 50,
                  "runs": 2, "base_seed": 1, "cells": [{"experiment": "test", "label": "full",
                  "inputs": [3, 4], "constraints": {}}]}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "run"
            run(config, path)
            self.assertTrue((path / "source.tar.gz").exists())
            with gzip.open(path / "trials.jsonl.gz", "rt") as stream:
                rows = [json.loads(line) for line in stream]
            self.assertEqual(len(rows), 2)
            replay = trial(config["cells"][0], 1, config)
            for key in rows[0].keys() - {"timestamp", "seconds"}:
                self.assertEqual(rows[0][key], replay[key], key)
            with self.assertRaises(FileExistsError):
                run(config, path)
            with self.assertRaises(ValueError):
                run({**config, "horizon": 0}, Path(temp) / "invalid")
            self.assertFalse((Path(temp) / "invalid").exists())


if __name__ == "__main__":
    unittest.main()
