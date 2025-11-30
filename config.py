"""
Global configuration for EvoBug.

Centralizing config makes it easy to tweak GA parameters, paths, and
experimental settings without scattering magic numbers everywhere.
"""

# GA parameters (adjust as needed)
POPULATION_SIZE = 30
NUM_GENERATIONS = 50
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
TOURNAMENT_SIZE = 3

# Experiment overrides (smaller defaults for quicker runs; tweak as needed)
EXPERIMENT_POPULATION_SIZE = 12
EXPERIMENT_NUM_GENERATIONS = 8

# Mutation testing configuration
MAX_RIP_HOPS = 9  # Ignore; leftover example in case you need general constants

MUTATION_TOOL = "mutpy"       # or 'custom', if you roll your own mutator
MUTATION_TIMEOUT_SECONDS = 10 # Time limit per mutant batch run

# Experiment settings
RANDOM_BASELINE_NUM_TESTS = 500  # Number of random tests to generate for baseline
NUM_RUNS_PER_PROBLEM = 5         # Repeats to average out randomness in GA

# Paths (you can expand these later if needed)
RESULTS_DIR = "experiments/results"
MUTANTS_CACHE_DIR = "mutation/mutants_cache"

# Reproducibility
GLOBAL_RANDOM_SEED = 42
