"""Round E1 machinery (GT-P004). Synthetic N=4 cells and published N=5 W4 cells only."""

from __future__ import annotations

import json
import sys

import numpy as np
import pytest

from rs_constraint_lab import gte0b, gte1, gtkernel, gtobs
from rs_constraint_lab.weights import alphabet_factors


def synthetic_item(family: str, alphabet: str = "W4", n: int = 4) -> dict:
    return {"alphabet": alphabet, "family": family, "grade": gte1.grade_of(family), "item_id": f"SYN-N{n}-{alphabet}-{family}", "mode": "HELD", "n": n, "role": "synthetic", "tranche": "synthetic"}


# --- manifest -------------------------------------------------------------------------------------


def test_manifest_is_option_b():
    cells = gte1.items()
    authorised = gte1.authorised_cells()
    assert len(cells) == 48 and len(authorised) == 32
    tranche1 = [c for c in cells if c["tranche"] == "I"]
    tranche2 = [c for c in cells if c["tranche"] == "II"]
    baseline = [c for c in cells if c["tranche"] == "baseline"]
    assert len(tranche1) == 8 and {c["n"] for c in tranche1} == {7} and {c["alphabet"] for c in tranche1} == {"W4"}
    assert len(tranche2) == 24 and {c["n"] for c in tranche2} == {5, 6} and {c["alphabet"] for c in tranche2} == {"W3", "W16"}
    assert {c["family"] for c in tranche2} == set(gte1.NON_GRADIENT)
    assert len(baseline) == 16 and {c["alphabet"] for c in baseline} == {"W4"} and {c["role"] for c in baseline} == {"baseline_rederivation_published"}
    assert {c["mode"] for c in cells} == {"HELD"}
    assert len({c["item_id"] for c in cells}) == 48
    roles = {c["family"]: c["role"] for c in tranche1}
    assert roles["NULL"] == "identity_control_exposed" and roles["CLOSEW"] == "gradient_control"
    assert {f for f, r in roles.items() if r == "open_scientific"} == set(gte1.NON_GRADIENT)


def test_families_and_grades_are_the_e0b_definitions():
    expected = {"CSPH": "strong_favour+weak_favour", "CSPF": "strong_favour+weak_suppress", "CWPH": "weak_favour+weak_favour", "CWPF": "weak_favour+weak_suppress", "PATHF": "weak_suppress", "PATHH": "weak_favour", "NULL": "none", "CLOSEW": "weak_favour"}
    for family, grade in expected.items():
        assert gte1.grade_of(family) == grade
        assert gte1.FAMILIES[family][grade] == gte0b.FAMILIES[family][grade]


def test_alphabet_log_strengths():
    assert gte1.log_strength("W4") == pytest.approx(1.0)
    assert gte1.log_strength("W3") == pytest.approx(np.log2(3))
    assert gte1.log_strength("W16") == pytest.approx(2.0)


# --- handover index -------------------------------------------------------------------------------


def test_handover_index_signs_and_steps():
    forward = {("F", "P", "F", "A", "adjacent"): 0.3, ("D", "A", "D", "P", "adjacent"): 0.1, ("F", "A", "D", "P", "adjacent"): 0.2, ("F", "P", "D", "A", "adjacent"): 0.05}
    h = gte1.handover_statistics(forward)
    assert h["index_adjacent"] == pytest.approx(0.2 + 0.15)
    assert h["forward_oriented_adjacent_steps"] == 2
    reverse = {(gte1.FLIP[t2], c2, gte1.FLIP[t1], c1, rel): v for (t1, c1, t2, c2, rel), v in forward.items()}
    assert gte1.handover_statistics(reverse)["index_adjacent"] == pytest.approx(-0.35)
    assert gte1.handover_statistics({})["index_all"] == 0.0


def test_handover_index_zero_for_reversible_cell():
    item = synthetic_item("CLOSEW", n=5)
    chain, _ = gtkernel.reachable_chain(5, "HELD", gte1.FAMILIES["CLOSEW"]["weak_favour"])
    stat = gtobs.stationary(chain, gtobs.start_index(chain, 5, "HELD"))
    h = gte1.handover_statistics(gtobs.event_pattern_probabilities(chain, stat["jump"], 5, "HELD"))
    assert abs(h["index_all"]) < 1e-12
    assert item["family"] == "CLOSEW"


