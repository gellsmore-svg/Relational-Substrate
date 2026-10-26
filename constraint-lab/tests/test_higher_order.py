"""Independent triadic relation: symmetry, bridge, reducibility, and resume."""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from rs_constraint_lab.cli import main
from rs_constraint_lab.constraints import parse_expression, set_cross_order_class
from rs_constraint_lab.dynamics import RelabelTables, canonical_tokens, family_ids
from rs_constraint_lab.exact import long_run, period_of
from rs_constraint_lab.execution import build_plan, run_spec, scientific_projection, verify_directory
from rs_constraint_lab.grammar import build_grammar
from rs_constraint_lab.higher_order import (
    classify_reducibility,
    clear_index_cache,
    coupling_report,
    emergent_memory_tv,
    information_flow,
    load_comparison_indexes,
    orbit_catalogue,
    pairwise_jump_kernels,
)
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.constraints import Choreography
from rs_constraint_lab.observables import heavy_observables, light_observables
from rs_constraint_lab.spec import validate_spec
from rs_constraint_lab.state import permutations, relabel_relation_state, relation_slots
from rs_constraint_lab.version import ENGINE_VERSION, SEMANTIC_VERSION
from rs_constraint_lab.weights import alphabet_factors

PIN_KEYS = [
    "G", "H", "L", "O", "S", "a_max", "alphabet", "analysis", "cardinality", "cell_index",
    "composition", "end", "engine_version", "grammar_version", "k_max", "n",
    "normalisation_version", "predicates", "rise_release_horizon", "semantic_version",
    "sensitivity_alphabets", "spec_hash", "start", "weights",
]


def _factors():
    return alphabet_factors("W4")


def _slots():
    return tuple(relation_slots(3, 3))


def _hyper(expressions, rho=1):
    constraints = tuple(parse_expression(text, 3, order=3) for text in expressions)
    baselines = (Fraction(1), Fraction(1), Fraction(1), Fraction(rho))
    kernel = build_kernel(
        3,
        Choreography(0, 0, constraints),
        _factors(),
        relation_slots=_slots(),
        baseline_weights=baselines,
    )
    return constraints, kernel


def _graph(expressions):
    constraints = tuple(parse_expression(text, 3) for text in expressions)
    return build_kernel(3, Choreography(0, 0, constraints), _factors())


def _indexes(tmp_path, monkeypatch):
    directory = tmp_path / "pairwise-index"
    directory.mkdir()
    tables = RelabelTables(3)
    baseline = build_kernel(3, Choreography(0, 0, ()), {})
    ids = family_ids(3, canonical_tokens(baseline, tables))
    favoured = _graph(["form(0-1) => strong_favour"])
    favoured_ids = family_ids(3, canonical_tokens(favoured, tables))
    (directory / "kernel-ids-n3-k3.txt").write_text(
        ids["exact_kernel_family"] + "\n" + favoured_ids["exact_kernel_family"] + "\n",
        encoding="utf-8",
    )
    (directory / "qualitative-ids-n3-k3.txt").write_text(
        ids["qualitative_family"] + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("RS_LAB_PAIRWISE_INDEX", str(directory))
    clear_index_cache()
    loaded = load_comparison_indexes()
    return loaded, ids, favoured_ids


def test_graph_shard_identity_is_unchanged():
    spec = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "identity-pin",
        "generation": 0,
        "semantics": "graph",
        "G": 0, "S": 0, "H": 0, "L": 0, "O": 2,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": "heavy-every-canonical",
        "predicates": ["edge"],
        "weights": ["prohibit", "strong_favour"],
        "cells": [{"N": 2, "K_max": 1, "cardinalities": [1]}],
    }
    plan = build_plan(spec, 2)
    shard = plan["shards"][0]
    assert shard["shard_id"] == "fe7e54a496ad68078d24acaf"
    assert sorted(shard["identity"]) == PIN_KEYS
    assert shard["identity"]["engine_version"] == ENGINE_VERSION == "0.2.0"
    assert shard["identity"]["semantic_version"] == SEMANTIC_VERSION == "0.2.0"
    assert shard["identity"]["grammar_version"] == "pairwise-edge-v1"
    assert plan["header"]["engine_version"] == "0.2.0"
    assert "rho3" not in shard["identity"]
    assert "semantics" not in shard["identity"]


