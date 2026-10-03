"""Bounded enumeration of the normal-form grammar.

The grammar is closed under entity relabelling. Each labelled constraint
receives an integer id. ``image[perm][id]`` is the id of that constraint
after the permutation, which makes orbit checks a table lookup.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from rs_constraint_lab.constraints import DISSOLVE, FORM, Constraint, relabel_constraint
from rs_constraint_lab.state import edge_count, edge_permutation_maps, edges


@dataclass(frozen=True)
class Grammar:
    n: int
    k_max: int
    weights: tuple[str, ...]
    edge_list: tuple[tuple[int, int], ...]
    labelled: tuple[Constraint, ...]
    image: tuple[tuple[int, ...], ...]

    def expression(self, constraint_id: int) -> str:
        return self.labelled[constraint_id].expression(list(self.edge_list))


def build_grammar(n: int, k_max: int, weights: tuple[str, ...] | list[str]) -> Grammar:
    if n < 2:
        raise ValueError("N must be at least 2")
    if k_max < 1:
        raise ValueError("K_max must be at least 1")
    weight_tuple = tuple(weights)
    edge_list = edges(n)
    slots = edge_count(n)
    labelled: list[Constraint] = []
    for action in range(slots):
        others = [edge for edge in range(slots) if edge != action]
        for polarity in (FORM, DISSOLVE):
            for size in range(k_max):
                for chosen in itertools.combinations(others, size):
                    for assignment in itertools.product((0, 1), repeat=size):
                        conditions = tuple(sorted(zip(chosen, assignment)))
                        for weight in weight_tuple:
                            labelled.append(Constraint(polarity, action, conditions, weight))
    index = {constraint.key(): i for i, constraint in enumerate(labelled)}
    if len(index) != len(labelled):
        raise RuntimeError("labelled grammar produced duplicate normal forms")
    image_rows: list[tuple[int, ...]] = []
    for edge_map in edge_permutation_maps(n):
        row = []
        for constraint in labelled:
            image = relabel_constraint(constraint, edge_map)
            try:
                row.append(index[image.key()])
            except KeyError as exc:
                raise RuntimeError("grammar is not closed under relabelling") from exc
        image_rows.append(tuple(row))
    identity = image_rows[0]
    if identity != tuple(range(len(labelled))):
        raise RuntimeError("the first permutation is not the identity on constraints")
    return Grammar(n, k_max, weight_tuple, tuple(edge_list), tuple(labelled), tuple(image_rows))


def is_canonical_ids(ids: tuple[int, ...], image: tuple[tuple[int, ...], ...]) -> bool:
    """True when ``ids`` is the lexicographically least labelling of its orbit."""
    ordered = tuple(sorted(ids))
    if ordered != ids:
        return False
    for row in image:
        imaged = [row[i] for i in ids]
        imaged.sort()
        if tuple(imaged) < ordered:
            return False
    return True


def canonical_id_tuple(ids: tuple[int, ...], image: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    best = tuple(sorted(ids))
    for row in image:
        imaged = [row[i] for i in ids]
        imaged.sort()
        imaged_t = tuple(imaged)
        if imaged_t < best:
            best = imaged_t
    return best
