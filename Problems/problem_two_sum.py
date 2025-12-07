"""LeetCode-style problem wrapper for two-sum."""

from typing import List, Tuple, Dict, Any
import random

name = "two_sum"

# INPUT_SPEC describes what the input vector looks like for this problem:
# Example: (nums: List[int], target: int)
INPUT_SPEC = {
    "args": [
        {
            "name": "nums",
            "type": "list_int",
            "length_range": (2, 20),
            "value_range": (-100, 100),
        },
        {
            "name": "target",
            "type": "int",
            "value_range": (-200, 200),
        },
    ]
}

BASE_TESTS = [
    ([2, 7, 11, 15], 9),
    ([3, 3], 6),
    ([3, 2, 4], 6),
    ([-1, -2, -3, -4, -5], -8),
    ([0, 4, 3, 0], 0),
    ([1, 2, 3, 4, 5], 10),
    ([5, 75, 25], 100),
    ([2, 5, 5, 11], 10),
    ([1, 3, 4, 2], 6),
    ([-3, 4, 3, 90], 0),
    ([1, 2, 3], 100),           # no solution
    ([1, 2, 3, 4, 5], 6),       # multiple pairs exist
    ([0, -1, 2, -3, 4], 1),     # mixed signs
    ([3, 3, 4, 2], 6),          # duplicate valid pairs
    ([5, 6, 1, 0], 7),          # zero plus positive
    ([1, 1, 1, 1], 2),          # all duplicates
]


def target_function(nums: List[int], target: int) -> List[int]:
    """
    The actual implementation under test.
    """
    lookup = {}
    for idx, val in enumerate(nums):
        complement = target - val
        if complement in lookup:
            return [lookup[complement], idx]
        lookup[val] = idx
    return []


def random_input() -> Tuple[List[int], int]:
    """
    Generate a single random input consistent with INPUT_SPEC.

    Used for:
    - initializing GA population
    - random baseline
    """
    nums_len = random.randint(*INPUT_SPEC["args"][0]["length_range"])
    lo, hi = INPUT_SPEC["args"][0]["value_range"]
    nums = [random.randint(lo, hi) for _ in range(nums_len)]

    lo_t, hi_t = INPUT_SPEC["args"][1]["value_range"]
    target = random.randint(lo_t, hi_t)

    return nums, target


def decode_individual(individual_genome: Any) -> Tuple[List[int], int]:
    """
    Convert a GA 'genome' representation into concrete function arguments.

    This is the link between the GA representation (which might be a flat list
    of integers, or a custom encoding) and the actual function inputs.
    """
    return individual_genome
