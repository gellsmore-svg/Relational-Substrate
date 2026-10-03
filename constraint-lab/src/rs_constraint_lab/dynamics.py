"""Canonical dynamical families.

Support, mode, and the exact kernel are each reduced under the full
symmetric group before they are hashed. The hash is not the canonicalisation.
Observable signatures are a separate derived grouping: equal signatures do
not mean equal kernels.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction

from rs_constraint_lab.constraints import DISSOLVE, Choreography, Constraint
from rs_constraint_lab.kernel import Kernel, build_kernel
from rs_constraint_lab.state import edge_count, edge_index, edge_permutation_maps, edges, permutations, relabel_state


def _encode(value) -> str:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return "(" + ",".join(_encode(item) for item in value) + ")"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    raise TypeError(f"cannot encode {type(value).__name__}")


def token_id(token: tuple) -> str:
    return hashlib.sha256(_encode(token).encode("utf-8")).hexdigest()


class RelabelTables:
    """State and edge images of S_N, built once per worker."""

    def __init__(self, n: int):
        self.n = n
        self.edge_list = edges(n)
        self.index = edge_index(n)
        self.perms = permutations(n)
        self.edge_maps = edge_permutation_maps(n)
        size = 1 << edge_count(n)
        self.state_images = []
        for perm in self.perms:
            self.state_images.append(
                tuple(relabel_state(state, perm, self.edge_list, self.index) for state in range(size))
            )


def canonical_tokens(kernel: Kernel, tables: RelabelTables) -> dict[str, tuple]:
    """Lexicographically least support, modal, and kernel tokens under S_N."""
    best_kernel = None
    best_support = None
    best_modal = None
    for edge_map, images in zip(tables.edge_maps, tables.state_images):
        kernel_rows = []
        support_rows = []
        modal_rows = []
        for state in range(kernel.n_states):
            image_state = images[state]
            if kernel.deadlock[state]:
                kernel_rows.append((image_state, ((image_state, Fraction(1)),)))
                support_rows.append((image_state, (image_state,)))
                modal_rows.append((image_state, (-1,)))
                continue
            successor = tuple(sorted((images[nxt], prob) for nxt, prob in kernel.successors[state]))
            support = tuple(sorted(images[nxt] for nxt, prob in kernel.successors[state] if prob > 0))
            weights = kernel.weights[state]
            best = max(weights)
            modal = tuple(sorted(edge_map[edge] for edge, weight in enumerate(weights) if weight == best))
            kernel_rows.append((image_state, successor))
            support_rows.append((image_state, support))
            modal_rows.append((image_state, modal))
        kernel_rows.sort()
        support_rows.sort()
        modal_rows.sort()
        kernel_token = tuple(kernel_rows)
        support_token = tuple(support_rows)
        modal_token = tuple(modal_rows)
        if best_kernel is None or kernel_token < best_kernel:
            best_kernel = kernel_token
        if best_support is None or support_token < best_support:
            best_support = support_token
        if best_modal is None or modal_token < best_modal:
            best_modal = modal_token
    return {"kernel": best_kernel, "support": best_support, "modal": best_modal}


def family_ids(n: int, tokens: dict[str, tuple]) -> dict[str, str]:
    support_id = token_id(tokens["support"])
    modal_id = token_id(tokens["modal"])
    kernel_id = token_id(tokens["kernel"])
    qualitative = hashlib.sha256(f"{n}|{support_id}|{modal_id}".encode("utf-8")).hexdigest()
    return {
        "support_family": support_id,
        "modal_family": modal_id,
        "exact_kernel_family": kernel_id,
        "qualitative_family": qualitative,
    }


def observable_signature(n: int, light: dict, heavy: dict) -> str:
    """Labelling-invariant scalars. This is not a kernel identity."""
    payload = {
        "n": n,
        "n_deadlock": light["n_deadlock"],
        "n_recurrent": light["n_recurrent"],
        "periods": list(light["periods"]),
        "support_matches_baseline": light["support_matches_baseline"],
        "equivalent_to_baseline": light["equivalent_to_baseline"],
        "shift": light.get("max_abs_dissolve_shift_exact"),
        "closing": light.get("closing_bias_exact"),
        "density": heavy.get("mean_edge_density_exact"),
        "triangle": heavy.get("triangle_mass_exact"),
        "halt": heavy.get("halt_mass_exact"),
        "rise": heavy.get("rise_then_release_exact"),
        "disjoint": heavy.get("disjoint_pair_mass_exact"),
        "tv": heavy.get("tv_from_uniform_exact"),
        "defect": heavy.get("reversibility_defect_exact"),
        "arithmetic": heavy.get("stationary_arithmetic"),
    }
    if payload["density"] is None and heavy.get("mean_edge_density") is not None:
        payload["density_rounded"] = round(float(heavy["mean_edge_density"]), 10)
        payload["halt_rounded"] = round(float(heavy.get("halt_mass") or 0.0), 10)
        payload["tv_rounded"] = round(float(heavy.get("tv_from_uniform") or 0.0), 10)
        payload["defect_rounded"] = round(float(heavy.get("reversibility_defect") or 0.0), 10)
        if heavy.get("disjoint_pair_mass") is not None:
            payload["disjoint_rounded"] = round(float(heavy["disjoint_pair_mass"]), 10)
    text = "|".join(f"{key}={payload[key]}" for key in sorted(payload))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_cancellation(n: int, constraints: tuple[Constraint, ...], factors, kernel: Kernel, baseline: Kernel) -> str | None:
    """Distinguish inherited baseline from a genuine structural cancellation.

    ``inherited_baseline``: every member is already baseline on its own, which
    is the one-edge positive-weight theorem at N=2, not a cancellation.

    ``genuine_global``: the set reproduces the baseline kernel, and at least
    one member does not.

    ``local``: two or more structurally distinct members meet on some toggle
    with a non-trivial factor product of 1, and the kernel is not baseline.
    """
    if len(constraints) < 2:
        return None
    if kernel.successors == baseline.successors:
        own_baseline = True
        for constraint in constraints:
            single = build_kernel(n, Choreography(0, 0, (constraint,)), factors)
            if single.successors != baseline.successors:
                own_baseline = False
                break
        if own_baseline:
            return "inherited_baseline"
        return "genuine_global"
    for state in range(kernel.n_states):
        for edge in range(kernel.n_edges):
            matched = [constraint for constraint in constraints if constraint.matches(state, edge)]
            if len({constraint.structural_key() for constraint in matched}) < 2:
                continue
            product = Fraction(1)
            nontrivial = False
            for constraint in matched:
                factor = factors[constraint.weight]
                product *= factor
                if factor != 1:
                    nontrivial = True
            if nontrivial and product == 1:
                return "local"
    return None


def observed_post_release_new_edge(kernel: Kernel, constraints: tuple[Constraint, ...], factors) -> bool:
    """Observational flag, not a target and not a screen.

    True when a count literal favours a dissolution and some later admissible
    state carries an edge that was absent before that dissolution. A hard trap
    after the dissolution does not qualify. Isomorphic reconnection is not
    interpreted here; the flag only records the edge event.
    """
    counted = [constraint for constraint in constraints if constraint.counts and constraint.polarity == DISSOLVE]
    if not counted:
        return False
    for state in range(kernel.n_states):
        for edge in range(kernel.n_edges):
            if ((state >> edge) & 1) == 0:
                continue
            matching = [constraint for constraint in counted if constraint.matches(state, edge)]
            if not matching:
                continue
            if not any(factors[constraint.weight] > 1 for constraint in matching):
                continue
            nxt = state ^ (1 << edge)
            if kernel.probability(state, nxt) == 0:
                continue
            seen = {nxt}
            stack = [nxt]
            while stack:
                here = stack.pop()
                if (~state & here) != 0:
                    return True
                for follow, prob in kernel.successors[here]:
                    if prob > 0 and follow not in seen:
                        seen.add(follow)
                        stack.append(follow)
    return False


def fraction_text(value: Fraction | None) -> str | None:
    if value is None:
        return None
    return f"{value.numerator}/{value.denominator}"
