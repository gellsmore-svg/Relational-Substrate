"""Bounded Generation 8D two-gate composition execution.

Each item is one structural orbit, or the one-gate weak-grade surface.
A completed item file is not recomputed when a later item fails.
The runner records wall time and refuses an item past the 120-second watchdog.
No stochastic trajectory is sampled.
"""

from __future__ import annotations

import csv
import io
import time
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, atomic_write_text, canonical_json, read_json, sha256_bytes
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.explore08d import (
    ANALYSIS_VERSION,
    CMI_TOLERANCE,
    EXPERIMENT_ID,
    GRADES,
    KERNEL_TOLERANCE,
    LOGIT_TOLERANCE,
    N_FULL_STATES,
    PROBABILITY_TOLERANCE,
    REDUCIBILITY_TOLERANCE,
    ROUND_ID,
    CompositionError,
    analyse_orbit,
    census_summary,
    duplicate_kernel_product,
    expressivity_bound,
    general_normalisation_identities,
    load_universe,
    one_gate_surface,
    universe_public,
)
from rs_constraint_lab.weights import alphabet_factors

PLAN_RELPATH = "constraint-lab/exploration/generation-008d/round-d0-plan.json"
WATCHDOG_SECONDS = 120
WALL_TIME_ESTIMATE_SECONDS = 1200
DISK_ESTIMATE_BYTES = 80_000_000
SCHEMA = "rs-constraint-lab.composition-tables/v1"
FAMILIES = (
    "complementary_gate",
    "different_actions_different_gates",
    "different_actions_same_gate",
    "same_action_different_gates",
    "same_slot_opposite_directions",
)
CLASS_DIMENSION = {"R0": 0, "R1U": 0, "R1G": 1, "R1T": 1, "R2S": 1, "R2G": 2}
SYNTACTIC_CLASSES = {"R0", "R1U", "R1G"}


class CompositionRunError(RuntimeError):
    """The D0 runner refused a plan, an item, or a table."""


def item_id(item: dict) -> str:
    if item["kind"] == "surface":
        return "surface"
    return f"orbit-{item['orbit_id']}"


def item_path(root: Path, item: dict) -> Path:
    return root / "items" / f"{item_id(item)}.json"


def d0_items() -> list[dict]:
    universe = load_universe()
    items = [{"kind": "orbit", "orbit_id": orbit["orbit_id"]} for orbit in universe["orbits"]]
    items.append({"kind": "surface", "orbit_id": None})
    return items


def _universe_record() -> dict:
    public = universe_public()
    digest = sha256_bytes(canonical_json(public).encode("utf-8"))
    return {
        "duplicate_structural_rules_allowed": False,
        "labelled_pair_count": public["labelled_pair_count"],
        "labelled_rule_count": public["labelled_rule_count"],
        "sha256": digest,
        "structural_orbit_count": public["structural_orbit_count"],
        "weighted_canonical_count": public["weighted_canonical_count"],
    }


