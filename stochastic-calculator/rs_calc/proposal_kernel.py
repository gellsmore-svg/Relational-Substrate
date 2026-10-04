"""Fixed proposal grammar with separately enforceable, answer-blind constraints.

This module has no numeric encoder, decoder, target, or verification dependency.
Indices and counts below address storage, not arithmetic operand values.
"""

from dataclasses import dataclass, replace
import random
from collections.abc import Iterator


KINDS = ("birth", "death", "flip", "pair_birth", "cancel", "rewire", "ready", "unready")


@dataclass(frozen=True)
class Bond:
    positive: bool
    source: int
    target: int
    ready: bool = False


@dataclass(frozen=True)
class Constraints:
    conservation: float = 1.0
    no_growth: bool = True
    readiness: bool = True
    local_cancel: bool = False

    def __post_init__(self):
        if not 0 <= self.conservation <= 1:
            raise ValueError("conservation must lie in [0, 1]")


@dataclass(frozen=True)
class Proposal:
    kind: str
    first: int
    second: int
    source: int
    target: int
    positive: bool
    enforcement: float


def proposals(seed: int, horizon: int, regions: int) -> Iterator[Proposal]:
    if horizon < 1 or regions < 2:
        raise ValueError("Positive horizon and at least two regions required")
    rng = random.Random(seed)
    for _ in range(horizon):
        # Draw every field unconditionally: ablations consume exactly the same tape.
        yield Proposal(rng.choice(KINDS), rng.getrandbits(64), rng.getrandbits(64),
                       rng.randrange(regions), rng.randrange(regions),
                       bool(rng.getrandbits(1)), rng.random())


def transition(state: tuple[Bond, ...], p: Proposal, c: Constraints,
               capacity: int) -> tuple[tuple[Bond, ...], str]:
    if capacity < 1 or len(state) > capacity:
        raise ValueError("Invalid population capacity")
    if p.kind not in KINDS:
        raise ValueError("Unknown proposal")
    growth = p.kind in {"birth", "pair_birth"}
    if not growth and not state:
        return state, "inapplicable"
    i = p.first % len(state) if state else 0
    j = p.second % len(state) if state else 0
    if p.kind == "cancel" and i == j:
        return state, "inapplicable"
    if p.kind == "cancel" and c.local_cancel and state[i].target != state[j].target:
        return state, "locality"
    violates_charge = p.kind in {"birth", "death", "flip"}
    if p.kind == "cancel":
        violates_charge = state[i].positive == state[j].positive
    if violates_charge and p.enforcement < c.conservation:
        return state, "conservation"
    if growth and c.no_growth:
        return state, "growth"
    if p.kind == "unready" and state[i].ready and c.readiness:
        return state, "readiness"
    if growth:
        extra = (Bond(p.positive, p.source, p.target),)
        if p.kind == "pair_birth":
            extra += (Bond(not p.positive, p.target, p.source),)
        if len(state) + len(extra) > capacity:
            return state, "capacity"
        return state + extra, "accepted"
    if p.kind in {"death", "cancel"}:
        removed = {i, j} if p.kind == "cancel" else {i}
        return tuple(b for k, b in enumerate(state) if k not in removed), "accepted"
    b = state[i]
    if p.kind == "flip":
        new = replace(b, positive=not b.positive)
    elif p.kind == "rewire":
        new = replace(b, source=b.target, target=p.target)
    else:
        new = replace(b, ready=p.kind == "ready")
    if new == b:
        return state, "noop"
    out = list(state)
    out[i] = new
    return tuple(out), "accepted"
