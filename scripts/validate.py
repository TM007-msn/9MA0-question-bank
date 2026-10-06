"""Validate every bank file against its JSON Schema and list entries with null fields.

Also checks that PDFs in source/papers, source/mark-schemes and
source/examiner-reports follow the naming rule. It never looks inside
source/reserved/ (or source/inbox/, which holds unfiled downloads).

Usage (from the project root, with the venv active):
    python scripts/validate.py

Exit code is 0 if everything is valid, 1 otherwise. Null fields are reported
but do not count as failures, because "unknown means null" is allowed.
"""

import json
import re
import sys

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from naming import FILENAME_RE, TYPE_FOLDERS, id_prefix
from paths import ROOT

SCHEMA_DIR = ROOT / "schemas"
BANK_DIR = ROOT / "bank"
SOURCE_DIR = ROOT / "source"

# Which schema each bank file follows. Array files are checked entry by entry;
# progress.json is a single object.
BANK_FILES = {
    "questions.json": "question.schema.json",
    "errors.json": "error.schema.json",
    "generated.json": "generated.schema.json",
    "rejected.json": "rejected.schema.json",
    "progress.json": "progress.schema.json",
}

# Files whose entries are questions (real or generated) and so carry an id,
# paper and series that must agree with each other.
QUESTION_FILES = {"questions.json", "generated.json", "rejected.json"}
GENERATED_FILES = {"generated.json", "rejected.json"}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_registry():
    """Register every schema under both its $id and its bare filename.

    generated.schema.json refers to "question.schema.json#/$defs/core". That
    relative reference resolves against generated's $id, so the full $id URI
    is what actually gets looked up. Registering the filename as well keeps
    the lookup working if someone drops the $id later.
    """
    registry = Registry()
    schemas = {}
    # *.schema.json plus topics.json, which the question and error schemas
    # reference for the topic enum. (spec_labels.json is data, not a schema.)
    for path in [*SCHEMA_DIR.glob("*.schema.json"), SCHEMA_DIR / "topics.json"]:
        schema = load_json(path)
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(path.name, resource)
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], resource)
        schemas[path.name] = schema
    return registry, schemas


def entry_label(entry, index):
    """A readable name for an entry in messages: its id if it has one."""
    if isinstance(entry, dict) and entry.get("id"):
        return entry["id"]
    if isinstance(entry, dict) and entry.get("topic"):
        return f"[{index}] {entry['topic']}"
    return f"[{index}]"


def null_fields(entry):
    """Top-level keys whose value is null."""
    if not isinstance(entry, dict):
        return []
    return [key for key, value in entry.items() if value is None]


def load_topics():
    """{topic name: topic} from schemas/topics.json."""
    return {t["name"]: t for t in load_json(SCHEMA_DIR / "topics.json")["topics"]}


TOPICS = load_topics()

# A figure description in question_latex starts "[Figure", e.g.
# "[Figure 2: sketch of ...]". Other square-bracket text (e.g. a printed
# "[In this question i and j are ...]") does not count.
FIGURE_RE = re.compile(r"\[Figure\b")

# SPEC combined papers whose sections are filed under the split paper codes:
# entries for these papers may point at the combined source_file.
SPEC_SPLITS = {"9MA0-31": "9MA0-03", "9MA0-32": "9MA0-03", "8MA0-21": "8MA0-02", "8MA0-22": "8MA0-02"}


def spec_ref_errors(entry):
    """spec_ref refs must exist in the entry's own qualification's spec, in
    the same strand (pure / statistics / mechanics) as its topic, and the
    first ref must belong to the topic itself."""
    topic = TOPICS.get(entry.get("topic"))
    refs_text = entry.get("spec_ref")
    if not topic or not refs_text:
        return []
    qual = entry["paper"].split("-")[0]
    if topic[qual] is None:
        return [f"topic {topic['name']!r} is not in the {qual} specification"]

    same_strand = {}
    for t in TOPICS.values():
        if t["strand"] == topic["strand"] and t[qual]:
            same_strand.update({r: t["name"] for r in t[qual]["refs"]})

    errors = []
    refs = refs_text.split(", ")
    for r in refs:
        if r not in same_strand:
            errors.append(f"spec_ref {r} is not a {qual} {topic['strand']} ref")
    if refs[0] in same_strand and same_strand[refs[0]] != topic["name"]:
        errors.append(f"first spec_ref {refs[0]} belongs to {same_strand[refs[0]]!r}, not the topic {topic['name']!r}")
    return errors


def source_file_errors(entry):
    """source_file must be this entry's own question paper (or, for a SPEC
    section filed under 31/32 or 21/22, the combined paper), and must exist
    in source/papers/. Never looks in source/reserved/."""
    name = entry.get("source_file")
    if not name:
        return []
    match = FILENAME_RE.match(name)
    if not match:
        return [f"source_file {name} doesn't follow the naming rule"]
    errors = []
    paper, series = entry.get("paper"), entry.get("series")
    allowed = {paper}
    if series == "SPEC" and paper in SPEC_SPLITS:
        allowed.add(SPEC_SPLITS[paper])
    if match["paper"] not in allowed or match["series"] != series:
        errors.append(f"source_file {name} doesn't match paper {paper} / series {series}")
    if not (SOURCE_DIR / "papers" / name).exists():
        errors.append(f"source_file {name} not found in source/papers/")
    return errors


