"""Tests for drill.py's question templates and levels, and daily.py's pool
switch. Nothing is built or saved.

Run from the project root:
    python -m unittest discover tests
"""

import random
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_pdf  # noqa: E402
import daily  # noqa: E402
import drill  # noqa: E402

# A spread of days: AS weeks 0-4, then A-level weeks 0-6 (the level caps at 6).
DAYS = [drill.START + timedelta(days=d) for d in range(0, 120, 9)]
SEEDS = range(6)


def template(name):
    return next(t for t in drill.TEMPLATES if t.make.__name__ == name)


class LevelTests(unittest.TestCase):
    def test_level_counts_whole_weeks_and_caps(self):
        self.assertEqual(drill.level_for(date(2026, 10, 15)), 0)
        self.assertEqual(drill.level_for(date(2026, 10, 22)), 0)
        self.assertEqual(drill.level_for(date(2026, 10, 23)), 1)
        self.assertEqual(drill.level_for(date(2027, 6, 1)), drill.MAX_LEVEL)

    def test_alevel_starts_on_15_november(self):
        self.assertIsNone(drill.alevel_level_for(date(2026, 11, 14)))
        self.assertEqual(drill.alevel_level_for(date(2026, 11, 15)), 0)
        self.assertEqual(drill.alevel_level_for(date(2026, 11, 29)), 2)


class SheetTests(unittest.TestCase):
    def test_every_sheet_is_24_to_27_marks_easiest_first(self):
        ranks = {t.make.__name__: t.rank for t in drill.TEMPLATES}
        for day in DAYS:
            sheet = drill.make_sheet(day.toordinal(), day)
            self.assertTrue(24 <= sum(i["marks"] for i in sheet) <= 27, day)
            order = [ranks[i["template"]] for i in sheet]
            self.assertEqual(order, sorted(order))

    def test_alevel_templates_only_from_15_november_and_mixed_in(self):
        alevel = {t.make.__name__ for t in drill.TEMPLATES if t.alevel}
        for day in DAYS:
            names = [i["template"] for i in drill.make_sheet(day.toordinal(), day)]
            found = [n for n in names if n in alevel]
            if day < drill.ALEVEL_START:
                self.assertEqual(found, [], day)
            else:
                self.assertIn(len(found), (2, 3), day)
                self.assertLess(len(found), len(names))  # AS questions too

    def test_templates_unlock_and_retire_by_level(self):
        as_names = lambda level: {t.make.__name__ for t in drill.available(level, False)[0]}
        self.assertNotIn("discriminant", as_names(1))
        self.assertIn("discriminant", as_names(2))
        self.assertIn("surds_simplify", as_names(1))
        self.assertNotIn("surds_simplify", as_names(2))

    def test_same_seed_and_day_give_same_sheet(self):
        day = date(2026, 11, 20)
        self.assertEqual(drill.make_sheet(5, day), drill.make_sheet(5, day))


class TemplateTests(unittest.TestCase):
    def items(self):
        for t in drill.TEMPLATES:
            for level in range(drill.MAX_LEVEL + 1):
                for seed in SEEDS:
                    yield t.make.__name__, level, t.make(random.Random(seed), level)

    def test_every_template_runs_at_every_level_with_balanced_maths(self):
        # An unclosed $ would print literally; split_maths leaves it in the text.
        for name, level, item in self.items():
            for text in [item["question"], item["answer"], *item["steps"]]:
                for kind, content in build_pdf.split_maths(text):
                    if kind == "text":
                        self.assertNotIn("$", content, (name, level, text))
                        self.assertNotIn("\\", content, (name, level, text))

    def test_answers_are_clean(self):
        for name, level, item in self.items():
            answer = item["answer"]
            self.assertNotRegex(answer, r"(?<!\d)1(\\sqrt|y|x)", (name, level))
            self.assertNotIn("\\log", answer, (name, level))
            self.assertNotRegex(answer, r"\d\.\d", (name, level))  # no decimals
            self.assertNotIn("+ -", answer, (name, level))

    def test_completing_the_square_has_a_not_1_from_level_1(self):
        for seed in SEEDS:
            item = template("completing_square").make(random.Random(seed), 0)
            self.assertIn("(x + p)^2 + q$, where $p$", item["question"])
            item = template("completing_square").make(random.Random(seed), 1)
            self.assertIn("a(x + p)^2 + q", item["question"])


class DailyTests(unittest.TestCase):
    def test_exam_pool_switches_on_15_november(self):
        self.assertEqual(daily.exam_pool(date(2026, 11, 14)), "as-pure")
        self.assertEqual(daily.exam_pool(date(2026, 11, 15)), "alevel-pure")
        self.assertEqual(daily.exam_pool(date(2027, 3, 1)), "alevel-pure")


if __name__ == "__main__":
    unittest.main()
