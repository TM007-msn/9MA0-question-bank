"""Tests for weak_topics.py's ranking and re-test dates. Nothing is written.

Run from the project root:
    python -m unittest discover tests
"""

import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from covered import load_topics  # noqa: E402
from weak_topics import retests_due, weak_refs  # noqa: E402

TOPICS = load_topics()
TODAY = date(2026, 10, 11)
BANK = {
    "9MA0-01_2019-06_Q01": {"paper": "9MA0-01", "topic": "Differentiation", "spec_ref": "7.3, 7.2", "marks": 4},
    "9MA0-01_2019-06_Q02": {"paper": "9MA0-01", "topic": "Integration", "spec_ref": "8.2", "marks": 6},
    "9MA0-31_2019-06_Q01": {"paper": "9MA0-31", "topic": "Probability", "spec_ref": "3.1", "marks": 2},
}
BANK["9MA0-01_2019-06_Q01-A"] = BANK["9MA0-01_2019-06_Q01"]
COVERED = {("9MA0", "pure"): {"7.2", "7.3", "8.2", "3.1"}}


def attempt(day, question_id, awarded, total, error="", topic="Differentiation"):
    return {"date": date(2026, *day), "question_id": question_id, "topic": topic,
            "marks_awarded": awarded, "marks_total": total, "error_type": error}


class WeakRefTests(unittest.TestCase):
    def test_ranked_by_marks_lost_with_main_ref_only(self):
        attempts = [
            attempt((10, 1), "9MA0-01_2019-06_Q01", 1, 4, "method"),
            attempt((10, 5), "9MA0-01_2019-06_Q01-A", 2, 4, "slip"),
            attempt((10, 6), "9MA0-01_2019-06_Q01", 3, 4, "slip"),
            attempt((10, 9), "9MA0-01_2019-06_Q02", 2, 6, "knowledge", "Integration"),
        ]
        rows = weak_refs(attempts, BANK, COVERED, TOPICS, TODAY, 14)
        self.assertEqual([(r["ref"], r["lost"], r["available"], r["error"]) for r in rows],
                         [("7.3", 6, 12, "slip"), ("8.2", 4, 6, "knowledge")])
        self.assertEqual(rows[0]["topic"], "Differentiation")
        self.assertAlmostEqual(rows[0]["dropped"], 50)

    def test_window_and_coverage(self):
        attempts = [
            attempt((9, 26), "9MA0-01_2019-06_Q01", 0, 4, "time"),       # 15 days before: outside
            attempt((9, 27), "9MA0-01_2019-06_Q02", 0, 6, "time"),       # 14 days before: inside
            attempt((10, 2), "9MA0-31_2019-06_Q01", 0, 2, "knowledge"),  # statistics 3.1 is not covered
        ]
        rows = weak_refs(attempts, BANK, COVERED, TOPICS, TODAY, 14)
        self.assertEqual([r["ref"] for r in rows], ["8.2"])


class RetestTests(unittest.TestCase):
    def test_7_and_21_days_after_lost_marks(self):
        attempts = [attempt((9, 20), "9MA0-01_2019-06_Q02", 3, 6, "slip")]
        due = retests_due(attempts, TODAY)
        # Day 7 (27 Sep) is overdue; day 21 (11 Oct) is today.
        self.assertEqual([(d["due"], d["after_days"]) for d in due],
                         [(date(2026, 9, 27), 7), (date(2026, 10, 11), 21)])

    def test_full_marks_need_no_retest(self):
        self.assertEqual(retests_due([attempt((10, 8), "9MA0-01_2019-06_Q02", 6, 6)], TODAY), [])

    def test_done_by_a_later_attempt_including_a_variant(self):
        attempts = [attempt((9, 20), "9MA0-01_2019-06_Q01", 1, 4, "method"),
                    attempt((9, 28), "9MA0-01_2019-06_Q01-A", 4, 4)]
        due = retests_due(attempts, TODAY)
        self.assertEqual([d["after_days"] for d in due], [21])

    def test_attempt_before_the_due_date_does_not_count(self):
        attempts = [attempt((10, 1), "9MA0-01_2019-06_Q01", 1, 4, "method"),
                    attempt((10, 3), "9MA0-01_2019-06_Q01", 4, 4)]
        self.assertEqual([d["due"] for d in retests_due(attempts, TODAY)], [date(2026, 10, 8)])

    def test_far_future_retests_are_not_listed(self):
        attempts = [attempt((10, 10), "9MA0-01_2019-06_Q01", 1, 4, "method")]
        # Day 7 is 17 Oct (within a week); day 21 is 31 Oct (not yet listed).
        self.assertEqual([d["after_days"] for d in retests_due(attempts, TODAY)], [7])


if __name__ == "__main__":
    unittest.main()
