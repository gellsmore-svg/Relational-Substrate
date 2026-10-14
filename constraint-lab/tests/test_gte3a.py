"""Round E3A machinery (GT-P006). Synthetic factor tables and HELD N=4 cells only (not round cells)."""

from __future__ import annotations

import itertools
import json
import sys

import numpy as np
import pytest

from rs_constraint_lab import gte2a, gte3a, gtkernel, gtobs
from rs_constraint_lab.state import edges

SYN = {"prohibit": 0.0, "strong_suppress": 0.13, "weak_suppress": 0.6, "neutral": 1.0, "weak_favour": 1.7, "strong_favour": 5.1}
HARD = [("path_form", "prohibit"), ("path_dissolve", "weak_suppress")]


def chain_of(n, comps, mode="FREE"):
    chain, _ = gtkernel.reachable_chain(n, mode, comps, SYN)
    return chain


def test_manifest():
    cells = gte3a.items()
    assert len(cells) == 29 and len({c["item_id"] for c in cells}) == 29
    assert sum(c["kind"] == "scan" for c in cells) == 2
    assert sum(1 for c in cells if c.get("reuse")) == 8
    assert {c["n"] for c in cells} == {4, 5}


@pytest.mark.parametrize("n", [4, 5])
def test_support_theorems_on_synthetic_hard_chain(n):
    chain = chain_of(n, HARD)
    assert gtobs.class_regime(chain, 0)["irreducible"]  # T3
    bits = gte2a._bits(chain)
    wit = gte3a._witnessed(chain, n)
    E = edges(n)
    for e in range(chain.n_slots):
        X = np.nonzero(bits[:, e] == 1)[0]
        assert (chain.W[X, e] > 0).all()  # T1: dissolution always admissible
        Y = chain.T[X, e]
        one_way = chain.W[Y, e] == 0
        assert np.array_equal(one_way, wit[X, e])  # T2
        dist = gte3a.gate_distance(chain, e)
        for x, y in list(zip(X, Y))[:40]:
            s = int(chain.states[y])
            a, b = E[e]
            present = [i for i in range(chain.n_slots) if (s >> i) & 1]
            # T4: 1 + minimum dissolutions that leave e unwitnessed
            best = None
            for k in range(len(present) + 1):
                for drop in itertools.combinations(present, k):
                    t = s
                    for i in drop:
                        t &= ~(1 << i)
                    idx = np.searchsorted(chain.states, t)
                    if idx < len(chain.states) and chain.states[idx] == t and not wit[idx, e]:
                        best = k
                        break
                if best is not None:
                    break
            assert dist[y] == best + 1


def test_soft_chain_has_gate_one_everywhere():
    chain = chain_of(5, [("path_form", "strong_suppress")])
    for e in range(chain.n_slots):
        dist = gte3a.gate_distance(chain, e)
        absent = ((chain.states >> e) & 1) == 0
        assert (dist[absent] == 1).all()


def test_recovery_solve_matches_iteration():
    chain = chain_of(4, HARD)
    wit = gte3a._witnessed(chain, 4)
    for e in range(chain.n_slots):
        assert gte3a.iterative_recovery_reference(chain, e, wit[:, e]) < 1e-8


def test_direct_recovery_zero_under_hard_rule_positive_under_soft():
    hard = chain_of(4, HARD)
    soft = chain_of(4, [("path_form", "strong_suppress")])
    for chain in (hard, soft):
        wit = gte3a._witnessed(chain, 4)
        sol = gte3a.recovery_solves(chain, 0, wit[:, 0])
        absent = ((chain.states >> 0) & 1) == 0
        d = sol["direct"][absent]
        if chain is hard:
            assert np.allclose(d, 0.0)
        else:
            assert d.max() > 0


