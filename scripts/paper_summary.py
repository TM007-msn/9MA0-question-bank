"""Print the numbers for a paper's end-of-extraction summary.

Usage (from the project root, with the venv active):
    python scripts/paper_summary.py 8MA0-01 2019-06

Prints: entries, marks, ALT lines, null fields (and which), difficulty
spread, and the entries with diagrams.
"""

import argparse
import json
import sys
from collections import Counter

from paths import ROOT

QUESTIONS = ROOT / "bank" / "questions.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paper")
    parser.add_argument("series")
    args = parser.parse_args()

    entries = [e for e in json.load(open(QUESTIONS, encoding="utf-8"))
               if e["paper"] == args.paper and e["series"] == args.series]
    if not entries:
        print(f"no entries for {args.paper} {args.series}")
        return 1

    def short(e):
        return e["id"].rsplit("_", 1)[1]

    alts = sum(m.startswith("ALT:") for e in entries for m in (e["mark_scheme"] or []))
    nulls = [(short(e), k) for e in entries for k, v in e.items() if v is None]
    spread = Counter(e["difficulty"] for e in entries)
    diagrams = [short(e) for e in entries if e["has_diagram"]]

    print(f"Entries:      {len(entries)}")
    print(f"Marks:        {sum(e['marks'] or 0 for e in entries)}")
    print(f"ALT lines:    {alts}")
    print(f"Null fields:  {len(nulls)}" + (": " + ", ".join(f"{q}.{k}" for q, k in nulls) if nulls else ""))
    print("Difficulty:   " + ", ".join(f"{level or 'null'} {spread[level]}" for level in ("easy", "medium", "hard", None) if spread[level]))
    print(f"Diagrams:     {len(diagrams)}" + (": " + ", ".join(diagrams) if diagrams else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
