"""Add a draft paper's entries to bank/questions.json, after safety checks.

Usage (from the project root, with the venv active):
    python scripts/add_entries.py path/to/draft.json
    python scripts/add_entries.py --replace path/to/draft.json
    python scripts/add_entries.py --replace-approved "why" path/to/draft.json

--replace swaps out the paper's existing entries for the draft. It is only
allowed while the paper is still in_review (i.e. being redone after review).

--replace-approved does the same for a paper that is already done (approved),
e.g. after a rule change applied across the bank. It needs a reason. The
paper stays done, and a dated record of the reason and of every id and field
that changed is appended to the paper's "history" in bank/progress.json.
Every check below still runs.

The draft is a JSON array of question entries, all from one paper and series.
Nothing is written unless every check passes:
  1. every entry follows schemas/question.schema.json and validate.py's
     cross-field rules (figure rule, spec refs, source_file)
  2. the paper/series is not reserved
  3. check_marks.py says the mark scheme matches the question paper ("ok")
  4. for each question, the entries' marks add up to the question paper's total
  5. no id is already in the bank, and no id repeats within the draft
If all pass, the entries are saved (a replaced paper keeps its place in the
file) and the paper is set to in_review in bank/progress.json (or, with
--replace-approved, stays done with a history record).
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date

from jsonschema import Draft202012Validator, FormatChecker

from check_marks import PAPERS_DIR, compare, qp_marks
from fetch_materials import RESERVED_SERIES
from paths import ROOT
from validate import build_registry, consistency_errors

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


def check_draft(draft, replace=None):
    """Return (paper, series, problems).

    replace is None for new entries, "in_review" for --replace and "done"
    for --replace-approved: the status the paper must have to be replaced.
    """
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
        for message in consistency_errors("questions.json", entry):
            problems.append(f"{entry.get('id', '?')}: {message}")
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

    existing = {e["id"] for e in load(QUESTIONS)
                if not (replace and e["paper"] == paper and e["series"] == series)}
    if replace:
        status = next((i["status"] for i in load(PROGRESS)["queue"]
                       if i["paper"] == paper and i["series"] == series), None)
        if status != replace:
            flag = "--replace" if replace == "in_review" else "--replace-approved"
            problems.append(f"{flag} is only for papers that are {replace}; {paper} {series} is {status}")
    seen = set()
    for entry in draft:
        if entry["id"] in existing:
            problems.append(f"{entry['id']}: already in questions.json")
        if entry["id"] in seen:
            problems.append(f"{entry['id']}: repeated in the draft")
        seen.add(entry["id"])

    return paper, series, problems


def changes(old, new):
    """What a replacement changes: ids added and removed, and "id: field" for
    each field whose value differs."""
    old_by_id = {e["id"]: e for e in old}
    new_by_id = {e["id"]: e for e in new}
    changed = []
    for entry_id in sorted(set(old_by_id) & set(new_by_id)):
        a, b = old_by_id[entry_id], new_by_id[entry_id]
        changed += [f"{entry_id}: {k}" for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    return {"added": sorted(set(new_by_id) - set(old_by_id)),
            "removed": sorted(set(old_by_id) - set(new_by_id)),
            "changed": changed}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("draft", help="JSON array of entries for one paper")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--replace", action="store_true",
                      help="replace this paper's existing entries (in_review only)")
    mode.add_argument("--replace-approved", metavar="REASON",
                      help="replace an approved (done) paper's entries; REASON is recorded in progress.json")
    args = parser.parse_args()
    if args.replace_approved is not None and not args.replace_approved.strip():
        parser.error("--replace-approved needs a reason")
    replace = "in_review" if args.replace else "done" if args.replace_approved else None
    draft = load(args.draft)
    paper, series, problems = check_draft(draft, replace)
    if problems:
        print("NOT SAVED:")
        for p in problems:
            print(f"  {p}")
        return 1

    bank = load(QUESTIONS)
    removed = []
    if replace:
        # Put the new entries where the old ones were, so the file keeps its order.
        is_this_paper = [e["paper"] == paper and e["series"] == series for e in bank]
        removed = [e for e, mine in zip(bank, is_this_paper) if mine]
        at = is_this_paper.index(True) if removed else len(bank)
        bank = [e for e, mine in zip(bank, is_this_paper) if not mine]
        bank[at:at] = draft
        print(f"Replacing {len(removed)} existing entries for {paper} {series}.")
    else:
        bank.extend(draft)

    diff = changes(removed, draft)
    if replace == "done" and not any(diff.values()):
        print(f"NOT SAVED: the draft is identical to the saved entries for {paper} {series}.")
        return 1
    save(QUESTIONS, bank)

    today = date.today().isoformat()
    progress = load(PROGRESS)
    status = None
    for item in progress["queue"]:
        if item["paper"] == paper and item["series"] == series:
            item["marks_check"] = "ok"
            if replace == "done":
                item.setdefault("history", []).append(
                    {"date": today, "reason": args.replace_approved.strip(), **diff})
            else:
                item["status"] = "in_review"
            status = item["status"]
    progress["updated"] = today
    save(PROGRESS, progress)

    print(f"Saved {len(draft)} entries for {paper} {series} "
          f"({sum(e['marks'] for e in draft)} marks). Status: {status}.")
    if replace == "done":
        print(f"History: {len(diff['changed'])} field changes, {len(diff['added'])} added, "
              f"{len(diff['removed'])} removed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
