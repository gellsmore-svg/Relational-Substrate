"""Gravity-time programme, Round G0: relational basin census.

Every rule is ordinary O=2 DSL text parsed by ``parse_expression`` and
compiled by ``build_kernel``. Templates are label-covariant: one template is
instantiated over every ordered witness, so no rule names a direction, a
place or a source. The held source is declared scaffolding: three relations
prohibited from dissolving. Relational distance is a derived observable
that no rule reads.

All quantities are exact kernel results: dense float64 linear algebra on a
reachable class, a lazy-iteration solve on the 32,768-state free mode, and
residual checks. No trajectory is sampled.
"""

from __future__ import annotations

import itertools
import math
from collections import deque
from fractions import Fraction

import numpy as np

from rs_constraint_lab.constraints import Choreography, Constraint, parse_expression
from rs_constraint_lab.exact import strongly_connected_components
from rs_constraint_lab.kernel import Kernel, build_kernel
from rs_constraint_lab.state import edge_index, edges
from rs_constraint_lab.weights import alphabet_factors

PROGRAMME = "GT"
ROUND_ID = "round-g0"
EXPERIMENT_ID = "gt-round-g0-relational-basin"
ANALYSIS_VERSION = "gt-g0/v1"
SOURCE = (0, 1, 2)  # legacy name: the source vertices of the default held triangle (K3)
FACTORS = alphabet_factors("W4")


# --- held-reference scaffold (GT-P007) -----------------------------------------------------
#
# A scaffold is a declared boundary condition: a set of pair relations held
# present and non-dissolvable. Its source vertex set (for measurements only) is
# the set of vertices incident on held edges. Rules never read the scaffold:
# rates depend on it only through the held relations being present and the
# prohibition of their dissolution, exactly as for the original triangle.


class Scaffold:
    __slots__ = ("name", "held")

    def __init__(self, name: str, held):
        pairs = tuple(sorted((min(a, b), max(a, b)) for a, b in held))
        if len(set(pairs)) != len(pairs) or any(a == b for a, b in pairs):
            raise ValueError("held edges must be distinct pairs")
        self.name = name
        self.held = pairs

    @property
    def source(self) -> tuple[int, ...]:
        return tuple(sorted({v for e in self.held for v in e}))

    def __repr__(self) -> str:
        return f"Scaffold({self.name!r}, {self.held!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Scaffold) and self.held == other.held and self.name == other.name

    def __hash__(self) -> int:
        return hash((self.name, self.held))

    def automorphisms(self, n: int) -> list[tuple[int, ...]]:
        """Vertex permutations of range(n) that map the held edge set onto itself (identity first)."""
        src = self.source
        probes = [v for v in range(n) if v not in src]
        held = set(self.held)
        out = []
        for s in itertools.permutations(src):
            mapping = dict(zip(src, s))
            if {(min(mapping[a], mapping[b]), max(mapping[a], mapping[b])) for a, b in held} != held:
                continue
            for p in itertools.permutations(probes):
                perm = list(range(n))
                for old, new in mapping.items():
                    perm[old] = new
                for old, new in zip(probes, p):
                    perm[old] = new
                out.append(tuple(perm))
        return out


SCAFFOLDS = {
    "K3": Scaffold("K3", ((0, 1), (0, 2), (1, 2))),
    "P3": Scaffold("P3", ((0, 1), (1, 2))),
    "K2": Scaffold("K2", ((0, 1),)),
}
_ACTIVE = [SCAFFOLDS["K3"]]


def active_scaffold() -> Scaffold:
    return _ACTIVE[-1]


def source() -> tuple[int, ...]:
    """Source vertices of the active scaffold (measurements only)."""
    return _ACTIVE[-1].source


def held_pairs() -> tuple[tuple[int, int], ...]:
    return _ACTIVE[-1].held


def held_slot_indices(n: int) -> list[int]:
    held = set(held_pairs())
    return [i for i, pair in enumerate(edges(n)) if pair in held]


