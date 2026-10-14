"""Round E2A machinery (GT-P005). Synthetic N=4 cells and synthetic factor tables only."""

from __future__ import annotations

import json
import math
import sys

import numpy as np
import pytest

from rs_constraint_lab import gte2a, gtkernel, gtobs

SYNTHETIC = {"prohibit": 0.0, "strong_suppress": 0.13, "weak_suppress": 0.41, "neutral": 1.0, "weak_favour": 2.7, "strong_favour": 6.3}


def syn(family, grade, mode="FREE", n=4):
    return {"family": family, "grade": grade, "item_id": f"SYN-{mode}-N{n}-{family}-{grade}", "mode": mode, "n": n, "stratum": "synthetic"}


def test_manifest():
    cells = gte2a.items()
    assert len(cells) == 46 and len({c["item_id"] for c in cells}) == 46
    assert {c["n"] for c in cells} == {5, 6}
    assert sum(c["n"] == 6 for c in cells) == 4 and all(c["mode"] == "HELD" for c in cells if c["n"] == 6)
    assert sum(c["mode"] == "FREE" for c in cells) == 21


def test_sigma_values():
    l2 = math.log(2)
    assert gte2a.sigma(gte2a.FAMILIES["PATHF"]["weak_suppress"]) == pytest.approx(l2)
    assert gte2a.sigma(gte2a.FAMILIES["PATHH"]["weak_suppress"]) == pytest.approx(-l2)
    assert gte2a.sigma(gte2a.FAMILIES["PFD"]["weak_suppress+weak_favour"]) == pytest.approx(2 * l2)
    assert gte2a.sigma(gte2a.FAMILIES["PFD"]["weak_favour+weak_favour"]) == 0.0
    assert gte2a.sigma(gte2a.FAMILIES["CLOSEW"]["weak_favour"]) == 0.0
    assert gte2a.sigma(gte2a.FAMILIES["PATHF"]["prohibit"]) == 0.0 and gte2a.has_hard(gte2a.FAMILIES["PATHF"]["prohibit"])


@pytest.mark.parametrize("n,mode", [(4, "FREE"), (5, "FREE"), (5, "HELD")])
@pytest.mark.parametrize("components", [[("path_form", "weak_favour")], [("path_dissolve", "strong_suppress")], [("path_form", "strong_suppress"), ("path_dissolve", "weak_favour"), ("close_form", "strong_favour"), ("adj_form", "weak_suppress")], [("path_form", "prohibit"), ("path_dissolve", "strong_favour")]])
def test_square_formula_on_synthetic_factor_tables(n, mode, components):
    chain, _ = gtkernel.reachable_chain(n, mode, components, SYNTHETIC)
    census = gte2a.square_census(chain, n, mode, components, None, SYNTHETIC)
    assert census["formula_max_abs_error"] <= 1e-12
    assert census["disjoint_max_abs_affinity"] <= 1e-12
    assert census["intact_squares"] > 0 or mode == "HELD"


def test_formula_detects_a_perturbed_rate():
    comps = [("path_dissolve", "weak_favour")]
    chain, _ = gtkernel.reachable_chain(4, "FREE", comps, SYNTHETIC)
    chain.W[5, 1] *= 1.01
    assert gte2a.square_census(chain, 4, "FREE", comps, None, SYNTHETIC)["formula_max_abs_error"] > 1e-6


def test_terminal_classes_absorbing():
    chain, _ = gtkernel.reachable_chain(4, "FREE", gte2a.FAMILIES["PATHH"]["prohibit"])
    closed = gte2a.terminal_classes(chain)
    assert len(closed) == 1 and len(closed[0]) == 1
    assert chain.rates[closed[0][0]] == 0


@pytest.mark.parametrize("family,grade", [("PATHF", "weak_suppress"), ("PATHH", "strong_suppress"), ("CLOSEW", "weak_favour"), ("PATHF", "prohibit")])
def test_partner_frame_matches_loop_reference(family, grade):
    chain, _ = gtkernel.reachable_chain(4, "FREE", gte2a.FAMILIES[family][grade])
    stat = gtobs.stationary(chain, gtobs.start_index(chain, 4, "FREE"))
    a = gte2a.partner_frame(chain, 4, stat["jump"])["index"]
    assert a == pytest.approx(gte2a.partner_frame_reference(chain, 4, stat["jump"]), abs=1e-13)


def test_partner_frame_zero_for_reversible_cell():
    chain, _ = gtkernel.reachable_chain(4, "FREE", gte2a.FAMILIES["CLOSEW"]["weak_favour"])
    stat = gtobs.stationary(chain, 0)
    assert abs(gte2a.partner_frame(chain, 4, stat["jump"])["index"]) < 1e-13


