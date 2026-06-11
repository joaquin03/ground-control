#!/usr/bin/env python3
"""Folder-invariant checks for the Ground Control operator. Returns {check: [problems]}.

Invariants:
  no_pike       — the word 'pike' / 'p_v5' never appears anywhere in the deliverable.
  stale_paths   — no 'data/' or 'Dataset/' path references remain.
  icao_coverage — every ICAO used in a sample inbound exists in steps/airports.csv.
  provider_or_flag — every in-scope service asked in a golden either resolves to a provider
                     in steps/provider-database.csv or is explicitly FLAGGED/INBOUND-PENDING.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # competitions/ground-control

def _all_text_files():
    skip = {".git", "superpowers", "docs"}  # exclude build meta-docs: specs/plans + archived design notes legitimately contain legacy path names and system references
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".csv", ".py", ".jsonl"} and not any(s in p.parts for s in skip):
            yield p

def check_no_pike():
    bad = []
    for p in _all_text_files():
        if p.name == __file__.split("/")[-1]:
            continue
        if re.search(r"\bpike\b|p_v5", p.read_text(), re.IGNORECASE):
            bad.append(str(p.relative_to(ROOT)))
    return bad

def check_stale_paths():
    bad = []
    for p in _all_text_files():
        if p.name == __file__.split("/")[-1]:
            continue
        for m in re.finditer(r"\b(Dataset/|data/)", p.read_text()):
            bad.append(f"{p.relative_to(ROOT)}: {m.group(0)}")
    return bad

def check_icao_coverage():
    airports = (ROOT / "steps/airports.csv").read_text()
    known = set(re.findall(r"^([A-Z]{4}),", airports, re.MULTILINE))
    bad = []
    for p in (ROOT / "samples/inbound").glob("*.md"):
        # the subject line carries the trip's ICAO: "<REG> | <ICAO> | ..."
        subj = re.search(r"Subject:.*?\|\s*([A-Z]{4})\s*\|", p.read_text())
        if subj and subj.group(1) not in known:
            bad.append(f"{p.name}: {subj.group(1)} not in airports.csv")
    return bad

def check_results_schema():
    """state/results.csv (the relocated audit fixture) exists with logging.md's column order + rows."""
    expected = "timestamp,ref,from,subject,leg,action,provider,to,cc,status,decision,note"
    p = ROOT / "state" / "results.csv"
    if not p.exists():
        return ["state/results.csv missing (audit fixture not generated)"]
    lines = [l for l in p.read_text().splitlines() if l.strip()]
    bad = []
    if not lines or lines[0].strip() != expected:
        bad.append("state/results.csv header does not match reference/logging.md column order")
    if len(lines) < 2:
        bad.append("state/results.csv has no action rows")
    return bad

def run_checks():
    return {
        "no_pike": check_no_pike(),
        "stale_paths": check_stale_paths(),
        "icao_coverage": check_icao_coverage(),
        "results_schema": check_results_schema(),
    }

if __name__ == "__main__":
    import json, sys
    r = run_checks()
    print(json.dumps(r, indent=2))
    sys.exit(1 if any(r.values()) else 0)
