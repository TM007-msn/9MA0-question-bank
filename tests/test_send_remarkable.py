"""Tests for send_remarkable.py. rmapi is never run: subprocess calls are faked.

Run from the project root:
    python -m unittest discover tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import send_remarkable  # noqa: E402
from send_remarkable import ANSWERS_FOLDER, FOLDER, SendError  # noqa: E402


def done(returncode=0, out="", err=""):
    return subprocess.CompletedProcess([], returncode, out, err)


class SendTests(unittest.TestCase):
    def setUp(self):
        # A fake out/ with one built set, and a fake paired config file.
        self.out = Path(tempfile.mkdtemp())
        sets = self.out / "to-remarkable"
        sets.mkdir()
        (sets / "demo_questions.pdf").write_bytes(b"%PDF-1.5")
        (sets / "demo_markscheme.pdf").write_bytes(b"%PDF-1.5")
        config = self.out / "rmapi.conf"
        config.write_text("devicetoken: x\n", encoding="utf-8")
        for patch in (mock.patch.object(send_remarkable, "OUT_DIR", self.out),
                      mock.patch.dict("os.environ", {"RMAPI_CONFIG": str(config)}),
                      mock.patch("shutil.which", return_value="rmapi"),
                      mock.patch("builtins.print")):
            patch.start()
            self.addCleanup(patch.stop)

    def test_send_uploads_only_the_questions_pdf_to_the_main_folder(self):
        with mock.patch("subprocess.run", return_value=done()) as run:
            send_remarkable.send("demo")
        puts = [c.args[0] for c in run.call_args_list if c.args[0][1] == "put"]
        self.assertEqual(len(puts), 1)
        # The bare file name, run from its folder: a full Windows path would
        # end up in the document's name on the tablet.
        self.assertEqual(puts[0][2], "demo_questions.pdf")
        put_call = next(c for c in run.call_args_list if c.args[0][1] == "put")
        self.assertEqual(put_call.kwargs["cwd"], self.out / "to-remarkable")
        self.assertEqual(puts[0][3], FOLDER)
        sent = " ".join(" ".join(c.args[0]) for c in run.call_args_list)
        self.assertNotIn("markscheme", sent)

    def test_never_forces_an_overwrite(self):
        with mock.patch("subprocess.run", return_value=done()) as run:
            send_remarkable.send("demo")
        for call in run.call_args_list:
            self.assertNotIn("--force", call.args[0])

    def test_stdin_is_closed(self):
        # An unpaired rmapi would otherwise wait for a one-time code.
        with mock.patch("subprocess.run", return_value=done()) as run:
            send_remarkable.send("demo")
        for call in run.call_args_list:
            self.assertIs(call.kwargs["stdin"], subprocess.DEVNULL)
            self.assertIn("timeout", call.kwargs)

    def test_folder_created_only_when_missing(self):
        replies = {"stat": done(1, err="entry doesn't exist"), "mkdir": done(), "put": done()}
        with mock.patch("subprocess.run", side_effect=lambda cmd, **kw: replies[cmd[1]]) as run:
            send_remarkable.send("demo")
        self.assertEqual([c.args[0][1] for c in run.call_args_list], ["stat", "mkdir", "put"])

        with mock.patch("subprocess.run", return_value=done()) as run:
            send_remarkable.send("demo")
        self.assertEqual([c.args[0][1] for c in run.call_args_list], ["stat", "put"])

    def test_mark_scheme_name_refused_as_a_question_sheet(self):
        with self.assertRaises(SendError):
            send_remarkable.questions_pdf("demo_markscheme")
        with self.assertRaises(SendError):
            send_remarkable.questions_pdf("drill_answers")

    def test_answers_go_only_to_the_answers_subfolder(self):
        (self.out / "to-remarkable" / "demo_answers.pdf").write_bytes(b"%PDF-1.5")
        with mock.patch("subprocess.run", return_value=done()) as run:
            send_remarkable.send_answers("demo")
        puts = [c.args[0] for c in run.call_args_list if c.args[0][1] == "put"]
        self.assertEqual(sorted(p[2] for p in puts), ["demo_answers.pdf", "demo_markscheme.pdf"])
        self.assertTrue(all(p[3] == ANSWERS_FOLDER for p in puts))
        self.assertEqual(ANSWERS_FOLDER, FOLDER + "/Answers")

    def test_mark_scheme_never_goes_to_the_main_folder(self):
        sets = self.out / "to-remarkable"
        with mock.patch("subprocess.run", return_value=done()) as run:
            for name in ("demo_markscheme.pdf", "demo_answers.pdf"):
                with self.assertRaises(SendError):
                    send_remarkable.upload(sets / name, FOLDER)
            # and question sheets don't go in with the answers
            with self.assertRaises(SendError):
                send_remarkable.upload(sets / "demo_questions.pdf", ANSWERS_FOLDER)
        run.assert_not_called()

    def test_answers_folder_and_its_parent_are_created_when_missing(self):
        made = []

        def reply(cmd, **kw):
            if cmd[1] == "stat":
                return done(0 if cmd[2] in made else 1)
            if cmd[1] == "mkdir":
                made.append(cmd[2])
            return done()
        with mock.patch("subprocess.run", side_effect=reply):
            send_remarkable.send_answers("demo")
        self.assertEqual(made, [FOLDER, ANSWERS_FOLDER])

    def test_send_answers_needs_a_built_answers_pdf(self):
        with mock.patch("subprocess.run") as run, self.assertRaises(SendError):
            send_remarkable.send_answers("nope")
        run.assert_not_called()

    def test_missing_pdf(self):
        with mock.patch("subprocess.run") as run, self.assertRaises(SendError):
            send_remarkable.send("nope")
        run.assert_not_called()

    def test_unpaired_stops_before_running_rmapi(self):
        with mock.patch.dict("os.environ", {"RMAPI_CONFIG": str(self.out / "absent.conf")}), \
                mock.patch("subprocess.run") as run, self.assertRaises(SendError):
            send_remarkable.send("demo")
        run.assert_not_called()

    def test_cleared_login_counts_as_unpaired(self):
        # What rmapi leaves behind when the cloud rejects its login.
        cleared = self.out / "cleared.conf"
        cleared.write_text('devicetoken: ""\nusertoken: ""\n', encoding="utf-8")
        with mock.patch.dict("os.environ", {"RMAPI_CONFIG": str(cleared)}), \
                mock.patch("subprocess.run") as run, self.assertRaises(SendError):
            send_remarkable.send("demo")
        run.assert_not_called()

    def test_repeated_prompt_lines_are_collapsed(self):
        noise = "".join(f"ERROR: 2026/10/15 20:46:{s:02d} auth.go:76: Code has the wrong length\n"
                        for s in range(60))
        message = send_remarkable.short_error(done(1, err=noise))
        self.assertEqual(message, "ERROR: auth.go:76: Code has the wrong length")

    def test_failed_put_is_reported(self):
        replies = {"stat": done(), "put": done(1, err="entry already exists")}
        with mock.patch("subprocess.run", side_effect=lambda cmd, **kw: replies[cmd[1]]), \
                self.assertRaises(SendError) as caught:
            send_remarkable.send("demo")
        self.assertIn("already exists", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
