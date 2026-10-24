# Opening atlas grammar

Status: definition, before any atlas cell runs. The frozen cells, once they exist, are a plan file. This note is the language those cells use.

Grammar id: `opening-prohibit-multiply-v1`. Engine string for new plans: `rrc-0.2.0`. RRC-001 stays `rrc-0.1.0` and is not recomputed.

## State and carrier

N labelled nodes. No geometry.

A carrier is the list of undirected pairs that may be events. `kind: complete` uses the Constraint Laboratory order, pairs `i < j` lexicographically. `kind: listed` uses the declared order as the bit order. The state is an integer in `0 .. 2^|carrier| - 1`. Bit `e` is 1 when carrier edge `e` is present.

A listed chain on five nodes is four bits, not the ten-bit complete graph, and not that complete graph with six weights held at zero. Those are different chains. The carrier's component count, isolated nodes included, is stored as an instrument.

## Clock

One step selects one carrier pair with probability proportional to its current integer weight and toggles it. A row of zeros is completed by a self-loop. The name of that convention is `halt_self_loop`. The self-loop is not a relational event.

## Constraints

Each constraint has:

- `effect`: `prohibit` or `multiply`
- `event`: a carrier pair
- `action`: `either`, `form`, or `dissolve`
- `when.edge`: a different carrier pair
- `when.polarity`: `present` or `absent`
- `factor`: an integer at least 2, and only on `multiply`

`form` matches only when the event is absent. `dissolve` matches only when it is present. `either` does not read the event bit. The condition is one literal. `form` or `dissolve` adds the event bit as a second literal.

There is no separate disfavour effect. Multiplying on the opposite polarity is the disfavour. There is no integer divisor, no overwrite, and no order-dependent composer.

## Composer

Baseline is a positive integer, 1 unless a cell says otherwise.

For each state and each event: if any matching prohibit applies, the weight is 0. Otherwise the weight is the baseline times the product of the matching multiply factors. A multiply of zero stays zero. List order does not change the table.

Because factors are integers of at least 2, no second multiply is the inverse of the first. Reinforcement moves the weight to `baseline * 4 * 4 = 16` when both factors are 4. It does not return the cell to the baseline.

Two prohibits of opposite polarity on the same event set that column to 0 in every state. That deletes support. It is not a cancellation back to the baseline.

## Cardinality and K, J

These are separate.

| Field | Meaning |
| --- | --- |
| `declared_cardinality` | Length of the constraint list, duplicates included |
| `j_positive` | Number of multiply features |
| `j_prohibit` | Number of prohibit features |
| `max_positive_k` | Over multiply features, `1 + literals` of that feature. 0 when there is no multiply |
| `max_prohibit_literals` | Most literals on one prohibit. 0 when there is no prohibit |
| `effective_cardinality` | Size of a smallest sublist with the same weight table |
| `removal_sensitive_count` | How many list entries change the table when that one entry is removed |

K is not the sum of literals across features. Two one-literal multiplies have `J = 2` and `max_positive_k = 2`. One form-and-condition multiply has one feature, two literals, and `max_positive_k = 3`.

A duplicate prohibit has declared cardinality 2, effective cardinality 1, and removal-sensitive count 0: each copy is redundant while the other remains, and one copy already reproduces the table.

Above 16 declared constraints the exact subset search is not run. The fields are then null and the method is `not_computed_above_16`.

`max_active_in_state` counts constraints whose guard matches, whether or not a later prohibit makes the multiply invisible in the number. `states_with_zero_active` is the complementary count.

## Compilation

The output is a current-state weight on a single toggle. Where every weight stays positive, that table is inside CL-T12 by growing J and K. A zero is the existing prohibit, not a new axis. The grammar does not add history, an independent hyperedge, or a multi-pair event. A count predicate is not one literal and is not in this grammar.

## Occupation

Report a stationary law only when there is one recurrent class.

If every column ignores the bit it toggles, and every row sum is positive, then `pi(G)` is proportional to the row sum `W(G)`. That identity is exact integer arithmetic. The balance `pi(G) * w(e,G) / W(G) = pi(G xor e) * w(e, G xor e) / W(G xor e)` reduces to `pi / W` constant when `w(e, G) = w(e, G xor e)`.

Otherwise use `stationary_balanced` from the uniform start and from the empty start, and a dense `pi P = pi` solve when the state count is at most 1,024. If those disagree past the item's tolerances, the occupation is `unresolved`. The support counts remain exact. An unresolved occupation is not filled in.

Several recurrent classes, including the all-halt chain where each state is its own class, are `not_unique`. No mean is attached to that result.

Means, when the law is unique: expected number of present carrier edges, expected number of components of the present graph (isolated nodes included), and the presence probability of each carrier edge.

## Instruments, named as such

- The carrier, its order, and its component count.
- Node labels.
- `imposed_rule_dependency`: the directed graph from each condition edge to its event edge. `has_cycle` and `longest_simple_path_edges` describe the rule text. They are not a cascade in the transition graph and not a period of the chain. The period-2 parity of a positive single-toggle chain is a clock fact.

## Common core of an `atlas_core` item

Carrier, clock, composer, compilation note, bookkeeping fields above, weight-table sha256, positive cells, zero cells, deadlocks, recurrent classes, the imposed rule-dependency record, and the occupation block under the rule above.

Equality of the sha256 is equality of the integer table in carrier order. Equality of one observable is not equality of the tables.
