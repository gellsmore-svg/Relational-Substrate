"""Checks of proof oracles and adversarial boundaries, not scientific runs."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "provenance/xor-mask-analysis-check.py"
MODULE_SPEC = importlib.util.spec_from_file_location("xor_mask_analysis", SCRIPT)
ANALYSIS = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(ANALYSIS)


def test_recoding_extends_independent_masks_and_preserves_all_edges():
    masks = [1, 6, 8]
    encoded = ANALYSIS.recoding(4, masks)
    assert set(encoded) == set(range(16))
    for source in range(16):
        for position, mask in enumerate(masks):
            assert encoded[source ^ mask] == encoded[source] ^ (2 ** position)
    assert ANALYSIS.binary_rank([1, 2, 6, 8]) == 4


@pytest.mark.parametrize("masks", ([1, 2, 3], [1, 2, 4, 7]))
def test_dependent_directions_are_not_coordinate_axes(masks):
    assert ANALYSIS.binary_rank(masks) < len(masks)
    assert ANALYSIS.subset_independent(masks) is False
    with pytest.raises(ValueError, match="dependent"):
        ANALYSIS.recoding(4, masks)


@pytest.mark.parametrize("width,masks", [(0, [1]), (9, [1]), (3, [0]), (3, [8]), (3, [True]), (3, [1, 1])])
def test_bad_domains_and_unaggregated_duplicate_masks_are_rejected(width, masks):
    with pytest.raises(ValueError):
        ANALYSIS.recoding(width, masks)


def test_empty_catalogue_is_a_bijection_with_no_active_coordinate():
    assert ANALYSIS.recoding(3, []) == list(range(8))
    assert ANALYSIS.subset_independent([]) is True


def test_odd_and_even_circuits_have_different_support_obstructions():
    odd = ANALYSIS.support(2, [1, 2, 3])
    even = ANALYSIS.support(4, [1, 2, 4, 7])
    cube = ANALYSIS.support(4, [1, 2, 4, 8])
    assert ANALYSIS.triangle(odd) is not None
    assert ANALYSIS.triangle(even) is None
    witness = ANALYSIS.excessive_common_neighbors(even)
    assert len(witness["common_neighbors"]) == 4
    assert ANALYSIS.excessive_common_neighbors(cube) is None


def test_common_rate_scaling_does_not_imply_failure_of_closure():
    assert ANALYSIS.closure_fixture([1, 2], [2, 4])["strongly_lumpable"] is True
    assert ANALYSIS.closure_fixture([1, 1], [1, 2])["strongly_lumpable"] is False


def test_zero_cross_products_are_not_sufficient_across_a_halt_mismatch():
    first, second = [0, 0], [1, 0]
    assert first[0] * second[1] == first[1] * second[0]
    assert ANALYSIS.closure_fixture(first, second)["strongly_lumpable"] is False
    assert ANALYSIS.closure_fixture(first, first)["strongly_lumpable"] is True


def test_block_aggregation_checks_distributions_not_just_support():
    matrix = [[Fraction(1, 3), Fraction(2, 3)], [Fraction(1, 2), Fraction(1, 2)]]
    assert ANALYSIS.block_rows_exact(matrix, [0, 0]) is True
    weights = [[1, 1] for _ in range(4)] + [[1, 2] for _ in range(4)]
    kernel = ANALYSIS.kernel(3, [1, 2], weights)
    assert all({target for target, probability in enumerate(row) if probability}
               == {source ^ 1, source ^ 2} for source, row in enumerate(kernel))
    assert ANALYSIS.block_rows_exact(kernel, [state % 4 for state in range(8)]) is False


def test_kernel_validates_shape_and_nonnegative_integer_weights():
    with pytest.raises(ValueError, match="shape"):
        ANALYSIS.kernel(2, [1], [[1]])
    for weight in (-1, True, Fraction(1, 2)):
        with pytest.raises(ValueError, match="nonnegative integers"):
            ANALYSIS.kernel(1, [1], [[weight], [1]])


def test_exhaustive_bounded_oracles_and_positive_negative_controls_agree():
    checked = ANALYSIS.run_checks()
    assert checked["status"] == "verified"
    assert checked["direction_sets_checked"] == checked["independent_sets"] + checked["dependent_sets"]
    assert checked["weight_vector_pairs_checked"] == 3 ** 4
    assert checked["exact_weight_vector_pairs"] + checked["nonexact_weight_vector_pairs"] == 3 ** 4
    assert checked["scientific_worker_invocations"] == checked["new_atlas_cells"] == 0
