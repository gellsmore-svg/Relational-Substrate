"""Typed composition operators on small relational objects.

These functions do not compile weights and do not change ``ENGINE_VERSION``.
A graph-valued output is not a Markov chain. A second application is
recorded only when the output is an object the same operator accepts.
"""

from __future__ import annotations

import json
from itertools import combinations, permutations

from rrc.constraints import present_graph
from rrc.model import lumpability, quotient_kernel


MAX_NERVE_BLOCKS = 12
# 8! = 40320. The search is exhaustive relabelling. A larger graph is refused.
MAX_CANONICAL_VERTICES = 8


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
    if operator == "canonical_simple_graph":
        nxt = canonical_simple_graph(result["vertex_count"], result["edges"])
        nxt["applied_to"] = "canonical_simple_graph"
        return nxt
    if operator in (
        "intersection_graph",
        "nerve",
        "labelled_line_graph",
        "carrier_orbit",
        "fixed_cover",
    ):
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


def _bounded_order(vertex_count) -> int:
    if isinstance(vertex_count, bool) or not isinstance(vertex_count, int) or vertex_count < 0:
        raise ValueError("vertex_count must be a non-negative integer")
    if vertex_count > MAX_CANONICAL_VERTICES:
        raise ValueError(
            f"canonical form is refused above the cap of {MAX_CANONICAL_VERTICES} vertices"
        )
    return vertex_count


def _placed_edges(vertex_count: int, edges) -> list[tuple[int, int]]:
    ordered = simple_edges(edges)
    for left, right in ordered:
        if left >= vertex_count or right >= vertex_count:
            raise ValueError("an endpoint lies outside vertex_count")
    return ordered


def canonical_simple_graph(vertex_count, edges) -> dict:
    """Lex-minimum edge list over every numbering of the vertices.

    ``vertex_count`` retains isolated vertices. Two orders are different
    graphs. The search is every permutation. Above the cap it is refused,
    and the refusal is not a canonical form. A second application returns
    the same edge list. That is idempotence, not a further level.
    """
    order = _bounded_order(vertex_count)
    placed = _placed_edges(order, edges)
    best: tuple[tuple[int, int], ...] | None = None
    for perm in permutations(range(order)):
        image = tuple(sorted(
            (perm[left], perm[right]) if perm[left] < perm[right] else (perm[right], perm[left])
            for left, right in placed
        ))
        if best is None or image < best:
            best = image
    return {
        "operator": "canonical_simple_graph",
        "representation": "R3_unlabelled_isomorphism",
        "input_type": "simple_undirected_graph",
        "output_type": "canonical_simple_graph",
        "new_state": False,
        "dynamics": "none",
        "second_application": "defined_and_idempotent",
        "vertex_count": order,
        "edges": _bare(list(best or ())),
        "method": "exhaustive_lex_min_relabeling",
        "cap": MAX_CANONICAL_VERTICES,
        "isolated_vertices_retained": True,
        "undefined_reason": None,
    }


def relabeling_exists(vertex_count, left_edges, right_edges) -> bool:
    """Whether some vertex numbering carries the left edge set onto the right.

    Degree pruning and backtracking are a separate search from the lex-min
    certificate. The two agree on the graphs the tests enumerate. Above the
    cap the search is refused.
    """
    order = _bounded_order(vertex_count)
    left = set(_placed_edges(order, left_edges))
    right = set(_placed_edges(order, right_edges))
    if len(left) != len(right):
        return False
    left_degree = [0] * order
    right_degree = [0] * order
    for start, end in left:
        left_degree[start] += 1
        left_degree[end] += 1
    for start, end in right:
        right_degree[start] += 1
        right_degree[end] += 1
    if sorted(left_degree) != sorted(right_degree):
        return False
    candidates = [
        [image for image in range(order) if right_degree[image] == left_degree[vertex]]
        for vertex in range(order)
    ]
    sequence = sorted(range(order), key=lambda vertex: -left_degree[vertex])
    used = [False] * order
    assignment = [-1] * order

    def agrees(vertex: int, image: int) -> bool:
        for earlier in range(order):
            if assignment[earlier] < 0:
                continue
            left_edge = (earlier, vertex) if earlier < vertex else (vertex, earlier)
            mapped_left = assignment[earlier]
            right_edge = (mapped_left, image) if mapped_left < image else (image, mapped_left)
            if (left_edge in left) != (right_edge in right):
                return False
        return True

    def search(position: int) -> bool:
        if position == order:
            return True
        vertex = sequence[position]
        for image in candidates[vertex]:
            if used[image] or not agrees(vertex, image):
                continue
            used[image] = True
            assignment[vertex] = image
            if search(position + 1):
                return True
            assignment[vertex] = -1
            used[image] = False
        return False

    return search(0)


