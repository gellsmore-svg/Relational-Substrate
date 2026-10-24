"""Incident-count predicate. Compiler checks. Not a scientific round."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rrc import ENGINE_VERSION
from rrc.constraints import compile_model, compile_weight_table, kernel_fingerprint, weight_table_hash
from rrc.items import execute_atlas_core


ROOT = Path(__file__).resolve().parents[1]
CHAIN = {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3]]}
PATH5 = {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]}
BRANCH = {"kind": "listed", "edges": [[0, 1], [0, 2], [0, 3]]}
CYCLE = {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3], [0, 3]]}
ALONE = {"kind": "listed", "edges": [[0, 1], [2, 3]]}


def _count(event, relation, threshold, effect="multiply", factor=3, action="either"):
    payload = {
        "effect": effect,
        "action": action,
        "event": [event[0], event[1]],
        "when": {"kind": "incident_count", "relation": relation, "threshold": threshold},
    }
    if effect == "multiply":
        payload["factor"] = factor
    return payload


def _incident(event, polarity, effect="multiply", factor=3, action="either"):
    payload = {
        "effect": effect,
        "action": action,
        "event": [event[0], event[1]],
        "when": {"kind": "incident_neighbour", "polarity": polarity},
    }
    if effect == "multiply":
        payload["factor"] = factor
    return payload


def _designated(event, condition):
    return {
        "effect": "multiply",
        "factor": 3,
        "action": "either",
        "event": [event[0], event[1]],
        "when": {"edge": [condition[0], condition[1]], "polarity": "present"},
    }


def test_ge_1_matches_present_and_eq_0_matches_absent():
    carriers = (CHAIN, PATH5, BRANCH, CYCLE, ALONE)
    events = {
        id(CHAIN): ((0, 1), (1, 2)),
        id(PATH5): ((0, 1), (1, 2), (2, 3)),
        id(BRANCH): ((0, 1),),
        id(CYCLE): ((0, 1),),
        id(ALONE): ((0, 1),),
    }
    for carrier in carriers:
        for event in events[id(carrier)]:
            for effect, action, factor in (
                ("multiply", "either", 3),
                ("prohibit", "either", None),
                ("multiply", "form", 5),
            ):
                present = compile_weight_table(
                    5,
                    carrier,
                    [_incident(event, "present", effect, factor or 3, action)],
                )
                absent = compile_weight_table(
                    5,
                    carrier,
                    [_incident(event, "absent", effect, factor or 3, action)],
                )
                at_least_one = compile_weight_table(
                    5,
                    carrier,
                    [_count(event, "ge", 1, effect, factor or 3, action)],
                )
                exactly_zero = compile_weight_table(
                    5,
                    carrier,
                    [_count(event, "eq", 0, effect, factor or 3, action)],
                )
                assert present.shape == at_least_one.shape
                assert (present == at_least_one).all()
                assert (absent == exactly_zero).all()


def test_eq_1_and_ge_2_differ_from_ge_1_on_a_two_edge_neighbourhood():
    """Middle edge of the three-edge chain. Neighbours are bits 0 and 2."""
    ge1 = compile_weight_table(4, CHAIN, [_count((1, 2), "ge", 1)])
    eq1 = compile_weight_table(4, CHAIN, [_count((1, 2), "eq", 1)])
    ge2 = compile_weight_table(4, CHAIN, [_count((1, 2), "ge", 2)])
    # 0b101: both neighbours present. 0b001: only the first neighbour.
    assert int(ge1[0b101, 1]) == 3
    assert int(eq1[0b101, 1]) == 1
    assert int(ge2[0b101, 1]) == 3
    assert int(ge1[0b001, 1]) == 3
    assert int(eq1[0b001, 1]) == 3
    assert int(ge2[0b001, 1]) == 1
    assert not (ge1 == eq1).all()
    assert not (ge1 == ge2).all()
    end = compile_weight_table(4, CHAIN, [_count((0, 1), "eq", 1)])
    end_ge = compile_weight_table(4, CHAIN, [_count((0, 1), "ge", 1)])
    assert (end == end_ge).all()


def test_count_expansion_is_not_declared_j():
    model = compile_model(4, CHAIN, [_count((1, 2), "eq", 1)])
    book = model["bookkeeping"]
    assert book["declared_cardinality"] == 1
    assert book["j_positive"] == 1
    assert book["expansion_j_total"] == 2
    assert book["max_expansion_k"] == 3
    assert book["max_positive_k"] == 0
    feature = book["features"][0]
    assert feature["relation"] == "eq"
    assert feature["threshold"] == 1
    assert "polarity" not in feature
    assert "exact minterms" in feature["expansion_note"]
    assert model["grammar_id"] == "incident-count-v1"
    lower = compile_model(4, CHAIN, [_count((1, 2), "ge", 2)])
    assert lower["bookkeeping"]["expansion_j_total"] == 1
    present = compile_model(4, CHAIN, [_count((1, 2), "ge", 1)])
    assert present["bookkeeping"]["expansion_j_total"] == 3
    assert present["bookkeeping"]["max_expansion_k"] == 3
    formed = compile_model(4, CHAIN, [_count((1, 2), "eq", 1, action="form")])
    assert formed["bookkeeping"]["expansion_j_total"] == 2
    assert formed["bookkeeping"]["max_expansion_k"] == 4
    always = compile_model(4, CHAIN, [_count((1, 2), "ge", 0)])
    assert always["bookkeeping"]["expansion_j_total"] == 1
    assert always["bookkeeping"]["max_expansion_k"] == 1
    assert int(always["weights"][0, 1]) == 3
    unreachable = compile_model(4, CHAIN, [_count((1, 2), "eq", 3)])
    assert unreachable["bookkeeping"]["expansion_j_total"] == 0
    assert unreachable["bookkeeping"]["max_expansion_k"] == 0
    assert (unreachable["weights"] == 1).all()
    empty = compile_model(4, ALONE, [_count((0, 1), "ge", 1)])
    assert empty["bookkeeping"]["expansion_j_total"] == 0
    assert (empty["weights"] == 1).all()
    empty_absent = compile_model(4, ALONE, [_count((0, 1), "eq", 0)])
    assert empty_absent["bookkeeping"]["expansion_j_total"] == 1
    assert (empty_absent["weights"][:, 0] == 3).all()


def test_count_grammars_stay_separate_from_the_boolean_incident_grammar():
    counted = compile_model(4, CHAIN, [_count((1, 2), "eq", 1)])
    assert counted["grammar_id"] == "incident-count-v1"
    mixed = compile_model(4, CHAIN, [_count((1, 2), "eq", 1), _designated((0, 1), (1, 2))])
    assert mixed["grammar_id"] == "mixed-current-state-v1"
    both = compile_model(
        4,
        CHAIN,
        [_count((1, 2), "eq", 1), _incident((0, 1), "present")],
    )
    assert both["grammar_id"] == "mixed-current-state-v1"
    boolean = compile_model(4, CHAIN, [_incident((1, 2), "present"), _designated((0, 1), (1, 2))])
    assert boolean["grammar_id"] == "opening-plus-incident-v1"
    opening = compile_model(3, {"kind": "complete"}, [])
    assert opening["grammar_id"] == "opening-prohibit-multiply-v1"
    assert weight_table_hash(opening["weights"]) == (
        "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7"
    )


def test_a_uniform_eq_1_template_is_covariant_under_path_reversal():
    chain = [(0, 1), (1, 2), (2, 3)]
    image = [(2, 3), (1, 2), (0, 1)]

    def template(edges):
        return [_count(edge, "eq", 1) for edge in edges]

    left = compile_weight_table(4, {"kind": "listed", "edges": [list(edge) for edge in chain]}, template(chain))
    right = compile_weight_table(4, {"kind": "listed", "edges": [list(edge) for edge in image]}, template(image))
    assert (left == right).all()
    end = compile_weight_table(4, CHAIN, [_count((0, 1), "eq", 1)])
    middle = compile_weight_table(4, CHAIN, [_count((1, 2), "eq", 1)])
    assert not (end == middle).all()


def test_mutual_count_constraints_are_syntax_cycles_not_cascades():
    mutual = compile_model(
        3,
        {"kind": "listed", "edges": [[0, 1], [1, 2]]},
        [_count((0, 1), "eq", 1), _count((1, 2), "eq", 1)],
    )
    dependency = mutual["imposed_rule_dependency"]
    assert dependency["has_cycle"] is True
    assert "not an observed dynamical cascade" in dependency["note"]


def test_malformed_counts_are_rejected():
    with pytest.raises(ValueError, match="edge or a polarity"):
        compile_weight_table(4, CHAIN, [_count((1, 2), "eq", 1) | {"when": {"kind": "incident_count", "relation": "eq", "threshold": 1, "polarity": "present"}}])
    with pytest.raises(ValueError, match="edge or a polarity"):
        compile_weight_table(
            4,
            CHAIN,
            [
                {
                    "effect": "multiply",
                    "factor": 3,
                    "action": "either",
                    "event": [1, 2],
                    "when": {"kind": "incident_count", "relation": "eq", "threshold": 1, "edge": [0, 1]},
                }
            ],
        )
    with pytest.raises(ValueError, match="integer >= 0"):
        compile_weight_table(4, CHAIN, [_count((1, 2), "eq", -1)])
    with pytest.raises(ValueError, match="integer >= 0"):
        compile_weight_table(4, CHAIN, [_count((1, 2), "ge", True)])
    with pytest.raises(ValueError, match="unknown count relation"):
        compile_weight_table(4, CHAIN, [_count((1, 2), "gt", 1)])
    with pytest.raises(ValueError, match="unknown polarity"):
        compile_weight_table(4, CHAIN, [_incident((1, 2), None)])


def test_a_count_cell_is_still_a_current_state_single_toggle():
    spec = {
        "id": "fixture",
        "round_id": "fixture",
        "type": "atlas_core",
        "n": 4,
        "carrier": CHAIN,
        "constraints": [_count((1, 2), "eq", 1)],
        "baseline": 1,
        "role": "fixture",
        "tolerance": 1e-12,
        "cross_tolerance": 1e-8,
        "max_iter": 10000,
        "dense_max_states": 1024,
    }
    result = execute_atlas_core(spec)
    assert result["status"] == "complete"
    assert result["engine_version"] == ENGINE_VERSION == "rrc-0.4.0"
    assert result["grammar_id"] == "incident-count-v1"
    assert result["compilation"]["new_primitive"] is False
    assert result["compilation"]["history"] is False


def test_historical_tables_stay_bit_identical():
    for round_id in ("atlas-001", "atlas-002", "atlas-003", "atlas-004", "atlas-005"):
        plan = json.loads((ROOT / "plans" / f"{round_id}.json").read_text(encoding="utf-8"))
        for item in plan["items"]:
            weights = compile_weight_table(
                item["n"],
                item["carrier"],
                item["constraints"],
                item.get("baseline", 1),
            )
            stored = json.loads(
                (ROOT / "results" / round_id / "items" / item["id"] / "result.json").read_text(encoding="utf-8")
            )
            assert weight_table_hash(weights) == stored["weight_sha256"]
            if "kernel_sha256" in stored:
                assert kernel_fingerprint(weights) == stored["kernel_sha256"]


def test_registers_keep_the_count_as_a_method():
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    }
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    }
    equivalences = {
        json.loads(line)["equivalence_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "equivalences.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    }
    assert ideas["IDEA-C08"]["status"] == "partial"
    assert ideas["IDEA-I04"]["status"] == "explored"
    assert coverage["COV-INCIDENT-COUNT-SAMPLE"]["status"] == "partial"
    assert "common-neighbour" in ideas["IDEA-I04"]["formulation"]
    assert coverage["COV-COUNTS"]["status"] == "open"
    assert equivalences["EQ-017"]["status"] == "method"
    assert equivalences["EQ-017"]["equivalence_type"] == "weight_table"
    text = (ROOT / "docs" / "atlas-0.4.md").read_text(encoding="utf-8")
    assert "common-neighbour" in text
    assert "not a scientific cell" in text
    assert "rrc-0.4.0" in text
