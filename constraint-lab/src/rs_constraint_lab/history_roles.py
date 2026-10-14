"""Label-covariant single features on current pairs and the last pair slot."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import cache, cached_property
from itertools import permutations
from math import comb

from rs_constraint_lab.history import HistoryError, HistoryState, RecentReversal
from rs_constraint_lab.memory_clocks import _solve_fraction_columns
from rs_constraint_lab.state import edges

RELATIONS = ("SAME", "ADJACENT", "DISJOINT")
DIRECTIONS = ("FORM", "DISSOLVE")


@dataclass(frozen=True)
class RoleFeature:
    name: str
    family: str
    relation: str | None
    direction: str | None

    def active(self, pair_mask: int, history: int | None, event: int, n: int = 4) -> bool:
        if self.relation is not None:
            if history is None or slot_relation(n, event, history) != self.relation:
                return False
        return self.direction is None or action_direction(pair_mask, event) == self.direction


FEATURES = (
    RoleFeature("SAME_ANY", "A", "SAME", None),
    RoleFeature("ADJ_ANY", "A", "ADJACENT", None),
    RoleFeature("DISJ_ANY", "A", "DISJOINT", None),
    RoleFeature("FORM_ANY", "B", None, "FORM"),
    RoleFeature("DISSOLVE_ANY", "B", None, "DISSOLVE"),
    RoleFeature("SAME_FORM", "C", "SAME", "FORM"),
    RoleFeature("SAME_DISSOLVE", "C", "SAME", "DISSOLVE"),
    RoleFeature("ADJ_FORM", "C", "ADJACENT", "FORM"),
    RoleFeature("ADJ_DISSOLVE", "C", "ADJACENT", "DISSOLVE"),
    RoleFeature("DISJ_FORM", "C", "DISJOINT", "FORM"),
    RoleFeature("DISJ_DISSOLVE", "C", "DISJOINT", "DISSOLVE"),
)
FEATURE_BY_NAME = {feature.name: feature for feature in FEATURES}


@cache
def slot_relation(n: int, event: int, history: int) -> str:
    pairs = edges(n)
    if not 0 <= event < len(pairs) or not 0 <= history < len(pairs):
        raise HistoryError("pair slot outside declared graph")
    if event == history:
        return "SAME"
    return "ADJACENT" if set(pairs[event]) & set(pairs[history]) else "DISJOINT"


def action_direction(pair_mask: int, event: int) -> str:
    return "DISSOLVE" if pair_mask & (1 << event) else "FORM"


@dataclass(frozen=True)
class RoleController:
    feature_name: str
    multiplier: Fraction
    n: int = 4

    def __post_init__(self):
        object.__setattr__(self, "multiplier", Fraction(self.multiplier))
        if self.feature_name not in FEATURE_BY_NAME or self.multiplier <= 0 or self.n not in (3, 4):
            raise HistoryError("unknown feature, nonpositive multiplier or unsupported fixture")

    @property
    def feature(self) -> RoleFeature:
        return FEATURE_BY_NAME[self.feature_name]

    @property
    def slots(self) -> int:
        return comb(self.n, 2)

    @property
    def state_count(self) -> int:
        return (1 << self.slots) * self.slots

    @cached_property
    def updates(self) -> RecentReversal:
        return RecentReversal(Fraction(1), self.slots, comb(self.n, 3))

    def validate_pair_state(self, pair_mask: int, history: int | None):
        if type(pair_mask) is not int or not 0 <= pair_mask < 1 << self.slots:
            raise HistoryError("invalid pair mask")
        self.updates.validate_history(history)

    @cache
    def full_probabilities(self, pair_mask: int, history: int | None) -> tuple[Fraction, ...]:
        self.validate_pair_state(pair_mask, history)
        weights = [
            self.multiplier if self.feature.active(pair_mask, history, event, self.n) else Fraction(1)
            for event in range(self.slots)
        ] + [Fraction(1)] * comb(self.n, 3)
        denominator = sum(weights)
        return tuple(weight / denominator for weight in weights)

    @cache
    def pair_probabilities(self, pair_mask: int, history: int | None) -> tuple[Fraction, ...]:
        full = self.full_probabilities(pair_mask, history)
        pair_mass = sum(full[:self.slots])
        return tuple(value / pair_mass for value in full[:self.slots])

    def full_row(self, state: HistoryState) -> dict[HistoryState, Fraction]:
        self.updates.validate_state(state)
        probabilities = self.full_probabilities(state.material & ((1 << self.slots) - 1), state.recent_pair)
        return {self.updates.advance(state, event): value for event, value in enumerate(probabilities)}

    @cache
    def kernel(self) -> tuple[dict[int, Fraction], ...]:
        return tuple({
            (pair_mask ^ (1 << event)) * self.slots + event: value
            for event, value in enumerate(self.pair_probabilities(pair_mask, history))
        } for pair_mask in range(1 << self.slots) for history in range(self.slots))

    def direct_next_pair_slots(self, pair_mask: int, history: int | None):
        self.validate_pair_state(pair_mask, history)
        size = 1 << comb(self.n, 3)
        matrix = [[Fraction(i == j) for j in range(size)] for i in range(size)]
        direct = [[Fraction(0) for _ in range(size)] for _ in range(self.slots)]
        for hidden in range(size):
            state = HistoryState(pair_mask | (hidden << self.slots), history)
            for target, probability in self.full_row(state).items():
                event = (state.material ^ target.material).bit_length() - 1
                if event < self.slots:
                    direct[event][hidden] += probability
                else:
                    matrix[hidden][target.material >> self.slots] -= probability
        columns = _solve_fraction_columns(matrix, direct)
        return [[columns[event][hidden] for event in range(self.slots)] for hidden in range(size)]


@cache
def role_descriptors(pair_mask: int, history: int, n: int = 4) -> tuple[int, int, int, int]:
    pairs = edges(n)
    index = {pair: i for i, pair in enumerate(pairs)}
    a, b = pairs[history]
    adjacent = sum(bool(pair_mask & (1 << event)) for event in range(len(pairs)) if slot_relation(n, event, history) == "ADJACENT")
    disjoint = sum(bool(pair_mask & (1 << event)) for event in range(len(pairs)) if slot_relation(n, event, history) == "DISJOINT")
    common = sum(
        bool(pair_mask & (1 << index[tuple(sorted((a, v)))]))
        and bool(pair_mask & (1 << index[tuple(sorted((b, v)))]))
        for v in range(n) if v not in (a, b)
    )
    return int(bool(pair_mask & (1 << history))), adjacent, disjoint, common


@dataclass(frozen=True)
class RoleOrbits:
    n: int
    members: tuple[tuple[int, ...], ...]
    orbit_of: tuple[int, ...]
    edge_maps: tuple[tuple[int, ...], ...]
    mask_maps: tuple[tuple[int, ...], ...]

    @property
    def slots(self):
        return comb(self.n, 2)

    def records(self) -> list[dict]:
        records = []
        for orbit, members in enumerate(self.members):
            p, h = divmod(members[0], self.slots)
            r, a, d, c = role_descriptors(p, h, self.n)
            records.append({
                "orbit_id": orbit, "orbit_size": len(members),
                "canonical_pair_mask": p, "canonical_h": h, "members": members,
                "R": r, "A_h": a, "D_h": d, "C_h": c,
            })
        return records


@cache
def role_orbits(n: int = 4) -> RoleOrbits:
    pairs = edges(n)
    index = {pair: i for i, pair in enumerate(pairs)}
    slots = len(pairs)
    edge_maps = tuple(tuple(index[tuple(sorted((perm[a], perm[b])))] for a, b in pairs) for perm in permutations(range(n)))
    mask_maps = tuple(tuple(sum(1 << mapping[e] for e in range(slots) if p & (1 << e)) for p in range(1 << slots)) for mapping in edge_maps)
    groups = defaultdict(list)
    for p in range(1 << slots):
        for h in range(slots):
            canonical = min(masks[p] * slots + mapping[h] for masks, mapping in zip(mask_maps, edge_maps))
            groups[canonical].append(p * slots + h)
    members = tuple(tuple(groups[key]) for key in sorted(groups))
    orbit_of = [0] * ((1 << slots) * slots)
    for orbit, group in enumerate(members):
        for state in group:
            orbit_of[state] = orbit
    return RoleOrbits(n, members, tuple(orbit_of), edge_maps, mask_maps)


def aggregate_quotient(rows, groups, orbit_of):
    result = []
    gap = Fraction(0)
    for group in groups:
        reference = None
        for source in group:
            row = defaultdict(Fraction)
            for target, probability in rows[source].items():
                row[orbit_of[target]] += probability
            if reference is None:
                reference = dict(row)
            else:
                gap = max(gap, max(abs(row.get(t, 0) - reference.get(t, 0)) for t in row.keys() | reference.keys()))
        result.append(reference)
    return tuple(result), gap


def covariance_gap(model: RoleController) -> Fraction:
    structure = role_orbits(model.n)
    gap = Fraction(0)
    for mapping, masks in zip(structure.edge_maps, structure.mask_maps):
        for p in range(1 << model.slots):
            for h in range(model.slots):
                original = model.pair_probabilities(p, h)
                image = model.pair_probabilities(masks[p], mapping[h])
                for event in range(model.slots):
                    gap = max(gap, abs(original[event] - image[mapping[event]]))
    return gap


def structural_record() -> dict:
    structure = role_orbits()
    descriptors = defaultdict(list)
    for row in structure.records():
        descriptors[tuple(row[key] for key in ("R", "A_h", "D_h", "C_h"))].append(row["orbit_id"])
    checked = 0
    for feature in FEATURES:
        for mapping, masks in zip(structure.edge_maps, structure.mask_maps):
            for p in range(64):
                for h in range(6):
                    for event in range(6):
                        if feature.active(p, h, event) != feature.active(masks[p], mapping[h], mapping[event]):
                            raise HistoryError("Boolean feature covariance failed")
                        checked += 1
    return {
        "state_count": 384, "orbit_count": len(structure.members), "orbits": structure.records(),
        "orbit_size_sum": sum(map(len, structure.members)),
        "descriptor_vector_count": len(descriptors),
        "descriptor_collisions": [{"descriptor": key, "orbit_ids": value} for key, value in sorted(descriptors.items()) if len(value) > 1],
        "boolean_covariance_comparisons": checked,
        "slot_relation_counts": [[sum(slot_relation(4, e, h) == relation for e in range(6)) for relation in RELATIONS] for h in range(6)],
        "pre_freeze_actual_non_neutral_I0_cells": 0,
    }
