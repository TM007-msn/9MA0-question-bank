# 9MA0 question bank

Question bank for Edexcel A-level Maths (9MA0) and AS Maths (8MA0), built from
past papers, sample assessment materials, mark schemes and examiner reports.

## Layout
- `source/papers/`, `source/mark-schemes/`, `source/examiner-reports/`: past-paper PDFs.
- `source/reference/`: 9MA0 and 8MA0 specifications, formulae booklet, large data set.
- `source/inbox/`: new files waiting to be renamed and filed.
- Mock papers: **outside the project**, in `C:\Users\taylo\9MA0-reserved\` (set once as `RESERVED_DIR` in `scripts/paths.py`). **Off limits** (see below).
- `bank/`: `questions.json`, `errors.json`, `generated.json`, `rejected.json`, `progress.json`.
- `schemas/`: JSON Schemas for bank entries, plus `topics.json` (canonical topics and spec refs, built by `scripts/build_topics.py`; don't edit by hand).
- `out/to-remarkable/`, `out/from-remarkable/`: worksheets going to the reMarkable, and marked work coming back.
- `out/review/`: review sheets from `scripts/build_review.py PAPER SERIES`.
- Worksheets: `scripts/build_pdf.py SETFILE NAME` (SETFILE is a JSON list of ids) builds `NAME_questions.pdf` and `NAME_markscheme.pdf` in `out/to-remarkable/` with Tectonic, from `templates/*.tex`. `--check-all` compiles every bank entry and lists failures; run it after changing LaTeX in `bank/` or the templates. `scripts/quick_set.py [--marks 50]` picks a set from approved papers using `bank/covered_topics.json` (refs by qualification and strand) and builds it; `--send` also uploads the questions PDF to the tablet (see "reMarkable upload" under Setup). `--pool as-pure` (all done 8MA0-01 entries) or `--pool alevel-pure` (all done 9MA0-01 and 9MA0-02 entries) ignores covered topics, re-tests and attempts.csv, and avoids repeats with `out/sets/sent_history.json` (updated only after a successful `--send`; least recently sent are reused once the pool runs out).
- Daily sheets: `scripts/drill.py` builds a ~25-mark SymPy algebra drill (`drill-YYYY-MM-DD_questions.pdf` and `_answers.pdf`, seeded by the date). `scripts/daily.py [--send]` builds the drill and an exam sheet `exam-YYYY-MM-DD` (50 marks, pool `as-pure` until 2026-11-14, `alevel-pure` from 2026-11-15) and sends both questions PDFs, never answers or mark schemes. It appends its output to `log/daily.log` (git-ignored). Windows Task Scheduler task "9MA0 daily sheets" runs `daily.py --send` at 06:30 daily, waking the computer.
- Marking: `/mark` (the skill in `.claude/skills/mark/`) marks the newest PDF in `out/from-remarkable/` against the bank's mark schemes and logs the attempts after I confirm. `scripts/mark_prep.py` matches it to `out/sets/NAME.json` by name and writes page images and `brief.md` to `out/marking/NAME/`.
- `log/attempts.csv`: one row per attempt: `date,question_id,topic,marks_awarded,marks_total,error_type`. Add rows only through `scripts/log_attempt.py`, which checks them (error types: knowledge, method, slip, misread, time).
- Practice loop (worked example in README.md): `scripts/cover_topic.py` edits `bank/covered_topics.json`, `scripts/weak_topics.py` ranks covered refs by marks lost and lists re-tests due. `scripts/covered.py` reads the covered-topics file for all of them.
- `extraction/`: one draft-builder script per extracted paper (from `_template.py`).
- `scripts/`: Python tools. `naming.py` holds the naming regexes, `paths.py` the shared paths.
- `tests/`: unit tests (`python -m unittest discover tests`). `templates/`: output templates.

## Rules
- **File naming:** `QUAL-0X_SERIES_TYPE.pdf`
  - QUAL is `9MA0` (A level) or `8MA0` (AS).
  - 9MA0 papers are 01, 02 and 03. From 2019 onwards Paper 3 is sat as two papers: `31` (Statistics) and `32` (Mechanics). June 2018, SAM and SPEC have a single `03`.
  - 8MA0 papers are 01 and 02. From 2019 onwards Paper 2 is sat as two papers: `21` (Statistics) and `22` (Mechanics). June 2018, SAM and SPEC have a single `02`.
  - SERIES is `YYYY-MM`, `SAM` for sample assessment materials, or `SPEC` for the separate specimen set.
  - TYPE is `QP`, `MS` or `ER`. QP files go in `papers/`, MS in `mark-schemes/`, ER in `examiner-reports/`.
  - Examples: `9MA0-01_2023-06_QP.pdf`, `9MA0-01_SAM_QP.pdf`, `9MA0-31_2022-06_MS.pdf`, `8MA0-02_2022-06_MS.pdf`.
- **Question ids:** `QUAL-0X_SERIES_Q<number><letter><roman>`. The number may be zero-padded, and the letter and roman numeral (i–x) are optional. When the paper numbers a part roman-then-letter, e.g. 12(ii)(a), the id follows that order: `Q12iia`. Examples: `9MA0-01_2023-06_Q07bii`, `9MA0-02_SAM_Q03a`, `9MA0-32_2022-06_Q04`, `8MA0-01_2021-10_Q12iia`. The id must start with the entry's own `paper` and `series`. Generated ids are the anchor id plus `-A`, `-B` or `-C`.
- The regexes live in `scripts/naming.py` and are copied into `schemas/question.schema.json`. Change both together, then run the tests.
- **NEVER open, read, list the contents of or extract anything in the mock-papers folder (`RESERVED_DIR`, `C:\Users\taylo\9MA0-reserved\`).** Those are my mock papers. Scripts may only write new files there (fetch_materials.py) and must never read from it. Guards:
  - the folder is outside the project;
  - `.claude/settings.json` denies Read/Edit on it;
  - a PreToolUse hook (`.claude/hooks/guard_mock_papers.py`) blocks any Bash or PowerShell command whose text contains "reserved", in any case. So keep that word out of shell commands, including commit messages (use `git commit -F <file>`).
  - Never weaken or bypass these guards.
- **Git:** push after every commit (`git push`; `master` tracks `origin`, the private GitHub repo TM007-msn/9MA0-question-bank). Never force-push. Before committing, check nothing under `out/` and nothing under `source/` except `.gitkeep` is staged.
- **Schemas:** every entry in `questions.json` must follow `schemas/question.schema.json`. Error entries follow `error.schema.json`. `generated.json` follows `generated.schema.json`, and `rejected.json` follows `rejected.schema.json` (generated fields plus `rejection_reason` and `rejected_on`, with `verified: false`). Run `python scripts/validate.py` after changing anything in `bank/`.
- **Kinematics:** use only the five SUVAT equations.
- **Statistics:** don't assume access to statistical tables. Use values given in the question or compute them directly.
- **Never invent mark scheme points or examiner comments.** If a value isn't in the source, it is `null`.
- **Generated questions** go into `generated.json` only after they pass verification (`verified: true`, with a `verified_on` date). Failed candidates go into `rejected.json`.
- **out/ is git-ignored**, so it may not exist. Any script that writes to `out/` must get its folder with `paths.ensure_out_dir("to-remarkable")` (or similar), which creates it if missing.
- **Python:** readable over clever. Add comments that explain any non-obvious step.

## Reserved mocks
These series are in the mock-papers folder (`RESERVED_DIR`) and are **never** opened, read or extracted. They are not in the question bank and must not be used to generate questions. `RESERVED_SERIES` in `scripts/fetch_materials.py` must match this table.

| Qualification | Series | Papers (QP + MS + ER each) |
|---|---|---|
| 9MA0 | June 2023 (`2023-06`) | 9MA0-01, 9MA0-02, 9MA0-31, 9MA0-32 |
| 9MA0 | June 2024 (`2024-06`) | 9MA0-01, 9MA0-02, 9MA0-31, 9MA0-32 |
| 9MA0 | June 2025 (`2025-06`) | 9MA0-01, 9MA0-02, 9MA0-31, 9MA0-32 |
| 8MA0 | June 2025 (`2025-06`) | 8MA0-01, 8MA0-21, 8MA0-22 |

## Fetching materials
`python scripts/fetch_materials.py` shows the plan and coverage grid. Add `--download` to fetch. It uses Pearson for files Pearson lists as public and PMT for everything else. It never downloads anything Pearson's past-papers page shows with a padlock (files stored under `/content/dam/secure/`, centre login required), and it stops if a site refuses scripted requests. Gaps are written to `log/missing.csv`. Files from a teacher go in `source/inbox/` first, then get renamed and filed.

## Extracting a paper
- Run `/extract-next` (the skill in `.claude/skills/extract-next/`) to extract the next queued paper. It does one paper per run and stops at the review. After you approve, run `/extract-next approved`. Helpers: `scripts/next_paper.py` (picks the paper, enforces one-in-review), `scripts/render_pages.py` (pages as images, refuses the mock-papers folder), `extraction/_template.py` (draft builder, copied to `extraction/PAPER_SERIES.py` per paper), and `scripts/paper_summary.py` (counts for the summary).
- Work through `bank/progress.json` in queue order. Stop after each paper whose status becomes `in_review` until I've reviewed it.
- Run `python scripts/check_marks.py PAPER SERIES` first. Only `ok` allows extraction. If it says `MISMATCH`, stop and tell me: the mark scheme probably belongs to a different paper. If it says `UNCHECKED`, fix the parser for that layout (or check by hand with me) before going on.
- Scanned question papers (no text layer, e.g. 9MA0-31/32 2019-06) can't be parsed. Read their "Total for Question N is X marks" lines from the page images and record them, with where they were read, in `bank/qp_totals_manual.json`. check_marks.py uses those only for scans, and still compares them against the mark scheme it parses.
- A question paper whose text layer is unreadable (fonts with no character mapping, e.g. 8MA0-01 SAM) is treated like a scan: record its hand-read totals with `"text_layer": "unreadable"`. These apply only when no "Total for Question" line can be parsed. Every hand-read entry needs `paper_total`, read from the paper, and the totals must add up to it, or the check fails.
- A misprinted or missing question total in a mark scheme goes in `bank/ms_corrections.json`, with what the parser reads (`printed`, or null), the true `total`, the MS `page` and the `reason`. A correction only applies while the PDF still reads as recorded. Only add one when the question paper's total and the mark scheme's own marks show it is a misprint, and tell me. Standing rule for a missing total: if the mark scheme prints no total for a question and its parts' marks add up exactly to the question paper's printed total, add the correction yourself (`printed: null`), let the review sheet header show it, list it in the summary, and carry on without stopping. Still stop for any real `MISMATCH`, any printed total that disagrees, or any total you can't account for. A mark-scheme row left out of the bank (e.g. a duplicated row printed under the wrong part) goes in the same file under `omitted_rows`, with the question, MS `page`, the `row` as printed and the `reason`; it changes no total. check_marks.py prints every override and omitted row, and the review sheet lists them at the top.
- Make one entry per separately marked part, e.g. `Q06c` covers 6(c)(i) and (ii) when they share one mark allocation. `question_latex` repeats the shared stem, so each entry stands alone.
- Describe figures in `question_latex` as `[Figure N: ...]`. Any entry with one must have `has_diagram: true` (validate.py enforces this). Read every figure from a 200 dpi render (`scripts/render_pages.py PDF PAGE --figure`, adding `--clip-bottom` to crop to the figure), never from the lower-dpi text render, so curve shapes and dashed or solid edges are described correctly.
- **"As printed" means the page image** whenever the text layer looks garbled (stray or missing symbols, overlapping glyphs, mangled maths). Re-render the passage at 200 dpi (`scripts/render_pages.py PDF PAGE --figure`, adding `--clip-bottom` to crop) and record what the image shows, even if the text layer holds characters the image hides.
- `source_file` is the question paper the entry comes from, and `source_page` is the page in that file where the question starts.
- `mark_scheme`: one string per mark of the main method, `CODE (AO x.y): scheme line. Notes: ...`, copied from the mark scheme. Exception: a multi-mark code (B2, M2, A2) is one string, and the marks check counts its value (`scripts/mark_codes.py`), so a B2 line counts as 2 marks. Then every alternative the mark scheme lists, as separate strings starting `ALT:`, one per mark. An alternative is anything the mark scheme labels as one: "Alt", "ALT", "Alternative(ly)", "Method N", a second scheme column or table, or "Either … Or …" between two methods. Keep alternatives out of the main strings.
- `examiner_notes`: sentences copied from the examiner report, in report order. A sentence about the whole question goes on every part. A sentence that names one or more parts goes only on those parts. Never paraphrase either field into new claims. Tag each report sentence with its part(s) and apply it with `scripts/er_notes.py`. If a sentence refers back to another ("this", "it", "these"), mark it with `ref` so the sentence it refers to goes with it. er_notes.py refuses to run until every sentence containing those words has been checked.
- **Examiner report errors:** when a report sentence is wrong about the paper (e.g. a wrong number), keep the sentence verbatim and mark it with `{"note": "..."}` in REPORT. er_notes.py appends ` [sic: ...]` after it in `examiner_notes`, e.g. "… dividing by 9 … [sic: the stone moves for 4 seconds and the mark scheme divides by 4]", so nothing built from the notes repeats the wrong value. The note says only what the question paper or mark scheme shows. `difficulty_evidence` stays the report's own sentence without the note (validate.py enforces this).
- `topic`: a name from `schemas/topics.json`, which uses the A level names for both qualifications.
- `spec_ref`: refs from the entry's own qualification's specification, comma-separated, main ref first. The first ref must belong to the topic, and the others must come from the same strand (pure, statistics or mechanics).
- Spec statement labels in `topics.json` come from the PDF text, except that statements with maths (or garbled text) use the hand-written LaTeX in `schemas/spec_labels.json`. When a spec statement's label looks garbled, add it there and rerun `scripts/build_topics.py`.
- `difficulty`: a judgement, made after reading everything the examiner report says about the question (its whole-question sentences and the sentences on every part). Use the rubric below.
- `difficulty_evidence`: the one sentence the rating rests on, copied exactly from the entry's `examiner_notes`. It's `null` only when `difficulty` is `null`, i.e. when the report says nothing usable about the part. Never guess a rating without evidence.

### Difficulty rubric
Wording is a guide, not a lookup:
- **easy:** most candidates scored all or most of the marks ("well done", "accessible", "well answered", "most candidates scored both marks", "almost universally correct").
- **medium:** most candidates got some of the marks but commonly lost others, or results were mixed ("mixed", "some candidates", "usually gained the first mark but …", "often lost the final mark").
- **hard:** most candidates scored few or none of the marks, or the report calls it demanding ("demanding", "challenging", "few candidates", "limited success", "poorly done", "many left it blank").

Weighting:
- Rate by how many candidates **completed** the part, not by how many earned its early method marks. "Most got the first marks but few finished" is **hard**. The line between medium and hard is how many finished: "often lost the final mark" (many still finished) is medium; "few finished", "rarely completed" or "few reached the answer" is hard, however many earned the opening marks. Many or most candidates losing only the final mark is **medium**; "many not finishing" means failing before the answer, not dropping the last mark.
- Quantity words: “most”, “the majority”, “almost all”, “generally” or “usually” doing well is **easy**; “many” doing well is **medium**; “many” scoring nothing or not finishing is **hard**.
- Sentences about how most candidates did outweigh comments about a minority's errors. "A few students used x = 2" doesn't make a part hard.
- Sentences about the part itself outweigh the whole-question summary. Use the summary when the report says little about the part.
- Prefer a sentence about the part as evidence. Use a whole-question sentence only if it's the best basis.

- Save only through `python scripts/add_entries.py draft.json`. It checks the schema, the reserved list, the marks check and per-question mark totals, and rejects duplicate ids.
- SPEC combined papers restart their numbering in Section B. Their sections are filed under the split codes: 9MA0-03 SPEC becomes 9MA0-31 (Section A) and 9MA0-32 (Section B), and 8MA0-02 SPEC becomes 8MA0-21 and 8MA0-22. `source_file` stays the combined PDF, e.g. `9MA0-03_SPEC_QP.pdf`. The 2018 and SAM combined papers number straight through and keep 03 / 02.
- After saving, build the review sheet (`python scripts/build_review.py PAPER SERIES`) and stop. To redo a paper that's in review, use `add_entries.py --replace`. To change a paper that's already done (e.g. after a rule change), use `add_entries.py --replace-approved "reason"`: every save check still runs, the paper stays done, and the reason and changed fields are recorded in its `history` in `progress.json`.
- **question_latex content and order:** each entry stands alone and follows the paper's order:
  - **Shared stem first:** all text printed before this part that isn't another part (the question's opening and any text between earlier parts), with its paragraph breaks kept as `\n`.
  - **Connective lead-ins go on the next part only:** only a connective fragment ending in a comma, such as "Using the model,", "Find, according to the model," or "From the instant when the tyre developed the puncture,", goes on the next part alone. Full sentences that give information (data, a model, a value, a condition) stay on every later part, as printed on the paper, e.g. "Given that the company made an annual profit of more than £80 000", "A random sample of 200 bottles is taken." and "Given the model predicts that the value of the car is decreasing at a rate of £500 per year at the instant when $t=T$,". When the part a connective introduces is shown as an earlier part, the connective goes with it. Exception: when the lead-in carries the command word and the parts below it each complete that sentence (e.g. "Find, according to the model," then "(a) the temperature of the cup of tea …", "(b) the value of $t$ …"), the lead-in goes on every part it completes, so no part loses its command word. Where leaving out a connective makes a part start with a lower-case word (e.g. "deduce the maximum total mass …"), capitalise that first word ("Deduce …"). Lines that continue a sentence printed just above them ("where $k$ is a constant.", "giving your answer …") keep the paper's case.
  - **Earlier parts only when this part depends on them:** when its wording refers back ("Hence", "your answer to part (a)", "the value found in part (b)", "using this value of a"), or it uses a result stated only in that part (e.g. a "show that" equation). Each goes on its own line(s), starting with its label as printed, e.g. `(a) Show that …`. Include the whole chain: if (c) needs (b) and (b) says "Hence" from (a), include (a) and (b). This part then starts with its own label too; with no earlier parts shown it has no label.
  - **The paper's wording, punctuation and line breaks:** one line per printed line or paragraph (sentences that merely wrap at the page edge are joined); displayed maths as its own `$$…$$` line; bullet points as `• ` lines; sub-parts (i), (ii) on their own lines. Copy the paper's punctuation exactly, including where it has none. Bold instruction lines are plain text; a single emphasised word may be `$\textbf{not}$`.
  - **Figures where they are printed:** the `[Figure N: …]` line goes at the position the figure has in the paper (e.g. before the text that refers to it, or between parts).
- **Quote marks and LaTeX that renders:** in every field, quotes are curly: “…” in plain text and `\text{“}…\text{”}` in maths (e.g. a mark scheme's "their" value `\text{“}10\text{”}`). Never write `\"`, which is an umlaut command, or any other LaTeX command outside `$…$`, since it prints literally. Degrees are `$35^\circ$C`, never `\,^\circ` with nothing before it. validate.py render-checks every LaTeX string in every bank file with KaTeX 0.16.11, the same version and delimiters as the review sheet, and fails if any string doesn't render.
- **question_latex layout:** multi-line working goes in one `$$\begin{aligned}...\end{aligned}$$` block, with explanations in `\text{...}`. `\quad`, `\qquad` and `\\` are only allowed inside maths; outside it they print literally. validate.py enforces this.

## Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
npm install                 # KaTeX for validate.py's render check (needs Node.js)
                            # Tectonic on PATH for build_pdf.py (tectonic-typesetting.github.io)
python scripts/validate.py
python -m unittest discover tests
```

### reMarkable upload
`python scripts/quick_set.py --send` builds a set and uploads its questions PDF to the "Maths practice" folder on the tablet; `python scripts/send_remarkable.py NAME` sends a set that's already built. Both use `scripts/send_remarkable.py`, which:
- sends only `NAME_questions.pdf`, **never the mark scheme**;
- creates "Maths practice" if it's missing;
- never overwrites (no `--force`, which would delete handwriting on the tablet copy): if a document with that name is already there, it stops, so rename the set or delete the old one on the tablet.

One-time setup on Windows:
1. Install rmapi from the maintained fork, https://github.com/ddvk/rmapi (juruen/rmapi is archived). Download `rmapi-win64.zip` from the latest release, check its SHA-256 against the digest on the release page, and put `rmapi.exe` in `C:\Users\taylo\.local\bin` (already on PATH). Installed: v0.0.35.
2. Pair it: open https://my.remarkable.com/device/browser/connect, get the 8-letter one-time code, run `rmapi` in a terminal and enter the code, then type `exit`. The token is saved in `%APPDATA%\rmapi\rmapi.conf`; nothing else needs a login.
3. Check: `rmapi ls /` lists the tablet's top-level folders. In Git Bash, run `export MSYS_NO_PATHCONV=1` first, or Git Bash turns `/` into `C:/Program Files/Git/` (send_remarkable.py isn't affected).

Pairing needs a real terminal window: a command run with Claude Code's `!` prefix gets no keyboard input, so rmapi just repeats its code prompt.

An unpaired rmapi asks for a code and, with no input, repeats the question forever, so send_remarkable.py checks for the token first and runs rmapi with stdin closed and a timeout. If the cloud rejects the saved login, rmapi clears it itself (`rmapi.conf` is left with `devicetoken: ""`) and the upload fails with a pairing reminder: pair again, then send the already-built set with `python scripts/send_remarkable.py NAME`. This happened once on 2026-10-15, twelve minutes after pairing. Re-pairing with a code from the **browser/connect** page (https://my.remarkable.com/device/browser/connect, the one rmapi's prompt names) worked, and the login held through the next upload.
