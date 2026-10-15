"""E5A runner plumbing on N=4 synthetic fixtures (N=4 is not an E5A size; no E5A cell is computed)."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from rs_constraint_lab import gte5a


def fixture_item(family, grade):
    return {"components": [list(c) for c in gte5a.components(family, grade)], "family": family, "grade": grade, "item_id": f"FREE-N4-{family}-{grade}", "n": 4, "prior_cell": "synthetic fixture", "role": gte5a.ROLE.get(family, "open_scientific")}


@pytest.fixture(scope="module")
def n4_results():
    out = {}
    for f, g in gte5a.FAMILY_GRADES:
        it = fixture_item(f, g)
        out[it["item_id"]] = gte5a.analyse_item(it)
    return out


def test_manifest():
    its = gte5a.items()
    assert len(its) == 12 and len(gte5a.predicate_ids()) == 72
    assert {it["n"] for it in its} == {5, 6}
    assert {(it["family"], it["grade"]) for it in its} == set(gte5a.FAMILY_GRADES)
    assert all(it["prior_cell"].startswith("round-e0b FREE-N") for it in its)
    from rs_constraint_lab import gte4a

    assert set(gte5a.FAMILY_GRADES) == set(gte4a.FAMILY_GRADES)


def test_n4_items_have_no_numerical_problems(n4_results):
    for key, r in n4_results.items():
        assert gte5a.check_problems(r) == [], key


def test_n4_frozen_identities_hold(n4_results):
    checks = gte5a.frozen_checks(n4_results, sizes=(4,))
    assert checks, "no checks"
    for key, c in checks.items():
        assert c["holds"], (key, c)
    assert {"N0-closed-forms-N4", "N0-lag-closed-forms-N4", "ND-fixed-point-N4", "PCOMP-uniform-ct-N4", "PCOMP-ND-is-scaled-NULL-N4"} <= set(checks)


def test_n4_assembly_and_discovery_matrix(n4_results):
    published = {k: {"class_table": r["class_table"], "mean_rate_ct": r["target"]["mean_rate_ct"]} for k, r in n4_results.items()}
    t = gte5a.assemble(n4_results, published, sizes=(4,))
    assert all(v["holds"] for k, v in t["frozen_expectations"].items() if k.startswith("REP-"))
    null_row = t["predicates"]["FREE-N4-NULL-none"]["F_TRI"]
    assert null_row["vs_N0"]["pattern"] == "tie_both_clocks|turnover_tie"
    assert null_row["vs_ND"]["pattern"] == "tie_both_clocks|turnover_tie"
    for key, rows in t["predicates"].items():
        for p, row in rows.items():
            pat = row["vs_ND"]["pattern"]
            assert pat.split("|")[0] in ("longer_both_clocks", "longer_ct_only", "longer_jump_only", "tie_both_clocks", "not_longer")
            if p.startswith("I_"):
                assert pat.endswith("intact_no_turnover")
    json.dumps(t)  # serialisable


def test_runner_end_to_end_on_synthetic_plan(tmp_path):
    plan = {"items": [fixture_item("NULL", "none"), fixture_item("PATHH", "weak_favour")], "plan_hash": "synthetic", "synthetic_fixture": True}
    out = gte5a.run(tmp_path, plan, workers=2, python=sys.executable, watchdogs={4: 300}, wall_cap=600, poll=0.2)
    assert [r["status"] for r in out] == ["complete", "complete"]
    assert "secondary_residual_life" in out[1]["result"]


def test_require_execution_refuses_without_commit(tmp_path):
    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte5a.require_execution(tmp_path, None)


def test_cli_rejects_items_outside_manifest(tmp_path):
    plan = {"items": [fixture_item("NULL", "none")], "plan_hash": "x"}
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    res = subprocess.run([sys.executable, "-m", "rs_constraint_lab.gte5a", "item", "--root", str(tmp_path), "--item-id", "FREE-N4-NULL-none"], capture_output=True, text=True)
    assert res.returncode != 0 and "manifest" in res.stderr
