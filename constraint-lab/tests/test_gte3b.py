"""Round E3B machinery (GT-P006). HELD N=4 cells only (not round cells)."""

from __future__ import annotations

import json
import sys

import numpy as np
import pytest

from rs_constraint_lab import gte2a, gte3b, gtkernel


def it4(family, grade):
    return {"family": family, "grade": grade, "item_id": f"SYN-HELD-N4-{family}-{grade}", "mode": "HELD", "n": 4}


def test_manifest():
    cells = gte3b.items()
    assert len(cells) == 18 and {c["n"] for c in cells} == {5, 6}


def test_t7_internal_witnesses_on_n4_states():
    chain, _ = gtkernel.reachable_chain(4, "HELD", gte3b.FAMILIES["PATHF"]["weak_suppress"])
    iw = gte3b.internal_witnesses(chain.states, 4)
    classes = gte2a.slot_classes(4, "HELD")
    for e, c in enumerate(classes):
        if c == "A":
            assert (iw[:, e] == 2).all()
        else:
            assert (iw[:, e] == 0).all()


@pytest.mark.parametrize("family,grade", [("PATHF", "weak_suppress"), ("PATHH", "weak_favour"), ("CSPH", "strong_favour+weak_favour"), ("PCOMP", "weak_favour+weak_favour")])
def test_t8_affinities_unchanged_by_neutralisation(family, grade):
    comps = gte3b.FAMILIES[family][grade]
    chain, _ = gtkernel.reachable_chain(4, "HELD", comps)
    neut = gte3b.neutralised(chain, 4, comps)
    assert gte3b.square_affinity_difference(chain, neut) <= 1e-12
    classes = np.array([c == "A" for c in gte2a.slot_classes(4, "HELD")])
    assert np.allclose(chain.W[:, ~classes], neut.W[:, ~classes])
    assert not np.allclose(chain.W[:, classes], neut.W[:, classes])


def test_affinity_difference_detects_a_change():
    comps = gte3b.FAMILIES["PATHH"]["weak_favour"]
    chain, _ = gtkernel.reachable_chain(4, "HELD", comps)
    other, _ = gtkernel.reachable_chain(4, "HELD", gte3b.FAMILIES["PATHH"]["weak_suppress"])
    assert gte3b.square_affinity_difference(chain, other) >= 0.0


@pytest.mark.parametrize("family,grade", [("CLOSEW", "weak_favour"), ("NULL", "none"), ("PATHF", "weak_suppress"), ("PCOMP", "weak_favour+weak_favour")])
def test_analyse_item_n4(family, grade):
    r, _ = gte3b.analyse_item(it4(family, grade))
    assert r["t7_two_internal_witnesses_on_every_attachment"]
    assert r["square_affinity_max_change"] <= 1e-12
    assert gte3b.check_problems(r) == []
    if family in ("CLOSEW", "NULL"):
        assert max(abs(v) for v in r["delta"].values()) <= 1e-12
    if family == "PCOMP":
        assert max(abs(v) for v in r["delta"].values()) <= 1e-9


def test_runner_publish_atlas(tmp_path):
    plan = {"items": [it4("PATHF", "weak_suppress"), it4("NULL", "none")], "plan_hash": "synthetic", "synthetic_fixture": True}
    rows = gte3b.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1, watchdogs={4: 300})
    assert [r["status"] for r in rows] == ["complete", "complete"]
    gte3b.publish(tmp_path, plan, tmp_path / "t.json", frozen_plan_commit="synthetic" * 5)
    text = gte3b.render_atlas(tmp_path, tmp_path / "t.json")
    assert all(it["item_id"] in text for it in plan["items"])


def test_plan_and_refusal():
    from pathlib import Path

    from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash

    repo = Path(__file__).resolve().parents[2]
    a, b = gte3b.prepare_plan(repo), gte3b.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a) and a["items"] == gte3b.items()
    with pytest.raises(FrozenPlanError):
        gte3b.require_execution(repo, None)
