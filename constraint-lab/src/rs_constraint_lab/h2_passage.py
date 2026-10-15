"""Exact stationary-source passage on the immutable Generation 8M chains.

Graph classes specify boundaries, never an assumed autonomous Markov chain.
Importing this module executes no scientific target.
"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import json

from flint import fmpq as Q, fmpq_mat
import mpmath as mp

from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_roles import (
    STATES, H1_STATES, RoleController, augmented_structure, fingerprint,
    js, kernel_from_events, lift, ln, mpq, number, project, quotient, residual,
)
from rs_constraint_lab.history import HistoryError

VERSION = "generation-008n-stationary-source-passage/v1"
LENGTHS = (2, 4, 6, 8, 10, 12)


def require(condition, message):
    if not condition:
        raise HistoryError(message)


def layers():
    table = pair_classes()
    result = {k: tuple(table.name_of[p] for p in table.representatives if p.bit_count() == k)
              for k in (2, 3, 4)}
    require(tuple(map(len, result.values())) == (2, 3, 2), "unexpected structural layers")
    return result


def apply(rows, values):
    return tuple(tuple(sum((w * values[t][j] for t, w in row.items()), Q(0))
                       for j in range(len(values[0]))) for row in rows)


def solve_boundary(rows, boundary, *, reward=0, independent=False):
    """Dirichlet equations with constant per-step reward on non-boundary states."""
    require(bool(boundary), "nonempty absorbing boundary required")
    width = len(next(iter(boundary.values())))
    require(width > 0 and all(len(v) == width for v in boundary.values()), "boundary width")
    unknown = [s for s in range(len(rows)) if s not in boundary]
    index = {s: i for i, s in enumerate(unknown)}
    a = [[Q(int(i == j)) for j in range(len(unknown))] for i in range(len(unknown))]
    b = [[Q(reward)] * width for _ in unknown]
    for s in unknown:
        for t, w in rows[s].items():
            if t in index:
                a[index[s]][index[t]] -= w
            else:
                for j in range(width):
                    b[index[s]][j] += w * boundary[t][j]
    values = [tuple(map(Q, boundary[s])) if s in boundary else None for s in range(len(rows))]
    if unknown:
        matrix, rhs = fmpq_mat(a), fmpq_mat(b)
        solution = matrix.solve(rhs, algorithm="dixon")
        if independent:
            require(solution == matrix.solve(rhs, algorithm="fflu"), "independent exact solve disagreement")
        for s in unknown:
            values[s] = tuple(solution[index[s], j] for j in range(width))
    evolved = apply(rows, values)
    require(all(values[s] == tuple(Q(reward) + x for x in evolved[s]) for s in unknown),
            "quotient absorbing equation residual")
    return tuple(values)


@dataclass
class Chain:
    depth: int
    full_rows: tuple
    full_pi: tuple

    def __post_init__(self):
        self.states = STATES if self.depth == 2 else H1_STATES
        self.blocks, self.lookup = augmented_structure(self.depth)
        self.rows = quotient(self.full_rows, self.depth)
        self.pi = tuple(sum((self.full_pi[s] for s in block), Q(0)) for block in self.blocks)
        self.classes = tuple(pair_classes().name_of[self.states[block[0]][0]] for block in self.blocks)
        self.counts = tuple(self.states[block[0]][0].bit_count() for block in self.blocks)
        self.class_pi = project(self.pi, self.classes)
        require(len(self.rows) == (120 if self.depth == 2 else 28), "unexpected valid S4 quotient")
        require(sum(self.full_pi) == 1 and min(self.full_pi) > 0, "stationary law not positive")
        require(residual(self.full_pi, self.full_rows) == residual(self.pi, self.rows) == 0,
                "immutable stationary residual")
        require(all(self.full_pi[s] == self.pi[b] / len(block)
                    for b, block in enumerate(self.blocks) for s in block), "stationary S4 invariance")

    def average(self, values, source):
        return tuple(sum((self.pi[s] * values[s][j] for s, c in enumerate(self.classes) if c == source), Q(0))
                     / self.class_pi[source] for j in range(len(values[0])))

    def certify(self, values, boundary, reward=0):
        """Lift each solution and check every full sparse hidden-state equation."""
        full = tuple(values[self.lookup[s]] for s in range(len(self.states)))
        evolved = apply(self.full_rows, full)
        for s in range(len(self.states)):
            b = self.lookup[s]
            expected = boundary[b] if b in boundary else tuple(Q(reward) + x for x in evolved[s])
            require(full[s] == tuple(expected), "full sparse boundary/equation residual")
        return {"quotient_values": values, "full_values_hash": fingerprint(full),
                "full_state_equations": len(full), "exact_residual": Q(0)}

    def return_layer(self, k, independent=False):
        names = layers()[k]
        boundary = {s: tuple(Q(c == target) for target in names)
                    for s, c in enumerate(self.classes) if self.counts[s] == k}
        hit = solve_boundary(self.rows, boundary, independent=independent)
        certificate = self.certify(hit, boundary)
        step = apply(self.rows, hit)
        route = {}
        for direction, sign in (("UP", 1), ("DOWN", -1)):
            values = tuple(tuple(sum((w * hit[t][j] for t, w in row.items()
                                     if self.counts[t] == k + sign), Q(0)) for j in range(len(names)))
                           for row in self.rows)
            route[direction] = {c: self.average(values, c) for c in names}
        total = {c: self.average(step, c) for c in names}
        for c in names:
            require(sum(total[c]) == 1, "first-return row not stochastic")
            require(total[c] == tuple(a + b for a, b in zip(route["UP"][c], route["DOWN"][c])),
                    "UP/DOWN decomposition")
        layer_mass = sum((self.class_pi[c] for c in names), Q(0))
        nu = tuple(self.class_pi[c] / layer_mass for c in names)
        require(all(sum((nu[i] * total[c][j] for i, c in enumerate(names)), Q(0)) == nu[j]
                    for j in range(len(names))), "restricted stationary return weights")
        # The killed chain acts only outside A. Boundary values supply the final hit.
        killed = tuple({t: w for t, w in row.items() if t not in boundary}
                       if s not in boundary else {} for s, row in enumerate(self.rows))
        term = tuple(tuple(sum((w * boundary[t][j] for t, w in row.items() if t in boundary), Q(0))
                           for j in range(len(names))) if s not in boundary else (Q(0),) * len(names)
                     for s, row in enumerate(self.rows))
        lengths, odd_hashes = {}, {}
        for n in range(2, 13):
            at_source = apply(self.rows, term)
            distribution = {c: self.average(at_source, c) for c in names}
            if n % 2:
                require(all(not any(row) for row in distribution.values()), "odd return length not zero")
                odd_hashes[str(n)] = fingerprint(distribution)
            else:
                lengths[str(n)] = distribution
            term = apply(killed, term)
        tail = {c: tuple(total[c][j] - sum((lengths[str(n)][c][j] for n in LENGTHS), Q(0))
                         for j in range(len(names))) for c in names}
        require(all(x >= 0 for row in tail.values() for x in row), "negative exact return tail")
        return {"classes": names, "R": total, **route, "nu": nu, "lengths": lengths,
                "tail": tail, "odd_zero_hashes": odd_hashes, "certificate": certificate}

    def hitting(self, independent=False):
        mfpt, kac, certificates, committors = {}, {}, {}, {}
        for names in layers().values():
            for target in names:
                boundary = {s: (Q(0),) for s, c in enumerate(self.classes) if c == target}
                values = solve_boundary(self.rows, boundary, reward=1, independent=independent)
                certificates[target] = self.certify(values, boundary, reward=1)
                mfpt[target] = {source: self.average(values, source)[0] for source in names if source != target}
                positive = tuple((Q(1) + row[0],) for row in apply(self.rows, values))
                kac[target] = self.average(positive, target)[0]
                require(kac[target] == 1 / self.class_pi[target], "Kac positive return control failed")
        for source in layers()[3]:
            a, b = (c for c in layers()[3] if c != source)
            boundary = {s: (Q(c == a),) for s, c in enumerate(self.classes) if c in (a, b)}
            values = solve_boundary(self.rows, boundary, independent=independent)
            require(all(0 <= x[0] <= 1 for x in values), "committor outside [0,1]")
            committors[source] = {"target_a": a, "target_b": b, "probability": self.average(values, source)[0],
                                  "certificate": self.certify(values, boundary)}
        return {"MFPT": mfpt, "Kac": kac, "MFPT_certificates": certificates, "committors": committors}


def reconstruct(repository, m_item):
    """Validate and consume existing 8M payloads; never change them."""
    path = Path(repository) / "constraint-lab/reports/items/generation-008m-m0" / (m_item["item_id"] + ".json")
    value = json.loads(path.read_text())
    r = value["result"]
    require(value["item"] == m_item and value["result_hash"] == fingerprint(r), "8M payload identity")
    events = RoleController(m_item["role"], m_item["family"], m_item["m"]).event_rows()
    rows2 = kernel_from_events(events)
    require(fingerprint(events) == r["kernel_fingerprint"], "8M reconstructed event fingerprint")
    pi2 = lift(tuple(Q(v) for v in r["stationary_orbit_masses"]))
    pi1 = tuple(Q(v) for v in r["stationary_P_H1"])
    events1 = tuple(tuple(Q(v) for v in row) for row in r["Kpi_H1"]["event_rows"])
    for p, i in H1_STATES:
        s = p * 6 + i
        require(sum(pi2[s * 6:s * 6 + 6]) == pi1[s], "source pushforward fails; stop before passage")
        for e in range(6):
            require(sum((pi2[s * 6 + j] * events[s * 6 + j][e] for j in range(6)), Q(0)) ==
                    pi1[s] * events1[s][e], "stationary adjacent/first-step match fails")
    a, b = Chain(2, rows2, pi2), Chain(1, kernel_from_events(events1, 1), pi1)
    require(a.class_pi == b.class_pi, "class occupancy match")
    require(project(pi2, [s[0] for s in STATES]) == project(pi1, [s[0] for s in H1_STATES]),
            "labelled occupancy match")
    sources = {c: fingerprint([(s[:2], pi2[i] / a.class_pi[c]) for i, s in enumerate(STATES)
                              if pair_classes().name_of[s[0]] == c]) for names in layers().values() for c in names}
    sources1 = {c: fingerprint([(s, pi1[i] / b.class_pi[c]) for i, s in enumerate(H1_STATES)
                               if pair_classes().name_of[s[0]] == c]) for names in layers().values() for c in names}
    controls = {"occupancy_match": True, "source_pushforward_match": True, "first_step_match": True,
                "stationary_H2_hash": fingerprint(pi2), "stationary_H1_hash": fingerprint(pi1),
                "source_H2_hashes": sources, "source_H1_hashes": sources1, "class_probabilities": a.class_pi,
                "H2_quotient_states": len(a.rows), "H1_quotient_states": len(b.rows),
                "source_result_hash": value["result_hash"],
                "category_8M": r["neutral_comparison"]["material_class"],
                "KU_equal_8M": r["uniform_H1_comparison"]["pair_equal"]}
    return a, b, controls


def compare(a, b):
    names = a["classes"]
    require(names == b["classes"] and a["nu"] == b["nu"], "matched return alphabets")
    require(a["lengths"]["2"] == b["lengths"]["2"], "two-event material triple control")
    result = {}
    for c in names:
        delta = tuple(x - y for x, y in zip(a["R"][c], b["R"][c]))
        length_flags = {str(n): a["lengths"][str(n)][c] != b["lengths"][str(n)][c] for n in LENGTHS}
        tail = a["tail"][c] != b["tail"][c]
        p, q = a["R"][c], b["R"][c]
        information = js(dict(enumerate(p)), dict(enumerate(q)))
        entropy = lambda v: -mp.fsum(mpq(x) * ln(x) for x in v if x)
        independent_information = entropy(tuple((x+y)/2 for x,y in zip(p,q))) - (entropy(p)+entropy(q))/2
        gap = abs(information-independent_information)
        require(gap <= mp.mpf("1e-25"), "independent JS route disagreement")
        result[c] = {"delta_R": delta, "routing_active": any(delta),
                     "row_JS": number(information), "information_route_gap": number(gap),
                     "UP_active": a["UP"][c] != b["UP"][c], "DOWN_active": a["DOWN"][c] != b["DOWN"][c],
                     "length_active": any(length_flags.values()) or tail, "length_flags": length_flags,
                     "tail_active": tail,
                     "first_length": next((n for n in LENGTHS if length_flags[str(n)]), "tail" if tail else None),
                     "R_H2_hash": fingerprint(a["R"][c]), "R_Kpi_hash": fingerprint(b["R"][c])}
    return result


def analyse(repository, m_item, independent=False):
    a, b, controls = reconstruct(repository, m_item)
    result = {"controls": controls, "layers": {}}
    for k in layers():
        left, right = a.return_layer(k, independent), b.return_layer(k, independent)
        result["layers"][str(k)] = {"H2": left, "Kpi": right, "comparison": compare(left, right)}
    left, right = a.hitting(independent), b.hitting(independent)
    result["hitting"] = {"H2": left, "Kpi": right,
        "MFPT_differences": {t: {s: v - right["MFPT"][t][s] for s, v in row.items()}
                             for t, row in left["MFPT"].items()},
        "MFPT_ratios": {t: {s: v / right["MFPT"][t][s] for s, v in row.items()}
                        for t, row in left["MFPT"].items()},
        "committor_differences": {s: row["probability"] - right["committors"][s]["probability"]
                                  for s, row in left["committors"].items()}}
    if m_item["m"] == "1":
        require(all(not row["length_active"] and not row["routing_active"] and
                    not row["UP_active"] and not row["DOWN_active"]
                    for layer in result["layers"].values() for row in layer["comparison"].values()), "neutral return null")
        require(not any(v for row in result["hitting"]["MFPT_differences"].values() for v in row.values()) and
                not any(result["hitting"]["committor_differences"].values()), "neutral hitting null")
    return result
