"""Set examiner_notes on a paper's entries from tagged report sentences.

A report is given as {question number (two digits): [sentence, ...]}, where
each sentence is (parts, text) or (parts, text, options):
  parts    None for a sentence about the whole question (it goes on every
           part), or a set of part keys such as {"a"}, {"b", "c"}, {"bi"}.
           Part keys are what follows the question number in the entry id,
           e.g. "a" for Q06a, "bii" for Q04bii, "i" for Q02i.
  text     the sentence copied from the report (maths as LaTeX).
  options  {"ref": ...} for a sentence that refers back to another one
           ("this", "it", "these" ...): True for the sentence just before
           it, or the opening words of the sentence it refers to. Wherever
           the sentence goes, the one it refers to goes too. {"ref": False}
           records that a sentence was checked and doesn't refer back.

Every sentence containing "this", "it", "these", "those" or "such" (other
than "this question/part/..." and similar) must carry a "ref" option, so a
back-reference can't be missed silently.

Notes keep report order. Difficulty is set separately, by judgement (see
CLAUDE.md), together with difficulty_evidence.
"""

import re

# Pronouns that may point at an earlier sentence. Phrases like "this question"
# or "this part" point at the question itself and don't need a ref.
BACKREF_RE = re.compile(
    r"\b(this|it|these|those|such)\b"
    r"(?!\s+(question|part|paper|method|methods|multi-step|kind|type|topic|case|phrase|"
    r"variable|approach|value|formula|quadratic|model|area|function|line|statement))",
    re.IGNORECASE)


def part_key(entry):
    """'9MA0-31_2019-06_Q04bii' -> ('04', 'bii'); a question with no parts -> ('10', None)."""
    tail = entry["id"].rsplit("_Q", 1)[1]
    digits = "".join(ch for ch in tail[:2] if ch.isdigit())
    return digits.zfill(2), tail[len(digits):] or None


def _normalise(sentences, q):
    """[(parts, text, ref_index or None)] with refs resolved to indexes."""
    out = []
    for i, s in enumerate(sentences):
        parts, text = s[0], s[1]
        options = s[2] if len(s) > 2 else {}
        if BACKREF_RE.search(text) and "ref" not in options:
            raise ValueError(f"Q{q}: sentence may refer back; mark it with ref=True/'opening words'/False: {text!r}")
        ref = options.get("ref", False)
        if ref is True:
            if i == 0:
                raise ValueError(f"Q{q}: first sentence can't refer to a previous one: {text!r}")
            ref_index = i - 1
        elif ref:
            matches = [j for j in range(i) if sentences[j][1].startswith(ref)]
            if len(matches) != 1:
                raise ValueError(f"Q{q}: ref {ref!r} must match exactly one earlier sentence")
            ref_index = matches[0]
        else:
            ref_index = None
        out.append((parts, text, ref_index))
    return out


def notes_for(sentences, part):
    """Sentence indexes that go on this part (None = question with no parts),
    including the sentences they refer back to, in report order."""
    chosen = {i for i, (parts, _, _) in enumerate(sentences) if parts is None or (part in parts)}
    # Follow back-references (a referred-to sentence may itself refer back).
    changed = True
    while changed:
        changed = False
        for i in list(chosen):
            ref = sentences[i][2]
            if ref is not None and ref not in chosen:
                chosen.add(ref)
                changed = True
    return sorted(chosen)


def apply_report(entries, report):
    """Set examiner_notes on entries in place. Returns {id: (old, new)} for
    entries whose notes changed."""
    present = {part_key(e) for e in entries}
    normalised = {}
    for q, sentences in report.items():
        normalised[q] = _normalise(sentences, q)
        for parts, _, _ in normalised[q]:
            for p in (parts or ()):
                if (q, p) not in present:
                    raise ValueError(f"report tags Q{q} part {p!r}, but there is no such entry")

    changes = {}
    for e in entries:
        q, part = part_key(e)
        sentences = normalised.get(q, [])
        if part is None and any(parts is not None for parts, _, _ in sentences):
            raise ValueError(f"Q{q} has no parts but the report sentences are tagged with parts")
        idx = notes_for(sentences, part)
        new = " ".join(sentences[i][1] for i in idx) if idx else None
        if new != e["examiner_notes"]:
            changes[e["id"]] = (e["examiner_notes"], new)
        e["examiner_notes"] = new
    return changes
