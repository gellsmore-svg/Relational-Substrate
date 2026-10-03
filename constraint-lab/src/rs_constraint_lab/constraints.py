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

    def expression(self, edge_list: list[tuple[int, ...]]) -> str:
        def render(slot: tuple[int, ...]) -> str:
            return "-".join(str(entity) for entity in slot)

        verb = "form" if self.polarity == FORM else "dissolve"
        head = f"{verb}({render(edge_list[self.action])})"
        parts = []
        for conditioned, required in self.conditions:
            kind = "present" if required else "absent"
            parts.append(f"{kind}({render(edge_list[conditioned])})")
        for op, threshold in self.counts:
            parts.append(f"count{_COUNT_SYMBOL[op]}{threshold}")
        if not parts:
            return f"{head} => {self.weight}"
        return f"{head} | " + " & ".join(parts) + f" => {self.weight}"

    def arity(self, edge_list: list[tuple[int, ...]]) -> int:
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


def cross_order_class(constraint: Constraint, n_pairs: int) -> str:
    """Classify one constraint by what it reads and what it toggles.

    Pair slots are the indexes below ``n_pairs``. Higher-order slots are the
    rest. A bare pair action is ``P->P``. A bare triadic action is ``T->T``.
    ``P->T`` reads a pair and toggles the higher-order relation. ``T->P``
    reads the higher-order relation and toggles a pair. A condition list that
    reads both orders is ``mixed``.
    """
    action_higher = constraint.action >= n_pairs
    reads_pair = any(slot < n_pairs for slot, _bit in constraint.conditions)
    reads_higher = any(slot >= n_pairs for slot, _bit in constraint.conditions)
    if reads_pair and reads_higher:
        return "mixed"
    if action_higher and reads_pair:
        return "P->T"
    if (not action_higher) and reads_higher:
        return "T->P"
    if action_higher:
        return "T->T"
    return "P->P"


def set_cross_order_class(constraints, n_pairs: int) -> str:
    found = {cross_order_class(constraint, n_pairs) for constraint in constraints}
    if not found:
        return "P->P"
    if len(found) == 1:
        return found.pop()
    return "mixed"


_HEAD_SLOT = re.compile(r"^(form|dissolve)\(([^)]+)\)(?: \| (.+))?$")
_COND_SLOT = re.compile(r"^(present|absent)\(([^)]+)\)$")


def _relation_entities(body: str, n: int) -> tuple[int, ...]:
    parts = [part.strip() for part in body.split("-")]
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError(f"unreadable relation {body!r}")
    entities = tuple(int(part) for part in parts)
    if len(entities) not in (2, 3):
        raise ValueError(f"a relation literal names 2 or 3 entities, not {body!r}")
    if len(set(entities)) != len(entities):
        raise ValueError(f"repeated entity in {body!r}")
    if any(entity < 0 or entity >= n for entity in entities):
        raise ValueError(f"entity outside 0..{n - 1} in {body!r}")
    return tuple(sorted(entities))


def _parse_independent_hypergraph(text: str, n: int) -> Constraint:
    """Order-3 parser. Pair literals stay pair slots. A triple is its own slot.

    Count literals are refused. They would otherwise read the triad bit as
    though it were another pairwise edge.
    """
    from rs_constraint_lab.state import relation_slots

    raw = text.strip()
    left, separator, weight = raw.rpartition(" => ")
    if not separator or _WEIGHT.fullmatch(weight) is None:
        raise ValueError(f"unreadable constraint expression: {text!r}")
    match = _HEAD_SLOT.fullmatch(left)
    if match is None:
        raise ValueError(f"unreadable constraint expression: {text!r}")
    verb, action_body, condition_text = match.groups()
    slots = relation_slots(n, 3)
    index = {slot: i for i, slot in enumerate(slots)}
    try:
        action = index[_relation_entities(action_body, n)]
    except KeyError as exc:
        raise ValueError(f"relation {action_body!r} is not a slot on N={n} at order 3") from exc
    except ValueError as exc:
        raise ValueError(f"unreadable constraint expression: {text!r}") from exc
    conditions: list[tuple[int, int]] = []
    if condition_text:
        for part in condition_text.split("&"):
            part = part.strip()
            if _COUNT.match(part) is not None:
                raise ValueError(
                    "count predicates are not part of the independent-hypergraph grammar: "
                    f"{text!r}"
                )
            cond = _COND_SLOT.fullmatch(part)
            if cond is None:
                raise ValueError(f"unreadable condition {part!r} in {text!r}")
            kind, body = cond.groups()
            try:
                slot = index[_relation_entities(body, n)]
            except KeyError as exc:
                raise ValueError(f"relation {body!r} is not a slot on N={n} at order 3") from exc
            if slot == action:
                raise ValueError(f"condition on the action slot is not normal form: {text!r}")
            conditions.append((slot, 1 if kind == "present" else 0))
    conditions_tuple = tuple(sorted(conditions))
    if len(conditions_tuple) != len(set(conditions)):
        raise ValueError(f"repeated condition in {text!r}")
    polarity = FORM if verb == "form" else DISSOLVE
    return Constraint(polarity, action, conditions_tuple, weight, ())


def match_entities_look_triadic(body: str) -> bool:
    parts = [part.strip() for part in body.split("-")]
    return len(parts) >= 3 and all(part.isdigit() for part in parts)


def parse_expression(text: str, n: int, *, order: int = 2) -> Constraint:
    if order == 3:
        return _parse_independent_hypergraph(text, n)
    if order != 2:
        raise ValueError(f"relation order {order} is not executable")
    raw = text.strip()
    left, separator, weight = raw.rpartition(" => ")
    if not separator or _WEIGHT.fullmatch(weight) is None:
        raise ValueError(f"unreadable constraint expression: {text!r}")
    slot_head = _HEAD_SLOT.fullmatch(left)
    if slot_head is not None and match_entities_look_triadic(slot_head.group(2)):
        raise ValueError(
            f"a triadic literal is not a pairwise constraint: {text!r}"
        )
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
