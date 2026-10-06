"""Find and download Edexcel A-level (9MA0) and AS (8MA0) Maths past papers and reference files.

Usage (from the project root, with the venv active):
    python scripts/fetch_materials.py              # plan only: print what would be fetched
    python scripts/fetch_materials.py --download   # download, then write log/missing.csv

Sources, in order of preference for each paper/series/type:
  1. Pearson, but only files that Pearson's public past-papers page lists
     as downloadable without a login (see is_login_only below).
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

# Series kept back as mock papers, per qualification: the most recent June
# series available when this was set up (2026-10). Fixed on purpose rather
# than worked out each run: if it moved forward automatically, an old mock
# series would land in source/papers/ the next time a new series came out.
# Keep in sync with the "Reserved mocks" table in CLAUDE.md.
RESERVED_SERIES = {
    "9MA0": {"2023-06", "2024-06", "2025-06"},
    "8MA0": {"2025-06"},
}

FIRST_YEAR = 2018
DELAY_SECONDS = 1
USER_AGENT = "9MA0-question-bank/1.0 (personal study script; python-requests)"

# Per qualification: PMT page, PMT folder prefix for each paper, and which
# paper split into Statistics/Mechanics papers from 2019 onwards.
QUALIFICATIONS = {
    "9MA0": {
        "pmt_page": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/papers/",
        "pmt_folder": "Paper-",
        "single_papers": ["01", "02", "03"],  # June 2018, SAM, SPEC
        "split_papers": ["01", "02", "31", "32"],  # 2019 onwards
        "split_from": "3",  # PMT "Paper-3 ... (Stats)" -> 31, "(Mech)" -> 32
    },
    "8MA0": {
        "pmt_page": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/papers-as/",
        "pmt_folder": "AS-Paper-",
        "single_papers": ["01", "02"],
        "split_papers": ["01", "21", "22"],
        "split_from": "2",  # PMT "AS-Paper-2 ... (Stats)" -> 21, "(Mech)" -> 22
    },
}

# Pearson's past-papers and course-materials pages fill their file lists
# from this Algolia search index. The app id and key are the public,
# search-only values embedded in those pages.
PEARSON_HOST = "https://qualifications.pearson.com"
ALGOLIA_URL = "https://L639T95U5A-dsn.algolia.net/1/indexes/qualifications-uk_LIVE_master-content/query"
ALGOLIA_HEADERS = {
    "X-Algolia-Application-Id": "L639T95U5A",
    "X-Algolia-API-Key": "f79c7a8352e9ffbdaec387bf43612ee6",
}
# What the public past-papers page asks the index for when you pick
# A level / AS Mathematics: question papers, mark schemes, examiner reports.
PAST_PAPERS_FILTER = (
    '(category:"Pearson-UK:Qualification-Family/A-Level" OR category:"Pearson-UK:Qualification-Family/AS")'
    ' AND category:"Pearson-UK:Qualification-Subject/Mathematics"'
    ' AND (category:"Pearson-UK:Document-Type/Question-paper"'
    ' OR category:"Pearson-UK:Document-Type/Mark-scheme"'
    ' OR category:"Pearson-UK:Document-Type/Examiner-report")'
)
# The reference files are listed on the course-materials page instead.
REFERENCE_FILTER = 'category:"Pearson-UK:Specification-Code/maths-2017-as-al"'

# Reference files: (file name in Pearson's index, name to save as).
REFERENCE_FILES = [
    ("a-level-l3-mathematics-specification-issue4.pdf", "9MA0_specification.pdf"),
    ("pearson-edexcel-a-level-gce-in-mathematics-formulae-book.pdf",
     "mathematical-formulae-and-statistical-tables.pdf"),
    ("Pearson Edexcel GCE AS and AL Mathematics data set - Issue 1 (1).xls", "large-data-set.xls"),
]

MONTHS = {"January": "01", "June": "06", "October": "10", "November": "11"}

# One name per series, whatever each site calls it:
# - Pearson calls the autumn 2021 series "November 2021" (PMT's AS page does
#   too), but the papers were sat in October 2021.
# - PMT's AS page calls the 2020 series "June 2020", but no exams were sat in
#   June 2020 (COVID); Pearson lists that series as October 2020.
SERIES_ALIASES = {"2021-11": "2021-10", "2020-06": "2020-10"}

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
    """("June", "2019") -> "2019-06", with SERIES_ALIASES applied."""
    series = f"{year}-{MONTHS[month]}"
    return SERIES_ALIASES.get(series, series)


def papers_for_series(qual, series):
    """Paper codes sat in a series. The applied paper split from 2019."""
    config = QUALIFICATIONS[qual]
    if series in ("SAM", "SPEC", "2018-06"):
        return config["single_papers"]
    return config["split_papers"]


def types_for_series(series):
    """No examiner reports exist for the sample or specimen sets."""
    return ["QP", "MS"] if series in ("SAM", "SPEC") else ["QP", "MS", "ER"]


def is_reserved(qual, series):
    return series in RESERVED_SERIES.get(qual, set())


# ---------------------------------------------------------------- listing

def list_pmt(session, qual):
    """Return {(qual, paper, series, type): url} for every QP/MS PMT links to."""
    config = QUALIFICATIONS[qual]
    html = http_get(session, config["pmt_page"]).text
    soup = BeautifulSoup(html, "html.parser")
    folder = re.escape(config["pmt_folder"])
    found = {}
    for link in soup.find_all("a", href=True):
        # e.g. .../Edexcel/Paper-3/MS/June 2019 MS (Stats).pdf
        #      .../Edexcel/AS-Paper-2/QP/November 2021 QP (Mech).pdf
        match = re.search(rf"/Edexcel/{folder}([123])/(QP|MS)/([^/]+)\.pdf$", link["href"])
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

        # PMT files the split paper under one folder with a (Stats)/(Mech)
        # suffix; Pearson numbers them e.g. 31/32 (9MA0) or 21/22 (8MA0).
        if section:
            assert paper_number == config["split_from"], link["href"]
            paper = config["split_from"] + ("1" if section == "Stats" else "2")
        else:
            paper = f"0{paper_number}"
        found[(qual, paper, series, doc_type)] = link["href"]
    return found


def query_pearson(session, filters):
    """All hits in Pearson's index matching an Algolia filter string."""
    hits, page = [], 0
    while True:
        body = {
            "query": "",
            "filters": filters,
            "hitsPerPage": 1000,
            "page": page,
            "attributesToRetrieve": ["title", "url", "id", "category"],
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


def is_login_only(hit):
    """True if Pearson's past-papers page shows this file with a padlock.

    The page's own script sets its "secure" flag (the padlock, "Secure
    download. Centre login required.") only when the file lives under
    /content/dam/secure/. The "secure-content/silver" category tag that many
    public files also carry is not used by the page.
    """
    return any("/content/dam/secure/" in (hit.get(field) or "") for field in ("url", "id"))


def category_value(hit, prefix):
    """Last part of the first category starting with prefix, or None."""
    for c in hit["category"]:
        if c.startswith(prefix):
            return c.rsplit("/", 1)[-1]
    return None


def list_pearson(hits):
    """Return {(qual, paper, series, type): (url, login_only)} for exam materials."""
    found = {}
    for hit in hits:
        filename = hit["url"].rsplit("/", 1)[-1]
        # e.g. 9ma0-01-que-2018.pdf, 9MA0_31_pef_20190815.pdf. One Pearson
        # file is named 8MA0_-21_pef_..., hence [-_]+. Skip zips and the
        # "modified" (accessibility) versions.
        match = re.match(r"([89]MA0)[-_]+(0[1-3]|2[12]|3[12])[-_]", filename, re.IGNORECASE)
        if not match or not filename.lower().endswith(".pdf") or "modified" in filename.lower():
            continue
        qual, paper = match.group(1).upper(), match.group(2)
        if paper not in set(QUALIFICATIONS[qual]["single_papers"]) | set(QUALIFICATIONS[qual]["split_papers"]):
            continue
        doc_type = PEARSON_TYPES.get(category_value(hit, "Pearson-UK:Document-Type/"))
        series_tag = category_value(hit, "Pearson-UK:Exam-Series/")  # e.g. June-2019
        if not doc_type or not series_tag:
            continue
        month, year = series_tag.split("-")
        if int(year) < FIRST_YEAR or month not in MONTHS:
            continue
        key = (qual, paper, series_from_words(month, year), doc_type)
        # If Pearson lists two versions, keep a public one over a login-only one.
        if key not in found or (found[key][1] and not is_login_only(hit)):
            found[key] = (PEARSON_HOST + hit["url"], is_login_only(hit))
    return found


def pearson_reference(hits):
    """Return {pearson file name: (url, login_only)} for the reference files we want."""
    wanted = {name for name, _ in REFERENCE_FILES}
    found = {}
    for hit in hits:
        filename = hit["url"].rsplit("/", 1)[-1]
        if filename in wanted:
            found[filename] = (PEARSON_HOST + hit["url"], is_login_only(hit))
    return found


# ---------------------------------------------------------------- planning

def build_plan(pmt, pearson, reference):
    """Work out, for every expected file, where it comes from or why it can't.

    Returns (planned, missing):
      planned: list of dicts with dest (Path), url, source and slot details
      missing: list of dicts with paper, series, type, reason
    """
    planned, missing = [], []

    for qual in QUALIFICATIONS:
        all_series = {k[2] for k in pmt if k[0] == qual} | {k[2] for k in pearson if k[0] == qual}
        for series in sorted(all_series):
            for paper in papers_for_series(qual, series):
                for doc_type in types_for_series(series):
                    key = (qual, paper, series, doc_type)
                    filename = f"{qual}-{paper}_{series}_{doc_type}.pdf"
                    assert FILENAME_RE.match(filename), filename
                    folder = "reserved" if is_reserved(qual, series) else TYPE_FOLDERS[doc_type]
                    slot = {"paper": f"{qual}-{paper}", "series": series, "type": doc_type}

                    pearson_entry = pearson.get(key)
                    if pearson_entry and not pearson_entry[1]:
                        planned.append({**slot, "dest": SOURCE_DIR / folder / filename,
                                        "url": pearson_entry[0], "source": "Pearson"})
                    elif key in pmt:
                        planned.append({**slot, "dest": SOURCE_DIR / folder / filename,
                                        "url": pmt[key], "source": "PMT"})
                    else:
                        if pearson_entry:
                            reason = "Pearson: centre login required (padlock)"
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
            reason = "Pearson: centre login required (padlock)" if entry else "Pearson: not listed"
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
    """One grid per qualification: series x paper. Each cell shows QP, MS, ER
    in that order: a letter when the file is planned or on disk, '.' when
    missing, and a blank when that type doesn't exist for the series."""
    have = {(i["paper"], i["series"], i["type"]) for i in planned}
    gone = {(m["paper"], m["series"], m["type"]) for m in missing}

    print("\nCoverage (Q = question paper, M = mark scheme, E = examiner report, . = missing)")
    for qual, config in QUALIFICATIONS.items():
        papers = sorted(set(config["single_papers"]) | set(config["split_papers"]))
        series_list = sorted({s for p, s, _ in have | gone if p.startswith(qual)})
        print(f"\n{'series':10}" + "".join(f"{qual}-{p:<6}" for p in papers))
        for series in series_list:
            cells = []
            for paper in papers:
                if paper not in papers_for_series(qual, series):
                    cells.append(f"{'':11}")
                    continue
                cell = ""
                for doc_type, letter in (("QP", "Q"), ("MS", "M"), ("ER", "E")):
                    key = (f"{qual}-{paper}", series, doc_type)
                    cell += letter if key in have else "." if key in gone else " "
                cells.append(f"{cell:11}")
            note = "  (reserved)" if is_reserved(qual, series) else ""
            print(f"{series:10}" + "".join(cells) + note)

    ref_missing = [m for m in missing if m["paper"] == "reference"]
    print(f"\nreference: {len(REFERENCE_FILES) - len(ref_missing)}/{len(REFERENCE_FILES)} available")


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
        pmt = {}
        for qual in QUALIFICATIONS:
            pmt.update(list_pmt(session, qual))
            time.sleep(DELAY_SECONDS)
        pearson = list_pearson(query_pearson(session, PAST_PAPERS_FILTER))
        reference = pearson_reference(query_pearson(session, REFERENCE_FILTER))
        planned, missing = build_plan(pmt, pearson, reference)

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
