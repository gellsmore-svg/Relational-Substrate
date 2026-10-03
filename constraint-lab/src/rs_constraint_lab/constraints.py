"""Constraint DSL.

A constraint is one action literal and zero or more condition literals,
conjoined, with a named weight:

    form(0-1) | present(0-2) & absent(1-2) => weak_suppress
    dissolve(0-1) => prohibit

The action literal already fixes the prior incidence of its own edge
(formation requires absence, dissolution requires presence). A condition on
the action edge is either contradictory or redundant and is not part of the
normal form.

``K`` is the number of literals: 1 for the action, plus one per condition.
``A`` is the number of distinct entities named by those literals.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rs_constraint_lab.state import edges

FORM = 1
DISSOLVE = -1

_EXPR = re.compile(
    r"^(form|dissolve)\((\d+)-(\d+)\)(?: \| ([^=]+))? => ([a-z_]+)$"
)
_COND = re.compile(r"^(present|absent)\((\d+)-(\d+)\)$")


@dataclass(frozen=True, slots=True)
class Constraint:
    polarity: int
    action: int
    conditions: tuple[tuple[int, int], ...]
    weight: str

    def k(self) -> int:
        return 1 + len(self.conditions)

    def key(self) -> tuple:
        return (self.polarity, self.action, self.conditions, self.weight)

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
        return True

    def expression(self, edge_list: list[tuple[int, int]]) -> str:
        a, b = edge_list[self.action]
        verb = "form" if self.polarity == FORM else "dissolve"
        head = f"{verb}({a}-{b})"
        if not self.conditions:
            return f"{head} => {self.weight}"
        parts = []
        for conditioned, required in self.conditions:
            i, j = edge_list[conditioned]
            kind = "present" if required else "absent"
            parts.append(f"{kind}({i}-{j})")
        return f"{head} | " + " & ".join(parts) + f" => {self.weight}"

    def arity(self, edge_list: list[tuple[int, int]]) -> int:
        named = set(edge_list[self.action])
        for conditioned, _required in self.conditions:
            named.update(edge_list[conditioned])
        return len(named)


def relabel_constraint(constraint: Constraint, edge_map: tuple[int, ...]) -> Constraint:
    conditions = tuple(
        sorted((edge_map[edge], bit) for edge, bit in constraint.conditions)
    )
    return Constraint(constraint.polarity, edge_map[constraint.action], conditions, constraint.weight)


def parse_expression(text: str, n: int) -> Constraint:
    match = _EXPR.match(text.strip())
    if match is None:
        raise ValueError(f"unreadable constraint expression: {text!r}")
    verb, a_text, b_text, condition_text, weight = match.groups()
    a, b = int(a_text), int(b_text)
    if a > b:
        a, b = b, a
    index = {pair: i for i, pair in enumerate(edges(n))}
    try:
        action = index[(a, b)]
    except KeyError as exc:
        raise ValueError(f"edge {(a, b)} is not an edge on N={n}") from exc
    conditions: list[tuple[int, int]] = []
    if condition_text:
        for part in condition_text.split("&"):
            part = part.strip()
            cond = _COND.match(part)
            if cond is None:
                raise ValueError(f"unreadable condition {part!r} in {text!r}")
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
    conditions_tuple = tuple(sorted(conditions))
    if len(conditions_tuple) != len(set(conditions)):
        raise ValueError(f"repeated condition in {text!r}")
    polarity = FORM if verb == "form" else DISSOLVE
    return Constraint(polarity, action, conditions_tuple, weight)


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
