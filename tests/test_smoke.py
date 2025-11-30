import importlib
from unittest import mock

from ga.engine import run_ga_for_problem


def test_ga_smoke_runs_with_stubbed_mutation():
    """
    Run a tiny GA loop with a stubbed mutation scorer to ensure the pipeline
    executes without hitting real MutPy.
    """
    with mock.patch(
        "mutation.mutpy_runner.run_mutation_tests",
        return_value={"mutation_score": 0.5, "killed": 1, "total": 2},
    ):
        result = run_ga_for_problem(
            "problems.problem_two_sum",
            population_size=6,
            num_generations=3,
        )
    assert "best_fitness" in result
    assert result["best_fitness"] >= 0.0
