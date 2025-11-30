"""
MutPy-backed mutation scorer.

Builds a temporary unittest module from provided + baseline inputs, runs MutPy,
and reports killed/total mutants. Falls back to an internal heuristic mutator
if MutPy fails or times out.
"""

from typing import Any, Dict, List
import importlib
import os
import subprocess
import sys
import tempfile

import yaml

from config import MUTATION_TIMEOUT_SECONDS


def _call_with_input(fn, test_input):
    if isinstance(test_input, (tuple, list)):
        return fn(*test_input)
    return fn(test_input)


def _baseline_outputs(problem_module, test_inputs: List[Any]) -> List[Any]:
    target_fn = getattr(problem_module, "target_function")
    outputs = []
    for test_input in test_inputs:
        try:
            outputs.append(_call_with_input(target_fn, test_input))
        except Exception as exc:  # noqa: BLE001 - capture for comparison
            outputs.append(exc)
    return outputs


def _format_literal(value: Any) -> str:
    """
    Safe-ish repr for embedding into generated test files.
    """
    if isinstance(value, Exception):
        return f"Exception('{type(value).__name__}')"
    return repr(value)


def _write_temp_tests(
    problem_module_name: str,
    test_inputs: List[Any],
    expected_outputs: List[Any],
) -> (str, str, str):
    """
    Create a temporary unittest module with one test per input.

    Returns (module_name, file_path, tmp_dir)
    """
    tmp_dir = tempfile.mkdtemp(prefix="mutpy_tests_")
    module_name = "generated_mutpy_tests"
    file_path = os.path.join(tmp_dir, f"{module_name}.py")

    lines = [
        "import unittest",
        "import importlib",
        "",
        f"problem_module = importlib.import_module('{problem_module_name}')",
        "target_function = getattr(problem_module, 'target_function')",
        "",
        "def _call_with_input(args):",
        "    if isinstance(args, (tuple, list)):",
        "        return target_function(*args)",
        "    return target_function(args)",
        "",
        "class GeneratedTests(unittest.TestCase):",
    ]

    for idx, (args, expected) in enumerate(zip(test_inputs, expected_outputs)):
        lines.append(f"    def test_case_{idx}(self):")
        lines.append(f"        args = {repr(args)}")
        lines.append(f"        expected = {_format_literal(expected)}")
        lines.append("        if isinstance(expected, Exception):")
        lines.append("            with self.assertRaises(Exception):")
        lines.append("                _call_with_input(args)")
        lines.append("            return")
        lines.append("        result = _call_with_input(args)")
        lines.append("        self.assertEqual(result, expected)")
        lines.append("")

    with open(file_path, "w") as f:
        f.write("\n".join(lines))

    return module_name, file_path, tmp_dir


def _fallback_lightweight(problem_module_name: str, test_inputs: List[Any]) -> Dict[str, Any]:
    """
    Simple internal mutant generator used when MutPy is unavailable.
    """
    problem_module = importlib.import_module(problem_module_name)
    target_fn = getattr(problem_module, "target_function")

    def _generate_mutants(target_fn):
        mutants = []

        def return_none(*args, **kwargs):
            return None

        def raise_error(*args, **kwargs):
            raise ValueError("mutant triggered error")

        def tweak_int_output(*args, **kwargs):
            res = target_fn(*args, **kwargs)
            if isinstance(res, int):
                return res + 1
            return res

        def reverse_sequence_output(*args, **kwargs):
            res = target_fn(*args, **kwargs)
            if isinstance(res, list) or isinstance(res, tuple):
                return res[::-1]
            return res

        def drop_last_sequence_output(*args, **kwargs):
            res = target_fn(*args, **kwargs)
            if isinstance(res, list) or isinstance(res, tuple):
                return res[:-1]
            return res

        def flip_bool_output(*args, **kwargs):
            res = target_fn(*args, **kwargs)
            if isinstance(res, bool):
                return not res
            return res

        mutants.extend(
            [
                return_none,
                raise_error,
                tweak_int_output,
                reverse_sequence_output,
                drop_last_sequence_output,
                flip_bool_output,
            ]
        )
        return mutants

    expected_outputs = _baseline_outputs(problem_module, test_inputs)
    mutants = _generate_mutants(target_fn)
    killed = 0
    for mutant in mutants:
        for test_input, expected in zip(test_inputs, expected_outputs):
            try:
                actual = _call_with_input(mutant, test_input)
            except Exception as exc:  # noqa: BLE001
                if not isinstance(expected, Exception) or type(exc) is not type(expected):
                    killed += 1
                    break
                continue
            if isinstance(expected, Exception) or actual != expected:
                killed += 1
                break
    total = len(mutants)
    return {
        "mutation_score": killed / total if total else 0.0,
        "killed": killed,
        "total": total,
        "fallback": True,
    }


