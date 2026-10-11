# 9MA0 question bank

Past-paper questions for Edexcel A level Maths (9MA0) and AS Maths (8MA0),
with mark schemes and examiner comments, plus tools to turn them into
practice sets for the reMarkable and track how they went. Setup and the
rules for extracting papers are in [CLAUDE.md](CLAUDE.md).

## Practice loop

| Step | Script | Reads / writes |
|---|---|---|
| Mark a spec ref as taught | `scripts/cover_topic.py` | `bank/covered_topics.json` |
| Build a set | `scripts/quick_set.py` (or `scripts/build_pdf.py SETFILE NAME`) | `out/to-remarkable/` |
| Log the marked work | `scripts/log_attempt.py` | `log/attempts.csv` |
| See what to work on | `scripts/weak_topics.py` | reads both |

Error types for marks lost: `knowledge` (didn't know the content),
`method` (wrong approach), `slip` (careless error), `misread` (misread the
question) and `time` (ran out of time).

## Worked example

Run from the project root with the venv active. The output below is real,
from a run with today as 11 October 2026.

**1. Mark what has been taught.** Refs are given by qualification, strand
and ref, because the statistics and mechanics numbers repeat the pure ones.
The script prints the statement from the specification and asks before
adding it:

```
> python scripts/cover_topic.py 8MA0 pure 2.1
8MA0 pure 2.1  (Algebra and functions)
  Statement:
    Understand and use the laws of indices for all rational exponents.

Add 8MA0 pure 2.1 to covered_topics.json? [y/N] y
Added 8MA0 pure 2.1 to covered_topics.json.
```

A bare topic number covers the whole topic (`python scripts/cover_topic.py
9MA0 pure 7`). `python scripts/cover_topic.py --list 9MA0 mechanics` shows
every ref in a strand with `[x]` against the covered ones.

**2. Build a set.** `python scripts/quick_set.py --marks 20` puts in any
re-tests that are overdue or due today (see step 4) first, then fills up
with parts whose refs are all covered, medium and hard first, skipping
anything attempted in the last 21 days. It writes the question sheet and mark
scheme PDFs to `out/to-remarkable/`. Each question carries its bank id in
small print, for logging.

**3. Log the marked work.** Paste rows (`--csv`, then Ctrl+Z Enter), or
run without `--csv` to be asked for each one. Leave `topic` blank to fill
it from the bank, and `error_type` blank for full marks:

```
> python scripts/log_attempt.py --csv
2026-10-02,9MA0-01_2022-06_Q08b,,3,4,slip
2026-10-03,8MA0-01_2019-06_Q02i,,2,4,knowledge
2026-10-06,9MA0-02_2019-06_Q14c,,3,7,method
2026-10-06,9MA0-02_2022-06_Q14c,,2,2,
2026-10-09,9MA0-01_2019-06_Q05c,,1,4,misread
^Z
  2026-10-02  9MA0-01_2022-06_Q08b       3/4  slip
  ...
Added 5 row(s) to attempts.csv
```

Nothing is written if any row fails a check, e.g.:

```
Nothing written:
  row 2: error_type 'carelessness' must be one of knowledge, method, slip, misread, time when marks were lost
  row 3: marks_total 5 is not 8MA0-01_2019-06_Q02i's 4 marks
```

**4. See what to work on.** (This log also had a 1/4 at
9MA0-01_2022-06_Q08b on 20 September.)

```
> python scripts/weak_topics.py
Weak spec refs, last 14 days (to 2026-10-11):
  Ref                  Lost Avail Dropped  Main error  Topic
  9MA0 pure 8.7           4     7     57%  method      Integration
  9MA0 pure 2.9           3     4     75%  misread     Algebra and functions
  8MA0 pure 2.1           2     4     50%  knowledge   Algebra and functions
  9MA0 pure 7.4           1     4     25%  slip        Differentiation
  9MA0 pure 8.8           0     2      0%  -           Integration

Re-tests due (overdue, or within 7 days):
  2026-10-09  overdue 2d  9MA0-01_2022-06_Q08b        7-day re-test of 2026-10-02 (lost 1/4)  Differentiation
  2026-10-10  overdue 1d  8MA0-01_2019-06_Q02i        7-day re-test of 2026-10-03 (lost 2/4)  Algebra and functions
  2026-10-11  today       9MA0-01_2022-06_Q08b       21-day re-test of 2026-09-20 (lost 3/4)  Differentiation
  2026-10-13  in 2d       9MA0-02_2019-06_Q14c        7-day re-test of 2026-10-06 (lost 4/7)  Integration
  2026-10-16  in 5d       9MA0-01_2019-06_Q05c        7-day re-test of 2026-10-09 (lost 3/4)  Algebra and functions
```

Each attempt counts towards its question's main (first) spec ref. The
20 September attempt is outside the 14 days, so it doesn't count in the
table, but it still has a 21-day re-test due. Its 7-day re-test was done
by the 2 October attempt. `--days 28` widens the window.

## Tests

```
python -m unittest discover tests
```
