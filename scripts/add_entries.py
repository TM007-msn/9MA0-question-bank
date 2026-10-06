"""Add a draft paper's entries to bank/questions.json, after safety checks.

Usage (from the project root, with the venv active):
    python scripts/add_entries.py path/to/draft.json

The draft is a JSON array of question entries, all from one paper and series.
Nothing is written unless every check passes:
  1. every entry follows schemas/question.schema.json
  2. the paper/series is not reserved
  3. check_marks.py says the mark scheme matches the question paper ("ok")
  4. for each question, the entries' marks add up to the question paper's total
  5. no id is already in the bank, and no id repeats within the draft
If all pass, the entries are appended and the paper is set to in_review in
bank/progress.json.
"""

import json
import sys
from collections import defaultdict
from datetime import date

from jsonschema import Draft202012Validator, FormatChecker

from check_marks import PAPERS_DIR, compare, qp_marks
from fetch_materials import RESERVED_SERIES
from paths import ROOT
from validate import build_registry

QUESTIONS = ROOT / "bank" / "questions.json"
PROGRESS = ROOT / "bank" / "progress.json"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def question_number(entry):
    """'9MA0-01_2018-06_Q07bii' -> 7."""
    part = entry["id"].rsplit("_Q", 1)[1]
    digits = ""
    for ch in part:
        if not ch.isdigit():
            break
        digits += ch
    return int(digits)


def check_draft(draft):
    """Return (paper, series, problems)."""
    problems = []
    if not isinstance(draft, list) or not draft:
        return None, None, ["draft must be a non-empty JSON array"]

    registry, schemas = build_registry()
    validator = Draft202012Validator(
        schemas["question.schema.json"], registry=registry, format_checker=FormatChecker()
    )
    for entry in draft:
        for err in validator.iter_errors(entry):
            problems.append(f"{entry.get('id', '?')} {err.json_path}: {err.message}")
    if problems:
        return None, None, problems

    papers = {(e["paper"], e["series"]) for e in draft}
    if len(papers) != 1:
        return None, None, [f"draft mixes papers/series: {sorted(papers)}"]
    paper, series = papers.pop()
    qual = paper.split("-")[0]

    if series in RESERVED_SERIES.get(qual, set()):
        return paper, series, [f"{paper} {series} is a reserved series; it must not go in the bank"]

    for entry in draft:
        if not entry["id"].startswith(f"{paper}_{series}_Q"):
            problems.append(f"{entry['id']}: id does not match paper {paper} / series {series}")

    status, mark_problems = compare(paper, series)
    if status != "ok":
        problems.append(f"marks check is {status}; not saving")
        problems.extend(f"    {p}" for p in mark_problems)

    qp_totals = qp_marks(PAPERS_DIR / f"{paper}_{series}_QP.pdf")
    draft_totals = defaultdict(int)
    for entry in draft:
        draft_totals[question_number(entry)] += entry["marks"] or 0
    for q in sorted(set(qp_totals) | set(draft_totals)):
        if qp_totals.get(q) != draft_totals.get(q):
            problems.append(f"Q{q}: entries add up to {draft_totals.get(q)}, question paper says {qp_totals.get(q)}")

    existing = {e["id"] for e in load(QUESTIONS)}
    seen = set()
    for entry in draft:
        if entry["id"] in existing:
            problems.append(f"{entry['id']}: already in questions.json")
        if entry["id"] in seen:
            problems.append(f"{entry['id']}: repeated in the draft")
        seen.add(entry["id"])

    return paper, series, problems


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    draft = load(sys.argv[1])
    paper, series, problems = check_draft(draft)
    if problems:
        print("NOT SAVED:")
        for p in problems:
            print(f"  {p}")
        return 1

    bank = load(QUESTIONS)
    bank.extend(draft)
    save(QUESTIONS, bank)

    progress = load(PROGRESS)
    for item in progress["queue"]:
        if item["paper"] == paper and item["series"] == series:
            item["status"] = "in_review"
            item["marks_check"] = "ok"
    progress["updated"] = date.today().isoformat()
    save(PROGRESS, progress)

    print(f"Saved {len(draft)} entries for {paper} {series} "
          f"({sum(e['marks'] for e in draft)} marks). Status: in_review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
