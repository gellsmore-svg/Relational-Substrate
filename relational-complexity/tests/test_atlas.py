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
