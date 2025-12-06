# AdvancedSoftwareEngineeringProject

Genetic Algorithms for mutating LeetCode-style programs (EvoBug).

EvoBug evolves test inputs to kill mutants generated from small LeetCode-style functions. Each problem module exposes a
standard interface (input spec, target function, random input, baseline tests), and the GA searches for inputs that
maximize mutation scores. Mutation scoring uses MutPy by default (with a lightweight fallback for speed), and
experiments compare GA performance against random testing across the included problems.

## Quick start
- Set up venv (recommended):
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Run all experiments (GA + random baseline): `python main.py`
- Run GA once on a specific problem: `python main.py --mode single-ga --problem problems.problem_two_sum`
- Run random baseline once on a specific problem: `python main.py --mode single-random --problem problems.problem_two_sum`
- Run GA on a specific problem: `python main.py --mode single-ga --problem problems.problem_two_sum`
- Run random baseline only: `python main.py --mode single-random --problem problems.problem_two_sum`
- Run tests: `pytest`
- Speed up mutation scoring by forcing the lightweight mutator: `EVOBUG_MUTPY=0 python main.py`

## Implemented problems
- `problems.problem_two_sum` (list of ints + target)
- `problems.problem_reverse_string` (simple string reversal)
- `problems.problem_rotated_sort` (rotated array search)
- `problems.problem_roman_to_int` (Roman numeral parsing)
- `problems.problem_supersequence` (shortest common supersequence)
- `problems.problem_dup_digits` (count numbers with duplicate digits)

## Experiments
- Defaults are tuned for quick runs (see `config.EXPERIMENT_*`); bump them up when you want final numbers.
- Results land in `experiments/results/` as JSON summaries, including GA run histories.

## Plots
- Use `viz/plots.py` to visualize GA per-run performance and GA vs random bars from the summary JSONs. Pass an
  `output_path` to save images.
- After running `python main.py`, check `experiments/results/plots/` for saved images (e.g., `ga_vs_random.png`). You can
  also open the JSON summaries in `experiments/results/` with `viz/plots.py` to generate additional fitness-by-generation
  plots.

## Limitations / notes
- MutPy on Python 3.14 is patched to run, but it can be slow; set `EVOBUG_MUTPY=0` to use the lightweight internal
  mutator for quick iterations.
- Matplotlib may warn about cache directory permissions; set `MPLCONFIGDIR` to a writable folder if needed.
- Experiment defaults use small populations/generations for speed—adjust in `config.py` when running “real” trials.
- Rough timings: with defaults and `EVOBUG_MUTPY=0`, `python main.py` completes in a couple of minutes on a laptop. With
  full MutPy scoring (no `EVOBUG_MUTPY=0`), expect runs to stretch to tens of minutes depending on hardware.

## How mutation scoring works
`mutation/mutpy_runner.py` shells out to MutPy (patched for Python 3.14) to run
mutation testing. If MutPy fails, it falls back to a simple internal mutator so
the GA can still run end-to-end.
Set `EVOBUG_MUTPY=0` to always use the lightweight mutator (useful for quick
experiments or headless environments).

## Results/outputs
- Experiment summaries are written to `experiments/results/`
- Mutation cache placeholder lives at `mutation/mutants_cache/`
