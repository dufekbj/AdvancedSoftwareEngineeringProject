"""Duplicate digits counter wrapper for the GA pipeline."""

from typing import Tuple
import random

name = "duplicate_digits"

INPUT_SPEC = {
    "args": [
        {
            "name": "N",
            "type": "int",
            "value_range": (1, 50000),
        },
    ]
}

BASE_TESTS = [
    (1,),
    (10,),
    (20,),
    (99,),
    (100,),
    (321,),
    (9876,),
    (9999,),
    (54321,),
    (50000,),
]


def target_function(N: int) -> int:
    """Return count of numbers with duplicate digits at most N."""

    def has_repeated(n: int) -> bool:
        s = str(n)
        return len(set(s)) != len(s)

    def permutation(n: int, k: int) -> int:
        prod = 1
        for i in range(k):
            prod *= n - i
        return prod

    def n_digit_no_repeat(n: int) -> int:
        if n == 1:
            return 9
        return 9 * permutation(9, n - 1)

    N_str = str(N)
    n_digit = len(N_str)
    digits = list(map(int, N_str))
    result = N - 1
    prefix = 0
    for i in range(1, n_digit):
        result -= n_digit_no_repeat(i)
    for i in range(n_digit):
        start = 0 if i else 1
        for j in range(start, digits[i]):
            if has_repeated(prefix * 10 + j):
                continue
            result -= permutation(9 - i, n_digit - 1 - i)
        prefix = prefix * 10 + digits[i]
    return result + has_repeated(N)


def random_input() -> Tuple[int]:
    lo, hi = INPUT_SPEC["args"][0]["value_range"]
    return (random.randint(lo, hi),)


def decode_individual(individual_genome):
    return individual_genome
