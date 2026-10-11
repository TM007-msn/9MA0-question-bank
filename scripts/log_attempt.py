"""Add marked attempts to log/attempts.csv, checking each one first.

Usage (from the project root, with the venv active):
    python scripts/log_attempt.py              # asks for each attempt in turn
    python scripts/log_attempt.py --csv        # paste CSV rows, then Ctrl+Z Enter (Ctrl+D on Mac/Linux)
    python scripts/log_attempt.py --csv FILE   # rows from a file

Pasted rows use the attempts.csv columns, with or without the header line:
    date,question_id,topic,marks_awarded,marks_total,error_type
date may be blank for today, and topic blank to fill it in from the bank.

Every row is checked, and nothing is written unless all of them pass:
  - question_id is in bank/questions.json or bank/generated.json
  - topic, if given, is that entry's topic
  - marks_awarded and marks_total are whole numbers, with
    0 <= marks_awarded <= marks_total, and marks_total is the entry's marks
  - error_type is one of knowledge, method, slip, misread, time when marks
    were lost, and blank for full marks
  - date is YYYY-MM-DD and not in the future
"""

import argparse
import csv
import io
import json
import sys
from datetime import date
from pathlib import Path

from paths import ROOT

ATTEMPTS = ROOT / "log" / "attempts.csv"
BANK_FILES = [ROOT / "bank" / "questions.json", ROOT / "bank" / "generated.json"]
FIELDS = ["date", "question_id", "topic", "marks_awarded", "marks_total", "error_type"]
ERROR_TYPES = ("knowledge", "method", "slip", "misread", "time")


def load_bank():
    """{id: entry} for questions.json and generated.json."""
    return {e["id"]: e for path in BANK_FILES for e in json.loads(path.read_text(encoding="utf-8"))}


def read_attempts(path=ATTEMPTS):
    """Rows of attempts.csv with date as a date and marks as ints ([] if no file)."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [{**row,
                 "date": date.fromisoformat(row["date"]),
                 "marks_awarded": int(row["marks_awarded"]),
                 "marks_total": int(row["marks_total"]),
                 "error_type": row["error_type"].strip()}
                for row in csv.DictReader(f)]


def check_row(raw, bank, today):
    """(row ready to write, [problems]) for one attempt given as {field: text}."""
    raw = {k: (raw.get(k) or "").strip() for k in FIELDS}
    problems = []
    row = dict(raw)

    if not raw["date"]:
        row["date"] = today.isoformat()
    else:
        try:
            if date.fromisoformat(raw["date"]) > today:
                problems.append(f"date {raw['date']} is in the future")
        except ValueError:
            problems.append(f"date {raw['date']!r} is not YYYY-MM-DD")

    entry = bank.get(raw["question_id"])
    if entry is None:
        problems.append(f"question_id {raw['question_id']!r} is not in questions.json or generated.json")
    elif not raw["topic"]:
        row["topic"] = entry["topic"]
    elif raw["topic"] != entry["topic"]:
        problems.append(f"topic {raw['topic']!r} is not {raw['question_id']}'s topic ({entry['topic']!r})")

    try:
        awarded, total = int(raw["marks_awarded"]), int(raw["marks_total"])
    except ValueError:
        problems.append(f"marks {raw['marks_awarded']!r}/{raw['marks_total']!r} are not whole numbers")
        return row, problems
    if not 0 <= awarded <= total:
        problems.append(f"marks_awarded {awarded} must be between 0 and marks_total {total}")
    if entry is not None and total != entry["marks"]:
        problems.append(f"marks_total {total} is not {raw['question_id']}'s {entry['marks']} marks")

    if awarded < total and raw["error_type"] not in ERROR_TYPES:
        problems.append(f"error_type {raw['error_type']!r} must be one of {', '.join(ERROR_TYPES)} "
                        "when marks were lost")
    elif awarded == total and raw["error_type"]:
        problems.append(f"error_type {raw['error_type']!r} given for full marks; leave it blank")
    return row, problems


def parse_pasted(text):
    """Rows ({field: text}) from pasted CSV, skipping blank lines and a header line."""
    rows = []
    for values in csv.reader(io.StringIO(text)):
        if not any(v.strip() for v in values):
            continue
        if [v.strip() for v in values] == FIELDS:
            continue
        if len(values) != len(FIELDS):
            rows.append({"question_id": ",".join(values), "_columns": len(values)})
            continue
        rows.append(dict(zip(FIELDS, values)))
    return rows


def check_rows(raw_rows, bank, today):
    """(rows, problems as 'row N: ...') for all rows."""
    rows, problems = [], []
    for n, raw in enumerate(raw_rows, 1):
        if "_columns" in raw:
            problems.append(f"row {n}: {raw['_columns']} columns, expected {len(FIELDS)} ({','.join(FIELDS)})")
            continue
        row, row_problems = check_row(raw, bank, today)
        rows.append(row)
        problems += [f"row {n}: {p}" for p in row_problems]
    return rows, problems


def append_rows(rows, path=ATTEMPTS):
    """Append rows, writing the header first if the file is new."""
    new = not path.exists() or path.stat().st_size == 0
    if not new and not path.read_bytes().endswith(b"\n"):
        with path.open("a", encoding="utf-8", newline="") as f:
            f.write("\n")
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        if new:
            writer.writeheader()
        writer.writerows(rows)


def ask_rows(bank, today, ask=input):
    """Ask for attempts one at a time until a blank question id."""
    rows = []
    while True:
        question_id = ask("question_id (blank to finish): ").strip()
        if not question_id:
            return rows
        entry = bank.get(question_id)
        if entry is None:
            print(f"  {question_id} is not in questions.json or generated.json")
            continue
        print(f"  {entry['topic']}, {entry['marks']} marks")
        raw = {"question_id": question_id, "marks_total": str(entry["marks"])}
        raw["marks_awarded"] = ask("  marks_awarded: ")
        if raw["marks_awarded"].strip() != raw["marks_total"]:
            raw["error_type"] = ask(f"  error_type ({'/'.join(ERROR_TYPES)}): ")
        raw["date"] = ask(f"  date [{today.isoformat()}]: ")
        row, problems = check_row(raw, bank, today)
        if problems:
            print("  Not added: " + "; ".join(problems))
            continue
        rows.append(row)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--csv", nargs="?", const="-", metavar="FILE",
                        help="read CSV rows from FILE, or paste them (no FILE)")
    parser.add_argument("--attempts", type=Path, default=ATTEMPTS,
                        help="attempts file to add to (default log/attempts.csv)")
    args = parser.parse_args()
    bank = load_bank()
    today = date.today()

    if args.csv is None:
        rows = ask_rows(bank, today)
    else:
        if args.csv == "-":
            print("Paste rows, then Ctrl+Z Enter (Ctrl+D on Mac/Linux):", file=sys.stderr)
            text = sys.stdin.read()
        else:
            with open(args.csv, encoding="utf-8") as f:
                text = f.read()
        rows, problems = check_rows(parse_pasted(text), bank, today)
        if problems:
            print("Nothing written:\n  " + "\n  ".join(problems))
            return 1

    if not rows:
        print("Nothing to add.")
        return 0
    append_rows(rows, args.attempts)
    for row in rows:
        print(f"  {row['date']}  {row['question_id']:<26} {row['marks_awarded']}/{row['marks_total']}"
              f"  {row['error_type']}")
    print(f"Added {len(rows)} row(s) to {args.attempts.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
