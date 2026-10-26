# A changing shared interface: what must agree and what can be forgotten?

## Actual execution and answer

The recovery audit found no unpublished adaptive-interface work in the inspected
repositories. This is **newly initiated analytical work**, recovery path C, not
recovered old computation and not a result inferred from the earlier prompt merge.
Starting local HEAD was `fda7db4`; after fetching, live research HEAD was
`253e0c4a5ef3937aaec77afdc7a0e68c1d6ea3c8`. Main was still fda7db4.
The audit is `../provenance/2026-10-26-adaptive-local-audit.md`.

Selection `9a7cd24849c3cab24ecfd13b6e2db21781f0f517` was committed and pushed before
the new validation domain ran. See `../docs/2026-10-26-shared-port-selection.md`
for the qualitative comparison with membership controllers, restricted-context
work and deferred recovery. The chosen question asks how an identified port can
change, support further composition, and correspond—or fail to correspond—to
Cartesian copies. This addresses the original adaptive-interface brief directly.

The result is a typed, reapplicable **shared-port product**, together with its
exact agreement-invariance criterion and a separate boundary-abstraction limit.
The full definitions and proofs are `../docs/shared-changing-port.md`.

## Formal result and limitations

Inputs have finite nonempty states, an onto map to one finite nonempty port
set P, fixed finite H and nonnegative integer labelled weights. Positive private
events preserve the port. Shared events may change it; two matching shared
events survive only if their target ports agree. Compatible states store one
identified port value, read from both constituents, with no extra independent
coordinate. Intermediate outputs remain raw weighted components; only final
admitted rows normalise. An empty row halts without manufacturing an event.

The output inherits the same boundary and private-write contract. Raw labelled
composition is associative under canonical reassociation. Its unit has one
state per port value and a unit shared transition between every pair of ports
for each h. It relays a shared write; it is not a one-state halt system. Private
port-changing writes are outside this contract, and a singleton port recovers
the previous Cartesian product. These laws are proved for the whole declared
finite domain, not inferred from enumerated fixtures.

The agreement image in the unfiltered Cartesian product is invariant **iff**
every positive pair of matching shared events, from compatible sources, has
compatible target ports. When this holds, identified dynamics are conjugate to
the copy system restricted to that invariant image. Otherwise filtering changes
the admitted catalogue. With positive admitted mass its normalized row is the
one-step Cartesian law conditioned on agreement; if all positive events are
rejected, conditioning is undefined and the new operator halts by convention.
This is an injective image comparison, not a quotient/lumpability theorem.

Equal component port marginals are insufficient. Two components with h weights
1 and 2 into the two port values each have marginal `[1/3,2/3]). Their copy
product leaks `4/9`; identification retains weights 1 and 4, giving
`[1/5,4/5]`. A separately declared rejected-attempts-as-holds policy instead
gives `[5/9,4/9]` and `[1/9,8/9]`. The difference is explicitly instrument
and clock dependent, not evidence of an ontological mechanism.

## Dynamic, null and representation controls

Components `(x,p)` and `(p,y)` share p. Shared h flips p; private events flip x
with weight `1+p` and y with weight one. The eight identified states are
ordinary `(x,p,y)` state. The dynamics are exactly three current-state bit flips:
x weight `1+p`, p and y weight one. This specific model compiles to the existing
single-toggle grammar with one conditional factor-2 multiply; arbitrary
shared-port systems are not claimed to have that encoding.
The independent choice of p relative to x and y was specified in the two input
state spaces. Identification removes its duplicated storage; it does not
generate a new degree of freedom from a grouping.

Dropping p gives differing rows at x=y=0:
`[1/3,1/3,1/3,0]` versus `[1/4,1/4,1/2,0]`. A changing shared interface can
therefore be consequential for the selected prediction while remaining ordinary
finite state. As a null, set x's weight to one at both p values: p still changes,
but the observation `(x,y)` becomes exactly Markov.

Even that closed null observation has **no inherited port map** to the original
P. For any surjective observation pi, such a map exists iff the original boundary
is constant within pi blocks. This elementary factorization is necessary for
the same typed boundary, and does not by itself ensure predictive closure.
Thus a closed prediction need not be a substitute in a later port-identified
composition. The earlier all-partner Cartesian theorem is not silently extended
to this different context class.

The port value changes, but P, H and event ownership do not. No evolving
membership, independent controller, causal intervention, autonomous entity,
physical timescale or RS ontology is established. Standard fibre products,
weighted automata, support invariance, conditioning and map factorization supply
the mathematics; the RRC contribution is the explicit dynamical contract and
the distinctions it exposes. Related open-Markov-process literature is cited
with its different continuous-time/boundary-state scope in the methods note.

## Independent exact verification

Method `shared-port-analysis-0.1.0` imports no production RRC calculations.
Sparse event pairing is compared with independent dense Cartesian label matrices
restricted through an explicit image. Exact Fraction rows independently check
the support criterion; a separate bit-table construction checks the reduction.
Tests also use hand fractions and the previous sparse Cartesian implementation.

| Predeclared software domain | Verified count |
| --- | --- |
| Empty plus single shared transitions/private self-loops, two port values | Seven basis components |
| All ordered basis pairs | 49 sparse/dense/image checks |
| All ordered basis triples | 343 raw-weight associativity checks |
| Both unit sides per basis component | Seven two-sided controls |
| Hold/flip/reset internal lifts against every basis partner | 147 further pair/image checks |
| Additional controls | Three-port and internal-state iteration, duplicates, zero/non-unit weights, multiple labels, malformed boundaries, private-write rejection, feedback/null, invariance/leakage and undefined conditioning |

These validate software and proofs; they are not a scientific sample or newly
frozen atlas cells. All **247 local RRC tests pass**, including 24 added tests;
the starting suite had 223. The saved deterministic evidence is
`../provenance/2026-10-26-shared-port-verification.json`, SHA-256
`3838d8f939662327b4c816ccb2b6d7009c38b3eb6c9b867e23152f46dc367974`.
From `relational-complexity/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 provenance/shared-port-analysis-check.py
PYTHONDONTWRITEBYTECODE=1 /home/cello/domains/Relational-Substrate/constraint-lab/.venv/bin/python -m pytest -q
```

The existing environment is reused without modification. Checker resource caps
are implementation limits, not theorem bounds. Existing engine and analysis
method IDs retain their meanings. There are **zero scientific worker invocations**
and **zero newly adopted atlas cells**.

The final audit reproduces the evidence byte-for-byte. All six living registers,
PROGRESS.md and the crosswalk retain their starting bytes as exact prefixes;
IDs are unique, relationship endpoints and evidence/commit references resolve.
The complete suite includes the historical ledger and frozen-plan tests. Frozen
plans, preflights, results, old methods, engine source and other programmes are
unchanged. Generated and deferred-directory hashes match the initial audit,
and all new files belong to cello.

## Publication, integration and restart

The mathematical inquiry is complete; commit/CI/PR and merge evidence is recorded
in PROGRESS.md and the integration PR. The standing AGENTS.md instruction
authorizes automatic merge after validation. Merge authority does not accept
unverified claims, execute prompts or change scientific status.

The atlas stays at 218 adopted cells, excluding 15 historical failed items.
All broad questions remain open. Atlas-019/020 and the old generated artifacts
remain unchanged and unadopted, with hashes in the initial audit. Frozen history,
old methods and all other programmes are preserved.

Restart with this report, the methods proof and the selection. Independently
choose any next inquiry: different private-write ownership, independently
evolving membership/H, typed abstractions or other gluing policies are possible,
not scheduled findings. No selected experiment remains unfinished.
