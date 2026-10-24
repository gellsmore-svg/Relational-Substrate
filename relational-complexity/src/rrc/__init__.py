"""Recursive relational complexity engine.

RRC-001 evaluates reductions of the single-toggle pair grammar.
The atlas compiler turns a list of current-state prohibit and multiply
constraints into that same kind of weight table. It does not add a relation
order, a history channel, or a geometric embedding.

``rrc-0.1.0`` is the engine string frozen into RRC-001. Atlas-001 and
atlas-002 use ``rrc-0.2.0``. The live string is ``rrc-0.3.0``: it adds the
halt_self_loop kernel fingerprint and the incident-neighbour predicate.
A plan is executed only when its own string matches the live one, so the
historical rounds are not recomputed.
"""

ENGINE_VERSION = "rrc-0.3.0"

# These four readings of "six" are different claims. Callers must name one.
SIX_CLAIMS = (
    "six_constituent_nodes",
    "six_edges_along_a_path",
    "six_levels_of_composition",
    "six_units_of_context",
)
