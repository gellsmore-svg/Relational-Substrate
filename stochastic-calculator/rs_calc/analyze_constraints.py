"""Trial-level analysis of fixed-proposal experiments; never used by the kernel."""

import argparse
from collections import defaultdict
import gzip
import json
from pathlib import Path

from .provenance import write_json


def analyze(paths: list[Path], output: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output.mkdir(parents=True, exist_ok=True)
    report = ["# Fixed-proposal results", "", "C: conservation; G: no growth; R: irreversible readiness.",
              "Intervals are trial-level marginal 95% Wilson intervals. Cells use paired tapes.",
              "Readability and correctness are terminal measurements, not convergence proofs.", ""]
    combined = {}
    for path in paths:
        summary = json.loads((path / "summary.json").read_text())
        config = json.loads((path / "manifest.json").read_text())["config"]
        labels = [cell["label"] for cell in config["cells"]]
        report.extend([f"## {path.name}", "", f"{config['runs']} seeds per cell; {config['horizon']} proposals per trial.", "",
                       "| Cell | Correct | 95% interval | Readable | Identity preserved | Mean escapes |", "| --- | --- | --- | --- | --- | --- |"])
        for label in labels:
            s = summary[label]
            lo, hi = s["wilson95"]
            report.append(f"| {label} | {s['correct']}/{s['runs']} | {lo:.3f}-{hi:.3f} | "
                          f"{s['terminal_readability']:.3f} | {s['identity_preserved_runs']}/{s['runs']} | {s['mean_escapes']:.2f} |")
        grouped = defaultdict(dict)
        with gzip.open(path / "trials.jsonl.gz", "rt") as stream:
            for line in stream:
                row = json.loads(line)
                if row["cell"] in grouped[row["seed"]]:
                    raise ValueError("Duplicate trial cell/seed")
                grouped[row["seed"]][row["cell"]] = row
        if set(grouped) != set(range(config["base_seed"], config["base_seed"] + config["runs"])):
            raise ValueError("Missing or unexpected trial seeds")
        for seed, cells in grouped.items():
            if set(cells) != set(labels) or len({r["proposal_tape"] for r in cells.values()}) != 1:
                raise ValueError(f"Unmatched proposal tapes or missing cells at seed {seed}")
        paired = {}
        for cell in config["cells"]:
            label = cell["label"]
            candidates = [c["label"] for c in config["cells"] if c["inputs"] == cell["inputs"]
                          and c["constraints"].get("conservation", 1) == 1
                          and c["constraints"].get("no_growth", True)
                          and c["constraints"].get("readiness", True)
                          and not c["constraints"].get("local_cancel", False)]
            reference = candidates[0] if candidates else label
            paired[label] = {
                "reference": reference,
                "reference_only_correct": sum(c[reference]["correct"] and not c[label]["correct"] for c in grouped.values()),
                "cell_only_correct": sum(c[label]["correct"] and not c[reference]["correct"] for c in grouped.values())}
        combined[path.name] = {"summary": summary, "paired_discordance": paired,
                               "matched_tapes_verified": len(grouped)}
        report.extend(["", f"Verified identical proposal hashes across cells for all {len(grouped)} paired seeds.",
                       "Paired discordances against full global constraints with matching inputs are retained in `statistics.json`.", ""])
        fig, axes = plt.subplots(2, 1, figsize=(max(8, len(labels) * 0.65), 7), layout="constrained")
        x = list(range(len(labels)))
        acc = [summary[l]["accuracy"] for l in labels]
        axes[0].errorbar(x, acc,
                        yerr=[[max(0, a-summary[l]["wilson95"][0]) for a,l in zip(acc,labels)],
                              [max(0, summary[l]["wilson95"][1]-a) for a,l in zip(acc,labels)]],
                        fmt="o", color="#167153", label="Correct at horizon (95% Wilson)")
        axes[0].plot([v-0.13 for v in x], [summary[l]["terminal_readability"] for l in labels], "x", color="#b04c25", label="Readable at horizon")
        axes[0].plot([v+0.13 for v in x], [summary[l]["identity_preserved_runs"]/summary[l]["runs"] for l in labels], "+", color="#634e9b", label="Identity preserved throughout")
        axes[0].set_ylim(-0.05, 1.08)
        axes[0].set_ylabel("Trial fraction")
        axes[0].legend(fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2)
        axes[1].bar(x, [summary[l]["correct_occupancy"] for l in labels], color="#31778a")
        axes[1].set_ylabel("Mean correct-readout occupancy")
        axes[1].set_ylim(0, 1)
        for ax in axes:
            ax.set_xticks(x, labels, rotation=35, ha="right")
            ax.grid(axis="y", alpha=0.2)
        fig.suptitle(f"{path.name}: fixed {config['horizon']}-proposal horizon")
        fig.savefig(output / f"{path.name}.png", dpi=150)
        fig.savefig(output / f"{path.name}.pdf")
        plt.close(fig)
    write_json(output / "statistics.json", combined)
    (output / "RESULTS.md").write_text("\n".join(report).rstrip() + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    analyze(args.runs, args.output)


if __name__ == "__main__":
    main()
