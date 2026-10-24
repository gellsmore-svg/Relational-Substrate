# Atlas expansion after atlas-002

Status: active continuation of the same atlas. Not a new programme.

Opened from commit `a0f4160`. RRC-001, atlas-001, and atlas-002 stay frozen. Their plans are not edited. Their results are not recomputed.

The avenues below are simultaneous coverage directions. A result in one of them does not appoint the next round.

## Limitations already on the record

The opening grammar reads designated carrier bits. On the atlas-002 chain and branch, the same bit rule produced the same weight table. That is a property of that grammar. It is not a theorem that those carriers have the same dynamics under every rule. PAT-004 records that component count also failed to separate them, while the non-increasing degree sequence did not. ATLAS-Q07 stays open. It is not an order to add that observable, and it is not the reason a later grammar exists.

Weight-table sha256 is equality of the integer table in the declared edge order. It is not equality of discrete-time transition probabilities. A row can change by a positive scale and leave `w / row-sum` unchanged. The clock that divides by the row sum is `halt_self_loop`. A zero row is the self-loop. This is not a continuous-time rate.

Atlas-001 used at most three constraints, and factor 4 whenever it multiplied. Atlas-002 used at most one constraint, and factor 4. Those are the explored cells, not the grammar's limit. The composer already accepts any integer factor of at least 2, and lists longer than three.

Declared cardinality, effective cardinality, K, and J stay separate. An expansion of a compound predicate into conjunction features is a third count. It is not declared J.

## Avenues

Constraint diversity, incidence-aware predicates, compositional definitions, and cross-atlas comparison stay open together.

An incidence predicate is topology-sensitive only when its truth value can change with the current incidence neighbourhood. A static fact that two named edges share a vertex does not by itself do that. The bit grammar remains the baseline representation.

Composition stays in the idea library until one definition is precise enough to calculate. A weak cell is not used to mark that region explored.

## Equivalence types

New equivalence rows carry `equivalence_type`. Older rows do not. For those, `status: composer` is an identity of the opening composer, and `status: cell` is equality of weight tables in the declared order.

| Type | Assumption |
| --- | --- |
| `weight_table` | Same integer table, same carrier order. No relabelling is implied |
| `transition_kernel` | Same `P(e given x)` under `halt_self_loop`, including the zero-row self-loop. Not every clock |
| `relabelling` | A declared mapping of nodes or of edge order. Hash equality without that mapping is not this type |
| `composer` | An identity of the composition rule, checked without a scientific cell |

## Engine

`rrc-0.2.0` is the engine of atlas-001 and atlas-002. A change of mathematical semantics uses a later engine string. `verify` still compares a result with the engine string in its own plan. `run` refuses a plan whose string is not the live one.