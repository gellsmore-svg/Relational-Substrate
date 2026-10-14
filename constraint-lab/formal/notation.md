# Notation and audit

## Audit decision

The audit covered `books/*.md`, `constraint-lab/docs/*.md` and the laboratory Python source before adopting new symbols. The search for standalone J, mathematical J variants and rule-cardinality terminology found a personal initial (J. Richard Middleton), not an established mathematical J. Existing formal documents use C for constraints and alignment, R/T for receive/transmit and trajectory descriptors, S for both a programme axis and historically state, and L for meta depth. We do not silently rename those historical documents.

**J denotes rule cardinality**, the number of simultaneously present rule occurrences. In the structurally simple normal form, occurrences have distinct structural identities, so J is also the number of rules in the set. Backend multiplicity is different from set deduplication.

The machine-readable [audit record](notation-audit.json) specifies search scope and decisions. The book's T1-T4 axiom IDs motivate CL-T01 etc., not a second unqualified T1 catalogue.

## Primitive descriptors

| Symbol | Meaning | Scope qualification |
| --- | --- | --- |
| N | Entity count | Finite labelled entities |
| A | Constraint entity arity | Union of entities named by action and relation literals; count predicates do not name entities in the implementation |
| O | Maximum relation cardinality/order | O=2 pair graph, O=3 independent pair/triad bits; not K |
| G | Geometry descriptor | G=0 throughout the integrated experiments |
| S | Additional internal/state channels | S=0; ordinary relation-incidence bits still exist |
| H | History depth | H=0 implemented; past dependence is not inferred from hidden current bits |
| K | Per-rule expression complexity | One action plus literal/count tokens; literal fragment: 1 + number of conditions |
| L | Meta-constraint depth | L=0 implemented; not another Boolean product |
| J | Number of simultaneous rule occurrences | Independent of maximum per-rule K |
| W | Multiplier alphabet descriptor | W4 soft grades 1/4, 1/2, 2, 4; neutral 1 and zero prohibit have separate roles |

The axes describe a representation. They are not all implemented at nonzero values. The experiment runner additionally bounds J to 1, 2 or 3 and named alphabets to W4/W3/W16. The parser/backend is a larger representation core.

## Working symbols

Use x for the full current bit state, e for an event slot, e_* for a distinguished action, b for its bit, y for hidden relation bits and z for other pair bits. Use D for total relation-slot count and p for pair-slot count. Use an ordered collection/multiset \(\mathcal C\) for backend rules, w for weights, \(\ell_e=\log w_e\) for event log weights, q for event probabilities and P for the full-event kernel. E denotes the next-pair-event epoch kernel. Model label M is used only in information comparisons.

A historical 'action logit' is a log multiplier relative to unit alternatives, not log odds of a binary Bernoulli outcome. A state-dependent common shift of every event log weight leaves q unchanged; one-action interaction comparisons fix the alternatives and therefore fix this gauge.

## Derived law descriptors

- **effective_gate_dimension:** number of essential gate coordinates of the declared local law; guards and fixed/admissible context must be stated.
- **gate_interaction_order:** largest nonzero multilinear degree in a specified event log-weight function over raw Boolean gates, after fixing gauge and admissibility.
- **distinct_local_law_rows:** number of distinct normalised local probability vectors over the stated coordinate domain.
- **minimal_coordinate_count:** number of essential current-state bit coordinates required for the stated law, including the action-bit guard when it affects applicability.

These are properties of a law, not primitive ontology axes. Coordinate encodings and observable projection must be declared; a hidden composite encoding does not erase essential raw-bit dependence.

K, J, O, effective gate dimension and interaction order cannot be substituted for one another. Even K-1 bounds interaction order only in the pure literal-conjunction fragment, not for arbitrary count predicates.

## Generation 8H notation extension

The primitive table above records 8G's implemented scope. Generation 8H executes
one H example: H_pair=1 remembers one prior pair event, with alphabet
{None,0,1,2,3,4,5}. None is the initial sentinel, not a seventh pair slot.
Temporal depth one and alphabet size six are different descriptors.

Use h for the register and z_H=(x,h) for augmented state, preserving the earlier
meaning of z for other pair coordinates. In the history document, p denotes a
pair mask; the number of pair slots is explicitly six. Pair event e sets h'=e;
triad events preserve h. H's general meaning remains dependence on prior process
information not determined by ordinary current x. K describes simultaneous
current-state expression complexity, J the feature count, and L dynamical
constraint structure. S=L=0 remain in H0; compiling h to a future S variable
would be a declared representation change.

## Generation 8K synthesis notation

The historical tables above remain unchanged. The synthesis audits collisions
explicitly in [state-taxonomy.md](state-taxonomy.md): T is the kernel;
Pi_Y and widehat-Pi_Y are the observation partition and its coarsest strong
refinement; B_t is its current block. X,H,Z,Y retain distinct declared roles.
Candidate constraint state is eta. A compilation class is mathfrak-A, not C
(already used for graph classes/constraints). Ent_mu(B), if needed, distinguishes
entropy from history H. No existing axis or older notation is silently renamed.
