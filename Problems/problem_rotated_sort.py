"""Rotated sorted array search wrapper for the GA pipeline."""

from typing import List, Tuple
import random

name = "rotated_sorted_array_search"

INPUT_SPEC = {
    "args": [
        {
            "name": "nums",
            "type": "list_int",
            "length_range": (1, 20),
            "value_range": (-100, 100),
        },
        {
            "name": "target",
            "type": "int",
            "value_range": (-150, 150),
        },
    ]
}

BASE_TESTS = [
    ([4, 5, 6, 7, 0, 1, 2], 0),
    ([4, 5, 6, 7, 0, 1, 2], 3),
    ([1], 0),
    ([1, 3], 3),
    ([6, 7, 1, 2, 3, 4, 5], 3),
    ([30, 40, 50, 10, 20], 10),
    ([2, 2, 2, 3, 4, 2], 3),
    ([0, 5, -20, -15, -10, -5], -15),
    ([10, 10, 10, 1, 10], 1),
    ([5, 1, 3], 2),
]


def target_function(nums: List[int], target: int) -> int:
    """
    Return index of target in rotated sorted array nums, or -1 if not found.
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def random_input() -> Tuple[List[int], int]:
    length = random.randint(*INPUT_SPEC["args"][0]["length_range"])
    lo, hi = INPUT_SPEC["args"][0]["value_range"]
    base = sorted(random.randint(lo, hi) for _ in range(length))

    # Rotate by a random pivot
    if length > 1:
        pivot = random.randint(0, length - 1)
        nums = base[pivot:] + base[:pivot]
    else:
        nums = base

    lo_t, hi_t = INPUT_SPEC["args"][1]["value_range"]
    target = random.randint(lo_t, hi_t)
    return nums, target


def decode_individual(individual_genome):
    return individual_genome
