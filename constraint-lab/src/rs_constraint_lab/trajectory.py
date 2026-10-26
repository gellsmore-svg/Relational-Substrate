"""Event-sourced trajectories.

Selection uses integer weights and ``random.Random.randrange``, which is
Python's MT19937. The stored draw is the integer consumed from that generator,
so replay compares the regenerated event list with the stored list.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from fractions import Fraction

from rs_constraint_lab.constraints import Constraint
from rs_constraint_lab.kernel import Kernel
from rs_constraint_lab.version import ENGINE_VERSION

PRNG_NAME = "python-random-MT19937"
SELECTION = "integer-weights-randrange"


def _lcm(values: list[int]) -> int:
    value = 1
    for item in values:
        value = math.lcm(value, item)
    return value


def sample_trajectory(
    kernel: Kernel,
    constraints: tuple[Constraint, ...],
    factors: dict[str, Fraction],
    edge_list: list[tuple[int, ...]],
    initial_state: int,
    seed: int,
    horizon: int,
    spec_hash: str,
    constraint_set_id: str,
    engine_version: str | None = None,
) -> dict:
    recorded_engine = ENGINE_VERSION if engine_version is None else engine_version
    generator = random.Random(seed)
    state = initial_state
    events = []
    for time in range(horizon):
        weights = kernel.weights[state]
        candidates = []
        for edge, weight in enumerate(weights):
            slot = edge_list[edge]
            if len(slot) == 2:
                rendered = [slot[0], slot[1]]
            else:
                rendered = list(slot)
            polarity = "form" if ((state >> edge) & 1) == 0 else "dissolve"
            applied = []
            for constraint in constraints:
                if constraint.matches(state, edge):
                    applied.append(
                        {
                            "expression": constraint.expression(edge_list),
                            "factor": str(factors[constraint.weight]),
                        }
                    )
            baseline = "1"
            if kernel.baseline_weights:
                baseline = str(kernel.baseline_weights[edge])
            candidates.append(
                {
                    "edge": rendered,
                    "edge_index": edge,
                    "polarity": polarity,
                    "baseline_weight": baseline,
                    "constraint_factors": applied,
                    "weight": str(weight),
                }
            )
        denominators = [weight.denominator for weight in weights]
        common = _lcm(denominators) if denominators else 1
        integer_weights = [int(weight * common) for weight in weights]
        total = sum(integer_weights)
        if total == 0:
            events.append(
                {
                    "t": time,
                    "state_before": state,
                    "candidates": candidates,
                    "normaliser": "0",
                    "draw": None,
                    "selected_edge": None,
                    "state_after": state,
                    "halt": True,
                }
            )
            break
        draw = generator.randrange(total)
        cumulative = 0
        selected = None
        for edge, weight in enumerate(integer_weights):
            cumulative += weight
            if draw < cumulative:
                selected = edge
                break
        if selected is None:
            raise RuntimeError("integer selection did not land in the weight table")
        nxt = state ^ (1 << selected)
        events.append(
            {
                "t": time,
                "state_before": state,
                "candidates": candidates,
                "normaliser": str(total),
                "draw": draw,
                "selected_edge": selected,
                "state_after": nxt,
                "halt": False,
            }
        )
        state = nxt
    identity_payload = {
        "engine": recorded_engine,
        "spec_hash": spec_hash,
        "constraint_set_id": constraint_set_id,
        "initial_state": initial_state,
        "seed": seed,
        "horizon": horizon,
        "prng": PRNG_NAME,
        "selection": SELECTION,
    }
    run_id = hashlib.sha256(
        json.dumps(identity_payload, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "run_id": run_id,
        "engine_version": recorded_engine,
        "spec_hash": spec_hash,
        "constraint_set_id": constraint_set_id,
        "initial_state": initial_state,
        "seed": seed,
        "horizon": horizon,
        "prng": PRNG_NAME,
        "selection": SELECTION,
        "events": events,
        "final_state": state,
    }


def replay_matches(stored: dict, regenerated: dict) -> bool:
    return stored["events"] == regenerated["events"] and stored["final_state"] == regenerated["final_state"]
