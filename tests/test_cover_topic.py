"""Tests for cover_topic.py. Only temporary files are written.

Run from the project root:
    python -m unittest discover tests
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_topics import SPECS  # noqa: E402
from cover_topic import add, format_covered  # noqa: E402
from covered import load_covered, load_topics  # noqa: E402

TOPICS = load_topics()
ALGEBRA_9MA0 = list(next(t for t in TOPICS if t["name"] == "Algebra and functions")["9MA0"]["refs"])


class AddTests(unittest.TestCase):
    def test_refs_are_kept_in_spec_order(self):
        data = {}
        for ref in ["10.2", "2.3", "9.1"]:
            self.assertTrue(add(data, "9MA0", "pure", ref, []))
        self.assertEqual(data, {"9MA0": {"pure": ["2.3", "9.1", "10.2"]}})

    def test_already_covered_is_not_added_again(self):
        data = {"9MA0": {"pure": ["2"]}}
        self.assertFalse(add(data, "9MA0", "pure", "2.3", ALGEBRA_9MA0))
        self.assertFalse(add(data, "9MA0", "pure", "2", ALGEBRA_9MA0))

    def test_whole_topic_replaces_its_single_refs(self):
        data = {"9MA0": {"pure": ["1.1", "2.3", "2.4"]}}
        add(data, "9MA0", "pure", "2", ALGEBRA_9MA0)
        self.assertEqual(data["9MA0"]["pure"], ["1.1", "2"])

    def test_written_file_loads_back(self):
        data = {"8MA0": {"statistics": ["2.1"]}, "9MA0": {"mechanics": ["7"], "pure": ["2.3"]}}
        text = format_covered(data)
        self.assertEqual(json.loads(text), data)
        # Fixed order: 9MA0 before 8MA0, pure before mechanics.
        self.assertLess(text.index("9MA0"), text.index("8MA0"))
        self.assertLess(text.index("pure"), text.index("mechanics"))


class CommandTests(unittest.TestCase):
    def setUp(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        self.covered = folder / "covered.json"

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "cover_topic.py"), *args,
                               "--covered", str(self.covered)],
                              capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL)

    def test_add_with_yes_writes_the_file(self):
        result = self.run_script("8MA0", "pure", "2.3", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Added 8MA0 pure 2.3", result.stdout)
        self.assertEqual(load_covered(self.covered, TOPICS)[("8MA0", "pure")], {"2.3"})

    def test_one_quoted_argument_works_too(self):
        self.assertEqual(self.run_script("8MA0 pure 2.3", "--yes").returncode, 0)

    def test_without_confirmation_nothing_is_written(self):
        result = self.run_script("8MA0", "pure", "2.3")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.covered.exists())

    def test_unknown_ref_is_refused(self):
        result = self.run_script("9MA0", "statistics", "9.9", "--yes")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.covered.exists())

    @unittest.skipUnless(SPECS["8MA0"].exists(), "AS specification not downloaded")
    def test_shows_the_full_statement_from_the_spec(self):
        result = self.run_script("8MA0", "pure", "2.3", "--yes")
        # The end of the statement, which topics.json's short label cuts off.
        self.assertIn("in a function of the unknown", " ".join(result.stdout.split()))

    def test_list_marks_covered_refs(self):
        self.run_script("9MA0", "mechanics", "7.3", "--yes")
        out = self.run_script("--list", "9MA0", "mechanics").stdout
        self.assertIn("[x] 7.3", out)
        self.assertIn("[ ] 7.1", out)


if __name__ == "__main__":
    unittest.main()
