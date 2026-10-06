"""Build an HTML review sheet for one paper's entries in bank/questions.json.

Usage (from the project root, with the venv active):
    python scripts/build_review.py 8MA0-01 2018-06

Writes out/review/PAPER_SERIES_review.html. For each question it shows a
crop of the question paper (from the entry's source_file) next to what was
extracted, so the two can be compared: question text (LaTeX rendered with
KaTeX, which loads from a CDN, so viewing needs internet), topic and spec
refs with their statements, difficulty, the mark scheme with ALT methods
marked, and the examiner notes.

Only source/papers/ is read. Entries can never point at the mock papers
(validate.py checks source_file), and this script refuses one that does.
"""

import argparse
import base64
import html
import json
import re
import sys
from collections import OrderedDict

import pymupdf

from add_entries import question_number
from check_marks import compare
from paths import RESERVED_DIR, ROOT, ensure_out_dir
from validate import consistency_errors, load_topics

PAPERS_DIR = ROOT / "source" / "papers"
QUESTIONS = ROOT / "bank" / "questions.json"
PROGRESS = ROOT / "bank" / "progress.json"

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"

STYLE = """
:root { --bg:#fbfaf7; --card:#fff; --ink:#1d1d1b; --muted:#6b6a65; --line:#e3e1da;
        --alt:#f3f0ff; --alt-ink:#4b3fa3; --warn:#9a3b00; --chip:#efede6; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#1a1a18; --card:#232320; --ink:#ecebe6; --muted:#a3a29b; --line:#3a3934;
          --alt:#2b2740; --alt-ink:#c9c0ff; --warn:#ffb27a; --chip:#2f2e2a; }
}
* { box-sizing:border-box; }
body { margin:0; padding:24px 16px 64px; background:var(--bg); color:var(--ink);
       font:15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width:1100px; margin:0 auto; }
h1 { font-size:22px; margin:0 0 4px; }
.summary { color:var(--muted); margin-bottom:24px; }
.summary b { color:var(--ink); }
.question { background:var(--card); border:1px solid var(--line); border-radius:10px;
            margin:0 0 28px; overflow:hidden; }
.question > h2 { margin:0; padding:12px 16px; font-size:17px; border-bottom:1px solid var(--line); }
.source { padding:12px 16px; border-bottom:1px solid var(--line); overflow-x:auto; }
.source img { display:block; max-width:100%; border:1px solid var(--line); background:#fff; }
.source .cap { color:var(--muted); font-size:12px; margin-top:4px; }
.entry { padding:14px 16px; border-top:1px dashed var(--line); }
.entry:first-of-type { border-top:none; }
.entry h3 { margin:0 0 8px; font-size:15px; }
.meta { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
.chip { background:var(--chip); border-radius:999px; padding:2px 10px; font-size:13px; }
.chip.null { color:var(--warn); }
.latex { background:var(--bg); border-left:3px solid var(--line); padding:8px 12px; margin:6px 0 12px;
         overflow-x:auto; }
.label { font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin-top:10px; }
ul.ms { margin:4px 0 0; padding-left:20px; }
ul.ms li { margin:4px 0; overflow-x:auto; }
ul.ms li.alt { background:var(--alt); color:var(--alt-ink); border-radius:6px; padding:4px 8px; list-style:none; margin-left:-20px; }
.refs { font-size:13px; color:var(--muted); margin:2px 0 0; padding-left:18px; }
.problems { color:var(--warn); font-weight:600; }
.notes { margin:4px 0 0; }
.evidence { font-size:13px; margin:0 0 6px; border-left:3px solid var(--line); padding-left:8px; }
"""


def esc(text):
    """Escape for HTML but keep line breaks. KaTeX reads the decoded text."""
    return html.escape(text or "").replace("\n", "<br>")


def crop_png(source_file, page_number):
    """PNG (base64) of the question region on a page: from the top margin
    down to the last "(n)" marks line. A scanned page has no text to find
    that line in, so the whole page is shown."""
    path = PAPERS_DIR / source_file
    if RESERVED_DIR.resolve() in path.resolve().parents:  # belt and braces: never read mock papers
        raise SystemExit("refusing to read the mock-papers folder")
    with pymupdf.open(path) as doc:
        page = doc[page_number - 1]
        marks = [b for b in page.get_text("blocks") if re.fullmatch(r"\(\d+\)", b[4].strip())]
        bottom = max(b[3] for b in marks) + 6 if marks else page.rect.height - 40
        clip = pymupdf.Rect(30, 30, page.rect.width - 45, bottom)
        png = page.get_pixmap(dpi=110, clip=clip).tobytes("png")
    return base64.b64encode(png).decode("ascii")


