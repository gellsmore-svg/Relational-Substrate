"""Generation 8 trajectory contracts.

These tests exercise the engine, the frozen-plan gate, and a tiny supervisor
run. They do not execute the Round 0 atlas.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.explore08 import (
    BASELINE_ROLE,
    CLASS_NAMES,
    CLASS_OF_MASK,
    EXPERIMENT_ID,
    FrozenPlanError,
    _context_label,
    _slots,
    apply_operator,
    atlas_from_summaries,
    attention_vector,
    build_round0_systems,
    derive_composite_anchor,
    derive_pp_archetypes,
    derive_seed,
    derive_tp_archetypes,
    dynamic_cache,
    enumerate_hidden_contexts,
    episode_id_for,
    episode_row,
    pair_automorphisms,
    plan_hash,
    query_transitions,
    replay_events,
    require_frozen_plan,
    route_from_runs,
    run_chained,
    run_episode,
    select_replay_ids,
    source_masks,
    transition_counts_from_events,
)
from rs_constraint_lab.gen008_exec import (
    baseline_is_descriptive,
    build_round0_plan,
    choose_batch_items,
    choose_horizon,
    execute_item,
    install_plan,
    merge_items,
    verify_generation,
)
from rs_constraint_lab.state import relabel_relation_state
from rs_constraint_lab.supervisor import format_status, supervise
from rs_constraint_lab.workstore import Layout

PYTHON = sys.executable
LAB = Path(__file__).resolve().parents[1]
SRC = LAB / "src" / "rs_constraint_lab"
LABEL = re.compile(r"^p\d{2}-t\d{2}-s\d+$")
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


def _sources():
    return enumerate_hidden_contexts()


def _star_context() -> dict:
    sources = _sources()
    return {**sources["star"]["orbits"][0], "class_index": sources["star"]["class_index"]}


def _identity(context: dict, replicate: int, round_id: str = "round-test", system_id: str = "S00") -> dict:
    return {
        "experiment_id": EXPERIMENT_ID,
        "hidden_context_orbit_id": context["hidden_context_orbit_id"],
        "replicate_index": replicate,
        "round_id": round_id,
        "source_graph_class": context["source_graph_class"],
        "system_id": system_id,
    }


def _run(system: dict, *, horizon: int = 16, cap: int = 64, replicate: int = 0) -> dict:
    context = _star_context()
    return run_episode(
        experiment_id=EXPERIMENT_ID,
        round_id="round-test",
        system=system,
        context=context,
        replicate=replicate,
        pair_horizon=horizon,
        full_event_cap=cap,
        plan_hash_value="unit",
        frozen_plan_commit="0" * 40,
    )


def _mini_plan(**overrides) -> dict:
    context = _star_context()
    context.pop("class_index")
    document = {
        "batch_item_count": 1,
        "batch_note": "test",
        "contexts": [context],
        "experiment_id": EXPERIMENT_ID,
        "full_event_cap": 64,
        "pair_horizon": 8,
        "replay_fraction": 1.0,
        "replicates": 2,
        "round_id": "round-test",
        "systems": [build_round0_systems()[0]],
    }
    document.update(overrides)
    document["plan_hash"] = plan_hash(document)
    return document


def _install(tmp_path: Path, document: dict) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    root = tmp_path / "run"
    commit = _commit_plan(repo, document)
    install_plan(root, repo / "plan.json", commit, repo, "plan.json", require_remote=False)
    return root, commit


def test_hidden_context_orbits_partition_each_source() -> None:
    sources = _sources()
    assert source_masks() == {"star": 7, "path": 13, "triangle": 11}
    expected = {"star": (8, 6), "path": (10, 2), "triangle": (8, 6)}
    total = 0
    for key, (orbits, autos) in expected.items():
        record = sources[key]
        assert record["orbit_count"] == orbits
        assert record["automorphism_group_size"] == autos
        seen: list[int] = []
        for orbit in record["orbits"]:
            assert orbit["orbit_size"] == len(orbit["members"])
            assert orbit["members"] == sorted(orbit["members"])
            assert orbit["canonical_triad"] == orbit["members"][0]
            assert orbit["start_state"] == record["canonical_pair_mask"] | (orbit["members"][0] << 6)
            seen.extend(orbit["members"])
        assert sorted(seen) == list(range(16))
        total += orbits
    assert total == 26


def test_stabiliser_keeps_equivalent_contexts_together() -> None:
    sources = _sources()
    slots = _slots()
    cache = dynamic_cache()
    for key in ("star", "path", "triangle"):
        record = sources[key]
        mask = record["canonical_pair_mask"]
        autos = pair_automorphisms(mask)
        assert len(autos) == record["automorphism_group_size"]
        labels = set()
        for orbit in record["orbits"]:
            group = set(orbit["members"])
            orbit_labels = set()
            for triad in group:
                state = mask | (triad << 6)
                orbit_labels.add(_context_label(state, cache))
                for perm in autos:
                    image = relabel_relation_state(state, perm, slots)
                    assert (image & 63) == mask
                    assert (image >> 6) in group
            assert len(orbit_labels) == 1
            labels.add(orbit_labels.pop())
        assert len(labels) == record["orbit_count"]


def test_pair_states_use_the_eleven_classes() -> None:
    assert len(CLASS_NAMES) == 11
    assert len(CLASS_OF_MASK) == 64
    assert {int(index) for index in CLASS_OF_MASK} == set(range(11))
    sources = _sources()
    assert sources["star"]["class_name"] == "e3-deg3111-tri0-comp1"
    assert sources["path"]["class_name"] == "e3-deg2211-tri0-comp1"
    assert sources["triangle"]["class_name"] == "e3-deg2220-tri1-comp2"


def test_round0_palette_comes_from_the_prior_tables() -> None:
    forms = derive_tp_archetypes()
    assert forms == [
        "dissolve(0-1) | absent(0-1-2)",
        "dissolve(0-1) | absent(0-2-3)",
        "dissolve(0-1) | present(0-1-2)",
        "dissolve(0-1) | present(0-2-3)",
        "form(0-1) | absent(0-1-2)",
        "form(0-1) | absent(0-2-3)",
        "form(0-1) | present(0-1-2)",
        "form(0-1) | present(0-2-3)",
    ]
    anchor = derive_composite_anchor()
    assert anchor["pair_id"] == "07f18bb89362ae4ea6606830"
    assert anchor["tie_pair_ids"] == [
        "07f18bb89362ae4ea6606830",
        "600141626a884b274e29285f",
        "83e30a0d85355dd29a222456",
        "c611dd214ae35aa8cf9e5cb8",
    ]
    assert anchor["pp_expression"] == "dissolve(0-1) => strong_suppress"
    assert anchor["tp_expression"] == "dissolve(2-3) | present(0-1-2) => strong_suppress"
    systems = build_round0_systems()
    assert len(systems) == 10
    assert systems[0]["role"] == BASELINE_ROLE
    assert systems[0]["expressions"] == []
    assert systems[-1]["system_id"] == "S09"
    assert all("prohibit" not in expression for system in systems for expression in system["expressions"])
    benchmark = {
        "event_count": 600,
        "gzip_bytes": 8000,
        "pair_event_count": 512,
        "pair_horizon": 512,
        "raw_bytes": 30000,
        "replay_seconds": 0.02,
        "seconds": 0.2,
    }
    plan = build_round0_plan(horizon=512, benchmark=benchmark, batch_items=40, batch_note="test")
    assert plan["work_count"]["total_round_episodes"] == 4160
    assert plan["work_count"]["total_hidden_context_starts"] == 26
    assert plan["plan_hash"] == plan_hash(plan)
    assert baseline_is_descriptive(plan)
    mutated = json.loads(json.dumps(plan))
    mutated["pair_horizon"] = 256
    assert plan_hash(mutated) != plan["plan_hash"]
    mutated = json.loads(json.dumps(plan))
    mutated["seed_function"] = "other"
    assert plan_hash(mutated) != plan["plan_hash"]
    mutated = json.loads(json.dumps(plan))
    mutated["systems"][1]["expressions"][0] += " extra"
    assert plan_hash(mutated) != plan["plan_hash"]
    mutated = json.loads(json.dumps(plan))
    mutated["contexts"][0]["hidden_context_orbit_id"] += "-other"
    assert plan_hash(mutated) != plan["plan_hash"]


def test_seed_derivation_is_deterministic() -> None:
    context = _star_context()
    left = _identity(context, 0)
    assert derive_seed(left) == derive_seed(dict(left))
    assert episode_id_for(left) == episode_id_for(dict(left))
    right = dict(left)
    right["replicate_index"] = 1
    assert derive_seed(right) != derive_seed(left)
    assert episode_id_for(right) != episode_id_for(left)


def test_episode_draw_matches_the_integer_kernel_and_replays() -> None:
    result = _run(build_round0_systems()[0], horizon=24)
    header = result["header"]
    assert header["termination_reason"] == "pair_horizon"
    assert header["pair_event_count"] == 24
    assert sum(run[1] for run in result["summary"]["class_runs"]) == 25
    assert sum(result["summary"]["transition_counts"]) == 24
    assert result["summary"]["transition_counts"] == transition_counts_from_events(result["events"])
    for event in result["events"]:
        weights = [Fraction(text) for text in event["weights"]]
        assert sum(weights) > 0
        assert event["uniform_draw"] == f"{event['draw']}/{event['norm']}"
        assert event["probability"] == f"{event['selected_integer']}/{event['norm']}"
        assert 0 <= event["draw"] < event["norm"]
        assert LABEL.fullmatch(event["context_before"])
        assert LABEL.fullmatch(event["context_after"])
        integer_total = 0
        common = 1
        for weight in weights:
            common = common * weight.denominator // __import__("math").gcd(common, weight.denominator)
        for weight in weights:
            integer_total += int(weight * common)
        assert integer_total == event["norm"]
    report = replay_events(header, result["events"], build_round0_systems()[0], initial_state=header["initial_state"])
    assert report["verification"] == "exact"
    chained = run_chained(
        segment_pair_epochs=8,
        experiment_id=EXPERIMENT_ID,
        round_id="round-test",
        system=build_round0_systems()[0],
        context=_star_context(),
        replicate=0,
        pair_horizon=24,
        full_event_cap=64,
        plan_hash_value="unit",
        frozen_plan_commit="0" * 40,
    )
    assert [event["post"] for event in chained["events"]] == [event["post"] for event in result["events"]]
    assert chained["header"]["trajectory_hash"] == header["trajectory_hash"]
    assert chained["header"]["event_payload_sha256"] == header["event_payload_sha256"]
    assert chained["header"]["termination_reason"] == "pair_horizon"


def test_full_event_cap_and_empty_support_are_observations() -> None:
    capped = _run(build_round0_systems()[0], horizon=1000, cap=5)
    assert capped["header"]["termination_reason"] == "full_event_cap"
    assert capped["header"]["event_count"] == 5
    from rs_constraint_lab.state import relation_slots

    expressions = []
    for slot in relation_slots(4, 3):
        text = "-".join(str(index) for index in slot)
        expressions.append(f"form({text}) => prohibit")
        expressions.append(f"dissolve({text}) => prohibit")
    halted = _run({"expressions": expressions, "role": "support-boundary", "system_id": "halt"}, horizon=8)
    assert halted["header"]["termination_reason"] == "no_admissible_event"
    assert halted["events"] == []
    report = replay_events(
        halted["header"],
        halted["events"],
        {"expressions": expressions, "system_id": "halt"},
        initial_state=halted["header"]["initial_state"],
    )
    assert report["verification"] == "exact"


def test_routes_are_recomputed_from_runs() -> None:
    sources = _sources()
    context = _star_context()
    result = _run(build_round0_systems()[1], horizon=32)
    row = episode_row(result)
    row["route"] = {"route_outcome": "route to star", "destination": "route to star"}
    recomputed = route_from_runs(
        row["class_runs"],
        sources["star"]["class_index"],
        {record["class_index"] for record in sources.values()},
        row["pair_event_count"],
    )
    atlas = atlas_from_summaries([row], sources)
    rendered = json.dumps(atlas["routing"])
    assert "route to star" not in rendered
    assert "p_value" not in json.dumps(atlas)
    assert atlas["routing"][0]["orbit_size"] == context["orbit_size"]
    assert atlas["routing"][0]["destinations"]
    assert recomputed["route_outcome"] in set(atlas["routing"][0]["destinations"]) | {"censored_at_horizon"}


def test_query_filters_pair_class_source_and_motif() -> None:
    sources = _sources()
    star = sources["star"]["class_name"]
    path = sources["path"]["class_name"]
    markers = [
        {
            "episode_id": "a",
            "hidden_context_orbit_id": "path-o00",
            "pair_after": CLASS_NAMES.index(star),
            "pair_before": CLASS_NAMES.index(path),
            "source_graph_class": "path",
            "system_id": "S00",
            "triad_before": 3,
        },
        {
            "episode_id": "b",
            "hidden_context_orbit_id": "star-o00",
            "pair_after": CLASS_NAMES.index(path),
            "pair_before": CLASS_NAMES.index(star),
            "source_graph_class": "star",
            "system_id": "S01",
            "triad_before": 1,
        },
    ]
    episodes = [
        {"class_runs": [[CLASS_NAMES.index(path), 1], [CLASS_NAMES.index(star), 1]], "episode_id": "a"},
        {"class_runs": [[CLASS_NAMES.index(star), 2]], "episode_id": "b"},
    ]
    found = query_transitions(markers, source_class=path, target_class=star)
    assert [row["episode_id"] for row in found] == ["a"]
    by_source = query_transitions(markers, source_class="path", orbit_id="path-o00")
    assert [row["episode_id"] for row in by_source] == ["a"]
    triads = query_transitions(markers, triad_count=2)
    assert [row["episode_id"] for row in triads] == ["a"]
    motif = query_transitions(markers, motif=[path, star], episodes=episodes)
    assert [row["episode_id"] for row in motif] == ["a"]


def test_attention_and_operators_stay_inside_the_bounds() -> None:
    vector = attention_vector({"CN": 1, "RD": 2, "RC": 3, "EC": 4, "CG": 5, "CB": 0})
    assert list(vector) == ["CN", "RD", "RC", "EC", "CG", "CB"]
    with pytest.raises(ValueError):
        attention_vector({**vector, "total": 15})
    with pytest.raises(ValueError):
        attention_vector({**vector, "CN": True})
    systems = build_round0_systems()
    tp = derive_tp_archetypes()
    pp = derive_pp_archetypes()
    shifted = apply_operator(
        systems[1],
        {"grade": "weak_favour", "op": "weight_shift", "rule_index": 0, "system_id": "P1"},
        tp_forms=tp,
        pp_forms=pp,
    )
    assert shifted["expressions"][0].endswith("=> weak_favour")
    with pytest.raises(ValueError):
        apply_operator(
            systems[1],
            {"grade": "prohibit", "op": "weight_shift", "rule_index": 0, "system_id": "P2"},
            tp_forms=tp,
            pp_forms=pp,
        )
    flipped = apply_operator(
        systems[1],
        {"op": "condition_polarity_flip", "rule_index": 0, "system_id": "P3"},
        tp_forms=tp,
        pp_forms=pp,
    )
    assert ("present(" in systems[1]["expressions"][0]) != ("present(" in flipped["expressions"][0])
    added = apply_operator(
        systems[1],
        {"op": "add_pp_companion", "structural_expression": pp[0], "system_id": "P4"},
        tp_forms=tp,
        pp_forms=pp,
    )
    assert len(added["expressions"]) == 2
    with pytest.raises(ValueError):
        apply_operator(
            systems[1],
            {"grade": "prohibit", "op": "add_pp_companion", "structural_expression": pp[0], "system_id": "P5"},
            tp_forms=tp,
            pp_forms=pp,
        )
    with pytest.raises(ValueError):
        apply_operator(
            systems[-1],
            {"op": "add_pp_companion", "structural_expression": pp[0], "system_id": "P6"},
            tp_forms=tp,
            pp_forms=pp,
        )
    removed = apply_operator(
        systems[-1],
        {"op": "remove_rule", "rule_index": 1, "system_id": "P7"},
        tp_forms=tp,
        pp_forms=pp,
    )
    assert len(removed["expressions"]) == 1
    neighbour = apply_operator(
        systems[1],
        {"op": "structural_tp_neighbour", "structural_expression": tp[3], "system_id": "P8"},
        tp_forms=tp,
        pp_forms=pp,
    )
    assert neighbour["expressions"][0].startswith(tp[3])


def test_horizon_rule_reads_cost_only() -> None:
    fast = {"gzip_bytes": 1000, "pair_horizon": 512, "replay_seconds": 0.01, "seconds": 0.2}
    assert choose_horizon(fast, 4160)["pair_horizon"] == 512
    slow = {"gzip_bytes": 1000, "pair_horizon": 512, "replay_seconds": 0.01, "seconds": 10}
    assert choose_horizon(slow, 4160)["pair_horizon"] == 256
    slower = {"gzip_bytes": 1000, "pair_horizon": 512, "replay_seconds": 0.01, "seconds": 20.5}
    assert choose_horizon(slower, 4160)["pair_horizon"] == 128
    refused = choose_horizon({**slower, "seconds": 100}, 4160)
    assert refused["refused"] is True
    assert refused["pair_horizon"] is None
    with pytest.raises(RuntimeError):
        choose_horizon({**fast, "route_outcome": "star"}, 10)
    items, note = choose_batch_items(0.5)
    assert items == 90
    assert "45" in note
    capped, floor_note = choose_batch_items(0.01)
    assert capped == 120
    assert "30s" in floor_note


def test_replay_sample_is_deterministic() -> None:
    ids = [f"episode-{index:02d}" for index in range(10)]
    assert select_replay_ids(ids, 1) == sorted(ids)
    assert select_replay_ids(ids, 0) == []
    sample = select_replay_ids(ids, 0.1)
    assert sample == select_replay_ids(list(reversed(ids)), 0.1)
    assert len(sample) >= 1


def test_status_lines_appear_only_for_a_round() -> None:
    plain = format_status({"experiment_id": "fault", "state": "RUNNING", "phase": "01"})
    assert "Round:" not in plain
    assert "State: RUNNING" in plain
    rounded = format_status(
        {
            "disk_used_bytes": 12,
            "episodes_complete": 1,
            "episodes_planned": 4,
            "events_written": 8,
            "experiment_id": EXPERIMENT_ID,
            "last_completed_episode": "abc",
            "phase": "04_TRAJECTORIES",
            "recent_items_per_second": 0.5,
            "round_id": "round-000",
            "state": "RUNNING",
            "systems_complete": 0,
            "systems_planned": 10,
        }
    )
    assert "Round: round-000" in rounded
    assert "Episodes: 1 / 4 complete" in rounded
    assert "Events written: 8" in rounded
    assert "Last completed episode: abc" in rounded


def test_engine_does_not_encode_a_destination() -> None:
    forbidden = (
        "seek organisation",
        "seek repair",
        "seek boundary",
        "route to star",
        "p_value",
        "maximum routing divergence",
    )
    for name in ("explore08.py", "gen008_exec.py"):
        text = (SRC / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text
    assert BASELINE_ROLE == "baseline relational dynamics"
    assert baseline_is_descriptive({"systems": [{"expressions": [], "role": "the null hypothesis", "system_id": "S00"}]}) is False


def test_execution_refuses_a_missing_frozen_commit(tmp_path: Path) -> None:
    with pytest.raises(FrozenPlanError):
        require_frozen_plan(tmp_path, None, "plan.json")
    with pytest.raises(FrozenPlanError):
        require_frozen_plan(tmp_path, "abc", "plan.json")
    layout = Layout(tmp_path / "run")
    layout.ensure()
    atomic_write_json(layout.manifest_path(), {"experiment_id": EXPERIMENT_ID})
    with pytest.raises(FrozenPlanError):
        execute_item({"input": {}, "kind": "episode"}, {"root": tmp_path / "run"})


def test_remote_gate_and_plan_drift(tmp_path: Path) -> None:
    document = _mini_plan()
    repo = tmp_path / "repo"
    commit = _commit_plan(repo, document)
    with pytest.raises(FrozenPlanError):
        install_plan(tmp_path / "run", repo / "plan.json", commit, repo, "plan.json", require_remote=True)
    drifted = json.loads((repo / "plan.json").read_text(encoding="utf-8"))
    drifted["pair_horizon"] = 4
    (repo / "plan.json").write_text(json.dumps(drifted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(FrozenPlanError):
        install_plan(tmp_path / "drift", repo / "plan.json", commit, repo, "plan.json", require_remote=False)


def test_mini_atlas_replays_and_rejects_a_corrupt_stream(tmp_path: Path) -> None:
    root, commit = _install(tmp_path, _mini_plan())
    first = supervise(root, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    assert first["state"] == "COMPLETE"
    hashes = {path.name: path.read_bytes() for path in (root / "items").glob("*.json")}
    second = supervise(root, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    assert second["state"] == "COMPLETE"
    assert {path.name: path.read_bytes() for path in (root / "items").glob("*.json")} == hashes
    summary = merge_items(root)
    assert summary["episodes"] == 2
    assert summary["replay_exact"] == 2
    assert summary["frozen_plan_commit"] == commit
    report = verify_generation(root, require_complete=True)
    assert report["ok"] is True
    stored = None
    for path in (root / "items").glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("kind") == "episode":
            stored = payload
            break
    assert stored is not None
    assert stored["result"]["frozen_plan_commit"] == commit
    stream = root / stored["result"]["event_stream"]
    original = stream.read_bytes()
    stream.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
    corrupted = verify_generation(root, require_complete=True)
    assert corrupted["ok"] is False
    assert any("corrupt" in problem for problem in corrupted["problems"])
    again = merge_items(root)
    assert again["episodes"] == summary["episodes"]


def test_timeout_quarantines_only_the_stalling_episode(tmp_path: Path) -> None:
    context = _star_context()
    context.pop("class_index")
    stalled = episode_id_for(_identity(context, 1))
    document = _mini_plan(fault_stall_episode_id=stalled, fault_stall_seconds=30, replay_fraction=0)
    root, _commit = _install(tmp_path, document)
    payload = supervise(root, workers=1, batch_size=1, heartbeat=0.2, watchdog=1, max_attempts=2, max_wall=20)
    assert payload["quarantined_items"] == 1
    assert payload["state"] == "PARTIAL"
    completed = []
    for path in (root / "items").glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        if item.get("kind") != "episode":
            continue
        completed.append(item["result"]["episode_id"])
    assert completed == [episode_id_for(_identity(context, 0))]
    assert stalled not in completed
    kinds = [
        json.loads(line).get("kind")
        for line in (root / "plan" / "work-items.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert "replay" not in kinds
    assert kinds.count("episode") == 2


def test_running_batches_lists_generation008_workers(tmp_path: Path) -> None:
    context = _star_context()
    context.pop("class_index")
    stalled = [
        episode_id_for(_identity(context, replicate))
        for replicate in (0, 1)
    ]
    document = _mini_plan(fault_stall_episode_ids=stalled, fault_stall_seconds=8, replay_fraction=0)
    root, _commit = _install(tmp_path, document)
    code = (
        "import sys\n"
        "from rs_constraint_lab.supervisor import supervise\n"
        "supervise(sys.argv[1], workers=2, batch_size=1, heartbeat=0.2, watchdog=30, max_wall=12)\n"
    )
    proc = subprocess.Popen([PYTHON, "-c", code, str(root)], cwd=LAB, text=True)
    try:
        seen = None
        deadline = time.time() + 10
        while time.time() < deadline:
            path = root / "progress" / "status.json"
            if path.exists():
                seen = json.loads(path.read_text(encoding="utf-8"))
                if len(seen.get("running_batches") or []) >= 2:
                    break
            time.sleep(0.05)
        assert seen is not None
        rows = seen["running_batches"]
        assert len(rows) == 2
        assert len({row["worker_pid"] for row in rows}) == 2
        assert seen["round_id"] == "round-test"
    finally:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=20)
