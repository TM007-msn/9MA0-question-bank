"""Tests for check_marks.py, including hand-read totals and mark-scheme corrections.

These read the local source PDFs (git-ignored), so they are skipped when the
PDFs aren't present.

Run from the project root:
    python -m unittest discover tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_marks  # noqa: E402

SAM_QP = check_marks.PAPERS_DIR / "8MA0-01_SAM_QP.pdf"
HAVE_SOURCES = SAM_QP.exists() and (check_marks.PAPERS_DIR / "8MA0-01_2018-06_QP.pdf").exists()

# Result of `check_marks.py --all` for every pair. Adding the hand-read totals
# for an unreadable text layer and the mark-scheme corrections changed only
# 8MA0-01 SAM (UNCHECKED -> ok); every other pair is as it was before.
EXPECTED = {
    ("8MA0-01", "2018-06"): "ok",
    ("8MA0-01", "2019-06"): "ok",
    ("8MA0-01", "2020-10"): "ok",
    ("8MA0-01", "2021-10"): "ok",
    ("8MA0-01", "2022-06"): "ok",
    ("8MA0-01", "2023-06"): "ok",
    ("8MA0-01", "2024-06"): "ok",
    ("8MA0-01", "SAM"): "ok",
    ("8MA0-01", "SPEC"): "ok",
    ("8MA0-02", "2018-06"): "UNCHECKED",
    ("8MA0-02", "SAM"): "ok",
    ("8MA0-02", "SPEC"): "UNCHECKED",
    ("8MA0-21", "2019-06"): "ok",
    ("8MA0-21", "2020-10"): "UNCHECKED",
    ("8MA0-21", "2021-10"): "UNCHECKED",
    ("8MA0-21", "2022-06"): "UNCHECKED",
    ("8MA0-21", "2023-06"): "ok",
    ("8MA0-21", "2024-06"): "UNCHECKED",
    ("8MA0-22", "2019-06"): "UNCHECKED",
    ("8MA0-22", "2020-10"): "ok",
    ("8MA0-22", "2021-10"): "ok",
    ("8MA0-22", "2022-06"): "UNCHECKED",
    ("8MA0-22", "2023-06"): "ok",
    ("8MA0-22", "2024-06"): "UNCHECKED",
    ("9MA0-01", "2018-06"): "ok",  # "Scheme for Substitution" headings (Q13)
    ("9MA0-01", "2019-06"): "ok",  # PMT footer, "(11marks)", Q10 total recorded in ms_corrections.json
    ("9MA0-01", "2020-10"): "ok",
    ("9MA0-01", "2021-10"): "ok",
    ("9MA0-01", "2022-06"): "ok",
    ("9MA0-01", "SAM"): "ok",  # unreadable text layer; QP totals read by hand
    ("9MA0-01", "SPEC"): "ok",
    ("9MA0-02", "2018-06"): "UNCHECKED",
    ("9MA0-02", "2019-06"): "ok",
    ("9MA0-02", "2020-10"): "UNCHECKED",
    ("9MA0-02", "2021-10"): "ok",
    ("9MA0-02", "2022-06"): "ok",
    ("9MA0-02", "SAM"): "UNCHECKED",
    ("9MA0-02", "SPEC"): "ok",
    ("9MA0-03", "2018-06"): "UNCHECKED",
    ("9MA0-03", "SAM"): "UNCHECKED",
    ("9MA0-03", "SPEC"): "UNCHECKED",
    ("9MA0-31", "2019-06"): "ok",
    ("9MA0-31", "2020-10"): "UNCHECKED",
    ("9MA0-31", "2021-10"): "UNCHECKED",
    ("9MA0-31", "2022-06"): "UNCHECKED",
    ("9MA0-32", "2019-06"): "UNCHECKED",
    ("9MA0-32", "2020-10"): "ok",
    ("9MA0-32", "2021-10"): "UNCHECKED",
    ("9MA0-32", "2022-06"): "ok",
}


class HeaderPatternTests(unittest.TestCase):
    def test_scheme_heading_may_name_the_method(self):
        for heading in ["Question \nScheme \nMarks \nAOs \n13 ",
                        "Question \nScheme for Substitution  \nMarks \nAOs \n13 ",
                        "Question \nAlt \nScheme for by parts \nMarks \nAOs \n13 "]:
            match = check_marks.MS_HEADER_RE.search(heading)
            self.assertIsNotNone(match, heading)
            self.assertEqual(match.group(1), "13")

    def test_page_footer_between_headings_and_label(self):
        match = check_marks.MS_HEADER_RE.search("Question \nScheme \nMarks \nAOs \nPMT\n\n4 (a) \n")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "4")

    def test_total_may_have_no_space(self):
        for text in ["(11marks)", "(11 marks)", "( 7 marks )"]:
            match = check_marks.MS_TOTAL_RE.search(text)
            self.assertIsNotNone(match, text)
        self.assertIsNone(check_marks.MS_TOTAL_RE.search("scores 0 marks in total"))


@unittest.skipUnless(HAVE_SOURCES, "source PDFs not present")
class AllPairsTests(unittest.TestCase):
    def test_every_pair_matches_the_recorded_result(self):
        found = {pair: check_marks.compare(*pair)[0] for pair in check_marks.all_pairs()}
        self.assertEqual(found, EXPECTED)


@unittest.skipUnless(HAVE_SOURCES, "source PDFs not present")
class OverrideTests(unittest.TestCase):
    """Each test points check_marks at temporary override files."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        real_manual = json.loads(check_marks.MANUAL_TOTALS.read_text(encoding="utf-8"))
        real_fixes = json.loads(check_marks.MS_CORRECTIONS.read_text(encoding="utf-8"))
        self.manual, self.fixes = real_manual, real_fixes

    def run_with(self, paper="8MA0-01", series="SAM"):
        manual = Path(self.dir.name) / "manual.json"
        fixes = Path(self.dir.name) / "fixes.json"
        manual.write_text(json.dumps(self.manual), encoding="utf-8")
        fixes.write_text(json.dumps(self.fixes), encoding="utf-8")
        with mock.patch.object(check_marks, "MANUAL_TOTALS", manual), \
                mock.patch.object(check_marks, "MS_CORRECTIONS", fixes):
            return check_marks.compare(paper, series), check_marks.overrides(paper, series)

    def sam(self):
        return self.manual["papers"]["8MA0-01_SAM_QP.pdf"]

    def test_recorded_overrides_make_the_sam_ok_and_are_listed(self):
        (status, problems), notes = self.run_with()
        self.assertEqual((status, problems), ("ok", []))
        self.assertTrue(any("unreadable text layer" in n for n in notes))
        self.assertTrue(any("MS correction Q1" in n and "MS page 1" in n for n in notes))
        self.assertTrue(any("MS correction Q14" in n and "MS page 13" in n for n in notes))

    def test_omitted_rows_are_listed_without_changing_the_result(self):
        (status, problems), notes = self.run_with("8MA0-01", "SPEC")
        self.assertEqual((status, problems), ("ok", []))
        self.assertTrue(any("MS row left out, Q13(c)" in n and "MS page 13" in n for n in notes))
        del self.fixes["papers"]["8MA0-01_SPEC_MS.pdf"]
        (status_without, _), notes_without = self.run_with("8MA0-01", "SPEC")
        self.assertEqual(status_without, "ok")
        self.assertEqual(notes_without, [])

    def test_hand_read_totals_must_add_up_to_the_paper_total(self):
        self.sam()["totals"]["17"] = 9
        (status, problems), _ = self.run_with()
        self.assertNotEqual(status, "ok")
        self.assertTrue(any("not the paper total 100" in p for p in problems))

    def test_hand_read_totals_need_a_paper_total(self):
        del self.sam()["paper_total"]
        (status, problems), _ = self.run_with()
        self.assertNotEqual(status, "ok")
        self.assertTrue(any("no paper_total" in p for p in problems))

    def test_without_the_correction_q1_is_a_mismatch(self):
        del self.fixes["papers"]["8MA0-01_SAM_MS.pdf"]["corrections"]["1"]
        (status, problems), _ = self.run_with()
        self.assertEqual(status, "MISMATCH")
        self.assertIn("Q1: QP says 3, MS says [7]", problems)

    def test_a_stale_correction_is_reported_not_applied(self):
        self.fixes["papers"]["8MA0-01_SAM_MS.pdf"]["corrections"]["1"]["printed"] = 6
        (status, problems), _ = self.run_with()
        self.assertNotEqual(status, "ok")
        self.assertTrue(any("expects the printed total to read 6" in p for p in problems))

    def test_unreadable_flag_never_overrides_a_readable_paper(self):
        # Hand-read totals recorded for a paper whose PDF text is readable are ignored.
        self.manual["papers"]["8MA0-01_2018-06_QP.pdf"] = {
            "totals": {"1": 99}, "paper_total": 99, "text_layer": "unreadable", "read_from": "test"}
        (status, problems), notes = self.run_with("8MA0-01", "2018-06")
        self.assertEqual((status, problems), ("ok", []))
        self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
