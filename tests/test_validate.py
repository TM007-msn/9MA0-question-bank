"""Tests for validate.py's cross-field rules and schemas/topics.json.

Run from the project root:
    python -m unittest discover tests
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate import consistency_errors  # noqa: E402

TOPICS = json.loads((ROOT / "schemas" / "topics.json").read_text(encoding="utf-8"))


def entry(**changes):
    """A valid 8MA0-01 2018-06 entry (matches a file that exists in source/papers/)."""
    base = {
        "id": "8MA0-01_2018-06_Q09c", "paper": "8MA0-01", "series": "2018-06",
        "question": "9(c)", "topic": "Algebra and functions", "spec_ref": "2.7, 2.5",
        "marks": 3, "question_latex": "[Figure 2: sketch] Deduce ...",
        "mark_scheme": None, "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
        "has_diagram": True, "source_page": 22, "source_file": "8MA0-01_2018-06_QP.pdf",
    }
    base.update(changes)
    return base


class TopicsTests(unittest.TestCase):
    def test_enum_matches_topic_list(self):
        names = [t["name"] for t in TOPICS["topics"]]
        self.assertEqual(TOPICS["$defs"]["topic_name"]["enum"], names)
        self.assertEqual(len(names), len(set(names)))

    def test_as_topics_use_a_level_names(self):
        # Every topic has A level refs; AS-only topics would have no 9MA0 entry.
        for t in TOPICS["topics"]:
            self.assertTrue(t["9MA0"]["refs"], t["name"])


class ConsistencyTests(unittest.TestCase):
    def check(self, **changes):
        return consistency_errors("questions.json", entry(**changes))

    def test_valid_entry_passes(self):
        self.assertEqual(self.check(), [])

    def test_figure_needs_has_diagram(self):
        self.assertTrue(any("has_diagram" in e for e in self.check(has_diagram=False)))
        self.assertTrue(any("has_diagram" in e for e in self.check(has_diagram=None)))

    def test_other_brackets_do_not_count_as_figures(self):
        errors = self.check(question_latex="[In this question i and j are unit vectors] Find ...", has_diagram=False)
        self.assertFalse(any("has_diagram" in e for e in errors))

    def test_spec_ref_must_exist_for_qualification(self):
        # 8.7 (differential equations) is A level only.
        self.assertTrue(self.check(topic="Integration", spec_ref="8.7"))

    def test_first_spec_ref_must_belong_to_topic(self):
        self.assertTrue(self.check(spec_ref="5.1, 2.7"))

    def test_spec_ref_from_another_pure_topic_is_allowed_after_the_first(self):
        self.assertEqual(self.check(topic="Integration", spec_ref="8.3, 7.3, 3.1"), [])

    def test_source_file_must_match_paper(self):
        self.assertTrue(self.check(source_file="8MA0-01_2019-06_QP.pdf"))

    def test_spec_split_may_point_at_combined_paper(self):
        errors = consistency_errors("questions.json", entry(
            id="9MA0-32_SPEC_Q01", paper="9MA0-32", series="SPEC", topic="Kinematics",
            spec_ref="7.3", source_file="9MA0-03_SPEC_QP.pdf"))
        self.assertEqual(errors, [])

    def test_difficulty_needs_evidence_from_notes(self):
        notes = "Part (c) was usually attempted, but with limited success. Some used x = 2."
        ok = self.check(examiner_notes=notes, difficulty="hard",
                        difficulty_evidence="Part (c) was usually attempted, but with limited success.")
        self.assertEqual(ok, [])
        self.assertTrue(self.check(examiner_notes=notes, difficulty="hard"))
        self.assertTrue(self.check(examiner_notes=notes, difficulty="hard", difficulty_evidence="Students found it hard."))
        self.assertTrue(self.check(examiner_notes=notes, difficulty_evidence="Some used x = 2."))

    def test_evidence_is_the_sentence_without_its_sic_note(self):
        notes = "Some forgot to divide by 9. [sic: the mark scheme divides by 4] Others omitted units."
        self.assertEqual(self.check(examiner_notes=notes, difficulty="medium",
                                    difficulty_evidence="Some forgot to divide by 9."), [])
        self.assertTrue(self.check(examiner_notes=notes, difficulty="medium",
                                   difficulty_evidence="Some forgot to divide by 9. [sic: the mark scheme divides by 4]"))

    def test_latex_commands_in_plain_text_are_refused(self):
        for field, value in (("question_latex", "[Figure 2: sketch] the \\textbf{not} case"),
                             ("mark_scheme", ['M1 (AO 1.1b): states \\"proved\\"']),
                             ("examiner_notes", 'the word \\"Hence\\" was missed')):
            with self.subTest(field=field):
                self.assertTrue(any("prints literally" in e for e in self.check(**{field: value})))
        self.assertEqual(self.check(mark_scheme=["M1 (AO 1.1b): states “proved” and $\\text{“}10\\text{”}$"],
                                    marks=1), [])

    def test_layout_commands_outside_maths_are_refused(self):
        for text in (r"[Figure 2: sketch] $\log_2 x=3$ \quad using the power law",
                     r"[Figure 2: sketch] Line one \\ line two",
                     r"[Figure 2: sketch] $x=1$ \qquad simplifying"):
            with self.subTest(text=text):
                self.assertTrue(any("outside maths" in e for e in self.check(question_latex=text)))

    def test_layout_commands_inside_maths_are_allowed(self):
        text = (r"[Figure 2: sketch] $$\begin{aligned}\log_2 x&=3&&\text{using the power law}\\"
                r"x&=8\end{aligned}$$ and $n=184\qquad\sum x=4153.6$")
        self.assertEqual(self.check(question_latex=text), [])

    def test_split_mapping_is_only_for_spec(self):
        errors = consistency_errors("questions.json", entry(
            id="9MA0-32_2018-06_Q06", paper="9MA0-32", series="2018-06", topic="Kinematics",
            spec_ref="7.3", source_file="9MA0-03_2018-06_QP.pdf"))
        self.assertTrue(any("source_file" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
