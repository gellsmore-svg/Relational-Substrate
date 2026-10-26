"""v0.4 clocks, N=4 layout, and the authored/agent-input distinction.

Generation 3 numeric observables are compared here. They are not redefined.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.census import (
    build_slotted,
    independent_hypergraph_orbits,
    n4_baseline_certificate,
)
from rs_constraint_lab.cli import main
from rs_constraint_lab.constraints import cross_order_class, parse_expression
from rs_constraint_lab.execution import build_plan
from rs_constraint_lab.grammar import build_grammar, count_canonical_simple_sets, is_canonical_ids
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.higher_order import clear_index_cache, emergent_memory_tv
from rs_constraint_lab.memory_clocks import (
    float_stationary,
    full_event_clock_memory_tv,
    full_event_pair_memory_tv,
    pair_event_epoch_memory_tv,
    pair_event_epoch_memory_tv_float,
)
from rs_constraint_lab.spec import validate_spec
from rs_constraint_lab.state import relation_slots, slot_permutation_maps
from rs_constraint_lab.version import ENGINE_VERSION, SEMANTIC_VERSION, hypergraph_version_for_n
from rs_constraint_lab.weights import alphabet_factors

LAB = Path(__file__).resolve().parents[1]
WEIGHTS = ["prohibit", "strong_suppress", "weak_suppress", "weak_favour", "strong_favour"]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _n3(text: str):
    constraint = parse_expression(text, 3, order=3)
    slots = tuple(relation_slots(3, 3))
    kernel = build_slotted(3, (constraint,), alphabet_factors("W4"), slots, Fraction(1))
    return constraint, kernel


def test_prompt_bytes_distinguish_authored_slot_from_agent_input():
    prompts = LAB / "provenance" / "prompts"
    captured = prompts / "003-v0.3-higher-order-relations.md"
    agent = prompts / "003-v0.3-agent-input.md"
    prompt4 = prompts / "004-v0.4-n4-higher-order-reconfiguration.md"
    assert captured.stat().st_size == 25995
    assert _sha(captured) == "9ac0de2c5d4cdd33749fec03a232f2d35fe5f6dbead9b0f572cafce4e23cbccb"
    assert agent.stat().st_size == 25996
    assert _sha(agent) == "451f462d1d6675023d836939b9647422cfb098926bc62bec15da371edc33e92e"
    assert agent.read_bytes()[1:] == captured.read_bytes()
    assert prompt4.stat().st_size == 32011
    assert _sha(prompt4) == "f261527e522cc780f0937097b7de7706f7953f8bf69c59837442bbb7e1cf76ef"
    rows = [
        json.loads(line)
        for line in (LAB / "provenance" / "ledger.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    repair = next(row for row in rows if row["record_type"] == "prompt_representation" and row["prompt_id"] == "003")
    assert repair["authored_prompt_status"] == "pending_verbatim_import"
    assert repair["authored_prompt_bytes_reported"] == 27580
    assert repair["relationship"] == "normalised"
    assert repair["agent_input_prompt_sha256"] != repair["captured_execution_prompt_sha256"]
    stored = next(row for row in rows if row["record_type"] == "prompt" and row["prompt_id"] == "004")
    assert stored["relationship"] == "unknown"
    assert stored["agent_input_prompt_sha256"] == stored["prompt_sha256"]
    assert stored["authored_prompt_sha256"] is None
    review = LAB / "provenance" / "reviews" / "003-chatgpt-review-v0.3.md"
    text = review.read_text(encoding="utf-8")
    assert "e04e0d4dcf979197b62d8d73fd747a0a2084c2b6" in text
    assert "37131636102" in text
    assert "not a line-by-line audit" in text


def test_full_event_clock_matches_generation3_and_epoch_can_differ():
    _, bare = _n3("form(0-1-2) => strong_favour")
    full = full_event_clock_memory_tv(bare)
    epoch, defect = pair_event_epoch_memory_tv(bare)
    assert full == emergent_memory_tv(bare) == Fraction(81, 1288)
    assert epoch == 0 and defect == 0
    _, coupled = _n3("form(0-1) | present(0-1-2) => strong_favour")
    assert full_event_clock_memory_tv(coupled) == emergent_memory_tv(coupled) == Fraction(27, 616)
    epoch_coupled, defect_coupled = pair_event_epoch_memory_tv(coupled)
    assert epoch_coupled == Fraction(34, 1485) and defect_coupled == 0
    pi, residual, _arithmetic, _periods = float_stationary(coupled)
    assert residual == 0.0
    assert abs(full_event_pair_memory_tv(coupled, pi) - float(Fraction(27, 616))) < 1e-12
    floated, float_defect = pair_event_epoch_memory_tv_float(coupled, pi)
    assert float_defect == 0.0
    assert abs(floated - float(Fraction(34, 1485))) < 1e-12


def test_n4_slots_are_independent_and_s4_moves_the_triads():
    slots = relation_slots(4, 3)
    assert slots == [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
        (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3),
    ]
    assert len(slots) == 10
    kernel = build_slotted(4, (), alphabet_factors("W4"), tuple(slots), Fraction(1))
    assert kernel.n_states == 1024
    triad_only = 1 << 6
    assert any(target == 0 for target, _prob in kernel.successors[triad_only])
    assert any(target == triad_only | 1 for target, _prob in kernel.successors[triad_only])
    maps = slot_permutation_maps(4, slots)
    assert len(maps) == 24
    swap = maps[1]
    assert swap[6:] != (6, 7, 8, 9)
    image = {slots[source]: slots[dest] for source, dest in enumerate(swap)}
    assert image[(0, 1, 2)] in {(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)}
    orbits = independent_hypergraph_orbits(4)
    assert orbits == {"labelled_states": 1024, "orbit_count": 90, "slots": 10}


def test_isomorphism_separates_the_two_edge_path_from_the_matching():
    table = pair_classes()
    assert len(table.representatives) == 11
    assert table.path_name == "e2-deg2110-tri0-comp2"
    assert table.matching_name == "e2-deg1111-tri0-comp2"
    assert table.path_mask != table.matching_mask
    path = table._mask_of_edges((0, 1), (1, 2))
    matching = table._mask_of_edges((0, 1), (2, 3))
    assert table.edge_count_of[path] == table.edge_count_of[matching] == 2
    assert table.same_cardinality_nonisomorphic(path, matching)
    assert table.by_mask[table.path_mask]["component_count"] == 2
    assert table.by_mask[table.matching_mask]["degree_multiset"] == (1, 1, 1, 1)


def test_n4_k2_singleton_grammar_and_canonicalisation():
    grammar = build_grammar(4, 2, WEIGHTS, a_max=4, predicates=("pair", "triad"), order=3)
    stats = grammar.stats
    assert stats["structural_normal_forms"] == 380
    assert stats["labelled_constraints"] == 1900
    assert stats["structural_by_class"] == {"P->P": 132, "P->T": 96, "T->P": 96, "T->T": 56, "mixed": 0}
    assert count_canonical_simple_sets(grammar, 1) == 160
    coupled = parse_expression("form(0-1) | present(0-1-2) => strong_favour", 4, order=3)
    backward = parse_expression("form(0-1-2) | present(0-1) => strong_favour", 4, order=3)
    assert cross_order_class(coupled, 6) == "T->P"
    assert cross_order_class(backward, 6) == "P->T"
    identified = grammar.labelled.index(coupled)
    assert is_canonical_ids((identified,), grammar.image) or any(
        is_canonical_ids((grammar.image[row][identified],), grammar.image)
        for row in range(len(grammar.image))
    )
    images = {grammar.image[row][identified] for row in range(len(grammar.image))}
    canonical = min(images)
    assert is_canonical_ids((canonical,), grammar.image)
    assert len(images) > 1


def test_n4_baseline_is_uniform_and_memoryless():
    slots = tuple(relation_slots(4, 3))
    kernel = build_slotted(4, (), alphabet_factors("W4"), slots, Fraction(1))
    certificate = n4_baseline_certificate(kernel)
    assert certificate["states"] == 1024
    assert certificate["slots"] == 10
    assert certificate["toggles_per_state_min"] == certificate["toggles_per_state_max"] == 10
    assert certificate["symmetric_regular"] is True
    assert certificate["periods"] == [2]
    assert certificate["stationary_arithmetic"] == "float64"
    assert certificate["stationary_residual"] < 1e-8
    assert certificate["tv_from_uniform_numerical"] < 1e-8
    assert abs(certificate["expected_pair_density"] - 0.5) < 1e-8
    assert abs(certificate["expected_triad_occupancy"] - 2.0) < 1e-8
    assert certificate["pair_triad_joint_gap"] < 1e-8
    assert certificate["pair_jump_dependence"] is False
    assert certificate["full_event_clock_status"] == "zero"
    assert certificate["pair_event_epoch_status"] == "zero"
    assert abs(certificate["cmi_triad_to_next_pair"]) < 1e-8
    assert certificate["hypergraph_orbit_count"] == 90
    assert certificate["pairwise_class_count"] == 11
    slots3 = tuple(relation_slots(3, 3))
    bare = build_slotted(
        3,
        (parse_expression("form(0-1-2) => strong_favour", 3, order=3),),
        alphabet_factors("W4"),
        slots3,
        Fraction(1),
    )
    pi, _residual, _arithmetic, _periods = float_stationary(bare)
    # N=3 stays on the exact clock. The float image is only a cross-check.
    assert emergent_memory_tv(bare) == Fraction(81, 1288)
    assert abs(full_event_pair_memory_tv(bare, pi) - float(Fraction(81, 1288))) < 1e-12


def test_n4_triad_only_rule_keeps_event_clock_memory_and_loses_epoch_memory():
    slots = tuple(relation_slots(4, 3))
    kernel = build_slotted(
        4,
        (parse_expression("form(0-1-2) => strong_favour", 4, order=3),),
        alphabet_factors("W4"),
        slots,
        Fraction(1),
    )
    pi, residual, arithmetic, _periods = float_stationary(kernel)
    assert arithmetic == "float64"
    assert residual < 1e-8
    full = full_event_pair_memory_tv(kernel, pi)
    epoch, defect = pair_event_epoch_memory_tv_float(kernel, pi)
    assert full > 1e-4
    assert epoch is not None and defect is not None and defect < 1e-8
    assert epoch < 1e-8


def test_versions_stay_split_by_n_and_simplicial_stays_refused():
    assert hypergraph_version_for_n(3) == ("0.3.0", "0.3.0")
    assert hypergraph_version_for_n(4) == ("0.4.0", "0.4.0")
    assert ENGINE_VERSION == SEMANTIC_VERSION == "0.2.0"
    with pytest.raises(ValueError, match="not compiled into independent hypergraph"):
        validate_spec({
            "schema": "rs-constraint-lab.experiment/v1",
            "experiment_id": "simplex-n4",
            "generation": 4,
            "semantics": "simplicial",
            "O": 3,
            "alphabet": "W4",
            "cells": [{"N": 4, "K_max": 2, "cardinalities": [1]}],
        })
    clock = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "clock-pin",
        "generation": 3,
        "semantics": "hypergraph",
        "G": 0, "S": 0, "H": 0, "L": 0, "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": "memory-clock-reanalysis",
        "predicates": ["pair", "triad"],
        "weights": ["strong_favour"],
        "cells": [{"N": 3, "K_max": 1, "A_max": 3, "cardinalities": [1]}],
    }
    plan = build_plan(clock, 4)
    assert plan["header"]["engine_version"] == "0.3.0"
    assert plan["header"]["semantic_version"] == "0.3.0"
    wider = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "n4-pin",
        "generation": 4,
        "semantics": "hypergraph",
        "G": 0, "S": 0, "H": 0, "L": 0, "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": "n4-singleton",
        "predicates": ["pair", "triad"],
        "weights": ["strong_favour"],
        "cells": [{"N": 4, "K_max": 2, "A_max": 4, "cardinalities": [1]}],
    }
    n4_plan = build_plan(wider, 20)
    assert n4_plan["header"]["engine_version"] == "0.4.0"
    assert n4_plan["header"]["semantic_version"] == "0.4.0"
    assert n4_plan["header"]["grammar_version"] == "independent-hypergraph-v1"
    assert "pairwise_n4_index_sha256" in n4_plan["header"]
    assert "comparison_kernel_index_sha256" not in n4_plan["shards"][0]["identity"]
    assert "pairwise_n4_index_sha256" in n4_plan["shards"][0]["identity"]
    refused = dict(wider)
    refused["cells"] = [{"N": 4, "K_max": 2, "cardinalities": [1, 2]}]
    with pytest.raises(ValueError, match="cardinality above 1"):
        build_plan(refused, 20)


def test_memory_clock_resume_replays_completed_shards(tmp_path, monkeypatch):
    monkeypatch.setenv("RS_LAB_PAIRWISE_INDEX", str(tmp_path / "no-index"))
    clear_index_cache()
    spec = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "miniature-clock-resume",
        "generation": 3,
        "semantics": "hypergraph",
        "G": 0, "S": 0, "H": 0, "L": 0, "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": "memory-clock-reanalysis",
        "predicates": ["pair", "triad"],
        "weights": ["strong_favour"],
        "cells": [{"N": 3, "K_max": 1, "A_max": 3, "cardinalities": [1]}],
    }
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    out = tmp_path / "out"
    assert main(["run", str(path), "--out", str(out), "--workers", "2", "--shard-items", "4", "--max-shards", "1"]) == 0
    progress = json.loads((out / "progress.json").read_text(encoding="utf-8"))
    assert progress["status"] == "IN_PROGRESS"
    assert progress["completed"] == 1
    plan = json.loads((out / "plan.json").read_text(encoding="utf-8"))
    done = next(
        shard["shard_id"]
        for shard in plan["shards"]
        if progress["shards"][shard["shard_id"]]["status"] == "completed"
    )
    receipt = (out / "shards" / done / "receipt.json").read_bytes()
    assert main(["run", str(path), "--out", str(out), "--workers", "2", "--shard-items", "4"]) == 0
    finished = json.loads((out / "progress.json").read_text(encoding="utf-8"))
    assert finished["status"] == "COMPLETE"
    assert (out / "shards" / done / "receipt.json").read_bytes() == receipt
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["engine_version"] == "0.3.0"
    assert summary["science"]["cells"][0]["clock_census"]["analysed"] > 0
