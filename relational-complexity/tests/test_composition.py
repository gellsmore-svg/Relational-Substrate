"""Typed composition operators. Validation fixtures, not a scientific round."""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from rrc.composition import (
    MAX_CANONICAL_VERTICES,
    _compact,
    active_intersection_labels,
    apply_again,
    block_family_report,
    canonical_simple_graph,
    carrier_automorphisms,
    carrier_orbit,
    intersection_graph,
    intersection_representation,
    iterate_line_graph,
    cover_count_labels,
    fixed_cover,
    labelled_active_block_labels,
    labelled_line_graph,
    labelled_realised_block_labels,
    line_graph,
    line_of_intersection,
    nerve,
    observation_law,
    present_canonical_line_graph_labels,
    present_carrier_orbit_labels,
    present_degree_labels,
    present_edge_count_labels,
    present_labelled_line_graph_labels,
    present_line_graph_labels,
    realised_intersection_labels,
    realised_overlap_count_labels,
    relabeling_exists,
    successive_observations,
)
from rrc.constraints import compile_weight_table
from rrc.items import execute_composition_observation


PATH4 = [[0, 1], [1, 2], [2, 3], [3, 4]]
CYCLE5 = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]]
TRIANGLE = [[0, 1], [1, 2], [0, 2]]
STAR = [[0, 1], [0, 2], [0, 3]]
CHAIN = [[0, 1], [1, 2], [2, 3]]


def labelled_adjacencies(result):
    vertices = [tuple(vertex) for vertex in result["vertices"]]
    return frozenset(
        frozenset((vertices[left], vertices[right]))
        for left, right in (tuple(edge) for edge in result["bare_edges"])
    )


def baseline(n, edges):
    return compile_weight_table(n, {"kind": "listed", "edges": edges}, [])


def test_a_path_reaches_the_empty_graph_and_a_cycle_is_fixed():
    steps = iterate_line_graph(PATH4, 6, vertex_count=5)
    edge_counts = [step["edge_count"] for step in steps]
    assert edge_counts == [4, 3, 2, 1, 0, 0, 0]
    assert steps[0]["vertex_count"] == 5
    assert steps[1]["vertex_count"] == 4
    assert steps[1]["input_isolated_vertices"] is None
    assert steps[5]["second_application"] == "defined"
    assert steps[5]["dynamics"] == "none"
    assert steps[5]["new_state"] is False
    cycle = iterate_line_graph(CYCLE5, 3, vertex_count=5)
    assert {tuple(edge) for edge in cycle[1]["bare_edges"]} == {tuple(edge) for edge in CYCLE5}
    assert [(step["vertex_count"], step["edge_count"]) for step in cycle[1:]] == [(5, 5), (5, 5), (5, 5)]
    assert cycle[1]["input_isolated_vertices"] is None


def test_isolated_input_vertices_are_absent_from_the_line_graph():
    graph = line_graph([[0, 1]], vertex_count=4)
    assert graph["vertex_count"] == 1
    assert graph["edge_count"] == 0
    assert graph["input_isolated_vertices"] == 2
    assert graph["vertices"] == [[0, 1]]
    again = apply_again(graph)
    assert again["vertex_count"] == 0
    assert again["bare_edges"] == []


def test_triangle_and_star_share_a_bare_line_graph_and_not_their_labels():
    triangle = line_graph(TRIANGLE)
    star = line_graph(STAR)
    assert triangle["bare_edges"] == star["bare_edges"] == [[0, 1], [0, 2], [1, 2]]
    assert triangle["vertices"] != star["vertices"]
    assert labelled_adjacencies(triangle) != labelled_adjacencies(star)
    forward = line_graph(PATH4)
    reordered = line_graph([[0, 1], [2, 3], [3, 4], [1, 2]])
    assert forward["bare_edges"] != reordered["bare_edges"]
    assert labelled_adjacencies(forward) == labelled_adjacencies(reordered)


def test_malformed_graphs_are_rejected():
    with pytest.raises(ValueError):
        line_graph([[0, 0]])
    with pytest.raises(ValueError):
        line_graph([[0, 1], [1, 0]])
    with pytest.raises(ValueError):
        line_graph([[0, 1]], vertex_count=True)


def test_intersection_graph_loses_information_the_nerve_can_keep():
    pairwise = [[1, 2], [2, 3], [1, 3]]
    common = [[1, 2], [1, 3], [1, 4]]
    nested = [[1], [1, 2], [1, 2, 3]]
    pair_graph = intersection_graph(pairwise)
    common_graph = intersection_graph(common)
    nested_graph = intersection_graph(nested)
    assert pair_graph["bare_edges"] == common_graph["bare_edges"] == nested_graph["bare_edges"]
    assert pair_graph["second_application"] == "undefined"
    assert pair_graph["new_state"] is False
    assert pair_graph["dynamics"] == "none"
    assert nerve(pairwise)["max_face_vertices"] == 2
    assert nerve(common)["max_face_vertices"] == 3
    assert nerve(nested)["faces"] == nerve(common)["faces"]
    assert nerve(nested)["blocks"] != nerve(common)["blocks"]
    assert apply_again(pair_graph)["second_application"] == "undefined"
    assert apply_again(nerve(pairwise))["output_type"] == "undefined"
    composed = line_of_intersection(pairwise)
    assert composed["composition"] == "line_graph_after_intersection_graph"
    assert composed["second_application"] == "defined"
    assert composed["edge_count"] == 3


def test_every_graph_in_the_fixture_has_an_intersection_representation():
    blocks = intersection_representation(5, PATH4)
    assert intersection_graph(blocks)["bare_edges"] == PATH4
    isolated = intersection_representation(3, [[0, 1]])
    graph = intersection_graph(isolated)
    assert graph["vertex_count"] == 3
    assert graph["bare_edges"] == [[0, 1]]


def test_a_large_nerve_is_refused_rather_than_simplified():
    blocks = [[index] for index in range(13)]
    with pytest.raises(ValueError, match="cap"):
        nerve(blocks)


