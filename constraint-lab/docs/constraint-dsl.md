# Constraint DSL

Generation 1 uses one normal form.

```text
form(i-j) | present(a-b) & absent(c-d) => weak_suppress
dissolve(i-j) => prohibit
```

The action is exactly one of `form(edge)` or `dissolve(edge)`. Conditions are a conjunction of `present` and `absent` literals on other edges. The weight is a name from the declared alphabet.

## Normal form

Formation already requires the action edge to be absent. Dissolution already requires it to be present. A condition on the action edge is either contradictory or redundant, and the parser rejects it. Repeated conditions are rejected. Entity endpoints are written in increasing order; `form(1-0)` parses as `form(0-1)`.

`K = 1 + (number of conditions)`. `A` is the number of distinct endpoints named by the action and the conditions.

There is no second effect keyword. `=> strong_favour` means “multiply the matching toggle’s weight by the strong-favour factor”. `=> prohibit` means “multiply it by 0”.

## What a constraint can target in this generation

The action literal targets the formation weight or the dissolution weight of one pairwise relation. The conditions read the current incidence of other pairwise relations. That is a constraint on relation formation, relation dissolution, and, through the product along a path, on candidate transitions.

The following targets are visible in the conceptual list and are not expressible in the Generation 1 normal form. They are unsearched, not rejected as nonsense:

- a weight on relation persistence separate from the dissolution toggle;
- an irreducible higher-order relation;
- an entity channel, a relation channel, or a constraint channel (`S > 0`);
- a numeric threshold (`count_at_least` and its relatives);
- history (`H > 0`);
- a constraint whose action is another constraint (`L > 0`).

## Enumeration

The generator walks, in this order: action edge, polarity (`form` then `dissolve`), condition size, combinations of the other edges, binary assignments, weight name (`prohibit`, `strong_suppress`, `weak_suppress`, `weak_favour`, `strong_favour`).

A raw template, used only for the coverage identity, marks every edge including the action edge with `{absent, present, any}`. The accounting partition is:

```text
raw = syntax-invalid + redundant + outside K + structural normal forms
labelled constraints = structural normal forms × |weight alphabet|
```

The generator’s labelled list must equal that product. The identity is checked at the start of every cell and in the unit tests.

## Sets

A constraint set is an unordered set of distinct labelled constraints. Canonicalisation maps the set to the lexicographically least id tuple in its `S_N` orbit. Pairs and triples are combinations, not multisets. Repeating one constraint is an unsearched region: it would be a change of grade, not a new pattern.

## Serialisation

Expressions are the human-readable canonical form. Sets are stored as sorted expression lists. The set id is the first 16 hex digits of SHA-256 over the alphabet name, a newline, and the sorted expressions. The same expressions under a different alphabet are a different id, because the factors differ. The same grades under `W4`, `W3`, and `W16` share a modal map; they do not share numerical kernels.

## Extension

A later literal, such as a threshold or a hyperedge, should be a new production in this language, with its own `K` and `A` rules, and a coverage partition that still sums to the raw count. Silent overloading of `present` to mean “a count” would make the Generation 1 census unreadable.

## Structural identity (engine 0.2)

Generation 1 treated each weighted expression as its own constraint. Two copies of one rule with reciprocal grades, `form(0-1) => strong_favour` and `form(0-1) => strong_suppress`, were therefore a cardinality-2 set. Their factors multiply to 1, and the pair reproduces the baseline kernel. That is legitimate multiplicative composition. It is not two structurally different constraints.

The structural identity is polarity, action, edge conditions, and count literals. The weight is an attribute of that identity. In the primary mode, `structural-simple`, a set may contain at most one weighted instance of each structural identity. The reciprocal pair above is a stacked-weight composition. It remains available under the named mode `stacked-weight`. It does not count toward cardinality, minimal motif size, or the number of independent constraints in the primary census.

A missing `composition` field means `structural-simple`. Generation 1 specifications have no such field. Their committed manifests were produced before this filter and are not rewritten. A fresh run of those specifications under engine 0.2 applies the filter; the semantic version on the shard says so.

## Occupation count (engine 0.2)

```text
form(0-1) | count>=2 => strong_favour
dissolve(0-1) | count==1 => strong_suppress
```

`count` is the number of present pairwise edges in the whole state. It is not a rise in relation order and it is not a hyperedge. The three relations are `count>=q`, `count<=q`, and `count==q`. A normal form carries at most one of them. `K` gains one for that literal. `A` does not: the literal names no entity.

Some literals never change a match, given the action precondition, and are excluded from the grammar. Formation can fire only while its own edge is absent, so the count is at most `M - 1`. Dissolution can fire only while its own edge is present, so the count is at least 1. `count>=0` and `count<=M` are tautologies on every state. `count==q` is not the same object as the pair of inequalities: under multiplicative composition those two constraints would apply the weight twice.

Edge constraints are still generated first, in the Generation 1 order. Count constraints are appended. An edge-only grammar keeps the Generation 1 ids.

The edge-template partition now also removes templates outside `A_max`:

```text
raw = syntax-invalid + redundant + outside K + outside A + structural normal forms
```

Count literals have their own partition (`candidates = tautology + unsatisfiable + outside K + outside A + structural forms`). They are not folded into the edge identity `2 * M * 3^M`.
