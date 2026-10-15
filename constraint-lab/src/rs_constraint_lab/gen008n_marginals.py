"""Post-census timing marginals of frozen joint length/destination tables.

No new kernel, stopping time, return length, solve or scientific item.
"""

from collections import Counter
from pathlib import Path

from flint import fmpq as Q

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.gen008m_exec import read, write
from rs_constraint_lab.gen008n_exec import TABLE


def main():
    root = Path(__file__).resolve().parents[3]
    source = TABLE + "return-lengths.json"
    rows = []
    for layer in read(root / source):
        for c in layer["H2"]["classes"]:
            laws = {}
            for model in ("H2", "Kpi"):
                data = layer[model]
                laws[model] = {str(n): sum((Q(v) for v in data["lengths"][str(n)][c]), Q(0))
                               for n in (2, 4, 6, 8, 10, 12)}
                laws[model]["tail"] = sum((Q(v) for v in data["tail"][c]), Q(0))
                assert sum(laws[model].values()) == 1
            delta = {n: laws["H2"][n] - laws["Kpi"][n] for n in laws["H2"]}
            rows.append({key: layer[key] for key in ("system_id", "family", "role", "m", "k")} |
                        {"source": c, **laws, "difference": delta,
                         "first_timing_difference": next((n for n in (2, 4, 6, 8, 10, 12) if delta[str(n)]),
                                                         "tail" if delta["tail"] else None)})
    output = {"source_path": source, "source_sha256": sha256_file(root / source),
              "meaning": "Marginal sum over destination of already frozen F_(k,n); tail is total >12 mass, not an all-order timing equivalence test.",
              "non_neutral_first_timing_lengths": dict(Counter(str(r["first_timing_difference"]) for r in rows if r["m"] != "1")),
              "rows": rows}
    write(root / (TABLE + "timing-marginals.json"), output)
    print(output["non_neutral_first_timing_lengths"])


if __name__ == "__main__":
    main()
