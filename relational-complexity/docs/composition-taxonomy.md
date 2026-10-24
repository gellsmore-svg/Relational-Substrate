# Composition taxonomy

Status: idea library. No scientific cell is attached to this note. No engine change. No placeholder experiment. Existing idea rows keep the status they had before this note. Six levels of composition are not a target.

Later status: `IDEA-L08`, `IDEA-L14`, and `IDEA-L16` are partial because the operators are implemented. `IDEA-L13` is partial after atlas-008 calculated three baseline label maps. That round is not a cell of this note.

The formulations below are alternative mathematical objects. None is the definition of relational composition. A later round may freeze one named operator. It does not inherit the others.

## Four readings

These four readings can overlap. A record that uses one word for all four has not named an operator.

### Relational dependency

One relation conditions the possible changes of another. In the current engine this is the directed graph stored as `imposed_rule_dependency`. An arc runs from each condition source to the event. A designated-edge constraint contributes one arc. An incident-neighbour constraint contributes one arc from each incident carrier edge. The stored fields are `has_cycle` and, when at most 12 edges are involved, `longest_simple_path_edges`. The stored note says this is imposed rule text, not an observed dynamical cascade.

### Relational reach

A local change has consequences for relationships beyond the edges named by one constraint. Three readings are in use here. They are not equivalent.

- **R-a.** The integer weight of event `f` in state `S` depends on the presence bit of edge `e`. That is a dependency arc, or a formation or dissolution literal when `e` is `f`.
- **R-b.** Under `halt_self_loop`, a positive row normalises by its sum. Changing the integer weight of event `e` in state `S` changes the transition probability of every event that has positive weight in that row, including an event whose integer weight does not read `e`. This coupling is a property of this clock. It is the coupling named beside IDEA-C06. It is not a path along the carrier.
- **R-c.** A marginal, a hitting time, or the set of states reachable in `k` steps, for an edge at a declared distance on the carrier. This is not a stored core field. IDEA-L01 names the occupation version and remains open.

A dependency path of length `k` does not establish R-c. An R-b change can occur with no dependency arc into the affected event.

### Relational composition

A collection of relations is the input of a further relational description or operation. The output is a mathematical object: a projection, a graph on those relations, a cover, or a product. The dependency graph is one such object. It is bookkeeping on a specification. It is not, by itself, a dynamics at a further level.

### Relational recursion

The same composition operator applied to its own output. Recursion is defined only when that output is an object the operator accepts. A dependency cycle is a directed cycle in rule text. A period of the Markov chain is a dynamical fact. Neither is an iterated operator. RRC-001 constructed one designated two-subset cut. That cut is one projection, already reported. It is not an operator this note iterates.

## How to read a family

Each family records the same fields. "Undefined" means the field has no mathematical answer until an operator is named. It is not a provisional yes.

## C1 — Relational chains

- **Objects.** Carrier edges, and directed condition arcs between them. A chain carrier, IDEA-R02, is a different object: a path in the permitted edge list.
- **Operator.** The dependency digraph of the constraint list. A relational chain in this family is a directed path in that digraph.
- **New state.** No.
- **Further participation.** The digraph is not a carrier state. Feeding it back as a presence bit needs a map this note does not define.
- **Associativity.** Concatenation of directed paths is associative as a graph operation. That fact is not an associativity of the transition law.
- **Overlap.** Arcs may share vertices. The family is not a partition of the edge set.
- **Recoverability.** The arc list is determined by the constraint list. The constraint list is not determined by the arc list: factors, actions, and polarities are lost.
- **Grammar.** Unchanged. The chain is bookkeeping.
- **Established mathematics.** Directed paths in a finite digraph.
- **Small-scale calculation.** Already computed for specifications that involve at most 12 edges. Above that cap the path length is stored as not computed.
- **Open.** IDEA-L01 and IDEA-L09 stay open. No cell in this note asks whether occupation changes along a carrier path.
- **Library.** IDEA-L01, IDEA-L07, IDEA-L09, IDEA-R02.

## C2 — Branching relational dependencies

- **Objects.** One event with several condition sources, or one source named by several events.
- **Operator.** In-degree and out-degree in the dependency digraph. Branching of this digraph is not the branching of a carrier. A star carrier is IDEA-R03.
- **New state.** No.
- **Further participation.** Same limit as C1.
- **Associativity.** In-degree is not a binary operator on structures. Associativity is undefined.
- **Overlap.** One edge may be a source and a target.
- **Recoverability.** The degrees do not determine the constraint list.
- **Grammar.** Unchanged.
- **Established mathematics.** Degree sequences of a finite digraph.
- **Small-scale calculation.** The digraph is already available with the dependency fields. Degree sequences of that digraph are not a separate stored observable.
- **Open.** IDEA-L02 is `explored` because verified batches reported the syntax. That word is not a dynamical confirmation. This note does not add a cell.
- **Library.** IDEA-L02, IDEA-C05, IDEA-C06.

