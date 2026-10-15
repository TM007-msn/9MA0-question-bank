"""Get a returned worksheet ready for marking with /mark.

Usage (from the project root, with the venv active):
    python scripts/mark_prep.py              # newest PDF in out/from-remarkable/
    python scripts/mark_prep.py FILE.pdf     # a particular returned PDF

It
  1. picks the newest PDF in out/from-remarkable/ (by modified time),
  2. matches it to its set by name: "test-five_questions.pdf" (or
     "test-five_questions (1).pdf", "test-five.pdf") -> out/sets/test-five.json,
  3. finds the pages each part is on, from the question id printed under
     each question number (in the PDF's text layer),
  4. renders every page to out/marking/NAME/page-NN.png, and
  5. writes out/marking/NAME/brief.md: for each part, its pages, the
     question and the bank's mark scheme, main lines (with mark values) and
     ALT lines.

It marks nothing. /mark (.claude/skills/mark/SKILL.md) reads the brief and
the page images, marks, and logs through log_attempt.py after confirmation.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import pymupdf

from log_attempt import load_bank, read_attempts
from mark_codes import mark_value
from paths import OUT_DIR, ensure_out_dir

RETURNED_DIR = OUT_DIR / "from-remarkable"
SETS_DIR = OUT_DIR / "sets"
PAGE_DPI = 150

# "NAME_questions", "NAME_questions (1)" or "NAME". The (1) is what a
# download gets when a file of that name is already there.
RETURNED_RE = re.compile(r"^(?P<name>.+?)(?:_questions)?(?:\s*\(\d+\))?$")


def newest_pdf(folder=RETURNED_DIR):
    pdfs = [p for p in folder.glob("*.pdf") if p.is_file()] if folder.is_dir() else []
    if not pdfs:
        raise SystemExit(f"No PDF in {folder}. Export the marked-up worksheet from the tablet there first.")
    return max(pdfs, key=lambda p: p.stat().st_mtime)


def set_name(pdf):
    """The set name a returned PDF belongs to, from its file name."""
    if "markscheme" in pdf.stem.lower():
        raise SystemExit(f"{pdf.name} looks like a mark scheme, not returned work.")
    return RETURNED_RE.match(pdf.stem).group("name")


def load_set(name, folder=SETS_DIR):
    path = folder / f"{name}.json"
    if not path.is_file():
        known = sorted(p.stem for p in folder.glob("*.json")) if folder.is_dir() else []
        raise SystemExit(f"No set called {name!r} in {folder}. Sets: {', '.join(known) or 'none'}")
    return path, json.loads(path.read_text(encoding="utf-8"))


def part_pages(page_texts, ids):
    """{id: [1-based pages]} from where each id is printed.

    A part's working can run on until the page where the next part starts,
    so its pages go from its own first page to that page, inclusive. The
    last part runs to the end (pages added on the tablet included). An id
    not found in the text layer maps to None: read every page for it.
    """
    starts = {}
    for i in ids:
        starts[i] = next((n for n, text in enumerate(page_texts, 1) if i in text), None)
    pages = {}
    for k, i in enumerate(ids):
        first = starts[i]
        if first is None:
            pages[i] = None
            continue
        later = [starts[j] for j in ids[k + 1:] if starts[j] is not None]
        last = later[0] if later else len(page_texts)
        pages[i] = list(range(first, max(first, last) + 1))
    return pages


def render(doc, out_dir, dpi=PAGE_DPI):
    # Clear pages from an earlier run, so a shorter export leaves no stale pages.
    for old in out_dir.glob("page-*.png"):
        old.unlink()
    paths = []
    for n, page in enumerate(doc, 1):
        path = out_dir / f"page-{n:02d}.png"
        page.get_pixmap(dpi=dpi).save(path)
        paths.append(path)
    return paths


def brief_text(name, pdf, ids, bank, pages, already):
    lines = [f"# Marking brief: {name}", "",
             f"Returned PDF: {pdf}", f"Parts: {len(ids)}, total {sum(bank[i]['marks'] for i in ids)} marks", ""]
    if already:
        lines += ["**Already in log/attempts.csv since the set was built:** " + ", ".join(already), ""]
    for n, i in enumerate(ids, 1):
        e = bank[i]
        where = ", ".join(f"page-{p:02d}.png" for p in pages[i]) if pages[i] else "not found: read every page"
        lines += [f"## {n}. {i}", "",
                  f"- Topic: {e['topic']}",
                  f"- Marks: {e['marks']}",
                  f"- Pages: {where}", "",
                  "### Question", "", e["question_latex"], "",
                  "### Mark scheme (main method)", ""]
        for line in e["mark_scheme"]:
            if not line.startswith("ALT:"):
                lines.append(f"- [{mark_value(line)}] {line}")
        alts = [line for line in e["mark_scheme"] if line.startswith("ALT:")]
        if alts:
            lines += ["", "### Alternatives (ALT)", ""] + [f"- {line}" for line in alts]
        if e.get("final_answer"):
            lines += ["", f"Final answer: {e['final_answer']}"]
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", nargs="?", type=Path, help="returned PDF (default: newest in out/from-remarkable/)")
    parser.add_argument("--dpi", type=int, default=PAGE_DPI, help=f"page render dpi (default {PAGE_DPI})")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    pdf = (args.pdf or newest_pdf()).resolve()
    name = set_name(pdf)
    set_path, ids = load_set(name)
    bank = load_bank()
    missing = [i for i in ids if i not in bank]
    if missing:
        raise SystemExit("Set ids not in the bank: " + ", ".join(missing))

    doc = pymupdf.open(pdf)
    pages = part_pages([page.get_text() for page in doc], ids)
    out_dir = ensure_out_dir(f"marking/{name}")
    images = render(doc, out_dir, args.dpi)

    # Rows logged for these ids on or after the day the set was built may
    # mean this work has been marked already.
    built = date.fromtimestamp(set_path.stat().st_mtime)
    already = sorted({r["question_id"] for r in read_attempts() if r["question_id"] in ids and r["date"] >= built})

    brief = out_dir / "brief.md"
    brief.write_text(brief_text(name, pdf, ids, bank, pages, already), encoding="utf-8")

    print(f"Returned PDF: {pdf.name} ({len(images)} pages)")
    print(f"Set: {name} ({len(ids)} parts, {sum(bank[i]['marks'] for i in ids)} marks)")
    for n, i in enumerate(ids, 1):
        where = ", ".join(map(str, pages[i])) if pages[i] else "NOT FOUND (read every page)"
        print(f"  {n}. {i:<26} {bank[i]['marks']:>2} marks  pages {where}")
    if already:
        print("Already logged since the set was built: " + ", ".join(already))
    print(f"Pages: {out_dir}\\page-NN.png")
    print(f"Brief: {brief}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
