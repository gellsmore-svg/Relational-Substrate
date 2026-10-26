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


def test_atlas_005_plan_is_a_spread_cardinality_sample():
    assert main(["plan", "--round", "atlas-005"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-005.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "2ab849ad8e43bd643685feea729533fcb3815d6f898a58aa19e236da57142f45"
    assert plan["engine_version"] == "rrc-0.3.0"
    assert plan["grammar_id"] == "opening-prohibit-multiply-v1"
    assert plan["definitions_commit"] == "26bf891ddf064ee4b90097dadf343bb7672720a0"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.857
    assert plan["no_sampling"] is True
    assert plan["coverage"]["declared_sample"] is True
    assert plan["coverage"]["not_exhaustive_lists"] is True
    assert plan["coverage"]["six_is_not_a_target"] is True
    assert plan["coverage"]["cardinality_10"] == "chain only"
    assert plan["questions"] == ["ATLAS-Q01", "ATLAS-Q05"]
    assert "ATLAS-Q07" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q09" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q12" in plan["questions_not_in_this_round"]
    menu = [
        ("prohibit", "either", "present", None),
        ("multiply", "either", "present", 2),
        ("multiply", "either", "absent", 3),
        ("prohibit", "form", "present", None),
        ("multiply", "either", "present", 5),
        ("prohibit", "dissolve", "absent", None),
        ("multiply", "either", "absent", 4),
        ("prohibit", "either", "absent", None),
    ]

    def generated(edges, length):
        count = len(edges)
        built = []
        for index in range(length):
            effect, action, polarity, factor = menu[index % len(menu)]
            event_index = index % count
            condition_index = (event_index + 1 + (index // count)) % count
            if condition_index == event_index:
                condition_index = (condition_index + 1) % count
            event = edges[event_index]
            condition = edges[condition_index]
            constraint = {
                "action": action,
                "effect": effect,
                "event": [event[0], event[1]],
                "when": {"edge": [condition[0], condition[1]], "polarity": polarity},
            }
            if factor is not None:
                constraint["factor"] = factor
            built.append(constraint)
        return built

    carriers = {
        "N3": (3, {"kind": "complete"}, [(0, 1), (0, 2), (1, 2)]),
        "P5": (5, {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]}, [(0, 1), (1, 2), (2, 3), (3, 4)]),
        "C5": (
            5,
            {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]]},
            [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)],
        ),
    }
    expected = {
        "A5-N3-base": ("N3", 0, "baseline"),
        "A5-N3-card5": ("N3", 5, "concentrated"),
        "A5-N3-card12": ("N3", 12, "concentrated"),
        "A5-P5-base": ("P5", 0, "baseline"),
        "A5-P5-card5": ("P5", 5, "spread"),
        "A5-P5-card9": ("P5", 9, "spread"),
        "A5-P5-card10": ("P5", 10, "spread"),
        "A5-P5-card12": ("P5", 12, "spread"),
        "A5-C5-base": ("C5", 0, "baseline"),
        "A5-C5-card5": ("C5", 5, "spread"),
        "A5-C5-card9": ("C5", 9, "spread"),
        "A5-C5-card12": ("C5", 12, "spread"),
    }
    by_id = {item["id"]: item for item in plan["items"]}
    assert list(by_id) == list(expected)
    forbidden = {"weight_sha256", "occupation", "expected", "kernel_sha256", "classes"}
    seen_factors = set()
    for item_id, (carrier_name, length, role) in expected.items():
        item = by_id[item_id]
        n, carrier, edges = carriers[carrier_name]
        assert item["n"] == n
        assert item["carrier"] == carrier
        assert item["role"] == role
        assert item["type"] == "atlas_core"
        assert item["baseline"] == 1
        assert "covariance is not claimed" in item["label"]
        assert forbidden.isdisjoint(item)
        assert item["constraints"] == generated(edges, length)
        guards = {}
        for constraint in item["constraints"]:
            assert constraint["when"].get("kind", "designated_edge") == "designated_edge"
            assert tuple(constraint["event"]) != tuple(constraint["when"]["edge"])
            assert tuple(constraint["event"]) in set(edges)
            assert tuple(constraint["when"]["edge"]) in set(edges)
            if constraint["effect"] == "multiply":
                seen_factors.add(constraint["factor"])
            else:
                assert "factor" not in constraint
                key = (tuple(constraint["event"]), tuple(constraint["when"]["edge"]), constraint["action"])
                guards.setdefault(key, set()).add(constraint["when"]["polarity"])
        assert all(polarities != {"present", "absent"} for polarities in guards.values())
    assert seen_factors == {2, 3, 4, 5}
    assert "incident" not in plan["grammar_id"]


def test_historical_round_still_verifies_and_is_not_reexecuted(tmp_path):
    assert main(["verify", "--round", "rrc-001", "--out", str(ROOT / "results" / "rrc-001")]) == 0
    assert main(["verify", "--round", "atlas-001", "--out", str(ROOT / "results" / "atlas-001")]) == 0
    assert main(["verify", "--round", "atlas-002", "--out", str(ROOT / "results" / "atlas-002")]) == 0
    assert main(["verify", "--round", "atlas-003", "--out", str(ROOT / "results" / "atlas-003")]) == 0
    assert main(["verify", "--round", "atlas-004", "--out", str(ROOT / "results" / "atlas-004")]) == 0
    assert main(["verify", "--round", "atlas-005", "--out", str(ROOT / "results" / "atlas-005")]) == 0
    plan = json.loads((ROOT / "plans" / "rrc-001.json").read_text(encoding="utf-8"))
    assert plan["engine_version"] != ENGINE_VERSION

    def explode(_item, _timeout):
        raise AssertionError("historical item was started")

    for round_id in ("rrc-001", "atlas-001", "atlas-002", "atlas-003", "atlas-004", "atlas-005"):
        historical = json.loads((ROOT / "plans" / f"{round_id}.json").read_text(encoding="utf-8"))
        with pytest.raises(SystemExit):
            execute_plan(historical, tmp_path, max_items=1, budget_seconds=5, child=explode)
        assert not (tmp_path / "manifest.json").exists()


