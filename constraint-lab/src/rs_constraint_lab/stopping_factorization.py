"""Exact conditional-reset / stopping operators. Import executes no target."""

from collections import defaultdict

from flint import fmpq as Q, fmpq_mat as Mat

from rs_constraint_lab.gen008m_exec import read
from rs_constraint_lab.gen008n_exec import source_item as n_source_item
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_passage import layers, reconstruct, require
from rs_constraint_lab.h2_roles import STATES, fingerprint

VERSION = "generation-008o-route-factor/v1"


def eye(n):
    return Mat([[int(i == j) for j in range(n)] for i in range(n)])


def matrix(rows):
    if isinstance(rows[0], dict):
        return Mat([[row.get(j, Q(0)) for j in range(len(rows))] for row in rows])
    return Mat(rows)


def data(m):
    return m.tolist()


def is_zero(m):
    return all(not m[i, j] for i in range(m.nrows()) for j in range(m.ncols()))


def exact_solve(a, rhs, independent=True):
    x = a.solve(rhs, algorithm="dixon")
    require(a * x == rhs, "exact solve residual")
    if independent:
        require(x == a.solve(rhs, algorithm="fflu"), "independent fraction-free disagreement")
    return x


def conditional_operators(pi, t, fibres):
    """Finite matrix construction; callers control scientific execution gates."""
    labels = tuple(sorted(set(fibres)))
    index = {label: i for i, label in enumerate(labels)}
    c = Mat(len(pi), len(labels))
    lifting = Mat(len(labels), len(pi))
    masses = [sum((pi[z] for z, f in enumerate(fibres) if f == label), Q(0)) for label in labels]
    require(min(pi) > 0 and sum(pi) == 1, "positive stationary law required")
    for z, label in enumerate(fibres):
        c[z, index[label]] = 1
        lifting[index[label], z] = pi[z] / masses[index[label]]
    require(lifting * c == eye(len(labels)), "LC dimensions/identity")
    reset = c * lifting
    require(reset * reset == reset, "conditional reset is not idempotent")
    k = lifting * t * c
    require(k * lifting == lifting * t * reset, "lifted Kpi step")
    return c, lifting, reset, k, labels


def generic_identity(q, reset, exit_readout):
    """Full-matrix identity for synthetic/neutral verification only."""
    n = q.nrows()
    ar = exact_solve(eye(n) - q, eye(n))
    mr = exact_solve(eye(n) - q * reset, eye(n))
    require(ar - reset * mr == ar * (eye(n) - reset) * mr, "resolvent order/identity")
    return ar, mr


def setup(repository, item):
    nitem = {k: item[k] for k in ("role", "family", "m", "source_item_id")}
    nitem["item_id"] = item["source_passage_id"]
    a, b, controls = reconstruct(repository, n_source_item(nitem))
    passage_path = "constraint-lab/reports/items/generation-008n-p0/" + item["source_passage_id"] + ".json"
    old = read(repository / passage_path)
    require(old["result_hash"] == fingerprint(old["result"]), "8N result fingerprint")
    fibres = tuple(b.lookup[STATES[block[0]][0] * 6 + STATES[block[0]][1]] for block in a.blocks)
    t = matrix(a.rows)
    c, lifting, reset, kpi, labels = conditional_operators(a.pi, t, fibres)
    require(labels == tuple(range(len(b.rows))) and kpi == matrix(b.rows), "Kpi = L T C differs from immutable comparator")
    require(Mat([a.pi]) * reset == Mat([a.pi]), "stationary reset invariance")
    return a, b, controls, old, t, c, lifting, reset, fibres


def subset(m, row_indices, col_indices):
    return Mat([[m[i, j] for j in col_indices] for i in row_indices])


def contribution_record(value):
    return {"value": value, "sign": (value > 0) - (value < 0),
            "absolute_numerator": str(abs(int(value.numerator))), "denominator": str(value.denominator)}