def test_sixteen_states_four_toggles_and_eight_orbits():
    constraints, kernel = _hyper([])
    assert kernel.n_states == 16
    assert kernel.n_edges == 4
    assert constraints == ()
    for state, row in enumerate(kernel.successors):
        assert len(row) == 4
        assert all(prob == Fraction(1, 4) for _nxt, prob in row)
        for nxt, _prob in row:
            assert (state ^ nxt).bit_count() == 1
    assert period_of(list(range(16)), kernel.successors) == 2
    ran = long_run(kernel, 0)
    assert ran["stationary_arithmetic"] == "rational"
    assert all(ran["distribution_exact"][state] == Fraction(1, 16) for state in range(16))
    heavy = heavy_observables(kernel, 4, 0)
    assert heavy["triad_occupancy_exact"] == "1/2"
    assert heavy["pair_density_triad_absent_exact"] == "1/2"
    assert heavy["pair_density_triad_present_exact"] == "1/2"
    catalogue = orbit_catalogue(3)
    assert catalogue["orbit_count"] == 8
    assert catalogue["labelled_states"] == 16
    names = {row["name"]: row["size"] for row in catalogue["orbits"]}
    assert names == {
        "empty-pairs-no-triad": 1,
        "empty-pairs-triad": 1,
        "one-pair-no-triad": 3,
        "one-pair-triad": 3,
        "wedge-no-triad": 3,
        "wedge-triad": 3,
        "triangle-no-triad": 1,
        "triangle-triad": 1,
    }


def test_triad_is_fixed_and_pairs_permute():
    slots = _slots()
    triad = 1 << 3
    pair = 1 << 0
    images_triad = {relabel_relation_state(triad, perm, slots) for perm in permutations(3)}
    images_pair = {relabel_relation_state(pair, perm, slots) for perm in permutations(3)}
    assert images_triad == {triad}
    assert images_pair == {1 << 0, 1 << 1, 1 << 2}
    grammar = build_grammar(3, 1, ["strong_favour"], predicates=("pair", "triad"), order=3)
    triad_rule = parse_expression("form(0-1-2) => strong_favour", 3, order=3)
    pair_rule = parse_expression("form(0-1) => strong_favour", 3, order=3)
    assert grammar.labelled[grammar.image[0][grammar.labelled.index(triad_rule)]] == triad_rule
    images = set()
    for row in grammar.image:
        image = grammar.labelled[row[grammar.labelled.index(pair_rule)]]
        images.add(image.expression(grammar.slot_list()))
    assert images == {
        "form(0-1) => strong_favour",
        "form(0-2) => strong_favour",
        "form(1-2) => strong_favour",
    }
    triad_images = set()
    for row in grammar.image:
        image = grammar.labelled[row[grammar.labelled.index(triad_rule)]]
        triad_images.add(image.expression(grammar.slot_list()))
    assert triad_images == {"form(0-1-2) => strong_favour"}


def test_cross_order_syntax_and_classes():
    samples = {
        "form(0-1) => strong_favour": "P->P",
        "form(0-1-2) => strong_favour": "T->T",
        "form(0-1-2) | present(0-1) => weak_favour": "P->T",
        "dissolve(0-1-2) | present(0-1) => prohibit": "P->T",
        "dissolve(0-1) | present(0-1-2) => strong_favour": "T->P",
        "form(0-1) | present(0-1-2) => strong_favour": "T->P",
        "form(0-1-2) | present(0-1-2) => strong_favour": None,
    }
    parsed = []
    for text, label in samples.items():
        if label is None:
            with pytest.raises(ValueError, match="not normal form"):
                parse_expression(text, 3, order=3)
            continue
        constraint = parse_expression(text, 3, order=3)
        assert constraint.expression(list(_slots())) == text
        assert set_cross_order_class((constraint,), 3) == label
        parsed.append(constraint)
    assert set_cross_order_class(parsed, 3) == "mixed"
    with pytest.raises(ValueError, match="not a pairwise"):
        parse_expression("form(0-1-2) => strong_favour", 3)
    with pytest.raises(ValueError, match="count predicates"):
        parse_expression("form(0-1) | count>=1 => strong_favour", 3, order=3)
    bare_triad = parse_expression("form(0-1-2) => strong_favour", 3, order=3)
    assert bare_triad.arity(list(_slots())) == 3
    assert bare_triad.k() == 1


