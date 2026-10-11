"""Spec refs and bank/covered_topics.json, shared by quick_set.py,
cover_topic.py and weak_topics.py.

covered_topics.json lists the spec refs covered so far, by qualification
(their numbering differs) and strand (in each spec the statistics and
mechanics topics reuse the pure numbers: statistics 2.1 is not pure 2.1).
A bare topic number covers all of that topic's refs. Strands with nothing
covered can be left out:
    {"9MA0": {"pure": ["1", "2", "7.1", "7.2"], "statistics": ["1"]},
     "8MA0": {"pure": ["2", "7.1"]}}
"""

import json
import re

from paths import ROOT

COVERED = ROOT / "bank" / "covered_topics.json"
TOPICS = ROOT / "schemas" / "topics.json"
QUALIFICATIONS = ("9MA0", "8MA0")
STRANDS = ("pure", "statistics", "mechanics")

FORMAT_HELP = ('    {"9MA0": {"pure": ["1", "2", "7.1", "7.2"], "statistics": ["1"]},\n'
               '     "8MA0": {"pure": ["2", "7.1"]}}\n'
               "A bare topic number covers all of that topic's refs.")


def load_topics():
    return json.loads(TOPICS.read_text(encoding="utf-8"))["topics"]


def spec_refs(topics, qual, strand):
    """{topic number: [refs]} for one qualification's strand, in spec order."""
    return {str(t[qual]["topic_number"]): list(t[qual]["refs"])
            for t in topics if t["strand"] == strand and t.get(qual)}


def ref_topic(topics, qual, strand, ref):
    """The topics.json topic that a ref (or bare topic number) belongs to, or None."""
    for t in topics:
        if t["strand"] == strand and t.get(qual):
            if ref == str(t[qual]["topic_number"]) or ref in t[qual]["refs"]:
                return t
    return None


def strand_of(topics):
    """{topic name: strand}."""
    return {t["name"]: t["strand"] for t in topics}


def ref_sort_key(ref):
    """'10.2' after '9.1', and a bare topic number before its refs."""
    return [int(n) for n in ref.split(".")]


def read_covered(path=COVERED):
    """The file as written ({qual: {strand: [items]}}), or {} if it doesn't exist."""
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_covered(path, topics):
    """{(qualification, strand): set of covered refs}, with topic numbers expanded."""
    if not path.exists():
        raise SystemExit(f"{path} not found. Create it with the spec refs covered so far "
                         f"(scripts/cover_topic.py does this), e.g.\n{FORMAT_HELP}")
    covered = {}
    for qual, strands in read_covered(path).items():
        if qual not in QUALIFICATIONS or not isinstance(strands, dict):
            raise SystemExit(f"{path.name}: expected {{\"9MA0\"|\"8MA0\": {{strand: [refs]}}}}, got {qual!r}")
        for strand, items in strands.items():
            by_topic = spec_refs(topics, qual, strand)
            if not by_topic:
                raise SystemExit(f"{path.name}: {qual} has no strand {strand!r} (use pure, statistics, mechanics)")
            known = {ref for refs in by_topic.values() for ref in refs}
            refs = covered.setdefault((qual, strand), set())
            for item in items:
                if item in by_topic:
                    refs.update(by_topic[item])
                elif item in known:
                    refs.add(item)
                else:
                    raise SystemExit(f"{path.name}: {item!r} is not a {qual} {strand} topic number or spec ref")
    return covered


def main_ref(entry):
    """An entry's main spec ref: the first in its comma-separated spec_ref."""
    return entry["spec_ref"].split(",")[0].strip()


def real_id(question_id):
    """A generated variant's real question: '..._Q05b-A' -> '..._Q05b'."""
    return re.sub(r"-[ABC]$", "", question_id.strip())
