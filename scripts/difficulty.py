"""Difficulty from examiner report wording, by a fixed phrase mapping.

The same mapping is written out in CLAUDE.md ("Difficulty mapping"); keep
the two in step. Matching is case-insensitive on whole words.

Rules, for one part of a question:
  1. Look at the report sentences about that part (including sentences that
     name it together with other parts). When one sentence judges different
     parts differently ("Part (a) was very accessible, part (b) less so"),
     each part is judged only on its own clause.
  2. If they contain both easy and hard phrases -> medium (mixed).
     Otherwise any hard phrase -> hard; any easy phrase -> easy;
     any medium phrase -> medium.
  3. If they contain none of the phrases, apply step 2 to the sentences
     about the whole question.
  4. If there is still nothing, difficulty is null. Never guess.
"""

import re

EASY = [
    "well done", "done well", "well answered", "accessible", "well prepared",
    "good source of marks", "good starting question", "good solutions",
    "was more successful", "much more successful",
    "many scoring full marks", "many gained all marks", "scored full marks",
]
MEDIUM = [
    "mixed", "varying success", "some success", "some candidates", "some students",
    "at least one mark",
]
HARD = [
    "demanding", "challenge", "difficult", "very few", "few candidates", "few students",
    "few responses", "few then", "rare", "rarely", "limited success", "less well",
    "less so", "struggled", "disappointing", "lacking", "unable to", "only more able",
    "significant hurdle", "frequently lost",
]

# Phrases that contain an easy phrase but mean the opposite.
NOT_EASY = {"well done": ["less well done"]}

def _matches(phrases, text):
    found = []
    for p in phrases:
        for m in re.finditer(rf"\b{re.escape(p)}\b", text):
            # "A few students made error X" describes a minority error, not
            # a hard part, so "few ..." right after "a " doesn't count.
            before = text[max(0, m.start() - 2):m.start()]
            if p.startswith("few") and before == "a ":
                continue
            # "less well done" is not "well done".
            if any(text[max(0, m.start() - len(n) + len(p)):m.end()] == n for n in NOT_EASY.get(p, [])):
                continue
            found.append(p)
            break
    return found


def classify(sentences):
    """(level or None, {level: [phrases found]}) for a list of sentences."""
    text = " ".join(sentences).lower()
    hits = {"easy": _matches(EASY, text), "medium": _matches(MEDIUM, text), "hard": _matches(HARD, text)}
    if hits["easy"] and hits["hard"]:
        return "medium", hits
    for level in ("hard", "easy", "medium"):
        if hits[level]:
            return level, hits
    return None, hits


def difficulty(part_sentences, whole_sentences):
    """Apply the rules above. Returns (level or None, basis) where basis says
    which sentences decided it and the phrases found."""
    level, hits = classify(part_sentences)
    if level:
        return level, {"from": "part", "phrases": {k: v for k, v in hits.items() if v}}
    level, hits = classify(whole_sentences)
    if level:
        return level, {"from": "whole question", "phrases": {k: v for k, v in hits.items() if v}}
    return None, {"from": None, "phrases": {}}
