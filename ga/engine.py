"""
Main GA loop.

This module ties together:
- population initialization
- fitness evaluation
- selection, crossover, mutation
- tracking best fitness per generation

It should be generic over problems.
"""

from typing import Dict, Any, List, Tuple
import importlib
import random

from config import POPULATION_SIZE, NUM_GENERATIONS, GLOBAL_RANDOM_SEED
from .representation import population_init
from .operators import tournament_selection, crossover, mutate
from .evaluation import evaluate_population


def run_ga_for_problem(
    problem_module_name: str,
    population_size: int | None = None,
    num_generations: int | None = None,
) -> Dict[str, Any]:
    """
    Run the GA for a single problem.

    Parameters
    ----------
    problem_module_name : str
        Import path to problem, e.g. 'problems.problem_two_sum'

    Returns
    -------
    results : dict
        Fields might include:
        - 'best_individual'
        - 'best_fitness'
        - 'fitness_history' (list of best per generation)
        - 'avg_fitness_history'
    """
    random.seed(GLOBAL_RANDOM_SEED)

    # Allow experiments to override defaults; fall back to config values.
    population_size = population_size or POPULATION_SIZE
    num_generations = num_generations or NUM_GENERATIONS

    problem_module = importlib.import_module(problem_module_name)
    decode_fn = getattr(problem_module, "decode_individual")

    # 1. Initialize population
    population = population_init(problem_module, population_size)

    # 2. Evaluate initial population
    fitnesses = evaluate_population(population, problem_module_name, decode_fn)

    best_individual = None
    best_fitness = -1.0
    fitness_history = []
    avg_fitness_history = []

    for gen in range(num_generations):
        # Track stats
        gen_best_index = max(range(len(population)), key=lambda i: fitnesses[i])
        gen_best_fitness = fitnesses[gen_best_index]
        gen_avg_fitness = sum(fitnesses) / len(fitnesses)

        fitness_history.append(gen_best_fitness)
        avg_fitness_history.append(gen_avg_fitness)

        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best_individual = population[gen_best_index]

        # 3. Create new population via selection + crossover + mutation
        new_population = []
        while len(new_population) < len(population):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            child1, child2 = crossover(parent1, parent2, problem_module)
            child1 = mutate(child1, problem_module)
            child2 = mutate(child2, problem_module)

            new_population.append(child1)
            if len(new_population) < len(population):
                new_population.append(child2)

        population = new_population
        fitnesses = evaluate_population(population, problem_module_name, decode_fn)

    return {
        "best_individual": best_individual,
        "best_fitness": best_fitness,
        "fitness_history": fitness_history,
        "avg_fitness_history": avg_fitness_history,
    }