def test_the_present_line_graph_is_not_a_new_state_and_not_always_markov():
    triangle = baseline(3, TRIANGLE)
    chain = baseline(4, CHAIN)
    triangle_labels = present_line_graph_labels(TRIANGLE)
    chain_labels = present_line_graph_labels(CHAIN)
    triangle_law = observation_law(triangle, triangle_labels)
    chain_law = observation_law(chain, chain_labels)
    assert triangle_law["new_state"] is False
    assert triangle_law["n_states"] == 8
    assert triangle_law["n_distinct_labels"] == 4
    assert triangle_law["injective"] is False
    assert triangle_law["exact"] is True
    assert triangle_law["defect_l1"] == 0
    assert chain_law["n_distinct_labels"] < 8
    assert chain_law["exact"] is False
    assert chain_law["defect_l1"] == Fraction(4, 9)
    for edges, weights in (
        (TRIANGLE, triangle),
        (CHAIN, chain),
        (STAR, baseline(4, STAR)),
    ):
        edge_law = observation_law(weights, present_edge_count_labels(edges))
        assert edge_law["exact"] is True
        assert edge_law["n_distinct_labels"] == len(edges) + 1
        assert edge_law["injective"] is False
        assert edge_law["new_state"] is False
    degree_law = observation_law(chain, present_degree_labels(4, CHAIN))
    assert degree_law["new_state"] is False
    assert degree_law["injective"] is False
    assert degree_law["exact"] is False
    assert degree_law["defect_l1"] == Fraction(4, 9)
    assert _same_partition(present_degree_labels(4, CHAIN), chain_labels)


def _same_partition(left, right):
    return all((left[i] == left[j]) == (right[i] == right[j]) for i in range(len(left)) for j in range(len(right)))


def test_baseline_observations_are_description_dependent():
    path = [[0, 1], [1, 2], [2, 3], [3, 4]]
    cycle = [[0, 1], [1, 2], [2, 3], [0, 3]]
    cases = (
        (5, path, False, Fraction(1, 3), False, Fraction(1, 3), False),
        (4, cycle, True, Fraction(0, 1), False, Fraction(1, 2), False),
    )
    for n, edges, degree_exact, degree_defect, line_exact, line_defect, same in cases:
        weights = baseline(n, edges)
        degree = present_degree_labels(n, edges)
        line = present_line_graph_labels(edges)
        degree_law = observation_law(weights, degree)
        line_law = observation_law(weights, line)
        edge_law = observation_law(weights, present_edge_count_labels(edges))
        assert edge_law["exact"] is True
        assert degree_law["exact"] is degree_exact
        assert degree_law["defect_l1"] == degree_defect
        assert line_law["exact"] is line_exact
        assert line_law["defect_l1"] == line_defect
        assert degree_law["new_state"] is False
        assert line_law["new_state"] is False
        assert _same_partition(degree, line) is same
        assert not _same_partition(line, present_edge_count_labels(edges))


def test_atlas_007_plan_is_a_baseline_observation_sample():
    import json
    from pathlib import Path

    from rrc.store import digest

    plan = json.loads((Path(__file__).resolve().parents[1] / "plans" / "atlas-007.json").read_text(encoding="utf-8"))
    assert digest(plan) == "8b655f094fb4b9bfc10c124a00fecab228a178b10df2310ea87e10fb0350c766"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "e5a97d27cfec31aa76ae2f7e8c88e73231cab649"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.001
    assert plan["no_sampling"] is True
    assert plan["questions"] == ["ATLAS-Q10"]
    assert "ATLAS-Q12" in plan["questions_not_in_this_round"]
    assert "EQ-020" in plan["selection"]
    assert len(plan["items"]) == 15
    seen = {}
    for item in plan["items"]:
        assert item["type"] == "composition_observation"
        assert item["constraints"] == []
        assert item["baseline"] == 1
        seen.setdefault(item["id"].split("-")[1], set()).add(item["observation"])
    expected = {
        "present_line_graph",
        "present_edge_count",
        "present_degree_sequence",
    }
    assert seen.keys() == {"triangle", "chain", "star", "path4", "cycle4"}
    assert all(value == expected for value in seen.values())


def test_atlas_008_plan_repeats_the_baseline_maps_with_round_ids():
    import json
    from pathlib import Path

    from rrc.store import digest

    plan = json.loads((Path(__file__).resolve().parents[1] / "plans" / "atlas-008.json").read_text(encoding="utf-8"))
    assert digest(plan) == "6d558c5191bf82c5bec3285f9ae39bb19b9a5934998f36601b52b0f810b9bdb4"
    assert plan["engine_version"] == "rrc-0.4.0"
    assert plan["definitions_commit"] == "6778da87f25c7ec13f875960ed04ba99a5a0ef11"
    assert plan["preflight_summary"]["scientific"] is False
    assert plan["preflight_summary"]["heaviest_cell_s"] == 0.001
    assert plan["no_sampling"] is True
    assert plan["questions"] == ["ATLAS-Q10"]
    assert "ATLAS-Q12" in plan["questions_not_in_this_round"]
    assert "EQ-020" in plan["selection"]
    assert "stored no law" in plan["selection"]
    assert len(plan["items"]) == 15
    seen = {}
    for item in plan["items"]:
        assert item["round_id"] == "atlas-008"
        assert item["id"].startswith("A8-")
        assert item["type"] == "composition_observation"
        assert item["constraints"] == []
        assert item["baseline"] == 1
        seen.setdefault(item["id"].split("-")[1], set()).add(item["observation"])
    expected = {
        "present_line_graph",
        "present_edge_count",
        "present_degree_sequence",
    }
    assert seen.keys() == {"triangle", "chain", "star", "path4", "cycle4"}
    assert all(value == expected for value in seen.values())


