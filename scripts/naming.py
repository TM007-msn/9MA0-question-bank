"""File and id naming rules, in one place.

The JSON Schemas in schemas/ repeat these patterns, because a schema cannot
import Python. tests/test_naming.py checks that the two copies agree.
"""

import re

# Qualification + paper: A level (9MA0) has three papers, AS (8MA0) has two.
PAPER = r"(9MA0-0[1-3]|8MA0-0[12])"

# Exam series: year-month (e.g. 2023-06), or SAM for sample assessment materials.
SERIES = r"([0-9]{4}-(0[1-9]|1[0-2])|SAM)"

# Question part: Q + number, then an optional letter, then an optional roman
# numeral from i to x. So Q7, Q07, Q07b and Q07bii are all valid.
# "vi{0,3}" covers v, vi, vii and viii; "i{1,3}" covers i, ii and iii.
PART = r"Q[0-9]{1,2}([a-z](i{1,3}|iv|vi{0,3}|ix|x)?)?"

# The three document types, and which source/ folder each one lives in.
TYPE_FOLDERS = {
    "QP": "papers",
    "MS": "mark-schemes",
    "ER": "examiner-reports",
}

QUESTION_ID_RE = re.compile(rf"^{PAPER}_{SERIES}_{PART}$")
GENERATED_ID_RE = re.compile(rf"^{PAPER}_{SERIES}_{PART}-[ABC]$")
FILENAME_RE = re.compile(rf"^(?P<paper>{PAPER})_(?P<series>{SERIES})_(?P<type>QP|MS|ER)\.pdf$")


def id_prefix(paper, series):
    """The start every question id must have for the given paper and series."""
    return f"{paper}_{series}_Q"
