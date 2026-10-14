"""Gravity-time open-thetical Round E0A contracts.

Pre-freeze tests use a synthetic 4-state cycle with analytic values, N=4
fixtures (not an E0A size) of theorem-fixed gradient families, and parse-level
checks of the non-gradient templates. They compute no E0A observable of a
non-null family at N=5 or N=6.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys

import numpy as np
import pytest

from rs_constraint_lab import gte0a
from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.explore08a import repository_root
from rs_constraint_lab.state import edges

REPO = repository_root()


def _cycle_fixture() -> gte0a.Chain:
    """Two slots, four states, forward cycle 0->1->3->2->0 at rate 2 and reverse at rate 1."""
    states = np.arange(4)
    forward = {(0, 0), (1, 1), (3, 0), (2, 1)}
    W = np.array([[2.0 if (i, e) in forward else 1.0 for e in range(2)] for i in range(4)])
    T = np.array([[i ^ (1 << e) for e in range(2)] for i in range(4)], dtype=np.int64)
    return gte0a.Chain(2, states, W, T)


def test_synthetic_cycle_reversibility_spectrum_and_autocorrelation() -> None:
    chain = _cycle_fixture()
    stat = gte0a.stationary(chain)
    assert np.allclose(stat["ct"], 0.25) and abs(stat["mean_rate_ct"] - 3.0) < 1e-12
    rev = gte0a.reversibility(chain, stat["ct"], stat["mean_rate_ct"])
    assert abs(rev["entropy_production_per_time"] - math.log(2)) < 1e-12
    assert abs(rev["max_square_affinity"] - math.log(16)) < 1e-12
    assert abs(rev["irreversible_flux_fraction"] - 1 / 3) < 1e-12
    spec = gte0a.spectrum(chain, stat["mean_rate_ct"])
    # generator eigenvalues -3 +- i and -6, divided by the mean rate 3
    assert abs(spec["relaxation_gap"] - 1.0) < 1e-12 and abs(spec["slowest_mode"][1] - 1 / 3) < 1e-12
    assert spec["complex_eigenvalue_count"] == 2 and abs(spec["max_oscillation_index"] - 1 / 3) < 1e-12
    tau = gte0a.autocorrelation_times(chain, stat["ct"], stat["mean_rate_ct"], {"bit0": (chain.states & 1).astype(float)})
    assert abs(tau["bit0"]["time"] - 0.3) < 1e-12  # checked against direct quadrature of C(t)


@pytest.mark.parametrize("kind,k", [("close_form", 3), ("close_dissolve", 3), ("adj_form", 2), ("path_form", 3), ("path_dissolve", 3)])
def test_components_parse_with_declared_k_and_are_label_covariant(kind: str, k: int) -> None:
    n = 5
    texts = gte0a.component_expressions(kind, n, "weak_favour")
    rules = [parse_expression(t, n, order=2) for t in texts]
    assert all(rule.k() == k for rule in rules)
    edge_list = edges(n)
    index = {pair: i for i, pair in enumerate(edge_list)}

    def key(rule, perm):
        def move(slot):
            a, b = edge_list[slot]
            return index[tuple(sorted((perm[a], perm[b])))]

        return (rule.polarity, move(rule.action), tuple(sorted((move(c), v) for c, v in rule.conditions)), rule.weight)

    identity = tuple(range(n))
    base = sorted(key(r, identity) for r in rules)
    for perm in itertools.permutations(range(n)):
        assert sorted(key(r, perm) for r in rules) == base


def test_path_witness_count() -> None:
    for n in (5, 6):
        assert len(gte0a.component_expressions("path_form", n, "weak_favour")) == math.comb(n, 2) * 2 * (n - 2) * (n - 3)


def test_gradient_classification_and_predicted_potentials() -> None:
    assert not gte0a.is_gradient("PATHF") and not gte0a.is_gradient("PATHH")
    assert gte0a.predicted_potential("COMPETE", "strong_favour+strong_favour")["theta"] == {"E": 0.0, "W": 0.0, "T": 0.0}
    split = gte0a.predicted_potential("SPLIT", "weak_favour+weak_suppress")["theta"]["T"]
    assert abs(split - gte0a.predicted_potential("CLOSE", "strong_favour")["theta"]["T"]) < 1e-15
    assert abs(split - gte0a.predicted_potential("HOLD", "strong_suppress")["theta"]["T"]) < 1e-15
    assert gte0a.predicted_potential("EXCL", "prohibit")["restricted_support"] is True
    frust = gte0a.predicted_potential("FRUST", "weak_favour+strong_favour")["theta"]
    assert abs(frust["W"] - math.log(2)) < 1e-15 and abs(frust["T"] + math.log(4)) < 1e-15


@pytest.mark.parametrize("family,grade,mode", [("NULL", "none", "FREE"), ("NULL", "none", "HELD"), ("CLOSE", "strong_favour", "FREE"), ("CLOSE", "strong_favour", "HELD")])
def test_n4_gradient_fixtures(family: str, grade: str, mode: str) -> None:
    result, trajectories = gte0a.analyse_item({"family": family, "grade": grade, "item_id": "fixture", "mode": mode, "n": 4})
    assert result["regime"] == "recurrent"
    assert result["reversibility"]["irreversible_flux_fraction"] < 1e-12
    assert result["event_order"]["pattern_asymmetry"] < 1e-12
    assert result["predicted_law_l1_gap"] < 1e-12 and abs(result["gibbs_projection"]["kl_nats"]) < 1e-12
    assert result["symmetry_max_abs_difference"] < 1e-12
    assert result["spectrum"]["max_abs_imag_relative"] < 1e-9
    if family == "NULL" and mode == "FREE":
        assert abs(result["autocorrelation"]["edges"]["time"] - 0.5) < 1e-12
        assert abs(result["localisation_persistence_index"] - 1.0) < 1e-12
    assert len(trajectories["trajectories"]) == gte0a.TRAJECTORIES_PER_CELL


def test_trajectories_replay_deterministically() -> None:
    kernel = gte0a.build("CLOSE", "strong_favour", 4, "FREE")
    chain = gte0a.chain_from_kernel(kernel, 0)
    one = gte0a.sample_trajectory(chain, 0, gte0a.trajectory_seed("fixture", 0), 50)
    two = gte0a.sample_trajectory(chain, 0, gte0a.trajectory_seed("fixture", 0), 50)
    assert one == two and len(one["events"]) == 50
    state = 0
    for slot, bit, _t in one["events"]:
        assert ((state >> slot) & 1) != bit
        state ^= 1 << slot


def test_e0a_plan_contract() -> None:
    plan = gte0a.prepare_plan()
    assert plan["plan_hash"] == plan_hash(plan)
    assert len(plan["items"]) == 48 and len({i["item_id"] for i in plan["items"]}) == 48
    assert plan["new_primitives"] is False and plan["history"] is False and plan["parameter_fit"] is False
    blob = json.dumps(plan)
    for key in ("irreversible_flux_fraction\":", "class_table\":", "relaxation_gap\":"):
        assert key not in blob


def test_cli_refuses_without_a_frozen_plan() -> None:
    completed = subprocess.run([sys.executable, "-m", "rs_constraint_lab", "gte0a", "run", "--allow-unpushed"], cwd=REPO, capture_output=True, text=True, check=False)
    assert completed.returncode == 2
    assert "frozen plan" in completed.stderr.lower()
