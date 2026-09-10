"""Raw-log analysis for passive readouts and recurrent defect dynamics."""

import argparse
from collections import defaultdict
import gzip
import json
import math
from itertools import cycle
from pathlib import Path

from .dynamics_lab import summarize
from .defect_prediction import stationary
from .provenance import write_json


def load_run(path):
    config = json.loads((path / "manifest.json").read_text())["config"]
    rows = {}
    with gzip.open(path / "trials.jsonl.gz", "rt") as f:
        for line in f:
            row = json.loads(line)
            key = (row["cell"], row["seed"], row["horizon"])
            if key in rows:
                raise ValueError("Duplicate checkpoint")
            rows[key] = row
    expected = {(c["label"], seed, h) for c in config["cells"]
                for seed in range(config["base_seed"], config["base_seed"]+config["runs"])
                for h in config["horizons"]}
    if set(rows) != expected:
        raise ValueError("Missing or unexpected checkpoint records")
    tapes = defaultdict(set)
    grouped = defaultdict(list)
    for (cell, seed, h), row in rows.items():
        tapes[seed,h].add(row["proposal_tape"])
        for field in ("defect_occupancy", "population_occupancy"):
            if sum(row[field].values()) != row["window_steps"]:
                raise ValueError("Occupancy denominator mismatch")
        if row["observers"]["ready"]["correct_steps"] > row["observers"]["pure"]["correct_steps"]:
            raise ValueError("Nested readout violation")
        grouped[cell,h].append(row)
    if any(len(t) != 1 for t in tapes.values()):
        raise ValueError("Proposal tapes differ between cells")
    return config, grouped


def compare_recurrent(config, grouped, stats, output, run_name, plt):
    h = max(config["horizons"])
    comparisons = {}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout="constrained")
    colors = cycle(("#13745b", "#a74925", "#63549b", "#28799d"))
    for cell in config["cells"]:
        rows = grouped[cell["label"], h]
        prediction = stationary(rows[0]["expected"], cell["capacity"], cell["birth_admission"])
        observed = [sum(r["defect_occupancy"].get(str(k), 0) for r in rows) /
                    sum(r["window_steps"] for r in rows) for k in range(len(prediction))]
        s = stats[f"{cell['label']}:{h}"]["observers"]["pure"]
        lo, hi = s["occupancy_bootstrap95"]
        comparisons[cell["label"]] = {"stationary_distribution": prediction,
                                      "observed_distribution": observed,
                                      "total_variation_distance": sum(abs(a-b) for a,b in zip(observed,prediction))/2,
                                      "stationary_pure_probability": prediction[0],
                                      "predicted_occupancy_inside_bootstrap95": lo <= prediction[0] <= hi}
        if cell["capacity"] == 32 and cell["birth_admission"] > 0:
            color = next(colors)
            xs = list(range(len(prediction)))
            axes[0].plot(xs, prediction, color=color, label=f"b={cell['birth_admission']}")
            axes[0].plot(xs, observed, ".", color=color)
            axes[1].plot(xs, [-math.log(p) if p else math.nan for p in prediction], color=color)
    axes[0].set_title("Defect occupancy: predicted lines, observed dots")
    axes[0].set_ylabel("Probability / measured time fraction")
    axes[0].legend(fontsize=8)
    axes[1].set_title("Defined statistical potential (not physical energy)")
    axes[1].set_ylabel("-log stationary probability")
    for ax in axes:
        ax.set_xlabel("Neutral defect count k (capacity 32)")
        ax.grid(alpha=.2)
    fig.savefig(output / f"{run_name}-comparator.png", dpi=150)
    fig.savefig(output / f"{run_name}-comparator.pdf")
    plt.close(fig)
    return comparisons


