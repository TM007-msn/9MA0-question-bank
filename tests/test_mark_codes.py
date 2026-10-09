import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from mark_codes import main_marks, mark_value  # noqa: E402


class MarkValueTests(unittest.TestCase):
    def test_single_mark_codes(self):
        for code in ["M1", "A1", "B1", "dM1", "ddM1", "dB1", "A1*", "A1ft", "B1ft", "A1 cso", "B1cso*"]:
            self.assertEqual(mark_value(f"{code} (AO 1.1b): x"), 1, code)

    def test_multi_mark_codes_count_their_value(self):
        self.assertEqual(mark_value("B2 (AO 3.5b): any two valid reasons"), 2)
        self.assertEqual(mark_value("M2 (AO 2.1): x"), 2)
        self.assertEqual(mark_value("A2 (AO 1.1b): x"), 2)

    def test_line_without_code_is_refused(self):
        with self.assertRaises(ValueError):
            mark_value("[second mark of the B2 above]")

    def test_alt_lines_do_not_count(self):
        ms = ["M1 (AO 1.1b): a", "B2 (AO 3.5b): b", "ALT: Way 2 — M1 (AO 1.1b): c"]
        self.assertEqual(main_marks(ms), 3)
        self.assertEqual(main_marks(None), 0)

    def test_every_bank_entry_matches_its_marks(self):
        bank = json.loads((ROOT / "bank" / "questions.json").read_text(encoding="utf-8"))
        wrong = [e["id"] for e in bank if e["mark_scheme"] is not None and main_marks(e["mark_scheme"]) != e["marks"]]
        self.assertEqual(wrong, [])


if __name__ == "__main__":
    unittest.main()
