"""E5B runner plumbing on N=4 synthetic fixtures (N=4 is not an E5B size; no E5B cell is computed)."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from rs_constraint_lab import gte5a, gte5b
from rs_constraint_lab import gtrenew as R


def fixture_item(family, grade):
    return {"components": [list(c) for c in gte5a.components(family, grade)], "family": family, "grade": grade, "item_id": f"FREE-N4-{family}-{grade}", "n": 4, "prior_cell": "synthetic fixture", "role": gte5a.ROLE.get(family, "open_scientific")}


MANIFEST = [fixture_item(f, g) for f, g in gte5b.FAMILY_GRADES]


@pytest.fixture(scope="module")
def n4_results():
    return {it["item_id"]: gte5b.analyse_item(it) for it in MANIFEST}


def test_manifest():
    its = gte5b.items()
    assert len(its) == 12 and len(gte5b.predicate_ids()) == 36
    assert [(it["n"], it["family"], it["grade"]) for it in its] == [(it["n"], it["family"], it["grade"]) for it in gte5a.items()]
    assert all(it["prior_cell"].startswith("round-e5a FREE-N") for it in its)
    assert gte5b.HUB_COMMIT == "38c2501bbab22ca1eb2288ea76a962ac0170d5e6"


def test_n4_items_have_only_the_expected_problem(n4_results):
    for key, r in n4_results.items():
        # N=4 has no published E5A cell to replicate; every other check must pass
        assert gte5b.check_problems(r) == ["E5A replication not checked"], key


def test_n4_frozen_checks_and_n0_analytic_control(n4_results):
    checks = gte5b.frozen_checks(n4_results, sizes=(4,), manifest=MANIFEST)
    assert checks["N0_analytic"] == {"4": "pass"}


def test_n4_assembly_rows(n4_results):
    t = gte5b.assemble(n4_results, sizes=(4,), manifest=MANIFEST)
    assert len(t["predicate_rows"]) == 5 * 3
    row = t["predicate_rows"]["FREE-N4-PCOMP-weak_favour+weak_favour:F_TRI"]
    assert set(row) == {"target", "N0", "ND", "NK", "vs_N0", "vs_ND", "vs_NK"}
    assert row["vs_NK"]["signs"]["prevalence_ct"] in ("tie", "higher", "lower")
    json.dumps(t)


def test_nk_differs_from_nd_for_pcomp(n4_results):
    r = n4_results["FREE-N4-PCOMP-weak_favour+weak_favour"]
    assert r["pcomp_uniform_max_relative"] < 1e-9
    nd_b = r["nd_construction"]["birth"][:-1]
    nk_b = r["nk_construction"]["birth"][:-1]
    assert max(abs(a / nd_b[0] - b / nk_b[0]) for a, b in zip(nd_b, nk_b)) > 1e-6  # NK is not rescaled NULL


def test_f_star_renewal_labelled_impossible(n4_results):
    for r in n4_results.values():
        for law in ("target", "nd", "nk"):
            assert r[law]["predicates"]["F_STAR"]["replacement"]["renewal_status"] == "STRUCTURALLY_IMPOSSIBLE"


def test_runner_end_to_end_on_synthetic_plan(tmp_path):
    plan = {"items": [MANIFEST[0], MANIFEST[5]], "plan_hash": "synthetic", "synthetic_fixture": True}
    out = gte5b.run(tmp_path, plan, workers=2, python=sys.executable, watchdogs={4: 300}, wall_cap=600, poll=0.2)
    assert [r["status"] for r in out] == ["complete", "complete"]
    assert "nk" in out[1]["result"]


def test_require_execution_refuses_without_commit(tmp_path):
    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte5b.require_execution(tmp_path, None)


def test_cli_rejects_items_outside_manifest(tmp_path):
    plan = {"items": [MANIFEST[0]], "plan_hash": "x"}
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    res = subprocess.run([sys.executable, "-m", "rs_constraint_lab.gte5b", "item", "--root", str(tmp_path), "--item-id", "FREE-N4-NULL-none"], capture_output=True, text=True)
    assert res.returncode != 0 and "manifest" in res.stderr


def test_observer_is_not_read_by_rules():
    """Static guard: the renewal module never touches kernel construction."""
    import inspect

    src = inspect.getsource(R)
    assert "gtkernel" not in src and "gtkernel.weights" not in src and "reachable_chain" not in src