def prepare_d0_plan(repo: Path | None = None) -> dict:
    """Analysis contract. No D0 measurement is stored here."""
    del repo
    universe = _universe_record()
    weighted = universe["weighted_canonical_count"]
    factors = alphabet_factors("W4")
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "canonicalisation": {
            "bit_complement": False,
            "rule_order": "unordered",
            "vertex_permutations": 24,
            "weight_reciprocity": False,
            "weight_tie_break": "lexicographic weight name, not grade order",
        },
        "estimands": [
            "labelled one-gate rules and allowed unordered pairs",
            "S4 structural orbits and W4 weighted canonical systems",
            "minimal raw coordinates of the six-slot law",
            "effective gate dimension in {0, 1, 2}",
            "truth table of literal activation and the normalised six-slot law",
            "log-weight additivity and the logit interaction on two literals",
            "probability-space normalisation for shared and distinct action slots",
            "local-law reducibility against the one-rule comparison grammar",
            "balanced I(current triad; next pair slot | full pair mask)",
            "ablation of each rule",
            "one-gate balanced information and edge drift at the four W4 grades",
        ],
        "execution": {
            "atomic_item": "one structural orbit, or the one-gate weak-grade surface",
            "commands": ["execute-item", "run-d0", "assemble"],
            "heartbeat": "status.json rewritten after each completed or skipped item",
            "resume": "an item file that already exists is not recomputed",
            "stochastic_trajectories": False,
            "supervisor": "not used; a measured orbit is a few seconds and stays under the watchdog",
            "watchdog_seconds": WATCHDOG_SECONDS,
            "workers": 1,
        },
        "experiment_id": EXPERIMENT_ID,
        "history": False,
        "items": d0_items(),
        "mode": "B",
        "new_controls": False,
        "ontology": {"G": 0, "H": 0, "hypergraph": "independent", "L": 0, "N": 4, "O": 3, "S": 0},
        "parameter_fit": False,
        "question": "When two higher-order relational gates coexist in the same memoryless relational system, what exact algebra of composition appears?",
        "round_id": ROUND_ID,
        "schema": "rs-constraint-lab.composition-plan/v1",
        "stochastic_trajectories": False,
        "timing_sample": {
            "max_item_seconds": 5.551,
            "measured_orbit_pass_seconds": 719.543,
            "note": "A complete orbit pass on this implementation finished in 719.543 seconds. The slowest orbit took 5.551 seconds. The wall-time figure is a bound above that pass, not a fitted parameter.",
            "sample_seconds": 7.472,
            "sample_systems": 52,
        },
        "tolerances": {
            "canonicalisation": "exact",
            "cmi_equality": CMI_TOLERANCE,
            "fraction_equality": "exact",
            "kernel_equality": KERNEL_TOLERANCE,
            "logit_additivity": LOGIT_TOLERANCE,
            "probability_gap": PROBABILITY_TOLERANCE,
            "reducibility": REDUCIBILITY_TOLERANCE,
        },
        "universe": universe,
        "weight_alphabet": {
            "factors": {name: f"{factors[name].numerator}/{factors[name].denominator}" for name in GRADES},
            "grades": list(GRADES),
            "name": "W4",
            "neutral_excluded": True,
        },
        "work_count": {
            "disk_estimate_bytes": DISK_ESTIMATE_BYTES,
            "full_state_evaluations": weighted * N_FULL_STATES,
            "items": universe["structural_orbit_count"] + 1,
            "kernel_agreement_evaluations": weighted * N_FULL_STATES,
            "s4_law_images": weighted * 24,
            "structural_orbit_items": universe["structural_orbit_count"],
            "surface_items": 1,
            "wall_time_estimate_seconds": WALL_TIME_ESTIMATE_SECONDS,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def _require_plan_contract(plan: dict) -> None:
    if plan.get("stochastic_trajectories") is not False or plan.get("history") is not False:
        raise CompositionRunError("execution refused: D0 does not add trajectories or history")
    if plan.get("new_controls") is not False or plan.get("parameter_fit") is not False:
        raise CompositionRunError("execution refused: D0 does not add controls or fit a parameter")
    if plan.get("ontology") != {"G": 0, "H": 0, "hypergraph": "independent", "L": 0, "N": 4, "O": 3, "S": 0}:
        raise CompositionRunError("execution refused: D0 ontology drifted")
    if plan.get("experiment_id") != EXPERIMENT_ID or plan.get("round_id") != ROUND_ID:
        raise CompositionRunError("execution refused: plan identity drifted")
    universe = _universe_record()
    if plan.get("universe") != universe:
        raise CompositionRunError("execution refused: the labelled universe drifted from the frozen plan")
    if [item["orbit_id"] for item in plan.get("items", []) if item["kind"] == "orbit"] != [
        item["orbit_id"] for item in d0_items() if item["kind"] == "orbit"
    ]:
        raise CompositionRunError("execution refused: the orbit item list drifted")


def require_d0_execution(
    repo: Path,
    commit: str | None,
    relpath: str,
    disk_path: Path | None = None,
    *,
    require_remote: bool = True,
) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, relpath, disk_path=disk_path)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    _require_plan_contract(plan)
    return plan