def test_grammar_size_is_exact_at_k2():
    weights = ["prohibit", "strong_suppress", "weak_suppress", "weak_favour", "strong_favour"]
    grammar = build_grammar(3, 2, weights, a_max=3, predicates=("pair", "triad"), order=3)
    stats = grammar.stats
    assert len(grammar.relation_slots) == 4
    assert stats["structural_normal_forms"] == 56
    assert stats["labelled_constraints"] == 280
    assert sum(stats["structural_by_class"].values()) == 56
    assert stats["structural_by_class"]["P->P"] > 0
    assert stats["structural_by_class"]["P->T"] > 0
    assert stats["structural_by_class"]["T->P"] > 0
    assert stats["structural_by_class"]["T->T"] > 0
    wider = build_grammar(3, 3, weights, predicates=("pair", "triad"), order=3)
    assert wider.stats["structural_normal_forms"] == 152
    assert wider.stats["labelled_constraints"] == 760


def test_pairwise_conditional_kernel_matches_generation_1b():
    rule = "form(0-2) | present(0-1) & present(1-2) => strong_favour"
    graph = _graph([rule])
    _constraints, hyper = _hyper([rule])
    absent, present = pairwise_jump_kernels(hyper)
    tables = RelabelTables(3)
    graph_ids = family_ids(3, canonical_tokens(graph, tables))
    absent_ids = family_ids(3, canonical_tokens(absent, tables))
    present_ids = family_ids(3, canonical_tokens(present, tables))
    assert absent_ids["exact_kernel_family"] == graph_ids["exact_kernel_family"]
    assert present_ids["exact_kernel_family"] == graph_ids["exact_kernel_family"]
    for state in range(8):
        assert absent.successors[state] == graph.successors[state]
        assert present.weights[state] == graph.weights[state]
    graph_light = light_observables(graph, _graph([]))
    hyper_light = light_observables(hyper, _hyper([])[1])
    assert graph_light["closing_bias_exact"] == "1/9"
    assert hyper_light["closing_bias_exact"] == "1/9"
    assert heavy_observables(graph, 4, 0)["triangle_mass_exact"] == "11/64"
    free_absent, free_present = pairwise_jump_kernels(_hyper([])[1])
    free_graph = _graph([])
    assert free_absent.successors == free_graph.successors
    assert free_present.successors == free_graph.successors


def test_reducibility_memory_and_information(tmp_path, monkeypatch):
    indexes, baseline_ids, favoured_ids = _indexes(tmp_path, monkeypatch)
    tables = indexes["graph_tables"]

    empty_constraints, empty = _hyper([])
    empty_report = coupling_report(empty, empty_constraints, indexes)
    assert empty_report["reducibility_class"] == "FULLY_REDUCIBLE"
    assert empty_report["reducibility"]["jump_id_triad_absent"] == baseline_ids["exact_kernel_family"]
    assert empty_report["emergent_memory_tv"] == 0
    assert empty_report["triad_predicts_next_pair"] == 0
    assert empty_report["pair_predicts_next_triad"] == 0
    assert information_flow(empty)["cmi_triad_to_pair_bits"] == 0
    assert information_flow(empty)["cmi_pair_to_triad_bits"] == 0

    edge_constraints, edge = _hyper(["form(0-1) => strong_favour"])
    edge_class = classify_reducibility(edge, indexes, tables)
    assert edge_class["class"] == "FULLY_REDUCIBLE"
    assert edge_class["jump_id_triad_absent"] == favoured_ids["exact_kernel_family"]
    assert edge_class["jump_equal"] is True
    assert edge_class["rate_competition"] is True
    edge_info = information_flow(edge)
    assert edge_info["triad_predicts_next_pair"] is False
    assert edge_info["pair_predicts_next_triad"] is True
    assert edge_info["cmi_pair_to_triad_bits"] > 0

    projection_constraints, projection = _hyper(["form(0-1-2) | present(0-1) => strong_favour"])
    projection_class = classify_reducibility(projection, indexes, tables)
    assert set_cross_order_class(projection_constraints, 3) == "P->T"
    assert projection_class["class"] == "PAIRWISE_PROJECTION_REDUCIBLE"
    assert projection_class["jump_id_triad_absent"] == baseline_ids["exact_kernel_family"]
    assert projection_class["triad_weight_depends_on_pairs"] is True

    coupled_constraints, coupled = _hyper(["form(0-1) | present(0-1-2) => strong_favour"])
    coupled_class = classify_reducibility(coupled, indexes, tables)
    assert set_cross_order_class(coupled_constraints, 3) == "T->P"
    assert coupled_class["class"] == "IRREDUCIBLE_DYNAMIC_COUPLING"
    assert coupled_class["jump_equal"] is False
    assert emergent_memory_tv(coupled) > 0
    assert information_flow(coupled)["triad_predicts_next_pair"] is True

    outside_constraints, outside = _hyper(["form(0-1) => weak_favour"])
    outside_class = classify_reducibility(outside, indexes, tables)
    assert outside_constraints
    assert outside_class["jump_equal"] is True
    assert outside_class["class"] == "OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR"

    missing = dict(indexes)
    missing["kernels"] = None
    assert classify_reducibility(empty, missing, tables)["class"] == "UNRESOLVED"


