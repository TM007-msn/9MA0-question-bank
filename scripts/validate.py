"""Validate every bank file against its JSON Schema and list entries with null fields.

Usage (from the project root, with the venv active):
    python scripts/validate.py

Exit code is 0 if every file is valid, 1 otherwise. Null fields are reported
but do not count as failures, because "unknown means null" is allowed.
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
BANK_DIR = ROOT / "bank"

# Which schema each bank file follows. Array files are checked entry by entry;
# progress.json is a single object.
BANK_FILES = {
    "questions.json": "question.schema.json",
    "errors.json": "error.schema.json",
    "generated.json": "generated.schema.json",
    "rejected.json": "generated.schema.json",
    "progress.json": "progress.schema.json",
}


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
    for path in SCHEMA_DIR.glob("*.schema.json"):
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


def check_file(filename, schema, registry):
    """Return (errors, null_report) for one bank file."""
    path = BANK_DIR / filename
    errors = []
    null_report = []

    if not path.exists():
        return [f"missing file {path.relative_to(ROOT)}"], []
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        return [f"not valid JSON: {exc}"], []

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

        # Duplicate ids are not something JSON Schema can catch on its own.
        entry_id = entry.get("id") if isinstance(entry, dict) else None
        if entry_id:
            if entry_id in seen_ids:
                errors.append(f"{label}: duplicate id")
            seen_ids.add(entry_id)

        # Project rule: generated.json only holds questions that passed
        # verification. Failed ones belong in rejected.json.
        if filename == "generated.json" and isinstance(entry, dict):
            if entry.get("verified") is not True or not entry.get("verified_on"):
                errors.append(
                    f"{label}: generated.json entries need verified=true and a verified_on date"
                )

        nulls = null_fields(entry)
        if nulls:
            null_report.append(f"{label}: {', '.join(nulls)}")

    return errors, null_report


def main():
    registry, schemas = build_registry()
    any_errors = False

    for filename, schema_name in BANK_FILES.items():
        errors, nulls = check_file(filename, schemas[schema_name], registry)
        status = "FAIL" if errors else "ok"
        print(f"{filename:<16} {status}")
        for message in errors:
            print(f"    error: {message}")
        if nulls:
            print(f"    {len(nulls)} entr{'y' if len(nulls) == 1 else 'ies'} with null fields:")
            for message in nulls:
                print(f"      {message}")
        any_errors = any_errors or bool(errors)

    return 1 if any_errors else 0


if __name__ == "__main__":
    sys.exit(main())