def test_edge_count_is_lumpable_for_any_constant_positive_baseline():
    disjoint = [[0, 1], [2, 3]]
    weights = compile_weight_table(4, {"kind": "listed", "edges": disjoint}, [], baseline=5)
    width = 2
    for state in range(1 << width):
        present = state.bit_count()
        row = [int(value) for value in weights[state]]
        total = sum(row)
        decrease = sum(row[bit] for bit in range(width) if (state >> bit) & 1)
        assert decrease * width == present * total
        assert (total - decrease) * width == (width - present) * total
    law = observation_law(weights, present_edge_count_labels(disjoint))
    assert law["exact"] is True
    assert law["defect_l1"] == Fraction(0)
    assert law["n_distinct_labels"] == 3
    assert law["new_state"] is False
    single = compile_weight_table(3, {"kind": "listed", "edges": [[0, 1]]}, [], baseline=1)
    single_law = observation_law(single, present_edge_count_labels([[0, 1]]))
    assert single_law["exact"] is True
    assert single_law["n_distinct_labels"] == 2


def test_atlas_008_execution_stores_the_label_laws():
    import json
    from pathlib import Path

    from rrc.cli import main

    root = Path(__file__).resolve().parents[1]
    assert main(["verify", "--round", "atlas-008", "--out", str(root / "results" / "atlas-008")]) == 0
    items = root / "results" / "atlas-008" / "items"

    def load(name):
        return json.loads((items / name / "result.json").read_text(encoding="utf-8"))

    chain = load("A8-chain-line")
    degree = load("A8-chain-degree")
    count = load("A8-chain-count")
    path_line = load("A8-path4-line")
    path_degree = load("A8-path4-degree")
    cycle_degree = load("A8-cycle4-degree")
    cycle_line = load("A8-cycle4-line")
    assert chain["defect_l1"]["num"] == "4" and chain["defect_l1"]["den"] == "9"
    assert degree["defect_l1"]["num"] == "4" and degree["n_distinct_labels"] == 5
    assert count["exact"] is True and count["n_distinct_labels"] == 4
    assert chain["weight_sha256"] == count["weight_sha256"] == degree["weight_sha256"]
    assert chain["weight_sha256"] == "3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7"
    assert path_line["defect_l1"]["num"] == "1" and path_line["defect_l1"]["den"] == "3"
    assert path_line["n_distinct_labels"] == 8 and path_degree["n_distinct_labels"] == 7
    assert path_degree["defect_l1"]["den"] == "3"
    assert cycle_degree["exact"] is True and cycle_degree["n_distinct_labels"] == 6
    assert cycle_line["defect_l1"]["num"] == "1" and cycle_line["defect_l1"]["den"] == "2"
    assert cycle_line["n_distinct_labels"] == 8
    assert path_line["weight_sha256"] == "5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3"
    for name in ("A8-triangle-line", "A8-star-count", "A8-cycle4-count"):
        result = load(name)
        assert result["new_state"] is False
        assert result["injective"] is False
        assert result["further_label"] == "undefined"
        assert result["kernel_sha256"] == result["weight_sha256"]


def test_atlas_007_execution_stored_no_law():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "results" / "atlas-007" / "items"
    names = sorted(path.name for path in root.iterdir())
    assert len(names) == 15
    for name in names:
        result = json.loads((root / name / "result.json").read_text(encoding="utf-8"))
        assert result["status"] == "failed"
        assert result["round_id"] == "atlas-007"
        assert "KeyError: 'round_id'" in result["error"]
        assert "weights" not in result
        assert "defect_l1" not in result
        assert "exact" not in result


def test_composition_observation_completes_when_the_spec_omits_round_id():
    spec = {
        "id": "fixture-chain-line-bare",
        "type": "composition_observation",
        "n": 4,
        "carrier": {"kind": "listed", "edges": CHAIN},
        "constraints": [],
        "baseline": 1,
        "observation": "present_line_graph",
    }
    result = execute_composition_observation(spec)
    assert "round_id" not in spec
    assert result["status"] == "complete"
    assert result["round_id"] is None
    assert result["exact"] is False
    assert result["defect_l1"]["num"] == "4"
    assert result["defect_l1"]["den"] == "9"


def test_composition_observation_item_matches_the_chain_fixture():
    result = execute_composition_observation(
        {
            "id": "fixture-chain-line",
            "round_id": "fixture",
            "type": "composition_observation",
            "n": 4,
            "carrier": {"kind": "listed", "edges": CHAIN},
            "constraints": [],
            "baseline": 1,
            "observation": "present_line_graph",
        }
    )
    assert result["status"] == "complete"
    assert result["new_state"] is False
    assert result["further_label"] == "undefined"
    assert result["exact"] is False
    assert result["defect_l1"]["num"] == "4"
    assert result["defect_l1"]["den"] == "9"
    assert result["n_states"] == 8
    assert result["n_distinct_labels"] == 5
    assert result["quotient"]["defined"] is False
    assert result["quotient"]["rows"] is None
    count = execute_composition_observation(
        {
            "id": "fixture-chain-count",
            "round_id": "fixture",
            "type": "composition_observation",
            "n": 4,
            "carrier": {"kind": "listed", "edges": CHAIN},
            "constraints": [],
            "observation": "present_edge_count",
        }
    )
    assert count["exact"] is True
    assert count["defect_l1"]["num"] == "0"
    assert count["weight_sha256"] == result["weight_sha256"]


CYCLE4 = [[0, 1], [1, 2], [2, 3], [0, 3]]


def _fraction(cell):
    return Fraction(int(cell["num"]), int(cell["den"]))


def _law(n, edges, labels, constraints=None):
    weights = compile_weight_table(
        n,
        {"kind": "listed", "edges": edges},
        [] if constraints is None else constraints,
    )
    return observation_law(weights, labels)


