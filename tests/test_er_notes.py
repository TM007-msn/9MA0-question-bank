"""Tests for er_notes.py: tagging report sentences onto entries.

Run from the project root:
    python -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report  # noqa: E402


def entries(*tails):
    return [{"id": f"8MA0-01_2021-10_Q{t}", "examiner_notes": None} for t in tails]


class NoteTests(unittest.TestCase):
    def test_sic_note_follows_its_sentence_verbatim(self):
        es = entries("04a", "04b")
        apply_report(es, {"04": [
            (None, "Generally well answered."),
            ({"b"}, "Some forgot to divide by 9.", {"note": "the mark scheme divides by 4"}),
        ]})
        self.assertEqual(es[1]["examiner_notes"],
                         "Generally well answered. Some forgot to divide by 9. [sic: the mark scheme divides by 4]")
        self.assertEqual(es[0]["examiner_notes"], "Generally well answered.")

    def test_note_travels_with_a_referred_to_sentence(self):
        es = entries("04a", "04b")
        apply_report(es, {"04": [
            ({"a"}, "Some divided by 9.", {"note": "it is 4"}),
            ({"b"}, "This cost them the mark.", {"ref": True}),
        ]})
        self.assertEqual(es[1]["examiner_notes"], "Some divided by 9. [sic: it is 4] This cost them the mark.")

    def test_bad_notes_are_refused(self):
        for note in ("", "  ", "[already bracketed]", 4):
            with self.subTest(note=note):
                with self.assertRaises(ValueError):
                    apply_report(entries("04a"), {"04": [({"a"}, "Some divided by 9.", {"note": note})]})


if __name__ == "__main__":
    unittest.main()