def run_mutation_tests(
    problem_module_name: str,
    test_inputs: List[Any],
) -> Dict[str, Any]:
    problem_module = importlib.import_module(problem_module_name)
    # Fold in deterministic BASE_TESTS so every run exercises known edge cases.
    base_tests = getattr(problem_module, "BASE_TESTS", [])

    def _dedupe(inputs: List[Any]) -> List[Any]:
        seen = set()
        uniq = []
        for item in inputs:
            key = repr(item)
            if key in seen:
                continue
            seen.add(key)
            uniq.append(item)
        return uniq

    all_tests = _dedupe(list(test_inputs) + list(base_tests))

    # Fast path: force fallback when EVOBUG_MUTPY=0
    if os.getenv("EVOBUG_MUTPY", "1") == "0":
        return _fallback_lightweight(problem_module_name, all_tests)

    expected_outputs = _baseline_outputs(problem_module, all_tests)
    test_module_name, test_file, tmp_dir = _write_temp_tests(
        problem_module_name, all_tests, expected_outputs
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [tmp_dir, os.getcwd(), env.get("PYTHONPATH", "")]
    )

    report_path = os.path.join(tmp_dir, "mutpy_report.yml")

    mutpy_bin = os.path.join(os.path.dirname(sys.executable), "mut.py")
    if not os.path.exists(mutpy_bin):
        import shutil
        mutpy_bin = shutil.which("mut.py", path=os.pathsep.join([os.path.dirname(sys.executable), env.get("PATH", "")]))
    if not mutpy_bin:
        try:
            os.remove(test_file)
            os.rmdir(tmp_dir)
        except OSError:
            pass
        return _fallback_lightweight(problem_module_name, all_tests)

    cmd = [
        mutpy_bin,
        "--target",
        problem_module_name,
        "--unit-test",
        test_module_name,
        "--path",
        tmp_dir,
        "--path",
        os.getcwd(),
        "--report",
        report_path,
        "--quiet",
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=MUTATION_TIMEOUT_SECONDS,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return {"mutation_score": 0.0, "killed": 0, "total": 0, "error": "timeout"}
    finally:
        try:
            os.remove(test_file)
        except OSError:
            pass

    if proc.returncode != 0 or not os.path.exists(report_path):
        reason = "missing_report" if proc.returncode == 0 else f"mutpy_returncode_{proc.returncode}"
        try:
            os.rmdir(tmp_dir)
        except OSError:
            pass
        fallback = _fallback_lightweight(problem_module_name, all_tests)
        fallback["error"] = reason
        fallback["stdout"] = proc.stdout
        fallback["stderr"] = proc.stderr
        return fallback

    try:
        class MutPyLoader(yaml.SafeLoader):
            pass

        def _unknown_python(loader, tag_suffix, node):
            # Treat unknown python tags as simple scalars
            if isinstance(node, yaml.ScalarNode):
                return loader.construct_scalar(node)
            return loader.construct_sequence(node)

        MutPyLoader.add_multi_constructor("tag:yaml.org,2002:python/", _unknown_python)

        with open(report_path, "r") as f:
            report = yaml.load(f, Loader=MutPyLoader) or {}
    except Exception as exc:
        try:
            os.rmdir(tmp_dir)
        except OSError:
            pass
        fallback = _fallback_lightweight(problem_module_name, all_tests)
        fallback["error"] = f"yaml_parse_error:{exc}"
        return fallback
    finally:
        try:
            os.remove(report_path)
            os.rmdir(tmp_dir)
        except OSError:
            pass

    mutants = report.get("mutants") or report.get("mutations") or []
    killed = sum(1 for m in mutants if m.get("status") == "killed")
    total = len(mutants)
    mutation_score = killed / total if total else 0.0

    return {
        "mutation_score": mutation_score,
        "killed": killed,
        "total": total,
        "fallback": False,
    }
