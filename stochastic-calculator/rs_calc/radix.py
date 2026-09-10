"""Decimal coordination experiment, independently of the unary calculator."""

from dataclasses import dataclass, replace

from .engine import Engine, Relation


@dataclass(frozen=True)
class DigitRelation:
    edge: Relation
    column: int


@dataclass(frozen=True)
class Gate:
    instance: int
    members: tuple[DigitRelation, ...]
    phase: str


def encode_decimal(value: int, engine: Engine) -> list[DigitRelation]:
    if type(value) is not int:
        raise TypeError("Integer required")
    state = []
    for column, digit in enumerate(reversed(str(abs(value)))):
        for _ in range(int(digit)):
            state.append(DigitRelation(engine.relation(value >= 0), column))
    engine.check_size(state)
    return state


def view(state: list[DigitRelation]):
    return sorted((d.column, d.edge.positive, d.edge.source, d.edge.target) for d in state)


def decode_decimal(state: list[DigitRelation]) -> str:
    if not state:
        return "0"
    if len({d.edge.positive for d in state}) != 1:
        raise ValueError("Mixed signs are not a decimal normal form")
    digits = []
    for column in range(max(d.column for d in state) + 1):
        units = [d for d in state if d.column == column]
        if len(units) >= 10:
            raise ValueError("Unresolved decimal bundle")
        digits.append(str(len(units)))
    number = "".join(reversed(digits))
    return number if state[0].edge.positive else "-" + number


def resolve(state: list[DigitRelation], engine: Engine,
            coordination: bool = True) -> list[DigitRelation]:
    state = list(state)
    gates: list[Gate] = []
    engine.context = {"kind": "radix", "population": state, "gates": gates}
    engine.event("radix_initial", state=view(state))
    while True:
        engine.check_size(state)
        actions = []
        columns = sorted({d.column for d in state})
        for col in columns:
            pos = [d for d in state if d.column == col and d.edge.positive]
            neg = [d for d in state if d.column == col and not d.edge.positive]
            if pos and neg:
                actions.append(("cancel", (pos, neg)))
        mixed = len({d.edge.positive for d in state}) > 1
        if not actions and mixed and not gates:
            for high in state:
                if any(low.column < high.column and low.edge.positive != high.edge.positive
                       for low in state):
                    actions.append(("borrow", high))
        if not mixed:
            for col in columns:
                for sign in [True, False]:
                    members = [d for d in state if d.column == col and d.edge.positive == sign]
                    if len(members) >= 10:
                        actions.append(("transmit", members))
        for gate in gates:
            actions.append((gate.phase, gate))
        if not actions:
            engine.event("radix_normal_form", state=view(state))
            return state
        kind, payload = engine.choose(actions)
        if kind == "cancel":
            pos, neg = payload
            a, b = engine.choose(pos), engine.choose(neg)
            state.remove(a)
            state.remove(b)
            engine.event("digit_cancel", column=a.column,
                         incidence=((a.edge.source, a.edge.target), (b.edge.source, b.edge.target)))
        elif kind == "borrow":
            high = payload
            state.remove(high)
            replacements = [DigitRelation(engine.relation(high.edge.positive), high.column - 1)
                            for _ in range(10)]
            state.extend(replacements)
            engine.event("borrow_split", source_column=high.column, outputs=view(replacements))
        elif kind == "transmit":
            pool = list(payload)
            chosen = []
            for _ in range(10):
                edge = engine.choose(pool)
                pool.remove(edge)
                chosen.append(edge)
                state.remove(edge)
            engine.serial += 1
            gate = Gate(engine.serial, tuple(chosen), "carry")
            gates.append(gate)
            engine.event("transmit", column=chosen[0].column, members=view(chosen))
        elif kind == "carry":
            gate = payload
            gates.remove(gate)
            engine.serial += 1
            gates.append(replace(gate, instance=engine.serial, phase="receive"))
            engine.event("carry", column=gate.members[0].column,
                         instance_replaced=True, members=view(list(gate.members)))
        else:
            gate = payload
            gates.remove(gate)
            exemplar = gate.members[0]
            output = DigitRelation(engine.relation(exemplar.edge.positive), exemplar.column + 1)
            state.append(output)
            engine.event("receive", output=view([output]))
            if engine.rng.random() < engine.config.fault_rate:
                admitted = not coordination or engine.rng.random() >= engine.config.strength
                engine.event("replay_admitted" if admitted else "replay_rejected",
                             column=output.column)
                if admitted:
                    state.append(DigitRelation(engine.relation(exemplar.edge.positive), output.column))
