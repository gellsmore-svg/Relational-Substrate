"""Round E2B machinery (GT-P005). Synthetic N=4 cells only."""

from __future__ import annotations

import json
import sys

import numpy as np
import pytest

from rs_constraint_lab import gte2a, gte2b, gtkernel, gtobs


def syn(hard, soft, mode="FREE", n=4):
    fam, grade = gte2b.family_name(hard, soft), gte2b.grade_name(hard, soft)
    return {"family": fam, "grade": grade, "hard": hard, "item_id": f"SYN-{mode}-N{n}-{fam}-{grade}", "mode": mode, "n": n, "soft": soft}


def test_manifest():
    cells = gte2b.items()
    assert len(cells) == 18 and len({c["item_id"] for c in cells}) == 18
    assert {c["n"] for c in cells} == {5}
    assert not set(gte2b.CELLS) & set(gte2b.CITED_FROM_E2A)
    assert all(gte2b.FAMILIES[c["family"]][c["grade"]][0] == gte2b.HARD[c["hard"]] for c in cells)


def test_race_matches_dense_solve():
    chain, _ = gtkernel.reachable_chain(4, "FREE", [("path_dissolve", "weak_favour")])
    P = chain.W / chain.rates[:, None]
    f, g = 0, 3
    h, it = gte2b.race_values(chain, f, g)
    size = len(chain.states)
    A = np.eye(size)
    b = P[:, f].copy()
    for e in range(chain.n_slots):
        if e in (f, g):
            continue
        for y in range(size):
            A[y, chain.T[y, e]] -= P[y, e]
    ref = np.linalg.solve(A, b)
    assert np.allclose(h, ref, atol=1e-12) and it < gte2b.RACE_CAP


@pytest.mark.parametrize("hard,soft", [("HAF", "none"), ("HAF", "PDwf"), ("HPF", "PDws"), ("HCF", "PFwf")])
@pytest.mark.parametrize("mode", ["FREE", "HELD"])
def test_synthetic_cells(hard, soft, mode):
    r, _ = gte2b.analyse_item(syn(hard, soft, mode), with_trajectories=False)
    if r["regime"] == "recurrent" and r["stationary"].get("resolved"):
        assert gte2b.check_problems(r) == []
        b = r["e2a"]
        assert 0.0 <= b["one_way_flux"]["share_of_total_flux"] <= 1.0
        for g in b["race"]["groups"].values():
            for k in ("race_from_x_minus_all", "race_from_x_minus_enabled", "race_from_x_with_g"):
                assert g[k] is None or -1e-12 <= g[k] <= 1 + 1e-12
    else:
        assert r["class_note"]


def test_hard_gradient_alone_is_reversible_without_one_way():
    r, _ = gte2b.analyse_item(syn("HAF", "none", "FREE"), with_trajectories=False)
    assert r["reversibility"]["irreversible_flux_fraction"] < 1e-12
    assert r["e2a"]["one_way"]["one_way_transitions"] == 0


def test_runner_and_publish(tmp_path):
    plan = {"items": [syn("HAF", "PDwf"), syn("HPF", "PDws")], "plan_hash": "synthetic", "synthetic_fixture": True}
    rows = gte2b.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1, watchdogs={4: 300})
    assert [r["status"] for r in rows] == ["complete", "complete"]
    gte2b.publish(tmp_path, plan, tmp_path / "t.json", frozen_plan_commit="synthetic")
    body = json.loads((tmp_path / "t.json").read_text())
    assert body["status_counts"] == {"complete": 2}


def test_require_execution_refuses_without_commit():
    from pathlib import Path

    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte2b.require_execution(Path(__file__).resolve().parents[2], None)


def test_plan_hash_deterministic():
    from pathlib import Path

    from rs_constraint_lab.explore08 import plan_hash

    repo = Path(__file__).resolve().parents[2]
    a, b = gte2b.prepare_plan(repo), gte2b.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a) and a["items"] == gte2b.items()
