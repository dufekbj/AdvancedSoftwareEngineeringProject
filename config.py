"""
Global configuration for EvoBug.

Centralizing config makes it easy to tweak GA parameters, paths, and
experimental settings without scattering magic numbers everywhere.
"""

# GA parameters (adjust as needed)
POPULATION_SIZE = 60
NUM_GENERATIONS = 20
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.25
TOURNAMENT_SIZE = 4

# Experiment overrides (smaller defaults for quicker runs; tweak as needed)
EXPERIMENT_POPULATION_SIZE = 30  # tuned to keep full suite ~10 minutes with MutPy
EXPERIMENT_NUM_GENERATIONS = 15

# Mutation testing configuration
MAX_RIP_HOPS = 9  # Ignore; leftover example in case you need general constants

MUTATION_TOOL = "mutpy"       # or 'custom', if you roll your own mutator
MUTATION_TIMEOUT_SECONDS = 15 # Time limit per mutant batch run

# Experiment settings
RANDOM_BASELINE_NUM_TESTS = 150  # Number of random tests to generate for baseline
NUM_RUNS_PER_PROBLEM = 2         # Repeats to average out randomness in GA

# Paths (you can expand these later if needed)
RESULTS_DIR = "experiments/results"
RESULTS_RUN_ID = None  # Set to a string to override auto timestamp per run
MUTANTS_CACHE_DIR = "mutation/mutants_cache"

# Reproducibility (set to None to sample a fresh seed each run; the chosen seed is recorded in results)
GLOBAL_RANDOM_SEED = None
