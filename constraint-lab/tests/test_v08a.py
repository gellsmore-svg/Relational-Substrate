"""Generation 8A raw-context and rule-aware symmetry contracts.

These tests do not execute the Round A0 atlas.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.explore08 import FrozenPlanError, pair_automorphisms, replay_events, run_episode, source_masks
from rs_constraint_lab.explore08a import (
    GENERATION8_CHRONOLOGY,
    SEED_FIELDS,
    ChronologyError,
    conditional_mutual_information,
    crosswalk,
    derive_seed,
    episode_id_for,
    graph_only_splits,
    load_repair_palette,
    mutual_information,
    permutation_preserves_constraints,
    preserving_permutations,
    raw_execution_contexts,
    repository_root,
    rule_aware_partition,
    seed_identity,
    symmetry_table,
    verify_plan_result_chronology,
    verify_recorded_chronology,
)
from rs_constraint_lab.gen008_exec import baseline_is_descriptive
from rs_constraint_lab.gen008a_exec import build_a0_plan, execute_item, install_plan, merge_items, verify_generation
from rs_constraint_lab.state import permutations, relation_slots, slot_permutation_maps
from rs_constraint_lab.supervisor import supervise

PYTHON = sys.executable
LAB = Path(__file__).resolve().parents[1]
SRC = LAB / "src" / "rs_constraint_lab"
REPO = repository_root()
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
    path = repo / relative
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "add", relative)
    _git(repo, "commit", "-m", "freeze test plan")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _benchmark() -> dict:
    return {
        "event_count": 8,
        "gzip_bytes": 100,
        "pair_event_count": 4,
        "pair_horizon": 4,
        "raw_bytes": 200,
        "replay_seconds": 0.01,
        "seconds": 0.01,
    }


def _tiny_plan() -> dict:
    systems = [load_repair_palette()[0]]
    contexts = [
        row
        for row in raw_execution_contexts()
        if row["source_graph_class"] == "star" and row["triad_config_id"] in {"t00", "t01"}
    ]
    return build_a0_plan(
        horizon=4,
        benchmark=_benchmark(),
        batch_items=1,
        batch_note="test",
        systems=systems,
        contexts=contexts,
        replicates=1,
        round_id="round-test",
        replay_fraction=1.0,
    )


def test_baseline_subgroup_is_the_source_automorphism_group() -> None:
    for mask in source_masks().values():
        assert preserving_permutations(mask, []) == pair_automorphisms(mask)


def test_labelled_constraint_is_preserved_only_by_system_automorphisms() -> None:
    expression = "dissolve(0-1) | absent(0-1-2) => strong_suppress"
    slots = tuple(relation_slots(4, 3))
    maps = {perm: image for perm, image in zip(permutations(4), slot_permutation_maps(4, slots))}
    for mask in source_masks().values():
        got = preserving_permutations(mask, [expression])
        expect = [
            perm
            for perm in pair_automorphisms(mask)
            if permutation_preserves_constraints([expression], perm)
        ]
        assert got == expect
        for perm in got:
            assert permutation_preserves_constraints([expression], perm)
            assert perm in maps


def test_asymmetric_star_rule_is_fixed_by_the_calculated_subgroup() -> None:
    mask = source_masks()["star"]
    expressions = ["dissolve(0-1) | absent(0-1-2) => strong_suppress"]
    got = preserving_permutations(mask, expressions)
    assert got == [(0, 1, 2, 3)]
    partition = rule_aware_partition(mask, expressions)
    assert partition["orbit_count"] == 16
    assert sum(orbit["orbit_size"] for orbit in partition["orbits"]) == 16


def test_unconditional_rule_keeps_automorphisms_that_fix_the_action_edge() -> None:
    mask = source_masks()["star"]
    expressions = ["dissolve(0-1) => strong_suppress"]
    got = preserving_permutations(mask, expressions)
    expect = [perm for perm in pair_automorphisms(mask) if {perm[0], perm[1]} == {0, 1}]
    assert got == expect
    assert len(got) == 2
    assert (0, 1, 2, 3) in got


def test_multi_rule_reordering_preserves_the_multiset() -> None:
    expressions = [
        "dissolve(0-1) => strong_suppress",
        "dissolve(2-3) => strong_suppress",
    ]
    swap = (2, 3, 0, 1)
    assert permutation_preserves_constraints(expressions, swap)
    changed = [
        "dissolve(0-1) => strong_favour",
        "dissolve(2-3) => strong_suppress",
    ]
    assert permutation_preserves_constraints(changed, swap) is False
    assert permutation_preserves_constraints(list(reversed(expressions)), swap)


def test_every_raw_context_is_executed_and_orbit_sizes_sum_to_16() -> None:
    contexts = raw_execution_contexts()
    assert len(contexts) == 48
    for source in ("star", "path", "triangle"):
        configs = [row["triad_config_id"] for row in contexts if row["source_graph_class"] == source]
        assert configs == [f"t{index:02d}" for index in range(16)]
        assert all(row["orbit_size"] == 1 for row in contexts if row["source_graph_class"] == source)
    systems = load_repair_palette()
    table = symmetry_table(systems)
    for system in systems:
        for source in ("star", "path", "triangle"):
            orbits = table[system["system_id"]][source]["orbits"]
            assert sum(orbit["orbit_size"] for orbit in orbits) == 16
            assert len(table[system["system_id"]][source]["lookup"]) == 16


def test_graph_only_orbits_can_split_under_a_labelled_rule() -> None:
    systems = [load_repair_palette()[1]]
    contexts = raw_execution_contexts()
    splits = graph_only_splits(symmetry_table(systems), contexts)
    star_splits = [row for row in splits if row["source_graph_class"] == "star"]
    assert star_splits
    assert any(row["graph_only_orbit_size"] > 1 for row in star_splits)


def test_seed_uses_the_raw_triad_and_not_the_graph_only_orbit() -> None:
    base = {
        "experiment_id": "generation-008a-context-repair",
        "raw_triad_config": "t00",
        "replicate_index": 0,
        "round_id": "round-a0",
        "source_graph_class": "star",
        "system_id": "R01",
    }
    first = derive_seed(base)
    assert first == derive_seed(dict(base))
    other = dict(base)
    other["raw_triad_config"] = "t01"
    assert derive_seed(other) != first
    identity = seed_identity(base)
    assert list(identity) == list(SEED_FIELDS)
    assert "graph_only_orbit_id" not in identity
    assert "hidden_context_orbit_id" not in identity
    assert episode_id_for(base) != episode_id_for(other)


def test_header_metadata_does_not_change_the_trajectory() -> None:
    system = load_repair_palette()[1]
    context = next(
        row
        for row in raw_execution_contexts()
        if row["source_graph_class"] == "star" and row["triad_config_id"] == "t03"
    )
    identity = seed_identity(
        {
            "experiment_id": "generation-008a-context-repair",
            "raw_triad_config": "t03",
            "replicate_index": 2,
            "round_id": "round-test",
            "source_graph_class": "star",
            "system_id": system["system_id"],
        }
    )
    common = dict(
        experiment_id="generation-008a-context-repair",
        round_id="round-test",
        system=system,
        context=context,
        replicate=2,
        pair_horizon=8,
        full_event_cap=64,
        plan_hash_value="unit",
        frozen_plan_commit="0" * 40,
        identity=identity,
    )
    left = run_episode(**common, header_extra={"graph_only_orbit_id": "star-o00", "triad_config_id": "t03", "runner_version": "generation-008a-trajectory/v1"})
    right = run_episode(**common, header_extra={"graph_only_orbit_id": "star-o99", "triad_config_id": "t03", "runner_version": "generation-008a-trajectory/v1"})
    assert left["events"] == right["events"]
    assert left["header"]["seed"] == right["header"]["seed"]
    assert left["header"]["episode_id"] == episode_id_for(identity)
    assert left["header"]["triad_config_id"] == "t03"
    assert left["header"]["graph_only_orbit_id"] != right["header"]["graph_only_orbit_id"]
    report = replay_events(left["header"], left["events"], system, initial_state=int(context["start_state"]))
    assert report["verification"] == "exact"


def test_uniform_raw_prior_is_labelled_apart_from_orbit_weight() -> None:
    uniform = {"t00": {"path": 1.0}, "t01": {"star": 1.0}}
    weighted = {"t00": {"path": 3.0}, "t01": {"star": 1.0}}
    uniform_info = mutual_information(uniform)
    weighted_info = mutual_information(weighted)
    assert uniform_info == pytest.approx(math.log(2))
    assert weighted_info != pytest.approx(uniform_info)
    catalogue = {row["id"] for row in __import__("rs_constraint_lab.explore08a", fromlist=["analysis_measure_catalogue"]).analysis_measure_catalogue()}
    assert "uniform_raw_triad" in catalogue
    assert "uniform_graph_only_orbit_from_this_sample" in catalogue
    assert "uniform_rule_aware_orbit" in catalogue


def test_contingency_counts_reproduce_mutual_information() -> None:
    contingency = {("t00", "path"): 16, ("t01", "star"): 16}
    by_context: dict[str, dict[str, float]] = {}
    for (context, destination), count in contingency.items():
        by_context.setdefault(context, {})[destination] = float(count)
    info = mutual_information(by_context)
    assert info == pytest.approx(math.log(2))
    total = sum(contingency.values())
    manual = 0.0
    for count in contingency.values():
        p_xy = count / total
        manual += p_xy * math.log(p_xy / (0.5 * 0.5))
    assert info == pytest.approx(manual)


def test_full_pair_mask_conditioning_is_distinct_from_class_conditioning() -> None:
    slot_class = Counter({(0, 0, 5): 10, (1, 1, 5): 10, (0, 1, 5): 10, (1, 0, 5): 10})
    slot_mask = Counter({(0, 0, 0): 10, (1, 1, 0): 10, (0, 1, 1): 10, (1, 0, 1): 10})
    by_class = conditional_mutual_information(slot_class)
    by_mask = conditional_mutual_information(slot_mask)
    assert by_class["nats"] == pytest.approx(0.0, abs=1e-12)
    assert by_mask["nats"] == pytest.approx(math.log(2))
    assert by_class["total"] == 40
    assert by_mask["nonzero_cells"] == 4


def test_palette_copies_generation8_expressions() -> None:
    systems = load_repair_palette()
    assert [row["system_id"] for row in systems] == [f"R0{index}" for index in range(8)]
    assert [row["parent_system_id"] for row in systems] == ["S00", "S01", "S05", "S10", "S11", "S09", "S12", "S16"]
    directory = LAB / "exploration" / "generation-008"
    for system in systems:
        document = json.loads((directory / f"{system['parent_round_id']}-plan.json").read_text(encoding="utf-8"))
        parent = next(row for row in document["systems"] if row["system_id"] == system["parent_system_id"])
        assert system["expressions"] == parent["expressions"]
        assert "prohibit" not in " ".join(system["expressions"])
    assert systems[0]["role"] == "baseline relational dynamics"
    assert baseline_is_descriptive({"systems": systems})
    bridges = crosswalk(systems)
    assert len(bridges) == 8 * 48
    assert {row["directly_sampled_in_generation8"] for row in bridges} == {True, False}


def test_a0_plan_freezes_6144_raw_episodes() -> None:
    plan = build_a0_plan(
        horizon=512,
        benchmark={
            "event_count": 800,
            "gzip_bytes": 28000,
            "pair_event_count": 512,
            "pair_horizon": 512,
            "raw_bytes": 400000,
            "replay_seconds": 0.05,
            "seconds": 0.07,
        },
        batch_items=40,
        batch_note="test",
    )
    assert plan["work_count"]["total_round_episodes"] == 6144
    assert plan["work_count"]["starts_per_system"] == 48
    assert plan["context_method"]["quotient_before_execution"] is False
    assert plan["seed_fields"] == list(SEED_FIELDS)
    assert "hidden_context_orbit_id" not in plan["seed_fields"]
    assert plan["prohibit_in_round"] is False
    again = build_a0_plan(
        horizon=512,
        benchmark={
            "event_count": 800,
            "gzip_bytes": 28000,
            "pair_event_count": 512,
            "pair_horizon": 512,
            "raw_bytes": 400000,
            "replay_seconds": 0.05,
            "seconds": 0.07,
        },
        batch_items=40,
        batch_note="test",
    )
    assert again["plan_hash"] == plan["plan_hash"]


def test_generation8_frozen_plans_are_ancestors_of_their_results() -> None:
    reports = verify_recorded_chronology(REPO, GENERATION8_CHRONOLOGY)
    assert [row["plan_hash"] for row in reports] == [row["plan_hash"] for row in GENERATION8_CHRONOLOGY]
    first = GENERATION8_CHRONOLOGY[0]
    with pytest.raises(ChronologyError):
        verify_plan_result_chronology(
            REPO,
            first["result_commit"],
            first["frozen_plan_commit"],
            first["plan_relpath"],
            first["plan_hash"],
        )


def test_execution_refuses_a_missing_or_unpushed_plan(tmp_path: Path) -> None:
    document = _tiny_plan()
    with pytest.raises(FrozenPlanError):
        install_plan(tmp_path / "run", tmp_path / "plan.json", "", tmp_path, "plan.json", require_remote=False)
    repo = tmp_path / "repo"
    commit = _commit_plan(repo, document)
    with pytest.raises(FrozenPlanError):
        install_plan(tmp_path / "remote", repo / "plan.json", commit, repo, "plan.json", require_remote=True)


def test_mini_raw_context_run_replays_exactly(tmp_path: Path) -> None:
    document = _tiny_plan()
    repo = tmp_path / "repo"
    root = tmp_path / "run"
    commit = _commit_plan(repo, document)
    summary = install_plan(root, repo / "plan.json", commit, repo, "plan.json", require_remote=False)
    assert summary["episodes"] == 2
    finished = supervise(root, workers=1, batch_size=1, heartbeat=0.2, watchdog=30)
    assert finished["state"] == "COMPLETE"
    merged = merge_items(root)
    assert merged["episodes"] == 2
    assert merged["replay_exact"] == 2
    report = verify_generation(root, require_complete=True)
    assert report["ok"] is True
    stored = None
    for path in (root / "items").glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("kind") == "episode":
            stored = payload
            break
    assert stored is not None
    assert stored["result"]["summary"]["triad_config_id"] in {"t00", "t01"}
    assert "markers" not in stored["result"]["summary"]
    assert stored["result"]["header"]["triad_config_id"] == stored["result"]["summary"]["triad_config_id"]
    assert stored["result"]["smoke_replay"] == "exact"
    assert "graph_only_orbit_id" not in stored["input"]


def test_direct_execute_refuses_an_unfrozen_manifest(tmp_path: Path) -> None:
    from rs_constraint_lab.workstore import Layout

    layout = Layout(tmp_path / "run")
    layout.ensure()
    atomic_write_json(layout.manifest_path(), {"experiment_id": "generation-008a-context-repair"})
    with pytest.raises(FrozenPlanError):
        execute_item({"input": {}, "kind": "episode"}, {"root": tmp_path / "run"})


def test_engine_language_stays_descriptive() -> None:
    forbidden = ("disprove rs", "confirm rs", "null hypothesis", "p_value", "route to star")
    for name in ("explore08a.py", "gen008a_exec.py"):
        text = (SRC / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text