def _execute_orbit(orbit_id: str) -> dict:
    universe = load_universe()
    orbit = next(item for item in universe["orbits"] if item["orbit_id"] == orbit_id)
    analysed = analyse_orbit(orbit_id, with_class=True)
    return {
        "canonical_rules": orbit["canonical_rules"],
        "descriptors": orbit["descriptors"],
        "orbit_id": orbit["orbit_id"],
        "orbit_size": orbit["orbit_size"],
        "systems": analysed["systems"],
    }


def _execute_surface() -> dict:
    return {
        "duplicate_rule": duplicate_kernel_product(),
        "expressivity": expressivity_bound(),
        "normalisation": general_normalisation_identities(),
        "one_gate_surface": one_gate_surface(),
    }


def execute_plan_item(item: dict) -> dict:
    started = time.perf_counter()
    kind = item["kind"]
    if kind == "orbit":
        result = _execute_orbit(item["orbit_id"])
    elif kind == "surface":
        result = _execute_surface()
    else:
        raise CompositionRunError(f"unknown D0 item kind {kind}")
    wall = time.perf_counter() - started
    if wall > WATCHDOG_SECONDS:
        raise CompositionRunError(f"{item_id(item)} exceeded the {WATCHDOG_SECONDS}s watchdog ({wall:.1f}s)")
    return {"item": item, "item_id": item_id(item), "result": result, "wall_seconds": wall}


def _reusable(path: Path, item: dict) -> bool:
    if not path.is_file():
        return False
    try:
        payload = read_json(path)
    except (OSError, ValueError):
        return False
    return payload.get("item_id") == item_id(item) and "result" in payload


def _write_status(root: Path, *, completed: int, total: int, last_item_id: str, last_wall: float, max_wall: float, skipped: int) -> None:
    atomic_write_json(
        root / "status.json",
        {
            "completed_items": completed,
            "item_count": total,
            "last_item_id": last_item_id,
            "last_wall_seconds": last_wall,
            "max_wall_seconds": max_wall,
            "skipped_existing_items": skipped,
            "updated_unix": time.time(),
        },
    )


def run_d0(root: Path, plan: dict) -> list[dict]:
    """Execute every missing item. An existing item file is left untouched."""
    summaries = []
    max_wall = 0.0
    skipped = 0
    total = len(plan["items"])
    for index, item in enumerate(plan["items"], start=1):
        path = item_path(root, item)
        reused = _reusable(path, item)
        if reused:
            payload = read_json(path)
            skipped += 1
        else:
            payload = execute_plan_item(item)
            atomic_write_json(path, payload)
        wall = float(payload["wall_seconds"])
        max_wall = max(max_wall, wall)
        summaries.append({"item_id": payload["item_id"], "skipped": reused, "wall_seconds": wall})
        _write_status(
            root,
            completed=index,
            total=total,
            last_item_id=payload["item_id"],
            last_wall=wall,
            max_wall=max_wall,
            skipped=skipped,
        )
    return summaries


def _fraction(text: str) -> Fraction:
    try:
        value = Fraction(text)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise CompositionError(f"not a fraction: {text}") from exc
    return value


def _check_law(text_row: list[str] | None, label: str, problems: list[str]) -> None:
    if text_row is None:
        return
    if len(text_row) != 6:
        problems.append(f"{label} does not have six slots")
        return
    weights = [_fraction(item) for item in text_row]
    if any(weight <= 0 for weight in weights):
        problems.append(f"{label} is not positive")
    if sum(weights, Fraction(0)) != 1:
        problems.append(f"{label} does not sum to 1")


