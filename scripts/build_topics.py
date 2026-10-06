"""Build schemas/topics.json from the A level (9MA0) and AS (8MA0) specifications.

Usage (from the project root, with the venv active):
    python scripts/build_topics.py          # write schemas/topics.json
    python scripts/build_topics.py --show   # print what was parsed, write nothing

The specification content tables have three columns: Topics (topic number
and name), Content (ref like "2.3" and the statement), and Guidance. The
text order inside the PDF mixes the columns, so this reads each word's x
position to work out which column it belongs to. Guidance is ignored.

Canonical topic names are the A level names. Each AS topic is matched to
the A level topic with the same name in the same strand (pure, statistics,
mechanics); an AS topic with no A level match stops the script.
"""

import argparse
import json
import re
import sys

import pymupdf

from paths import ROOT

SPECS = {
    "9MA0": ROOT / "source" / "reference" / "9MA0_specification.pdf",
    "8MA0": ROOT / "source" / "reference" / "8MA0_specification.pdf",
}
OUT = ROOT / "schemas" / "topics.json"

REF_RE = re.compile(r"^\d{1,2}\.\d{1,2}$")


def part_for(page, current):
    """Pure or applied (statistics + mechanics), from the section heading.

    Only text near the top of the page counts: guidance text further down
    sometimes mentions "Pure Mathematics" on a mechanics page. Pages without
    a heading continue the current part.
    """
    heading = " ".join(b[4] for b in page.get_text("blocks") if b[1] < 100)
    if re.search(r"Paper \d: Statistics and Mechanics", heading):
        return "applied"
    if re.search(r"Paper 1( and Paper 2)?: Pure Mathematics", heading):
        return "pure"
    return current


def split_applied(topics):
    """Statistics topics come first; mechanics starts at the first topic
    whose name mentions mechanics ("Quantities and units in mechanics")."""
    for i, t in enumerate(topics):
        if "mechanics" in t["name"].lower():
            return topics[:i], topics[i:]
    return topics, []


def reading_order(words, tolerance=3):
    """Sort words top to bottom, then left to right within a line.

    Words on the same printed line can differ in y by a point or two (a ref
    number is set slightly lower than the statement next to it), so words
    within `tolerance` of a line's first word count as that line.
    """
    lines = []
    for w in sorted(words, key=lambda w: w[1]):
        if lines and w[1] - lines[-1][0][1] < tolerance:
            lines[-1].append(w)
        else:
            lines.append([w])
    return [w for line in lines for w in sorted(line, key=lambda w: w[0])]


