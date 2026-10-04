from dataclasses import replace
import unittest

from rs_calc.constraint_lab import observe
from rs_calc.defect_prediction import stationary
from rs_calc.dynamics_lab import trial, validate
from rs_calc.proposal_kernel import Bond, Constraints, Proposal, proposals, transition as fixed
from rs_calc.recurrent_kernel import RecurrentRule, transition


class RecurrentTests(unittest.TestCase):
    def test_birth_and_cancellation_both_possible(self):
        state = (Bond(True, 0, 1, True),)
        p = Proposal("pair_birth", 1, 2, 0, 1, True, .1)
        grown, status = transition(state, p, RecurrentRule(.2), 32)
        self.assertEqual(status, "accepted")
        recovered, status = transition(grown, replace(p, kind="cancel"), RecurrentRule(.2), 32)
        self.assertEqual(recovered, state)
        self.assertEqual(status, "accepted")
        self.assertEqual(transition(state, replace(p, enforcement=.8), RecurrentRule(.2), 32)[1], "birth_bias")

    def test_conservation_and_zero_bias_comparator(self):
        initial = (Bond(True, 0, 1), Bond(False, 1, 0), Bond(True, 0, 1))
        for rate in (0, .01, .2, .5, 1):
            state = initial
            for p in proposals(192, 1000, 8):
                state, _ = transition(state, p, RecurrentRule(rate), 32)
                self.assertEqual(observe(list(state))[0], 1)
        left = right = initial
        for p in proposals(92, 1000, 8):
            left, _ = transition(left, p, RecurrentRule(0), 32)
            right, _ = fixed(right, p, Constraints(readiness=False), 32)
            self.assertEqual(left, right)

    def test_stationary_flow_and_boundaries(self):
        for q in (0, 1, 7, 12):
            for b in (0, .01, .2, .5, 1):
                pi = stationary(q, 32, b)
                self.assertAlmostEqual(sum(pi), 1)
                for k in range(len(pi)-1):
                    death = 2*(k+1)*(q+k+1)/(q+2*k+2)**2
                    self.assertAlmostEqual(pi[k]*b, pi[k+1]*death)
        self.assertEqual(stationary(7, 7, .2), [1.0])
        with self.assertRaises(ValueError):
            stationary(8, 7, .2)
        with self.assertRaises(ValueError):
            RecurrentRule(-.1)

    def test_tapes_match_fixed_kernel_and_invalid_policy_rejected(self):
        config = {"experiment": "test", "base_seed": 1, "runs": 1, "regions": 8,
                  "neutral_pairs": 3, "horizons": [100], "burn_in": 50,
                  "cells": [{"label": "recurrent", "inputs": [3,4], "capacity": 32,
                             "constraints": {"no_growth": False, "readiness": False}, "birth_admission": .2}]}
        cell = config["cells"][0]
        a = trial(cell, 92, config)[0]
        fixed_cell = {k:v for k,v in cell.items() if k != "birth_admission"}
        b = trial(fixed_cell, 92, config)[0]
        self.assertEqual(a["proposal_tape"], b["proposal_tape"])
        bad = {**cell, "constraints": {}}
        with self.assertRaises(ValueError):
            validate({**config, "cells": [bad]})
        with self.assertRaises(ValueError):
            trial(bad, 92, config)


if __name__ == "__main__":
    unittest.main()
