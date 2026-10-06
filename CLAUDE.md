# 9MA0 question bank

Question bank for Edexcel A-level Maths (9MA0) and AS Maths (8MA0), built from
past papers, sample assessment materials, mark schemes and examiner reports.

## Layout
- `source/papers/`, `source/mark-schemes/`, `source/examiner-reports/`: past-paper PDFs.
- `source/reference/`: spec, formula booklet and similar.
- `source/inbox/`: new files waiting to be renamed and filed.
- `source/reserved/`: **off limits** (see below).
- `bank/`: `questions.json`, `errors.json`, `generated.json`, `rejected.json`, `progress.json`.
- `schemas/`: JSON Schemas for bank entries.
- `out/to-remarkable/`, `out/from-remarkable/`: worksheets going to the reMarkable, and marked work coming back.
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

## Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover tests
```
