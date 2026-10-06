"""Find and download Edexcel A-level Maths (9MA0) past papers and reference files.

Usage (from the project root, with the venv active):
    python scripts/fetch_materials.py              # plan only: print what would be fetched
    python scripts/fetch_materials.py --download   # download, then write log/missing.csv

Sources, in order of preference for each paper/series/type:
  1. Pearson, but only files Pearson lists as public. Anything Pearson tags
     as secure content (teacher login) is never downloaded from Pearson.
  2. Physics & Maths Tutor (PMT), for question papers and mark schemes.
Anything neither source can supply goes into log/missing.csv.

Files for RESERVED_SERIES go into source/reserved/ (my mock papers). This
script only writes there; it never opens, reads or lists that folder. The
only thing it checks is whether a file it is about to write already exists.

If a site refuses scripted downloads (HTTP 401/403/429), the script stops
straight away instead of retrying or working around it.
"""

import argparse
import csv
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

from naming import FILENAME_RE, TYPE_FOLDERS
from paths import ROOT

SOURCE_DIR = ROOT / "source"
MISSING_CSV = ROOT / "log" / "missing.csv"

# The three most recent June series available when this was set up
# (2026-10). Fixed on purpose rather than worked out each run: if it moved
# forward automatically, an old mock series would land in source/papers/
# the next time a new series came out. Keep in sync with CLAUDE.md.
RESERVED_SERIES = {"2023-06", "2024-06", "2025-06"}

FIRST_YEAR = 2018
DELAY_SECONDS = 1
USER_AGENT = "9MA0-question-bank/1.0 (personal study script; python-requests)"

PMT_PAGE = "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/papers/"

# Pearson's course-materials page fills its file list from this Algolia
# search index. The app id and key are the public, search-only values
# embedded in that page; they can only read the public listing.
PEARSON_HOST = "https://qualifications.pearson.com"
ALGOLIA_URL = "https://L639T95U5A-dsn.algolia.net/1/indexes/qualifications-uk_LIVE_master-content/query"
ALGOLIA_HEADERS = {
    "X-Algolia-Application-Id": "L639T95U5A",
    "X-Algolia-API-Key": "f79c7a8352e9ffbdaec387bf43612ee6",
}
ALGOLIA_FILTERS = [
    ["category:Pearson-UK:Specification-Code/maths-2017-as-al"],
]

# Reference files: (file name in Pearson's index, name to save as).
REFERENCE_FILES = [
    ("a-level-l3-mathematics-specification-issue4.pdf", "9MA0_specification.pdf"),
    ("pearson-edexcel-a-level-gce-in-mathematics-formulae-book.pdf",
     "mathematical-formulae-and-statistical-tables.pdf"),
    ("Pearson Edexcel GCE AS and AL Mathematics data set - Issue 1 (1).xls", "large-data-set.xls"),
]

MONTHS = {"January": "01", "June": "06", "October": "10", "November": "11"}

# Pearson calls the autumn 2021 series "November 2021", but the papers were
# sat in October 2021 and PMT lists them as October. Use one name for both.
SERIES_ALIASES = {"2021-11": "2021-10"}

PEARSON_TYPES = {
    "Question-paper": "QP",
    "Mark-scheme": "MS",
    "Examiner-report": "ER",
}


class Blocked(Exception):
    """A site refused a scripted request. We stop rather than work around it."""


def http_get(session, url, **kwargs):
    response = session.get(url, timeout=60, **kwargs)
    if response.status_code in (401, 403, 429):
        raise Blocked(f"{response.status_code} from {url}")
    return response


def series_from_words(month, year):
    """("June", "2019") -> "2019-06", with the November 2021 alias applied."""
    series = f"{year}-{MONTHS[month]}"
    return SERIES_ALIASES.get(series, series)


def papers_for_series(series):
    """Paper codes sat in a series. Paper 3 split into 31 and 32 from 2019."""
    if series in ("SAM", "SPEC", "2018-06"):
        return ["01", "02", "03"]
    return ["01", "02", "31", "32"]


def types_for_series(series):
    """No examiner reports exist for the sample or specimen sets."""
    return ["QP", "MS"] if series in ("SAM", "SPEC") else ["QP", "MS", "ER"]


# ---------------------------------------------------------------- listing

