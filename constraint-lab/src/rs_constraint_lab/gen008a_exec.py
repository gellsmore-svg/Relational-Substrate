"""Micro-batch adapter for Generation 8A raw-context trajectories.

Scientific trajectories start only after a frozen plan commit is on a
remote-tracking branch. The seed uses the raw triad configuration.
Graph-only and rule-aware orbit ids are header metadata.
"""

from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, read_json, sha256_file
from rs_constraint_lab.explore08 import (
    CHECKPOINTS,
    FULL_EVENT_CAP,
    FrozenPlanError,
    atlas_from_summaries,
    dynamic_cache,
    enumerate_hidden_contexts,
    episode_row,
    iter_jsonl_gzip,
    plan_hash,
    replay_events,
    require_frozen_plan,
    route_from_runs,
    run_episode,
    select_replay_ids,
    three_edge_indexes,
    write_jsonl_gzip,
    write_stream,
)
from rs_constraint_lab.explore08a import (
    EXPERIMENT_ID,
    REPLAY_FRACTION,
    REPLICATES,
    ROUND_ID,
    RUNNER_VERSION,
    SEED_FIELDS,
    SEED_FUNCTION,
    SEMANTIC_VERSION,
    SMOKE_REPLAY,
    analysis_measure_catalogue,
    crosswalk,
    derive_seed,
    episode_id_for,
    graph_only_splits,
    load_repair_palette,
    raw_execution_contexts,
    repair_from_rows,
    seed_identity,
    symmetry_table,
    system_occupancy,
    additive_residual,
)
from rs_constraint_lab.gen008_exec import choose_batch_items, choose_horizon
from rs_constraint_lab.supervisor import ensure_planned
from rs_constraint_lab.workstore import (
    Layout,
    load_state,
    load_work_items,
    log_progress,
    make_item_record,
    read_valid_item,
)

ANALYSIS_VERSION = RUNNER_VERSION
_STORED_OMIT = frozenset({"edge_count_sequence", "markers", "triad_count_sequence"})
_PLAN_CACHE: dict[str, dict] = {}


def _load_round_plan(layout: Layout) -> dict:
    key = str(layout.root.resolve())
    cached = _PLAN_CACHE.get(key)
    if cached is not None:
        return cached
    plan = read_json(layout.plan() / "round-plan.json")
    _PLAN_CACHE[key] = plan
    return plan


def _context_index(plan: dict) -> dict[tuple[str, str], dict]:
    return {
        (row["source_graph_class"], row["triad_config_id"]): row
        for row in plan["contexts"]
    }


def _system_index(plan: dict) -> dict[str, dict]:
    return {row["system_id"]: row for row in plan["systems"]}


def benchmark_cost(*, horizon: int = 512) -> dict:
    """Time one baseline episode and one labelled episode.

    The sample records durations and byte counts. It does not record a route.
    """
    contexts = raw_execution_contexts()
    context = next(row for row in contexts if row["source_graph_class"] == "star" and row["triad_config_id"] == "t00")
    systems = load_repair_palette()
    cache = dynamic_cache()
    samples = []
    for system in (systems[0], systems[1]):
        identity = seed_identity(
            {
                "experiment_id": EXPERIMENT_ID,
                "raw_triad_config": context["raw_triad_config"],
                "replicate_index": 0,
                "round_id": "preflight",
                "source_graph_class": context["source_graph_class"],
                "system_id": system["system_id"],
            }
        )
        started = time.perf_counter()
        result = run_episode(
            experiment_id=EXPERIMENT_ID,
            round_id="preflight",
            system=system,
            context=context,
            replicate=0,
            pair_horizon=horizon,
            full_event_cap=FULL_EVENT_CAP,
            plan_hash_value="preflight",
            frozen_plan_commit="0" * 40,
            cache=cache,
            identity=identity,
            header_extra={"runner_version": RUNNER_VERSION, "triad_config_id": context["triad_config_id"]},
        )
        elapsed = time.perf_counter() - started
        replay_started = time.perf_counter()
        report = replay_events(
            result["header"],
            result["events"],
            system,
            initial_state=int(context["start_state"]),
        )
        replay_elapsed = time.perf_counter() - replay_started
        if report["verification"] != "exact":
            raise RuntimeError(f"preflight replay mismatch: {report}")
        import gzip

        compressed = gzip.compress(result["payload"], mtime=0)
        samples.append(
            {
                "event_count": len(result["events"]),
                "gzip_bytes": len(compressed),
                "pair_event_count": result["summary"]["pair_event_count"],
                "pair_horizon": horizon,
                "raw_bytes": len(result["payload"]),
                "replay_seconds": replay_elapsed,
                "seconds": elapsed,
                "system_id": system["system_id"],
            }
        )
    slowest = max(samples, key=lambda row: row["seconds"])
    largest = max(samples, key=lambda row: row["gzip_bytes"])
    return {
        "event_count": largest["event_count"],
        "gzip_bytes": largest["gzip_bytes"],
        "pair_event_count": largest["pair_event_count"],
        "pair_horizon": horizon,
        "raw_bytes": largest["raw_bytes"],
        "replay_seconds": max(row["replay_seconds"] for row in samples),
        "seconds": slowest["seconds"],
        "samples": [
            {
                key: row[key]
                for key in (
                    "event_count",
                    "gzip_bytes",
                    "pair_event_count",
                    "raw_bytes",
                    "replay_seconds",
                    "seconds",
                    "system_id",
                )
            }
            for row in samples
        ],
    }


