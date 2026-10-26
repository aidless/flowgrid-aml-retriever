import subprocess
import sys
import unittest
from pathlib import Path


class TestDemoAddSearch(unittest.TestCase):
    def test_runs_offline(self):
        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, "examples/demo_add_search.py"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("current launch", proc.stdout)
        self.assertIn("bob sees 0 hits", proc.stdout)
        self.assertIn("no server, no API key", proc.stdout)
