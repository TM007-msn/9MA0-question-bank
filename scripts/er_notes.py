"""Set examiner_notes and difficulty on a paper's entries from tagged report sentences.

A report is given as {question number (two digits): [sentence, ...]}, where
each sentence is (parts, text) or (parts, text, clauses):
  parts    None for a sentence about the whole question (it goes on every
           part), or a set of part keys such as {"a"}, {"b", "c"}, {"bi"}.
           Part keys are what follows the question number in the entry id,
           e.g. "a" for Q06a, "bii" for Q04bii, "i" for Q02i.
  text     the sentence copied from the report (maths as LaTeX).
  clauses  optional {part: clause} when one sentence judges parts
           differently; difficulty then uses only that part's clause.

Notes keep report order. Difficulty follows scripts/difficulty.py.
"""

from difficulty import difficulty


def part_key(entry):
    """'9MA0-31_2019-06_Q04bii' -> ('04', 'bii'); a question with no parts -> ('10', None)."""
    tail = entry["id"].rsplit("_Q", 1)[1]
    digits = "".join(ch for ch in tail[:2] if ch.isdigit())
    number = digits.zfill(2)
    rest = tail[len(digits):]
    return number, rest or None


def apply_report(entries, report):
    """Update entries in place. Returns a list of (id, old difficulty, new
    difficulty, basis, notes_changed) for review."""
    present = {part_key(e) for e in entries}
    for q, sentences in report.items():
        for s in sentences:
            for p in (s[0] or ()):
                if (q, p) not in present:
                    raise ValueError(f"report tags Q{q} part {p!r}, but there is no such entry")

    log = []
    for e in entries:
        q, part = part_key(e)
        sentences = [(s[0], s[1], s[2] if len(s) > 2 else {}) for s in report.get(q, [])]
        if part is None and any(tag is not None for tag, _, _ in sentences):
            raise ValueError(f"Q{q} has no parts but the report sentences are tagged with parts")

        notes = [text for tag, text, _ in sentences if tag is None or part in tag]
        part_only = [clauses.get(part, text) for tag, text, clauses in sentences if tag is not None and part in tag]
        whole = [text for tag, text, _ in sentences if tag is None]

        old_notes, old_diff = e["examiner_notes"], e["difficulty"]
        e["examiner_notes"] = " ".join(notes) if notes else None
        if not sentences:
            level, basis = None, {"from": None, "phrases": {}}
        elif part is None:
            level, basis = difficulty(whole, [])
        else:
            level, basis = difficulty(part_only, whole)
        e["difficulty"] = level
        log.append((e["id"], old_diff, level, basis, old_notes != e["examiner_notes"]))
    return log
