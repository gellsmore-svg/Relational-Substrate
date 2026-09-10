"""Bidirectional neutral-defect dynamics, not a claim of microscopic detailed balance."""

from dataclasses import dataclass

from .proposal_kernel import Bond, Constraints, Proposal, transition as fixed_transition


_CONSERVING = Constraints(conservation=1, no_growth=False, readiness=False)


@dataclass(frozen=True)
class RecurrentRule:
    birth_admission: float

    def __post_init__(self):
        if not 0 <= self.birth_admission <= 1:
            raise ValueError("birth_admission must lie in [0, 1]")


def transition(state: tuple[Bond, ...], p: Proposal, rule: RecurrentRule,
               capacity: int) -> tuple[tuple[Bond, ...], str]:
    if capacity < 1 or len(state) > capacity:
        raise ValueError("Invalid population capacity")
    # This bias is independent of state, operands, number class and expected answer.
    if p.kind == "pair_birth" and p.enforcement >= rule.birth_admission:
        return state, "birth_bias"
    return fixed_transition(state, p, _CONSERVING, capacity)