## C3 — Cyclic dependencies

- **Objects.** Directed cycles in the dependency digraph.
- **Operator.** The stored Boolean `has_cycle`. A cycle carrier is a different object. A periodic orbit of the chain is a third object.
- **New state.** No.
- **Further participation.** The Boolean does not name the cycles, so it cannot be the input of a further cycle operator.
- **Associativity.** Undefined. A Boolean is not a composition operator.
- **Overlap.** One vertex may lie on several cycles. The flag does not record them.
- **Recoverability.** The flag does not determine the constraint list, nor which cycles exist.
- **Grammar.** Unchanged.
- **Established mathematics.** Cycle detection in a finite digraph.
- **Small-scale calculation.** Already stored. PAT-006 records the flag together with one recurrent class and together with two. `schedules_follow_up` is false. This note does not reopen that pattern.
- **Open.** Which cycles exist, and whether a dependency cycle changes the chain, stay open. IDEA-L03 stays `explored` as syntax.
- **Library.** IDEA-L03, IDEA-R03.

## C4 — Relations as participants

Two operators. They do not share a state space.

### C4a — Functional further graph

- **Objects.** A graph whose vertices are the carrier edges.
- **Operator.** Two instances are named. The line graph joins two vertices when the carrier edges share an endpoint. The dependency digraph joins them by C1. Both are functions of the carrier listing and the rule text. Presence of a line-graph vertex, read as the carrier bit, is the existing state.
- **New state.** No.
- **Further participation.** The line-graph operator `L` is unary on simple graphs. `L` applied again is defined. On a path with `m` edges, `L` is a path with `m-1` edges, and the graph is empty of edges after finitely many applications. On a cycle of length at least 3, `L` is a cycle of the same length. These are textbook facts about simple graphs. They are not RRC theorems and not facts about the Markov chain. This note attaches no chain to `L`.
- **Associativity.** `L` is unary. Associativity is the wrong property. Iteration is defined for this static operator only.
- **Overlap.** Line-graph adjacency is shared endpoints. It is not a partition of the carrier.
- **Recoverability.** The carrier edge set determines the line graph. The line graph does not determine the carrier: a triangle and a three-edge star have the same line graph. EQ-014 uses that identity for one prohibit. That identity names deadlock states of the pair chain. It is not a dynamics whose events are the edges of the line graph.
- **Grammar.** Unchanged on the pair chain. A dynamics that toggles edges of the line graph is not this operator and is not defined.
- **Established mathematics.** Line graphs; total domination enters only through EQ-014, which stays scoped to one prohibit.
- **Small-scale calculation.** The static graph is readable from the edge list. No cell is run. The domination enumerator is not rerun.
- **Open.** IDEA-L16. ATLAS-Q10 stays open.
- **Library.** IDEA-L05 is pair-to-pair conditionality, which is dependency. IDEA-L16 is this split. IDEA-G01 is the scoped deadlock identity and is not a composition result.

### C4b — Independent further bit

- **Objects.** A relation between relations with a presence bit that is not a function of the carrier bits.
- **Operator.** Not defined. A toggle of that bit would be a new event.
- **New state.** Yes, if the bit is added. It is not added.
- **Further participation.** Undefined until the bit exists.
- **Associativity.** Undefined.
- **Overlap.** Undefined.
- **Recoverability.** An independent bit is not recoverable from the pair state. That is the reason it is new state.
- **Grammar.** Outside the current pair grammar. The compilation gate requires a witness before an engine change: two situations with the same pair bits and different next rows, or an event that is not a pair toggle. No witness is claimed.
- **Established mathematics.** None is invoked, because the operator is not defined.
- **Small-scale calculation.** Not available in this engine.
- **Open.** IDEA-L16 and ATLAS-Q06. COV-HYPEREDGE stays open and is the independent-relation region, which is not this note's experiment.
- **Library.** IDEA-L16, IDEA-C09 for history, which is a different extra coordinate.

An incidence graph of the carrier, with nodes on one side and carrier edges on the other, is a function of the listing plus the current subset. It adds no bit. A factor graph with constraint vertices is static bookkeeping. Forgetting the constraint vertices and keeping arcs from conditions to events recovers the dependency digraph and loses factors, actions, and polarities. Neither graph is given a dynamics here.

## C5 — Structures interacting with structures

