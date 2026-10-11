"""Tests for build_pdf.py: bank text to LaTeX, labels, log parsing, page crops.

The compile tests are skipped when Tectonic isn't installed, and the crop
test when the source paper isn't downloaded (source/ is git-ignored).

Run from the project root:
    python -m unittest discover tests
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_pdf  # noqa: E402
from build_pdf import (bank_to_latex, log_problems, mark_point_latex, part_label,  # noqa: E402
                       split_maths, suggested_minutes, text_only_maths)


class SplitMathsTests(unittest.TestCase):
    def test_inline_and_display(self):
        self.assertEqual(split_maths("Find $x$ in\n$$x^2=4$$\nnow"),
                         [("text", "Find "), ("inline", "x"), ("text", " in\n"),
                          ("display", "x^2=4"), ("text", "\nnow")])

    def test_dollar_inside_braces_does_not_close(self):
        # The same rule as KaTeX auto-render.
        self.assertEqual(split_maths(r"$\text{a$b}$"), [("inline", r"\text{a$b}")])

    def test_unclosed_dollar_stays_text(self):
        self.assertEqual(split_maths("cost $5"), [("text", "cost $5")])


class BankToLatexTests(unittest.TestCase):
    def test_text_specials_are_escaped(self):
        self.assertEqual(bank_to_latex("50% & #1_a"), r"50\% \& \#1\_a")

    def test_maths_is_left_alone(self):
        self.assertEqual(bank_to_latex(r"$a\%b$"), r"\fitinline{a\%b}")

    def test_line_breaks_become_paragraphs(self):
        self.assertEqual(bank_to_latex("one\ntwo"), "one\\par\ntwo")

    def test_no_blank_paragraphs_around_displays(self):
        self.assertEqual(bank_to_latex("Find\n$$x$$\nnow"), r"Find\fitdisplay{x}now")

    def test_styled_words_in_maths_become_text(self):
        self.assertEqual(bank_to_latex(r"$\textbf{Depends on M1}$ only"), r"\textbf{Depends on M1} only")


class TextOnlyMathsTests(unittest.TestCase):
    def test_plain_wrappers(self):
        self.assertEqual(text_only_maths(r"\textbf{Note this}"), r"\textbf{Note this}")
        self.assertEqual(text_only_maths(r"\text{explicitly}"), "explicitly")

    def test_underline_goes_innermost_so_it_can_break(self):
        self.assertEqual(text_only_maths(r"\underline{\textbf{Must use it}}"), r"\textbf{\uline{Must use it}}")

    def test_real_maths_is_not_text(self):
        self.assertIsNone(text_only_maths(r"\textbf{a}+b"))
        self.assertIsNone(text_only_maths(r"\textbf{half \frac{1}{2}}"))
        self.assertIsNone(text_only_maths("x^2"))


class MarkPointTests(unittest.TestCase):
    def test_label_and_notes(self):
        is_alt, latex = mark_point_latex("M1 (AO 1.1b): Integrates $x^2$. Notes: Any correct power.")
        self.assertFalse(is_alt)
        self.assertEqual(latex, "\\mspoint{M1 (AO 1.1b)}{Integrates \\fitinline{x^2}.}\n"
                                "\\msnotes{Notes: Any correct power.}")

    def test_alt(self):
        is_alt, latex = mark_point_latex("ALT: Way 2 — A1 (AO 2.1): $x=3$")
        self.assertTrue(is_alt)
        self.assertEqual(latex, r"\mspoint{Way 2 — A1 (AO 2.1)}{\fitinline{x=3}}")

    def test_no_label(self):
        self.assertEqual(mark_point_latex("$x=3$ seen")[1], r"\mspoint{}{\fitinline{x=3} seen}")


class LabelTests(unittest.TestCase):
    def test_part_labels(self):
        self.assertEqual(part_label("9MA0-01_2019-06_Q05"), "5")
        self.assertEqual(part_label("9MA0-01_2019-06_Q05b"), "5(b)")
        self.assertEqual(part_label("9MA0-01_2019-06_Q07bii"), "7(b)(ii)")
        self.assertEqual(part_label("9MA0-02_SAM_Q06i"), "6(i)")
        self.assertEqual(part_label("8MA0-01_2021-10_Q12iia"), "12(ii)(a)")
        self.assertEqual(part_label("9MA0-01_2019-06_Q05b-A"), "5(b)")

    def test_suggested_minutes_rounds_up_without_float_error(self):
        self.assertEqual(suggested_minutes(50), 60)
        self.assertEqual(suggested_minutes(23), 28)
        self.assertEqual(suggested_minutes(5), 6)


class LogTests(unittest.TestCase):
    def test_problems_belong_to_last_marker(self):
        log = "\n".join([
            "@@ENTRY A",
            "Missing character: There is no あ in font lmroman10-regular!",
            "@@ENTRY B",
            "! Undefined control sequence.",
            "l.42 \\foo",
            "Overfull \\hbox (12.5pt too wide) in paragraph at lines 3--3",
            "Overfull \\hbox (1.0pt too wide) in paragraph at lines 4--4",
        ])
        problems = log_problems(log)
        self.assertEqual([(kind, entry) for kind, entry, _ in problems],
                         [("glyph", "A"), ("error", "B"), ("overfull", "B")])
        self.assertIn("l.42", problems[1][2])


class SourcePageTests(unittest.TestCase):
    def test_refuses_source_file_outside_papers(self):
        entry = {"id": "x", "source_file": "../mark-schemes/9MA0-01_2018-06_MS.pdf", "source_page": 1}
        with self.assertRaises(SystemExit):
            build_pdf.source_page_image(entry, Path(tempfile.gettempdir()))

    @unittest.skipUnless((build_pdf.PAPERS_DIR / "9MA0-01_2018-06_QP.pdf").exists(), "source paper not downloaded")
    def test_crop_starts_at_question_and_stops_before_answer_lines(self):
        import pymupdf
        with pymupdf.open(build_pdf.PAPERS_DIR / "9MA0-01_2018-06_QP.pdf") as doc:
            page = doc[11]  # Question 6 starts on page 12
            clip = build_pdf.question_clip(page, 6)
            number = page.search_for("6.")[0]
            self.assertLess(abs(clip.y0 - number.y0), 15)
            # The question text ends about half way down; the answer lines fill the rest.
            self.assertLess(clip.y1, page.rect.height * 0.7)


@unittest.skipUnless(shutil.which("tectonic"), "Tectonic not installed")
class CompileTests(unittest.TestCase):
    def compile(self, body):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        tex = folder / "t.tex"
        tex.write_text(build_pdf.fill_template("questions.tex", "t", "", body), encoding="utf-8")
        return build_pdf.compile_tex(tex)

    def test_bank_unicode_compiles_with_no_missing_glyphs(self):
        text = bank_to_latex("“quoted” ⩽ ⩾ ℝ ✓ ✗ £5 – 35°C\n$$\\begin{aligned}x&=1\\\\y&=2\\end{aligned}$$")
        ok, log, _ = self.compile("\\typeout{@@ENTRY t}\n" + text)
        self.assertTrue(ok)
        self.assertEqual(log_problems(log), [])

    def test_missing_glyph_is_reported(self):
        ok, log, _ = self.compile("\\typeout{@@ENTRY t}\nあ")
        self.assertIn(("glyph", "t"), [(kind, entry) for kind, entry, _ in log_problems(log)])


if __name__ == "__main__":
    unittest.main()
