"""Upload a set's PDFs to the reMarkable with rmapi.

Usage (from the project root, with the venv active):
    python scripts/send_remarkable.py NAME            # NAME_questions.pdf
    python scripts/send_remarkable.py NAME --answers  # also its mark scheme / answers;
                                                      # skips questions already sent

quick_set.py --send calls send() after building a set; daily.py --send calls
send() and then send_answers() for the day's drill and exam sheet.

Where each PDF may go (upload() enforces this for every file):
  NAME_questions.pdf                        -> "Maths practice"
  NAME_markscheme.pdf and NAME_answers.pdf  -> "Maths practice/Answers" only,
                                               never the main folder
so the question sheets in the main folder never sit next to their answers.

Folders are created if missing. An existing document with the same name is
never overwritten: rmapi's --force would wipe any handwriting on it, so the
upload stops instead.

Needs rmapi (the ddvk fork) on PATH and paired once; see "reMarkable upload"
in CLAUDE.md.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from paths import OUT_DIR

FOLDER = "/Maths practice"
ANSWERS_FOLDER = FOLDER + "/Answers"
# File-name endings of the PDFs that hold mark schemes or worked answers.
ANSWER_SUFFIXES = ("_markscheme.pdf", "_answers.pdf")
TIMEOUT_SECONDS = 120


class SendError(Exception):
    pass


def questions_pdf(name):
    """The questions PDF for set NAME. Never the mark scheme."""
    path = OUT_DIR / "to-remarkable" / f"{name}_questions.pdf"
    # Belt and braces: a set name like "x_markscheme" would still end in
    # _questions.pdf, but refuse anything that mentions the mark scheme.
    if is_answers(path):
        raise SendError(f"Refusing to send {path.name} as a question sheet.")
    return path


def is_answers(path):
    """True for a mark scheme or answers PDF (or anything named like one)."""
    name = Path(path).name.lower()
    return name.endswith(ANSWER_SUFFIXES) or "markscheme" in name or "answers" in name


def answer_pdfs(name):
    """The set's mark scheme and/or answers PDFs that exist."""
    folder = OUT_DIR / "to-remarkable"
    return [folder / f"{name}{suffix}" for suffix in ANSWER_SUFFIXES if (folder / f"{name}{suffix}").is_file()]


def config_files():
    """Places rmapi keeps its pairing token: RMAPI_CONFIG if set, else the
    defaults for this fork (%APPDATA%\\rmapi\\rmapi.conf on Windows, ~/.rmapi)."""
    if os.environ.get("RMAPI_CONFIG"):
        return [Path(os.environ["RMAPI_CONFIG"])]
    candidates = [Path.home() / ".rmapi"]
    if os.environ.get("APPDATA"):
        candidates.insert(0, Path(os.environ["APPDATA"]) / "rmapi" / "rmapi.conf")
    return candidates


def has_device_token(path):
    """True if the config file holds a non-empty devicetoken.

    When the cloud rejects the saved login, rmapi rewrites the file with
    empty tokens (devicetoken: "") rather than deleting it, so the file
    existing isn't enough.
    """
    if not path.is_file():
        return False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "devicetoken":
            return value.strip().strip("\"'") != ""
    return False


def short_error(result):
    """rmapi's message, without the hundreds of repeated code-prompt lines
    an auth failure produces: the distinct lines, at most five."""
    lines = []
    for line in (result.stderr or result.stdout).splitlines():
        # Drop the timestamp so repeated messages compare equal.
        line = re.sub(r"^ERROR: \S+ \S+ ", "ERROR: ", line.strip())
        if line and line not in lines:
            lines.append(line)
    return " | ".join(lines[:5])


def check_ready():
    """Stop with a clear message if rmapi is missing or not paired.

    This matters: an unpaired rmapi asks for a one-time code and, with no
    keyboard input, repeats the question forever instead of exiting.
    """
    if shutil.which("rmapi") is None:
        raise SendError("rmapi is not on PATH. See \"reMarkable upload\" in CLAUDE.md.")
    if not any(has_device_token(p) for p in config_files()):
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


def repair_hint():
    """A pairing reminder if rmapi has just cleared its login."""
    if any(has_device_token(p) for p in config_files()):
        return ""
    return ("\nrmapi's login was rejected and cleared. Pair it again in a separate terminal "
            "(see \"reMarkable upload\" in CLAUDE.md), then rerun "
            "`python scripts/send_remarkable.py NAME` to send the set already built.")


def ensure_folder(folder=FOLDER):
    """Create the folder (and the main folder above Answers) if missing."""
    if folder != FOLDER:
        ensure_folder(FOLDER)
    if rmapi("stat", folder).returncode != 0:
        made = rmapi("mkdir", folder)
        if made.returncode != 0:
            raise SendError(f"Couldn't create {folder}: {short_error(made)}{repair_hint()}")


def upload(pdf, folder):
    """Upload one PDF. Mark schemes and answers go only to ANSWERS_FOLDER,
    question sheets only to FOLDER; anything else is refused."""
    allowed = ANSWERS_FOLDER if is_answers(pdf) else FOLDER
    if folder != allowed:
        raise SendError(f"Refusing to send {pdf.name} to {folder}: it may only go to {allowed}.")
    if not pdf.is_file():
        raise SendError(f"{pdf} doesn't exist. Build the set first.")
    check_ready()
    ensure_folder(folder)
    # No --force: replacing a document deletes its annotations.
    # rmapi names the document after the path it's given, and on Windows it
    # keeps the whole C:\...\ path in the name, so pass the bare file name
    # and run from the PDF's folder.
    put = rmapi("put", pdf.name, folder, cwd=pdf.parent)
    if put.returncode != 0:
        raise SendError(f"Upload failed (an existing \"{pdf.stem}\" in {folder} is never "
                        f"overwritten; rename the set or delete it on the tablet): "
                        f"{short_error(put)}{repair_hint()}")
    print(f"Sent {pdf.name} to {folder} on the reMarkable.")


def on_tablet(pdf, folder):
    """True if a document named like this PDF (its stem) is already in folder."""
    check_ready()
    return rmapi("stat", f"{folder}/{pdf.stem}").returncode == 0


def send(name):
    """Upload NAME_questions.pdf to the Maths practice folder."""
    upload(questions_pdf(name), FOLDER)


def send_answers(name):
    """Upload the set's mark scheme and/or answers PDF to Maths practice/Answers."""
    pdfs = answer_pdfs(name)
    if not pdfs:
        raise SendError(f"No mark scheme or answers PDF for {name}. Build the set first.")
    for pdf in pdfs:
        upload(pdf, ANSWERS_FOLDER)


def main():
    args = sys.argv[1:]
    answers = "--answers" in args
    names = [a for a in args if a != "--answers"]
    if len(names) != 1:
        raise SystemExit(__doc__.strip().splitlines()[0]
                         + "\nUsage: python scripts/send_remarkable.py NAME [--answers]")
    try:
        questions = questions_pdf(names[0])
        # With --answers, a question sheet already on the tablet is left as
        # it is (never overwritten) and the answers still go.
        if answers and questions.is_file() and on_tablet(questions, FOLDER):
            print(f"{questions.stem} is already in {FOLDER}; not sending it again.")
        else:
            send(names[0])
        if answers:
            send_answers(names[0])
    except SendError as error:
        raise SystemExit(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main())
