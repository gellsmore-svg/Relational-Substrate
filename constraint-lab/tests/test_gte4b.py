"""Round E4B machinery (GT-P007): S4 and P4 scaffolds. N=4/5 and NULL-only checks (not round cells)."""

from __future__ import annotations

import math
import sys

import pytest

from rs_constraint_lab import gt0, gte0a, gte0b, gte4a, gte4b, gtkernel

FAMILIES = {**gte0a.FAMILIES, **gte0b.FAMILIES}


def test_manifest():
    cells = gte4b.items()
    assert len(cells) == 12 and {c["scaffold"] for c in cells} == {"S4", "P4"} and {c["n"] for c in cells} == {6}


@pytest.mark.parametrize("scaffold,floor", [("S4", {0: 0, 1: 2, 2: 2, 3: 2}), ("P4", {0: 1, 1: 1, 2: 1, 3: 1})])
def test_floor_formula(scaffold, floor):
    assert gte4a.analytic_floor(scaffold, 6) == floor
    sc = gt0.SCAFFOLDS[scaffold]
    deg = {v: sum(v in e for e in sc.held) for v in sc.source}
    for s in sc.source:
        assert floor[s] == sum(deg[c] - 1 for c in sc.source if (min(s, c), max(s, c)) in set(sc.held))


@pytest.mark.parametrize("scaffold", ["S4", "P4"])
@pytest.mark.parametrize("family,grade", [("PATHF", "weak_suppress"), ("CSPH", "strong_favour+weak_favour"), ("NULL", "none")])
def test_rule_string_equality_n5(scaffold, family, grade):
    with gt0.use_scaffold(scaffold):
        cmp = gtkernel.compare_with_build_kernel(family, grade, 5, "HELD", FAMILIES)
    assert cmp["same_states"] and cmp["same_targets"] and cmp["weights_identical"]


@pytest.mark.parametrize("scaffold,group", [("S4", 6 * 2), ("P4", 2 * 2)])
def test_automorphisms(scaffold, group):
    assert len(gt0.SCAFFOLDS[scaffold].automorphisms(6)) == group


def test_reference_probe_avoids_source():
    with gt0.use_scaffold("S4"):
        assert gt0.reference_probe(6) == 4
    with gt0.use_scaffold("K3"):
        assert gt0.reference_probe(6) == 3
    with gt0.use_scaffold("K2"):
        assert gt0.reference_probe(6) == 3


def test_geometry():
    for sc in ("S4", "P4"):
        g = gte4a.null_geometry(sc, 6)
        assert g["free_slots"] == 12 and g["attachment_slots"] == 8 and g["nonheld_source_internal_slots"] == 3
        assert g["r0"] == pytest.approx(8 / 12)


def test_n4_pipeline_under_s4():
    it = {"alphabet": "W4", "family": "PATHH", "grade": "weak_favour", "item_id": "SYN-HELD-S4-N5-PATHH", "mode": "HELD", "n": 5, "role": "synthetic", "scaffold": "S4", "held": [[0, 1], [0, 2], [0, 3]]}
    r, _ = gte4a.analyse_item(it)
    assert gte4a.check_problems(r) == []


def test_plan_and_refusal():
    from pathlib import Path

    from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash

    repo = Path(__file__).resolve().parents[2]
    a, b = gte4b.prepare_plan(repo), gte4b.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a) and a["items"] == gte4b.items()
    with pytest.raises(FrozenPlanError):
        gte4b.require_execution(repo, None)
