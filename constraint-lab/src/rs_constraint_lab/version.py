"""Engine identity recorded on every shard, manifest, and replay.

``ENGINE_VERSION`` is the package release. ``SEMANTIC_VERSION`` is the
scientific meaning of a completed shard. A shard computed under one semantic
version is not reusable under another. Bump ``SEMANTIC_VERSION`` when a fix
changes kernels, census membership, family identity, or exact observables.
A wording change does not bump it and does not require a rerun.

The git commit is provenance. It is recorded on the run header and is not part
of the shard id, so a documentation commit does not invalidate completed work.
"""

ENGINE_VERSION = "0.2.0"
SEMANTIC_VERSION = "0.2.0"

# Independent-hypergraph runs record these versions. The constants above stay
# at 0.2.0 because they are part of every pairwise shard id. A hypergraph
# shard must not resume as a graph shard, and a documentation change to the
# pairwise engine must not move the hypergraph ids either.
HYPERGRAPH_ENGINE_VERSION = "0.3.0"
HYPERGRAPH_SEMANTIC_VERSION = "0.3.0"

NORMALISATION_STRUCTURAL = "structural-unique-v1"
NORMALISATION_STACKED = "stacked-weight-v1"
GRAMMAR_EDGE = "pairwise-edge-v1"
GRAMMAR_COUNT = "pairwise-count-v1"
GRAMMAR_HYPERGRAPH = "independent-hypergraph-v1"

COMPOSITION_STRUCTURAL = "structural-simple"
COMPOSITION_STACKED = "stacked-weight"
ANALYSIS_HEAVY_EVERY = "heavy-every-canonical"

DEFAULT_COMPOSITION = COMPOSITION_STRUCTURAL
DEFAULT_ANALYSIS = ANALYSIS_HEAVY_EVERY
DEFAULT_PREDICATES = ("edge",)

# Item budget for one shard. Sized from a measured worst window on this
# machine, not from the opening combination prefix. See PROFILE_NOTE.
# The same record is copied into docs/execution-resilience.md.
DEFAULT_SHARD_ITEMS = 4000
PROFILE_NOTE = (
    "Measured 2026-10-03 on this development machine, one worker, "
    "OMP/OPENBLAS/MKL threads 1. Binding window: N=4, K<=2, cardinality 2, "
    "combination ranks 4000:8000, 3262 canonical-simple float64 kernels, "
    "66.7s. N=3, K<=3, cardinality 3, ranks 180000:190000 analysed 9399 "
    "rational kernels in 13.6s. The N=3 opening prefix is cheap (ranks "
    "0:1000 analysed nothing) because weights are innermost, so early "
    "combinations stack grades on the first structures. 4000 items keeps "
    "the measured worst window inside 60-90s and under 120s."
)

DEFAULT_WORKERS = 2
MAX_ATTEMPTS = 3
MAX_TASKS_PER_CHILD = 1

EXECUTION_PRINCIPLE = (
    "Prefer bounded, independently reproducible, idempotent units of work "
    "with durable checkpoints, so completed progress is monotonic and "
    "interruption is cheap."
)


def engine_version_for(semantics: str) -> str:
    if semantics == "hypergraph":
        return HYPERGRAPH_ENGINE_VERSION
    return ENGINE_VERSION


def semantic_version_for(semantics: str) -> str:
    if semantics == "hypergraph":
        return HYPERGRAPH_SEMANTIC_VERSION
    return SEMANTIC_VERSION
