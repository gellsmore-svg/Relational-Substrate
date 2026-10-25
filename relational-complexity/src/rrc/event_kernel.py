"""Exact one-step kernels for a declared catalogue of events.

The atlas engine is unchanged. This module does not compile a carrier
weight table and is not a frozen round. No intervention operator is defined.

A row with no positive-weight event is completed by a self-loop. That
self-loop is not an event. A no-op is a declared event whose target is its
source. The two records can put probability 1 on the same diagonal cell.
"""

from __future__ import annotations

from fractions import Fraction

METHOD_ID = "event-kernel-0.1.0"
CLOCK = "one_declared_event"
KINDS = ("toggle", "joint", "noop")
MAX_STATES = 16


def _state(value, name: str, n_states: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer state")
    if value < 0 or value >= n_states:
        raise ValueError(f"{name} must be an integer state in 0 .. {n_states - 1}")
    return value


def _weight(value) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("weight must be a nonnegative integer")
    if value < 0:
        raise ValueError("weight must be a nonnegative integer")
    return value


def _event(raw, n_states: int, seen: set[str]) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("an event must be a record")
    name = raw.get("name")
    if not isinstance(name, str) or name == "":
        raise ValueError("an event needs a name")
    if name in seen:
        raise ValueError(f"duplicate event name {name}")
    seen.add(name)
    kind = raw.get("kind")
    if kind not in KINDS:
        raise ValueError("event kind must be toggle, joint, or noop")
    source = _state(raw.get("source"), "source", n_states)
    target = _state(raw.get("target"), "target", n_states)
    weight = _weight(raw.get("weight"))
    if kind == "noop" and target != source:
        raise ValueError("a noop event stays in its source state")
    if kind != "noop" and target == source:
        raise ValueError("a toggle or joint event changes the state")
    return {
        "name": name,
        "kind": kind,
        "source": source,
        "target": target,
        "weight": weight,
    }


def kernel(n_states: int, events: list) -> dict:
    """Aggregate declared events and normalise each row with ``Fraction``.

    Events that share a source and a target add their positive weights.
    A weight of 0 contributes nothing. Event order does not change the sums.
    """
    if isinstance(n_states, bool) or not isinstance(n_states, int) or n_states < 1:
        raise ValueError("n_states must be a positive integer")
    if n_states > MAX_STATES:
        raise ValueError(f"n_states must be at most {MAX_STATES}")
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    seen: set[str] = set()
    parsed = [_event(raw, n_states, seen) for raw in events]
    aggregated = [[0 for _ in range(n_states)] for _ in range(n_states)]
    enabled = [0 for _ in range(n_states)]
    noop_mass = [0 for _ in range(n_states)]
    for event in parsed:
        if event["weight"] == 0:
            continue
        aggregated[event["source"]][event["target"]] += event["weight"]
        enabled[event["source"]] += 1
        if event["kind"] == "noop":
            noop_mass[event["source"]] += event["weight"]
    probabilities = []
    completions = []
    row_sums = []
    for state in range(n_states):
        total = sum(aggregated[state])
        row_sums.append(total)
        if total == 0:
            row = [Fraction(0) for _ in range(n_states)]
            row[state] = Fraction(1)
            completions.append("halt_self_loop")
        else:
            row = [Fraction(aggregated[state][target], total) for target in range(n_states)]
            if noop_mass[state] == total:
                completions.append("noop_event")
            elif noop_mass[state] > 0:
                completions.append("normalised_events_including_noop")
            else:
                completions.append("normalised_events")
        probabilities.append(row)
    return {
        "method": METHOD_ID,
        "clock": CLOCK,
        "n_states": n_states,
        "halt_self_loop_is_event": False,
        "aggregated_weights": aggregated,
        "row_sums": row_sums,
        "enabled_event_counts": enabled,
        "completions": completions,
        "probabilities": probabilities,
    }


def single_toggle_catalogue(rows: list) -> list[dict]:
    """One toggle event per bit of each mask. The row length is the width.

    The catalogue has one row for every mask of that width. A zero weight
    stays in the list and adds no transition.
    """
    if not isinstance(rows, list) or not rows:
        raise ValueError("rows must be a nonempty list")
    width = len(rows[0])
    if isinstance(width, bool) or width < 1 or any(len(row) != width for row in rows):
        raise ValueError("each row needs the same positive width")
    if len(rows) != (1 << width):
        raise ValueError("a single-toggle catalogue has one row per mask")
    events = []
    for state, row in enumerate(rows):
        for bit, weight in enumerate(row):
            events.append(
                {
                    "name": f"toggle-{state}-{bit}",
                    "kind": "toggle",
                    "source": state,
                    "target": state ^ (1 << bit),
                    "weight": weight,
                }
            )
    return events