def analyze(paths, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output.mkdir(parents=True, exist_ok=True)
    report = ["# Passive-readout and recurrence results", "",
              "Pure: single-polarity cardinality. Ready: pure plus all records ready.",
              "Terminal counts use seed-level Wilson intervals; occupancy intervals use 1,000 seed-level bootstrap resamples.",
              "Checkpoints and observers share trajectories and are not independent replications.", ""]
    statistics = {}
    for path in paths:
        config, grouped = load_run(path)
        cells = config["cells"]
        stats = {f"{label}:{h}": summarize(rows) for (label,h),rows in grouped.items()}
        statistics[path.name] = {"configuration": config, "summary": stats,
                                 "paired_readout_discordances": {
                                     f"{label}:{h}": sum(r["observers"]["pure"]["correct"] and not r["observers"]["ready"]["correct"] for r in rows)
                                     for (label,h),rows in grouped.items()}}
        if all("birth_admission" in c for c in cells):
            statistics[path.name]["stationary_comparator"] = compare_recurrent(config, grouped, stats, output, path.name, plt)
        report.extend([f"## {config['experiment']}: {path.name}", "",
                       f"{config['runs'] * len(cells)} trajectories, {len(config['horizons'])} checkpoint(s) each; burn-in {config['burn_in']}.",
                       "All cell/seed/checkpoint combinations and paired tape hashes verified.", "",
                       "| Cell | Horizon | Pure correct | Ready correct | Pure occupancy | Ready occupancy | Mean population | Cap rejects |",
                       "| --- | --- | --- | --- | --- | --- | --- | --- |"])
        for cell in cells:
            for h in config["horizons"]:
                s = stats[f"{cell['label']}:{h}"]
                pure, ready = s["observers"]["pure"], s["observers"]["ready"]
                report.append(f"| {cell['label']} | {h} | {pure['terminal_correct']}/{s['runs']} | "
                              f"{ready['terminal_correct']}/{s['runs']} | {pure['mean_correct_occupancy']:.4f} | "
                              f"{ready['mean_correct_occupancy']:.4f} | {s['mean_population']:.2f} | {s['capacity_rejections']} |")
        report.extend(["", "Complete intervals, recurrence counts and paired readout disagreements are in `statistics.json`.", ""])
        if "stationary_comparator" in statistics[path.name]:
            report.extend(["| Cell | Predicted stationary pure occupancy | Measured occupancy (95% seed bootstrap) | Escapes | Complete returns |",
                           "| --- | --- | --- | --- | --- |"])
            for cell in cells:
                pred = statistics[path.name]["stationary_comparator"][cell["label"]]
                obs = stats[f"{cell['label']}:{max(config['horizons'])}"]["observers"]["pure"]
                lo, hi = obs["occupancy_bootstrap95"]
                report.append(f"| {cell['label']} | {pred['stationary_pure_probability']:.5f} | {obs['mean_correct_occupancy']:.5f} "
                              f"({lo:.5f}-{hi:.5f}) | {obs['total_escapes']} | {obs['complete_recovery_episodes']} |")
            report.extend(["", "The comparator was specified before collection. Burn-in alone does not establish equilibrium; intervals are marginal, not simultaneous.", ""])
        fig, axes = plt.subplots(1, 2, figsize=(11, max(4, len(cells)*0.55)), layout="constrained")
        for ax, name in zip(axes, ("pure", "ready")):
            grid = [[stats[f"{cell['label']}:{h}"]["observers"][name]["terminal_correct"]/config["runs"]
                     for h in config["horizons"]] for cell in cells]
            im = ax.imshow(grid, vmin=0, vmax=1, cmap="cividis", aspect="auto")
            ax.set_xticks(range(len(config["horizons"])), config["horizons"])
            ax.set_yticks(range(len(cells)), [c["label"] for c in cells])
            ax.set_title(name.title() + " terminal correctness")
            ax.set_xlabel("Proposal checkpoint")
            for i, row in enumerate(grid):
                for j, val in enumerate(row):
                    ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="white" if val < .5 else "black")
        fig.colorbar(im, ax=axes, label="Fraction of seed trajectories", shrink=.8)
        fig.savefig(output / f"{path.name}-readouts.png", dpi=150)
        fig.savefig(output / f"{path.name}-readouts.pdf")
        plt.close(fig)
        h = max(config["horizons"])
        fig, ax = plt.subplots(figsize=(max(8, len(cells)*.8), 4.5), layout="constrained")
        for name, offset, color in (("pure", -.10, "#187153"), ("ready", .10, "#a74728")):
            data = [stats[f"{cell['label']}:{h}"]["observers"][name] for cell in cells]
            ys = [d["mean_correct_occupancy"] for d in data]
            errs = [[max(0, y-d["occupancy_bootstrap95"][0]) for y,d in zip(ys,data)],
                    [max(0, d["occupancy_bootstrap95"][1]-y) for y,d in zip(ys,data)]]
            ax.errorbar([i+offset for i in range(len(cells))], ys, yerr=errs, fmt="o", color=color, label=name)
        ax.set_xticks(range(len(cells)), [c["label"] for c in cells], rotation=30, ha="right")
        ax.set_ylim(-.03, 1.05)
        ax.set_ylabel("Mean correct-readout occupancy")
        ax.set_title(f"{config['experiment']}: steps {config['burn_in']+1} through {h}, seed-bootstrap 95% intervals")
        ax.legend()
        ax.grid(axis="y", alpha=.2)
        fig.savefig(output / f"{path.name}-occupancy.png", dpi=150)
        fig.savefig(output / f"{path.name}-occupancy.pdf")
        plt.close(fig)
    write_json(output / "statistics.json", statistics)
    (output / "RESULTS.md").write_text("\n".join(report).rstrip() + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    analyze(args.runs, args.output)


if __name__ == "__main__":
    main()
