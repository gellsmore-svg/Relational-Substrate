"""Coverage arithmetic for one grammar cell.

Raw templates assign every edge, including the action edge, a mark in
``{any, present, absent}``, choose a polarity, and choose an action edge.
That raw set is then partitioned:

- contradictory action mark (syntax invalid);
- redundant action mark, which normalises to the same constraint as ``any``;
- normal forms whose literal count exceeds ``K_max`` (outside the cell);
- normal forms inside the cell, before the weight alphabet and before symmetry.
"""

from __future__ import annotations

import itertools

from rs_constraint_lab.constraints import DISSOLVE, FORM
from rs_constraint_lab.state import edge_count, edges, n_states as state_count


def template_accounting(n: int, k_max: int, n_weights: int, a_max: int | None = None) -> dict[str, int]:
    slots = edge_count(n)
    edge_list = edges(n)
    raw = 0
    syntax_invalid = 0
    redundant_collapsed = 0
    outside_k = 0
    outside_a = 0
    normal_forms = 0
    for action in range(slots):
        for polarity in (FORM, DISSOLVE):
            for assignment in itertools.product((0, 1, 2), repeat=slots):
                raw += 1
                mark = assignment[action]
                if polarity == FORM and mark == 1:
                    syntax_invalid += 1
                    continue
                if polarity == DISSOLVE and mark == 0:
                    syntax_invalid += 1
                    continue
                if (polarity == FORM and mark == 0) or (polarity == DISSOLVE and mark == 1):
                    redundant_collapsed += 1
                    continue
                conditions = [
                    edge
                    for edge, edge_mark in enumerate(assignment)
                    if edge != action and edge_mark != 2
                ]
                if 1 + len(conditions) > k_max:
                    outside_k += 1
                    continue
                if a_max is not None:
                    named = set(edge_list[action])
                    for edge in conditions:
                        named.update(edge_list[edge])
                    if len(named) > a_max:
                        outside_a += 1
                        continue
                normal_forms += 1
    labelled = normal_forms * n_weights
    return {
        "labelled_states": state_count(n),
        "relation_slots": slots,
        "raw_structural_templates": raw,
        "removed_syntax_invalid": syntax_invalid,
        "removed_redundant_normalisation": redundant_collapsed,
        "outside_k_bound": outside_k,
        "outside_a_bound": outside_a,
        "structural_normal_forms": normal_forms,
        "weight_alphabet_size": n_weights,
        "labelled_constraints": labelled,
    }
