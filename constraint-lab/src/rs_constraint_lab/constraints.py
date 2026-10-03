"""Constraint DSL.

A constraint is one action literal and zero or more condition literals,
conjoined, with a named weight:

    form(0-1) | present(0-2) & absent(1-2) => weak_suppress
    dissolve(0-1) => prohibit
    form(0-1) | count>=2 => strong_favour

The action literal already fixes the prior incidence of its own edge
(formation requires absence, dissolution requires presence). A condition on
the action edge is either contradictory or redundant and is not part of the
normal form.

``K`` is the number of literals: 1 for the action, plus one per edge
condition, plus one per occupation-count literal. ``A`` is the number of
distinct entities named by the action and the edge conditions. A count
literal names no entity. It reads the number of present pairwise edges in
the whole state.

The structural identity is polarity, action, edge conditions, and count
literals. The weight is an attribute of that identity, not part of it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rs_constraint_lab.state import edges

FORM = 1
DISSOLVE = -1

_HEAD = re.compile(
    r"^(form|dissolve)\((\d+)-(\d+)\)(?: \| (.+))?$"
)
_WEIGHT = re.compile(r"^[a-z_]+$")
_COND = re.compile(r"^(present|absent)\((\d+)-(\d+)\)$")
_COUNT = re.compile(r"^count\s*(>=|<=|==)\s*(\d+)$")

_COUNT_OP = {">=": "ge", "<=": "le", "==": "eq"}
_COUNT_SYMBOL = {"ge": ">=", "le": "<=", "eq": "=="}


@dataclass(frozen=True, slots=True)
class Constraint:
    polarity: int
    action: int
    conditions: tuple[tuple[int, int], ...]
    weight: str
    counts: tuple[tuple[str, int], ...] = ()

    def k(self) -> int:
        return 1 + len(self.conditions) + len(self.counts)

    def structural_key(self) -> tuple:
        return (self.polarity, self.action, self.conditions, self.counts)

    def key(self) -> tuple:
        return self.structural_key() + (self.weight,)

    def matches(self, state: int, edge: int) -> bool:
        if edge != self.action:
            return False
        present = (state >> edge) & 1
        if self.polarity == FORM and present:
            return False
        if self.polarity == DISSOLVE and not present:
            return False
        for conditioned, required in self.conditions:
            if ((state >> conditioned) & 1) != required:
                return False
        if self.counts:
            occupied = state.bit_count()
            for op, threshold in self.counts:
                if op == "ge" and occupied < threshold:
                    return False
                if op == "le" and occupied > threshold:
                    return False
                if op == "eq" and occupied != threshold:
                    return False
        return True

    def expression(self, edge_list: list[tuple[int, int]]) -> str:
        a, b = edge_list[self.action]
        verb = "form" if self.polarity == FORM else "dissolve"
        head = f"{verb}({a}-{b})"
        parts = []
        for conditioned, required in self.conditions:
            i, j = edge_list[conditioned]
            kind = "present" if required else "absent"
            parts.append(f"{kind}({i}-{j})")
        for op, threshold in self.counts:
            parts.append(f"count{_COUNT_SYMBOL[op]}{threshold}")
        if not parts:
            return f"{head} => {self.weight}"
        return f"{head} | " + " & ".join(parts) + f" => {self.weight}"

    def arity(self, edge_list: list[tuple[int, int]]) -> int:
        named = set(edge_list[self.action])
        for conditioned, _required in self.conditions:
            named.update(edge_list[conditioned])
        return len(named)

    def has_count_literal(self) -> bool:
        return bool(self.counts)


def structurally_simple(constraints) -> bool:
    """True when each structural identity occurs at most once."""
    seen = set()
    for constraint in constraints:
        key = constraint.structural_key()
        if key in seen:
            return False
        seen.add(key)
    return True


def count_literal_status(polarity: int, op: str, threshold: int, slots: int) -> str:
    """Classify one occupation literal given the action precondition.

    The count is the number of present pairwise edges in the current state.
    Formation can fire only when its own edge is absent, so the count is at
    most ``slots - 1``. Dissolution can fire only when its own edge is
    present, so the count is at least 1. Literals that are true on every
    state the action can match are tautologies. Literals that are false on
    every such state are unsatisfiable. Both are excluded from the grammar.
    """
    if op not in _COUNT_SYMBOL:
        raise ValueError(f"unknown count operator {op!r}")
    if threshold < 0 or threshold > slots:
        return "unsatisfiable"
    if op == "ge" and threshold == 0:
        return "tautology"
    if op == "le" and threshold == slots:
        return "tautology"
    if polarity == FORM:
        if op == "ge" and threshold >= slots:
            return "unsatisfiable"
        if op == "eq" and threshold >= slots:
            return "unsatisfiable"
        if op == "le" and threshold >= slots - 1:
            return "tautology"
    elif polarity == DISSOLVE:
        if op == "le" and threshold <= 0:
            return "unsatisfiable"
        if op == "eq" and threshold <= 0:
            return "unsatisfiable"
        if op == "ge" and threshold <= 1:
            return "tautology"
    else:
        raise ValueError(f"unknown polarity {polarity}")
    return "ok"


def count_candidates(slots: int) -> tuple[tuple[str, int], ...]:
    """Every globally well-typed literal, including ones the action later drops."""
    literals = []
    for threshold in range(slots + 1):
        literals.append(("ge", threshold))
    for threshold in range(slots + 1):
        literals.append(("le", threshold))
    for threshold in range(slots + 1):
        literals.append(("eq", threshold))
    return tuple(literals)


def relabel_constraint(constraint: Constraint, edge_map: tuple[int, ...]) -> Constraint:
    conditions = tuple(
        sorted((edge_map[edge], bit) for edge, bit in constraint.conditions)
    )
    return Constraint(
        constraint.polarity,
        edge_map[constraint.action],
        conditions,
        constraint.weight,
        constraint.counts,
    )


def parse_expression(text: str, n: int) -> Constraint:
    raw = text.strip()
    left, separator, weight = raw.rpartition(" => ")
    if not separator or _WEIGHT.fullmatch(weight) is None:
        raise ValueError(f"unreadable constraint expression: {text!r}")
    match = _HEAD.fullmatch(left)
    if match is None:
        raise ValueError(f"unreadable constraint expression: {text!r}")
    verb, a_text, b_text, condition_text = match.groups()
    a, b = int(a_text), int(b_text)
    if a > b:
        a, b = b, a
    index = {pair: i for i, pair in enumerate(edges(n))}
    try:
        action = index[(a, b)]
    except KeyError as exc:
        raise ValueError(f"edge {(a, b)} is not an edge on N={n}") from exc
    conditions: list[tuple[int, int]] = []
    counts: list[tuple[str, int]] = []
    if condition_text:
        for part in condition_text.split("&"):
            part = part.strip()
            cond = _COND.match(part)
            if cond is not None:
                kind, i_text, j_text = cond.groups()
                i, j = int(i_text), int(j_text)
                if i > j:
                    i, j = j, i
                try:
                    edge = index[(i, j)]
                except KeyError as exc:
                    raise ValueError(f"edge {(i, j)} is not an edge on N={n}") from exc
                if edge == action:
                    raise ValueError(
                        f"condition on the action edge is not normal form: {text!r}"
                    )
                conditions.append((edge, 1 if kind == "present" else 0))
                continue
            counted = _COUNT.match(part)
            if counted is None:
                raise ValueError(f"unreadable condition {part!r} in {text!r}")
            symbol, threshold_text = counted.groups()
            counts.append((_COUNT_OP[symbol], int(threshold_text)))
    conditions_tuple = tuple(sorted(conditions))
    counts_tuple = tuple(sorted(counts))
    if len(conditions_tuple) != len(set(conditions)):
        raise ValueError(f"repeated condition in {text!r}")
    if len(counts_tuple) != len(set(counts)):
        raise ValueError(f"repeated count literal in {text!r}")
    if len(counts_tuple) > 1:
        raise ValueError(f"a normal form has at most one count literal: {text!r}")
    polarity = FORM if verb == "form" else DISSOLVE
    return Constraint(polarity, action, conditions_tuple, weight, counts_tuple)


@dataclass(frozen=True, slots=True)
class Choreography:
    """Active constraints at H=0, L=0.

    The kernel calls ``active`` on every state. History and constraint-state
    arguments are part of the call so a later choreography can gate or rewrite
    constraints without a second kernel.
    """

    history_depth: int
    meta_depth: int
    constraints: tuple[Constraint, ...]

    def active(self, state: int, history: tuple, constraint_state: dict) -> tuple[Constraint, ...]:
        del state
        if self.history_depth != 0 or self.meta_depth != 0:
            raise NotImplementedError(
                "H>0 or L>0 choreography is represented and not executed in this generation"
            )
        if history or constraint_state:
            raise NotImplementedError(
                "non-empty history or constraint state is outside H=0, L=0"
            )
        return self.constraints
