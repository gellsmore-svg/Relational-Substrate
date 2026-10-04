"""Experiment specifications.

A specification is a JSON object with schema
``rs-constraint-lab.experiment/v1``. Validation is explicit so the laboratory
does not take a JSON-schema dependency.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rs_constraint_lab.semantics import semantics_names
from rs_constraint_lab.weights import ALPHABET_BASE, ENUMERATED_WEIGHTS

SCHEMA = "rs-constraint-lab.experiment/v1"

# Pairwise values the graph engine will execute. Any other declared value is refused.
# Absence of an axis means the implemented value, which is the only legal one
# for graph semantics. Independent hypergraph executes O=3 and refuses the
# graph default. Simplicial semantics are named and refused.
IMPLEMENTED_AXES = {"G": 0, "S": 0, "H": 0, "L": 0, "O": 2}
HYPERGRAPH_AXES = {"G": 0, "S": 0, "H": 0, "L": 0, "O": 3}
COMPOSITIONS = ("structural-simple", "stacked-weight")
ANALYSES = (
    "heavy-every-canonical",
    "memory-clock-reanalysis",
    "n4-singleton",
    "n4-reconfiguration-sensitivity",
    "n4-targeted-pairs",
    "n4-graded-matched-controls",
)
PREDICATES = ("edge", "count")
HYPERGRAPH_PREDICATES = ("pair", "triad")


def load_spec(path: Path | str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_spec(data)
    return data


def spec_hash(data: dict) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_spec(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("experiment spec must be a JSON object")
    if data.get("schema") != SCHEMA:
        raise ValueError(f"spec schema must be {SCHEMA}")
    for key in ("experiment_id", "generation", "semantics", "alphabet", "cells"):
        if key not in data:
            raise ValueError(f"spec is missing {key}")
    if data["semantics"] not in semantics_names():
        raise ValueError(f"unknown semantics {data['semantics']!r}")
    if data["semantics"] == "simplicial":
        raise ValueError(
            "simplicial semantics are represented and not executed; "
            "a simplex is not compiled into independent hypergraph semantics"
        )
    if data["alphabet"] not in ALPHABET_BASE:
        raise ValueError(f"unknown alphabet {data['alphabet']!r}")
    axes = HYPERGRAPH_AXES if data["semantics"] == "hypergraph" else IMPLEMENTED_AXES
    for axis, implemented in axes.items():
        if axis not in data:
            continue
        if not isinstance(data[axis], int) or isinstance(data[axis], bool):
            raise ValueError(f"{axis} must be an integer")
        if data[axis] != implemented:
            raise ValueError(
                f"{axis}={data[axis]} is not executable; the implemented value is {implemented}"
            )
    if "composition" in data and data["composition"] not in COMPOSITIONS:
        raise ValueError(
            f"composition must be one of {', '.join(COMPOSITIONS)}"
        )
    if "analysis" in data and data["analysis"] not in ANALYSES:
        raise ValueError(f"analysis must be one of {', '.join(ANALYSES)}")
    if data["semantics"] == "hypergraph":
        predicates = data.get("predicates", ["pair", "triad"])
        if not isinstance(predicates, list) or not predicates:
            raise ValueError("predicates must be a non-empty list")
        if any(name not in HYPERGRAPH_PREDICATES for name in predicates):
            raise ValueError(
                "independent-hypergraph predicates must be drawn from pair, triad; "
                "count predicates are refused in this generation"
            )
    else:
        predicates = data.get("predicates", ["edge"])
        if not isinstance(predicates, list) or not predicates:
            raise ValueError("predicates must be a non-empty list")
        if any(name not in PREDICATES for name in predicates):
            raise ValueError(f"predicates must be drawn from {', '.join(PREDICATES)}")
    weights = tuple(data.get("weights", ENUMERATED_WEIGHTS))
    if "neutral" in weights:
        raise ValueError("neutral is the multiplicative identity and is not enumerated")
    if any(weight not in ENUMERATED_WEIGHTS for weight in weights):
        raise ValueError("weights must be drawn from the declared alphabet names")
    if not isinstance(data["cells"], list) or not data["cells"]:
        raise ValueError("cells must be a non-empty list")
    for cell in data["cells"]:
        for key in ("N", "K_max", "cardinalities"):
            if key not in cell:
                raise ValueError(f"cell is missing {key}")
        if cell["N"] < 2 or cell["K_max"] < 1:
            raise ValueError("cell N must be >= 2 and K_max >= 1")
        if data["semantics"] == "hypergraph" and cell["N"] < 3:
            raise ValueError("independent hypergraph order 3 requires N >= 3")
        if any(card not in (1, 2, 3) for card in cell["cardinalities"]):
            raise ValueError("cardinalities must be chosen from 1, 2, 3")
        if "A_max" in cell:
            if not isinstance(cell["A_max"], int) or isinstance(cell["A_max"], bool):
                raise ValueError("A_max must be an integer")
            if cell["A_max"] < 1:
                raise ValueError("A_max must be at least 1")
    for name in data.get("sensitivity_alphabets", []):
        if name not in ALPHABET_BASE:
            raise ValueError(f"unknown sensitivity alphabet {name!r}")


def effective_options(data: dict) -> dict:
    """Defaults applied by engine 0.2 when a specification omits them.

    A missing composition is structural-simple. That is a different census
    from the Generation 1 runner, which had no structural filter. The spec
    hash does not change when the default is applied; the semantic version
    and the normalisation version recorded on each shard do.
    """
    hypergraph = data.get("semantics") == "hypergraph"
    axes = HYPERGRAPH_AXES if hypergraph else IMPLEMENTED_AXES
    default_predicates = ["pair", "triad"] if hypergraph else ["edge"]
    predicates = tuple(data.get("predicates", default_predicates))
    return {
        "composition": data.get("composition", "structural-simple"),
        "analysis": data.get("analysis", "heavy-every-canonical"),
        "predicates": predicates,
        "G": data.get("G", axes["G"]),
        "S": data.get("S", axes["S"]),
        "H": data.get("H", axes["H"]),
        "L": data.get("L", axes["L"]),
        "O": data.get("O", axes["O"]),
    }
