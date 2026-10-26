"""Typed couplings of two declared bits.

The readings are not a frozen round. They call ``strict_kernel`` and the
existing strong-lumpability check. They do not compile a carrier weight
table. No intervention operator is defined.
"""

from __future__ import annotations

from rrc.composition import rational_lumpability
from rrc.event_kernel import single_toggle_catalogue, strict_kernel
from rrc.state_families import (
    JOINED_BLOCKS,
    SPLIT_BLOCKS,
    single_toggle_successors,
)

X_BIT = 0
H_BIT = 1


def _bit(state: int, bit: int) -> int:
    return (state >> bit) & 1


def _events_from(state: int, steps: list[tuple[str, str, int, int]]) -> list[dict]:
    events = []
    for name, kind, target, weight in steps:
        events.append(
            {
                "name": name,
                "kind": kind,
                "source": state,
                "target": target,
                "weight": weight,
            }
        )
    return events


def _law(events: list[dict], n_states: int, bit_width: int) -> dict:
    report = strict_kernel(n_states, events, bit_width=bit_width)
    return report


def positive_targets(probabilities, source: int) -> set[int]:
    """Targets that receive positive probability from ``source``."""
    return {target for target, prob in enumerate(probabilities[source]) if prob > 0}


def subset_invariant(probabilities, subset: set[int]) -> bool:
    """Every positive successor of a state in ``subset`` stays in ``subset``.

    Halt mass on a state counts as staying there. Mass that leaves is a
    failure. This check does not renormalise a leaking row.
    """
    return all(positive_targets(probabilities, state) <= subset for state in subset)


def correspondence(small, large, mapping: dict[int, int]) -> dict:
    """Compare a law on an image with a law on a smaller state space.

    The map must be injective. Conjugacy requires the image to be invariant
    and every small-state probability to equal the large-state probability
    of the mapped pair. A bijection whose image is not invariant is not a
    correspondence, and no restricted row is invented for it.
    """
    if not mapping:
        raise ValueError("a state map needs a state")
    if any(isinstance(state, bool) or not isinstance(state, int) for state in mapping):
        raise ValueError("a state map uses integer states")
    if any(isinstance(image, bool) or not isinstance(image, int) for image in mapping.values()):
        raise ValueError("a state map uses integer states")
    domain = sorted(mapping)
    if domain != list(range(len(small))):
        raise ValueError("a state map must cover the smaller state space")
    image = [mapping[state] for state in domain]
    if len(set(image)) != len(image):
        raise ValueError("a state map must be injective")
    if any(state < 0 or state >= len(large) for state in image):
        raise ValueError("a state map must land in the larger state space")
    image_set = set(image)
    invariant = subset_invariant(large, image_set)
    rows = None
    matches = False
    if invariant:
        rows = [
            [large[mapping[source]][mapping[target]] for target in domain]
            for source in domain
        ]
        matches = rows == [list(row) for row in small]
    return {
        "injective": True,
        "domain": domain,
        "image": image,
        "image_invariant": invariant,
        "conjugate": matches,
        "restricted_rows": rows,
    }


def _projection(probabilities, bit: int) -> dict:
    labels = [_bit(state, bit) for state in range(len(probabilities))]
    report = rational_lumpability(probabilities, labels)
    return {
        "bit": bit,
        "exact": report["exact"],
        "defined": report["defined"],
        "rows": report["rows"],
        "defect_l1": report["defect_l1"],
        "reason": report["reason"],
    }


def _two_step_paths(n_bits: int, source: int, target: int) -> list[tuple[int, int, int]]:
    paths = []
    for mid in single_toggle_successors(n_bits, source):
        if target in single_toggle_successors(n_bits, mid):
            paths.append((source, mid, target))
    return paths


