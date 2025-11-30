"""Reverse-string wrapper used by the GA pipeline."""

from typing import Tuple
import random
import string

name = "reverse_string"

INPUT_SPEC = {
    "args": [
        {
            "name": "s",
            "type": "str",
            "length_range": (1, 30),
        },
    ]
}

BASE_TESTS = [
    ("hello",),
    ("racecar",),
    ("a",),
    ("",),
]


def target_function(s: str) -> str:
    """Return the reversed string."""
    return s[::-1]


def random_input() -> Tuple[str]:
    """Generate a random ASCII lowercase string within the specified length."""
    length = random.randint(*INPUT_SPEC["args"][0]["length_range"])
    chars = string.ascii_lowercase
    generated = "".join(random.choice(chars) for _ in range(length))
    return (generated,)


def decode_individual(individual_genome):
    """
    In this simple problem the genome is already the argument tuple.
    """
    return individual_genome
