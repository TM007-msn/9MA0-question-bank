# 9MA0 question bank

Question bank for Edexcel A-level Maths (9MA0), built from past papers, mark
schemes and examiner reports.

## Layout
- `source/papers/`, `source/mark-schemes/`, `source/examiner-reports/`: past-paper PDFs.
- `source/reference/`: spec, formula booklet and similar.
- `source/inbox/`: new files waiting to be renamed and filed.
- `source/reserved/`: **off limits** (see below).
- `bank/`: `questions.json`, `errors.json`, `generated.json`, `rejected.json`, `progress.json`.
- `schemas/`: JSON Schemas for bank entries.
- `out/to-remarkable/`, `out/from-remarkable/`: worksheets going to the reMarkable, and marked work coming back.
- `log/attempts.csv`: one row per attempt: `date,question_id,topic,marks_awarded,marks_total,error_type`.
- `scripts/`: Python tools. `templates/`: output templates.

## Rules
- **File naming:** `9MA0-0X_YYYY-MM_TYPE.pdf`, where X is the paper (1–3), YYYY-MM is the series, and TYPE is `QP`, `MS` or `ER`. Example: `9MA0-01_2023-06_QP.pdf`.
- **NEVER open, read, list the contents of or extract anything in `source/reserved/`.** Those are my mock papers. Scripts must skip that folder too.
- **Schemas:** every entry in `questions.json` must follow `schemas/question.schema.json`. Error entries follow `error.schema.json`. Generated and rejected entries follow `generated.schema.json`. Run `python scripts/validate.py` after changing anything in `bank/`.
- **Kinematics:** use only the five SUVAT equations.
- **Statistics:** don't assume access to statistical tables. Use values given in the question or compute them directly.
- **Never invent mark scheme points or examiner comments.** If a value isn't in the source, it is `null`.
- **Generated questions** go into `generated.json` only after they pass verification (`verified: true`, with a `verified_on` date). Failed candidates go into `rejected.json`.
- **Python:** readable over clever. Add comments that explain any non-obvious step.

## Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate.py
```
