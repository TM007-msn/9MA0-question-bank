"""Pick a quick practice set of real questions and build its PDFs.

Usage (from the project root, with the venv active):
    python scripts/quick_set.py                  # 50 marks
    python scripts/quick_set.py --marks 30 --name algebra-mix
    python scripts/quick_set.py --dry-run        # show the pick, build nothing
    python scripts/quick_set.py --send           # build, then upload the questions PDF
    python scripts/quick_set.py --pool as-pure --send   # from a fixed pool (see below)

A stopgap until the weekly set builder exists. Re-tests that are due go in
first: weak_topics.py's 7- and 21-day re-tests that are overdue or due
today, soonest first, while they fit in the mark total. The rest of the set
is entries from bank/questions.json that
  - come from a paper marked done (approved) in bank/progress.json,
  - have every spec ref in bank/covered_topics.json, and
  - were not attempted in the last 21 days (log/attempts.csv; an attempt at
    a generated variant, e.g. ..._Q05b-A, counts for its real question too).
Medium and hard parts are taken first, then easy, then unrated, each group
in random order, adding parts while the total stays within the mark total.
The set is listed in paper order, written to out/sets/NAME.json and built by
build_pdf.py into out/to-remarkable/. --send then uploads the questions PDF
(never the mark scheme) to the "Maths practice" folder with send_remarkable.py.

bank/covered_topics.json is described in covered.py; cover_topic.py edits it.

--pool picks from a fixed pool of done papers instead, ignoring
covered_topics.json, re-tests and attempts.csv:
  as-pure      every entry from done 8MA0-01 papers
  alevel-pure  every entry from done 9MA0-01 and 9MA0-02 papers
Repeats are avoided with the sent history, out/sets/sent_history.json
({question id: date last sent}), which is updated only after a successful
--send. Questions never sent come first (medium/hard, then easy, then
unrated, as above). Once all of those are used up, the least recently sent
are reused, oldest first. daily.py builds its exam sheet this way.
"""

import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import build_pdf
import send_remarkable
from covered import COVERED, load_covered, load_topics, real_id, strand_of
from log_attempt import ATTEMPTS, read_attempts
from paths import ROOT, ensure_out_dir
from weak_topics import retests_due

QUESTIONS = ROOT / "bank" / "questions.json"
PROGRESS = ROOT / "bank" / "progress.json"

SENT_HISTORY = ROOT / "out" / "sets" / "sent_history.json"

# Which done papers each --pool draws from.
POOLS = {
    "as-pure": {"8MA0-01"},
    "alevel-pure": {"9MA0-01", "9MA0-02"},
}

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


def due_retests(attempts, entries, today):
    """Real questions with a re-test overdue or due today, soonest first, each once."""
    by_id = {e["id"]: e for e in entries}
    chosen = []
    for retest in retests_due(attempts, today, ahead=0):
        entry = by_id.get(retest["question_id"])
        if entry is not None and entry not in chosen:
            chosen.append(entry)
    return chosen


def pick(candidates, total_marks, rng, retests=()):
    """Due re-tests first (in the order given), then medium/hard, then easy,
    then unrated, without going over total_marks."""
    picked, marks = [], 0
    for entry in retests:
        if marks + entry["marks"] <= total_marks:
            picked.append(entry)
            marks += entry["marks"]
    for group in PREFERENCE:
        pool = [e for e in candidates if e["difficulty"] in group and e not in picked]
        rng.shuffle(pool)
        for entry in pool:
            if marks + entry["marks"] <= total_marks:
                picked.append(entry)
                marks += entry["marks"]
    # Paper order, so parts of one question sit together.
    return sorted(picked, key=lambda e: e["id"])


# ---------------------------------------------------------------- pools

def pool_entries(entries, pool, approved):
    """Every entry of the pool's papers that come from a done paper."""
    papers = POOLS[pool]
    return [e for e in entries if e["paper"] in papers and (e["paper"], e["series"]) in approved]


def read_history(path=SENT_HISTORY):
    """{question id: date last sent}; empty if nothing has been sent yet."""
    if not path.is_file():
        return {}
    return {qid: date.fromisoformat(day) for qid, day in json.loads(path.read_text(encoding="utf-8")).items()}


def record_sent(ids, day, path=SENT_HISTORY):
    history = read_history(path)
    history.update({qid: day for qid in ids})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({qid: d.isoformat() for qid, d in sorted(history.items())}, indent=2) + "\n",
                    encoding="utf-8")


def pick_from_pool(candidates, total_marks, rng, history):
    """Never-sent entries first, then the least recently sent.

    Entries are grouped by the date they were last sent, never sent being
    the oldest, and the groups are drawn from oldest first, adding entries
    while the total stays within total_marks. So a sent question only goes
    in once every unsent one is in the set or too big for the marks left.
    Within a group: medium/hard, then easy, then unrated, each shuffled.
    """
    by_day = {}
    for entry in candidates:
        by_day.setdefault(history.get(entry["id"], date.min), []).append(entry)
    picked, marks = [], 0
    for day in sorted(by_day):
        for preference in PREFERENCE:
            pool = [e for e in by_day[day] if e["difficulty"] in preference]
            rng.shuffle(pool)
            for entry in pool:
                if marks + entry["marks"] <= total_marks:
                    picked.append(entry)
                    marks += entry["marks"]
    return sorted(picked, key=lambda e: e["id"])