def test_simplicial_is_not_compiled(tmp_path):
    spec = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "simplex",
        "generation": 3,
        "semantics": "simplicial",
        "O": 3,
        "alphabet": "W4",
        "cells": [{"N": 3, "K_max": 1, "cardinalities": [1]}],
    }
    with pytest.raises(ValueError, match="not compiled into independent hypergraph"):
        validate_spec(spec)
    path = tmp_path / "simplex.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    with pytest.raises(ValueError, match="not compiled into independent hypergraph"):
        main(["plan", str(path)])


def _hyper_spec():
    return {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "miniature-hypergraph-resume",
        "generation": 3,
        "semantics": "hypergraph",
        "G": 0, "S": 0, "H": 0, "L": 0, "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": "heavy-every-canonical",
        "predicates": ["pair", "triad"],
        "weights": ["prohibit", "strong_favour"],
        "cells": [{"N": 3, "K_max": 1, "A_max": 3, "cardinalities": [1]}],
        "trajectory": {"horizon": 4, "seeds": [0]},
        "rise_release_horizon": 2,
    }


def test_hypergraph_resume_keeps_shard_identity(tmp_path, monkeypatch):
    monkeypatch.setenv("RS_LAB_PAIRWISE_INDEX", str(tmp_path / "no-index"))
    monkeypatch.delenv("RS_LAB_FAULT", raising=False)
    clear_index_cache()
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_hyper_spec()), encoding="utf-8")
    assert main(["plan", str(spec_path), "--shard-items", "4"]) == 0
    plan = build_plan(_hyper_spec(), 4)
    assert plan["header"]["engine_version"] == "0.3.0"
    assert plan["header"]["semantic_version"] == "0.3.0"
    assert plan["header"]["grammar_version"] == "independent-hypergraph-v1"
    assert plan["header"]["rho3"] == "1"
    assert plan["estimates"]["cells"][0]["labelled_states"] == 16
    assert plan["estimates"]["cells"][0]["canonical_states"] == 8
    identity = plan["shards"][0]["identity"]
    assert identity["semantics"] == "hypergraph"
    assert identity["O"] == 3
    assert identity["engine_version"] == "0.3.0"
    assert "comparison_kernel_index_sha256" in identity

    interrupted = tmp_path / "interrupted"
    assert main([
        "run", str(spec_path),
        "--out", str(interrupted),
        "--workers", "2",
        "--shard-items", "4",
        "--max-shards", "1",
    ]) == 0
    progress = json.loads((interrupted / "progress.json").read_text(encoding="utf-8"))
    assert progress["status"] == "IN_PROGRESS"
    assert progress["completed"] == 1
    receipt_before = {
        shard["shard_id"]: (interrupted / "shards" / shard["shard_id"] / "receipt.json").read_text(encoding="utf-8")
        for shard in plan["shards"]
        if (interrupted / "shards" / shard["shard_id"] / "receipt.json").is_file()
    }
    assert len(receipt_before) == 1
    assert main(["resume", str(interrupted), "--workers", "2"]) == 0
    for shard_id, text in receipt_before.items():
        assert (interrupted / "shards" / shard_id / "receipt.json").read_text(encoding="utf-8") == text
    assert verify_directory(interrupted)["ok"] is True
    clean = tmp_path / "clean"
    assert main([
        "run", str(spec_path),
        "--out", str(clean),
        "--workers", "2",
        "--shard-items", "4",
    ]) == 0
    left = scientific_projection(json.loads((interrupted / "summary.json").read_text(encoding="utf-8")))
    right = scientific_projection(json.loads((clean / "summary.json").read_text(encoding="utf-8")))
    assert left == right
    assert right["cells"][0]["cardinalities"]["1"]["canonical"] == 8
    assert sum(right["cells"][0]["higher_order"]["sets_by_class"].values()) == 8
    assert left["cells"][0]["higher_order"]["kernel_index_present"] is False
    assert run_spec(_hyper_spec(), clean, workers=2, shard_items=4)["status"] == "COMPLETE"
