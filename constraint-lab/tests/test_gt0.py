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


def test_sparse_and_dense_absorption_agree(monkeypatch: pytest.MonkeyPatch) -> None:
    for n, mode in ((4, "FREE"), (4, "HELD")):
        kernel = gt0.build("LOCK", n, "prohibit", mode)
        start = gt0.start_state(n, mode)
        states = gt0.reachable(kernel, start)
        absorbing = gt0.class_structure(kernel, states)["absorbing_states"]
        dense = gt0.absorption(kernel, states, start, absorbing)
        monkeypatch.setattr(gt0, "DENSE_ABSORPTION_LIMIT", 0)
        sparse = gt0.absorption(kernel, states, start, absorbing)
        monkeypatch.setattr(gt0, "DENSE_ABSORPTION_LIMIT", 4096)
        assert sparse["absorption_method"] == "sparse_iteration"
        assert abs(dense["expected_steps_to_absorption"] - sparse["expected_steps_to_absorption"]) <= 1e-10 * dense["expected_steps_to_absorption"]
        for key, value in dense["absorption_probabilities"].items():
            assert abs(value - sparse["absorption_probabilities"][key]) < 1e-10


def test_gibbs_identity_on_an_n4_fixture() -> None:
    from rs_constraint_lab.state import edges

    el = edges(4)
    for family, grade, m in (("CLOSE", "strong_favour", 4.0), ("HOLD", "strong_suppress", 4.0), ("DENS", "weak_favour", 2.0)):
        kernel = gt0.build(family, 4, grade, "FREE")
        states = gt0.reachable(kernel, 0)
        pi, _ = gt0.stationary_dense(kernel, states)
        ct = gt0.continuous_time(pi, gt0.total_rates(kernel, states))
        stat = (lambda s: s.bit_count()) if family == "DENS" else (lambda s: gt0.triangles(s, 4, el))
        g = np.array([m ** stat(s) for s in states])
        assert float(np.abs(ct - g / g.sum()).max()) < 1e-12


def test_g1_fixture_and_plan_contract() -> None:
    from rs_constraint_lab import gt1

    plan = gt1.prepare_plan()
    assert plan["plan_hash"] == plan_hash(plan) and len(plan["items"]) == 18
    item = {"family": "CLOSE", "grade": "strong_favour", "item_id": "fixture", "mode": "HELD", "n": 4}
    result = gt1.analyse_item(item)
    assert set(result) >= {"jump", "continuous"} and result["stationary_residual"] < 1e-12


def test_g0_journey_descends_from_its_frozen_plan() -> None:
    from rs_constraint_lab.explore08a import verify_journey_chronology

    reports = verify_journey_chronology(REPO, REPO / "gravity-time" / "plans" / "journey.jsonl")
    g0 = [r for r in reports if r["frozen_plan_commit"] == "b45f10b148fe7df1f54ffb7db35d4ea828b170ef"]
    assert g0 and g0[0]["result_commit"] == "97c2daa5d445e57110fa64baa690e64934a6373a"


def test_g1_journey_and_published_tables() -> None:
    from rs_constraint_lab.durable import canonical_json, sha256_bytes
    from rs_constraint_lab.explore08a import verify_journey_chronology

    reports = verify_journey_chronology(REPO, REPO / "gravity-time" / "plans" / "journey.jsonl")
    g1 = [r for r in reports if r["frozen_plan_commit"] == "331d5197dc5332aaf14b57c8661eb7004b54e259"]
    assert g1 and g1[0]["result_commit"] == "3dccd0a3f0e5227ef7e373d1aada7d01f6fcfba9"
    for name in ("round-g0-tables.json", "round-g1-tables.json"):
        body = json.loads((REPO / "gravity-time" / "reports" / name).read_text(encoding="utf-8"))
        payload = {k: v for k, v in body.items() if k != "payload_sha256"}
        assert sha256_bytes(canonical_json(payload).encode("utf-8")) == body["payload_sha256"]
    g1t = json.loads((REPO / "gravity-time" / "reports" / "round-g1-tables.json").read_text(encoding="utf-8"))
    assert all(v["holds"] for k, v in g1t["frozen_predictions"].items() if k.startswith(("P1", "P3")))
    assert sum(v["holds"] for k, v in g1t["frozen_predictions"].items() if k.startswith("P2")) == 1


def test_gt_coherence_ledger_is_valid_and_views_match() -> None:
    from rs_constraint_lab.coherence import build_markdown, build_mermaid, load_ledger, validate_ledger

    root = REPO / "gravity-time" / "coherence"
    findings, relations = load_ledger(root)
    assert validate_ledger(findings, relations) == []
    assert (root / "current-map.md").read_text(encoding="utf-8") == build_markdown(findings, relations)
    assert (root / "current-map.mmd").read_text(encoding="utf-8") == build_mermaid(findings, relations)
    statuses = {row["finding_id"]: row["status"] for row in findings}
    assert statuses["GT-Q01-KINETIC-CONVENTION"] == "unresolved"
    assert all("overall_score" not in row for row in findings)
