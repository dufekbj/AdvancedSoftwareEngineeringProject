"""
Script to run experiments across all selected problems.

Produces:
- Per-problem JSON/CSV files summarizing GA vs random results.
- Data for later visualization.
"""

from typing import List, Dict, Any
import json
import os
import random
from statistics import mean
from datetime import datetime

from config import (
    RESULTS_DIR,
    RESULTS_RUN_ID,
    GLOBAL_RANDOM_SEED,
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


def ensure_results_dir(run_dir: str):
    os.makedirs(run_dir, exist_ok=True)


def run_all_experiments():
    # Base seed for this batch (recorded in seeds.txt); per-run seeds derive from this.
    base_seed = GLOBAL_RANDOM_SEED if GLOBAL_RANDOM_SEED is not None else random.randint(0, 1_000_000)
    random.seed(base_seed)
    try:
        import numpy as np
        np.random.seed(base_seed)
    except Exception:
        pass
    run_tag = RESULTS_RUN_ID or datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(RESULTS_DIR, run_tag)
    ensure_results_dir(run_dir)
    seeds_used = []

    for problem in PROBLEMS:
        print(f"Running experiments for {problem}...")
        ga_scores = []
        random_scores = []
        ga_runs = []

        # Run GA multiple times to get average behavior
        for i in range(NUM_RUNS_PER_PROBLEM):
            run_seed = random.randint(0, 1_000_000)
            seeds_used.append({"problem": problem, "run_index": i, "seed": run_seed})
            random.seed(run_seed)
            try:
                import numpy as np
                np.random.seed(run_seed)
            except Exception:
                pass
            ga_result = run_ga_for_problem(
                problem,
                population_size=EXPERIMENT_POPULATION_SIZE,
                num_generations=EXPERIMENT_NUM_GENERATIONS,
                seed=run_seed,
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
        random_seed = random.randint(0, 1_000_000)
        seeds_used.append({"problem": problem, "random_seed": random_seed})
        random.seed(random_seed)
        try:
            import numpy as np
            np.random.seed(random_seed)
        except Exception:
            pass
        random_result = run_random_baseline(problem, seed=random_seed)
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
                "results_run_id": run_tag,
                "base_seed": base_seed,
            },
        }

        out_path = os.path.join(run_dir, f"{problem.replace('.', '_')}_summary.json")
        with open(out_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"Saved summary to {out_path}")

    # Write seeds used for this batch
    seeds_path = os.path.join(run_dir, "seeds_used.txt")
    with open(seeds_path, "w") as sf:
        sf.write(f"base_seed={base_seed}\n")
        for entry in seeds_used:
            sf.write(json.dumps(entry) + "\n")
    print(f"Recorded seeds to {seeds_path}")


if __name__ == "__main__":
    run_all_experiments()
