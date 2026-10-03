"""Independent-hypergraph measures for one triadic slot at N=3.

The triadic bit is a relation, not an extra state channel. These functions
compare the pairwise projection of that process with the searched O=2
grammar. They do not treat a 16-state hash as an 8-state hash.

Comparison domain
-----------------
Generation 1b, N=3, K<=3, cardinalities 1, 2 and 3, structural-simple,
pairwise-edge grammar. The kernel-id file is
``kernel-ids-n3-k3.txt``. The unconstrained O=2 baseline kernel is added
even though the empty set was not an enumerated cardinality. Count
predicates, stacked weights, other N, and K>3 are outside the domain.
A miss against that file is not absolute irreducibility.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
from collections import deque
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.constraints import Choreography, set_cross_order_class
from rs_constraint_lab.dynamics import RelabelTables, canonical_tokens, family_ids
from rs_constraint_lab.exact import long_run, period_of, reachable_from, recurrent_components
from rs_constraint_lab.kernel import Kernel, build_kernel, modal_map, support_map
from rs_constraint_lab.observables import rise_then_release_probability
from rs_constraint_lab.state import component_count, edges, permutations, relabel_relation_state, relation_slots
from rs_constraint_lab.state import edge_count as pair_slot_count

COMPARISON_DOMAIN = (
    "Generation 1b N=3 K<=3 cardinalities {1,2,3} structural-simple "
    "pairwise-edge grammar, kernel ids in kernel-ids-n3-k3.txt, plus the "
    "unconstrained O=2 baseline under the same S_3 canonicalisation. "
    "Count predicates, stacked weights, N other than 3, and K>3 are outside "
    "this domain. Raw 16-state hashes are not compared with 8-state hashes."
)

N3_LIMITATION = (
    "At N=3 a pairwise graph class is the edge count. A relabelled wedge is "
    "the same class. Same-cardinality non-isomorphic reconfiguration is "
    "impossible here, so an edge-count change is not a new organisation."
)

class _IdList(list):
    """Id accumulator. A builtin list cannot carry a membership set."""

    def __init__(self, values=()):
        super().__init__()
        self.seen = set()
        for value in values:
            if value not in self.seen:
                self.seen.add(value)
                list.append(self, value)


_CLASSES = ("P->P", "P->T", "T->P", "T->T", "mixed")
_REDUCIBILITY = (
    "FULLY_REDUCIBLE",
    "PAIRWISE_PROJECTION_REDUCIBLE",
    "IRREDUCIBLE_DYNAMIC_COUPLING",
    "OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR",
    "UNRESOLVED",
)
_SUPPORT_RE = re.compile(r'"support_family": "([0-9a-f]{64})"')
_INDEX_CACHE: dict | None = None


def comparison_directory() -> Path:
    override = os.environ.get("RS_LAB_PAIRWISE_INDEX")
    if override:
        return Path(override)
    return (
        Path(__file__).resolve().parents[2]
        / "generated"
        / "generation-001b-structurally-normalised"
    )


def file_sha256(path: Path) -> str:
    if not path.is_file():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _text(value: Fraction | None) -> str | None:
    if value is None:
        return None
    return f"{value.numerator}/{value.denominator}"


def _read_id_file(path: Path) -> set[str] | None:
    if not path.is_file():
        return None
    found = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line:
            found.add(line.strip())
    return found


def _read_support_ids(path: Path) -> set[str] | None:
    if not path.is_file():
        return None
    found = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            match = _SUPPORT_RE.search(line)
            if match:
                found.add(match.group(1))
    return found


def load_comparison_indexes() -> dict:
    """Load the O=2 comparison sets once per process."""
    global _INDEX_CACHE
    directory = comparison_directory()
    key = str(directory.resolve()) if directory.exists() else str(directory)
    if _INDEX_CACHE is not None and _INDEX_CACHE.get("directory") == key:
        return _INDEX_CACHE
    kernels = _read_id_file(directory / "kernel-ids-n3-k3.txt")
    qualitative = _read_id_file(directory / "qualitative-ids-n3-k3.txt")
    supports = _read_support_ids(directory / "families-n3-k3.jsonl")
    tables = RelabelTables(3)
    baseline = build_kernel(3, Choreography(0, 0, ()), {})
    base_ids = family_ids(3, canonical_tokens(baseline, tables))
    if kernels is not None:
        kernels.add(base_ids["exact_kernel_family"])
    if qualitative is not None:
        qualitative.add(base_ids["qualitative_family"])
    if supports is not None:
        supports.add(base_ids["support_family"])
    _INDEX_CACHE = {
        "directory": key,
        "kernels": kernels,
        "qualitative": qualitative,
        "supports": supports,
        "baseline_kernel_id": base_ids["exact_kernel_family"],
        "baseline_support_id": base_ids["support_family"],
        "baseline_qualitative_id": base_ids["qualitative_family"],
        "kernel_index_present": kernels is not None,
        "qualitative_index_present": qualitative is not None,
        "support_index_present": supports is not None,
        "domain": COMPARISON_DOMAIN,
        "graph_tables": tables,
    }
    return _INDEX_CACHE


def orbit_catalogue(n: int = 3) -> dict:
    """Coarse S_N orbits of the independent-hypergraph state at N=3.

    Classes are the pairwise isomorphism type crossed with the triadic bit.
    They are not the total number of present relations.
    """
    if n != 3:
        raise ValueError("the coarse orbit catalogue is implemented for N=3")
    slots = relation_slots(3, 3)
    names = {
        (0, 0): "empty-pairs-no-triad",
        (0, 1): "empty-pairs-triad",
        (1, 0): "one-pair-no-triad",
        (1, 1): "one-pair-triad",
        (2, 0): "wedge-no-triad",
        (2, 1): "wedge-triad",
        (3, 0): "triangle-no-triad",
        (3, 1): "triangle-triad",
    }
    orbits: dict[int, dict] = {}
    for state in range(16):
        images = {relabel_relation_state(state, perm, slots) for perm in permutations(3)}
        representative = min(images)
        if representative in orbits:
            continue
        pair_edges = (representative & 0b111).bit_count()
        triad = (representative >> 3) & 1
        orbits[representative] = {
            "representative": representative,
            "size": len(images),
            "pair_edges": pair_edges,
            "triad_present": triad,
            "name": names[(pair_edges, triad)],
            "states": sorted(images),
        }
    rows = [orbits[key] for key in sorted(orbits)]
    covered = sum(row["size"] for row in rows)
    if covered != 16 or len(rows) != 8:
        raise RuntimeError(f"N=3 hypergraph orbit catalogue covered {covered} states in {len(rows)} orbits")
    return {
        "labelled_states": 16,
        "orbit_count": len(rows),
        "limitation": N3_LIMITATION,
        "orbits": rows,
    }


def _require_n3_layout(kernel: Kernel) -> tuple[list[int], int]:
    slots = kernel.relation_slots
    pair_indexes = [i for i, slot in enumerate(slots) if len(slot) == 2]
    triad_indexes = [i for i, slot in enumerate(slots) if len(slot) == 3]
    if pair_indexes != [0, 1, 2] or triad_indexes != [3]:
        raise ValueError("higher-order measures expect three pairwise bits and then one triadic bit")
    return pair_indexes, 3


def _pair_popcount(state: int) -> int:
    return (state & 0b111).bit_count()


def _fraction_row(weights: tuple[Fraction, ...], indexes: list[int]) -> tuple[Fraction, Fraction]:
    total = sum((weights[index] for index in indexes), Fraction(0))
    return total, total


def hypergraph_light_observables(kernel: Kernel, baseline: Kernel) -> dict:
    """Pairwise observables conditioned on the next event being a pair toggle.

    The screened dissolution shift uses that conditional probability, so the
    free triadic toggle is not scored as a trivial shift away from m/3.
    """
    _require_n3_layout(kernel)
    deadlocks = [state for state, halted in enumerate(kernel.deadlock) if halted]
    recurrent = recurrent_components(kernel)
    periods = sorted({period_of(component, kernel.successors) for component in recurrent})
    reachable = reachable_from(kernel, 0)
    reachable_recurrent = sum(1 for component in recurrent if any(state in reachable for state in component))
    max_shift = Fraction(0)
    sum_shift = Fraction(0)
    counted = 0
    for state in range(kernel.n_states):
        if kernel.deadlock[state]:
            continue
        weights = kernel.weights[state]
        pair_total = sum(weights[index] for index in (0, 1, 2))
        if pair_total == 0:
            continue
        occupied = _pair_popcount(state)
        dissolve = sum((weights[index] for index in (0, 1, 2) if (state >> index) & 1), Fraction(0)) / pair_total
        shift = abs(dissolve - Fraction(occupied, 3))
        if shift > max_shift:
            max_shift = shift
        sum_shift += shift
        counted += 1
    closing = _conditional_closing_bias(kernel)
    mean_shift = (sum_shift / counted) if counted else Fraction(0)
    modes = modal_map(kernel)
    support = support_map(kernel)
    base_support = support_map(baseline)
    return {
        "n_deadlock": len(deadlocks),
        "deadlock_states": deadlocks,
        "n_recurrent": len(recurrent),
        "n_recurrent_reachable_from_empty": reachable_recurrent,
        "periods": periods,
        "reachable_from_empty": len(reachable),
        "max_abs_dissolve_shift": float(max_shift),
        "max_abs_dissolve_shift_exact": _text(max_shift),
        "mean_abs_dissolve_shift": float(mean_shift),
        "mean_abs_dissolve_shift_exact": _text(mean_shift),
        "closing_bias": None if closing is None else float(closing),
        "closing_bias_exact": _text(closing),
        "support_matches_baseline": support == base_support,
        "modal_family": hashlib.sha256(repr((kernel.n, modes)).encode("utf-8")).hexdigest()[:16],
        "support_family": hashlib.sha256(repr((kernel.n, support)).encode("utf-8")).hexdigest()[:16],
        "modes": modes,
    }


def _conditional_closing_bias(kernel: Kernel) -> Fraction | None:
    values = []
    for state in range(kernel.n_states):
        if _pair_popcount(state) != 2:
            continue
        if kernel.deadlock[state]:
            values.append(Fraction(0))
            continue
        weights = kernel.weights[state]
        pair_total = sum(weights[index] for index in (0, 1, 2))
        if pair_total == 0:
            values.append(Fraction(0))
            continue
        missing = next(bit for bit in (0, 1, 2) if ((state >> bit) & 1) == 0)
        values.append(weights[missing] / pair_total)
    if not values:
        return None
    return sum(values, Fraction(0)) / len(values) - Fraction(1, 3)


def hypergraph_heavy_observables(kernel: Kernel, horizon: int = 4, start: int = 0) -> dict:
    """Stationary observables. Pair density ignores the triadic bit.

    Triangle mass is the stationary mass of states whose three pairs are
    present, whether or not the independent triad is present. It is not the
    mass of state 15.
    """
    _require_n3_layout(kernel)
    ran = long_run(kernel, start)
    pi_exact = ran["distribution_exact"]
    pi = ran["distribution"]
    edge_list = edges(kernel.n)
    rise_exact = None
    if kernel.n_states <= 64:
        rise_exact = rise_then_release_probability(kernel, horizon, start, occupancy=_pair_popcount)
    if pi_exact is not None:
        density_sum = sum((mass * _pair_popcount(state) for state, mass in pi_exact.items()), Fraction(0))
        component_sum = sum(
            (mass * component_count(state, kernel.n, edge_list) for state, mass in pi_exact.items()),
            Fraction(0),
        )
        occupancy = [Fraction(0) for _ in range(4)]
        halt_mass = Fraction(0)
        triad_mass = Fraction(0)
        absent_pair = Fraction(0)
        absent_mass = Fraction(0)
        present_pair = Fraction(0)
        present_mass = Fraction(0)
        triangle = Fraction(0)
        formation = Fraction(0)
        dissolution = Fraction(0)
        class_joint: dict[tuple[int, int], Fraction] = {}
        entropy = 0.0
        for state, mass in pi_exact.items():
            occupied = _pair_popcount(state)
            occupancy[occupied] += mass
            triad = (state >> 3) & 1
            class_joint[(triad, occupied)] = class_joint.get((triad, occupied), Fraction(0)) + mass
            if (state & 0b111) == 0b111:
                triangle += mass
            if kernel.deadlock[state]:
                halt_mass += mass
            else:
                weights = kernel.weights[state]
                total = sum(weights, Fraction(0))
                step = weights[3] / total if total else Fraction(0)
                if triad:
                    dissolution += mass * step
                    present_pair += mass * occupied
                    present_mass += mass
                    triad_mass += mass
                else:
                    formation += mass * step
                    absent_pair += mass * occupied
                    absent_mass += mass
            mass_float = float(mass)
            for _nxt, prob in kernel.successors[state]:
                probability = float(prob)
                if probability > 0.0 and mass_float > 0.0:
                    entropy -= mass_float * probability * math.log(probability)
        uniform = Fraction(1, kernel.n_states)
        tv = Fraction(1, 2) * sum(
            (abs(pi_exact.get(state, Fraction(0)) - uniform) for state in range(kernel.n_states)),
            Fraction(0),
        )
        from rs_constraint_lab.observables import _reversibility_defect_exact

        defect = _reversibility_defect_exact(kernel, pi_exact)
        density = density_sum / 3
        density_absent = (absent_pair / absent_mass / 3) if absent_mass else None
        density_present = (present_pair / present_mass / 3) if present_mass else None
        sojourn = (triad_mass / dissolution) if dissolution else None
        return {
            "mean_edge_density": float(density),
            "mean_edge_density_exact": _text(density),
            "edge_count_occupancy": [float(item) for item in occupancy],
            "edge_count_occupancy_exact": [_text(item) for item in occupancy],
            "mean_component_count": float(component_sum),
            "entropy_rate_nats": entropy,
            "entropy_rate_bits": entropy / math.log(2),
            "tv_from_uniform": float(tv),
            "tv_from_uniform_exact": _text(tv),
            "reversibility_defect": float(defect),
            "reversibility_defect_exact": _text(defect),
            "halt_mass": float(halt_mass),
            "halt_mass_exact": _text(halt_mass),
            "triangle_mass": float(triangle),
            "triangle_mass_exact": _text(triangle),
            "disjoint_pair_mass": None,
            "disjoint_pair_mass_exact": None,
            "rise_then_release": None if rise_exact is None else float(rise_exact),
            "rise_then_release_exact": _text(rise_exact),
            "stationary_arithmetic": ran["stationary_arithmetic"],
            "stationary_residual": ran["stationary_residual"],
            "n_recurrent": ran["n_recurrent"],
            "periods": ran["periods"],
            "reachable_count": ran["reachable_count"],
            "triad_occupancy_exact": _text(triad_mass),
            "pair_density_triad_absent_exact": _text(density_absent),
            "pair_density_triad_present_exact": _text(density_present),
            "triad_formation_flux_exact": _text(formation),
            "triad_dissolution_flux_exact": _text(dissolution),
            "triad_present_sojourn_exact": _text(sojourn),
            "triad_graph_class_mi_bits": _mutual_information(class_joint),
        }
    return _heavy_float(kernel, ran, pi, edge_list, rise_exact)


def _heavy_float(kernel, ran, pi, edge_list, rise_exact) -> dict:
    density_sum = 0.0
    component_sum = 0.0
    occupancy = [0.0 for _ in range(4)]
    halt = 0.0
    entropy = 0.0
    for state, mass in pi.items():
        occupied = _pair_popcount(state)
        density_sum += mass * occupied
        occupancy[occupied] += mass
        component_sum += mass * component_count(state, kernel.n, edge_list)
        if kernel.deadlock[state]:
            halt += mass
        for _nxt, prob in kernel.successors[state]:
            probability = float(prob)
            if probability > 0.0 and mass > 0.0:
                entropy -= mass * probability * math.log(probability)
    uniform = 1.0 / kernel.n_states
    tv = 0.5 * sum(abs(pi.get(state, 0.0) - uniform) for state in range(kernel.n_states))
    return {
        "mean_edge_density": density_sum / 3,
        "mean_edge_density_exact": None,
        "edge_count_occupancy": occupancy,
        "edge_count_occupancy_exact": None,
        "mean_component_count": component_sum,
        "entropy_rate_nats": entropy,
        "entropy_rate_bits": entropy / math.log(2),
        "tv_from_uniform": tv,
        "tv_from_uniform_exact": None,
        "reversibility_defect": None,
        "reversibility_defect_exact": None,
        "halt_mass": halt,
        "halt_mass_exact": None,
        "triangle_mass": sum(mass for state, mass in pi.items() if (state & 0b111) == 0b111),
        "triangle_mass_exact": None,
        "disjoint_pair_mass": None,
        "disjoint_pair_mass_exact": None,
        "rise_then_release": None if rise_exact is None else float(rise_exact),
        "rise_then_release_exact": _text(rise_exact),
        "stationary_arithmetic": ran["stationary_arithmetic"],
        "stationary_residual": ran["stationary_residual"],
        "n_recurrent": ran["n_recurrent"],
        "periods": ran["periods"],
        "reachable_count": ran["reachable_count"],
        "triad_occupancy_exact": None,
        "pair_density_triad_absent_exact": None,
        "pair_density_triad_present_exact": None,
        "triad_formation_flux_exact": None,
        "triad_dissolution_flux_exact": None,
        "triad_present_sojourn_exact": None,
        "triad_graph_class_mi_bits": None,
    }


def _mutual_information(joint: dict[tuple[int, int], Fraction]) -> float:
    row: dict[int, Fraction] = {}
    column: dict[int, Fraction] = {}
    for (left, right), mass in joint.items():
        row[left] = row.get(left, Fraction(0)) + mass
        column[right] = column.get(right, Fraction(0)) + mass
    info = 0.0
    for (left, right), mass in joint.items():
        if mass == 0:
            continue
        independent = row[left] * column[right]
        if independent == 0:
            continue
        info += float(mass) * math.log2(float(mass / independent))
    return info


def pairwise_jump_kernels(kernel: Kernel) -> tuple[Kernel, Kernel]:
    """8-state kernels obtained by conditioning on a pairwise toggle.

    ``rho3`` cancels inside a slice when the triadic baseline is constant
    on that slice, which it is for a state-independent baseline. The three
    pair weights are renormalised. The result is a graph kernel: no
    relation slots, three toggles, eight states.
    """
    _require_n3_layout(kernel)

    def one(triad_value: int) -> Kernel:
        successors = []
        weights_out = []
        deadlock = []
        for pair_state in range(8):
            full = pair_state | (triad_value << 3)
            row = kernel.weights[full]
            pair_weights = (row[0], row[1], row[2])
            total = sum(pair_weights, Fraction(0))
            weights_out.append(pair_weights)
            if kernel.deadlock[full] or total == 0:
                deadlock.append(True)
                successors.append(((pair_state, Fraction(1)),))
                continue
            outgoing = []
            for bit, weight in enumerate(pair_weights):
                if weight != 0:
                    outgoing.append((pair_state ^ (1 << bit), weight / total))
            deadlock.append(False)
            successors.append(tuple(outgoing))
        return Kernel(kernel.n, 8, 3, tuple(successors), tuple(weights_out), tuple(deadlock))

    return one(0), one(1)


def triad_weight_depends_on_pairs(kernel: Kernel) -> bool:
    _require_n3_layout(kernel)
    for triad in (0, 1):
        values = [kernel.weights[pair_state | (triad << 3)][3] for pair_state in range(8)]
        if len(set(values)) > 1:
            return True
    return False


def _jump_ids(kernel: Kernel, tables: RelabelTables) -> dict:
    return family_ids(kernel.n, canonical_tokens(kernel, tables))


def classify_reducibility(kernel: Kernel, indexes: dict, tables: RelabelTables) -> dict:
    jump_absent, jump_present = pairwise_jump_kernels(kernel)
    absent_ids = _jump_ids(jump_absent, tables)
    present_ids = _jump_ids(jump_present, tables)
    same = absent_ids["exact_kernel_family"] == present_ids["exact_kernel_family"]
    depends = triad_weight_depends_on_pairs(kernel)
    known = indexes.get("kernels")
    if known is None:
        label = "UNRESOLVED"
    elif not same:
        label = "IRREDUCIBLE_DYNAMIC_COUPLING"
    elif absent_ids["exact_kernel_family"] not in known:
        label = "OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR"
    elif depends:
        label = "PAIRWISE_PROJECTION_REDUCIBLE"
    else:
        label = "FULLY_REDUCIBLE"
    supports = indexes.get("supports")
    qualitative = indexes.get("qualitative")
    support_outside = None
    if supports is not None:
        support_outside = (
            absent_ids["support_family"] not in supports or present_ids["support_family"] not in supports
        )
    qualitative_outside = None
    if qualitative is not None:
        qualitative_outside = (
            absent_ids["qualitative_family"] not in qualitative
            or present_ids["qualitative_family"] not in qualitative
        )
    max_tv = Fraction(0)
    for state in range(8):
        max_tv = max(max_tv, _distribution_tv(jump_absent, jump_present, state))
    return {
        "class": label,
        "jump_equal": same,
        "jump_id_triad_absent": absent_ids["exact_kernel_family"],
        "jump_id_triad_present": present_ids["exact_kernel_family"],
        "jump_support_triad_absent": absent_ids["support_family"],
        "jump_support_triad_present": present_ids["support_family"],
        "jump_qualitative_triad_absent": absent_ids["qualitative_family"],
        "jump_qualitative_triad_present": present_ids["qualitative_family"],
        "triad_weight_depends_on_pairs": depends,
        "jump_support_outside_index": support_outside,
        "jump_qualitative_outside_index": qualitative_outside,
        "pairwise_jump_tv_exact": _text(max_tv),
        "rate_competition": _rate_competition(kernel, depends),
    }


def _distribution_tv(left: Kernel, right: Kernel, state: int) -> Fraction:
    masses: dict[int, Fraction] = {}
    for nxt, prob in left.successors[state]:
        masses[nxt] = masses.get(nxt, Fraction(0)) + prob
    for nxt, prob in right.successors[state]:
        masses[nxt] = masses.get(nxt, Fraction(0)) - prob
    return sum((abs(value) for value in masses.values()), Fraction(0)) / 2


def _rate_competition(kernel: Kernel, depends: bool) -> bool:
    """Pair weights change the chance that the next event is the triad.

    This can make I(P; T'|T) positive while the pairwise jump law is
    independent of the triad. It is not irreducible dynamic coupling.
    """
    if depends:
        return False
    probabilities = []
    for state in range(kernel.n_states):
        if kernel.deadlock[state]:
            continue
        weights = kernel.weights[state]
        total = sum(weights, Fraction(0))
        if total == 0:
            continue
        probabilities.append(weights[3] / total)
    return len(set(probabilities)) > 1


def _stationary(kernel: Kernel) -> list[Fraction]:
    ran = long_run(kernel, 0)
    exact = ran["distribution_exact"]
    if exact is None:
        raise RuntimeError("emergent-memory comparison requires the rational stationary distribution")
    return [exact.get(state, Fraction(0)) for state in range(kernel.n_states)]


def _transition_table(kernel: Kernel) -> list[dict[int, Fraction]]:
    """Successor lookup for one kernel object.

    The table is local to the call. Caching it by ``id(kernel)`` is unsafe:
    CPython reuses ids after collection, and a later kernel would then read
    the previous kernel's transitions.
    """
    return [{nxt: prob for nxt, prob in row} for row in kernel.successors]


def _prob(table: list[dict[int, Fraction]], source: int, target: int) -> Fraction:
    return table[source].get(target, Fraction(0))


def emergent_memory_tv(kernel: Kernel, pi: list[Fraction] | None = None) -> Fraction:
    """Max total variation between P(P'|P) and P(P'|P, P_prev) after hiding the triad.

    Zero means the pairwise marginal is still first-order Markov on the
    stationary pair process. A positive value is emergent memory under
    coarse-graining, not a fundamental history variable.
    """
    _require_n3_layout(kernel)
    if pi is None:
        pi = _stationary(kernel)
    table = _transition_table(kernel)
    maximum = Fraction(0)
    for previous in range(8):
        for current in range(8):
            joint = Fraction(0)
            history = [Fraction(0) for _ in range(8)]
            for triad_prev in (0, 1):
                source = previous | (triad_prev << 3)
                mass = pi[source]
                if mass == 0:
                    continue
                for triad_now in (0, 1):
                    middle = current | (triad_now << 3)
                    step = _prob(table, source, middle)
                    if step == 0:
                        continue
                    joint += mass * step
                    for nxt in range(8):
                        follow = Fraction(0)
                        for triad_next in (0, 1):
                            follow += _prob(table, middle, nxt | (triad_next << 3))
                        history[nxt] += mass * step * follow
            if joint == 0:
                continue
            current_mass = pi[current] + pi[current | 8]
            if current_mass == 0:
                continue
            marginal = [Fraction(0) for _ in range(8)]
            for triad_now in (0, 1):
                middle = current | (triad_now << 3)
                mass = pi[middle]
                if mass == 0:
                    continue
                for nxt in range(8):
                    follow = Fraction(0)
                    for triad_next in (0, 1):
                        follow += _prob(table, middle, nxt | (triad_next << 3))
                    marginal[nxt] += mass * follow
            tv = sum(
                (abs(history[nxt] / joint - marginal[nxt] / current_mass) for nxt in range(8)),
                Fraction(0),
            ) / 2
            if tv > maximum:
                maximum = tv
    return maximum


def information_flow(kernel: Kernel, pi: list[Fraction] | None = None) -> dict:
    """Exact conditional mutual information from the stationary kernel.

    ``I(T; P'|P)`` asks whether the triadic bit improves the prediction of
    the next pairwise state. ``I(P; T'|T)`` asks the converse. A positive
    value from rate competition is flagged separately from a change in the
    pairwise jump law.
    """
    _require_n3_layout(kernel)
    if pi is None:
        pi = _stationary(kernel)
    table = _transition_table(kernel)
    triad_to_pair = _cmi_triad_to_pair(table, pi)
    pair_to_triad = _cmi_pair_to_triad(table, pi)
    return {
        "cmi_triad_to_pair_bits": triad_to_pair["bits"],
        "cmi_pair_to_triad_bits": pair_to_triad["bits"],
        "triad_predicts_next_pair": triad_to_pair["depends"],
        "pair_predicts_next_triad": pair_to_triad["depends"],
    }


def _cmi_triad_to_pair(table: list[dict[int, Fraction]], pi: list[Fraction]) -> dict:
    bits = 0.0
    depends = False
    for current in range(8):
        mass_current = pi[current] + pi[current | 8]
        if mass_current == 0:
            continue
        marginal = [Fraction(0) for _ in range(8)]
        conditional = []
        weights = []
        for triad in (0, 1):
            source = current | (triad << 3)
            mass = pi[source]
            law = [Fraction(0) for _ in range(8)]
            for nxt in range(8):
                step = Fraction(0)
                for triad_next in (0, 1):
                    step += _prob(table, source, nxt | (triad_next << 3))
                law[nxt] = step
                if mass:
                    marginal[nxt] += mass * step
            conditional.append(law)
            weights.append(mass)
        marginal = [value / mass_current for value in marginal]
        for triad, law in enumerate(conditional):
            mass = weights[triad]
            if mass == 0:
                continue
            if any(law[nxt] != marginal[nxt] for nxt in range(8)):
                depends = True
            for nxt in range(8):
                joint = mass * law[nxt]
                if joint == 0 or marginal[nxt] == 0 or law[nxt] == 0:
                    continue
                bits += float(joint) * math.log2(float(law[nxt] / marginal[nxt]))
    return {"bits": bits, "depends": depends}


def _cmi_pair_to_triad(table: list[dict[int, Fraction]], pi: list[Fraction]) -> dict:
    bits = 0.0
    depends = False
    for triad in (0, 1):
        mass_triad = sum((pi[pair_state | (triad << 3)] for pair_state in range(8)), Fraction(0))
        if mass_triad == 0:
            continue
        marginal = [Fraction(0), Fraction(0)]
        rows = []
        masses = []
        for pair_state in range(8):
            source = pair_state | (triad << 3)
            mass = pi[source]
            law = [Fraction(0), Fraction(0)]
            for triad_next in (0, 1):
                step = Fraction(0)
                for nxt in range(8):
                    step += _prob(table, source, nxt | (triad_next << 3))
                law[triad_next] = step
                if mass:
                    marginal[triad_next] += mass * step
            rows.append(law)
            masses.append(mass)
        marginal = [value / mass_triad for value in marginal]
        for law, mass in zip(rows, masses):
            if mass == 0:
                continue
            if law[0] != marginal[0] or law[1] != marginal[1]:
                depends = True
            for triad_next in (0, 1):
                joint = mass * law[triad_next]
                if joint == 0 or marginal[triad_next] == 0 or law[triad_next] == 0:
                    continue
                bits += float(joint) * math.log2(float(law[triad_next] / marginal[triad_next]))
    return {"bits": bits, "depends": depends}


def trajectory_flags(kernel: Kernel) -> dict:
    """Support-level detector for a cross-order sequence.

    The sequence is a triadic toggle, then a later pairwise edge loss, then
    a pairwise class. At N=3 that class is the edge count. ``edge_count_differs``
    is recorded and is not called a new organisation.
    """
    _require_n3_layout(kernel)
    succ: list[list[int]] = []
    for state in range(16):
        row = []
        if not kernel.deadlock[state]:
            for nxt, prob in kernel.successors[state]:
                if prob > 0 and nxt != state:
                    row.append(nxt)
        succ.append(row)
    sequence = False
    differs = False
    formation_loss = False
    for state in range(16):
        for nxt in succ[state]:
            if (state ^ nxt) != (1 << 3):
                continue
            before = _pair_popcount(state)
            formed = ((state >> 3) & 1) == 0
            seen = {(nxt, False, False)}
            queue = deque([(nxt, False, False)])
            while queue:
                here, seen_loss, loss_while = queue.popleft()
                for follow in succ[here]:
                    loss = _pair_popcount(follow) < _pair_popcount(here)
                    new_loss = seen_loss or loss
                    new_while = loss_while or (loss and ((here >> 3) & 1) == 1)
                    if new_loss:
                        sequence = True
                        if _pair_popcount(follow) != before:
                            differs = True
                        if formed and new_while and _pair_popcount(follow) != before:
                            formation_loss = True
                    node = (follow, new_loss, new_while)
                    if node not in seen:
                        seen.add(node)
                        queue.append(node)
    return {
        "cross_order_sequence": sequence,
        "edge_count_differs": differs,
        "isomorphic_only": sequence and not differs,
        "formation_then_loss_edge_count_differs": formation_loss,
        "same_cardinality_nonisomorphic": False,
    }


def _rho_baselines(rho: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return (Fraction(1), Fraction(1), Fraction(1), rho)


def kernel_at_rho(n: int, constraints, factors, slots, rho: Fraction) -> Kernel:
    return build_kernel(
        n,
        Choreography(0, 0, tuple(constraints)),
        factors,
        relation_slots=slots,
        baseline_weights=_rho_baselines(rho),
    )


def coupling_report(kernel: Kernel, constraints, indexes: dict) -> dict:
    """One canonical set: reducibility, coarse-grained memory, and information."""
    tables = indexes.get("graph_tables") or RelabelTables(3)
    pi = _stationary(kernel)
    reducibility = classify_reducibility(kernel, indexes, tables)
    memory = emergent_memory_tv(kernel, pi)
    info = information_flow(kernel, pi)
    flags = trajectory_flags(kernel)
    n_pairs = pair_slot_count(kernel.n)
    return {
        "cross_order_class": set_cross_order_class(constraints, n_pairs),
        "reducibility_class": reducibility["class"],
        "reducibility": reducibility,
        "emergent_memory_tv": memory,
        "emergent_memory_tv_exact": _text(memory),
        "emergent_memory": int(memory > 0),
        "triad_predicts_next_pair": int(info["triad_predicts_next_pair"]),
        "pair_predicts_next_triad": int(info["pair_predicts_next_triad"]),
        "cmi_triad_to_pair_bits": info["cmi_triad_to_pair_bits"],
        "cmi_pair_to_triad_bits": info["cmi_pair_to_triad_bits"],
        "rate_competition": int(reducibility["rate_competition"]),
        "trajectory": flags,
        "pairwise_jump_tv_exact": reducibility["pairwise_jump_tv_exact"],
        "jump_support_outside_index": reducibility["jump_support_outside_index"],
        "jump_qualitative_outside_index": reducibility["jump_qualitative_outside_index"],
    }


def fresh_higher_order(indexes: dict | None = None) -> dict:
    reducibility = {name: 0 for name in _REDUCIBILITY}
    box = {
        "sets_by_class": {name: 0 for name in _CLASSES},
        "kernel_ids_by_class": {name: _IdList() for name in _CLASSES},
        "support_ids_by_class": {name: _IdList() for name in _CLASSES},
        "qualitative_ids_by_class": {name: _IdList() for name in _CLASSES},
        "reducibility": dict(reducibility),
        "reducibility_by_class": {name: dict(reducibility) for name in _CLASSES},
        "jump_support_outside_index": 0,
        "jump_qualitative_outside_index": 0,
        "jump_support_known": 0,
        "emergent_memory_sets": 0,
        "emergent_memory_max_tv": "0/1",
        "triad_predicts_pair_sets": 0,
        "pair_predicts_triad_sets": 0,
        "rate_competition_sets": 0,
        "rate_competition_and_pair_predicts_triad": 0,
        "trajectory": {
            "cross_order_sequence": 0,
            "edge_count_differs": 0,
            "isomorphic_only": 0,
            "formation_then_loss_edge_count_differs": 0,
            "same_cardinality_nonisomorphic": 0,
        },
        "examples": {name: [] for name in list(_REDUCIBILITY) + ["emergent_memory", "formation_then_loss"]},
        "sensitivity": {"1/2": _fresh_sensitivity(), "2": _fresh_sensitivity()},
        "qualitative_ids": _IdList(),
        "comparison_domain": COMPARISON_DOMAIN,
        "n3_limitation": N3_LIMITATION,
        "kernel_index_present": None if indexes is None else indexes.get("kernel_index_present"),
        "support_index_present": None if indexes is None else indexes.get("support_index_present"),
        "qualitative_index_present": None if indexes is None else indexes.get("qualitative_index_present"),
    }
    return box


def _fresh_sensitivity() -> dict:
    return {
        "kernel_changed": 0,
        "support_changed": 0,
        "modal_changed": 0,
        "qualitative_changed": 0,
        "reducibility_changed": 0,
        "emergent_memory_changed": 0,
        "coupling_changed": 0,
        "qualitative_ids": _IdList(),
    }


def _keep(bucket: list, expressions, limit: int = 4) -> None:
    row = list(expressions)
    if row in bucket:
        return
    bucket.append(row)
    bucket.sort()
    del bucket[limit:]


def _max_fraction(left: str, right: str) -> str:
    first = Fraction(left)
    second = Fraction(right)
    winner = first if first >= second else second
    return f"{winner.numerator}/{winner.denominator}"


def note_higher_order(box: dict, report: dict, expressions, ids: dict) -> None:
    label = report["cross_order_class"]
    box["sets_by_class"][label] += 1
    box["reducibility"][report["reducibility_class"]] += 1
    box["reducibility_by_class"][label][report["reducibility_class"]] += 1
    if report["jump_support_outside_index"] is True:
        box["jump_support_outside_index"] += 1
    if report["jump_support_outside_index"] is not None:
        box["jump_support_known"] += 1
    if report["jump_qualitative_outside_index"] is True:
        box["jump_qualitative_outside_index"] += 1
    if report["emergent_memory"]:
        box["emergent_memory_sets"] += 1
        _keep(box["examples"]["emergent_memory"], expressions)
    box["emergent_memory_max_tv"] = _max_fraction(
        box["emergent_memory_max_tv"], report["emergent_memory_tv_exact"]
    )
    if report["triad_predicts_next_pair"]:
        box["triad_predicts_pair_sets"] += 1
    if report["pair_predicts_next_triad"]:
        box["pair_predicts_triad_sets"] += 1
    if report["rate_competition"]:
        box["rate_competition_sets"] += 1
        if report["pair_predicts_next_triad"] and report["reducibility_class"] != "IRREDUCIBLE_DYNAMIC_COUPLING":
            box["rate_competition_and_pair_predicts_triad"] += 1
    flags = report["trajectory"]
    for name in box["trajectory"]:
        if flags.get(name):
            box["trajectory"][name] += 1
    if flags.get("formation_then_loss_edge_count_differs"):
        _keep(box["examples"]["formation_then_loss"], expressions)
    _keep(box["examples"][report["reducibility_class"]], expressions)
    _add_id(box["qualitative_ids"], ids["qualitative_family"])
    _add_id(box["kernel_ids_by_class"][label], ids["exact_kernel_family"])
    _add_id(box["support_ids_by_class"][label], ids["support_family"])
    _add_id(box["qualitative_ids_by_class"][label], ids["qualitative_family"])


def _add_id(bucket: _IdList, value: str) -> None:
    if value not in bucket.seen:
        bucket.seen.add(value)
        bucket.append(value)


def note_sensitivity(box: dict, rho_key: str, primary_ids: dict, other_ids: dict, primary_report: dict, other_report: dict) -> None:
    slot = box["sensitivity"][rho_key]
    if other_ids["exact_kernel_family"] != primary_ids["exact_kernel_family"]:
        slot["kernel_changed"] += 1
    if other_ids["support_family"] != primary_ids["support_family"]:
        slot["support_changed"] += 1
    if other_ids["modal_family"] != primary_ids["modal_family"]:
        slot["modal_changed"] += 1
    if other_ids["qualitative_family"] != primary_ids["qualitative_family"]:
        slot["qualitative_changed"] += 1
    if other_report["reducibility_class"] != primary_report["reducibility_class"]:
        slot["reducibility_changed"] += 1
    if other_report["emergent_memory"] != primary_report["emergent_memory"]:
        slot["emergent_memory_changed"] += 1
    primary_coupling = primary_report["reducibility_class"] == "IRREDUCIBLE_DYNAMIC_COUPLING"
    other_coupling = other_report["reducibility_class"] == "IRREDUCIBLE_DYNAMIC_COUPLING"
    if primary_coupling != other_coupling:
        slot["coupling_changed"] += 1
    _add_id(slot["qualitative_ids"], other_ids["qualitative_family"])


def serialise_higher_order(box: dict) -> dict:
    def convert(value):
        if isinstance(value, list) and hasattr(value, "seen"):
            return sorted(value.seen)
        if isinstance(value, dict):
            return {key: convert(item) for key, item in value.items()}
        if isinstance(value, list):
            return [convert(item) for item in value]
        return value

    return convert(box)


def _as_id_list(values) -> _IdList:
    return _IdList(values or ())


def absorb_higher_order(dest: dict, src: dict) -> None:
    if "sets_by_class" not in dest:
        fresh = fresh_higher_order()
        dest.update(fresh)
        dest["kernel_ids_by_class"] = {name: _as_id_list([]) for name in _CLASSES}
        dest["support_ids_by_class"] = {name: _as_id_list([]) for name in _CLASSES}
        dest["qualitative_ids_by_class"] = {name: _as_id_list([]) for name in _CLASSES}
        dest["qualitative_ids"] = _as_id_list([])
        for key in dest["sensitivity"]:
            dest["sensitivity"][key]["qualitative_ids"] = _as_id_list([])
    for name, count in src.get("sets_by_class", {}).items():
        dest["sets_by_class"][name] = dest["sets_by_class"].get(name, 0) + count
    for name, count in src.get("reducibility", {}).items():
        dest["reducibility"][name] = dest["reducibility"].get(name, 0) + count
    for label, row in src.get("reducibility_by_class", {}).items():
        dest_row = dest["reducibility_by_class"].setdefault(label, {name: 0 for name in _REDUCIBILITY})
        for name, count in row.items():
            dest_row[name] = dest_row.get(name, 0) + count
    for name in (
        "jump_support_outside_index",
        "jump_qualitative_outside_index",
        "jump_support_known",
        "emergent_memory_sets",
        "triad_predicts_pair_sets",
        "pair_predicts_triad_sets",
        "rate_competition_sets",
        "rate_competition_and_pair_predicts_triad",
    ):
        dest[name] = dest.get(name, 0) + src.get(name, 0)
    dest["emergent_memory_max_tv"] = _max_fraction(
        dest.get("emergent_memory_max_tv", "0/1"), src.get("emergent_memory_max_tv", "0/1")
    )
    for name, count in src.get("trajectory", {}).items():
        dest["trajectory"][name] = dest["trajectory"].get(name, 0) + count
    for name, rows in src.get("examples", {}).items():
        bucket = dest["examples"].setdefault(name, [])
        for row in rows:
            _keep(bucket, row)
    for name in _CLASSES:
        for kind in ("kernel_ids_by_class", "support_ids_by_class", "qualitative_ids_by_class"):
            dest_bucket = dest[kind].setdefault(name, [])
            if not hasattr(dest_bucket, "seen"):
                replacement = _as_id_list(dest_bucket)
                dest[kind][name] = replacement
                dest_bucket = replacement
            for value in src.get(kind, {}).get(name, []):
                _add_id(dest_bucket, value)
    qual = dest.get("qualitative_ids", [])
    if not hasattr(qual, "seen"):
        qual = _as_id_list(qual)
        dest["qualitative_ids"] = qual
    for value in src.get("qualitative_ids", []):
        _add_id(qual, value)
    for rho, row in src.get("sensitivity", {}).items():
        slot = dest["sensitivity"].setdefault(rho, _fresh_sensitivity())
        for name in (
            "kernel_changed",
            "support_changed",
            "modal_changed",
            "qualitative_changed",
            "reducibility_changed",
            "emergent_memory_changed",
            "coupling_changed",
        ):
            slot[name] = slot.get(name, 0) + row.get(name, 0)
        ids = slot.get("qualitative_ids", [])
        if not hasattr(ids, "seen"):
            ids = _as_id_list(ids)
            slot["qualitative_ids"] = ids
        for value in row.get("qualitative_ids", []):
            _add_id(ids, value)
    for name in ("kernel_index_present", "support_index_present", "qualitative_index_present"):
        if src.get(name) is not None:
            dest[name] = src[name]
    dest["comparison_domain"] = src.get("comparison_domain", dest.get("comparison_domain"))
    dest["n3_limitation"] = src.get("n3_limitation", dest.get("n3_limitation"))


def higher_order_science(box: dict) -> dict:
    """Counts and hashes. Full id lists stay in the cell summary."""
    serial = serialise_higher_order(box)

    def digest(values) -> str:
        payload = "\n".join(values)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    sensitivity = {}
    primary = set(serial.get("qualitative_ids") or [])
    for rho, row in serial.get("sensitivity", {}).items():
        other = set(row.get("qualitative_ids") or [])
        sensitivity[rho] = {
            "kernel_changed": row["kernel_changed"],
            "support_changed": row["support_changed"],
            "modal_changed": row["modal_changed"],
            "qualitative_changed": row["qualitative_changed"],
            "reducibility_changed": row["reducibility_changed"],
            "emergent_memory_changed": row["emergent_memory_changed"],
            "coupling_changed": row["coupling_changed"],
            "qualitative_family_count": len(other),
            "qualitative_families_equal_primary": other == primary,
        }
    return {
        "sets_by_class": serial["sets_by_class"],
        "reducibility": serial["reducibility"],
        "reducibility_by_class": serial["reducibility_by_class"],
        "jump_support_outside_index": serial["jump_support_outside_index"],
        "jump_qualitative_outside_index": serial["jump_qualitative_outside_index"],
        "emergent_memory_sets": serial["emergent_memory_sets"],
        "emergent_memory_max_tv": serial["emergent_memory_max_tv"],
        "triad_predicts_pair_sets": serial["triad_predicts_pair_sets"],
        "pair_predicts_triad_sets": serial["pair_predicts_triad_sets"],
        "rate_competition_sets": serial["rate_competition_sets"],
        "rate_competition_and_pair_predicts_triad": serial["rate_competition_and_pair_predicts_triad"],
        "trajectory": serial["trajectory"],
        "sensitivity": sensitivity,
        "qualitative_family_count": len(serial.get("qualitative_ids") or []),
        "qualitative_ids_sha256": digest(serial.get("qualitative_ids") or []),
        "kernel_ids_sha256": digest(
            [
                f"{label}:{value}"
                for label, values in sorted(serial.get("kernel_ids_by_class", {}).items())
                for value in values
            ]
        ),
        "comparison_domain": serial.get("comparison_domain"),
        "kernel_index_present": serial.get("kernel_index_present"),
        "support_index_present": serial.get("support_index_present"),
        "qualitative_index_present": serial.get("qualitative_index_present"),
        "n3_limitation": serial.get("n3_limitation"),
    }


def clear_index_cache() -> None:
    global _INDEX_CACHE
    _INDEX_CACHE = None
