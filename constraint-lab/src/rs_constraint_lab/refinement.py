"""Coarsest strongly lumpable refinement of a finite observation partition."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction

from rs_constraint_lab.history import HistoryError


def partition_from_labels(labels):
    groups = defaultdict(list)
    for state, label in enumerate(labels):
        groups[label].append(state)
    return canonical_partition(groups.values(), len(labels))


def canonical_partition(blocks, size):
    result = tuple(sorted((tuple(sorted(block)) for block in blocks), key=lambda block: block[0] if block else -1))
    if any(not block for block in result):
        raise HistoryError("partition blocks must be nonempty")
    flat = [state for block in result for state in block]
    if any(type(state) is not int for state in flat) or sorted(flat) != list(range(size)):
        raise HistoryError("partition must cover each state exactly once")
    return result


def validate_kernel(rows):
    size = len(rows)
    if not size:
        raise HistoryError("nonempty finite kernel required")
    for row in rows:
        if not row or any(type(target) is not int or not 0 <= target < size for target in row):
            raise HistoryError("transition target outside finite state space")
        if any(not isinstance(value, (int, Fraction)) or value < 0 for value in row.values()):
            raise HistoryError("exact nonnegative rational transition weights required")
        if sum(row.values()) != 1:
            raise HistoryError("transition row does not sum to one")


def block_index(blocks, size):
    index = [None] * size
    for position, block in enumerate(blocks):
        for state in block:
            index[state] = position
    return tuple(index)


def signatures(rows, blocks):
    mapping = block_index(blocks, len(rows))
    result = []
    for row in rows:
        masses = defaultdict(Fraction)
        for target, value in row.items():
            masses[mapping[target]] += value
        result.append(tuple(sorted((target, mass) for target, mass in masses.items() if mass)))
    return tuple(result)


def lumpability(rows, blocks):
    blocks = canonical_partition(blocks, len(rows))
    state_rows = signatures(rows, blocks)
    quotient, gap = [], Fraction(0)
    for block in blocks:
        reference = dict(state_rows[block[0]])
        for state in block[1:]:
            actual = dict(state_rows[state])
            gap = max(gap, max((abs(actual.get(target, 0) - reference.get(target, 0))
                                for target in actual.keys() | reference.keys()), default=Fraction(0)))
        quotient.append(reference)
    return tuple(quotient), gap


def merge_certificates(rows, initial, stable, quotient):
    initial_of = block_index(initial, len(rows))
    observed = signatures(rows, initial)
    obstructions, immediate_separation = [], True
    for left, a in enumerate(stable):
        for right in range(left + 1, len(stable)):
            b = stable[right]
            if initial_of[a[0]] != initial_of[b[0]]:
                continue
            qa, qb = quotient[left], quotient[right]
            targets = sorted((qa.keys() | qb.keys() | {left}) - {right})
            witness = None
            for target in targets:
                merged = target == left
                pa = qa.get(target, 0) + (qa.get(right, 0) if merged else 0)
                pb = qb.get(target, 0) + (qb.get(right, 0) if merged else 0)
                if pa != pb:
                    witness = {"target_blocks_after_merge": [left, right] if merged else [target],
                               "probability_A": Fraction(pa), "probability_B": Fraction(pb)}
                    break
            if witness is None:
                raise HistoryError("two stable same-observation blocks can still be lumped")
            oa, ob = dict(observed[a[0]]), dict(observed[b[0]])
            immediate = next(({"target_observation_block": target,
                               "probability_A": Fraction(oa.get(target, 0)),
                               "probability_B": Fraction(ob.get(target, 0))}
                              for target in sorted(oa.keys() | ob.keys())
                              if oa.get(target, 0) != ob.get(target, 0)), None)
            immediate_separation &= immediate is not None
            obstructions.append({"block_A": left, "block_B": right,
                                 "current_observation_block": initial_of[a[0]],
                                 "merge_obstruction": witness, "next_observation_obstruction": immediate})
    return obstructions, immediate_separation


def refine(rows, initial_partition):
    validate_kernel(rows)
    initial = canonical_partition(initial_partition, len(rows))
    current, chronology = initial, []
    while True:
        vectors = signatures(rows, current)
        following, splits = [], []
        for position, block in enumerate(current):
            groups = defaultdict(list)
            for state in block:
                groups[vectors[state]].append(state)
            following.extend(groups.values())
            if len(groups) > 1:
                splits.append({"old_block": position,
                               "parts": [{"signature": signature, "members": members}
                                         for signature, members in sorted(groups.items())]})
        following = canonical_partition(following, len(rows))
        if following == current:
            break
        chronology.append({"before_count": len(current), "after_count": len(following), "splits": splits})
        current = following
    quotient, gap = lumpability(rows, current)
    if gap:
        raise HistoryError("fixed-point block rows are not strongly lumpable")
    certificates, immediate = merge_certificates(rows, initial, current, quotient)
    initial_of = block_index(initial, len(rows))
    if any(len({initial_of[state] for state in block}) != 1 for block in current):
        raise HistoryError("stable partition does not refine initial observation")
    return {
        "initial_blocks": initial, "stable_blocks": current,
        "state_to_block": block_index(current, len(rows)),
        "initial_block_count": len(initial), "stable_block_count": len(current),
        "refinement_rounds": len(chronology), "refinement_chronology": chronology,
        "quotient_kernel": [sorted(row.items()) for row in quotient],
        "stable_signatures": [tuple(sorted(row.items())) for row in quotient],
        "strong_lumpability_verified": True, "strong_lumpability_gap": gap,
        "merge_obstructions": certificates,
        "distinct_next_observation_rows_within_current_observation": immediate,
    }
