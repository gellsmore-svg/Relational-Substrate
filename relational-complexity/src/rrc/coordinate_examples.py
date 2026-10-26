"""Two exact readings of an extra coordinate.

A derived count is a function of a two-bit pair mask. The activity rows
are a third bit with current-state single-bit weights. This module does
not compile constraints and does not change the engine. A bit that is
not a listed carrier edge is a different model and is not built here.
"""

from __future__ import annotations


def derived_pair_count(pair_mask: int) -> int:
    """Number of present bits in a two-bit pair mask.

    Each mask has one count. The count is not injective: masks 1 and 2
    both have count 1. The value does not read any further coordinate.
    """
    if isinstance(pair_mask, bool) or not isinstance(pair_mask, int):
        raise ValueError("pair mask must be an integer in 0 .. 3")
    if pair_mask < 0 or pair_mask > 3:
        raise ValueError("pair mask must be an integer in 0 .. 3")
    return (pair_mask & 1) + ((pair_mask >> 1) & 1)


def activity_weight_rows() -> list[list[int]]:
    """Eight rows for bits ``(pair0, pair1, activity)``.

    Column 0 weighs 3 when the activity bit is present and 1 when it is
    absent. Column 1 weighs 1 in every state. Column 2 weighs 1 when
    pair0 is present and 0 when pair0 is absent. Each column toggles one
    bit. The activity bit is not a function of the two pair bits.
    """
    rows = []
    for state in range(8):
        pair0 = state & 1
        activity = (state >> 2) & 1
        rows.append([
            3 if activity else 1,
            1,
            1 if pair0 else 0,
        ])
    return rows
