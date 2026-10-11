"""Tests for quick_set.py's selection rules. Nothing is built or saved.

Run from the project root:
    python -m unittest discover tests
"""

import json
import random
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from covered import load_covered, load_topics  # noqa: E402
from quick_set import due_retests, eligible, pick, recently_attempted  # noqa: E402

TOPICS = load_topics()


def temp_file(test, name, text):
    folder = Path(tempfile.mkdtemp())
    path = folder / name
    path.write_text(text, encoding="utf-8")
    test.addCleanup(path.unlink)
    return path


def entry(id_, topic, spec_ref, marks=3, difficulty="medium"):
    paper, series = id_.split("_")[:2]
    return {"id": id_, "paper": paper, "series": series, "topic": topic,
            "spec_ref": spec_ref, "marks": marks, "difficulty": difficulty}


class CoveredTests(unittest.TestCase):
    def covered(self, data):
        return load_covered(temp_file(self, "covered.json", json.dumps(data)), TOPICS)

    def test_topic_number_expands_within_its_strand(self):
        covered = self.covered({"9MA0": {"pure": ["7"], "statistics": ["2.1"]}})
        differentiation = next(t for t in TOPICS if t["name"] == "Differentiation")
        self.assertEqual(covered[("9MA0", "pure")], set(differentiation["9MA0"]["refs"]))
        self.assertEqual(covered[("9MA0", "statistics")], {"2.1"})

    def test_unknown_ref_or_strand_is_refused(self):
        with self.assertRaises(SystemExit):
            self.covered({"9MA0": {"pure": ["7.9"]}})
        with self.assertRaises(SystemExit):
            self.covered({"9MA0": {"algebra": ["2"]}})

    def test_missing_file_explains_the_format(self):
        with self.assertRaises(SystemExit) as caught:
            load_covered(Path(tempfile.gettempdir()) / "no-such-covered.json", TOPICS)
        self.assertIn('"pure"', str(caught.exception))


class EligibleTests(unittest.TestCase):
    approved = {("9MA0-01", "2019-06"), ("9MA0-31", "2019-06")}

    def test_refs_are_matched_within_the_entry_strand(self):
        # Pure 3 is coordinate geometry; statistics 3.1 (probability) is not covered by it.
        covered = {("9MA0", "pure"): {"3.1", "3.2"}}
        pure = entry("9MA0-01_2019-06_Q01", "Coordinate geometry in the (x,y) plane", "3.1")
        stats = entry("9MA0-31_2019-06_Q01", "Probability", "3.1")
        self.assertEqual(eligible([pure, stats], covered, set(), self.approved, TOPICS), [pure])

    def test_every_ref_must_be_covered(self):
        covered = {("9MA0", "pure"): {"7.3"}}
        e = entry("9MA0-01_2019-06_Q02", "Differentiation", "7.3, 7.2")
        self.assertEqual(eligible([e], covered, set(), self.approved, TOPICS), [])

    def test_recent_and_unapproved_are_skipped(self):
        covered = {("9MA0", "pure"): {"7.3"}}
        recent = entry("9MA0-01_2019-06_Q02", "Differentiation", "7.3")
        unapproved = entry("9MA0-01_2020-10_Q02", "Differentiation", "7.3")
        self.assertEqual(eligible([recent, unapproved], covered, {recent["id"]}, self.approved, TOPICS), [])


class AttemptTests(unittest.TestCase):
    def test_last_21_days_and_variants_count(self):
        csv_text = ("date,question_id,topic,marks_awarded,marks_total,error_type\n"
                    "2026-09-19,9MA0-01_2019-06_Q01,Proof,1,2,\n"     # 22 days before: too old
                    "2026-09-20,9MA0-01_2019-06_Q02,Proof,1,2,\n"     # 21 days before: recent
                    "2026-10-05,9MA0-01_2019-06_Q03b-A,Proof,1,2,\n")  # variant of Q03b
        recent = recently_attempted(date(2026, 10, 11), temp_file(self, "attempts.csv", csv_text))
        self.assertEqual(recent, {"9MA0-01_2019-06_Q02", "9MA0-01_2019-06_Q03b"})


class PickTests(unittest.TestCase):
    def test_medium_and_hard_first_and_never_over_total(self):
        pool = ([entry(f"9MA0-01_2019-06_Q{n:02d}", "Proof", "1.1", 4, "easy") for n in range(1, 6)]
                + [entry(f"9MA0-01_2019-06_Q{n:02d}", "Proof", "1.1", 4, "hard") for n in range(6, 9)])
        picked = pick(pool, 14, random.Random(0))
        self.assertLessEqual(sum(e["marks"] for e in picked), 14)
        self.assertEqual(sum(e["difficulty"] == "hard" for e in picked), 3)
        self.assertEqual([e["id"] for e in picked], sorted(e["id"] for e in picked))


class RetestTests(unittest.TestCase):
    def attempt(self, day, question_id, awarded, total):
        return {"date": date(2026, *day), "question_id": question_id, "topic": "Proof",
                "marks_awarded": awarded, "marks_total": total, "error_type": "slip" if awarded < total else ""}

    def test_due_retests_soonest_first_each_once_including_variants(self):
        entries = [entry(f"9MA0-01_2019-06_Q0{n}", "Proof", "1.1") for n in (1, 2, 3)]
        attempts = [self.attempt((9, 20), "9MA0-01_2019-06_Q02", 1, 3),    # 7-day due 27 Sep, 21-day due today
                    self.attempt((10, 1), "9MA0-01_2019-06_Q01-A", 1, 3),  # variant: re-test its real question
                    self.attempt((10, 8), "9MA0-01_2019-06_Q03", 1, 3)]    # not due until 15 Oct
        retests = due_retests(attempts, entries, date(2026, 10, 11))
        self.assertEqual([e["id"] for e in retests], ["9MA0-01_2019-06_Q02", "9MA0-01_2019-06_Q01"])

    def test_retests_go_in_first_even_if_attempted_recently(self):
        retest = entry("9MA0-01_2019-06_Q09", "Proof", "1.1", 5, "easy")
        others = [entry(f"9MA0-01_2019-06_Q0{n}", "Proof", "1.1", 4, "hard") for n in range(1, 4)]
        picked = pick(others, 13, random.Random(0), [retest])
        self.assertIn(retest, picked)
        self.assertEqual(sum(e["marks"] for e in picked), 13)
        self.assertEqual(len(picked), len(set(e["id"] for e in picked)))

    def test_retests_that_do_not_fit_are_skipped(self):
        big = entry("9MA0-01_2019-06_Q09", "Proof", "1.1", 20)
        self.assertNotIn(big, pick([], 10, random.Random(0), [big]))


if __name__ == "__main__":
    unittest.main()
