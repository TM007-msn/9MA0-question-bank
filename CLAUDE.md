# 9MA0 question bank

Question bank for Edexcel A-level Maths (9MA0) and AS Maths (8MA0), built from
past papers, sample assessment materials, mark schemes and examiner reports.

## Layout
- `source/papers/`, `source/mark-schemes/`, `source/examiner-reports/`: past-paper PDFs.
- `source/reference/`: 9MA0 and 8MA0 specifications, formulae booklet, large data set.
- `source/inbox/`: new files waiting to be renamed and filed.
- `source/reserved/`: **off limits** (see below).
- `bank/`: `questions.json`, `errors.json`, `generated.json`, `rejected.json`, `progress.json`.
- `schemas/`: JSON Schemas for bank entries, plus `topics.json` (canonical topics and spec refs, built by `scripts/build_topics.py`; don't edit by hand).
- `out/to-remarkable/`, `out/from-remarkable/`: worksheets going to the reMarkable, and marked work coming back.
- `out/review/`: review sheets from `scripts/build_review.py PAPER SERIES`.
- `log/attempts.csv`: one row per attempt: `date,question_id,topic,marks_awarded,marks_total,error_type`.
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
- **Question ids:** `QUAL-0X_SERIES_Q<number><letter><roman>`. The number may be zero-padded, and the letter and roman numeral (i–x) are optional. Examples: `9MA0-01_2023-06_Q07bii`, `9MA0-02_SAM_Q03a`, `9MA0-32_2022-06_Q04`. The id must start with the entry's own `paper` and `series`. Generated ids are the anchor id plus `-A`, `-B` or `-C`.
- The regexes live in `scripts/naming.py` and are copied into `schemas/question.schema.json`. Change both together, then run the tests.
- **NEVER open, read, list the contents of or extract anything in `source/reserved/`.** Those are my mock papers. Scripts must skip that folder too.
- **Schemas:** every entry in `questions.json` must follow `schemas/question.schema.json`. Error entries follow `error.schema.json`. `generated.json` follows `generated.schema.json`, and `rejected.json` follows `rejected.schema.json` (generated fields plus `rejection_reason` and `rejected_on`, with `verified: false`). Run `python scripts/validate.py` after changing anything in `bank/`.
- **Kinematics:** use only the five SUVAT equations.
- **Statistics:** don't assume access to statistical tables. Use values given in the question or compute them directly.
- **Never invent mark scheme points or examiner comments.** If a value isn't in the source, it is `null`.
- **Generated questions** go into `generated.json` only after they pass verification (`verified: true`, with a `verified_on` date). Failed candidates go into `rejected.json`.
- **out/ is git-ignored**, so it may not exist. Any script that writes to `out/` must get its folder with `paths.ensure_out_dir("to-remarkable")` (or similar), which creates it if missing.
- **Python:** readable over clever. Add comments that explain any non-obvious step.

## Reserved mocks
These series are in `source/reserved/` and are **never** opened, read or extracted. They are not in the question bank and must not be used to generate questions. `RESERVED_SERIES` in `scripts/fetch_materials.py` must match this table.

| Qualification | Series | Papers (QP + MS + ER each) |
|---|---|---|
| 9MA0 | June 2023 (`2023-06`) | 9MA0-01, 9MA0-02, 9MA0-31, 9MA0-32 |
| 9MA0 | June 2024 (`2024-06`) | 9MA0-01, 9MA0-02, 9MA0-31, 9MA0-32 |
| 9MA0 | June 2025 (`2025-06`) | 9MA0-01, 9MA0-02, 9MA0-31, 9MA0-32 |
| 8MA0 | June 2025 (`2025-06`) | 8MA0-01, 8MA0-21, 8MA0-22 |

## Fetching materials
`python scripts/fetch_materials.py` shows the plan and coverage grid. Add `--download` to fetch. It uses Pearson for files Pearson lists as public and PMT for everything else. It never downloads anything Pearson's past-papers page shows with a padlock (files stored under `/content/dam/secure/`, centre login required), and it stops if a site refuses scripted requests. Gaps are written to `log/missing.csv`. Files from a teacher go in `source/inbox/` first, then get renamed and filed.

## Extracting a paper
- Work through `bank/progress.json` in queue order. Stop after each paper whose status becomes `in_review` until I've reviewed it.
- Run `python scripts/check_marks.py PAPER SERIES` first. Only `ok` allows extraction. If it says `MISMATCH`, stop and tell me: the mark scheme probably belongs to a different paper. If it says `UNCHECKED`, fix the parser for that layout (or check by hand with me) before going on.
- Make one entry per separately marked part, e.g. `Q06c` covers 6(c)(i) and (ii) when they share one mark allocation. `question_latex` repeats the shared stem, so each entry stands alone.
- Describe figures in `question_latex` as `[Figure N: ...]`. Any entry with one must have `has_diagram: true` (validate.py enforces this).
- `source_file` is the question paper the entry comes from, and `source_page` is the page in that file where the question starts.
- `mark_scheme`: one string per mark of the main method, `CODE (AO x.y): scheme line. Notes: ...`, copied from the mark scheme. Then every alternative the mark scheme lists, as separate strings starting `ALT:`, one per mark. An alternative is anything the mark scheme labels as one: "Alt", "ALT", "Alternative(ly)", "Method N", a second scheme column or table, or "Either … Or …" between two methods. Keep alternatives out of the main strings.
- `examiner_notes`: sentences copied from the examiner report, in report order. A sentence about the whole question goes on every part. A sentence that names one or more parts goes only on those parts. Never paraphrase either field into new claims.
- `topic`: a name from `schemas/topics.json`, which uses the A level names for both qualifications.
- `spec_ref`: refs from the entry's own qualification's specification, comma-separated, main ref first. The first ref must belong to the topic, and the others must come from the same strand (pure, statistics or mechanics).
- Spec statement labels in `topics.json` come from the PDF text, except that statements with maths (or garbled text) use the hand-written LaTeX in `schemas/spec_labels.json`. When a spec statement's label looks garbled, add it there and rerun `scripts/build_topics.py`.
- `difficulty`: set by `scripts/difficulty.py` from the examiner report's wording, using the mapping below. Never set it by judgement.

### Difficulty mapping
Phrases (case-insensitive, whole words):
- **easy:** “well done”, “done well”, “well answered”, “accessible”, “well prepared”, “good source of marks”, “good starting question”, “good solutions”, “was more successful”, “much more successful”, “many scoring full marks”, “many gained all marks”, “scored full marks”
- **medium:** “mixed”, “varying success”, “some success”, “some candidates”, “some students”, “at least one mark”
- **hard:** “demanding”, “challenge”, “difficult”, “very few”, “few candidates”, “few students”, “few responses”, “few then”, “rare”, “rarely”, “limited success”, “less well”, “less so”, “struggled”, “disappointing”, “lacking”, “unable to”, “only more able”, “significant hurdle”, “frequently lost”

Exceptions: "a few students/candidates/responses" (a minority error) doesn't count as "few", and "less well done" isn't "well done".

For each part:
1. Use the report sentences about that part, including sentences that name it alongside other parts. When one sentence judges parts differently ("Part (a) was very accessible, part (b) less so"), each part uses only its own clause.
2. Easy and hard phrases both present → medium. Otherwise: any hard phrase → hard, then any easy phrase → easy, then any medium phrase → medium.
3. No phrases found → apply step 2 to the sentences about the whole question.
4. Still nothing (or no report) → `null`.

The phrase lists in this section and in `scripts/difficulty.py` must match.
- Save only through `python scripts/add_entries.py draft.json`. It checks the schema, the reserved list, the marks check and per-question mark totals, and rejects duplicate ids.
- SPEC combined papers restart their numbering in Section B. Their sections are filed under the split codes: 9MA0-03 SPEC becomes 9MA0-31 (Section A) and 9MA0-32 (Section B), and 8MA0-02 SPEC becomes 8MA0-21 and 8MA0-22. `source_file` stays the combined PDF, e.g. `9MA0-03_SPEC_QP.pdf`. The 2018 and SAM combined papers number straight through and keep 03 / 02.
- After saving, build the review sheet (`python scripts/build_review.py PAPER SERIES`) and stop. To redo a paper that's in review, use `add_entries.py --replace`.

## Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover tests
```
