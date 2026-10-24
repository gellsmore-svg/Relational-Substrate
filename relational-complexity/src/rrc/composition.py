"""Typed composition operators on small relational objects.

These functions do not compile weights and do not change ``ENGINE_VERSION``.
A graph-valued output is not a Markov chain. A second application is
recorded only when the output is an object the same operator accepts.
"""

from __future__ import annotations

import json
from itertools import combinations

from rrc.constraints import present_graph
from rrc.model import lumpability


MAX_NERVE_BLOCKS = 12


def _endpoint(value) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("an endpoint must be an integer")
    if value < 0:
        raise ValueError("an endpoint must be non-negative")
    return value


def simple_edges(edges) -> list[tuple[int, int]]:
    """Undirected edges in input order. Endpoint order inside an edge is normalised."""
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    ordered = []
    seen = set()
    for raw in edges:
        if not isinstance(raw, (list, tuple)) or len(raw) != 2:
            raise ValueError("an edge must be a pair")
        left = _endpoint(raw[0])
        right = _endpoint(raw[1])
        if left == right:
            raise ValueError("a loop is not a simple edge")
        edge = (left, right) if left < right else (right, left)
        if edge in seen:
            raise ValueError(f"duplicate edge {edge}")
        seen.add(edge)
        ordered.append(edge)
    return ordered


def _bare(edges: list[tuple[int, int]]) -> list[list[int]]:
    return [[left, right] for left, right in edges]


def line_graph(edges, vertex_count: int | None = None) -> dict:
    """Line graph of a simple undirected graph.

    The input edge list is the edge set. ``vertex_count``, when given, is
    the order of the input vertex set ``0 .. vertex_count-1``. Isolated
    input vertices are absent from both outputs. The bare output numbers
    line-graph vertices by input edge order and drops those labels. The
    augmented output keeps the input edges as vertex labels.
    """
    ordered = simple_edges(edges)
    isolated = None
    if vertex_count is not None:
        if isinstance(vertex_count, bool) or not isinstance(vertex_count, int) or vertex_count < 0:
            raise ValueError("vertex_count must be a non-negative integer")
        for left, right in ordered:
            if left >= vertex_count or right >= vertex_count:
                raise ValueError("an endpoint lies outside vertex_count")
        used = {node for edge in ordered for node in edge}
        isolated = vertex_count - len(used)
    nodes = [set(edge) for edge in ordered]
    bare = []
    for left in range(len(ordered)):
        for right in range(left + 1, len(ordered)):
            if nodes[left] & nodes[right]:
                bare.append((left, right))
    return {
        "operator": "line_graph",
        "input_type": "simple_undirected_graph",
        "output_type": "simple_undirected_graph",
        "new_state": False,
        "dynamics": "none",
        "second_application": "defined",
        "vertex_count": len(ordered),
        "edge_count": len(bare),
        "bare_edges": _bare(bare),
        "vertices": _bare(ordered),
        "input_isolated_vertices": isolated,
    }


def iterate_line_graph(edges, steps: int, vertex_count: int | None = None) -> list[dict]:
    """Apply the bare line-graph operator ``steps`` times after the input.

    Step 0 is the input edge list. Later steps use the previous bare edge
    list. Isolated vertices of an intermediate graph are not edges, so they
    are not vertices of the next line graph. That loss is the operator.
    """
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    current = simple_edges(edges)
    if vertex_count is not None:
        line_graph(current, vertex_count)
    records = [
        {
            "operator": "input_graph",
            "step": 0,
            "vertex_count": vertex_count,
            "edge_count": len(current),
            "bare_edges": _bare(current),
            "second_application": "not_applicable",
            "dynamics": "none",
            "new_state": False,
        }
    ]
    for step in range(1, steps + 1):
        record = line_graph(current)
        record["step"] = step
        records.append(record)
        current = simple_edges(record["bare_edges"])
    return records


def _blocks(blocks) -> list[tuple]:
    if not isinstance(blocks, list):
        raise ValueError("a cover must be a list of blocks")
    parsed = []
    for raw in blocks:
        if not isinstance(raw, list):
            raise ValueError("a block must be a list")
        elements = []
        for element in raw:
            if isinstance(element, list):
                raise ValueError("a block element must not be a list")
            if isinstance(element, bool) or not isinstance(element, (int, str, tuple)):
                raise ValueError("a block element must be an int, a string, or a tuple")
            elements.append(element)
        parsed.append(tuple(elements))
    return parsed


def intersection_graph(blocks) -> dict:
    """One vertex per block. An edge when the blocks have a common element.

    The bare output is that graph. The augmented output also stores the
    blocks. A second application is undefined: the output is not a cover.
    """
    parsed = _blocks(blocks)
    sets = [set(block) for block in parsed]
    bare = []
    for left in range(len(sets)):
        for right in range(left + 1, len(sets)):
            if sets[left] & sets[right]:
                bare.append((left, right))
    return {
        "operator": "intersection_graph",
        "input_type": "ordered_cover",
        "output_type": "simple_undirected_graph",
        "new_state": False,
        "dynamics": "none",
        "second_application": "undefined",
        "undefined_reason": "the output is a graph, not a cover",
        "vertex_count": len(parsed),
        "edge_count": len(bare),
        "bare_edges": _bare(bare),
        "blocks": [list(block) for block in parsed],
    }


