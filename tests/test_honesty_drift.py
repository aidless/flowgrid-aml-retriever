"""Lock public claims to the suite, the package version, and the unscored status.

The README count is the number of tests pytest collects under tests/, which
matches TestLoader.discover().countTestCases() (skipped tests still count).
`python -m unittest discover` prints Ran = that number minus the four
TestDenseNomicIntegration methods, because setUpClass SkipTest is one
class-level skip rather than four skipped cases.
"""
from __future__ import annotations

import unittest
from pathlib import Path

from aml_retriever import __version__

ROOT = Path(__file__).resolve().parents[1]
OLLAMA_CLASS_TESTS = 4


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def _collected() -> int:
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), pattern="test*.py", top_level_dir=str(ROOT / "tests"),
    )
    return suite.countTestCases()


def _problem_lines(readme: str) -> list[str]:
    head, _, rest = readme.partition("## Problem\n")
    if head == readme:
        return []
    body = rest.split("\n## ", 1)[0]
    return [line.strip() for line in body.splitlines() if line.strip()]


class TestHonestyDrift(unittest.TestCase):
    def test_documented_count_matches_suite(self):
        n = _collected()
        sentence = (
            f"pytest collects {n} tests in `tests/` "
            f"(unittest discover reports Ran {n - OLLAMA_CLASS_TESTS} "
            "when the four Ollama tests are a class-level skip)."
        )
        self.assertIn(sentence, _read("README.md"))
        self.assertIn(sentence, _read("README.zh-CN.md"))

    def test_problem_statement_is_three_lines(self):
        lines = _problem_lines(_read("README.md"))
        self.assertEqual(len(lines), 3, lines)
        blob = " ".join(lines)
        self.assertIn("Add", blob)
        self.assertIn("Search", blob)
        self.assertIn("does not generate", blob)
        self.assertIn("no official", blob)

    def test_status_stays_work_in_progress(self):
        for name in ("README.md", "README.zh-CN.md"):
            text = _read(name)
            self.assertIn("STATUS: WORK-IN-PROGRESS — not A yet", text)
            self.assertIn("no official", text.lower())

    def test_version_string_matches_package(self):
        readme = _read("README.md")
        zh = _read("README.zh-CN.md")
        self.assertIn(__version__, readme)
        self.assertIn(__version__, zh)
        self.assertIn("aml-retriever/1.1", readme)
        if not __version__.startswith("1.4"):
            self.assertNotIn("current version is v1.4", readme.lower())
            self.assertNotIn("当前版本为 v1.4", zh)

    def test_withdrawn_claims_are_absent(self):
        for name in ("README.md", "README.zh-CN.md", "docs/EVAL.md"):
            text = _read(name)
            self.assertNotIn("+5.3", text)
            self.assertNotIn("253 passed", text)
            self.assertNotIn("150 项", text)
        ci = _read(".github/workflows/ci.yml")
        self.assertNotIn("253 passed", ci)
        self.assertNotIn("71 passed", ci)

    def test_ci_pytest_targets_tests_tree(self):
        for name in (".github/workflows/checks.yml", ".github/workflows/ci.yml"):
            text = _read(name)
            self.assertIn("python -m pytest tests", text)
        ini = _read("pytest.ini")
        self.assertIn("testpaths = tests", ini)
        checks = _read(".github/workflows/checks.yml")
        self.assertIn("python -m unittest discover -s tests", checks)
        self.assertIn("3.10", checks)
        self.assertIn("3.12", checks)

    def test_failure_modes_cover_required_risks(self):
        text = _read("docs/FAILURE_MODES.md")
        self.assertIn("False greens from synthetic queries", text)
        self.assertIn("User isolation leaks", text)
        self.assertIn("Temporal heuristics overclaim", text)
        self.assertIn("no official", text.lower())
        self.assertIn(__version__, text)

    def test_eval_limits_and_no_machine_path(self):
        text = _read("docs/EVAL.md")
        self.assertIn("## Methodology limits", text)
        self.assertNotIn("cd aml-retriever", text)
        self.assertNotIn("/tmp/repo", text)
        self.assertNotIn("/Users/", text)
        self.assertNotIn("/home/", text)

    def test_contributing_clone_url(self):
        text = _read("CONTRIBUTING.md")
        self.assertIn("aidless/flowgrid-aml-retriever.git", text)
        self.assertNotIn("aidless/just-agent.git", text)
