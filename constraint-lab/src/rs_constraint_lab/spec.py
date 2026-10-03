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
    if data["alphabet"] not in ALPHABET_BASE:
        raise ValueError(f"unknown alphabet {data['alphabet']!r}")
    for axis in ("G", "S", "H", "L", "O"):
        if axis in data and not isinstance(data[axis], int):
            raise ValueError(f"{axis} must be an integer")
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
        if any(card not in (1, 2, 3) for card in cell["cardinalities"]):
            raise ValueError("cardinalities must be chosen from 1, 2, 3")
    for name in data.get("sensitivity_alphabets", []):
        if name not in ALPHABET_BASE:
            raise ValueError(f"unknown sensitivity alphabet {name!r}")
