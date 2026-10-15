"""Mark a spec ref as covered in bank/covered_topics.json, or list a strand's refs.

Usage (from the project root, with the venv active):
    python scripts/cover_topic.py 8MA0 pure 2.3          # show the statement, confirm, add
    python scripts/cover_topic.py 9MA0 statistics 2      # a whole topic
    python scripts/cover_topic.py 8MA0 pure 2.3 --yes    # add without asking
    python scripts/cover_topic.py --list 9MA0 mechanics  # every ref with its statement

The statement shown is the full Content text from the specification PDF in
source/reference/. Some statements come out of the PDF garbled (maths) or cut
short, so for those the hand-written label from schemas/spec_labels.json is shown
first, and the PDF text after it. Without the PDF only
the opening words from schemas/topics.json are available, and the output
says so.

The file's format is described in covered.py. Adding a whole topic replaces
any of its single refs already listed; adding a ref that is already covered
changes nothing.
"""

import argparse
import json
import sys
import textwrap
from pathlib import Path

from build_topics import SPECS, parse_spec
from covered import (COVERED, QUALIFICATIONS, STRANDS, read_covered, ref_sort_key, ref_topic,
                     spec_refs, load_topics)
from paths import ROOT

LABELS = ROOT / "schemas" / "spec_labels.json"


def spec_statements(qual):
    """{(strand, ref): full statement text} from the spec PDF, or None if it isn't downloaded."""
    if not SPECS[qual].exists():
        return None
    return {(strand, ref): text
            for strand, topics in parse_spec(SPECS[qual]).items()
            for topic in topics for ref, text in topic["refs"].items()}


def statement(qual, strand, ref, topic, pdf_text, hand_labels):
    """[(heading, text)] describing one ref's statement."""
    hand = hand_labels.get(qual, {}).get(strand, {}).get(ref)
    if pdf_text is None:
        return [("Opening words only (spec PDF not in source/reference/)", topic[qual]["refs"][ref])]
    full = pdf_text.get((strand, ref), "")
    if hand:
        return [("Statement (hand-written LaTeX, schemas/spec_labels.json)", hand),
                ("PDF text (garbled or cut short)", full)]
    return [("Statement", full)]


def print_wrapped(text, indent):
    print(textwrap.fill(text, width=100, initial_indent=indent, subsequent_indent=indent))


def show_ref(qual, strand, ref, topic, pdf_text, hand_labels):
    print(f"{qual} {strand} {ref}  ({topic['name']})")
    for heading, text in statement(qual, strand, ref, topic, pdf_text, hand_labels):
        print(f"  {heading}:")
        print_wrapped(text, "    ")


def is_covered(items, ref):
    """True if ref (or its whole topic) is already in the strand's list."""
    return ref in items or ref.split(".")[0] in items


def add(data, qual, strand, ref, topic_refs):
    """Add ref (or a bare topic number) to data in place. Returns False if already covered."""
    items = data.setdefault(qual, {}).setdefault(strand, [])
    if is_covered(items, ref):
        return False
    if "." not in ref:
        # A whole topic makes its single refs redundant.
        items[:] = [i for i in items if i not in topic_refs]
    items.append(ref)
    items.sort(key=ref_sort_key)
    return True


def format_covered(data):
    """JSON text in a fixed order, one strand per line, so diffs stay small."""
    quals = [q for q in QUALIFICATIONS if data.get(q)]
    lines = ["{"]
    for qn, qual in enumerate(quals):
        strands = [s for s in STRANDS if data[qual].get(s)]
        lines.append(f'  "{qual}": {{')
        for sn, strand in enumerate(strands):
            comma = "," if sn < len(strands) - 1 else ""
            lines.append(f'    "{strand}": {json.dumps(data[qual][strand])}{comma}')
        lines.append("  }" + ("," if qn < len(quals) - 1 else ""))
    lines.append("}")
    return "\n".join(lines) + "\n"


def list_strand(qual, strand, topics, covered_items, pdf_text, hand_labels):
    for number, refs in spec_refs(topics, qual, strand).items():
        topic = ref_topic(topics, qual, strand, number)
        whole = number in covered_items
        print(f"\n{qual} {strand} topic {number}: {topic['name']}{'  [whole topic covered]' if whole else ''}")
        for ref in refs:
            mark = "[x]" if whole or ref in covered_items else "[ ]"
            # One statement per ref: the hand-written label where the PDF text is garbled.
            heading, text = statement(qual, strand, ref, topic, pdf_text, hand_labels)[0]
            print(textwrap.fill(f"{mark} {ref:<5} {text}", width=100,
                                initial_indent="  ", subsequent_indent=" " * 12))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("words", nargs="+", help='qualification, strand and ref, e.g. 8MA0 pure 2.3 '
                                                 '(with --list, just qualification and strand)')
    parser.add_argument("--list", action="store_true", help="list every ref in the strand")
    parser.add_argument("--yes", action="store_true", help="add without asking to confirm")
    parser.add_argument("--covered", type=Path, default=COVERED,
                        help="covered-topics file (default bank/covered_topics.json)")
    args = parser.parse_args()
    # Piped or redirected output on Windows would otherwise use the locale
    # code page (cp1252), so "Newton’s laws" reaches a UTF-8 reader as a
    # stray 0x92 byte. The console itself is unaffected.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Accept "8MA0 pure 2.3" as one quoted argument too.
    words = " ".join(args.words).split()
    expected = 2 if args.list else 3
    if len(words) != expected:
        parser.error("give " + ("QUAL STRAND" if args.list else "QUAL STRAND REF") + ", e.g. 8MA0 pure 2.3")
    qual, strand = words[0].upper(), words[1].lower()
    if qual not in QUALIFICATIONS or strand not in STRANDS:
        parser.error(f"qualification is one of {', '.join(QUALIFICATIONS)}; strand one of {', '.join(STRANDS)}")

    topics = load_topics()
    hand_labels = json.loads(LABELS.read_text(encoding="utf-8"))
    pdf_text = spec_statements(qual)
    data = read_covered(args.covered)
    items = data.get(qual, {}).get(strand, [])

    if args.list:
        list_strand(qual, strand, topics, items, pdf_text, hand_labels)
        return 0

    ref = words[2]
    topic = ref_topic(topics, qual, strand, ref)
    if topic is None:
        print(f"{ref} is not a {qual} {strand} topic number or spec ref. "
              f"See: python scripts/cover_topic.py --list {qual} {strand}")
        return 1
    topic_refs = list(topic[qual]["refs"])
    for r in topic_refs if "." not in ref else [ref]:
        show_ref(qual, strand, r, topic, pdf_text, hand_labels)

    if is_covered(items, ref):
        print(f"\nAlready covered; {args.covered.name} not changed.")
        return 0
    if not args.yes:
        if not sys.stdin.isatty():
            print("\nNot added: confirm interactively, or rerun with --yes.")
            return 1
        try:
            answer = input(f"\nAdd {qual} {strand} {ref} to {args.covered.name}? [y/N] ")
        except EOFError:
            # Windows reports NUL as a terminal, so input can still run out here.
            answer = ""
        if answer.strip().lower() not in ("y", "yes"):
            print("\nNot added.")
            return 1

    add(data, qual, strand, ref, topic_refs)
    args.covered.write_text(format_covered(data), encoding="utf-8")
    print(f"Added {qual} {strand} {ref} to {args.covered.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
