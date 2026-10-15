"""Upload a set's questions PDF to the reMarkable with rmapi.

Usage (from the project root, with the venv active):
    python scripts/send_remarkable.py NAME     # sends out/to-remarkable/NAME_questions.pdf

quick_set.py --send calls send() after building a set.

Only the questions PDF is ever sent. The mark scheme stays on this computer,
so it can't be read on the tablet before the work is marked.

The file goes to the "Maths practice" folder, which is created if missing.
An existing document with the same name is never overwritten: rmapi's
--force would wipe any handwriting on it, so the upload stops instead.

Needs rmapi (the ddvk fork) on PATH and paired once; see "reMarkable upload"
in CLAUDE.md.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from paths import OUT_DIR

FOLDER = "/Maths practice"
TIMEOUT_SECONDS = 120


class SendError(Exception):
    pass


def questions_pdf(name):
    """The questions PDF for set NAME. Never the mark scheme."""
    path = OUT_DIR / "to-remarkable" / f"{name}_questions.pdf"
    # Belt and braces: a set name like "x_markscheme" would still end in
    # _questions.pdf, but refuse anything that mentions the mark scheme.
    if "markscheme" in path.name.lower():
        raise SendError(f"Refusing to send {path.name}: mark schemes are never sent.")
    return path


def config_files():
    """Places rmapi keeps its pairing token: RMAPI_CONFIG if set, else the
    defaults for this fork (%APPDATA%\\rmapi\\rmapi.conf on Windows, ~/.rmapi)."""
    if os.environ.get("RMAPI_CONFIG"):
        return [Path(os.environ["RMAPI_CONFIG"])]
    candidates = [Path.home() / ".rmapi"]
    if os.environ.get("APPDATA"):
        candidates.insert(0, Path(os.environ["APPDATA"]) / "rmapi" / "rmapi.conf")
    return candidates


def check_ready():
    """Stop with a clear message if rmapi is missing or not paired.

    This matters: an unpaired rmapi asks for a one-time code and, with no
    keyboard input, repeats the question forever instead of exiting.
    """
    if shutil.which("rmapi") is None:
        raise SendError("rmapi is not on PATH. See \"reMarkable upload\" in CLAUDE.md.")
    if not any(p.is_file() and p.stat().st_size > 0 for p in config_files()):
        raise SendError("rmapi is not paired with your reMarkable account yet. "
                        "Run `rmapi` once in a terminal and enter the one-time code "
                        "(see \"reMarkable upload\" in CLAUDE.md).")


def rmapi(*args, cwd=None):
    """Run one rmapi command non-interactively and return the result.

    stdin is closed so a pairing prompt can never wait for input, and the
    timeout stops the run if rmapi loops on that prompt anyway.
    """
    try:
        return subprocess.run(["rmapi", *args], stdin=subprocess.DEVNULL, cwd=cwd,
                              capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        raise SendError(f"rmapi {' '.join(args)} took over {TIMEOUT_SECONDS}s and was stopped. "
                        "If it is asking for a one-time code, pair it again.")


def ensure_folder():
    if rmapi("stat", FOLDER).returncode != 0:
        made = rmapi("mkdir", FOLDER)
        if made.returncode != 0:
            raise SendError(f"Couldn't create {FOLDER}: {(made.stderr or made.stdout).strip()}")


def send(name):
    """Upload NAME_questions.pdf to the Maths practice folder."""
    pdf = questions_pdf(name)
    if not pdf.is_file():
        raise SendError(f"{pdf} doesn't exist. Build the set first.")
    check_ready()
    ensure_folder()
    # No --force: replacing a document deletes its annotations.
    # rmapi names the document after the path it's given, and on Windows it
    # keeps the whole C:\...\ path in the name, so pass the bare file name
    # and run from the PDF's folder.
    put = rmapi("put", pdf.name, FOLDER, cwd=pdf.parent)
    if put.returncode != 0:
        raise SendError(f"Upload failed (an existing \"{pdf.stem}\" in {FOLDER} is never "
                        f"overwritten; rename the set or delete it on the tablet): "
                        f"{(put.stderr or put.stdout).strip()}")
    print(f"Sent {pdf.name} to {FOLDER} on the reMarkable.")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.strip().splitlines()[0] + "\nUsage: python scripts/send_remarkable.py NAME")
    try:
        send(sys.argv[1])
    except SendError as error:
        raise SystemExit(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main())
