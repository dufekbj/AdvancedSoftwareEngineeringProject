"""Representation helpers for GA genomes/test inputs."""

from typing import Any, List, Callable
import random

def create_random_individual(problem_module) -> Any:
    """Create a single random individual using the problem's random_input()."""
    return problem_module.random_input()


def population_init(problem_module, population_size: int) -> List[Any]:
    """Initialize a population of random individuals."""
    return [create_random_individual(problem_module) for _ in range(population_size)]
