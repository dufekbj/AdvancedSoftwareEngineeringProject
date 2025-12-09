# AdvancedSoftwareEngineeringProject (EvoBug)

Genetic-algorithm harness to evolve test inputs that kill mutants for small LeetCode-style functions. Each problem
module exposes a common interface (`INPUT_SPEC`, `target_function`, `random_input`, `decode_individual`, `BASE_TESTS`)
and the GA searches for inputs that maximize mutation scores. MutPy is the primary scorer with a lightweight fallback for
speed and robustness.

## Requirements
- Python 3.10 recommended for MutPy (MutPy 0.6.1 targets 3.10). Other Python versions can run the fallback mutator.
- Dependencies: `pip install -r requirements.txt` (numpy, matplotlib, mutpy, PyYAML, pytest, etc.).
- macOS MutPy patches (3.10 venv): in `mutpy/utils.py`, return `MutationTestRunnerThread` from
  `get_mutation_test_runner_class`, and change `isAlive()` to `is_alive()` in `MutationTestRunnerThread.terminate`.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the code
- All experiments (GA + random baseline across all problems): `python main.py`
- GA once on a problem: `python main.py --mode single-ga --problem problems.problem_two_sum`
- Random baseline once: `python main.py --mode single-random --problem problems.problem_two_sum`
- Force lightweight scorer for speed: `EVOBUG_MUTPY=0 python main.py`
- Run tests (stdlib): `python -m unittest discover`
- Pytest optional: `pytest` (if installed) for nicer output/timeouts

Outputs land in `experiments/results/<timestamp>/` with per-problem JSON summaries and `seeds_used.txt` for
reproducibility. Per-run GA vs Random bars are saved as `ga_vs_random.png` in each run folder.

## Plotting and reproduction
- Aggregate plots across all runs: `python -m viz.plots --mode scores_over_runs --problem problems.problem_two_sum`
  (and similarly for `--mode histories`). Images save if `--output` is provided; otherwise they display.
- First vs latest run comparison (already generated): see `experiments/results/plots_first_vs_latest/` for
  `<problem>_scores_first_vs_latest.png` and `<problem>_histories_first_vs_latest.png`.
- Aggregated plots across all runs: `experiments/results/plots/` holds GA vs Random means and overlaid histories per
  problem after running the provided plotting scripts.

## Configuration (config.py highlights)
- Global budgets: `POPULATION_SIZE`, `NUM_GENERATIONS`, crossover/mutation rates, tournament size.
- Experiment budgets (used by `main.py` default all-experiments mode): `EXPERIMENT_POPULATION_SIZE`, `EXPERIMENT_NUM_GENERATIONS`, `NUM_RUNS_PER_PROBLEM`.
- Problem-specific overrides to tame long runs: `PROBLEM_BUDGET_OVERRIDES`, e.g.
  `{"problems.problem_rotated_sort": {"population_size": 12, "num_generations": 6}}`.
- Mutation scoring: `MUTATION_TIMEOUT_SECONDS` (default 15s); `EVOBUG_MUTPY=0` env var forces fallback scorer.
- Fitness evaluation tweaks (ceiling-raising):
  - `GA_INCLUDE_BASE_TESTS` (default False) controls whether GA fitness includes `BASE_TESTS`; random baseline keeps them via `BASELINE_INCLUDE_BASE_TESTS=True`.
  - `INDIVIDUAL_SUITE_SIZE` (default 3) evaluates each individual as a small suite (genome + extra random inputs) to give more kill chances without higher budgets.

## Implemented problems
- `problems.problem_two_sum`
- `problems.problem_reverse_string` (string generation/mutation uses letters/digits/punctuation/space)
- `problems.problem_rotated_sort`
- `problems.problem_roman_to_int`
- `problems.problem_supersequence` (string generation widened to letters/digits/punctuation/space)
- `problems.problem_dup_digits`

## How mutation scoring works
- `mutation/mutpy_runner.py` builds a temp unittest module from GA inputs (+ optional `BASE_TESTS`) and shells out to
  MutPy. If MutPy fails or times out, it falls back to the internal lightweight mutator (also reachable via
  `EVOBUG_MUTPY=0`).
- Seeds are recorded in `seeds_used.txt` per run; summaries capture per-generation fitness histories for reproducibility
  and plotting.

## Notes and timing expectations
- With defaults and `EVOBUG_MUTPY=0`, a full run finishes in a few minutes. With MutPy enabled, timing scales with mutant
  count per problem; rotated_sort is the heaviest (see `PROBLEM_BUDGET_OVERRIDES` for reduced budgets there).
- Matplotlib may need `MPLCONFIGDIR` set to a writable directory in some environments.