def identified_toggle() -> dict:
    """One bit, toggled in both directions. Ordinary single-toggle grammar."""
    events = [
        {"name": "up", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
        {"name": "down", "kind": "toggle", "source": 1, "target": 0, "weight": 1},
    ]
    report = _law(events, 2, 1)
    return {
        "name": "identified_toggle",
        "coordinates": "one bit",
        "clock": report["clock"],
        "method": report["method"],
        "classification": "ordinary_single_toggle",
        "new_primitive": False,
        "new_event_type": False,
        "probabilities": report["probabilities"],
        "events": report["events"],
    }


def independent_product() -> dict:
    """Each bit toggles at a weight that does not depend on the other bit.

    Bit 0 has weight 2 and bit 1 has weight 5 in every state. Neither
    projection needs the other bit. The extra bit is still ordinary state.
    """
    events = []
    for state in range(4):
        events.extend(
            _events_from(
                state,
                [
                    (f"x-{state}", "toggle", state ^ (1 << X_BIT), 2),
                    (f"h-{state}", "toggle", state ^ (1 << H_BIT), 5),
                ],
            )
        )
    report = _law(events, 4, 2)
    return {
        "name": "independent_product",
        "coordinates": "bit 0 and bit 1, weights independent of the other bit",
        "clock": report["clock"],
        "method": report["method"],
        "classification": "ordinary_single_toggle",
        "new_primitive": False,
        "new_event_type": False,
        "influence": "none",
        "probabilities": report["probabilities"],
        "aggregated_weights": report["aggregated_weights"],
        "x_projection": _projection(report["probabilities"], X_BIT),
        "h_projection": _projection(report["probabilities"], H_BIT),
    }


def rescaled_rates() -> dict:
    """Integer weights depend on bit 1. The normalised event probabilities do not.

    From bit 1 equal to 0 the weights are 2 and 5. From bit 1 equal to 1
    the weights are 4 and 10. Each row still puts probability 2/7 on the
    bit-0 toggle and 5/7 on the bit-1 toggle. The integer rows differ.
    """
    events = []
    for state in range(4):
        scale = 1 if _bit(state, H_BIT) == 0 else 2
        events.extend(
            _events_from(
                state,
                [
                    (f"x-{state}", "toggle", state ^ (1 << X_BIT), 2 * scale),
                    (f"h-{state}", "toggle", state ^ (1 << H_BIT), 5 * scale),
                ],
            )
        )
    report = _law(events, 4, 2)
    return {
        "name": "rescaled_rates",
        "coordinates": "bit 0 and bit 1, integer weights scaled by bit 1",
        "clock": report["clock"],
        "method": report["method"],
        "classification": "ordinary_single_toggle",
        "new_primitive": False,
        "new_event_type": False,
        "influence": "integer weights depend on bit 1; normalised rows do not",
        "probabilities": report["probabilities"],
        "aggregated_weights": report["aggregated_weights"],
        "x_projection": _projection(report["probabilities"], X_BIT),
        "h_projection": _projection(report["probabilities"], H_BIT),
    }


def support_constraint() -> dict:
    """Bit 0 may toggle only while bit 1 is 1. Both steps stay single-bit.

    When bit 1 is 0, the only event toggles bit 1, with weight 1. When bit
    1 is 1, bit 1 toggles with weight 5 and bit 0 toggles with weight 2.
    The projection onto bit 0 is not strongly lumpable. Its quotient rows
    are absent. The projection onto bit 1 is exact. The law is still a
    current-state weight table on one-bit toggles.
    """
    events = []
    for state in range(4):
        steps = [(f"h-{state}", "toggle", state ^ (1 << H_BIT), 5 if _bit(state, H_BIT) else 1)]
        if _bit(state, H_BIT) == 1:
            steps.append((f"x-{state}", "toggle", state ^ (1 << X_BIT), 2))
        events.extend(_events_from(state, steps))
    report = _law(events, 4, 2)
    return {
        "name": "support_constraint",
        "coordinates": "bit 0 may toggle only while bit 1 is 1",
        "clock": report["clock"],
        "method": report["method"],
        "classification": "ordinary_single_toggle",
        "new_primitive": False,
        "new_event_type": False,
        "influence": "support of bit 0 depends on bit 1",
        "probabilities": report["probabilities"],
        "events": report["events"],
        "enabled_event_counts": report["enabled_event_counts"],
        "x_projection": _projection(report["probabilities"], X_BIT),
        "h_projection": _projection(report["probabilities"], H_BIT),
    }


def coupled_agreement() -> dict:
    """One joint step between states 0 and 3.

    The image of the one-bit toggle is {0, 3}. That image is invariant, and
    both orientations of the two-cycle match the one-bit law. The set {0, 1}
    is a two-element bijection target and is not invariant, so it is not a
    correspondence. States 1 and 2 halt. The joint step is outside the
    one-step single-toggle support. Two single toggles still reach state 3.
    """
    events = [
        {"name": "together-up", "kind": "joint", "source": 0, "target": 3, "weight": 1},
        {"name": "together-down", "kind": "joint", "source": 3, "target": 0, "weight": 1},
    ]
    report = _law(events, 4, 2)
    small = identified_toggle()["probabilities"]
    forward = correspondence(small, report["probabilities"], {0: 0, 1: 3})
    reverse = correspondence(small, report["probabilities"], {0: 3, 1: 0})
    leaked = correspondence(small, report["probabilities"], {0: 0, 1: 1})
    return {
        "name": "coupled_agreement",
        "coordinates": "two bits, joint update of both",
        "clock": report["clock"],
        "method": report["method"],
        "classification": "outside_one_step_single_toggle",
        "correspondence": "exact_on_invariant_image",
        "new_primitive": False,
        "new_event_type": True,
        "new_event_type_scope": "outside the one-step single-toggle support on this clock",
        "probabilities": report["probabilities"],
        "completions": report["completions"],
        "events": report["events"],
        "agreement": [0, 3],
        "forward": forward,
        "reverse": reverse,
        "leaked_image": leaked,
        "one_step_successors_of_zero": single_toggle_successors(2, 0),
        "joint_in_one_step_support": 3 in single_toggle_successors(2, 0),
        "two_step_paths": _two_step_paths(2, 0, 3),
        "universal_impossibility": False,
        "x_projection": _projection(report["probabilities"], X_BIT),
        "h_projection": _projection(report["probabilities"], H_BIT),
    }


def free_product_agreement() -> dict:
    """The all-ones single-toggle catalogue. Agreement is not invariant.

    This is the same event shape as the atlas-017 all-ones control. Leaving
    the agreement set is a property of that law. It is not a new table.
    """
    events = single_toggle_catalogue([[1, 1], [1, 1], [1, 1], [1, 1]])
    report = _law(events, 4, 2)
    small = identified_toggle()["probabilities"]
    image = correspondence(small, report["probabilities"], {0: 0, 1: 3})
    return {
        "name": "free_product",
        "coordinates": "two bits, one toggle at a time",
        "clock": report["clock"],
        "method": report["method"],
        "classification": "ordinary_single_toggle",
        "new_primitive": False,
        "new_event_type": False,
        "probabilities": report["probabilities"],
        "agreement_correspondence": image,
    }


def family_membership() -> dict:
    """A family bit is listed state. A joint flip with the edge is not.

    The fixed instrument stores only the edge bit. The family is then an
    instrument, not a coordinate. Encoding the family as bit 1 makes two
    ordinary toggles. Flipping both bits in one step is a joint event.
    The block count is a reading of that bit: 2 for the split family and
    1 for the joined family. This carrier is one edge. The earlier
    changing-family witness uses two edges and different state counts.
    """
    listed = []
    for state in range(4):
        listed.extend(
            _events_from(
                state,
                [
                    (f"edge-{state}", "toggle", state ^ 1, 1),
                    (f"family-{state}", "toggle", state ^ 2, 1),
                ],
            )
        )
    listed_report = _law(listed, 4, 2)
    joint = [
        {"name": "both", "kind": "joint", "source": 0, "target": 3, "weight": 1},
    ]
    joint_report = _law(joint, 4, 2)
    fixed = _law(
        [
            {"name": "up", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
            {"name": "down", "kind": "toggle", "source": 1, "target": 0, "weight": 1},
        ],
        2,
        1,
    )
    return {
        "name": "family_membership",
        "fixed": {
            "classification": "family_not_in_the_state",
            "n_states": fixed["n_states"],
            "method": fixed["method"],
            "new_primitive": False,
        },
        "listed": {
            "classification": "reducible_to_listed_bit",
            "method": listed_report["method"],
            "new_primitive": False,
            "new_event_type": False,
            "probabilities": listed_report["probabilities"],
        },
        "joint": {
            "classification": "outside_one_step_single_toggle",
            "method": joint_report["method"],
            "new_primitive": False,
            "hamming": (0 ^ 3).bit_count(),
            "in_one_step_support": 3 in single_toggle_successors(2, 0),
            "probabilities": joint_report["probabilities"],
        },
        "split_block_count": len(SPLIT_BLOCKS),
        "joined_block_count": len(JOINED_BLOCKS),
        "block_count_is_state": False,
    }


def coupled_records() -> dict:
    """The typed readings. None of them is a frozen cell."""
    return {
        "identified_toggle": identified_toggle(),
        "independent_product": independent_product(),
        "rescaled_rates": rescaled_rates(),
        "support_constraint": support_constraint(),
        "coupled_agreement": coupled_agreement(),
        "free_product": free_product_agreement(),
        "family_membership": family_membership(),
    }
