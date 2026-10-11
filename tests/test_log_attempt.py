"""Tests for log_attempt.py's checks. Only temporary files are written.

Run from the project root:
    python -m unittest discover tests
"""

import shutil
import sys
import tempfile
import unittest
import unittest.mock
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from log_attempt import (append_rows, ask_rows, check_row, check_rows, parse_pasted,  # noqa: E402
                         read_attempts)

TODAY = date(2026, 10, 11)
BANK = {"9MA0-01_2019-06_Q05c": {"topic": "Algebra and functions", "marks": 4},
        "9MA0-01_2019-06_Q05c-A": {"topic": "Algebra and functions", "marks": 4}}


def raw(**fields):
    base = {"date": "2026-10-10", "question_id": "9MA0-01_2019-06_Q05c", "topic": "",
            "marks_awarded": "2", "marks_total": "4", "error_type": "slip"}
    return {**base, **fields}


class CheckRowTests(unittest.TestCase):
    def problems(self, **fields):
        return check_row(raw(**fields), BANK, TODAY)[1]

    def test_good_row_gets_its_topic_from_the_bank(self):
        row, problems = check_row(raw(), BANK, TODAY)
        self.assertEqual(problems, [])
        self.assertEqual(row["topic"], "Algebra and functions")

    def test_generated_ids_are_accepted(self):
        self.assertEqual(self.problems(question_id="9MA0-01_2019-06_Q05c-A"), [])

    def test_blank_date_is_today(self):
        self.assertEqual(check_row(raw(date=""), BANK, TODAY)[0]["date"], "2026-10-11")

    def test_each_check(self):
        cases = {
            "not in questions.json": {"question_id": "9MA0-01_2019-06_Q99"},
            "between 0 and marks_total": {"marks_awarded": "5", "error_type": ""},
            "is not 9MA0-01_2019-06_Q05c's 4 marks": {"marks_total": "5"},
            "must be one of": {"error_type": "careless"},
            "leave it blank": {"marks_awarded": "4", "error_type": "slip"},
            "not whole numbers": {"marks_awarded": "two"},
            "in the future": {"date": "2026-10-12"},
            "not YYYY-MM-DD": {"date": "10/10/2026"},
            "is not 9MA0-01_2019-06_Q05c's topic": {"topic": "Integration"},
        }
        for message, fields in cases.items():
            with self.subTest(message):
                self.assertTrue(any(message in p for p in self.problems(**fields)), self.problems(**fields))

    def test_full_marks_need_no_error_type(self):
        self.assertEqual(self.problems(marks_awarded="4", error_type=""), [])


class PastedTests(unittest.TestCase):
    def test_header_and_blank_lines_are_skipped(self):
        text = ("date,question_id,topic,marks_awarded,marks_total,error_type\n\n"
                "2026-10-10,9MA0-01_2019-06_Q05c,,2,4,slip\n")
        self.assertEqual(parse_pasted(text), [raw()])

    def test_wrong_column_count_is_a_problem(self):
        rows, problems = check_rows(parse_pasted("2026-10-10,9MA0-01_2019-06_Q05c,2,4\n"), BANK, TODAY)
        self.assertEqual(rows, [])
        self.assertIn("4 columns", problems[0])


class FileTests(unittest.TestCase):
    def setUp(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        self.path = folder / "attempts.csv"

    def test_new_file_gets_a_header_and_rows_read_back(self):
        row, _ = check_row(raw(), BANK, TODAY)
        append_rows([row], self.path)
        append_rows([row], self.path)
        lines = self.path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "date,question_id,topic,marks_awarded,marks_total,error_type")
        self.assertEqual(len(lines), 3)
        back = read_attempts(self.path)
        self.assertEqual((back[0]["date"], back[0]["marks_awarded"]), (date(2026, 10, 10), 2))

    def test_file_without_final_newline_is_appended_to_cleanly(self):
        self.path.write_text("date,question_id,topic,marks_awarded,marks_total,error_type", encoding="utf-8")
        append_rows([check_row(raw(), BANK, TODAY)[0]], self.path)
        self.assertEqual(len(read_attempts(self.path)), 1)


class InteractiveTests(unittest.TestCase):
    def test_asks_until_blank_and_skips_bad_answers(self):
        answers = iter(["9MA0-01_2019-06_Q99",                      # unknown id: asked again
                        "9MA0-01_2019-06_Q05c", "2", "careless", "",  # bad error type: not added
                        "9MA0-01_2019-06_Q05c", "2", "slip", "",      # good
                        "9MA0-01_2019-06_Q05c", "4", "2026-10-01",    # full marks: no error type asked
                        ""])
        with unittest.mock.patch("builtins.print"):
            rows = ask_rows(BANK, TODAY, ask=lambda prompt: next(answers))
        self.assertEqual([(r["marks_awarded"], r["error_type"], r["date"]) for r in rows],
                         [("2", "slip", "2026-10-11"), ("4", "", "2026-10-01")])


if __name__ == "__main__":
    unittest.main()
