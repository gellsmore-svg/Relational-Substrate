"""Exact software checks of XOR-mask recoding proofs; not an atlas worker."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json


METHOD_ID = "xor-mask-analysis-0.1.0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def directions(width: int, masks: list[int]) -> None:
    require(type(width) is int and 1 <= width <= 8, "width must be between 1 and 8")
    require(all(type(mask) is int and 0 < mask < 2 ** width for mask in masks), "invalid nonzero mask")
    require(len(set(masks)) == len(masks), "aggregate duplicate directions before analysis")


def binary_rank(masks: list[int]) -> int:
    pivots = {}
    for mask in masks:
        require(type(mask) is int and mask > 0, "rank requires nonzero integer masks")
        residual = mask
        while residual:
            leading = residual.bit_length() - 1
            if leading in pivots:
                residual ^= pivots[leading]
            else:
                pivots[leading] = residual
                break
    return len(pivots)


def subset_independent(masks: list[int]) -> bool:
    require(len(masks) <= 8, "subset oracle is capped at eight masks")
    for size in range(1, len(masks) + 1):
        for selected in combinations(masks, size):
            combined = 0
            for mask in selected:
                combined ^= mask
            if combined == 0:
                return False
    return True


def recoding(width: int, masks: list[int]) -> list[int]:
    directions(width, masks)
    require(binary_rank(masks) == len(masks), "dependent directions cannot form coordinate axes")
    basis = list(masks)
    for bit in range(width):
        candidate = 2 ** bit
        if binary_rank(basis + [candidate]) > len(basis):
            basis.append(candidate)
    encoded = {0: 0}
    for bit, vector in enumerate(basis):
        previous = list(encoded.items())
        for state, coordinates in previous:
            encoded[state ^ vector] = coordinates | (2 ** bit)
    require(len(encoded) == 2 ** width, "basis does not span the state space")
    return [encoded[state] for state in range(2 ** width)]


def kernel(width: int, masks: list[int], weights: list[list[int]]) -> list[list[Fraction]]:
    directions(width, masks)
    size = 2 ** width
    require(len(weights) == size and all(len(row) == len(masks) for row in weights), "weight shape mismatch")
    require(all(type(weight) is int and weight >= 0 for row in weights for weight in row), "weights must be nonnegative integers")
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for source, row in enumerate(weights):
        total = sum(row)
        if total == 0:
            matrix[source][source] = Fraction(1)
        else:
            for mask, weight in zip(masks, row):
                matrix[source][source ^ mask] += Fraction(weight, total)
    return matrix


def block_rows_exact(matrix: list[list[Fraction]], labels: list[int]) -> bool:
    size = len(matrix)
    require(len(labels) == size and all(len(row) == size for row in matrix), "partition shape mismatch")
    blocks = sorted(set(labels))
    first = {}
    for source, label in enumerate(labels):
        observed = tuple(sum(matrix[source][target] for target in range(size) if labels[target] == block)
                         for block in blocks)
        if label in first and observed != first[label]:
            return False
        first[label] = observed
    return True


def proportional_blocks(weights: list[list[int]], labels: list[int]) -> bool:
    require(len(weights) == len(labels), "weight partition mismatch")
    require(bool(weights) and all(len(row) == len(weights[0]) for row in weights), "weight vector mismatch")
    require(all(type(weight) is int and weight >= 0 for row in weights for weight in row), "weights must be nonnegative integers")
    first = {}
    for row, label in zip(weights, labels):
        if label not in first:
            first[label] = row
            continue
        reference = first[label]
        if bool(sum(row)) != bool(sum(reference)):
            return False
        if any(row[left] * reference[right] != row[right] * reference[left]
               for left in range(len(row)) for right in range(left + 1, len(row))):
            return False
    return True


def support(width: int, masks: list[int]) -> list[set[int]]:
    directions(width, masks)
    return [{state ^ mask for mask in masks} for state in range(2 ** width)]


def triangle(graph: list[set[int]]) -> list[int] | None:
    for source, neighbors in enumerate(graph):
        for left, right in combinations(sorted(neighbors), 2):
            if right in graph[left]:
                return [source, left, right]
    return None


def excessive_common_neighbors(graph: list[set[int]]) -> dict | None:
    for left, right in combinations(range(len(graph)), 2):
        common = sorted(graph[left] & graph[right])
        if len(common) > 2:
            return {"states": [left, right], "common_neighbors": common}
    return None


def closure_fixture(first: list[int], second: list[int]) -> dict:
    weights = [list(first if state < 4 else second) for state in range(8)]
    labels = [state % 4 for state in range(8)]
    matrix = kernel(3, [1, 2], weights)
    algebraic = proportional_blocks(weights, labels)
    exact = block_rows_exact(matrix, labels)
    require(algebraic == exact, "algebraic criterion disagrees with block-row aggregation")
    return {"first_weights": first, "second_weights": second, "strongly_lumpable": exact}


def run_checks() -> dict:
    sets_checked = 0
    independent_sets = 0
    dependent_sets = 0
    edge_checks = 0
    for width in range(1, 5):
        for size in range(width + 1):
            for selected in combinations(range(1, 2 ** width), size):
                masks = list(selected)
                independent = subset_independent(masks)
                require((binary_rank(masks) == len(masks)) == independent, "rank and subset oracle disagree")
                sets_checked += 1
                if not independent:
                    dependent_sets += 1
                    try:
                        recoding(width, masks)
                    except ValueError:
                        continue
                    raise ValueError("dependent directions were assigned independent axes")
                independent_sets += 1
                encoded = recoding(width, masks)
                require(set(encoded) == set(range(2 ** width)), "recoding is not a permutation")
                for state in range(2 ** width):
                    for position, mask in enumerate(masks):
                        require(encoded[state ^ mask] == encoded[state] ^ (2 ** position), "recoded direction drift")
                        require(encoded[state] >> size == encoded[state ^ mask] >> size, "inactive coordinate drift")
                        edge_checks += 1
    square = support(2, [1, 2])
    odd_circuit = support(2, [1, 2, 3])
    cube = support(4, [1, 2, 4, 8])
    even_circuit = support(4, [1, 2, 4, 7])
    require(triangle(square) is None and triangle(cube) is None, "independent control has a triangle")
    odd_witness = triangle(odd_circuit)
    require(odd_witness is not None, "three-mask circuit has no triangle")
    require(triangle(even_circuit) is None, "four-mask control was meant to be bipartite")
    require(excessive_common_neighbors(cube) is None, "cube violates its common-neighbor bound")
    even_witness = excessive_common_neighbors(even_circuit)
    require(even_witness is not None, "four-mask circuit lacks the stronger obstruction")
    weighted_checked = 0
    exact_weighted = 0
    alphabet = list(product(range(3), repeat=2))
    for first, second in product(alphabet, repeat=2):
        checked = closure_fixture(list(first), list(second))
        weighted_checked += 1
        exact_weighted += int(checked["strongly_lumpable"])
    controls = {
        "common_scale": closure_fixture([1, 2], [2, 4]),
        "relative_rates": closure_fixture([1, 1], [1, 2]),
        "support_switch": closure_fixture([1, 0], [0, 1]),
        "halt_mismatch": closure_fixture([0, 0], [1, 0]),
        "all_halt": closure_fixture([0, 0], [0, 0]),
    }
    require([controls[name]["strongly_lumpable"] for name in controls]
            == [True, False, False, False, True], "named closure control failed")
    atlas_masks = [1, 6, 8]
    extended_masks = [1, 2, 6, 8]
    require(binary_rank(atlas_masks) == 3 and binary_rank(extended_masks) == 4, "interface direction rank mismatch")
    return {"method": METHOD_ID, "evidence_type": "analytic-proof software validation",
            "scientific_worker_invocations": 0, "new_atlas_cells": 0,
            "direction_subset_domain": "all subsets of nonzero masks of cardinality <= width, widths 1..4",
            "direction_sets_checked": sets_checked, "independent_sets": independent_sets,
            "dependent_sets": dependent_sets, "directed_edges_checked": edge_checks,
            "three_mask_triangle": odd_witness, "four_mask_common_neighbors": even_witness,
            "weight_vector_pairs_checked": weighted_checked, "exact_weight_vector_pairs": exact_weighted,
            "nonexact_weight_vector_pairs": weighted_checked - exact_weighted,
            "weight_domain": "two directions, one hidden bit, vector entries in {0,1,2}; validation fixtures only",
            "controls": controls,
            "interface_reencoding": {"atlas_masks": atlas_masks, "rank": 3,
                                     "extended_masks": extended_masks, "extended_rank": 4},
            "status": "verified"}


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