def labelled_line_graph(edges) -> dict:
    """Line graph whose vertices are the original edges.

    The vertex list is sorted, so the carrier edge order does not change
    the label. A node permutation does. The output is not a simple graph
    on integer endpoints, so ``line_graph`` does not accept it. No encoding
    is added to make a second application possible.
    """
    ordered = simple_edges(edges)
    vertices = sorted(_bare(ordered))
    adjacent = []
    for left, right in combinations(range(len(ordered)), 2):
        if set(ordered[left]) & set(ordered[right]):
            adjacent.append(sorted([list(ordered[left]), list(ordered[right])]))
    adjacent.sort()
    return {
        "operator": "labelled_line_graph",
        "representation": "R1_relationship_labelled",
        "input_type": "simple_undirected_graph",
        "output_type": "edge_labelled_line_graph",
        "new_state": False,
        "dynamics": "none",
        "second_application": "undefined",
        "vertices": vertices,
        "adjacent": adjacent,
        "recovers_present_edges": True,
        "undefined_reason": (
            "the vertices are the original edges, and the line-graph operator "
            "accepts integer endpoints"
        ),
    }


def carrier_automorphisms(vertex_count, edges) -> list[tuple[int, ...]]:
    """Vertex permutations that preserve the carrier edge set.

    The search is exhaustive. Above the cap it is refused.
    """
    order = _bounded_order(vertex_count)
    placed = _placed_edges(order, edges)
    target = set(placed)
    found = []
    for perm in permutations(range(order)):
        image = {
            (perm[left], perm[right]) if perm[left] < perm[right] else (perm[right], perm[left])
            for left, right in target
        }
        if image == target:
            found.append(perm)
    return found


def carrier_orbit(vertex_count, edges) -> dict:
    """Type of the carrier-orbit map. No subgraph is selected here."""
    automorphisms = carrier_automorphisms(vertex_count, edges)
    return {
        "operator": "carrier_orbit",
        "representation": "R4_carrier_automorphism",
        "input_type": "subgraph_of_a_fixed_carrier",
        "output_type": "edge_subset_of_the_same_carrier",
        "new_state": False,
        "dynamics": "none",
        "second_application": "undefined",
        "automorphism_count": len(automorphisms),
        "method": "exhaustive_vertex_permutations",
        "cap": MAX_CANONICAL_VERTICES,
        "undefined_reason": (
            "the automorphism group belongs to the carrier, and a representative "
            "subgraph does not determine that carrier"
        ),
    }


def _orbit_representative(vertex_count: int, edges, present, automorphisms) -> list[list[int]]:
    ordered = _placed_edges(vertex_count, edges)
    index = {edge: bit for bit, edge in enumerate(ordered)}
    present_edges = _placed_edges(vertex_count, present)
    for edge in present_edges:
        if edge not in index:
            raise ValueError("a present edge is not a carrier edge")
    best: tuple[tuple[int, int], ...] | None = None
    for perm in automorphisms:
        image = tuple(sorted(
            (perm[left], perm[right]) if perm[left] < perm[right] else (perm[right], perm[left])
            for left, right in present_edges
        ))
        if best is None or image < best:
            best = image
    return _bare(list(best or ()))


def present_labelled_line_graph_labels(edges) -> list[dict]:
    """R1. One labelled line graph for each present subset."""
    ordered = simple_edges(edges)
    labels = []
    width = len(ordered)
    for state in range(1 << width):
        present = [list(ordered[bit]) for bit in range(width) if (state >> bit) & 1]
        graph = labelled_line_graph(present)
        labels.append({"vertices": graph["vertices"], "adjacent": graph["adjacent"]})
    return labels


def present_canonical_line_graph_labels(edges) -> list[dict]:
    """R3. Unlabelled isomorphism class of the bare line graph.

    The class keeps the line-graph vertex count, including isolated
    line-graph vertices. It does not keep the original edge names.
    """
    ordered = simple_edges(edges)
    labels = []
    width = len(ordered)
    for state in range(1 << width):
        present = [list(ordered[bit]) for bit in range(width) if (state >> bit) & 1]
        graph = line_graph(present)
        certificate = canonical_simple_graph(graph["vertex_count"], graph["bare_edges"])
        labels.append({
            "vertex_count": certificate["vertex_count"],
            "edges": certificate["edges"],
        })
    return labels


def present_carrier_orbit_labels(vertex_count: int, edges) -> list[dict]:
    """R4. Lex-min present edge set under automorphisms of the carrier.

    The minimum is the sorted edge list, so the carrier's list order does
    not choose the representative. The integer node labels do.
    """
    ordered = _placed_edges(vertex_count, edges)
    automorphisms = carrier_automorphisms(vertex_count, ordered)
    labels = []
    width = len(ordered)
    for state in range(1 << width):
        present = [list(ordered[bit]) for bit in range(width) if (state >> bit) & 1]
        labels.append({
            "representative_edges": _orbit_representative(
                vertex_count, ordered, present, automorphisms
            ),
        })
    return labels


def _carrier_blocks(edges, blocks):
    if not isinstance(blocks, list):
        raise ValueError("a cover must be a list of blocks")
    ordered = simple_edges(edges)
    index = {edge: bit for bit, edge in enumerate(ordered)}
    parsed = []
    for block in blocks:
        members = simple_edges(block)
        bits = []
        for edge in members:
            if edge not in index:
                raise ValueError("a block edge is not a carrier edge")
            bits.append(index[edge])
        parsed.append(tuple(bits))
    return ordered, parsed