def test_canonical_form_agrees_with_an_independent_search_and_stops_at_the_cap():
    from itertools import combinations

    possible = [list(pair) for pair in combinations(range(4), 2)]
    graphs = []
    for mask in range(1 << len(possible)):
        graphs.append([possible[bit] for bit in range(len(possible)) if (mask >> bit) & 1])
    certificates = [
        tuple(tuple(edge) for edge in canonical_simple_graph(4, edges)["edges"])
        for edges in graphs
    ]
    for left in range(len(graphs)):
        for right in range(left, len(graphs)):
            same = relabeling_exists(4, graphs[left], graphs[right])
            assert (certificates[left] == certificates[right]) is same
    cycle = canonical_simple_graph(4, CYCLE4)
    rotated = canonical_simple_graph(4, [[1, 2], [2, 3], [0, 3], [0, 1]])
    assert cycle["edges"] == rotated["edges"]
    assert relabeling_exists(4, CYCLE4, [[1, 2], [2, 3], [0, 3], [0, 1]]) is True
    path = [[0, 1], [1, 2], [2, 3]]
    assert relabeling_exists(4, CYCLE4, path) is False
    assert canonical_simple_graph(4, path)["edges"] != cycle["edges"]
    assert canonical_simple_graph(3, [[0, 1]])["vertex_count"] == 3
    assert canonical_simple_graph(2, [[0, 1]])["edges"] == [[0, 1]]
    assert canonical_simple_graph(0, [])["edges"] == []
    again = apply_again(cycle)
    assert again["edges"] == cycle["edges"]
    assert again["second_application"] == "defined_and_idempotent"
    with pytest.raises(ValueError, match="cap"):
        canonical_simple_graph(MAX_CANONICAL_VERTICES + 1, [])
    assert canonical_simple_graph(MAX_CANONICAL_VERTICES, [])["vertex_count"] == MAX_CANONICAL_VERTICES


def test_labelled_line_graph_keeps_edges_and_does_not_reapply():
    forward = labelled_line_graph([[0, 1], [1, 2], [2, 3]])
    reordered = labelled_line_graph([[2, 3], [0, 1], [1, 2]])
    shifted = labelled_line_graph([[1, 2], [2, 3], [3, 4]])
    assert forward["vertices"] == reordered["vertices"]
    assert forward["adjacent"] == reordered["adjacent"]
    assert forward["vertices"] != shifted["vertices"]
    assert forward["second_application"] == "undefined"
    assert apply_again(forward)["output_type"] == "undefined"
    triangle = labelled_line_graph(TRIANGLE)
    star = labelled_line_graph(STAR)
    assert triangle["vertices"] != star["vertices"]
    bare_triangle = canonical_simple_graph(3, line_graph(TRIANGLE)["bare_edges"])
    bare_star = canonical_simple_graph(3, line_graph(STAR)["bare_edges"])
    assert bare_triangle["edges"] == bare_star["edges"]
    labels = present_labelled_line_graph_labels(CYCLE4)
    assert len(labels) == len({json.dumps(label, sort_keys=True) for label in labels})
    for constraints in (
        [],
        [{
            "effect": "multiply",
            "factor": 3,
            "event": [0, 1],
            "action": "either",
            "when": {"edge": [1, 2], "polarity": "present"},
        }],
    ):
        law = _law(4, CYCLE4, labels, constraints)
        assert law["injective"] is True
        assert law["exact"] is True
        assert law["new_state"] is False
        assert law["defect_l1"] == 0
        assert law["quotient"]["defined"] is True


def test_four_cycle_canonical_line_graph_is_exact_and_the_indexed_label_is_not():
    indexed = present_line_graph_labels(CYCLE4)
    canonical = present_canonical_line_graph_labels(CYCLE4)
    orbits = present_carrier_orbit_labels(4, CYCLE4)
    degrees = present_degree_labels(4, CYCLE4)
    counts = present_edge_count_labels(CYCLE4)
    indexed_law = _law(4, CYCLE4, indexed)
    canonical_law = _law(4, CYCLE4, canonical)
    orbit_law = _law(4, CYCLE4, orbits)
    assert indexed_law["n_distinct_labels"] == 8
    assert indexed_law["exact"] is False
    assert indexed_law["defect_l1"] == Fraction(1, 2)
    assert indexed_law["quotient"]["defined"] is False
    assert canonical_law["n_distinct_labels"] == 6
    assert canonical_law["exact"] is True
    assert canonical_law["defect_l1"] == 0
    assert orbit_law["exact"] is True
    assert orbit_law["n_distinct_labels"] == 6
    assert _same_partition(canonical, orbits)
    assert _same_partition(canonical, degrees)
    assert not _same_partition(canonical, indexed)
    assert not _same_partition(canonical, counts)
    drawing_a = line_graph([CYCLE4[0], CYCLE4[2], CYCLE4[3]])
    drawing_b = line_graph([CYCLE4[0], CYCLE4[1], CYCLE4[2]])
    assert drawing_a["bare_edges"] != drawing_b["bare_edges"]
    assert canonical_simple_graph(drawing_a["vertex_count"], drawing_a["bare_edges"])["edges"] == (
        canonical_simple_graph(drawing_b["vertex_count"], drawing_b["bare_edges"])["edges"]
    )
    compact, _blocks = _compact(canonical)
    rows = canonical_law["quotient"]["rows"]

    def probability(state, target):
        cell = rows[compact[state]][compact[target]]
        return _fraction(cell)

    for row in rows:
        assert sum(_fraction(cell) for cell in row) == 1
    assert probability(0, 1) == 1
    assert probability(1, 0) == Fraction(1, 4)
    assert probability(1, 0b0011) == Fraction(1, 2)
    assert probability(1, 0b0101) == Fraction(1, 4)
    assert probability(0b0011, 1) == Fraction(1, 2)
    assert probability(0b0011, 0b0111) == Fraction(1, 2)
    assert probability(0b0101, 1) == Fraction(1, 2)
    assert probability(0b0101, 0b0111) == Fraction(1, 2)
    assert probability(0b0111, 0b0011) == Fraction(1, 2)
    assert probability(0b0111, 0b0101) == Fraction(1, 4)
    assert probability(0b0111, 0b1111) == Fraction(1, 4)
    assert probability(0b1111, 0b0111) == 1