def verify_full(a, b, side, names, k, direction):
    """Lift new occupation and reset actions to every original sparse state."""
    indices = side["B_orbit_indices"]
    local = {orb: i for i, orb in enumerate(indices)}
    states = [z for z in range(len(a.states)) if a.lookup[z] in local]
    allowed = set(states)
    counts = {z: a.states[z][0].bit_count() for z in states}
    require(all((v > k if direction == "UP" else v < k) for v in counts.values()), "route-side support")
    v, w, occupation, u, entrance = (matrix(side[key]) for key in ("V", "W", "occupation", "U", "entrance"))
    width = len(names)
    pi1 = b.full_pi
    full_v = {z: tuple(v[local[a.lookup[z]], j] for j in range(width)) for z in states}
    means = {}
    for z in states:
        s = z // 6
        if s not in means:
            means[s] = tuple(sum((a.full_pi[s * 6 + h] * full_v[s * 6 + h][j] for h in range(6)), Q(0)) / pi1[s]
                             for j in range(width))
    for z in states:
        local_z = local[a.lookup[z]]
        require(tuple(w[local_z, j] for j in range(width)) == tuple(full_v[z][j] - means[z // 6][j] for j in range(width)),
                "full reset target action")
        for j, target in enumerate(names):
            rhs = sum((p * Q(a.classes[a.lookup[t]] == target) for t, p in a.full_rows[z].items() if t not in allowed), Q(0))
            require(full_v[z][j] - sum((p * means[t // 6][j] for t, p in a.full_rows[z].items() if t in allowed), Q(0)) == rhs,
                    "full lifted comparator killed equation")
    for i, source in enumerate(names):
        full_b = {z: occupation[i, local[a.lookup[z]]] / len(a.blocks[a.lookup[z]]) for z in states}
        incoming, first = defaultdict(Q), defaultdict(Q)
        for z in states:
            for t, p in a.full_rows[z].items():
                if t in allowed:
                    incoming[t] += full_b[z] * p
        for z, row in enumerate(a.full_rows):
            if a.classes[a.lookup[z]] == source:
                for t, p in row.items():
                    if t in allowed:
                        first[t] += a.full_pi[z] * p / a.class_pi[source]
        totals = defaultdict(Q)
        for z in states:
            totals[z // 6] += full_b[z]
        for z in states:
            o = a.lookup[z]
            require(full_b[z] - incoming[z] == first[z], "full occupation left-resolvent equation")
            require(first[z] == entrance[i, local[o]] / len(a.blocks[o]), "full entrance aggregation")
            require(full_b[z] - totals[z // 6] * a.full_pi[z] / pi1[z // 6] == u[i, local[o]] / len(a.blocks[o]),
                    "full upstream off-manifold action")
    return {"full_B_states": len(states), "full_S_states": len(means),
            "all_sparse_occupation_and_reset_equations": True, "exact_gap": Q(0)}


def analyse(repository, item, independent=True):
    a, b, controls, old, t, c, lifting, reset, fibres = setup(repository, item)
    result = {"source_8N_result_hash": old["result_hash"], "stationary_source_controls": controls,
              "dimensions": {"full_Z": len(a.states), "full_S": len(b.states), "sector_Z": len(a.rows), "sector_S": len(b.rows)},
              "operator_hashes": {"C": fingerprint(data(c)), "L": fingerprint(data(lifting)), "Pi": fingerprint(data(reset))},
              "LC_identity": True, "Pi_idempotence": True, "Kpi_LTC_exact": True,
              "sides": {}, "rows": [], "timing_rows": []}
    for k, names in layers().items():
        for direction in ("UP", "DOWN"):
            indices = [i for i, count in enumerate(a.counts) if (count > k if direction == "UP" else count < k)]
            q, p = subset(t, indices, indices), subset(reset, indices, indices)
            n, d = len(indices), eye(len(indices)) - p
            exit_readout = Mat([[sum((v for target, v in a.rows[s].items() if a.classes[target] == name), Q(0))
                                for name in names] for s in indices])
            entrance = Mat([[sum((a.pi[z] * a.rows[z].get(s, Q(0)) / a.class_pi[source]
                                 for z, name in enumerate(a.classes) if name == source), Q(0)) for s in indices] for source in names])
            require(entrance * p == entrance, "universal first-step stationary-conditional balance")
            hit2 = matrix([[Q(v) for v in old["result"]["layers"][str(k)]["H2"]["certificate"]["quotient_values"][s]] for s in indices])
            hit1 = matrix([[Q(v) for v in old["result"]["layers"][str(k)]["Kpi"]["certificate"]["quotient_values"][fibres[s]]] for s in indices])
            v = exit_readout + q * hit1
            require(p * v == hit1 and (eye(n) - q * p) * v == exit_readout, "Mres action / ordinary Kpi equivalence")
            require((eye(n) - q) * hit2 == exit_readout, "immutable H2 killed action")
            occupation = exact_solve((eye(n) - q).transpose(), entrance.transpose(), independent).transpose()
            u, w = occupation * d, d * v
            delta = u * v
            require(delta == u * w == entrance * hit2 - entrance * p * v, "route-passage factorization")
            x = hit2 - p * v
            require((eye(n) - q) * x == w and entrance * x == delta, "resolvent identity on full target readout")
            zero2 = entrance * d * exit_readout
            require(is_zero(zero2), "two-event entrance annihilation")
            terms4 = [entrance * d * (q * p) * (q * p) * exit_readout,
                      entrance * q * d * q * p * exit_readout, entrance * q * q * d * exit_readout]
            four = sum(terms4, Mat(len(names), len(names)))
            require(four == entrance * q * q * exit_readout - entrance * p * q * p * q * p * exit_readout, "four-event insertion formula")
            require(is_zero(terms4[0]), "initial insertion should vanish")
            side = {"k": k, "route": direction, "classes": names, "B_orbit_indices": indices,
                    "fibre_ids": [fibres[s] for s in indices], "entrance": data(entrance), "occupation": data(occupation),
                    "U": data(u), "V": data(v), "W": data(w), "Delta": data(delta),
                    "F4": data(four), "F4_insertions": [data(term) for term in terms4],
                    "Q_hash": fingerprint(data(q)), "Pi_B_hash": fingerprint(data(p)),
                    "ranks": {"sector_I_minus_Pi": d.rank(), "sector_Ares_I_minus_Pi": d.rank(),
                              "W_full_and_sector": w.rank(), "route_class_map": delta.rank(), "U_class_rows": u.rank()},
                    "W_zero": is_zero(w), "identity_on_readout": True}
            require(d.rank() == n - len(set(side["fibre_ids"])), "invariant-sector projection rank")
            full_validation = verify_full(a, b, side, names, k, direction)
            full_rank = full_validation["full_B_states"] - full_validation["full_S_states"]
            side["ranks"].update({"full_I_minus_Pi": full_rank, "full_Ares_I_minus_Pi": full_rank,
                                  "full_rank_method": "conditional projection dimension and invertible left factor; not inferred from sector"})
            side["full_validation"] = full_validation
            for i, source in enumerate(names):
                published_left = tuple(Q(vv) for vv in old["result"]["layers"][str(k)]["H2"][direction][source])
                published_right = tuple(Q(vv) for vv in old["result"]["layers"][str(k)]["Kpi"][direction][source])
                require(tuple(delta[i, j] for j in range(len(names))) == tuple(x-y for x,y in zip(published_left,published_right)), "published 8N route residual")
                require(tuple((entrance * hit2)[i, j] for j in range(len(names))) == published_left and
                        tuple((entrance * p * v)[i, j] for j in range(len(names))) == published_right, "published route rows")
                uzero = all(not u[i, j] for j in range(n))
                productzero = all(not delta[i, j] for j in range(len(names)))
                mechanism = ("ACTIVE" if not productzero else "N0_UPSTREAM_ANNIHILATION" if uzero else
                             "N1_TARGET_INSENSITIVITY" if side["W_zero"] else "N2_BILINEAR_ORTHOGONALITY")
                contributions, sparse, fibre_sums = [], [], defaultdict(lambda: [Q(0)] * len(names))
                for j, orbit in enumerate(indices):
                    values = [u[i, j] * w[j, target] for target in range(len(names))]
                    contributions.append(values)
                    for target, value in enumerate(values):
                        fibre_sums[fibres[orbit]][target] += value
                    if any(values):
                        sparse.append({"orbit_id": f"Z{orbit:03d}", "target_contributions": [contribution_record(value) for value in values]})
                require(all(sum((row[j] for row in contributions), Q(0)) == delta[i, j] for j in range(len(names))), "orbit contribution sum")
                subtype = ("ORBITWISE_ZERO" if not sparse else "FIBREWISE_CANCELLATION" if all(not any(vv) for vv in fibre_sums.values())
                           else "SIGNED_BILINEAR_CANCELLATION") if productzero else None
                result["rows"].append({"model_id": item["item_id"], "role": item["role"], "family": item["family"], "m": item["m"],
                    "k": k, "source": source, "route": direction, "source_8N": item["source_passage_id"],
                    "published_route_active": not productzero, "DeltaR": [delta[i, j] for j in range(len(names))],
                    "exact_DeltaR_hash": fingerprint([delta[i,j] for j in range(len(names))]),
                    "U_zero": uzero, "V_zero": is_zero(v), "W_zero": side["W_zero"], "bilinear_product_zero": productzero,
                    "mechanism": mechanism, "cancellation_subtype": subtype, "ranks": side["ranks"],
                    "orbit_contribution_hash": fingerprint(contributions), "sparse_orbit_contributions": sparse,
                    "contribution_convention": "U orbit mass times W invariant value; omitted entries zero; complete B order in side certificate",
                    "symmetry_explanation_id": None, "validation": {"published_rows": True, "factorization": True, "full_sparse": True, "entrance_reset": True}})
            result["sides"][f"{k}-{direction}"] = side
        up, down = (matrix(result["sides"][f"{k}-{direction}"]["F4"]) for direction in ("UP", "DOWN"))
        total4 = up + down
        for i, source in enumerate(names):
            expected = [Q(x)-Q(y) for x,y in zip(old["result"]["layers"][str(k)]["H2"]["lengths"]["4"][source],
                                                old["result"]["layers"][str(k)]["Kpi"]["lengths"]["4"][source])]
            require(expected == [total4[i,j] for j in range(len(names))], "published total four-event residual")
            term_totals = [sum((matrix(result["sides"][f"{k}-{direction}"]["F4_insertions"][term])[i,j]
                                for direction in ("UP","DOWN") for j in range(len(names))), Q(0)) for term in range(3)]
            scalar = sum(expected, Q(0))
            result["timing_rows"].append({"model_id": item["item_id"], "k": k, "source": source,
                "destination_delta4": expected, "timing_delta4": scalar, "insertion_timing_contributions": term_totals,
                "structured_nonzero": any(expected), "aggregation_annihilates": not scalar,
                "classification": "NEUTRAL" if not any(expected) else "INSERTIONWISE_TARGET_AGGREGATION_ZERO" if not scalar and not any(term_totals)
                                  else "BETWEEN_INSERTION_CANCELLATION" if not scalar else "TIMING_ACTIVE_AT_FOUR"})
    return result
