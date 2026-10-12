"""Generation 8 trajectory atlas.

Mode B records what an N=4 independent hypergraph does when a visible
pair organisation is held as the start and the hidden triad configuration
varies. The sampler is the existing integer-weight toggle kernel. Nothing
in this module rewards a destination, a residence, or an entropy.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import platform
import random
import re
from collections import Counter
from collections.abc import Iterable, Iterator
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.state import permutations, relation_slots, relabel_relation_state
from rs_constraint_lab.weights import alphabet_factors

EXPERIMENT_ID = "generation-008-open-relational-exploration"
RUNNER_VERSION = "generation-008-trajectory/v1"
SEED_FUNCTION = "sha256-u64-v1"
SEED_FIELDS = (
    "experiment_id",
    "round_id",
    "system_id",
    "source_graph_class",
    "hidden_context_orbit_id",
    "replicate_index",
)
FINITE_GRADES = ("strong_suppress", "weak_suppress", "weak_favour", "strong_favour")
PAIR_SLOTS = 6
N_SLOTS = 10
PAIR_HORIZON = 512
FULL_EVENT_CAP = 16384
REPLICATES = 16
CHECKPOINTS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512)
EVENT_FIELDS = (
    "t",
    "pre",
    "post",
    "slot",
    "kind",
    "pair_index",
    "full_index",
    "draw",
    "norm",
    "uniform_draw",
    "selected_weight",
    "selected_integer",
    "probability",
    "weight_hash",
    "weights",
    "rules",
    "pair_before",
    "pair_after",
    "triad_before",
    "triad_after",
    "context_before",
    "context_after",
    "rng_token",
)
ATTENTION_COORDINATES = ("CN", "RD", "RC", "EC", "CG", "CB")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
# Generation 5 reports the four-member tie as one observable inside 1e-8.
MOTIF_TIE = 1e-8
BASELINE_ROLE = "baseline relational dynamics"

LAB_ROOT = Path(__file__).resolve().parents[2]
GEN4_CSV = LAB_ROOT / "reports" / "tables" / "generation-004-n4-higher-order-reconfiguration-singles-n4-k2.csv"
GEN5_CSV = LAB_ROOT / "reports" / "tables" / "generation-005-targeted-tp-pp-pairs-singles-n4-k2.csv"


class FrozenPlanError(RuntimeError):
    """Execution is refused until a matching pushed plan commit is supplied."""


def _lcm(values: list[int]) -> int:
    value = 1
    for item in values:
        value = math.lcm(value, item)
    return value


def _class_index() -> tuple[tuple[str, ...], tuple[int, ...]]:
    table = pair_classes()
    names = tuple(sorted({table.name_of[mask] for mask in range(64)}))
    if len(names) != 11:
        raise RuntimeError(f"expected 11 pair classes, found {len(names)}")
    index = {name: position for position, name in enumerate(names)}
    by_mask = tuple(index[table.name_of[mask]] for mask in range(64))
    return names, by_mask


CLASS_NAMES, CLASS_OF_MASK = _class_index()


def class_name(index: int) -> str:
    return CLASS_NAMES[index]


def mask_class(pair_mask: int) -> int:
    return CLASS_OF_MASK[pair_mask & 63]


def source_masks() -> dict[str, int]:
    """Canonical labelled representative of each 3-edge class.

    The representative is the minimum mask in the S4 orbit, which is the
    representative already stored by PairClassTable. The three classes are
    recognised by degree, triangle, and component structure.
    """
    table = pair_classes()
    found: dict[str, int] = {}
    for mask, desc in table.by_mask.items():
        if desc["edge_count"] != 3:
            continue
        degrees = tuple(desc["degree_multiset"])
        if degrees == (3, 1, 1, 1) and desc["triangle_count"] == 0 and desc["component_count"] == 1:
            found["star"] = mask
        elif degrees == (2, 2, 1, 1) and desc["triangle_count"] == 0 and desc["component_count"] == 1:
            found["path"] = mask
        elif degrees == (2, 2, 2, 0) and desc["triangle_count"] == 1 and desc["component_count"] == 2:
            found["triangle"] = mask
    if set(found) != {"star", "path", "triangle"}:
        raise RuntimeError(f"3-edge source classes drifted: {found}")
    return found


def _slots():
    return tuple(relation_slots(4, 3))


def pair_automorphisms(pair_mask: int) -> list[tuple[int, ...]]:
    pair_slots = _slots()[:PAIR_SLOTS]
    return [
        perm
        for perm in permutations(4)
        if relabel_relation_state(pair_mask, perm, pair_slots) == pair_mask
    ]


def _orbit_members(pair_mask: int) -> tuple[list[tuple[int, ...]], int]:
    slots = _slots()
    autos = pair_automorphisms(pair_mask)
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
        for perm in autos:
            image = relabel_relation_state(state, perm, slots)
            if (image & 63) != pair_mask:
                raise RuntimeError("a pair-graph automorphism moved the pair graph")
            union(triad, image >> PAIR_SLOTS)
    groups: dict[int, list[int]] = {}
    for triad in range(16):
        groups.setdefault(find(triad), []).append(triad)
    members = [tuple(sorted(group)) for group in groups.values()]
    members.sort()
    return members, len(autos)


def enumerate_hidden_contexts() -> dict[str, dict]:
    """One orbit record per stabiliser class of each fixed source graph.

    The symmetry is the automorphism group of that labelled pair graph.
    Full S4 canonicalisation is intentionally not used: it would erase
    distinct hidden contexts of the same visible graph.
    """
    table = pair_classes()
    masks = source_masks()
    sources = {}
    for key in ("star", "path", "triangle"):
        mask = masks[key]
        members, autos = _orbit_members(mask)
        if sum(len(group) for group in members) != 16:
            raise RuntimeError(f"{key} orbit sizes do not cover 16 triad configurations")
        descriptor = table.by_mask[table.class_of[mask]]
        orbits = []
        for position, group in enumerate(members):
            orbits.append(
                {
                    "automorphism_group_size": autos,
                    "canonical_pair_mask": mask,
                    "canonical_triad": group[0],
                    "class_name": descriptor["name"],
                    "hidden_context_orbit_id": f"{key}-o{position:02d}",
                    "members": list(group),
                    "orbit_size": len(group),
                    "source_graph_class": key,
                    "start_state": mask | (group[0] << PAIR_SLOTS),
                }
            )
        sources[key] = {
            "automorphism_group_size": autos,
            "canonical_pair_mask": mask,
            "class_index": mask_class(mask),
            "class_name": descriptor["name"],
            "orbit_count": len(orbits),
            "orbits": orbits,
            "source_graph_class": key,
        }
    return sources


def three_edge_indexes(sources: dict[str, dict] | None = None) -> dict[str, int]:
    chosen = sources if sources is not None else enumerate_hidden_contexts()
    return {key: record["class_index"] for key, record in chosen.items()}


def _structural(expression: str) -> str:
    left, separator, _weight = expression.rpartition(" => ")
    if not separator:
        raise ValueError(f"expression has no weight: {expression}")
    return left


def _regrade(expression: str, grade: str) -> str:
    left = _structural(expression)
    return f"{left} => {grade}"


def derive_tp_archetypes(csv_path: Path | None = None) -> list[str]:
    path = GEN4_CSV if csv_path is None else csv_path
    forms = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["cross_order_class"] != "T->P":
                continue
            forms.add(_structural(row["expression"]))
    return sorted(forms)


def derive_pp_archetypes(csv_path: Path | None = None) -> list[str]:
    path = GEN4_CSV if csv_path is None else csv_path
    forms = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["cross_order_class"] != "P->P":
                continue
            forms.add(_structural(row["expression"]))
    return sorted(forms)


def derive_composite_anchor(csv_path: Path | None = None) -> dict:
    """Lexicographically smallest pair id inside the Generation 5 tie.

    The tie is the disjoint prohibit/prohibit family whose path-to-matching
    interaction sits within 1e-8 of the maximum, the floor stated by the
    Generation 5 report. Round 0 instantiates both rules at strong_suppress.
    """
    path = GEN5_CSV if csv_path is None else csv_path
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["action_edge_relation"] != "disjoint":
                continue
            if not row["pp"].endswith("=> prohibit") or not row["tp"].endswith("=> prohibit"):
                continue
            rows.append(row)
    if not rows:
        raise RuntimeError("no disjoint prohibit pairs in the Generation 5 table")
    best = max(float(row["path_to_matching.I_interaction"]) for row in rows)
    tied = [
        row
        for row in rows
        if abs(float(row["path_to_matching.I_interaction"]) - best) <= MOTIF_TIE
    ]
    tied.sort(key=lambda row: row["pair_id"])
    chosen = tied[0]
    return {
        "grade": "strong_suppress",
        "pair_id": chosen["pair_id"],
        "path_to_matching_I": chosen["path_to_matching.I_interaction"],
        "pp_expression": _regrade(chosen["pp"], "strong_suppress"),
        "pp_source_expression": chosen["pp"],
        "selection_rule": (
            "disjoint action, both source weights prohibit, "
            "path_to_matching.I_interaction within 1e-8 of the maximum, "
            "lexicographically smallest pair_id"
        ),
        "tie_pair_ids": [row["pair_id"] for row in tied],
        "tp_expression": _regrade(chosen["tp"], "strong_suppress"),
        "tp_source_expression": chosen["tp"],
    }


def build_round0_systems() -> list[dict]:
    forms = derive_tp_archetypes()
    anchor = derive_composite_anchor()
    systems = [
        {
            "expressions": [],
            "role": BASELINE_ROLE,
            "source": "unconstrained toggle kernel",
            "system_id": "S00",
        }
    ]
    for position, form in enumerate(forms, start=1):
        systems.append(
            {
                "expressions": [f"{form} => strong_suppress"],
                "role": "tp_structural_archetype",
                "source": "generation-004 T->P structural orbit",
                "structural_expression": form,
                "system_id": f"S{position:02d}",
            }
        )
    systems.append(
        {
            "expressions": [anchor["pp_expression"], anchor["tp_expression"]],
            "pair_id": anchor["pair_id"],
            "role": "composite_anchor",
            "source": "generation-005 disjoint prohibit motif, regraded to strong_suppress",
            "system_id": f"S{len(forms) + 1:02d}",
            "tie_pair_ids": anchor["tie_pair_ids"],
        }
    )
    return systems


def derive_seed(fields: dict) -> int:
    payload = {key: fields[key] for key in SEED_FIELDS}
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def episode_identity(fields: dict) -> dict:
    return {key: fields[key] for key in SEED_FIELDS}


def episode_id_for(fields: dict) -> str:
    return sha256_bytes(canonical_json(episode_identity(fields)).encode("utf-8"))[:24]


def plan_hash(document: dict) -> str:
    body = {key: value for key, value in document.items() if key != "plan_hash"}
    return sha256_bytes(canonical_json(body).encode("utf-8"))


def attention_vector(scores: dict) -> dict:
    if set(scores) != set(ATTENTION_COORDINATES):
        raise ValueError("an attention vector has exactly the six named coordinates")
    rendered = {}
    for key in ATTENTION_COORDINATES:
        value = scores[key]
        if type(value) is not int or value < 0 or value > 5:
            raise ValueError(f"{key} must be an ordinal 0–5")
        rendered[key] = value
    return rendered


def _flip_condition(expression: str, condition_index: int) -> str:
    left = _structural(expression)
    weight = expression.rpartition(" => ")[2]
    head, separator, conditions = left.partition(" | ")
    if not separator:
        raise ValueError("polarity flip requires an existing condition")
    parts = [part.strip() for part in conditions.split("&")]
    if condition_index < 0 or condition_index >= len(parts):
        raise ValueError("condition index is outside the expression")
    part = parts[condition_index]
    if part.startswith("present("):
        parts[condition_index] = "absent(" + part[len("present("):]
    elif part.startswith("absent("):
        parts[condition_index] = "present(" + part[len("absent("):]
    else:
        raise ValueError("polarity flip applies to a present/absent literal")
    return f"{head} | " + " & ".join(parts) + f" => {weight}"


def apply_operator(system: dict, operator: dict, *, tp_forms: list[str], pp_forms: list[str]) -> dict:
    """Bounded perturbation. The result is a new system record, not a reward."""
    kind = operator["op"]
    expressions = list(system["expressions"])
    if kind == "weight_shift":
        grade = operator["grade"]
        if grade not in FINITE_GRADES:
            raise ValueError("weight_shift does not introduce prohibit")
        expressions[operator["rule_index"]] = _regrade(expressions[operator["rule_index"]], grade)
    elif kind == "condition_polarity_flip":
        expressions[operator["rule_index"]] = _flip_condition(
            expressions[operator["rule_index"]], int(operator.get("condition_index", 0))
        )
    elif kind == "structural_tp_neighbour":
        target = operator["structural_expression"]
        if target not in tp_forms:
            raise ValueError("structural neighbour is outside the canonical T->P set")
        replaced = False
        for index, expression in enumerate(expressions):
            if _structural(expression) in tp_forms:
                weight = expression.rpartition(" => ")[2]
                expressions[index] = f"{target} => {weight}"
                replaced = True
                break
        if not replaced:
            raise ValueError("the system has no T->P rule to replace")
    elif kind == "add_pp_companion":
        form = operator["structural_expression"]
        if form not in pp_forms:
            raise ValueError("P->P companion is outside the Generation 4 canonical set")
        if len(expressions) >= 2:
            raise ValueError("Generation 8 keeps at most two rules")
        grade = operator.get("grade", "strong_suppress")
        if grade not in FINITE_GRADES:
            raise ValueError("add_pp_companion does not introduce prohibit")
        expressions.append(f"{form} => {grade}")
    elif kind == "remove_rule":
        if len(expressions) != 2:
            raise ValueError("remove_rule applies to a two-rule system")
        del expressions[int(operator["rule_index"])]
    else:
        raise ValueError(f"operator {kind} is not in the Generation 8 set")
    return {
        "expressions": expressions,
        "operator": operator,
        "parent_system_id": system["system_id"],
        "role": "perturbation",
        "system_id": operator["system_id"],
    }


def _compiled(expressions: list[str]):
    rules = tuple(parse_expression(expression, 4, order=3) for expression in expressions)
    return rules, alphabet_factors("W4")


def _context_label(state: int, cache: dict[int, tuple[tuple[int, ...], tuple[int, ...]]]) -> str:
    """Orbit of the current triad under the labelled pair graph's automorphisms.

    The label is ``p{mask}-t{canonical}-s{size}``. It is a name for the orbit.
    The raw full state remains the ground truth.
    """
    pair_mask = state & 63
    triad = (state >> PAIR_SLOTS) & 15
    canonical, sizes = cache[pair_mask]
    return f"p{pair_mask:02d}-t{canonical[triad]:02d}-s{sizes[triad]}"


def _dynamic_cache() -> dict[int, tuple[tuple[int, ...], tuple[int, ...]]]:
    cache = {}
    for mask in range(64):
        members, _autos = _orbit_members(mask)
        canonical = [0] * 16
        sizes = [0] * 16
        for group in members:
            for triad in group:
                canonical[triad] = group[0]
                sizes[triad] = len(group)
        cache[mask] = (tuple(canonical), tuple(sizes))
    return cache


_DYNAMIC_CACHE: dict | None = None


def dynamic_cache() -> dict[int, tuple[tuple[int, ...], tuple[int, ...]]]:
    """Process-wide orbit table. Replay must not rebuild it per episode."""
    global _DYNAMIC_CACHE
    if _DYNAMIC_CACHE is None:
        _DYNAMIC_CACHE = _dynamic_cache()
    return _DYNAMIC_CACHE


def _encode_rng(generator: random.Random) -> dict:
    version, state, gauss = generator.getstate()
    return {"gauss": gauss, "state": list(state), "version": version}


def _decode_rng(payload: dict) -> random.Random:
    generator = random.Random()
    generator.setstate((payload["version"], tuple(payload["state"]), payload["gauss"]))
    return generator


def _weights(state: int, rules, factors) -> list[Fraction]:
    weights = [Fraction(1) for _ in range(N_SLOTS)]
    for rule in rules:
        for slot in range(N_SLOTS):
            if rule.matches(state, slot):
                weights[slot] *= factors[rule.weight]
    return weights


def _integer_weights(weights: list[Fraction]) -> tuple[list[int], int]:
    common = _lcm([weight.denominator for weight in weights]) if weights else 1
    integer = [int(weight * common) for weight in weights]
    return integer, sum(integer)


def _select(draw: int, integer_weights: list[int]) -> int:
    cumulative = 0
    for slot, weight in enumerate(integer_weights):
        cumulative += weight
        if draw < cumulative:
            return slot
    raise RuntimeError("integer selection did not land in the weight table")


def _event_record(
    *,
    t: int,
    pre: int,
    post: int,
    slot: int,
    kind: str,
    pair_index: int | None,
    draw: int,
    norm: int,
    weights: list[Fraction],
    integer_weights: list[int],
    rules: list[int],
    pair_before: int,
    pair_after: int,
    triad_before: int,
    triad_after: int,
    context_before: str,
    context_after: str,
) -> dict:
    rendered = [f"{weight.numerator}/{weight.denominator}" for weight in weights]
    selected = integer_weights[slot]
    return {
        "context_after": context_after,
        "context_before": context_before,
        "draw": draw,
        "full_index": t,
        "kind": kind,
        "norm": norm,
        "pair_after": pair_after,
        "pair_before": pair_before,
        "pair_index": pair_index,
        "post": post,
        "pre": pre,
        "probability": f"{selected}/{norm}",
        "rng_token": f"{SEED_FUNCTION}:{t}",
        "rules": rules,
        "selected_integer": selected,
        "selected_weight": rendered[slot],
        "slot": slot,
        "t": t,
        "triad_after": triad_after,
        "triad_before": triad_before,
        "uniform_draw": f"{draw}/{norm}",
        "weight_hash": sha256_bytes(",".join(rendered).encode("utf-8")),
        "weights": rendered,
    }


def _rolling(previous: str, event: dict) -> str:
    return sha256_bytes(f"{previous}\n{canonical_json(event)}".encode("utf-8"))


def run_episode(
    *,
    experiment_id: str,
    round_id: str,
    system: dict,
    context: dict,
    replicate: int,
    pair_horizon: int,
    full_event_cap: int,
    plan_hash_value: str,
    frozen_plan_commit: str,
    resume: dict | None = None,
    pair_epoch_limit: int | None = None,
    cache: dict | None = None,
    stall_seconds: float | None = None,
) -> dict:
    if stall_seconds:
        import time

        time.sleep(stall_seconds)
    identity = {
        "experiment_id": experiment_id,
        "hidden_context_orbit_id": context["hidden_context_orbit_id"],
        "replicate_index": replicate,
        "round_id": round_id,
        "source_graph_class": context["source_graph_class"],
        "system_id": system["system_id"],
    }
    seed = derive_seed(identity)
    episode_id = episode_id_for(identity)
    rules, factors = _compiled(list(system.get("expressions") or []))
    dynamic = cache if cache is not None else dynamic_cache()
    if resume is None:
        state = int(context["start_state"])
        generator = random.Random(seed)
        full_events = 0
        pair_events = 0
        rolling = sha256_bytes(
            canonical_json({"initial_state": state, "seed": seed}).encode("utf-8")
        )
        segment_origin = 0
    else:
        state = int(resume["state"])
        generator = _decode_rng(resume["rng_state"])
        full_events = int(resume["full_events"])
        pair_events = int(resume["pair_events"])
        rolling = resume["rolling_hash"]
        segment_origin = pair_events
        seed = int(resume["seed"])
        episode_id = resume["episode_id"]
    events = []
    reason = None
    while True:
        if pair_events >= pair_horizon:
            reason = "pair_horizon"
            break
        if full_events >= full_event_cap:
            reason = "full_event_cap"
            break
        if pair_epoch_limit is not None and pair_events >= segment_origin + pair_epoch_limit:
            reason = "segment_boundary"
            break
        weights = _weights(state, rules, factors)
        integer, total = _integer_weights(weights)
        if total == 0:
            reason = "no_admissible_event"
            break
        draw = generator.randrange(total)
        slot = _select(draw, integer)
        kind = "dissolve" if ((state >> slot) & 1) else "form"
        post = state ^ (1 << slot)
        active = [index for index, rule in enumerate(rules) if rule.matches(state, slot)]
        pair_index = pair_events if slot < PAIR_SLOTS else None
        event = _event_record(
            t=full_events,
            pre=state,
            post=post,
            slot=slot,
            kind=kind,
            pair_index=pair_index,
            draw=draw,
            norm=total,
            weights=weights,
            integer_weights=integer,
            rules=active,
            pair_before=mask_class(state),
            pair_after=mask_class(post),
            triad_before=(state >> PAIR_SLOTS) & 15,
            triad_after=(post >> PAIR_SLOTS) & 15,
            context_before=_context_label(state, dynamic),
            context_after=_context_label(post, dynamic),
        )
        rolling = _rolling(rolling, event)
        events.append(event)
        state = post
        full_events += 1
        if slot < PAIR_SLOTS:
            pair_events += 1
    payload = "".join(canonical_json(event) + "\n" for event in events).encode("utf-8")
    summary = summarize_episode(
        events,
        initial_state=int(context["start_state"]) if resume is None else int(resume.get("initial_state", context["start_state"])),
        source_index=int(context["class_index"]),
        three_edge=three_edge_indexes(),
    )
    if resume is not None:
        # A segment summary describes only its own events. The caller combines them.
        summary = summarize_episode(
            events,
            initial_state=int(resume["segment_initial_state"]),
            source_index=mask_class(int(resume["segment_initial_state"])),
            three_edge=three_edge_indexes(),
        )
    summary["orbit_size"] = int(context["orbit_size"])
    header = {
        "constraint_system_hash": sha256_bytes(
            canonical_json(list(system.get("expressions") or [])).encode("utf-8")
        ),
        "episode_id": episode_id,
        "event_count": len(events),
        "event_payload_sha256": sha256_bytes(payload),
        "experiment_id": experiment_id,
        "final_state": state,
        "final_state_hash": sha256_bytes(canonical_json({"state": state}).encode("utf-8")),
        "frozen_plan_commit": frozen_plan_commit,
        "full_event_cap": full_event_cap,
        "hidden_context_orbit_id": context["hidden_context_orbit_id"],
        "initial_state": int(context["start_state"]) if resume is None else int(resume["initial_state"]),
        "initial_state_hash": sha256_bytes(
            canonical_json(
                {"state": int(context["start_state"]) if resume is None else int(resume["initial_state"])}
            ).encode("utf-8")
        ),
        "pair_event_count": pair_events if resume is None else int(resume["pair_events"]) + sum(1 for event in events if event["pair_index"] is not None),
        "pair_horizon": pair_horizon,
        "plan_hash": plan_hash_value,
        "python_version": platform.python_version(),
        "replicate_index": replicate,
        "round_id": round_id,
        "runner_version": RUNNER_VERSION,
        "seed": seed,
        "seed_function": SEED_FUNCTION,
        "source_graph_class": context["source_graph_class"],
        "spec_hash": plan_hash_value,
        "system_id": system["system_id"],
        "termination_reason": reason,
        "trajectory_hash": rolling,
    }
    cursor = {
        "episode_id": episode_id,
        "full_events": full_events if resume is None else int(resume["full_events"]) + len(events),
        "initial_state": header["initial_state"],
        "pair_events": header["pair_event_count"],
        "rng_state": _encode_rng(generator),
        "rolling_hash": rolling,
        "seed": seed,
        "segment_initial_state": state,
        "state": state,
    }
    return {
        "cursor": cursor,
        "events": events,
        "header": header,
        "payload": payload,
        "summary": summary,
    }


def run_chained(
    *,
    segment_pair_epochs: int,
    experiment_id: str,
    round_id: str,
    system: dict,
    context: dict,
    replicate: int,
    pair_horizon: int,
    full_event_cap: int,
    plan_hash_value: str,
    frozen_plan_commit: str,
    cache: dict | None = None,
) -> dict:
    """Segmented execution. The concatenated stream matches one process."""
    dynamic = cache if cache is not None else dynamic_cache()
    collected = []
    resume = None
    final = None
    while True:
        final = run_episode(
            experiment_id=experiment_id,
            round_id=round_id,
            system=system,
            context=context,
            replicate=replicate,
            pair_horizon=pair_horizon,
            full_event_cap=full_event_cap,
            plan_hash_value=plan_hash_value,
            frozen_plan_commit=frozen_plan_commit,
            resume=resume,
            pair_epoch_limit=segment_pair_epochs,
            cache=dynamic,
        )
        collected.extend(final["events"])
        if final["header"]["termination_reason"] != "segment_boundary":
            break
        resume = dict(final["cursor"])
        resume["initial_state"] = int(context["start_state"])
    single_summary = summarize_episode(
        collected,
        initial_state=int(context["start_state"]),
        source_index=int(context["class_index"]),
        three_edge=three_edge_indexes(),
    )
    rolling = sha256_bytes(
        canonical_json({"initial_state": int(context["start_state"]), "seed": derive_seed({
            "experiment_id": experiment_id,
            "hidden_context_orbit_id": context["hidden_context_orbit_id"],
            "replicate_index": replicate,
            "round_id": round_id,
            "source_graph_class": context["source_graph_class"],
            "system_id": system["system_id"],
        })}).encode("utf-8")
    )
    for event in collected:
        rolling = _rolling(rolling, event)
    payload = "".join(canonical_json(event) + "\n" for event in collected).encode("utf-8")
    final["events"] = collected
    final["payload"] = payload
    final["summary"] = single_summary
    final["header"]["event_count"] = len(collected)
    final["header"]["event_payload_sha256"] = sha256_bytes(payload)
    final["header"]["final_state"] = collected[-1]["post"] if collected else int(context["start_state"])
    final["header"]["pair_event_count"] = single_summary["pair_event_count"]
    final["header"]["trajectory_hash"] = rolling
    final["header"]["final_state_hash"] = sha256_bytes(
        canonical_json({"state": final["header"]["final_state"]}).encode("utf-8")
    )
    return final


def episode_row(result: dict) -> dict:
    """Header plus summary. Route labels inside the summary are not authoritative."""
    row = dict(result["summary"])
    header = result["header"]
    row.update(
        {
            "episode_id": header["episode_id"],
            "frozen_plan_commit": header["frozen_plan_commit"],
            "hidden_context_orbit_id": header["hidden_context_orbit_id"],
            "replicate_index": header["replicate_index"],
            "seed": header["seed"],
            "source_graph_class": header["source_graph_class"],
            "system_id": header["system_id"],
            "termination_reason": header["termination_reason"],
            "trajectory_hash": header["trajectory_hash"],
        }
    )
    stamped = []
    for marker in row.get("markers") or []:
        stamped.append(
            {
                **marker,
                "episode_id": header["episode_id"],
                "hidden_context_orbit_id": header["hidden_context_orbit_id"],
                "source_graph_class": header["source_graph_class"],
                "system_id": header["system_id"],
            }
        )
    row["markers"] = stamped
    return row


def expand_runs(runs: list[list[int]]) -> list[int]:
    sequence = []
    for class_index, length in runs:
        sequence.extend([class_index] * int(length))
    return sequence


def summarize_episode(events: list[dict], *, initial_state: int, source_index: int, three_edge: dict[str, int]) -> dict:
    pair_sequence = [mask_class(initial_state)]
    edge_sequence = [(initial_state & 63).bit_count()]
    triad_sequence = [((initial_state >> PAIR_SLOTS) & 15).bit_count()]
    matrix = [[0 for _ in range(11)] for _ in range(11)]
    full_counts: Counter[int] = Counter([initial_state])
    pair_state_counts: Counter[int] = Counter([initial_state & 63])
    triad_only = 0
    class_changes = []
    last_change_pair = 0
    context_changes = 0
    triad_transitions = 0
    for event in events:
        full_counts[event["post"]] += 1
        if event["slot"] >= PAIR_SLOTS:
            triad_only += 1
            triad_transitions += 1
            continue
        matrix[event["pair_before"]][event["pair_after"]] += 1
        pair_sequence.append(event["pair_after"])
        edge_sequence.append((event["post"] & 63).bit_count())
        triad_sequence.append(event["triad_after"].bit_count())
        pair_state_counts[event["post"] & 63] += 1
        if event["context_before"] != event["context_after"]:
            context_changes += 1
        if event["pair_before"] != event["pair_after"]:
            pair_index = int(event["pair_index"])
            class_changes.append(
                {
                    "context_after": event["context_after"],
                    "context_before": event["context_before"],
                    "full_index": event["full_index"],
                    "kind": event["kind"],
                    "pair_after": event["pair_after"],
                    "pair_before": event["pair_before"],
                    "pair_epochs_since_previous_change": pair_index - last_change_pair,
                    "pair_index": pair_index,
                    "post": event["post"],
                    "pre": event["pre"],
                    "rules": list(event["rules"]),
                    "slot": event["slot"],
                    "triad_after": event["triad_after"],
                    "triad_before": event["triad_before"],
                }
            )
            last_change_pair = pair_index
    runs: list[list[int]] = []
    for class_index in pair_sequence:
        if not runs or runs[-1][0] != class_index:
            runs.append([class_index, 1])
        else:
            runs[-1][1] += 1
    occupancy = [0] * 11
    for class_index, length in runs:
        occupancy[class_index] += length
    first_entry = {str(index): None for index in range(11)}
    cursor = 0
    for class_index, length in runs:
        if first_entry[str(class_index)] is None:
            first_entry[str(class_index)] = cursor
        cursor += length
    return_times = []
    cursor = 0
    for position, (class_index, length) in enumerate(runs):
        if position == 0:
            cursor += length
            continue
        if class_index == source_index and runs[position - 1][0] != source_index:
            return_times.append(cursor)
        cursor += length
    route = route_from_runs(runs, source_index, set(three_edge.values()), len(pair_sequence) - 1)
    distinct_full = len(full_counts)
    distinct_pair_states = len(pair_state_counts)
    return {
        "class_changes": len(class_changes),
        "class_runs": runs,
        "context_label_changes": context_changes,
        "distinct_full_states": distinct_full,
        "distinct_pair_classes": sum(1 for count in occupancy if count),
        "distinct_pair_states": distinct_pair_states,
        "edge_count_sequence": edge_sequence,
        "final_pair_class": CLASS_NAMES[pair_sequence[-1]],
        "final_triad": events[-1]["triad_after"] if events else ((initial_state >> PAIR_SLOTS) & 15),
        "first_entry_pair_epoch": first_entry,
        "full_state_entropy": _entropy(full_counts.values()),
        "full_state_revisits": sum(full_counts.values()) - distinct_full,
        "initial_source_residence": runs[0][1] if runs else 0,
        "initial_triad": (initial_state >> PAIR_SLOTS) & 15,
        "markers": class_changes,
        "pair_class_entropy": _entropy(occupancy),
        "pair_class_occupancy": occupancy,
        "pair_event_count": len(pair_sequence) - 1,
        "pair_state_revisits": sum(pair_state_counts.values()) - distinct_pair_states,
        "return_times": return_times,
        "route": route,
        "source_returns": len(return_times),
        "transition_counts": [cell for row in matrix for cell in row],
        "triad_count_sequence": triad_sequence,
        "triad_only_events": triad_only,
        "triad_only_fraction": (triad_only / len(events)) if events else 0.0,
        "triad_transition_count": triad_transitions,
        "event_count": len(events),
    }


def _entropy(counts) -> float:
    total = sum(counts)
    if total <= 0:
        return 0.0
    value = 0.0
    for count in counts:
        if count:
            probability = count / total
            value -= probability * math.log(probability)
    return value


def route_from_runs(runs: list[list[int]], source_index: int, three_edge: set[int], pair_events: int) -> dict:
    """Route labels are a function of the class runs alone."""
    del pair_events
    if not runs:
        return {
            "destination": "censored_at_horizon",
            "intermediate": [],
            "never_left_source": True,
            "return_before_other_3edge": None,
            "route_outcome": "censored_at_horizon",
            "time_to_next_3edge": None,
        }
    intermediate: list[int] = []
    epoch = 0
    seen_leave = False
    returned = False
    destination = None
    dest_at = None
    for class_index, length in runs:
        if not seen_leave:
            if class_index == source_index:
                epoch += length
                continue
            seen_leave = True
        if class_index in three_edge and class_index != source_index:
            destination = class_index
            dest_at = epoch
            break
        if class_index == source_index:
            returned = True
        intermediate.append(class_index)
        epoch += length
    outcome = "censored_at_horizon" if destination is None else CLASS_NAMES[destination]
    return {
        "destination": outcome,
        "intermediate": [CLASS_NAMES[index] for index in intermediate],
        "never_left_source": not seen_leave,
        "return_before_other_3edge": None if not seen_leave else returned,
        "route_outcome": outcome,
        "time_to_next_3edge": dest_at,
    }


def runs_through(runs: list[list[int]], pair_epoch: int) -> list[list[int]]:
    """Prefix of the run list covering pair epochs 0..pair_epoch inclusive."""
    remaining = pair_epoch + 1
    prefix = []
    for class_index, length in runs:
        if remaining <= 0:
            break
        take = min(length, remaining)
        prefix.append([class_index, take])
        remaining -= take
    return prefix


def replay_events(header: dict, events: list[dict], system: dict, *, initial_state: int) -> dict:
    rules, factors = _compiled(list(system.get("expressions") or []))
    dynamic = dynamic_cache()
    generator = random.Random(int(header["seed"]))
    state = int(initial_state)
    rolling = sha256_bytes(canonical_json({"initial_state": state, "seed": int(header["seed"])}).encode("utf-8"))
    payload = bytearray()
    for event in events:
        weights = _weights(state, rules, factors)
        integer, total = _integer_weights(weights)
        if total == 0:
            return {"field": "norm", "step": event["t"], "verification": "mismatch"}
        draw = generator.randrange(total)
        if draw != event["draw"]:
            return {"field": "draw", "recomputed": draw, "step": event["t"], "stored": event["draw"], "verification": "mismatch"}
        slot = _select(draw, integer)
        if slot != event["slot"] or total != event["norm"]:
            return {"field": "slot", "recomputed": slot, "step": event["t"], "stored": event["slot"], "verification": "mismatch"}
        rendered = [f"{weight.numerator}/{weight.denominator}" for weight in weights]
        digest = sha256_bytes(",".join(rendered).encode("utf-8"))
        if rendered != event["weights"] or digest != event["weight_hash"]:
            return {"field": "weights", "step": event["t"], "verification": "mismatch"}
        post = state ^ (1 << slot)
        if post != event["post"] or state != event["pre"]:
            return {"field": "state", "step": event["t"], "verification": "mismatch"}
        active = [index for index, rule in enumerate(rules) if rule.matches(state, slot)]
        if active != event["rules"]:
            return {"field": "rules", "step": event["t"], "verification": "mismatch"}
        if mask_class(state) != event["pair_before"] or mask_class(post) != event["pair_after"]:
            return {"field": "pair_class", "step": event["t"], "verification": "mismatch"}
        if event["probability"] != f"{integer[slot]}/{total}":
            return {"field": "probability", "step": event["t"], "verification": "mismatch"}
        if event.get("context_before") != _context_label(state, dynamic) or event.get("context_after") != _context_label(post, dynamic):
            return {"field": "context", "step": event["t"], "verification": "mismatch"}
        rolling = _rolling(rolling, event)
        payload.extend(canonical_json(event).encode("utf-8"))
        payload.extend(b"\n")
        state = post
    payload_hash = sha256_bytes(bytes(payload))
    if payload_hash != header.get("event_payload_sha256") and header.get("event_payload_sha256") is not None:
        # Header hash is checked when the caller stored one. A bare unit replay may omit it.
        if "event_payload_sha256" in header and header["event_payload_sha256"] != payload_hash:
            return {"field": "event_payload_sha256", "verification": "mismatch"}
    if header.get("trajectory_hash") not in {None, rolling}:
        return {"field": "trajectory_hash", "recomputed": rolling, "stored": header["trajectory_hash"], "verification": "mismatch"}
    if header.get("final_state") not in {None, state}:
        return {"field": "final_state", "recomputed": state, "stored": header["final_state"], "verification": "mismatch"}
    return {"events": len(events), "final_state": state, "trajectory_hash": rolling, "verification": "exact"}


def select_replay_ids(episode_ids: list[str], fraction: float) -> list[str]:
    ordered = sorted(episode_ids)
    if fraction <= 0 or not ordered:
        return []
    if fraction >= 1:
        return ordered
    chosen = [
        episode_id
        for episode_id in ordered
        if int(hashlib.sha256(episode_id.encode("utf-8")).hexdigest()[:8], 16) % 10 == 0
    ]
    minimum = math.ceil(len(ordered) * fraction)
    if len(chosen) >= minimum:
        return chosen
    for episode_id in sorted(ordered, key=lambda item: hashlib.sha256(item.encode("utf-8")).hexdigest()):
        if episode_id not in chosen:
            chosen.append(episode_id)
        if len(chosen) >= minimum:
            break
    return sorted(chosen)


def _distribution(labels: list[str], weights: list[float] | None = None) -> dict[str, float]:
    totals: dict[str, float] = {}
    for index, label in enumerate(labels):
        weight = 1.0 if weights is None else weights[index]
        totals[label] = totals.get(label, 0.0) + weight
    return totals


def _js(left: dict[str, float], right: dict[str, float]) -> float:
    keys = sorted(set(left) | set(right))
    left_total = sum(left.values()) or 1.0
    right_total = sum(right.values()) or 1.0
    pl = [left.get(key, 0.0) / left_total for key in keys]
    pr = [right.get(key, 0.0) / right_total for key in keys]
    pm = [(a + b) / 2 for a, b in zip(pl, pr)]

    def kl(source, mixture) -> float:
        value = 0.0
        for probability, mixed in zip(source, mixture):
            if probability and mixed:
                value += probability * math.log(probability / mixed)
        return value

    return 0.5 * kl(pl, pm) + 0.5 * kl(pr, pm)


def _mutual_information(by_context: dict[str, dict[str, float]]) -> float | None:
    if len(by_context) < 2:
        return None
    joint = []
    for context, counts in by_context.items():
        for destination, count in counts.items():
            if count:
                joint.append((context, destination, count))
    total = sum(count for _context, _destination, count in joint)
    if total <= 0:
        return None
    dest = Counter()
    ctx = Counter()
    for context, destination, count in joint:
        dest[destination] += count
        ctx[context] += count
    information = 0.0
    for context, destination, count in joint:
        p_xy = count / total
        p_x = ctx[context] / total
        p_y = dest[destination] / total
        information += p_xy * math.log(p_xy / (p_x * p_y))
    return information


def atlas_from_summaries(rows: list[dict], sources: dict[str, dict]) -> dict:
    """Aggregate tables. Route fields on the rows are ignored and recomputed."""
    three_edge = three_edge_indexes(sources)
    enriched = []
    for row in rows:
        route = route_from_runs(
            row["class_runs"],
            sources[row["source_graph_class"]]["class_index"],
            set(three_edge.values()),
            row["pair_event_count"],
        )
        enriched.append({**row, "route_recomputed": route})
    systems = sorted({row["system_id"] for row in enriched})
    matrices = {}
    routing = []
    divergences = []
    information = []
    persistence = []
    residence = []
    for system_id in systems:
        system_rows = [row for row in enriched if row["system_id"] == system_id]
        matrix = [0] * 121
        for row in system_rows:
            for index, count in enumerate(row["transition_counts"]):
                matrix[index] += int(count)
        support = sum(matrix)
        probabilities = []
        for row_index in range(11):
            row_sum = sum(matrix[row_index * 11:(row_index + 1) * 11])
            for column in range(11):
                count = matrix[row_index * 11 + column]
                probabilities.append(None if row_sum == 0 else count / row_sum)
        matrices[system_id] = {
            "counts": matrix,
            "pair_event_support": support,
            "row_normalised": probabilities,
        }
        for source_key, source in sources.items():
            source_rows = [row for row in system_rows if row["source_graph_class"] == source_key]
            by_orbit: dict[str, list[dict]] = {}
            for row in source_rows:
                by_orbit.setdefault(row["hidden_context_orbit_id"], []).append(row)
            orbit_distributions = {}
            weighted_distributions = {}
            for orbit_id, group in sorted(by_orbit.items()):
                labels = [item["route_recomputed"]["route_outcome"] for item in group]
                orbit_distributions[orbit_id] = _distribution(labels)
                weighted_distributions[orbit_id] = _distribution(
                    labels, [float(item["orbit_size"]) for item in group]
                )
                returned = [
                    item["route_recomputed"]["return_before_other_3edge"]
                    for item in group
                    if item["route_recomputed"]["return_before_other_3edge"] is not None
                ]
                times = [
                    item["route_recomputed"]["time_to_next_3edge"]
                    for item in group
                    if item["route_recomputed"]["time_to_next_3edge"] is not None
                ]
                routing.append(
                    {
                        "censored": sum(1 for label in labels if label == "censored_at_horizon"),
                        "destinations": orbit_distributions[orbit_id],
                        "episodes": len(group),
                        "mean_time_to_next_3edge": (sum(times) / len(times)) if times else None,
                        "never_left_source": sum(1 for item in group if item["route_recomputed"]["never_left_source"]),
                        "orbit_id": orbit_id,
                        "orbit_size": group[0]["orbit_size"],
                        "return_before_other_3edge": (sum(bool(item) for item in returned) / len(returned)) if returned else None,
                        "source_graph_class": source_key,
                        "system_id": system_id,
                    }
                )
                residence.append(
                    {
                        "mean_initial_residence": sum(item["initial_source_residence"] for item in group) / len(group),
                        "mean_source_returns": sum(item["source_returns"] for item in group) / len(group),
                        "orbit_id": orbit_id,
                        "source_graph_class": source_key,
                        "system_id": system_id,
                    }
                )
            orbit_ids = sorted(orbit_distributions)
            js_values = []
            for left_index, left in enumerate(orbit_ids):
                for right in orbit_ids[left_index + 1:]:
                    js_values.append(_js(orbit_distributions[left], orbit_distributions[right]))
            divergences.append(
                {
                    "max_js": max(js_values) if js_values else 0.0,
                    "mean_js": (sum(js_values) / len(js_values)) if js_values else 0.0,
                    "source_graph_class": source_key,
                    "system_id": system_id,
                }
            )
            information.append(
                {
                    "configuration_weighted": _mutual_information(weighted_distributions),
                    "episode_equal": _mutual_information(orbit_distributions),
                    "source_graph_class": source_key,
                    "system_id": system_id,
                }
            )
            for checkpoint in CHECKPOINTS:
                checkpoint_distributions = {}
                usable = 0
                for orbit_id, group in by_orbit.items():
                    labels = []
                    for item in group:
                        if item["pair_event_count"] < checkpoint:
                            continue
                        prefix = runs_through(item["class_runs"], checkpoint)
                        outcome = route_from_runs(
                            prefix,
                            source["class_index"],
                            set(three_edge.values()),
                            checkpoint,
                        )["route_outcome"]
                        labels.append(outcome)
                        usable += 1
                    if labels:
                        checkpoint_distributions[orbit_id] = _distribution(labels)
                persistence.append(
                    {
                        "checkpoint": checkpoint,
                        "episodes": usable,
                        "information": _mutual_information(checkpoint_distributions),
                        "source_graph_class": source_key,
                        "system_id": system_id,
                    }
                )
    motifs, motifs_omitted = _motifs(enriched)
    occupancy = {}
    terminations: dict[str, dict[str, int]] = {}
    for system_id in systems:
        system_rows = [row for row in enriched if row["system_id"] == system_id]
        counts = [0] * 11
        triad_sum = 0.0
        triad_n = 0
        reasons: dict[str, int] = {}
        for row in system_rows:
            for index, count in enumerate(row.get("pair_class_occupancy") or []):
                counts[index] += int(count)
            if row.get("triad_only_fraction") is not None:
                triad_sum += float(row["triad_only_fraction"])
                triad_n += 1
            reason = str(row.get("termination_reason"))
            reasons[reason] = reasons.get(reason, 0) + 1
        occupancy[system_id] = {
            "counts": counts,
            "names": list(CLASS_NAMES),
            "triad_only_fraction_mean": (triad_sum / triad_n) if triad_n else None,
        }
        terminations[system_id] = reasons
    return {
        "context_divergences": divergences,
        "context_information": information,
        "context_persistence": persistence,
        "episodes": len(enriched),
        "index_rows": [
            {
                "distinct_pair_classes": row["distinct_pair_classes"],
                "episode_id": row["episode_id"],
                "event_count": row["event_count"],
                "final_pair_class": row["final_pair_class"],
                "full_state_entropy": row["full_state_entropy"],
                "hidden_context_orbit": row["hidden_context_orbit_id"],
                "pair_class_entropy": row["pair_class_entropy"],
                "pair_event_count": row["pair_event_count"],
                "replicate": row["replicate_index"],
                "seed": row["seed"],
                "source_graph_class": row["source_graph_class"],
                "source_returns": row["source_returns"],
                "system_id": row["system_id"],
                "termination_reason": row["termination_reason"],
                "trajectory_hash": row["trajectory_hash"],
            }
            for row in enriched
        ],
        "motif_clock": "pair_class_change",
        "motifs": motifs,
        "motifs_omitted": motifs_omitted,
        "occupancy": occupancy,
        "representatives": representative_episodes(enriched),
        "residence": residence,
        "terminations": terminations,
        "routing": routing,
        "transition_matrices": matrices,
    }


def _motifs(rows: list[dict]) -> tuple[list[dict], int]:
    """Change-compressed class paths. Stays stay in the transition matrix."""
    found: dict[tuple[str, ...], dict] = {}
    for row in rows:
        classes = [CLASS_NAMES[run[0]] for run in row["class_runs"]]
        for length in (2, 3, 4):
            for start in range(0, len(classes) - length + 1):
                key = tuple(classes[start:start + length])
                slot = found.setdefault(
                    key,
                    {"count": 0, "episode_ids": [], "sources": set(), "systems": set()},
                )
                slot["count"] += 1
                slot["systems"].add(row["system_id"])
                slot["sources"].add(f"{row['source_graph_class']}:{row['hidden_context_orbit_id']}")
                if len(slot["episode_ids"]) < 3 and row["episode_id"] not in slot["episode_ids"]:
                    slot["episode_ids"].append(row["episode_id"])
    ranked = sorted(found.items(), key=lambda item: (-item[1]["count"], item[0]))
    retained = []
    for key, slot in ranked[:60]:
        sources = sorted(slot["sources"])
        retained.append(
            {
                "classes": list(key),
                "count": slot["count"],
                "episode_ids": sorted(slot["episode_ids"]),
                "length": len(key),
                "source_contexts": sources[:12],
                "source_contexts_omitted": max(0, len(sources) - 12),
                "systems": sorted(slot["systems"]),
            }
        )
    return retained, max(0, len(ranked) - 60)


def _select_representatives(rows: list[dict], scope: str) -> list[dict]:
    signatures: dict[tuple[str, ...], list[dict]] = {}
    for row in rows:
        signature = tuple(CLASS_NAMES[run[0]] for run in row["class_runs"])
        signatures.setdefault(signature, []).append(row)
    medoid_key = max(signatures, key=lambda key: (len(signatures[key]), key))
    medoid = min(signatures[medoid_key], key=lambda row: row["episode_id"])
    rare_key = min(signatures, key=lambda key: (len(signatures[key]), key))
    rare = min(signatures[rare_key], key=lambda row: row["episode_id"])
    longest = min(rows, key=lambda row: (-row["initial_source_residence"], row["episode_id"]))
    returns = min(rows, key=lambda row: (-row["source_returns"], row["episode_id"]))
    return [
        {"episode_id": medoid["episode_id"], "rule": "medoid_route_signature", "scope": scope, "signature_length": len(medoid_key)},
        {"episode_id": rare["episode_id"], "rule": "earliest_rare_route", "scope": scope, "signature_count": len(signatures[rare_key])},
        {"episode_id": longest["episode_id"], "rule": "longest_source_residence", "residence": longest["initial_source_residence"], "scope": scope},
        {"episode_id": returns["episode_id"], "rule": "highest_source_returns", "scope": scope, "source_returns": returns["source_returns"]},
    ]


def representative_episodes(rows: list[dict]) -> list[dict]:
    """Predeclared selectors. The episode id is the tie break.

    A global selection is always returned. When more than one system is
    present, the same four rules are applied inside each system.
    """
    if not rows:
        return []
    selected = _select_representatives(rows, "global")
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("system_id", "unspecified")), []).append(row)
    if len(grouped) > 1:
        for system_id in sorted(grouped):
            selected.extend(_select_representatives(grouped[system_id], system_id))
    return selected


def transition_counts_from_events(events: list[dict]) -> list[int]:
    matrix = [0] * 121
    for event in events:
        if event["pair_index"] is None:
            continue
        matrix[event["pair_before"] * 11 + event["pair_after"]] += 1
    return matrix


def require_frozen_plan(repo: Path, commit: str | None, relpath: str, disk_path: Path | None = None) -> dict:
    if not commit or not HEX40.fullmatch(commit):
        raise FrozenPlanError("execution refused: a 40-hex frozen plan commit is required")
    import subprocess

    check = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{commit}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        raise FrozenPlanError("execution refused: frozen plan commit is not in this repository")
    ancestor = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", commit, "HEAD"],
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise FrozenPlanError("execution refused: frozen plan commit is not an ancestor of HEAD")
    shown = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{relpath}"],
        capture_output=True,
    )
    if shown.returncode != 0:
        raise FrozenPlanError("execution refused: the plan file is not in the frozen commit")
    committed = json.loads(shown.stdout.decode("utf-8"))
    digest = plan_hash(committed)
    if committed.get("plan_hash") != digest:
        raise FrozenPlanError("execution refused: committed plan_hash does not match the plan body")
    if disk_path is not None:
        disk = json.loads(disk_path.read_text(encoding="utf-8"))
        if plan_hash(disk) != digest:
            raise FrozenPlanError("execution refused: the working plan drifted from the frozen commit")
    return committed


def remote_contains(repo: Path, commit: str) -> bool:
    """True when a remote-tracking ref already contains the plan commit."""
    import subprocess

    shown = subprocess.run(
        ["git", "-C", str(repo), "branch", "-r", "--contains", commit],
        capture_output=True,
        text=True,
    )
    if shown.returncode != 0:
        return False
    return any(line.strip() for line in shown.stdout.splitlines())


def write_stream(path: Path, payload: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = gzip.compress(payload, mtime=0)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)
    return sha256_bytes(raw)


def write_jsonl_gzip(path: Path, lines: Iterable[str]) -> int:
    """Write JSONL into gzip with mtime 0. The iterator is consumed once."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    count = 0
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for line in lines:
                if not line.endswith("\n"):
                    line = line + "\n"
                handle.write(line.encode("utf-8"))
                count += 1
    temporary.replace(path)
    return count


