"""
Script to run experiments across all selected problems.

Produces:
- Per-problem JSON/CSV files summarizing GA vs random results.
- Data for later visualization.
"""

from typing import List, Dict, Any
import json
import os
from statistics import mean

from config import (
    RESULTS_DIR,
    NUM_RUNS_PER_PROBLEM,
    EXPERIMENT_NUM_GENERATIONS,
    EXPERIMENT_POPULATION_SIZE,
)
from ga.engine import run_ga_for_problem
from baselines.random_testing import run_random_baseline


PROBLEMS = [
    "problems.problem_two_sum",
    "problems.problem_reverse_string",
    "problems.problem_rotated_sort",
    "problems.problem_roman_to_int",
    "problems.problem_supersequence",
    "problems.problem_dup_digits",
]


def ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def run_all_experiments():
    ensure_results_dir()

    for problem in PROBLEMS:
        print(f"Running experiments for {problem}...")
        ga_scores = []
        random_scores = []
        ga_runs = []

        # Run GA multiple times to get average behavior
        for i in range(NUM_RUNS_PER_PROBLEM):
            ga_result = run_ga_for_problem(
                problem,
                population_size=EXPERIMENT_POPULATION_SIZE,
                num_generations=EXPERIMENT_NUM_GENERATIONS,
            )
            ga_scores.append(ga_result["best_fitness"])
            ga_runs.append(
                {
                    "best_fitness": ga_result["best_fitness"],
                    "fitness_history": ga_result["fitness_history"],
                    "avg_fitness_history": ga_result["avg_fitness_history"],
                }
            )

        # Single (or multiple) runs for random baseline
        random_result = run_random_baseline(problem)
        random_scores.append(random_result["mutation_score"])

        summary = {
            "problem": problem,
            "ga_best_scores": ga_scores,
            "ga_best_score_mean": mean(ga_scores),
            "ga_runs": ga_runs,
            "random_scores": random_scores,
            "random_score_mean": mean(random_scores),
            "random_details": random_result,
            "config": {
                "population_size": EXPERIMENT_POPULATION_SIZE,
                "num_generations": EXPERIMENT_NUM_GENERATIONS,
                "num_runs": NUM_RUNS_PER_PROBLEM,
            },
        }

        out_path = os.path.join(
            RESULTS_DIR,
            f"{problem.replace('.', '_')}_summary.json"
        )
        with open(out_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"Saved summary to {out_path}")


if __name__ == "__main__":
    run_all_experiments()