def validate_orbit_result(result: dict) -> list[str]:
    """Software checks. A failure is an execution problem, not a scientific ranking."""
    problems: list[str] = []
    descriptors = result["descriptors"]
    family = descriptors["composition_family"]
    if family not in FAMILIES:
        problems.append(f"{result['orbit_id']} has an unclassified family {family}")
    # A repeated rule is the same slot, the same gate, the same literal, and
    # the same direction. Form and dissolve on that slot are two rules.
    repeated = (
        descriptors["action_relation"] == "same_pair"
        and descriptors["gate_relation"] == "same_triad"
        and descriptors["polarity_relation"] == "same_polarity"
        and descriptors["direction_relation"] == "same_direction"
    )
    if repeated:
        problems.append(f"{result['orbit_id']} repeats a structural rule")
    for system in result["systems"]:
        label = system["system_id"]
        if system["effective_gate_dimension"] != CLASS_DIMENSION[system["reducibility_class"]]:
            problems.append(f"{label} class and effective dimension disagree")
        syntactic = system["reducibility_class"] in SYNTACTIC_CLASSES
        if system["syntactic_one_rule"] is not syntactic:
            problems.append(f"{label} syntactic flag disagrees with its class")
        if syntactic and system["reducibility_class"] in {"R1U", "R1G"} and len(system["comparator_expressions"]) != 1:
            problems.append(f"{label} is missing its one-rule comparator")
        if not syntactic and system["comparator_expressions"]:
            problems.append(f"{label} carries a comparator outside the one-rule classes")
        if system["kernel_max_abs_gap"] > KERNEL_TOLERANCE:
            problems.append(f"{label} kernel gap {system['kernel_max_abs_gap']}")
        if system["log_weight_gap"] > LOGIT_TOLERANCE:
            problems.append(f"{label} log-weight gap {system['log_weight_gap']}")
        if system["information"]["truth_table_cmi_gap"] > CMI_TOLERANCE:
            problems.append(f"{label} truth-table CMI gap")
        if sum(row["state_count"] for row in system["truth_table"]) != N_FULL_STATES:
            problems.append(f"{label} truth table misses a state")
        if sum(row["state_count"] for row in system["row_fingerprints"]) != N_FULL_STATES:
            problems.append(f"{label} fingerprint misses a state")
        if len(system["row_fingerprints"]) != system["distinct_local_law_rows"]:
            problems.append(f"{label} row count disagrees with its fingerprints")
        for row in system["truth_table"]:
            _check_law(row["normalised_slot_law"], label, problems)
        if any(len(chosen) != system["minimal_coordinate_count"] for chosen in system["minimal_coordinate_sets"]):
            problems.append(f"{label} minimal coordinate set has the wrong length")
        ablations = {row["ablation"]: row for row in system["ablations"]}
        if not ablations["full"]["law_equal_to_full"] or ablations["full"]["max_probability_gap"] != 0.0:
            problems.append(f"{label} full ablation is not the system itself")
        for role, other_name in ((system["gate_roles"][0], "rule_2_only"), (system["gate_roles"][1], "rule_1_only")):
            redundant = ablations[other_name]["law_equal_to_full"]
            if role["redundant"] is not redundant or role["necessary_for_a_local_law_distinction"] is redundant:
                problems.append(f"{label} gate role disagrees with its ablation")
            if role["active_on_a_proper_subset"] is not True:
                problems.append(f"{label} gate is not active on a proper subset")
        masked = family == "complementary_gate" and system["weights"][0] == system["weights"][1]
        if any(role["masked_by_equal_weights"] is not masked for role in system["gate_roles"]):
            problems.append(f"{label} equal-weight mask flag disagrees with the family")
        identities = system["identities"]
        if family == "same_action_different_gates":
            if identities["logit_interaction_checks"] != 1 or identities["logit_interaction_gap"] > LOGIT_TOLERANCE:
                problems.append(f"{label} logit interaction was not verified")
            if identities["same_action_gap"] > REDUCIBILITY_TOLERANCE or identities["same_action_both_active_checks"] <= 0:
                problems.append(f"{label} same-action normalisation was not verified")
        if family in {"different_actions_same_gate", "different_actions_different_gates"}:
            # Opposite literals of one gate cannot be true together, so the
            # shared denominator has no realised state.
            exclusive = descriptors["polarity_relation"] == "opposite_polarity"
            if exclusive:
                if identities["different_action_both_active_checks"] or identities["different_action_gap"] > REDUCIBILITY_TOLERANCE:
                    problems.append(f"{label} opposite gate literals were both active")
            elif identities["different_action_gap"] > REDUCIBILITY_TOLERANCE or identities["different_action_both_active_checks"] <= 0:
                problems.append(f"{label} different-action normalisation was not verified")
        if family == "same_slot_opposite_directions":
            if identities["same_action_both_active_checks"] or identities["different_action_both_active_checks"]:
                problems.append(f"{label} opposite directions on one slot were both active")
        if family == "complementary_gate" and system["reducibility_class"] not in {"R1U", "R1T"}:
            problems.append(f"{label} complementary gate is not R1U or R1T")
        if family == "complementary_gate" and system["weights"][0] == system["weights"][1] and system["reducibility_class"] != "R1U":
            problems.append(f"{label} equal complementary gates did not eliminate")
        if family == "complementary_gate" and system["weights"][0] != system["weights"][1] and system["reducibility_class"] != "R1T":
            problems.append(f"{label} unequal complementary gates did not stay two-level")
        if descriptors["gate_relation"] == "different_triads":
            info = system["information"]
            if None in (info["gate_1_marginal_information"], info["gate_2_marginal_information"], info["conditional_gate_1_given_2"], info["conditional_gate_2_given_1"]):
                problems.append(f"{label} is missing a two-gate information term")
        else:
            info = system["information"]
            if info["conditional_gate_1_given_2"] is not None or info["conditional_gate_2_given_1"] is not None:
                problems.append(f"{label} has a conditional term for one shared gate")
    return problems