def test_event_order_unchanged_by_refactor():
    chain, _ = gtkernel.reachable_chain(5, "HELD", gte1.FAMILIES["CSPH"]["strong_favour+weak_favour"])
    stat = gtobs.stationary(chain, gtobs.start_index(chain, 5, "HELD"))
    eo = gtobs.event_order(chain, stat["jump"], 5, "HELD")
    probs = gtobs.event_pattern_probabilities(chain, stat["jump"], 5, "HELD")
    assert sum(probs.values()) == pytest.approx(1.0)
    assert eo["immediate_reversal_probability"] == pytest.approx(sum(v for k, v in probs.items() if k[4] == "same"))


# --- classification rules -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "c5w4,c5w16,c6w4,expected",
    [
        (0.0, 0.1, 0.1, "same_sign_comparable_size"),
        (0.0, 0.5, 0.1, "same_sign_different_size"),
        (0.0, -0.1, 0.1, "opposite"),
        (0.0, 0.0001, 0.1, "strength_step_negligible"),
        (0.0, 0.1, 0.0001, "size_step_negligible"),
        (0.0, 0.0001, 0.0002, "both_negligible"),
        (None, 0.1, 0.1, "unavailable"),
    ],
)
def test_calibration_classes(c5w4, c5w16, c6w4, expected):
    assert gte1.classify_calibration(c5w4, c5w16, c6w4)["class"] == expected


def test_proxy_verdicts():
    rows = lambda classes: {str(i): {"class": c} for i, c in enumerate(classes)}
    assert gte1.proxy_verdict(rows(["same_sign_comparable_size"] * 2 + ["opposite"]))["verdict"] == "usable_proxy"
    assert gte1.proxy_verdict(rows(["same_sign_different_size"] * 2 + ["opposite"]))["verdict"] == "direction_only_proxy"
    assert gte1.proxy_verdict(rows(["opposite"] * 2 + ["same_sign_comparable_size"]))["verdict"] == "poor_proxy"
    assert gte1.proxy_verdict(rows(["size_step_negligible", "both_negligible"]))["verdict"] == "no_non_negligible_size_step"


@pytest.mark.parametrize(
    "c6w4,c6w3,c6w16,c7w4,expected",
    [
        (0.0, 0.05, 0.1, 0.07, "same_sign_within_bracket_range"),
        (0.0, 0.05, 0.1, 0.5, "same_sign_outside_bracket_range"),
        (0.0, 0.05, 0.1, -0.07, "opposite_to_strength_response"),
        (0.0, 0.05, -0.1, 0.07, "strength_response_non_monotone"),
        (0.0, 0.0001, 0.0002, 0.07, "no_strength_response"),
        (0.0, 0.05, 0.1, 0.0001, "size_step_negligible"),
        (0.0, 0.0001, 0.1, 0.07, "same_sign_within_bracket_range"),
        (0.0, None, 0.1, 0.07, "unavailable"),
    ],
)
def test_n7_reading_classes(c6w4, c6w3, c6w16, c7w4, expected):
    assert gte1.classify_n7(c6w4, c6w3, c6w16, c7w4)["class"] == expected


# --- numerical checks -----------------------------------------------------------------------------


@pytest.mark.parametrize("alphabet", ["W4", "W3", "W16"])
@pytest.mark.parametrize("family", ["CSPH", "PATHF", "CLOSEW", "NULL"])
def test_synthetic_cell_passes_every_check(alphabet, family):
    result, _ = gte1.analyse_item(synthetic_item(family, alphabet), with_trajectories=False)
    assert gte1.check_problems(result) == []
    assert result["e1_round"]["checks"]["kernel_sample"]["sampled_states"] == result["reachable_states"]
    assert result["spectrum"] is None and result["spectrum_status"].startswith("unavailable")
    profile = gte1.channels(result)
    assert set(gte1.DECLARED_CHANNELS) <= set(profile)


def test_kernel_sample_check_detects_a_wrong_weight():
    item = synthetic_item("PATHF", "W16", n=5)
    chain, _ = gtkernel.reachable_chain(5, "HELD", gte1.FAMILIES["PATHF"]["weak_suppress"], alphabet_factors("W16"))
    start = gtobs.start_index(chain, 5, "HELD")
    assert gte1.kernel_sample_check(item, chain, start)["max_relative_weight_difference"] <= gte1.KERNEL_RELATIVE_TOLERANCE
    chain.W[start, 5] *= 1.0 + 1e-9
    assert gte1.kernel_sample_check(item, chain, start)["max_relative_weight_difference"] > gte1.KERNEL_RELATIVE_TOLERANCE