def test_hit_probabilities_match_enumeration():
    chain, _ = gtkernel.reachable_chain(4, "FREE", gte2a.FAMILIES["PATHH"]["weak_favour"])
    u = gte2a.hit_probabilities(chain, horizons=(1, 2, 3))
    for y in (0, 7, 33, 63):
        for f in range(6):
            for h in (1, 2, 3):
                assert u[h][y, f] == pytest.approx(gte2a.hit_reference_exact(chain, y, f, h), abs=1e-14)
    assert np.all(u[3] >= u[2] - 1e-15) and np.all(u[2] >= u[1] - 1e-15)


def test_matched_dissolution_finds_strict_enabling_only_with_hard_support():
    def groups(family, grade):
        chain, _ = gtkernel.reachable_chain(4, "FREE", gte2a.FAMILIES[family][grade])
        stat = gtobs.stationary(chain, 0)
        return gte2a.matched_dissolution(chain, 4, "FREE", stat["jump"])

    excl = groups("EXCL", "prohibit")
    assert any(g["enabled_share"] > 0 for g in excl.values())
    null = groups("NULL", "none")
    assert all(g["enabled_share"] == 0 and g["disabled_share"] == 0 for g in null.values())
    assert all(abs(g["mean_rate_log_ratio"]) < 1e-12 for g in null.values())
    pathh = groups("PATHH", "weak_favour")
    assert all(g["enabled_share"] == 0 for g in pathh.values())
    assert any("rate_facilitation" in g["mechanisms"] or "rate_suppression" in g["mechanisms"] for g in pathh.values())


@pytest.mark.parametrize("family,grade,mode", [("PATHF", "weak_suppress", "FREE"), ("EXCL", "prohibit", "FREE"), ("PATHF", "prohibit", "FREE"), ("NULL", "none", "HELD"), ("PATHH", "prohibit", "FREE"), ("PATHF", "prohibit", "HELD")])
def test_synthetic_cells_pass_checks_or_report_structure(family, grade, mode):
    r, _ = gte2a.analyse_item(syn(family, grade, mode), with_trajectories=False)
    if r["regime"] == "recurrent":
        assert gte2a.check_problems(r) == []
        assert r["e2a"]["squares"]["formula_max_abs_error"] <= 1e-12
    else:
        assert r["regime"] in ("absorbing", "arrested", "mixed")
        assert r["class_note"]


def test_one_way_irreversibility_without_square_affinity():
    r, _ = gte2a.analyse_item(syn("PATHF", "prohibit", "FREE"), with_trajectories=False)
    b = r["e2a"]
    assert b["one_way"]["one_way_transitions"] > 0
    assert all(v["affinity_nonzero"] == 0 for v in b["squares"]["roles"].values())


def test_assemble_on_synthetic_results():
    results = {}
    for fam, grade, mode in [("NULL", "none", "FREE"), ("PFD", "weak_suppress+weak_suppress", "FREE"), ("PATHH", "weak_favour", "FREE"), ("PATHH", "prohibit", "FREE")]:
        it = syn(fam, grade, mode)
        r, _ = gte2a.analyse_item(it, with_trajectories=False)
        results[it["item_id"]] = r
    out = gte2a.assemble(results)
    assert all(v["holds"] for k, v in out["frozen_expectations"].items() if k.startswith(("I1", "I2", "I3", "I4", "Z5")))
    assert any(t["cell"].endswith("PATHH-weak_favour") for t in out["sigma_sign_table"])


def synthetic_plan():
    return {"items": [syn("PATHF", "weak_suppress"), syn("EXCL", "prohibit"), syn("PATHH", "prohibit")], "plan_hash": "synthetic", "synthetic_fixture": True}


def test_runner_and_publish(tmp_path):
    plan = synthetic_plan()
    rows = gte2a.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1, watchdogs={4: 300})
    assert [r["status"] for r in rows] == ["complete"] * 3
    digest = gte2a.publish(tmp_path, plan, tmp_path / "t.json", frozen_plan_commit="synthetic")
    body = json.loads((tmp_path / "t.json").read_text())
    assert body["payload_sha256"] == digest and body["status_counts"] == {"complete": 3}


def test_require_execution_refuses_without_commit():
    from pathlib import Path

    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte2a.require_execution(Path(__file__).resolve().parents[2], None)


def test_plan_hash_deterministic_and_exposure_declared():
    from pathlib import Path

    from rs_constraint_lab.explore08 import plan_hash

    repo = Path(__file__).resolve().parents[2]
    a, b = gte2a.prepare_plan(repo), gte2a.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a)
    assert a["items"] == gte2a.items()
    exposed = a["pre_freeze_exposure"]["published_cells_standard_channels"]
    assert "HELD-N5-PATHF-weak_suppress" in exposed and "FREE-N5-PFD-weak_favour+weak_favour" in exposed
    assert "HELD-N5-PATHF-strong_suppress" not in exposed
