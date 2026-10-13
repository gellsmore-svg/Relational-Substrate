"""Gravity-time Round G0 contracts.

Pre-freeze tests use N=4 fixtures, which are not a G0 size, and theorem-fixed
NULL behaviour. They do not compute any G0 observable of a non-null family.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys

import numpy as np
import pytest

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.explore08a import repository_root
from rs_constraint_lab import gt0
from rs_constraint_lab.gt0_exec import prepare_g0_plan

REPO = repository_root()


def _relabel(text: str, perm: tuple[int, ...], n: int) -> str:
    rule = parse_expression(text, n, order=2)
    from rs_constraint_lab.state import edges

    edge_list = edges(n)
    index = {pair: i for i, pair in enumerate(edge_list)}

    def move(slot: int) -> int:
        a, b = edge_list[slot]
        return index[tuple(sorted((perm[a], perm[b])))]

    return (rule.polarity, move(rule.action), tuple(sorted((move(c), v) for c, v in rule.conditions)), rule.weight)


@pytest.mark.parametrize("family,grade,k", [("DENS", "weak_favour", 1), ("ADJ", "weak_favour", 2), ("CLOSE", "strong_favour", 3), ("HOLD", "weak_suppress", 3), ("LOCK", "prohibit", 3)])
def test_templates_parse_with_declared_k_and_are_label_covariant(family: str, grade: str, k: int) -> None:
    n = 5
    texts = gt0.template_expressions(family, n, grade)
    rules = [parse_expression(t, n, order=2) for t in texts]
    assert all(rule.k() == k for rule in rules)
    keys = {(r.polarity, r.action, r.conditions, r.weight) for r in rules}
    for perm in itertools.permutations(range(n)):
        assert {_relabel(t, perm, n) for t in texts} == keys


def test_held_scaffold_prohibits_only_source_dissolution() -> None:
    texts = gt0.scaffold_expressions("HELD")
    assert texts == ["dissolve(0-1) => prohibit", "dissolve(0-2) => prohibit", "dissolve(1-2) => prohibit"]
    assert gt0.scaffold_expressions("FREE") == []


def test_n4_fixtures_null_uniform_and_lock_absorbs() -> None:
    null = gt0.analyse_item({"family": "NULL", "grade": None, "mode": "FREE", "n": 4, "item_id": "fixture"})
    assert null["regime"] == "recurrent" and max(null["max_deviation_from_uniform"].values()) < 1e-12
    lock = gt0.analyse_item({"family": "LOCK", "grade": "prohibit", "mode": "FREE", "n": 4, "item_id": "fixture"})
    assert lock["regime"] == "absorbing" and lock["absorbing_states"] == [63]
    assert abs(sum(lock["absorption_probabilities"].values()) - 1.0) < 1e-12


def test_dense_and_lazy_solvers_agree_on_an_n4_fixture() -> None:
    kernel = gt0.build("CLOSE", 4, "strong_favour", "FREE")
    states = gt0.reachable(kernel, 0)
    dense, r1 = gt0.stationary_dense(kernel, states)
    lazy, r2, _ = gt0.stationary_lazy(kernel, states)
    assert r1 < 1e-12 and r2 < 1e-12 and float(np.abs(dense - lazy).max()) < 1e-12


def test_continuous_time_law_reweights_by_inverse_total_rate() -> None:
    pi = np.array([0.5, 0.5])
    assert np.allclose(gt0.continuous_time(pi, np.array([1.0, 3.0])), [0.75, 0.25])


def test_null_triangle_conditional_counts_at_n4() -> None:
    values = gt0.null_triangles_given_edges(4)
    assert values["0"] == 0 and values["6"] == 4
    assert abs(values["3"] - 4 / 20) < 1e-12


def test_g0_plan_contract() -> None:
    plan = prepare_g0_plan()
    assert plan["plan_hash"] == plan_hash(plan)
    assert len(plan["items"]) == 40
    assert plan["new_primitives"] is False and plan["history"] is False
    blob = json.dumps(plan)
    for key in ("attachment_fraction\":", "radial_drift_among_finite_moves\":"):
        assert key not in blob


def test_cli_refuses_without_a_frozen_plan() -> None:
    completed = subprocess.run([sys.executable, "-m", "rs_constraint_lab", "gt0", "verify", "--allow-unpushed"], cwd=REPO, capture_output=True, text=True, check=False)
    assert completed.returncode == 2
    assert "frozen plan" in completed.stderr.lower()
