"""Bounded proof checks: synthetic chains and read-only published certificates.

No event-row constructor, scientific solve, or new actual parameter evaluation.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from flint import fmpq as Q, fmpq_mat as Mat, fmpq_poly as Poly

from rs_constraint_lab.h2_roles import STATES, augmented_structure, fingerprint, ready, relation, role_of, state_index
from rs_constraint_lab.stopping_factorization import is_zero
from rs_constraint_lab.stopping_sufficiency import synthetic_examples

TABLE = "constraint-lab/reports/tables/generation-008p-proof-checks.json"
OLD = "constraint-lab/reports/items/generation-008o-f0"


def selector_identities():
    counts = Counter()
    for p, i, j in STATES:
        for e in range(6):
            role = role_of(i, j, e)
            if role in (0, 1, 2):
                assert i == j
            if role in (3, 9):
                assert e == i and i != j
            if role in (4, 11):
                assert e == j and i != j
            if p.bit_count() == 5 and not (p >> i & 1):
                # FORM R04/R11 cannot activate when h1 is the unique missing edge.
                assert not (role in (4, 11) and not (p >> e & 1))
            counts[role] += 1
    return {"original_states": len(STATES), "candidate_checks": sum(counts.values()),
            "equal_history_gate": True, "recent_selector": True, "older_selector": True,
            "absent_h1_at_five_inactive": True}


def polynomial_flux():
    m = Poly([0, 1])
    d, delta = m + 5, m - 1
    out = {}
    for v in (1, 4):
        den, num = 36 * d * d - 5 * v * delta * delta, 36 * d * (6 * d + v * delta)
        # Eliminate beta in the original flux equation with x=num, y=den.
        assert 36*d*d*num - 216*d*d*den - 36*v*delta*d*den - 5*v*delta*delta*num == 0
        assert all(c > 0 for c in den.coeffs()) and all(c > 0 for c in num.coeffs())
        out[str(v)] = {"numerator_coefficients_low_first": list(map(str, num.coeffs())),
                       "denominator_coefficients_low_first": list(map(str, den.coeffs())),
                       "polynomial_identity": True, "positive_domain": "finite m>0; not arbitrary event weights"}
    return out


def old_certificates(root):
    blocks, lookup = augmented_structure()
    records, hashes, timing, controls = [], {}, [], []
    for path in sorted((root / OLD).glob("*.json")):
        obj = json.loads(path.read_text())
        result, item = obj["result"], obj["item"]
        assert fingerprint(result) == obj["result_hash"]
        hashes[path.name] = sha256(path.read_bytes()).hexdigest()
        for row in result["rows"]:
            if row["m"] == "1" or not row["bilinear_product_zero"]:
                continue
            side = result["sides"][str(row["k"]) + "-" + row["route"]]
            index = {o: i for i, o in enumerate(side["B_orbit_indices"])}
            src = side["classes"].index(row["source"])
            def full(key, z, target=None):
                orbit = lookup[z]
                local = index[orbit]
                if key in ("U", "occupation"):
                    return Q(side[key][src][local]) / len(blocks[orbit])
                return Q(side[key][local][target])
            comp = row["k"] == 4 or item["family"] == "DISSOLVE"
            if row["mechanism"] == "N1_TARGET_INSENSITIVITY":
                mechanism = "PREVIOUS_CL_T95_ALL_POSITIVE_M"
            elif row["cancellation_subtype"] == "ORBITWISE_ZERO":
                assert item["role"] in (0, 1, 2, 3, 9)
                for z in range(len(STATES)):
                    if lookup[z] not in index:
                        continue
                    p, i, j = STATES[z]
                    p = p ^ 63 if comp else p
                    u = full("U", z)
                    if p.bit_count() == 1 and not (p >> i & 1):
                        assert not u
                    elif item["role"] in (0, 1, 2) and p.bit_count() == 1:
                        assert not u
                    else:
                        assert all(not full("W", z, t) for t in range(len(side["classes"])))
                mechanism = "ALL_POSITIVE_M_REGENERATION" if item["role"] in (0, 1, 2) else "ALL_POSITIVE_M_EXIT_RATIO"
            elif row["cancellation_subtype"] == "FIBREWISE_CANCELLATION":
                assert item["role"] in (4, 11) and row["k"] == 3
                for z in range(len(STATES)):
                    if lookup[z] not in index:
                        continue
                    p, i, j = STATES[z]
                    p = p ^ 63 if comp else p
                    if p.bit_count() >= 5:
                        assert all(not full("W", z, t) for t in range(3))
                    elif p >> i & 1 or (not (p >> j & 1) and j != i):
                        assert not full("U", z)
                def mass(p, i, j):
                    return full("occupation", state_index(p ^ 63 if comp else p, i, j))
                x = sum(mass(63, i, j) for i in range(6) for j in range(6))
                ys = {sum(mass(63 ^ (1 << i) ^ (1 << j), i, h) for h in range(6))
                      for i in range(6) for j in range(6) if i != j}
                assert len(ys) == 1
                y = next(iter(ys))
                m, v = Q(item["m"]), (4 if item["role"] == 4 else 1)
                d, delta = m + 5, m - 1
                assert x/y == 36*d*(6*d+v*delta)/(36*d*d-5*v*delta*delta)
                assert all(mass(63 ^ (1 << i) ^ (1 << j), i, j) == x/36
                           for i in range(6) for j in range(6) if i != j)
                mechanism = "ALL_POSITIVE_M_TWO_LEVEL_FLUX_CENTERING"
            else:
                assert row["mechanism"] == "N1_TARGET_INSENSITIVITY"
                mechanism = "PREVIOUS_CL_T95_ALL_POSITIVE_M"
            records.append({"model": row["model_id"], "source": row["source"], "k": row["k"],
                            "route": row["route"], "old_subtype": row["cancellation_subtype"],
                            "proof_family": mechanism, "old_factor_conditions_exact": True})
        for row in result["timing_rows"]:
            if item["m"] == "1":
                continue
            entry = {"model": item["item_id"], "role": item["role"], "family": item["family"], "m": item["m"], **row}
            if row["aggregation_annihilates"]:
                assert row["structured_nonzero"] and all(not Q(v) for v in row["insertion_timing_contributions"])
                timing.append(entry)
            elif item["role"] in (3, 9) and item["family"] in ("FORM", "DISSOLVE"):
                controls.append(entry)
        if item["role"] in (3, 9) and item["family"] in ("FORM", "DISSOLVE"):
            name = "2-DOWN" if item["family"] == "FORM" else "4-UP"
            side = result["sides"][name]
            for term in side["F4_insertions"]:
                assert all(sum(map(Q, values)) == 0 for values in term)
    assert len(hashes) == 73 and len(records) == 200 and len(timing) == 20
    assert Counter(r["proof_family"] for r in records) == {
        "ALL_POSITIVE_M_REGENERATION": 48, "ALL_POSITIVE_M_EXIT_RATIO": 32,
        "ALL_POSITIVE_M_TWO_LEVEL_FLUX_CENTERING": 24, "PREVIOUS_CL_T95_ALL_POSITIVE_M": 96}
    return {"old_item_file_hashes": hashes, "family_followup": records,
            "timing_twenty_finite_only": timing, "nearby_published_timing_active_controls": controls,
            "all_m_total_twenty_status": "UNRESOLVED; no new parameter point authorised or executed"}


def proof_checks(root):
    examples = {}
    for name, (t, v) in synthetic_examples().items():
        a, q, p, r = (v[k] for k in ("a", "Q", "P", "R"))
        examples[name] = {"T": t.tolist(), "stationary": v["pi"], "source": a.tolist(),
                          "reset": p.tolist(), "Q": q.tolist(), "R": r.tolist(),
                          "eventual_delta": v["eventual_delta"].tolist(), "U": v["U"].tolist(),
                          "entrance_reset": a*p == a, "certificate": v["certificate"],
                          "first_six_coefficients": [(a*(q**j-p*(q*p)**j)*r).tolist() for j in range(6)]}
    return {"kind": "synthetic proof fixtures and read-only old certificate followup, not new scientific atlas",
            "new_actual_scientific_cells": 0, "synthetic": examples, "selector_identities": selector_identities(),
            "polynomial_flux": polynomial_flux(), "published_followup": old_certificates(root)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    value = ready(proof_checks(root))
    path = root / TABLE
    if args.verify:
        assert json.loads(path.read_text()) == value
        print("VERIFIED: bounded proof checks; zero new actual scientific cells")
    else:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        print(fingerprint(value))


if __name__ == "__main__":
    main()