def iter_jsonl_gzip(path: Path) -> Iterator[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def read_stream(path: Path) -> list[dict]:
    return list(iter_jsonl_gzip(path))


def inspect_lines(events: list[dict], limit: int = 40) -> list[str]:
    lines = []
    for event in events[:limit]:
        lines.append(
            f"t={event['t']} {event['kind']} slot={event['slot']} "
            f"{CLASS_NAMES[event['pair_before']]} -> {CLASS_NAMES[event['pair_after']]} "
            f"triad={event['triad_before']}->{event['triad_after']} p={event['probability']} "
            f"draw={event['uniform_draw']} rules={event['rules']}"
        )
    if len(events) > limit:
        lines.append(f"... {len(events) - limit} further events")
    return lines


def query_transitions(markers: Iterable[dict], *, source_class: str | None = None, target_class: str | None = None, orbit_id: str | None = None, system_id: str | None = None, triad_count: int | None = None, motif: list[str] | None = None, episodes: list[dict] | None = None, limit: int = 50) -> list[dict]:
    """Filter transition markers. A class name filters the pair class.

    A source key such as ``path`` filters the episode's source graph.
    A motif filters the change-compressed class path of the episode.
    """
    matched_ids = None
    if motif:
        wanted = tuple(motif)
        matched_ids = set()
        for row in episodes or []:
            classes = [CLASS_NAMES[run[0]] for run in row["class_runs"]]
            for start in range(0, len(classes) - len(wanted) + 1):
                if tuple(classes[start:start + len(wanted)]) == wanted:
                    matched_ids.add(row["episode_id"])
                    break
    class_names = set(CLASS_NAMES)
    chosen = []
    for row in markers:
        if matched_ids is not None and row.get("episode_id") not in matched_ids:
            continue
        if system_id and row.get("system_id") != system_id:
            continue
        if orbit_id and row.get("hidden_context_orbit_id") != orbit_id:
            continue
        if source_class:
            if source_class in class_names:
                if CLASS_NAMES[row["pair_before"]] != source_class:
                    continue
            elif row.get("source_graph_class") != source_class:
                continue
        if target_class and CLASS_NAMES[row["pair_after"]] != target_class:
            continue
        if triad_count is not None and int(row["triad_before"]).bit_count() != triad_count:
            continue
        chosen.append(row)
        if len(chosen) >= limit:
            break
    return chosen
