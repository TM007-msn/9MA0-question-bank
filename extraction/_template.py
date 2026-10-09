"""Draft builder for PAPER SERIES. Copy to extraction/PAPER_SERIES.py and fill in.

Run (from the project root, with the venv active):
    python extraction/PAPER_SERIES.py        # writes out/drafts/PAPER_SERIES.json
then save with:
    python scripts/add_entries.py out/drafts/PAPER_SERIES.json

Everything here is transcribed from the source PDFs (read as page images
where the text layer garbles maths). Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from mark_codes import main_marks  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "PAPER", "SERIES"            # e.g. "8MA0-01", "2019-06"
SRC = f"{P}_{S}_QP.pdf"             # for a SPEC section: the combined PDF, e.g. "9MA0-03_SPEC_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "04bii"); label as printed (e.g. "4(b)(ii)")."""
    return {"id": f"{P}_{S}_Q{q}", "paper": P, "series": S, "question": label, "topic": topic,
            "spec_ref": spec, "marks": marks, "question_latex": latex, "mark_scheme": ms,
            "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
            "has_diagram": diagram, "source_page": page, "source_file": SRC}


# Shared stems go in variables so each part's question_latex stands alone.
# Figures: "[Figure N: description]" and has_diagram True.
DRAFT = [
    # e("01", "1", "Integration", "8.2", 4,
    #   r"Find $$\int\ldots\,\mathrm{d}x$$ ...",
    #   [r"M1 (AO 1.1a): <scheme line>. Notes: <notes for this mark>",
    #    r"A1 (AO 1.1b): ...",
    #    r"ALT: <method name as labelled in the MS> — M1 (AO x.y): ..."],
    #   False, 2),
]

# Examiner report, sentence by sentence, in report order.
#   (None, text)              about the whole question -> every part
#   ({"a"}, text)             about part (a) only; {"b", "c"} for both
#   (parts, text, {"ref": True})        refers back to the sentence before
#   (parts, text, {"ref": "Opening words"})  refers back to that earlier sentence
#   (parts, text, {"ref": False})       contains this/it/these/... but doesn't refer back
W = None
REPORT = {
    # "01": [(W, "A good starting question."), ({"a"}, "..."), ...],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
# The sentence index points into REPORT[question]; it must be in that entry's notes.
# Use (None, None) only if the report says nothing usable about the part.
RATINGS = {
    # "01": ("easy", ("01", 3)),
}


def build():
    entries = [dict(d) for d in DRAFT]
    apply_report(entries, REPORT)
    keys = {q + (p or "") for q, p in map(part_key, entries)}
    if set(RATINGS) != keys:
        raise SystemExit(f"RATINGS keys differ from entries: {sorted(set(RATINGS) ^ keys)}")
    for entry in entries:
        q, p = part_key(entry)
        rating, where = RATINGS[q + (p or "")]
        if rating is not None:
            entry["difficulty"] = rating
            entry["difficulty_evidence"] = REPORT[where[0]][where[1]][1]
        # Each main line counts its code's value (B2 is one line worth 2 marks); ALT lines don't count.
        if entry["mark_scheme"] is not None and main_marks(entry["mark_scheme"]) != entry["marks"]:
            raise SystemExit(f"{entry['id']}: main mark-scheme lines are worth {main_marks(entry['mark_scheme'])} "
                             f"marks, entry has {entry['marks']}")
    return entries


if __name__ == "__main__":
    out = ensure_out_dir("drafts") / f"{P}_{S}.json"
    entries = build()
    out.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(entries)} entries, {sum(x['marks'] or 0 for x in entries)} marks -> {out}")