def slot_classes(n: int) -> list[str]:
    """Measurement classes of every slot under the active scaffold.

    A: source-probe (attachment); S: held; C: both ends in the source but not held
    (a free source chord, e.g. the P3 closing chord); P: probe-probe. Under the
    default triangle no slot is C, so legacy classes are unchanged.
    """
    src = set(source())
    held = set(held_pairs())
    out = []
    for a, b in edges(n):
        if (a in src) != (b in src):
            out.append("A")
        elif a in src:
            out.append("S" if (a, b) in held else "C")
        else:
            out.append("P")
    return out


def free_slot_indices(n: int) -> list[int]:
    held = set(held_slot_indices(n))
    return [i for i in range(len(edges(n))) if i not in held]


def attach_slot_indices(n: int) -> list[int]:
    return [i for i, c in enumerate(slot_classes(n)) if c == "A"]


class use_scaffold:
    """Context manager: make ``scaffold`` the active held reference within the block."""

    def __init__(self, scaffold: Scaffold | str):
        self.scaffold = SCAFFOLDS[scaffold] if isinstance(scaffold, str) else scaffold

    def __enter__(self):
        _ACTIVE.append(self.scaffold)
        return self.scaffold

    def __exit__(self, *exc):
        _ACTIVE.pop()
        return False
STATIONARY_RESIDUAL_TOLERANCE = 1e-12
NULL_IDENTITY_TOLERANCE = 1e-12
FAMILY_GRADES = {
    "NULL": (None,),
    "DENS": ("weak_favour", "strong_favour"),
    "ADJ": ("weak_favour", "strong_favour"),
    "CLOSE": ("weak_favour", "strong_favour"),
    "HOLD": ("weak_suppress", "strong_suppress"),
    "LOCK": ("prohibit",),
}
FAMILY_K = {"NULL": None, "DENS": 1, "ADJ": 2, "CLOSE": 3, "HOLD": 3, "LOCK": 3}
MODES = ("HELD", "FREE")
SIZES = (5, 6)
FREE_MODE_ITERATION_CAP = 200_000


class BasinError(ValueError):
    """A G0 invariant did not hold."""


def _e(a: int, b: int) -> str:
    return f"{min(a, b)}-{max(a, b)}"


def template_expressions(family: str, n: int, grade: str | None) -> list[str]:
    """Label-covariant instances of one template over every ordered witness."""
    out: list[str] = []
    for a, b in itertools.combinations(range(n), 2):
        if family == "NULL":
            continue
        if family == "DENS":
            out.append(f"form({_e(a, b)}) => {grade}")
            continue
        for c in range(n):
            if c in (a, b):
                continue
            if family == "ADJ":
                out.append(f"form({_e(a, b)}) | present({_e(a, c)}) => {grade}")
                out.append(f"form({_e(a, b)}) | present({_e(b, c)}) => {grade}")
            elif family == "CLOSE":
                out.append(f"form({_e(a, b)}) | present({_e(a, c)}) & present({_e(b, c)}) => {grade}")
            elif family in ("HOLD", "LOCK"):
                out.append(f"dissolve({_e(a, b)}) | present({_e(a, c)}) & present({_e(b, c)}) => {grade}")
            else:
                raise BasinError(f"unknown family {family}")
    return out


def scaffold_expressions(mode: str) -> list[str]:
    if mode == "FREE":
        return []
    if mode == "HELD":
        return [f"dissolve({_e(a, b)}) => prohibit" for a, b in held_pairs()]
    raise BasinError(f"unknown mode {mode}")


def rules_for(family: str, n: int, grade: str | None, mode: str) -> tuple[Constraint, ...]:
    texts = template_expressions(family, n, grade) + scaffold_expressions(mode)
    rules = tuple(parse_expression(text, n, order=2) for text in texts)
    if family != "NULL" and FAMILY_K[family] is not None:
        if any(rule.k() != FAMILY_K[family] for rule in rules[: len(rules) - len(scaffold_expressions(mode))]):
            raise BasinError(f"{family} rule has the wrong K")
    return rules


def start_state(n: int, mode: str) -> int:
    if mode == "FREE":
        return 0
    index = edge_index(n)
    state = 0
    for a, b in held_pairs():
        state |= 1 << index[(a, b)]
    return state