def test_carrier_orbit_follows_baseline_symmetry_and_not_a_broken_law():
    assert carrier_orbit(4, CYCLE4)["automorphism_count"] == 8
    assert carrier_orbit(5, PATH4)["automorphism_count"] == 2
    assert carrier_orbit(3, TRIANGLE)["automorphism_count"] == 6
    assert apply_again(carrier_orbit(4, CYCLE4))["output_type"] == "undefined"
    for n, edges in ((4, CYCLE4), (5, PATH4), (4, CHAIN), (3, TRIANGLE), (4, STAR)):
        law = _law(n, edges, present_carrier_orbit_labels(n, edges))
        assert law["exact"] is True
        assert law["new_state"] is False
        assert law["quotient"]["defined"] is True
    forward = present_carrier_orbit_labels(5, PATH4)
    backward = present_carrier_orbit_labels(5, list(reversed(PATH4)))
    assert forward[1]["representative_edges"] == backward[1 << 3]["representative_edges"]
    assert forward[1]["representative_edges"] != forward[1 << 1]["representative_edges"]
    end = present_canonical_line_graph_labels(PATH4)
    assert end[1] == end[1 << 1]
    chain_indexed = present_line_graph_labels(CHAIN)
    chain_canonical = present_canonical_line_graph_labels(CHAIN)
    chain_orbits = present_carrier_orbit_labels(4, CHAIN)
    assert _same_partition(chain_indexed, chain_canonical)
    assert not _same_partition(chain_canonical, chain_orbits)
    assert _law(4, CHAIN, chain_orbits)["n_distinct_labels"] == 6
    path_indexed = present_line_graph_labels(PATH4)
    path_canonical = present_canonical_line_graph_labels(PATH4)
    path_orbits = present_carrier_orbit_labels(5, PATH4)
    path_degrees = present_degree_labels(5, PATH4)
    assert _same_partition(path_canonical, path_degrees)
    assert not _same_partition(path_indexed, path_canonical)
    assert not _same_partition(path_orbits, path_canonical)
    assert _law(5, PATH4, path_indexed)["defect_l1"] == Fraction(1, 3)
    assert _law(5, PATH4, path_canonical)["defect_l1"] == Fraction(1, 3)
    assert _law(5, PATH4, path_indexed)["n_distinct_labels"] == 8
    assert _law(5, PATH4, path_canonical)["n_distinct_labels"] == 7
    assert _law(5, PATH4, path_orbits)["n_distinct_labels"] == 10
    for edges in (TRIANGLE, STAR):
        n = 3 if edges is TRIANGLE else 4
        maps = [
            present_line_graph_labels(edges),
            present_canonical_line_graph_labels(edges),
            present_carrier_orbit_labels(n, edges),
            present_degree_labels(n, edges),
            present_edge_count_labels(edges),
        ]
        for other in maps[1:]:
            assert _same_partition(maps[0], other)
    broken = [{
        "effect": "multiply",
        "factor": 3,
        "event": [0, 1],
        "action": "either",
        "when": {"edge": [1, 2], "polarity": "present"},
    }]
    broken_law = _law(4, CYCLE4, present_carrier_orbit_labels(4, CYCLE4), broken)
    assert broken_law["exact"] is False
    assert broken_law["n_distinct_labels"] == 6
    assert broken_law["defect_l1"] == Fraction(11, 24)
    assert broken_law["quotient"]["rows"] is None