def block_family_report(edges, blocks) -> dict:
    """Classify a fixed family of carrier-edge blocks.

    The union of the blocks decides a full cover against a partial family.
    Potential overlap is a nonempty intersection of those blocks. It does
    not read which edges are present. Realised overlap is a different
    condition and is not computed here. The report does not change
    ``cover_count_labels``, ``active_intersection_labels``, or
    ``labelled_active_block_labels``.
    """
    ordered, parsed = _carrier_blocks(edges, blocks)
    carrier = set(range(len(ordered)))
    sets = [set(bits) for bits in parsed]
    covered: set[int] = set()
    for bits in sets:
        covered |= bits
    missed = sorted(carrier - covered)
    empty_block = any(len(bits) == 0 for bits in sets)
    potential_pairs = [
        [left, right]
        for left, right in combinations(range(len(sets)), 2)
        if sets[left] & sets[right]
    ]
    nested = any(
        sets[left] < sets[right] or sets[right] < sets[left]
        for left, right in combinations(range(len(sets)), 2)
    )
    pairwise_disjoint = all(not (sets[left] & sets[right]) for left, right in combinations(range(len(sets)), 2))
    full_cover = covered == carrier
    return {
        "full_cover": full_cover,
        "partial_family": not full_cover,
        "partition": full_cover and pairwise_disjoint and not empty_block,
        "overlapping": bool(potential_pairs),
        "nested": nested,
        "empty_block": empty_block,
        "missed_edges": [list(ordered[bit]) for bit in missed],
        "potential_overlap_pairs": potential_pairs,
        "new_state": False,
        "dynamics": "none",
    }


def fixed_cover(edges, blocks) -> dict:
    """A fixed family of blocks on a carrier. The family is not a state variable.

    Counts and active-block graphs derived from it are functions of the
    present edges. A count tuple is not a cover, so the operator does not
    accept its own output.
    """
    _ordered, parsed = _carrier_blocks(edges, blocks)
    return {
        "operator": "fixed_cover",
        "input_type": "carrier_and_ordered_cover",
        "output_type": "label_of_the_carrier_state",
        "new_state": False,
        "dynamics": "none",
        "second_application": "undefined",
        "undefined_reason": "a count tuple or an intersection graph is not a cover of carrier edges",
        "n_blocks": len(parsed),
    }


def cover_count_labels(edges, blocks) -> list[dict]:
    """How many edges of each fixed block are present.

    The cover stays put. Empty blocks stay at count 0. Overlap is allowed,
    and a block is not required to be disjoint from the others.
    """
    ordered, parsed = _carrier_blocks(edges, blocks)
    width = len(ordered)
    labels = []
    for state in range(1 << width):
        labels.append({
            "counts": [sum((state >> bit) & 1 for bit in bits) for bits in parsed],
        })
    return labels


def _active_blocks(ordered, parsed, state):
    active = []
    for index, bits in enumerate(parsed):
        if any((state >> bit) & 1 for bit in bits):
            active.append(index)
    return active


def active_intersection_labels(edges, blocks) -> list[dict]:
    """Bare intersection graph of the blocks that contain a present edge.

    Adjacency is potential overlap: the fixed edge sets meet. The shared
    edge need not be present. Realised overlap is not this label. The bare
    graph drops the block indices. The vertex count keeps an empty active
    set distinct from a single active block.
    """
    ordered, parsed = _carrier_blocks(edges, blocks)
    sets = [frozenset(bits) for bits in parsed]
    width = len(ordered)
    labels = []
    for state in range(1 << width):
        active = _active_blocks(ordered, parsed, state)
        chosen = [[int(bit) for bit in sets[index]] for index in active]
        graph = intersection_graph(chosen)
        labels.append({"vertices": graph["vertex_count"], "edges": graph["bare_edges"]})
    return labels


def labelled_active_block_labels(edges, blocks) -> list[dict]:
    """Active block indices, and the pairs of those blocks that intersect.

    The indices are the family's own order. This keeps which block is active.
    The bare intersection graph does not. Adjacency is potential overlap of
    the fixed blocks, not realised overlap.
    """
    ordered, parsed = _carrier_blocks(edges, blocks)
    sets = [frozenset(bits) for bits in parsed]
    width = len(ordered)
    labels = []
    for state in range(1 << width):
        active = _active_blocks(ordered, parsed, state)
        adjacent = []
        for left, right in combinations(active, 2):
            if sets[left] & sets[right]:
                adjacent.append([left, right])
        labels.append({"active": active, "adjacent": adjacent})
    return labels


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
    kernel = quotient_kernel(weights, compact)
    quotient_rows = None
    if kernel["defined"]:
        quotient_rows = [
            [dict(cell) for cell in row]
            for row in kernel["rows"]
        ]
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
        "quotient": {
            "defined": kernel["defined"],
            "reason": kernel["reason"],
            "blocks": kernel["blocks"],
            "rows": quotient_rows,
        },
    }
