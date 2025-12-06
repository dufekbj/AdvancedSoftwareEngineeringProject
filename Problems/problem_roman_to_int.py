"""Roman numeral to int wrapper for the GA pipeline."""

from typing import Tuple
import random

name = "roman_to_int"

INPUT_SPEC = {
    "args": [
        {
            "name": "s",
            "type": "str",
            "length_range": (1, 15),
        },
    ]
}

BASE_TESTS = [
    ("III",),
    ("LVIII",),
    ("MCMXCIV",),
    ("IV",),
    ("CDXLIV",),
    ("MMMCMXCIX",),  # 3999 max standard value
    ("XLII",),       # 42
    ("XCIX",),       # 99
    ("IX",),
    ("MDCLXVI",),
]


def target_function(s: str) -> int:
    values = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    total = 0
    for i in range(len(s)):
        if i + 1 < len(s) and values[s[i]] < values[s[i + 1]]:
            total -= values[s[i]]
        else:
            total += values[s[i]]
    return total


def _int_to_roman(num: int) -> str:
    val = [
        1000,
        900,
        500,
        400,
        100,
        90,
        50,
        40,
        10,
        9,
        5,
        4,
        1,
    ]
    syms = [
        "M",
        "CM",
        "D",
        "CD",
        "C",
        "XC",
        "L",
        "XL",
        "X",
        "IX",
        "V",
        "IV",
        "I",
    ]
    roman_num = []
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num.append(syms[i])
            num -= val[i]
        i += 1
    return "".join(roman_num)


def random_input() -> Tuple[str]:
    # Keep in standard Roman range
    value = random.randint(1, 3999)
    return (_int_to_roman(value),)


def decode_individual(individual_genome):
    return individual_genome