def nerve(blocks, max_blocks: int = MAX_NERVE_BLOCKS) -> dict:
    """Nerve of an ordered cover: faces are block-index sets with nonempty common intersection.

    The 1-skeleton is the intersection graph, including isolated block
    vertices that the edge list does not show. A second application is
    undefined: the output is a simplicial complex, not a cover.
    """
    if isinstance(max_blocks, bool) or not isinstance(max_blocks, int) or max_blocks < 1:
        raise ValueError("max_blocks must be a positive integer")
    parsed = _blocks(blocks)
    if len(parsed) > max_blocks:
        raise ValueError(
            f"a nerve of {len(parsed)} blocks enumerates 2^{len(parsed)} subcollections; "
            f"the cap is {max_blocks}"
        )
    sets = [set(block) for block in parsed]
    faces = []
    for width in range(1, len(sets) + 1):
        for combo in combinations(range(len(sets)), width):
            common = sets[combo[0]].copy()
            for index in combo[1:]:
                common &= sets[index]
            if common:
                faces.append(list(combo))
    skeleton = [face for face in faces if len(face) == 2]
    return {
        "operator": "nerve",
        "input_type": "ordered_cover",
        "output_type": "simplicial_complex",
        "new_state": False,
        "dynamics": "none",
        "second_application": "undefined",
        "undefined_reason": "the output is a simplicial complex, not a cover",
        "vertex_count": len(parsed),
        "faces": faces,
        "max_face_vertices": max((len(face) for face in faces), default=0),
        "bare_edges": skeleton,
        "blocks": [list(block) for block in parsed],
    }


def apply_again(result: dict) -> dict:
    """Apply the same operator to its output, or record that this is undefined."""
    operator = result.get("operator")
    if operator == "line_graph":
        nxt = line_graph(result["bare_edges"])
        nxt["applied_to"] = "bare_line_graph"
        return nxt
    if operator in ("intersection_graph", "nerve"):
        return {
            "operator": operator,
            "input_type": result["output_type"],
            "output_type": "undefined",
            "new_state": False,
            "dynamics": "none",
            "second_application": "undefined",
            "undefined_reason": result["undefined_reason"],
        }
    raise ValueError(f"unknown operator result {operator}")


def line_of_intersection(blocks) -> dict:
    """``line_graph`` applied to the bare intersection graph.

    This composes two operators. It is not a second application of the
    cover operator, and it does not make the cover operator recursive.
    """
    cover = intersection_graph(blocks)
    graph = line_graph(cover["bare_edges"])
    graph["applied_to"] = "bare_intersection_graph"
    graph["composition"] = "line_graph_after_intersection_graph"
    return graph


def intersection_representation(vertex_count: int, edges) -> list[list]:
    """One standard cover whose intersection graph is the given simple graph.

    Block ``i`` contains the indices of edges incident to ``i``, plus a
    private element. This is an established representation, not a new theorem.
    """
    ordered = simple_edges(edges)
    if isinstance(vertex_count, bool) or not isinstance(vertex_count, int) or vertex_count < 0:
        raise ValueError("vertex_count must be a non-negative integer")
    for left, right in ordered:
        if left >= vertex_count or right >= vertex_count:
            raise ValueError("an endpoint lies outside vertex_count")
    blocks = []
    for vertex in range(vertex_count):
        incident = [index for index, edge in enumerate(ordered) if vertex in edge]
        blocks.append(incident + [("private", vertex)])
    return blocks


def _compact(labels: list) -> tuple[list[int], int]:
    index = {}
    compact = []
    for label in labels:
        key = json.dumps(label, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if key not in index:
            index[key] = len(index)
        compact.append(index[key])
    return compact, len(index)


def present_line_graph_labels(edges) -> list[dict]:
    """Bare line graph of the edges present in each carrier state.

    The label keeps the line-graph vertex count. An edge list alone would
    identify every edgeless present graph.
    """
    ordered = simple_edges(edges)
    labels = []
    width = len(ordered)
    for state in range(1 << width):
        present = [ordered[bit] for bit in range(width) if (state >> bit) & 1]
        graph = line_graph([list(edge) for edge in present])
        labels.append({"edges": graph["bare_edges"], "vertices": graph["vertex_count"]})
    return labels


def present_edge_count_labels(edges) -> list[dict]:
    ordered = simple_edges(edges)
    return [{"present_edges": (state.bit_count())} for state in range(1 << len(ordered))]


def present_degree_labels(n: int, edges) -> list[dict]:
    ordered = simple_edges(edges)
    return [
        {"degree_sequence": present_graph(n, ordered, state)["degree_sequence"]}
        for state in range(1 << len(ordered))
    ]


def observation_law(weights, labels: list) -> dict:
    """Strong lumpability of a label map under the weight table's toggle law.

    ``lumpability`` uses the integer weights directly. A zero row is a
    self-loop. A positive row is one toggle, with probability proportional
    to the weight. The label map adds no state. ``exact`` is strong
    lumpability of this observation. It is not an approximate closure.
    """
    if len(labels) != int(weights.shape[0]):
        raise ValueError("labels must cover every state")
    compact, distinct = _compact(labels)
    report = lumpability(weights, compact)
    return {
        "exact": report["exact"],
        "defect_l1": report["defect_l1"],
        "n_blocks": report["n_blocks"],
        "n_states": len(labels),
        "n_distinct_labels": distinct,
        "injective": distinct == len(labels),
        "max_block_size": report["max_block_size"],
        "new_state": False,
        "witness": report["witness"],
    }
