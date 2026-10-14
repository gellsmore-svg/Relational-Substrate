"""Two remembered pair events; exact, sparse SECOND-RECENT analysis."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations

from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.exact import period_of, strongly_connected_components
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import (
    HistoryError, PRECISION, RecentReversal, analytic_row_js, analytic_shape_js,
    entropy_information, js, mutual_information,
)
from rs_constraint_lab.memory_clocks import _solve_fraction_columns
from rs_constraint_lab.predictive_state import balance_gap, conditional_information, row_gap
from rs_constraint_lab.refinement import (
    canonical_partition, lumpability, partition_from_labels, refine, signatures,
)
from rs_constraint_lab.state import edges

CLOCK = "pair-event epoch"
VERSION = "generation-008l-history-depth/v2-validation"


def digest(value):
    return sha256_bytes(canonical_json(value).encode())


@dataclass(frozen=True, slots=True)
class DepthTwoState:
    material: int
    h1: int | None = None
    h2: int | None = None


@dataclass(frozen=True)
class SecondRecent:
    multiplier: F
    pair_slots: int = 6
    triad_slots: int = 4

    def __post_init__(self):
        # The old positive selector arithmetic is reused; only update semantics differ.
        selector = RecentReversal(self.multiplier, self.pair_slots, self.triad_slots)
        object.__setattr__(self, "multiplier", selector.multiplier)

    @property
    def width(self):
        return self.pair_slots + self.triad_slots

    @property
    def size(self):
        return (1 << self.pair_slots) * self.pair_slots ** 2

    def validate_history(self, h1, h2):
        selector = RecentReversal(self.multiplier, self.pair_slots, self.triad_slots)
        selector.validate_history(h1)
        selector.validate_history(h2)
        if h1 is None and h2 is not None:
            raise HistoryError("second pair cannot exist before a first pair")

    def validate_state(self, state):
        self.validate_history(state.h1, state.h2)
        if type(state.material) is not int or not 0 <= state.material < 1 << self.width:
            raise HistoryError("material state outside unchanged relation space")

    def advance(self, state, event):
        self.validate_state(state)
        if type(event) is not int or not 0 <= event < self.width:
            raise HistoryError("event outside ordinary toggle support")
        h1, h2 = (event, state.h1) if event < self.pair_slots else (state.h1, state.h2)
        return DepthTwoState(state.material ^ (1 << event), h1, h2)

    @lru_cache(maxsize=None, typed=True)
    def full_probabilities(self, h1, h2):
        self.validate_history(h1, h2)
        return RecentReversal(self.multiplier, self.pair_slots, self.triad_slots).full_probabilities(h2)

    @lru_cache(maxsize=None, typed=True)
    def pair_probabilities(self, h1, h2):
        full = self.full_probabilities(h1, h2)
        pair_mass = sum(full[:self.pair_slots])
        return tuple(value / pair_mass for value in full[:self.pair_slots])

    def full_row(self, state):
        self.validate_state(state)
        return {self.advance(state, event): value
                for event, value in enumerate(self.full_probabilities(state.h1, state.h2))}

    def epoch_index(self, mask, h1, h2):
        self.validate_history(h1, h2)
        if h1 is None or h2 is None or type(mask) is not int or not 0 <= mask < 1 << self.pair_slots:
            raise HistoryError("recurrent index needs a mask and two pair slots")
        return (mask * self.pair_slots + h1) * self.pair_slots + h2

    def epoch_state(self, index):
        if type(index) is not int or not 0 <= index < self.size:
            raise HistoryError("pair-epoch index out of range")
        rest, h2 = divmod(index, self.pair_slots)
        mask, h1 = divmod(rest, self.pair_slots)
        return mask, h1, h2

    def epoch_kernel(self):
        return [
            {self.epoch_index(mask ^ (1 << event), event, h1): value
             for event, value in enumerate(self.pair_probabilities(h1, h2))}
            for mask, h1, h2 in map(self.epoch_state, range(self.size))
        ]

    def direct_next_pair_slots(self, mask, h1, h2):
        """Independent finite absorption solve from actual full-event rows."""
        if type(mask) is not int or not 0 <= mask < 1 << self.pair_slots:
            raise HistoryError("pair mask out of range")
        self.validate_history(h1, h2)
        size = 1 << self.triad_slots
        matrix = [[F(i == j) for j in range(size)] for i in range(size)]
        rhs = [[F(0) for _ in range(size)] for _ in range(self.pair_slots)]
        for hidden in range(size):
            state = DepthTwoState(mask | (hidden << self.pair_slots), h1, h2)
            for target, probability in self.full_row(state).items():
                event = (state.material ^ target.material).bit_length() - 1
                if event < self.pair_slots:
                    rhs[event][hidden] += probability
                else:
                    if (target.h1, target.h2) != (h1, h2):
                        raise HistoryError("triad excursion changed pair history")
                    matrix[hidden][target.material >> self.pair_slots] -= probability
        columns = _solve_fraction_columns(matrix, rhs)
        return [[columns[event][hidden] for event in range(self.pair_slots)] for hidden in range(size)]


def analyse_witness(model):
    if (model.pair_slots, model.triad_slots) != (6, 4):
        raise HistoryError("canonical witness is N4 O3 only")
    a, b, c = (edges(4).index(pair) for pair in ((0, 1), (1, 2), (2, 3)))
    paths = []
    for events in ((a, b, c), (b, a, c)):
        state, full_mass, pair_mass = DepthTwoState(0), F(1), F(1)
        material_path = [state.material]
        for event in events:
            if state.material & (1 << event):
                raise HistoryError("canonical event is not formation")
            target = model.advance(state, event)
            full_mass *= model.full_row(state)[target]
            pair_mass *= model.pair_probabilities(state.h1, state.h2)[event]
            state = target
            material_path.append(state.material)
        paths.append({
            "events": events, "material_path": material_path,
            "endpoint": state, "path_full_probability": full_mass, "path_pair_probability": pair_mass,
        })
    left, right = [path["endpoint"] for path in paths]
    if left.material != right.material or left.h1 != right.h1 or left.h2 == right.h2:
        raise HistoryError("same-(X,h1), different-h2 endpoint control failed")
    if paths[0]["material_path"][-2:] != paths[1]["material_path"][-2:]:
        raise HistoryError("last two material masks disagree")
    if any(paths[0][key] != paths[1][key] for key in ("path_full_probability", "path_pair_probability")):
        raise HistoryError("path probabilities disagree")
    m = model.multiplier
    if paths[0]["path_full_probability"] != 1 / (100 * (m + 9)):
        raise HistoryError("full-clock path formula failed")
    if paths[0]["path_pair_probability"] != 1 / (36 * (m + 5)):
        raise HistoryError("pair-clock path formula failed")
    full = [model.full_probabilities(s.h1, s.h2) for s in (left, right)]
    pair = [model.pair_probabilities(s.h1, s.h2) for s in (left, right)]
    table, shapes, counts = pair_classes(), [], []
    for row in pair:
        shape, count = defaultdict(F), defaultdict(F)
        for event, value in enumerate(row):
            target = left.material ^ (1 << event)
            shape[table.name_of[target]] += value
            count[target.bit_count()] += value
        shapes.append(dict(sorted(shape.items())))
        counts.append(dict(sorted(count.items())))
    shape_labels = sorted(shapes[0].keys() | shapes[1].keys())
    shape_js = js([shapes[0].get(k, F(0)) for k in shape_labels],
                  [shapes[1].get(k, F(0)) for k in shape_labels])
    gaps = [abs(x - y) for x, y in zip(pair[0], pair[1])]
    changed = [i for i, gap in enumerate(gaps) if gap]
    if changed != ([] if m == 1 else [a, b]):
        raise HistoryError("row contradiction changed unexpected event coordinates")
    if counts[0] != counts[1] or counts[0] != {2: (m + 2) / (m + 5), 4: 3 / (m + 5)}:
        raise HistoryError("pure-shape edge-count control failed")
    expected_shapes = []
    for selected in (b, a):
        expected = defaultdict(F)
        for event in range(6):
            expected[table.name_of[left.material ^ (1 << event)]] += (m if event == selected else 1) / (m + 5)
        expected_shapes.append(dict(sorted(expected.items())))
    if shapes != expected_shapes:
        raise HistoryError("mechanical class projection disagrees with weights")
    information_gaps = [
        abs(js(*pair) - analytic_row_js(m, m + 5)),
        abs(js(*full) - analytic_row_js(m, m + 9)),
        abs(shape_js - analytic_shape_js(m)),
    ]
    return {
        "clock": CLOCK, "m": m, "controller": "SECOND-RECENT", "start_state": 0,
        "start_history": [None, None], "history_A_events": [a, b, c], "history_B_events": [b, a, c],
        "material_paths": [path["material_path"] for path in paths],
        "endpoint_state": left.material, "endpoint_pair_mask": left.material & 63,
        "endpoint_bytes_little_endian": list(left.material.to_bytes(2, "little")),
        "all_ten_bits": format(left.material, "010b"), "endpoint_history_A": [left.h1, left.h2],
        "endpoint_history_B": [right.h1, right.h2], "same_X": True, "same_h1": True,
        "path_full_probability_A": paths[0]["path_full_probability"],
        "path_full_probability_B": paths[1]["path_full_probability"],
        "path_pair_probability_A": paths[0]["path_pair_probability"],
        "path_pair_probability_B": paths[1]["path_pair_probability"],
        "ordinary_support": list(range(10)), "baseline_weights": [1] * 10, "ordinary_constraints": [],
        "full_rows": full, "pair_rows": pair, "changed_pair_slots": changed,
        "full_row_gap": max(abs(x-y) for x, y in zip(*full)), "pair_row_gap": max(gaps),
        "full_row_JS": str(js(*full)), "pair_row_JS": str(js(*pair)),
        "edge_count_laws": counts, "edge_count_JS": "0", "graph_class_laws": shapes,
        "graph_class_JS": str(shape_js), "information_formula_gap": str(max(information_gaps)),
        "strict_H1_lumpability": m == 1, "strict_H1_noncompilability": m != 1,
    }


def covariance(model):
    pairs, checks = edges(4), 0
    for perm in permutations(range(4)):
        mapping = [pairs.index(tuple(sorted((perm[a], perm[b])))) for a, b in pairs]
        for h1 in range(6):
            for h2 in range(6):
                original = model.pair_probabilities(h1, h2)
                transformed = model.pair_probabilities(mapping[h1], mapping[h2])
                for event in range(6):
                    if original[event] != transformed[mapping[event]]:
                        raise HistoryError("SECOND-RECENT covariance failed")
                    checks += 1
        for mask in range(64):
            mapped = sum(1 << mapping[e] for e in range(6) if mask & (1 << e))
            for event in range(6):
                target = mask ^ (1 << event)
                mapped_target = sum(1 << mapping[e] for e in range(6) if target & (1 << e))
                if mapped_target != mapped ^ (1 << mapping[event]):
                    raise HistoryError("ordinary toggle covariance failed")
                checks += 1
    return {"comparisons": checks, "exact": True}


def analyse_kernel(model):
    rows, n = model.epoch_kernel(), model.size
    if n != 2304:
        raise HistoryError("primary kernel is not the declared N4 representation")
    columns = [F(0)] * n
    pair_mass, hist_mass, pair_hist = [F(0)] * 64, [F(0)] * 36, defaultdict(F)
    material_joint = defaultdict(F)
    for source, row in enumerate(rows):
        if len(row) != 6 or sum(row.values()) != 1:
            raise HistoryError("pair epoch support/normalisation failure")
        p, i, j = model.epoch_state(source)
        pair_mass[p] += F(1, n)
        hist_mass[i * 6 + j] += F(1, n)
        pair_hist[p, i, j] += F(1, n)
        for target, value in row.items():
            columns[target] += value
            material_joint[p, model.epoch_state(target)[0]] += value / n
    if any(value != 1 for value in columns):
        raise HistoryError("uniform column balance failed")
    successors = [sorted(row.items()) for row in rows]
    components = strongly_connected_components(successors)
    if len(components) != 1:
        raise HistoryError("recurrent representation is not irreducible")
    period = period_of(components[0], successors)
    quotient_gaps = []
    for p in (0, 41, 63):
        for i, j in ((None, None), (0, None), (5, 0), (5, 3), (2, 2)):
            expected = model.pair_probabilities(i, j)
            for direct in model.direct_next_pair_slots(p, i, j):
                quotient_gaps.extend(abs(a-b) for a, b in zip(direct, expected))
    one_step_gap = max(abs(value - F(1, 384)) for value in material_joint.values())
    independence_gap = max(abs(mass - pair_mass[p] * hist_mass[i*6+j])
                           for (p, i, j), mass in pair_hist.items())
    if one_step_gap or independence_gap or max(quotient_gaps):
        raise HistoryError("stationary projection or full-to-pair quotient failed")
    edge_mass, class_mass = defaultdict(F), defaultdict(F)
    for p, mass in enumerate(pair_mass):
        edge_mass[p.bit_count()] += mass
        class_mass[pair_classes().name_of[p]] += mass
    return {
        "clock": CLOCK, "m": model.multiplier, "state_count": n, "transition_count": sum(map(len, rows)),
        "state_order": "index=(pair_mask*6+h1)*6+h2", "kernel": successors, "kernel_sha256": digest(successors),
        "stationary_weight_per_state": F(1, n), "stationary_residual": balance_gap([F(1,n)] * n, rows),
        "uniform_joint_gap": F(0), "column_sum_gap": max(abs(v-1) for v in columns),
        "pair_marginal": pair_mass, "history_pair_marginal": hist_mass,
        "history_pair_independence_gap": independence_gap, "edge_count_marginal": dict(edge_mass),
        "graph_class_marginal": dict(sorted(class_mass.items())), "stationary_one_step_H0_gap": one_step_gap,
        "communicating_classes": len(components), "unique_stationary": True, "period": period,
        "row_sum_gap": max(abs(sum(row.values())-1) for row in rows),
        "full_vs_pair_quotient_gap": max(quotient_gaps), "raw_triad_absorption_rows": len(quotient_gaps) // 6,
        "covariance": covariance(model),
    }


def analyse_refinement(model):
    rows = model.epoch_kernel()
    labels = [model.epoch_state(s)[0] for s in range(model.size)]
    initial = partition_from_labels(labels)
    result = refine(rows, initial)
    permutation = list(reversed(range(model.size)))
    inverse = {old: new for new, old in enumerate(permutation)}
    shuffled = [{inverse[t]: value for t, value in rows[old].items()} for old in permutation]
    reverse = refine(shuffled, partition_from_labels([labels[old] for old in permutation]))
    restored = canonical_partition([[permutation[s] for s in block] for block in reverse["stable_blocks"]], model.size)
    if restored != result["stable_blocks"]:
        raise HistoryError("refinement depends on state enumeration order")
    observed = signatures(rows, initial)
    first = partition_from_labels([(p, j) for p, i, j in map(model.epoch_state, range(model.size))])
    after_first = signatures(rows, first)
    counts, samples = Counter(), {}
    if model.multiplier != 1:
        for p in range(64):
            states = [model.epoch_index(p, i, j) for i in range(6) for j in range(6)]
            for left, right in combinations(states, 2):
                _, i, j = model.epoch_state(left)
                _, ii, jj = model.epoch_state(right)
                key = "different_h2_immediate" if j != jj else "same_h2_different_h1_later"
                va, vb = observed[left] if j != jj else after_first[left], observed[right] if j != jj else after_first[right]
                if va == vb:
                    raise HistoryError("compact merge-obstruction schema failed")
                counts[key] += 1
                samples.setdefault(key, {"state_A": left, "state_B": right, "signature_A": va, "signature_B": vb})
    membership = result["stable_blocks"]
    expected = initial if model.multiplier == 1 else tuple((s,) for s in range(model.size))
    return {
        "clock": CLOCK, "m": model.multiplier, "initial_block_count": len(initial),
        "block_counts_by_round": [len(initial)] + [r["after_count"] for r in result["refinement_chronology"]],
        "refinement_rounds": result["refinement_rounds"], "stable_block_count": len(membership),
        "stable_blocks": membership, "membership_sha256": digest(membership),
        "chronology": result["refinement_chronology"], "strong_lumpability_gap": result["strong_lumpability_gap"],
        "state_reordering_gap": F(0), "merge_obstruction_classes": dict(counts), "obstruction_samples": samples,
        "analytic_membership_gap": int(membership != expected),
        "generic_merge_certificates_sha256": digest(result["merge_obstructions"]),
        "generic_merge_certificate_count": len(result["merge_obstructions"]),
        "immediate_observed_rows_separate_all": result["distinct_next_observation_rows_within_current_observation"],
        "coarseness_basis": "CL-T52 universal-property induction; exhaustive same-observation separation schemas",
    }


def stationary_words(model):
    """Backward reconstruction from current register, then one full sparse step."""
    triples, quadruples = defaultdict(F), defaultdict(F)
    adjacent, lagged = [[F(0) for _ in range(6)] for _ in range(6)], [[F(0) for _ in range(6)] for _ in range(6)]
    for state, row in enumerate(model.epoch_kernel()):
        p, i, j = model.epoch_state(state)
        prev, prevprev = p ^ (1 << i), p ^ (1 << i) ^ (1 << j)
        for target, probability in row.items():
            nxt, event, _ = model.epoch_state(target)
            mass = probability / model.size
            triples[prev, p, nxt] += mass
            quadruples[prevprev, prev, p, nxt] += mass
            adjacent[i][event] += mass
            lagged[j][event] += mass
    return dict(sorted(triples.items())), dict(sorted(quadruples.items())), adjacent, lagged


def forward_quadruples(model):
    rows, answer = model.epoch_kernel(), defaultdict(F)
    masks = [model.epoch_state(s)[0] for s in range(model.size)]
    for a, row in enumerate(rows):
        for b, x in row.items():
            for c, y in rows[b].items():
                for d, z in rows[c].items():
                    answer[masks[a], masks[b], masks[c], masks[d]] += x * y * z / model.size
    return dict(sorted(answer.items()))


def analyse_temporal(model):
    triples, quads, adjacent, lagged = stationary_words(model)
    forward = forward_quadruples(model)
    if quads != forward or sum(quads.values()) != 1 or sum(triples.values()) != 1:
        raise HistoryError("independent stationary word construction mismatch")
    order2, independent = conditional_information(triples)
    conditional_quads = {(a, (b,c), d): mass for (a,b,c,d), mass in quads.items()}
    order3, _ = conditional_information(conditional_quads)
    lag_mi = mutual_information(lagged)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        formula = entropy_information(model.multiplier/(model.multiplier+5), 1/(model.multiplier+5), 6)
        formula_gap = max(abs(lag_mi-formula), abs(order3-formula))
    if not independent or any(v != F(1,36) for row in adjacent for v in row):
        raise HistoryError("adjacent exact null failed; do not round it away")
    if any(mass != F(1,2304) for mass in triples.values()):
        raise HistoryError("stationary material triple law differs from H0")
    suffix_rows, witness, sufficiency_gap = defaultdict(dict), None, F(0)
    for (p2,p1,p,nxt), mass in quads.items():
        suffix_rows[p2,p1,p][nxt] = mass
    next_rows = {}
    groups = defaultdict(list)
    for suffix, row in suffix_rows.items():
        total = sum(row.values())
        conditional = {nxt: mass/total for nxt, mass in row.items()}
        p2,p1,p = suffix
        h2 = (p2 ^ p1).bit_length()-1
        h1 = (p1 ^ p).bit_length()-1
        actual = {p ^ (1 << e): v for e,v in enumerate(model.pair_probabilities(h1,h2))}
        sufficiency_gap = max(sufficiency_gap, row_gap(conditional, actual))
        next_rows[suffix] = conditional
        groups[p1,p].append(suffix)
    for suffixes in groups.values():
        for a,b in combinations(suffixes,2):
            if next_rows[a] != next_rows[b]:
                witness = {"last_two_masks": list(a[1:]), "earlier_A": a[0], "earlier_B": b[0],
                           "next_row_A": next_rows[a], "next_row_B": next_rows[b],
                           "positive_triple_mass_A": sum(suffix_rows[a].values()),
                           "positive_triple_mass_B": sum(suffix_rows[b].values())}
                break
        if witness:
            break
    if sufficiency_gap or (witness is None) != (model.multiplier == 1):
        raise HistoryError("Markov-order witness or sufficiency failed")
    return {
        "clock": CLOCK, "m": model.multiplier, "precision_decimal_digits": PRECISION, "unit": "nats",
        "adjacent_event_joint": adjacent, "lag_two_event_joint": lagged,
        "adjacent_event_MI": "0", "adjacent_event_independence_exact": True,
        "lag_two_repeat": sum(lagged[e][e] for e in range(6)), "lag_two_event_MI": str(lag_mi),
        "order_two_mask_CMI": "0", "order_two_mask_independence_exact": independent,
        "order_three_mask_CMI": str(order3), "information_formula_gap": str(formula_gap),
        "stationary_triple_count": len(triples), "stationary_quadruple_count": len(quads),
        "stationary_triples": [{"word": w, "probability": v} for w,v in triples.items()],
        "stationary_quadruples": [{"word": w, "probability": v} for w,v in quads.items()],
        "independent_forward_word_gap": F(0), "stationary_triples_H0_gap": F(0),
        "order_three_sufficiency_gap": sufficiency_gap, "order_two_failure_witness": witness,
        "pair_mask_markov_order": 1 if model.multiplier == 1 else 3,
        "event_slot_markov_order": 1 if model.multiplier == 1 else 2,
        "event_slot_neutral_iid": model.multiplier == 1,
    }