def test_a_fixed_cover_is_not_a_new_state_and_not_a_line_graph():
    partition = [PATH4[0:2], PATH4[2:4]]
    overlap = [PATH4[0:3], PATH4[1:4]]
    record = fixed_cover(PATH4, overlap)
    assert record["new_state"] is False
    assert record["dynamics"] == "none"
    assert apply_again(record)["output_type"] == "undefined"
    with pytest.raises(ValueError, match="not a carrier edge"):
        cover_count_labels(PATH4, [[[0, 1], [5, 6]]])
    with pytest.raises(ValueError, match="duplicate"):
        cover_count_labels(PATH4, [[[0, 1], [0, 1]]])
    only = {name: 1 << bit for bit, name in enumerate(("e0", "e1", "e2", "e3"))}
    part = cover_count_labels(PATH4, partition)
    over = cover_count_labels(PATH4, overlap)
    assert part[only["e0"]] == part[only["e1"]]
    assert part[only["e1"]] != part[only["e2"]]
    assert over[only["e0"]] != over[only["e1"]]
    assert over[only["e1"]] == over[only["e2"]]
    bare = active_intersection_labels(PATH4, overlap)
    labelled = labelled_active_block_labels(PATH4, overlap)
    assert bare[only["e0"]] == bare[only["e3"]]
    assert labelled[only["e0"]] != labelled[only["e3"]]
    both = only["e0"] | only["e3"]
    # The partition blocks share a vertex and no edge. Both being active
    # leaves the intersection graph edgeless. The overlapping blocks share
    # edges, so the same present pair puts an edge in their active graph.
    part_bare = active_intersection_labels(PATH4, partition)
    assert part_bare[both]["vertices"] == 2
    assert part_bare[both]["edges"] == []
    assert bare[both]["edges"] == [[0, 1]]
    part_law = _law(5, PATH4, part)
    over_law = _law(5, PATH4, over)
    assert part_law["exact"] is True
    assert part_law["new_state"] is False
    assert part_law["n_distinct_labels"] == 9
    assert part_law["quotient"]["defined"] is True
    assert over_law["exact"] is False
    assert over_law["defect_l1"] == 1
    assert over_law["n_distinct_labels"] == 10
    broken = [{
        "effect": "multiply",
        "factor": 3,
        "event": [0, 1],
        "action": "either",
        "when": {"edge": [1, 2], "polarity": "present"},
    }]
    broken_part = _law(5, PATH4, part, broken)
    assert broken_part["exact"] is False
    assert broken_part["defect_l1"] == Fraction(1, 4)
    stored = execute_composition_observation({
        "id": "fixture-cover-count",
        "round_id": "fixture",
        "type": "composition_observation",
        "n": 5,
        "carrier": {"kind": "listed", "edges": PATH4},
        "constraints": [],
        "baseline": 1,
        "observation": "cover_count",
        "cover": partition,
    })
    assert stored["cover"] == partition
    assert stored["new_state"] is False
    assert stored["exact"] is True
    with pytest.raises(ValueError, match="requires a cover"):
        execute_composition_observation({
            "id": "fixture-cover-missing",
            "type": "composition_observation",
            "n": 5,
            "carrier": {"kind": "listed", "edges": PATH4},
            "constraints": [],
            "observation": "cover_count",
        })
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (root / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (root / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L19"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L19"]["methods"]
    assert coverage["COV-COVER-OBSERVATION"]["status"] == "open"
    note = (root / "docs" / "cover-observations.md").read_text(encoding="utf-8")
    assert "No scientific cell is attached to this note." in note


def test_representation_records_stay_fixtures():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (root / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    equivalences = {
        json.loads(line)["equivalence_id"]: json.loads(line)
        for line in (root / "atlas" / "equivalences.jsonl").read_text(encoding="utf-8").splitlines()
    }
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (root / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L18"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L18"]["methods"]
    assert equivalences["EQ-022"]["status"] == "method"
    assert equivalences["EQ-023"]["status"] == "method"
    assert "constrained" in equivalences["EQ-023"]["not_claimed"]
    assert coverage["COV-REPRESENTATIONS"]["status"] == "open"
    note = (root / "docs" / "representations.md").read_text(encoding="utf-8")
    assert "No scientific cell is attached to this note." in note
    assert "8 vertices" in note


def test_position_index_follows_edge_positions_and_not_node_names():
    path = [[0, 1], [1, 2], [2, 3]]
    renamed = [[1, 2], [2, 3], [3, 4]]
    reordered = [[1, 2], [0, 1], [2, 3]]
    assert present_line_graph_labels(path) == present_line_graph_labels(renamed)
    assert present_line_graph_labels(path) != present_line_graph_labels(reordered)
    assert labelled_line_graph(path)["vertices"] != labelled_line_graph(renamed)["vertices"]
    full = (1 << 3) - 1
    assert present_line_graph_labels(path)[full]["edges"] == [[0, 1], [1, 2]]
    assert present_line_graph_labels(reordered)[full]["edges"] == [[0, 1], [0, 2]]
    automorphisms = carrier_automorphisms(4, path)
    assert automorphisms == [(0, 1, 2, 3), (3, 2, 1, 0)]
    induced = []
    for perm in automorphisms:
        image = []
        for left, right in path:
            a, b = perm[left], perm[right]
            image.append((a, b) if a < b else (b, a))
        induced.append(tuple(image))
    assert ((0, 1), (1, 2), (2, 3)) in induced
    assert ((2, 3), (1, 2), (0, 1)) in induced
    assert ((0, 1), (2, 3), (1, 2)) not in induced


def test_canonicalisation_is_not_line_graph_iteration():
    path = [[0, 1], [1, 2], [2, 3]]
    certificate = canonical_simple_graph(4, path)
    assert certificate["edges"] == [[0, 1], [0, 2], [1, 3]]
    assert certificate["edges"] != path
    again = apply_again(certificate)
    assert again["edges"] == certificate["edges"]
    assert again["second_application"] == "defined_and_idempotent"
    assert again["applied_to"] == "canonical_simple_graph"
    built = line_graph(certificate["edges"])
    assert built["operator"] == "line_graph"
    assert built["vertex_count"] == 3
    assert built["bare_edges"] == [[0, 1], [0, 2]]
    assert built["bare_edges"] != certificate["edges"]
    steps = iterate_line_graph(certificate["edges"], 2)
    assert steps[0]["bare_edges"] == certificate["edges"]
    assert steps[1]["bare_edges"] == [[0, 1], [0, 2]]
    assert steps[2]["bare_edges"] == [[0, 1]]
    assert steps[2]["vertex_count"] == 2
    assert certificate["dynamics"] == "none"
    assert certificate["new_state"] is False


def test_block_family_report_separates_covers_from_partial_families():
    partition = [PATH4[0:2], PATH4[2:4]]
    overlap = [PATH4[0:3], PATH4[1:4]]
    part = block_family_report(PATH4, partition)
    over = block_family_report(PATH4, overlap)
    assert part["full_cover"] is True
    assert part["partition"] is True
    assert part["partial_family"] is False
    assert part["overlapping"] is False
    assert part["nested"] is False
    assert part["new_state"] is False
    assert part["dynamics"] == "none"
    assert over["full_cover"] is True
    assert over["overlapping"] is True
    assert over["partition"] is False
    assert over["nested"] is False
    assert over["potential_overlap_pairs"] == [[0, 1]]
    copies = block_family_report(PATH4, [PATH4, list(PATH4)])
    assert copies["full_cover"] is True
    assert copies["overlapping"] is True
    assert copies["nested"] is False
    assert copies["partition"] is False
    omitted = block_family_report(TRIANGLE, [TRIANGLE[0:1], TRIANGLE[1:2]])
    assert omitted["partial_family"] is True
    assert omitted["full_cover"] is False
    assert omitted["missed_edges"] == [[0, 2]]
    nested = block_family_report(CYCLE4, [list(CYCLE4), [CYCLE4[0], CYCLE4[2]]])
    assert nested["full_cover"] is True
    assert nested["nested"] is True
    assert nested["overlapping"] is True
    assert nested["partition"] is False
    empty_carrier = block_family_report([], [])
    assert empty_carrier["full_cover"] is True
    assert empty_carrier["partition"] is True
    assert empty_carrier["partial_family"] is False
    empty_family = block_family_report(PATH4, [])
    assert empty_family["partial_family"] is True
    assert empty_family["full_cover"] is False
    assert empty_family["partition"] is False
    with_empty = block_family_report(PATH4, [PATH4[0:2], PATH4[2:4], []])
    assert with_empty["full_cover"] is True
    assert with_empty["empty_block"] is True
    assert with_empty["partition"] is False
    with pytest.raises(ValueError, match="not a carrier edge"):
        block_family_report(PATH4, [[[0, 1], [5, 6]]])
    with pytest.raises(ValueError, match="duplicate"):
        block_family_report(PATH4, [[[0, 1], [0, 1]]])
    with pytest.raises(ValueError, match="a cover must be a list of blocks"):
        block_family_report(PATH4, None)
    # Both end edges are present and the two shared edges are absent.
    # The active-block map still draws the fixed intersection.
    both_ends = 1 | (1 << 3)
    bare = active_intersection_labels(PATH4, overlap)
    assert bare[both_ends]["edges"] == [[0, 1]]
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (root / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (root / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
    }
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (root / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L20"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L20"]["methods"]
    assert "successive_observations" in ideas["IDEA-L20"]["feasibility"]
    assert "not a frozen cell" in ideas["IDEA-L20"]["feasibility"]
    assert ideas["IDEA-L21"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L21"]["methods"]
    assert ideas["IDEA-L22"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L22"]["methods"]
    assert ideas["IDEA-L23"]["status"] == "open"
    assert "not a frozen cell" in ideas["IDEA-L23"]["methods"]
    for coverage_id in (
        "COV-SUCCESSIVE-QUOTIENT",
        "COV-REALISED-OVERLAP",
        "COV-HIGHER-ORDER-STATE",
        "COV-DYNAMICAL-PROPAGATION",
    ):
        assert coverage[coverage_id]["status"] == "open"
    assert "successive_observations" in coverage["COV-SUCCESSIVE-QUOTIENT"]["method"]
    assert "not yet compared" not in coverage["COV-SUCCESSIVE-QUOTIENT"]["notes"]
    assert "EQ-026" in coverage["COV-SUCCESSIVE-QUOTIENT"]["notes"]
    for question_id in ("ATLAS-Q13", "ATLAS-Q14", "ATLAS-Q15"):
        assert questions[question_id]["status"] == "open"
    representations = (root / "docs" / "representations.md").read_text(encoding="utf-8")
    assert "Five operations" in representations
    assert "Canonicalisation is not iteration" in representations
    cover = (root / "docs" / "cover-observations.md").read_text(encoding="utf-8")
    assert "No scientific cell is attached to this note." in cover
    assert "partial family" in cover
    assert "realised overlap" in cover


def _parity_labels(edges):
    return [{"parity": label["present_edges"] & 1} for label in present_edge_count_labels(edges)]


def _constant_labels(edges):
    return [{"trivial": True} for _label in present_edge_count_labels(edges)]


def _empty_labels(edges):
    return [
        {"empty": label["present_edges"] == 0}
        for label in present_edge_count_labels(edges)
    ]


def test_successive_quotients_separate_exact_undefined_and_untyped_maps():
    import numpy as np

    weights = compile_weight_table(4, {"kind": "listed", "edges": CYCLE4}, [])
    counts = present_edge_count_labels(CYCLE4)
    parity = _parity_labels(CYCLE4)
    constant = _constant_labels(CYCLE4)
    for state in range(weights.shape[0]):
        total = int(weights[state].sum())
        assert total > 0
        stayed = 0
        for edge, weight in enumerate(weights[state]):
            weight = int(weight)
            if weight == 0:
                continue
            nxt = state ^ (1 << edge)
            if (nxt.bit_count() & 1) == (state.bit_count() & 1):
                stayed += weight
        assert stayed == 0
    chain = successive_observations(weights, [counts, parity, constant])
    assert chain["new_state"] is False
    assert chain["exact_prefix"] == 3
    assert chain["agreement"] == "exact"
    assert chain["kernels_agree"] is True
    assert chain["conditional_exactness"] == "not_computed"
    assert chain["history_dependent"] == "not_computed"
    assert [stage["exact"] for stage in chain["stages"]] == [True, True, True]
    assert chain["label_counts"] == [5, 2, 1]
    parity_rows = chain["stages"][1]["quotient_rows"]
    assert _fraction(parity_rows[0][0]) == 0
    assert _fraction(parity_rows[0][1]) == 1
    assert _fraction(parity_rows[1][0]) == 1
    assert _fraction(parity_rows[1][1]) == 0
    assert _fraction(chain["stages"][2]["quotient_rows"][0][0]) == 1
    for stage in chain["stages"]:
        for row in stage["quotient_rows"]:
            assert sum(_fraction(cell) for cell in row) == 1
    broken = successive_observations(weights, [counts, parity, counts])
    assert broken["exact_prefix"] == 2
    assert broken["agreement"] == "exact"
    assert broken["stages"][2]["typed"] is False
    assert broken["stages"][2]["exact"] is None
    assert broken["stages"][2]["defect_l1"] is None
    assert broken["stages"][2]["quotient_rows"] is None
    degrees = present_degree_labels(4, CYCLE4)
    untyped = successive_observations(weights, [counts, degrees])
    assert untyped["stages"][1]["typed"] is False
    assert untyped["stages"][1]["factors_through_previous"] is False
    assert untyped["stages"][1]["exact"] is None
    assert untyped["direct"][1]["exact"] is True
    assert untyped["agreement"] == "undefined"
    assert untyped["kernels_agree"] is None
    indexed = present_line_graph_labels(CYCLE4)
    intermediate = successive_observations(weights, [indexed, counts])
    assert intermediate["stages"][0]["exact"] is False
    assert intermediate["stages"][0]["defect_l1"] == Fraction(1, 2)
    assert intermediate["stages"][0]["quotient_rows"] is None
    assert intermediate["stages"][1]["typed"] is True
    assert intermediate["stages"][1]["exact"] is None
    assert intermediate["stages"][1]["defect_l1"] is None
    assert intermediate["stages"][1]["quotient_rows"] is None
    assert intermediate["stages"][1]["undefined_reason"] == "the previous partition is not strongly lumpable"
    assert intermediate["direct"][1]["exact"] is True
    assert intermediate["agreement"] == "undefined"
    empty = successive_observations(weights, [counts, _empty_labels(CYCLE4)])
    assert empty["stages"][0]["exact"] is True
    assert empty["stages"][1]["typed"] is True
    assert empty["stages"][1]["exact"] is False
    assert empty["stages"][1]["defect_l1"] > 0
    assert empty["stages"][1]["quotient_rows"] is None
    assert empty["direct"][1]["exact"] is False
    assert empty["direct"][1]["quotient_rows"] is None
    both = successive_observations(weights, [indexed, _empty_labels(CYCLE4)])
    assert both["stages"][0]["exact"] is False
    assert both["stages"][1]["quotient_rows"] is None
    assert both["direct"][1]["exact"] is False
    halted = np.ones((4, 2), dtype=int)
    halted[0] = 0
    disjoint = [[0, 1], [2, 3]]
    halted_chain = successive_observations(
        halted,
        [present_edge_count_labels(disjoint), _parity_labels(disjoint)],
    )
    assert halted_chain["stages"][0]["exact"] is True
    assert halted_chain["stages"][1]["exact"] is False
    assert halted_chain["stages"][1]["quotient_rows"] is None
    assert halted_chain["direct"][1]["quotient_rows"] is None
    baseline = compile_weight_table(4, {"kind": "listed", "edges": disjoint}, [], baseline=5)
    again = successive_observations(
        baseline,
        [present_edge_count_labels(disjoint), _parity_labels(disjoint)],
    )
    assert again["agreement"] == "exact"
    assert again["label_counts"] == [3, 2]
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    equivalences = {
        json.loads(line)["equivalence_id"]: json.loads(line)
        for line in (root / "atlas" / "equivalences.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert equivalences["EQ-026"]["status"] == "method"
    assert "zero" in equivalences["EQ-026"]["not_claimed"]
    assert "not a new theorem" in (root / "docs" / "composition-operators.md").read_text(encoding="utf-8")


def test_realised_overlap_needs_a_present_shared_edge():
    overlap = [PATH4[0:3], PATH4[1:4]]
    partition = [PATH4[0:2], PATH4[2:4]]
    both_ends = 1 | (1 << 3)
    potential = active_intersection_labels(PATH4, overlap)
    realised = realised_intersection_labels(PATH4, overlap)
    assert potential[both_ends]["edges"] == [[0, 1]]
    assert realised[both_ends] == {"vertices": 2, "edges": []}
    labelled_potential = labelled_active_block_labels(PATH4, overlap)
    labelled_realised = labelled_realised_block_labels(PATH4, overlap)
    assert labelled_potential[both_ends]["adjacent"] == [[0, 1]]
    assert labelled_realised[both_ends]["adjacent"] == []
    one_shared = 1 << 1
    two_shared = (1 << 1) | (1 << 2)
    assert realised[one_shared]["edges"] == [[0, 1]]
    assert realised[two_shared]["edges"] == [[0, 1]]
    counts = realised_overlap_count_labels(PATH4, overlap)
    assert counts[one_shared]["shared"] == [1]
    assert counts[two_shared]["shared"] == [2]
    assert realised_intersection_labels(PATH4, partition) == active_intersection_labels(PATH4, partition)
    opposite = [[[0, 1], [2, 3]], [[1, 2], [0, 3]]]
    assert realised_intersection_labels(CYCLE4, opposite) == active_intersection_labels(CYCLE4, opposite)
    assert labelled_realised_block_labels(CYCLE4, opposite) == labelled_active_block_labels(CYCLE4, opposite)
    constant = realised_overlap_count_labels(CYCLE4, opposite)
    assert constant == [{"shared": [0]} for _state in range(1 << 4)]
    omitted = [TRIANGLE[0:1], TRIANGLE[1:2]]
    assert block_family_report(TRIANGLE, omitted)["partial_family"] is True
    assert len(labelled_realised_block_labels(TRIANGLE, omitted)) == 1 << 3
    with pytest.raises(ValueError, match="not a carrier edge"):
        realised_intersection_labels(PATH4, [[[0, 1], [5, 6]]])
    with pytest.raises(ValueError, match="duplicate"):
        labelled_realised_block_labels(PATH4, [[[0, 1], [0, 1]]])
    triangle_overlap = [TRIANGLE[0:2], [TRIANGLE[1], TRIANGLE[2]]]
    base = _law(3, TRIANGLE, labelled_realised_block_labels(TRIANGLE, triangle_overlap))
    assert base["exact"] is False
    assert base["n_distinct_labels"] == 5
    assert base["defect_l1"] == Fraction(1, 2)
    assert base["quotient"]["rows"] is None
    assert base["new_state"] is False
    multiply = [{
        "effect": "multiply",
        "factor": 3,
        "event": [0, 1],
        "action": "either",
        "when": {"edge": [1, 2], "polarity": "present"},
    }]
    constrained = _law(
        3, TRIANGLE, labelled_realised_block_labels(TRIANGLE, triangle_overlap), multiply
    )
    assert constrained["n_distinct_labels"] == 5
    assert constrained["defect_l1"] == Fraction(3, 10)
    assert constrained["quotient"]["rows"] is None
    for constraints in ([], multiply):
        count_law = _law(
            3, TRIANGLE, realised_overlap_count_labels(TRIANGLE, triangle_overlap), constraints
        )
        assert count_law["exact"] is True
        assert count_law["n_distinct_labels"] == 2
        assert count_law["quotient"]["defined"] is True
    path_count = _law(5, PATH4, realised_overlap_count_labels(PATH4, overlap))
    assert path_count["exact"] is True
    assert path_count["n_distinct_labels"] == 3
    path_constrained = _law(5, PATH4, realised_overlap_count_labels(PATH4, overlap), multiply)
    assert path_constrained["exact"] is False
    assert path_constrained["defect_l1"] == Fraction(1, 6)
    assert path_constrained["quotient"]["rows"] is None
    stored = execute_composition_observation({
        "id": "fixture-realised",
        "round_id": "fixture",
        "type": "composition_observation",
        "n": 3,
        "carrier": {"kind": "listed", "edges": TRIANGLE},
        "constraints": [],
        "baseline": 1,
        "observation": "labelled_realised_blocks",
        "cover": triangle_overlap,
    })
    assert stored["cover"] == triangle_overlap
    assert stored["new_state"] is False
    assert stored["further_label"] == "undefined"
    assert stored["exact"] is False
    with pytest.raises(ValueError, match="requires a cover"):
        execute_composition_observation({
            "id": "fixture-realised-missing",
            "type": "composition_observation",
            "n": 3,
            "carrier": {"kind": "listed", "edges": TRIANGLE},
            "constraints": [],
            "observation": "realised_overlap_count",
        })
