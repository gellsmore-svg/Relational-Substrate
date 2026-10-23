# What RRC-001 found

This is the plain-language account of the first completed round. The mathematical reading, with fractions and proofs, is `rrc-001-interpretation.md`. The cell-by-cell table is `rrc-001-atlas.md`.

## The question

The programme asks whether a complicated relational structure can be replaced by a smaller description and still behave the same way toward the outside, and whether those smaller pieces can be used again as pieces of a larger structure.

The first round looked at small complete sets of labelled points, from three points up to six. A state is a set of pairwise relations: each possible pair is either on or off. At each step, one pair flips. The chance of a flip depends on the current pattern of relations. Three rules were compared.

- Every pair is equally likely to flip.
- A pair with no common neighbour is forbidden from turning on. Turning off stays allowed. This is the hard wedge rule.
- A pair with a common neighbour is four times more likely to flip than a pair without one. This is the soft wedge rule.

"Outside" means the pairs that touch a designated group of points. The pairs inside that group are hidden. The test of a smaller description is strict: from the outside, the next step must look exactly the same no matter which hidden pattern is behind it. A merely similar average does not count.

Six points were one of the sizes in the comparison. They were not the size the round was trying to confirm.

## What came out

Equal flip chances do have an exact outside description. Hiding the inside does not change the next outside step. The outside process is the same kind of process as the whole: one pair flips, and the visible pairs share one common chance of holding still. This remains true when the hidden part is one triangle, and when it is two triangles at once.

Both wedge rules fail that test at every size in the round, starting at three points. Three is the smallest size at which a wedge can use a hidden pair. Two different hidden patterns can show the same outside pattern and still disagree about what the outside does next.

Keeping a simple summary of the hidden part rarely repairs the failure. The number of hidden pairs, and the parity of that number, repair it only when there is exactly one hidden pair, because then the summary is the hidden pair itself. A profile of wedge counts makes things worse in a way the round did not expect: it can take an outside description that was exact and make it inexact. That happened for the equal-chance rule at every size.

For the soft wedge, the exact repair is the whole pattern. No two patterns with the same outside view are interchangeable. For the hard wedge, a handful of patterns remain interchangeable, but the handful is small beside the full set (one pattern out of eight at the smallest cell, and a few dozen out of 32,768 at six points). The hard wedge also has a simple long-run fate: every present pair can disappear, and the empty pattern can create nothing, so the empty pattern is the only pattern that lasts. The round's class counts agree with that consequence of the rule. The hard wedge does not stabilise a nonempty structure.

## How a local change travels

Raising the flip weights on the pairs that touch one chosen point does not send a fading effect along a path of points.

For equal underlying chances, the long-run chance that a pair is present stays one half everywhere. What changes is how often each pair flips. Pairs that touch the chosen point speed up. Every other pair slows down by the same amount. Pairs far from the chosen point along the labelling do not slow down any further.

The soft wedge has the same flip rates, exactly, not merely approximately. A short argument explains why. The long-run chance of being in a pattern is proportional to the total flip weight of that pattern, and a constant boost then factors out of the averages. The calculation agrees with the stored numerical solutions to about a trillionth.

Presence does change under the soft wedge. The boost moves presence between the pairs that touch the chosen point and all the other pairs. It does not create a further step-by-step gradient. At three points the touched pairs become less present. At five and six points they become more present. At four points the presence of every pair stays exactly where it was. That four-point cancellation is exact for the weights used in the round. It is a property of four points under this rule, and it is one of the surprises.

## Six points

Six points behave like their neighbours. The hard-wedge defect for a hidden triangle is the same fraction, 51/40, at four, five and six points. The soft-wedge defect for a hidden triangle is the same fraction, 486/935, at five and six points. Nothing in the exact results singles six out.

The two-triangle arrangement at six points, the round's one attempt at composition, follows the same split: equal chances stay exact, and both wedge rules fail. The fractions differ from the single-triangle fractions. One constructed level of composition was tested. Six levels of composition were not.

## What the round does not say

These are facts about this small family of pair-flip rules and about groups of points chosen in the plan. They are not a claim about physical space, about a universal bound of six, or about an ontology. The round did not sample, did not look at seven or more points, and did not study memory of the past.

## What a later inquiry would be for

The comparisons the round was built to make are already separated at five points, and six points repeat them. A larger enumeration is not the next informative step. Two mathematical leftovers are recorded: why some defect fractions repeat from one size to the next, and why the four-point presence cancellation happens. A future computational round would need a new question and a new instrument. That proposal is written down and is not yet a frozen plan.