def build_pool_set(pool, marks, name, send=False, seed=None, today=None):
    """Pick from a pool, build the PDFs and, with send, upload and record them.

    Returns the picked entries. Raises send_remarkable.SendError if the upload fails.
    """
    today = today or date.today()
    entries = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    candidates = pool_entries(entries, pool, approved_papers())
    history = read_history()
    picked = pick_from_pool(candidates, marks, random.Random(seed), history)
    if not picked:
        raise SystemExit(f"No questions in pool {pool!r}.")
    total = sum(e["marks"] for e in picked)
    unsent = sum(1 for e in candidates if e["id"] not in history)
    print(f"Pool {pool}: {len(candidates)} parts, {unsent} never sent; "
          f"picked {len(picked)} for {total} of {marks} marks:")
    for e in picked:
        last = history.get(e["id"])
        print(f"  {e['id']:<26} {e['marks']:>2}  {str(e['difficulty']):<6}  "
              f"{'sent ' + last.isoformat() if last else '':<16}  {e['topic']}")
    set_file = ensure_out_dir("sets") / f"{name}.json"
    set_file.write_text(json.dumps([e["id"] for e in picked], indent=2) + "\n", encoding="utf-8")
    print(set_file)
    build_pdf.build([e["id"] for e in picked], name)
    if send:
        send_remarkable.send(name)
        record_sent([e["id"] for e in picked], today)
    return picked


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--marks", type=int, default=50, help="mark total (default 50)")
    parser.add_argument("--name", help="set name (default quick-YYYY-MM-DD)")
    parser.add_argument("--seed", type=int, help="random seed, to repeat a pick")
    parser.add_argument("--dry-run", action="store_true", help="show the pick but build nothing")
    parser.add_argument("--send", action="store_true",
                        help="upload the questions PDF (not the mark scheme) to the reMarkable")
    parser.add_argument("--pool", choices=sorted(POOLS),
                        help="pick from a fixed pool with the sent history (ignores covered topics)")
    parser.add_argument("--covered", type=Path, default=COVERED,
                        help="covered-topics file (default bank/covered_topics.json)")
    parser.add_argument("--attempts", type=Path, default=ATTEMPTS,
                        help="attempts file (default log/attempts.csv)")
    args = parser.parse_args()
    if args.send and args.dry_run:
        parser.error("--send needs a built set, so it can't be used with --dry-run")
    if args.send:
        # Check before picking and building, so a missing or unpaired rmapi
        # is reported straight away rather than after the PDFs are built.
        try:
            send_remarkable.check_ready()
        except send_remarkable.SendError as error:
            raise SystemExit(str(error))

    today = date.today()
    name = args.name or f"quick-{today.isoformat()}"
    if args.pool:
        if args.dry_run:
            parser.error("--dry-run isn't available with --pool")
        try:
            build_pool_set(args.pool, args.marks, name, args.send, args.seed, today)
        except send_remarkable.SendError as error:
            raise SystemExit(str(error))
        return 0
    entries = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    topics = load_topics()
    attempts = read_attempts(args.attempts)
    retests = due_retests(attempts, entries, today)
    candidates = eligible(entries, load_covered(args.covered, topics),
                          recently_attempted(today, args.attempts), approved_papers(), topics)
    picked = pick(candidates, args.marks, random.Random(args.seed), retests)
    if not picked:
        raise SystemExit(f"No eligible questions ({len(candidates)} candidates); check covered_topics.json.")

    total = sum(e["marks"] for e in picked)
    print(f"{len(retests)} re-test(s) due, {len(candidates)} other eligible parts; "
          f"picked {len(picked)} for {total} of {args.marks} marks:")
    for e in picked:
        marker = "re-test" if e in retests else ""
        print(f"  {e['id']:<26} {e['marks']:>2}  {str(e['difficulty']):<6}  {marker:<7}  {e['topic']}")
    left_out = [e["id"] for e in retests if e not in picked]
    if left_out:
        print(f"Re-tests that didn't fit: {', '.join(left_out)}")
    if total < args.marks:
        print(f"Note: only {total} marks could be filled without going over {args.marks}.")
    if args.dry_run:
        return 0

    set_file = ensure_out_dir("sets") / f"{name}.json"
    set_file.write_text(json.dumps([e["id"] for e in picked], indent=2) + "\n", encoding="utf-8")
    print(set_file)
    build_pdf.build([e["id"] for e in picked], name)
    if args.send:
        try:
            send_remarkable.send(name)
        except send_remarkable.SendError as error:
            raise SystemExit(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main())
