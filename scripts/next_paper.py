"""Pick the next paper to extract from bank/progress.json.

Usage (from the project root, with the venv active):
    python scripts/next_paper.py            # print the next paper as JSON
    python scripts/next_paper.py --approve  # first mark papers in_review as done

Rules:
- Papers are taken in queue order (the order set in progress.json), skipping
  done and blocked ones.
- If a paper is still in_review, nothing new is picked: it must be approved
  first. --approve marks every in_review paper done; only use it when the
  user has said those papers are approved.
- A reserved series is never picked, even if it were somehow in the queue.

Exit code 0 with the paper as JSON on stdout; 1 with a reason on stderr if
nothing can be picked.
"""

import argparse
import json
import sys
from datetime import date

from fetch_materials import RESERVED_SERIES
from paths import ROOT

PROGRESS = ROOT / "bank" / "progress.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--approve", action="store_true",
                        help="mark papers currently in_review as done (user approved them)")
    args = parser.parse_args()

    progress = json.load(open(PROGRESS, encoding="utf-8"))
    queue = progress["queue"]
    in_review = [i for i in queue if i["status"] == "in_review"]

    if args.approve and in_review:
        for item in in_review:
            item["status"] = "done"
            item["note"] = f"Approved {date.today().isoformat()}."
        progress["updated"] = date.today().isoformat()
        with open(PROGRESS, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("Marked done: " + ", ".join(f"{i['paper']} {i['series']}" for i in in_review), file=sys.stderr)
        in_review = []

    if in_review:
        names = ", ".join(f"{i['paper']} {i['series']}" for i in in_review)
        print(f"STOP: {names} still in_review. Review it first; run with --approve once the user approves.",
              file=sys.stderr)
        return 1

    for item in queue:
        if item["status"] != "queued":
            continue
        qual = item["paper"].split("-")[0]
        if item["series"] in RESERVED_SERIES.get(qual, set()):
            print(f"STOP: {item['paper']} {item['series']} is a reserved series but is queued; fix progress.json.",
                  file=sys.stderr)
            return 1
        print(json.dumps(item, ensure_ascii=False))
        return 0

    print("Nothing left: every paper is done or blocked.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
