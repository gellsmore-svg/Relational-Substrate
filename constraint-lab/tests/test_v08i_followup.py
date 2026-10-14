"""I1 fixtures use only neutral/smaller synthetic cases before independent freeze."""

from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import read_json
from rs_constraint_lab.gen008i_exec import decode
from rs_constraint_lab.gen008i_followup import (
    ITEMS, candidate_same_stationary, coordinate_case, generated_group_size,
    permute_bits, prepare_plan, require_execution, validate,
)
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.history_roles import RoleController
from rs_constraint_lab.role_atlas import balance_gap

ROOT = Path(__file__).resolve().parents[2]
PUBLISHED = pytest.mark.skipif(not (ROOT / "constraint-lab/reports/generation-008i-round-i1-tables.json").exists(), reason="I1 target checks wait for independent frozen publication")


def test_coordinate_group_and_neutral_oracle_only():
    assert generated_group_size(3) == 6 and generated_group_size(6) == 720
    assert permute_bits(3, (2, 1, 0)) == 6
    model = RoleController("SAME_FORM", Fraction(1))
    result = coordinate_case(model, [Fraction(1, 384)] * 384)
    validate(ITEMS[0], {"generated_group_size": 720, "cases": [result]})
    assert result["other_bit_probability"] == Fraction(1, 2)


@pytest.mark.parametrize("feature", ["SAME_FORM", "SAME_DISSOLVE"])
def test_factorisation_on_smaller_synthetic_graph(feature):
    model = RoleController(feature, Fraction(2), 3)
    r, pi = candidate_same_stationary(model)
    assert r == (Fraction(4, 7) if feature == "SAME_FORM" else Fraction(3, 7))
    assert sum(pi) == 1 and balance_gap(pi, model.kernel()) == 0
    result = coordinate_case(model, pi)
    assert result["generator_kernel_gap"] == result["candidate_vs_I0_gap"] == 0


def test_I1_plan_only_declares_reused_inputs():
    plan = prepare_plan()
    assert plan_hash(plan) == plan["plan_hash"]
    assert plan["work_counts"]["new_stationary_solves"] == 0
    assert plan["work_counts"]["atomic_items"] == 2
    assert plan["exposure"]["new_I1_non_neutral_checks_or_contrasts_before_freeze"] == 0
    with pytest.raises(FrozenPlanError):
        require_execution(ROOT, None)


@PUBLISHED
def test_published_I1_mechanisms_and_matched_comparisons():
    root = ROOT / "constraint-lab/reports/items/generation-008i-i1"
    symmetry = decode(read_json(root / (ITEMS[0] + ".json"))["result"])
    matched = decode(read_json(root / (ITEMS[1] + ".json"))["result"])
    validate(ITEMS[0], symmetry)
    validate(ITEMS[1], matched)
    assert len(symmetry["cases"]) == 8 and len(matched["pairs"]) == 4
    for row in symmetry["cases"]:
        if row["feature"].startswith("DISJ"):
            assert row["generator_kernel_gap"] > 0
            assert row["generator_witness"]
    for row in matched["pairs"]:
        assert row["stationary_pair_max_gap"] > 0
        assert Decimal(row["stationary_material_comparison"]["shape_given_edge"]) > 0
