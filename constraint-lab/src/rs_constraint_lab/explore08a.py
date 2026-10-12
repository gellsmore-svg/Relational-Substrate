"""Generation 8A context-alignment repair.

Execution enumerates every raw triad configuration. Symmetry is an analysis
of those completed trajectories. It does not choose which starts run.

The seed document is the six Generation 8A fields. A graph-only orbit id is
not one of them. Generation 8 trajectories stay historical.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

from rs_constraint_lab.constraints import DISSOLVE, FORM, parse_expression, relabel_constraint
from rs_constraint_lab.durable import canonical_json
from rs_constraint_lab.explore08 import (
    CHECKPOINTS,
    CLASS_NAMES,
    FULL_EVENT_CAP,
    LAB_ROOT,
    PAIR_SLOTS,
    REPLICATES,
    SEED_FUNCTION,
    _episode_id_from_identity,
    _js,
    _mutual_information,
    _seed_from_identity,
    enumerate_hidden_contexts,
    pair_automorphisms,
    plan_hash,
    source_masks,
)
from rs_constraint_lab.state import permutations, relation_slots, relabel_relation_state, slot_permutation_maps

EXPERIMENT_ID = "generation-008a-context-repair"
RUNNER_VERSION = "generation-008a-trajectory/v1"
SEMANTIC_VERSION = "generation-008a-mode-b/v1"
SEED_FIELDS = (
    "experiment_id",
    "round_id",
    "system_id",
    "source_graph_class",
    "raw_triad_config",
    "replicate_index",
)
ROUND_ID = "round-a0"
REPLAY_FRACTION = 0.1
# Smoke replay is an exact replay before the episode item is stored.
# The durable sample re-reads the stored stream.
SMOKE_REPLAY = "exact"
CURRENT_CONTEXT_SYSTEMS = ("R00", "R01", "R03", "R05", "R06", "R07")
PALETTE = (
    ("R00", "round-000", "S00"),
    ("R01", "round-000", "S01"),
    ("R02", "round-000", "S05"),
    ("R03", "round-001", "S10"),
    ("R04", "round-001", "S11"),
    ("R05", "round-000", "S09"),
    ("R06", "round-001", "S12"),
    ("R07", "round-002", "S16"),
)
_COPIED_FIELDS = ("expressions", "pair_id", "role", "source", "structural_expression", "tie_pair_ids")
_EDGE_NAME = re.compile(r"^e(\d+)")

# Historical Generation 8 chronology. The plan blob at the frozen commit is
# hashed again; the working tree is not the source of the hash.
GENERATION8_CHRONOLOGY = (
    {
        "frozen_plan_commit": "0a9e74f287b3ecb24efd3981b9562e53086ffee9",
        "plan_hash": "fec52960f5e16706e12e9baf0a45169f49c2414b6e7e3ecc80b1b9d0f97c3b86",
        "plan_relpath": "constraint-lab/exploration/generation-008/round-000-plan.json",
        "result_commit": "2b1778306f08e556df195d735e482c8b3533d796",
        "round_id": "round-000",
    },
    {
        "frozen_plan_commit": "509e80fbb5b472d8da61ba7ba85fcedba15939c1",
        "plan_hash": "6f19f8d9ad374792eae970b7691f3eca63699a9d743c13016550e266a9de8354",
        "plan_relpath": "constraint-lab/exploration/generation-008/round-001-plan.json",
        "result_commit": "7b7dc28b4631f1d2a675b7a43135da2d6d06ead4",
        "round_id": "round-001",
    },
    {
        "frozen_plan_commit": "93253e2d249a6f44ace3e7c63ce42306404fa401",
        "plan_hash": "d5141d33f817357cf028ac97de8d7dad486113685f86a0c71734003cfef437a0",
        "plan_relpath": "constraint-lab/exploration/generation-008/round-002-plan.json",
        "result_commit": "8bf0b9f13bba194089141c54c10eb9e73084ae1f",
        "round_id": "round-002",
    },
)


class ChronologyError(RuntimeError):
    """A result commit does not descend from its frozen plan."""


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def seed_identity(fields: dict) -> dict:
    missing = [key for key in SEED_FIELDS if key not in fields]
    if missing:
        raise KeyError(f"seed identity is missing {missing}")
    return {key: fields[key] for key in SEED_FIELDS}


def derive_seed(fields: dict) -> int:
    return _seed_from_identity(seed_identity(fields))


def episode_id_for(fields: dict) -> str:
    return _episode_id_from_identity(seed_identity(fields))


def triad_config_id(triad: int) -> str:
    if triad < 0 or triad > 15:
        raise ValueError(f"triad configuration {triad} is outside 0..15")
    return f"t{triad:02d}"


def _slots():
    return tuple(relation_slots(4, 3))


def _canonical_constraint_key(constraint) -> tuple:
    conditions = tuple(sorted(constraint.conditions))
    counts = tuple(sorted(constraint.counts))
    return (constraint.polarity, constraint.action, conditions, counts, constraint.weight)


def constraint_multiset(expressions: list[str]):
    rules = [parse_expression(expression, 4, order=3) for expression in expressions]
    return Counter(_canonical_constraint_key(rule) for rule in rules)


def permutation_preserves_constraints(expressions: list[str], perm: tuple[int, ...]) -> bool:
    """True when the perm maps the constraint multiset onto itself.

    Rules may be reordered. A change of action, direction, condition,
    polarity, weight, or multiplicity is not preservation. The slot map is
    the full order-3 map, so a triad condition moves with the vertices.
    """
    slots = _slots()
    maps = {item: image for item, image in zip(permutations(4), slot_permutation_maps(4, slots))}
    edge_map = maps[perm]
    rules = [parse_expression(expression, 4, order=3) for expression in expressions]
    original = Counter(_canonical_constraint_key(rule) for rule in rules)
    image = Counter(
        _canonical_constraint_key(relabel_constraint(rule, edge_map)) for rule in rules
    )
    return image == original


def preserving_permutations(pair_mask: int, expressions: list[str]) -> list[tuple[int, ...]]:
    """Aut(source graph, constraint system), listed in S4 order.

    A permutation must preserve the labelled source pair mask and the full
    labelled constraint multiset. Baseline expressions are empty, so the
    group is the source-graph automorphism group.
    """
    slots = _slots()
    kept = []
    for perm in pair_automorphisms(pair_mask):
        if permutation_preserves_constraints(expressions, perm):
            image = relabel_relation_state(pair_mask, perm, slots[:PAIR_SLOTS])
            if image != pair_mask:
                raise RuntimeError("a retained permutation moved the source pair mask")
            kept.append(perm)
    return kept


def _orbits_under(pair_mask: int, perms: list[tuple[int, ...]]) -> list[dict]:
    slots = _slots()
    parent = list(range(16))

    def find(item: int) -> int:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: int, right: int) -> None:
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    for triad in range(16):
        state = pair_mask | (triad << PAIR_SLOTS)
        for perm in perms:
            image = relabel_relation_state(state, perm, slots)
            if (image & 63) != pair_mask:
                raise RuntimeError("a rule-aware automorphism moved the source pair mask")
            union(triad, image >> PAIR_SLOTS)
    groups: dict[int, list[int]] = {}
    for triad in range(16):
        groups.setdefault(find(triad), []).append(triad)
    members = [tuple(sorted(group)) for group in groups.values()]
    members.sort()
    if sum(len(group) for group in members) != 16:
        raise RuntimeError("rule-aware orbits do not cover 16 triad configurations")
    return [
        {
            "canonical_triad": group[0],
            "members": list(group),
            "orbit_size": len(group),
            "raw_triad_configs": [triad_config_id(triad) for triad in group],
        }
        for group in members
    ]


def rule_aware_partition(pair_mask: int, expressions: list[str]) -> dict:
    perms = preserving_permutations(pair_mask, expressions)
    orbits = _orbits_under(pair_mask, perms)
    return {
        "automorphism_group_size": len(perms),
        "automorphisms": [list(perm) for perm in perms],
        "orbit_count": len(orbits),
        "orbits": orbits,
    }


def load_repair_palette(plan_dir: Path | None = None) -> list[dict]:
    """Copy the eight A0 systems from the committed Generation 8 plans.

    Expressions are read from those files. They are not rebuilt from a
    remembered formula.
    """
    directory = plan_dir if plan_dir is not None else LAB_ROOT / "exploration" / "generation-008"
    loaded: dict[tuple[str, str], dict] = {}
    for _system_id, round_id, _parent in PALETTE:
        key = round_id
        if key in {item[0] for item in loaded}:
            continue
        path = directory / f"{round_id}-plan.json"
        if not path.is_file():
            raise FileNotFoundError(f"Generation 8 plan is not on disk: {path}")
        document = json.loads(path.read_text(encoding="utf-8"))
        for row in document["systems"]:
            loaded[(round_id, row["system_id"])] = row
    systems = []
    for system_id, round_id, parent_id in PALETTE:
        source = loaded.get((round_id, parent_id))
        if source is None or "expressions" not in source:
            raise RuntimeError(f"{round_id} {parent_id} has no stored expressions")
        expressions = list(source["expressions"])
        if any("prohibit" in expression for expression in expressions):
            raise RuntimeError(f"{parent_id} still contains prohibit; A0 does not")
        row = {
            "expressions": expressions,
            "parent_round_id": round_id,
            "parent_system_id": parent_id,
            "system_id": system_id,
        }
        for field in _COPIED_FIELDS:
            if field in source and field not in row:
                row[field] = source[field]
        systems.append(row)
    if [row["system_id"] for row in systems] != [item[0] for item in PALETTE]:
        raise RuntimeError("repair palette order drifted")
    return systems


def raw_execution_contexts() -> list[dict]:
    """48 starts. Every raw triad is present, whatever its orbit size."""
    sources = enumerate_hidden_contexts()
    masks = source_masks()
    graph_orbits = {}
    for key, record in sources.items():
        for orbit in record["orbits"]:
            for triad in orbit["members"]:
                graph_orbits[(key, triad)] = orbit
    contexts = []
    for key in ("star", "path", "triangle"):
        mask = masks[key]
        record = sources[key]
        for triad in range(16):
            orbit = graph_orbits[(key, triad)]
            config = triad_config_id(triad)
            contexts.append(
                {
                    "canonical_pair_mask": mask,
                    "canonical_triad": triad,
                    "class_index": record["class_index"],
                    "class_name": record["class_name"],
                    "directly_sampled_in_generation8": triad == orbit["canonical_triad"],
                    "graph_only_orbit_id": orbit["hidden_context_orbit_id"],
                    "graph_only_orbit_size": orbit["orbit_size"],
                    "hidden_context_orbit_id": config,
                    "orbit_size": 1,
                    "raw_triad_config": config,
                    "source_graph_class": key,
                    "start_state": mask | (triad << PAIR_SLOTS),
                    "triad_config_id": config,
                }
            )
    if len(contexts) != 48:
        raise RuntimeError(f"expected 48 raw starts, found {len(contexts)}")
    return contexts


def symmetry_table(systems: list[dict] | None = None) -> dict:
    chosen = systems if systems is not None else load_repair_palette()
    masks = source_masks()
    table = {}
    for system in chosen:
        per_source = {}
        for key in ("star", "path", "triangle"):
            partition = rule_aware_partition(masks[key], list(system["expressions"]))
            orbits = []
            for position, orbit in enumerate(partition["orbits"]):
                orbits.append(
                    {
                        **orbit,
                        "rule_aware_orbit_id": f"{key}-r{position:02d}",
                    }
                )
            lookup = {}
            for orbit in orbits:
                for config in orbit["raw_triad_configs"]:
                    lookup[config] = {
                        "rule_aware_orbit_id": orbit["rule_aware_orbit_id"],
                        "rule_aware_orbit_size": orbit["orbit_size"],
                    }
            per_source[key] = {
                "automorphism_group_size": partition["automorphism_group_size"],
                "automorphisms": partition["automorphisms"],
                "lookup": lookup,
                "orbit_count": len(orbits),
                "orbits": orbits,
            }
        table[system["system_id"]] = per_source
    return table


def _support_edges(triple: tuple[int, ...], slots) -> list[int]:
    named = set(triple)
    return [index for index, edge in enumerate(slots[:PAIR_SLOTS]) if set(edge) <= named]


def rule_relative_features(expressions: list[str], pair_mask: int, triad: int) -> list[dict]:
    """Analysis coordinates. They are not read by the sampler."""
    slots = _slots()
    state = pair_mask | (triad << PAIR_SLOTS)
    features = []
    for index, expression in enumerate(expressions):
        rule = parse_expression(expression, 4, order=3)
        conditions = []
        for slot, required in rule.conditions:
            support = None
            if slot >= PAIR_SLOTS:
                support = sum(1 for edge in _support_edges(slots[slot], slots) if (pair_mask >> edge) & 1)
            conditions.append(
                {
                    "polarity": "present" if required else "absent",
                    "present_in_start": bool((state >> slot) & 1),
                    "slot": slot,
                    "support_pair_edges_present": support,
                }
            )
        features.append(
            {
                "action_edge_in_source_graph": bool((pair_mask >> rule.action) & 1),
                "action_edge_present": bool((state >> rule.action) & 1),
                "action_slot": rule.action,
                "conditions": conditions,
                "direction": "form" if rule.polarity == FORM else "dissolve" if rule.polarity == DISSOLVE else str(rule.polarity),
                "expression": expression,
                "rule_index": index,
            }
        )
    return features


def crosswalk(systems: list[dict] | None = None, contexts: list[dict] | None = None, symmetry: dict | None = None) -> list[dict]:
    chosen = systems if systems is not None else load_repair_palette()
    starts = contexts if contexts is not None else raw_execution_contexts()
    groups = symmetry if symmetry is not None else symmetry_table(chosen)
    rows = []
    by_system = {system["system_id"]: system for system in chosen}
    for context in starts:
        for system in chosen:
            source = context["source_graph_class"]
            config = context["triad_config_id"]
            aware = groups[system["system_id"]][source]["lookup"][config]
            rows.append(
                {
                    "directly_sampled_in_generation8": context["directly_sampled_in_generation8"],
                    "graph_only_orbit_id": context["graph_only_orbit_id"],
                    "graph_only_orbit_size": context["graph_only_orbit_size"],
                    "parent_system_id": system["parent_system_id"],
                    "raw_triad_config": config,
                    "rule_aware_orbit_id": aware["rule_aware_orbit_id"],
                    "rule_aware_orbit_size": aware["rule_aware_orbit_size"],
                    "rule_features": rule_relative_features(
                        list(system["expressions"]),
                        int(context["canonical_pair_mask"]),
                        int(context["canonical_triad"]),
                    ),
                    "source_graph_class": source,
                    "system_id": system["system_id"],
                }
            )
    del by_system
    return rows


def graph_only_splits(symmetry: dict, contexts: list[dict]) -> list[dict]:
    """Graph-only orbits whose raw members receive more than one rule-aware orbit."""
    by_source_triad = {(row["source_graph_class"], row["triad_config_id"]): row for row in contexts}
    found = []
    for system_id, sources in symmetry.items():
        for source, record in sources.items():
            grouped: dict[str, set[str]] = {}
            sizes: dict[str, int] = {}
            for config, aware in record["lookup"].items():
                context = by_source_triad.get((source, config))
                if context is None:
                    continue
                grouped.setdefault(context["graph_only_orbit_id"], set()).add(aware["rule_aware_orbit_id"])
                sizes[context["graph_only_orbit_id"]] = context["graph_only_orbit_size"]
            for orbit_id, aware_ids in sorted(grouped.items()):
                if len(aware_ids) > 1:
                    found.append(
                        {
                            "graph_only_orbit_id": orbit_id,
                            "graph_only_orbit_size": sizes[orbit_id],
                            "rule_aware_orbit_ids": sorted(aware_ids),
                            "source_graph_class": source,
                            "system_id": system_id,
                        }
                    )
    return found


def class_edge_counts() -> list[int]:
    counts = []
    for name in CLASS_NAMES:
        match = _EDGE_NAME.match(name)
        if match is None:
            raise RuntimeError(f"pair class name has no edge count: {name}")
        counts.append(int(match.group(1)))
    if len(counts) != 11:
        raise RuntimeError("edge-count axis lost a pair class")
    return counts


def occupancy_shares(counts: list[int] | list[float]) -> dict[str, float]:
    total = float(sum(counts)) or 1.0
    edges = class_edge_counts()
    sparse = dense = three = 0.0
    for count, edge_count in zip(counts, edges):
        if edge_count <= 2:
            sparse += count
        elif edge_count == 3:
            three += count
        else:
            dense += count
    return {
        "dense_minus_sparse": (dense - sparse) / total,
        "dense_share": dense / total,
        "sparse_share": sparse / total,
        "three_edge_share": three / total,
    }


def _l1(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("occupancy vectors differ in length")
    left_total = sum(left) or 1.0
    right_total = sum(right) or 1.0
    return sum(abs((a / left_total) - (b / right_total)) for a, b in zip(left, right))


def conditional_mutual_information(cells: dict[tuple, int]) -> dict:
    """I(X; Y | Z) in nats from raw cells keyed (x, y, z)."""
    total = sum(cells.values())
    if total <= 0:
        return {"nats": None, "nonzero_cells": 0, "total": 0}
    z_count: Counter = Counter()
    xz_count: Counter = Counter()
    yz_count: Counter = Counter()
    for (x_value, y_value, z_value), count in cells.items():
        z_count[z_value] += count
        xz_count[(x_value, z_value)] += count
        yz_count[(y_value, z_value)] += count
    information = 0.0
    for (x_value, y_value, z_value), count in cells.items():
        if not count:
            continue
        p_xyz = count / total
        p_z = z_count[z_value] / total
        p_xz = xz_count[(x_value, z_value)] / total
        p_yz = yz_count[(y_value, z_value)] / total
        information += p_xyz * math.log((p_xyz * p_z) / (p_xz * p_yz))
    return {"nats": information, "nonzero_cells": sum(1 for count in cells.values() if count), "total": total}


def mutual_information(by_context: dict[str, dict[str, float]]) -> float | None:
    return _mutual_information(by_context)


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _range(values: list[float]) -> float | None:
    if not values:
        return None
    return max(values) - min(values)


def _group_rows(rows: list[dict]) -> dict[tuple[str, str, str], list[dict]]:
    grouped: dict[tuple[str, str, str], list[dict]] = {}
    for row in rows:
        key = (row["system_id"], row["source_graph_class"], row["triad_config_id"])
        grouped.setdefault(key, []).append(row)
    return grouped


def _destination_counts(group: list[dict]) -> dict[str, float]:
    counts: dict[str, float] = {}
    for row in group:
        label = row["route_recomputed"]["route_outcome"]
        counts[label] = counts.get(label, 0.0) + 1.0
    return counts


def _cell_summary(group: list[dict]) -> dict:
    destinations = _destination_counts(group)
    occupancy = [0] * 11
    returns = []
    times = []
    source_returns = []
    triad_fraction = []
    for row in group:
        for index, count in enumerate(row["pair_class_occupancy"]):
            occupancy[index] += int(count)
        route = row["route_recomputed"]
        if route["return_before_other_3edge"] is not None:
            returns.append(1.0 if route["return_before_other_3edge"] else 0.0)
        if route["time_to_next_3edge"] is not None:
            times.append(float(route["time_to_next_3edge"]))
        source_returns.append(float(row["source_returns"]))
        triad_fraction.append(float(row["triad_only_fraction"]))
    shares = occupancy_shares(occupancy)
    return {
        "dense_minus_sparse": shares["dense_minus_sparse"],
        "dense_share": shares["dense_share"],
        "destination_counts": destinations,
        "episodes": len(group),
        "mean_source_returns": _mean(source_returns),
        "mean_time_to_next_3edge": _mean(times),
        "occupancy_counts": occupancy,
        "return_before_other_3edge": _mean(returns),
        "sparse_share": shares["sparse_share"],
        "three_edge_share": shares["three_edge_share"],
        "triad_only_fraction": _mean(triad_fraction),
    }


def _pair_record(left_key, right_key, left: dict, right: dict) -> dict:
    return {
        "destination_js": _js(left["destination_counts"], right["destination_counts"]),
        "left": left_key[2],
        "mean_passage_left": left["mean_time_to_next_3edge"],
        "mean_passage_right": right["mean_time_to_next_3edge"],
        "occupancy_l1": _l1(left["occupancy_counts"], right["occupancy_counts"]),
        "return_before_left": left["return_before_other_3edge"],
        "return_before_right": right["return_before_other_3edge"],
        "right": right_key[2],
        "source_graph_class": left_key[1],
        "source_return_left": left["mean_source_returns"],
        "source_return_right": right["mean_source_returns"],
        "system_id": left_key[0],
    }


def _information_from_cells(cells: dict[tuple[str, str, str], dict], weight: str) -> list[dict]:
    """weight is uniform_raw_triad or uniform_orbit.

    uniform_raw_triad gives every raw configuration equal weight.
    uniform_orbit gives every named orbit equal weight, mixing its raw
    members equally before the orbit is weighted.
    """
    grouped: dict[tuple[str, str], dict[str, list[dict]]] = {}
    for (system_id, source, label), summary in cells.items():
        grouped.setdefault((system_id, source), {}).setdefault(label, []).append(summary)
    rows = []
    for (system_id, source), orbits in sorted(grouped.items()):
        by_context = {}
        contingencies = {}
        for label, members in sorted(orbits.items()):
            mixed: dict[str, float] = {}
            for summary in members:
                scale = 1.0 / len(members)
                for destination, count in summary["destination_counts"].items():
                    mixed[destination] = mixed.get(destination, 0.0) + scale * count
            by_context[label] = mixed
            contingencies[label] = mixed
        rows.append(
            {
                "contingency": contingencies,
                "measure": weight,
                "nats": mutual_information(by_context),
                "source_graph_class": source,
                "system_id": system_id,
                "unit": "nats",
            }
        )
    return rows


def _checkpoint_class(runs: list[list[int]], checkpoint: int) -> int | None:
    remaining = checkpoint
    for class_index, length in runs:
        if remaining < length:
            return class_index
        remaining -= length
    return None


def _checkpoint_information(rows: list[dict]) -> list[dict]:
    """I(raw initial triad; pair class at checkpoint), uniform over episodes of each config.

    Replicates are balanced, so episode-equal inside a config and then
    equal config weight matches the uniform raw-triad prior.
    """
    found = []
    systems = sorted({row["system_id"] for row in rows})
    sources = ("star", "path", "triangle")
    for system_id in systems:
        for source in sources:
            block = [row for row in rows if row["system_id"] == system_id and row["source_graph_class"] == source]
            if not block:
                continue
            for checkpoint in CHECKPOINTS:
                by_context: dict[str, dict[str, float]] = {}
                for row in block:
                    if row["pair_event_count"] < checkpoint:
                        continue
                    class_index = _checkpoint_class(row["class_runs"], checkpoint)
                    if class_index is None:
                        continue
                    label = CLASS_NAMES[class_index]
                    slot = by_context.setdefault(row["triad_config_id"], {})
                    slot[label] = slot.get(label, 0.0) + 1.0
                found.append(
                    {
                        "checkpoint": checkpoint,
                        "contingency": by_context,
                        "measure": "uniform_raw_triad",
                        "nats": mutual_information(by_context),
                        "source_graph_class": source,
                        "system_id": system_id,
                        "unit": "nats",
                    }
                )
    return found


def _cell_rows(cells: dict[tuple, int]) -> list[dict]:
    return [
        {"count": count, "x": item[0], "y": item[1], "z": item[2]}
        for item, count in sorted(cells.items())
        if count
    ]


def _conditional_report(conditional_counts: dict[tuple[str, str], dict]) -> list[dict]:
    rows = []
    for (system_id, source), buckets in sorted(conditional_counts.items()):
        class_given = conditional_mutual_information(buckets["class"])
        slot_class = conditional_mutual_information(buckets["slot_class"])
        slot_mask = conditional_mutual_information(buckets["slot_mask"])
        rows.append(
            {
                "cells": {
                    "current_triad_next_pair_class_given_pair_class": _cell_rows(buckets["class"]),
                    "current_triad_next_pair_slot_given_full_pair_mask": _cell_rows(buckets["slot_mask"]),
                    "current_triad_next_pair_slot_given_pair_class": _cell_rows(buckets["slot_class"]),
                },
                "current_triad_next_pair_class_given_pair_class": class_given,
                "current_triad_next_pair_slot_given_full_pair_mask": slot_mask,
                "current_triad_next_pair_slot_given_pair_class": slot_class,
                "event_definition": "next pair event is the pair-slot index 0..5; direction is the pre-state bit of that slot",
                "in_predeclared_current_context_subset": system_id in CURRENT_CONTEXT_SYSTEMS,
                "measure": "pair_event_weighted",
                "source_graph_class": source,
                "system_id": system_id,
                "unit": "nats",
            }
        )
    return rows


def _representative(rows: list[dict], system_id: str, source: str, configs: set[str]) -> str | None:
    chosen = [
        row
        for row in rows
        if row["system_id"] == system_id
        and row["source_graph_class"] == source
        and row["triad_config_id"] in configs
        and int(row["replicate_index"]) == 0
    ]
    if not chosen:
        chosen = [
            row
            for row in rows
            if row["system_id"] == system_id and row["source_graph_class"] == source and row["triad_config_id"] in configs
        ]
    if not chosen:
        return None
    return min(chosen, key=lambda row: row["episode_id"])["episode_id"]


def select_representatives(rows: list[dict], pairs: list[dict], conditionals: list[dict]) -> dict:
    """Deterministic episodes. Ties break by system, source, then config id.

    The four roles are the largest raw-context destination divergence, the
    largest raw-context occupancy divergence, the largest current-triad
    conditional on the full pair mask, and the smallest destination divergence.
    """
    def cell_key(row: dict) -> tuple:
        return (row["system_id"], row["source_graph_class"], row["left"], row["right"])

    if pairs:
        routing = min(pairs, key=lambda row: (-row["destination_js"], cell_key(row)))
        occupancy = min(pairs, key=lambda row: (-row["occupancy_l1"], cell_key(row)))
        quiet = min(pairs, key=lambda row: (row["destination_js"], cell_key(row)))
    else:
        routing = occupancy = quiet = None
    mask_rows = [
        row
        for row in conditionals
        if row["current_triad_next_pair_slot_given_full_pair_mask"]["nats"] is not None
    ]
    if mask_rows:
        conditional = min(
            mask_rows,
            key=lambda row: (
                -(row["current_triad_next_pair_slot_given_full_pair_mask"]["nats"]),
                row["system_id"],
                row["source_graph_class"],
            ),
        )
    else:
        conditional = None

    def pack(kind: str, pair: dict | None, configs: set[str] | None = None) -> dict | None:
        if pair is None:
            return None
        used = configs if configs is not None else {pair["left"], pair["right"]}
        return {
            "episode_id": _representative(rows, pair["system_id"], pair["source_graph_class"], used),
            "kind": kind,
            "selection": pair,
        }

    conditional_pack = None
    if conditional is not None:
        configs = {
            row["triad_config_id"]
            for row in rows
            if row["system_id"] == conditional["system_id"] and row["source_graph_class"] == conditional["source_graph_class"]
        }
        conditional_pack = {
            "episode_id": _representative(rows, conditional["system_id"], conditional["source_graph_class"], configs),
            "kind": "largest_current_triad_full_mask",
            "selection": {
                "nats": conditional["current_triad_next_pair_slot_given_full_pair_mask"]["nats"],
                "source_graph_class": conditional["source_graph_class"],
                "system_id": conditional["system_id"],
            },
        }
    return {
        "context_insensitive": pack("smallest_destination_js", quiet),
        "largest_current_triad_conditional": conditional_pack,
        "largest_occupancy_difference": pack("largest_occupancy_l1", occupancy),
        "largest_routing_difference": pack("largest_destination_js", routing),
        "rule": (
            "largest destination JS, then largest occupancy L1, then largest "
            "full-pair-mask current-triad conditional mutual information, then "
            "smallest destination JS; ties break by system id, source, and config id; "
            "the episode is replicate 0 with the smallest episode id"
        ),
    }


def repair_from_rows(rows: list[dict], plan: dict, conditional_counts: dict[tuple[str, str], dict]) -> dict:
    """Label every information figure with its measure."""
    cells = _group_rows(rows)
    summaries = {key: _cell_summary(group) for key, group in cells.items()}
    by_source: dict[tuple[str, str], list[tuple]] = {}
    for key in summaries:
        by_source.setdefault((key[0], key[1]), []).append(key)
    pairs = []
    split_pairs = []
    lookup = {}
    for row in plan["crosswalk"]:
        lookup[(row["system_id"], row["source_graph_class"], row["raw_triad_config"])] = row
    for (system_id, source), keys in sorted(by_source.items()):
        ordered = sorted(keys)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1:]:
                record = _pair_record(left, right, summaries[left], summaries[right])
                pairs.append(record)
                left_meta = lookup[(system_id, source, left[2])]
                right_meta = lookup[(system_id, source, right[2])]
                same_rule = left_meta["rule_aware_orbit_id"] == right_meta["rule_aware_orbit_id"]
                same_graph = left_meta["graph_only_orbit_id"] == right_meta["graph_only_orbit_id"]
                if same_graph and not same_rule:
                    split_pairs.append(record)
    raw_cells = {(key[0], key[1], key[2]): summary for key, summary in summaries.items()}
    rule_cells: dict[tuple[str, str, str], list] = {}
    graph_cells: dict[tuple[str, str, str], list] = {}
    for key, summary in summaries.items():
        meta = lookup[key]
        rule_cells.setdefault((key[0], key[1], meta["rule_aware_orbit_id"]), []).append(summary)
        graph_cells.setdefault((key[0], key[1], meta["graph_only_orbit_id"]), []).append(summary)
    orbit_rows = []
    for (system_id, source, orbit_id), members in sorted(rule_cells.items()):
        if len(members) < 2:
            continue
        js_values = []
        l1_values = []
        for index, left in enumerate(members):
            for right in members[index + 1:]:
                js_values.append(_js(left["destination_counts"], right["destination_counts"]))
                l1_values.append(_l1(left["occupancy_counts"], right["occupancy_counts"]))
        returns = [
            member["return_before_other_3edge"]
            for member in members
            if member["return_before_other_3edge"] is not None
        ]
        orbit_rows.append(
            {
                "max_destination_js": max(js_values) if js_values else 0.0,
                "max_occupancy_l1": max(l1_values) if l1_values else 0.0,
                "raw_contexts": len(members),
                "return_rate_range": _range(returns),
                "rule_aware_orbit_id": orbit_id,
                "source_graph_class": source,
                "system_id": system_id,
            }
        )

    def mix(groups: dict[tuple[str, str, str], list[dict]]) -> dict[tuple[str, str, str], dict]:
        mixed = {}
        for key, members in groups.items():
            mixed[key] = members[0] if len(members) == 1 else {
                "destination_counts": _mix_counts(members),
            }
        return mixed

    routing_rows = []
    for key, summary in sorted(summaries.items()):
        routing_rows.append(
            {
                "dense_minus_sparse": summary["dense_minus_sparse"],
                "dense_share": summary["dense_share"],
                "destination_counts": summary["destination_counts"],
                "episodes": summary["episodes"],
                "mean_source_returns": summary["mean_source_returns"],
                "mean_time_to_next_3edge": summary["mean_time_to_next_3edge"],
                "measure": "uniform_raw_triad",
                "return_before_other_3edge": summary["return_before_other_3edge"],
                "source_graph_class": key[1],
                "sparse_share": summary["sparse_share"],
                "system_id": key[0],
                "three_edge_share": summary["three_edge_share"],
                "triad_config_id": key[2],
                "triad_only_fraction": summary["triad_only_fraction"],
            }
        )
    source_rows = []
    for (system_id, source), keys in sorted(by_source.items()):
        block = [summaries[key] for key in keys]
        js_values = [
            record["destination_js"]
            for record in pairs
            if record["system_id"] == system_id and record["source_graph_class"] == source
        ]
        l1_values = [
            record["occupancy_l1"]
            for record in pairs
            if record["system_id"] == system_id and record["source_graph_class"] == source
        ]
        returns = [summaries[key]["return_before_other_3edge"] for key in keys if summaries[key]["return_before_other_3edge"] is not None]
        times = [summaries[key]["mean_time_to_next_3edge"] for key in keys if summaries[key]["mean_time_to_next_3edge"] is not None]
        orbit_block = [
            record
            for record in orbit_rows
            if record["system_id"] == system_id and record["source_graph_class"] == source
        ]
        split_block = [
            record
            for record in split_pairs
            if record["system_id"] == system_id and record["source_graph_class"] == source
        ]
        split_configs = {record["left"] for record in split_block} | {record["right"] for record in split_block}
        split_returns = [
            summaries[(system_id, source, config)]["return_before_other_3edge"]
            for config in split_configs
            if summaries[(system_id, source, config)]["return_before_other_3edge"] is not None
        ]
        source_rows.append(
            {
                "max_destination_js": max(js_values) if js_values else 0.0,
                "max_occupancy_l1": max(l1_values) if l1_values else 0.0,
                "median_destination_js": _median(js_values),
                "passage_time_range": _range([value for value in times if value is not None]),
                "raw_context_count": len(keys),
                "return_before_range": _range(returns),
                "source_graph_class": source,
                "split_graph_only_max_destination_js": max((row["destination_js"] for row in split_block), default=None),
                "split_graph_only_max_occupancy_l1": max((row["occupancy_l1"] for row in split_block), default=None),
                "split_graph_only_return_range": _range(split_returns),
                "system_id": system_id,
                "within_rule_aware_max_destination_js": max((row["max_destination_js"] for row in orbit_block), default=None),
                "within_rule_aware_max_occupancy_l1": max((row["max_occupancy_l1"] for row in orbit_block), default=None),
                "within_rule_aware_return_range": max((row["return_rate_range"] for row in orbit_block if row["return_rate_range"] is not None), default=None),
            }
        )
        del block
    conditionals = _conditional_report(conditional_counts)
    return {
        "checkpoint_pair_class_information": _checkpoint_information(rows),
        "current_context": conditionals,
        "pairwise_count": len(pairs),
        "rule_aware_orbit_consistency": orbit_rows,
        "raw_context_routing": routing_rows,
        "representatives": select_representatives(rows, pairs, conditionals),
        "source_comparisons": source_rows,
        "uniform_graph_only_orbit_from_this_sample": _information_from_cells(mix(graph_cells), "uniform_graph_only_orbit"),
        "uniform_raw_triad_information": _information_from_cells(raw_cells, "uniform_raw_triad"),
        "uniform_rule_aware_orbit_information": _information_from_cells(mix(rule_cells), "uniform_rule_aware_orbit"),
    }


def _mix_counts(members: list[dict]) -> dict[str, float]:
    mixed: dict[str, float] = {}
    scale = 1.0 / len(members)
    for summary in members:
        for destination, count in summary["destination_counts"].items():
            mixed[destination] = mixed.get(destination, 0.0) + scale * count
    return mixed


def system_occupancy(rows: list[dict]) -> dict[str, dict]:
    found = {}
    for system_id in sorted({row["system_id"] for row in rows}):
        totals = [0] * 11
        block = [row for row in rows if row["system_id"] == system_id]
        for row in block:
            for index, count in enumerate(row["pair_class_occupancy"]):
                totals[index] += int(count)
        shares = occupancy_shares(totals)
        found[system_id] = {"counts": totals, **shares, "episodes": len(block)}
    return found


def additive_residual(occupancy: dict[str, dict]) -> dict | None:
    """R05 against R03 + R04 - R00, on the 11-class share. Descriptive only."""
    needed = ("R00", "R03", "R04", "R05")
    if any(key not in occupancy for key in needed):
        return None
    vectors = {}
    for key in needed:
        counts = occupancy[key]["counts"]
        total = float(sum(counts)) or 1.0
        vectors[key] = [count / total for count in counts]
    residual = [
        vectors["R05"][index] - (vectors["R03"][index] + vectors["R04"][index] - vectors["R00"][index])
        for index in range(11)
    ]
    return {
        "definition": "R05 share minus (R03 share + R04 share - R00 share)",
        "dense_minus_sparse": {
            key: occupancy[key]["dense_minus_sparse"] for key in needed
        },
        "l1": sum(abs(value) for value in residual),
        "residual_share": residual,
    }


def verify_plan_result_chronology(
    repo: Path,
    frozen: str,
    result: str,
    relpath: str,
    expected_hash: str | None = None,
) -> dict:
    """The frozen plan commit is an ancestor of the result, and its plan hashes."""
    import subprocess

    ancestor = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", frozen, result],
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise ChronologyError(f"{frozen} is not an ancestor of {result}")
    shown = subprocess.run(
        ["git", "-C", str(repo), "show", f"{frozen}:{relpath}"],
        capture_output=True,
    )
    if shown.returncode != 0:
        raise ChronologyError(f"plan file {relpath} is absent at {frozen}")
    document = json.loads(shown.stdout.decode("utf-8"))
    digest = plan_hash(document)
    if document.get("plan_hash") != digest:
        raise ChronologyError("recorded plan_hash does not match the plan body")
    if expected_hash is not None and digest != expected_hash:
        raise ChronologyError(f"plan hash {digest} does not match the expected record {expected_hash}")
    return {
        "frozen_plan_commit": frozen,
        "plan_hash": digest,
        "plan_relpath": relpath,
        "result_commit": result,
    }


def verify_recorded_chronology(repo: Path, rounds: list[dict] | tuple[dict, ...]) -> list[dict]:
    return [
        verify_plan_result_chronology(
            repo,
            row["frozen_plan_commit"],
            row["result_commit"],
            row["plan_relpath"],
            row["plan_hash"],
        )
        for row in rounds
    ]


def verify_journey_chronology(repo: Path, path: Path) -> list[dict]:
    """Check journey lines that already name both commits and a plan path.

    A line written before the result commit exists is skipped. The check does
    not rewrite the line.
    """
    if not path.is_file():
        return []
    reports = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        frozen = row.get("frozen_plan_commit")
        result = row.get("result_commit")
        relpath = row.get("plan_relpath")
        if not frozen or not result or not relpath:
            continue
        reports.append(
            verify_plan_result_chronology(repo, frozen, result, relpath, row.get("plan_hash"))
        )
    return reports


def analysis_measure_catalogue() -> list[dict]:
    return [
        {
            "estimand": "I(raw initial triad; first other 3-edge destination)",
            "id": "uniform_raw_triad",
            "prior": "each of the 16 raw triad configurations has equal weight",
            "unit": "nats",
        },
        {
            "estimand": "I(rule-aware orbit; first other 3-edge destination)",
            "id": "uniform_rule_aware_orbit",
            "prior": "each rule-aware orbit has equal weight; raw members inside an orbit are mixed equally",
            "unit": "nats",
        },
        {
            "estimand": "I(graph-only orbit; first other 3-edge destination) on the Generation 8A raw sample",
            "id": "uniform_graph_only_orbit_from_this_sample",
            "note": "This pools raw configurations that share a Generation 8 orbit. It is not the Generation 8 published estimate, which executed one representative per orbit under a different seed.",
            "prior": "each graph-only orbit has equal weight",
            "unit": "nats",
        },
        {
            "estimand": "I(raw initial triad; pair class at checkpoint)",
            "id": "checkpoint_pair_class",
            "checkpoints": list(CHECKPOINTS),
            "prior": "uniform raw triad",
            "unit": "nats",
        },
        {
            "estimand": "I(current triad; next pair class | current pair class)",
            "event_definition": "next pair class is the isomorphism class after a pair-slot toggle",
            "id": "current_triad_next_pair_class_given_pair_class",
            "systems": "every A0 system, which includes " + ", ".join(CURRENT_CONTEXT_SYSTEMS),
            "weight": "pair events",
            "unit": "nats",
        },
        {
            "estimand": "I(current triad; next pair slot | current pair isomorphism class)",
            "event_definition": "next pair event is the pair-slot index 0..5",
            "id": "current_triad_next_pair_slot_given_pair_class",
            "unit": "nats",
        },
        {
            "estimand": "I(current triad; next pair slot | full labelled pair mask)",
            "event_definition": "the conditioner is the 6-bit pair mask, not the 11-class label",
            "id": "current_triad_next_pair_slot_given_full_pair_mask",
            "unit": "nats",
        },
    ]


def canonical_plan_body(document: dict) -> str:
    return canonical_json({key: value for key, value in document.items() if key != "plan_hash"})
