# Generation 8 event schema

Schema id: `rs-constraint-lab.generation-008-event/v1`

The event stream is the primary scientific object. Derived tables are summaries of that stream. A seed by itself is not the forensic record.

## Clocks and draw

Selection reuses the laboratory toggle kernel. Baseline weight is 1 on every relation slot. A matching constraint multiplies that weight by its alphabet factor. Round 0 uses alphabet `W4`. `strong_suppress` is `1/4`.

The draw is one call to Python `random.Random.randrange(norm)` on MT19937. `norm` is the sum of the integer weights after the least common multiple of the fraction denominators. The stored uniform draw is the unreduced rational `draw/norm`. That is a discrete uniform integer on `0 .. norm-1`. It is not a binary floating-point sample.

A pair slot is one of the first six relation slots. A triad slot is one of the last four. `pair_index` is null on a triad-only event. Those events remain in the stream.

## Episode header

Each episode record stores:

```text
episode_id
experiment_id
round_id
system_id
source_graph_class
hidden_context_orbit_id
replicate_index
seed
seed_function
initial_state
initial_state_hash
final_state
final_state_hash
constraint_system_hash
event_stream_sha256
event_payload_sha256
trajectory_hash
spec_hash
frozen_plan_commit
runner_version
python_version
termination_reason
event_count
pair_event_count
```

`trajectory_hash` is the rolling SHA-256. It starts from the canonical initial-state record and folds each canonical event line.

`event_payload_sha256` is the SHA-256 of the uncompressed canonical JSONL bytes. `event_stream_sha256` is the SHA-256 of the gzip file that stores those bytes. Replay checks the payload hash, the rolling hash, the recomputed weights, and the draw.

## Event fields

One JSON object per line, canonical key order when hashed:

```text
t
pre
post
slot
kind
pair_index
full_index
draw
norm
uniform_draw
selected_weight
selected_integer
probability
weight_hash
weights
rules
pair_before
pair_after
triad_before
triad_after
context_before
context_after
rng_token
```

`weights` is the ten fraction strings, one per slot, before normalisation. `weight_hash` is their SHA-256. `rules` lists the indexes of constraints whose `matches` predicate accepted the selected slot. `kind` is `form` or `dissolve`. `rng_token` is `sha256-u64-v1:<draws consumed before this event>`. Restoring the seed and consuming `randrange` that many times restores the generator. Segment cursors also store `random.Random.getstate()` so a resumed segment does not recompute earlier events.

`pair_before` and `pair_after` are indexes into the eleven-name class table stored on the episode header. `context_before` and `context_after` name the triad-configuration orbit under the automorphism group of the current labelled pair graph. The label is `p{pair_mask:02d}-t{canonical_triad:02d}-s{orbit_size}`. `canonical_triad` is the least triad index in that orbit. The raw full state remains the ground truth.

## Storage

```text
episodes/<episode_id>.json          header and derived summary
streams/<episode_id>.jsonl.gz       canonical event JSONL, gzip
```

`trajectory inspect <episode-id>` prints the events with class names. Replay of a valid episode reports `verification = exact`.

## Segment chain

If a segment boundary is used, the next segment receives the previous final state, the RNG state, the event counts, and the rolling trajectory hash. The chained stream is required to match a one-process execution of the same episode. `segment_boundary` is an execution cursor. It is not a scientific termination reason.

## Derived summaries

Summaries are computed from the event stream. Route labels are recomputed from the run-length encoding of the pair-class sequence. A cached route string is not an input to that calculation.

The pair-class sequence includes epoch 0, the initial state. Each pair event appends the post-event class. Run lengths sum to `pair_event_count + 1`. The 11×11 transition matrix counts pair events, including events that stay inside a class. Its total is `pair_event_count`.

Route motifs of length 2, 3, and 4 are counted on the change-compressed class path. That path collapses consecutive events that stay inside one isomorphism class. The transition matrix keeps those stays. The atlas records how many motif keys were omitted above the retained 60.