def test_long_double_residual_detects_clipping_and_error():
    chain, _ = gtkernel.reachable_chain(5, "HELD", gte1.FAMILIES["CSPH"]["strong_favour+weak_favour"])
    stat = gtobs.stationary(chain, gtobs.start_index(chain, 5, "HELD"))
    good = gte1.long_double_residual(chain, stat["jump"])
    assert good["zero_mass_states"] == 0 and good["max_relative"] < 1e-12
    bad = stat["jump"].copy()
    bad[int(np.argmin(bad))] = 0.0
    assert gte1.long_double_residual(chain, bad)["zero_mass_states"] == 1
    perturbed = stat["jump"].copy()
    perturbed[3] *= 1 + 1e-6
    assert gte1.long_double_residual(chain, perturbed)["max_relative"] > gte1.RESIDUAL_MAX_RELATIVE


def test_null_profile_is_the_identity():
    result, _ = gte1.analyse_item(synthetic_item("NULL", n=5), with_trajectories=False)
    p = gte1.channels(result)
    for name in ("margin_raw_ct", "margin_raw_jump", "margin_standardised_ct", "margin_standardised_jump", "irreversible_flux_fraction", "handover_index_adjacent"):
        assert abs(p[name]) < 1e-12, name


def test_published_baseline_replicates():
    tables = json.loads((gte1_repo() / gte1.E0B_TABLES_RELPATH).read_text())["results"]
    item = next(i for i in gte1.items() if i["item_id"] == "HELD-N5-W4-PATHH-weak_favour")
    result, _ = gte1.analyse_item(item, with_trajectories=False)
    check = gte1.replication_check(result, tables["HELD-N5-PATHH-weak_favour"])
    assert check["holds"], check


def gte1_repo():
    from pathlib import Path

    return Path(__file__).resolve().parents[2]


def test_assemble_tolerates_partial_and_unresolved_results():
    results = {}
    for family in ("CSPH", "NULL", "CLOSEW"):
        item = synthetic_item(family, n=5)
        r, _ = gte1.analyse_item(item, with_trajectories=False)
        r["item_id"] = gte1.item_id(5, "W4", family)
        results[r["item_id"]] = r
    results["X"] = {"family": "PATHF", "grade": "weak_suppress", "n": 5, "alphabet": "W3", "item_id": "X", "regime": "recurrent", "stationary": {"resolved": False, "reason": "iteration cap reached"}}
    out = gte1.assemble(results, {})
    assert out["frozen_expectations"]["Z5-X"]["holds"] is False
    assert out["frozen_expectations"][f"Z1-{gte1.item_id(5, 'W4', 'NULL')}"]["holds"]
    assert out["frozen_expectations"][f"Z2-{gte1.item_id(5, 'W4', 'CLOSEW')}"]["holds"]
    assert out["calibration_n5w16_vs_n6w4"]["CSPH"]["verdict"] == "no_non_negligible_size_step"
    assert out["n7_against_n6_strength_response"]["PATHF"]["class_counts"] == {"unavailable": len(gte1.DECLARED_CHANNELS)}


# --- plan and runner ------------------------------------------------------------------------------


def test_plan_hash_is_deterministic_and_contract_holds():
    from rs_constraint_lab.explore08 import plan_hash

    repo = gte1_repo()
    a, b = gte1.prepare_plan(repo), gte1.prepare_plan(repo)
    assert a["plan_hash"] == b["plan_hash"] == plan_hash(a)
    assert a["items"] == gte1.items()
    assert a["work_count"]["authorised_cells"] == 32
    assert "free_n7" in a["deliberate_omissions"] and "spectrum" in a["deliberate_omissions"]
    assert set(a["pre_freeze_exposure"]["reference_hashes"]) == set(gte1.REFERENCE_FILES)


def test_require_execution_refuses_without_a_frozen_commit():
    from rs_constraint_lab.explore08 import FrozenPlanError

    with pytest.raises(FrozenPlanError):
        gte1.require_execution(gte1_repo(), None)
    with pytest.raises(FrozenPlanError):
        gte1.require_execution(gte1_repo(), "0" * 40)