def ref_lines(entry, topics):
    """[(ref, statement label)] for the entry's spec_ref, from topics.json."""
    if not entry.get("spec_ref"):
        return []
    qual = entry["paper"].split("-")[0]
    labels = {}
    for t in topics.values():
        if t[qual] and t["strand"] == topics[entry["topic"]]["strand"]:
            labels.update(t[qual]["refs"])
    return [(r, labels.get(r, "?")) for r in entry["spec_ref"].split(", ")]


def chip(label, value):
    if value is None:
        return f'<span class="chip null">{label}: null</span>'
    # json.dumps shows booleans as true/false, matching the bank files.
    shown = json.dumps(value) if isinstance(value, bool) else str(value)
    return f'<span class="chip">{label}: {esc(shown)}</span>'


def render_entry(entry, topics):
    problems = consistency_errors("questions.json", entry)
    parts = [f'<section class="entry" id="{esc(entry["id"])}">',
             f'<h3>{esc(entry["question"])} &nbsp;·&nbsp; <code>{esc(entry["id"])}</code></h3>',
             '<div class="meta">',
             chip("marks", entry["marks"]), chip("topic", entry["topic"]),
             chip("spec_ref", entry["spec_ref"]), chip("difficulty", entry["difficulty"]),
             chip("has_diagram", entry["has_diagram"]), chip("page", entry["source_page"]),
             '</div>']
    if entry.get("difficulty_evidence"):
        parts.append(f'<p class="evidence"><b>Difficulty evidence:</b> {esc(entry["difficulty_evidence"])}</p>')
    refs = ref_lines(entry, topics)
    if refs:
        parts.append('<ul class="refs">' + "".join(
            f"<li><b>{esc(r)}</b> {esc(s)}</li>" for r, s in refs) + "</ul>")
    if problems:
        parts.append('<p class="problems">' + "<br>".join(esc(p) for p in problems) + "</p>")

    parts.append('<div class="label">Question</div>')
    parts.append(f'<div class="latex">{esc(entry["question_latex"])}</div>')

    parts.append('<div class="label">Mark scheme</div>')
    if entry["mark_scheme"] is None:
        parts.append('<p class="chip null">null</p>')
    else:
        items = []
        for m in entry["mark_scheme"]:
            cls = ' class="alt"' if m.startswith("ALT:") else ""
            items.append(f"<li{cls}>{esc(m)}</li>")
        parts.append('<ul class="ms">' + "".join(items) + "</ul>")

    parts.append('<div class="label">Examiner notes</div>')
    parts.append(f'<p class="notes">{esc(entry["examiner_notes"]) if entry["examiner_notes"] else "<span class=chip null>null</span>"}</p>')
    parts.append("</section>")
    return "\n".join(parts)


def build(paper, series):
    entries = [e for e in json.load(open(QUESTIONS, encoding="utf-8"))
               if e["paper"] == paper and e["series"] == series]
    if not entries:
        raise SystemExit(f"no entries for {paper} {series} in questions.json")
    topics = load_topics()
    progress = next((i for i in json.load(open(PROGRESS, encoding="utf-8"))["queue"]
                     if i["paper"] == paper and i["series"] == series), {})

    by_question = OrderedDict()
    for e in sorted(entries, key=lambda e: (question_number(e), e["id"])):
        by_question.setdefault(question_number(e), []).append(e)

    marks_status, _ = compare(paper, series)
    total = sum(e["marks"] or 0 for e in entries)
    alts = sum(m.startswith("ALT:") for e in entries for m in (e["mark_scheme"] or []))
    nulls = sum(1 for e in entries for v in e.values() if v is None)
    problems = sum(len(consistency_errors("questions.json", e)) for e in entries)

    body = [f"<h1>Review: {paper} {series}</h1>",
            '<p class="summary">',
            f"Status <b>{esc(progress.get('status', '?'))}</b> · marks check <b>{marks_status}</b> · "
            f"<b>{len(entries)}</b> entries · <b>{total}</b> marks · <b>{alts}</b> ALT mark-scheme lines · "
            f"<b>{nulls}</b> null fields · <b>{problems}</b> validation problems",
            "</p>"]
    for q, group in by_question.items():
        first = group[0]
        img = crop_png(first["source_file"], first["source_page"])
        body.append(f'<article class="question"><h2>Question {q}</h2>')
        body.append(f'<div class="source"><img alt="Question {q} as printed" src="data:image/png;base64,{img}">'
                    f'<div class="cap">{esc(first["source_file"])}, page {first["source_page"]} (question start)</div></div>')
        body.extend(render_entry(e, topics) for e in group)
        body.append("</article>")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Review {paper} {series}</title>
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}], throwOnError:false}})"></script>
<style>{STYLE}</style></head>
<body><main>
{chr(10).join(body)}
</main></body></html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paper", help="e.g. 8MA0-01")
    parser.add_argument("series", help="e.g. 2018-06")
    args = parser.parse_args()

    out_dir = ensure_out_dir("review")
    out = out_dir / f"{args.paper}_{args.series}_review.html"
    out.write_text(build(args.paper, args.series), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
