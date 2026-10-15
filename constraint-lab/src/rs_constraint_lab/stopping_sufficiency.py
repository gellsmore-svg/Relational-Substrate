"""Small exact task-relative proof utilities; no CL parameter-cell adapter."""

from fractions import Fraction

from flint import fmpq as Q, fmpq_mat as Mat

from rs_constraint_lab.stopping_factorization import eye, is_zero, subset


def stationary(t):
    """Synthetic irreducible-chain stationary solve, independently checked below."""
    n = t.nrows()
    if n > 16 or n != t.ncols():
        raise ValueError("synthetic fixture limit: square, at most 16 states")
    if any(t[i, j] < 0 for i in range(n) for j in range(n)) or any(sum(t[i, j] for j in range(n)) != 1 for i in range(n)):
        raise ValueError("stochastic kernel required")
    a = t.transpose() - eye(n)
    for j in range(n):
        a[n - 1, j] = 1
    rhs = Mat([[int(i == n - 1)] for i in range(n)])
    pi = a.solve(rhs).transpose()
    assert pi * t == pi and sum(pi.tolist()[0]) == 1 and min(pi.tolist()[0]) > 0
    assert [Fraction(str(x)) for x in pi.tolist()[0]] == fraction_solve(a.tolist(), rhs.tolist())
    return pi.tolist()[0]


def fraction_solve(a, rhs):
    """Independent standard-library Gauss-Jordan route (one RHS)."""
    rows = [[Fraction(str(x)) for x in r] + [Fraction(str(b[0]))] for r, b in zip(a, rhs)]
    n = len(rows)
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v / scale for v in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [v - scale * w for v, w in zip(rows[i], rows[j])]
    return [r[-1] for r in rows]


def realization(q, p, sources, readout):
    b = q.nrows()
    if b == 0 or 2 * b > 32 or q.ncols() != b or p.nrows() != b or p.ncols() != b:
        raise ValueError("small square operators required; block limit 32")
    if sources.ncols() != b or readout.nrows() != b or p * p != p:
        raise ValueError("typed sources/readouts and idempotent reset required")
    h = Mat(2 * b, 2 * b)
    qp = q * p
    for i in range(b):
        for j in range(b):
            h[i, j], h[b + i, b + j] = q[i, j], qp[i, j]
    e = Mat([r + s for r, s in zip(sources.tolist(), (-sources * p).tolist())])
    f = Mat(readout.tolist() + readout.tolist())
    return h, e, f


def all_length_certificate(q, p, sources, readout):
    """Exact reachable closure. Basis rows can be signed, not physical priors."""
    h, e, f = realization(q, p, sources, readout)
    basis = []
    block, first, steps = e, None, []
    for j in range(h.nrows() + 1):
        out = block * f
        if first is None and not is_zero(out):
            first = j
        old_rank = len(basis)
        for row in block.tolist():
            if Mat(basis + [row]).rank() > len(basis):
                basis.append(row)
        steps.append(len(basis))
        if len(basis) == old_rank:
            break
        block = block * h
    else:
        raise AssertionError("finite reachable closure failed")
    k = Mat(basis) if basis else Mat(0, h.nrows())
    assert Mat(basis + (k * h).tolist()).rank() == len(basis)
    equal = is_zero(k * f)
    assert equal == (first is None)
    # Independent bounded power test from Cayley-Hamilton, not closure logic.
    direct = all(is_zero(sources * (q ** j - p * (q * p) ** j) * readout) for j in range(h.nrows()))
    assert equal == direct
    return {"all_lengths_equal": equal, "first_differing_j": first,
            "reachable_dimension": len(basis), "rank_chronology": steps,
            "generic_power_bound": h.nrows(), "closure_exact": True}


def stopped_fixture(t, fibres, a_indices, source):
    from rs_constraint_lab.stopping_factorization import conditional_operators, generic_identity
    pi = stationary(t)
    c, lifting, reset, kpi, labels = conditional_operators(pi, t, fibres)
    assert Mat([pi]) * t == Mat([pi])
    assert all(all((z in a_indices) == (w in a_indices) for w in range(len(fibres)) if fibres[w] == fibres[z]) for z in range(len(fibres)))
    b_indices = [i for i in range(t.nrows()) if i not in a_indices]
    q = subset(t, b_indices, b_indices)
    p = subset(reset, b_indices, b_indices)
    r = subset(t, b_indices, a_indices)
    ar, mr = generic_identity(q, p, r)
    a = Mat([source])
    assert a.ncols() == len(b_indices) and min(source) >= 0 and sum(source) == 1
    return {"pi": pi, "C": c, "L": lifting, "Pi": reset, "Kpi": kpi,
            "Q": q, "P": p, "R": r, "a": a,
            "U": a * ar * (eye(q.nrows()) - p),
            "eventual_delta": a * (ar - p * mr) * r,
            "certificate": all_length_certificate(q, p, a, r)}


def synthetic_examples():
    # A0,A1,B0,B1: equal eventual target ratio, unequal hidden exit hazards.
    timing = Mat([[0, 0, Q(3, 4), Q(1, 4)], [0, 0, Q(1, 4), Q(3, 4)],
                  [Q(1, 4), Q(1, 4), Q(1, 4), Q(1, 4)],
                  [Q(1, 8), Q(1, 8), Q(1, 4), Q(1, 2)]])
    pi = stationary(timing)
    lifted = [pi[2] / (pi[2] + pi[3]), pi[3] / (pi[2] + pi[3])]
    a = stopped_fixture(timing, (0, 1, 2, 2), [0, 1], lifted)
    # Different exit ratios: same stationary/adjacent coarse law, different hit law.
    target = Mat([[0, 0, Q(3, 4), Q(1, 4)], [0, 0, Q(1, 4), Q(3, 4)],
                  [Q(3, 8), Q(1, 8), Q(1, 4), Q(1, 4)],
                  [Q(1, 16), Q(3, 16), Q(1, 4), Q(1, 2)]])
    b = stopped_fixture(target, (0, 1, 2, 2), [0, 1], [Q(3, 4), Q(1, 4)])
    # A,B0,B1,C: constant exit hazard, non-lumpable internal coarse dynamics.
    path = Mat([[0, Q(1, 2), Q(1, 4), Q(1, 4)],
                [Q(1, 4), Q(1, 2), Q(1, 8), Q(1, 8)],
                [Q(1, 4), Q(1, 8), Q(1, 8), Q(1, 2)],
                [Q(1, 4), Q(1, 4), Q(1, 4), Q(1, 4)]])
    d = stopped_fixture(path, (0, 1, 1, 2), [0], [Q(1, 2), Q(1, 4), Q(1, 4)])
    # Bipartite support: parity removes odd returns, not even timing defects.
    parity = Mat([[0, Q(3, 4), Q(1, 4), 0, 0],
                  [Q(1, 2), 0, 0, Q(1, 2), 0], [Q(1, 4), 0, 0, 0, Q(3, 4)],
                  [0, Q(3, 4), Q(1, 4), 0, 0], [0, Q(1, 4), Q(3, 4), 0, 0]])
    pi = stationary(parity)
    mass = pi[1] + pi[2]
    e = stopped_fixture(parity, (0, 1, 1, 2, 2), [0], [pi[1] / mass, pi[2] / mass, Q(0), Q(0)])
    return {"eventual_not_all_lengths": (timing, a), "aggregation_erases_target": (target, b),
            "all_lengths_not_all_paths": (path, d), "parity_not_timing_equality": (parity, e)}
