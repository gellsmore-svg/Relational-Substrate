"""Audit saved Atlas-018 records without importing or executing the RRC engine."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_HASH = "2468bf59c1fce72fb909482dc94e1abeae30e627f0bd71e4536ed8b10b7a27e0"


def canonical_hash(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def probability_rows(payload: list) -> list[list[Fraction]]:
    return [[Fraction(int(cell["num"]), int(cell["den"])) for cell in row] for row in payload]


def oracle(spec: dict) -> dict:
    size = spec["n_states"]
    width = spec["bit_width"]
    require(type(width) is int and width > 0 and size == 2 ** width and size <= 16, "invalid bit width")
    if spec.get("catalogue") == "single_toggle":
        weights = spec["rows"]
        require(len(weights) == size and all(len(row) == width for row in weights), "invalid catalogue shape")
        events = [
            {"name": f"toggle-{state}-{bit}", "kind": "toggle", "source": state,
             "target": state ^ (2 ** bit), "weight": weight}
            for state, row in enumerate(weights)
            for bit, weight in enumerate(row)
        ]
    else:
        events = spec["events"]
    names = set()
    sums = [Counter() for _ in range(size)]
    enabled = [0] * size
    noop = [0] * size
    for event in events:
        name, kind = event["name"], event["kind"]
        source, target, weight = event["source"], event["target"], event["weight"]
        require(isinstance(name, str) and bool(name) and name not in names, "duplicate or missing event name")
        names.add(name)
        require(type(source) is int and type(target) is int and 0 <= source < size and 0 <= target < size, "invalid event state")
        require(type(weight) is int and weight >= 0, "invalid event weight")
        distance = sum(first != second for first, second in zip(f"{source:0{width}b}", f"{target:0{width}b}"))
        valid = {"toggle": distance == 1, "joint": distance >= 2,
                 "noop": source == target, "transition": source != target}
        require(kind in valid and valid[kind], "event kind disagrees with its update")
        if weight:
            sums[source][target] += weight
            enabled[source] += 1
            if kind == "noop":
                noop[source] += weight
    totals = [sum(row.values()) for row in sums]
    probabilities = [
        [Fraction(sums[source][target], totals[source]) if totals[source]
         else Fraction(source == target) for target in range(size)]
        for source in range(size)
    ]
    completions = [
        "halt_self_loop" if not total else "noop_event" if noop[source] == total
        else "normalised_events_including_noop" if noop[source] else "normalised_events"
        for source, total in enumerate(totals)
    ]
    return {"events": events, "probabilities": probabilities,
            "aggregated_weights": [[row[target] for target in range(size)] for row in sums],
            "row_sums": totals, "enabled_event_counts": enabled, "completions": completions}


def expected_correspondence(spec: dict, probabilities: list[list[Fraction]]) -> dict | None:
    image = spec.get("image_map")
    if image is None:
        return None
    reference = oracle(spec["reference"])["probabilities"]
    require(len(image) == len(reference) and len(set(image)) == len(image), "image must be an injection")
    require(all(type(state) is int and 0 <= state < len(probabilities) for state in image), "invalid image state")
    included = set(image)
    invariant = all(not probabilities[source][target] for source in image
                    for target in range(len(probabilities)) if target not in included)
    restricted = [[probabilities[source][target] for target in image] for source in image] if invariant else None
    return {"image": sorted(image), "image_invariant": invariant,
            "conjugate": invariant and restricted == reference, "restricted_rows": restricted}


def check_record(spec: dict, result: dict, receipt: dict, result_bytes: bytes,
                 plan_hash: str, engine: str) -> dict:
    item_id = spec["id"]
    spec_hash = canonical_hash(spec)
    for payload in (result, receipt):
        require(payload.get("item_id") == item_id, "item identity drift")
        require(payload.get("plan_hash") == plan_hash and payload.get("spec_hash") == spec_hash, "input hash drift")
        require(payload.get("status") == "complete", "item is not complete")
    require(receipt.get("result_sha256") == hashlib.sha256(result_bytes).hexdigest(), "receipt byte hash drift")
    require(result.get("engine_version") == engine and result.get("round_id") == spec["round_id"], "engine or round drift")
    require(result.get("type") == "strict_event_comparison", "item type drift")
    require(result.get("method") == "event-kernel-0.2.0" and result.get("clock") == "one_declared_event", "method or clock drift")
    require(result.get("semantics") == "bitmask" and result.get("bit_width") == spec["bit_width"], "state semantics drift")
    require(result.get("n_states") == spec["n_states"] and result.get("family") == spec["family"], "state count or family drift")
    require(result.get("new_primitive") is False and result.get("halt_self_loop_is_event") is False, "primitive or halt claim drift")
    expected = oracle(spec)
    for field in ("events", "aggregated_weights", "row_sums", "enabled_event_counts", "completions"):
        require(result.get(field) == expected[field], f"{field} differs from frozen specification")
    require(result.get("event_count") == len(expected["events"]), "event count drift")
    probabilities = probability_rows(result["probabilities"])
    require(probabilities == expected["probabilities"], "probability rows differ from independent oracle")
    require(all(sum(row) == 1 and all(cell >= 0 for cell in row) for row in probabilities), "nonstochastic row")
    compared = result.get("correspondence")
    expected_comparison = expected_correspondence(spec, probabilities)
    if expected_comparison is None:
        require(compared is None, "unexpected correspondence")
    else:
        require(isinstance(compared, dict), "missing correspondence")
        for field in ("image", "image_invariant", "conjugate"):
            require(compared.get(field) == expected_comparison[field], f"correspondence {field} drift")
        actual_rows = compared.get("restricted_rows")
        actual_rows = probability_rows(actual_rows) if actual_rows is not None else None
        require(actual_rows == expected_comparison["restricted_rows"], "restricted rows drift")
    return {"item_id": item_id, "states": len(probabilities),
            "probability_cells_checked": sum(map(len, probabilities)),
            "image_invariant": expected_comparison["image_invariant"] if expected_comparison else None,
            "conjugate": expected_comparison["conjugate"] if expected_comparison else None,
            "result_sha256": receipt["result_sha256"]}


def coupled_encoding(probabilities: list[list[Fraction]]) -> dict:
    require(len(probabilities) == 16, "encoding check requires four bits")
    encoded = []
    for state in range(16):
        outer_left = state & 1
        first_copy = (state >> 1) & 1
        second_copy = (state >> 2) & 1
        outer_right = (state >> 3) & 1
        encoded.append(outer_left | (first_copy << 1) | (outer_right << 2)
                       | ((first_copy ^ second_copy) << 3))
    require(set(encoded) == set(range(16)), "recoding is not bijective")
    require(all(probabilities[source][target] ==
                (Fraction(1, 3) if encoded[target] in {encoded[source] ^ flip for flip in (1, 2, 4)} else 0)
                for source in range(16) for target in range(16)), "recoded kernel does not match three toggles and a frozen bit")
    require(all(sum(probabilities[source][target] for target in range(16) if encoded[target] % 8 == label)
                == (Fraction(1, 3) if label in {encoded[source] % 8 ^ flip for flip in (1, 2, 4)} else 0)
                for source in range(16) for label in range(8)), "dropping disagreement is not an exact quotient")
    return {"state_map": encoded, "recoded_kernel_exact": True,
            "dropped_disagreement_quotient_exact": True,
            "scope": "post-execution kernel recoding; original joint-event kinds are not preserved"}


def audit(output: Path) -> dict:
    plan = json.loads((ROOT / "plans/atlas-018.json").read_text())
    require(canonical_hash(plan) == PLAN_HASH, "frozen plan drift")
    manifest = json.loads((output / "manifest.json").read_text())
    require(manifest == {"plan_hash": PLAN_HASH, "round_id": "atlas-018",
                         "engine_version": plan["engine_version"]}, "manifest drift")
    summaries = []
    matrices = {}
    inventory = {"manifest.json"}
    for spec in plan["items"]:
        directory = output / "items" / spec["id"]
        raw = (directory / "result.json").read_bytes()
        result = json.loads(raw)
        receipt = json.loads((directory / "receipt.json").read_text())
        summaries.append(check_record(spec, result, receipt, raw, PLAN_HASH, plan["engine_version"]))
        status = json.loads((directory / "status.json").read_text())
        require(status == {"item_id": spec["id"], "status": "complete", "plan_hash": PLAN_HASH}, "status record drift")
        matrices[spec["id"]] = probability_rows(result["probabilities"])
        inventory.update(str((directory / name).relative_to(output)) for name in ("result.json", "receipt.json", "status.json"))
    require({str(path.relative_to(output)) for path in output.rglob("*") if path.is_file()} == inventory, "unexpected output inventory")
    image = plan["items"][1]["image_map"]
    leakages = [sum(matrices["A18-free"][source][target] for target in range(16) if target not in image) for source in image]
    return {"status": "verified", "round_id": "atlas-018", "plan_hash": PLAN_HASH,
            "scientific_worker_invocations": 0, "verified_items": len(summaries),
            "probability_cells_checked": sum(item["probability_cells_checked"] for item in summaries),
            "items": summaries, "free_image_leakage": [str(value) for value in leakages],
            "post_execution_analysis": coupled_encoding(matrices["A18-coupled"])}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "results/atlas-018")
    args = parser.parse_args()
    print(json.dumps(audit(args.out), indent=2))


if __name__ == "__main__":
    main()
