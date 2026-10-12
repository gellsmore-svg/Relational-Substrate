"""Generation 8B information-calibration contracts.

These tests check identities, reproduction, and execution refusal.
They do not publish the Round B0 tables.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
from pathlib import Path

import numpy as np
import pytest

from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.explore08 import CLASS_OF_MASK, FrozenPlanError, plan_hash, source_masks
from rs_constraint_lab.explore08a import (
    ChronologyError,
    mutual_information,
    repository_root,
    verify_journey_chronology,
    verify_plan_result_chronology,
)
from rs_constraint_lab.explore08b import (
    ZERO_INFORMATION_FLOOR,
    absorbing_kernel,
    balanced_slot_cmi,
    cmi_from_count_tables,
    class_from_mask,
    decompose_class_information,
    distributions_at_starts,
    empirical_slot_cmi,
    epoch_landing,
    expand_contingency,
    first_destination_laws,
    information_from_conditionals,
    initial_null_values,
    kernel_row_error,
    layout_guard,
    leading_order_bias,
    load_a0_palette,
    mutual_information_codes,
    pair_slot_laws,
    percentile_rank,
    permutation_null_initial,
    permutation_seed,
    plugin_from_contingency,
    propagate_pair_marginals,
    reproduce_plugin_tables,
    source_start_states,
    stationary_distribution,
    stationary_slot_cmi,
    structural_triad_independence,
    symmetry_destination_gap,
    system_kernel,
    triad_weight_span,
    visits_from_slot_mask_cells,
    _prepared_conditional_tables,
)
from rs_constraint_lab.gen008b_exec import prepare_b0_plan, require_b0_execution

REPO = repository_root()
SRC = REPO / "constraint-lab" / "src" / "rs_constraint_lab"
TABLES = REPO / "constraint-lab" / "reports" / "generation-008a-round-a0-tables.json"
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


def _commit_plan(repo: Path, document: dict, relative: str = "plan.json") -> str:
    repo.mkdir(parents=True, exist_ok=True)
    atomic_write_json(repo / relative, document)
    _git(repo, "init")
    _git(repo, "add", relative)
    _git(repo, "commit", "-m", "freeze test plan")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


@pytest.fixture(scope="module")
def palette() -> dict[str, dict]:
    return {row["system_id"]: row for row in load_a0_palette()}


@pytest.fixture(scope="module")
def tables() -> dict:
    return json.loads(TABLES.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def baseline(palette: dict[str, dict]) -> dict:
    kernel = system_kernel(palette["R00"]["expressions"])
    landing, defect = epoch_landing(kernel, solver="block")
    return {"defect": defect, "kernel": kernel, "landing": landing}


def test_plugin_units_are_nats_and_order_is_irrelevant() -> None:
    table = {"t00": {"left": 1.0}, "t01": {"right": 1.0}}
    swapped = {"t01": {"right": 1.0}, "t00": {"left": 1.0}}
    value = mutual_information(table)
    assert value is not None
    assert abs(value - math.log(2.0)) < 1e-12
    assert mutual_information(swapped) == value
    codes, outcomes = expand_contingency(table)
    assert abs(mutual_information_codes(codes, outcomes) - value) < 1e-12


def test_committed_generation8a_plugin_values_reproduce(tables: dict) -> None:
    report = reproduce_plugin_tables(tables)
    assert report["within_tolerance"] is True
    assert report["max_abs_gap"] <= 1e-9
    sample = next(
        row
        for row in tables["uniform_raw_triad_information"]
        if row["system_id"] == "R00" and row["source_graph_class"] == "path"
    )
    assert abs(plugin_from_contingency(sample["contingency"]) - sample["nats"]) <= 1e-9


def test_permutation_seeds_and_blocks_are_deterministic() -> None:
    first = permutation_seed("first_destination", "R00", "path", 0)
    assert first == permutation_seed("first_destination", "R00", "path", 0)
    assert first != permutation_seed("first_destination", "R00", "path", 1)
    contingency = {f"t{index:02d}": {"a": 8.0, "b": 8.0} for index in range(16)}
    whole = initial_null_values(
        contingency,
        estimand_id="first_destination",
        system_id="R00",
        source_graph="path",
        count=4,
    )
    head = initial_null_values(
        contingency,
        estimand_id="first_destination",
        system_id="R00",
        source_graph="path",
        count=2,
    )
    tail = initial_null_values(
        contingency,
        estimand_id="first_destination",
        system_id="R00",
        source_graph="path",
        count=2,
        start=2,
    )
    assert np.array_equal(whole, np.concatenate([head, tail]))


def test_identity_labels_match_the_plugin_and_keep_marginals() -> None:
    contingency = {"t00": {"a": 10.0, "b": 6.0}, "t01": {"a": 4.0, "b": 12.0}}
    contexts, outcomes = expand_contingency(contingency)
    assert mutual_information_codes(contexts, outcomes) == pytest.approx(
        plugin_from_contingency(contingency)
    )
    generator = np.random.Generator(np.random.PCG64(permutation_seed("estimand", "R00", "star", 3)))
    shuffled = generator.permutation(contexts)
    assert sorted(shuffled.tolist()) == sorted(contexts.tolist())
    summary = permutation_null_initial(
        {f"t{index:02d}": {"a": 8.0, "b": 8.0} for index in range(16)},
        estimand_id="balanced-table",
        system_id="R00",
        source_graph="path",
        count=40,
    )
    assert summary["observed_plugin"] == pytest.approx(0.0, abs=1e-12)
    assert summary["plugin_minus_null_mean"] < 0.0


def test_synthetic_independence_null_tracks_the_leading_bias() -> None:
    generator = np.random.Generator(np.random.PCG64(20261012))
    draws = generator.integers(0, 2, size=256)
    contingency: dict[str, dict[str, float]] = {}
    for index, draw in enumerate(draws):
        context = f"t{index // 16:02d}"
        outcome = "a" if int(draw) == 0 else "b"
        contingency.setdefault(context, {"a": 0.0, "b": 0.0})
        contingency[context][outcome] += 1.0
    summary = permutation_null_initial(
        contingency,
        estimand_id="synthetic-independence",
        system_id="R00",
        source_graph="star",
        count=200,
    )
    bias = leading_order_bias(16, 2, 256)
    assert abs(summary["null_mean"] - bias) < 0.02
    assert abs(summary["plugin_minus_null_mean"]) < 4.0 * summary["null_sd"]
    assert percentile_rank(200, 0.95) == 189


def test_conditional_tables_match_the_plugin_and_preserve_margins(tables: dict) -> None:
    row = next(
        item
        for item in tables["current_context"]
        if item["system_id"] == "R00" and item["source_graph_class"] == "path"
    )
    cells = row["cells"]["current_triad_next_pair_slot_given_full_pair_mask"]
    from rs_constraint_lab.explore08b import conditional_null_values

    from rs_constraint_lab.explore08a import conditional_mutual_information

    counted = {(item["x"], item["y"], item["z"]): int(item["count"]) for item in cells}
    official = conditional_mutual_information(counted)["nats"]
    fast = cmi_from_count_tables(_prepared_conditional_tables(cells))
    assert abs(fast - official) <= 1e-9
    block = conditional_null_values(
        cells,
        estimand_id="current_triad_next_pair_slot_given_full_pair_mask",
        system_id="R00",
        source_graph="path",
        count=2,
    )
    again = conditional_null_values(
        cells,
        estimand_id="current_triad_next_pair_slot_given_full_pair_mask",
        system_id="R00",
        source_graph="path",
        count=2,
    )
    assert np.array_equal(block, again)
    table = np.array([[4, 1], [2, 3], [0, 5]], dtype=np.int64)
    remaining = table.sum(axis=1).astype(np.int64)
    generator = np.random.Generator(np.random.PCG64(1))
    drawn = np.zeros_like(table)
    for column in range(table.shape[1]):
        need = int(table[:, column].sum())
        take = generator.multivariate_hypergeometric(remaining, need)
        remaining -= take
        drawn[:, column] = take
    assert drawn.sum(axis=1).tolist() == table.sum(axis=1).tolist()
    assert drawn.sum(axis=0).tolist() == table.sum(axis=0).tolist()


def test_absorbing_update_is_diagonal() -> None:
    from rs_constraint_lab.explore08 import CLASS_NAMES

    landing = np.full((1024, 1024), 1.0 / 1024.0)
    modified, absorbing = absorbing_kernel(landing, [CLASS_NAMES[4]])
    indices = np.flatnonzero(absorbing)
    assert indices.size > 0
    assert np.max(np.abs(modified[indices].sum(axis=1) - 1.0)) < 1e-12
    kept = np.ones(1024, dtype=bool)
    kept[indices] = False
    assert float(np.max(modified[indices][:, kept])) == 0.0


def test_baseline_destination_and_checkpoints_are_numerical_zero(baseline: dict, palette: dict) -> None:
    layout_guard(baseline["kernel"])
    assert structural_triad_independence(palette["R00"]["expressions"])["structural_zero_control"] is True
    assert triad_weight_span(baseline["kernel"]) <= ZERO_INFORMATION_FLOOR
    assert kernel_row_error(baseline["landing"]) <= 1e-9
    dense, _defect = epoch_landing(baseline["kernel"], solver="dense")
    assert float(np.max(np.abs(dense - baseline["landing"]))) <= 1e-8
    starts = source_start_states()
    for source, states in starts.items():
        solved = first_destination_laws(baseline["landing"], int(CLASS_OF_MASK[states[0] & 63]))
        assert solved["max_abs_total_gap"] <= 1e-8
        laws = distributions_at_starts(solved["height"], states)
        assert float(np.max(np.abs(laws - laws[:1]).sum(axis=1))) <= ZERO_INFORMATION_FLOOR
        assert abs(information_from_conditionals(laws)) <= ZERO_INFORMATION_FLOOR
        assert symmetry_destination_gap(palette["R00"]["expressions"], states[0] & 63, laws) <= ZERO_INFORMATION_FLOOR
    propagated = propagate_pair_marginals(baseline["landing"], starts["path"], checkpoints=(1, 2, 4), horizon=4)
    direct = baseline["landing"][starts["path"][0]].reshape(16, 64).sum(axis=0)
    assert np.max(np.abs(propagated["mask_at_checkpoint"][1][0] - direct)) <= 1e-12
    start = np.zeros(1024, dtype=np.float64)
    start[starts["path"][0]] = 1.0
    powered = start @ np.linalg.matrix_power(baseline["landing"], 4)
    powered_mask = powered.reshape(16, 64).sum(axis=0)
    assert np.max(np.abs(powered_mask - propagated["mask_at_checkpoint"][4][0])) <= 1e-9
    pieces = decompose_class_information(class_from_mask(propagated["mask_at_checkpoint"][2]))
    assert abs(pieces["chain_rule_gap"]) <= 1e-9
    assert abs(pieces["class_information"]) <= ZERO_INFORMATION_FLOOR


def test_zero_controls_have_no_current_context_information(palette: dict, tables: dict) -> None:
    for system_id in ("R00", "R03", "R07"):
        expressions = palette[system_id]["expressions"]
        assert structural_triad_independence(expressions)["structural_zero_control"] is True
        kernel = system_kernel(expressions)
        assert triad_weight_span(kernel) <= ZERO_INFORMATION_FLOOR
        laws = pair_slot_laws(kernel)
        assert float(np.max(np.abs(laws["conditional"].sum(axis=1) - 1.0))) <= 1e-9
        assert abs(balanced_slot_cmi(laws["conditional"])) <= ZERO_INFORMATION_FLOOR
        stationary = stationary_distribution(kernel)
        assert stationary["residual"] <= 1e-8
        assert abs(stationary_slot_cmi(kernel, stationary["pi"], laws["full_event"])) <= ZERO_INFORMATION_FLOOR
        for source in ("star", "path", "triangle"):
            row = next(
                item
                for item in tables["current_context"]
                if item["system_id"] == system_id and item["source_graph_class"] == source
            )
            visits = visits_from_slot_mask_cells(row["cells"]["current_triad_next_pair_slot_given_full_pair_mask"])
            assert visits.sum() == 131072
            assert abs(empirical_slot_cmi(visits, laws["conditional"])) <= ZERO_INFORMATION_FLOOR


def test_labelled_rule_changes_pair_weight_and_solvers_agree(palette: dict) -> None:
    kernel = system_kernel(palette["R01"]["expressions"])
    assert structural_triad_independence(palette["R01"]["expressions"])["pair_event_law_reads_triad"] is True
    assert triad_weight_span(kernel) > 0.0
    block, _block_defect = epoch_landing(kernel, solver="block")
    dense, _dense_defect = epoch_landing(kernel, solver="dense")
    assert float(np.max(np.abs(block - dense))) <= 1e-8
    states = source_start_states()["triangle"]
    solved = first_destination_laws(block, int(CLASS_OF_MASK[states[0] & 63]))
    laws = distributions_at_starts(solved["height"], states)
    assert symmetry_destination_gap(palette["R01"]["expressions"], source_masks()["triangle"], laws) <= ZERO_INFORMATION_FLOOR
    propagated = propagate_pair_marginals(block, states, checkpoints=(1,), horizon=1)
    pieces = decompose_class_information(class_from_mask(propagated["mask_at_checkpoint"][1]))
    assert abs(pieces["chain_rule_gap"]) <= 1e-9


def test_empirical_exact_law_matches_a_direct_sample() -> None:
    law = np.full((1024, 6), 1.0 / 6.0)
    law[0] = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    law[1 << 6] = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    visits = np.zeros((16, 64), dtype=np.float64)
    visits[0, 0] = 2.0
    visits[1, 0] = 2.0
    assert abs(empirical_slot_cmi(visits, law) - math.log(2.0)) < 1e-12


def test_b0_plan_hash_is_stable_and_execution_is_refused(tmp_path: Path) -> None:
    plan = prepare_b0_plan()
    assert plan["plan_hash"] == plan_hash(plan)
    assert prepare_b0_plan()["plan_hash"] == plan["plan_hash"]
    assert plan["stochastic_trajectories"] is False
    assert "exact_MI" not in json.dumps(plan)
    with pytest.raises(FrozenPlanError):
        require_b0_execution(tmp_path, None, "plan.json", require_remote=False)
    with pytest.raises(FrozenPlanError):
        require_b0_execution(tmp_path, "abc", "plan.json", require_remote=False)
    repo = tmp_path / "repo"
    commit = _commit_plan(repo, plan, "constraint-lab/exploration/generation-008b/round-b0-plan.json")
    with pytest.raises(FrozenPlanError):
        require_b0_execution(
            repo,
            commit,
            "constraint-lab/exploration/generation-008b/round-b0-plan.json",
            disk_path=repo / "constraint-lab/exploration/generation-008b/round-b0-plan.json",
            require_remote=True,
        )
    accepted = require_b0_execution(
        repo,
        commit,
        "constraint-lab/exploration/generation-008b/round-b0-plan.json",
        disk_path=repo / "constraint-lab/exploration/generation-008b/round-b0-plan.json",
        require_remote=False,
    )
    assert accepted["plan_hash"] == plan["plan_hash"]
    drifted = json.loads(json.dumps(plan))
    drifted["permutations"]["initial_context"] = 10
    drifted["plan_hash"] = plan_hash(drifted)
    bad = tmp_path / "bad"
    bad_commit = _commit_plan(bad, drifted, "plan.json")
    with pytest.raises(FrozenPlanError):
        require_b0_execution(bad, bad_commit, "plan.json", disk_path=bad / "plan.json", require_remote=False)


def test_journey_without_a_result_is_skipped(tmp_path: Path) -> None:
    path = tmp_path / "journey.jsonl"
    path.write_text(json.dumps({"frozen_plan_commit": None, "result_commit": None, "round_id": "round-b0"}) + "\n", encoding="utf-8")
    assert verify_journey_chronology(REPO, path) == []
    with pytest.raises(ChronologyError):
        verify_plan_result_chronology(
            REPO,
            "4897d9e02b2942670bafc52bc966ef6709167b64",
            "61ed53075238284850e792aff5743f0a8a7b6695",
            "constraint-lab/exploration/generation-008a/round-a0-plan.json",
        )


def test_recorded_journeys_descend_from_their_frozen_plans() -> None:
    expected = {
        "constraint-lab/exploration/generation-008a/journey.jsonl": "61ed53075238284850e792aff5743f0a8a7b6695",
        "constraint-lab/exploration/generation-008b/journey.jsonl": "466d54339738d315ed621ea4256a239cb026498a",
    }
    for relative, frozen in expected.items():
        reports = verify_journey_chronology(REPO, REPO / relative)
        assert reports
        assert {row["frozen_plan_commit"] for row in reports} == {frozen}
        assert all(row["result_commit"] for row in reports)


def test_engine_language_stays_descriptive() -> None:
    forbidden = ("disprove rs", "confirm rs", "null hypothesis", "p_value", "route to star")
    for name in ("explore08b.py", "gen008b_exec.py"):
        text = (SRC / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text
