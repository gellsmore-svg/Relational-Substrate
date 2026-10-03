"""Bounded enumeration of the normal-form grammar.

The grammar is closed under entity relabelling. Each labelled constraint
receives an integer id. ``image[perm][id]`` is the id of that constraint
after the permutation, which makes orbit checks a table lookup.

Edge constraints are generated first, in the Generation 1 order, so an
edge-only grammar keeps the same ids. Occupation-count constraints are
appended after them. A count literal is invariant under relabelling; the
action edge still moves with the permutation.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from rs_constraint_lab.constraints import (
    DISSOLVE,
    FORM,
    Constraint,
    count_candidates,
    count_literal_status,
    relabel_constraint,
)
from rs_constraint_lab.state import edge_count, edge_permutation_maps, edges


@dataclass(frozen=True)
class Grammar:
    n: int
    k_max: int
    weights: tuple[str, ...]
    edge_list: tuple[tuple[int, int], ...]
    labelled: tuple[Constraint, ...]
    image: tuple[tuple[int, ...], ...]
    predicates: tuple[str, ...] = ("edge",)
    a_max: int | None = None
    stats: dict | None = None

    def expression(self, constraint_id: int) -> str:
        return self.labelled[constraint_id].expression(list(self.edge_list))


def _arity(edge_list, action: int, conditions) -> int:
    named = set(edge_list[action])
    for edge, _bit in conditions:
        named.update(edge_list[edge])
    return len(named)


def _empty_stats() -> dict:
    return {
        "edge_structural": 0,
        "edge_outside_a": 0,
        "count_candidates": 0,
        "count_tautology": 0,
        "count_unsatisfiable": 0,
        "count_outside_k": 0,
        "count_outside_a": 0,
        "count_structural": 0,
        "structural_normal_forms": 0,
        "labelled_constraints": 0,
    }


def enumerate_labelled(
    n: int,
    k_max: int,
    weights: tuple[str, ...] | list[str],
    *,
    a_max: int | None = None,
    predicates: tuple[str, ...] | list[str] = ("edge",),
) -> tuple[list[Constraint], dict]:
    if n < 2:
        raise ValueError("N must be at least 2")
    if k_max < 1:
        raise ValueError("K_max must be at least 1")
    predicate_set = tuple(predicates)
    unknown = [name for name in predicate_set if name not in {"edge", "count"}]
    if unknown or not predicate_set:
        raise ValueError(f"predicates must be a non-empty subset of edge, count; got {predicate_set}")
    weight_tuple = tuple(weights)
    edge_list = edges(n)
    slots = edge_count(n)
    stats = _empty_stats()
    labelled: list[Constraint] = []

    def accept(polarity: int, action: int, conditions, counts, bucket: str) -> None:
        if a_max is not None and _arity(edge_list, action, conditions) > a_max:
            if bucket == "edge":
                stats["edge_outside_a"] += 1
            else:
                stats["count_outside_a"] += 1
            return
        if bucket == "edge":
            stats["edge_structural"] += 1
        else:
            stats["count_structural"] += 1
        stats["structural_normal_forms"] += 1
        for weight in weight_tuple:
            labelled.append(Constraint(polarity, action, conditions, weight, counts))

    if "edge" in predicate_set:
        for action in range(slots):
            others = [edge for edge in range(slots) if edge != action]
            for polarity in (FORM, DISSOLVE):
                for size in range(k_max):
                    for chosen in itertools.combinations(others, size):
                        for assignment in itertools.product((0, 1), repeat=size):
                            conditions = tuple(sorted(zip(chosen, assignment)))
                            accept(polarity, action, conditions, (), "edge")

    if "count" in predicate_set:
        literals = count_candidates(slots)
        max_extra = k_max - 2
        for action in range(slots):
            others = [edge for edge in range(slots) if edge != action]
            for polarity in (FORM, DISSOLVE):
                for op, threshold in literals:
                    status = count_literal_status(polarity, op, threshold, slots)
                    extra_sizes = range(0, max_extra + 1) if "edge" in predicate_set and max_extra >= 0 else (0,)
                    # A count literal with no legal K still needs a partition row
                    # when the edge-condition size is zero. Larger sizes are the
                    # same literal with extra edge conditions.
                    if status != "ok":
                        for size in extra_sizes:
                            for _chosen in itertools.combinations(others, size):
                                for _assignment in itertools.product((0, 1), repeat=size):
                                    stats["count_candidates"] += 1
                                    stats[f"count_{status}"] += 1
                        continue
                    for size in extra_sizes:
                        for chosen in itertools.combinations(others, size):
                            for assignment in itertools.product((0, 1), repeat=size):
                                stats["count_candidates"] += 1
                                if size > 0 and "edge" not in predicate_set:
                                    stats["count_outside_k"] += 1
                                    continue
                                if k_max < 2 + size:
                                    stats["count_outside_k"] += 1
                                    continue
                                conditions = tuple(sorted(zip(chosen, assignment)))
                                accept(polarity, action, conditions, ((op, threshold),), "count")

    stats["labelled_constraints"] = len(labelled)
    stats["weight_alphabet_size"] = len(weight_tuple)
    return labelled, stats


def grammar_statistics(
    n: int,
    k_max: int,
    n_weights: int,
    *,
    a_max: int | None = None,
    predicates: tuple[str, ...] | list[str] = ("edge",),
    weight_names: tuple[str, ...] | list[str] | None = None,
) -> dict:
    weights = tuple(weight_names) if weight_names is not None else tuple(f"w{i}" for i in range(n_weights))
    if len(weights) != n_weights:
        raise ValueError("weight_names and n_weights disagree")
    _labelled, stats = enumerate_labelled(
        n, k_max, weights, a_max=a_max, predicates=predicates
    )
    return stats


def build_grammar(
    n: int,
    k_max: int,
    weights: tuple[str, ...] | list[str],
    *,
    a_max: int | None = None,
    predicates: tuple[str, ...] | list[str] = ("edge",),
) -> Grammar:
    weight_tuple = tuple(weights)
    predicate_tuple = tuple(predicates)
    labelled, stats = enumerate_labelled(
        n, k_max, weight_tuple, a_max=a_max, predicates=predicate_tuple
    )
    index = {constraint.key(): i for i, constraint in enumerate(labelled)}
    if len(index) != len(labelled):
        raise RuntimeError("labelled grammar produced duplicate normal forms")
    edge_list = edges(n)
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
    if labelled:
        identity = image_rows[0]
        if identity != tuple(range(len(labelled))):
            raise RuntimeError("the first permutation is not the identity on constraints")
    return Grammar(
        n,
        k_max,
        weight_tuple,
        tuple(edge_list),
        tuple(labelled),
        tuple(image_rows),
        predicate_tuple,
        a_max,
        stats,
    )


def is_canonical_ids(ids: tuple[int, ...], image: tuple[tuple[int, ...], ...]) -> bool:
    """True when ``ids`` is the lexicographically least labelling of its orbit."""
    if not image:
        return True
    ordered = tuple(sorted(ids))
    if ordered != ids:
        return False
    for row in image:
        imaged = [row[i] for i in ids]
        imaged.sort()
        if tuple(imaged) < ordered:
            return False
    return True


def labelled_simple_count(structural: int, n_weights: int, cardinality: int) -> int:
    """Labelled sets whose structural identities are pairwise distinct.

    Each structural form is paired with every enumerated weight exactly once.
    Stacked-weight sets are the complement inside the labelled combinations.
    """
    if cardinality < 1 or structural < cardinality:
        return 0
    return math.comb(structural, cardinality) * (n_weights ** cardinality)


def canonical_id_tuple(ids: tuple[int, ...], image: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    best = tuple(sorted(ids))
    for row in image:
        imaged = [row[i] for i in ids]
        imaged.sort()
        imaged_t = tuple(imaged)
        if imaged_t < best:
            best = imaged_t
    return best
