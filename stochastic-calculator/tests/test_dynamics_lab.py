import gzip
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

from rs_calc.dynamics_lab import ReadoutWindow, observations, run, trial, validate
from rs_calc.analyze_dynamics import load_run
from rs_calc.proposal_kernel import Bond


class DynamicsLabTests(unittest.TestCase):
    def config(self):
        return {"experiment": "test", "base_seed": 1, "runs": 2, "regions": 8,
                "neutral_pairs": 2, "horizons": [100, 300], "burn_in": 0,
                "cells": [{"label": "CG", "inputs": [3, 4], "capacity": 32,
                           "constraints": {"readiness": False}}]}

    def test_two_passive_readouts(self):
        p, n = Bond(True, 0, 1), Bond(False, 1, 0)
        values, charge, defect = observations((p, n, p))
        self.assertEqual(values, {"pure": None, "ready": None})
        self.assertEqual((charge, defect), (1, 1))
        self.assertEqual(observations((p, p))[0], {"pure": 2, "ready": None})
        self.assertEqual(observations(())[0], {"pure": 0, "ready": 0})

    def test_checkpoint_prefix_and_readout_nesting(self):
        config = self.config()
        cell = config["cells"][0]
        longer = trial(cell, 72, config)
        short = trial(cell, 72, {**config, "horizons": [100]})[0]
        for key in short.keys() - {"timestamp", "seconds"}:
            self.assertEqual(short[key], longer[0][key], key)
        for row in longer:
            self.assertEqual(sum(row["population_occupancy"].values()), row["window_steps"])
            self.assertEqual(row["identity_violating_steps"], 0)
            self.assertLessEqual(row["observers"]["ready"]["correct_steps"], row["observers"]["pure"]["correct_steps"])

    def test_episode_censoring(self):
        window = ReadoutWindow(True, start=10)
        for step, value in [(11, 7), (12, None), (13, None), (14, 7), (15, 7), (16, None)]:
            window.update(value, 7, step)
        row = window.snapshot(None, 7, 18)
        self.assertEqual(row["complete_residences"], [2])
        self.assertEqual(row["complete_recoveries"], [2])
        self.assertEqual((row["captures"], row["escapes"]), (1, 2))
        self.assertEqual(row["right_censored_recovery"], 2)
        self.assertFalse(row["terminal_episode_left_censored"])
        initial = ReadoutWindow(True, start=10).snapshot(7, 7, 18)
        self.assertEqual(initial["right_censored_residence"], 8)
        self.assertTrue(initial["terminal_episode_left_censored"])

    def test_burn_in_does_not_change_dynamics(self):
        config = self.config()
        cell = config["cells"][0]
        full = trial(cell, 91, config)[-1]
        burnt = trial(cell, 91, {**config, "burn_in": 50})[-1]
        for key in ("final", "proposal_tape", "trajectory", "events"):
            self.assertEqual(full[key], burnt[key])
        self.assertEqual(sum(burnt["defect_occupancy"].values()), 250)

    def test_readiness_gate_does_not_change_purity(self):
        config = self.config()
        cg = config["cells"][0]
        cgr = {**cg, "constraints": {}}
        a, b = trial(cg, 14, config), trial(cgr, 14, config)
        for x, y in zip(a, b):
            self.assertEqual(x["observers"]["pure"], y["observers"]["pure"])
            self.assertEqual(x["defect_occupancy"], y["defect_occupancy"])

    def test_logging_protocol_and_invalid_config(self):
        config = self.config()
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            run(config, output)
            self.assertTrue((output / "protocol.md").exists())
            with gzip.open(output / "trials.jsonl.gz", "rt") as f:
                rows = [json.loads(line) for line in f]
            self.assertEqual(len(rows), 4)
            loaded, groups = load_run(output)
            self.assertEqual(loaded, config)
            self.assertEqual(len(groups), 2)
            replay = subprocess.run([sys.executable, "-m", "rs_calc.dynamics_lab", "--replay", str(output)],
                                    capture_output=True, text=True)
            self.assertEqual(replay.returncode, 0, replay.stderr)
            self.assertIn("4 checkpoint records", replay.stdout)
            with self.assertRaises(FileExistsError):
                run(config, output)
            with gzip.open(output / "trials.jsonl.gz", "at") as f:
                f.write(json.dumps(rows[0]) + "\n")
            with self.assertRaises(ValueError):
                load_run(output)
            with gzip.open(output / "trials.jsonl.gz", "wt") as f:
                for row in rows[:-1]:
                    f.write(json.dumps(row) + "\n")
            replay = subprocess.run([sys.executable, "-m", "rs_calc.dynamics_lab", "--replay", str(output)],
                                    capture_output=True, text=True)
            self.assertNotEqual(replay.returncode, 0)
            self.assertIn("Incomplete replay dataset", replay.stderr)
        for change in ({"horizons": [300, 100]}, {"horizons": [100, 100]}, {"burn_in": 100}, {"runs": 0}):
            with self.assertRaises(ValueError):
                validate({**config, **change})


if __name__ == "__main__":
    unittest.main()
