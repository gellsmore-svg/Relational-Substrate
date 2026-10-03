"""Relation semantics are an experimental axis.

``graph``, ``hypergraph``, and ``simplicial`` are not interchangeable
encodings of one another.

- A pairwise graph stores independent binary incidences.
- Independent hypergraph semantics add irreducible hyperrelations. At order 3
  the triple is its own bit: it does not imply its pairs, and the pairs do
  not imply it.
- A simplicial relation would carry its faces. That rule is not compiled
  into the hypergraph bit.

Generation 1 executes ``graph``. Generation 3 executes independent
hypergraph at ``O = 3``. Simplicial semantics still raise, so a simplex is
never stored as a free hyperedge.
"""

from __future__ import annotations

from rs_constraint_lab.state import relation_slots as independent_slots


class PairwiseGraphSemantics:
    name = "graph"

    def relation_slots(self, n: int) -> int:
        return n * (n - 1) // 2


class HypergraphSemantics:
    """Independent hypergraph. Not a simplex and not a shorthand for its pairs."""

    name = "hypergraph"

    def relation_slots(self, n: int) -> int:
        return len(independent_slots(n, 3))


class SimplicialSemantics:
    name = "simplicial"

    def relation_slots(self, n: int) -> int:
        raise NotImplementedError(
            "Simplicial semantics are unsearched. A simplex is not identified "
            "with a hyperedge, and it is not identified with the set of its faces alone."
        )


_SEMANTICS = {
    "graph": PairwiseGraphSemantics,
    "hypergraph": HypergraphSemantics,
    "simplicial": SimplicialSemantics,
}


def get_semantics(name: str):
    try:
        return _SEMANTICS[name]()
    except KeyError as exc:
        known = ", ".join(sorted(_SEMANTICS))
        raise KeyError(f"unknown relation semantics {name!r}; known: {known}") from exc


def semantics_names() -> tuple[str, ...]:
    return tuple(sorted(_SEMANTICS))
