"""Typed composition operators. Validation fixtures, not a scientific round."""

from __future__ import annotations

from fractions import Fraction

import pytest

from rrc.composition import (
    apply_again,
    intersection_graph,
    intersection_representation,
    iterate_line_graph,
    line_graph,
    line_of_intersection,
    nerve,
    observation_law,
    present_degree_labels,
    present_edge_count_labels,
    present_line_graph_labels,
)
from rrc.constraints import compile_weight_table


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
