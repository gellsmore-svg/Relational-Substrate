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
