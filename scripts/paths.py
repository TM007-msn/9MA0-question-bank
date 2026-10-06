"""Shared project paths.

out/ is git-ignored, so a fresh clone does not have it. Any script that
writes there must get its folder through ensure_out_dir().
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "out"


def ensure_out_dir(subdir=""):
    """Return out/<subdir>, creating it (and out/ itself) if missing."""
    path = OUT_DIR / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path