def synthetic_plan(families=("CSPH", "PATHH", "NULL")) -> dict:
    return {"items": [synthetic_item(f) for f in families], "plan_hash": "synthetic", "synthetic_fixture": True}


def test_runner_completes_and_resumes(tmp_path):
    plan = synthetic_plan()
    rows = gte1.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1)
    assert [r["status"] for r in rows] == ["complete"] * 3
    assert all(r["peak_rss_mb"] > 0 and r["wall_seconds"] > 0 for r in rows)
    assert all(not (tmp_path / "items" / f"{it['item_id']}.partial.json").exists() for it in plan["items"])
    stamps = [(tmp_path / "items" / f"{it['item_id']}.json").stat().st_mtime_ns for it in plan["items"]]
    gte1.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1)
    assert stamps == [(tmp_path / "items" / f"{it['item_id']}.json").stat().st_mtime_ns for it in plan["items"]]
    status = json.loads((tmp_path / "status.json").read_text())
    assert status["completed_items"] == 3 and status["running"] == []


def test_runner_refuses_a_directory_of_another_plan(tmp_path):
    gte1.run(tmp_path, synthetic_plan(("NULL",)), workers=1, python=sys.executable, poll=0.1)
    other = synthetic_plan(("NULL",))
    other["plan_hash"] = "different"
    with pytest.raises(RuntimeError):
        gte1.run(tmp_path, other, workers=1, python=sys.executable, poll=0.1)


def test_runner_watchdog_records_unresolved(tmp_path):
    rows = gte1.run(tmp_path, synthetic_plan(("CSPH",)), workers=1, python=sys.executable, watchdogs={4: 0.0}, poll=0.05)
    assert rows[0]["status"] in ("unresolved_watchdog", "complete_checks_interrupted")
    if rows[0]["status"] == "unresolved_watchdog":
        assert rows[0]["watchdog_seconds"] == 0.0


def test_runner_wall_cap_stops_and_records(tmp_path):
    rows = gte1.run(tmp_path, synthetic_plan(), workers=1, python=sys.executable, wall_cap=-1.0, poll=0.05)
    assert {r["status"] for r in rows} == {"not_started_wall_cap"}


def test_publish_on_synthetic_round(tmp_path):
    plan = synthetic_plan(("CSPH", "NULL"))
    gte1.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1)
    out = tmp_path / "tables.json"
    digest = gte1.publish(tmp_path, plan, out, frozen_plan_commit="synthetic", e0b_tables=gte1_repo() / gte1.E0B_TABLES_RELPATH)
    body = json.loads(out.read_text())
    assert body["payload_sha256"] == digest
    assert body["status_counts"] == {"complete": 2}
    assert all(r["numerical_problems"] == [] for r in body["item_records"].values())


def test_atlas_renders_every_item_of_a_synthetic_round(tmp_path):
    from rs_constraint_lab import gte1_atlas

    plan = synthetic_plan(("CSPH", "NULL"))
    gte1.run(tmp_path, plan, workers=2, python=sys.executable, poll=0.1)
    gte1.publish(tmp_path, plan, tmp_path / "tables.json", frozen_plan_commit="synthetic" * 5, e0b_tables=gte1_repo() / gte1.E0B_TABLES_RELPATH)
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    text = gte1_atlas.build(gte1_repo(), tmp_path / "tables.json", tmp_path / "plan.json")
    assert all(it["item_id"] in text for it in plan["items"])
    assert "unavailable" in text and "Z5" in text


def test_runner_survives_a_child_reaped_elsewhere(tmp_path, monkeypatch):
    """Regression (CI run 38592301540): a child reaped by subprocess's own cleanup made os.wait4 raise ECHILD."""
    import os

    real = os.wait4
    seen: set[int] = set()

    def flaky(pid, flags):
        if pid not in seen:
            seen.add(pid)
            real(pid, 0)
            raise ChildProcessError(10, "No child processes")
        return real(pid, flags)

    monkeypatch.setattr(os, "wait4", flaky)
    rows = gte1.run(tmp_path, synthetic_plan(("NULL", "CSPH")), workers=2, python=sys.executable, poll=0.05)
    assert [r["status"] for r in rows] == ["complete", "complete"]