def _identity_rows(system: dict, family: str) -> list[dict]:
    rows = [
        {
            "comparison_system": None,
            "identity_type": "log_weight_additivity",
            "max_gap": system["log_weight_gap"],
            "system_id": system["system_id"],
            "verified": system["log_weight_gap"] <= LOGIT_TOLERANCE,
        },
        {
            "comparison_system": "build_kernel",
            "identity_type": "kernel_agreement",
            "max_gap": system["kernel_max_abs_gap"],
            "system_id": system["system_id"],
            "verified": system["kernel_max_abs_gap"] <= KERNEL_TOLERANCE,
        },
    ]
    identities = system["identities"]
    if identities["same_action_both_active_checks"]:
        rows.append(
            {
                "comparison_system": "m1*m2/(m1*m2+5)",
                "identity_type": "same_action_normalisation",
                "max_gap": identities["same_action_gap"],
                "system_id": system["system_id"],
                "verified": identities["same_action_gap"] <= REDUCIBILITY_TOLERANCE,
            }
        )
    if identities["different_action_both_active_checks"]:
        rows.append(
            {
                "comparison_system": "(m1+m2+4)",
                "identity_type": "different_action_normalisation",
                "max_gap": identities["different_action_gap"],
                "system_id": system["system_id"],
                "verified": identities["different_action_gap"] <= REDUCIBILITY_TOLERANCE,
            }
        )
    if identities["logit_interaction_checks"]:
        rows.append(
            {
                "comparison_system": "L11-L10-L01+L00",
                "identity_type": "logit_interaction",
                "max_gap": identities["logit_interaction_gap"],
                "system_id": system["system_id"],
                "verified": identities["logit_interaction_gap"] <= LOGIT_TOLERANCE,
            }
        )
    if system["comparator_expressions"]:
        rows.append(
            {
                "comparison_system": " + ".join(system["comparator_expressions"]),
                "identity_type": "complementary_gate_elimination" if family == "complementary_gate" else "reducible_kernel_equality",
                "max_gap": 0.0,
                "system_id": system["system_id"],
                "verified": True,
            }
        )
    elif system["reducibility_class"] == "R1T":
        rows.append(
            {
                "comparison_system": "algebraic two-level law; not one primitive DSL rule",
                "identity_type": "two_level_complementary_law",
                "max_gap": 0.0,
                "system_id": system["system_id"],
                "verified": True,
            }
        )
    return rows


def _load_items(root: Path, plan: dict) -> dict[str, dict]:
    loaded = {}
    missing = []
    for item in plan["items"]:
        path = item_path(root, item)
        if not path.is_file():
            missing.append(item_id(item))
            continue
        loaded[item_id(item)] = read_json(path)
    if missing:
        raise CompositionRunError("D0 assemble is missing items: " + ", ".join(missing[:12]))
    return loaded


