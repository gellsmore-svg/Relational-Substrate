"""Pairwise binary relation states as bitsets.

Entity labels are ``0 .. N-1``. Undirected edges are the pairs ``i < j`` in
lexicographic order. Bit ``e`` of a state integer is 1 when that edge is present.

The binary incidence bit is the relation itself. It is not an extra state
channel (see the definition of ``S`` in the dimension model).
"""

from __future__ import annotations

import itertools


def edge_count(n: int) -> int:
    if n < 0:
        raise ValueError("N must be non-negative")
    return n * (n - 1) // 2


def n_states(n: int) -> int:
    return 1 << edge_count(n)


def edges(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def edge_index(n: int) -> dict[tuple[int, int], int]:
    return {pair: index for index, pair in enumerate(edges(n))}


def permutations(n: int) -> list[tuple[int, ...]]:
    return list(itertools.permutations(range(n)))


def edge_permutation_maps(n: int) -> list[tuple[int, ...]]:
    """For each entity permutation, the image of every edge index."""
    edge_list = edges(n)
    index = edge_index(n)
    maps: list[tuple[int, ...]] = []
    for perm in permutations(n):
        mapped = []
        for a, b in edge_list:
            na, nb = perm[a], perm[b]
            if na > nb:
                na, nb = nb, na
            mapped.append(index[(na, nb)])
        maps.append(tuple(mapped))
    return maps


def relabel_state(
    state: int,
    perm: tuple[int, ...],
    edge_list: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
) -> int:
    out = 0
    for bit, (a, b) in enumerate(edge_list):
        if (state >> bit) & 1:
            na, nb = perm[a], perm[b]
            if na > nb:
                na, nb = nb, na
            out |= 1 << index[(na, nb)]
    return out


def canonical_state(state: int, n: int) -> int:
    edge_list = edges(n)
    index = edge_index(n)
    best = state
    for perm in permutations(n):
        best = min(best, relabel_state(state, perm, edge_list, index))
    return best


def canonical_states(n: int) -> list[int]:
    seen: set[int] = set()
    for state in range(n_states(n)):
        seen.add(canonical_state(state, n))
    return sorted(seen)


def triples(n: int) -> list[tuple[int, int, int]]:
    """Undirected 3-subsets in lexicographic order. Empty when N < 3."""
    return [
        (i, j, k)
        for i in range(n)
        for j in range(i + 1, n)
        for k in range(j + 1, n)
    ]


def relation_slots(n: int, order: int = 2) -> list[tuple[int, ...]]:
    """Independent relation slots.

    Order 2 is the pairwise edge list, in the same order as ``edges``.
    Order 3 appends every unordered triple after those pairs. The triple is
    its own bit. It is not implied by the three pairs, and the three pairs
    are not implied by the triple. This is independent-hypergraph layout,
    not a simplex.
    """
    if order == 2:
        return list(edges(n))
    if order != 3:
        raise NotImplementedError(f"relation order {order} is not implemented")
    if n < 3:
        raise ValueError("order 3 requires N >= 3")
    return [*edges(n), *triples(n)]


def slot_index(slots: list[tuple[int, ...]] | tuple[tuple[int, ...], ...]) -> dict[tuple[int, ...], int]:
    return {tuple(slot): index for index, slot in enumerate(slots)}


def slot_permutation_maps(n: int, slots: list[tuple[int, ...]] | tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    """Image of every slot index under each entity permutation.

    A triple on all N entities is fixed by S_N. Pairwise slots move.
    """
    index = slot_index(slots)
    maps: list[tuple[int, ...]] = []
    for perm in permutations(n):
        mapped = []
        for slot in slots:
            image = tuple(sorted(perm[entity] for entity in slot))
            mapped.append(index[image])
        maps.append(tuple(mapped))
    return maps


def relabel_relation_state(state: int, perm: tuple[int, ...], slots) -> int:
    index = slot_index(slots)
    out = 0
    for bit, slot in enumerate(slots):
        if (state >> bit) & 1:
            image = tuple(sorted(perm[entity] for entity in slot))
            out |= 1 << index[image]
    return out


def component_count(state: int, n: int, edge_list: list[tuple[int, int]] | None = None) -> int:
    if edge_list is None:
        edge_list = edges(n)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for bit, (a, b) in enumerate(edge_list):
        if (state >> bit) & 1:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
    return len({find(i) for i in range(n)})
