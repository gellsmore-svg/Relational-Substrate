"""Independent full-state post-execution audit of frozen P0 summaries.

No new solves or estimands: reconstruct exact original equations and finite
path sums from the immutable kernel and published solution certificates.
"""

from collections import defaultdict

from flint import fmpq as Q

from rs_constraint_lab.gen008n_exec import source_item, verify_certificates
from rs_constraint_lab.h2_passage import apply, layers, reconstruct, require
from rs_constraint_lab.h2_roles import fingerprint


def verify(repository, item, result):
    verify_certificates(repository, item, result)
    a, b, _ = reconstruct(repository, source_item(item))
    for model, chain in (("H2", a), ("Kpi", b)):
        names_full = tuple(chain.classes[block] for block in chain.lookup)
        counts = tuple(state[0].bit_count() for state in chain.states)

        def average(values, source):
            return tuple(sum((mass * values[s][j] for s, mass in enumerate(chain.full_pi)
                              if names_full[s] == source), Q(0)) / chain.class_pi[source]
                         for j in range(len(values[0])))

        for k, names in layers().items():
            stored = result["layers"][str(k)][model]
            cert = stored["certificate"]
            hit = tuple(tuple(Q(v) for v in cert["quotient_values"][block]) for block in chain.lookup)
            total = apply(chain.full_rows, hit)
            directions = {d: tuple({t: w for t, w in row.items() if counts[t] == k + delta}
                                   for row in chain.full_rows) for d, delta in (("UP", 1), ("DOWN", -1))}
            for field, values in (("R", total), *((d, apply(rows, hit)) for d, rows in directions.items())):
                require(all(average(values, c) == tuple(Q(v) for v in stored[field][c]) for c in names),
                        "full-state return aggregation: " + field)
            boundary = tuple(tuple(Q(names_full[s] == target) for target in names) if counts[s] == k
                             else (Q(0),) * len(names) for s in range(len(chain.full_rows)))
            # Enumerate exact first-return finite path masses on the full chain.
            v = boundary
            for step in range(1, 13):
                v = apply(chain.full_rows, v)
                if step in (2, 4, 6, 8, 10, 12):
                    require(all(average(v, c) == tuple(Q(x) for x in stored["lengths"][str(step)][c]) for c in names),
                            "full-state first-return path sum")
                elif step % 2:
                    require(all(not any(average(v, c)) for c in names), "full-state odd return")
                v = tuple((Q(0),) * len(names) if counts[s] == k else row for s, row in enumerate(v))
            for c in names:
                expected = tuple(Q(stored["R"][c][j]) - sum((Q(stored["lengths"][str(n)][c][j])
                                      for n in (2, 4, 6, 8, 10, 12)), Q(0)) for j in range(len(names)))
                require(expected == tuple(Q(x) for x in stored["tail"][c]) and min(expected) >= 0, "exact return tail")
        hitting = result["hitting"][model]
        for target, cert in hitting["MFPT_certificates"].items():
            values = tuple(tuple(Q(x) for x in cert["quotient_values"][block]) for block in chain.lookup)
            for source, value in hitting["MFPT"][target].items():
                require(average(values, source)[0] == Q(value), "full source MFPT aggregation")
            positive = tuple((Q(1) + row[0],) for row in apply(chain.full_rows, values))
            require(average(positive, target)[0] == Q(hitting["Kac"][target]) == 1 / chain.class_pi[target], "full Kac")
        for source, row in hitting["committors"].items():
            values = tuple(tuple(Q(x) for x in row["certificate"]["quotient_values"][block]) for block in chain.lookup)
            require(average(values, source)[0] == Q(row["probability"]), "full source committor aggregation")
    return {"system_id": item["item_id"], "exact": True, "full_state_return_path_sums_through": 12,
            "full_state_reward_and_harmonic_aggregations": True, "result_hash": fingerprint(result)}
