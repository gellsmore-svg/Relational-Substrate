"""Pre-freeze fixtures: synthetic algebra and common neutral only."""

from pathlib import Path

import pytest
pytest.importorskip("flint")
from flint import fmpq as Q, fmpq_mat as Mat

from rs_constraint_lab.gen008n_exec import items
from rs_constraint_lab.stopping_factorization import (
    analyse, conditional_operators, eye, generic_identity, is_zero,
)

ROOT = Path(__file__).resolve().parents[2]


def test_conditional_lifting_dimensions_and_stationary_reset():
    t = Mat([[Q(1, 2), Q(1, 3), Q(1, 6)],
             [Q(1, 4), Q(1, 2), Q(1, 4)],
             [Q(1, 6), Q(1, 3), Q(1, 2)]])
    c, l, p, k, labels = conditional_operators([Q(1, 4), Q(1, 2), Q(1, 4)], t, [0, 1, 0])
    assert (c.nrows(), c.ncols(), l.nrows(), l.ncols()) == (3, 2, 2, 3)
    assert labels == (0, 1) and l * c == eye(2) and p * p == p
    assert k == l * t * c and k * l == l * t * p
    assert Mat([[Q(1, 4), Q(1, 2), Q(1, 4)]]) * p == Mat([[Q(1, 4), Q(1, 2), Q(1, 4)]])


@pytest.mark.parametrize("denominator", [3, 7, 11])
def test_noncommuting_synthetic_resolvents_and_finite_insertions(denominator):
    q = Mat([[Q(1, denominator), Q(1, 2 * denominator)],
             [Q(1, 3 * denominator), Q(1, denominator)]])
    p = Mat([[Q(1, 3), Q(2, 3)], [Q(1, 3), Q(2, 3)]])
    r = Mat([[1, 0], [0, 1]])
    ar, mr = generic_identity(q, p, r)
    assert not is_zero(q * p - p * q)
    assert ar - p * mr == ar * (eye(2) - p) * mr
    for j in range(5):
        rhs = sum((q ** ell * (eye(2) - p) * (q * p) ** (j - ell) for ell in range(j + 1)), Mat(2, 2))
        assert q ** j - p * (q * p) ** j == rhs


def test_common_neutral_all_route_factors_and_full_state_certificates():
    item = dict(items()[0])
    assert item["m"] == "1"
    item["source_passage_id"] = item["item_id"]
    item["item_id"] = "F0-NEUTRAL"
    result = analyse(ROOT, item)
    assert len(result["rows"]) == 14
    assert all(r["bilinear_product_zero"] and r["W_zero"] for r in result["rows"])
    assert all(s["full_validation"]["all_sparse_occupation_and_reset_equations"] for s in result["sides"].values())
    assert all(not any(r["destination_delta4"]) for r in result["timing_rows"])


def test_neutral_operator_transports_and_pairing_protocol():
    from rs_constraint_lab.gen008o_exec import items as factor_items, symmetry_pairing, transport
    item = factor_items()[0]
    result = analyse(ROOT, item)
    symmetry_pairing(result)
    assert transport(ROOT, item, item, result, result)["exact"]
    assert transport(ROOT, item, item, result, result, True)["exact"]
    assert all(r["symmetry_explanation_id"] is None for r in result["rows"])
