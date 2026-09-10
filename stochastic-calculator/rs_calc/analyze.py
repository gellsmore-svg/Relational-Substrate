"""Offline statistical analysis and publication/export plots, never a solver."""

import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import statistics

from .metrics import summarize
from .provenance import write_json


def analyze(directories: list[Path], output: Path, plots=True):
    output.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(list)
    sources = []
    cells = {}
    for directory in directories:
        pre = json.loads((directory / "manifest.json").read_text())
        sources.append({"directory": str(directory), "source_sha256": pre["source_sha256"],
                        "config_sha256": pre["config_sha256"]})
        for cell in pre["config"]["cells"]:
            cells[f'{cell["experiment"]}:{cell["label"]}'] = cell
        with gzip.open(directory / "trials.jsonl.gz", "rt") as log:
            for line in log:
                row = json.loads(line)
                row.pop("initial", None)
                row.pop("final", None)
                groups[f'{row["experiment"]}:{row["cell"]}'].append(row)
    results = {}
    for key, rows in groups.items():
        summary = summarize(rows)
        summary["mean_seconds"] = statistics.mean(r["seconds"] for r in rows)
        summary["mean_transition_counts"] = {
            event: statistics.mean(r["events"].get(event, 0) for r in rows)
            for event in sorted({e for r in rows for e in r["events"]})}
        if key.startswith("SC-017"):
            positive = [r["diagnostics"]["positive"] for r in rows]
            negative = [r["diagnostics"]["negative"] for r in rows]
            net = [r["diagnostics"]["net"] for r in rows]
            summary["covariance"] = {"var_positive": statistics.variance(positive),
                                     "var_negative": statistics.variance(negative),
                                     "cov_positive_negative": statistics.covariance(positive, negative),
                                     "var_net": statistics.variance(net)}
        if key.startswith(("SC-009", "SC-020")):
            occupancy = [x for r in rows for x in r["diagnostics"]["occupancy"]]
            summary["occupancy"] = dict(Counter(occupancy))
            summary["escape_events"] = sum(r["diagnostics"]["escape_events"] for r in rows)
            summary["return_events"] = sum(r["diagnostics"]["return_events"] for r in rows)
        if key.startswith(("SC-006", "SC-022")):
            cell = cells[key]
            d = cell["fault_rate"] * (1 - cell["strength"])
            predicted = ((1 - d) / (1 + d)) ** (cell["a"] + cell["b"])
            summary["survival_comparator"] = {"predicted_accuracy": predicted,
                "observed_minus_predicted": summary["accuracy"] - predicted,
                "inside_wilson95": summary["wilson95"][0] <= predicted <= summary["wilson95"][1]}
        results[key] = summary
    write_json(output / "statistics.json", {"sources": sources, "cells": results})
    lines = ["# Measured results", "", "Generated from the listed raw logs; no synthetic outcomes.", "",
             "Intervals are per-cell 95% Wilson binomial intervals, without multiplicity correction.",
             "Timeouts count as incorrect and remain in denominators. Replication details remain",
             "in each run's summary. Timing includes trace hashing and is machine/load dependent.", "",
             "| Experiment / cell | Correct / trials | Accuracy [95% CI] | Mean / p95 transitions | Timeout fraction | Outcome entropy (bits) | Unique paths |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for key in sorted(results):
        s = results[key]
        lo, hi = s["wilson95"]
        lines.append(f'| {key} | {s["correct"]}/{s["runs"]} | {s["accuracy"]:.4f} [{lo:.4f}, {hi:.4f}] | '
                     f'{s["mean_iterations"]:.1f} / {s["p95_iterations"]} | {s["nonconvergence"]:.4f} | '
                     f'{s["outcome_entropy_bits"]:.3f} | {s["unique_trajectories"]} |')
    lines.extend(["", "## Covariance", "", "Statistics across independent trial microstates, not autocorrelated time samples.", ""])
    for key, summary in results.items():
        if "covariance" in summary:
            lines.extend([f"### {key}", "", "```json", json.dumps(summary["covariance"], indent=2), "```", ""])
    lines.extend(["## Occupancy and escape", "", "These are kicked normalization cycles, not equilibrium sampling or physical energy wells.", ""])
    for key, summary in results.items():
        if "occupancy" in summary:
            lines.extend([f"- {key}: {summary['escape_events']} departures from the original identity; "
                          f"{summary['return_events']} returns; occupancy {summary['occupancy']}."])
    lines.extend(["", "## Provenance", "", "```json", json.dumps(sources, indent=2), "```", ""])
    lines.extend(["## No-fit survival comparator", "",
                  "SC-006 motivated the comparator; SC-022 tests it at new noise rates.", "",
                  "| Cell | Predicted | Observed | Difference | Inside pointwise 95% interval |",
                  "| --- | --- | --- | --- | --- |"])
    for key, summary in results.items():
        if "survival_comparator" in summary:
            c = summary["survival_comparator"]
            lines.append(f'| {key} | {c["predicted_accuracy"]:.5f} | {summary["accuracy"]:.5f} | '
                         f'{c["observed_minus_predicted"]:.5f} | {c["inside_wilson95"]} |')
    (output / "RESULTS.md").write_text("\n".join(lines))
    if plots:
        render(groups, cells, results, output)
    return results


def render(groups, cells, results, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "figure.dpi": 140, "savefig.dpi": 180})

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(output / f"{name}.png")
        fig.savefig(output / f"{name}.pdf")
        plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for experiment, label, color in [("SC-003", "Identity 7 + neutral defects", "#007c83"),
                                      ("SC-006", "Addition 3 + 4", "#a73a46")]:
        keys = sorted((k for k in results if k.startswith(experiment)), key=lambda k: cells[k]["strength"])
        x = [cells[k]["strength"] for k in keys]
        y = [results[k]["accuracy"] for k in keys]
        low = [max(0, results[k]["accuracy"] - results[k]["wilson95"][0]) for k in keys]
        high = [max(0, results[k]["wilson95"][1] - results[k]["accuracy"]) for k in keys]
        axes[0].errorbar(x, y, yerr=[low, high], marker="o", capsize=3, color=color, label=label)
        axes[1].plot(x, [results[k]["outcome_entropy_bits"] for k in keys], "o-", color=color, label=label)
    axes[0].set(xlabel="Fault-rejection probability", ylabel="Accuracy (95% Wilson CI)", ylim=(-0.03, 1.03))
    axes[1].set(xlabel="Fault-rejection probability", ylabel="Outcome entropy (bits)")
    axes[0].legend(fontsize=8)
    fig.suptitle("Constraint sweep at fixed attempted deletion rate 0.15")
    save(fig, "constraint")

    keys = sorted(k for k in results if k.startswith("SC-022"))
    if keys:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot([0, 1], [0, 1], color="#555555", linestyle="--", label="No-fit prediction")
        ax.errorbar([results[k]["survival_comparator"]["predicted_accuracy"] for k in keys],
                    [results[k]["accuracy"] for k in keys],
                    yerr=[[results[k]["accuracy"] - results[k]["wilson95"][0] for k in keys],
                          [results[k]["wilson95"][1] - results[k]["accuracy"] for k in keys]],
                    fmt="o", capsize=3, color="#007c83")
        ax.set(xlabel="Predicted accuracy", ylabel="Observed accuracy (95% CI)",
               title="SC-022: held-out noise rates", xlim=(0, 1), ylim=(0, 1))
        save(fig, "survival-comparator")

    fig, ax = plt.subplots(figsize=(6, 4))
    for flag, label, color in [(True, "Bundle replay excluded", "#007c83"),
                                (False, "Replay exclusion removed", "#a73a46")]:
        keys = sorted((k for k in results if k.startswith("SC-014") and cells[k]["coordination"] == flag),
                      key=lambda k: cells[k]["fault_rate"])
        ax.plot([cells[k]["fault_rate"] for k in keys], [results[k]["accuracy"] for k in keys],
                "o-", color=color, label=label)
    ax.set(xlabel="Attempted receive-replay probability", ylabel="Accuracy", ylim=(0, 1.05),
           title="37 + 48: coordination ablation")
    ax.legend()
    save(fig, "coordination")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for key, color in [("SC-017:covariance-neutral", "#007c83"), ("SC-017:covariance-erase", "#a73a46")]:
        rows = groups[key]
        label = cells[key]["perturb"]
        axes[0].scatter([r["diagnostics"]["positive"] for r in rows],
                        [r["diagnostics"]["negative"] for r in rows], s=10, alpha=0.3, color=color, label=label)
        counts = Counter(r["diagnostics"]["net"] for r in rows)
        axes[1].plot(sorted(counts), [counts[x] / len(rows) for x in sorted(counts)], "o-", color=color, label=label)
    axes[0].set(xlabel="Positive contribution", ylabel="Negative contribution", title="Covariance across independent microstates")
    axes[1].set(xlabel="Net signed identity", ylabel="Empirical probability", title="Aggregate variation")
    axes[0].legend()
    save(fig, "covariance")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for locality, color in [("local", "#a73a46"), ("global", "#007c83")]:
        keys = sorted((k for k in results if k.startswith("SC-013") and cells[k]["locality"] == locality),
                      key=lambda k: cells[k]["regions"])
        axes[0].plot([cells[k]["regions"] for k in keys], [results[k]["mean_iterations"] for k in keys],
                     "o-", color=color, label=locality)
    keys = sorted((k for k in results if k.startswith("SC-018")), key=lambda k: cells[k]["max_steps"])
    axes[1].plot([cells[k]["max_steps"] for k in keys], [results[k]["nonconvergence"] for k in keys], "o-", color="#a73a46")
    axes[0].set(xlabel="Ring regions", ylabel="Mean transitions", title="12 - 9: locality cost")
    axes[0].legend()
    axes[1].set(xlabel="Transition budget", ylabel="Timeout fraction", title="32-region local dynamics")
    save(fig, "locality")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    keys = sorted((k for k in results if k.startswith("SC-015")), key=lambda k: cells[k]["a"])
    scale = [cells[k]["a"] + cells[k]["b"] for k in keys]
    axes[0].plot(scale, [results[k]["mean_iterations"] for k in keys], "o-", color="#007c83")
    axes[1].plot(scale, [results[k]["mean_seconds"] for k in keys], "o-", color="#a73a46")
    axes[0].set(xlabel="Input population", ylabel="Mean transitions", title="Unary addition work")
    axes[1].set(xlabel="Input population", ylabel="Mean seconds", title="Observed runtime (including hashing)")
    save(fig, "scaling")

    fig, ax = plt.subplots(figsize=(7, 4))
    for mode, color in [("neutral", "#007c83"), ("flip", "#a73a46")]:
        rows = groups[f"SC-009:occupancy-{mode}"]
        occupancy = [r["diagnostics"]["occupancy"] for r in rows]
        rates = [statistics.mean(path[t] == 7 for path in occupancy) for t in range(len(occupancy[0]))]
        ax.plot(range(len(rates)), rates, "o-", color=color, label=mode)
    ax.set(xlabel="Perturbation / normalization cycle", ylabel="Fraction at original identity 7",
           title="Normal-form recovery versus cross-class damage", ylim=(-0.03, 1.03))
    ax.legend()
    save(fig, "occupancy")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for label, color in [("fixed-initial-3-4", "#007c83"), ("fixed-initial-17-28", "#a73a46")]:
        rows = groups[f"SC-019:{label}"]
        axes[0].hist([r["iterations"] for r in rows], bins=25, alpha=0.65, color=color, label=label)
    axes[0].set(xlabel="Transitions", ylabel="Trials", title="Identical initial states, varying schedules")
    axes[0].legend(fontsize=8)
    axes[1].bar(["3 + 4", "17 + 28"], [results[f"SC-019:{label}"]["unique_trajectories"]
                 for label in ["fixed-initial-3-4", "fixed-initial-17-28"]], color=["#007c83", "#a73a46"])
    axes[1].set(ylabel="Unique structural trajectory hashes", title="2,000 trials per operation")
    save(fig, "trajectory")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args()
    analyze(args.runs, args.output, not args.no_plots)


if __name__ == "__main__":
    main()
