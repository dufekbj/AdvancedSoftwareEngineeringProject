"""Fitness helpers: compute mutation-score fitness for individuals/suites."""

from typing import Any, List
import importlib

from mutation.mutpy_runner import run_mutation_tests
from config import GA_INCLUDE_BASE_TESTS, INDIVIDUAL_SUITE_SIZE


def evaluate_individual(
    individual: Any,
    problem_module_name: str,
    decode_fn,
) -> float:
    """Decode a genome, build a small test suite, and return its mutation-score fitness."""
    problem_module = importlib.import_module(problem_module_name)
    decoded_input = decode_fn(individual)

    # Optional hook: problem module can provide suite_from_individual to build a small suite from a genome.
    if hasattr(problem_module, "suite_from_individual"):
        test_inputs = problem_module.suite_from_individual(decoded_input)
    else:
        suite_size = max(1, INDIVIDUAL_SUITE_SIZE)
        test_inputs = [decoded_input]
        while len(test_inputs) < suite_size:
            # Top up the suite with fresh random cases to give each individual more chances to kill mutants.
            test_inputs.append(problem_module.random_input())

    result = run_mutation_tests(problem_module_name, test_inputs, use_base_tests=GA_INCLUDE_BASE_TESTS)
    return result["mutation_score"]


def evaluate_population(
    population: List[Any],
    problem_module_name: str,
    decode_fn,
) -> List[float]:
    """Score every individual in the population."""
    return [
        evaluate_individual(individual, problem_module_name, decode_fn)
        for individual in population
    ]
