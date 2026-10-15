"""Build today's two sheets and (with --send) upload them to the reMarkable.

Usage (from the project root, with the venv active):
    python scripts/daily.py            # build only
    python scripts/daily.py --send     # build, then upload both questions PDFs

The two sheets:
  drill-YYYY-MM-DD   ~25-mark algebra fluency drill (drill.py)
  exam-YYYY-MM-DD    exam questions from quick_set.py's --pool: as-pure until
                     2026-11-14, alevel-pure from 2026-11-15 on

Only the questions PDFs are sent: the drill's answers and the exam sheet's
mark scheme stay in out/to-remarkable/. Everything printed is also appended
to log/daily.log, with the time of the run. Windows Task Scheduler runs
`daily.py --send` at 06:30 every day (task "9MA0 daily sheets").
"""

import argparse
import sys
import traceback
from datetime import date, datetime

import drill
import quick_set
import send_remarkable
from paths import ROOT

LOG = ROOT / "log" / "daily.log"
ALEVEL_FROM = date(2026, 11, 15)
EXAM_MARKS = 50


def exam_pool(today):
    return "alevel-pure" if today >= ALEVEL_FROM else "as-pure"


class Tee:
    """Writes to the console and the log file both."""

    def __init__(self, console, log):
        self.console, self.log = console, log

    def write(self, text):
        if self.console is not None:
            self.console.write(text)
        self.log.write(text)
        self.log.flush()

    def flush(self):
        if self.console is not None:
            self.console.flush()


def run(today, send, exam_marks):
    """Build both sheets, then send them. Returns the exit code."""
    if send:
        # Fail before building if rmapi is missing or unpaired.
        send_remarkable.check_ready()
    drill_name = f"drill-{today.isoformat()}"
    exam_name = f"exam-{today.isoformat()}"
    pool = exam_pool(today)

    print(f"Drill sheet: {drill_name}")
    drill.build(drill_name, seed=today.toordinal())
    print(f"\nExam sheet: {exam_name} (pool {pool})")
    # The exam sheet is sent inside build_pool_set, which then records it in
    # the sent history. The drill goes after it, so a failed drill upload
    # can't stop the exam sheet being recorded.
    failures = []
    try:
        quick_set.build_pool_set(pool, exam_marks, exam_name, send=send, today=today)
    except send_remarkable.SendError as error:
        failures.append(f"{exam_name}: {error}")
    if send:
        try:
            send_remarkable.send(drill_name)
        except send_remarkable.SendError as error:
            failures.append(f"{drill_name}: {error}")
    for failure in failures:
        print(f"UPLOAD FAILED {failure}")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--send", action="store_true",
                        help="upload both questions PDFs (never the answers or mark scheme)")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(),
                        help="the day the sheets are for (default today)")
    parser.add_argument("--exam-marks", type=int, default=EXAM_MARKS,
                        help=f"mark total for the exam sheet (default {EXAM_MARKS})")
    args = parser.parse_args()

    LOG.parent.mkdir(exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as log:
        # UTF-8 to the console too, so the · and √ in output don't fail on
        # a cp1252 console or pipe.
        for stream in (sys.stdout, sys.stderr):
            if stream is not None and hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout, sys.stderr = Tee(sys.stdout, log), Tee(sys.stderr, log)
        print(f"\n===== {datetime.now():%Y-%m-%d %H:%M:%S} daily.py{' --send' if args.send else ''}")
        try:
            code = run(args.date, args.send, args.exam_marks)
        except send_remarkable.SendError as error:
            print(f"FAILED: {error}")
            code = 1
        except SystemExit as error:
            # build_pdf and quick_set stop with SystemExit("message").
            if error.code not in (0, None):
                print(f"FAILED: {error.code}")
            code = error.code if isinstance(error.code, int) else 1
        except Exception:
            traceback.print_exc()
            code = 1
        print(f"===== exit {code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