def test_atlas_006_plan_is_a_matched_count_sample():
    assert main(["plan", "--round", "atlas-006"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-006.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "9b551e3e24afb1bdf21c243f52e6a08cb4d287880ce14553d92170cd2ee3cdcb"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "ba8661b95da2863094438626d33b28a36d9072cb"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.007
    assert plan["no_sampling"] is True
    assert plan["coverage"]["declared_sample"] is True
    assert plan["coverage"]["not_every_threshold"] is True
    assert plan["coverage"]["six_is_not_a_target"] is True
    assert plan["coverage"]["ge_1_not_rerun"] is True
    assert plan["questions"] == ["ATLAS-Q09"]
    assert "ATLAS-Q11" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q12" in plan["questions_not_in_this_round"]
    assert "PAT-008" in plan["selection"]
    carriers = {
        "chain": [(0, 1), (1, 2), (2, 3)],
        "branch": [(0, 1), (0, 2), (0, 3)],
        "disc": [(0, 1), (2, 3)],
        "path5": [(0, 1), (1, 2), (2, 3), (3, 4)],
        "cycle5": [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)],
    }
    assert len(plan["items"]) == 15
    seen = {}
    for item in plan["items"]:
        name, grammar = item["id"].removeprefix("A6-").rsplit("-", 1)
        edges = [tuple(edge) for edge in item["carrier"]["edges"]]
        assert edges == carriers[name]
        assert item["n"] == (5 if name in {"path5", "cycle5"} else 4)
        seen.setdefault(name, set()).add(grammar)
        for constraint in item["constraints"]:
            assert constraint["effect"] == "multiply"
            assert constraint["factor"] == 3
            assert constraint["action"] == "either"
        if grammar == "bit":
            assert item["role"] == "instrument"
            assert "not claimed covariant" in item["label"]
            assert len(item["constraints"]) == 1
            constraint = item["constraints"][0]
            assert tuple(constraint["event"]) == edges[0]
            assert tuple(constraint["when"]["edge"]) == edges[1]
            assert constraint["when"]["polarity"] == "present"
            assert "kind" not in constraint["when"]
        else:
            assert item["role"] == "template"
            assert "IDEA-I04" in item["idea_ids"]
            relation, threshold = ("eq", 1) if grammar == "eq1" else ("ge", 2)
            assert [tuple(constraint["event"]) for constraint in item["constraints"]] == edges
            for constraint in item["constraints"]:
                assert constraint["when"] == {
                    "kind": "incident_count",
                    "relation": relation,
                    "threshold": threshold,
                }
    assert seen == {name: {"bit", "eq1", "ge2"} for name in carriers}


def test_atlas_009_plan_uses_two_placement_methods():
    assert main(["plan", "--round", "atlas-009"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-009.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "51b0e0c533c6fa9bada24a3acaa1740c042a50392a0359fe61c15f7b0b4826d8"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "405e804dc1136b6fa54454cdc524e0dbdc2e48cb"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.001
    assert plan["no_sampling"] is True
    assert plan["questions"] == ["ATLAS-Q01"]
    assert "ATLAS-Q03" in plan["questions_not_in_this_round"]
    assert "atlas-005" in plan["selection"]
    assert "EQ-020" in plan["selection"]
    assert len(plan["items"]) == 16
    roles = {}
    for item in plan["items"]:
        assert item["round_id"] == "atlas-009"
        assert item["type"] == "atlas_core"
        assert item["baseline"] == 1
        assert item["n"] == 5
        roles.setdefault(item["role"], []).append(item)
        for constraint in item["constraints"]:
            assert constraint["effect"] == "multiply"
            assert constraint["factor"] == 2
            assert constraint["action"] == "either"
            assert constraint["when"]["polarity"] == "present"
            assert constraint["event"] != constraint["when"]["edge"]
    assert len(roles["baseline"]) == 1 and roles["baseline"][0]["constraints"] == []
    assert len(roles["grammar"]) == 12
    assert {item["id"] for item in roles["instrument"]} == {
        "A9-dep-path",
        "A9-dep-mutual",
        "A9-dep-disjoint",
    }
    assert all(len(item["constraints"]) == 2 for item in roles["instrument"])
    assert all(len(item["constraints"]) == 1 for item in roles["grammar"])


def test_atlas_009_execution_separates_tables_that_share_a_mean():
    assert main(["verify", "--round", "atlas-009", "--out", str(ROOT / "results" / "atlas-009")]) == 0
    items = ROOT / "results" / "atlas-009" / "items"

    def load(name):
        return json.loads((items / name / "result.json").read_text(encoding="utf-8"))

    def edges_of(result):
        return [(item["num"], item["den"]) for item in result["occupation"]["edge_presence"]]

    base = load("A9-base")
    assert base["weight_sha256"] == "5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3"
    assert base["occupation"]["mean_present_edges"]["num"] == "2"
    grammar = [load(f"A9-g-e{event}-c{condition}") for event in range(4) for condition in range(4) if condition != event]
    assert len({item["weight_sha256"] for item in grammar}) == 12
    assert base["weight_sha256"] not in {item["weight_sha256"] for item in grammar}
    for item in grammar:
        assert item["bookkeeping"]["effective_cardinality"] == 1
        assert item["occupation"]["mean_present_edges"]["num"] == "37"
        assert item["occupation"]["mean_present_edges"]["den"] == "18"
        assert item["kernel_sha256"] == item["weight_sha256"]
    assert edges_of(load("A9-g-e0-c1")) == [("1", "2"), ("5", "9"), ("1", "2"), ("1", "2")]
    assert edges_of(load("A9-g-e1-c0")) == [("5", "9"), ("1", "2"), ("1", "2"), ("1", "2")]
    path = load("A9-dep-path")
    mutual = load("A9-dep-mutual")
    disjoint = load("A9-dep-disjoint")
    assert path["weight_sha256"] != mutual["weight_sha256"]
    assert edges_of(path) == edges_of(mutual) == [("11", "20"), ("11", "20"), ("1", "2"), ("1", "2")]
    assert edges_of(disjoint) == [("1", "2"), ("11", "20"), ("1", "2"), ("11", "20")]
    assert path["imposed_rule_dependency"]["has_cycle"] is False
    assert path["imposed_rule_dependency"]["longest_simple_path_edges"] == 2
    assert mutual["imposed_rule_dependency"]["has_cycle"] is True
    assert disjoint["imposed_rule_dependency"]["has_cycle"] is False
    for item in (path, mutual, disjoint):
        assert item["bookkeeping"]["declared_cardinality"] == 2
        assert item["bookkeeping"]["effective_cardinality"] == 2
        assert item["occupation"]["mean_present_edges"]["num"] == "21"
        assert item["occupation"]["mean_present_edges"]["den"] == "10"


def test_atlas_010_plan_compares_three_representations():
    assert main(["plan", "--round", "atlas-010"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-010.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "1d838e1e4a3c038ac08ca03816b67118442ceaf03d9466a072934a0ef5e5285a"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "2ecea775b6ef37083d9e12273fe19337a22fdb01"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
    assert plan["no_sampling"] is True
    assert plan["questions"] == ["ATLAS-Q10"]
    assert "ATLAS-Q11" in plan["questions_not_in_this_round"]
    assert "atlas-008" in plan["selection"]
    assert "EQ-023" in plan["selection"]
    assert len(plan["items"]) == 15
    baseline = []
    constrained = []
    for item in plan["items"]:
        assert item["round_id"] == "atlas-010"
        assert item["type"] == "composition_observation"
        assert item["baseline"] == 1
        assert item["n"] in (3, 4)
        if item["constraints"] == []:
            baseline.append(item)
            assert item["observation"] in {"canonical_line_graph", "carrier_orbit"}
        else:
            constrained.append(item)
            assert len(item["constraints"]) == 1
            constraint = item["constraints"][0]
            assert constraint["factor"] == 3
            assert constraint["effect"] == "multiply"
            assert constraint["action"] == "either"
            assert constraint["when"]["polarity"] == "present"
            assert constraint["event"] == [0, 1]
            assert constraint["when"]["edge"] == [1, 2]
    assert len(baseline) == 6
    assert len(constrained) == 9
    assert {item["observation"] for item in constrained} == {
        "present_line_graph",
        "canonical_line_graph",
        "carrier_orbit",
    }
    assert "baseline present_line_graph" in plan["coverage"]["excluded"]


def test_atlas_010_execution_separates_the_weight_table_from_the_observation():
    assert main(["verify", "--round", "atlas-010", "--out", str(ROOT / "results" / "atlas-010")]) == 0
    items = ROOT / "results" / "atlas-010" / "items"
    baseline = "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7"
    multiply = "7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9"
    four = "5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3"
    cycle_multiply = "c7f6b804ebe70d93942121c4df693dd9ff27cd3c33b03c799eeb1d2aa1860aa7"
    expected = {
        "A10-triangle-base-canon": (True, 4, ("0", "1"), baseline),
        "A10-triangle-base-orbit": (True, 4, ("0", "1"), baseline),
        "A10-triangle-mul-line": (False, 4, ("4", "9"), multiply),
        "A10-triangle-mul-canon": (False, 4, ("4", "9"), multiply),
        "A10-triangle-mul-orbit": (False, 4, ("4", "9"), multiply),
        "A10-chain-base-canon": (False, 5, ("4", "9"), baseline),
        "A10-chain-base-orbit": (True, 6, ("0", "1"), baseline),
        "A10-chain-mul-line": (False, 5, ("28", "45"), multiply),
        "A10-chain-mul-canon": (False, 5, ("28", "45"), multiply),
        "A10-chain-mul-orbit": (False, 6, ("2", "5"), multiply),
        "A10-cycle4-base-canon": (True, 6, ("0", "1"), four),
        "A10-cycle4-base-orbit": (True, 6, ("0", "1"), four),
        "A10-cycle4-mul-line": (False, 8, ("19", "24"), cycle_multiply),
        "A10-cycle4-mul-canon": (False, 6, ("11", "24"), cycle_multiply),
        "A10-cycle4-mul-orbit": (False, 6, ("11", "24"), cycle_multiply),
    }

    def load(name):
        return json.loads((items / name / "result.json").read_text(encoding="utf-8"))

    from fractions import Fraction

    stored = {}
    for name, (exact, labels, defect, digest) in expected.items():
        result = load(name)
        stored[name] = result
        assert result["exact"] is exact
        assert result["n_distinct_labels"] == labels
        assert (result["defect_l1"]["num"], result["defect_l1"]["den"]) == defect
        assert result["weight_sha256"] == digest
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["new_state"] is False
        assert result["injective"] is False
        assert result["further_label"] == "undefined"
        assert result["cover"] is None
        assert result["grammar_id"] == "opening-prohibit-multiply-v1"
        assert result["quotient"]["defined"] is exact
        if exact:
            rows = result["quotient"]["rows"]
            assert len(rows) == result["n_blocks"]
            for row in rows:
                assert sum(Fraction(int(cell["num"]), int(cell["den"])) for cell in row) == 1
        else:
            assert result["quotient"]["rows"] is None

    assert stored["A10-triangle-mul-canon"]["weights"] == stored["A10-chain-mul-canon"]["weights"]
    assert stored["A10-triangle-base-canon"]["weights"] == stored["A10-chain-base-canon"]["weights"]
    assert stored["A10-triangle-base-canon"]["n_distinct_labels"] != stored["A10-chain-base-canon"]["n_distinct_labels"]
    earlier = json.loads((ROOT / "results" / "atlas-006" / "items" / "A6-chain-bit" / "result.json").read_text(encoding="utf-8"))
    assert earlier["weight_sha256"] == multiply
    indexed = json.loads((ROOT / "results" / "atlas-008" / "items" / "A8-cycle4-line" / "result.json").read_text(encoding="utf-8"))
    assert indexed["weight_sha256"] == four
    assert indexed["observation"] == "present_line_graph"
    assert indexed["n_distinct_labels"] == 8
    assert indexed["exact"] is False
    assert (indexed["defect_l1"]["num"], indexed["defect_l1"]["den"]) == ("1", "2")

    from rrc.composition import (
        present_canonical_line_graph_labels,
        present_carrier_orbit_labels,
        present_line_graph_labels,
    )

    def same_partition(left, right):
        return all(
            (left[i] == left[j]) == (right[i] == right[j])
            for i in range(len(left))
            for j in range(len(right))
        )

    seen = {}
    for result in stored.values():
        seen[(result["n"], tuple(tuple(edge) for edge in result["carrier"]["edges"]))] = result["n"]
    assert len(seen) == 3
    for (n, edges_t) in seen:
        edges = [list(edge) for edge in edges_t]
        line = present_line_graph_labels(edges)
        canon = present_canonical_line_graph_labels(edges)
        orbit = present_carrier_orbit_labels(n, edges)
        if n == 3:
            assert same_partition(line, canon) and same_partition(canon, orbit)
        elif edges == [[0, 1], [1, 2], [2, 3]]:
            assert same_partition(line, canon) and not same_partition(canon, orbit)
        else:
            assert edges == [[0, 1], [1, 2], [2, 3], [0, 3]]
            assert same_partition(canon, orbit) and not same_partition(line, canon)


def test_atlas_011_plan_observes_covers_outside_the_path_fixture():
    assert main(["plan", "--round", "atlas-011"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-011.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "9b3309c6d9dc9880be6fb8948ab408aa5636816a77de03d397923f996bd27993"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "e4eb431350325d0b2179a695d185c44d2e1b890a"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
    assert plan["no_sampling"] is True
    assert plan["questions"] == ["ATLAS-Q10"]
    assert "ATLAS-Q12" in plan["questions_not_in_this_round"]
    assert "four-edge path" in plan["selection"]
    assert "EQ-021" in plan["selection"]
    assert "nested cover" in plan["coverage"]["excluded"]
    assert len(plan["items"]) == 17
    bare = []
    omissions = []
    for item in plan["items"]:
        assert item["round_id"] == "atlas-011"
        assert item["type"] == "composition_observation"
        assert item["baseline"] == 1
        assert item["n"] in (3, 4)
        assert isinstance(item["cover"], list) and item["cover"]
        assert [3, 4] not in item["carrier"]["edges"]
        assert "IDEA-L19" in item["idea_ids"]
        if item["constraints"]:
            constraint = item["constraints"][0]
            assert constraint["factor"] == 3
            assert constraint["event"] == [0, 1]
            assert constraint["when"]["edge"] == [1, 2]
        if item["observation"] == "active_intersection":
            bare.append(item)
        if item["id"].startswith("A11-tri-") and item["id"].split("-")[2] in {"far", "cond", "event"}:
            omissions.append(item)
    assert len(bare) == 1
    assert bare[0]["id"] == "A11-tri-single-mul-bare"
    assert bare[0]["constraints"]
    assert {item["id"] for item in omissions} == {
        "A11-tri-far-base-count",
        "A11-tri-far-mul-count",
        "A11-tri-cond-base-count",
        "A11-tri-cond-mul-count",
        "A11-tri-event-base-count",
        "A11-tri-event-mul-count",
    }
    opposite = [item for item in plan["items"] if item["id"].startswith("A11-cyc-opp-")]
    assert len(opposite) == 4
    assert opposite[0]["cover"] == [[[0, 1], [2, 3]], [[1, 2], [0, 3]]]


def test_atlas_011_execution_separates_omission_from_a_collapsed_cover():
    assert main(["verify", "--round", "atlas-011", "--out", str(ROOT / "results" / "atlas-011")]) == 0
    items = ROOT / "results" / "atlas-011" / "items"

    def load(name, directory="atlas-011"):
        return json.loads((ROOT / "results" / directory / "items" / name / "result.json").read_text(encoding="utf-8"))

    def defect(result):
        return (result["defect_l1"]["num"], result["defect_l1"]["den"])

    expected = {
        "A11-tri-single-base-count": (True, 8, ("0", "1"), True),
        "A11-tri-single-mul-count": (True, 8, ("0", "1"), True),
        "A11-tri-single-mul-bare": (False, 4, ("4", "9"), False),
        "A11-tri-over-base-count": (False, 7, ("1", "1"), False),
        "A11-tri-over-mul-count": (False, 7, ("1", "1"), False),
        "A11-tri-over-base-active": (False, 4, ("4", "5"), False),
        "A11-tri-over-mul-active": (False, 4, ("68", "75"), False),
        "A11-tri-far-base-count": (True, 4, ("0", "1"), False),
        "A11-tri-far-mul-count": (True, 4, ("0", "1"), False),
        "A11-tri-cond-base-count": (True, 4, ("0", "1"), False),
        "A11-tri-cond-mul-count": (False, 4, ("4", "15"), False),
        "A11-tri-event-base-count": (True, 4, ("0", "1"), False),
        "A11-tri-event-mul-count": (True, 4, ("0", "1"), False),
        "A11-cyc-opp-base-count": (True, 9, ("0", "1"), False),
        "A11-cyc-opp-mul-count": (False, 9, ("5", "12"), False),
        "A11-cyc-opp-base-active": (False, 4, ("2", "3"), False),
        "A11-cyc-opp-mul-active": (False, 4, ("37", "54"), False),
    }
    from fractions import Fraction

    stored = {}
    for name, (exact, labels, pair, injective) in expected.items():
        result = load(name)
        stored[name] = result
        assert result["exact"] is exact
        assert result["n_distinct_labels"] == labels
        assert defect(result) == pair
        assert result["injective"] is injective
        assert result["new_state"] is False
        assert result["further_label"] == "undefined"
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["quotient"]["defined"] is exact
        if exact:
            for row in result["quotient"]["rows"]:
                assert sum(Fraction(int(cell["num"]), int(cell["den"])) for cell in row) == 1
        else:
            assert result["quotient"]["rows"] is None

    triangle_multiply = load("A10-triangle-mul-canon", "atlas-010")
    cycle_multiply = load("A10-cycle4-mul-canon", "atlas-010")
    assert stored["A11-tri-single-mul-bare"]["weight_sha256"] == triangle_multiply["weight_sha256"]
    assert defect(stored["A11-tri-single-mul-bare"]) == defect(triangle_multiply)
    assert stored["A11-cyc-opp-mul-count"]["weight_sha256"] == cycle_multiply["weight_sha256"]
    assert stored["A11-tri-over-base-count"]["weight_sha256"] == stored["A11-tri-single-base-count"]["weight_sha256"]
    assert stored["A11-tri-over-mul-count"]["weight_sha256"] != stored["A11-tri-over-base-count"]["weight_sha256"]

    from rrc.composition import (
        active_intersection_labels,
        cover_count_labels,
        labelled_active_block_labels,
        present_canonical_line_graph_labels,
        present_edge_count_labels,
    )

    def same_partition(left, right):
        return all(
            (left[i] == left[j]) == (right[i] == right[j])
            for i in range(len(left))
            for j in range(len(right))
        )

    triangle = [[0, 1], [1, 2], [0, 2]]
    cycle = [[0, 1], [1, 2], [2, 3], [0, 3]]
    singletons = [[[0, 1]], [[1, 2]], [[0, 2]]]
    overlap = [[[0, 1], [1, 2]], [[1, 2], [0, 2]]]
    far = [[[0, 1]], [[1, 2]]]
    condition = [[[0, 1]], [[0, 2]]]
    event = [[[1, 2]], [[0, 2]]]
    opposite = [[[0, 1], [2, 3]], [[1, 2], [0, 3]]]
    adjacent = [[[0, 1], [1, 2]], [[2, 3], [0, 3]]]
    bare = active_intersection_labels(triangle, singletons)
    assert same_partition(bare, present_edge_count_labels(triangle))
    assert same_partition(bare, present_canonical_line_graph_labels(triangle))
    assert not same_partition(cover_count_labels(triangle, singletons), bare)
    assert not same_partition(cover_count_labels(triangle, overlap), labelled_active_block_labels(triangle, overlap))
    assert not same_partition(labelled_active_block_labels(triangle, overlap), active_intersection_labels(triangle, overlap))
    assert not same_partition(cover_count_labels(triangle, far), cover_count_labels(triangle, condition))
    assert not same_partition(cover_count_labels(triangle, far), cover_count_labels(triangle, event))
    assert not same_partition(cover_count_labels(cycle, opposite), labelled_active_block_labels(cycle, opposite))
    assert not same_partition(cover_count_labels(cycle, opposite), cover_count_labels(cycle, adjacent))


def test_atlas_012_plan_pairs_polarity_with_event_arrangement():
    assert main(["plan", "--round", "atlas-012"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-012.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "1dffac3ff30ff7d6a37fbe0df4c63e90b1988cf454a9d8a7a4ba746515de5185"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "040bfabddc848e3986dec4fd2000b932991eade7"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.001
    assert plan["questions"] == ["ATLAS-Q03"]
    assert "ATLAS-Q01" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q04" in plan["questions_not_in_this_round"]
    assert "atlas-009" in plan["selection"]
    assert "atlas-009 factor-2 path grid" in plan["coverage"]["excluded"]
    assert len(plan["items"]) == 7
    roles = {}
    for item in plan["items"]:
        assert item["round_id"] == "atlas-012"
        assert item["type"] == "atlas_core"
        assert item["n"] == 4
        assert item["carrier"]["edges"] == [[0, 1], [1, 2], [2, 3]]
        assert item["baseline"] == 1
        roles.setdefault(item["role"], []).append(item)
        for constraint in item["constraints"]:
            assert constraint["effect"] == "multiply"
            assert constraint["factor"] == 3
            assert constraint["action"] == "either"
    assert roles["baseline"][0]["constraints"] == []
    present, absent = roles["polarity"]
    assert present["constraints"][0]["when"]["polarity"] == "present"
    assert absent["constraints"][0]["when"]["polarity"] == "absent"
    assert present["constraints"][0]["event"] == absent["constraints"][0]["event"] == [0, 1]
    assert present["constraints"][0]["when"]["edge"] == absent["constraints"][0]["when"]["edge"] == [1, 2]
    one = roles["one_event"][0]["constraints"]
    two = roles["two_event"][0]["constraints"]
    assert len(one) == len(two) == 2
    assert one[0]["event"] == one[1]["event"]
    assert two[0]["event"] != two[1]["event"]
    assert {constraint["when"]["polarity"] for constraint in one + two} == {"present"}


def test_atlas_012_execution_separates_arrangement_from_a_bit_relabeling():
    assert main(["verify", "--round", "atlas-012", "--out", str(ROOT / "results" / "atlas-012")]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-012.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "1dffac3ff30ff7d6a37fbe0df4c63e90b1988cf454a9d8a7a4ba746515de5185"
    items = ROOT / "results" / "atlas-012" / "items"

    def load(name, directory="atlas-012"):
        return json.loads((ROOT / "results" / directory / "items" / name / "result.json").read_text(encoding="utf-8"))

    names = [
        "A12-base",
        "A12-pol-present",
        "A12-pol-absent",
        "A12-single-far",
        "A12-single-other",
        "A12-one-event",
        "A12-two-event",
    ]
    stored = {name: load(name) for name in names}
    hashes = {
        "A12-base": "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7",
        "A12-pol-present": "7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9",
        "A12-pol-absent": "a30d2af41e1b65601390615151522d627502825abba5d36195739e051a798cff",
        "A12-single-far": "35818e425b302f38df5d28715a61ec5e21b1a765ab3ceee5f81ee55c40156e82",
        "A12-single-other": "f4b5f62c8045ae02a0e81f3fde6202933c166f3c92862e0348b0f3382b3945ad",
        "A12-one-event": "4689196251660b2458b053cf65ecf08d19ca17a2182ac10f8f040495d6ff2328",
        "A12-two-event": "f1e515bd6d9dba119ac4ea8833c34d628796fb62f07736ea6951c787b88bacc5",
    }
    assert len(set(hashes.values())) == 7
    from fractions import Fraction

    for name, result in stored.items():
        assert result["weight_sha256"] == hashes[name]
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["engine_version"] == plan["engine_version"]
        assert result["plan_hash"] == digest(plan)
        assert result["grammar_id"] == "opening-prohibit-multiply-v1"
        assert result["compilation"]["new_primitive"] is False
        assert result["zero_cells"] == 0
        assert result["classes"]["recurrent_classes"] == 1
        assert result["occupation"]["method"] == "integer_pi_proportional_to_total_weight"
        edges = Fraction(int(result["occupation"]["mean_present_edges"]["num"]), int(result["occupation"]["mean_present_edges"]["den"]))
        components = Fraction(int(result["occupation"]["mean_components"]["num"]), int(result["occupation"]["mean_components"]["den"]))
        assert components == 4 - edges
    assert stored["A12-base"]["bookkeeping"]["effective_cardinality"] == 0
    assert stored["A12-pol-present"]["bookkeeping"]["effective_cardinality"] == 1
    assert stored["A12-pol-absent"]["bookkeeping"]["effective_cardinality"] == 1
    assert stored["A12-one-event"]["bookkeeping"]["effective_cardinality"] == 2
    assert stored["A12-two-event"]["bookkeeping"]["effective_cardinality"] == 2
    assert stored["A12-one-event"]["bookkeeping"]["kernel_effective_cardinality"] == 2
    assert stored["A12-two-event"]["bookkeeping"]["kernel_effective_cardinality"] == 2
    chain = load("A10-chain-mul-canon", "atlas-010")
    assert stored["A12-pol-present"]["weight_sha256"] == chain["weight_sha256"]
    singles = ["A12-pol-present", "A12-pol-absent", "A12-single-far", "A12-single-other"]
    for length2 in ("A12-one-event", "A12-two-event"):
        assert stored[length2]["weight_sha256"] not in {stored[name]["weight_sha256"] for name in singles}
        assert stored[length2]["weight_sha256"] != stored["A12-base"]["weight_sha256"]
    assert stored["A12-one-event"]["weight_sha256"] != stored["A12-two-event"]["weight_sha256"]

    def marginals(name):
        return tuple(
            Fraction(int(cell["num"]), int(cell["den"]))
            for cell in stored[name]["occupation"]["edge_presence"]
        )

    assert marginals("A12-pol-present") == (Fraction(1, 2), Fraction(5, 8), Fraction(1, 2))
    assert marginals("A12-pol-absent") == (Fraction(1, 2), Fraction(3, 8), Fraction(1, 2))
    assert marginals("A12-single-far") == (Fraction(1, 2), Fraction(1, 2), Fraction(5, 8))
    assert marginals("A12-single-other") == marginals("A12-pol-present")
    assert marginals("A12-one-event") == (Fraction(1, 2), Fraction(2, 3), Fraction(2, 3))
    assert marginals("A12-two-event") == (Fraction(1, 2), Fraction(7, 10), Fraction(1, 2))

    def rev_state(state):
        return ((state & 1) << 2) | (state & 2) | ((state >> 2) & 1)

    def translated(table, mask):
        return [table[state ^ mask] for state in range(8)]

    def reversed_table(table):
        out = [[None] * 3 for _ in range(8)]
        for state in range(8):
            for edge, image in ((0, 2), (1, 1), (2, 0)):
                out[rev_state(state)][image] = table[state][edge]
        return out

    def product(left, right):
        return [[left[state][edge] * right[state][edge] for edge in range(3)] for state in range(8)]

    present = stored["A12-pol-present"]["weights"]
    absent = stored["A12-pol-absent"]["weights"]
    far = stored["A12-single-far"]["weights"]
    other = stored["A12-single-other"]["weights"]
    one = stored["A12-one-event"]["weights"]
    two = stored["A12-two-event"]["weights"]
    assert absent == translated(present, 2)
    assert other == reversed_table(present)
    assert far != reversed_table(present)
    assert one == product(present, far)
    assert two == product(present, other)

    import itertools

    def image(table, perm, mask):
        out = [[None] * 3 for _ in range(8)]
        for state in range(8):
            sigma = mask
            for edge in range(3):
                if (state >> edge) & 1:
                    sigma ^= 1 << perm[edge]
            for edge in range(3):
                out[sigma][perm[edge]] = table[state][edge]
        return out

    perms = list(itertools.permutations(range(3)))
    assert not any(image(one, perm, mask) == two for perm in perms for mask in range(8))
    for single in (present, absent, far, other, stored["A12-base"]["weights"]):
        assert not any(image(one, perm, mask) == single for perm in perms for mask in range(8))
        assert not any(image(two, perm, mask) == single for perm in perms for mask in range(8))
    assert items.is_dir()


def test_atlas_015_execution_separates_potential_overlap_from_realised_overlap():
    assert main(["verify", "--round", "atlas-015", "--out", str(ROOT / "results" / "atlas-015")]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-015.json").read_text(encoding="utf-8"))
    from fractions import Fraction

    from rrc.store import digest

    assert digest(plan) == "75f36e40fc647bb953c64d7d91e65820db40e8bd459bfea6bf0c07b7392e1b0b"
    assert plan["engine_version"] == "rrc-0.4.0"
    items = ROOT / "results" / "atlas-015" / "items"

    def load(name):
        return json.loads((items / name / "result.json").read_text(encoding="utf-8"))

    def fraction(payload):
        return Fraction(int(payload["num"]), int(payload["den"]))

    names = [item["id"] for item in plan["items"]]
    stored = {name: load(name) for name in names}
    structure = "e6f7386ece69cd8888eca2be7cbc621dc46a80b61c6ddebb9f0a18abfceea8cc"
    hashes = {
        "base": "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7",
        "pro-shared": "fe1f4d4e5e5fcac700a7efc7ec32acb0dfcc1c21f5bb401f6b27738b527b2d7c",
        "pro-own": "d65a9800e618e62c49e0199f0d5cac3ca201448067180dbbbe4139a641958007",
        "mul-shared": "fa10bdcc43d20cf87f97823c9a8b9ec9aefc370aabebd884ec98038b6123e915",
        "mul-ends": "92189689622ad7ebd818c01b8ab01236265258c1cacdf43adf9de5c3f124311c",
    }
    counts = {"active": 3, "realised": 4, "labelled": 5, "count": 2}
    for name, result in stored.items():
        law, observation = name.removeprefix("A15-").rsplit("-", 1)
        assert result["engine_version"] == plan["engine_version"]
        assert result["plan_hash"] == digest(plan)
        assert result["weight_sha256"] == hashes[law]
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["structure_sha256"] == structure
        assert result["new_state"] is False
        assert result["further_label"] == "undefined"
        assert result["n_distinct_labels"] == counts[observation]
        assert result["grammar_id"] == "opening-prohibit-multiply-v1"
    assert stored["A15-base-count"]["exact"] is True
    assert fraction(stored["A15-base-count"]["defect_l1"]) == 0
    assert stored["A15-pro-own-count"]["exact"] is True
    assert fraction(stored["A15-pro-own-count"]["defect_l1"]) == 0
    assert fraction(stored["A15-pro-shared-count"]["defect_l1"]) == Fraction(1, 3)
    assert stored["A15-pro-shared-count"]["witness"]["states"] == [0, 1]
    assert fraction(stored["A15-mul-shared-count"]["defect_l1"]) == Fraction(4, 15)
    assert fraction(stored["A15-mul-ends-count"]["defect_l1"]) == Fraction(2, 15)
    assert stored["A15-mul-shared-realised"]["witness"]["states"] == [2, 7]
    assert stored["A15-mul-shared-labelled"]["witness"]["states"] == [2, 6]
    assert fraction(stored["A15-mul-shared-realised"]["defect_l1"]) == Fraction(9, 10)
    assert fraction(stored["A15-mul-shared-labelled"]["defect_l1"]) == Fraction(9, 10)

    def zero_cells(name):
        weights = stored[name]["weights"]
        return [
            (row_index, column)
            for row_index, row in enumerate(weights)
            for column, weight in enumerate(row)
            if weight == 0
        ]

    assert zero_cells("A15-pro-shared-count") == [(1, 1), (3, 1), (5, 1), (7, 1)]
    assert zero_cells("A15-pro-own-count") == [(2, 0), (3, 0), (6, 0), (7, 0)]
    assert zero_cells("A15-mul-shared-count") == []
    assert zero_cells("A15-mul-ends-count") == []
    assert {weight for row in stored["A15-base-count"]["weights"] for weight in row} == {1}
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q14"]["status"] == "open"


def test_atlas_015_plan_is_the_chain_overlap_sample():
    assert main(["plan", "--round", "atlas-015"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-015.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "75f36e40fc647bb953c64d7d91e65820db40e8bd459bfea6bf0c07b7392e1b0b"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "081d52aa6c5ac3b1a228b833a2777973aa631aea"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
    assert plan["questions"] == ["ATLAS-Q14"]
    assert "ATLAS-Q13" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q02" in plan["questions_not_in_this_round"]
    assert len(plan["items"]) == 20
    chain = [[0, 1], [1, 2], [2, 3]]
    cover = [[[0, 1], [1, 2]], [[1, 2], [2, 3]]]
    shared = {
        "action": "either",
        "effect": "prohibit",
        "event": [1, 2],
        "when": {"edge": [0, 1], "polarity": "present"},
    }
    own = {
        "action": "either",
        "effect": "prohibit",
        "event": [0, 1],
        "when": {"edge": [1, 2], "polarity": "present"},
    }
    mul_shared = {
        "action": "either",
        "effect": "multiply",
        "factor": 3,
        "event": [1, 2],
        "when": {"edge": [2, 3], "polarity": "present"},
    }
    mul_ends = {
        "action": "either",
        "effect": "multiply",
        "factor": 3,
        "event": [2, 3],
        "when": {"edge": [0, 1], "polarity": "present"},
    }
    laws = {
        "base": [],
        "pro-shared": [shared],
        "pro-own": [own],
        "mul-shared": [mul_shared],
        "mul-ends": [mul_ends],
    }
    maps = {
        "active": "active_intersection",
        "realised": "realised_intersection",
        "labelled": "labelled_realised_blocks",
        "count": "realised_overlap_count",
    }
    expected = [
        (f"A15-{law}-{map_name}", constraints, observation)
        for law, constraints in laws.items()
        for map_name, observation in maps.items()
    ]
    assert [(item["id"], item["constraints"], item["observation"]) for item in plan["items"]] == expected
    for item in plan["items"]:
        assert item["type"] == "composition_observation"
        assert item["n"] == 4
        assert item["carrier"]["edges"] == chain
        assert item["cover"] == cover
        assert item["baseline"] == 1
        assert "parity" not in item["observation"]
        for constraint in item["constraints"]:
            assert constraint["action"] == "either"
            assert constraint["when"]["polarity"] == "present"
            if constraint["effect"] == "prohibit":
                assert "factor" not in constraint
            else:
                assert constraint["factor"] == 3


def test_atlas_014_plan_is_the_four_cycle_successive_sample():
    assert main(["plan", "--round", "atlas-014"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-014.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "c8f63dc8054478c71467db630aee633b4f39f884b5f2331cc76ec180a5715790"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "d82d23ada194a4d5266bdaf29880b47e483eee26"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.004
    assert plan["questions"] == ["ATLAS-Q13"]
    assert "ATLAS-Q14" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q02" in plan["questions_not_in_this_round"]
    assert len(plan["items"]) == 8
    cycle = [[0, 1], [1, 2], [2, 3], [0, 3]]
    prohibit = {
        "action": "either",
        "effect": "prohibit",
        "event": [0, 1],
        "when": {"edge": [2, 3], "polarity": "present"},
    }
    expected = [
        ("A14-base-orbit-count", [], ["carrier_orbit", "present_edge_count"]),
        ("A14-pro-orbit-count", [prohibit], ["carrier_orbit", "present_edge_count"]),
        ("A14-pro-line-count", [prohibit], ["present_line_graph", "present_edge_count"]),
        ("A14-pro-count-degree", [prohibit], ["present_edge_count", "present_degree_sequence"]),
        ("A14-pro-degree-count", [prohibit], ["present_degree_sequence", "present_edge_count"]),
        ("A14-pro-orbit-constant", [prohibit], ["carrier_orbit", "constant_label"]),
        ("A14-pro-injective-degree", [prohibit], ["labelled_line_graph", "present_degree_sequence"]),
        ("A14-pro-overlap-count", [prohibit], ["realised_overlap_count", "present_edge_count"]),
    ]
    for item, (item_id, constraints, observations) in zip(plan["items"], expected):
        assert item["id"] == item_id
        assert item["type"] == "successive_observation"
        assert item["n"] == 4
        assert item["carrier"]["edges"] == cycle
        assert item["constraints"] == constraints
        assert item["observations"] == observations
        assert len(item["observations"]) == 2
        assert "parity" not in "".join(item["observations"])
    overlap = plan["items"][-1]
    assert overlap["cover"] == [[[0, 1], [1, 2]], [[1, 2], [2, 3]]]
    assert "cover" not in plan["items"][0]


def test_atlas_014_execution_keeps_undefined_stages_empty():
    assert main(["verify", "--round", "atlas-014", "--out", str(ROOT / "results" / "atlas-014")]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-014.json").read_text(encoding="utf-8"))
    from fractions import Fraction

    from rrc.store import digest

    assert digest(plan) == "c8f63dc8054478c71467db630aee633b4f39f884b5f2331cc76ec180a5715790"
    assert plan["engine_version"] == "rrc-0.4.0"
    items = ROOT / "results" / "atlas-014" / "items"
    names = [item["id"] for item in plan["items"]]

    def load(name):
        return json.loads((items / name / "result.json").read_text(encoding="utf-8"))

    def fraction(payload):
        return Fraction(int(payload["num"]), int(payload["den"]))

    stored = {name: load(name) for name in names}
    structure = "5747f684d10b1fc3f48c38b0a9b4176e5c1aa137469d113d0caa3126c12f7a51"
    baseline_hash = "5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3"
    prohibit_hash = "b6ab427edcb7b603d898e81a3286efa03802664ccdd6b33152b8716d0ee35d79"
    for name, result in stored.items():
        assert result["engine_version"] == plan["engine_version"]
        assert result["plan_hash"] == digest(plan)
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["structure_sha256"] == structure
        assert result["grammar_id"] == "opening-prohibit-multiply-v1"
        assert result["new_state"] is False
        assert result["conditional_exactness"] == "not_computed"
        assert result["history_dependent"] == "not_computed"
        assert result["n_states"] == 16
    base = stored["A14-base-orbit-count"]
    assert base["weight_sha256"] == baseline_hash
    assert base["agreement"] == "exact"
    assert base["kernels_agree"] is True
    assert base["exact_prefix"] == 2
    assert [stage["exact"] for stage in base["stages"]] == [True, True]
    assert [fraction(stage["defect_l1"]) for stage in base["stages"]] == [0, 0]
    assert base["label_counts"] == [6, 5]
    assert base["stages"][1]["quotient_rows"] == base["direct"][1]["quotient_rows"]
    assert base["stages"][1]["quotient_rows"] is not None
    prohibit = [name for name in names if name != "A14-base-orbit-count"]
    zeros = [(4, 0), (5, 0), (6, 0), (7, 0), (12, 0), (13, 0), (14, 0), (15, 0)]
    for name in prohibit:
        result = stored[name]
        assert result["weight_sha256"] == prohibit_hash
        assert result["agreement"] == "undefined"
        assert result["kernels_agree"] is None
        found = [
            (row_index, column)
            for row_index, row in enumerate(result["weights"])
            for column, weight in enumerate(row)
            if weight == 0
        ]
        assert found == zeros
        assert {weight for row in result["weights"] for weight in row if weight} == {1}
    assert stored["A14-pro-injective-degree"]["exact_prefix"] == 1
    assert {stored[name]["exact_prefix"] for name in prohibit if name != "A14-pro-injective-degree"} == {0}
    untyped = stored["A14-pro-count-degree"]
    assert untyped["stages"][1]["factors_through_previous"] is False
    assert untyped["stages"][1]["defect_l1"] is None
    assert untyped["stages"][1]["quotient_rows"] is None
    assert untyped["stages"][1]["exact"] is None
    degree_count = stored["A14-pro-degree-count"]
    assert degree_count["stages"][1]["factors_through_previous"] is True
    assert degree_count["stages"][1]["defect_l1"] is None
    assert degree_count["stages"][1]["quotient_rows"] is None
    assert fraction(degree_count["direct"][0]["defect_l1"]) == Fraction(11, 24)
    assert fraction(degree_count["direct"][1]["defect_l1"]) == Fraction(11, 24)
    line = stored["A14-pro-line-count"]
    assert fraction(line["direct"][0]["defect_l1"]) == Fraction(5, 8)
    assert line["direct"][0]["n_distinct_labels"] == 8
    assert line["stages"][1]["quotient_rows"] is None
    constant = stored["A14-pro-orbit-constant"]
    assert constant["direct"][1]["exact"] is True
    assert fraction(constant["direct"][1]["defect_l1"]) == 0
    assert constant["direct"][1]["n_distinct_labels"] == 1
    assert constant["stages"][1]["quotient_rows"] is None
    assert constant["stages"][1]["defect_l1"] is None
    injective = stored["A14-pro-injective-degree"]
    assert injective["stages"][0]["exact"] is True
    assert injective["stages"][0]["n_distinct_labels"] == 16
    assert injective["stages"][1]["exact"] is False
    assert fraction(injective["stages"][1]["defect_l1"]) == Fraction(11, 24)
    assert injective["stages"][1]["quotient_rows"] is None
    overlap = stored["A14-pro-overlap-count"]
    assert fraction(overlap["direct"][0]["defect_l1"]) == Fraction(1, 12)
    assert overlap["direct"][0]["n_distinct_labels"] == 2
    assert overlap["stages"][1]["factors_through_previous"] is False
    assert overlap["stages"][1]["defect_l1"] is None
    assert overlap["stages"][1]["quotient_rows"] is None
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q13"]["status"] == "open"


def test_atlas_013_plan_is_the_star_prohibit_slice():
    assert main(["plan", "--round", "atlas-013"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-013.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "5f39cf2cc5f5d8bd7975422eb0cd039544d606ef47e3fde38c07654bd79dc010"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "9068c99f0c79a43a61a2ef1f14b5e696104901fc"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
    assert plan["questions"] == ["ATLAS-Q02"]
    assert "ATLAS-Q04" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q09" in plan["questions_not_in_this_round"]
    assert len(plan["items"]) == 5
    star = [[0, 1], [0, 2], [0, 3]]
    for item in plan["items"]:
        assert item["round_id"] == "atlas-013"
        assert item["type"] == "atlas_core"
        assert item["carrier"]["edges"] == star
        assert item["baseline"] == 1
        for constraint in item["constraints"]:
            assert constraint["effect"] == "prohibit"
            assert constraint["action"] == "either"
            assert "factor" not in constraint
            assert constraint["when"]["kind"] == "incident_count"
    assert plan["items"][0]["constraints"] == []
    assert [item["constraints"][0]["when"]["relation"] for item in plan["items"][1:]] == [
        "eq",
        "eq",
        "ge",
        "eq",
    ]
    assert [item["constraints"][0]["when"]["threshold"] for item in plan["items"][1:]] == [1, 2, 2, 2]
    assert len(plan["items"][4]["constraints"]) == 1
    assert len(plan["items"][1]["constraints"]) == 3


def test_atlas_013_execution_separates_support_from_a_rescaled_rate():
    assert main(["verify", "--round", "atlas-013", "--out", str(ROOT / "results" / "atlas-013")]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-013.json").read_text(encoding="utf-8"))
    from fractions import Fraction

    from rrc.model import strongly_connected_components, support_successors
    from rrc.store import digest

    assert digest(plan) == "5f39cf2cc5f5d8bd7975422eb0cd039544d606ef47e3fde38c07654bd79dc010"
    items = ROOT / "results" / "atlas-013" / "items"

    def load(name):
        return json.loads((items / name / "result.json").read_text(encoding="utf-8"))

    stored = {name: load(name) for name in ("A13-base", "A13-eq1", "A13-eq2", "A13-ge2", "A13-one")}
    hashes = {
        "A13-base": "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7",
        "A13-eq1": "1f82f333586889368e6492f1d1e050aa9bfe371d399299433a7b6b7080a45695",
        "A13-eq2": "3811f60d68e33785a86d79fd47e1030351152dd33251b252e9cf164537db574c",
        "A13-ge2": "3811f60d68e33785a86d79fd47e1030351152dd33251b252e9cf164537db574c",
        "A13-one": "559a60132ec515f31a30395d46d560d4672a104e447331beaeaea53dfd6e4f6f",
    }
    for name, result in stored.items():
        assert result["weight_sha256"] == hashes[name]
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["engine_version"] == plan["engine_version"]
        assert result["plan_hash"] == digest(plan)
        assert result["compilation"]["new_primitive"] is False
        assert result["empirical_bit_independent"] is True
        assert result["structure_sha256"] == "6c959c90bc45976a55a7d874b0e0e4a6c4c31cf14f231e39417136e5ddf1e1d1"
        assert result["bookkeeping"]["max_positive_k"] == 0
    assert stored["A13-base"]["grammar_id"] == "opening-prohibit-multiply-v1"
    assert stored["A13-eq1"]["grammar_id"] == "incident-count-v1"
    assert stored["A13-eq2"]["weights"] == stored["A13-ge2"]["weights"]
    assert stored["A13-eq1"]["occupation"]["status"] == "not_unique"
    assert stored["A13-eq2"]["occupation"]["status"] == "not_unique"
    assert "mean_present_edges" not in stored["A13-eq1"]["occupation"]
    assert "mean_present_edges" not in stored["A13-eq2"]["occupation"]
    assert stored["A13-eq2"]["classes"]["deadlock_states"] == 1
    assert stored["A13-eq2"]["classes"]["recurrent_classes"] == 2
    assert stored["A13-eq1"]["classes"]["deadlock_states"] == 0
    assert stored["A13-eq1"]["zero_cells"] == 12
    assert stored["A13-one"]["classes"]["recurrent_classes"] == 1
    assert stored["A13-one"]["bookkeeping"]["declared_cardinality"] == 1
    assert stored["A13-eq2"]["bookkeeping"]["effective_cardinality"] == 3

    def fraction(payload):
        return Fraction(int(payload["num"]), int(payload["den"]))

    base = stored["A13-base"]["occupation"]
    one = stored["A13-one"]["occupation"]
    assert fraction(base["mean_present_edges"]) == Fraction(3, 2)
    assert fraction(base["mean_components"]) == Fraction(5, 2)
    assert fraction(one["mean_present_edges"]) == Fraction(31, 22)
    assert fraction(one["mean_components"]) == Fraction(57, 22)
    assert [fraction(cell) for cell in one["edge_presence"]] == [
        Fraction(1, 2),
        Fraction(5, 11),
        Fraction(5, 11),
    ]
    assert fraction(base["mean_present_edges"]) + fraction(base["mean_components"]) == 4
    assert fraction(one["mean_present_edges"]) + fraction(one["mean_components"]) == 4

    def recurrent_masks(name):
        weights = np.array(stored[name]["weights"], dtype=np.int64)
        successors, _deadlocks = support_successors(weights)
        found = []
        for component in strongly_connected_components(successors):
            members = set(component)
            leaves = any(nxt not in members for state in component for nxt in successors[state])
            if not leaves:
                found.append(set(component))
        return found

    assert recurrent_masks("A13-eq1") == [{0, 1, 2, 4}, {3, 5, 6, 7}] or recurrent_masks("A13-eq1") == [
        {3, 5, 6, 7},
        {0, 1, 2, 4},
    ]
    assert {7} in recurrent_masks("A13-eq2")
    assert recurrent_masks("A13-eq2") == recurrent_masks("A13-ge2")
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q02"]["status"] == "open"
    equivalences = {
        json.loads(line)["equivalence_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "equivalences.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert equivalences["EQ-028"]["status"] == "cell"
    assert "neighbourhood" in equivalences["EQ-028"]["not_claimed"]
    wider = [[0, 1], [0, 2], [0, 3], [0, 4]]

    def uniform(relation):
        return [
            {
                "effect": "prohibit",
                "action": "either",
                "event": edge,
                "when": {"kind": "incident_count", "relation": relation, "threshold": 2},
            }
            for edge in wider
        ]

    carrier = {"kind": "listed", "edges": wider}
    assert not np.array_equal(
        compile_weight_table(5, carrier, uniform("eq")),
        compile_weight_table(5, carrier, uniform("ge")),
    )


def test_atlas_016_plan_is_the_incident_and_disjoint_sample():
    assert main(["plan", "--round", "atlas-016"]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-016.json").read_text(encoding="utf-8"))
    from rrc.store import digest

    assert digest(plan) == "d933e17efe85ea998c3a81229e4bd3436d02a7cd42ccdb7d6d73d20e40688c1d"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "72ee4e50d463aba4c3f6cd3e8e5a06aa944daa52"
    assert plan["grammar_id"] == "opening-prohibit-multiply-v1"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
    assert plan["questions"] == ["ATLAS-Q02"]
    assert "ATLAS-Q14" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q15" in plan["questions_not_in_this_round"]
    assert plan["coverage"]["six_is_not_a_target"] is True
    assert len(plan["items"]) == 8
    edges = [[0, 1], [1, 2], [3, 4]]
    pro_incident = {
        "action": "either",
        "effect": "prohibit",
        "event": [1, 2],
        "when": {"edge": [0, 1], "polarity": "present"},
    }
    mul_incident = {
        "action": "either",
        "effect": "multiply",
        "factor": 3,
        "event": [1, 2],
        "when": {"edge": [0, 1], "polarity": "present"},
    }
    pro_across = {
        "action": "either",
        "effect": "prohibit",
        "event": [0, 1],
        "when": {"edge": [3, 4], "polarity": "present"},
    }
    mul_across = {
        "action": "either",
        "effect": "multiply",
        "factor": 3,
        "event": [0, 1],
        "when": {"edge": [3, 4], "polarity": "present"},
    }
    pro_disjoint = {
        "action": "either",
        "effect": "prohibit",
        "event": [3, 4],
        "when": {"edge": [0, 1], "polarity": "present"},
    }
    mul_disjoint = {
        "action": "either",
        "effect": "multiply",
        "factor": 3,
        "event": [3, 4],
        "when": {"edge": [0, 1], "polarity": "present"},
    }
    expected = [
        ("A16-base", []),
        ("A16-pro-incident", [pro_incident]),
        ("A16-mul-incident", [mul_incident]),
        ("A16-pro-across", [pro_across]),
        ("A16-mul-across", [mul_across]),
        ("A16-pro-disjoint", [pro_disjoint]),
        ("A16-mul-disjoint", [mul_disjoint]),
        ("A16-mixed", [pro_incident, mul_disjoint]),
    ]
    assert [(item["id"], item["constraints"]) for item in plan["items"]] == expected
    for item in plan["items"]:
        assert item["type"] == "atlas_core"
        assert item["n"] == 5
        assert item["carrier"]["edges"] == edges
        assert item["baseline"] == 1
        assert "incident_count" not in json.dumps(item["constraints"])
        for constraint in item["constraints"]:
            assert constraint["action"] == "either"
            assert constraint["when"]["polarity"] == "present"
            if constraint["effect"] == "prohibit":
                assert "factor" not in constraint
            else:
                assert constraint["factor"] == 3
    incident = plan["items"][1]["constraints"][0]
    assert incident["event"] == [1, 2]
    assert incident["when"]["edge"] == [0, 1]


def test_atlas_016_execution_separates_support_from_rate():
    assert main(["verify", "--round", "atlas-016", "--out", str(ROOT / "results" / "atlas-016")]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-016.json").read_text(encoding="utf-8"))
    from fractions import Fraction

    from rrc.composition import carrier_automorphisms
    from rrc.store import digest

    assert digest(plan) == "d933e17efe85ea998c3a81229e4bd3436d02a7cd42ccdb7d6d73d20e40688c1d"
    assert plan["engine_version"] == "rrc-0.4.0"
    items = ROOT / "results" / "atlas-016" / "items"
    names = [item["id"] for item in plan["items"]]
    stored = {
        name: json.loads((items / name / "result.json").read_text(encoding="utf-8"))
        for name in names
    }
    structure = "0963ca7e652f311e3382a80a52a2c8efe545700c1c793db7444f5140bb162fbd"
    hashes = {
        "A16-base": "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7",
        "A16-pro-incident": "fe1f4d4e5e5fcac700a7efc7ec32acb0dfcc1c21f5bb401f6b27738b527b2d7c",
        "A16-mul-incident": "badcbc1cecba75dbdb76f74ea9cc1368c0dc49c55eb52346b9575889e02dd84b",
        "A16-pro-across": "866005248da1269bc32a3c62e3d391cae91e841b57fa180d634f832f11e67fc6",
        "A16-mul-across": "35818e425b302f38df5d28715a61ec5e21b1a765ab3ceee5f81ee55c40156e82",
        "A16-pro-disjoint": "b54fee3ce4ed5f19f4843249d82b4217eb004fba882f25d8894b2b5d08fe7eb3",
        "A16-mul-disjoint": "92189689622ad7ebd818c01b8ab01236265258c1cacdf43adf9de5c3f124311c",
        "A16-mixed": "f83fd2d4e2aeb937143f26dceae8a06363691ad470e2570e5d16dc6c4b64219b",
    }
    assert len(set(hashes.values())) == 8

    def fraction(payload):
        return Fraction(int(payload["num"]), int(payload["den"]))

    fractions = {
        "A16-base": (Fraction(3, 2), Fraction(7, 2), [Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)]),
        "A16-pro-incident": (Fraction(7, 5), Fraction(18, 5), [Fraction(2, 5), Fraction(1, 2), Fraction(1, 2)]),
        "A16-mul-incident": (Fraction(13, 8), Fraction(27, 8), [Fraction(5, 8), Fraction(1, 2), Fraction(1, 2)]),
        "A16-pro-across": (Fraction(7, 5), Fraction(18, 5), [Fraction(1, 2), Fraction(1, 2), Fraction(2, 5)]),
        "A16-mul-across": (Fraction(13, 8), Fraction(27, 8), [Fraction(1, 2), Fraction(1, 2), Fraction(5, 8)]),
        "A16-pro-disjoint": (Fraction(7, 5), Fraction(18, 5), [Fraction(2, 5), Fraction(1, 2), Fraction(1, 2)]),
        "A16-mul-disjoint": (Fraction(13, 8), Fraction(27, 8), [Fraction(5, 8), Fraction(1, 2), Fraction(1, 2)]),
        "A16-mixed": (Fraction(11, 7), Fraction(24, 7), [Fraction(4, 7), Fraction(1, 2), Fraction(1, 2)]),
    }
    values = {
        "A16-base": {1},
        "A16-pro-incident": {0, 1},
        "A16-mul-incident": {1, 3},
        "A16-pro-across": {0, 1},
        "A16-mul-across": {1, 3},
        "A16-pro-disjoint": {0, 1},
        "A16-mul-disjoint": {1, 3},
        "A16-mixed": {0, 1, 3},
    }
    positive = {
        "A16-base": True,
        "A16-pro-incident": False,
        "A16-mul-incident": True,
        "A16-pro-across": False,
        "A16-mul-across": True,
        "A16-pro-disjoint": False,
        "A16-mul-disjoint": True,
        "A16-mixed": False,
    }
    effective = {
        "A16-base": 0,
        "A16-pro-incident": 1,
        "A16-mul-incident": 1,
        "A16-pro-across": 1,
        "A16-mul-across": 1,
        "A16-pro-disjoint": 1,
        "A16-mul-disjoint": 1,
        "A16-mixed": 2,
    }
    for name, result in stored.items():
        occupation = result["occupation"]
        assert result["engine_version"] == plan["engine_version"]
        assert result["plan_hash"] == digest(plan)
        assert result["weight_sha256"] == hashes[name]
        assert result["kernel_sha256"] == result["weight_sha256"]
        assert result["structure_sha256"] == structure
        assert result["grammar_id"] == "opening-prohibit-multiply-v1"
        assert result["compilation"]["new_primitive"] is False
        assert result["compilation"]["all_weights_positive"] is positive[name]
        assert result["bookkeeping"]["effective_cardinality"] == effective[name]
        assert result["classes"]["recurrent_classes"] == 1
        assert result["classes"]["deadlock_states"] == 0
        assert result["carrier"]["components"] == 2
        assert occupation["status"] == "unique"
        assert occupation["method"] == "integer_pi_proportional_to_total_weight"
        edges, components, marginals = fractions[name]
        assert fraction(occupation["mean_present_edges"]) == edges
        assert fraction(occupation["mean_components"]) == components
        assert [fraction(cell) for cell in occupation["edge_presence"]] == marginals
        assert edges + components == 5
        assert {weight for row in result["weights"] for weight in row} == values[name]

    def zero_cells(name):
        weights = stored[name]["weights"]
        return [
            (row_index, column)
            for row_index, row in enumerate(weights)
            for column, weight in enumerate(row)
            if weight == 0
        ]

    assert zero_cells("A16-base") == []
    assert zero_cells("A16-pro-incident") == [(1, 1), (3, 1), (5, 1), (7, 1)]
    assert zero_cells("A16-mul-incident") == []
    assert zero_cells("A16-pro-across") == [(4, 0), (5, 0), (6, 0), (7, 0)]
    assert zero_cells("A16-mul-across") == []
    assert zero_cells("A16-pro-disjoint") == [(1, 2), (3, 2), (5, 2), (7, 2)]
    assert zero_cells("A16-mul-disjoint") == []
    assert zero_cells("A16-mixed") == [(1, 1), (3, 1), (5, 1), (7, 1)]

    def permute(table, perm):
        out = [[None] * 3 for _ in range(8)]
        for state in range(8):
            sigma = 0
            for edge in range(3):
                if (state >> edge) & 1:
                    sigma |= 1 << perm[edge]
            for edge in range(3):
                out[sigma][perm[edge]] = table[state][edge]
        return out

    swap = (0, 2, 1)
    assert permute(stored["A16-pro-incident"]["weights"], swap) == stored["A16-pro-disjoint"]["weights"]
    assert permute(stored["A16-mul-incident"]["weights"], swap) == stored["A16-mul-disjoint"]["weights"]
    product = [
        [left * right for left, right in zip(pro_row, mul_row)]
        for pro_row, mul_row in zip(
            stored["A16-pro-incident"]["weights"],
            stored["A16-mul-disjoint"]["weights"],
        )
    ]
    assert product == stored["A16-mixed"]["weights"]

    here = [(0, 1), (1, 2), (3, 4)]
    automorphisms = carrier_automorphisms(5, here)
    assert automorphisms == [
        (0, 1, 2, 3, 4),
        (0, 1, 2, 4, 3),
        (2, 1, 0, 3, 4),
        (2, 1, 0, 4, 3),
    ]

    def image(perm, edge):
        left, right = perm[edge[0]], perm[edge[1]]
        return (left, right) if left < right else (right, left)

    for perm in automorphisms:
        assert image(perm, here[1]) != here[2]

    def forest_components(mask):
        parent = list(range(5))

        def find(vertex):
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        present = 0
        for bit, edge in enumerate(here):
            if (mask >> bit) & 1:
                present += 1
                left, right = find(edge[0]), find(edge[1])
                if left != right:
                    parent[left] = right
        return present + len({find(vertex) for vertex in range(5)})

    assert [forest_components(mask) for mask in range(8)] == [5] * 8

    chain_edges = [[0, 1], [1, 2], [2, 3]]
    here_edges = [[0, 1], [1, 2], [3, 4]]
    by_id = {item["id"]: item for item in plan["items"]}

    def chain_rule(event, effect, condition, factor=None):
        row = {
            "action": "either",
            "effect": effect,
            "event": event,
            "when": {"edge": condition, "polarity": "present"},
        }
        if factor is not None:
            row["factor"] = factor
        return [row]

    comparisons = [
        ("A16-pro-incident", chain_rule([1, 2], "prohibit", [0, 1])),
        ("A16-mul-disjoint", chain_rule([2, 3], "multiply", [0, 1], 3)),
        ("A16-mul-across", chain_rule([0, 1], "multiply", [2, 3], 3)),
    ]
    for item_id, chain_constraints in comparisons:
        left = compile_weight_table(4, {"kind": "listed", "edges": chain_edges}, chain_constraints)
        right = compile_weight_table(
            5,
            {"kind": "listed", "edges": here_edges},
            by_id[item_id]["constraints"],
        )
        assert np.array_equal(left, right)
        assert chain_edges != here_edges
        assert right.tolist() == stored[item_id]["weights"]

    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q02"]["status"] == "open"
    equivalences = {
        json.loads(line)["equivalence_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "equivalences.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert equivalences["EQ-032"]["status"] == "method"
    assert equivalences["EQ-032"]["equivalence_type"] == "weight_table"
    assert "carrier" in equivalences["EQ-032"]["not_claimed"]


def test_atlas_017_plan_is_the_declared_event_sample():
    assert main(["plan", "--round", "atlas-017"]) == 0
    plan_text = (ROOT / "plans" / "atlas-017.json").read_text(encoding="utf-8")
    plan = json.loads(plan_text)
    from rrc.store import digest

    assert digest(plan) == "61b502a25bf1689d9e7f7c6bac461fffed24983cde804c7ec6ba785c8b4ce143"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "e189bd2eff912fc49917b65b959896fbfd3b6b5c"
    assert plan["grammar_id"] == "one-declared-event-v1"
    assert plan["method_id"] == "event-kernel-0.1.0"
    assert plan["grammar"]["clock"] == "one_declared_event"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
    assert plan["questions"] == ["ATLAS-Q06"]
    assert "ATLAS-Q02" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q15" in plan["questions_not_in_this_round"]
    assert plan["coverage"]["six_is_not_a_target"] is True
    assert plan["coverage"]["cells"] == 6
    assert len(plan["items"]) == 6
    for phrase in ("1/2", "1/3", "2/3", "13/8"):
        assert phrase not in plan_text
    preflight = (ROOT / "docs" / "atlas-017-preflight.md").read_text(encoding="utf-8")
    assert "scientific` is false" in preflight
    assert "Observables were not retained" in preflight
    assert "ATLAS-Q06" in preflight
    assert "event-kernel-0.1.0" in preflight
    joint = []
    for state, toggle_target, joint_target in ((0, 1, 3), (1, 0, 2), (2, 3, 1), (3, 2, 0)):
        joint.append(
            {
                "name": f"bit0-{state}",
                "kind": "toggle",
                "source": state,
                "target": toggle_target,
                "weight": 1,
            }
        )
        joint.append(
            {
                "name": f"both-{state}",
                "kind": "joint",
                "source": state,
                "target": joint_target,
                "weight": 1,
            }
        )
    expected = {
        "A17-g0": {
            "family": "single_toggle",
            "role": "control",
            "n_states": 4,
            "bit_width": 2,
            "catalogue": "single_toggle",
            "rows": [[1, 1], [1, 1], [1, 1], [1, 1]],
        },
        "A17-g1": {
            "family": "joint_and_toggle",
            "role": "comparison",
            "n_states": 4,
            "bit_width": 2,
            "events": joint,
        },
        "A17-identified": {
            "family": "identified_interface",
            "role": "control",
            "n_states": 2,
            "bit_width": 1,
            "events": [
                {"name": "up", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
                {"name": "down", "kind": "toggle", "source": 1, "target": 0, "weight": 1},
            ],
        },
        "A17-coupled": {
            "family": "coupled_copies",
            "role": "comparison",
            "n_states": 4,
            "bit_width": 2,
            "events": [
                {"name": "together-up", "kind": "joint", "source": 0, "target": 3, "weight": 1},
                {"name": "together-down", "kind": "joint", "source": 3, "target": 0, "weight": 1},
            ],
        },
        "A17-halt": {
            "family": "empty_catalogue",
            "role": "control",
            "n_states": 1,
            "events": [],
        },
        "A17-noop": {
            "family": "noop_event",
            "role": "comparison",
            "n_states": 1,
            "events": [
                {"name": "stay", "kind": "noop", "source": 0, "target": 0, "weight": 1}
            ],
        },
    }
    assert [item["id"] for item in plan["items"]] == list(expected)
    for item in plan["items"]:
        assert item["type"] == "event_kernel"
        assert item["round_id"] == "atlas-017"
        assert "constraints" not in item
        assert "carrier" not in item
        assert "idea_ids" not in item
        spec = expected[item["id"]]
        for key, value in spec.items():
            assert item[key] == value
        if "events" in spec:
            assert "catalogue" not in item
            assert "rows" not in item
        else:
            assert "events" not in item
        if item["id"] in {"A17-halt", "A17-noop"}:
            assert "bit_width" not in item
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q06"]["status"] == "open"
    assert questions["ATLAS-Q15"]["status"] == "open"
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L23"]["status"] == "open"
    assert ideas["IDEA-L23"]["status"] != "selected"


def test_atlas_017_execution_separates_support_from_the_single_toggle_law():
    assert main(["verify", "--round", "atlas-017", "--out", str(ROOT / "results" / "atlas-017")]) == 0
    plan = json.loads((ROOT / "plans" / "atlas-017.json").read_text(encoding="utf-8"))
    from fractions import Fraction

    from rrc.state_families import single_toggle_successors
    from rrc.store import digest

    assert digest(plan) == "61b502a25bf1689d9e7f7c6bac461fffed24983cde804c7ec6ba785c8b4ce143"
    assert plan["engine_version"] == "rrc-0.4.0"
    items = ROOT / "results" / "atlas-017" / "items"
    stored = {
        item["id"]: json.loads((items / item["id"] / "result.json").read_text(encoding="utf-8"))
        for item in plan["items"]
    }

    def fraction_row(result, state):
        return [
            Fraction(int(cell["num"]), int(cell["den"]))
            for cell in result["probabilities"][state]
        ]

    def positive_steps(result):
        steps = []
        for source, row in enumerate(result["probabilities"]):
            for target, cell in enumerate(row):
                if Fraction(int(cell["num"]), int(cell["den"])) > 0 and source != target:
                    steps.append((source, target))
        return steps

    for result in stored.values():
        assert result["engine_version"] == plan["engine_version"]
        assert result["plan_hash"] == digest(plan)
        assert result["method"] == "event-kernel-0.1.0"
        assert result["clock"] == "one_declared_event"
        assert result["new_primitive"] is False
        assert result["halt_self_loop_is_event"] is False
        assert "occupation" not in result
        assert "weight_sha256" not in result
        assert "kernel_method" not in result
        for row in result["probabilities"]:
            assert sum(Fraction(int(cell["num"]), int(cell["den"])) for cell in row) == 1

    g0 = stored["A17-g0"]
    g1 = stored["A17-g1"]
    identified = stored["A17-identified"]
    coupled = stored["A17-coupled"]
    halt = stored["A17-halt"]
    noop = stored["A17-noop"]
    assert fraction_row(g0, 0) == [Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(0)]
    assert fraction_row(g1, 0) == [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)]
    assert fraction_row(identified, 0) == [Fraction(0), Fraction(1)]
    assert fraction_row(identified, 1) == [Fraction(1), Fraction(0)]
    assert fraction_row(coupled, 0) == [Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
    assert fraction_row(coupled, 3) == [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
    assert coupled["completions"][1] == coupled["completions"][2] == "halt_self_loop"
    assert coupled["enabled_event_counts"][1] == coupled["enabled_event_counts"][2] == 0
    assert halt["probabilities"] == noop["probabilities"]
    assert halt["completions"] == ["halt_self_loop"]
    assert noop["completions"] == ["noop_event"]
    assert halt["enabled_event_counts"] == [0]
    assert noop["enabled_event_counts"] == [1]
    assert all((source ^ target).bit_count() == 1 for source, target in positive_steps(g0))
    assert all((source ^ target).bit_count() == 1 for source, target in positive_steps(identified))
    g1_by_source = {}
    for source, target in positive_steps(g1):
        g1_by_source.setdefault(source, set()).add((source ^ target).bit_count())
    assert g1_by_source == {0: {1, 2}, 1: {1, 2}, 2: {1, 2}, 3: {1, 2}}
    assert [(source ^ target).bit_count() for source, target in positive_steps(coupled)] == [2, 2]
    assert 3 not in single_toggle_successors(2, 0)
    assert 3 in single_toggle_successors(2, 1)
    image = {0: 0, 1: 3}
    assert fraction_row(identified, 0)[1] == fraction_row(coupled, image[0])[image[1]]
    assert fraction_row(identified, 1)[0] == fraction_row(coupled, image[1])[image[0]]
    assert fraction_row(g0, 0)[3] == 0
    assert 1 not in {0, 3} and 2 not in {0, 3}
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q06"]["status"] == "open"
    assert questions["ATLAS-Q15"]["status"] == "open"
    findings = [
        json.loads(line)
        for line in (ROOT / "coherence" / "findings.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    finding = next(row for row in findings if row["finding_id"] == "RRC-ATLAS-018")
    assert finding["finding_id"] == "RRC-ATLAS-018"
    assert finding["created_commit"] == "070fc79"
    assert finding["status"] == "active"
    assert "ATLAS-Q06 stays open" in finding["statement"]
    relations = [
        json.loads(line)
        for line in (ROOT / "coherence" / "relations.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    relation = next(row for row in relations if row["relation_id"] == "RRC-R054")
    assert relation["relation_id"] == "RRC-R054"
    assert relation["from_finding"] == "RRC-ATLAS-018"
    assert relation["to_finding"] == "RRC-M01-NO-NEW-AXIS"
    assert "does not close ATLAS-Q06" in relation["rationale"]
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert coverage["COV-HIGHER-ORDER-STATE"]["status"] == "open"
    assert "not a frozen round" in coverage["COV-HIGHER-ORDER-STATE"]["method"]
    assert "atlas-017" in coverage["COV-HIGHER-ORDER-STATE"]["notes"]
    assert "state-event-families.md" in coverage["COV-HIGHER-ORDER-STATE"]["notes"]