def list_pmt(session):
    """Return {(paper, series, type): url} for every 9MA0 QP/MS PMT links to."""
    html = http_get(session, PMT_PAGE).text
    soup = BeautifulSoup(html, "html.parser")
    found = {}
    for link in soup.find_all("a", href=True):
        # e.g. .../Edexcel/Paper-3/MS/June 2019 MS (Stats).pdf
        match = re.search(r"/Edexcel/Paper-([123])/(QP|MS)/([^/]+)\.pdf$", link["href"])
        if not match:
            continue
        paper_number, doc_type, name = match.groups()

        dated = re.fullmatch(r"(\w+) (\d{4}) (?:QP|MS)(?: \((Mech|Stats)\))?", name)
        early = re.fullmatch(r"(Sample|Specimen) (?:QP|MS)", name)
        if dated:
            month, year, section = dated.groups()
            if int(year) < FIRST_YEAR or month not in MONTHS:
                continue
            series = series_from_words(month, year)
        elif early:
            series = "SAM" if early.group(1) == "Sample" else "SPEC"
            section = None
        else:
            continue

        # PMT keeps the split Paper 3 under Paper-3 with a (Stats)/(Mech) suffix.
        paper = {"Stats": "31", "Mech": "32"}.get(section, f"0{paper_number}")
        found[(paper, series, doc_type)] = link["href"]
    return found


def query_pearson(session):
    """All hits in Pearson's index for the 2017 maths specification."""
    hits, page = [], 0
    while True:
        body = {
            "query": "",
            "hitsPerPage": 500,
            "page": page,
            "facetFilters": ALGOLIA_FILTERS,
            "attributesToRetrieve": ["title", "url", "category"],
            "attributesToHighlight": [],
        }
        response = session.post(ALGOLIA_URL, headers=ALGOLIA_HEADERS, json=body, timeout=60)
        if response.status_code in (401, 403, 429):
            raise Blocked(f"{response.status_code} from Pearson's search index")
        response.raise_for_status()
        data = response.json()
        hits.extend(data["hits"])
        page += 1
        if page >= data["nbPages"]:
            return hits


def is_secure(hit):
    return any("secure-content" in c for c in hit["category"])


def category_value(hit, prefix):
    """Last part of the first category starting with prefix, or None."""
    for c in hit["category"]:
        if c.startswith(prefix):
            return c.rsplit("/", 1)[-1]
    return None


def list_pearson(hits):
    """Return {(paper, series, type): (url, secure)} for 9MA0 exam materials."""
    found = {}
    for hit in hits:
        filename = hit["url"].rsplit("/", 1)[-1]
        # e.g. 9ma0-01-que-2018.pdf, 9MA0_31_pef_20190815.pdf. Skip zips and
        # the "modified" (accessibility) versions.
        match = re.match(r"9ma0[-_](0[1-3]|3[12])[-_]", filename, re.IGNORECASE)
        if not match or not filename.lower().endswith(".pdf") or "modified" in filename.lower():
            continue
        doc_type = PEARSON_TYPES.get(category_value(hit, "Pearson-UK:Document-Type/"))
        series_tag = category_value(hit, "Pearson-UK:Exam-Series/")  # e.g. June-2019
        if not doc_type or not series_tag:
            continue
        month, year = series_tag.split("-")
        if int(year) < FIRST_YEAR or month not in MONTHS:
            continue
        key = (match.group(1), series_from_words(month, year), doc_type)
        # If Pearson lists two versions, keep a public one over a secure one.
        if key not in found or (found[key][1] and not is_secure(hit)):
            found[key] = (PEARSON_HOST + hit["url"], is_secure(hit))
    return found


def pearson_reference(hits):
    """Return {pearson file name: (url, secure)} for the reference files we want."""
    wanted = {name for name, _ in REFERENCE_FILES}
    found = {}
    for hit in hits:
        filename = hit["url"].rsplit("/", 1)[-1]
        if filename in wanted:
            found[filename] = (PEARSON_HOST + hit["url"], is_secure(hit))
    return found


# ---------------------------------------------------------------- planning

def build_plan(pmt, pearson, reference):
    """Work out, for every expected file, where it comes from or why it can't.

    Returns (planned, missing):
      planned: list of dicts with dest (Path), url, source and slot details
      missing: list of dicts with paper, series, type, reason
    """
    all_series = {key[1] for key in pmt} | {key[1] for key in pearson}
    planned, missing = [], []

    for series in sorted(all_series):
        for paper in papers_for_series(series):
            for doc_type in types_for_series(series):
                key = (paper, series, doc_type)
                filename = f"9MA0-{paper}_{series}_{doc_type}.pdf"
                assert FILENAME_RE.match(filename), filename
                folder = "reserved" if series in RESERVED_SERIES else TYPE_FOLDERS[doc_type]
                slot = {"paper": f"9MA0-{paper}", "series": series, "type": doc_type}

                pearson_entry = pearson.get(key)
                if pearson_entry and not pearson_entry[1]:
                    planned.append({**slot, "dest": SOURCE_DIR / folder / filename,
                                    "url": pearson_entry[0], "source": "Pearson"})
                elif key in pmt:
                    planned.append({**slot, "dest": SOURCE_DIR / folder / filename,
                                    "url": pmt[key], "source": "PMT"})
                else:
                    if pearson_entry:
                        reason = "Pearson: secure (login only)"
                    else:
                        reason = "Pearson: not listed"
                    reason += "; PMT: no examiner reports" if doc_type == "ER" else "; PMT: not listed"
                    missing.append({**slot, "reason": reason})

    for pearson_name, save_as in REFERENCE_FILES:
        entry = reference.get(pearson_name)
        slot = {"paper": "reference", "series": "", "type": save_as}
        if entry and not entry[1]:
            planned.append({**slot, "dest": SOURCE_DIR / "reference" / save_as,
                            "url": entry[0], "source": "Pearson"})
        else:
            reason = "Pearson: secure (login only)" if entry else "Pearson: not listed"
            missing.append({**slot, "reason": reason})

    return planned, missing


