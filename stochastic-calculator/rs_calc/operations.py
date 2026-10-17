"""Arithmetic as population redistribution, composition, and matching."""

from dataclasses import dataclass, replace

from .engine import Engine, Population


@dataclass
class Value:
    population: Population
    remainder: Population | None = None

    def composable(self) -> Population:
        if self.remainder:
            raise ValueError("Non-exact division cannot be chained implicitly; use // or %")
        return self.population


def reopen(population: Population) -> Population:
    return [replace(e, ready=False) for e in population]


def add(left: Population, right: Population, engine: Engine) -> Population:
    state = reopen(left)
    state.extend(reopen(right))
    return engine.normalize(state)


def subtract(left: Population, right: Population, engine: Engine) -> Population:
    return add(left, engine.invert(right), engine)


def multiply(left: Population, right: Population, engine: Engine,
             model: str = "product") -> Population:
    left = engine.normalize(left)
    right = engine.normalize(right)
    if model == "repeated":
        output: Population = []
        pending = list(left)
        while pending:
            anchor = engine.choose(pending)
            pending.remove(anchor)
            replica = [engine.relation(anchor.positive == edge.positive) for edge in right]
            engine.event("replicate_row", anchor=(anchor.source, anchor.target), size=len(replica))
            output = add(output, replica, engine)
        return output
    if model != "product":
        raise ValueError("Unknown multiplication model")
    # Each pair is an incidence relation between operand relations, consumed once.
    obligations = []
    output = []
    engine.context = {"kind": "product", "obligations": obligations, "output": output}
    for a in left:
        for b in right:
            obligations.append((a, b))
            engine.check_size(obligations)
    engine.event("product_initial", obligations=[
        ((a.positive, a.source, a.target), (b.positive, b.source, b.target))
        for a, b in obligations])
    while obligations:
        pair = engine.choose(obligations)
        obligations.remove(pair)
        a, b = pair
        edge = engine.relation(a.positive == b.positive)
        output.append(edge)
        engine.event("compose", left=(a.positive, a.source, a.target),
                     right=(b.positive, b.source, b.target),
                     output=(edge.positive, edge.source, edge.target))
    return engine.normalize(output)


def divide(left: Population, right: Population, engine: Engine) -> Value:
    dividend = engine.normalize(left)
    divisor = engine.normalize(right)
    if not divisor:
        raise ZeroDivisionError("Division by zero has no admissible partition")
    positive = not dividend or dividend[0].positive == divisor[0].positive
    available = list(dividend)
    quotient = []
    engine.context = {"kind": "partition", "available": available, "quotient": quotient}
    while available:
        slots = list(divisor)
        bindings = []
        engine.context.update(slots=slots, bindings=bindings)
        while slots and available:
            slot = engine.choose(slots)
            unit = engine.choose(available)
            slots.remove(slot)
            available.remove(unit)
            bindings.append((slot, unit))
            engine.event("bind", slot=(slot.source, slot.target),
                         unit=(unit.source, unit.target))
        if slots:
            residual = [unit for _, unit in bindings]
            engine.event("residual", unmatched_slots=len(slots), residual=len(residual))
            return Value(engine.normalize(quotient), engine.normalize(residual))
        # The gate depends on complete injective matching, not a numeric quotient.
        edge = engine.relation(positive)
        quotient.append(edge)
        engine.event("partition_commit", bindings=[
            ((s.source, s.target), (u.source, u.target)) for s, u in bindings],
            output=(edge.positive, edge.source, edge.target))
    return Value(engine.normalize(quotient), [])