def test_partner_split_sums_to_partner_index():
    chain = chain_of(5, HARD)
    stat = gtobs.stationary(chain, 0)
    split = gte3a.partner_split(chain, 5, stat["jump"])
    total = sum(split["index_parts"].values())
    assert total == pytest.approx(gte2a.partner_frame(chain, 5, stat["jump"])["index"], abs=1e-12)
    soft = chain_of(5, [("path_form", "strong_suppress")])
    s2 = gtobs.stationary(soft, 0)
    assert gte3a.partner_split(soft, 5, s2["jump"])["index_parts"]["with_one_way"] == 0.0


def held4(family, grade, alphabet="W4"):
    return {"alphabet": alphabet, "family": family, "grade": grade, "item_id": f"SYN-HELD-N4-{alphabet}-{family}-{grade}", "kind": "cell", "mode": "HELD", "n": 4, "reuse": None, "stratum": "synthetic"}


@pytest.mark.parametrize("family,grade,alphabet", [("PF", "strong_suppress", "W16"), ("PF", "weak_suppress", "W4"), ("NULL", "none", "W4"), ("PFD", "strong_suppress+strong_suppress", "W16")])
def test_held_n4_pipeline(family, grade, alphabet):
    r, _ = gte3a.analyse_item(held4(family, grade, alphabet), with_trajectories=False)
    assert r["regime"] == "recurrent"
    assert gte3a.check_problems(r) == []
    assert "release_recovery" in r["e2a"]


def test_held_n4_hard_is_arrested():
    r, _ = gte3a.analyse_item(held4("PF", "prohibit"), with_trajectories=False)
    assert r["regime"] == "arrested"


def test_scan_on_synthetic_grid_runs():
    it = {"item_id": "SYN-SCAN", "kind": "scan", "mode": "FREE", "n": 4, "stratum": "syn", "exponents": [-1.0, 0.0, 1.0]}
    r, _ = gte3a.analyse_item(it)
    sc = r["scan"]
    assert sc["grid_points"] == 9 and sc["unresolved"] == 0
    diag = [row for row in sc["rows"] if abs(row["sigma"]) < 1e-12]
    assert all(abs(row["partner_index"]) < 1e-12 for row in diag)


def test_runner_publish_and_assemble(tmp_path):
    plan = {"items": [held4("PF", "strong_suppress", "W16"), held4("NULL", "none"), {"item_id": "SYN-SCAN", "kind": "scan", "mode": "FREE", "n": 4, "stratum": "syn", "exponents": [-1.0, 1.0]}], "plan_hash": "synthetic", "synthetic_fixture": True}
    rows = gte3a.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1, watchdogs={4: 300})
    assert [r["status"] for r in rows] == ["complete"] * 3
    gte3a.publish(tmp_path, plan, tmp_path / "t.json", frozen_plan_commit="synthetic")
    body = json.loads((tmp_path / "t.json").read_text())
    assert body["status_counts"] == {"complete": 3}
    assert "SYN-SCAN" in body["scans"]


def test_require_execution_refuses_without_commit():
    from pathlib import Path

    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte3a.require_execution(Path(__file__).resolve().parents[2], None)


def test_plan_hash_deterministic():
    from pathlib import Path

    from rs_constraint_lab.explore08 import plan_hash

    repo = Path(__file__).resolve().parents[2]
    a, b = gte3a.prepare_plan(repo), gte3a.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a) and a["items"] == gte3a.items()
    assert len(a["pre_freeze_exposure"]["published_kernels"]) == 8


def test_atlas_on_synthetic_round(tmp_path):
    plan = {"items": [held4("PF", "strong_suppress", "W16"), {"item_id": "SYN-SCAN", "kind": "scan", "mode": "FREE", "n": 4, "stratum": "syn", "exponents": [-1.0, 1.0]}], "plan_hash": "synthetic", "synthetic_fixture": True}
    gte3a.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1, watchdogs={4: 300})
    gte3a.publish(tmp_path, plan, tmp_path / "t.json", frozen_plan_commit="synthetic" * 5)
    (tmp_path / "p.json").write_text(json.dumps(plan))
    text = gte3a.render_atlas(tmp_path, tmp_path / "t.json", tmp_path / "p.json")
    assert all(it["item_id"] in text for it in plan["items"]) and "counterexample scans" in text
