"""Relation semantics are an experimental axis.

``graph``, ``hypergraph``, and ``simplicial`` are not interchangeable
encodings of one another.

- A pairwise graph stores independent binary incidences.
- An irreducible hyperrelation on three entities need not imply any of its pairs.
- A simplicial relation carries its faces.

Generation 1 executes only ``graph``. The other two classes exist so a later
cell can be named in a specification and refused explicitly, rather than
silently compiled into pairs.
"""

from __future__ import annotations


class PairwiseGraphSemantics:
    name = "graph"

    def relation_slots(self, n: int) -> int:
        return n * (n - 1) // 2


class HypergraphSemantics:
    name = "hypergraph"

    def relation_slots(self, n: int) -> int:
        raise NotImplementedError(
            "Hypergraph semantics are unsearched. An irreducible hyperrelation "
            "is not reduced to a collection of pairwise edges."
        )


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