def assemble_tables(root: Path, plan: dict, *, repo: Path | None = None, frozen_plan_commit: str | None = None) -> dict:
    del repo
    loaded = _load_items(root, plan)
    problems: list[str] = []
    orbits = []
    systems = []
    truth_rows = []
    information_rows = []
    ablation_rows = []
    identity_rows = []
    analysis_rows = []
    orbit_meta = []
    for item in plan["items"]:
        if item["kind"] != "orbit":
            continue
        payload = loaded[item_id(item)]
        result = payload["result"]
        problems.extend(validate_orbit_result(result))
        descriptors = result["descriptors"]
        orbits.append(
            {
                "action_relation": descriptors["action_relation"],
                "canonical_rules": result["canonical_rules"],
                "composition_family": descriptors["composition_family"],
                "cross_incidence": descriptors["cross_incidence"],
                "direction_relation": descriptors["direction_relation"],
                "gate_relation": descriptors["gate_relation"],
                "incidence_matrix": descriptors["incidence_matrix"],
                "orbit_id": result["orbit_id"],
                "orbit_size": result["orbit_size"],
                "own_incidence": descriptors["own_incidence"],
                "polarity_relation": descriptors["polarity_relation"],
                "weighted_system_count": len(result["systems"]),
            }
        )
        orbit_meta.append({"descriptors": descriptors, "orbit_id": result["orbit_id"]})
        for system in result["systems"]:
            analysis_rows.append(system)
            systems.append(
                {
                    "canonical_weighted_rules": system["canonical_weighted_rules"],
                    "comparator_expressions": system["comparator_expressions"],
                    "composition_family": descriptors["composition_family"],
                    "distinct_local_law_rows": system["distinct_local_law_rows"],
                    "effective_gate_dimension": system["effective_gate_dimension"],
                    "labelled_law_sha256": system["labelled_law_sha256"],
                    "local_law_class": system["local_law_class"],
                    "minimal_coordinate_count": system["minimal_coordinate_count"],
                    "minimal_coordinate_sets": system["minimal_coordinate_sets"],
                    "reducibility_class": system["reducibility_class"],
                    "structural_orbit_id": system["structural_orbit_id"],
                    "syntactic_one_rule": system["syntactic_one_rule"],
                    "system_id": system["system_id"],
                    "weights": system["weights"],
                }
            )
            for cell in system["truth_table"]:
                truth_rows.append(
                    {
                        "active_rules": cell["active_rules"],
                        "gate_literal_state": cell["gate_literal_state"],
                        "normalised_slot_law": cell["normalised_slot_law"],
                        "pair_admissibility_state": cell["pair_admissibility_state"],
                        "pre_normalisation_weights": cell["pre_normalisation_weights"],
                        "realised": cell["realised"],
                        "state_count": cell["state_count"],
                        "system_id": system["system_id"],
                    }
                )
            info = system["information"]
            information_rows.append(
                {
                    "balanced_full_triad_cmi": info["balanced_full_triad_cmi"],
                    "conditional_gate_1_given_2": info["conditional_gate_1_given_2"],
                    "conditional_gate_2_given_1": info["conditional_gate_2_given_1"],
                    "gate_1_marginal_information": info["gate_1_marginal_information"],
                    "gate_2_marginal_information": info["gate_2_marginal_information"],
                    "joint_gate_information": info["balanced_full_triad_cmi"] if descriptors["gate_relation"] == "different_triads" else None,
                    "system_id": system["system_id"],
                    "truth_table_cmi_gap": info["truth_table_cmi_gap"],
                }
            )
            for ablation in system["ablations"]:
                ablation_rows.append({"system_id": system["system_id"], **ablation})
            identity_rows.extend(_identity_rows(system, descriptors["composition_family"]))
    if sum(orbit["orbit_size"] for orbit in orbits) != plan["universe"]["labelled_pair_count"]:
        problems.append("orbit sizes do not sum to the labelled-pair count")
    if len(systems) != plan["universe"]["weighted_canonical_count"]:
        problems.append("weighted system count drifted")
    surface = loaded["surface"]["result"]
    if surface["duplicate_rule"]["accepted_in_atlas"] is not False:
        problems.append("a duplicate structural rule entered the atlas")
    if surface["one_gate_surface"]["unconditional_doubles_conditional"] is not True:
        problems.append("unconditional drift did not double the one-gate mean")
    for sample in surface["normalisation"]["samples"]:
        if _fraction(str(sample["same_action_gap"])) != 0 or _fraction(str(sample["different_action_gap"])) != 0:
            problems.append("a general normalisation sample missed")
    summary = census_summary(analysis_rows, orbit_meta)
    walls = [float(payload["wall_seconds"]) for payload in loaded.values()]
    return {
        "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "plan_hash": plan["plan_hash"],
        "round_id": ROUND_ID,
        "schema": SCHEMA,
        "stochastic_trajectories": False,
        "summary": summary,
        "surface": surface,
        "tables": {
            "ablations": ablation_rows,
            "identities": identity_rows,
            "information": information_rows,
            "structural_orbits": orbits,
            "truth_tables": truth_rows,
            "weighted_systems": systems,
        },
        "validation": {"ok": not problems, "problems": problems},
        "wall_seconds_max": max(walls) if walls else None,
    }


