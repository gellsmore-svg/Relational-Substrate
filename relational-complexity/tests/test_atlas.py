"""Opening constraint grammar. These tests do not run a frozen atlas round."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from rrc import ENGINE_VERSION
from rrc.cli import main
from rrc.constraints import (
    compile_model,
    compile_weight_table,
    weight_table_hash,
)
from rrc.items import execute_atlas_core
from rrc.model import stationary_dense
from rrc.runner import execute_plan

ROOT = Path(__file__).resolve().parents[1]
COMPLETE = {"kind": "complete"}
BUDGET = {
    "tolerance": 1e-12,
    "cross_tolerance": 1e-8,
    "max_iter": 10000,
    "dense_max_states": 1024,
}


def _spec(**overrides):
    payload = {
        "id": "fixture",
        "round_id": "fixture",
        "type": "atlas_core",
        "n": 3,
        "carrier": COMPLETE,
        "constraints": [],
        "baseline": 1,
        "role": "fixture",
    }
    payload.update(BUDGET)
    payload.update(overrides)
    return payload


def _prohibit(event, condition, polarity="present", action="either"):
    return {
        "effect": "prohibit",
        "event": [event[0], event[1]],
        "action": action,
        "when": {"edge": [condition[0], condition[1]], "polarity": polarity},
    }


def _multiply(event, condition, factor=4, polarity="present", action="either"):
    return {
        "effect": "multiply",
        "factor": factor,
        "event": [event[0], event[1]],
        "action": action,
        "when": {"edge": [condition[0], condition[1]], "polarity": polarity},
    }


def test_baseline_is_ones_and_the_integer_occupation_is_exact():
    result = execute_atlas_core(_spec())
    assert result["status"] == "complete"
    assert result["engine_version"] == ENGINE_VERSION
    assert result["n_states"] == 8
    assert result["n_edges"] == 3
    assert result["empirical_bit_independent"] is True
    assert result["action_bit_independent"] is True
    weights = compile_weight_table(3, COMPLETE, [])
    assert np.array_equal(weights, np.ones((8, 3), dtype=np.int64))
    book = result["bookkeeping"]
    assert book["declared_cardinality"] == 0
    assert book["j_positive"] == 0
    assert book["j_prohibit"] == 0
    assert book["max_positive_k"] == 0
    assert book["effective_cardinality"] == 0
    assert book["max_active_in_state"] == 0
    occupation = result["occupation"]
    assert occupation["status"] == "unique"
    assert occupation["method"] == "integer_pi_proportional_to_total_weight"
    assert occupation["mean_present_edges"] == {"num": "3", "den": "2", "float": 1.5}
    assert occupation["mean_components"]["num"] == "13"
    assert occupation["mean_components"]["den"] == "8"
    assert all(item["num"] == "1" and item["den"] == "2" for item in occupation["edge_presence"])
    assert result["solver_budget"]["used"] is False
    assert result["imposed_rule_dependency"]["longest_simple_path_edges"] == 0
    assert result["imposed_rule_dependency"]["has_cycle"] is False


def test_weight_hash_is_the_canonical_integer_table():
    weights = np.ones((8, 3), dtype=np.int64)
    blob = json.dumps([[1, 1, 1]] * 8, separators=(",", ":")).encode("ascii")
    assert weight_table_hash(weights) == hashlib.sha256(blob).hexdigest()


def test_prohibit_zeros_only_the_matching_cells():
    weights = compile_weight_table(3, COMPLETE, [_prohibit((0, 1), (0, 2))])
    for state in range(8):
        condition = (state >> 1) & 1
        assert int(weights[state, 0]) == (0 if condition else 1)
        assert int(weights[state, 1]) == 1
        assert int(weights[state, 2]) == 1


def test_duplicate_prohibit_matches_one_copy_and_is_individually_redundant():
    single = [_prohibit((0, 1), (0, 2))]
    duplicate = single + single
    assert weight_table_hash(compile_weight_table(3, COMPLETE, single)) == weight_table_hash(
        compile_weight_table(3, COMPLETE, duplicate)
    )
    book = compile_model(3, COMPLETE, duplicate)["bookkeeping"]
    assert book["declared_cardinality"] == 2
    assert book["effective_cardinality"] == 1
    assert book["removal_sensitive_count"] == 0
    assert book["j_prohibit"] == 2
    assert book["max_positive_k"] == 0


def test_polarity_and_order_are_not_the_same_change():
    present = compile_weight_table(3, COMPLETE, [_multiply((0, 1), (0, 2), polarity="present")])
    absent = compile_weight_table(3, COMPLETE, [_multiply((0, 1), (0, 2), polarity="absent")])
    assert not np.array_equal(present, absent)
    left = [_prohibit((0, 1), (0, 2)), _multiply((1, 2), (0, 1))]
    right = list(reversed(left))
    assert weight_table_hash(compile_weight_table(3, COMPLETE, left)) == weight_table_hash(
        compile_weight_table(3, COMPLETE, right)
    )


def test_form_and_dissolve_depend_on_the_event_bit():
    formed = compile_weight_table(3, COMPLETE, [_prohibit((0, 1), (0, 2), action="form")])
    dissolved = compile_weight_table(3, COMPLETE, [_prohibit((0, 1), (0, 2), action="dissolve")])
    assert not np.array_equal(formed, dissolved)
    state = 0b010
    assert int(formed[state, 0]) == 0
    assert int(formed[state ^ 1, 0]) == 1
    model = compile_model(3, COMPLETE, [_prohibit((0, 1), (0, 2), action="form")])
    assert model["action_bit_independent"] is False
    assert model["empirical_bit_independent"] is False
    assert model["bookkeeping"]["max_prohibit_literals"] == 2
    multiplied = compile_model(3, COMPLETE, [_multiply((0, 1), (0, 2), action="form")])
    assert multiplied["bookkeeping"]["max_positive_k"] == 3
    assert multiplied["bookkeeping"]["j_positive"] == 1


def test_two_multiplies_reinforce_and_do_not_cancel_to_baseline():
    weights = compile_weight_table(
        3,
        COMPLETE,
        [_multiply((0, 1), (0, 2)), _multiply((0, 1), (1, 2))],
    )
    assert int(weights[0b110, 0]) == 16
    assert int(weights[0b010, 0]) == 4
    assert int(weights[0, 0]) == 1
    book = compile_model(3, COMPLETE, [_multiply((0, 1), (0, 2)), _multiply((0, 1), (1, 2))])["bookkeeping"]
    assert book["j_positive"] == 2
    assert book["max_positive_k"] == 2
    assert book["effective_cardinality"] == 2


def test_prohibit_makes_a_multiply_on_the_same_guard_redundant():
    both = [_prohibit((0, 1), (0, 2)), _multiply((0, 1), (0, 2))]
    only = [_prohibit((0, 1), (0, 2))]
    assert np.array_equal(compile_weight_table(3, COMPLETE, both), compile_weight_table(3, COMPLETE, only))
    book = compile_model(3, COMPLETE, both)["bookkeeping"]
    assert book["declared_cardinality"] == 2
    assert book["effective_cardinality"] == 1
    assert book["removal_sensitive_count"] == 1


def test_opposite_polarities_delete_support_rather_than_restore_baseline():
    constraints = [
        _prohibit((0, 1), (0, 2), "present"),
        _prohibit((0, 1), (0, 2), "absent"),
    ]
    weights = compile_weight_table(3, COMPLETE, constraints)
    assert np.all(weights[:, 0] == 0)
    assert np.all(weights[:, 1:] == 1)
    assert not np.array_equal(weights, np.ones_like(weights))
    result = execute_atlas_core(_spec(constraints=constraints))
    assert result["status"] == "complete"
    assert result["classes"]["recurrent_classes"] == 2
    assert result["occupation"]["status"] == "not_unique"
    assert "mean_present_edges" not in result["occupation"]


def test_killing_every_event_makes_one_class_per_state():
    carrier = {"kind": "listed", "edges": [[0, 1], [1, 2]]}
    constraints = [
        _prohibit((0, 1), (1, 2), "present"),
        _prohibit((0, 1), (1, 2), "absent"),
        _prohibit((1, 2), (0, 1), "present"),
        _prohibit((1, 2), (0, 1), "absent"),
    ]
    result = execute_atlas_core(_spec(n=3, carrier=carrier, constraints=constraints))
    assert result["n_states"] == 4
    assert result["positive_transitions"] == 0
    assert result["zero_cells"] == 8
    assert result["classes"]["deadlock_states"] == 4
    assert result["classes"]["recurrent_classes"] == 4
    assert result["occupation"]["status"] == "not_unique"


def test_bit_independent_occupation_matches_the_dense_solve():
    constraints = [_multiply((0, 1), (0, 2))]
    result = execute_atlas_core(_spec(constraints=constraints))
    presence = result["occupation"]["edge_presence"]
    assert presence[0]["num"] == "1" and presence[0]["den"] == "2"
    assert presence[1]["num"] == "2" and presence[1]["den"] == "3"
    assert presence[2]["num"] == "1" and presence[2]["den"] == "2"
    weights = compile_weight_table(3, COMPLETE, constraints)
    dense = stationary_dense(weights)
    mass = np.array(result["occupation"]["unnormalized_total_weight"], dtype=np.float64)
    assert float(np.abs(dense - mass / mass.sum()).sum()) <= 1e-8


def test_a_chain_is_not_a_complete_graph_with_the_same_nodes():
    carrier = {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3]]}
    result = execute_atlas_core(
        _spec(n=4, carrier=carrier, constraints=[_prohibit((0, 1), (1, 2))])
    )
    assert result["n_states"] == 8
    assert result["n_edges"] == 3
    assert result["carrier"]["kind"] == "listed"
    assert result["carrier"]["components"] == 1
    with pytest.raises(ValueError):
        compile_weight_table(4, carrier, [_prohibit((0, 1), (0, 2))])


def test_a_rule_cycle_is_recorded_as_syntax():
    constraints = [
        _prohibit((0, 1), (0, 2)),
        _multiply((1, 2), (0, 1)),
        _prohibit((0, 2), (1, 2), action="form"),
    ]
    dependency = compile_model(3, COMPLETE, constraints)["imposed_rule_dependency"]
    assert dependency["has_cycle"] is True
    assert dependency["longest_simple_path_edges"] == 2
    assert dependency["note"]
    single = compile_model(3, COMPLETE, [_prohibit((0, 1), (0, 2))])["imposed_rule_dependency"]
    assert single["has_cycle"] is False
    assert single["longest_simple_path_edges"] == 1


def test_malformed_constraints_are_rejected():
    with pytest.raises(ValueError):
        compile_weight_table(3, COMPLETE, [_multiply((0, 1), (0, 2), factor=1)])
    with pytest.raises(ValueError):
        compile_weight_table(3, COMPLETE, [_prohibit((0, 1), (0, 1))])
    bad = _prohibit((0, 1), (0, 2))
    bad["factor"] = 4
    with pytest.raises(ValueError):
        compile_weight_table(3, COMPLETE, [bad])
    with pytest.raises(ValueError):
        compile_weight_table(3, {"kind": "listed", "edges": []}, [])


def test_atlas_001_plan_is_frozen_coverage_not_a_result():
    assert main(["plan", "--round", "atlas-001"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-001.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "646aa4fd2e3f45ac1dc4e1dbd11db5aff108da77e4818199cd5432b3c00bea7f"
    assert plan["engine_version"] == "rrc-0.2.0"
    assert plan["engine_version"] != ENGINE_VERSION
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["no_sampling"] is True
    assert len(plan["items"]) == 24
    assert len({item["id"] for item in plan["items"]}) == 24
    assert {item["n"] for item in plan["items"]} == {3, 4}
    by_size = {3: [], 4: []}
    forbidden = {"weight_sha256", "occupation", "expected", "exact", "recurrent_classes"}
    allowed_pairs = {(0, 1), (0, 2), (1, 2)}
    for item in plan["items"]:
        assert item["type"] == "atlas_core"
        assert item["carrier"] == {"kind": "complete"}
        assert item["baseline"] == 1
        assert forbidden.isdisjoint(item)
        by_size[item["n"]].append(item["constraints"])
        for constraint in item["constraints"]:
            assert tuple(constraint["event"]) in allowed_pairs
            assert tuple(constraint["when"]["edge"]) in allowed_pairs
            if "factor" in constraint:
                assert constraint["factor"] == 4
    assert by_size[3] == by_size[4]


def test_atlas_002_plan_is_a_carrier_batch_not_a_replay():
    assert main(["plan", "--round", "atlas-002"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-002.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "937573af07c6d5b40e43802b4f32bac76b32c66eefbca7a68aaab8d15a8bb26e"
    assert plan["engine_version"] == "rrc-0.2.0"
    assert plan["engine_version"] != ENGINE_VERSION
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["coverage"]["complete_carrier_not_repeated"] is True
    assert len(plan["items"]) == 16
    seen = set()
    for item in plan["items"]:
        assert item["n"] == 4
        assert item["type"] == "atlas_core"
        assert item["carrier"]["kind"] == "listed"
        edges = {tuple(pair) for pair in item["carrier"]["edges"]}
        seen.add(frozenset(edges))
        assert "occupation" not in item
        for constraint in item["constraints"]:
            assert tuple(constraint["event"]) in edges
            assert tuple(constraint["when"]["edge"]) in edges
            assert tuple(constraint["event"]) == tuple(item["carrier"]["edges"][0])
            assert tuple(constraint["when"]["edge"]) == tuple(item["carrier"]["edges"][1])
    assert len(seen) == 4


def test_atlas_003_plan_is_a_declared_cardinality_sample():
    assert main(["plan", "--round", "atlas-003"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-003.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "05de332578ff435f6e25eb2550db0a92ca576fdda187c99c8861fb9fdb77fc26"
    assert plan["engine_version"] == "rrc-0.3.0"
    assert plan["engine_version"] == ENGINE_VERSION
    assert plan["grammar_id"] == "opening-prohibit-multiply-v1"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.013
    assert plan["no_sampling"] is True
    assert plan["coverage"]["declared_sample"] is True
    assert plan["coverage"]["not_exhaustive_lists"] is True
    assert plan["coverage"]["six_is_not_a_target"] is True
    assert plan["questions"] == ["ATLAS-Q08"]
    assert "ATLAS-Q07" in plan["questions_not_in_this_round"]
    edges = [(0, 1), (0, 2), (1, 2)]
    factors = [2, 3, 5]
    generated = []
    for index, factor in enumerate(factors):
        event = edges[index]
        condition_a = edges[(index + 1) % 3]
        condition_b = edges[(index + 2) % 3]
        generated.append(
            {
                "action": "either",
                "effect": "prohibit",
                "event": [event[0], event[1]],
                "when": {"edge": [condition_a[0], condition_a[1]], "polarity": "present"},
            }
        )
        generated.append(
            {
                "action": "either",
                "effect": "multiply",
                "event": [event[0], event[1]],
                "factor": factor,
                "when": {"edge": [condition_b[0], condition_b[1]], "polarity": "present"},
            }
        )
    tail = generated + [
        {
            "action": "either",
            "effect": "multiply",
            "event": [0, 1],
            "factor": 4,
            "when": {"edge": [0, 2], "polarity": "absent"},
        },
        {
            "action": "dissolve",
            "effect": "prohibit",
            "event": [0, 2],
            "when": {"edge": [1, 2], "polarity": "present"},
        },
    ]
    by_id = {item["id"]: item for item in plan["items"]}
    assert len(by_id) == 13
    assert [len(item["constraints"]) for item in plan["items"]] == [0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 4, 6, 8]
    assert by_id["A3-12-card6"]["constraints"] == generated
    assert by_id["A3-11-card4"]["constraints"] == generated[:4]
    assert by_id["A3-13-card8"]["constraints"] == tail
    assert by_id["A3-04-mul-present-4"]["role"] == "control"
    assert by_id["A3-04-mul-present-4"]["constraints"][0]["factor"] == 4
    forbidden = {"weight_sha256", "occupation", "expected", "exact", "kernel_sha256"}
    seen_factors = set()
    for item in plan["items"]:
        assert item["type"] == "atlas_core"
        assert item["n"] == 3
        assert item["baseline"] == 1
        assert item["carrier"] == {"kind": "complete"}
        assert forbidden.isdisjoint(item)
        for constraint in item["constraints"]:
            assert "kind" not in constraint.get("when", {})
            assert tuple(constraint["event"]) in set(edges)
            assert tuple(constraint["when"]["edge"]) in set(edges)
            if constraint["effect"] == "multiply":
                seen_factors.add(constraint["factor"])
            else:
                assert "factor" not in constraint
    assert seen_factors == {2, 3, 4, 5}
    both = [
        item
        for item in plan["items"]
        if sum(constraint["effect"] == "prohibit" for constraint in item["constraints"]) >= 2
        and {constraint["when"]["polarity"] for constraint in item["constraints"] if constraint["effect"] == "prohibit"}
        == {"present", "absent"}
    ]
    assert both == []


def test_atlas_004_plan_is_an_incidence_sample_not_a_chase():
    assert main(["plan", "--round", "atlas-004"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-004.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "f6a9680feb02700b5dd8aa9fe024dfe1668d51bdfcbc8aaf5c64607d6c8391fe"
    assert plan["engine_version"] == "rrc-0.3.0"
    assert plan["engine_version"] == ENGINE_VERSION
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.003
    assert plan["no_sampling"] is True
    assert plan["coverage"]["six_is_not_a_target"] is True
    assert plan["coverage"]["not_every_graph"] is True
    assert plan["questions"] == ["ATLAS-Q09", "ATLAS-Q11"]
    assert "ATLAS-Q07" in plan["questions_not_in_this_round"]
    previous = json.loads((ROOT / "plans" / "atlas-002.json").read_text(encoding="utf-8"))
    previous_edges = {
        item["id"].split("-")[1]: item["carrier"]["edges"]
        for item in previous["items"]
        if item["id"].endswith("-base")
    }
    by_id = {item["id"]: item for item in plan["items"]}
    assert len(by_id) == 18
    forbidden = {"weight_sha256", "occupation", "expected", "kernel_sha256"}
    for name, edges in previous_edges.items():
        for suffix, role in (
            ("base", "baseline"),
            ("bit-pro", "control"),
            ("inc-mul", "template"),
            ("inc-pro", "template"),
        ):
            item = by_id[f"A4-{name}-{suffix}"]
            assert item["n"] == 4
            assert item["carrier"]["edges"] == edges
            assert item["role"] == role
            assert forbidden.isdisjoint(item)
        control = by_id[f"A4-{name}-bit-pro"]["constraints"]
        assert len(control) == 1
        assert control[0]["event"] == edges[0]
        assert control[0]["when"] == {"edge": edges[1], "polarity": "present"}
        assert control[0]["effect"] == "prohibit"
        for suffix, effect in (("inc-mul", "multiply"), ("inc-pro", "prohibit")):
            constraints = by_id[f"A4-{name}-{suffix}"]["constraints"]
            assert len(constraints) == len(edges)
            assert [constraint["event"] for constraint in constraints] == edges
            for constraint in constraints:
                assert constraint["effect"] == effect
                assert constraint["when"] == {"kind": "incident_neighbour", "polarity": "present"}
                assert constraint["action"] == "either"
                if effect == "multiply":
                    assert constraint["factor"] == 3
                else:
                    assert "factor" not in constraint
    end = by_id["A4-chain-end-mul"]
    mid = by_id["A4-chain-mid-mul"]
    assert end["role"] == "instrument" and mid["role"] == "instrument"
    assert end["constraints"][0]["event"] == [0, 1]
    assert mid["constraints"][0]["event"] == [1, 2]
    assert "not claimed covariant" in end["label"]
    assert "not claimed covariant" in mid["label"]


def test_historical_round_still_verifies_and_is_not_reexecuted(tmp_path):
    assert main(["verify", "--round", "rrc-001", "--out", str(ROOT / "results" / "rrc-001")]) == 0
    assert main(["verify", "--round", "atlas-001", "--out", str(ROOT / "results" / "atlas-001")]) == 0
    assert main(["verify", "--round", "atlas-002", "--out", str(ROOT / "results" / "atlas-002")]) == 0
    plan = json.loads((ROOT / "plans" / "rrc-001.json").read_text(encoding="utf-8"))
    assert plan["engine_version"] != ENGINE_VERSION

    def explode(_item, _timeout):
        raise AssertionError("historical item was started")

    for round_id in ("rrc-001", "atlas-001", "atlas-002"):
        historical = json.loads((ROOT / "plans" / f"{round_id}.json").read_text(encoding="utf-8"))
        with pytest.raises(SystemExit):
            execute_plan(historical, tmp_path, max_items=1, budget_seconds=5, child=explode)
        assert not (tmp_path / "manifest.json").exists()
