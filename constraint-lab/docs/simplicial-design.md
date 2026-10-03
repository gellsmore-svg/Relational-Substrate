# Simplicial semantics — design note, not a result

Generation 3 executed independent hypergraph semantics. This note does not choose a simplicial dynamics, and it does not report a simplicial run.

A 2-simplex on `A`, `B`, and `C` is not the bit used in Generation 3. In this laboratory a simplex carries its faces. The independent triad does not.

These are separate design questions. An implementation has to answer each one. Leaving one implicit would compile a simplex into the hypergraph bit, which Generation 3 refuses.

1. How is formation of the simplex represented? Is it one event, or a derived label on a state that already has the three faces?
2. Does forming the simplex create faces that were absent?
3. Is formation prohibited unless all three faces are already present?
4. Does deleting a face delete the simplex?
5. Is dissolution of the simplex an event of its own, or only a consequence of losing a face?

Each answer is a different kernel. For example, automatic face creation is not the same rule as prohibiting formation until the faces exist, and neither is the same as deleting the simplex when one face is deleted. Generation 3 does not pick among them.

A later simplicial cell should name the answers in its specification before any shard runs. The comparison with Generation 3, if it is made, should use the same `N`, the same weights, and the pairwise conditional jump kernel, so a change of support or of reducibility can be attributed to face-closure rather than to a larger grammar.
