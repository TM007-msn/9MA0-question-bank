"""Mark values of mark-scheme lines.

Each main mark_scheme string starts with its code, e.g. "M1 (AO 1.1b): ...",
"dM1 ...", "A1* ...", "B1ft ...". A multi-mark code such as B2, M2 or A2 is
stored as one string, so the number in the code is the marks that line is
worth. ALT lines are alternatives and don't count towards the entry's marks.
"""

import re

# Optional dependency prefix (d, dd), the letter, then the mark value: "ddM1" -> 1, "B2" -> 2.
CODE_RE = re.compile(r"^d*[MAB](\d+)")


def mark_value(line):
    """Marks a main mark-scheme line is worth, read from its code."""
    match = CODE_RE.match(line)
    if match is None:
        raise ValueError(f"mark-scheme line has no mark code (M1, A1, B2, ...): {line[:60]!r}")
    return int(match.group(1))


def main_marks(mark_scheme):
    """Total marks of the main method: the sum of the code values of every non-ALT line."""
    return sum(mark_value(m) for m in mark_scheme or [] if not m.startswith("ALT:"))