# ---------------------------------------------------------------- output

def relative(path):
    return path.relative_to(ROOT).as_posix()


def print_plan(planned, missing):
    print(f"{'DESTINATION':58} SOURCE   URL")
    for item in planned:
        print(f"{relative(item['dest']):58} {item['source']:8} {item['url']}")
    print(f"\n{len(planned)} files planned, {len(missing)} slots missing.")


def print_coverage(planned, missing):
    """Grid of series x paper. Each cell shows QP, MS, ER in that order:
    a letter when the file is planned or on disk, '.' when missing,
    and a blank when that type doesn't exist for the series."""
    have = {(i["paper"], i["series"], i["type"]) for i in planned}
    gone = {(m["paper"], m["series"], m["type"]) for m in missing}
    papers = ["01", "02", "03", "31", "32"]
    series_list = sorted({s for _, s, _ in have | gone if s})

    print("\nCoverage (Q = question paper, M = mark scheme, E = examiner report, . = missing)")
    print(f"{'series':10}" + "".join(f"9MA0-{p:<6}" for p in papers))
    for series in series_list:
        cells = []
        for paper in papers:
            if paper not in papers_for_series(series):
                cells.append(f"{'':11}")
                continue
            cell = ""
            for doc_type, letter in (("QP", "Q"), ("MS", "M"), ("ER", "E")):
                key = (f"9MA0-{paper}", series, doc_type)
                cell += letter if key in have else "." if key in gone else " "
            cells.append(f"{cell:11}")
        note = "  (reserved)" if series in RESERVED_SERIES else ""
        print(f"{series:10}" + "".join(cells) + note)

    ref_missing = [m for m in missing if m["paper"] == "reference"]
    print(f"reference: {3 - len(ref_missing)}/3 available")


def write_missing(missing):
    MISSING_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(MISSING_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["paper", "series", "type", "reason"])
        writer.writeheader()
        writer.writerows(missing)


# ---------------------------------------------------------------- download

def looks_right(response, dest):
    """Reject HTML error pages served with a 200 status."""
    content_type = response.headers.get("Content-Type", "").lower()
    if dest.suffix == ".pdf":
        return "pdf" in content_type or "octet-stream" in content_type
    return "html" not in content_type


def download_all(session, planned, missing):
    """Download each planned file that isn't already on disk.

    Files that fail are moved from planned into missing, so the coverage
    grid and missing.csv show what actually arrived.
    """
    downloaded = skipped = 0
    first = True
    for item in list(planned):
        dest = item["dest"]
        if dest.exists():
            skipped += 1
            continue

        if not first:
            time.sleep(DELAY_SECONDS)
        first = False

        response = http_get(session, item["url"], stream=True)
        if response.status_code != 200 or not looks_right(response, dest):
            reason = f"{item['source']}: HTTP {response.status_code} {response.headers.get('Content-Type', '')}"
            print(f"  FAILED {relative(dest)}: {reason}")
            planned.remove(item)
            missing.append({k: item[k] for k in ("paper", "series", "type")} | {"reason": reason})
            continue

        # Write to a .part file first, so an interrupted download never
        # leaves a half-written file that "skip if exists" would trust.
        dest.parent.mkdir(parents=True, exist_ok=True)
        partial = dest.with_name(dest.name + ".part")
        with open(partial, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                f.write(chunk)
        partial.replace(dest)
        downloaded += 1
        print(f"  saved {relative(dest)}")

    print(f"\nDownloaded {downloaded}, skipped {skipped} already present.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--download", action="store_true",
                        help="download the planned files (default: only show the plan)")
    args = parser.parse_args()

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    try:
        pmt = list_pmt(session)
        time.sleep(DELAY_SECONDS)
        hits = query_pearson(session)
        planned, missing = build_plan(pmt, list_pearson(hits), pearson_reference(hits))

        if not args.download:
            print_plan(planned, missing)
            print_coverage(planned, missing)
            print("\nPlan only. Run with --download to fetch these files.")
            return 0

        download_all(session, planned, missing)
    except Blocked as exc:
        print(f"\nSTOPPED: a site refused a scripted request ({exc}).")
        print("Not retrying or working around it. Nothing further was downloaded.")
        return 2

    write_missing(missing)
    print_coverage(planned, missing)
    print(f"\nMissing list written to {relative(MISSING_CSV)} ({len(missing)} rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
