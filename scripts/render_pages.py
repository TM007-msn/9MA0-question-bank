"""Render PDF pages to PNG so they can be read as images.

Usage (from the project root, with the venv active):
    python scripts/render_pages.py source/papers/8MA0-01_2019-06_QP.pdf 2 4 6
    python scripts/render_pages.py source/mark-schemes/8MA0-01_2019-06_MS.pdf all --dpi 80
    python scripts/render_pages.py source/papers/X_QP.pdf 2 --clip-bottom 0.5   # top half only
    python scripts/render_pages.py source/papers/X_QP.pdf 22 --figure   # figure page at 200 dpi

Writes out/pages/<pdf name>_p<N>.png (or _p<N>_fig.png with --figure) and prints the paths.
Figures are always read at FIGURE_DPI, so curve shapes and dashed edges are clear. Use it wherever
the PDF text layer garbles maths, for scanned papers, and for figures.
Refuses anything in the mock-papers folder (RESERVED_DIR in paths.py).
"""

import argparse
import sys
from pathlib import Path

import pymupdf

from paths import RESERVED_DIR, ensure_out_dir

FIGURE_DPI = 200


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", help="path to a PDF under source/")
    parser.add_argument("pages", nargs="+", help="1-based page numbers, or 'all'")
    parser.add_argument("--dpi", type=int, default=110)
    parser.add_argument("--figure", action="store_true",
                        help=f"render at {FIGURE_DPI} dpi for reading figures (overrides --dpi)")
    parser.add_argument("--clip-bottom", type=float, default=1.0,
                        help="keep only this fraction of the page from the top (e.g. 0.5)")
    args = parser.parse_args()
    if args.figure:
        args.dpi = FIGURE_DPI

    path = Path(args.pdf).resolve()
    if RESERVED_DIR.resolve() in path.parents:
        print("Refusing: the mock-papers folder is never opened.", file=sys.stderr)
        return 1

    out_dir = ensure_out_dir("pages")
    with pymupdf.open(path) as doc:
        numbers = range(1, doc.page_count + 1) if args.pages == ["all"] else [int(p) for p in args.pages]
        for n in numbers:
            page = doc[n - 1]
            clip = pymupdf.Rect(0, 0, page.rect.width, page.rect.height * args.clip_bottom)
            # Figure renders get their own name so they don't overwrite the lower-dpi text render.
            suffix = "_fig" if args.figure else ""
            out = out_dir / f"{path.stem}_p{n:02d}{suffix}.png"
            page.get_pixmap(dpi=args.dpi, clip=clip).save(out)
            print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
