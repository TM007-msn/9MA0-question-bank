"""Check that a mark scheme belongs to its question paper.

Compares the marks per question printed in the question paper ("Total for
Question 3 is 7 marks") with the per-question totals in the mark scheme
("(7 marks)"). A mismatch usually means the mark scheme is for a different
paper or series. Run this before saving any bank entries for a paper.

Usage (from the project root, with the venv active):
    python scripts/check_marks.py 8MA0-01 2018-06    # one paper
    python scripts/check_marks.py --all              # every pair in papers/ + mark-schemes/

Only source/papers/ and source/mark-schemes/ are read; the mock papers
(outside the project) are never touched.

Each pair gets one of three results:
  ok         every question's total was read from both files and they agree
  MISMATCH   at least one question's total was read cleanly from both files
             and they differ: the mark scheme is probably for another paper
  UNCHECKED  the layout couldn't be read well enough to compare every
             question; check by hand or improve the parser before trusting it
Exit code is 0 only if every pair is ok.
"""

import argparse
import json
import re
import sys

import pymupdf

from naming import FILENAME_RE
from paths import ROOT

PAPERS_DIR = ROOT / "source" / "papers"
MARK_SCHEMES_DIR = ROOT / "source" / "mark-schemes"

QP_TOTAL_RE = re.compile(r"Total\s+for\s+Question\s+(\d+)\s+is\s+(\d+)\s+marks?", re.IGNORECASE)

# Each mark scheme table starts with the column headings, then the question
# label in the first cell, e.g. "Question\nScheme\nMarks\nAOs\n2(i)".
# Some tables leave the "Question" heading cell blank (8MA0-01 2019-06 Q13).
MS_HEADER_RE = re.compile(r"(?:Question\s*\n\s*)?Scheme\s*\n\s*Marks\s*\n\s*AOs\s*\n\s*(\d+)")
# Some questions open with a page of notes headed just "Question 15" on its
# own line, before the scheme table (8MA0-01 2019-06 Q15). Lines such as
# "Notes on Question 4 continue" don't match because the line must hold
# nothing else.
MS_HEADING_RE = re.compile(r"^[ \t]*Question[ \t]+(\d+)[ \t]*$", re.MULTILINE)
# The total is usually "(7 marks)"; occasionally it is printed without
# brackets, as a line of its own ("4 marks"). The unbracketed form must be
# alone on its line so that notes like "scores 0 marks" aren't counted.
MS_TOTAL_RE = re.compile(r"\(\s*(\d+)\s+marks?\s*\)|^[ \t]*(\d+)[ \t]+marks?[ \t]*$",
                         re.IGNORECASE | re.MULTILINE)


def pdf_text(path):
    with pymupdf.open(path) as doc:
        return "\n".join(page.get_text() for page in doc)


MANUAL_TOTALS = ROOT / "bank" / "qp_totals_manual.json"
MS_CORRECTIONS = ROOT / "bank" / "ms_corrections.json"


def has_text_layer(path, min_chars_per_page=100):
    """False for scanned PDFs, whose pages are images with no extractable text.
    ('PMT' watermarks don't count as text.)"""
    with pymupdf.open(path) as doc:
        chars = sum(len(page.get_text().replace("PMT", "").strip()) for page in doc)
        return chars >= min_chars_per_page * doc.page_count / 10


