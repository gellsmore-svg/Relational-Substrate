"""Finite weight alphabets for soft and hard reweighting.

A constraint multiplies the baseline weight of a toggle. The multiplicative
identity is 1 (neutral, not enumerated). The multiplicative zero is
``prohibit``. Soft grades are integer powers of a base r > 1, symmetric
under g -> -g, so favour and suppress of the same grade are reciprocals.

W4, W3, and W16 use the same grades {-2, -1, +1, +2} and bases 2, 3, and 4.
For a fixed grade assignment the ordering of positive transition weights is
therefore independent of the base. See ``formalism.md``.
"""

from __future__ import annotations

from fractions import Fraction

GRADES: dict[str, int | None] = {
    "prohibit": None,
    "strong_suppress": -2,
    "weak_suppress": -1,
    "neutral": 0,
    "weak_favour": 1,
    "strong_favour": 2,
}

ENUMERATED_WEIGHTS: tuple[str, ...] = (
    "prohibit",
    "strong_suppress",
    "weak_suppress",
    "weak_favour",
    "strong_favour",
)

ALPHABET_BASE: dict[str, int] = {"W4": 2, "W3": 3, "W16": 4}


def alphabet_factors(name: str) -> dict[str, Fraction]:
    if name not in ALPHABET_BASE:
        known = ", ".join(sorted(ALPHABET_BASE))
        raise KeyError(f"unknown weight alphabet {name!r}; known: {known}")
    base = ALPHABET_BASE[name]
    factors: dict[str, Fraction] = {}
    for weight, grade in GRADES.items():
        if grade is None:
            factors[weight] = Fraction(0)
        else:
            factors[weight] = Fraction(base) ** grade
    return factors


def is_geometric_pair(left: str, right: str) -> bool:
    """True when two alphabets share the grade table and differ only in base."""
    return left in ALPHABET_BASE and right in ALPHABET_BASE
