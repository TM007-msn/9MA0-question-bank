---
name: mark
description: Mark the newest returned worksheet in out/from-remarkable/ strictly against the bank's mark schemes, as an Edexcel examiner, then log the attempts after the user confirms. Use only when the user types /mark.
disable-model-invocation: true
argument-hint: "[FILE.pdf]"
---

# /mark: mark one returned worksheet

Read CLAUDE.md first; every rule there applies (above all: never invent mark scheme points, and never touch the mock-papers folder). All commands run from the project root with `.venv/Scripts/python.exe` and `PYTHONIOENCODING=utf-8`.

## 1. Prepare
Run `python scripts/mark_prep.py` (or `python scripts/mark_prep.py FILE.pdf` if the user named one). It picks the newest PDF in `out/from-remarkable/`, matches it by name to `out/sets/NAME.json`, renders every page to `out/marking/NAME/page-NN.png` and writes `out/marking/NAME/brief.md`.
- If it exits with an error (no PDF, no matching set, ids not in the bank), **stop** and report the message.
- If it says some ids are **already logged** since the set was built, tell the user and ask whether to go on before marking.

Read `brief.md`, then read every page image listed for each part. A part marked "not found" means reading every page for it. If handwriting is too small to read with confidence, re-render that page at 200 dpi (`python scripts/mark_prep.py FILE --dpi 200`) before calling anything unreadable.

## 2. Mark each part, strictly
You are an Edexcel examiner marking against the brief's mark scheme only. The scheme in the brief is the bank's copy of the official one; it is the whole of what can earn marks.

- **One method per part.** Decide which method the working follows: the main scheme or one ALT. Mark it wholly by that scheme. Never mix marks from different methods. If both are attempted and neither is crossed out, mark each and award the higher; if one is crossed out, mark the other (Edexcel: crossed-out work is marked only if it's the sole attempt).
- **A method not in the scheme** (no main or ALT line covers it) is not marked by you: flag the part "method not in the mark scheme" and leave it for the user. Don't invent equivalent marks.
- **Conventions:**
  - **M**: method, given for a correct method even with arithmetic slips.
  - **dM**: needs the M mark(s) it depends on.
  - **A**: accuracy; needs the M mark it follows, so M0 means A0.
  - **B**: independent.
  - **ft**: follow-through on “their” earlier value.
  - **cao**: correct answer only. **cso**: correct solution only, no errors anywhere.
  - **oe**: or equivalent. **awrt**: answer which rounds to.
  - **isw**: ignore subsequent working, so a correct answer followed by an incorrect simplification keeps the mark.
  - Apply the scheme's own Notes exactly.
- **Command words.** "Show that", "Using algebra", "Hence", "You must show your working": an answer without the required working scores no marks unless the scheme says so. A "show that" needs every step the scheme lists, ending at the printed result.
- **Multi-mark codes** (B2, M2, A2) are one line worth that many marks; their Notes say when a partial mark (e.g. B1) is given.
- **Quote the working for every mark, given or withheld.** Transcribe the exact line(s) the decision rests on, in quotes, with maths in `$…$` as written (keep the candidate's errors). For a withheld mark with nothing to quote, say what is missing ("no attempt at $b^2-4ac$").
- **Unreadable, not guessed.** If the work a mark depends on can't be read with confidence, the mark is "unreadable": don't award or withhold it. A part with any unreadable mark gets no score and no attempts row; list it at the end for the user to read out or re-export.
- **Blank part:** every mark withheld, quote "no working".

## 3. Tag each lost mark
Every withheld mark gets exactly one tag:
- **knowledge**: didn't know the fact, formula, result or technique needed (e.g. wrong log law, didn't know to use the discriminant).
- **method**: knew the topic but chose a wrong or incomplete approach, or left out a required step, justification or conclusion.
- **slip**: arithmetic, sign, copying or algebra error in an otherwise right method.
- **misread**: answered a different question from the one printed (wrong value copied from the question, wrong interval, wrong accuracy asked for).
- **time**: not reached or left unfinished for lack of time.

A mark lost only because a mark it depends on was lost (A0 after M0, dM0) takes the same tag as that mark, noted "(follows M1)". For a blank part, propose **time** if it's at or near the end with later parts also blank, otherwise **knowledge**, and say it's a guess for the user to confirm. The attempts.csv row holds one `error_type` per part: use the tag of the **earliest** lost mark in the scheme's order, since later losses usually follow from it. Full marks: blank `error_type`.

## 4. Show the results
Per part, a mark-by-mark table:

| Mark | Given | Working quoted | Tag |
|---|---|---|---|
| M1 (AO 3.1a) | ✓ | “$x^2+k^2x^2-6x+10kx+9=0$” | |
| A1 (AO 1.1b) | ✗ | “$(1+k^2)x^2+(10k+6)x+9=0$”: sign of $6x$ term | slip |

Mark the method used (main or ALT) above each table. Then a summary:

| # | Question id | Marks | Error type |
|---|---|---|---|

with the set's total and percentage, then the rows for `log/attempts.csv` in a code block, one per scored part, in the file's column order:

```
date,question_id,topic,marks_awarded,marks_total,error_type
```

- **date:** today, YYYY-MM-DD.
- **topic:** the entry's topic from the brief.
- **marks_total:** the entry's marks.

List separately any parts not scored (unreadable, or method not in the scheme), with why.

## 5. Confirm, then log
Ask the user (AskUserQuestion) whether to log the rows as shown, or say what to change. Never log before a yes. Apply any changes they give (marks, tags, date), show the changed rows again, and ask again.

On a yes:
1. Write the rows (header line plus rows) to `out/marking/NAME/attempts_rows.csv`.
2. Run `python scripts/log_attempt.py --csv out/marking/NAME/attempts_rows.csv`. It checks every row and writes nothing if one fails; if it refuses, show its message, fix the row with the user, and run it again.
3. Commit `log/attempts.csv` with the message "Log attempts: NAME (X/Y marks)", written to a file and committed with `git commit -F <file>`, ending with the attribution line from the session instructions. Then `git push` (CLAUDE.md: push after every commit).
4. Report what was logged, the commit hash, whether the push worked, and the parts left unscored.
