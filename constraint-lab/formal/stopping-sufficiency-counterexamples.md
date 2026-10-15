# Exact Converse Boundaries

All examples are synthetic rational chains in stopping_sufficiency.py; their complete matrices, exact stationary priors, entrance rows, killed operators and coefficients are in generation-008p-proof-checks.json. They are not N4 scientific cells and need not satisfy CL's special pair-history shift.

| Tempting implication | Exact obstruction |
| --- | --- |
| Same stationary and adjacent coarse law implies same stopping law | aggregation_erases_target: Kpi=LTC has the matched stationary adjacent law, but the A0 post-first-step entrance gives eventual destination difference (2/45,-2/45) |
| Same eventual target vector implies every length matches | eventual_not_all_lengths: eventual vector difference is zero, while j=1 coefficient is (-5/1568,-5/1568) |
| A stationary lifted entrance gives no propagated defect | The same fixture has aP=a but U=(-4/49,4/49) |
| All return lengths match implies all projected paths match | all_lengths_not_all_paths: all lengths to singleton A match, yet stationary word (A,B,C) has difference 3/11680; B fine states have different coarse successor rows |
| A vector with zero component sum is zero | (2/45,-2/45) is nonzero but the ones readout erases it |
| Parity and lifted entrance force even timing equality | A five-state bipartite chain has aP=a, all odd returns impossible, but j=2 timing difference -3/200 |

For each fixture, the fine stationary law is solved by FLINT, checked by independent standard-library Fraction elimination, and substituted into pi T=pi. The stationary coarse adjacent flow is checked entry by entry. All-length claims use exact reachable closure plus an independent Cayley-Hamilton bounded power calculation. The path counterexample is computed from original fine-state word probabilities, not a quotient omitting the observation.

No conclusion follows about arbitrary finite horizons from observing a few leading zeros unless a recurrence/closure proof supplies it. No synthetic example invalidates CL's extra three-mask matching theorem: that theorem has the additional pair-history shift hypothesis, absent in these generic chains.
