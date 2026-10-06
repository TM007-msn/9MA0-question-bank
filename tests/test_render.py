"""Tests for validate.py's KaTeX render check (scripts/katex_check.mjs).

Skipped when Node or the KaTeX package isn't installed (run `npm install`).

Run from the project root:
    python -m unittest discover tests
"""

import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate import latex_strings, render_errors  # noqa: E402


@unittest.skipUnless(shutil.which("node") and (ROOT / "node_modules" / "katex").is_dir(), "KaTeX not installed")
class RenderTests(unittest.TestCase):
    def errors(self, text):
        return render_errors({"t": text})

    def test_good_latex_renders(self):
        self.assertEqual(self.errors(r"Find $\int x^2\,\mathrm{d}x$ and $$\frac{1}{2}$$ at $35^\circ$C"), [])
        self.assertEqual(self.errors(r"their $y-13=\text{“}20\text{”}(x-2)$"), [])

    def test_umlaut_quote_command_fails(self):
        self.assertTrue(self.errors(r'their $y-13=\text{\"}20\text{\"}(x-2)$'))

    def test_degree_superscript_with_no_base_fails(self):
        self.assertTrue(self.errors(r"$7.6\,^\circ\text{C}$"))

    def test_unclosed_dollar_fails(self):
        self.assertTrue(any("unclosed" in e for e in self.errors("open $x+1")))

    def test_latex_strings_finds_nested_maths(self):
        found = latex_strings({"a": "no maths", "b": ["$x$", {"c": "$y$"}]}, "e")
        self.assertEqual(found, {"e.b[0]": "$x$", "e.b[1].c": "$y$"})


if __name__ == "__main__":
    unittest.main()
