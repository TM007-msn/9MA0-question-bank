"""Tests for add_entries.py's replace modes.

These only read the bank; nothing is saved.

Run from the project root:
    python -m unittest discover tests
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from add_entries import changes, check_draft  # noqa: E402

BANK = json.loads((ROOT / "bank" / "questions.json").read_text(encoding="utf-8"))
PROGRESS = json.loads((ROOT / "bank" / "progress.json").read_text(encoding="utf-8"))


def paper_with_status(status):
    """(paper, series) of a paper in the bank with this status, or None."""
    in_bank = {(e["paper"], e["series"]) for e in BANK}
    return next(((i["paper"], i["series"]) for i in PROGRESS["queue"]
                 if i["status"] == status and (i["paper"], i["series"]) in in_bank), None)


def entries(paper_series):
    return [dict(e) for e in BANK if (e["paper"], e["series"]) == paper_series]


class ChangesTests(unittest.TestCase):
    def test_lists_changed_fields_added_and_removed_ids(self):
        old = [{"id": "A", "difficulty": "medium", "marks": 2}, {"id": "B", "marks": 1}]
        new = [{"id": "A", "difficulty": "hard", "marks": 2}, {"id": "C", "marks": 1}]
        self.assertEqual(changes(old, new), {"added": ["C"], "removed": ["B"], "changed": ["A: difficulty"]})


class ReplaceModeTests(unittest.TestCase):
    def test_replace_approved_refuses_a_paper_in_review(self):
        target = paper_with_status("in_review")
        if target is None:
            self.skipTest("no paper in review")
        _, _, problems = check_draft(entries(target), replace="done")
        self.assertTrue(any("--replace-approved is only for papers that are done" in p for p in problems))

    def test_replace_refuses_a_done_paper(self):
        target = paper_with_status("done")
        if target is None:
            self.skipTest("no done paper")
        _, _, problems = check_draft(entries(target), replace="in_review")
        self.assertTrue(any("--replace is only for papers that are in_review" in p for p in problems))

    def test_replace_approved_still_runs_the_save_checks(self):
        target = paper_with_status("done")
        if target is None:
            self.skipTest("no done paper")
        draft = entries(target)
        draft[0]["marks"] += 1          # per-question totals no longer match the paper
        draft[0]["topic"] = "Not a topic"  # schema failure
        _, _, problems = check_draft(draft, replace="done")
        self.assertTrue(problems)

    def test_replace_approved_accepts_an_unchanged_done_paper(self):
        target = paper_with_status("done")
        if target is None:
            self.skipTest("no done paper")
        _, _, problems = check_draft(entries(target), replace="done")
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
