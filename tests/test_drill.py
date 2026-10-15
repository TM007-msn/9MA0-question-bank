"""Tests for drill.py's question templates and daily.py's pool switch.
Nothing is built or saved.

Run from the project root:
    python -m unittest discover tests
"""

import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_pdf  # noqa: E402
import daily  # noqa: E402
import drill  # noqa: E402

SEEDS = range(25)


class DrillTests(unittest.TestCase):
    def test_sheet_is_about_25_marks_and_covers_every_template(self):
        for seed in SEEDS:
            sheet = drill.make_sheet(seed)
            self.assertEqual(len(sheet), len(drill.TEMPLATES))
            self.assertTrue(24 <= sum(item["marks"] for item in sheet) <= 27)

    def test_same_seed_gives_same_sheet(self):
        self.assertEqual(drill.make_sheet(3), drill.make_sheet(3))
        self.assertNotEqual(drill.make_sheet(3), drill.make_sheet(4))

    def test_every_string_has_balanced_maths(self):
        # An unclosed $ would print literally; split_maths leaves it in the text.
        for seed in SEEDS:
            for item in drill.make_sheet(seed):
                for text in [item["question"], item["answer"], *item["steps"]]:
                    for kind, content in build_pdf.split_maths(text):
                        if kind == "text":
                            self.assertNotIn("$", content, text)
                            self.assertNotIn("\\", content, text)

    def test_answers_are_clean(self):
        for seed in SEEDS:
            for item in drill.make_sheet(seed):
                self.assertNotRegex(item["answer"], r"(?<!\d)1(\\sqrt|y)")
                self.assertNotIn(".", item["answer"].replace("\\ ", ""))  # no decimals


class DailyTests(unittest.TestCase):
    def test_exam_pool_switches_on_15_november(self):
        self.assertEqual(daily.exam_pool(date(2026, 11, 14)), "as-pure")
        self.assertEqual(daily.exam_pool(date(2026, 11, 15)), "alevel-pure")
        self.assertEqual(daily.exam_pool(date(2027, 3, 1)), "alevel-pure")


if __name__ == "__main__":
    unittest.main()