def build(family: str, n: int, grade: str | None, mode: str) -> Kernel:
    return build_kernel(n, Choreography(0, 0, rules_for(family, n, grade, mode)), FACTORS)


def reachable(kernel: Kernel, start: int) -> list[int]:
    seen = {start}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for nxt, _prob in kernel.successors[state]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen)


def class_structure(kernel: Kernel, states: list[int]) -> dict:
    """Recurrent classes of the chain restricted to a reachable set (closed by construction)."""
    position = {s: i for i, s in enumerate(states)}
    successors = [[(position[t], p) for t, p in kernel.successors[s]] for s in states]
    components = strongly_connected_components(successors)
    member = {}
    for index, component in enumerate(components):
        for node in component:
            member[node] = index
    recurrent = []
    for index, component in enumerate(components):
        closed = all(member[t] == index for node in component for t, _p in successors[node])
        if closed:
            recurrent.append(sorted(states[node] for node in component))
    absorbing = [c[0] for c in recurrent if len(c) == 1]
    return {"absorbing_states": absorbing, "recurrent_classes": recurrent}


def _matrix(kernel: Kernel, states: list[int]) -> tuple[dict[int, int], np.ndarray]:
    position = {s: i for i, s in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    for s in states:
        for t, p in kernel.successors[s]:
            matrix[position[s], position[t]] += float(p)
    return position, matrix


def stationary_dense(kernel: Kernel, states: list[int]) -> tuple[np.ndarray, float]:
    _position, matrix = _matrix(kernel, states)
    size = len(states)
    system = matrix.T - np.eye(size)
    system[-1, :] = 1.0
    rhs = np.zeros(size)
    rhs[-1] = 1.0
    pi = np.linalg.solve(system, rhs)
    residual = float(np.abs(pi @ matrix - pi).sum())
    return pi, residual


def stationary_lazy(kernel: Kernel, states: list[int], *, tolerance: float = 1e-15, cap: int = FREE_MODE_ITERATION_CAP) -> tuple[np.ndarray, float, int]:
    """Lazy power iteration pi <- pi (I + P)/2. The lazy chain has P's stationary law and is aperiodic."""
    position = {s: i for i, s in enumerate(states)}
    rows, cols, vals = [], [], []
    for s in states:
        for t, p in kernel.successors[s]:
            rows.append(position[s])
            cols.append(position[t])
            vals.append(float(p))
    rows_a, cols_a, vals_a = np.array(rows), np.array(cols), np.array(vals)
    pi = np.full(len(states), 1.0 / len(states))
    iterations = 0
    for iterations in range(1, cap + 1):
        moved = np.bincount(cols_a, weights=pi[rows_a] * vals_a, minlength=len(pi))
        nxt = 0.5 * (pi + moved)
        delta = float(np.abs(nxt - pi).sum())
        pi = nxt
        if delta < tolerance:
            break
    moved = np.bincount(cols_a, weights=pi[rows_a] * vals_a, minlength=len(pi))
    return pi, float(np.abs(moved - pi).sum()), iterations


def total_rates(kernel: Kernel, states: list[int]) -> np.ndarray:
    return np.array([float(sum(kernel.weights[s])) for s in states])


def continuous_time(pi: np.ndarray, rates: np.ndarray) -> np.ndarray:
    """Stationary law of the continuous-time chain with per-slot rates equal to the event weights."""
    raw = pi / rates
    return raw / raw.sum()


DENSE_ABSORPTION_LIMIT = 4096
ABSORPTION_ITERATION_TOLERANCE = 1e-13
ABSORPTION_ITERATION_CAP = 2_000_000


def absorption(kernel: Kernel, states: list[int], start: int, absorbing: list[int]) -> dict:
    """Absorption probabilities and expected steps from ``start``.

    Dense LU on reachable sets of at most 4,096 states; above that, an
    iterative fixed-point solve h = Q h + r and t = 1 + Q t on the sparse
    transient matrix. The two paths agree on every set small enough for both.
    """
    absorbing_set = set(absorbing)
    if start in absorbing_set:
        return {"absorption_method": "start_absorbed", "absorption_probabilities": {str(s): (1.0 if s == start else 0.0) for s in absorbing}, "expected_steps_to_absorption": 0.0}
    transient = [s for s in states if s not in absorbing_set]
    tpos = {s: i for i, s in enumerate(transient)}
    apos = {s: i for i, s in enumerate(absorbing)}
    if len(states) <= DENSE_ABSORPTION_LIMIT:
        q = np.zeros((len(transient), len(transient)))
        r = np.zeros((len(transient), len(absorbing)))
        for s in transient:
            for t, p in kernel.successors[s]:
                if t in tpos:
                    q[tpos[s], tpos[t]] += float(p)
                else:
                    r[tpos[s], apos[t]] += float(p)
        fundamental = np.eye(len(transient)) - q
        probabilities = np.linalg.solve(fundamental, r)
        steps = np.linalg.solve(fundamental, np.ones(len(transient)))
        return {
            "absorption_method": "dense_solve",
            "absorption_probabilities": {str(s): float(probabilities[tpos[start], apos[s]]) for s in absorbing},
            "expected_steps_to_absorption": float(steps[tpos[start]]),
        }
    rows, cols, vals = [], [], []
    r = np.zeros((len(transient), len(absorbing)))
    for s in transient:
        for t, p in kernel.successors[s]:
            if t in tpos:
                rows.append(tpos[s])
                cols.append(tpos[t])
                vals.append(float(p))
            else:
                r[tpos[s], apos[t]] += float(p)
    rows_a, cols_a, vals_a = np.array(rows), np.array(cols), np.array(vals)
    size = len(transient)

    def apply(vector: np.ndarray) -> np.ndarray:
        return np.bincount(rows_a, weights=vals_a * vector[cols_a], minlength=size)

    steps = np.zeros(size)
    iterations = 0
    for iterations in range(1, ABSORPTION_ITERATION_CAP + 1):
        nxt = 1.0 + apply(steps)
        delta = float(np.abs(nxt - steps).max())
        steps = nxt
        if delta < ABSORPTION_ITERATION_TOLERANCE * max(1.0, float(steps.max())):
            break
    probabilities = {}
    for s, column in apos.items():
        h = r[:, column].copy()
        for _ in range(ABSORPTION_ITERATION_CAP):
            nxt = r[:, column] + apply(h)
            delta = float(np.abs(nxt - h).max())
            h = nxt
            if delta < ABSORPTION_ITERATION_TOLERANCE:
                break
        probabilities[str(s)] = float(h[tpos[start]])
    return {
        "absorption_iterations": iterations,
        "absorption_method": "sparse_iteration",
        "absorption_probabilities": probabilities,
        "expected_steps_to_absorption": float(steps[tpos[start]]),
    }


# --- observables --------------------------------------------------------


def _adjacency(state: int, n: int, edge_list: list[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for i, (a, b) in enumerate(edge_list):
        if (state >> i) & 1:
            adj[a].add(b)
            adj[b].add(a)
    return adj


def distance_to_source(state: int, n: int, edge_list: list[tuple[int, int]], probe: int) -> float:
    adj = _adjacency(state, n, edge_list)
    seen = {probe: 0}
    queue = deque([probe])
    while queue:
        node = queue.popleft()
        if node in source():
            return float(seen[node])
        for nxt in adj[node]:
            if nxt not in seen:
                seen[nxt] = seen[node] + 1
                queue.append(nxt)
    return math.inf


def triangles(state: int, n: int, edge_list: list[tuple[int, int]]) -> int:
    adj = _adjacency(state, n, edge_list)
    return sum(1 for a, b, c in itertools.combinations(range(n), 3) if b in adj[a] and c in adj[a] and c in adj[b])


def _shell(d: float) -> str:
    return "inf" if math.isinf(d) else str(int(d))


def held_observables(kernel: Kernel, states: list[int], law: np.ndarray, n: int, *, per_unit_time: bool = False) -> dict:
    """Jump clock: drift per event. Continuous clock: drift per unit time (event weights as rates)."""
    edge_list = edges(n)
    index = edge_index(n)
    src = source()
    probes = [p for p in range(n) if p not in src]
    source_slots = set(held_slot_indices(n))
    attach_slots = {i for i, (a, b) in enumerate(edge_list) if (a in src) != (b in src)}
    free_slots = [i for i in range(len(edge_list)) if i not in source_slots]
    del index
    dist = {p: {} for p in probes}
    drift_num = {p: {} for p in probes}
    drift_den = {p: {} for p in probes}
    escape_num = {p: {} for p in probes}
    capture_num = {p: 0.0 for p in probes}
    capture_den = {p: 0.0 for p in probes}
    by_k_attach: dict[int, float] = {}
    by_k_mass: dict[int, float] = {}
    exp_attach = 0.0
    exp_free = 0.0
    cache: dict[tuple[int, int], float] = {}

    def d_of(s: int, p: int) -> float:
        key = (s, p)
        if key not in cache:
            cache[key] = distance_to_source(s, n, edge_list, p)
        return cache[key]

    for i, s in enumerate(states):
        w = float(law[i])
        attach = sum(1 for slot in attach_slots if (s >> slot) & 1)
        free = sum(1 for slot in free_slots if (s >> slot) & 1)
        exp_attach += w * attach
        exp_free += w * free
        by_k_attach[free] = by_k_attach.get(free, 0.0) + w * attach
        by_k_mass[free] = by_k_mass.get(free, 0.0) + w
        for p in probes:
            d = d_of(s, p)
            shell = _shell(d)
            dist[p][shell] = dist[p].get(shell, 0.0) + w
            change = 0.0
            enter = 0.0
            escape = 0.0
            scale = float(sum(kernel.weights[s])) if per_unit_time else 1.0
            for t, prob in kernel.successors[s]:
                dt = d_of(t, p)
                rate = float(prob) * scale
                if math.isinf(d):
                    if not math.isinf(dt):
                        enter += rate
                elif math.isinf(dt):
                    escape += rate
                else:
                    change += rate * (dt - d)
            if math.isinf(d):
                capture_num[p] += w * enter
                capture_den[p] += w
            else:
                drift_num[p][shell] = drift_num[p].get(shell, 0.0) + w * change
                escape_num[p][shell] = escape_num[p].get(shell, 0.0) + w * escape
                drift_den[p][shell] = drift_den[p].get(shell, 0.0) + w
    avg_dist: dict[str, float] = {}
    for p in probes:
        for shell, mass in dist[p].items():
            avg_dist[shell] = avg_dist.get(shell, 0.0) + mass / len(probes)
    drift: dict[str, float] = {}
    escape: dict[str, float] = {}
    for shell in sorted({sh for p in probes for sh in drift_den[p]}):
        num = sum(drift_num[p].get(shell, 0.0) for p in probes)
        den = sum(drift_den[p].get(shell, 0.0) for p in probes)
        if den > 0:
            drift[shell] = num / den
            escape[shell] = sum(escape_num[p].get(shell, 0.0) for p in probes) / den
    capture = sum(capture_num.values()) / sum(capture_den.values()) if sum(capture_den.values()) > 0 else None
    return {
        "attachment_fraction": exp_attach / exp_free if exp_free > 0 else None,
        "attachment_fraction_by_free_edge_count": {str(k): (by_k_attach[k] / (by_k_mass[k] * k) if k > 0 and by_k_mass[k] > 0 else None) for k in sorted(by_k_mass)},
        "attachment_slots": len(attach_slots),
        "distance_distribution": dict(sorted(avg_dist.items())),
        "expected_free_edges": exp_free,
        "free_edge_count_distribution": {str(k): by_k_mass[k] for k in sorted(by_k_mass)},
        "free_slots": len(free_slots),
        "null_attachment_fraction": len(attach_slots) / len(free_slots),
        "capture_rate_when_detached": capture,
        "clock": "continuous_per_unit_time" if per_unit_time else "jump_per_event",
        "escape_rate_to_detached": escape,
        "radial_drift_among_finite_moves": drift,
    }


def free_observables(states: list[int], law: np.ndarray, n: int) -> dict:
    edge_list = edges(n)
    tri_by_k: dict[int, float] = {}
    mass_by_k: dict[int, float] = {}
    for i, s in enumerate(states):
        w = float(law[i])
        k = s.bit_count()
        tri_by_k[k] = tri_by_k.get(k, 0.0) + w * triangles(s, n, edge_list)
        mass_by_k[k] = mass_by_k.get(k, 0.0) + w
    return {
        "edge_count_distribution": {str(k): mass_by_k[k] for k in sorted(mass_by_k)},
        "expected_edges": sum(k * m for k, m in mass_by_k.items()),
        "expected_triangles": sum(tri_by_k.values()),
        "triangles_given_edge_count": {str(k): (tri_by_k[k] / mass_by_k[k] if mass_by_k[k] > 0 else None) for k in sorted(mass_by_k)},
    }


def null_triangles_given_edges(n: int) -> dict[str, float]:
    """Mean triangle count over all labelled graphs with k edges: the uniform conditional law."""
    edge_list = edges(n)
    total: dict[int, int] = {}
    count: dict[int, int] = {}
    for s in range(1 << len(edge_list)):
        k = s.bit_count()
        total[k] = total.get(k, 0) + triangles(s, n, edge_list)
        count[k] = count.get(k, 0) + 1
    return {str(k): total[k] / count[k] for k in sorted(count)}


def analyse_item(item: dict) -> dict:
    family, n, grade, mode = item["family"], item["n"], item["grade"], item["mode"]
    kernel = build(family, n, grade, mode)
    start = start_state(n, mode)
    states = reachable(kernel, start)
    structure = class_structure(kernel, states)
    out: dict = {
        "family": family,
        "grade": grade,
        "K": FAMILY_K[family],
        "mode": mode,
        "n": n,
        "reachable_states": len(states),
        "recurrent_class_count": len(structure["recurrent_classes"]),
        "recurrent_class_sizes": [len(c) for c in structure["recurrent_classes"]],
        "absorbing_state_count": len(structure["absorbing_states"]),
        "rule_instances": len(rules_for(family, n, grade, mode)),
    }
    if structure["absorbing_states"] and len(structure["recurrent_classes"]) == len(structure["absorbing_states"]):
        out["regime"] = "absorbing"
        out["absorbing_states"] = structure["absorbing_states"]
        out["absorbing_edge_counts"] = [s.bit_count() for s in structure["absorbing_states"]]
        out.update(absorption(kernel, states, start, structure["absorbing_states"]))
        return out
    if len(structure["recurrent_classes"]) != 1 or len(structure["recurrent_classes"][0]) != len(states):
        out["regime"] = "mixed"
        return out
    out["regime"] = "recurrent"
    if len(states) <= 4096:
        pi, residual = stationary_dense(kernel, states)
        out["stationary_method"] = "dense_solve"
        out["iterations"] = None
    else:
        pi, residual, iterations = stationary_lazy(kernel, states)
        out["stationary_method"] = "lazy_iteration"
        out["iterations"] = iterations
    if residual > STATIONARY_RESIDUAL_TOLERANCE or (pi < -1e-15).any():
        raise BasinError(f"stationary residual {residual} on {item}")
    rates = total_rates(kernel, states)
    ct = continuous_time(pi, rates)
    out["stationary_residual"] = residual
    out["max_deviation_from_uniform"] = {"continuous": float(np.abs(ct - 1.0 / len(states)).max()), "jump": float(np.abs(pi - 1.0 / len(states)).max())}
    observe = held_observables if mode == "HELD" else None
    if mode == "HELD":
        out["jump"] = observe(kernel, states, pi, n)
        out["continuous"] = observe(kernel, states, ct, n, per_unit_time=True)
    else:
        out["jump"] = free_observables(states, pi, n)
        out["continuous"] = free_observables(states, ct, n)
    return out


def items() -> list[dict]:
    out = []
    for n in SIZES:
        for mode in MODES:
            for family, grades in FAMILY_GRADES.items():
                for grade in grades:
                    out.append({"family": family, "grade": grade, "item_id": f"{mode}-N{n}-{family}-{grade or 'none'}", "mode": mode, "n": n})
    return out
