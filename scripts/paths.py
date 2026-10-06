"""Shared project paths.

out/ is git-ignored, so a fresh clone does not have it. Any script that
writes there must get its folder through ensure_out_dir().
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "out"

# The mock papers (reserved series) live OUTSIDE the project, so nothing that
# works inside the project can stumble on them. This is the one place the
# location is set; scripts that file reserved papers (fetch_materials.py)
# write here and nothing ever reads from here.
RESERVED_DIR = Path.home() / "9MA0-reserved"


def ensure_out_dir(subdir=""):
    """Return out/<subdir>, creating it (and out/ itself) if missing."""
    path = OUT_DIR / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path
