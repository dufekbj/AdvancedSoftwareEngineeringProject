"""
Visualization utilities.

Goal:
- Plot GA results stored by `experiments/run_experiments.py`.
"""

import json
import os
from typing import List
import matplotlib.pyplot as plt

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