def _csv(rows: list[dict], columns: list[str]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        rendered = {}
        for column in columns:
            value = row.get(column)
            if isinstance(value, (list, dict)):
                value = canonical_json(value)
            rendered[column] = value
        writer.writerow(rendered)
    return buffer.getvalue()


def publish_tables(payload: dict, reports: Path) -> dict[str, str]:
    """Write the summary and the column tables. Returns the sha256 of each file's canonical body."""
    tables = payload["tables"]
    summary = {key: value for key, value in payload.items() if key != "tables"}
    detail_hashes = {
        "ablations": sha256_bytes(canonical_json(tables["ablations"]).encode("utf-8")),
        "identities": sha256_bytes(canonical_json(tables["identities"]).encode("utf-8")),
        "information": sha256_bytes(canonical_json(tables["information"]).encode("utf-8")),
        "structural_orbits": sha256_bytes(canonical_json(tables["structural_orbits"]).encode("utf-8")),
        "truth_tables": sha256_bytes(canonical_json(tables["truth_tables"]).encode("utf-8")),
        "weighted_systems": sha256_bytes(canonical_json(tables["weighted_systems"]).encode("utf-8")),
    }
    summary["detail_sha256"] = detail_hashes
    body = dict(summary)
    body["payload_sha256"] = sha256_bytes(canonical_json(summary).encode("utf-8"))
    atomic_write_json(reports / "generation-008d-round-d0-tables.json", body)
    table_dir = reports / "tables"
    atomic_write_json(table_dir / "generation-008d-structural-orbits.json", tables["structural_orbits"])
    atomic_write_json(table_dir / "generation-008d-weighted-systems.json", tables["weighted_systems"])
    atomic_write_json(table_dir / "generation-008d-information.json", tables["information"])
    atomic_write_json(table_dir / "generation-008d-ablations.json", tables["ablations"])
    atomic_write_json(table_dir / "generation-008d-identities.json", tables["identities"])
    truth_lines = "".join(canonical_json(row) + "\n" for row in tables["truth_tables"])
    atomic_write_text(table_dir / "generation-008d-truth-tables.jsonl", truth_lines)
    atomic_write_text(
        table_dir / "generation-008d-structural-orbits.csv",
        _csv(
            tables["structural_orbits"],
            [
                "orbit_id",
                "orbit_size",
                "canonical_rules",
                "action_relation",
                "direction_relation",
                "gate_relation",
                "polarity_relation",
                "composition_family",
                "incidence_matrix",
            ],
        ),
    )
    atomic_write_text(
        table_dir / "generation-008d-weighted-systems.csv",
        _csv(
            tables["weighted_systems"],
            [
                "system_id",
                "structural_orbit_id",
                "weights",
                "canonical_weighted_rules",
                "effective_gate_dimension",
                "minimal_coordinate_count",
                "distinct_local_law_rows",
                "reducibility_class",
                "composition_family",
                "local_law_class",
            ],
        ),
    )
    return {"payload_sha256": body["payload_sha256"], **detail_hashes}
