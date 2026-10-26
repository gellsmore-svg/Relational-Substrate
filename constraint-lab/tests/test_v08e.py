"""Generation 8E conjunctive-gate contracts.

These tests check the parser, the K3 universe, representative local laws,
the algebra items and the execution refusal. They do not publish the
Round E0 tables. The E0 plan hash is pinned only in the journey test,
beside the result commit.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.constraints import DISSOLVE, FORM, Constraint, parse_expression, structurally_simple
from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.explore08a import repository_root
from rs_constraint_lab.explore08d import GRADE_FACTOR, GRADES, SLOT_MAPS, product_weights
from rs_constraint_lab.explore08e import (
    ConjunctionError,
    _relabel,
    analyse_orbit,
    analytic_balanced_cmi,
    analytic_balanced_drift,
    basis_items,
    boolean_constructions,
    build_universe,
    canonical_key,
    check_k3_rule,
    general_conjunction_check,
    load_d8_index,
    mobius,
    parser_semantics,
    reconstruct,
    rule_key,
    symbolic_additive_comparison,
    w4_coverage,
)
from rs_constraint_lab.gen008e_exec import (
    PLAN_RELPATH,
    ConjunctionRunError,
    prepare_e0_plan,
    require_e0_execution,
)
from rs_constraint_lab.weights import alphabet_factors

REPO = repository_root()
GIT_ENV = {
    "GIT_AUTHOR_NAME": "gellsmore-svg",
    "GIT_AUTHOR_EMAIL": "gellsmore@googlemail.com",
    "GIT_COMMITTER_NAME": "gellsmore-svg",
    "GIT_COMMITTER_EMAIL": "gellsmore@googlemail.com",
}


def _git(repo: Path, *args: str) -> None:
    env = os.environ.copy()
    env.update(GIT_ENV)
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=env)


def _commit_plan(repo: Path, document: dict) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    atomic_write_json(repo / PLAN_RELPATH, document)
    _git(repo, "init")
    _git(repo, "add", PLAN_RELPATH)
    _git(repo, "commit", "-m", "freeze test plan")
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture(scope="module")
def universe() -> dict:
    return build_universe()


def test_two_triad_conjunction_parses_at_order_3_with_k_3() -> None:
    rule = parse_expression("dissolve(0-1) | present(0-1-3) & absent(0-1-2) => strong_favour", 4, order=3)
    assert len(rule.conditions) == 2
    assert list(rule.conditions) == sorted(rule.conditions)
    assert rule.counts == ()
    assert rule.k() == 3
    semantics = parser_semantics()
    assert semantics["k"] == 3
    assert semantics["repeated_literal_rejected"] is True
    assert semantics["action_slot_condition_rejected"] is True
    assert semantics["count_predicate_rejected"] is True
    # The parser rejects a repeated literal but accepts both literals of one
    # triad. That rule never matches, and the census requires distinct triads.
    assert semantics["contradictory_same_triad_accepted"] is True
    assert semantics["contradictory_same_triad_matches"] == 0
    with pytest.raises(ConjunctionError):
        check_k3_rule(Constraint(DISSOLVE, 0, ((6, 0), (6, 1)), "strong_favour", ()))


def test_w4_factors_are_the_four_grades() -> None:
    factors = alphabet_factors("W4")
    assert [factors[g] for g in GRADES] == [Fraction(1, 4), Fraction(1, 2), Fraction(2), Fraction(4)]


def test_k3_universe_is_288_rules_in_20_orbits(universe: dict) -> None:
    assert universe["labelled_rule_count"] == 6 * 2 * 6 * 4
    assert universe["structural_orbit_count"] == 20
    assert universe["weighted_system_count"] == 80
    assert sum(orbit["orbit_size"] for orbit in universe["orbits"]) == 288
    for orbit in universe["orbits"]:
        key = orbit["canonical_key"]
        assert canonical_key(key) == key
        gates = [gate for gate, _required in key[2]]
        assert len(set(gates)) == 2 and all(gate >= 6 for gate in gates)
        for edge_map in SLOT_MAPS:
            assert canonical_key(_relabel(key, edge_map)) == key
        for system in orbit["systems"]:
            rule = parse_expression(system["canonical_weighted_rule"], 4, order=3)
            assert rule.k() == 3 and rule_key(rule) == key


def test_representative_orbits_have_the_single_corner_law() -> None:
    index = load_d8_index(REPO)
    for orbit_id in ("K3-00", "K3-03"):
        result = analyse_orbit(orbit_id, d8_index=index)
        for system in result["systems"]:
            m = GRADE_FACTOR[system["grade"]]
            assert system["minimal_coordinate_count"] == 3
            assert system["effective_gate_dimension"] == 2
            assert system["gate_interaction_order"] == 2
            assert system["distinct_local_law_rows"] == 2
            assert system["active_state_count"] == 128
            assert abs(system["interaction"]["literal_delta12"] - math.log(m)) < 1e-12
            assert system["balanced_cmi_gap"] < 1e-12
            assert system["balanced_edge_drift"] == system["balanced_edge_drift_analytic"]
            assert system["comparison"]["d8_exact_labelled_match_count"] == 0
            assert system["comparison"]["d8_exact_s4_match_count"] == 0
    mixed = analyse_orbit("K3-03")["systems"][0]
    assert mixed["interaction"]["raw_delta12"] == pytest.approx(-math.log(GRADE_FACTOR[mixed["grade"]]))


def test_analytic_surface_matches_the_review_predictions() -> None:
    predictions = {"strong_suppress": 0.006761384413735834, "weak_suppress": 0.002333270369315642, "weak_favour": 0.003961514536995468, "strong_favour": 0.018447186631125900}
    for grade, value in predictions.items():
        assert abs(analytic_balanced_cmi(GRADE_FACTOR[grade]) - value) < 1e-12
    assert analytic_balanced_drift(Fraction(1, 4), DISSOLVE) == Fraction(5, 336)
    assert analytic_balanced_drift(Fraction(4), DISSOLVE) == Fraction(-5, 144)
    assert analytic_balanced_drift(Fraction(2), FORM) == Fraction(5, 336)


def test_conjunction_is_outside_the_additive_span() -> None:
    result = symbolic_additive_comparison()
    assert result["additive_with_constant_rank"] == 3
    assert result["additive_with_constant_plus_conjunction_rank"] == 4
    assert result["additive_without_constant_rank"] == 2
    assert result["additive_without_constant_plus_conjunction_rank"] == 3


def test_mobius_and_corner_bases_reconstruct_exactly() -> None:
    table = {(0, 0): Fraction(2), (1, 0): Fraction(-7, 5), (0, 1): Fraction(3, 11), (1, 1): Fraction(19, 4)}
    coefficients = mobius(table)
    assert coefficients["d"] == table[(1, 1)] - table[(1, 0)] - table[(0, 1)] + table[(0, 0)]
    assert reconstruct(coefficients) == table
    items = basis_items()
    assert items["corner_polynomial_determinant"] in ("1/1", "-1/1")
    assert all(row["reconstruction_gap"] == "0/1" for row in items["examples"])
    names = {row["name"]: row for row in items["examples"]}
    assert names["xor"]["mobius_coefficients"]["d"] == "-2/1"
    assert names["additive"]["interaction_order"] == 1


def test_xor_xnor_and_four_corner_constructions() -> None:
    result = boolean_constructions()
    for row in result["constructions"]:
        table = row["gate_table"]
        if row["construction"] == "xor":
            assert table["00"] == table["11"] == "1/1" and table["01"] == table["10"] != "1/1"
        else:
            assert table["01"] == table["10"] == "1/1" and table["00"] == table["11"] != "1/1"
        assert row["kernel_gap"] == 0
    assert result["four_corner"]["gate_table"] == {"00": "1/4", "01": "1/2", "10": "2/1", "11": "4/1"}


def test_r_literal_monomial_law_on_one_placement() -> None:
    rows = general_conjunction_check()["rows"]
    assert {row["r"] for row in rows} == {1, 2, 3, 4}
    assert all(row["K"] == row["r"] + 1 and row["gap"] < 1e-12 for row in rows)


def test_w4_coverage_of_the_two_bases() -> None:
    coverage = w4_coverage()
    assert coverage["corner_basis_tables"] == 625
    assert coverage["polynomial_basis_tables"] == 625


def test_plan_contract_has_no_result_and_execution_is_refused(tmp_path: Path) -> None:
    plan = prepare_e0_plan(REPO)
    assert plan["plan_hash"] == plan_hash(plan)
    assert prepare_e0_plan(REPO)["plan_hash"] == plan["plan_hash"]
    assert plan["universe"]["labelled_rule_count"] == 288
    assert plan["universe"]["structural_orbit_count"] == 20
    assert plan["universe"]["weighted_system_count"] == 80
    assert plan["meta_constraints"] is False and plan["history"] is False
    blob = json.dumps(plan)
    for key in ("balanced_cmi", "truth_table", "raw_delta12"):
        assert key not in blob
    with pytest.raises(FrozenPlanError):
        require_e0_execution(tmp_path, None, PLAN_RELPATH, require_remote=False)
    commit = _commit_plan(tmp_path / "repo", plan)
    repo = tmp_path / "repo"
    accepted = require_e0_execution(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH, require_remote=False)
    assert accepted["plan_hash"] == plan["plan_hash"]
    drifted = json.loads(json.dumps(plan))
    drifted["meta_constraints"] = True
    drifted["plan_hash"] = plan_hash(drifted)
    bad = _commit_plan(tmp_path / "bad", drifted)
    with pytest.raises(ConjunctionRunError):
        require_e0_execution(tmp_path / "bad", bad, PLAN_RELPATH, disk_path=tmp_path / "bad" / PLAN_RELPATH, require_remote=False)


def test_cli_refuses_an_unfrozen_plan() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "rs_constraint_lab", "generation008e", "verify", "--allow-unpushed"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "frozen plan" in completed.stderr.lower()


def test_engine_language_stays_descriptive() -> None:
    forbidden = ("synergy", "overall_score", "best system", "disprove rs", "more real")
    root = REPO / "constraint-lab" / "src" / "rs_constraint_lab"
    for name in ("explore08e.py", "gen008e_exec.py"):
        text = (root / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text


def test_single_k3_rule_is_structurally_simple() -> None:
    rule = Constraint(FORM, 0, ((6, 1), (7, 0)), "weak_favour", ())
    assert structurally_simple((rule,))
    assert product_weights((rule,))[0][0] == 1


def test_recorded_e0_journey_descends_from_the_frozen_plan() -> None:
    from rs_constraint_lab.explore08a import verify_journey_chronology

    path = REPO / "constraint-lab" / "exploration" / "generation-008e" / "journey.jsonl"
    reports = verify_journey_chronology(REPO, path)
    assert len(reports) == 1
    assert reports[0]["frozen_plan_commit"] == "5303388815a3695ac6bf4eb4176c0102b9ca460c"
    assert reports[0]["result_commit"] == "2daf1ce3f54f8bacbc331b6bc575b44ed3f20c27"
    assert reports[0]["plan_hash"] == "ec515306c2d3fa669f15ce31a86cdaac78f5fcab0d01ea7ad82533fde71c9be6"


def _published() -> tuple[dict, dict]:
    from rs_constraint_lab.durable import canonical_json, sha256_bytes

    reports = REPO / "constraint-lab" / "reports"
    body = json.loads((reports / "generation-008e-round-e0-tables.json").read_text(encoding="utf-8"))
    summary = {key: value for key, value in body.items() if key != "payload_sha256"}
    assert sha256_bytes(canonical_json(summary).encode("utf-8")) == body["payload_sha256"]
    tables = {}
    for name, digest in body["detail_sha256"].items():
        rows = json.loads((reports / "tables" / f"generation-008e-{name.replace('_', '-')}.json").read_text(encoding="utf-8"))
        assert sha256_bytes(canonical_json(rows).encode("utf-8")) == digest
        tables[name] = rows
    return body, tables


def test_every_published_e0_system_is_a_single_corner_conjunction() -> None:
    body, tables = _published()
    assert body["validation"] == {"ok": True, "problems": []}
    systems = tables["weighted_systems"]
    assert len(systems) == 80
    for s in systems:
        assert (s["K"], s["rule_cardinality"], s["minimal_coordinate_count"], s["effective_gate_dimension"], s["gate_interaction_order"], s["distinct_local_law_rows"]) == (3, 1, 3, 2, 2, 2)
    by_system: dict[str, list[dict]] = {}
    for row in tables["truth_tables"]:
        by_system.setdefault(row["system_id"], []).append(row)
    for rows in by_system.values():
        assert sum(r["state_count"] for r in rows) == 1024
        active = [r for r in rows if r["active"]]
        assert len(active) == 1 and active[0]["state_count"] == 128
        assert active[0]["literal_1_truth"] == active[0]["literal_2_truth"] == 1
        for r in rows:
            if not r["active"]:
                assert r["normalised_slot_law"] == ["1/6"] * 6
    for row in tables["interaction"]:
        assert row["gap"] <= 1e-12 and row["literal_delta12"] != 0
    for row in tables["comparison_8d"]:
        assert row["8d_exact_labelled_match_count"] == 0 and row["8d_exact_s4_match_count"] == 0
        assert row["symbolic_additive_representable"] is False
