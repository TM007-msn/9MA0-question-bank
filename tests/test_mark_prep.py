"""Tests for mark_prep.py: finding the returned PDF, its set, and each part's pages.

Run from the project root:
    python -m unittest discover tests
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from mark_prep import load_set, newest_pdf, part_pages, set_name  # noqa: E402


class NameTests(unittest.TestCase):
    def test_returned_names_match_the_set(self):
        for file, name in [("test-five_questions.pdf", "test-five"),
                           ("test-five_questions (1).pdf", "test-five"),
                           ("test-five_questions(2).pdf", "test-five"),
                           ("test-five.pdf", "test-five"),
                           ("quick-2026-10-11_questions.pdf", "quick-2026-10-11")]:
            self.assertEqual(set_name(Path(file)), name, file)

    def test_mark_scheme_refused(self):
        with self.assertRaises(SystemExit):
            set_name(Path("test-five_markscheme.pdf"))

    def test_unknown_set_lists_the_known_ones(self):
        folder = Path(tempfile.mkdtemp())
        (folder / "test-five.json").write_text("[]", encoding="utf-8")
        with self.assertRaises(SystemExit) as caught:
            load_set("nope", folder)
        self.assertIn("test-five", str(caught.exception))


class NewestTests(unittest.TestCase):
    def test_newest_by_modified_time(self):
        folder = Path(tempfile.mkdtemp())
        old, new = folder / "b.pdf", folder / "a.pdf"
        old.write_bytes(b"")
        new.write_bytes(b"")
        os.utime(old, (1_000_000, 1_000_000))
        os.utime(new, (2_000_000, 2_000_000))
        (folder / ".gitkeep").write_bytes(b"")
        self.assertEqual(newest_pdf(folder), new)

    def test_empty_folder(self):
        with self.assertRaises(SystemExit):
            newest_pdf(Path(tempfile.mkdtemp()))


class PageTests(unittest.TestCase):
    IDS = ["A_Q01", "B_Q02", "C_Q03"]

    def test_runs_to_the_page_the_next_part_starts(self):
        texts = ["1 A_Q01 ...", "working", "2 B_Q02 ... 3 C_Q03", "more"]
        self.assertEqual(part_pages(texts, self.IDS),
                         {"A_Q01": [1, 2, 3], "B_Q02": [3], "C_Q03": [3, 4]})

    def test_missing_id_means_every_page(self):
        texts = ["1 A_Q01", "3 C_Q03"]
        pages = part_pages(texts, self.IDS)
        self.assertIsNone(pages["B_Q02"])
        # A_Q01 runs to the next part that was found.
        self.assertEqual(pages["A_Q01"], [1, 2])


if __name__ == "__main__":
    unittest.main()