def parse_spec(path):
    """Return {strand: [ {number, name, refs: {ref: statement}} ]} in spec order."""
    doc = pymupdf.open(path)
    parts = {"pure": [], "applied": []}
    strand = None
    topic = None
    name_top = None  # y of the current topic's number, to keep its name close by
    ref = None
    # Column edges. Defaults match both specs; updated from the "Content" and
    # "Guidance" header words when a page has them.
    content_x, guidance_x = 165, 350

    for page in doc:
        text = page.get_text()
        # Content tables are the pages with a "What students need to learn" header.
        if "What students need to learn" not in text:
            continue
        strand = part_for(page, strand)
        if strand is None:
            continue

        words = page.get_text("words")  # (x0, y0, x1, y1, word, block, line, n)
        for w in words:
            if w[4] == "Content":
                content_x = w[0] - 5
            elif w[4] == "Guidance":
                guidance_x = w[0] - 5

        # Ignore the running header/footer and the table header row.
        header_bottom = max((w[3] for w in words if w[4] in ("Content", "Guidance")), default=0)
        body = [w for w in words if header_bottom < w[1] < page.rect.height - 60]
        body = reading_order(body)

        # One pass in reading order (top to bottom), sending each word to
        # its column. Topic and ref must be handled together: a page can
        # hold the end of one topic and the start of the next.
        #
        # Topics column: a topic starts with a bare number; the words just
        # under it are its name. A topic that runs onto another page is
        # repeated there as e.g. "7 Kinematics continued": reuse the topic.
        # Words far below the number (e.g. the assessment notes after the
        # last table) are not part of the name.
        # Content column: a ref like "2.3" starts a statement; the content
        # words after it belong to it.
        pending = False
        name_words = []
        last_y = header_bottom  # y of the last word added to the current statement
        for w in body:
            if w[0] < content_x:
                if re.fullmatch(r"\d{1,2}", w[4]):
                    number = int(w[4])
                    name_top = w[1]
                    existing = [t for t in parts[strand] if t["number"] == number]
                    if existing:
                        topic = existing[-1]
                        pending = False  # continuation: name already known
                    else:
                        topic = {"number": number, "name": "", "refs": {}}
                        parts[strand].append(topic)
                        pending = True
                        name_words = []
                elif pending and w[1] - name_top < 60 and w[4] != "Topics":
                    # Keep PDF line order (block, line, word) so "(x, y)" stays put.
                    name_words.append(w)
                    name_words.sort(key=lambda n: (n[5], n[6], n[7]))
                    topic["name"] = " ".join(n[4] for n in name_words)
            elif w[0] < guidance_x and topic is not None:
                if REF_RE.fullmatch(w[4]) and w[4].split(".")[0] == str(topic["number"]):
                    ref = w[4]
                    topic["refs"][ref] = ""
                    last_y = w[1]
                elif ref in topic["refs"]:
                    # A big vertical gap means the table has ended (e.g. the
                    # assessment notes under the last topic): stop collecting.
                    if w[1] - last_y > 80:
                        ref = None
                        continue
                    topic["refs"][ref] = (topic["refs"][ref] + " " + w[4]).strip()
                    last_y = w[1]

    statistics, mechanics = split_applied(parts["applied"])
    return {"pure": parts["pure"], "statistics": statistics, "mechanics": mechanics}


def short(statement, words=18):
    """First few words of a statement, as a label (not the full spec text)."""
    parts = statement.split()
    return " ".join(parts[:words]) + (" …" if len(parts) > words else "")


def build():
    parsed = {qual: parse_spec(path) for qual, path in SPECS.items()}
    topics = []
    for strand in ("pure", "statistics", "mechanics"):
        a_level = parsed["9MA0"][strand]
        as_level = {t["name"]: t for t in parsed["8MA0"][strand]}
        for t in a_level:
            as_topic = as_level.pop(t["name"], None)
            topics.append({
                "name": t["name"],
                "strand": strand,
                "9MA0": {"topic_number": t["number"],
                         "refs": {r: short(s) for r, s in t["refs"].items()}},
                "8MA0": None if as_topic is None else {
                    "topic_number": as_topic["number"],
                    "refs": {r: short(s) for r, s in as_topic["refs"].items()}},
            })
        if as_level:
            sys.exit(f"AS {strand} topics with no A level match: {sorted(as_level)}")
    return parsed, topics


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--show", action="store_true", help="print the parse, write nothing")
    args = parser.parse_args()

    if args.show:
        parsed = {qual: parse_spec(path) for qual, path in SPECS.items()}
        for qual, strands in parsed.items():
            print(f"== {qual}")
            for strand, items in strands.items():
                for t in items:
                    print(f"  {strand:10} {t['number']:>2} {t['name']:45} refs: {', '.join(t['refs'])}")
        return 0

    parsed, topics = build()
    names = [t["name"] for t in topics]
    document = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://9ma0-bank.local/schemas/topics.json",
        "title": "Topics",
        "description": "Canonical topic list built from the 9MA0 and 8MA0 specifications by scripts/build_topics.py. Names are the A level names; AS topics use the same name. Do not edit by hand: rerun the script.",
        "$defs": {"topic_name": {"enum": names}},
        "topics": topics,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(document, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT.relative_to(ROOT).as_posix()}: {len(topics)} topics")
    return 0


if __name__ == "__main__":
    sys.exit(main())
