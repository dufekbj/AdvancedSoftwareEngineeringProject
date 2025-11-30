"""
Representation of GA individuals (test inputs).

Key question: what is a "genome"?
- For some problems, you can directly use (args tuple) as the genome.
- For more complex problems, you might want a flat list of integers, etc.

The design here should be generic enough to work with multiple problems:
- We'll let each problem module handle the details via its decode function,
  but representation.py defines:
    * how to initialize a random individual (per problem)
    * how to copy, mutate, and crossover them shape-wise
"""

from typing import Any, List, Callable
import random

def create_random_individual(problem_module) -> Any:
    """
    Create a single random individual for the given problem.

    Parameters
    ----------
    problem_module : module
        Module that exposes `random_input()`.

    Returns
    -------
    genome : Any
        The GA 'genome'. For now, we just use problem_module.random_input().
    """
    return problem_module.random_input()


def population_init(problem_module, population_size: int) -> List[Any]:
    """
    Initialize a population of random individuals.

    Parameters
    ----------
    problem_module : module
        LeetCode-style problem module with random_input().
    population_size : int

    Returns
    -------
    population : List[Any]
    """
    return [create_random_individual(problem_module) for _ in range(population_size)]
