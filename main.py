"""CLI entry point for running GA, random baseline, or full experiments."""

import argparse

from ga.engine import run_ga_for_problem
from baselines.random_testing import run_random_baseline
from experiments.run_experiments import run_all_experiments


def main():
    parser = argparse.ArgumentParser(description="EvoBug - GA for killing mutants")
    parser.add_argument(
        "--mode",
        choices=["single-ga", "single-random", "all-experiments"],
        default="all-experiments",
    )
    parser.add_argument(
        "--problem",
        type=str,
        help="Problem module, e.g., problems.problem_two_sum",
    )
    args = parser.parse_args()

    if args.mode == "single-ga":
        if not args.problem:
            raise ValueError("You must provide --problem for mode=single-ga")
        result = run_ga_for_problem(args.problem)
        print("Best fitness:", result["best_fitness"])
        print("Best individual:", result["best_individual"])

    elif args.mode == "single-random":
        if not args.problem:
            raise ValueError("You must provide --problem for mode=single-random")
        result = run_random_baseline(args.problem)
        print("Random baseline mutation score:", result["mutation_score"])

    elif args.mode == "all-experiments":
        run_all_experiments()


if __name__ == "__main__":
    main()
