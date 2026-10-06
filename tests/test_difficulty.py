"""Tests for the examiner-report difficulty mapping (scripts/difficulty.py).

Run from the project root:
    python -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from difficulty import classify, difficulty  # noqa: E402


class ClassifyTests(unittest.TestCase):
    def test_easy(self):
        self.assertEqual(classify(["This question was very accessible."])[0], "easy")

    def test_hard(self):
        self.assertEqual(classify(["This proved to be a very demanding question."])[0], "hard")

    def test_medium_phrase(self):
        self.assertEqual(classify(["Some candidates found the root."])[0], "medium")

    def test_easy_and_hard_is_medium(self):
        self.assertEqual(classify(["Overall well done, but few candidates found both roots."])[0], "medium")

    def test_a_few_is_not_few(self):
        self.assertIsNone(classify(["A few students used x = 2."])[0])

    def test_less_well_done_is_hard_not_easy(self):
        level, hits = classify(["Tying the two parts together was less well done."])
        self.assertEqual(level, "hard")
        self.assertFalse(hits["easy"])

    def test_no_phrases_is_none(self):
        self.assertIsNone(classify(["Students substituted x = 4."])[0])


class DifficultyTests(unittest.TestCase):
    def test_part_sentences_win_over_whole_question(self):
        level, basis = difficulty(["Part (b) was well answered."], ["This proved to be a challenge."])
        self.assertEqual((level, basis["from"]), ("easy", "part"))

    def test_falls_back_to_whole_question(self):
        level, basis = difficulty(["Students substituted x = 4."], ["This proved to be a challenge."])
        self.assertEqual((level, basis["from"]), ("hard", "whole question"))

    def test_nothing_is_null(self):
        self.assertEqual(difficulty(["Students substituted x = 4."], [])[0], None)


class MappingDocumentedTests(unittest.TestCase):
    def test_claude_md_lists_match_code(self):
        from difficulty import EASY, HARD, MEDIUM
        text = (Path(__file__).resolve().parent.parent / "CLAUDE.md").read_text(encoding="utf-8")
        for level, phrases in (("easy", EASY), ("medium", MEDIUM), ("hard", HARD)):
            line = next(l for l in text.splitlines() if l.startswith(f"- **{level}:**"))
            documented = [p.strip(" “”") for p in line.split(":**", 1)[1].split(",")]
            self.assertEqual(documented, phrases, level)


if __name__ == "__main__":
    unittest.main()
