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
  - QUAL is `9MA0` (A level, papers 01–03) or `8MA0` (AS, papers 01–02).
  - SERIES is `YYYY-MM`, or `SAM` for sample assessment materials.
  - TYPE is `QP`, `MS` or `ER`. QP files go in `papers/`, MS in `mark-schemes/`, ER in `examiner-reports/`.
  - Examples: `9MA0-01_2023-06_QP.pdf`, `9MA0-01_SAM_QP.pdf`, `8MA0-02_2022-06_MS.pdf`.
- **Question ids:** `QUAL-0X_SERIES_Q<number><letter><roman>`. The number may be zero-padded, and the letter and roman numeral (i–x) are optional. Examples: `9MA0-01_2023-06_Q07bii`, `9MA0-02_SAM_Q03a`. The id must start with the entry's own `paper` and `series`. Generated ids are the anchor id plus `-A`, `-B` or `-C`.
- The regexes live in `scripts/naming.py` and are copied into `schemas/question.schema.json`. Change both together, then run the tests.
- **NEVER open, read, list the contents of or extract anything in `source/reserved/`.** Those are my mock papers. Scripts must skip that folder too.
- **Schemas:** every entry in `questions.json` must follow `schemas/question.schema.json`. Error entries follow `error.schema.json`. `generated.json` follows `generated.schema.json`, and `rejected.json` follows `rejected.schema.json` (generated fields plus `rejection_reason` and `rejected_on`, with `verified: false`). Run `python scripts/validate.py` after changing anything in `bank/`.
- **Kinematics:** use only the five SUVAT equations.
- **Statistics:** don't assume access to statistical tables. Use values given in the question or compute them directly.
- **Never invent mark scheme points or examiner comments.** If a value isn't in the source, it is `null`.
- **Generated questions** go into `generated.json` only after they pass verification (`verified: true`, with a `verified_on` date). Failed candidates go into `rejected.json`.
- **out/ is git-ignored**, so it may not exist. Any script that writes to `out/` must get its folder with `paths.ensure_out_dir("to-remarkable")` (or similar), which creates it if missing.
- **Python:** readable over clever. Add comments that explain any non-obvious step.

## Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover tests
```