- **Objects.** Two designated collections of relations.
- **Operator.** Three readings are already typed, and none of them creates an entity from a name. A disjoint union of edge lists is one carrier whose state is the product of the bitsets (IDEA-R04). A constraint on an edge in one collection whose condition is an edge in the other is ordinary dependency across a cut. A projection onto a declared visible set is a Markov chain only when strong lumpability holds. A fourth reading, a map that sends the law of each collection to a law of a new entity, is not named.
- **New state.** The product and the cut stay inside pair state. A fresh bit that means "the collection" would be new state. It is not introduced. Naming a collection does not make it an entity.
- **Further participation.** A projection can be the input of another projection only when the first projection is Markov and the second partition is declared. That second partition is not declared. The unnamed entity map has no output to pass on.
- **Associativity.** Undefined for the unnamed map. Function composition of declared projections is associative when each projection is a function on a declared state. This note does not exhibit such a pair of projections.
- **Overlap.** Collections that share edges are not a Cartesian product. That case is C6. The product reading assumes disjoint edge lists.
- **Recoverability.** The full product state determines each component. A projection need not determine the full state.
- **Grammar.** Preserved on the full pair state. On a projection, the compilation gate already records the alternatives: the same event shape with possibly different weights, or no closed interface grammar.
- **Established mathematics.** Disjoint union of graphs; strong lumpability of Markov chains.
- **Small-scale calculation.** A small product can be compiled as an ordinary listed carrier. That compilation does not test the unnamed entity map, so it is not run here. RRC-001's two-subset cut is not reopened.
- **Open.** IDEA-L04, IDEA-L17, ATLAS-Q10, RRC-Q09. IDEA-L13 is partial and is not this family's cell.
- **Library.** IDEA-L04, IDEA-L17, IDEA-R04.

## C6 — Overlapping structural composition

- **Objects.** A family of named subcollections of the carrier. A full cover is a family whose union is the carrier. A partial family misses at least one carrier edge. A partition, an overlapping cover, and a nested family are further distinctions. Intersections may be non-empty. The family need not be nested and need not be a partition.
- **Operator.** Not defined. The cover is an instrument written beside the carrier. There is no function from the cover to a new chain.
- **New state.** No, while the cover is only a labelling of existing edges. A presence bit per block would be C4b and is not opened.
- **Further participation.** Undefined. Encoding each block as a fresh node so that a tree algorithm can store the cover would replace the cover with a different object. IDEA-L14 records that refusal.
- **Associativity.** Undefined.
- **Overlap.** Yes, by the definition of this family. A partition is the special case of empty intersections. The family is not restricted to that case.
- **Recoverability.** The edge set does not determine which cover was written.
- **Grammar.** Unchanged, because no operator acts on the chain.
- **Established mathematics.** Set covers. The cover is not COV-HYPEREDGE: that row is an independent relation of order 3 as state.
- **Small-scale calculation.** The underlying chain is the ordinary carrier. Atlas-011 later stored observations of fixed families outside this note. This note still has no cell. An omission list in that round is a partial family. The stored plans were not rewritten.
- **Open.** IDEA-L08 and IDEA-L14 are partial. The implemented cover operators are not cells of this note.
- **Library.** IDEA-L08, IDEA-L14.

## C7 — Repeated composition

- **Objects.** An operator whose output is an input of the same operator.
- **Operator.** Not one operator. The typed cases diverge. Static `L` from C4a can be iterated, and its output is a simple graph, not a constraint specification and not a Markov chain. The dependency construction `D` outputs a digraph. `D` applied to that digraph is untyped, because a digraph is not a constraint list. A projection outputs a chain only when it is Markov, and a second partition is not declared. The entity map of C5 is unnamed, so it cannot be applied twice.
- **New state.** No new state is added by recording this gap.
- **Further participation.** This is the field that fails for `D` and for the unnamed map. It holds for static `L` only as a graph operation.
- **Associativity.** Undefined whenever the operator is not a binary operation on one set. Unary iteration is a different property and is stated only for static `L`.
- **Overlap.** Not a property of an unnamed operator.
- **Recoverability.** Undefined until the operator is named. Static `L` need not be invertible, as C4a records for the triangle and the three-edge star.
- **Grammar.** IDEA-L13 lists one-step possibilities: the transition law might be preserved, the weights might change shape, or a closed description might fail. Those are alternatives, not predictions. None is known for a second application.
- **Established mathematics.** Iteration of the line-graph operator, as cited under C4a. No dynamical theorem is claimed.
- **Small-scale calculation.** Iterating `L` on a named small graph is a graph-theory exercise. It is not run as an RRC cell. A token chain with a label "level 2" would not make `D` typed.
- **Open.** IDEA-L06 stays open. IDEA-L13 is partial: a second application of a label map is still undefined. ATLAS-Q12 asks which named operators accept their own output. It is not scheduled. Six levels of composition are not a target.
- **Library.** IDEA-L06, IDEA-L13, IDEA-L15.

