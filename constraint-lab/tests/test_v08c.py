"""Generation 8C mechanism contracts.

These tests check closed forms, topology, and execution refusal.
They do not publish the Round C0 tables, and they do not pin the C0 plan
hash. That pin belongs with the journey line that names the result commit.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.explore08a import repository_root
from rs_constraint_lab.explore08c import (
    CHECKPOINT_REPRODUCTION_TOLERANCE,
    CLOSED_FORM_TOLERANCE,
    PUBLISHED_BALANCED_CMI,
    MechanismError,
    action_on_source,
    active_six,
    analytic_balanced_cmi,
    asymmetry_table,
    checkpoint_source,
    contribution_atlas,
    drift_report,
    excursion_report,
    gate_memory_curve,
    hierarchy_report,
    projection_counterfactual,
    projection_report,
    r05_local_law,
    single_rule_local_law,
    symmetry_report,
    topology_atlas,
    topology_shape_summary,
    w4_factors,
)
from rs_constraint_lab.gen008c_exec import (
    PARENT_TABLES_RELPATH,
    PLAN_RELPATH,
    c0_items,
    execute_plan_item,
    prepare_c0_plan,
    require_c0_execution,
)
from rs_constraint_lab.graphs import pair_classes

REPO = repository_root()
SRC = REPO / "constraint-lab" / "src" / "rs_constraint_lab"
PARENT = REPO / PARENT_TABLES_RELPATH
GIT_ENV = {
    "GIT_AUTHOR_NAME": "gellsmore-svg",
    "GIT_AUTHOR_EMAIL": "gellsmore@googlemail.com",
    "GIT_COMMITTER_NAME": "gellsmore-svg",
    "GIT_COMMITTER_EMAIL": "gellsmore@googlemail.com",
}


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(GIT_ENV)
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )


def _commit_plan(repo: Path, document: dict, relative: str) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    atomic_write_json(repo / relative, document)
    _git(repo, "init")
    _git(repo, "add", relative)
    _git(repo, "commit", "-m", "freeze test plan")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _cell(tables: dict, system_id: str, weighting: str, conditioner: str, outcome: str) -> float:
    for row in tables["current_context"]:
        if (
            row["system_id"] == system_id
            and row["weighting"] == weighting
            and row["conditioner"] == conditioner
            and row["outcome"] == outcome
        ):
            return row["exact_law_CMI"]
    raise AssertionError(f"missing 8B cell {system_id} {weighting} {conditioner} {outcome}")


def _checkpoint(tables: dict, system_id: str, source: str) -> dict:
    for row in tables["checkpoints"]:
        if row["system_id"] == system_id and row["source_graph_class"] == source and row["checkpoint"] == 1:
            return row
    raise AssertionError(f"missing 8B checkpoint {system_id} {source}")


@pytest.fixture(scope="module")
def tables() -> dict:
    return json.loads(PARENT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def laws() -> dict[str, dict]:
    rows = {system_id: single_rule_local_law(system_id) for system_id in ("R01", "R02", "R04", "R06")}
    rows["R05"] = r05_local_law()
    return rows


@pytest.fixture(scope="module")
def shapes() -> dict:
    rows = topology_atlas()
    return {"rows": rows, "summary": topology_shape_summary(rows)}


@pytest.fixture(scope="module")
def checkpoints() -> dict[tuple[str, str], dict]:
    wanted = (
        ("R00", "path"),
        ("R01", "path"),
        ("R01", "star"),
        ("R02", "path"),
        ("R04", "path"),
        ("R06", "path"),
        ("R06", "star"),
    )
    return {key: checkpoint_source(*key) for key in wanted}


@pytest.fixture(scope="module")
def memory() -> dict[tuple[str, str], list[dict]]:
    return {key: gate_memory_curve(*key) for key in (("R00", "path"), ("R01", "path"), ("R06", "path"))}


@pytest.fixture(scope="module")
def atlases() -> dict[str, dict]:
    return {system_id: contribution_atlas(system_id) for system_id in ("R00", "R01", "R05", "R06")}


@pytest.fixture(scope="module")
def projections() -> dict[str, dict]:
    return {system_id: projection_report(system_id) for system_id in ("R01", "R06")}


@pytest.fixture(scope="module")
def drifts() -> dict[str, dict]:
    return {system_id: drift_report(system_id) for system_id in ("R01", "R02", "R03", "R04", "R06", "R07")}


def test_w4_grades_and_closed_form_slot_law() -> None:
    factors = w4_factors()
    assert factors["strong_suppress"] == Fraction(1, 4)
    assert factors["strong_favour"] == Fraction(4)
    inactive = [Fraction(1, 6)] * 6
    suppress = active_six(Fraction(1, 4), 0)
    favour = active_six(Fraction(4), 0)
    assert suppress[0] == Fraction(1, 21)
    assert suppress[1] == Fraction(4, 21)
    assert favour[0] == Fraction(4, 9)
    assert favour[1] == Fraction(1, 9)
    assert inactive[0] == Fraction(1, 6)
    assert abs(analytic_balanced_cmi(Fraction(1, 4)) - PUBLISHED_BALANCED_CMI["suppress"]) < 1e-15
    assert abs(analytic_balanced_cmi(Fraction(4)) - PUBLISHED_BALANCED_CMI["favour"]) < 1e-15
    assert abs(analytic_balanced_cmi(Fraction(1, 4)) - analytic_balanced_cmi(Fraction(4))) > 1e-3


def test_single_rule_enumeration_matches_the_closed_form(laws: dict[str, dict]) -> None:
    for system_id in ("R01", "R02", "R04"):
        assert laws[system_id]["gap"] < CLOSED_FORM_TOLERANCE
        assert laws[system_id]["multiplier"] == "1/4"
        assert laws[system_id]["minimal_state_coordinates"] == ["rule_active"]
        assert laws[system_id]["raw_sufficient_coordinates"] == ["action_edge_bit", "condition_triad_bit"]
        proof = laws[system_id]["state_count_proof"]
        assert proof["inactive_is_uniform"] is True
        assert proof["active_matches_closed_form"] is True
        assert proof["other_bits_irrelevant"] is True
        assert proof["active_state_count"] == 256
        assert proof["mask_weight_is_one_half"] is True
        assert proof["gate_weight_is_one_half"] is True
        assert proof["exact_weight_gap"] == "0/1"
    values = [laws[system_id]["enumerated_balanced_CMI"] for system_id in ("R01", "R02", "R04")]
    assert max(values) - min(values) < CLOSED_FORM_TOLERANCE
    assert laws["R06"]["gap"] < CLOSED_FORM_TOLERANCE
    assert laws["R06"]["enumerated_balanced_CMI"] > 2 * laws["R01"]["enumerated_balanced_CMI"]
    assert abs(laws["R01"]["enumerated_balanced_CMI"] - _cell_from_law(laws["R01"])) < CLOSED_FORM_TOLERANCE


def _cell_from_law(row: dict) -> float:
    return row["analytic_balanced_CMI"]


def test_balanced_cmi_reproduces_generation_8b(laws: dict[str, dict], tables: dict) -> None:
    for system_id in ("R01", "R02", "R04", "R06", "R05"):
        published = _cell(tables, system_id, "balanced_law", "full_pair_mask", "next_pair_slot")
        assert abs(laws[system_id]["enumerated_balanced_CMI"] - published) < 1e-12
    assert laws["R05"]["gap"] < 1e-12
    assert laws["R05"]["formula_fraction_gap"] == "0/1"
    assert laws["R05"]["weight_fraction_gap"] == "0/1"
    assert laws["R05"]["groups_constant"] is True
    assert laws["R05"]["multiplier"] == "1/4;1/4"
    assert len(laws["R05"]["minimal_state_coordinates"]) == 3
    assert laws["R05"]["enumerated_balanced_CMI"] > laws["R01"]["enumerated_balanced_CMI"]


def test_suppress_and_favour_are_not_reciprocal_in_information() -> None:
    rows = {row["grade"]: row for row in asymmetry_table()}
    assert abs(rows["strong_suppress"]["total_variation_from_uniform"] - 5 / 42) < 1e-12
    assert abs(rows["strong_favour"]["total_variation_from_uniform"] - 5 / 18) < 1e-12
    assert rows["strong_favour"]["balanced_CMI"] > rows["strong_suppress"]["balanced_CMI"]
    assert rows["strong_favour"]["action_slot_probability"] > 1 / 6
    assert rows["strong_suppress"]["action_slot_probability"] < 1 / 6


def test_one_step_atlas_separates_path_from_star_and_triangle(shapes: dict) -> None:
    rows = shapes["rows"]
    assert len(rows) == 18
    table = pair_classes()
    for source in ("star", "path", "triangle"):
        selected = [row for row in rows if row["source_graph"] == source]
        assert len(selected) == 6
        assert {row["slot"] for row in selected} == set(range(6))
    for row in rows:
        result = row["source_mask"] ^ (1 << row["slot"])
        assert row["result_edge_count"] == result.bit_count()
        assert row["result_graph_class"] == table.name_of[result]
    summary = shapes["summary"]
    assert summary["star"]["one_class_per_edge_count"] is True
    assert summary["triangle"]["one_class_per_edge_count"] is True
    assert summary["path"]["one_class_per_edge_count"] is False
    assert len(summary["path"]["classes_by_edge_count"]["2"]) == 2
    assert len(summary["path"]["classes_by_edge_count"]["4"]) == 2
    assert summary["path"]["categories"] == {
        "path_end": 2,
        "path_long_chord": 1,
        "path_middle": 1,
        "path_short_chord": 2,
    }


def test_action_slot_is_admissible_only_for_dissolve_0_1_on_canonical_sources() -> None:
    for system_id in ("R01", "R06"):
        rows = action_on_source(system_id)
        assert len(rows) == 3
        assert all(row["action_admissible_on_source"] for row in rows)
        by_source = {row["source_graph"]: row["slot_topology_category"] for row in rows}
        assert by_source["path"] == "path_middle"
        assert by_source["star"] == "spoke"
        assert by_source["triangle"] == "triangle_edge"
    for system_id in ("R02", "R04"):
        assert all(not row["action_admissible_on_source"] for row in action_on_source(system_id))


def test_checkpoint_1_reproduces_the_epoch_kernel(checkpoints: dict, tables: dict) -> None:
    for system_id, source in (("R01", "path"), ("R06", "path"), ("R01", "star"), ("R06", "star")):
        got = checkpoints[(system_id, source)]["epoch_mi"]
        parent = _checkpoint(tables, system_id, source)
        assert abs(got["class_information"] - parent["exact_class_MI"]) < CHECKPOINT_REPRODUCTION_TOLERANCE
        assert abs(got["edge_count_information"] - parent["exact_edge_count_MI"]) < CHECKPOINT_REPRODUCTION_TOLERANCE
        assert abs(got["class_given_edge_count"] - parent["exact_class_given_edge_count_MI"]) < CHECKPOINT_REPRODUCTION_TOLERANCE
        assert abs(got["chain_rule_gap"]) < 1e-12
        assert checkpoints[(system_id, source)]["kernel_row_error"] < 1e-12
    assert checkpoints[("R01", "path")]["epoch_mi"]["class_given_edge_count"] > 1e-3
    assert abs(checkpoints[("R01", "star")]["epoch_mi"]["class_given_edge_count"]) < 1e-12
    assert abs(checkpoints[("R06", "star")]["epoch_mi"]["class_given_edge_count"]) < 1e-12
    assert checkpoints[("R01", "path")]["immediate_mi"]["class_information"] > checkpoints[("R01", "path")]["epoch_mi"]["class_information"]
    for system_id in ("R00", "R02", "R04"):
        assert abs(checkpoints[(system_id, "path")]["epoch_mi"]["class_information"]) < 1e-10


def test_excursions_normalise_and_dilute_the_gate() -> None:
    baseline = excursion_report("R00", "path")
    assert abs(baseline["excursion_length_mass"] - 1.0) < 1e-12
    assert abs(baseline["probability_pair_event_is_immediate"] - 0.6) < 1e-12
    assert abs(baseline["probability_pre_pair_gate_equals_initial"] - 0.875) < 1e-12
    assert baseline["residual_unabsorbed"] < 1e-12
    favour = excursion_report("R06", "path")
    suppress = excursion_report("R01", "path")
    assert favour["probability_pair_event_is_immediate"] > baseline["probability_pair_event_is_immediate"]
    assert suppress["probability_pair_event_is_immediate"] < baseline["probability_pair_event_is_immediate"]
    assert favour["probability_pre_pair_gate_equals_initial"] > suppress["probability_pre_pair_gate_equals_initial"]


def test_gate_memory_decays_and_the_other_triad_bits_carry_no_pair_information(memory: dict) -> None:
    for row in memory[("R00", "path")]:
        assert abs(row["distribution_mass"] - 1.0) < 1e-12
        assert abs(row["I_initial_full_triad_current_pair_mask"]) <= 1e-10
    r01 = {row["checkpoint"]: row for row in memory[("R01", "path")]}
    assert abs(r01[0]["I_initial_gate_current_gate"] - math.log(2.0)) < 1e-12
    assert abs(r01[0]["Pr_current_gate_equals_initial_gate"] - 1.0) < 1e-12
    assert r01[1]["I_initial_gate_current_pair_mask"] > 1e-3
    assert abs(r01[1]["gate_pair_gap"]) < 1e-12
    assert r01[64]["I_initial_gate_current_pair_mask"] < 1e-10
    assert abs(r01[64]["Pr_current_gate_equals_initial_gate"] - 0.5) < 1e-8
    r06 = {row["checkpoint"]: row for row in memory[("R06", "path")]}
    assert r06[1]["I_initial_gate_current_pair_mask"] > r01[1]["I_initial_gate_current_pair_mask"]
    assert r06[64]["I_initial_full_triad_current_pair_mask"] < 1e-10


def test_mask_contributions_sum_and_single_rule_masks_share_one_value(atlases: dict) -> None:
    for system_id, atlas in atlases.items():
        assert atlas["sum_gap_balanced"] < 1e-12
        assert atlas["sum_gap_stationary"] < 1e-12
    r01 = atlases["R01"]
    assert r01["active_balanced_contribution_span"] < 1e-12
    assert r01["inactive_balanced_abs_max"] <= 1e-15
    assert r01["zero_contribution_mask_count"] == 32
    assert atlases["R06"]["active_balanced_contribution_span"] < 1e-12
    assert atlases["R05"]["active_balanced_contribution_span"] > 1e-6
    assert atlases["R00"]["balanced_cmi"] < 1e-12
    assert r01["balanced_cmi"] > 1e-3


def test_class_projection_accounts_for_the_labelled_remainder(projections: dict, tables: dict) -> None:
    for system_id, fraction in (("R01", 0.6607695878326966), ("R06", 0.44344850381118717)):
        report = projections[system_id]
        full = _cell(tables, system_id, "stationary_pair_event", "full_pair_mask", "next_pair_slot")
        retained = _cell(tables, system_id, "stationary_pair_event", "pair_graph_class", "next_pair_slot")
        assert abs(report["full_mask_cmi"] - full) < 1e-12
        assert abs(report["class_cmi"] - retained) < 1e-12
        assert abs(report["retained_fraction"] - fraction) < 1e-12
        assert abs(report["loss_sum_gap"]) < 1e-12
        assert report["discarded"] > 0.0
    assert projections["R06"]["retained_fraction"] < projections["R01"]["retained_fraction"]


def test_counterfactual_separates_occupancy_from_the_multiplier() -> None:
    rows = projection_counterfactual()["rows"]

    def pick(weighting: str, law: str) -> dict:
        return next(row for row in rows if row["weighting"] == weighting and row["law_system"] == law)

    balanced_suppress = pick("balanced", "R01")["retained_fraction"]
    balanced_favour = pick("balanced", "R06")["retained_fraction"]
    stationary_suppress = pick("R01", "R01")["retained_fraction"]
    stationary_favour = pick("R06", "R06")["retained_fraction"]
    assert balanced_favour > balanced_suppress
    assert stationary_favour < stationary_suppress
    assert pick("R01", "R06")["retained_fraction"] > pick("R06", "R01")["retained_fraction"]


def test_drift_closed_form_sign_and_stationary_balance(drifts: dict) -> None:
    assert abs(drifts["R01"]["balanced_rule_induced_drift"] - float(Fraction(5, 168))) < 1e-12
    assert abs(drifts["R04"]["balanced_rule_induced_drift"] - drifts["R01"]["balanced_rule_induced_drift"]) < 1e-12
    assert abs(drifts["R02"]["balanced_rule_induced_drift"] + drifts["R01"]["balanced_rule_induced_drift"]) < 1e-12
    assert abs(drifts["R03"]["balanced_rule_induced_drift"] - 2 * drifts["R01"]["balanced_rule_induced_drift"]) < 1e-12
    assert abs(drifts["R06"]["balanced_rule_induced_drift"] - float(Fraction(-5, 72))) < 1e-12
    assert abs(drifts["R07"]["balanced_rule_induced_drift"] - 2 * drifts["R06"]["balanced_rule_induced_drift"]) < 1e-12
    assert drifts["R01"]["active_rule_induced_sign"] == "positive"
    assert drifts["R02"]["active_rule_induced_sign"] == "negative"
    assert drifts["R06"]["active_rule_induced_sign"] == "negative"
    for row in drifts.values():
        assert row["closed_form_defined"] is True
        assert row["closed_form_gap"] < 1e-12
        assert row["direct_identity_gap"] < 1e-12
        assert row["per_state_drift_gap"] < 1e-12
        assert abs(row["stationary_expected_drift"]) < 1e-9


def test_labelled_conjugacy_does_not_preserve_graph_class() -> None:
    report = symmetry_report()
    assert report["r02_to_r01_transition_gap"] < 1e-12
    assert report["r04_to_r01_transition_gap"] < 1e-12
    assert report["preserves_labelled_slot_cmi"] is True
    assert report["preserves_graph_class"] is False
    assert report["r02_preserves_pair_class"] is False
    assert report["r04_preserves_pair_class"] is False
    assert report["r04_class_image_example"]["source_class"] != report["r04_class_image_example"]["image_class"]


def test_hierarchy_arrows_are_measured() -> None:
    report = hierarchy_report()
    arrows = report["arrows"]
    assert arrows["one_slot_reweight_matches_the_closed_form"]["r01_gap"] < 1e-12
    assert arrows["favour_and_suppress_are_different_distances"]["favour_cmi"] > arrows["favour_and_suppress_are_different_distances"]["suppress_cmi"]
    assert arrows["path_splits_shape_and_star_does_not"]["path_one_class_per_edge_count"] is False
    assert arrows["path_splits_shape_and_star_does_not"]["star_one_class_per_edge_count"] is True
    assert arrows["path_splits_shape_and_star_does_not"]["r01_path_shape"] > 1e-3
    assert abs(arrows["path_splits_shape_and_star_does_not"]["r01_star_shape"]) < 1e-12
    refresh = arrows["gate_refresh_erases_initial_pair_information"]
    assert refresh["r01_pair_mask_mi_at_1"] > 1e-3
    assert refresh["r01_pair_mask_mi_at_64"] < 1e-10
    assert refresh["r00_pair_mask_mi_max_abs"] <= 1e-10
    current = arrows["current_gate_still_biases_the_slot_law"]
    assert current["r01_balanced_cmi"] > 1e-3
    assert current["r00_balanced_cmi"] < 1e-12
    assert arrows["rule_induced_drift_sign"]["R01"]["sign"] == "positive"
    assert arrows["rule_induced_drift_sign"]["R06"]["sign"] == "negative"
    assert abs(arrows["rule_induced_drift_sign"]["R01"]["stationary_expected_drift"]) < 1e-9


def test_plan_contract_has_no_result_and_execution_is_refused(tmp_path: Path) -> None:
    plan = prepare_c0_plan(REPO)
    assert plan["plan_hash"] == plan_hash(plan)
    assert prepare_c0_plan(REPO)["plan_hash"] == plan["plan_hash"]
    assert plan["stochastic_trajectories"] is False
    assert plan["new_controls"] is False
    assert plan["parameter_fit"] is False
    blob = json.dumps(plan)
    for key in ("enumerated_balanced_CMI", "exact_MI", "checkpoint_rows", "mask_contribution"):
        assert key not in blob
    assert len(c0_items()) == 60
    assert len({"-".join(str(part) for part in (item["kind"], item["system"], item["source"])) for item in c0_items()}) == 60
    with pytest.raises(FrozenPlanError):
        require_c0_execution(tmp_path, None, PLAN_RELPATH, require_remote=False)
    repo = tmp_path / "repo"
    (repo / "constraint-lab" / "reports").mkdir(parents=True)
    shutil.copyfile(PARENT, repo / PARENT_TABLES_RELPATH)
    commit = _commit_plan(repo, plan, PLAN_RELPATH)
    accepted = require_c0_execution(
        repo,
        commit,
        PLAN_RELPATH,
        disk_path=repo / PLAN_RELPATH,
        require_remote=False,
    )
    assert accepted["plan_hash"] == plan["plan_hash"]
    with pytest.raises(FrozenPlanError):
        require_c0_execution(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH, require_remote=True)
    drifted = json.loads(json.dumps(plan))
    drifted["stochastic_trajectories"] = True
    drifted["plan_hash"] = plan_hash(drifted)
    bad = tmp_path / "bad"
    (bad / "constraint-lab" / "reports").mkdir(parents=True)
    shutil.copyfile(PARENT, bad / PARENT_TABLES_RELPATH)
    bad_commit = _commit_plan(bad, drifted, PLAN_RELPATH)
    with pytest.raises(MechanismError):
        require_c0_execution(bad, bad_commit, PLAN_RELPATH, disk_path=bad / PLAN_RELPATH, require_remote=False)


def test_one_executor_item_is_bounded() -> None:
    payload = execute_plan_item({"kind": "local-law", "source": None, "system": "R01"})
    assert payload["item_id"] == "local-law-R01"
    assert payload["wall_seconds"] < 120
    assert payload["result"]["gap"] < CLOSED_FORM_TOLERANCE


def test_engine_language_stays_descriptive() -> None:
    forbidden = ("disprove rs", "confirm rs", "null hypothesis", "p_value", "route to star")
    for name in ("explore08c.py", "gen008c_exec.py"):
        text = (SRC / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text
