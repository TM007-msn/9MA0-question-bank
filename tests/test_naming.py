"""Tests for id and file naming.

Each id is checked against both the Python regex in scripts/naming.py and
the JSON Schema pattern, so the two copies can't drift apart unnoticed.

Run from the project root:
    python -m unittest discover tests
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from naming import FILENAME_RE, GENERATED_ID_RE, QUESTION_ID_RE  # noqa: E402

question_schema = json.loads((ROOT / "schemas" / "question.schema.json").read_text(encoding="utf-8"))
SCHEMA_QUESTION_ID = re.compile(question_schema["$defs"]["question_id"]["pattern"])
SCHEMA_GENERATED_ID = re.compile(question_schema["$defs"]["generated_id"]["pattern"])

VALID_QUESTION_IDS = [
    "9MA0-01_2023-06_Q07bii",  # multi-level part
    "9MA0-02_SAM_Q03a",        # sample assessment materials
    "9MA0-03_2019-06_Q12",
    "9MA0-01_2022-10_Q7",
    "8MA0-01_2023-06_Q05c",    # AS
    "8MA0-02_SAM_Q01aiv",
    "9MA0-01_2023-06_Q04aviii",
    "9MA0-31_2022-06_Q03a",    # Paper 3 Statistics
    "9MA0-32_2019-06_Q05",     # Paper 3 Mechanics
    "9MA0-01_SPEC_Q02b",       # specimen set
    "8MA0-21_2023-06_Q02",     # AS Paper 2 Statistics
    "8MA0-22_SPEC_Q01a",       # AS Paper 2 Mechanics
]

INVALID_QUESTION_IDS = [
    "9MA0-04_2023-06_Q01",     # no paper 4
    "8MA0-03_2023-06_Q01",     # AS has only 2 papers
    "7MA0-01_2023-06_Q01",     # unknown qualification
    "9MA0-01_2023-13_Q01",     # month 13
    "9MA0-01_sam_Q01",         # SAM must be upper case
    "9MA0-01_2023-06_Q07bxi",  # roman numerals stop at x
    "9MA0-01_2023-06_Q07biiii",
    "9MA0-01_2023-06_Q07B",
    "9MA0-01_2023-06_Q123",
    "9MA0-01_2023-06",
    "9MA0-33_2022-06_Q01",     # only 31 and 32 exist
    "8MA0-31_2022-06_Q01",     # AS has no Paper 3
    "8MA0-23_2022-06_Q01",     # only 21 and 22 exist
    "9MA0-21_2022-06_Q01",     # 21/22 are AS-only
    "9MA0-01_Spec_Q01",        # SPEC must be upper case
]

VALID_FILENAMES = [
    "9MA0-01_2023-06_QP.pdf",
    "9MA0-01_SAM_QP.pdf",
    "8MA0-02_2022-06_MS.pdf",
    "9MA0-03_2019-06_ER.pdf",
    "9MA0-31_2022-06_QP.pdf",
    "9MA0-32_2021-10_MS.pdf",
    "9MA0-02_SPEC_MS.pdf",
    "8MA0-21_2020-10_ER.pdf",
]

INVALID_FILENAMES = [
    "9MA0-01_2023-06_qp.pdf",
    "9MA0-01_2023_QP.pdf",
    "8MA0-03_SAM_QP.pdf",
    "9MA0-01_SAM_XX.pdf",
    "9MA0-01_SAM_QP.PDF",
]


class QuestionIdTests(unittest.TestCase):
    def test_valid_ids(self):
        for qid in VALID_QUESTION_IDS:
            with self.subTest(qid=qid):
                self.assertRegex(qid, QUESTION_ID_RE)
                self.assertRegex(qid, SCHEMA_QUESTION_ID)

    def test_invalid_ids(self):
        for qid in INVALID_QUESTION_IDS:
            with self.subTest(qid=qid):
                self.assertNotRegex(qid, QUESTION_ID_RE)
                self.assertNotRegex(qid, SCHEMA_QUESTION_ID)

    def test_generated_ids(self):
        for qid in VALID_QUESTION_IDS:
            for variant in "ABC":
                with self.subTest(qid=qid, variant=variant):
                    gid = f"{qid}-{variant}"
                    self.assertRegex(gid, GENERATED_ID_RE)
                    self.assertRegex(gid, SCHEMA_GENERATED_ID)
            with self.subTest(qid=qid, variant="D"):
                self.assertNotRegex(f"{qid}-D", GENERATED_ID_RE)
                self.assertNotRegex(f"{qid}-D", SCHEMA_GENERATED_ID)


class FilenameTests(unittest.TestCase):
    def test_valid_filenames(self):
        for name in VALID_FILENAMES:
            with self.subTest(name=name):
                self.assertRegex(name, FILENAME_RE)

    def test_invalid_filenames(self):
        for name in INVALID_FILENAMES:
            with self.subTest(name=name):
                self.assertNotRegex(name, FILENAME_RE)


class OutDirTests(unittest.TestCase):
    def test_ensure_out_dir_creates_missing_folder(self):
        import tempfile

        import paths

        with tempfile.TemporaryDirectory() as tmp:
            original = paths.OUT_DIR
            paths.OUT_DIR = Path(tmp) / "out"
            try:
                created = paths.ensure_out_dir("to-remarkable")
                self.assertTrue(created.is_dir())
                # Calling again on an existing folder must not fail.
                paths.ensure_out_dir("to-remarkable")
            finally:
                paths.OUT_DIR = original


if __name__ == "__main__":
    unittest.main()
