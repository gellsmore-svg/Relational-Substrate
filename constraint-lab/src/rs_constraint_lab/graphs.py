"""Pairwise graph isomorphism classes at N=4.

The organisation of a visible pairwise state is its isomorphism class under
S4. Edge count is a descriptor of that class. It is not the class. Two graphs
with the same number of edges can fail to be isomorphic. No scalar combines
these descriptors into an organisation score.
"""

from __future__ import annotations

from rs_constraint_lab.state import edges, permutations, relabel_state


def _component_count(mask: int, edge_list: list[tuple[int, int]], n: int = 4) -> int:
    parent = list(range(n))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for bit, (left, right) in enumerate(edge_list):
        if (mask >> bit) & 1:
            a = find(left)
            b = find(right)
            if a != b:
                parent[b] = a
    return len({find(vertex) for vertex in range(n)})


def _triangle_count(mask: int, edge_list: list[tuple[int, int]]) -> int:
    present = {(a, b) for bit, (a, b) in enumerate(edge_list) if (mask >> bit) & 1}
    count = 0
    for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        pairs = (tuple(sorted((a, b))), tuple(sorted((a, c))), tuple(sorted((b, c))))
        if all(pair in present for pair in pairs):
            count += 1
    return count


def _degree_multiset(mask: int, edge_list: list[tuple[int, int]], n: int = 4) -> tuple[int, ...]:
    degrees = [0] * n
    for bit, (left, right) in enumerate(edge_list):
        if (mask >> bit) & 1:
            degrees[left] += 1
            degrees[right] += 1
    return tuple(sorted(degrees, reverse=True))


def _automorphisms(mask: int, edge_list: list[tuple[int, int]], index: dict[tuple[int, int], int]) -> int:
    count = 0
    for perm in permutations(4):
        if relabel_state(mask, perm, edge_list, index) == mask:
            count += 1
    return count


class PairClassTable:
    """Canonical S4 class of each of the 64 pairwise graphs on 4 vertices."""

    def __init__(self) -> None:
        self.n = 4
        self.edge_list = edges(4)
        self.index = {pair: bit for bit, pair in enumerate(self.edge_list)}
        self.n_graphs = 1 << len(self.edge_list)
        canonical = []
        for mask in range(self.n_graphs):
            best = mask
            for perm in permutations(4):
                best = min(best, relabel_state(mask, perm, self.edge_list, self.index))
            canonical.append(best)
        self.canonical = tuple(canonical)
        representatives = sorted(set(canonical))
        self.representatives = tuple(representatives)
        descriptors = {}
        for mask in representatives:
            edges_present = mask.bit_count()
            components = _component_count(mask, self.edge_list)
            triangles = _triangle_count(mask, self.edge_list)
            degrees = _degree_multiset(mask, self.edge_list)
            autos = _automorphisms(mask, self.edge_list, self.index)
            name = (
                f"e{edges_present}-deg{''.join(str(item) for item in degrees)}"
                f"-tri{triangles}-comp{components}"
            )
            descriptors[mask] = {
                "canonical_mask": mask,
                "name": name,
                "edge_count": edges_present,
                "pair_density": edges_present / len(self.edge_list),
                "component_count": components,
                "degree_multiset": degrees,
                "triangle_count": triangles,
                "connected": components == 1,
                "automorphism_group_size": autos,
                "orbit_size": sum(1 for item in canonical if item == mask),
            }
        names = [descriptors[mask]["name"] for mask in representatives]
        if len(names) != len(set(names)):
            raise RuntimeError("pairwise class names are not unique")
        if len(representatives) != 11:
            raise RuntimeError(f"N=4 has 11 unlabelled simple graphs, found {len(representatives)}")
        self.by_mask = descriptors
        self.class_of = tuple(canonical)
        self.name_of = tuple(descriptors[item]["name"] for item in canonical)
        self.edge_count_of = tuple(descriptors[item]["edge_count"] for item in canonical)
        path = self._mask_of_edges((0, 1), (1, 2))
        matching = self._mask_of_edges((0, 1), (2, 3))
        self.path_mask = self.canonical[path]
        self.matching_mask = self.canonical[matching]
        if self.path_mask == self.matching_mask:
            raise RuntimeError("the two-edge path and the two-edge matching share an orbit")
        self.path_name = self.by_mask[self.path_mask]["name"]
        self.matching_name = self.by_mask[self.matching_mask]["name"]

    def _mask_of_edges(self, *pairs: tuple[int, int]) -> int:
        mask = 0
        for pair in pairs:
            mask |= 1 << self.index[tuple(sorted(pair))]
        return mask

    def same_cardinality_nonisomorphic(self, left: int, right: int) -> bool:
        return self.edge_count_of[left] == self.edge_count_of[right] and self.class_of[left] != self.class_of[right]


def pair_classes() -> PairClassTable:
    global _TABLE
    if _TABLE is None:
        _TABLE = PairClassTable()
    return _TABLE


_TABLE: PairClassTable | None = None