def load_overrides(path, key="papers"):
    """{file name: entry} from a bank override file, or {} if it doesn't exist."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)[key]


def manual_entry(path):
    """The hand-read totals entry for this question paper, if it may be used.

    Hand-read totals never override totals read from the PDF itself. They are
    used only when the PDF has no text layer (a scan), or when the entry says
    the text layer is unreadable (fonts with no character mapping) and no
    "Total for Question" lines can be parsed from it.
    """
    entry = load_overrides(MANUAL_TOTALS).get(path.name)
    if not entry:
        return None
    if not has_text_layer(path):
        return entry
    if entry.get("text_layer") == "unreadable" and not QP_TOTAL_RE.search(pdf_text(path)):
        return entry
    return None


def manual_totals(path):
    """Hand-read totals {question: marks} for this question paper, or None."""
    entry = manual_entry(path)
    return {int(q): m for q, m in entry["totals"].items()} if entry else None


def manual_problems(path):
    """Problems with a hand-read totals entry: they must add up to the paper total."""
    entry = manual_entry(path)
    if not entry:
        return []
    added = sum(entry["totals"].values())
    if "paper_total" not in entry:
        return [f"hand-read totals for {path.name} have no paper_total to check against"]
    if added != entry["paper_total"]:
        return [f"hand-read totals for {path.name} add up to {added}, not the paper total {entry['paper_total']}"]
    return []


def qp_marks(path):
    """{question number: total marks} from the question paper.

    For a scan, or a paper whose text layer is recorded as unreadable, this
    falls back to the totals read by hand in bank/qp_totals_manual.json.
    """
    found = {int(q): int(m) for q, m in QP_TOTAL_RE.findall(pdf_text(path))}
    if not found:
        found = manual_totals(path) or {}
    return found


def ms_marks(path):
    """{question number: total marks} from the mark scheme.

    Walks through the text in order. Each "(N marks)" belongs to the most
    recent question header before it. Totals seen before the first header
    (the general marking instructions) are ignored.
    """
    text = pdf_text(path)
    events = [(m.start(), "header", int(m.group(1))) for m in MS_HEADER_RE.finditer(text)]
    events += [(m.start(), "header", int(m.group(1))) for m in MS_HEADING_RE.finditer(text)]
    # MS_TOTAL_RE has one group per form; whichever matched holds the number.
    events += [(m.start(), "total", int(m.group(1) or m.group(2))) for m in MS_TOTAL_RE.finditer(text)]
    events.sort()

    totals = {}
    current = None
    for _, kind, value in events:
        if kind == "header":
            current = value
        elif current is not None:
            # A question has one "(N marks)" line; if the notes repeat it,
            # a different number would show up as a conflict below.
            totals.setdefault(current, set()).add(value)
    return totals


def corrected_ms_marks(path):
    """(totals, problems): the mark scheme's totals with any recorded
    corrections applied (bank/ms_corrections.json).

    A correction states what the parser reads from the PDF ("printed": a
    number, or null when no total is printed) and the true total. It only
    applies while the PDF still reads that way; otherwise it is reported as a
    problem, so a stale or wrong correction can't hide a real mismatch.
    """
    totals = ms_marks(path)
    problems = []
    for q, fix in load_overrides(MS_CORRECTIONS).get(path.name, {}).get("corrections", {}).items():
        q = int(q)
        read = totals.get(q, set())
        expected = set() if fix["printed"] is None else {fix["printed"]}
        if read != expected:
            problems.append(f"Q{q}: MS correction expects the printed total to read {fix['printed']}, "
                            f"but the parser reads {sorted(read) or 'none'}")
            continue
        totals[q] = {fix["total"]}
    return totals, problems


def overrides(paper, series):
    """Human-readable list of every hand-read total and mark-scheme correction
    used for this paper (shown in check_marks output and on the review sheet)."""
    notes = []
    qp_path = PAPERS_DIR / f"{paper}_{series}_QP.pdf"
    ms_path = MARK_SCHEMES_DIR / f"{paper}_{series}_MS.pdf"
    entry = manual_entry(qp_path) if qp_path.exists() else None
    if entry:
        why = "scan with no text layer" if entry.get("text_layer") != "unreadable" else "unreadable text layer"
        totals = ", ".join(f"Q{q} {m}" for q, m in entry["totals"].items())
        notes.append(f"QP totals read by hand ({why}): {totals}; they add up to "
                     f"{sum(entry['totals'].values())} of {entry.get('paper_total', '?')}. "
                     f"Read from: {entry['read_from']}")
    fixes = load_overrides(MS_CORRECTIONS).get(ms_path.name, {}).get("corrections", {})
    for q, fix in fixes.items():
        printed = "no total printed" if fix["printed"] is None else f"printed {fix['printed']}"
        notes.append(f"MS correction Q{q}: {printed}, corrected to {fix['total']} "
                     f"(MS page {fix['page']}). {fix['reason']}")
    return notes


def compare(paper, series):
    """Return (status, problems) where status is ok, MISMATCH or UNCHECKED."""
    qp_path = PAPERS_DIR / f"{paper}_{series}_QP.pdf"
    ms_path = MARK_SCHEMES_DIR / f"{paper}_{series}_MS.pdf"
    for path in (qp_path, ms_path):
        if not path.exists():
            return "UNCHECKED", [f"missing {path.relative_to(ROOT).as_posix()}"]

    qp = qp_marks(qp_path)
    ms, problems = corrected_ms_marks(ms_path)
    problems += manual_problems(qp_path)
    # A real mismatch needs one clean total on each side that disagree.
    # Anything else (missing or several totals) means the parser lost track.
    mismatch = False
    if not qp:
        if has_text_layer(qp_path):
            problems.append("no 'Total for Question N is X marks' lines found in the QP")
        else:
            problems.append("QP is a scan with no text layer; read its totals from the page "
                            "images and record them in bank/qp_totals_manual.json")
    if not ms:
        problems.append("no question totals found in the MS")

    for q in sorted(set(qp) | set(ms)):
        in_qp = qp.get(q)
        in_ms = ms.get(q, set())
        if in_qp is None:
            problems.append(f"Q{q}: in MS ({sorted(in_ms)}) but not in QP")
        elif not in_ms:
            problems.append(f"Q{q}: QP says {in_qp}, no total found in MS")
        elif in_ms != {in_qp}:
            problems.append(f"Q{q}: QP says {in_qp}, MS says {sorted(in_ms)}")
            if len(in_ms) == 1:
                mismatch = True

    if mismatch:
        return "MISMATCH", problems
    return ("UNCHECKED" if problems else "ok"), problems


def all_pairs():
    """(paper, series) for every QP that has a matching MS file."""
    pairs = []
    for qp in sorted(PAPERS_DIR.glob("*_QP.pdf")):
        match = FILENAME_RE.match(qp.name)
        if match and (MARK_SCHEMES_DIR / qp.name.replace("_QP", "_MS")).exists():
            pairs.append((match["paper"], match["series"]))
    return pairs


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paper", nargs="?", help="e.g. 8MA0-01")
    parser.add_argument("series", nargs="?", help="e.g. 2018-06, SAM, SPEC")
    parser.add_argument("--all", action="store_true", help="check every QP/MS pair")
    args = parser.parse_args()

    if args.all:
        pairs = all_pairs()
    elif args.paper and args.series:
        pairs = [(args.paper, args.series)]
    else:
        parser.error("give PAPER SERIES, or --all")

    failed = 0
    for paper, series in pairs:
        status, problems = compare(paper, series)
        if problems:
            failed += 1
            print(f"{status:9} {paper} {series}")
            for p in problems:
                print(f"    {p}")
        else:
            qp_path = PAPERS_DIR / f"{paper}_{series}_QP.pdf"
            total = sum(qp_marks(qp_path).values())
            print(f"{'ok':9} {paper} {series}  ({total} marks)")
            for note in overrides(paper, series):
                print(f"    [override] {note}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
