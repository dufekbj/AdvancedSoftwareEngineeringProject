"""
Random testing baseline.

Goal:
- Compare GA performance to purely random input generation.
- For a fixed budget of test inputs (e.g., 500), generate random inputs
  and compute resulting mutation score.

Design choice:
- Evaluate mutation score of the whole random suite at once.
"""

from typing import Any, Dict
import importlib
import random

try:
    import numpy as np
except Exception:  # pragma: no cover - numpy optional
    np = None

from mutation.mutpy_runner import run_mutation_tests
from config import RANDOM_BASELINE_NUM_TESTS, BASELINE_INCLUDE_BASE_TESTS


def run_random_baseline(problem_module_name: str, seed: int | None = None) -> Dict[str, Any]:
    """
    Run random testing for a single problem.

    Steps:
    - Import problem module.
    - Use problem_module.random_input() to generate N test inputs.
    - Call run_mutation_tests() with the whole test suite.
    - Return mutation score and other stats.

    Returns
    -------
    result : dict
        At least:
        - 'mutation_score'
        - 'killed'
        - 'total'
        - 'num_tests'
    """
    if seed is not None:
        random.seed(seed)
        if np is not None:
            try:
                np.random.seed(seed)
            except Exception:
                pass
    problem_module = importlib.import_module(problem_module_name)

    test_inputs = [problem_module.random_input()
                   for _ in range(RANDOM_BASELINE_NUM_TESTS)]

    result = run_mutation_tests(problem_module_name, test_inputs, use_base_tests=BASELINE_INCLUDE_BASE_TESTS)
    # Short-circuit on timeout to avoid stalling the whole run.
    if result.get("error") == "timeout":
        return {
            "mutation_score": 0.0,
            "killed": 0,
            "total": 0,
            "fallback": result.get("fallback", False),
            "num_tests": len(test_inputs),
            "error": "timeout",
        }
    result["num_tests"] = RANDOM_BASELINE_NUM_TESTS
    return result
