"""Generation 8D two-gate composition contracts.

These tests check the labelled universe, the local algebra, and the
execution refusal. They do not publish the Round D0 tables. The D0 plan
hash is pinned only in the journey test, beside the result commit.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.constraints import DISSOLVE, FORM, structurally_simple
from rs_constraint_lab.durable import atomic_write_json, canonical_json, sha256_bytes
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.explore08a import repository_root, verify_journey_chronology
from rs_constraint_lab.explore08d import (
    GRADES,
    SLOT_MAPS,
    _law_hash,
    _relabel_fast,
    analyse_system,
    balanced_drift_formula,
    build_universe,
    canonical_structural_key,
    canonical_weighted_key,
    constraint_from_key,
    duplicate_kernel_product,
    expressivity_bound,
    general_normalisation_identities,
    load_universe,
    local_law_class,
    one_gate_surface,
    one_rule_catalogue,
    product_weights,
)
from rs_constraint_lab.gen008d_exec import (
    PLAN_RELPATH,
    WATCHDOG_SECONDS,
    CompositionRunError,
    execute_plan_item,
    prepare_d0_plan,
    require_d0_execution,
    run_d0,
    validate_orbit_result,
)
from rs_constraint_lab.weights import alphabet_factors

REPO = repository_root()
GIT_ENV = {
    "GIT_AUTHOR_NAME": "gellsmore-svg",
    "GIT_AUTHOR_EMAIL": "gellsmore@googlemail.com",
    "GIT_COMMITTER_NAME": "gellsmore-svg",
    "GIT_COMMITTER_EMAIL": "gellsmore@googlemail.com",
}
FAMILIES = {
    "complementary_gate",
    "different_actions_different_gates",
    "different_actions_same_gate",
    "same_action_different_gates",
    "same_slot_opposite_directions",
}


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(GIT_ENV)
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=env)


def _commit_plan(repo: Path, document: dict) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    relative = PLAN_RELPATH
    atomic_write_json(repo / relative, document)
    _git(repo, "init")
    _git(repo, "add", relative)
    _git(repo, "commit", "-m", "freeze test plan")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _find(family: str, predicate, descriptor_predicate=None) -> tuple[dict, dict]:
    for orbit in load_universe()["orbits"]:
        if orbit["descriptors"]["composition_family"] != family:
            continue
        if descriptor_predicate is not None and not descriptor_predicate(orbit["descriptors"]):
            continue
        for system in orbit["systems"]:
            if predicate(system):
                return orbit, system
    raise AssertionError(family)


@pytest.fixture(scope="module")
def universe() -> dict:
    return build_universe()


def test_labelled_universe_is_the_unordered_pairs_of_96_rules(universe: dict) -> None:
    assert universe["labelled_rule_count"] == 2 * 6 * 4 * 2
    assert universe["labelled_pair_count"] == 4560
    assert universe["structural_orbit_count"] == 236
    assert universe["weighted_canonical_count"] == 3584
    assert universe["duplicate_structural_rules_allowed"] is False
    assert sum(orbit["orbit_size"] for orbit in universe["orbits"]) == 4560
    assert set(Counter(orbit["descriptors"]["composition_family"] for orbit in universe["orbits"])) == FAMILIES
    factors = alphabet_factors("W4")
    assert [factors[name] for name in GRADES] == [Fraction(1, 4), Fraction(1, 2), Fraction(2), Fraction(4)]


def test_canonicalisation_is_idempotent_and_forgets_rule_order(universe: dict) -> None:
    for orbit in universe["orbits"]:
        key = orbit["canonical_structural_key"]
        assert key[0] != key[1]
        assert canonical_structural_key(key[0], key[1]) == key
        for edge_map in SLOT_MAPS:
            image = canonical_structural_key(_relabel_fast(key[0], edge_map), _relabel_fast(key[1], edge_map))
            assert image == key
        for system in orbit["systems"]:
            weighted = system["weighted_key"]
            assert canonical_weighted_key(weighted[0][0], weighted[0][1], weighted[1][0], weighted[1][1]) == weighted
            assert canonical_weighted_key(weighted[1][0], weighted[1][1], weighted[0][0], weighted[0][1]) == weighted


def test_duplicate_structural_rules_are_outside_the_atlas() -> None:
    left = constraint_from_key((FORM, 0, 6, 1), "strong_favour")
    right = constraint_from_key((FORM, 0, 6, 1), "weak_suppress")
    assert not structurally_simple((left, right))
    recorded = duplicate_kernel_product()
    assert recorded["accepted_in_atlas"] is False
    assert recorded["kernel_weight"] == recorded["expected_product"] == "2/1"


def test_one_gate_surface_covers_the_weak_grades_and_the_strong_ratios() -> None:
    surface = one_gate_surface()
    by_grade = {row["grade"]: row for row in surface["grades"]}
    assert by_grade["strong_suppress"]["balanced_dissolve_drift"] == "5/168"
    assert by_grade["strong_suppress"]["balanced_form_drift"] == "-5/168"
    assert by_grade["strong_favour"]["balanced_dissolve_drift"] == "-5/72"
    assert by_grade["weak_suppress"]["balanced_dissolve_drift"] == "5/264"
    assert by_grade["weak_favour"]["balanced_form_drift"] == "5/168"
    assert by_grade["strong_suppress"]["analytic_balanced_cmi"] == pytest.approx(0.009748566529643857)
    assert by_grade["strong_favour"]["analytic_balanced_cmi"] == pytest.approx(0.02336844477204944)
    assert by_grade["weak_suppress"]["enumerated_balanced_cmi"] < by_grade["strong_suppress"]["enumerated_balanced_cmi"]
    assert surface["unconditional_doubles_conditional"] is True
    assert balanced_drift_formula(Fraction(1, 4), DISSOLVE) == Fraction(5, 168)
    assert balanced_drift_formula(Fraction(4), FORM) == Fraction(5, 72)


def test_general_normalisation_and_expressivity_bound() -> None:
    for sample in general_normalisation_identities()["samples"]:
        assert sample["same_action_gap"] == 0
        assert sample["different_action_gap"] == 0
    bound = expressivity_bound()
    assert bound["independent_conjunction_term"] is False
    assert bound["xor_isolated_by_two_primitive_literals"] is False
    assert bound["both_active_determined_by_the_other_three"] is True
    assert "λ1" in bound["representation"]


def test_family_representatives_have_the_expected_local_law() -> None:
    equal_orbit, equal_system = _find("complementary_gate", lambda system: system["weights"][0] == system["weights"][1])
    unequal_orbit, unequal_system = _find("complementary_gate", lambda system: system["weights"][0] != system["weights"][1])
    same_orbit, same_system = _find("same_action_different_gates", lambda system: system["weights"] == ["weak_suppress", "weak_suppress"])
    shared_orbit, shared_system = _find(
        "different_actions_same_gate",
        lambda system: system["weights"] == ["strong_favour", "strong_favour"],
        lambda descriptors: descriptors["polarity_relation"] == "same_polarity",
    )
    partition_orbit, partition_system = _find(
        "different_actions_same_gate",
        lambda system: system["weights"] == ["strong_favour", "strong_favour"],
        lambda descriptors: descriptors["polarity_relation"] == "opposite_polarity",
    )
    split_orbit, split_system = _find("different_actions_different_gates", lambda system: True)
    opposed_orbit, opposed_system = _find("same_slot_opposite_directions", lambda system: True)
    equal = analyse_system(equal_orbit, equal_system)
    unequal = analyse_system(unequal_orbit, unequal_system)
    same = analyse_system(same_orbit, same_system)
    shared = analyse_system(shared_orbit, shared_system)
    split = analyse_system(split_orbit, split_system)
    opposed = analyse_system(opposed_orbit, opposed_system)
    partition = analyse_system(partition_orbit, partition_system)

    assert equal["reducibility_class"] == "R1U"
    assert equal["effective_gate_dimension"] == 0
    assert equal["syntactic_one_rule"] is True
    assert len(equal["comparator_expressions"]) == 1
    assert " | " not in equal["comparator_expressions"][0]
    assert abs(equal["information"]["balanced_full_triad_cmi"]) < 1e-12
    assert unequal["reducibility_class"] == "R1T"
    assert unequal["effective_gate_dimension"] == 1
    assert unequal["syntactic_one_rule"] is False
    assert same["reducibility_class"] == "R2G"
    assert same["effective_gate_dimension"] == 2
    assert same["identities"]["logit_interaction_gap"] == 0.0
    assert same["identities"]["same_action_gap"] == 0.0
    assert shared["reducibility_class"] == "R2S"
    assert shared["effective_gate_dimension"] == 1
    assert shared["identities"]["different_action_both_active_checks"] > 0
    assert shared["identities"]["different_action_gap"] == 0.0
    assert partition_orbit["descriptors"]["gate_relation"] == "same_triad"
    assert partition["reducibility_class"] == "R2S"
    assert partition["effective_gate_dimension"] == 1
    assert partition["identities"]["different_action_both_active_checks"] == 0
    assert partition["identities"]["different_action_gap"] == 0.0
    assert split["reducibility_class"] == "R2G"
    assert split["effective_gate_dimension"] == 2
    assert opposed["identities"]["same_action_both_active_checks"] == 0
    assert opposed["identities"]["different_action_both_active_checks"] == 0
    assert same["information"]["balanced_full_triad_cmi"] < shared["information"]["balanced_full_triad_cmi"]
    favour = next(row for row in one_gate_surface()["grades"] if row["grade"] == "strong_favour")
    assert equal["information"]["balanced_full_triad_cmi"] < favour["analytic_balanced_cmi"]
    for row in (equal, unequal, same, shared, split, opposed, partition):
        assert row["kernel_max_abs_gap"] <= 1e-12
        assert row["log_weight_gap"] <= 1e-12
        assert row["minimal_coordinate_sets"]
        realised = [cell for cell in row["truth_table"] if cell["realised"]]
        assert sum(cell["state_count"] for cell in row["truth_table"]) == 1024
        for cell in realised:
            weights = [Fraction(item) for item in cell["normalised_slot_law"]]
            assert all(weight > 0 for weight in weights)
            assert sum(weights, Fraction(0)) == 1


def test_opposite_directions_are_not_a_repeated_structural_rule() -> None:
    base = {
        "action_relation": "same_pair",
        "composition_family": "same_slot_opposite_directions",
        "gate_relation": "same_triad",
        "polarity_relation": "same_polarity",
    }
    opposite = validate_orbit_result(
        {
            "descriptors": {**base, "direction_relation": "opposite_direction"},
            "orbit_id": "X",
            "systems": [],
        }
    )
    repeated = validate_orbit_result(
        {
            "descriptors": {**base, "direction_relation": "same_direction"},
            "orbit_id": "X",
            "systems": [],
        }
    )
    assert opposite == []
    assert repeated == ["X repeats a structural rule"]


def test_local_law_hash_is_the_minimum_s4_image() -> None:
    orbit, system = _find("same_action_different_gates", lambda item: item["weights"] == ["weak_suppress", "weak_suppress"])
    analysed = analyse_system(orbit, system)
    key = system["weighted_key"]
    constraints = (constraint_from_key(key[0][0], key[0][1]), constraint_from_key(key[1][0], key[1][1]))
    rows = product_weights(constraints)
    digest = hashlib.sha256()
    for weight_row in rows:
        for weight in weight_row:
            digest.update(int(weight.numerator).to_bytes(8, "little", signed=True))
            digest.update(int(weight.denominator).to_bytes(8, "little", signed=False))
    assert _law_hash(rows) == digest.hexdigest()
    assert _law_hash(rows) == analysed["labelled_law_sha256"]
    assert local_law_class(rows) == analysed["local_law_class"]
    assert analysed["local_law_class"] <= analysed["labelled_law_sha256"]
    assert _law_hash(rows) not in one_rule_catalogue()


def test_plan_contract_has_no_result_and_execution_is_refused(tmp_path: Path) -> None:
    plan = prepare_d0_plan(REPO)
    assert plan["plan_hash"] == plan_hash(plan)
    assert prepare_d0_plan(REPO)["plan_hash"] == plan["plan_hash"]
    assert plan["stochastic_trajectories"] is False
    assert plan["new_controls"] is False
    assert plan["parameter_fit"] is False
    assert plan["history"] is False
    assert plan["universe"]["labelled_rule_count"] == 96
    assert plan["universe"]["labelled_pair_count"] == 4560
    assert plan["universe"]["structural_orbit_count"] == 236
    assert plan["universe"]["weighted_canonical_count"] == 3584
    assert plan["work_count"]["full_state_evaluations"] == 3584 * 1024
    assert len(plan["items"]) == 237
    blob = json.dumps(plan)
    for key in ("balanced_full_triad_cmi", "reducibility_class", "truth_table"):
        assert key not in blob
    with pytest.raises(FrozenPlanError):
        require_d0_execution(tmp_path, None, PLAN_RELPATH, require_remote=False)
    commit = _commit_plan(tmp_path / "repo", plan)
    repo = tmp_path / "repo"
    accepted = require_d0_execution(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH, require_remote=False)
    assert accepted["plan_hash"] == plan["plan_hash"]
    with pytest.raises(FrozenPlanError):
        require_d0_execution(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH, require_remote=True)
    drifted = json.loads(json.dumps(plan))
    drifted["history"] = True
    drifted["plan_hash"] = plan_hash(drifted)
    bad_commit = _commit_plan(tmp_path / "bad", drifted)
    with pytest.raises(CompositionRunError):
        require_d0_execution(tmp_path / "bad", bad_commit, PLAN_RELPATH, disk_path=tmp_path / "bad" / PLAN_RELPATH, require_remote=False)


def test_a_completed_surface_item_is_not_recomputed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    plan = prepare_d0_plan(REPO)
    plan["items"] = [item for item in plan["items"] if item["kind"] == "surface"]
    first = run_d0(tmp_path, plan)
    assert first[0]["skipped"] is False
    assert first[0]["wall_seconds"] < WATCHDOG_SECONDS

    def refuse(item: dict) -> dict:
        del item
        raise AssertionError("a completed surface item was recomputed")

    monkeypatch.setattr("rs_constraint_lab.gen008d_exec.execute_plan_item", refuse)
    second = run_d0(tmp_path, plan)
    assert second[0]["skipped"] is True


def test_surface_executor_item_is_bounded() -> None:
    payload = execute_plan_item({"kind": "surface", "orbit_id": None})
    assert payload["item_id"] == "surface"
    assert payload["wall_seconds"] < WATCHDOG_SECONDS
    assert payload["result"]["duplicate_rule"]["accepted_in_atlas"] is False


def test_cli_refuses_an_unfrozen_plan() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "rs_constraint_lab", "generation008d", "verify", "--allow-unpushed"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "frozen plan" in completed.stderr.lower()


def test_recorded_d0_journey_descends_from_the_frozen_plan() -> None:
    path = REPO / "constraint-lab" / "exploration" / "generation-008d" / "journey.jsonl"
    reports = verify_journey_chronology(REPO, path)
    assert len(reports) == 1
    assert reports[0]["frozen_plan_commit"] == "ac037f32df81271e04381c79efebf6f5b3d0b607"
    assert reports[0]["result_commit"] == "093e460e9992e3ddc4fd24cdb43d6d5397de4e29"
    assert reports[0]["plan_hash"] == "10a3114bcf7a1a914e9eff19e08f77a9fbcf71852bc4a22f14f04d723912ce07"


def test_published_d0_tables_match_their_recorded_hashes() -> None:
    reports = REPO / "constraint-lab" / "reports"
    body = json.loads((reports / "generation-008d-round-d0-tables.json").read_text(encoding="utf-8"))
    summary = {key: value for key, value in body.items() if key != "payload_sha256"}
    assert sha256_bytes(canonical_json(summary).encode("utf-8")) == body["payload_sha256"]
    assert body["validation"] == {"ok": True, "problems": []}
    assert body["summary"]["system_count"] == 3584
    assert body["summary"]["reducibility_counts"] == {"R0": 0, "R1G": 0, "R1T": 48, "R1U": 16, "R2G": 2608, "R2S": 912}
    tables = reports / "tables"
    for name in ("ablations", "identities", "information", "structural_orbits", "weighted_systems"):
        rows = json.loads((tables / f"generation-008d-{name.replace('_', '-')}.json").read_text(encoding="utf-8"))
        assert sha256_bytes(canonical_json(rows).encode("utf-8")) == body["detail_sha256"][name]
    lines = (tables / "generation-008d-truth-tables.jsonl").read_text(encoding="utf-8").splitlines()
    rows = [json.loads(line) for line in lines]
    assert sha256_bytes(canonical_json(rows).encode("utf-8")) == body["detail_sha256"]["truth_tables"]


SLOT_01 = 0
TRIAD_012 = 6
TRIAD_023 = 8


def test_reciprocal_literal_flip_gives_the_same_law() -> None:
    # On one slot the log multiplier is c + b1*G1 + b2*G2. An absent literal
    # adds its log weight to c, so flipping both literals keeps c only when the
    # two log weights cancel.
    flipped = (
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_012, 0), "strong_favour"),
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_023, 0), "strong_suppress"),
    )
    direct = (
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_012, 1), "strong_suppress"),
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_023, 1), "strong_favour"),
    )
    assert product_weights(flipped) == product_weights(direct)
    unbalanced = (
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_012, 1), "weak_suppress"),
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_023, 1), "strong_favour"),
    )
    unbalanced_flip = (
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_012, 0), "weak_favour"),
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_023, 0), "strong_suppress"),
    )
    assert product_weights(unbalanced) != product_weights(unbalanced_flip)


def test_equal_form_and_dissolve_on_one_gate_drop_the_slot_bit() -> None:
    toggle = (
        constraint_from_key((FORM, SLOT_01, TRIAD_012, 1), "strong_favour"),
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_012, 1), "strong_favour"),
    )
    rows = product_weights(toggle)
    for state, row in enumerate(rows):
        gate = (state >> TRIAD_012) & 1
        assert row[SLOT_01] == (Fraction(4) if gate else Fraction(1))
        assert all(weight == 1 for slot, weight in enumerate(row) if slot != SLOT_01)


def test_opposite_literals_on_opposite_directions_realise_slot_gate_xor() -> None:
    xor = (
        constraint_from_key((DISSOLVE, SLOT_01, TRIAD_012, 0), "strong_favour"),
        constraint_from_key((FORM, SLOT_01, TRIAD_012, 1), "strong_favour"),
    )
    rows = product_weights(xor)
    for state, row in enumerate(rows):
        edge = (state >> SLOT_01) & 1
        gate = (state >> TRIAD_012) & 1
        assert row[SLOT_01] == (Fraction(4) if edge ^ gate else Fraction(1))


def test_engine_language_stays_descriptive() -> None:
    forbidden = ("synergy", "antagonism", "cooperation", "overall_score", "best system", "disprove rs")
    root = REPO / "constraint-lab" / "src" / "rs_constraint_lab"
    for name in ("explore08d.py", "gen008d_exec.py"):
        text = (root / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text
