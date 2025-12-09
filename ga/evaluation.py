"""
Fitness evaluation for GA individuals.

Fitness here = mutation score (or a function of it) when using this
individual as a test input (or part of a test suite).

Design choice:
- You can treat each individual as a *single test input*.
- Fitness of an individual = mutation score when using just that one input.
- Or: treat an individual as a *set of test inputs*, and evaluate them as a suite.

For simplicity for now:
- Each individual == single test input.
- Fitness = #killed mutants / total mutants (float in [0, 1]).
"""

from typing import Any, List
import importlib

from mutation.mutpy_runner import run_mutation_tests
from config import GA_INCLUDE_BASE_TESTS, INDIVIDUAL_SUITE_SIZE


def evaluate_individual(
    individual: Any,
    problem_module_name: str,
    decode_fn,
) -> float:
    """
    Evaluate a single individual.

    Steps:
    - Decode the GA genome into function arguments.
    - Build a one-element test suite [decoded_input].
    - Call `run_mutation_tests` with that suite.
    - Return mutation_score as fitness.

    Parameters
    ----------
    individual : Any
        GA genome.
    problem_module_name : str
        E.g., 'problems.problem_two_sum'
    decode_fn : callable
        Function that turns an individual into concrete args, e.g.,
        decode_fn(individual) -> (nums, target)

    Returns
    -------
    fitness : float
        Mutation score.
    """
    problem_module = importlib.import_module(problem_module_name)
    decoded_input = decode_fn(individual)

    # Optional hook: problem module can provide suite_from_individual to build a small suite from a genome.
    if hasattr(problem_module, "suite_from_individual"):
        test_inputs = problem_module.suite_from_individual(decoded_input)
    else:
        suite_size = max(1, INDIVIDUAL_SUITE_SIZE)
        test_inputs = [decoded_input]
        while len(test_inputs) < suite_size:
            test_inputs.append(problem_module.random_input())

    result = run_mutation_tests(problem_module_name, test_inputs, use_base_tests=GA_INCLUDE_BASE_TESTS)
    return result["mutation_score"]


def evaluate_population(
    population: List[Any],
    problem_module_name: str,
    decode_fn,
) -> List[float]:
    """
    Evaluate all individuals in the population.

    NOTE:
    - This is potentially expensive, because it might call the mutation
      tool once per individual.
    - You may later want to batch or cache evaluations.

    Returns
    -------
    fitnesses : List[float]
    """
    return [
        evaluate_individual(individual, problem_module_name, decode_fn)
        for individual in population
    ]
