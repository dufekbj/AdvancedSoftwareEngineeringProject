"""Project-wide configuration for EvoBug."""

# GA parameters (adjust as needed)
POPULATION_SIZE = 60
NUM_GENERATIONS = 20
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.25
TOURNAMENT_SIZE = 4

# Experiment overrides (short runs to iterate quickly)
EXPERIMENT_POPULATION_SIZE = 20
EXPERIMENT_NUM_GENERATIONS = 10

# Mutation testing configuration
MAX_RIP_HOPS = 9  # Ignore; leftover example in case you need general constants

MUTATION_TOOL = "mutpy"       # or 'custom', if you roll your own mutator
MUTATION_TIMEOUT_SECONDS = 15 # Slightly higher to reduce timeouts on harder problems

# Experiment settings
RANDOM_BASELINE_NUM_TESTS = 10  # Number of random tests to generate for baseline
NUM_RUNS_PER_PROBLEM = 2         # Repeats to average out randomness in GA

# Paths (you can expand these later if needed)
RESULTS_DIR = "experiments/results"
RESULTS_RUN_ID = None  # Set to a string to override auto timestamp per run
MUTANTS_CACHE_DIR = "mutation/mutants_cache"

# Reproducibility (set to None to sample a fresh seed each run; the chosen seed is recorded in results)
GLOBAL_RANDOM_SEED = None

# GA evaluation tweaks (to raise ceiling without increasing budgets)
GA_INCLUDE_BASE_TESTS = False  # When False, GA fitness is scored only on the individual's suite (no BASE_TESTS)
INDIVIDUAL_SUITE_SIZE = 3      # How many test inputs a single individual encodes (1 = current behavior)
BASELINE_INCLUDE_BASE_TESTS = True  # Random baseline still keeps BASE_TESTS for comparison

# Problem-specific budget overrides (helps tame long-running problems)
# Keys are problem module paths; values can set population_size and/or num_generations.
PROBLEM_BUDGET_OVERRIDES = {
    "problems.problem_rotated_sort": {"population_size": 6, "num_generations": 3},  # keeps long MutPy runs manageable
}
