"""
GA operators: selection, crossover, mutation.

These stay as problem-agnostic as possible and lean on INPUT_SPEC when present.
"""

from typing import List, Any, Tuple
import random

from config import TOURNAMENT_SIZE, CROSSOVER_RATE, MUTATION_RATE


def tournament_selection(population: List[Any], fitnesses: List[float]) -> Any:
    """
    Tournament selection: pick TOURNAMENT_SIZE individuals at random
    and return the one with highest fitness.

    Parameters
    ----------
    population : List[Any]
        Current population.
    fitnesses : List[float]
        Fitness values aligned with population indices.

    Returns
    -------
    selected : Any
        Selected individual (genome).
    """
    indices = random.sample(range(len(population)), TOURNAMENT_SIZE)
    best_index = max(indices, key=lambda i: fitnesses[i])
    return population[best_index]


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _arg_type(spec):
    return spec.get("type")


def crossover(parent1: Any, parent2: Any, problem_module=None) -> Tuple[Any, Any]:
    """
    Single-point crossover for tuple- or list-like genomes.

    For problem-specific genomes, you might override or extend this.

    For now, we assume:
    - Each genome is either:
        * a tuple of arguments, where each arg is a list/int/etc., or
        * a flat list.
    - We handle the flat-list case and a per-argument crossover for tuples.
    """
    if random.random() > CROSSOVER_RATE:
        return parent1, parent2

    spec_args = getattr(problem_module, "INPUT_SPEC", {}).get("args", []) if problem_module else []

    # Tuple/list genome with per-arg crossover
    if isinstance(parent1, (tuple, list)) and isinstance(parent2, (tuple, list)) and len(parent1) == len(parent2):
        children1 = []
        children2 = []
        for idx, (a, b) in enumerate(zip(parent1, parent2)):
            arg_spec = spec_args[idx] if idx < len(spec_args) else {}
            arg_type = _arg_type(arg_spec)

            if isinstance(a, list) and isinstance(b, list):
                if len(a) < 2 or len(b) < 2:
                    children1.append(random.choice([a, b]))
                    children2.append(random.choice([a, b]))
                else:
                    point = random.randint(1, min(len(a), len(b)) - 1)
                    children1.append(a[:point] + b[point:])
                    children2.append(b[:point] + a[point:])
            elif arg_type == "str" and isinstance(a, str) and isinstance(b, str):
                if len(a) < 2 or len(b) < 2:
                    children1.append(random.choice([a, b]))
                    children2.append(random.choice([a, b]))
                else:
                    point = random.randint(1, min(len(a), len(b)) - 1)
                    children1.append(a[:point] + b[point:])
                    children2.append(b[:point] + a[point:])
            else:
                children1.append(random.choice([a, b]))
                children2.append(random.choice([a, b]))

        child1 = tuple(children1) if isinstance(parent1, tuple) else children1
        child2 = tuple(children2) if isinstance(parent2, tuple) else children2
        return child1, child2

    # Fallback single-point crossover for flat indexables
    if hasattr(parent1, "__len__") and hasattr(parent2, "__len__"):
        length = min(len(parent1), len(parent2))
        if length < 2:
            return parent1, parent2
        point = random.randint(1, length - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    return parent1, parent2


def _mutate_int(value: int, arg_spec: dict) -> int:
    lo, hi = arg_spec.get("value_range", (-1_000_000, 1_000_000))
    delta = random.randint(-5, 5)
    return _clamp(value + delta, lo, hi)


def _mutate_list_int(values: list, arg_spec: dict) -> list:
    lo, hi = arg_spec.get("value_range", (-1_000_000, 1_000_000))
    len_lo, len_hi = arg_spec.get("length_range", (1, len(values) or 1))

    values = list(values)
    if values and random.random() < 0.5:
        idx = random.randrange(len(values))
        values[idx] = _clamp(values[idx] + random.randint(-5, 5), lo, hi)
    else:
        if len(values) < len_hi and random.random() < 0.5:
            values.append(random.randint(lo, hi))
        elif len(values) > len_lo:
            values.pop(random.randrange(len(values)))
    return values


def _mutate_str(value: str, arg_spec: dict) -> str:
    import string

    len_lo, len_hi = arg_spec.get("length_range", (1, max(1, len(value))))
    value_list = list(value)
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "

    action = random.random()
    if action < 0.34 and value_list:
        idx = random.randrange(len(value_list))
        value_list[idx] = random.choice(alphabet)
    elif action < 0.67 and len(value_list) < len_hi:
        value_list.insert(random.randrange(len(value_list) + 1), random.choice(alphabet))
    elif len(value_list) > len_lo:
        value_list.pop(random.randrange(len(value_list)))
    return "".join(value_list)


def mutate(individual: Any, problem_module=None) -> Any:
    """
    Mutation operator using problem INPUT_SPEC to stay within bounds.
    """
    if random.random() > MUTATION_RATE:
        return individual

    spec_args = getattr(problem_module, "INPUT_SPEC", {}).get("args", []) if problem_module else []

    if isinstance(individual, (tuple, list)) and spec_args and len(individual) == len(spec_args):
        mutated = list(individual)
        idx = random.randrange(len(mutated))
        arg_spec = spec_args[idx]
        arg_type = _arg_type(arg_spec)

        if arg_type == "list_int" and isinstance(mutated[idx], list):
            mutated[idx] = _mutate_list_int(mutated[idx], arg_spec)
        elif arg_type == "int" and isinstance(mutated[idx], int):
            mutated[idx] = _mutate_int(mutated[idx], arg_spec)
        elif arg_type == "str" and isinstance(mutated[idx], str):
            mutated[idx] = _mutate_str(mutated[idx], arg_spec)
        else:
            # Fallback: perturb ints or leave untouched
            if isinstance(mutated[idx], int):
                mutated[idx] = mutated[idx] + random.randint(-3, 3)
        return tuple(mutated) if isinstance(individual, tuple) else mutated

    # Fallback: leave unchanged
    return individual
