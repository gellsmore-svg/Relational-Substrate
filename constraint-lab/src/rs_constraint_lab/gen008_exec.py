"""Micro-batch adapter for the Generation 8 trajectory atlas.

Scientific trajectories start only after ``require_frozen_plan`` accepts a
40-hex commit. Preflight benchmarking records cost and does not record routes.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, read_json, sha256_file
from rs_constraint_lab.explore08 import (
    BASELINE_ROLE,
    CHECKPOINTS,
    CLASS_NAMES,
    EXPERIMENT_ID,
    FULL_EVENT_CAP,
    REPLICATES,
    RUNNER_VERSION,
    SEED_FIELDS,
    SEED_FUNCTION,
    FrozenPlanError,
    atlas_from_summaries,
    build_round0_systems,
    derive_composite_anchor,
    derive_pp_archetypes,
    derive_seed,
    derive_tp_archetypes,
    dynamic_cache,
    enumerate_hidden_contexts,
    episode_id_for,
    episode_row,
    inspect_lines,
    iter_jsonl_gzip,
    plan_hash,
    query_transitions,
    read_stream,
    remote_contains,
    replay_events,
    require_frozen_plan,
    run_episode,
    select_replay_ids,
    write_jsonl_gzip,
    write_stream,
)

# These summary fields stay on the item files. The atlas does not read them,
# and holding one copy per episode exceeds a comfortable merge footprint.
_ATLAS_OMIT = frozenset({"edge_count_sequence", "markers", "triad_count_sequence"})
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
SEMANTIC_VERSION = "generation-008-mode-b/v1"
MAX_ESTIMATED_WALL_SECONDS = 3 * 3600
MAX_COMPRESSED_BYTES = 2 * 1024 ** 3
MAX_REPLAY_SECONDS = 5.0
BATCH_ITEM_CAP = 120

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
        (row["source_graph_class"], row["hidden_context_orbit_id"]): row
        for row in plan["contexts"]
    }


def _system_index(plan: dict) -> dict[str, dict]:
    return {row["system_id"]: row for row in plan["systems"]}


def choose_batch_items(episode_seconds: float) -> tuple[int, str]:
    if episode_seconds <= 0:
        return 1, "episode timing was not positive"
    items = 1
    while items < BATCH_ITEM_CAP and (items + 1) * episode_seconds <= 60:
        items += 1
        if items * episode_seconds >= 45:
            break
    note = "batch item count targets about 45s and stays inside 60s"
    if items * episode_seconds < 30:
        note = (
            "episodes are shorter than the 30s batch floor; "
            f"item count is capped at {items} so one watchdog still isolates a small set"
        )
    return items, note


def choose_horizon(sample: dict, episodes: int, workers: int = 2) -> dict:
    """Operational horizon rule. It reads durations and byte counts only."""
    forbidden = [key for key in sample if "route" in key or "destination" in key or "class_run" in key]
    if forbidden:
        raise RuntimeError(f"horizon selection was given scientific fields: {forbidden}")
    chosen = None
    estimates = []
    for horizon in (512, 256, 128):
        scale = horizon / float(sample["pair_horizon"])
        seconds = float(sample["seconds"]) * scale
        gzip_bytes = int(float(sample["gzip_bytes"]) * scale)
        wall = seconds * episodes / workers
        replay = float(sample["replay_seconds"]) * scale
        row = {
            "compressed_bytes": gzip_bytes,
            "episode_seconds": round(seconds, 6),
            "pair_horizon": horizon,
            "replay_seconds": round(replay, 6),
            "wall_seconds": int(round(wall)),
        }
        estimates.append(row)
        if chosen is None and wall <= MAX_ESTIMATED_WALL_SECONDS and gzip_bytes <= MAX_COMPRESSED_BYTES and replay <= MAX_REPLAY_SECONDS:
            chosen = row
    if chosen is None:
        return {"estimates": estimates, "pair_horizon": None, "refused": True}
    return {"estimates": estimates, "pair_horizon": chosen["pair_horizon"], "refused": False, "selected": chosen}


def build_round0_plan(*, horizon: int, benchmark: dict, batch_items: int, batch_note: str) -> dict:
    sources = enumerate_hidden_contexts()
    systems = build_round0_systems()
    anchor = derive_composite_anchor()
    contexts = []
    orbit_counts = {}
    for key in ("star", "path", "triangle"):
        orbit_counts[key] = sources[key]["orbit_count"]
        contexts.extend(sources[key]["orbits"])
    starts = len(contexts)
    episodes = len(systems) * starts * REPLICATES
    scale = horizon / float(benchmark["pair_horizon"])
    event_count = int(round(float(benchmark["event_count"]) * scale))
    document = {
        "alphabet": "W4",
        "anchor": anchor,
        "batch_item_count": batch_items,
        "batch_note": batch_note,
        "checkpoints": list(CHECKPOINTS),
        "contexts": contexts,
        "experiment_id": EXPERIMENT_ID,
        "full_event_cap": FULL_EVENT_CAP,
        "grade": "strong_suppress",
        "mode": "B",
        "observables": [
            "pair_class_sequence",
            "edge_count_sequence",
            "triad_count_sequence",
            "visitation",
            "transition_counts",
            "residence",
            "first_entry",
            "source_returns",
            "entropy",
            "triad_only_fraction",
            "routing",
            "motifs_length_2_3_4",
            "context_divergence",
            "context_information",
            "context_persistence",
        ],
        "ontology": {"G": 0, "H": 0, "L": 0, "N": 4, "O": 3, "S": 0, "grammar": "independent-hypergraph"},
        "operators": [
            "weight_shift",
            "condition_polarity_flip",
            "structural_tp_neighbour",
            "add_pp_companion",
            "remove_rule",
        ],
        "pair_horizon": horizon,
        "pp_archetype_count": len(derive_pp_archetypes()),
        "prohibit_in_round": False,
        "replay_fraction": 0.1,
        "replicates": REPLICATES,
        "round_id": "round-000",
        "round_limits": {"max_rounds": 4, "max_rules": 2, "max_systems_per_adaptive_round": 4},
        "schema": "rs-constraint-lab.exploration-plan/v1",
        "seed_fields": list(SEED_FIELDS),
        "seed_function": SEED_FUNCTION,
        "source_graph_class_count": 3,
        "source_summaries": {
            key: {
                "automorphism_group_size": sources[key]["automorphism_group_size"],
                "canonical_pair_mask": sources[key]["canonical_pair_mask"],
                "class_name": sources[key]["class_name"],
                "orbit_count": sources[key]["orbit_count"],
            }
            for key in ("star", "path", "triangle")
        },
        "systems": systems,
        "tp_structural_count": len(derive_tp_archetypes()),
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
            "hidden_context_orbits": orbit_counts,
            "raw_bytes_per_benchmark_episode": int(benchmark["raw_bytes"]),
            "replicates_per_start": REPLICATES,
            "source_graph_classes": 3,
            "starter_systems": len(systems),
            "total_hidden_context_starts": starts,
            "total_round_episodes": episodes,
            "worst_case_full_events": episodes * FULL_EVENT_CAP,
        },
    }
    if document["tp_structural_count"] != 8:
        document["tp_count_note"] = (
            f"Generation 4 table contains {document['tp_structural_count']} T->P structural forms; "
            "Round 0 uses that count rather than an assumed 8"
        )
    document["plan_hash"] = plan_hash(document)
    return document


def benchmark_cost(*, horizon: int = 512) -> dict:
    """Time one baseline episode and one constrained episode. Routes are discarded."""
    sources = enumerate_hidden_contexts()
    systems = build_round0_systems()
    context = sources["star"]["orbits"][0]
    context = {**context, "class_index": sources["star"]["class_index"]}
    cache = dynamic_cache()
    samples = []
    for system in (systems[0], systems[1]):
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
        payload = result["payload"]
        import gzip

        compressed = gzip.compress(payload, mtime=0)
        samples.append(
            {
                "event_count": len(result["events"]),
                "gzip_bytes": len(compressed),
                "pair_event_count": result["summary"]["pair_event_count"],
                "pair_horizon": horizon,
                "raw_bytes": len(payload),
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
            {key: row[key] for key in ("event_count", "gzip_bytes", "pair_event_count", "raw_bytes", "replay_seconds", "seconds", "system_id")}
            for row in samples
        ],
    }


def install_plan(root: Path, plan_path: Path, commit: str, repo: Path, relpath: str, *, require_remote: bool = True) -> dict:
    plan = require_frozen_plan(repo, commit, relpath, disk_path=plan_path)
    if require_remote and not remote_contains(repo, commit):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    layout = Layout(root)
    layout.ensure()
    atomic_write_json(layout.plan() / "round-plan.json", plan)
    _PLAN_CACHE[str(layout.root.resolve())] = plan
    manifest = {
        "advance": "rs_constraint_lab.gen008_exec:advance",
        "analysis_version": ANALYSIS_VERSION,
        "counts": "rs_constraint_lab.gen008_exec:counts",
        "executor": "rs_constraint_lab.gen008_exec:execute_item",
        "experiment_id": plan["experiment_id"],
        "frozen_plan_commit": commit,
        "heartbeat_seconds": 10,
        "merge": "rs_constraint_lab.gen008_exec:merge_items",
        "phase": "rs_constraint_lab.gen008_exec:phase",
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
    items, note = plan.get("batch_item_count", 1), plan.get("batch_note", "")
    atomic_write_json(
        layout.policy_path(),
        {"kinds": {"default": {"items": items}, "episode": {"items": items}, "replay": {"items": items}}, "note": note},
    )
    atomic_write_json(layout.dependency_path(), {"replay_planned": False})
    context_by_id = _context_index(plan)
    planned = 0
    for system in plan["systems"]:
        for context in plan["contexts"]:
            for replicate in range(int(plan["replicates"])):
                identity = {
                    "experiment_id": plan["experiment_id"],
                    "hidden_context_orbit_id": context["hidden_context_orbit_id"],
                    "replicate_index": replicate,
                    "round_id": plan["round_id"],
                    "source_graph_class": context["source_graph_class"],
                    "system_id": system["system_id"],
                }
                item_input = {
                    **identity,
                    "episode_id": episode_id_for(identity),
                    "frozen_plan_commit": commit,
                    "full_event_cap": plan["full_event_cap"],
                    "pair_horizon": plan["pair_horizon"],
                    "plan_hash": plan["plan_hash"],
                    "seed": derive_seed(identity),
                }
                if context["hidden_context_orbit_id"] not in {
                    row["hidden_context_orbit_id"] for row in context_by_id.values()
                }:
                    raise RuntimeError("context id drifted while planning")
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


def _refuse_unfrozen(manifest: dict, layout: Layout, context: dict) -> None:
    """Check the frozen commit once per worker process."""
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
        (record["input"]["source_graph_class"], record["input"]["hidden_context_orbit_id"])
    ]
    sources = context.setdefault("sources", enumerate_hidden_contexts())
    source = sources[orbit["source_graph_class"]]
    compiled_context = {
        **orbit,
        "class_index": source["class_index"],
    }
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
        context=compiled_context,
        replicate=int(record["input"]["replicate_index"]),
        pair_horizon=int(plan["pair_horizon"]),
        full_event_cap=int(plan["full_event_cap"]),
        plan_hash_value=plan["plan_hash"],
        frozen_plan_commit=str(commit),
        cache=context.setdefault("dynamic", dynamic_cache()),
        stall_seconds=stall,
    )
    if result["header"]["seed"] != record["input"]["seed"]:
        raise RuntimeError("derived seed drifted from the planned seed")
    if result["header"]["episode_id"] != record["input"]["episode_id"]:
        raise RuntimeError("episode id drifted from the planned id")
    episode_id = result["header"]["episode_id"]
    stream_path = layout.root / "streams" / f"{episode_id}.jsonl.gz"
    stream_hash = write_stream(stream_path, result["payload"])
    row = episode_row(result)
    # The summary route is retained as a derived cache. Atlas recomputes it.
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
    events = read_stream(layout.root / result["event_stream"])
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
    fraction = float(plan.get("replay_fraction", 0.1))
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
    systems_complete = sum(1 for system_id, total in expected.items() if len(by_system.get(system_id, [])) == total and total)
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
        "generation": "008",
        "last_completed_episode": last,
        "round_id": plan.get("round_id"),
        "systems_complete": systems_complete,
        "systems_planned": systems_planned,
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
                for marker in summary.get("markers") or []:
                    marker_count += 1
                    yield json.dumps(marker, sort_keys=True)
                run_lines.append(json.dumps(
                    {
                        "class_runs": summary["class_runs"],
                        "episode_id": summary["episode_id"],
                        "hidden_context_orbit_id": summary["hidden_context_orbit_id"],
                        "initial_source_residence": summary["initial_source_residence"],
                        "source_graph_class": summary["source_graph_class"],
                        "source_returns": summary["source_returns"],
                        "system_id": summary["system_id"],
                    },
                    sort_keys=True,
                ))
                rows.append({key: value for key, value in summary.items() if key not in _ATLAS_OMIT})
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
    atlas = atlas_from_summaries(rows, sources) if rows else {"episodes": 0}
    atomic_write_json(layout.merge() / "atlas.json", atlas)
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
    from rs_constraint_lab.supervisor import verify_root

    report = verify_root(root, require_complete=require_complete)
    layout = Layout(root)
    if not layout.manifest_path().exists():
        return report
    manifest = read_json(layout.manifest_path())
    extra = []
    if not manifest.get("frozen_plan_commit"):
        extra.append("frozen plan commit is absent")
    for record in load_work_items(layout) if layout.work_items_path().exists() else []:
        if record["kind"] != "episode":
            continue
        stored = read_valid_item(layout, record["item_id"], manifest["spec_hash"])
        if stored is None:
            continue
        result = stored["result"]
        if result.get("frozen_plan_commit") != manifest.get("frozen_plan_commit"):
            extra.append(f"{record['item_id']} lost the frozen plan commit")
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


def role_names(plan: dict) -> list[str]:
    return [system["role"] for system in plan["systems"]]


def baseline_is_descriptive(plan: dict) -> bool:
    roles = role_names(plan)
    return BASELINE_ROLE in roles and "null hypothesis" not in " ".join(roles)


def prepare_round0_plan(*, horizon: int | None = None) -> dict:
    """Benchmark cost, apply the operational horizon rule, and build the plan.

    This does not execute Round 0. The returned plan still has to be committed
    and pushed before ``install_plan``.
    """
    sources = enumerate_hidden_contexts()
    systems = build_round0_systems()
    episodes = len(systems) * sum(row["orbit_count"] for row in sources.values()) * REPLICATES
    sample = benchmark_cost(horizon=512)
    decision = choose_horizon(sample, episodes)
    chosen = horizon if horizon is not None else decision["pair_horizon"]
    if chosen is None:
        return {"benchmark": sample, "decision": decision, "episodes": episodes, "plan": None}
    scale = chosen / float(sample["pair_horizon"])
    items, note = choose_batch_items(float(sample["seconds"]) * scale)
    plan = build_round0_plan(horizon=chosen, benchmark=sample, batch_items=items, batch_note=note)
    return {"benchmark": sample, "decision": decision, "episodes": episodes, "plan": plan}


def _episode_result(layout: Layout, episode_id: str) -> dict | None:
    if not layout.manifest_path().exists():
        return None
    manifest = read_json(layout.manifest_path())
    for record in load_work_items(layout) if layout.work_items_path().exists() else []:
        if record.get("kind") != "episode":
            continue
        if record.get("input", {}).get("episode_id") != episode_id:
            continue
        stored = read_valid_item(layout, record["item_id"], manifest["spec_hash"])
        if stored is not None:
            return stored["result"]
    return None


def _load_atlas(root: Path) -> dict:
    path = Layout(root).merge() / "atlas.json"
    if not path.exists():
        raise FileNotFoundError(f"atlas is not merged at {path}")
    return read_json(path)


def atlas_view(root: Path, view: str, selectors: list[str] | None = None, *, limit: int = 20) -> str:
    """Compact atlas text. It does not print raw event streams except one episode."""
    selectors = selectors or []
    atlas = _load_atlas(root)
    if view == "summary":
        lines = [
            f"episodes {atlas.get('episodes')}",
            f"systems {len(atlas.get('transition_matrices') or {})}",
            f"motifs {len(atlas.get('motifs') or [])}",
            f"motifs_omitted {atlas.get('motifs_omitted')}",
            f"motif_clock {atlas.get('motif_clock')}",
        ]
        return "\n".join(lines)
    if view == "routes":
        lines = []
        for row in (atlas.get("routing") or [])[:limit]:
            lines.append(
                f"{row['system_id']} {row['source_graph_class']} {row['orbit_id']} "
                f"n={row['episodes']} size={row['orbit_size']} {row['destinations']}"
            )
        hidden = max(0, len(atlas.get("routing") or []) - limit)
        if hidden:
            lines.append(f"... {hidden} further route rows")
        return "\n".join(lines)
    if view == "contexts":
        lines = []
        for row in atlas.get("context_information") or []:
            lines.append(
                f"{row['system_id']} {row['source_graph_class']} "
                f"episode_equal={row['episode_equal']} weighted={row['configuration_weighted']}"
            )
        for row in (atlas.get("context_divergences") or [])[:limit]:
            lines.append(
                f"js {row['system_id']} {row['source_graph_class']} "
                f"mean={row['mean_js']} max={row['max_js']}"
            )
        return "\n".join(lines)
    if view == "motifs":
        lines = []
        for row in (atlas.get("motifs") or [])[:limit]:
            lines.append(
                f"n={row['count']} {' -> '.join(row['classes'])} systems={','.join(row['systems'])} "
                f"episodes={','.join(row['episode_ids'])}"
            )
        return "\n".join(lines)
    if view == "episode":
        if len(selectors) != 1:
            raise ValueError("atlas episode requires one episode id")
        return _episode_text(root, selectors[0], limit=limit)
    if view == "replay":
        if len(selectors) != 1:
            raise ValueError("atlas replay requires one episode id")
        return _replay_text(root, selectors[0])
    if view == "compare":
        if len(selectors) != 2:
            raise ValueError("atlas compare requires two system ids")
        return _compare_text(atlas, selectors[0], selectors[1])
    raise ValueError(f"unknown atlas view {view}")


def _episode_text(root: Path, episode_id: str, *, limit: int) -> str:
    layout = Layout(root)
    result = _episode_result(layout, episode_id)
    if result is None:
        raise FileNotFoundError(episode_id)
    header = result["header"]
    summary = result["summary"]
    events = read_stream(layout.root / result["event_stream"])
    lines = [
        f"episode {episode_id}",
        f"system {header['system_id']} source {header['source_graph_class']} orbit {header['hidden_context_orbit_id']}",
        f"seed {header['seed']} termination {header['termination_reason']}",
        f"events {header['event_count']} pair_events {header['pair_event_count']}",
        f"final_class {summary['final_pair_class']} returns {summary['source_returns']}",
        f"trajectory {header['trajectory_hash']}",
    ]
    lines.extend(inspect_lines(events, limit=limit))
    return "\n".join(lines)


def _replay_text(root: Path, episode_id: str) -> str:
    layout = Layout(root)
    result = _episode_result(layout, episode_id)
    if result is None:
        raise FileNotFoundError(episode_id)
    plan = _load_round_plan(layout)
    system = _system_index(plan)[result["summary"]["system_id"]]
    events = read_stream(layout.root / result["event_stream"])
    report = replay_events(result["header"], events, system, initial_state=int(result["header"]["initial_state"]))
    return (
        f"episode {episode_id}\n"
        f"verification {report['verification']}\n"
        f"field {report.get('field', '-')}\n"
        f"events {report.get('events', 0)}"
    )


def _compare_text(atlas: dict, left: str, right: str) -> str:
    matrices = atlas.get("transition_matrices") or {}
    if left not in matrices or right not in matrices:
        raise KeyError(f"systems in the atlas are {sorted(matrices)}")
    distance = 0.0
    cells = 0
    for value_left, value_right in zip(matrices[left]["row_normalised"], matrices[right]["row_normalised"]):
        if value_left is None or value_right is None:
            continue
        distance += abs(value_left - value_right)
        cells += 1
    lines = [
        f"compare {left} {right}",
        f"pair_event_support {matrices[left]['pair_event_support']} {matrices[right]['pair_event_support']}",
        f"row_normalised_l1 {distance} cells {cells}",
    ]
    for row in atlas.get("context_information") or []:
        if row["system_id"] in {left, right}:
            lines.append(
                f"I {row['system_id']} {row['source_graph_class']} "
                f"episode_equal={row['episode_equal']} weighted={row['configuration_weighted']}"
            )
    return "\n".join(lines)


def transitions_view(
    root: Path,
    *,
    source_class: str | None = None,
    target_class: str | None = None,
    orbit_id: str | None = None,
    system_id: str | None = None,
    triad_count: int | None = None,
    motif: list[str] | None = None,
    limit: int = 50,
) -> str:
    layout = Layout(root)
    path = layout.root / "index" / "transitions.jsonl.gz"
    if not path.exists():
        raise FileNotFoundError(path)
    episodes = None
    runs_path = layout.root / "index" / "class-runs.jsonl.gz"
    if motif and runs_path.exists():
        episodes = list(iter_jsonl_gzip(runs_path))
    elif motif:
        episodes = []
        manifest = read_json(layout.manifest_path())
        for record in load_work_items(layout):
            if record.get("kind") != "episode":
                continue
            stored = read_valid_item(layout, record["item_id"], manifest["spec_hash"])
            if stored is not None:
                episodes.append(stored["result"]["summary"])
    chosen = query_transitions(
        iter_jsonl_gzip(path),
        source_class=source_class,
        target_class=target_class,
        orbit_id=orbit_id,
        system_id=system_id,
        triad_count=triad_count,
        motif=motif,
        episodes=episodes,
        limit=limit,
    )
    lines = [f"matches {len(chosen)}"]
    for row in chosen:
        lines.append(
            f"{row.get('episode_id')} {row.get('system_id')} "
            f"{CLASS_NAMES[row['pair_before']]} -> {CLASS_NAMES[row['pair_after']]} "
            f"triads={row['triad_before']}->{row['triad_after']} t={row.get('pair_index')}"
        )
    return "\n".join(lines)
