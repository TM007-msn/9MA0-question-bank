"""Tests for drill.py's question templates and levels, and daily.py's pool
switch. Nothing is built or saved.

Run from the project root:
    python -m unittest discover tests
"""

import json
import random
import tempfile
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
            # Everything was on yesterday's sheet, so nothing is due.
            yesterday = {day - timedelta(days=1): drill.available_names(day)}
            names = [i["template"] for i in drill.make_sheet(day.toordinal(), day, yesterday)]
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


class RotationTests(unittest.TestCase):
    def test_due_means_available_all_week_and_on_no_sheet(self):
        day = date(2026, 12, 1)
        window = [day - timedelta(days=b) for b in range(1, drill.WINDOW)]
        everything = drill.available_names(day)
        history = {d: set() for d in window}
        self.assertEqual(drill.due_names(day, history), everything)
        history[window[-1]] = {"modulus"}  # on the sheet six days ago
        self.assertNotIn("modulus", drill.due_names(day, history))
        # Unlocked fewer than six days ago (A level starts 15 Nov): not due yet.
        self.assertNotIn("modulus", drill.due_names(date(2026, 11, 18), {}))

    def test_due_templates_go_on_the_sheet(self):
        day = date(2026, 12, 1)
        everything = drill.available_names(day)
        # Everything except two templates appeared yesterday.
        history = {day - timedelta(days=1): everything - {"rationalising", "partial_fractions"}}
        names = {i["template"] for i in drill.make_sheet(1, day, history)}
        self.assertTrue({"rationalising", "partial_fractions"} <= names)

    def test_read_history_takes_daily_records_from_the_last_six_days(self):
        folder = Path(tempfile.mkdtemp())
        day = date(2026, 12, 1)

        def record(name, templates):
            path = folder / f"{name}.json"
            path.write_text(json.dumps({"questions": [{"template": t} for t in templates]}), encoding="utf-8")
            self.addCleanup(path.unlink)
        record("drill-2026-11-30", ["indices"])
        record("drill-2026-11-25", ["modulus"])
        record("drill-2026-11-24", ["binomial"])     # seven days back: outside the window
        record("drill-2026-12-01", ["factorising"])  # today's own record: ignored
        record("drilltest-2026-11-29", ["surds"])    # not a daily record
        self.assertEqual(drill.read_history(day, folder),
                         {date(2026, 11, 30): {"indices"}, date(2026, 11, 25): {"modulus"}})

    def test_consecutive_days_meet_the_seven_day_guarantee(self):
        # Five weeks across the start of A level, each day seeing the sheets before it.
        history = {}
        days = [date(2026, 11, 1) + timedelta(days=i) for i in range(35)]
        for day in days:
            window = {d: names for d, names in history.items() if (day - d).days < drill.WINDOW}
            history[day] = {i["template"] for i in drill.make_sheet(day.toordinal(), day, window)}
        for i in range(len(days) - drill.WINDOW + 1):
            week = days[i:i + drill.WINDOW]
            needed = set.intersection(*(drill.available_names(d) for d in week))
            seen = set().union(*(history[d] for d in week))
            self.assertEqual(needed - seen, set(), week[0])


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
