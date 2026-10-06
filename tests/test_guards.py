"""Tests for the mock-papers guards: the folder setting, where reserved
series are filed, the page renderer's refusal, and the shell-command hook.

Nothing here opens or lists the mock-papers folder; paths under it are only
built and compared.

Run from the project root:
    python -m unittest discover tests
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from fetch_materials import RESERVED_SERIES, SOURCE_DIR, build_plan  # noqa: E402
from paths import RESERVED_DIR  # noqa: E402

HOOK = ROOT / ".claude" / "hooks" / "guard_mock_papers.py"


def run_hook(tool_name, command):
    payload = json.dumps({"tool_name": tool_name, "tool_input": {"command": command}})
    return subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True)


class FolderTests(unittest.TestCase):
    def test_mock_papers_live_outside_the_project(self):
        self.assertNotIn(ROOT.resolve(), RESERVED_DIR.resolve().parents)
        self.assertFalse((ROOT / "source" / "reserved").exists())

    def test_reserved_series_are_filed_in_the_mock_folder(self):
        qual = "9MA0"
        series = sorted(RESERVED_SERIES[qual])[0]
        pmt = {(qual, "01", series, "QP"): "https://example.invalid/a.pdf",
               (qual, "01", "2019-06", "QP"): "https://example.invalid/b.pdf"}
        planned, _ = build_plan(pmt, {}, {})
        dest = {p["series"]: p["dest"] for p in planned if p["type"] == "QP" and p["paper"] == "9MA0-01"}
        self.assertEqual(dest[series].parent, RESERVED_DIR)
        self.assertEqual(dest["2019-06"].parent, SOURCE_DIR / "papers")


class RendererTests(unittest.TestCase):
    def test_refuses_the_mock_folder(self):
        # The file doesn't need to exist: the refusal happens before opening.
        target = RESERVED_DIR / "anything.pdf"
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_pages.py"), str(target), "1"],
                                capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 1)
        self.assertIn("never opened", result.stderr)


class HookTests(unittest.TestCase):
    def test_blocks_bash_command_naming_the_folder(self):
        self.assertEqual(run_hook("Bash", "ls ~/9MA0-reserved").returncode, 2)

    def test_blocks_powershell_any_case(self):
        self.assertEqual(run_hook("PowerShell", r"Get-ChildItem C:\Users\taylo\9MA0-RESERVED").returncode, 2)

    def test_blocks_upper_and_title_case_in_both_shells(self):
        for word in ("RESERVED", "Reserved"):
            for tool in ("Bash", "PowerShell"):
                with self.subTest(word=word, tool=tool):
                    result = run_hook(tool, f"echo {word}-hook-test")
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("Blocked", result.stderr)

    def test_allows_other_commands(self):
        self.assertEqual(run_hook("Bash", "git status").returncode, 0)

    def test_malformed_payload_is_judged_on_raw_text(self):
        result = subprocess.run([sys.executable, str(HOOK)], input="not json reserved",
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
