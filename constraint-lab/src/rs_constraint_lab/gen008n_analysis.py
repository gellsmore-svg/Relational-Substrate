"""Post-census exact classification of existing frozen P0 outputs, no new cells."""

from collections import Counter
from pathlib import Path

from flint import fmpq as Q

from rs_constraint_lab.gen008m_exec import read, write
from rs_constraint_lab.gen008n_exec import DIRECTORY, OUTPUT, TABLE, items


def main():
    root = Path(__file__).resolve().parents[3]
    summary = read(root / (TABLE + "summary.json"))
    mfpt = read(root / (TABLE + "mfpt.json"))
    committor = read(root / (TABLE + "committor.json"))
    classifications = []
    for item in items():
        identity = item["item_id"]
        rows = [r for r in summary if r["system_id"] == identity]
        means = [r for r in mfpt if r["system_id"] == identity]
        probs = [r for r in committor if r["system_id"] == identity]
        flags = {"RETURN_ROUTING": any(r["routing_active"] for r in rows),
                 "CROSS_CLASS_MFPT": any(Q(r["difference"]) for r in means),
                 "K3_COMMITTOR": any(Q(r["difference"]) for r in probs),
                 "LENGTH_PROFILE": any(r["length_active"] for r in rows),
                 "UP_ROUTE": any(r["UP_active"] for r in rows), "DOWN_ROUTE": any(r["DOWN_active"] for r in rows)}
        classifications.append({"system_id": identity, "classifications": {key: key + ("_ACTIVE" if value else "_SILENT")
                                for key, value in flags.items()}, "active_source_rows": sum(r["routing_active"] for r in rows),
                                "active_MFPT_tasks": sum(bool(Q(r["difference"])) for r in means),
                                "active_committor_sources": sum(bool(Q(r["difference"])) for r in probs)})
    nonneutral = [r for r in summary if r["m"] != "1"]
    overview = {}
    for label in ("ANY", "FORM", "DISSOLVE", "ALL"):
        s = [r for r in nonneutral if label == "ALL" or r["family"] == label]
        m = [r for r in mfpt if r["m"] != "1" and (label == "ALL" or r["family"] == label)]
        c = [r for r in committor if r["m"] != "1" and (label == "ALL" or r["family"] == label)]
        overview[label] = {"source_rows": len(s), "routing_active": sum(r["routing_active"] for r in s),
                           "UP_active": sum(r["UP_active"] for r in s), "DOWN_active": sum(r["DOWN_active"] for r in s),
                           "length_active": sum(r["length_active"] for r in s), "tail_active": sum(r["tail_active"] for r in s),
                           "first_lengths": dict(Counter(str(r["first_length"]) for r in s)),
                           "MFPT_tasks": len(m), "MFPT_active": sum(bool(Q(r["difference"])) for r in m),
                           "MFPT_slower": sum(Q(r["difference"]) > 0 for r in m),
                           "MFPT_faster": sum(Q(r["difference"]) < 0 for r in m),
                           "committor_tasks": len(c), "committor_active": sum(bool(Q(r["difference"])) for r in c),
                           "committor_silent": sum(not Q(r["difference"]) for r in c)}
    receipts = [read(root / OUTPUT / (item["item_id"] + ".json")) for item in items()]
    overview["execution"] = {"items": len(receipts), "sum_item_seconds": sum(r["wall_seconds"] for r in receipts),
                             "max_item_seconds": max(r["wall_seconds"] for r in receipts),
                             "item_bytes": sum((root / OUTPUT / (item["item_id"] + ".json")).stat().st_size for item in items()),
                             "retry": 0, "quarantine": 0, "split": 0, "scientific_amendment": 0}
    overview["interpretation"] = "Exact finite palette counts, not all-positive-m passage theorems or a scalar ranking."
    write(root / (TABLE + "classifications.json"), classifications)
    write(root / (TABLE + "overview.json"), overview)
    print(overview, flush=True)


if __name__ == "__main__":
    main()
