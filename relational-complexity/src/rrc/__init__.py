"""Recursive relational complexity engine.

The engine evaluates reductions of the existing single-toggle pair grammar.
It does not add a relation order, a history channel, or a geometric embedding.
"""

ENGINE_VERSION = "rrc-0.1.0"

# These four readings of "six" are different claims. Callers must name one.
SIX_CLAIMS = (
    "six_constituent_nodes",
    "six_edges_along_a_path",
    "six_levels_of_composition",
    "six_units_of_context",
)
