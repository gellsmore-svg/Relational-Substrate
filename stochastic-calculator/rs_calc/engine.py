"""Population rewrites. Numeric operations here are bookkeeping, never operands."""

from collections import Counter
from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
import random


class ResourceLimit(RuntimeError):
    """The trial is censored, not a successful calculation."""


@dataclass(frozen=True)
class Config:
    regions: int = 8
    locality: str = "global"
    strength: float = 1.0
    fault_rate: float = 0.0
    max_steps: int = 100000
    max_relations: int = 20000
    scheduler: str = "random"

    def __post_init__(self):
        if self.regions < 2 or self.max_steps < 1 or self.max_relations < 1:
            raise ValueError("Invalid region count or resource limit")
        if not 0 <= self.strength <= 1 or not 0 <= self.fault_rate <= 1:
            raise ValueError("strength and fault_rate must lie in [0, 1]")
        if self.locality not in {"global", "local"}:
            raise ValueError("locality must be global or local")
        if self.scheduler not in {"random", "ordered"}:
            raise ValueError("Unknown scheduler")


@dataclass(frozen=True)
class Relation:
    uid: int
    positive: bool
    source: int
    target: int
    ready: bool = False


Population = list[Relation]


def snapshot(state: Population) -> list[dict]:
    return [asdict(edge) for edge in state]


def structural(state: Population) -> list[tuple]:
    """Ignores instance labels and list order; keeps fixed-region incidence."""
    return sorted((e.positive, e.source, e.target, e.ready) for e in state)


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class Engine:
    def __init__(self, seed: int, config: Config | None = None, trace: bool = False):
        self.seed = seed
        self.config = config or Config()
        self.rng = random.Random(seed)
        self.serial = 0
        self.steps = 0
        self.counts: Counter = Counter()
        self.events: list[dict] | None = [] if trace else None
        self._hash = sha256()
        self.intervention: dict | None = None
        self._intervened = False
        self.context: dict = {}

    @property
    def trajectory(self) -> str:
        return self._hash.hexdigest()

    def choose(self, sequence):
        return sequence[0] if self.config.scheduler == "ordered" else self.rng.choice(sequence)

    def relation(self, positive: bool, ready: bool = False, source: int | None = None,
                 target: int | None = None) -> Relation:
        self.serial += 1
        return Relation(self.serial, positive,
                        self.rng.randrange(self.config.regions) if source is None else source,
                        self.rng.randrange(self.config.regions) if target is None else target, ready)

    def event(self, kind: str, **payload):
        if self.steps >= self.config.max_steps:
            raise ResourceLimit("Transition budget exhausted")
        self.steps += 1
        self.counts[kind] += 1
        row = {"event": kind, **payload}
        self._hash.update(json.dumps(row, sort_keys=True, separators=(",", ":")).encode())
        if self.events is not None:
            self.events.append(row)

    def check_size(self, state):
        if len(state) > self.config.max_relations:
            raise ResourceLimit("Relational population budget exhausted")

    def fault(self, state: Population):
        if state and self.rng.random() < self.config.fault_rate:
            edge = self.choose(state)
            admitted = self.rng.random() >= self.config.strength
            self.event("fault_admitted" if admitted else "fault_rejected",
                       edge=(edge.positive, edge.source, edge.target))
            if admitted:
                state.remove(edge)

    def normalize(self, population: Population) -> Population:
        state = list(population)
        self.context = {"kind": "population", "population": state}
        self.check_size(state)
        self.event("initial", state=structural(state))
        while True:
            if self.intervention and not self._intervened and self.steps >= self.intervention["at"]:
                self._intervened = True
                state = self.perturb(state, self.intervention["mode"], self.intervention.get("pairs", 6))
                self.context["population"] = state
            pending = [e for e in state if not e.ready]
            positive = [e for e in state if e.positive]
            negative = [e for e in state if not e.positive]
            if not pending and not (positive and negative):
                self.event("normal_form", state=structural(state))
                return state
            self.fault(state)
            pending = [e for e in state if not e.ready]
            positive = [e for e in state if e.positive]
            negative = [e for e in state if not e.positive]
            sites = []
            if self.config.locality == "local":
                sites = sorted({e.target for e in positive} & {e.target for e in negative})
            choices = []
            if pending:
                choices.append("handoff")
            if positive and negative and (self.config.locality == "global" or sites):
                choices.append("cancel")
            if state:
                choices.append("rewire")
            if not choices:
                continue
            kind = self.choose(choices)
            if kind == "cancel":
                if self.config.locality == "local":
                    site = self.choose(sites)
                    positive = [e for e in positive if e.target == site]
                    negative = [e for e in negative if e.target == site]
                p, n = self.choose(positive), self.choose(negative)
                state.remove(p)
                state.remove(n)
                self.event("cancel", positive=(p.source, p.target), negative=(n.source, n.target))
            else:
                old = self.choose(pending if kind == "handoff" else state)
                target = self.rng.randrange(self.config.regions)
                if self.config.locality == "local":
                    target = (old.target + self.choose([-1, 1])) % self.config.regions
                new = self.relation(old.positive, kind == "handoff" or old.ready,
                                    source=old.target, target=target)
                state.remove(old)
                state.append(new)
                self.event(kind, polarity=old.positive, before=(old.source, old.target),
                           after=(new.source, new.target), ready=new.ready)

    def perturb(self, population: Population, mode: str, pairs: int = 6) -> Population:
        if pairs < 0:
            raise ValueError("pairs must be nonnegative")
        state = [self.relation(e.positive, e.ready) for e in population]
        if mode == "neutral":
            for _ in range(pairs):
                state.extend([self.relation(True), self.relation(False)])
        elif mode == "erase":
            if state:
                state.remove(self.choose(state))
        elif mode == "flip":
            if state:
                edge = self.choose(state)
                state.remove(edge)
                state.append(replace(edge, positive=not edge.positive, ready=False))
        elif mode != "rewire":
            raise ValueError("Unknown perturbation mode")
        self.check_size(state)
        self.event("perturb", mode=mode, state=structural(state))
        return state

    def invert(self, population: Population) -> Population:
        return [replace(e, positive=not e.positive, ready=False) for e in population]
