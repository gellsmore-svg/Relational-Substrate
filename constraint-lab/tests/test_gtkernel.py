"""Vectorised GT template kernel: exact equivalence with build_kernel and solver agreement.

The N=6 equivalence over all 36 E0 cells was run once at build time (see the
GT E1 machinery note); CI keeps N=4 and N=5, which cover every family and both
modes.
"""

from __future__ import annotations

import numpy as np
import pytest

from rs_constraint_lab import gt0, gte0a, gtkernel

FAMILIES = gtkernel.all_e0_components()
CELLS = [(f, g) for f, grades in FAMILIES.items() for g in grades]


@pytest.mark.parametrize("n", [4, 5])
@pytest.mark.parametrize("mode", ["HELD", "FREE"])
@pytest.mark.parametrize("family,grade", CELLS)
def test_weights_and_reachable_class_equal_build_kernel_exactly(family: str, grade: str, mode: str, n: int) -> None:
    result = gtkernel.compare_with_build_kernel(family, grade, n, mode, FAMILIES)
    assert result == {"max_weight_difference": 0.0, "same_states": True, "same_targets": True, "weights_identical": True}


def test_held_candidate_space_is_sorted_and_contains_the_source() -> None:
    space = gtkernel.candidate_states(6, "HELD")
    source = gt0.start_state(6, "HELD")
    assert len(space) == 1 << 12 and np.all(np.diff(space) > 0) and np.all(space & source == source)


@pytest.mark.parametrize("family,grade", [("CLOSE", "strong_favour"), ("PATHF", "weak_suppress"), ("CSPH", "strong_favour+weak_favour"), ("EXCL", "prohibit")])
def test_sparse_and_dense_stationary_agree(family: str, grade: str) -> None:
    chain, _ = gtkernel.reachable_chain(5, "HELD", FAMILIES[family][grade])
    dense = gte0a.stationary(chain)
    sparse = gtkernel.stationary_sparse(chain)
    assert sparse["resolved"] and float(np.abs(dense["ct"] - sparse["ct"]).max()) < 1e-13


def test_sparse_null_converges_to_uniform_from_a_non_uniform_start() -> None:
    chain, _ = gtkernel.reachable_chain(5, "FREE", [])
    start = np.random.default_rng(1).random(len(chain.states)) + 0.5
    sparse = gtkernel.stationary_sparse(chain, start=start)
    assert float(np.abs(sparse["ct"] - 1.0 / len(chain.states)).max()) < 1e-14


def test_path_witness_total_matches_the_template_instances() -> None:
    for n in (5, 6, 7):
        assert gtkernel.path_witness_total(n) == len(gte0a.component_expressions("path_form", n, "weak_favour"))