## C8 — Alternative effective descriptions

One chain, and a declared set of observables. The six descriptions below stay separate.

1. **Full internal state.** The carrier bitset. Exact. This is the current model. Calculable at the sizes the engine already compiles.
2. **External interface.** A declared set of visible bits or cut edges. Exact when strongly lumpable. Otherwise the interface process is not Markov. RRC-001 reported this for other rules. The atlas grammar is not given a new interface cell here.
3. **Reduced sufficient state.** A statistic, coarser than the bitset, that still determines the next law of the chosen observables. Sufficiency is exact. It is a different claim from lumpability of a named partition, and lumpability is one case of it. No search is run.
4. **Approximate representation.** A declared partition and a declared defect. IDEA-L11. No defect is computed in this note. An approximate lumping is not reported as an exact interface.
5. **Historical information.** A coordinate that is not a function of the current bitset. IDEA-C09. Formation and dissolution are not this case: they read the current event bit. The gate still requires a witness.
6. **Another named observable.** Degree sequence, component sizes, and edge count are functions of the current state. The structure hash already stores some of them. A function of a Markov chain need not be a Markov chain. ATLAS-Q07 asks whether a later core should carry a degree sequence and does not schedule that core. This note does not answer it.

- **Objects.** The chain, and one of the six descriptions.
- **Operator.** The description map. Only (1) is the identity. (2), (3), (4), and (6) are functions or attempted quotients. (5) is an extension.
- **New state.** Only (5) would add state. It is not added.
- **Further participation.** (1) can be the input of another description. (2) can, when it is Markov. (4) does not yield a law. (5) would be a larger state if it existed.
- **Associativity.** Composition of functions on one state is associative. That is ordinary mathematics of the maps, and only where each map is defined. It is not a dynamical result. This note does not compose two non-trivial descriptions.
- **Overlap.** Two observable sets may share coordinates. Sharing is not a tree.
- **Recoverability.** (1) recovers itself. (2), (3), (4), and (6) need not. (5) is not a function of (1), so (1) does not recover it either.
- **Grammar.** (1) is the grammar. (2) may transform weights or lose the Markov property. (3) preserves the law of the chosen observables when the statistic is sufficient. (4) does not claim preservation. (5) is outside the grammar. (6) is not a grammar.
- **Established mathematics.** Strong lumpability; sufficient statistics; functions of a Markov chain.
- **Small-scale calculation.** (1) is the existing cell machinery. The others wait for a declaration. No cell.
- **Open.** ATLAS-Q07, ATLAS-Q10, IDEA-L11, IDEA-C09. IDEA-L13 is partial. Atlas-008 calculated three of the named observables on the baseline and did not close the question.
- **Library.** IDEA-L11, IDEA-L13, IDEA-C09, IDEA-O01.

## What remains untyped

| Family | Operator status | Cell |
| --- | --- | --- |
| C1 | Dependency digraph, already stored | None in this note |
| C2 | Degrees of that digraph; degrees themselves are not a stored observable | None |
| C3 | Stored Boolean | None; earlier syntax is not reopened |
| C4a | Static line graph and dependency digraph | None; EQ-014 is not rerun |
| C4b | Independent bit | None; not in the engine |
| C5 | Product, cut, and projection are typed; an entity map is not | None; RRC-001 is not reopened |
| C6 | Cover as instrument only | None |
| C7 | Iteration typed only for static `L` | None |
| C8 | Full state is the current model; the other five descriptions are not frozen | None |

## Implemented operators

The sentences above that leave an operator undefined describe this library at the time it was written. Two operators now have code. The note still has no scientific cell.

`line_graph` is the static operator in C4a. `intersection_graph` and `nerve` accept an ordered family of blocks for C6. A second application is defined for the bare line graph and undefined for both of those operators. `line_graph` may be applied to a bare intersection graph. That composition is not recursion of the family operator. The specifications, the triangle and star exception, the shared nerves, and the baseline observation defects are in `docs/composition-operators.md`.

The present line graph, the present edge count, and the present degree sequence are label maps of an existing chain. They add no state. A label map is a Markov chain only when it is strongly lumpable. On the unconstrained baseline the edge count is lumpable. The present line graph is lumpable on some of the fixture carriers and not on others. Those checks do not freeze a cell. C4b remains undefined. No witness for an independent bit is claimed.

`COV-COMPOSITION` and `COV-COMPOSITION-LIBRARY` stay `open`. A written formulation is not a calculated region. ATLAS-Q01 through ATLAS-Q11 stay open. ATLAS-Q12 is the iterability question and is not a queue. ATLAS-Q13, ATLAS-Q14, and ATLAS-Q15 ask about an intermediate quotient, realised overlap, and a higher-order coordinate. They are open and they are not a queue.
