"""Exact predictive refinements of the unchanged RECENT-REVERSAL process."""

from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache
from itertools import permutations
from math import comb

from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import HistoryError, PRECISION, RecentReversal, entropy_information
from rs_constraint_lab.refinement import block_index, canonical_partition, lumpability, partition_from_labels, refine
from rs_constraint_lab.state import edges

PROJECTIONS = ("labelled_mask", "graph_class", "edge_count", "parity")
CLOCK = "pair-event epoch"
SIZE = 384


def observation(projection, mask):
    if projection == "labelled_mask":
        return mask
    if projection == "graph_class":
        return pair_classes().name_of[mask]
    if projection == "edge_count":
        return mask.bit_count()
    if projection == "parity":
        return mask.bit_count() % 2
    raise HistoryError("unknown material projection")


def observation_labels(projection):
    return tuple(observation(projection, state // 6) for state in range(SIZE))


def balance_gap(pi, rows):
    incoming = [Fraction(0)] * len(rows)
    for source, row in enumerate(rows):
        for target, mass in row.items():
            incoming[target] += pi[source] * mass
    return max(abs(a - b) for a, b in zip(pi, incoming))


@cache
def geometry():
    pairs = edges(4)
    index = {pair: i for i, pair in enumerate(pairs)}
    edge_maps = tuple(tuple(index[tuple(sorted((perm[a], perm[b])))] for a, b in pairs)
                      for perm in permutations(range(4)))
    mask_maps = tuple(tuple(sum(1 << mapping[e] for e in range(6) if p & (1 << e))
                            for p in range(64)) for mapping in edge_maps)
    canonical = [min(masks[p] * 6 + mapping[h] for masks, mapping in zip(mask_maps, edge_maps))
                 for p in range(64) for h in range(6)]
    orbit_blocks = partition_from_labels(canonical)
    return edge_maps, mask_maps, orbit_blocks


def edge_role_partition():
    return partition_from_labels(tuple((p.bit_count(), (p >> h) & 1) for p in range(64) for h in range(6)))


def current_triples(rows, projection):
    triples = defaultdict(Fraction)
    for state, row in enumerate(rows):
        p, h = divmod(state, 6)
        prefix = (observation(projection, p ^ (1 << h)), observation(projection, p))
        for target, mass in row.items():
            triples[prefix + (observation(projection, target // 6),)] += mass / SIZE
    return dict(sorted(triples.items()))


def forward_triples(rows, projection):
    triples = defaultdict(Fraction)
    for source, row in enumerate(rows):
        for middle, first in row.items():
            for target, second in rows[middle].items():
                word = tuple(observation(projection, state // 6) for state in (source, middle, target))
                triples[word] += first * second / SIZE
    return dict(sorted(triples.items()))


def decimal_fraction(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


@cache
def ln_fraction(value):
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return decimal_fraction(value).ln()


def information_term(mass, ratio):
    if not mass or ratio == 1:
        return Decimal(0)
    return decimal_fraction(mass) * ln_fraction(ratio)


def conditional_information(triples):
    ab, bc, middle = defaultdict(Fraction), defaultdict(Fraction), defaultdict(Fraction)
    for (a, b, c), mass in triples.items():
        ab[a, b] += mass
        bc[b, c] += mass
        middle[b] += mass
    with localcontext() as ctx:
        ctx.prec = PRECISION
        value = Decimal(0)
        exact_independence = True
        for (a, b, c), mass in triples.items():
            ratio = mass * middle[b] / (ab[a, b] * bc[b, c])
            exact_independence &= ratio == 1
            value += information_term(mass, ratio)
        return +value, exact_independence


def observed_rows(quotient, stable, labels):
    result = []
    for row in quotient:
        masses = defaultdict(Fraction)
        for target, mass in row.items():
            masses[labels[stable[target][0]]] += mass
        result.append(dict(masses))
    return result


def quotient_information(pi, quotient, stable, labels):
    rows = observed_rows(quotient, stable, labels)
    joint, marginal = defaultdict(lambda: defaultdict(Fraction)), defaultdict(Fraction)
    for block, mass in enumerate(pi):
        y = labels[stable[block][0]]
        marginal[y] += mass
        for target, value in rows[block].items():
            joint[y][target] += mass * value
    with localcontext() as ctx:
        ctx.prec = PRECISION
        information = Decimal(0)
        for block, mass in enumerate(pi):
            y = labels[stable[block][0]]
            for target, value in rows[block].items():
                information += information_term(mass * value, value * marginal[y] / joint[y][target])
        return +information


def stationary_observed_rows(rows, labels):
    joint, marginal = defaultdict(lambda: defaultdict(Fraction)), defaultdict(Fraction)
    for source, row in enumerate(rows):
        y = labels[source]
        marginal[y] += Fraction(1, SIZE)
        for target, mass in row.items():
            joint[y][labels[target]] += mass / SIZE
    return {y: {target: value / marginal[y] for target, value in sorted(row.items())}
            for y, row in sorted(joint.items())}


def row_gap(a, b):
    return max((abs(a.get(key, 0) - b.get(key, 0)) for key in a.keys() | b.keys()), default=Fraction(0))


def synchronization(rows, result, projection):
    labels = observation_labels(projection)
    stable = result["stable_blocks"]
    state_to_block = result["state_to_block"]
    quotient = tuple(dict(row) for row in result["quotient_kernel"])
    next_rows = observed_rows(quotient, stable, labels)
    pairs = defaultdict(set)
    masses = defaultdict(Fraction)
    for state in range(SIZE):
        p, h = divmod(state, 6)
        pair = observation(projection, p ^ (1 << h)), labels[state]
        pairs[pair].add(state_to_block[state])
        masses[pair] += Fraction(1, SIZE)
    collisions = [{"pair": pair, "blocks": sorted(blocks)} for pair, blocks in sorted(pairs.items()) if len(blocks) != 1]
    if collisions:
        raise HistoryError("two observations fail to synchronize declared refinement")
    pair_rows = {pair: next_rows[next(iter(blocks))] for pair, blocks in sorted(pairs.items())}
    gap, witness = Fraction(0), None
    ordered = list(pair_rows)
    for index, left in enumerate(ordered):
        for right in ordered[index + 1:]:
            if left[1] != right[1]:
                continue
            difference = row_gap(pair_rows[left], pair_rows[right])
            if difference > gap:
                gap = difference
                target = next(target for target in sorted(pair_rows[left].keys() | pair_rows[right].keys())
                              if pair_rows[left].get(target, 0) != pair_rows[right].get(target, 0))
                witness = {"current_observation": left[1], "previous_A": left[0], "previous_B": right[0],
                           "next_observation": target, "probability_A": pair_rows[left].get(target, Fraction(0)),
                           "probability_B": pair_rows[right].get(target, Fraction(0)),
                           "positive_pair_mass_A": masses[left], "positive_pair_mass_B": masses[right]}
    single = result["initial_block_count"] == result["stable_block_count"]
    return {
        "projection": projection, "legal_ordered_observation_pairs": len(pairs),
        "predictive_states": len(stable), "pair_determines_block": True,
        "bijection_verified": len(pairs) == len(stable) and len({next(iter(s)) for s in pairs.values()}) == len(stable),
        "synchronization_length": 1 if single else 2,
        "markov_order": 2 if gap else 1, "order1_witness_gap": gap, "order1_witness": witness,
        "order2_sufficiency_gap": Fraction(0),
        "sufficiency_basis": "the last two observations determine a strongly lumpable predictive block",
        "order0_excluded_by_stationary_parity_alternation": True,
        "ordered_pair_atlas": [
            {"previous": pair[0], "current": pair[1], "predictive_block": next(iter(pairs[pair])),
             "stationary_probability": masses[pair], "next_observation_row": sorted(pair_rows[pair].items())}
            for pair in ordered
        ],
    }


def analytic_edge_quotient(model):
    rows = model.epoch_kernel()
    blocks = edge_role_partition()
    mapping = block_index(blocks, SIZE)
    labels = tuple(((block[0] // 6).bit_count(), ((block[0] // 6) >> (block[0] % 6)) & 1) for block in blocks)
    index = {label: i for i, label in enumerate(labels)}
    quotient, gap = lumpability(rows, blocks)
    records = []
    for source, (k, r) in enumerate(labels):
        down = (k + (model.multiplier - 1) * r) / (model.multiplier + 5)
        up = (6 - k + (model.multiplier - 1) * (1 - r)) / (model.multiplier + 5)
        expected = {}
        if down:
            expected[index[k - 1, 0]] = down
        if up:
            expected[index[k + 1, 1]] = up
        actual_mass = Fraction(len(blocks[source]), SIZE)
        expected_mass = Fraction(comb(5, k - r), 64)
        if expected != quotient[source] or actual_mass != expected_mass:
            raise HistoryError("analytic edge-role row/stationary formula failed")
        records.append({"k": k, "r": r, "block": source, "dissolution": down, "formation": up,
                        "stationary_mass": actual_mass, "binomial_formula_mass": expected_mass})
    return {"state_count": len(blocks), "blocks": blocks, "rows": records,
            "quotient_kernel": [sorted(row.items()) for row in quotient], "exact_gap": gap}


def analyse_projection(model, projection):
    if model.pair_slots != 6 or model.triad_slots != 4:
        raise HistoryError("primary predictive analysis is fixed N4/O3")
    rows = model.epoch_kernel()
    labels = observation_labels(projection)
    initial = partition_from_labels(labels)
    result = refine(rows, initial)
    stable = result["stable_blocks"]
    candidate = (tuple((state,) for state in range(SIZE)) if projection == "labelled_mask" else
                 geometry()[2] if projection == "graph_class" else
                 edge_role_partition() if projection == "edge_count" else initial)
    if model.multiplier == 1:
        candidate = initial
    if stable != canonical_partition(candidate, SIZE):
        raise HistoryError("independent analytic/symmetry partition differs: retain and diagnose, do not force counts")
    _, initial_gap = lumpability(rows, initial)
    pi = [Fraction(len(block), SIZE) for block in stable]
    quotient = [dict(row) for row in result["quotient_kernel"]]
    full_gap = balance_gap([Fraction(1, SIZE)] * SIZE, rows)
    stationary_gap = balance_gap(pi, quotient)
    if full_gap or stationary_gap:
        raise HistoryError("uniform full/pushed stationary balance failed")
    triples = current_triples(rows, projection)
    oracle = forward_triples(rows, projection)
    if triples != oracle:
        raise HistoryError("independent stationary triple constructions differ")
    sync = synchronization(rows, result, projection)
    information, independent = conditional_information(triples)
    quotient_info = quotient_information(pi, quotient, stable, labels)
    current_rows = stationary_observed_rows(rows, labels)
    baseline_rows = stationary_observed_rows(RecentReversal(Fraction(1)).epoch_kernel(), labels)
    one_step_gap = max(row_gap(current_rows[y], baseline_rows[y]) for y in current_rows)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        information_gap = abs(information - quotient_info)
        event_formula = entropy_information(model.multiplier / (model.multiplier + 5),
                                            Fraction(1) / (model.multiplier + 5), 6) if projection == "labelled_mask" else None
        formula_gap = abs(information - event_formula) if event_formula is not None else None
    reverse_rows = [{SIZE - 1 - target: mass for target, mass in rows[SIZE - 1 - source].items()} for source in range(SIZE)]
    reverse_initial = partition_from_labels(tuple(labels[SIZE - 1 - source] for source in range(SIZE)))
    reordered = refine(reverse_rows, reverse_initial)
    restored = canonical_partition(tuple(tuple(SIZE - 1 - state for state in block) for block in reordered["stable_blocks"]), SIZE)
    if restored != stable or one_step_gap or information_gap > Decimal("1e-25") or (formula_gap is not None and formula_gap > Decimal("1e-25")):
        raise HistoryError("enumeration order, information identity or one-step equality failed")
    if model.multiplier == 1 and (not independent or information != 0 or initial_gap or stable != initial):
        raise HistoryError("neutral collapse/control failed")
    if projection == "parity" and (information != 0 or initial_gap or len(stable) != 2):
        raise HistoryError("parity erasure control failed")
    if not result["distinct_next_observation_rows_within_current_observation"]:
        raise HistoryError("particular-controller future-word minimality requires direct row separation")
    result.update({
        "projection": projection, "m": model.multiplier, "clock": CLOCK,
        "initial_strong_lumpability": initial_gap == 0, "initial_lumpability_gap": initial_gap,
        "stationary_mass": pi, "full_stationary_gap": full_gap, "quotient_stationary_gap": stationary_gap,
        "independent_route_membership_gap": Fraction(0), "state_reordering_gap": Fraction(0),
        "one_step_H0_gap": one_step_gap, "stationary_observed_rows": [
            {"current": y, "next": sorted(row.items())} for y, row in current_rows.items()],
        "synchronization": sync,
        "temporal_information": {"conditional_MI": str(information), "precision": PRECISION, "unit": "nats",
                                 "exact_conditional_independence": independent, "stationary_triple_count": len(triples),
                                 "independent_triple_gap": Fraction(0), "quotient_KL_value": str(quotient_info),
                                 "formula_enumeration_gap": str(information_gap),
                                 "event_MI_formula": None if event_formula is None else str(event_formula),
                                 "event_MI_formula_gap": None if formula_gap is None else str(formula_gap)},
        "stationary_triples": [{"word": word, "probability": mass} for word, mass in triples.items()],
        "H0_first_distinguishing_word_length": 3 if not independent else None,
        "all_order_erasure_proof": "parity_t=parity_0 xor (t mod 2)" if projection == "parity" else None,
    })
    if projection == "edge_count":
        result["analytic_edge_role_quotient"] = analytic_edge_quotient(model)
    return result


def orbit_atlas():
    edge_maps, mask_maps, blocks = geometry()
    table = pair_classes()
    state_orbit = block_index(blocks, SIZE)
    records = []
    for p in table.representatives:
        automorphisms = [mapping for mapping, masks in zip(edge_maps, mask_maps) if masks[p] == p]
        unseen = set(range(6))
        while unseen:
            h = min(unseen)
            members = sorted({mapping[h] for mapping in automorphisms})
            unseen.difference_update(members)
            orbit = state_orbit[p * 6 + h]
            graph_size = sum(value == p for value in table.canonical)
            mass = Fraction(graph_size * len(members), SIZE)
            if len(blocks[orbit]) != graph_size * len(members):
                raise HistoryError("independent automorphism/global S4 orbit construction differs")
            records.append({
                "history_orbit_id": orbit, "canonical_mask": p, "graph_class": table.name_of[p],
                "edge_count": p.bit_count(), "automorphism_group_size": len(automorphisms),
                "representative_history_slot": h, "representative_pair": edges(4)[h],
                "pair_slot_orbit_members": members, "pair_slot_orbit_size": len(members),
                "augmented_orbit_size": len(blocks[orbit]), "present": bool(p & (1 << h)),
                "predecessor_class": table.name_of[p ^ (1 << h)],
                "remembered_toggle_next_class": table.name_of[p ^ (1 << h)],
                "six_next_class_counts": dict(sorted(Counter(table.name_of[p ^ (1 << e)] for e in range(6)).items())),
                "stationary_mass": mass,
            })
    if len(records) != len(blocks) or len({r["history_orbit_id"] for r in records}) != len(blocks):
        raise HistoryError("automorphism atlas does not cover each global orbit")
    return {"clock": CLOCK, "state_count": SIZE, "orbit_count": len(blocks),
            "blocks": blocks, "orbit_atlas": records,
            "class_orbit_counts": [{"canonical_mask": p, "roles": sum(r["canonical_mask"] == p for r in records)}
                                   for p in table.representatives]}


def covariance(model):
    rows = model.epoch_kernel()
    edge_maps, mask_maps, _ = geometry()
    for mapping, masks in zip(edge_maps, mask_maps):
        transform = tuple(masks[p] * 6 + mapping[h] for p in range(64) for h in range(6))
        for source, row in enumerate(rows):
            if {transform[target]: mass for target, mass in row.items()} != rows[transform[source]]:
                raise HistoryError("S4 must transform pair mask and remembered slot together")
    return {"m": model.multiplier, "clock": CLOCK, "exact_gap": Fraction(0),
            "comparisons": 24 * SIZE * 6}


def commute(results):
    records = []
    for grade in ("m025", "m1", "m4"):
        for source_name, target_name in zip(PROJECTIONS, PROJECTIONS[1:]):
            source, target = results[grade, source_name], results[grade, target_name]
            source_blocks, target_blocks = source["stable_blocks"], target["stable_blocks"]
            target_of = block_index(target_blocks, SIZE)
            source_to_target = []
            for block in source_blocks:
                destinations = {target_of[state] for state in block}
                if len(destinations) != 1:
                    raise HistoryError("predictive partitions do not form a refinement ladder")
                source_to_target.append(destinations.pop())
            q = [dict(row) for row in source["quotient_kernel"]]
            nested = partition_from_labels(source_to_target)
            aggregated, gap = lumpability(q, nested)
            # Canonical nested-block order follows the first source block, not target IDs.
            target_ids = [source_to_target[group[0]] for group in nested]
            for index, row in enumerate(aggregated):
                translated = {target_ids[destination]: mass for destination, mass in row.items()}
                if translated != dict(target["quotient_kernel"][target_ids[index]]):
                    raise HistoryError("commuting quotient rows differ from direct refinement")
            pushed = [Fraction(0)] * len(target_blocks)
            for block, mass in enumerate(source["stationary_mass"]):
                pushed[source_to_target[block]] += mass
            if pushed != target["stationary_mass"] or gap:
                raise HistoryError("quotient commutation/stationary pushforward failed")
            records.append({"grade": grade, "clock": CLOCK, "source_partition": source_name,
                            "target_partition": target_name, "source_states": len(source_blocks),
                            "target_states": len(target_blocks), "deterministic_quotient": True,
                            "strong_lumping": True, "source_to_target": source_to_target,
                            "exact_block_transition_gap": gap, "stationary_pushforward_gap": Fraction(0)})
    return records