def build_a0_plan(
    *,
    horizon: int,
    benchmark: dict,
    batch_items: int,
    batch_note: str,
    systems: list[dict] | None = None,
    contexts: list[dict] | None = None,
    replicates: int | None = None,
    round_id: str = ROUND_ID,
    replay_fraction: float | None = None,
) -> dict:
    chosen = systems if systems is not None else load_repair_palette()
    starts = contexts if contexts is not None else raw_execution_contexts()
    replicate_count = REPLICATES if replicates is None else replicates
    symmetry = symmetry_table(chosen)
    bridges = crosswalk(chosen, starts, symmetry)
    splits = graph_only_splits(symmetry, starts)
    episodes = len(chosen) * len(starts) * replicate_count
    scale = horizon / float(benchmark["pair_horizon"])
    event_count = int(round(float(benchmark["event_count"]) * scale))
    document = {
        "alphabet": "W4",
        "analysis_measures": analysis_measure_catalogue(),
        "batch_item_count": batch_items,
        "batch_note": batch_note,
        "checkpoints": list(CHECKPOINTS),
        "contexts": starts,
        "context_method": {
            "analysis_basis": "optional graph-only and rule-aware symmetry classes after execution",
            "execution_basis": "all raw triad configurations",
            "quotient_before_execution": False,
            "statement": (
                "Do not quotient hidden triad starts. Execute all 16 raw configurations "
                "for each visible source graph. Symmetry describes equivalence after the "
                "trajectories exist."
            ),
        },
        "crosswalk": bridges,
        "experiment_id": EXPERIMENT_ID,
        "full_event_cap": FULL_EVENT_CAP,
        "graph_only_splits": splits,
        "legacy_comparator": (
            "Generation 8 trajectories are not Generation 8A replicates. "
            "A matching initial state is not reused."
        ),
        "mode": "B",
        "observables": [
            "complete_event_stream",
            "pair_class_trajectory",
            "triad_trajectory",
            "full_state_trajectory",
            "transition_markers",
            "source_returns",
            "route_to_next_3edge_class",
            "occupancy_vector",
            "entropy",
            "triad_only_fraction",
            "uniform_raw_context_information",
            "current_triad_conditional_information",
            "full_pair_mask_versus_isomorphism_class",
        ],
        "ontology": {"G": 0, "H": 0, "L": 0, "N": 4, "O": 3, "S": 0, "grammar": "independent-hypergraph"},
        "pair_horizon": horizon,
        "prohibit_in_round": False,
        "replay_fraction": REPLAY_FRACTION if replay_fraction is None else replay_fraction,
        "replicates": replicate_count,
        "representative_rule": (
            "largest destination JS, largest occupancy L1, largest full-pair-mask "
            "current-triad conditional mutual information, smallest destination JS; "
            "ties break by system, source, and config id; episode is replicate 0"
        ),
        "round_id": round_id,
        "round_limits": {"max_rounds": 3, "round_ids": ["round-a0", "round-a1", "round-a2"]},
        "schema": "rs-constraint-lab.context-repair-plan/v1",
        "seed_fields": list(SEED_FIELDS),
        "seed_function": SEED_FUNCTION,
        "smoke_replay": SMOKE_REPLAY,
        "source_graph_class_count": 3,
        "symmetry": symmetry,
        "systems": chosen,
        "work_count": {
            "batch_item_count": batch_items,
            "benchmark_episode_microseconds": int(round(float(benchmark["seconds"]) * 1_000_000)),
            "benchmark_replay_microseconds": int(round(float(benchmark["replay_seconds"]) * 1_000_000)),
            "compressed_bytes_per_benchmark_episode": int(benchmark["gzip_bytes"]),
            "episode_pair_horizon": horizon,
            "estimated_compressed_bytes": int(int(benchmark["gzip_bytes"]) * scale * episodes),
            "estimated_event_records": event_count * episodes,
            "estimated_raw_bytes": int(int(benchmark["raw_bytes"]) * scale * episodes),
            "estimated_wall_seconds": int(round(float(benchmark["seconds"]) * scale * episodes / 2)),
            "raw_bytes_per_benchmark_episode": int(benchmark["raw_bytes"]),
            "raw_triad_configurations_per_source": 16,
            "replicates_per_start": replicate_count,
            "source_graph_classes": 3,
            "starts_per_system": len(starts),
            "systems": len(chosen),
            "total_round_episodes": episodes,
            "worst_case_full_events": episodes * FULL_EVENT_CAP,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def prepare_a0_plan(*, sample_horizon: int = 512) -> dict:
    sample = benchmark_cost(horizon=sample_horizon)
    episodes = len(PALETTE_SIZE()) * 48 * REPLICATES
    decision = choose_horizon(sample, episodes)
    if decision.get("refused") or decision.get("pair_horizon") is None:
        return {"benchmark": sample, "decision": decision, "plan": None}
    items, note = choose_batch_items(float(sample["seconds"]) * (decision["pair_horizon"] / sample_horizon))
    plan = build_a0_plan(
        horizon=int(decision["pair_horizon"]),
        benchmark=sample,
        batch_items=items,
        batch_note=note,
    )
    return {"benchmark": sample, "decision": decision, "plan": plan}


def PALETTE_SIZE() -> list[str]:
    return [row["system_id"] for row in load_repair_palette()]


def install_plan(
    root: Path,
    plan_path: Path,
    commit: str,
    repo: Path,
    relpath: str,
    *,
    require_remote: bool = True,
) -> dict:
    plan = require_frozen_plan(repo, commit, relpath, disk_path=plan_path)
    if require_remote and not remote_contains(repo, commit):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    layout = Layout(root)
    layout.ensure()
    atomic_write_json(layout.plan() / "round-plan.json", plan)
    _PLAN_CACHE[str(layout.root.resolve())] = plan
    manifest = {
        "advance": "rs_constraint_lab.gen008a_exec:advance",
        "analysis_version": ANALYSIS_VERSION,
        "counts": "rs_constraint_lab.gen008a_exec:counts",
        "executor": "rs_constraint_lab.gen008a_exec:execute_item",
        "experiment_id": plan["experiment_id"],
        "frozen_plan_commit": commit,
        "heartbeat_seconds": 10,
        "merge": "rs_constraint_lab.gen008a_exec:merge_items",
        "phase": "rs_constraint_lab.gen008a_exec:phase",
        "plan_hash": plan["plan_hash"],
        "plan_relpath": relpath,
        "repo": str(repo),
        "require_remote": require_remote,
        "round_id": plan["round_id"],
        "semantic_version": SEMANTIC_VERSION,
        "spec_hash": plan["plan_hash"],
        "watchdog_seconds": 120,
    }
    atomic_write_json(layout.manifest_path(), manifest)
    items = plan.get("batch_item_count", 1)
    note = plan.get("batch_note", "")
    atomic_write_json(
        layout.policy_path(),
        {
            "kinds": {"default": {"items": items}, "episode": {"items": items}, "replay": {"items": items}},
            "note": note,
        },
    )
    atomic_write_json(layout.dependency_path(), {"replay_planned": False})
    planned = 0
    for system in plan["systems"]:
        for context in plan["contexts"]:
            for replicate in range(int(plan["replicates"])):
                identity = seed_identity(
                    {
                        "experiment_id": plan["experiment_id"],
                        "raw_triad_config": context["raw_triad_config"],
                        "replicate_index": replicate,
                        "round_id": plan["round_id"],
                        "source_graph_class": context["source_graph_class"],
                        "system_id": system["system_id"],
                    }
                )
                item_input = {
                    **identity,
                    "episode_id": episode_id_for(identity),
                    "frozen_plan_commit": commit,
                    "full_event_cap": plan["full_event_cap"],
                    "pair_horizon": plan["pair_horizon"],
                    "plan_hash": plan["plan_hash"],
                    "seed": derive_seed(identity),
                    "triad_config_id": context["triad_config_id"],
                }
                record = make_item_record(
                    plan["plan_hash"], SEMANTIC_VERSION, ANALYSIS_VERSION, "episode", item_input
                )
                if ensure_planned(layout, record):
                    planned += 1
    summary = {
        "episodes": len(plan["systems"]) * len(plan["contexts"]) * int(plan["replicates"]),
        "frozen_plan_commit": commit,
        "plan_hash": plan["plan_hash"],
        "planned_new_items": planned,
        "round_id": plan["round_id"],
    }
    atomic_write_json(layout.plan() / "plan.json", summary)
    log_progress(layout, f"PLAN round={plan['round_id']} new_items={planned} commit={commit}")
    return summary


def remote_contains(repo: Path, commit: str) -> bool:
    from rs_constraint_lab.explore08 import remote_contains as _remote_contains

    return _remote_contains(repo, commit)


def _refuse_unfrozen(manifest: dict, layout: Layout, context: dict) -> None:
    if context.get("frozen_checked"):
        return
    commit = manifest.get("frozen_plan_commit")
    repo = manifest.get("repo")
    relpath = manifest.get("plan_relpath")
    if not repo or not relpath:
        raise FrozenPlanError("execution refused: manifest does not name the frozen plan")
    require_frozen_plan(Path(repo), commit, relpath, disk_path=layout.plan() / "round-plan.json")
    if manifest.get("require_remote", True) and not remote_contains(Path(repo), str(commit)):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    context["frozen_checked"] = True


def execute_item(record: dict, context: dict) -> dict:
    layout = Layout(context["root"])
    manifest = read_json(layout.manifest_path())
    _refuse_unfrozen(manifest, layout, context)
    commit = manifest["frozen_plan_commit"]
    plan = _load_round_plan(layout)
    if record["kind"] == "replay":
        return _execute_replay(layout, record, plan)
    if record["kind"] != "episode":
        raise RuntimeError(f"unknown work kind {record['kind']}")
    system = _system_index(plan)[record["input"]["system_id"]]
    orbit = _context_index(plan)[
        (record["input"]["source_graph_class"], record["input"]["triad_config_id"])
    ]
    aware = plan["symmetry"][system["system_id"]][orbit["source_graph_class"]]["lookup"][orbit["triad_config_id"]]
    identity = seed_identity(record["input"])
    if identity["raw_triad_config"] != orbit["triad_config_id"]:
        raise RuntimeError("raw triad configuration drifted from the execution context")
    header_extra = {
        "directly_sampled_in_generation8": orbit["directly_sampled_in_generation8"],
        "graph_only_orbit_id": orbit["graph_only_orbit_id"],
        "graph_only_orbit_size": orbit["graph_only_orbit_size"],
        "raw_triad_config": orbit["raw_triad_config"],
        "rule_aware_orbit_id": aware["rule_aware_orbit_id"],
        "rule_aware_orbit_size": aware["rule_aware_orbit_size"],
        "runner_version": RUNNER_VERSION,
        "triad_config_id": orbit["triad_config_id"],
    }
    compiled = {**orbit, "hidden_context_orbit_id": orbit["triad_config_id"], "orbit_size": 1}
    stall_ids = list(plan.get("fault_stall_episode_ids") or [])
    if plan.get("fault_stall_episode_id"):
        stall_ids.append(plan["fault_stall_episode_id"])
    stall = None
    if record["input"]["episode_id"] in stall_ids:
        stall = float(plan.get("fault_stall_seconds", 30))
    result = run_episode(
        experiment_id=plan["experiment_id"],
        round_id=plan["round_id"],
        system=system,
        context=compiled,
        replicate=int(record["input"]["replicate_index"]),
        pair_horizon=int(plan["pair_horizon"]),
        full_event_cap=int(plan["full_event_cap"]),
        plan_hash_value=plan["plan_hash"],
        frozen_plan_commit=str(commit),
        cache=context.setdefault("dynamic", dynamic_cache()),
        stall_seconds=stall,
        identity=identity,
        header_extra=header_extra,
    )
    if result["header"]["seed"] != record["input"]["seed"]:
        raise RuntimeError("derived seed drifted from the planned seed")
    if result["header"]["episode_id"] != record["input"]["episode_id"]:
        raise RuntimeError("episode id drifted from the planned id")
    if result["header"].get("triad_config_id") != orbit["triad_config_id"]:
        raise RuntimeError("raw triad configuration is absent from the header")
    report = replay_events(
        result["header"],
        result["events"],
        system,
        initial_state=int(result["header"]["initial_state"]),
    )
    if report["verification"] != "exact":
        raise RuntimeError(f"smoke replay mismatch {report}")
    episode_id = result["header"]["episode_id"]
    stream_path = layout.root / "streams" / f"{episode_id}.jsonl.gz"
    stream_hash = write_stream(stream_path, result["payload"])
    row = episode_row(result)
    for key in _STORED_OMIT:
        row.pop(key, None)
    for key in (
        "graph_only_orbit_id",
        "graph_only_orbit_size",
        "raw_triad_config",
        "rule_aware_orbit_id",
        "rule_aware_orbit_size",
        "triad_config_id",
    ):
        row[key] = result["header"][key]
    payload = {
        "constraint_system_hash": result["header"]["constraint_system_hash"],
        "episode_id": episode_id,
        "event_count": result["header"]["event_count"],
        "event_payload_sha256": result["header"]["event_payload_sha256"],
        "event_stream": f"streams/{episode_id}.jsonl.gz",
        "event_stream_sha256": stream_hash,
        "final_state_hash": result["header"]["final_state_hash"],
        "frozen_plan_commit": str(commit),
        "header": result["header"],
        "initial_state_hash": result["header"]["initial_state_hash"],
        "pair_event_count": result["summary"]["pair_event_count"],
        "plan_hash": plan["plan_hash"],
        "runner_version": result["header"]["runner_version"],
        "seed": result["header"]["seed"],
        "smoke_replay": "exact",
        "spec_hash": plan["plan_hash"],
        "summary": row,
        "termination_reason": result["header"]["termination_reason"],
        "trajectory_hash": result["header"]["trajectory_hash"],
    }
    note_dir = layout.progress() / "episode-notes"
    note_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        note_dir / f"{record['item_id']}.json",
        {"episode_id": episode_id, "event_count": payload["event_count"], "item_id": record["item_id"]},
    )
    return payload


def _execute_replay(layout: Layout, record: dict, plan: dict) -> dict:
    episode_item_id = record["input"]["episode_item_id"]
    stored = read_valid_item(layout, episode_item_id, plan["plan_hash"])
    if stored is None:
        raise RuntimeError("replay target is not a valid episode item")
    result = stored["result"]
    events = list(iter_jsonl_gzip(layout.root / result["event_stream"]))
    system = _system_index(plan)[result["summary"]["system_id"]]
    report = replay_events(
        result["header"],
        events,
        system,
        initial_state=int(result["header"]["initial_state"]),
    )
    if report["verification"] != "exact":
        raise RuntimeError(f"replay mismatch {report}")
    stream_hash = sha256_file(layout.root / result["event_stream"])
    if stream_hash != result["event_stream_sha256"]:
        raise RuntimeError("replay detected a corrupted event stream")
    return {
        "episode_id": result["episode_id"],
        "frozen_plan_commit": result["frozen_plan_commit"],
        "verification": "exact",
    }


def advance(root: Path) -> int:
    layout = Layout(root)
    plan = _load_round_plan(layout)
    dependency = read_json(layout.dependency_path()) if layout.dependency_path().exists() else {}
    if dependency.get("replay_planned"):
        return 0
    state = load_state(layout)
    items = [row for row in load_work_items(layout) if row["kind"] == "episode"]
    if any(state.get(row["item_id"], {}).get("status") not in {"complete", "quarantined"} for row in items):
        return 0
    complete = [row for row in items if state.get(row["item_id"], {}).get("status") == "complete"]
    fraction = float(plan.get("replay_fraction", REPLAY_FRACTION))
    chosen = select_replay_ids([row["input"]["episode_id"] for row in complete], fraction)
    by_episode = {row["input"]["episode_id"]: row for row in complete}
    added = 0
    manifest = read_json(layout.manifest_path())
    for episode_id in chosen:
        source = by_episode[episode_id]
        item_input = {
            "episode_id": episode_id,
            "episode_item_id": source["item_id"],
            "frozen_plan_commit": manifest["frozen_plan_commit"],
            "plan_hash": plan["plan_hash"],
            "round_id": plan["round_id"],
        }
        record = make_item_record(plan["plan_hash"], SEMANTIC_VERSION, ANALYSIS_VERSION, "replay", item_input)
        if ensure_planned(layout, record):
            added += 1
    dependency["replay_planned"] = True
    atomic_write_json(layout.dependency_path(), dependency)
    log_progress(layout, f"REPLAY planned={added} fraction={fraction}")
    return added


def phase(root: Path) -> str:
    layout = Layout(root)
    state = load_state(layout) if layout.item_state_path().exists() else {}
    items = load_work_items(layout) if layout.work_items_path().exists() else []
    episodes = [row for row in items if row["kind"] == "episode"]
    replays = [row for row in items if row["kind"] == "replay"]
    if not episodes or any(state.get(row["item_id"], {}).get("status") == "pending" for row in episodes):
        return "04_TRAJECTORIES"
    dependency = read_json(layout.dependency_path()) if layout.dependency_path().exists() else {}
    if not dependency.get("replay_planned") or any(state.get(row["item_id"], {}).get("status") == "pending" for row in replays):
        return "05_REPLAY_VERIFY"
    return "06_ATLAS_MERGE"


def counts(root: Path) -> dict:
    layout = Layout(root)
    plan = _load_round_plan(layout) if (layout.plan() / "round-plan.json").exists() else {}
    state = load_state(layout) if layout.item_state_path().exists() else {}
    items = load_work_items(layout) if layout.work_items_path().exists() else []
    episodes = [row for row in items if row["kind"] == "episode"]
    by_system: dict[str, list[str]] = {}
    done = 0
    for row in episodes:
        system_id = row["input"]["system_id"]
        by_system.setdefault(system_id, [])
        if state.get(row["item_id"], {}).get("status") == "complete":
            done += 1
            by_system[system_id].append(row["item_id"])
    systems_planned = len(plan.get("systems") or []) or len(by_system)
    expected = {}
    for row in episodes:
        expected[row["input"]["system_id"]] = expected.get(row["input"]["system_id"], 0) + 1
    systems_complete = sum(
        1 for system_id, total in expected.items() if len(by_system.get(system_id, [])) == total and total
    )
    events = 0
    last = None
    notes = layout.progress() / "episode-notes"
    if notes.exists():
        newest = None
        for path in notes.glob("*.json"):
            payload = read_json(path)
            events += int(payload.get("event_count") or 0)
            stamp = path.stat().st_mtime
            if newest is None or stamp >= newest:
                newest = stamp
                last = payload.get("episode_id")
    disk = 0
    if layout.root.exists():
        for path in layout.root.rglob("*"):
            if path.is_file():
                disk += path.stat().st_size
    return {
        "cache_hits": 0,
        "cache_misses": 0,
        "calibrations_complete": 0,
        "calibrations_total": 0,
        "calibrations_unresolved": 0,
        "disk_used_bytes": disk,
        "episodes_complete": done,
        "episodes_planned": len(episodes),
        "events_written": events,
        "generation": "008a",
        "last_completed_episode": last,
        "round_id": plan.get("round_id"),
        "systems_complete": systems_complete,
        "systems_planned": systems_planned,
    }


def _transition(event: dict, summary: dict, gap: int) -> dict:
    return {
        "context_after": event["context_after"],
        "context_before": event["context_before"],
        "episode_id": summary["episode_id"],
        "full_index": event["full_index"],
        "graph_only_orbit_id": summary.get("graph_only_orbit_id"),
        "hidden_context_orbit_id": summary["hidden_context_orbit_id"],
        "kind": event["kind"],
        "pair_after": event["pair_after"],
        "pair_before": event["pair_before"],
        "pair_epochs_since_previous_change": gap,
        "pair_index": event["pair_index"],
        "post": event["post"],
        "pre": event["pre"],
        "rule_aware_orbit_id": summary.get("rule_aware_orbit_id"),
        "rules": event["rules"],
        "slot": event["slot"],
        "source_graph_class": summary["source_graph_class"],
        "system_id": summary["system_id"],
        "triad_after": event["triad_after"],
        "triad_before": event["triad_before"],
        "triad_config_id": summary["triad_config_id"],
    }


def merge_items(root: Path) -> dict:
    layout = Layout(root)
    plan = _load_round_plan(layout)
    manifest = read_json(layout.manifest_path())
    state = load_state(layout)
    rows = []
    listed = []
    replay_exact = 0
    replay_mismatch = 0
    index = layout.root / "index"
    index.mkdir(parents=True, exist_ok=True)
    run_lines: list[str] = []
    marker_count = 0
    conditional: dict[tuple[str, str], dict[str, Counter]] = {}

    def marker_lines():
        nonlocal marker_count, replay_exact, replay_mismatch
        seen = 0
        for record in load_work_items(layout):
            if state.get(record["item_id"], {}).get("status") != "complete":
                continue
            stored = read_valid_item(layout, record["item_id"], manifest["spec_hash"])
            if stored is None:
                continue
            listed.append({"item_id": record["item_id"], "result_hash": stored["result_hash"]})
            atomic_write_json(layout.merge() / "items" / f"{record['item_id']}.json", stored)
            seen += 1
            if seen % 400 == 0:
                log_progress(layout, f"MERGE scanned={seen}")
            if record["kind"] == "episode":
                summary = stored["result"]["summary"]
                if any(key in summary for key in ("markers", "edge_count_sequence", "triad_count_sequence")):
                    raise RuntimeError("stored episode summary still duplicates transition markers")
                last_pair = None
                bucket = conditional.setdefault(
                    (summary["system_id"], summary["source_graph_class"]),
                    {"class": Counter(), "slot_class": Counter(), "slot_mask": Counter()},
                )
                for event in iter_jsonl_gzip(layout.root / stored["result"]["event_stream"]):
                    if event["slot"] >= 6:
                        continue
                    gap = event["pair_index"] if last_pair is None else event["pair_index"] - last_pair
                    last_pair = event["pair_index"]
                    marker_count += 1
                    yield json.dumps(_transition(event, summary, gap), sort_keys=True)
                    triad = event["triad_before"]
                    bucket["class"][(triad, event["pair_after"], event["pair_before"])] += 1
                    bucket["slot_class"][(triad, event["slot"], event["pair_before"])] += 1
                    bucket["slot_mask"][(triad, event["slot"], event["pre"] & 63)] += 1
                run_lines.append(
                    json.dumps(
                        {
                            "class_runs": summary["class_runs"],
                            "episode_id": summary["episode_id"],
                            "hidden_context_orbit_id": summary["hidden_context_orbit_id"],
                            "initial_source_residence": summary["initial_source_residence"],
                            "source_graph_class": summary["source_graph_class"],
                            "source_returns": summary["source_returns"],
                            "system_id": summary["system_id"],
                            "triad_config_id": summary["triad_config_id"],
                        },
                        sort_keys=True,
                    )
                )
                rows.append(dict(summary))
            elif record["kind"] == "replay":
                if stored["result"].get("verification") == "exact":
                    replay_exact += 1
                else:
                    replay_mismatch += 1
            del stored

    written = write_jsonl_gzip(index / "transitions.jsonl.gz", marker_lines())
    if written != marker_count:
        raise RuntimeError("transition index line count drifted")
    write_jsonl_gzip(index / "class-runs.jsonl.gz", run_lines)
    if replay_mismatch:
        raise RuntimeError("replay mismatches are present; scientific merge is refused")
    sources = enumerate_hidden_contexts()
    three = set(three_edge_indexes(sources).values())
    for row in rows:
        row["route_recomputed"] = route_from_runs(
            row["class_runs"],
            sources[row["source_graph_class"]]["class_index"],
            three,
            row["pair_event_count"],
        )
    atlas = atlas_from_summaries(rows, sources) if rows else {"episodes": 0}
    repair = repair_from_rows(rows, plan, conditional) if rows else {}
    occupancy = system_occupancy(rows) if rows else {}
    residual = additive_residual(occupancy) if occupancy else None
    payload = {
        "episodes": len(rows),
        "experiment_id": plan["experiment_id"],
        "occupancy_by_system": occupancy,
        "repair": repair,
        "residual_r05": residual,
        "trajectory_atlas": atlas,
    }
    atomic_write_json(layout.merge() / "atlas.json", payload)
    summary = {
        "episodes": len(rows),
        "experiment_id": plan["experiment_id"],
        "frozen_plan_commit": manifest.get("frozen_plan_commit"),
        "items": listed,
        "plan_hash": plan["plan_hash"],
        "replay_exact": replay_exact,
        "replay_mismatch": replay_mismatch,
        "round_id": plan["round_id"],
        "rows": [],
        "transition_markers": marker_count,
    }
    atomic_write_json(layout.merge() / "summary.json", summary)
    log_progress(layout, f"MERGE episodes={len(rows)} replay_exact={replay_exact} markers={marker_count}")
    return summary


def verify_generation(root: Path, *, require_complete: bool = False) -> dict:
    from rs_constraint_lab.explore08a import verify_plan_result_chronology
    from rs_constraint_lab.supervisor import verify_root

    report = verify_root(root, require_complete=require_complete)
    layout = Layout(root)
    if not layout.manifest_path().exists():
        return report
    manifest = read_json(layout.manifest_path())
    extra = []
    if not manifest.get("frozen_plan_commit"):
        extra.append("frozen plan commit is absent")
    result_commit = manifest.get("result_commit")
    if result_commit and manifest.get("repo") and manifest.get("plan_relpath"):
        try:
            verify_plan_result_chronology(
                Path(manifest["repo"]),
                manifest["frozen_plan_commit"],
                result_commit,
                manifest["plan_relpath"],
                manifest.get("plan_hash"),
            )
        except Exception as exc:
            extra.append(str(exc))
    for record in load_work_items(layout) if layout.work_items_path().exists() else []:
        if record["kind"] != "episode":
            continue
        stored = read_valid_item(layout, record["item_id"], manifest["spec_hash"])
        if stored is None:
            continue
        result = stored["result"]
        if result.get("frozen_plan_commit") != manifest.get("frozen_plan_commit"):
            extra.append(f"{record['item_id']} lost the frozen plan commit")
        if result.get("summary", {}).get("triad_config_id") != record["input"].get("triad_config_id"):
            extra.append(f"{record['item_id']} lost the raw triad configuration")
        path = layout.root / result["event_stream"]
        if not path.exists():
            extra.append(f"missing event stream {result['event_stream']}")
            continue
        digest = sha256_file(path)
        if digest != result.get("event_stream_sha256"):
            extra.append(f"corrupted event stream {result['episode_id']}")
    report["problems"] = list(report.get("problems") or []) + extra
    report["ok"] = bool(report["ok"]) and not extra
    return report
