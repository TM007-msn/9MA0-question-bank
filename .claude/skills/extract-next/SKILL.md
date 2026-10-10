---
name: extract-next
description: Extract the next paper in bank/progress.json into the question bank, with every check, then build its review sheet and stop. One paper per run. Use only when the user types /extract-next.
disable-model-invocation: true
argument-hint: "[approved]"
---

# /extract-next: extract ONE paper, then stop

Read CLAUDE.md first. Every rule there applies. This file is the order of work and the stop conditions. Never open, read, list or render anything in the mock-papers folder (`RESERVED_DIR` in `scripts/paths.py`, outside the project). A hook blocks shell commands containing the word "reserved", so keep it out of commands and commit messages (commit with `git commit -F <file>`).

All commands run from the project root with `.venv/Scripts/python.exe`. Set `PYTHONIOENCODING=utf-8`.

## 0. Pick the paper
- If the user passed `approved` (they've approved the paper in review): `python scripts/next_paper.py --approve`. Otherwise: `python scripts/next_paper.py`.
- If it exits 1 (a paper is still `in_review`, or nothing is left), **stop** and report its message. Never approve on the user's behalf.
- The JSON it prints is the paper: `paper`, `series`, `source_file`, `section`. Work on that paper only.

## 1. Marks check (before saving anything)
`python scripts/check_marks.py PAPER SERIES`
- **ok:** continue.
- **MISMATCH:** **stop.** Tell the user which questions disagree. The mark scheme may belong to another paper. Don't extract.
- **UNCHECKED, question paper is a scan:** render the pages (`scripts/render_pages.py`), read every "(Total for Question N is X marks)" line, and check they add up to the paper total on the cover. Record them in `bank/qp_totals_manual.json`, saying where each was read. Re-run the check.
- **UNCHECKED, question paper text layer unreadable** (garbled text, no totals parsed): treat it like a scan, adding `"text_layer": "unreadable"` and `paper_total` to its `qp_totals_manual.json` entry. A mark-scheme misprint or missing total found this way is **not** fixed silently: stop, show the user the evidence, and add a `bank/ms_corrections.json` entry only with their agreement.
- **UNCHECKED, text layout not parsed:** you may improve the parser in `scripts/check_marks.py`. Then run `python scripts/check_marks.py --all`. No pair that was `ok` before may change, and no `MISMATCH` may appear. If that can't be done cleanly, **stop** and explain.
- **UNCHECKED, mark scheme prints no total for a question:** if the parts' marks in the mark scheme add up exactly to the question paper's printed total, add a `bank/ms_corrections.json` entry yourself (`printed: null`, the `total`, the MS `page`, and a `reason` showing the parts adding up), re-run the check, and carry on. It appears in the review sheet header; list it in the summary. Stop instead if the parts don't add up to the question paper's total, if a printed total disagrees, or if the total can't be accounted for.
- **SPEC section** (`section` is A or B): check_marks.py can't yet check one section of a combined PDF. **Stop** and tell the user that per-section support is needed first.

## 2. Read the sources
- **Question paper** (`source/papers/<source_file>`): render each question page with `scripts/render_pages.py` and read it as an image. Text extraction garbles maths. Note each question's start page, every part's marks, and every figure. Re-render every figure page with `--figure` (200 dpi; add `--clip-bottom` to crop to the figure) and describe the figure from that render.
- **Mark scheme** (`source/mark-schemes/PAPER_SERIES_MS.pdf`): render every page with content and read each mark, AO, scheme line and note, and every alternative.
- **Examiner report** (`source/examiner-reports/PAPER_SERIES_ER.pdf`): text extraction is fine for prose. Render the passages where maths was garbled. If there's no report (SAM, SPEC, or missing), `examiner_notes`, `difficulty` and `difficulty_evidence` are all `null`.

## 3. Write the draft builder
Copy `extraction/_template.py` to `extraction/PAPER_SERIES.py` and fill it in. The fields follow CLAUDE.md:
- **Entries:** one per separately marked part. Use the id scheme in CLAUDE.md. `question_latex` repeats the shared stem. Figures are `[Figure N: …]` with `has_diagram: true`. Set `source_page` and `source_file`.
- **Topic and spec refs:** `topic` comes from `schemas/topics.json`. `spec_ref` uses refs from the entry's own qualification, main ref first, others from the same strand.
- **Mark scheme:** one main string per mark: `CODE (AO x.y): scheme line. Notes: …`. A multi-mark code (B2, M2, A2) is one string; the builder's check counts its value. Then every alternative the mark scheme labels as one ("Alt", "ALT", "Alternative(ly)", "Method N", a second scheme column or table, "Either … Or …" between two methods), as separate `ALT:` strings. Keep alternatives out of the main strings. Copy; never invent.
- **REPORT:** every examiner-report sentence for each question, in order, tagged with its part(s), or `None` for the whole question. Sentences that refer back ("this", "it", "these" …) get `{"ref": True}` or `{"ref": "opening words"}`. Sentences that contain those words but don't refer back get `{"ref": False}`. `er_notes.py` refuses to run until every one is marked.
- **RATINGS:** difficulty by judgement, using the rubric in CLAUDE.md. Read everything the report says about the question, and weight how most candidates did over a minority's errors. Each rating points at the one sentence it rests on. `None` only if the report says nothing usable.

Run `python extraction/PAPER_SERIES.py`. It writes `out/drafts/PAPER_SERIES.json`.

## 4. Check the maths independently
Recompute every final answer in the mark scheme (sympy, `fractions`, `statistics.NormalDist`). Kinematics uses only the five SUVAT equations. Don't assume statistical tables. Any disagreement goes in the summary under "odd". Don't change the mark scheme to match your answer.

## 5. Standalone check (before saving)
Go through every part after the first in each multi-part question and ask whether it can be answered from its own `question_latex`.
- **Show an earlier part** if this part needs a value, expression or equation that only that earlier part produces (e.g. the model's constants found in (a), the coordinates of $P$ found in (a), the radius found in (b), the expansion found in (a)), or if it says "Hence". Read the mark scheme's main method to see what the part actually uses.
- A "their (a)" follow-through note on its own isn't enough. Nor is an earlier part that is only one possible route, or a marking note such as "may be seen in (a)".
- Show the whole chain: if the earlier part itself needs another part, show that one too. Use the layout rules in CLAUDE.md (labels as printed, connective lead-ins with the part they introduce, info lines in paper order).
- Fix the builder, re-run it, and list in the summary any part where the call was borderline.

## 6. Save through the guard
`python scripts/add_entries.py out/drafts/PAPER_SERIES.json`
- It checks the schema, the figure rule, spec refs, `source_file`, difficulty evidence, the reserved list, the marks check and per-question mark totals, and refuses duplicate ids.
- If it refuses, fix the draft and run again. **Never** edit the guards, schemas or validate.py to make a draft pass.

## 7. Validate, test, review sheet
- `python scripts/validate.py`. Every file must be ok.
- `python -m unittest discover tests`. All must pass.
- `python scripts/build_review.py PAPER SERIES`. This writes `out/review/PAPER_SERIES_review.html`.

## 8. Commit
Commit `extraction/PAPER_SERIES.py`, `bank/questions.json`, `bank/progress.json`, and any `qp_totals_manual.json` or `check_marks.py` change. The message is "Extract PAPER SERIES (in review)" plus the counts, ending with the attribution line from the session instructions. Write the message to a file and use `git commit -F <file>`.

## 9. Summary, then STOP
Start with `python scripts/paper_summary.py PAPER SERIES` and report:
- **Entries added:** count and marks.
- **ALT lines:** count.
- **Nulls:** count, and which fields and why.
- **Difficulty spread:** easy / medium / hard / null.
- **Diagram questions:** the entries with `has_diagram: true`.
- **Least sure of:** the 3 entries you're least sure of, each with the reason. For example: a hard-to-read scan, a borderline difficulty call, an ambiguous spec ref, or a figure described from a sketch.
- **Anything odd:** e.g. mark scheme typos, report sentences that don't match the paper, answers you couldn't reproduce, layout fixes made to check_marks.py.
- The review sheet path.

Then stop. Don't start the next paper. The next run needs `/extract-next approved` once the user has approved this one.
