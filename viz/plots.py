"""
Visualization utilities.

Goal:
- Plot GA results stored by `experiments/run_experiments.py`.
"""

import argparse
import json
import os
from typing import List
import matplotlib.pyplot as plt
from glob import glob

from config import RESULTS_DIR


def plot_fitness_history(problem_results_file: str, output_path: str | None = None):
    """
    Plot GA best fitness per run from a summary JSON.
    """
    with open(problem_results_file, "r") as f:
        data = json.load(f)

    scores = data.get("ga_best_scores", [])
    if not scores:
        raise ValueError("No GA scores found in summary file.")

    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(scores) + 1), scores, marker="o")
    plt.xlabel("Run")
    plt.ylabel("Best fitness (mutation score)")
    plt.title(f"GA best scores per run for {data.get('problem', 'unknown')}")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()

    # If per-generation history is available, plot the first run as a sample.
    if data.get("ga_runs"):
        history = data["ga_runs"][0].get("fitness_history", [])
        if history:
            plt.figure(figsize=(8, 4))
            plt.plot(range(1, len(history) + 1), history, marker="o")
            plt.xlabel("Generation")
            plt.ylabel("Best fitness (mutation score)")
            plt.title(f"GA fitness by generation (run 1) for {data.get('problem', 'unknown')}")
            plt.grid(True, linestyle="--", alpha=0.4)
            plt.tight_layout()
            if output_path:
                stem, ext = os.path.splitext(output_path)
                plt.savefig(f"{stem}_history{ext or '.png'}", bbox_inches="tight")
            else:
                plt.show()


def plot_ga_vs_random_bar(problem_results_files: List[str], output_path: str | None = None):
    """
    For each problem summary JSON, extract mean GA and random scores
    and plot them in a bar chart.
    """
    problems = []
    ga_means = []
    rand_means = []

    for fpath in problem_results_files:
        with open(fpath, "r") as f:
            data = json.load(f)
        problems.append(data.get("problem", os.path.basename(fpath)))
        ga_means.append(data.get("ga_best_score_mean", 0.0))
        rand_means.append(data.get("random_score_mean", 0.0))

    x = range(len(problems))
    width = 0.35

    plt.figure(figsize=(10, 5))
    plt.bar([i - width / 2 for i in x], ga_means, width=width, label="GA")
    plt.bar([i + width / 2 for i in x], rand_means, width=width, label="Random")
    plt.xticks(list(x), problems, rotation=20, ha="right")
    plt.ylabel("Mutation score (mean)")
    plt.title("GA vs Random mutation scores")
    plt.legend()
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()


def collect_problem_summaries(results_root: str = RESULTS_DIR):
    """
    Walk all timestamped results folders and collect summaries per problem.
    Returns a dict: problem -> list of (run_id, summary_dict).
    """
    summaries = {}
    for summary_path in glob(os.path.join(results_root, "**", "*_summary.json"), recursive=True):
        with open(summary_path, "r") as f:
            data = json.load(f)
        run_id = data.get("config", {}).get("results_run_id", os.path.basename(os.path.dirname(summary_path)))
        problem = data.get("problem", os.path.basename(summary_path))
        summaries.setdefault(problem, []).append({"run_id": run_id, "data": data})
    return summaries


def plot_problem_scores_over_runs(problem: str, summaries: List[dict], output_path: str | None = None):
    """
    Plot GA vs random mean scores across runs for a single problem.
    """
    if not summaries:
        raise ValueError(f"No summaries provided for {problem}")

    run_ids = []
    ga_means = []
    rand_means = []
    for entry in sorted(summaries, key=lambda e: e["run_id"]):
        run_ids.append(entry["run_id"])
        data = entry["data"]
        ga_means.append(data.get("ga_best_score_mean", 0.0))
        rand_means.append(data.get("random_score_mean", 0.0))

    x = range(len(run_ids))
    width = 0.35
    plt.figure(figsize=(10, 5))
    plt.bar([i - width / 2 for i in x], ga_means, width=width, label="GA")
    plt.bar([i + width / 2 for i in x], rand_means, width=width, label="Random")
    plt.xticks(list(x), run_ids, rotation=25, ha="right")
    plt.ylabel("Mutation score (mean)")
    plt.title(f"GA vs Random mutation scores over runs: {problem}")
    plt.legend()
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()


def plot_problem_histories(problem: str, summaries: List[dict], output_path: str | None = None):
    """
    Overlay best-fitness histories for each GA run across all summaries of a problem.
    """
    plt.figure(figsize=(10, 5))
    any_history = False
    for entry in sorted(summaries, key=lambda e: e["run_id"]):
        run_id = entry["run_id"]
        data = entry["data"]
        ga_runs = data.get("ga_runs", [])
        for idx, run in enumerate(ga_runs):
            history = run.get("fitness_history", [])
            if not history:
                continue
            any_history = True
            label = f"{run_id}-run{idx+1}"
            plt.plot(range(1, len(history) + 1), history, marker="", alpha=0.7, label=label)
    if not any_history:
        plt.close()
        raise ValueError(f"No fitness_history found for {problem}")

    plt.xlabel("Generation")
    plt.ylabel("Best fitness (mutation score)")
    plt.title(f"GA fitness by generation across runs: {problem}")
    plt.legend(fontsize="small", ncol=2)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot GA experiment results.")
    parser.add_argument(
        "--mode",
        choices=["scores_over_runs", "histories"],
        required=True,
        help="Which plot to generate: scores_over_runs or histories.",
    )
    parser.add_argument(
        "--problem",
        required=True,
        help="Problem import path (e.g., problems.problem_two_sum).",
    )
    parser.add_argument(
        "--results-root",
        default=RESULTS_DIR,
        help=f"Root directory containing results (default: {RESULTS_DIR}).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save the plot; otherwise show interactively.",
    )
    args = parser.parse_args()

    summaries = collect_problem_summaries(args.results_root)
    problem_summaries = summaries.get(args.problem, [])
    if not problem_summaries:
        raise SystemExit(f"No summaries found for {args.problem} under {args.results_root}")

    if args.mode == "scores_over_runs":
        plot_problem_scores_over_runs(args.problem, problem_summaries, output_path=args.output)
    elif args.mode == "histories":
        plot_problem_histories(args.problem, problem_summaries, output_path=args.output)


if __name__ == "__main__":
    main()
