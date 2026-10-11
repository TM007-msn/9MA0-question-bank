"""Pick a quick practice set of real questions and build its PDFs.

Usage (from the project root, with the venv active):
    python scripts/quick_set.py                  # 50 marks
    python scripts/quick_set.py --marks 30 --name algebra-mix
    python scripts/quick_set.py --dry-run        # show the pick, build nothing

A stopgap until the weekly set builder exists. It picks entries from
bank/questions.json that
  - come from a paper marked done (approved) in bank/progress.json,
  - have every spec ref in bank/covered_topics.json, and
  - were not attempted in the last 21 days (log/attempts.csv; an attempt at
    a generated variant, e.g. ..._Q05b-A, counts for its real question too).
Medium and hard parts are taken first, then easy, then unrated, each group
in random order, adding parts while the total stays within the mark total.
The set is listed in paper order, written to out/sets/NAME.json and built by
build_pdf.py into out/to-remarkable/.

bank/covered_topics.json is described in covered.py; cover_topic.py edits it.
"""

import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import build_pdf
from covered import COVERED, load_covered, load_topics, real_id, strand_of
from log_attempt import ATTEMPTS, read_attempts
from paths import ROOT, ensure_out_dir

QUESTIONS = ROOT / "bank" / "questions.json"
PROGRESS = ROOT / "bank" / "progress.json"

RECENT_DAYS = 21
# Difficulty groups in the order they are drawn from.
PREFERENCE = [{"medium", "hard"}, {"easy"}, {None}]


def recently_attempted(today, path=ATTEMPTS, days=RECENT_DAYS):
    """Ids of real questions attempted within `days` days before today."""
    since = today - timedelta(days=days)
    return {real_id(row["question_id"]) for row in read_attempts(path) if row["date"] >= since}


def approved_papers(path=PROGRESS):
    progress = json.loads(path.read_text(encoding="utf-8"))
    return {(p["paper"], p["series"]) for p in progress["queue"] if p["status"] == "done"}


def eligible(entries, covered, recent, approved, topics):
    """Entries that may go in the set."""
    strands = strand_of(topics)
    chosen = []
    for entry in entries:
        # All of an entry's refs are from its topic's strand (validate.py checks this).
        refs_covered = covered.get((entry["paper"][:4], strands[entry["topic"]]), set())
        refs = [r.strip() for r in entry["spec_ref"].split(",")]
        if ((entry["paper"], entry["series"]) in approved
                and all(r in refs_covered for r in refs)
                and entry["id"] not in recent):
            chosen.append(entry)
    return chosen


def pick(candidates, total_marks, rng):
    """Medium/hard first, then easy, then unrated, without going over total_marks."""
    picked, marks = [], 0
    for group in PREFERENCE:
        pool = [e for e in candidates if e["difficulty"] in group]
        rng.shuffle(pool)
        for entry in pool:
            if marks + entry["marks"] <= total_marks:
                picked.append(entry)
                marks += entry["marks"]
    # Paper order, so parts of one question sit together.
    return sorted(picked, key=lambda e: e["id"])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--marks", type=int, default=50, help="mark total (default 50)")
    parser.add_argument("--name", help="set name (default quick-YYYY-MM-DD)")
    parser.add_argument("--seed", type=int, help="random seed, to repeat a pick")
    parser.add_argument("--dry-run", action="store_true", help="show the pick but build nothing")
    parser.add_argument("--covered", type=Path, default=COVERED,
                        help="covered-topics file (default bank/covered_topics.json)")
    args = parser.parse_args()

    today = date.today()
    name = args.name or f"quick-{today.isoformat()}"
    entries = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    topics = load_topics()
    candidates = eligible(entries, load_covered(args.covered, topics), recently_attempted(today),
                          approved_papers(), topics)
    picked = pick(candidates, args.marks, random.Random(args.seed))
    if not picked:
        raise SystemExit(f"No eligible questions ({len(candidates)} candidates); check covered_topics.json.")

    total = sum(e["marks"] for e in picked)
    print(f"{len(candidates)} eligible parts; picked {len(picked)} for {total} of {args.marks} marks:")
    for e in picked:
        print(f"  {e['id']:<26} {e['marks']:>2}  {str(e['difficulty']):<6}  {e['topic']}")
    if total < args.marks:
        print(f"Note: only {total} marks could be filled without going over {args.marks}.")
    if args.dry_run:
        return 0

    set_file = ensure_out_dir("sets") / f"{name}.json"
    set_file.write_text(json.dumps([e["id"] for e in picked], indent=2) + "\n", encoding="utf-8")
    print(set_file)
    build_pdf.build([e["id"] for e in picked], name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
