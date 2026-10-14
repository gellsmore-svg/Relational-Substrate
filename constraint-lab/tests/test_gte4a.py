"""Round E4A machinery (GT-P007). N=4 cells (not round cells) and synthetic factor tables only."""

from __future__ import annotations

import json
import sys

import numpy as np
import pytest

from rs_constraint_lab import gt0, gte4a, gtkernel


def it4(scaffold, family, grade):
    return {"alphabet": "W4", "family": family, "grade": grade, "item_id": f"SYN-HELD-{scaffold}-N4-{family}-{grade}", "mode": "HELD", "n": 4, "role": "synthetic", "scaffold": scaffold, "held": [list(e) for e in gt0.SCAFFOLDS[scaffold].held]}


def test_manifest():
    cells = gte4a.items()
    assert len(cells) == 36 and len({c["item_id"] for c in cells}) == 36
    assert sum(c["role"] == "replication_published_triangle" for c in cells) == 12


@pytest.mark.parametrize("scaffold,n,expected", [("K2", 5, (1, 9, 6, 6 / 9)), ("P3", 5, (2, 8, 6, 6 / 8)), ("K3", 5, (3, 7, 6, 6 / 7)), ("K2", 6, (1, 14, 8, 8 / 14)), ("P3", 6, (2, 13, 9, 9 / 13)), ("K3", 6, (3, 12, 9, 9 / 12))])
def test_null_geometry_table(scaffold, n, expected):
    g = gte4a.null_geometry(scaffold, n)
    assert (g["held_edges"], g["free_slots"], g["attachment_slots"]) == expected[:3]
    assert g["r0"] == pytest.approx(expected[3])


@pytest.mark.parametrize("scaffold,floor", [("K2", {0: 0, 1: 0}), ("P3", {0: 1, 1: 0, 2: 1}), ("K3", {0: 2, 1: 2, 2: 2})])
@pytest.mark.parametrize("n", [4, 5, 6])
def test_analytic_floor_and_census(scaffold, floor, n):
    assert gte4a.analytic_floor(scaffold, n) == floor
    with gt0.use_scaffold(scaffold):
        states = gtkernel.candidate_states(n, "HELD")
        census = gte4a.witness_census(states, n)
        classes = gt0.slot_classes(n)
        from rs_constraint_lab.state import edges

        for i, (a, b) in enumerate(edges(n)):
            if classes[i] == "A":
                s = a if a in gt0.source() else b
                assert (census["held_floor"][:, i] == floor[s]).all()
            if classes[i] == "P":
                assert (census["held_floor"][:, i] == 0).all()
        total = gtkernel.witness_counts(states, n, "path_form")
        assert np.array_equal(total, census["held_floor"] + census["chord_internal"] + census["other"])


def test_p3_chord_raises_witnesses_to_triangle_like():
    n = 5
    with gt0.use_scaffold("P3"):
        from rs_constraint_lab.state import edges

        E = edges(n)
        states = gtkernel.candidate_states(n, "HELD")
        census = gte4a.witness_census(states, n)
        chord = E.index((0, 2))
        present = ((states >> chord) & 1) == 1
        for s in (0, 1, 2):
            slot = E.index((s, 3))
            internal = census["held_floor"][:, slot] + census["chord_internal"][:, slot]
            assert (internal[present] == 2).all()
        assert (census["held_floor"][:, E.index((0, 3))] + census["chord_internal"][:, E.index((0, 3))])[~present].max() == 1


def test_source_orbits():
    with gt0.use_scaffold("P3"):
        assert gte4a.source_orbits(5) == [[0, 2], [1]]
    with gt0.use_scaffold("K2"):
        assert gte4a.source_orbits(5) == [[0, 1]]
    with gt0.use_scaffold("K3"):
        assert gte4a.source_orbits(5) == [[0, 1, 2]]


@pytest.mark.parametrize("scaffold", ["K2", "P3", "K3"])
@pytest.mark.parametrize("family,grade", [("NULL", "none"), ("PATHH", "weak_favour"), ("PCOMP", "weak_favour+weak_favour"), ("CLOSEW", "weak_favour")])
def test_n4_pipeline(scaffold, family, grade):
    r, _ = gte4a.analyse_item(it4(scaffold, family, grade))
    assert gte4a.check_problems(r) == []
    p = gte4a.profile(r)
    if family == "NULL":
        assert abs(p["margin_raw_ct"]) < 1e-12 and abs(p["margin_raw_jump"]) < 1e-12
    if family == "PCOMP":
        assert abs(p["margin_raw_ct"]) < 1e-12
    assert gt0.active_scaffold().name == "K3"


def test_runner_publish_atlas(tmp_path):
    plan = {"items": [it4("K2", "NULL", "none"), it4("P3", "PATHH", "weak_favour")], "plan_hash": "synthetic", "synthetic_fixture": True}
    rows = gte4a.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1, watchdogs={4: 300})
    assert [r["status"] for r in rows] == ["complete", "complete"]


def test_plan_and_refusal():
    from pathlib import Path

    from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash

    repo = Path(__file__).resolve().parents[2]
    a, b = gte4a.prepare_plan(repo), gte4a.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a) and a["items"] == gte4a.items()
    with pytest.raises(FrozenPlanError):
        gte4a.require_execution(repo, None)
