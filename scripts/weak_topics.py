"""Rank covered spec refs by marks lost recently, and list re-tests that are due.

Usage (from the project root, with the venv active):
    python scripts/weak_topics.py              # last 14 days
    python scripts/weak_topics.py --days 28

Weak refs: every attempt in log/attempts.csv from the last N days (dated
today minus N days or later) counts towards its question's main spec ref, the first in its
spec_ref, so a part's marks are counted once. Only refs in
bank/covered_topics.json are ranked. For each ref it shows the marks lost,
the marks available, the % dropped and the most common error type among the
attempts that lost marks, ranked by marks lost, then % dropped.

Re-tests: every attempt that lost marks, however old, is due a re-test 7
days and 21 days after it. A re-test counts as done once that question (or
a generated variant of it) has been attempted on or after its due date.
Shown are re-tests not yet done that are overdue or due within the next
7 days.
"""

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from covered import COVERED, load_covered, load_topics, main_ref, real_id, ref_topic, strand_of
from log_attempt import ATTEMPTS, load_bank, read_attempts

RETEST_AFTER_DAYS = (7, 21)
LOOK_AHEAD_DAYS = 7


def weak_refs(attempts, bank, covered, topics, today, days):
    """Rows for covered refs attempted in the window, worst first.

    Each row: {qual, strand, ref, topic, lost, available, dropped (0-100), error}.
    """
    since = today - timedelta(days=days)  # the same window rule as quick_set.py's 21 days
    strands = strand_of(topics)
    totals = defaultdict(lambda: {"lost": 0, "available": 0, "errors": Counter()})
    for row in attempts:
        entry = bank.get(row["question_id"])
        if entry is None or not since <= row["date"] <= today:
            continue
        qual, strand, ref = entry["paper"][:4], strands[entry["topic"]], main_ref(entry)
        if ref not in covered.get((qual, strand), set()):
            continue
        t = totals[(qual, strand, ref)]
        lost = row["marks_total"] - row["marks_awarded"]
        t["lost"] += lost
        t["available"] += row["marks_total"]
        if lost:
            t["errors"][row["error_type"]] += 1

    rows = []
    for (qual, strand, ref), t in totals.items():
        # Most common error type; a tie goes to the type named first in the log.
        error = t["errors"].most_common(1)[0][0] if t["errors"] else ""
        rows.append({"qual": qual, "strand": strand, "ref": ref,
                     "topic": ref_topic(topics, qual, strand, ref)["name"],
                     "lost": t["lost"], "available": t["available"],
                     "dropped": 100 * t["lost"] / t["available"], "error": error})
    return sorted(rows, key=lambda r: (-r["lost"], -r["dropped"], r["qual"], r["strand"], r["ref"]))


def retests_due(attempts, today, ahead=LOOK_AHEAD_DAYS):
    """Re-tests not yet done that are overdue or due within `ahead` days, soonest first.

    Each: {due, after_days, question_id (the real question), attempted, lost, total, topic}.
    """
    dates_by_question = defaultdict(list)
    for row in attempts:
        dates_by_question[real_id(row["question_id"])].append(row["date"])

    due = []
    for row in attempts:
        lost = row["marks_total"] - row["marks_awarded"]
        if not lost:
            continue
        question = real_id(row["question_id"])
        for after in RETEST_AFTER_DAYS:
            when = row["date"] + timedelta(days=after)
            done = any(d >= when for d in dates_by_question[question])
            if not done and when <= today + timedelta(days=ahead):
                due.append({"due": when, "after_days": after, "question_id": question,
                            "attempted": row["date"], "lost": lost, "total": row["marks_total"],
                            "topic": row["topic"]})
    return sorted(due, key=lambda d: (d["due"], d["question_id"]))


def when_text(due, today):
    days = (due - today).days
    if days < 0:
        return f"overdue {-days}d"
    return "today" if days == 0 else f"in {days}d"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--days", type=int, default=14, help="window in days (default 14)")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(),
                        help="pretend today is this date (YYYY-MM-DD)")
    parser.add_argument("--attempts", type=Path, default=ATTEMPTS, help="attempts file (default log/attempts.csv)")
    parser.add_argument("--covered", type=Path, default=COVERED,
                        help="covered-topics file (default bank/covered_topics.json)")
    args = parser.parse_args()
    sys.stdout.reconfigure(errors="replace")

    topics = load_topics()
    attempts = read_attempts(args.attempts)
    bank = load_bank()
    unknown = sorted({r["question_id"] for r in attempts if r["question_id"] not in bank})
    if unknown:
        print(f"Skipped attempts at ids not in the bank: {', '.join(unknown)}\n")

    rows = weak_refs(attempts, bank, load_covered(args.covered, topics), topics, args.today, args.days)
    print(f"Weak spec refs, last {args.days} days (to {args.today.isoformat()}):")
    if not rows:
        print("  No attempts at covered refs in this window.")
    else:
        print(f"  {'Ref':<20} {'Lost':>4} {'Avail':>5} {'Dropped':>7}  {'Main error':<10}  Topic")
        for r in rows:
            name = f"{r['qual']} {r['strand']} {r['ref']}"
            print(f"  {name:<20} {r['lost']:>4} {r['available']:>5} {r['dropped']:>6.0f}%  "
                  f"{r['error'] or '-':<10}  {r['topic']}")

    due = retests_due(attempts, args.today)
    print(f"\nRe-tests due (overdue, or within {LOOK_AHEAD_DAYS} days):")
    if not due:
        print("  None.")
    for d in due:
        print(f"  {d['due'].isoformat()}  {when_text(d['due'], args.today):<11} {d['question_id']:<26} "
              f"{d['after_days']:>2}-day re-test of {d['attempted'].isoformat()} "
              f"(lost {d['lost']}/{d['total']})  {d['topic']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
