#!/usr/bin/env python3
"""Regression harness for Ground Control.

Usage:
  python3 run_eval.py --list                 # list case ids
  python3 run_eval.py <file.md>              # check one capture/golden
  python3 run_eval.py --check <dir>          # check every *.md in dir (exit 1 on any FAIL)
"""
import sys, json
from pathlib import Path
from headers import parse_header
from differ import diff_case
from cardbody import check_card_body

HERE = Path(__file__).parent

def load_cases():
    cases = {}
    for line in (HERE / "cases.jsonl").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            c = json.loads(line)
            cases[c["id"]] = c
    return cases

def case_id_for(path, header):
    if header.get("case"):
        return header["case"]
    return path.stem[:-7] if path.stem.endswith("-OUTPUT") else path.stem

def check_file(path, cases):
    text = path.read_text()
    h = parse_header(text)
    cid = case_id_for(path, h)
    case = cases.get(cid)
    if not case:
        print(f"  ?? {path.name}: no case for id '{cid}'")
        return False
    fails = diff_case(case, h)
    body_problems = check_card_body(h, text)
    if fails or body_problems:
        print(f"  FAIL {cid}")
        for field, exp, act in fails:
            print(f"       {field}: expected {exp!r} got {act!r}")
        for p in body_problems:
            print(f"       body: {p}")
        return False
    guards = ", ".join(case.get("guards", []))
    print(f"  PASS {cid}   (soft: {guards})")
    return True

def main(argv):
    cases = load_cases()
    if not argv or argv[0] == "--list":
        for cid in sorted(cases):
            print(cid)
        return 0
    if argv[0] == "--check":
        d = Path(argv[1])
        files = sorted(d.glob("*.md"))
        ok = all([check_file(f, cases) for f in files])
        print(f"\n{'ALL PASS' if ok else 'FAILURES PRESENT'} — {len(files)} files, {len(cases)} cases")
        return 0 if ok else 1
    return 0 if check_file(Path(argv[0]), cases) else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
