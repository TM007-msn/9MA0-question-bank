"""Build a question sheet and its mark scheme as PDFs for the reMarkable.

Usage (from the project root, with the venv active):
    python scripts/build_pdf.py SETFILE NAME
    python scripts/build_pdf.py --check-all

SETFILE is a JSON list of question ids from bank/questions.json or
bank/generated.json. NAME names the set. Writes, compiled with Tectonic:
    out/to-remarkable/NAME_questions.pdf    questions in set order, each with
        its number, the set's question id in small print, marks in brackets
        and blank working space scaled to the marks
    out/to-remarkable/NAME_markscheme.pdf   the mark points, in the same order
The .tex sources, page images and Tectonic logs stay in out/build/NAME/.

A real question with has_diagram = true is shown as its source page from the
question paper (rendered with PyMuPDF) instead of the LaTeX text. Generated
questions always use their LaTeX text, since the source page shows the
original question, not the variant.

--check-all compiles every entry in bank/questions.json (question text and
mark scheme, as LaTeX even where the sheet would show the page image) and
lists every entry that fails to compile, has a character the font can't
show, or has a line too wide for the page.

Only source/papers/ is read. A source_file that resolves anywhere else, or
into the mock-papers folder, is refused.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pymupdf

from add_entries import question_number
from paths import RESERVED_DIR, ROOT, ensure_out_dir

BANK_FILES = [ROOT / "bank" / "questions.json", ROOT / "bank" / "generated.json"]
PAPERS_DIR = ROOT / "source" / "papers"
TEMPLATES_DIR = ROOT / "templates"

# Suggested time and working space, both scaled to the marks.
MINUTES_PER_MARK = 1.2
SPACE_CM_PER_MARK = 2.5
MIN_SPACE_CM = 3
MAX_SPACE_CM = 20

PAGE_DPI = 200  # same as render_pages.py's FIGURE_DPI, so diagrams stay sharp
OVERFULL_PT = 5  # lines wider than the page by more than this are reported

SET_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
ROMAN_RE = re.compile(r"^(i{1,3}|iv|vi{0,3}|ix|x)$")

# Characters LaTeX treats as commands in text. Maths is passed through as is.
TEXT_ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "%": r"\%",
    "&": r"\&",
    "#": r"\#",
    "_": r"\_",
    "^": r"\^{}",
    "~": r"\textasciitilde{}",
    "$": r"\$",
}

# Text-style commands that may wrap a whole $...$, and their text-mode form.
# \uline (ulem) underlines and still lets the line break.
TEXT_WRAPPERS = {
    r"\textbf": r"\textbf",
    r"\textit": r"\textit",
    r"\underline": r"\uline",
    r"\text": "",
}


# ---------------------------------------------------------------- bank text to LaTeX

def find_end_of_maths(text, delimiter, start):
    """Index of the closing delimiter, or -1.

    The same rule as KaTeX auto-render (which the bank is checked against):
    a delimiter inside braces doesn't count, and a backslash skips the
    character after it, so \\$ or \\} don't end anything.
    """
    depth = 0
    i = start
    while i < len(text):
        if depth <= 0 and text.startswith(delimiter, i):
            return i
        if text[i] == "\\":
            i += 1
        elif text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return -1


def split_maths(text):
    """Split a bank string into [(kind, content)], kind 'text', 'inline' or 'display'.

    $$...$$ is display maths and $...$ inline, as in KaTeX auto-render. An
    unclosed $ is left in the text (validate.py rejects those anyway).
    """
    parts = []
    start = i = 0
    while i < len(text):
        if text[i] != "$":
            i += 1
            continue
        delimiter = "$$" if text.startswith("$$", i) else "$"
        end = find_end_of_maths(text, delimiter, i + len(delimiter))
        if end == -1:
            break
        parts.append(("text", text[start:i]))
        parts.append(("display" if delimiter == "$$" else "inline", text[i + len(delimiter):end]))
        start = i = end + len(delimiter)
    parts.append(("text", text[start:]))
    return [p for p in parts if p != ("text", "")]


def escape_text(text):
    return "".join(TEXT_ESCAPES.get(ch, ch) for ch in text)


def closing_brace(text, open_index):
    """Index of the } matching the { at open_index, or -1."""
    depth = 0
    i = open_index
    while i < len(text):
        if text[i] == "\\":
            i += 1
        elif text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def text_only_maths(maths):
    """Text-mode LaTeX for maths that is only styled words, else None.

    Mark schemes put whole sentences in maths as $\\textbf{...}$ or
    $\\underline{\\textbf{...}}$. KaTeX's HTML wraps those like text, but in
    LaTeX maths they are one unbreakable box that runs off the page, so they
    are typeset as ordinary text instead.
    """
    found = styled_words(maths)
    if found is None:
        return None
    styles, words = found
    # ulem can only break lines inside \uline when it holds plain words (a
    # \textbf group inside it is one unbreakable unit), so it goes innermost.
    if r"\uline" in styles:
        words = rf"\uline{{{words}}}"
    for style in reversed(styles):
        if style and style != r"\uline":
            words = f"{style}{{{words}}}"
    return words


def styled_words(maths):
    """([text-mode style commands], words) if maths is only wrapped words, else None."""
    s = maths.strip()
    for command, replacement in TEXT_WRAPPERS.items():
        # The command's braces must hold everything, not just the start.
        if not (s.startswith(command + "{") and closing_brace(s, len(command)) == len(s) - 1):
            continue
        inner = s[len(command) + 1:-1]
        if not re.search(r"\\[a-zA-Z]", inner):
            return [replacement], inner
        # The only command allowed inside is another wrapper, as in
        # \underline{\textbf{...}}; anything else is real maths.
        found = styled_words(inner)
        if found is None:
            return None
        return [replacement, *found[0]], found[1]
    return None


def bank_to_latex(text):
    """Turn a bank string (KaTeX delimiters, \\n line breaks) into LaTeX."""
    parts = split_maths(text)
    out = []
    for n, (kind, content) in enumerate(parts):
        if kind == "display":
            out.append(f"\\fitdisplay{{{content}}}")
        elif kind == "inline":
            text = text_only_maths(content)
            out.append(text if text is not None else f"\\fitinline{{{content}}}")
        else:
            # A display already starts and ends its own line, so the line
            # breaks either side of it would only add blank paragraphs.
            if n > 0 and parts[n - 1][0] == "display":
                content = content.removeprefix("\n")
            if n + 1 < len(parts) and parts[n + 1][0] == "display":
                content = content.removesuffix("\n")
            out.append(escape_text(content).replace("\n", "\\par\n"))
    return "".join(out)


def mark_point_latex(point):
    """(is_alt, LaTeX) for one mark_scheme string.

    The label before the first colon ("M1 (AO 1.1b)", "Way 2 — A1 (AO 2.1)")
    goes in bold, and the "Notes:" part on its own smaller line.
    """
    is_alt = point.startswith("ALT:")
    if is_alt:
        point = point[len("ALT:"):].strip()
    # A label is short and has no maths; otherwise the whole string is text.
    match = re.match(r"([^$:]{1,60}?):\s", point)
    label, rest = (match.group(1), point[match.end():]) if match else ("", point)
    body, _, notes = rest.partition(" Notes: ")
    latex = f"\\mspoint{{{escape_text(label)}}}{{{bank_to_latex(body)}}}"
    if notes:
        latex += f"\n\\msnotes{{Notes: {bank_to_latex(notes)}}}"
    return is_alt, latex


def part_label(entry_id):
    """'9MA0-01_2019-06_Q05bii' -> '5(b)(ii)', 'X_Q12iia' -> '12(ii)(a)'."""
    part = entry_id.rsplit("_Q", 1)[1].split("-")[0]
    number = re.match(r"\d+", part).group()
    suffix = part[len(number):]
    if not suffix:
        pieces = []
    elif ROMAN_RE.match(suffix):
        pieces = [suffix]
    elif ROMAN_RE.match(suffix[1:]) or len(suffix) == 1:
        pieces = [suffix[0], suffix[1:]]  # letter then roman, e.g. b + ii
    else:
        pieces = [suffix[:-1], suffix[-1]]  # roman then letter, e.g. ii + a
    return str(int(number)) + "".join(f"({p})" for p in pieces if p)


# ---------------------------------------------------------------- bank and set

def load_bank():
    """{id: entry} for questions.json and generated.json."""
    bank = {}
    for path in BANK_FILES:
        for entry in json.loads(path.read_text(encoding="utf-8")):
            bank[entry["id"]] = entry
    return bank


def load_set(path):
    ids = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
        raise SystemExit(f"{path}: a set file must be a JSON list of question ids")
    return ids


def is_generated(entry):
    return "anchor_id" in entry


def question_clip(page, number):
    """The part of an Edexcel page that holds question `number`, or None.

    Starts at the printed question number (or the first line of text, when
    the question doesn't start on this page's left margin) and ends after its
    last line of text, taking in any figure in between. Left out: the end of
    the previous question above it, the answer lines below the text, the
    "DO NOT WRITE IN THIS AREA" margin bars, the page frame and the footer.
    None for a scanned page with no text layer, which is used whole.
    """
    width, height = page.rect.width, page.rect.height
    lines = []
    answer_lines = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            box = pymupdf.Rect(line["bbox"])
            text = "".join(span["text"] for span in line["spans"]).strip()
            # Horizontal text only (the margin bars are rotated), and not the
            # page number or barcode digits in the header and footer.
            if not (text and line["dir"] == (1, 0) and height * 0.04 < box.y0 and box.y1 < height * 0.93):
                continue
            # The answer lines are rows of dots in the text layer (which a
            # font with no character mapping turns into some other repeated
            # character).
            if len(text) >= 10 and len(set(text.replace(" ", ""))) == 1:
                answer_lines.append(box)
            else:
                lines.append((box, text))
    # Nothing of the question comes after its answer space: text below the
    # last answer line is "(Total for Question N is X marks)" or a footer,
    # which an unmapped font can make unrecognisable.
    if answer_lines:
        last = max(b.y0 for b in answer_lines)
        lines = [(box, text) for box, text in lines if box.y0 < last]
    if not lines:
        return None

    # The question number is printed alone at the left margin, e.g. "6.".
    starts = [box for box, text in lines
              if re.fullmatch(rf"{number}\.?", text) and box.x0 < width * 0.2]
    top = min(starts, key=lambda b: b.y0).y0 if starts else min(b.y0 for b, _ in lines)
    below = [box for box, _ in lines if box.y0 >= top - 2]
    clip = pymupdf.Rect(below[0])
    for box in below:
        clip |= box

    # Add figures (vector drawings and images) that sit between the question
    # number and its last line of text, inside the text column. That skips
    # the page frame, the margin bars and the answer lines underneath.
    shapes = [d["rect"] for d in page.get_drawings()] + [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
    for shape in shapes:
        centre_x = (shape.x0 + shape.x1) / 2
        if (shape.y0 >= top - 2 and shape.y1 <= clip.y1 + 2 and clip.x0 <= centre_x <= clip.x1
                and shape.width < width * 0.8):
            clip |= shape
    margin = 8
    return pymupdf.Rect(clip.x0 - margin, clip.y0 - margin, clip.x1 + margin, clip.y1 + margin) & page.rect


def source_page_image(entry, build_dir):
    """Render the entry's question from its source page to a PNG in build_dir.

    Returns the image's file name.
    """
    pdf = (PAPERS_DIR / entry["source_file"]).resolve()
    # source_file is only a file name, but check where it really points before opening.
    if pdf.parent != PAPERS_DIR.resolve() or RESERVED_DIR.resolve() in pdf.parents:
        raise SystemExit(f"{entry['id']}: refusing source_file outside source/papers/: {entry['source_file']}")
    if not pdf.is_file():
        raise SystemExit(f"{entry['id']}: source paper not found: {pdf}")
    # Two questions can start on one page, and each gets its own crop.
    name = f"{pdf.stem}_p{entry['source_page']:02d}_Q{question_number(entry)}.png"
    image = build_dir / name
    with pymupdf.open(pdf) as doc:
        page = doc[entry["source_page"] - 1]
        clip = question_clip(page, question_number(entry))
        page.get_pixmap(dpi=PAGE_DPI, clip=clip).save(image)
    return name


# ---------------------------------------------------------------- LaTeX documents

def working_space_cm(marks):
    return min(MAX_SPACE_CM, max(MIN_SPACE_CM, SPACE_CM_PER_MARK * marks))


def suggested_minutes(total_marks):
    # Whole minutes, rounded up. Integer arithmetic, since 1.2 * 50 in floats
    # is 60.000000000000014 and would round up to 61.
    return -(-total_marks * round(MINUTES_PER_MARK * 10) // 10)


def question_body(entry, build_dir, as_text=False):
    """LaTeX for the question itself: its text, or its source page for a diagram."""
    if entry["has_diagram"] and not is_generated(entry) and not as_text:
        image = source_page_image(entry, build_dir)
        note = (f"Source: {entry['paper']} {entry['series']}, page {entry['source_page']}. "
                f"Answer Question {part_label(entry['id'])} only.")
        return f"\\bankfigurepage{{{image}}}{{{escape_text(note)}}}"
    return bank_to_latex(entry["question_latex"])


def question_block(number, entry, build_dir, as_text=False, space_cm=None):
    space = working_space_cm(entry["marks"]) if space_cm is None else space_cm
    return (f"\\bankquestion{{{number}}}{{{escape_text(entry['id'])}}}{{{entry['marks']}}}{{{space}cm}}{{%\n"
            f"{question_body(entry, build_dir, as_text)}}}\n")


def mark_scheme_block(number, entry):
    lines = [f"\\msquestion{{{number}}}{{{escape_text(entry['id'])}}}{{{entry['marks']}}}"]
    main, alts = [], []
    for point in entry["mark_scheme"]:
        is_alt, latex = mark_point_latex(point)
        (alts if is_alt else main).append(latex)
    lines += main
    if alts:
        lines.append("\\msalt")
        lines += alts
    if entry.get("final_answer"):
        lines.append(f"\\mspoint{{Answer:}}{{{bank_to_latex(entry['final_answer'])}}}")
    return "\n".join(lines) + "\n"


def fill_template(name, title, cover, body):
    preamble = (TEMPLATES_DIR / "preamble.tex").read_text(encoding="utf-8")
    template = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    # One pass, so text in the body can never be mistaken for a placeholder.
    values = {"PREAMBLE": preamble, "TITLE": title, "COVER": cover, "BODY": body}
    return re.sub(r"<<(PREAMBLE|TITLE|COVER|BODY)>>", lambda m: values[m.group(1)], template)


# ---------------------------------------------------------------- compiling

def tectonic():
    exe = shutil.which("tectonic")
    if not exe:
        raise SystemExit("Tectonic not found. Install it from https://tectonic-typesetting.github.io "
                         "and put tectonic.exe on PATH.")
    return exe


def compile_tex(tex_path):
    """Compile with Tectonic in tex_path's folder. Returns (ok, log text, stderr)."""
    result = subprocess.run(
        [tectonic(), "--chatter", "minimal", "--keep-logs", tex_path.name],
        cwd=tex_path.parent, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    log_path = tex_path.with_suffix(".log")
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    return result.returncode == 0, log, result.stderr


def log_problems(log):
    """[(kind, entry id or None, message)] from a Tectonic log.

    kind is 'error', 'glyph' (a character the font can't show) or 'overfull'.
    Each entry's LaTeX is preceded by a "@@ENTRY id" line in the log
    (\\typeout), so a problem belongs to the last marker before it.
    """
    problems = []
    current = None
    lines = log.splitlines()
    for n, line in enumerate(lines):
        if line.startswith("@@ENTRY "):
            current = line.removeprefix("@@ENTRY ").strip()
        elif line.startswith("! "):
            # The "l.123 ..." line after an error shows where TeX stopped.
            context = next((l.strip() for l in lines[n + 1:n + 8] if l.startswith("l.")), "")
            problems.append(("error", current, f"{line[2:]} {context}".strip()))
        elif line.startswith("Missing character"):
            problems.append(("glyph", current, line.strip()))
        elif match := re.match(r"Overfull \\hbox \(([\d.]+)pt too wide\)", line):
            if float(match.group(1)) > OVERFULL_PT:
                problems.append(("overfull", current, line.strip()))
    return problems


def compile_or_exit(tex_path, out_pdf):
    ok, log, stderr = compile_tex(tex_path)
    problems = log_problems(log)
    for kind, entry_id, message in problems:
        print(f"  {kind}{f' in {entry_id}' if entry_id else ''}: {message}")
    if not ok:
        print(stderr.strip())
        raise SystemExit(f"Tectonic failed on {tex_path} (log: {tex_path.with_suffix('.log')})")
    shutil.copyfile(tex_path.with_suffix(".pdf"), out_pdf)
    print(out_pdf)


# ---------------------------------------------------------------- commands

def build(ids, name):
    """Build NAME_questions.pdf and NAME_markscheme.pdf for the ids, in order."""
    if not SET_NAME_RE.match(name):
        raise SystemExit(f"set name {name!r}: use only letters, digits, '-', '_' and '.'")
    bank = load_bank()
    unknown = [i for i in ids if i not in bank]
    if unknown:
        raise SystemExit("not in questions.json or generated.json: " + ", ".join(unknown))
    if len(set(ids)) != len(ids):
        raise SystemExit("the set lists an id more than once")
    entries = [bank[i] for i in ids]

    build_dir = ensure_out_dir(f"build/{name}")
    out_dir = ensure_out_dir("to-remarkable")
    total = sum(e["marks"] for e in entries)
    cover = escape_text(f"{len(entries)} questions · Total {total} marks · "
                        f"Suggested time {suggested_minutes(total)} minutes")
    title = escape_text(name)

    questions = "\n".join(question_block(n, e, build_dir) for n, e in enumerate(entries, 1))
    scheme = "\n".join(mark_scheme_block(n, e) for n, e in enumerate(entries, 1))
    for template, heading, body, suffix in [("questions.tex", title, questions, "questions"),
                                            ("markscheme.tex", f"{title} --- mark scheme", scheme, "markscheme")]:
        tex = build_dir / f"{name}_{suffix}.tex"
        tex.write_text(fill_template(template, heading, cover, body), encoding="utf-8")
        compile_or_exit(tex, out_dir / f"{name}_{suffix}.pdf")


def check_all():
    """Compile every questions.json entry as text and list the ones that fail."""
    entries = json.loads(BANK_FILES[0].read_text(encoding="utf-8"))
    build_dir = ensure_out_dir("build/_check-all")
    tex = build_dir / "check-all.tex"
    failed = {}  # id -> first error
    while True:
        blocks = []
        for n, entry in enumerate(e for e in entries if e["id"] not in failed):
            blocks.append(f"\\typeout{{@@ENTRY {entry['id']}}}\n"
                          + question_block(n + 1, entry, build_dir, as_text=True, space_cm=0)
                          + mark_scheme_block(n + 1, entry))
        tex.write_text(fill_template("questions.tex", "check-all", "", "\n".join(blocks)), encoding="utf-8")
        ok, log, stderr = compile_tex(tex)
        problems = log_problems(log)
        if ok:
            break
        # Tectonic stops at the first error. Set that entry aside and go
        # again, until everything left compiles.
        error = next((p for p in problems if p[0] == "error"), None)
        if error is None or error[1] is None or error[1] in failed:
            print(stderr.strip())
            raise SystemExit(f"Tectonic failed outside any entry; see {tex.with_suffix('.log')}")
        failed[error[1]] = error[2]
        print(f"FAIL {error[1]}: {error[2]}")

    print(f"\nCompiled {len(entries) - len(failed)} of {len(entries)} entries.")
    print(f"Failed to compile: {len(failed)}")
    for entry_id, message in failed.items():
        print(f"  {entry_id}: {message}")
    for kind, heading in [("glyph", "Characters the font can't show"),
                          ("overfull", f"Lines more than {OVERFULL_PT}pt too wide for the page")]:
        found = [p for p in problems if p[0] == kind]
        print(f"{heading}: {len(found)}")
        for _, entry_id, message in found:
            print(f"  {entry_id}: {message}")
    return 1 if failed or any(p[0] == "glyph" for p in problems) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("setfile", nargs="?", help="JSON list of question ids")
    parser.add_argument("name", nargs="?", help="set name, used in the PDF file names")
    parser.add_argument("--check-all", action="store_true",
                        help="compile every questions.json entry and list failures")
    args = parser.parse_args()
    if args.check_all:
        return check_all()
    if not (args.setfile and args.name):
        parser.error("give SETFILE and NAME, or --check-all")
    build(load_set(Path(args.setfile)), args.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
