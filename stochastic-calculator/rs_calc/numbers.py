"""Explicit boundary transducers, not an expression evaluator."""

from .engine import Engine, Population


def encode(value: int, engine: Engine) -> Population:
    if type(value) is not int:
        raise TypeError("Integer operands required")
    magnitude = abs(value)
    if magnitude > engine.config.max_relations:
        from .engine import ResourceLimit
        raise ResourceLimit("Input exceeds unary population budget")
    return [engine.relation(value >= 0) for _ in range(magnitude)]


def decode(population: Population) -> int:
    if any(not e.ready for e in population):
        raise ValueError("Cannot decode an unfinished output")
    signs = {e.positive for e in population}
    if len(signs) > 1:
        raise ValueError("Cannot decode a non-normal population")
    magnitude = len(population)
    return magnitude if not population or population[0].positive else -magnitude
