"""Typed state, event, and interface families.

The families are separate readings. This module does not compile a weight
table, does not change the engine, and is not a frozen round. No
intervention operator is defined.
"""

from __future__ import annotations

from rrc.coordinate_examples import derived_pair_count

PAIR_EDGES = ((0, 1), (1, 2))
IDENTIFIED_EDGES = ((0, 1), (1, 2), (2, 3))
CHANGING_CARRIER = ((0, 1), (1, 2))
SPLIT_BLOCKS = (((0, 1),), ((1, 2),))
JOINED_BLOCKS = (((0, 1), (1, 2),),)


def _bit_value(value, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")
    return value


def _mask(value, name: str, width: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer mask")
    if value < 0 or value >= (1 << width):
        raise ValueError(f"{name} must be an integer mask of width {width}")
    return value


def single_toggle_successors(n_bits: int, state: int) -> list[int]:
    """States reached by flipping one bit of ``state``."""
    if isinstance(n_bits, bool) or not isinstance(n_bits, int) or n_bits < 1:
        raise ValueError("n_bits must be a positive integer")
    state = _mask(state, "state", n_bits)
    return [state ^ (1 << bit) for bit in range(n_bits)]


def swap_pair_bits(mask: int) -> int:
    """Exchange the two bits of a pair mask. The count is unchanged."""
    mask = _mask(mask, "pair mask", 2)
    return ((mask & 1) << 1) | ((mask >> 1) & 1)


def derived_report() -> dict:
    """A count of present pair bits. The count is one value per mask."""
    counts = {mask: derived_pair_count(mask) for mask in range(4)}
    swapped = {mask: derived_pair_count(swap_pair_bits(mask)) for mask in range(4)}
    return {
        "family": "derived",
        "input": "pair mask in 0 .. 3",
        "output": "count of present bits",
        "state": "the pair mask",
        "transition_law": "none",
        "event_support": "none",
        "constraints": "none",
        "permitted_relabelling": "a swap of the two pair bits preserves the count",
        "recoverability": "masks 1 and 2 share count 1",
        "further_composition": "a function of the count is a function of the mask",
        "classification": "reducible_observation",
        "new_state": False,
        "counts": counts,
        "counts_after_bit_swap": swapped,
        "edge_names": PAIR_EDGES,
        "edge_names_after_bit_swap": (PAIR_EDGES[1], PAIR_EDGES[0]),
    }


def extended_report() -> dict:
    """States 1 and 5 share a pair mask and differ in a third listed bit."""
    shared = (1, 5)
    return {
        "family": "extended",
        "input": "three listed bits (pair0, pair1, activity)",
        "output": "the three-bit state",
        "state": "ordinary pair state once the third bit is a listed edge",
        "transition_law": "current-state weights on single toggles; the activity table is EQ-027",
        "event_support": "one-bit toggles of the three listed bits",
        "constraints": "the activity rows are the compiled chain in EQ-027",
        "permitted_relabelling": "a bit permutation carries the event columns and the weights",
        "recoverability": "the pair mask does not determine the third bit",
        "further_composition": "a label of the three-bit state is a label of listed pair state",
        "classification": "reducible_to_listed_bit",
        "new_event_type": False,
        "equivalence": "EQ-027",
        "states_sharing_pair_mask": shared,
        "pair_mask": 1 & 3,
        "third_bits": tuple((state >> 2) & 1 for state in shared),
        "n_bits": 3,
        "n_states": 8,
    }


def joint_event_report() -> dict:
    """A two-bit step on the same three bits and the one-step clock.

    State 5 is the joint flip of bits 0 and 2 from state 0. The one-step
    single-toggle successors of state 0 are 1, 2, and 4. Two single
    toggles reach state 5. No universal impossibility is claimed.
    """
    n_bits = 3
    source = 0
    target = 5
    successors = single_toggle_successors(n_bits, source)
    paths = []
    for mid in successors:
        if target in single_toggle_successors(n_bits, mid):
            paths.append((source, mid, target))
    return {
        "family": "joint_event",
        "input": "three-bit state",
        "output": "a proposed next state",
        "state": "the same three bits as the extended family",
        "transition_law": "not a weight on the one-step single-toggle support",
        "event_support": "one-step single toggle",
        "constraints": "none added",
        "permitted_relabelling": "a bit permutation preserves Hamming distance",
        "recoverability": "the target is a state of the same space",
        "further_composition": "two successive single toggles are the existing clock",
        "classification": "outside_one_step_single_toggle",
        "source": source,
        "target": target,
        "hamming": (source ^ target).bit_count(),
        "one_step_successors": successors,
        "reachable_in_one_step": target in successors,
        "two_step_paths": paths,
        "universal_impossibility": False,
        "scope": "same three-bit state, one-step clock, single-toggle support",
    }


def _identified_state(e0: int, e1: int, e2: int) -> int:
    return e0 | (e1 << 1) | (e2 << 2)


def identified_to_duplicated(e0: int, e1: int, e2: int) -> int:
    """Send one shared edge to two copies that carry the same bit."""
    e0 = _bit_value(e0, "e0")
    e1 = _bit_value(e1, "e1")
    e2 = _bit_value(e2, "e2")
    return e0 | (e1 << 1) | (e1 << 2) | (e2 << 3)


def _copies_agree(state: int) -> bool:
    return ((state >> 1) & 1) == ((state >> 2) & 1)


def interface_report() -> dict:
    """An identified 3-bit carrier and a 4-bit product with two copies.

    The image of ``identified_to_duplicated`` is the set of 4-bit states
    whose two shared-edge copies agree. Widths 3 and 4 are different, so
    the correspondence is not a bit permutation of one table. Toggling
    one copy leaves that set. Toggling both copies in one step stays in
    the set, has Hamming distance 2, and matches one toggle of the
    identified shared edge.
    """
    triples = [
        (e0, e1, e2)
        for e0 in (0, 1)
        for e1 in (0, 1)
        for e2 in (0, 1)
    ]
    image = {identified_to_duplicated(*triple) for triple in triples}
    agreement = [state for state in range(16) if _copies_agree(state)]
    joint_matches = True
    for e0, e1, e2 in triples:
        identified = _identified_state(e0, e1, e2)
        duplicated = identified_to_duplicated(e0, e1, e2)
        joint = duplicated ^ (1 << 1) ^ (1 << 2)
        identified_toggled = _identified_state(e0, 1 - e1, e2)
        if identified_to_duplicated(e0, 1 - e1, e2) != joint:
            joint_matches = False
        if (identified ^ identified_toggled).bit_count() != 1:
            joint_matches = False
        if (duplicated ^ joint).bit_count() != 2:
            joint_matches = False
    one_copy_leaves = all(
        not _copies_agree(state ^ (1 << bit))
        for state in agreement
        for bit in (1, 2)
    )
    return {
        "identified": {
            "family": "identified_interface",
            "input": "edges (0,1), (1,2), (2,3)",
            "output": "one 3-bit carrier state",
            "state": "listed pair state of the identified carrier",
            "transition_law": "current-state weights on single toggles of the three edges",
            "event_support": "one-bit toggles",
            "constraints": "none in this witness",
            "permitted_relabelling": "a carrier automorphism moves edges, events, and weights together",
            "recoverability": "each edge bit is the state",
            "further_composition": "a label of the 3-bit state is a label of listed pair state",
            "classification": "reducible_to_listed_carrier",
            "edges": IDENTIFIED_EDGES,
            "n_bits": 3,
            "n_states": 8,
        },
        "duplicated": {
            "family": "duplicated_interface",
            "input": "bits (0,1), copy A of (1,2), copy B of (1,2), (2,3)",
            "output": "one 4-bit product state",
            "state": "listed pair state of four bits",
            "transition_law": "the free product toggles one bit; the coupled update flips both copies",
            "event_support": "one-bit toggles on the free product",
            "constraints": "agreement of the two copies is a subset, not a new bit",
            "permitted_relabelling": "swapping the two copy bits preserves agreement",
            "recoverability": "the identified state is recovered from an agreement state by reading one copy",
            "further_composition": "the coupled update is one identified toggle and is outside the 4-bit one-step support",
            "free_product_classification": "single_toggle_on_more_bits",
            "coupled_update_classification": "outside_one_step_single_toggle",
            "n_bits": 4,
            "n_states": 16,
            "agreement_states": agreement,
            "image_of_identified_map": sorted(image),
            "map_is_bijection_onto_agreement": sorted(image) == agreement,
            "one_copy_toggle_leaves_agreement": one_copy_leaves,
            "coupled_update_matches_identified_toggle": joint_matches,
            "coupled_update_from_zero": 6,
            "coupled_update_in_one_step_support": 6 in single_toggle_successors(4, 0),
        },
    }


def encode_family_state(mask: int, family_bit: int) -> int:
    """Store a 2-bit edge mask and one family bit. Width 3."""
    mask = _mask(mask, "mask", 2)
    family_bit = _bit_value(family_bit, "family bit")
    return mask | (family_bit << 2)


def changing_family_report() -> dict:
    """The same present edges can sit in two declared block families.

    Family 0 has two blocks. Family 1 has one block. A fixed instrument
    uses one family for every mask. Encoding the choice as a bit makes
    that bit a listed coordinate. Changing an edge bit and the family
    bit in one step is outside the one-step single-toggle support.
    """
    n_bits = 3
    source = encode_family_state(0, 0)
    family_only = encode_family_state(0, 1)
    joint = encode_family_state(1, 1)
    successors = single_toggle_successors(n_bits, source)
    paths = []
    for mid in successors:
        if joint in single_toggle_successors(n_bits, mid):
            paths.append((source, mid, joint))
    return {
        "family": "changing_family",
        "input": "carrier (0,1), (1,2) and a declared block family",
        "output": "the mask, or the mask together with the family bit",
        "state": "the encoded state is mask | (family << 2)",
        "transition_law": "a listed family bit uses the single-toggle law; a fixed instrument has no family event",
        "event_support": "one-bit toggles of the encoded state",
        "constraints": "none in this witness",
        "permitted_relabelling": "renaming the family bit is a listed-bit permutation when the event moves with it",
        "recoverability": "the mask does not determine which family was declared",
        "further_composition": "a fixed instrument applies one family to every mask",
        "family_bit_classification": "reducible_to_listed_bit",
        "same_step_classification": "outside_one_step_single_toggle",
        "carrier": CHANGING_CARRIER,
        "split_blocks": SPLIT_BLOCKS,
        "joined_blocks": JOINED_BLOCKS,
        "split_block_count": len(SPLIT_BLOCKS),
        "joined_block_count": len(JOINED_BLOCKS),
        "same_mask": 0,
        "split_state": source,
        "joined_state": family_only,
        "family_bit_hamming": (source ^ family_only).bit_count(),
        "family_bit_in_one_step_support": family_only in successors,
        "joint_state": joint,
        "joint_hamming": (source ^ joint).bit_count(),
        "joint_in_one_step_support": joint in successors,
        "two_step_paths": paths,
        "fixed_instrument_states": 4,
        "encoded_states": 8,
    }


def intervention_report() -> dict:
    """The operator is absent. This record stores no distribution."""
    return {
        "family": "intervention",
        "defined": False,
        "operator": None,
        "distribution": None,
        "comparison_law": None,
        "propagation": "undefined",
        "statement": "No intervention operator is defined.",
    }


def family_records() -> tuple[dict, ...]:
    """One record for each family. Intervention is a separate record."""
    interface = interface_report()
    return (
        derived_report(),
        extended_report(),
        joint_event_report(),
        interface["identified"],
        interface["duplicated"],
        changing_family_report(),
    )
