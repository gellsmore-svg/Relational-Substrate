"""E5D runner plumbing on N=4 synthetic fixtures (N=4 is not an E5D size; no E5D cell is computed)."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from rs_constraint_lab import gte5a, gte5d


def fixture_item(family, grade):
    return {"components": [list(c) for c in gte5a.components(family, grade)], "family": family, "grade": grade, "item_id": f"FREE-N4-{family}-{grade}", "n": 4, "prior_cell": "synthetic fixture", "role": gte5a.ROLE.get(family, "open_scientific")}


MANIFEST = [fixture_item(f, g) for f, g in gte5d.FAMILY_GRADES]


@pytest.fixture(scope="module")
def n4_results():
    return {it["item_id"]: gte5d.analyse_item(it) for it in MANIFEST}


def test_manifest():
    assert len(gte5d.items()) == 12 and len(gte5d.predicate_ids()) == 18
    assert gte5d.predicates_for(5) == ("F_TRI",) and gte5d.predicates_for(6) == ("F_TRI", "F_2PATH")
    assert all(it["prior_cell"].startswith("round-e5c FREE-N") for it in gte5d.items())


def test_n4_items_have_no_problems(n4_results):
    for key, r in n4_results.items():
        assert gte5d.check_problems(r) == [], key


def test_n4_null_fixed_point_and_assembly(n4_results):
    t = gte5d.assemble(n4_results, sizes=(4,), manifest=MANIFEST)
    assert t["frozen_checks"]["NULL_fixed_point"] == {"4": "pass"}
    row = t["predicate_rows"]["FREE-N4-PCOMP-weak_favour+weak_favour:F_TRI"]
    assert set(row) >= {"target", "N0", "ND", "NK", "NL", "vs_NL", "target_macro", "nl_reversible"}
    json.dumps(t)


def test_runner_end_to_end_on_synthetic_plan(tmp_path):
    plan = {"items": [MANIFEST[0], MANIFEST[5]], "plan_hash": "synthetic", "synthetic_fixture": True}
    out = gte5d.run(tmp_path, plan, workers=2, python=sys.executable, watchdogs={4: 300}, wall_cap=600, poll=0.2)
    assert [r["status"] for r in out] == ["complete", "complete"]
    assert "nl" in out[1]["result"]


def test_require_execution_refuses_without_commit(tmp_path):
    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte5d.require_execution(tmp_path, None)


def test_cli_rejects_items_outside_manifest(tmp_path):
    (tmp_path / "plan.json").write_text(json.dumps({"items": [MANIFEST[0]], "plan_hash": "x"}))
    res = subprocess.run([sys.executable, "-m", "rs_constraint_lab.gte5d", "item", "--root", str(tmp_path), "--item-id", "FREE-N4-NULL-none"], capture_output=True, text=True)
    assert res.returncode != 0 and "manifest" in res.stderr