def difficulty_errors(entry):
    """A rating needs evidence, and the evidence must be a sentence from
    the entry's own examiner_notes (so it's copied from the report, not
    written by us). No rating means no evidence."""
    rating, evidence = entry.get("difficulty"), entry.get("difficulty_evidence")
    if rating is None and evidence is None:
        return []
    if rating is None:
        return ["difficulty_evidence is set but difficulty is null"]
    if evidence is None:
        return ["difficulty is set but difficulty_evidence is null"]
    if evidence not in (entry.get("examiner_notes") or ""):
        return ["difficulty_evidence is not a sentence from examiner_notes"]
    return []


def consistency_errors(filename, entry):
    """Checks a schema can't express: fields that must agree with each other."""
    errors = []
    if not isinstance(entry, dict):
        return errors
    entry_id = entry.get("id") or ""

    if filename in QUESTION_FILES:
        # A figure described in the question text means the entry has a diagram.
        if FIGURE_RE.search(entry.get("question_latex") or "") and entry.get("has_diagram") is not True:
            errors.append("question_latex describes a [Figure ...] but has_diagram is not true")
        errors.extend(spec_ref_errors(entry))
        errors.extend(source_file_errors(entry))
        errors.extend(difficulty_errors(entry))

    # The id must start with the entry's own paper and series, so an id like
    # 9MA0-01_2023-06_Q03 can't sit on an entry marked paper 9MA0-02.
    if filename in QUESTION_FILES and entry.get("paper") and entry.get("series"):
        prefix = id_prefix(entry["paper"], entry["series"])
        if not entry_id.startswith(prefix):
            errors.append(f"id should start with {prefix} to match paper and series")

    # A generated id is exactly its anchor id plus the variant letter.
    if filename in GENERATED_FILES and entry.get("anchor_id") and entry.get("variant"):
        expected = f"{entry['anchor_id']}-{entry['variant']}"
        if entry_id != expected:
            errors.append(f"id should be {expected} (anchor_id + variant)")

    return errors


def check_file(filename, schema, registry, bank_dir=BANK_DIR):
    """Return (errors, null_report) for one bank file."""
    path = bank_dir / filename
    errors = []
    null_report = []

    if not path.exists():
        return [f"missing file {path}"], []
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        return [f"not valid JSON: {exc}"], []

    # FormatChecker makes "format": "date" an actual check, not just a label.
    validator = Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker()
    )

    if filename == "progress.json":
        # Single object, not a list of entries.
        for err in validator.iter_errors(data):
            errors.append(f"{err.json_path}: {err.message}")
        return errors, null_report

    if not isinstance(data, list):
        return ["top level must be a JSON array"], []

    seen_ids = set()
    for index, entry in enumerate(data):
        label = entry_label(entry, index)

        for err in validator.iter_errors(entry):
            errors.append(f"{label} {err.json_path}: {err.message}")
        for message in consistency_errors(filename, entry):
            errors.append(f"{label}: {message}")

        # Duplicate ids are not something JSON Schema can catch on its own.
        entry_id = entry.get("id") if isinstance(entry, dict) else None
        if entry_id:
            if entry_id in seen_ids:
                errors.append(f"{label}: duplicate id")
            seen_ids.add(entry_id)

        nulls = null_fields(entry)
        if nulls:
            null_report.append(f"{label}: {', '.join(nulls)}")

    return errors, null_report


def check_source_names(source_dir=SOURCE_DIR):
    """Return naming errors for PDFs in the papers / mark-schemes / examiner-reports folders.

    Only the folders named in TYPE_FOLDERS are listed. source/reserved/ is
    never touched.
    """
    errors = []
    for doc_type, folder in TYPE_FOLDERS.items():
        folder_path = source_dir / folder
        if not folder_path.is_dir():
            continue
        for pdf in sorted(folder_path.glob("*.pdf")):
            match = FILENAME_RE.match(pdf.name)
            if not match:
                errors.append(f"{folder}/{pdf.name}: should be PAPER_SERIES_TYPE.pdf, e.g. 9MA0-01_2023-06_{doc_type}.pdf")
            elif match["type"] != doc_type:
                errors.append(f"{folder}/{pdf.name}: {match['type']} files belong in source/{TYPE_FOLDERS[match['type']]}/, not {folder}/")
    return errors


def main(bank_dir=BANK_DIR, source_dir=SOURCE_DIR):
    registry, schemas = build_registry()
    any_errors = False

    for filename, schema_name in BANK_FILES.items():
        errors, nulls = check_file(filename, schemas[schema_name], registry, bank_dir)
        status = "FAIL" if errors else "ok"
        print(f"{filename:<16} {status}")
        for message in errors:
            print(f"    error: {message}")
        if nulls:
            print(f"    {len(nulls)} entr{'y' if len(nulls) == 1 else 'ies'} with null fields:")
            for message in nulls:
                print(f"      {message}")
        any_errors = any_errors or bool(errors)

    name_errors = check_source_names(source_dir)
    print(f"{'source names':<16} {'FAIL' if name_errors else 'ok'}")
    for message in name_errors:
        print(f"    error: {message}")
    any_errors = any_errors or bool(name_errors)

    return 1 if any_errors else 0


if __name__ == "__main__":
    sys.exit(main())
