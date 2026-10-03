"""Lexicographic combination ranking.

Shard boundaries are half-open intervals of the combination index. The index
is the position of a k-subset in lexicographic order. It does not depend on
the clock, and a shard does not walk the combinations that precede it.
"""

from __future__ import annotations

import math


def combination_count(n: int, k: int) -> int:
    if k < 0 or n < 0 or k > n:
        return 0
    return math.comb(n, k)


def unrank_combination(rank: int, n: int, k: int) -> tuple[int, ...]:
    """Return the combination at ``rank`` among the k-subsets of ``range(n)``."""
    if k == 0:
        if rank != 0:
            raise ValueError("rank out of range")
        return ()
    total = math.comb(n, k)
    if rank < 0 or rank >= total:
        raise ValueError(f"rank {rank} is outside 0..{total - 1}")
    chosen: list[int] = []
    remaining = rank
    start = 0
    for left in range(k, 0, -1):
        for candidate in range(start, n):
            count = math.comb(n - candidate - 1, left - 1)
            if remaining < count:
                chosen.append(candidate)
                start = candidate + 1
                break
            remaining -= count
        else:
            raise RuntimeError("combinadic unrank failed")
    return tuple(chosen)


def next_combination(combo: tuple[int, ...], n: int) -> tuple[int, ...] | None:
    """Successor in lexicographic order, or None at the last combination."""
    if not combo:
        return None
    k = len(combo)
    values = list(combo)
    index = k - 1
    while index >= 0 and values[index] == n - k + index:
        index -= 1
    if index < 0:
        return None
    values[index] += 1
    for cursor in range(index + 1, k):
        values[cursor] = values[cursor - 1] + 1
    return tuple(values)
